@echo off
echo.
echo ╔══════════════════════════════════════════╗
echo ║     AI-IDS Windows Installer            ║
echo ╚══════════════════════════════════════════╝
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.10+
    echo https://python.org
    pause
    exit
)

echo.
echo Running setup...
python setup.py

echo.
echo ✅ Done! AI-IDS will start on next boot.
echo To start now: python start_ids.py
pause