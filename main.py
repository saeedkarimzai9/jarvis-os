from __future__ import annotations
import sys
from datetime import datetime
from PySide6.QtCore import Qt, QTimer, QObject, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget, QDialog
)
from core.actions import DesktopActions, ActionError
from core.speech import SpeechEngine

class VoiceBridge(QObject):
    text = Signal(str)
    log = Signal(str)

class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS OS")
        self.resize(1100, 720)
        self.setMinimumSize(850, 580)
        self.actions = DesktopActions()
        self.voice_active = False
        self.voice_bridge = VoiceBridge()
        self.voice_bridge.text.connect(self.handle_voice_text)
        self.voice_bridge.log.connect(self.log)
        self.speech = SpeechEngine()
        self._build_ui()
        self._clock = QTimer(self)
        self._clock.timeout.connect(self.update_clock)
        self._clock.start(1000)
        self.update_clock()
        self.log("SYSTEM ONLINE. Local command engine ready.")
        self.log("Say 'Jarvis, wake up' then speak commands, or type 'help'.")

    def _build_ui(self):
        root = QWidget(); root.setObjectName("root"); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(28,22,28,24); outer.setSpacing(16)
        top = QHBoxLayout()
        brand = QLabel("J A R V I S  <span style='color:#6ee7ff'>/ OS</span>"); brand.setObjectName("brand")
        top.addWidget(brand); top.addStretch()
        self.clock_label = QLabel(); self.clock_label.setObjectName("clock"); top.addWidget(self.clock_label)
        outer.addLayout(top)
        hero = QFrame(); hero.setObjectName("hero"); hero_layout = QVBoxLayout(hero); hero_layout.setContentsMargins(22,18,22,18)
        status_row = QHBoxLayout()
        self.status = QLabel("● SYSTEM READY"); self.status.setObjectName("status"); status_row.addWidget(self.status); status_row.addStretch()
        self.mode = QLabel("LOCAL CONTROL // SAFE MODE"); self.mode.setObjectName("muted"); status_row.addWidget(self.mode)
        hero_layout.addLayout(status_row)
        centre = QVBoxLayout(); centre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb = QLabel("◉"); self.orb.setObjectName("orb"); self.orb.setAlignment(Qt.AlignmentFlag.AlignCenter); centre.addWidget(self.orb)
        title = QLabel("HOW CAN I HELP?"); title.setObjectName("hero_title"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); centre.addWidget(title)
        subtitle = QLabel("VOICE-CONTROLLED DESKTOP INTERFACE"); subtitle.setObjectName("muted"); subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter); centre.addWidget(subtitle)
        hero_layout.addLayout(centre); outer.addWidget(hero,3)
        cards = QHBoxLayout(); cards.setSpacing(12)
        for heading,detail in [("DESKTOP","Launch apps and tools"),("GAME INPUT","W / A / S / D + Space"),("VOICE","Wake word + continuous commands"),("INTELLIGENCE","Network + local memory")]:
            card=QFrame(); card.setObjectName("card"); lay=QVBoxLayout(card)
            h=QLabel(heading); h.setObjectName("card_title"); d=QLabel(detail); d.setObjectName("muted")
            lay.addWidget(h); lay.addWidget(d); cards.addWidget(card)
        outer.addLayout(cards)
        console_frame=QFrame(); console_frame.setObjectName("console"); console_layout=QVBoxLayout(console_frame); console_layout.setContentsMargins(14,12,14,12)
        console_head=QHBoxLayout(); console_title=QLabel("ACTIVITY LOG"); console_title.setObjectName("card_title"); console_head.addWidget(console_title); console_head.addStretch()
        voice_btn=QPushButton("VOICE: OFF"); voice_btn.clicked.connect(self.toggle_voice); self.voice_btn=voice_btn; console_head.addWidget(voice_btn)
        console_layout.addLayout(console_head)
        self.console=QTextEdit(); self.console.setReadOnly(True); self.console.setMaximumHeight(145); self.console.setObjectName("console_text"); console_layout.addWidget(self.console)
        outer.addWidget(console_frame,2)
        command_row=QHBoxLayout(); self.input=QLineEdit()
        self.input.setPlaceholderText("Try: show me your network | what have you learned | open Roblox")
        self.input.returnPressed.connect(self.run_command); command_row.addWidget(self.input,1)
        send=QPushButton("EXECUTE  ↗"); send.setObjectName("execute"); send.clicked.connect(self.run_command); command_row.addWidget(send)
        access=QPushButton("VOICE ACCESS"); access.clicked.connect(self.prepare_voice_access); command_row.addWidget(access)
        stop=QPushButton("STOP"); stop.setObjectName("stop"); stop.clicked.connect(self.emergency_stop); command_row.addWidget(stop)
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

    def log(self,message:str):
        stamp=datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{stamp}]  {message}")

    def show_report(self,title:str,content:str):
        dialog=QDialog(self); dialog.setWindowTitle("JARVIS // "+title); dialog.resize(680,480)
        layout=QVBoxLayout(dialog); heading=QLabel(title.upper()); heading.setStyleSheet("color:#6ee7ff;font-size:16px;font-weight:700;")
        view=QTextEdit(); view.setReadOnly(True); view.setPlainText(content)
        view.setStyleSheet("background:#080e18;color:#bdefff;border:1px solid #24516a;font-family:Consolas;font-size:12px;padding:12px;")
        close=QPushButton("CLOSE"); close.clicked.connect(dialog.accept)
        layout.addWidget(heading); layout.addWidget(view,1); layout.addWidget(close); dialog.exec()

    def run_command(self):
        command=self.input.text().strip()
        if not command: return
        self.log(f"> {command}")
        try:
            result=self.actions.execute(command)
            self.log("JARVIS: "+result.replace("\n"," | "))
            self.status.setText("● COMMAND COMPLETE")
            self.speech.say(result.splitlines()[0])
            low=command.lower()
            if any(term in low for term in ("network","ip address","what have you learned","what do you remember","show memory","learned")):
                self.show_report("Network report" if "network" in low or "ip address" in low else "Local memory",result)
        except ActionError as exc:
            self.log(f"JARVIS: {exc}"); self.status.setText("● COMMAND NOT RECOGNISED"); self.speech.say(str(exc))
        except Exception as exc:
            self.log(f"SYSTEM ERROR: {exc}"); self.status.setText("● CHECK LOG")
        self.input.clear()

    def prepare_voice_access(self):
        """Prepare the command box for Windows Voice Access dictation."""
        self.input.setFocus()
        self.status.setText("● READY FOR WINDOWS VOICE ACCESS")
        self.log("VOICE ACCESS: Dictate a command into the command box, then say 'press Enter'.")
        self.speech.say("Command box ready. Dictate your command, then say press enter.")

    def emergency_stop(self):
        result=self.actions.release_all(); self.log("EMERGENCY STOP: "+result); self.status.setText("● INPUT RELEASED"); self.speech.say("Movement keys released.")

    def toggle_voice(self):
        try:
            from core.voice import VoiceWorker
            if self.voice_active:
                self.voice_worker.stop(); self.voice_active=False; self.voice_btn.setText("VOICE: OFF")
                self.status.setText("● SYSTEM READY"); self.log("Voice listener stopped."); self.speech.say("Voice listener stopped.")
                return
            self.voice_worker=VoiceWorker(self.voice_bridge.text.emit,self.voice_bridge.log.emit)
            self.voice_worker.start(); self.voice_active=True; self.voice_btn.setText("VOICE: ON")
            self.status.setText("● VOICE LISTENER STARTING"); self.speech.say("Voice systems online. Say Jarvis, wake up.")
        except Exception as exc:
            QMessageBox.information(self,"Voice setup",str(exc)+"\n\nTyped commands still work.")
            self.log(f"VOICE: {exc}")

    def handle_voice_text(self,text:str):
        self.log("VOICE: "+text)
        low=text.lower()
        if "jarvis" in low and any(w in low for w in ("wake","awake","hello")):
            self.status.setText("● JARVIS AWAKE"); self.log("JARVIS: I'm awake. Listening for commands."); self.speech.say("I'm awake. How can I help?")
        else:
            self.input.setText(text); self.run_command()

    def closeEvent(self,event):
        self.actions.release_all()
        if self.voice_active:
            try: self.voice_worker.stop()
            except Exception: pass
        event.accept()

def main():
    app=QApplication(sys.argv); app.setApplicationName("JARVIS OS"); app.setFont(QFont("Segoe UI",10))
    window=JarvisWindow(); window.show(); sys.exit(app.exec())

if __name__=="__main__": main()
