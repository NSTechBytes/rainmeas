import os
import json
import sys
from typing import Dict, Any, Optional

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_app_version():
    """Get application version from VERSION file"""
    # Try to find VERSION file in different locations
    version_file_paths = [
        resource_path("VERSION"),  # For PyInstaller
        os.path.join(os.path.dirname(__file__), "..", "VERSION"),  # For development
        os.path.join(os.path.dirname(__file__), "..", "..", "VERSION"),  # For development
        "VERSION"  # Current directory
    ]
    
    for version_file in version_file_paths:
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r') as f:
                    version = f.read().strip()
                    return version
            except Exception:
                continue
    
    # Default version if VERSION file is not found
    return "0.0.1"

def find_rainmeter_skin_root(start_path: str = ".") -> Optional[str]:
    """Find the root of a Rainmeter skin by looking for key files/directories"""
    current_path = os.path.abspath(start_path)
    
    while current_path != os.path.dirname(current_path):  # Not at root
        # Look for typical Rainmeter skin indicators
        if (os.path.exists(os.path.join(current_path, "@Resources")) or
            os.path.exists(os.path.join(current_path, "Rainmeter.ini")) or
            os.path.exists(os.path.join(current_path, "@Backup"))):
            return current_path
        
        # Move up one directory
        current_path = os.path.dirname(current_path)
    
    return None

def load_rainmeas_config(skin_root: str) -> Dict[str, Any]:
    """Load the rainmeas-package.json configuration file"""
    config_path = os.path.join(skin_root, "rainmeas-package.json")
    
    if not os.path.exists(config_path):
        return {"packages": {}}
    
    with open(config_path, 'r') as f:
        return json.load(f)

def save_rainmeas_config(skin_root: str, config: Dict[str, Any]) -> None:
    """Save the rainmeas-package.json configuration file"""
    config_path = os.path.join(skin_root, "rainmeas-package.json")
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def is_rainmeter_skin(path: str) -> bool:
    """Check if a directory is a Rainmeter skin directory"""
    return (os.path.exists(os.path.join(path, "@Resources")) or
            os.path.exists(os.path.join(path, "Rainmeter.ini")))

def get_installed_packages(skin_root: str) -> Dict[str, str]:
    """Get a dictionary of installed packages and their versions"""
    config = load_rainmeas_config(skin_root)
    return config.get("packages", {})