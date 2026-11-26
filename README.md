# JARVIS OS

A local-first Windows desktop assistant with a futuristic interface, offline Vosk speech recognition, queued text-to-speech, safe desktop actions, network reports, and a small local command history.

## Setup
1. Install Python 3.11, 3.12, or 3.13 and make sure `python` works in Command Prompt.
2. Extract this repository.
3. Run `setup.bat`, then `run.bat`.

If setup.bat cannot find the Python launcher, use:
```bat
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Windows Voice Access (no speech-model download)
1. In Windows 11, open **Settings → Accessibility → Speech** and turn on **Voice access**. Complete the first-time setup if Windows asks.
2. Start JARVIS and click **VOICE ACCESS**. This focuses the command box.
3. Use Voice Access to dictate a command, such as "open Roblox" or "show me your network".
4. Say **"press Enter"** using Voice Access to submit the command to JARVIS.

Windows Voice Access is a Windows feature, not a direct speech-recognition API exposed to JARVIS. This mode uses its normal dictation into the focused command field. The separate **VOICE: OFF** listener is the optional Vosk-based offline wake-word feature described below.

### Optional Vosk wake-word listener
1. Run `install_voice.bat` to install the optional speech packages.
2. Download the small English Vosk model from https://alphacephei.com/vosk/models (vosk-model-small-en-us-0.15).
3. Extract it to `models/vosk-model-small-en-us-0.15`.
4. Click **VOICE: OFF** in JARVIS, then say "Jarvis, wake up".
5. JARVIS then accepts repeated commands. Say "go to sleep" to return to wake-word mode.

## Text-to-speech
JARVIS uses pyttsx3 with the Windows speech engine. It speaks command responses through a background queue so the interface remains responsive. If speech is silent, run:
```bat
.venv\Scripts\python.exe -m pip install pyttsx3 pywin32
```

## Example commands
- "Show me your network" / "network status" - opens a report with device name, local IP, adapter IPv4, gateway and DNS lines from Windows ipconfig.
- "What have you learned?" / "show memory" - displays the recent local command history. This is a history log, not AI training.
- "Open Roblox", "launch Notepad", "open Calculator", "open Chrome", "open Paint", "open File Explorer", "open Task Manager", "open Settings".
- "Move forward", "go back", "move left", "move right", "jump", "stop".
- "Help".

## Local memory and privacy
Command history is stored in `jarvis_memory.json` on this PC and capped at the latest 100 commands. It is not uploaded. Do not dictate passwords or other secrets: commands may be recorded in that local history.

## Safety and limitations
JARVIS does not execute arbitrary shell commands, delete files, enter passwords, or bypass security prompts. App launching uses an allowlist. Keyboard control is limited to W/A/S/D/Space and sends input to the focused window. Use STOP to release movement keys. Network reports show local network details; they do not scan other devices or query your public IP.
