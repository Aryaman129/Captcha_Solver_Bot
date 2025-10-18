@echo off
REM Run CAPTCHA Solver (Standard ADB Mode)

echo ===============================================
echo    CAPTCHA Solver - Standard Mode
echo ===============================================
echo.

REM Activate virtual environment
if exist "captcha_env\Scripts\activate.bat" (
    call captcha_env\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found
    echo Run setup.bat first to install dependencies
    pause
    exit /b 1
)

echo Starting CAPTCHA solver...
echo Press Ctrl+C to stop
echo.

REM Run the solver
python src\captcha_solver_adb.py %*

echo.
echo Solver stopped.
pause
