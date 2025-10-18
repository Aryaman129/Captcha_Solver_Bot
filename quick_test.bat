@echo off
REM Quick ADB Connection and Device Info Test
REM This verifies your phone is connected and shows device details

echo.
echo ================================================
echo    Quick Connection Test
echo ================================================
echo.

REM Check if ADB is available
if exist "platform-tools\adb.exe" (
    set ADB=platform-tools\adb.exe
) else (
    set ADB=adb
)

echo Testing ADB connection...
echo.

REM Check devices
%ADB% devices -l

echo.
echo ------------------------------------------------

REM Count connected devices
for /f "skip=1 tokens=2" %%i in ('%ADB% devices 2^>nul ^| findstr /r "device$"') do (
    echo [OK] Device found!
    echo.
    
    echo Device Information:
    echo -------------------
    
    REM Get phone model
    for /f "delims=" %%a in ('%ADB% shell getprop ro.product.model 2^>nul') do echo   Model: %%a
    
    REM Get Android version
    for /f "delims=" %%a in ('%ADB% shell getprop ro.build.version.release 2^>nul') do echo   Android: %%a
    
    REM Get screen resolution
    for /f "tokens=3" %%a in ('%ADB% shell wm size 2^>nul ^| findstr "Physical"') do echo   Resolution: %%a
    
    echo.
    echo [OK] Connection successful!
    echo.
    echo Next Steps:
    echo   1. Edit config.json with YOUR app details
    echo   2. Run setup.bat to install dependencies
    echo   3. Run test_solver.bat to test
    echo.
    goto :end
)

echo [ERROR] No devices found!
echo.
echo Troubleshooting:
echo   1. Enable USB Debugging on your phone
echo   2. Connect USB cable
echo   3. Accept USB debugging prompt on phone
echo   4. Try: adb kill-server then adb start-server
echo.

:end
pause
