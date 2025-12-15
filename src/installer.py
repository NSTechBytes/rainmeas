import os
import json
import shutil
import sys
import urllib.request
import zipfile
import tempfile
from typing import Dict, Any, Optional, Set

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Dynamic imports to handle PyInstaller
def import_modules():
    """Dynamically import modules to handle PyInstaller bundling"""
    try:
        import registry
        import utils
        return registry, utils
    except ImportError:
        # Try alternative import paths for PyInstaller
        sys.path.append(resource_path('src'))
        import registry
        import utils
        return registry, utils

# Import modules
try:
    registry, utils = import_modules()
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class Installer:
    def __init__(self, skin_root: str, registry: registry.Registry):
        self.skin_root = skin_root
        self.registry = registry
        self.modules_dir = os.path.join(skin_root, "@Resources", "@rainmeas-modules")
        # Track installed packages to avoid circular dependencies
        self._installed_packages: Set[str] = set()
    
    def install_package(self, package_name: str, version: str = "latest") -> bool:
        """Install a package and its dependencies"""
        # Check for circular dependency
        if package_name in self._installed_packages:
            print(f"Skipping {package_name} (already installed in this session)")
            return True
            
        # Get package info from registry
        package_info = self.registry.get_package_info(package_name)
        if not package_info:
            print(f"Package '{package_name}' not found in registry")
            return False
        
        # Resolve version
        if version == "latest":
            version = self.registry.get_latest_version(package_name)
            if not version:
                print(f"Could not determine latest version for package '{package_name}'")
                return False
        
        # Check if version exists
        available_versions = self.registry.get_available_versions(package_name)
        if version not in available_versions:
            print(f"Version '{version}' not found for package '{package_name}'")
            print(f"Available versions: {', '.join(available_versions)}")
            return False
        
        # Get download URL
        download_url = self.registry.get_version_download_url(package_name, version)
        if not download_url:
            print(f"No download URL found for {package_name}@{version}")
            return False
        
        # Check for dependencies and install them first
        dependencies = self._get_package_dependencies(package_info, version)
        if dependencies:
            print(f"Found dependencies for {package_name}@{version}:")
            for dep_name, dep_version in dependencies.items():
                print(f"  Installing dependency: {dep_name}@{dep_version}")
                if not self.install_package(dep_name, dep_version):
                    print(f"Failed to install dependency {dep_name}@{dep_version}")
                    return False
        
        # Mark as being installed to prevent circular dependencies
        self._installed_packages.add(package_name)
        
        # Create modules directory if it doesn't exist
        os.makedirs(self.modules_dir, exist_ok=True)
        
        # Download and extract package
        print(f"Installing {package_name}@{version}...")
        print(f"Download URL: {download_url}")
        
        # Create a temporary file for the downloaded ZIP
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            tmp_filename = tmp_file.name
        
        try:
            # Download the ZIP file
            print("Downloading package...")
            urllib.request.urlretrieve(download_url, tmp_filename)
            
            # Extract the ZIP file to the package directory
            print("Extracting package...")
            package_dir = os.path.join(self.modules_dir, package_name)
            
            # Remove existing package directory if it exists
            if os.path.exists(package_dir):
                shutil.rmtree(package_dir)
            
            # Extract ZIP file
            with zipfile.ZipFile(tmp_filename, 'r') as zip_ref:
                zip_ref.extractall(package_dir)
            
            # Clean up temporary file
            os.unlink(tmp_filename)
            
            print("Package downloaded and extracted successfully")
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
                os.unlink(tmp_filename)
            
            print(f"Error downloading or extracting package: {e}")
            return False
        
        # Update rainmeas config
        self._update_config(package_name, version)
        
        print(f"Successfully installed {package_name}@{version}")
        return True
    
    def _get_package_dependencies(self, package_info: Dict[str, Any], version: str) -> Dict[str, str]:
        """Get dependencies for a specific package version"""
        versions = package_info.get("versions", {})
        
        # Check if dependencies are defined at the versions level (same level as version keys)
        return versions.get("dependencies", {})
    
    def remove_package(self, package_name: str) -> bool:
        """Remove a package"""
        # Check if package is installed
        installed_packages = self._get_installed_packages()
        if package_name not in installed_packages:
            print(f"Package '{package_name}' is not installed")
            return False
        
        # Remove package directory
        package_dir = os.path.join(self.modules_dir, package_name)
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
            print(f"Removed package directory: {package_dir}")
        
        # Update rainmeas config
        self._remove_from_config(package_name)
        
        print(f"Successfully removed {package_name}")
        return True
    
    def _get_installed_packages(self) -> Dict[str, str]:
        """Get installed packages from config"""
        config = utils.load_rainmeas_config(self.skin_root)
        return config.get("packages", {})
    
    def _update_config(self, package_name: str, version: str) -> None:
        """Update rainmeas config with installed package"""
        config = utils.load_rainmeas_config(self.skin_root)
        
        if "packages" not in config:
            config["packages"] = {}
        
        config["packages"][package_name] = version
        
        utils.save_rainmeas_config(self.skin_root, config)
    
    def _remove_from_config(self, package_name: str) -> None:
        """Remove package from rainmeas config"""
        config = utils.load_rainmeas_config(self.skin_root)
        
        if "packages" in config and package_name in config["packages"]:
            del config["packages"][package_name]
        
        utils.save_rainmeas_config(self.skin_root, config)
    
    def list_installed_packages(self) -> Dict[str, str]:
        """List all installed packages"""
        return self._get_installed_packages()
    
    def install_all_packages(self, packages: Dict[str, str]) -> bool:
        """Install all packages with dependency handling"""
        success_count = 0
        fail_count = 0
        
        print("Installing packages with dependency resolution...")
        
        # Reset the installed packages tracker for this session
        self._installed_packages.clear()
        
        for package_name, version in packages.items():
            # Handle @latest version specifier
            if version == "@latest":
                result = self.install_package(package_name, "latest")
            else:
                result = self.install_package(package_name, version)
            
            if result:
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\nInstallation summary: {success_count} succeeded, {fail_count} failed")
        return fail_count == 0
