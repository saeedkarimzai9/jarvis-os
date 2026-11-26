"""Safe, local Windows actions and information commands."""
from __future__ import annotations
import os, platform, socket, subprocess, webbrowser
from typing import Callable
from core.memory import remember, summary

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.04
except Exception:
    pyautogui = None

APP_COMMANDS = {
    "notepad": ["notepad.exe"], "calculator": ["calc.exe"], "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"], "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"], "settings": ["cmd", "/c", "start", "ms-settings:"],
    "chrome": ["cmd", "/c", "start", "", "chrome"], "roblox": ["cmd", "/c", "start", "", "roblox-player:"],
}
KEYS = {"w":"w", "a":"a", "s":"s", "d":"d", "space":"space"}

class ActionError(Exception): pass

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
        if normalized not in KEYS: raise ActionError("Only W, A, S, D and Space are enabled.")
        if pyautogui is None: raise ActionError("Keyboard control needs pyautogui. Run setup.bat again.")
        pyautogui.keyDown(KEYS[normalized]); self.held.add(KEYS[normalized])
        return f"Holding {normalized.upper()}."

    def release_all(self) -> str:
        if pyautogui is not None:
            for key in KEYS.values():
                try: pyautogui.keyUp(key)
                except Exception: pass
        self.held.clear()
        return "All movement keys released."

    def network_report(self) -> str:
        host = socket.gethostname()
        try: local_ip = socket.gethostbyname(host)
        except Exception: local_ip = "Unavailable"
        try:
            details = subprocess.check_output(["ipconfig"], text=True, errors="replace", timeout=5)
            useful = [line.strip() for line in details.splitlines() if any(tag in line.lower() for tag in ("adapter", "ipv4", "default gateway", "dns servers"))]
            details = "\n".join(useful[:18]) or "No adapter details found."
        except Exception: details = "Could not read ipconfig."
        return f"NETWORK STATUS\nDevice: {host}\nLocal IP: {local_ip}\n\n{details}\n\nPublic IP is not queried."

    def execute(self, command: str) -> str:
        original = command.strip()
        text = original.lower().strip().replace(".", "").replace("?", "")
        for prefix in ("hey jarvis", "jarvis"):
            if text.startswith(prefix): text = text[len(prefix):].strip(" ,")
        if not text: return "I didn't catch a command."
        if text in {"stop", "release", "release keys", "stop moving", "cancel movement"}: result = self.release_all()
        elif text in {"move forward", "forward", "go forward", "hold w", "press w", "walk forward"}: result = self.hold_key("w")
        elif text in {"move backward", "backward", "back", "go back", "hold s", "press s", "walk backward"}: result = self.hold_key("s")
        elif text in {"move left", "left", "go left", "hold a", "press a"}: result = self.hold_key("a")
        elif text in {"move right", "right", "go right", "hold d", "press d"}: result = self.hold_key("d")
        elif text in {"jump", "hold space", "press space"}: result = self.hold_key("space")
        elif text.startswith("open ") or text.startswith("launch "): result = self.open_app(text.split(" ", 1)[1].strip())
        elif any(p in text for p in ("show me your network", "show network", "network status", "network information", "what is my ip")): result = self.network_report()
        elif any(p in text for p in ("what have you learned", "what do you remember", "show memory", "show what you learned")): result = summary()
        elif text in {"help", "what can you do", "commands"}:
            result = "I can launch allowlisted apps, control W/A/S/D/Space, show network details, and report my local command history. Say 'go to sleep' to pause voice commands, or 'stop' to release movement keys."
        elif text in {"go to sleep", "sleep", "stop listening"}: result = "Voice command received. Use the wake phrase to activate me again."
        else: raise ActionError("I don't know that yet. Try 'show me your network', 'what have you learned', 'open Roblox', 'move forward', or 'help'.")
        remember(original, result)
        return result
