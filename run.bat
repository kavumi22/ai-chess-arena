@echo off

echo Starting AI Chess Arena...

python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

if not exist requirements.txt (
    echo requirements.txt not found. Please ensure you're in the correct directory.
    pause
    exit /b 1
)

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Launching AI Chess Arena...
python main.py

pause
