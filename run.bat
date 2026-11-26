@echo off
title JARVIS OS
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python main.py
if errorlevel 1 (
  echo.
  echo JARVIS stopped with an error. Read the message above.
  pause
)
