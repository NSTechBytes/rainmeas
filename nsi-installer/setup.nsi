;--------------------------------
; Rainmeas Installer Script
;--------------------------------

; The name of the installer
Name "Rainmeas"

; The file to write
OutFile "..\dist\rainmeas_v0.0.1_setup.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\Rainmeas"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Rainmeas" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------
; Interface Settings
;--------------------------------
!include "MUI2.nsh"

; Icon
!define MUI_ICON "assets\installer.ico"
!define MUI_UNICON "assets\uninstall.ico"

; Header image
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "assets\header.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "assets\header.bmp"

; Wizard image
!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\wizard.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "assets\wizard.bmp"

; Welcome page
!define MUI_WELCOMEPAGE_TITLE "Welcome to the Rainmeas Setup Wizard"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of Rainmeas, a package manager for Rainmeter skins.$\r$\n$\r$\nClick Next to continue."

; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\rainmeas.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Run Rainmeas CLI"

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Data
;--------------------------------

; License data
LicenseData "..\LICENSE"

;--------------------------------
; Sections
;--------------------------------

Section "Rainmeas" SecMain

  SetOutPath "$INSTDIR"
  
  ; Add files
  File "..\dist\rainmeas.exe"
  File "..\LICENSE"
  File "..\README.md"
  
  ; Store installation folder
  WriteRegStr HKLM "Software\Rainmeas" "Install_Dir" "$INSTDIR"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayName" "Rainmeas v0.0.1"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayIcon" "$INSTDIR\rainmeas.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "Publisher" "Rainmeas Team"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "HelpLink" "https://github.com/Rainmeas/rainmeas"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayVersion" "0.0.1"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "NoRepair" 1

SectionEnd

; Optional section (can be disabled by the user)
Section "Add to PATH" SecPATH

  ; Add the installation directory to the PATH
  ; Since EnVar plugin might not be available, we'll use a simpler approach
  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" \
                   "PATH" "$INSTDIR;$%PATH%"
  
  ; Set Section flag
  SectionIn RO

SectionEnd

; Optional section (can be disabled by the user)
Section "Desktop Shortcut" SecDesktop

  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\Rainmeas.lnk" "$INSTDIR\rainmeas.exe" "" "$INSTDIR\rainmeas.exe" 0
  
SectionEnd

;--------------------------------
; Descriptions
;--------------------------------

; Language strings
LangString DESC_SecMain ${LANG_ENGLISH} "Main Rainmeas application files."
LangString DESC_SecPATH ${LANG_ENGLISH} "Add Rainmeas to your system PATH for easy access from command line."
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create a desktop shortcut for Rainmeas."

; Assign language strings to sections
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
!insertmacro MUI_DESCRIPTION_TEXT ${SecPATH} $(DESC_SecPATH)
!insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller
;--------------------------------

Section "Uninstall"

  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas"
  DeleteRegKey HKLM "Software\Rainmeas"

  ; Remove files and uninstaller
  Delete "$INSTDIR\rainmeas.exe"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove directories used
  RMDir "$INSTDIR"

  ; Remove from PATH (simple approach)
  DeleteRegValue HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "PATH"
  
  ; Remove desktop shortcut
  Delete "$DESKTOP\Rainmeas.lnk"

SectionEnd
