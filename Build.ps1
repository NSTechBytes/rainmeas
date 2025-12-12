# Build script for rainmeas CLI tool
# This script creates a standalone executable using PyInstaller and then builds an installer with NSIS

# Define paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AssetsDir = Join-Path $ScriptDir "assets"
$SrcDir = Join-Path $ScriptDir "src"
$OutputDir = Join-Path $ScriptDir "dist"
$IconPath = Join-Path $AssetsDir "icon.ico"
$EntryPoint = Join-Path $ScriptDir "run_cli.py"
$NsisDir = Join-Path $ScriptDir "nsi-installer"
$NsisScript = Join-Path $NsisDir "setup.nsi"
$VersionFile = Join-Path $ScriptDir "VERSION"

# Read version from VERSION file
if (Test-Path $VersionFile) {
    $AppVersion = Get-Content $VersionFile -First 1
    $AppVersion = $AppVersion.Trim()
    Write-Host "Application version: $AppVersion"
} else {
    Write-Error "Version file not found: $VersionFile"
    exit 1
}

# Check if required files exist
if (-not (Test-Path $EntryPoint)) {
    Write-Error "Entry point script not found: $EntryPoint"
    exit 1
}

if (-not (Test-Path $IconPath)) {
    Write-Error "Icon file not found: $IconPath"
    exit 1
}

# Create output directory if it doesn't exist
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Check if PyInstaller is installed
try {
    $pyinstallerVersion = & pip show pyinstaller | Select-String "Version"
    if ($null -eq $pyinstallerVersion) {
        throw "PyInstaller not found"
    }
    Write-Host "Found PyInstaller: $pyinstallerVersion"
} catch {
    Write-Host "PyInstaller not found. Installing..."
    & pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller"
        exit 1
    }
}

# Build the executable with proper module inclusion
Write-Host "Building rainmeas executable..."
& pyinstaller --onefile --console --icon="$IconPath" --name="rainmeas" --distpath="$OutputDir" --workpath="$ScriptDir\build" --specpath="$ScriptDir" --add-data="$SrcDir;src" --add-data="$AssetsDir;assets" --add-data="$VersionFile;." "$EntryPoint"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build executable"
    exit 1
}

Write-Host "Executable build successful!"
Write-Host "Executable location: $(Join-Path $OutputDir "rainmeas.exe")"

# Define NSIS path (check common installation locations)
$NsisPaths = @(
    "C:\Program Files (x86)\NSIS\makensis.exe",
    "C:\Program Files\NSIS\makensis.exe",
    "makensis.exe"  # For PATH-based installations
)

$NsisExe = $null
foreach ($Path in $NsisPaths) {
    if (Test-Path $Path) {
        $NsisExe = $Path
        break
    }
}

# Check if NSIS is installed
if ($null -eq $NsisExe) {
    Write-Warning "NSIS (makensis) not found. Skipping installer creation."
    Write-Host "To create an installer, please install NSIS from http://nsis.sourceforge.net/"
    Write-Host "Download link: https://sourceforge.net/projects/nsis/files/latest/download"
    Write-Host ""
    Write-Host "After installing NSIS, you can run this script again to build the installer."
    exit 0
}

# Check if NSIS script exists
if (-not (Test-Path $NsisScript)) {
    Write-Error "NSIS script not found: $NsisScript"
    exit 1
}

# Build the installer
Write-Host "Building installer..."
& "$NsisExe" "$NsisScript"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build installer"
    exit 1
}

Write-Host "Installer build successful!"
Write-Host "Installer location: $(Join-Path $OutputDir "rainmeas_v$AppVersion`_setup.exe")"