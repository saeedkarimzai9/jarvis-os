@echo off
title JARVIS OS - Offline Voice Setup
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pip install vosk sounddevice
if not exist models mkdir models
echo.
echo Voice packages installed.
echo Download vosk-model-small-en-us-0.15 from https://alphacephei.com/vosk/models
echo Extract it into: %CD%\models\vosk-model-small-en-us-0.15
pause
