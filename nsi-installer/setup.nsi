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

;--------------------------------
; Windows Message Constants
;--------------------------------
!ifndef WM_WININICHANGE
!define WM_WININICHANGE 0x001A
!endif
!ifndef HWND_BROADCAST
!define HWND_BROADCAST 0xFFFF
!endif

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
  ; Read the current PATH
  ReadEnvStr $R0 "PATH"
  ; Append our installation directory to the PATH
  StrCpy $R1 "$R0;$INSTDIR"
  ; Write the updated PATH back to the registry
  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "PATH" $R1
  
  ; Send a message to all applications to let them know the PATH has changed
  SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
  
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

  ; Remove rainmeas from PATH
  ReadEnvStr $R0 "PATH"
  ; Remove our installation directory from the PATH
  Push $R0
  Push "$INSTDIR"
  Call un.RemoveFromPath
  Pop $R1
  ; Write the updated PATH back to the registry
  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "PATH" $R1
  
  ; Remove desktop shortcut
  Delete "$DESKTOP\Rainmeas.lnk"

SectionEnd

; Function to remove a directory from the PATH environment variable
Function un.RemoveFromPath
  Exch $0 ; directory to remove
  Exch
  Exch $1 ; PATH variable
  Push $2
  Push $3
  Push $4
  Push $5
  
  ; Backup the original PATH
  StrCpy $2 $1
  
  ; Loop to find and remove all instances of the directory
  loop:
    ; Find the directory in the PATH
    StrCpy $3 $2 1 0
    StrCmp $3 "" done
    StrCpy $4 $2 "" 0
    StrCpy $5 $4 1 0
    StrCmp $5 ";" 0 +2
    StrCpy $4 $4 "" 1
    StrCmp $4 $0 0 next
    
    ; Found the directory, remove it
    StrLen $3 $0
    StrCpy $4 $2 "" $3
    StrCpy $2 $2 $3
    StrCpy $2 $2$4
    
    Goto loop
    
    next:
      StrCpy $3 $2 1 0
      StrCmp $3 "" done
      StrCpy $4 $2 "" 1
      StrCpy $2 $4
      Goto loop
      
  done:
    ; Remove trailing semicolon if present
    StrCpy $3 $2 "" -1
    StrCmp $3 ";" 0 +2
    StrCpy $2 $2 -1
    
    ; Remove leading semicolon if present
    StrCpy $3 $2 1 0
    StrCmp $3 ";" 0 +2
    StrCpy $2 $2 "" 1
    
    ; Return the modified PATH
    Pop $5
    Pop $4
    Pop $3
    Exch $2
    Exch
    Pop $0
    Exch $1
FunctionEnd