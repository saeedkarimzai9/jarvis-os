@echo off
title JARVIS OS - Setup
cd /d "%~dp0"
echo.
echo  JARVIS OS - INSTALLATION
echo  ========================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python and enable Add Python to PATH.
  pause
  exit /b 1
)
python --version
if not exist .venv (
  python -m venv .venv
  if errorlevel 1 (
    echo Could not create the virtual environment.
    pause
    exit /b 1
  )
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 (
  echo Could not upgrade pip.
  pause
  exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection and error above.
  pause
  exit /b 1
)
echo.
echo Setup complete. Run run.bat to launch JARVIS.
pause
