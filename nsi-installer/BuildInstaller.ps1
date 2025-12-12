# Build script for NSIS installer
# This script builds the installer using NSIS

# Define paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$NsisScript = Join-Path $ScriptDir "setup.nsi"
$OutputDir = Join-Path $ScriptDir "..\dist"
$GenerateNsisScript = Join-Path $ScriptDir "GenerateNsisScript.ps1"
$VersionFile = Join-Path $ScriptDir "..\VERSION"

# Read version from VERSION file
if (Test-Path $VersionFile) {
    $AppVersion = Get-Content $VersionFile -First 1
    $AppVersion = $AppVersion.Trim()
    Write-Host "Application version: $AppVersion"
} else {
    Write-Error "Version file not found: $VersionFile"
    exit 1
}

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

Write-Host "Building Rainmeas NSIS Installer..."

# Check if NSIS is installed
if ($null -eq $NsisExe) {
    Write-Error "NSIS (makensis) not found. Please install NSIS from https://nsis.sourceforge.io/Download"
    exit 1
} else {
    Write-Host "Found NSIS at: $NsisExe"
}

# Check if NSIS script generator exists
if (-not (Test-Path $GenerateNsisScript)) {
    Write-Error "NSIS script generator not found: $GenerateNsisScript"
    exit 1
}

# Generate the NSIS script with the correct version
Write-Host "Generating NSIS script..."
& powershell -ExecutionPolicy Bypass -File "$GenerateNsisScript"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate NSIS script"
    exit 1
}

# Check if NSIS script exists
if (-not (Test-Path $NsisScript)) {
    Write-Error "NSIS script not found: $NsisScript"
    exit 1
}

# Check if the executable exists
$Executable = Join-Path $OutputDir "rainmeas.exe"
if (-not (Test-Path $Executable)) {
    Write-Error "Executable not found: $Executable. Please build the executable first using Build.ps1"
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