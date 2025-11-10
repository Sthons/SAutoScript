@echo off
chcp 65001 >nul

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment does not exist, creating...
    call python install.py
    if errorlevel 1 (
        echo Installation failed, please check error messages
        pause
        exit /b 1
    )
)

REM Check if command line argument is provided
if not defined choice (
    echo ========================================
    echo DNAAS Game Auto Script System
    echo ========================================
    echo.
    echo 1. Run example script
echo 2. Run template script
echo 3. Run main program
echo 4. Run window locator example
echo 5. Run template example (BaseGameScript)
echo 6. Run error logging example
echo 7. Reinstall dependencies
echo 8. Exit
echo.
set /p "choice=Please select an option (1-8):"
) else (
    echo Running option %choice%...
)

if "%choice%"=="1" (
    echo Running example script...
    .venv\Scripts\python scripts\example.py
) else if "%choice%"=="2" (
    echo Running template script...
    .venv\Scripts\python scripts\template.py
) else if "%choice%"=="3" (
    echo Running main program...
    .venv\Scripts\python main.py
) else if "%choice%"=="4" (
    echo Running window locator example...
    .venv\Scripts\python scripts\window_locator_example.py
) else if "%choice%"=="5" (
    echo Running template example (BaseGameScript)...
    .venv\Scripts\python scripts\template_example.py
) else if "%choice%"=="6" (
    echo Running error logging example...
    .venv\Scripts\python scripts\error_logging_example.py
) else if "%choice%"=="7" (
    echo Reinstalling dependencies...
    call python install.py
) else if "%choice%"=="8" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid selection, please run the script again
    pause
)

REM Only pause if no command line argument was provided
if "%1"=="" pause