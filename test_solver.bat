@echo off
REM Test CAPTCHA Solver (Solves ONE captcha only)

echo ===============================================
echo    CAPTCHA Solver - Test Mode
echo ===============================================
echo.
echo This will solve ONE captcha to test the setup
echo.

REM Activate virtual environment
if exist "captcha_env\Scripts\activate.bat" (
    call captcha_env\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found
    echo Run setup.bat first
    pause
    exit /b 1
)

echo Running test...
echo.

REM Run in test mode
python src\captcha_solver_adb.py --test

echo.
echo Test complete!
echo Check the logs folder for details
pause
