@echo off
REM Quick Setup Script for NovaAI Models - Windows

echo.
echo ============================================================
echo NovaAI - Model Setup
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Error: Virtual environment not found
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Activating virtual environment...
echo.

REM Run the Python setup script
echo Running Python setup script...
python setup_models.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Setup script failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Make sure Ollama is running (ollama serve in separate terminal)
echo 2. Start the app with: python -m uvicorn backend.main:app --reload
echo 3. Visit http://127.0.0.1:8000
echo.
pause
