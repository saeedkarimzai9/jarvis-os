"""Small local history of commands JARVIS has handled. No cloud or model training."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

PATH = Path(__file__).resolve().parent.parent / "jarvis_memory.json"

def remember(command: str, result: str) -> None:
    try:
        data = json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else []
        data.append({"time": datetime.now().isoformat(timespec="seconds"), "command": command[:200], "result": result[:300]})
        PATH.write_text(json.dumps(data[-100:], indent=2), encoding="utf-8")
    except Exception:
        pass

def summary() -> str:
    try:
        data = json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else []
    except Exception:
        data = []
    if not data:
        return "I haven't saved any command history yet. I can remember the last 100 commands handled on this PC."
    recent = data[-8:]
    lines = [f"Local command history: {len(data)} entries saved (maximum 100)."]
    lines.extend(f"- {item.get('time','')}: {item.get('command','')}" for item in recent)
    return "\n".join(lines) + "\nThis is local history, not model training or human-like learning."
