@echo off
REM Setup Script for CAPTCHA Solver
REM Installs required Python packages and checks dependencies

echo ===============================================
echo    CAPTCHA Solver - Setup Script
echo ===============================================
echo.

REM Check Python
python --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if virtual environment exists
if exist "captcha_env\" (
    echo [INFO] Virtual environment already exists
    echo Activating virtual environment...
    call captcha_env\Scripts\activate.bat
) else (
    echo [INFO] Creating virtual environment...
    python -m venv captcha_env
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo Activating virtual environment...
    call captcha_env\Scripts\activate.bat
)

echo.
echo [INFO] Installing required packages...
echo This may take a few minutes...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install packages
    pause
    exit /b 1
)

echo.
echo ===============================================
echo    Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo   1. Run check_connection.bat to verify ADB connection
echo   2. Edit config.json to set your CAPTCHA app details
echo   3. Run run_solver.bat to start solving CAPTCHAs
echo.
pause
