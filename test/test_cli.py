#!/usr/bin/env python3
import sys
import os

# Add the src directory to the path (adjusting for new location in test folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(script_dir, '..', 'src')
sys.path.insert(0, src_path)

# Now we can import the modules directly
import cli
import registry

def test_registry():
    """Test that registry module works"""
    reg = registry.Registry()
    print("Registry module loaded successfully")
    return True

def test_cli_creation():
    """Test that CLI can be created"""
    cli_instance = cli.RainmeasCLI()
    print("CLI module loaded successfully")
    return True

if __name__ == "__main__":
    print("Running basic CLI tests...")
    try:
        test_registry()
        test_cli_creation()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)