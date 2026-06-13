@echo off
title BookletsGo Windows Executable Builder
cls

echo ====================================================
echo             BookletsGo Build Automation
echo ====================================================
echo.

:: 1. CHECK: Are we already in an active venv?
:: ------------------------------------------------------
if defined VIRTUAL_ENV (
    echo [INFO] An active virtual environment was detected.
    echo        Path: %VIRTUAL_ENV%
    echo.
    set "SHOULD_DEACTIVATE=0"
) else (
    echo [INFO] No active virtual environment detected. Attempting activation...

    :: Check if the venv folder and the activation file exist
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
        set "SHOULD_DEACTIVATE=1"
        echo [SUCCESS] Virtual environment activated successfully.
        echo.
    ) else (
        echo [ERROR] The folder '.venv\Scripts\activate.bat' was not found!
        echo         Make sure to run this script from the project root directory.
        echo.
        goto ERROR_EXIT
    )
)

:: 2. EXECUTION: Run PyInstaller
:: ------------------------------------------------------
echo [BUILD] Launching PyInstaller compilation...
echo.

pyinstaller --noconsole --onedir --collect-all customtkinter --icon=assets/bookletsgo.ico --add-data "assets/bookletsgo.ico;assets" --add-data "assets/Inter-Regular.ttf;assets" --name BookletsGo run.py

:: Check if PyInstaller ran successfully (returned with error code 0)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] PyInstaller encountered an error during compilation!
    goto ERROR_EXIT
)

echo.
echo [SUCCESS] Compilation completed successfully. Target: /dist/BookletsGo/
echo.

:: 3. EXIT: Venv deactivate (only if we entered)
:: ------------------------------------------------------
if "%SHOULD_DEACTIVATE%"=="1" (
    echo [INFO] Deactivating the temporary virtual environment session...
    call deactivate
)

echo.
echo ====================================================
echo   Done! You can close this window.
echo ====================================================
pause
exit /b 0

:ERROR_EXIT
echo ====================================================
echo   BUILD FAILED! Please check the error messages above.
echo ====================================================
pause
exit /b 1
