;--------------------------------
; Rainmeas Installer Script
;--------------------------------

; Define global version variable
!define VERSION "0.0.1"

; The name of the installer
Name "Rainmeas"

; The file to write
OutFile "..\dist\rainmeas_v${VERSION}_setup.exe"

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

;--------------------------------
; Windows Message Constants
;--------------------------------
!ifndef WM_WININICHANGE
!define WM_WININICHANGE 0x001A
!endif
!ifndef HWND_BROADCAST
!define HWND_BROADCAST 0xFFFF
!endif

;--------------------------------
; EnVar Plugin for PATH manipulation
;--------------------------------

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
!undef MUI_PAGE_LICENSE
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

;--------------------------------
; Sections
;--------------------------------

Section "Rainmeas" SecMain

  SetOutPath "$INSTDIR"
  
  ; Add files
  File "..\dist\rainmeas.exe"
  
  ; Store installation folder
  WriteRegStr HKLM "Software\Rainmeas" "Install_Dir" "$INSTDIR"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayName" "Rainmeas v${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayIcon" "$INSTDIR\rainmeas.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "Publisher" "Rainmeas Team"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "HelpLink" "https://github.com/Rainmeas/rainmeas"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "DisplayVersion" "${VERSION}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas" \
                   "NoRepair" 1

SectionEnd

; Optional section (can be disabled by the user)
Section "Add to PATH" SecPATH

  ; Add the installation directory to the PATH using EnVar plugin
  EnVar::SetHKLM
  EnVar::AddValue "PATH" "$INSTDIR"
  Pop $0
  DetailPrint "Add to PATH returned=|$0|"
  
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

  ; Read the installation directory from the registry BEFORE deleting registry keys
  ReadRegStr $INSTDIR HKLM "Software\Rainmeas" "Install_Dir"
  
  ; Remove rainmeas from PATH using EnVar plugin
  EnVar::SetHKLM
  EnVar::DeleteValue "PATH" "$INSTDIR"
  Pop $0
  DetailPrint "Remove from PATH returned=|$0|"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Rainmeas"
  DeleteRegKey HKLM "Software\Rainmeas"

  ; Remove files and uninstaller
  Delete "$INSTDIR\rainmeas.exe"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove directories used
  RMDir "$INSTDIR"
  
  ; Remove desktop shortcut
  Delete "$DESKTOP\Rainmeas.lnk"

SectionEnd