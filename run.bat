@echo off
echo ===================================================
echo  Starting Recruiter Candidate Management Application
echo ===================================================

IF NOT EXIST venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Application URL: http://127.0.0.1:8000
echo Swagger API Docs: http://127.0.0.1:8000/docs
echo.

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload