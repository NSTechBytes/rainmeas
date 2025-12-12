import sys
import argparse
from typing import List
import os

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
        self.registry = registry.Registry()
        self.skin_root = utils.find_rainmeter_skin_root()
        if self.skin_root:
            self.installer = installer.Installer(self.skin_root, self.registry)
        else:
            self.installer = None
    
    def run(self, args: List[str]) -> int:
        # Get application version
        app_version = utils.get_app_version()
        
        parser = argparse.ArgumentParser(
            prog="rainmeas",
            description="Rainmeas CLI for managing Rainmeter skin packages"
        )
        
        # Add version argument to main parser
        parser.add_argument("--version", action="version", version=f"rainmeas {app_version}")
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Init command
        init_parser = subparsers.add_parser("init", help="Initialize Rainmeas in a Rainmeter skin")
        
        # Install command
        install_parser = subparsers.add_parser("install", help="Install a package")
        install_parser.add_argument("package", help="Package name and optional version (e.g., freshweather or freshweather@1.3.0)")
        
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
        elif parsed_args.command == "install":
            if "@" in parsed_args.package:
                package_name, version = parsed_args.package.split("@", 1)
                return self.install(package_name, version)
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
        if not self.skin_root:
            print("Error: Not in a Rainmeter skin directory")
            return 1
        
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
        if not self.installer:
            print("Error: Not in a Rainmeter skin directory")
            return 1
        
        if self.installer.install_package(package_name, version):
            return 0
        else:
            return 1
    
    def remove(self, package_name: str) -> int:
        """Remove a package"""
        if not self.installer:
            print("Error: Not in a Rainmeter skin directory")
            return 1
        
        if self.installer.remove_package(package_name):
            return 0
        else:
            return 1
    
    def update_package(self, package_name: str) -> int:
        """Update a specific package"""
        print(f"Updating package: {package_name}")
        # Placeholder implementation
        return 0
    
    def update_all(self) -> int:
        """Update all packages"""
        print("Updating all packages")
        # Placeholder implementation
        return 0
    
    def list_packages(self) -> int:
        """List installed packages"""
        if not self.installer:
            print("Error: Not in a Rainmeter skin directory")
            return 1
        
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
        print("Verifying packages...")
        # Placeholder implementation
        return 0
    
    def clean(self) -> int:
        """Clean unused modules"""
        print("Cleaning unused modules...")
        # Placeholder implementation
        return 0
    
    def version(self) -> int:
        """Show version"""
        app_version = utils.get_app_version()
        print(f"rainmeas {app_version}")
        return 0

def main():
    """Main entry point"""
    cli = RainmeasCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()