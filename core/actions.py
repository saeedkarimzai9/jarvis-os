"""Allowlisted Windows actions for the JARVIS starter build."""
from __future__ import annotations

import os
import subprocess
import webbrowser
from typing import Callable

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.04
except Exception:
    pyautogui = None

APP_COMMANDS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"],
    "settings": ["cmd", "/c", "start", "ms-settings:"],
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "roblox": ["cmd", "/c", "start", "", "roblox-player:"],
}
KEYS = {"w": "w", "a": "a", "s": "s", "d": "d", "space": "space"}


class ActionError(Exception):
    pass


class DesktopActions:
    def __init__(self, log: Callable[[str], None] | None = None):
        self.log = log or (lambda message: None)
        self.held: set[str] = set()

    def open_app(self, name: str) -> str:
        key = name.strip().lower()
        if key in {"youtube", "google", "browser"}:
            webbrowser.open("https://www.google.com")
            return "Opening your browser."
        command = APP_COMMANDS.get(key)
        if not command:
            raise ActionError(f"'{name}' isn't in the safe app list yet.")
        subprocess.Popen(command, shell=False)
        return f"Launching {key}."

    def hold_key(self, key: str) -> str:
        normalized = key.lower().strip()
        if normalized not in KEYS:
            raise ActionError("Only W, A, S, D and Space are enabled in this build.")
        if pyautogui is None:
            raise ActionError("Keyboard control needs pyautogui. Run setup.bat again.")
        pyautogui.keyDown(KEYS[normalized])
        self.held.add(KEYS[normalized])
        return f"Holding {normalized.upper()}."

    def release_all(self) -> str:
        if pyautogui is not None:
            try:
                pyautogui.keyUp("w")
                pyautogui.keyUp("a")
                pyautogui.keyUp("s")
                pyautogui.keyUp("d")
                pyautogui.keyUp("space")
            except Exception:
                pass
        self.held.clear()
        return "All movement keys released."

    def execute(self, command: str) -> str:
        text = command.lower().strip().replace(".", "")
        if not text:
            return "I didn't catch a command."
        if text in {"stop", "release", "release keys", "stop moving", "cancel movement"}:
            return self.release_all()
        if text in {"move forward", "forward", "hold w", "press w"}:
            return self.hold_key("w")
        if text in {"move backward", "backward", "back", "hold s", "press s"}:
            return self.hold_key("s")
        if text in {"move left", "left", "hold a", "press a"}:
            return self.hold_key("a")
        if text in {"move right", "right", "hold d", "press d"}:
            return self.hold_key("d")
        if text in {"jump", "hold space", "press space"}:
            return self.hold_key("space")
        if text.startswith("open "):
            return self.open_app(text[5:].strip())
        if text in {"help", "what can you do"}:
            return "I can open allowlisted apps and hold or release W, A, S, D and Space. Try: open Roblox, move forward, jump, or stop."
        raise ActionError("I don't know that command yet. Type 'help' to see supported commands.")
