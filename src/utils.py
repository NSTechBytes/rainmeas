import os
import json
import sys
import time
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

# Removed find_rainmeter_skin_root function as per user request
# Not all modules have @Resources folder, so we don't check for module directories

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

def get_installed_packages(skin_root: str) -> Dict[str, str]:
    """Get a dictionary of installed packages and their versions"""
    config = load_rainmeas_config(skin_root)
    return config.get("packages", {})

def get_current_timestamp() -> str:
    """Get current timestamp as ISO format string"""
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())