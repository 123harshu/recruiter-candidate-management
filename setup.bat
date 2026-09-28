@echo off
SETLOCAL EnableDelayedExpansion
echo ===================================================
echo  Recruiter Candidate Management Setup Script
echo ===================================================

:: 1. Check Python installation
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not added to PATH.
    echo Please install Python 3.12+ and try again.
    exit /b 1
)

:: 2. Create virtual environment
IF NOT EXIST .venv (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
) ELSE (
    echo Virtual environment (.venv) already exists.
)

:: 3. Activate virtual environment
call .venv\Scripts\activate.bat

:: 4. Upgrade pip and install requirements
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

:: 5. Create required directories
IF NOT EXIST data mkdir data

:: 6. Run database seed
echo Initializing database and running seed script...
python seed.py

:: 7. Run Pytest suite
echo Running automated tests...
pytest

IF %ERRORLEVEL% NEQ 0 (
    echo WARNING: Some tests failed. Please check output.
) ELSE (
    echo ALL TESTS PASSED SUCCESSFULLY!
)

echo.
echo ===================================================
echo  Setup Completed Successfully!
echo  To start the application, run: run.bat
echo ===================================================
pause