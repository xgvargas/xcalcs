
[Setup]
AppId={{E4F287EE-414F-48DB-B820-9929DE9A8807}
AppName=CommCenter
AppVersion=0.2.1
;AppVerName=CommCenter 0.2.1
AppPublisher=My Company, Inc.
AppPublisherURL=http://www.example.com/
AppSupportURL=http://www.example.com/
AppUpdatesURL=http://www.example.com/
DefaultDirName={pf}\CommCenter
DefaultGroupName=CommCenter
OutputBaseFilename=CommCenter-setup
Compression=lzma
SolidCompression=yes
ShowLanguageDialog=no
OutputDir=dist
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\exe.win32-3.4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CommCenter"; Filename: "{app}\conncenter.exe"
Name: "{group}\{cm:UninstallProgram,CommCenter}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CommCenter"; Filename: "{app}\conncenter.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\conncenter.exe"; Description: "{cm:LaunchProgram,CommCenter}"; Flags: nowait postinstall skipifsilent
