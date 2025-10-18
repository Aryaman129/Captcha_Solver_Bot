@echo off
REM Run CAPTCHA Solver with Virtual Display (scrcpy)

echo ===============================================
echo    CAPTCHA Solver - Virtual Display Mode
echo ===============================================
echo.
echo This mode will:
echo   - Turn OFF your phone screen
echo   - Run in the background
echo   - Keep your phone display hidden
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

echo Starting CAPTCHA solver with virtual display...
echo Press Ctrl+C to stop
echo.

REM Run the virtual display solver
python src\captcha_solver_virtual.py %*

echo.
echo Solver stopped.
pause
