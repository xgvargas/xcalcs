; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "XcalcS"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "gvTech"
#define MyAppURL "http://www.gvtech.xyz/"
#define MyAppExeName "xcalcs.exe"

[Setup]
AppId={{A6198042-E8B3-4031-909F-CDF751DBB631}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userpf}\{#MyAppName}
DisableDirPage=auto
DefaultGroupName={#MyAppName}
OutputBaseFilename={#MyAppName}-{#MyAppVersion}-Setup
Compression=lzma/ultra
SolidCompression=yes
ShowLanguageDialog=no
OutputDir=dist
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp
PrivilegesRequired=none
AlwaysShowGroupOnReadyPage=True
AlwaysShowDirOnReadyPage=True
LicenseFile=D:\Projetos\xcalcs\license
; SetupIconFile=D:\Projetos\xcalcs\ui\exeicon.ico
; VersionInfoVersion=12
; VersionInfoCompany=gvTech
; VersionInfoProductVersion=0.1.1

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "pt"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\pack\xcalcs.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\pack\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "python34.dll"
Source: "..\vcredist_x86-2010-python3.4.exe"; DestDir: "{tmp}"; DestName: "vcredist_x86.exe"; Flags: deleteafterinstall

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: {tmp}\vcredist_x86.exe; Parameters: "/passive /Q:a /c:""msiexec /qb /i vcredist.msi"" "; StatusMsg: "Installing VC++ 2010 Redistributables..."
Filename: "{app}\{#MyAppExeName}"; Flags: nowait postinstall skipifsilent; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"

[INI]
Filename: "{app}\xcalcs.cfg"; Section: "Config"; Key: "language"; String: "{language}"

; exemplo de como fazer associacoes
; [Setup]
; ChangesAssociations = yes
; [Tasks]
; Name: mypAssociation; Description: "Associate "".mpl"" extension"; GroupDescription: File extensions:
; [Registry]
; Root: HKCR; Subkey: ".mpl";                             ValueData: "{#MyAppName}";          Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Tasks: mypAssociation
; Root: HKCR; Subkey: "{#MyAppName}";                     ValueData: "Program {#MyAppName}";  Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Tasks: mypAssociation
; Root: HKCR; Subkey: "{#MyAppName}\DefaultIcon";         ValueData: "{app}\{#MyAppExeName},0";               ValueType: string;  ValueName: ""; Tasks: mypAssociation
; Root: HKCR; Subkey: "{#MyAppName}\shell\open\command";  ValueData: """{app}\{#MyAppExeName}.EXE"" ""%1""";  ValueType: string;  ValueName: ""; Tasks: mypAssociation
