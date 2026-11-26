"""Optional offline Vosk speech listener. Requires vosk, sounddevice and a model."""
from __future__ import annotations

import json
import os
import threading


class VoiceWorker:
    def __init__(self, on_text, on_log):
        self.on_text = on_text
        self.on_log = on_log
        self.running = False
        self.thread = None
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "vosk-model-small-en-us-0.15")

    def start(self):
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except ImportError as exc:
            raise RuntimeError("Offline voice packages are missing. Run: pip install vosk sounddevice") from exc
        if not os.path.isdir(self.model_path):
            raise RuntimeError("Vosk model not found. Download vosk-model-small-en-us-0.15 and extract it into the models folder. See README.")
        self.running = True

        def listen():
            import queue
            audio_queue = queue.Queue()
            model = Model(self.model_path)
            recognizer = KaldiRecognizer(model, 16000)
            def callback(indata, frames, time_info, status):
                if self.running:
                    audio_queue.put(bytes(indata))
            try:
                with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
                    self.on_log("Microphone active. Say 'Jarvis, wake up'.")
                    awake = False
                    while self.running:
                        data = audio_queue.get()
                        if recognizer.AcceptWaveform(data):
                            result = json.loads(recognizer.Result())
                            spoken = result.get("text", "").strip()
                            if not spoken:
                                continue
                            if not awake:
                                if "jarvis" in spoken and any(word in spoken for word in ("wake", "awake", "hello")):
                                    awake = True
                                    self.on_text("Jarvis, wake up")
                                continue
                            self.on_text(spoken)
                            awake = False
            except Exception as exc:
                self.on_log(f"Microphone error: {exc}")
                self.running = False

        self.thread = threading.Thread(target=listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
