import json
import os
import sys
from typing import Dict, Any, Optional, List
try:
    import urllib.request
    import urllib.error
except ImportError:
    # For older Python versions
    import urllib2 as urllib
    urllib.request = urllib
    urllib.error = urllib

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Registry:
    def __init__(self):
        """
        Initialize the Registry for remote access only.
        """
        self.remote_base_url = "https://raw.githubusercontent.com/Rainmeas/rainmeas-registry/main"
    
    def _fetch_remote_json(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch JSON data from a remote URL."""
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Error fetching remote data from {url}: {e}")
            return None
    
    def list_all_package_names(self) -> List[str]:
        """List all package names from the remote index."""
        # Fetch from remote index.json
        index_url = f"{self.remote_base_url}/index.json"
        index_data = self._fetch_remote_json(index_url)
        if index_data:
            return list(index_data.keys())
        return []
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific package from remote."""
        # Fetch from remote package file
        package_url = f"{self.remote_base_url}/packages/{package_name}.json"
        return self._fetch_remote_json(package_url)
    
    def search_packages(self, query: str) -> Dict[str, Any]:
        """Search for packages matching a query."""
        results = {}
        
        # Get all package names
        package_names = self.list_all_package_names()
        if not package_names:
            return results
        
        # Scan all package files
        for package_name in package_names:
            package_info = self.get_package_info(package_name)
            if not package_info:
                continue
            
            # Match by package name
            if query.lower() in package_name.lower():
                # Create a simplified info object for search results
                latest_version = self.get_latest_version(package_name, package_info)
                versions = self.get_available_versions(package_name, package_info)
                results[package_name] = {
                    "latest": latest_version or "unknown",
                    "versions": versions
                }
            else:
                # Match by package details
                if (query.lower() in package_info.get("description", "").lower() or
                    query.lower() in package_info.get("author", "").lower()):
                    # Create a simplified info object for search results
                    latest_version = self.get_latest_version(package_name, package_info)
                    versions = self.get_available_versions(package_name, package_info)
                    results[package_name] = {
                        "latest": latest_version or "unknown",
                        "versions": versions
                    }
        
        return results
    
    def get_latest_version(self, package_name: str, package_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Get the latest version of a package."""
        if package_info is None:
            package_info = self.get_package_info(package_name)
        
        if not package_info:
            return None
        
        # Get latest version from the package file
        versions = package_info.get("versions", {})
        if "latest" in versions:
            return versions["latest"]
        
        # If no explicit "latest" key, return the highest version
        version_keys = [k for k in versions.keys() if k != "latest"]
        if version_keys:
            # Simple version sorting (in a real implementation, you'd want proper semver sorting)
            return sorted(version_keys)[-1]
        
        return None
    
    def get_available_versions(self, package_name: str, package_info: Optional[Dict[str, Any]] = None) -> List[str]:
        """Get all available versions of a package."""
        if package_info is None:
            package_info = self.get_package_info(package_name)
        
        if not package_info:
            return []
        
        versions = package_info.get("versions", {})
        # Return all version keys except "latest"
        return [k for k in versions.keys() if k != "latest"]
    
    def get_version_download_url(self, package_name: str, version: str) -> Optional[str]:
        """Get the download URL for a specific package version."""
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return None
        
        versions = package_info.get("versions", {})
        if version in versions and isinstance(versions[version], dict):
            return versions[version].get("download")
        
        return None