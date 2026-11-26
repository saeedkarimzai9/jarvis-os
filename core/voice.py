"""Offline Vosk listener. Wake once, then accept repeated commands until told to sleep."""
from __future__ import annotations
import json, os, threading

class VoiceWorker:
    def __init__(self, on_text, on_log):
        self.on_text, self.on_log = on_text, on_log
        self.running = False
        self.thread = None
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "vosk-model-small-en-us-0.15")

    def start(self):
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except ImportError as exc:
            raise RuntimeError("Offline voice packages are missing. Run install_voice.bat.") from exc
        if not os.path.isdir(self.model_path):
            raise RuntimeError("Vosk model not found in the models folder.")
        self.running = True
        def listen():
            import queue
            audio_queue = queue.Queue()
            try:
                model = Model(self.model_path)
                recognizer = KaldiRecognizer(model, 16000)
                def callback(indata, frames, time_info, status):
                    if self.running: audio_queue.put(bytes(indata))
                with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
                    self.on_log("Microphone active. Say 'Jarvis, wake up'.")
                    awake = False
                    while self.running:
                        data = audio_queue.get()
                        if recognizer.AcceptWaveform(data):
                            spoken = json.loads(recognizer.Result()).get("text", "").strip()
                            if not spoken: continue
                            if not awake:
                                if "jarvis" in spoken and any(w in spoken for w in ("wake", "awake", "hello")):
                                    awake = True
                                    self.on_text("Jarvis, wake up")
                                    self.on_log("JARVIS awake. Listening for repeated commands.")
                                continue
                            self.on_text(spoken)
                            if any(phrase in spoken for phrase in ("go to sleep", "stop listening")):
                                awake = False
                                self.on_log("Voice paused. Say 'Jarvis, wake up' to resume.")
            except Exception as exc:
                self.on_log(f"Microphone error: {exc}")
                self.running = False
        self.thread = threading.Thread(target=listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
