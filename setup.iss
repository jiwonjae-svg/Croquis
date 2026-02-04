; Croquis Installer Script for Inno Setup
; Version: 1.0.1
; Created: February 4, 2026

#define MyAppName "Croquis"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Croquis Development Team"
#define MyAppURL "https://github.com/jiwonjae-svg/Croquis"
#define MyAppExeName "Croquis.exe"
#define MyAppDescription "Figure Drawing Practice Application"

[Setup]
; Basic Information
AppId={{8F7A2E3D-9C1B-4A5E-8D6F-2B4C7E9A1F3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=RELEASE_NOTES.md
OutputDir=installer
OutputBaseFilename=CroquisSetup-{#MyAppVersion}
SetupIconFile=src\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Version Information
VersionInfoVersion={#MyAppVersion}
VersionInfoDescription={#MyAppDescription}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Visual Appearance
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Translation files (if using external CSV)
Source: "translations.csv"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "RELEASE_NOTES.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

; Create data directories (will be populated by application)
; These are created automatically by the app, but can be pre-created
; Source: "deck\*"; DestDir: "{app}\deck"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".gitkeep"

[Dirs]
; Create user data directories with proper permissions
Name: "{userappdata}\{#MyAppName}"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\deck"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\dat"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\logs"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\croquis_pairs"; Permissions: users-full

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Registry]
; Associate application with Windows for easier launching
Root: HKCU; Subkey: "Software\{#MyAppName}"; Flags: uninsdeletekeyifempty
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: string; ValueName: "DataPath"; ValueData: "{userappdata}\{#MyAppName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up application data (optional - user may want to keep practice data)
Type: filesandordirs; Name: "{userappdata}\{#MyAppName}\logs"
Type: files; Name: "{userappdata}\{#MyAppName}\*.log"

[Code]
var
  DataDirPage: TInputDirWizardPage;
  PreserveDataCheckBox: TNewCheckBox;

procedure InitializeWizard;
var
  InfoLabel: TNewStaticText;
begin
  // Create custom page for data directory selection
  DataDirPage := CreateInputDirPage(wpSelectDir,
    'Select Data Folder', 'Where should practice data be stored?',
    'Select the folder where your decks, settings, and practice history will be saved, then click Next.',
    False, '');
  DataDirPage.Add('');
  DataDirPage.Values[0] := ExpandConstant('{userappdata}\{#MyAppName}');

  // Add info label
  InfoLabel := TNewStaticText.Create(DataDirPage);
  InfoLabel.Parent := DataDirPage.Surface;
  InfoLabel.Caption := 'Default location is recommended for most users.' + #13#10 +
    'You can change this later in application settings.';
  InfoLabel.AutoSize := True;
  InfoLabel.Top := DataDirPage.Edits[0].Top + DataDirPage.Edits[0].Height + 8;
  InfoLabel.Left := DataDirPage.Edits[0].Left;
end;

function GetDataDir(Param: String): String;
begin
  Result := DataDirPage.Values[0];
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
  PreserveData: Boolean;
begin
  if CurUninstallStep = usUninstall then
  begin
    // Ask user if they want to preserve practice data
    PreserveData := MsgBox('Do you want to keep your practice data (decks, settings, history)?' + #13#10 + #13#10 +
      'Choose Yes to preserve your data for future installations.' + #13#10 +
      'Choose No to completely remove all application data.',
      mbConfirmation, MB_YESNO) = IDYES;

    if not PreserveData then
    begin
      // Remove all user data
      if DirExists(ExpandConstant('{userappdata}\{#MyAppName}')) then
        DelTree(ExpandConstant('{userappdata}\{#MyAppName}'), True, True, True);
      
      MsgBox('All application data has been removed.', mbInformation, MB_OK);
    end
    else
    begin
      MsgBox('Your practice data has been preserved in:' + #13#10 +
        ExpandConstant('{userappdata}\{#MyAppName}'), mbInformation, MB_OK);
    end;
  end;
end;

function InitializeSetup(): Boolean;
var
  OldVersion: String;
  ResultCode: Integer;
begin
  Result := True;

  // Check if application is already installed
  if RegQueryStringValue(HKCU, 'Software\{#MyAppName}\Settings', 'Version', OldVersion) then
  begin
    if OldVersion = '{#MyAppVersion}' then
    begin
      if MsgBox('{#MyAppName} {#MyAppVersion} is already installed. Do you want to reinstall?',
        mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
        Exit;
      end;
    end
    else
    begin
      MsgBox('Upgrading from version ' + OldVersion + ' to {#MyAppVersion}.' + #13#10 +
        'Your practice data will be preserved.',
        mbInformation, MB_OK);
    end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Result := '';
  
  // Check if application is running
  if CheckForMutexes('{#MyAppName}Mutex') then
  begin
    Result := '{#MyAppName} is currently running. Please close the application before continuing installation.';
    Exit;
  end;
end;

[Messages]
; Custom messages
BeveledLabel={#MyAppName} v{#MyAppVersion}

[CustomMessages]
; English
english.LaunchAfterInstall=Launch {#MyAppName} after installation
english.DataDirInfo=Practice data will be stored in this folder
english.PreserveData=Keep my practice data

; Korean
korean.LaunchAfterInstall=설치 후 {#MyAppName} 실행
korean.DataDirInfo=연습 데이터가 이 폴더에 저장됩니다
korean.PreserveData=내 연습 데이터 보관

; Japanese
japanese.LaunchAfterInstall=インストール後に{#MyAppName}を起動
japanese.DataDirInfo=練習データはこのフォルダに保存されます
japanese.PreserveData=練習データを保持する
