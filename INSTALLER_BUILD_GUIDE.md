# 🔧 Building Installer with Inno Setup

This guide explains how to create a Windows installer for Croquis using Inno Setup.

## Prerequisites

1. **Download Inno Setup**
   - Visit: https://jrsoftware.org/isdl.php
   - Download: Inno Setup 6.x (latest version)
   - Install with default settings

2. **Build Croquis Executable**
   ```powershell
   python scripts/build.py
   ```
   This creates `dist/Croquis.exe`

## Creating the Installer

### Method 1: GUI (Recommended for First-Time Users)

1. **Open Inno Setup Compiler**
   - Launch "Inno Setup Compiler" from Start Menu

2. **Open Script**
   - File → Open → Select `setup.iss`

3. **Compile**
   - Build → Compile (or press F9)
   - Wait for compilation to complete

4. **Output**
   - Installer will be created in `installer/` folder
   - Filename: `CroquisSetup-1.0.1.exe`

### Method 2: Command Line (For Automation)

```powershell
# Compile installer from command line
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss

# Or create a batch file
.\build_installer.bat
```

### Method 3: Automated Build Script

Create `build_installer.bat`:
```batch
@echo off
echo ============================================================
echo Croquis Installer Build Script
echo ============================================================

REM Step 1: Build executable
echo.
echo [1/3] Building executable...
python scripts\build.py
if errorlevel 1 (
    echo ERROR: Executable build failed!
    pause
    exit /b 1
)

REM Step 2: Create installer directory
echo.
echo [2/3] Preparing installer directory...
if not exist "installer" mkdir installer

REM Step 3: Compile installer
echo.
echo [3/3] Compiling installer with Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
if errorlevel 1 (
    echo ERROR: Installer compilation failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! Installer created in installer\ folder
echo ============================================================
pause
```

Then run:
```powershell
.\build_installer.bat
```

## Installer Features

### What's Included
- ✅ Croquis.exe (single-file executable)
- ✅ translations.csv (multi-language support)
- ✅ README.md (documentation)
- ✅ RELEASE_NOTES.md (version history)
- ✅ LICENSE (MIT license)

### Installation Options
- **Installation Directory**: Default = `C:\Program Files\Croquis`
- **Data Directory**: Default = `%APPDATA%\Croquis`
- **Desktop Icon**: Optional (unchecked by default)
- **Quick Launch**: Optional (Windows 10/11)

### Languages Supported
- 🇬🇧 English
- 🇰🇷 Korean
- 🇯🇵 Japanese

### User Data Handling
- **Installation**: Creates data folders with proper permissions
- **Upgrade**: Preserves existing practice data
- **Uninstallation**: Asks user to keep or remove data

## Customization

### Changing Version Number

Edit `setup.iss`:
```pascal
#define MyAppVersion "1.0.2"  ; Update this line
```

### Changing Install Location

Edit `setup.iss`:
```pascal
DefaultDirName={autopf}\{#MyAppName}  ; Change to custom path
```

### Adding Files

Edit `[Files]` section in `setup.iss`:
```pascal
Source: "your-file.txt"; DestDir: "{app}"; Flags: ignoreversion
```

### Custom Messages

Edit `[CustomMessages]` section:
```pascal
english.YourMessage=Your English text
korean.YourMessage=한글 텍스트
japanese.YourMessage=日本語テキスト
```

## Testing the Installer

### Before Distribution
1. **Clean Environment Test**
   - Install on a clean Windows VM
   - Verify all features work
   - Check desktop/start menu shortcuts

2. **Upgrade Test**
   - Install older version first
   - Run new installer
   - Verify data preservation

3. **Uninstall Test**
   - Uninstall application
   - Verify clean removal
   - Check data preservation options

### Installer Verification Checklist
- [ ] Application launches correctly
- [ ] All translations load properly
- [ ] Data directories created with permissions
- [ ] Desktop icon works (if selected)
- [ ] Start menu shortcuts functional
- [ ] Uninstaller removes application cleanly
- [ ] User data preservation works

## Troubleshooting

### "ISCC.exe not found"
- Install Inno Setup from: https://jrsoftware.org/isdl.php
- Or update path in build script to match your installation

### "Source file not found: dist\Croquis.exe"
- Build executable first: `python scripts/build.py`
- Verify `dist/Croquis.exe` exists

### "Access Denied" during compilation
- Run Inno Setup Compiler as Administrator
- Check antivirus isn't blocking compilation

### Installer too large
- Check `dist/Croquis.exe` size (should be ~48MB)
- Verify no unnecessary files in `[Files]` section
- Use `Compression=lzma2/max` for best compression

## Distribution

### Before Release
1. **Test installer on multiple systems**
   - Windows 10 (x64)
   - Windows 11 (x64)
   - Clean install vs. upgrade

2. **Code Signing (Optional but Recommended)**
   - Obtain code signing certificate
   - Sign both `Croquis.exe` and `CroquisSetup.exe`
   - Prevents "Unknown Publisher" warnings

3. **Create checksums**
   ```powershell
   Get-FileHash installer\CroquisSetup-1.0.1.exe -Algorithm SHA256
   ```

### Release Checklist
- [ ] Installer tested on clean Windows
- [ ] Version numbers match (app + installer)
- [ ] Release notes included
- [ ] LICENSE file present
- [ ] README.md updated
- [ ] GitHub release created
- [ ] Checksums provided

## Advanced Features

### Silent Installation
```powershell
CroquisSetup-1.0.1.exe /SILENT
# Or completely silent:
CroquisSetup-1.0.1.exe /VERYSILENT
```

### Custom Install Directory
```powershell
CroquisSetup-1.0.1.exe /DIR="D:\MyApps\Croquis"
```

### No Desktop Icon
```powershell
CroquisSetup-1.0.1.exe /TASKS="!desktopicon"
```

## Support

For issues with Inno Setup:
- Documentation: https://jrsoftware.org/ishelp/
- Forum: https://groups.google.com/g/innosetup

For Croquis-specific issues:
- GitHub Issues: https://github.com/jiwonjae-svg/Croquis/issues

---

**Happy Building!** 🚀
