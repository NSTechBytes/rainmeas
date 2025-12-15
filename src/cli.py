import sys
import argparse
from typing import List
import os
import json
import shutil

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
        import installer
        import utils
        return registry, installer, utils
    except ImportError:
        # Try alternative import paths for PyInstaller
        sys.path.append(resource_path('src'))
        import registry
        import installer
        import utils
        return registry, installer, utils

# Import modules
try:
    registry, installer, utils = import_modules()
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class RainmeasCLI:
    def __init__(self):
        # Use remote registry only
        self.registry = registry.Registry()
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we initialize without checking
        self.skin_root = os.getcwd()  # Use current directory as default
        self.installer = installer.Installer(self.skin_root, self.registry)
    
    def run(self, args: List[str]) -> int:
        # Get application version
        app_version = utils.get_app_version()
        
        parser = argparse.ArgumentParser(
            prog="rainmeas",
            description="Rainmeas CLI for managing Rainmeter module packages"
        )
        
        # Add version argument to main parser
        parser.add_argument("-v", "--version", action="version", version=f"rainmeas {app_version}")
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Init command
        init_parser = subparsers.add_parser("init", help="Initialize Rainmeas in a Rainmeter modules directory")
        
        # Install command
        install_parser = subparsers.add_parser("install", help="Install a package or all packages from rainmeas-package.json")
        install_parser.add_argument("package", nargs="?", help="Package name and optional version (e.g., nurashadeweather or nurashadeweather@1.1.0). If omitted, installs all packages from rainmeas-package.json in current directory.")
        
        # Alias for install command
        i_parser = subparsers.add_parser("i", help="Install a package or all packages from rainmeas-package.json (alias for install)")
        i_parser.add_argument("package", nargs="?", help="Package name and optional version (e.g., nurashadeweather or nurashadeweather@1.1.0). If omitted, installs all packages from rainmeas-package.json in current directory.")
        
        # Remove command
        remove_parser = subparsers.add_parser("remove", help="Remove a package")
        remove_parser.add_argument("package", help="Package name to remove")
        
        # Update command
        update_parser = subparsers.add_parser("update", help="Update packages")
        update_parser.add_argument("package", nargs="?", help="Specific package to update (optional)")
        
        # List command
        list_parser = subparsers.add_parser("list", help="List installed packages")
        
        # Search command
        search_parser = subparsers.add_parser("search", help="Search for packages")
        search_parser.add_argument("query", help="Search query")
        
        # Info command
        info_parser = subparsers.add_parser("info", help="Show package information")
        info_parser.add_argument("package", help="Package name")
        
        # Verify command
        verify_parser = subparsers.add_parser("verify", help="Verify package integrity")
        
        # Clean command
        clean_parser = subparsers.add_parser("clean", help="Clean unused modules")
        
        # Version command
        version_parser = subparsers.add_parser("version", help="Show CLI version")
        
        # Help command
        help_parser = subparsers.add_parser("help", help="Show help")
        
        # Parse arguments
        parsed_args = parser.parse_args(args)
        
        # Execute command
        if parsed_args.command == "init":
            return self.init()
        elif parsed_args.command in ["install", "i"]:
            # Check if we're installing all packages from rainmeas-package.json
            if not parsed_args.package:
                return self.install_all_from_config()
            # Check if we're installing a specific package with version
            elif "@" in parsed_args.package:
                package_name, version = parsed_args.package.split("@", 1)
                return self.install(package_name, version)
            # Install a specific package with latest version
            else:
                return self.install(parsed_args.package)
        elif parsed_args.command == "remove":
            return self.remove(parsed_args.package)
        elif parsed_args.command == "update":
            if parsed_args.package:
                return self.update_package(parsed_args.package)
            else:
                return self.update_all()
        elif parsed_args.command == "list":
            return self.list_packages()
        elif parsed_args.command == "search":
            return self.search(parsed_args.query)
        elif parsed_args.command == "info":
            return self.info(parsed_args.package)
        elif parsed_args.command == "verify":
            return self.verify()
        elif parsed_args.command == "clean":
            return self.clean()
        elif parsed_args.command == "version":
            return self.version()
        elif parsed_args.command == "help":
            parser.print_help()
            return 0
        else:
            parser.print_help()
            return 1
    
    def init(self) -> int:
        """Initialize Rainmeas in current directory"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        print(f"Initializing Rainmeas in {self.skin_root}")
        # Create necessary directories and files
        import os
        modules_dir = os.path.join(self.skin_root, "@Resources", "@rainmeas-modules")
        os.makedirs(modules_dir, exist_ok=True)
        
        # Create initial config if it doesn't exist
        config_path = os.path.join(self.skin_root, "rainmeas-package.json")
        if not os.path.exists(config_path):
            import json
            with open(config_path, "w") as f:
                json.dump({"packages": {}}, f, indent=2)
        
        print("Rainmeas initialized successfully")
        return 0
    
    def install(self, package_name: str, version: str = "latest") -> int:
        """Install a package"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        if self.installer.install_package(package_name, version):
            return 0
        else:
            return 1
    
    def remove(self, package_name: str) -> int:
        """Remove a package"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        if self.installer.remove_package(package_name):
            return 0
        else:
            return 1
    
    def update_package(self, package_name: str) -> int:
        """Update a specific package"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        # Check if package is installed
        installed_packages = self.installer.list_installed_packages()
        if package_name not in installed_packages:
            print(f"Package '{package_name}' is not installed")
            return 1
        
        # Get the latest version from registry
        latest_version = self.registry.get_latest_version(package_name)
        if not latest_version:
            print(f"Could not determine latest version for package '{package_name}'")
            return 1
        
        # Check if already at latest version
        current_version = installed_packages[package_name]
        if current_version == latest_version:
            print(f"Package '{package_name}' is already at the latest version ({latest_version})")
            return 0
        
        # Remove the current version
        if not self.installer.remove_package(package_name):
            print(f"Failed to remove current version of '{package_name}'")
            return 1
        
        # Install the latest version
        if self.installer.install_package(package_name, latest_version):
            print(f"Successfully updated '{package_name}' from {current_version} to {latest_version}")
            return 0
        else:
            print(f"Failed to install updated version of '{package_name}'")
            return 1
    
    def update_all(self) -> int:
        """Update all packages"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        # Get installed packages
        installed_packages = self.installer.list_installed_packages()
        if not installed_packages:
            print("No packages installed")
            return 0
        
        updated_count = 0
        failed_count = 0
        
        print("Checking for updates...")
        
        for package_name, current_version in installed_packages.items():
            # Get the latest version from registry
            latest_version = self.registry.get_latest_version(package_name)
            if not latest_version:
                print(f"Could not determine latest version for package '{package_name}'")
                failed_count += 1
                continue
            
            # Check if update is needed
            if current_version != latest_version:
                print(f"Updating '{package_name}' from {current_version} to {latest_version}...")
                
                # Remove the current version
                if not self.installer.remove_package(package_name):
                    print(f"Failed to remove current version of '{package_name}'")
                    failed_count += 1
                    continue
                
                # Install the latest version
                if self.installer.install_package(package_name, latest_version):
                    print(f"Successfully updated '{package_name}'")
                    updated_count += 1
                else:
                    print(f"Failed to install updated version of '{package_name}'")
                    failed_count += 1
            else:
                print(f"'{package_name}' is already up to date ({current_version})")
        
        print(f"\nUpdate summary: {updated_count} updated, {failed_count} failed")
        return 0 if failed_count == 0 else 1
    
    def list_packages(self) -> int:
        """List installed packages"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        packages = self.installer.list_installed_packages()
        if not packages:
            print("No packages installed")
            return 0
        
        print("Installed packages:")
        for name, version in packages.items():
            print(f"  {name}@{version}")
        
        return 0
    
    def search(self, query: str) -> int:
        """Search for packages"""
        results = self.registry.search_packages(query)
        if not results:
            print(f"No packages found matching '{query}'")
            return 0
        
        print(f"Packages matching '{query}':")
        for name, info in results.items():
            print(f"  {name} (latest: {info['latest']})")
        
        return 0
    
    def info(self, package_name: str) -> int:
        """Show package information"""
        info = self.registry.get_package_info(package_name)
        if not info:
            print(f"Package '{package_name}' not found")
            return 1
        
        print(f"Package: {package_name}")
        print(f"Description: {info.get('description', 'No description')}")
        print(f"Author: {info.get('author', 'Unknown')}")
        print(f"License: {info.get('license', 'Unknown')}")
        print(f"Homepage: {info.get('homepage', 'None')}")
        
        # Show version information
        latest_version = self.registry.get_latest_version(package_name)
        if latest_version:
            print(f"Latest version: {latest_version}")
        
        available_versions = self.registry.get_available_versions(package_name)
        if available_versions:
            print(f"Available versions: {', '.join(available_versions)}")
        
        return 0
    
    def verify(self) -> int:
        """Verify package integrity"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        # Get installed packages
        installed_packages = self.installer.list_installed_packages()
        if not installed_packages:
            print("No packages installed")
            return 0
        
        verified_count = 0
        missing_count = 0
        
        print("Verifying package integrity...")
        
        for package_name, version in installed_packages.items():
            package_dir = os.path.join(self.installer.modules_dir, package_name)
            if os.path.exists(package_dir):
                print(f"✓ {package_name}@{version} - OK")
                verified_count += 1
            else:
                print(f"✗ {package_name}@{version} - MISSING")
                missing_count += 1
        
        print(f"\nVerification summary: {verified_count} verified, {missing_count} missing")
        return 0 if missing_count == 0 else 1
    
    def clean(self) -> int:
        """Clean unused modules"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        # Get installed packages from config
        installed_packages = self.installer.list_installed_packages()
        
        # Check modules directory
        if not os.path.exists(self.installer.modules_dir):
            print("No modules directory found")
            return 0
        
        cleaned_count = 0
        
        # Iterate through directories in modules folder
        for item in os.listdir(self.installer.modules_dir):
            item_path = os.path.join(self.installer.modules_dir, item)
            
            # Check if it's a directory and not in installed packages
            if os.path.isdir(item_path) and item not in installed_packages:
                try:
                    shutil.rmtree(item_path)
                    print(f"Removed unused module: {item}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"Failed to remove {item}: {e}")
        
        if cleaned_count > 0:
            print(f"Cleaned {cleaned_count} unused modules")
        else:
            print("No unused modules found")
        
        return 0
    
    def version(self) -> int:
        """Show version"""
        app_version = utils.get_app_version()
        print(f"rainmeas {app_version}")
        return 0
    
    def install_all_from_config(self) -> int:
        """Install all packages specified in rainmeas-package.json"""
        # Removed skin directory check as per user request
        # Not all modules have @Resources folder, so we proceed without validation
        
        # Load the rainmeas-package.json file from current directory
        config_path = "rainmeas-package.json"
        if not os.path.exists(config_path):
            print("Error: rainmeas-package.json not found in current directory")
            return 1
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error reading rainmeas-package.json: {e}")
            return 1
        
        packages = config.get("packages", {})
        if not packages:
            print("No packages specified in rainmeas-package.json")
            return 0
        
        # Use the installer's method that handles dependencies
        if self.installer.install_all_packages(packages):
            return 0
        else:
            return 1


def main():
    """Main entry point"""
    cli = RainmeasCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()