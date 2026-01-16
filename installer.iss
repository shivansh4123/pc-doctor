; Inno Setup Script for PC Doctor
; Download Inno Setup from: https://jrsoftware.org/isdl.php




#define MyAppName "PC Doctor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Shivansh Seth"
#define MyAppURL "https://yourwebsite.com"
#define MyAppExeName "PCDoctor.exe"

[Setup]
; Basic info
AppId={{86F61A52-0D5E-4B1A-974D-6C56C8ACCE76}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=PCDoctor_Setup_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=favicon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Visual setup
WizardImageFile=installer_image.bmp
WizardSmallImageFile=installer_small.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\PCDoctor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
; Add any other files needed

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Check if .NET Framework or other dependencies are installed
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Add dependency checks here
end;

// Custom page for API key input
var
  APIKeyPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  // Create custom page for API key
  APIKeyPage := CreateInputQueryPage(wpWelcome,
    'Gemini API Key', 'Enter your Google Gemini API key',
    'PC Doctor requires a Gemini API key to function. You can get one free at https://aistudio.google.com/app/apikey');
  APIKeyPage.Add('API Key:', False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  APIKey: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Save API key to config file
    APIKey := APIKeyPage.Values[0];
    if APIKey <> '' then
    begin
      ConfigFile := ExpandConstant('{app}\config.ini');
      SaveStringToFile(ConfigFile, '[API]' + #13#10 + 'GEMINI_API_KEY=' + APIKey + #13#10, False);
    end;
  end;
end;
