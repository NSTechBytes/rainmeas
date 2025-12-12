#!/usr/bin/env python3
"""
Test script to verify that all modules can be imported correctly
"""
import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        import cli
        print("✓ cli module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import cli module: {e}")
        return False
    
    try:
        import registry
        print("✓ registry module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import registry module: {e}")
        return False
    
    try:
        import installer
        print("✓ installer module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import installer module: {e}")
        return False
    
    try:
        import utils
        print("✓ utils module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utils module: {e}")
        return False
    
    try:
        import semver
        print("✓ semver module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import semver module: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nAll modules imported successfully!")
    else:
        print("\nSome modules failed to import!")
    sys.exit(0 if success else 1)