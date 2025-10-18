@echo off
REM Check ADB Connection Script
REM Verifies that ADB can see your Android device

echo ===============================================
echo    ADB Connection Checker
echo ===============================================
echo.

REM Check if ADB is installed
where adb >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ADB is not installed or not in PATH
    echo.
    echo Please install ADB from:
    echo https://developer.android.com/tools/releases/platform-tools
    echo.
    echo Or use the platform-tools folder in this project
    pause
    exit /b 1
)

echo [OK] ADB is installed
echo.

REM Check for connected devices
echo Checking for connected devices...
echo.
adb devices
echo.

REM Check if any device is connected
adb devices | findstr /R "device$" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No devices connected!
    echo.
    echo For USB Connection:
    echo   1. Connect your phone via USB cable
    echo   2. Enable USB Debugging in Developer Options
    echo   3. Accept the USB debugging prompt on your phone
    echo.
    echo For Wireless Connection:
    echo   1. Connect phone via USB first
    echo   2. Run: adb tcpip 5555
    echo   3. Find your phone's IP: Settings ^> About Phone ^> Status ^> IP Address
    echo   4. Run: adb connect YOUR_PHONE_IP:5555
    echo   5. Disconnect USB cable
    echo.
    pause
    exit /b 1
)

echo [OK] Device(s) connected successfully!
echo.
echo Device details:
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
echo.

echo ===============================================
echo    Connection Check Complete!
echo ===============================================
echo.
echo You can now run the CAPTCHA solver.
echo.
pause
