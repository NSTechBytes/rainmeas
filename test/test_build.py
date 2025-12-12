#!/usr/bin/env python3
"""
Test script to verify the build process
"""
import subprocess
import sys
import os

def test_build():
    """Test that the build process works correctly"""
    # Change to the rainmeas directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the build script
    print("Testing build process...")
    try:
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Build.ps1"], 
                              capture_output=True, text=True, timeout=300)
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("Return code:", result.returncode)
        
        if result.returncode == 0:
            print("Build process completed successfully!")
            return True
        else:
            print("Build process failed!")
            return False
    except subprocess.TimeoutExpired:
        print("Build process timed out!")
        return False
    except Exception as e:
        print(f"Error running build process: {e}")
        return False

if __name__ == "__main__":
    success = test_build()
    sys.exit(0 if success else 1)