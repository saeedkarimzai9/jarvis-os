# JARVIS OS

A local-first, voice-controlled Windows desktop assistant with a futuristic control-panel interface.

## Quick start (Windows 10/11)
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/windows/ and tick **Add Python to PATH**.
2. Download this repository as a ZIP and extract it, or clone it with Git.
3. Double-click **setup.bat** once.
4. Double-click **run.bat** whenever you want to launch JARVIS.

Manual setup:
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Voice activation (optional, offline)
1. Run **install_voice.bat**.
2. Download the small English Vosk model from https://alphacephei.com/vosk/models (vosk-model-small-en-us-0.15).
3. Extract the model so this folder exists: `models/vosk-model-small-en-us-0.15`.
4. Launch JARVIS and click **VOICE: OPTIONAL**.
5. Say **“Jarvis, wake up”**, then speak one supported command.

If voice is not installed/configured, typed commands still work.

## Supported commands
- `open Roblox`, `open Notepad`, `open Calculator`, `open Chrome`, `open Paint`, `open File Explorer`, `open Task Manager`, `open Settings`
- `move forward` / `hold W`
- `move backward` / `hold S`
- `move left` / `hold A`
- `move right` / `hold D`
- `jump` / `hold space`
- `stop` / `release keys`
- `help`

For game controls, click/focus the game first. **STOP** releases all movement keys. Keyboard control is intentionally restricted to W/A/S/D/Space.

## Safety and limitations
This is the first working foundation, not a full autonomous AI operating system yet. It does not run arbitrary terminal commands, delete files, enter passwords, or bypass security prompts. App launching uses an allowlist. The focused window receives movement keys, so check which window is active before issuing movement commands. Respect game rules and terms.

## Troubleshooting
- If the app does not open, run `run.bat` from Command Prompt and read the error.
- If Python is not found, reinstall Python and enable **Add Python to PATH**.
- If voice fails, check Windows microphone privacy permissions and confirm the Vosk model folder is named exactly as shown above.
