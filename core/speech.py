"""Queued Windows text-to-speech using pyttsx3."""
from __future__ import annotations
import queue
import threading

class SpeechEngine:
    def __init__(self):
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def say(self, text: str) -> None:
        if text:
            self.queue.put(str(text)[:700])

    def _worker(self):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 0.9)
            while True:
                text = self.queue.get()
                if text is None:
                    break
                try:
                    engine.say(text)
                    engine.runAndWait()
                except Exception:
                    pass
        except Exception:
            # GUI and text commands remain usable if TTS is unavailable.
            return
