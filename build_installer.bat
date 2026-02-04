@echo off
REM Croquis Installer Build Script
REM This script builds the executable and creates an installer using Inno Setup

echo ============================================================
echo Croquis Installer Build Script
echo ============================================================
echo.

REM Check if Inno Setup is installed
set INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_SETUP_PATH%" (
    echo ERROR: Inno Setup not found!
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

REM Step 1: Build executable
echo [1/3] Building Croquis executable...
echo.
python scripts\build.py
if errorlevel 1 (
    echo.
    echo ERROR: Executable build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

REM Verify executable exists
if not exist "dist\Croquis.exe" (
    echo.
    echo ERROR: Executable not found at dist\Croquis.exe
    echo Build may have failed silently.
    echo.
    pause
    exit /b 1
)

echo.
echo SUCCESS: Executable built successfully!
echo Size: 
for %%F in ("dist\Croquis.exe") do echo %%~zF bytes
echo.

REM Step 2: Create installer directory
echo [2/3] Preparing installer directory...
if not exist "installer" mkdir installer
echo SUCCESS: Installer directory ready
echo.

REM Step 3: Compile installer
echo [3/3] Compiling installer with Inno Setup...
echo.
"%INNO_SETUP_PATH%" setup.iss
if errorlevel 1 (
    echo.
    echo ERROR: Installer compilation failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

REM Show installer details
echo.
echo ============================================================
echo SUCCESS! Installer created successfully!
echo ============================================================
echo.
echo Output location: installer\CroquisSetup-1.0.1.exe
echo Installer size:
for %%F in ("installer\CroquisSetup-1.0.1.exe") do echo %%~zF bytes
echo.
echo Next steps:
echo 1. Test the installer on a clean system
echo 2. Create SHA256 checksum: Get-FileHash installer\CroquisSetup-1.0.1.exe
echo 3. Upload to GitHub Releases
echo.
pause
