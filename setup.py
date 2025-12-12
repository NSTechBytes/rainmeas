from setuptools import setup, find_packages
import os

# Read the contents of README.md for the long description
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

# Read version from VERSION file
version = "0.0.1"  # Default fallback version
version_path = os.path.join(os.path.dirname(__file__), "VERSION")
if os.path.exists(version_path):
    with open(version_path, "r") as f:
        version = f.read().strip()

setup(
    name="rainmeas",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["../assets/*.ico", "../VERSION"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rainmeas=cli:main",
        ]
    },
    install_requires=[],
    python_requires=">=3.6",
    author="Rainmeas Team",
    description="CLI tool for managing Rainmeter skin packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="rainmeter package manager cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)