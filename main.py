from __future__ import annotations

import sys
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
)

from core.actions import DesktopActions, ActionError


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS OS")
        self.resize(1100, 720)
        self.setMinimumSize(850, 580)
        self.actions = DesktopActions()
        self.voice_active = False
        self._build_ui()
        self._clock = QTimer(self)
        self._clock.timeout.connect(self.update_clock)
        self._clock.start(1000)
        self.update_clock()
        self.log("SYSTEM ONLINE. Local command engine ready.")
        self.log("Type 'help' to see what I can do.")

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(28, 22, 28, 24)
        outer.setSpacing(16)

        top = QHBoxLayout()
        brand = QLabel("J A R V I S  <span style='color:#6ee7ff'>/ OS</span>")
        brand.setObjectName("brand")
        top.addWidget(brand)
        top.addStretch()
        self.clock_label = QLabel()
        self.clock_label.setObjectName("clock")
        top.addWidget(self.clock_label)
        outer.addLayout(top)

        hero = QFrame()
        hero.setObjectName("hero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(22, 18, 22, 18)
        status_row = QHBoxLayout()
        self.status = QLabel("● SYSTEM READY")
        self.status.setObjectName("status")
        status_row.addWidget(self.status)
        status_row.addStretch()
        self.mode = QLabel("LOCAL CONTROL // SAFE MODE")
        self.mode.setObjectName("muted")
        status_row.addWidget(self.mode)
        hero_layout.addLayout(status_row)

        centre = QVBoxLayout()
        centre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb = QLabel("◉")
        self.orb.setObjectName("orb")
        self.orb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        centre.addWidget(self.orb)
        title = QLabel("HOW CAN I HELP?")
        title.setObjectName("hero_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        centre.addWidget(title)
        subtitle = QLabel("VOICE-CONTROLLED DESKTOP INTERFACE")
        subtitle.setObjectName("muted")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        centre.addWidget(subtitle)
        hero_layout.addLayout(centre)
        outer.addWidget(hero, 3)

        cards = QHBoxLayout()
        cards.setSpacing(12)
        for heading, detail in [
            ("DESKTOP", "Launch apps and tools"),
            ("GAME INPUT", "W / A / S / D + Space"),
            ("VOICE", "Optional offline wake word"),
        ]:
            card = QFrame()
            card.setObjectName("card")
            lay = QVBoxLayout(card)
            h = QLabel(heading)
            h.setObjectName("card_title")
            d = QLabel(detail)
            d.setObjectName("muted")
            lay.addWidget(h)
            lay.addWidget(d)
            cards.addWidget(card)
        outer.addLayout(cards)

        console_frame = QFrame()
        console_frame.setObjectName("console")
        console_layout = QVBoxLayout(console_frame)
        console_layout.setContentsMargins(14, 12, 14, 12)
        console_head = QHBoxLayout()
        console_title = QLabel("ACTIVITY LOG")
        console_title.setObjectName("card_title")
        console_head.addWidget(console_title)
        console_head.addStretch()
        voice_btn = QPushButton("VOICE: OPTIONAL")
        voice_btn.clicked.connect(self.toggle_voice)
        console_head.addWidget(voice_btn)
        console_layout.addLayout(console_head)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(145)
        self.console.setObjectName("console_text")
        console_layout.addWidget(self.console)
        outer.addWidget(console_frame, 2)

        command_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a command…  e.g. open Roblox  |  move forward  |  stop")
        self.input.returnPressed.connect(self.run_command)
        command_row.addWidget(self.input, 1)
        send = QPushButton("EXECUTE  ↗")
        send.setObjectName("execute")
        send.clicked.connect(self.run_command)
        command_row.addWidget(send)
        stop = QPushButton("STOP")
        stop.setObjectName("stop")
        stop.clicked.connect(self.emergency_stop)
        command_row.addWidget(stop)
        outer.addLayout(command_row)

        self.setStyleSheet("""
            QWidget#root { background:#070b14; color:#d9f5ff; font-family:'Segoe UI'; }
            QLabel#brand { color:#eafaff; font-size:22px; font-weight:700; letter-spacing:3px; }
            QLabel#clock { color:#7e9aaa; font-size:13px; }
            QFrame#hero { background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #101e31,stop:1 #0b1220); border:1px solid #1b5367; border-radius:18px; }
            QLabel#status { color:#65f5c1; font-size:12px; font-weight:700; letter-spacing:2px; }
            QLabel#muted { color:#7292a5; font-size:11px; letter-spacing:1px; }
            QLabel#orb { color:#6ee7ff; font-size:100px; padding:8px; }
            QLabel#hero_title { color:#effcff; font-size:24px; font-weight:600; letter-spacing:5px; }
            QFrame#card, QFrame#console { background:#0c1421; border:1px solid #1b3043; border-radius:12px; }
            QLabel#card_title { color:#6ee7ff; font-size:12px; font-weight:700; letter-spacing:2px; }
            QTextEdit#console_text { background:#080e18; border:0; color:#9dd9e8; font-family:Consolas; font-size:12px; }
            QLineEdit { background:#0c1725; border:1px solid #24516a; border-radius:9px; padding:14px; color:#eaffff; font-size:14px; }
            QPushButton { background:#14283a; border:1px solid #28617a; border-radius:9px; padding:12px 16px; color:#bdefff; font-weight:700; }
            QPushButton:hover { background:#1b3b52; }
            QPushButton#execute { background:#087e9e; color:white; border:0; }
            QPushButton#stop { background:#642c3b; color:#ffe2e8; border:1px solid #a44b60; }
        """)

    def update_clock(self):
        self.clock_label.setText(datetime.now().strftime("%a %d %b  %H:%M:%S"))

    def log(self, message: str):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{stamp}]  {message}")

    def run_command(self):
        command = self.input.text().strip()
        if not command:
            return
        self.log(f"> {command}")
        try:
            result = self.actions.execute(command)
            self.log(f"JARVIS: {result}")
            self.status.setText("● COMMAND COMPLETE")
        except ActionError as exc:
            self.log(f"JARVIS: {exc}")
            self.status.setText("● COMMAND NOT RECOGNISED")
        except Exception as exc:
            self.log(f"SYSTEM ERROR: {exc}")
            self.status.setText("● CHECK LOG")
        self.input.clear()

    def emergency_stop(self):
        result = self.actions.release_all()
        self.log(f"EMERGENCY STOP: {result}")
        self.status.setText("● INPUT RELEASED")

    def toggle_voice(self):
        try:
            from core.voice import VoiceWorker
            if self.voice_active:
                self.voice_worker.stop()
                self.voice_active = False
                self.status.setText("● SYSTEM READY")
                self.log("Voice listener stopped.")
                return
            self.voice_worker = VoiceWorker(self.handle_voice_text, self.log)
            self.voice_worker.start()
            self.voice_active = True
            self.status.setText("● VOICE LISTENER STARTING")
        except Exception as exc:
            QMessageBox.information(self, "Voice setup", str(exc) + "\n\nTyped commands still work. See README for offline voice setup.")
            self.log(f"VOICE: {exc}")

    def handle_voice_text(self, text: str):
        self.log(f"VOICE: {text}")
        if "jarvis" in text.lower() and any(w in text.lower() for w in ("wake", "awake", "hello")):
            self.status.setText("● JARVIS AWAKE")
            self.log("JARVIS: I'm awake. Listening for a command.")
        else:
            self.input.setText(text)
            self.run_command()

    def closeEvent(self, event):
        self.actions.release_all()
        if self.voice_active:
            try:
                self.voice_worker.stop()
            except Exception:
                pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS OS")
    app.setFont(QFont("Segoe UI", 10))
    window = JarvisWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
