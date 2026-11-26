@echo off
title JARVIS OS - Setup
cd /d "%~dp0"
echo.
echo  JARVIS OS - INSTALLATION
echo  ========================
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 or 3.12 from python.org
  echo Make sure "Add Python to PATH" is checked.
  pause
  exit /b 1
)
if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete. Run run.bat to launch JARVIS.
pause
