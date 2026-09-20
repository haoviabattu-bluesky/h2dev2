"""satori_render_gui.py — GUI tool làm video YouTube faceless "NÃO = CLAUDE" (mọi ngách) → .exe.

KHÁC tool full-ramcloud (tab a3): tool NÀY dùng CLAUDE làm bộ não (chạy trên máy CÓ Claude Code). Luồng:
  1) dán URL/@handle KÊNH đối thủ → QUÉT VIDEO (tên · view · thời lượng)
  2) tick chọn video (hoặc chạy tất cả)
  3) [tuỳ chọn] PHÂN TÍCH GIỌNG: mỗi video tự nhận người kể (nam/nữ·già/trẻ) → chọn giọng khớp (khác nhau)
  4) RENDER: mỗi video → cào transcript → Claude viết kịch bản+prompt+master (tự QC/sửa) →
     gpt-image-2 sinh ảnh · ElevenLabs đọc · Gemini QC · ffmpeg ghép.

GUI mỏng: gọi pipeline/brain_channel.py (+ channel_scan.py) bằng py-3.13 của máy (config.json). Nút DỪNG
taskkill cả cây. Xem skill tao_tool_exe.md (#20 selftest · #21 BASE · #24 taskkill cây · #26 QSS app-level).

Chạy: py satori_render_gui.py   |   Build: build_satori_gui.bat   |   Smoke: "H2Dev Render.exe" --selftest
"""
import io
import json
import os
import re
import subprocess
import sys
import traceback

if sys.stdout and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

CONFIG = os.path.join(BASE, "satori_gui_config.json")
DEFAULT_CFG = {"project_root": r"E:\CLAUDE\YOUTUBE\h2dev", "python_cmd": ["py", "-3.13"],
               "profile": "satori-jp-obaa"}


def load_cfg():
    try:
        c = json.loads(open(CONFIG, encoding="utf-8").read())
        return {**DEFAULT_CFG, **c}
    except Exception:
        return dict(DEFAULT_CFG)


def pipeline_dir(cfg):
    return os.path.join(cfg["project_root"], "pipeline")


def selftest():
    out = []
    try:
        cfg = load_cfg()
        root = cfg["project_root"]
        pdir = pipeline_dir(cfg)
        out += [f"BASE = {BASE}", f"frozen = {getattr(sys,'frozen',False)}",
                f"config = {CONFIG} (exists={os.path.exists(CONFIG)})",
                f"project_root = {root} (exists={os.path.isdir(root)})",
                f"python_cmd = {cfg['python_cmd']}"]
        for f in ("brain_channel.py", "channel_scan.py", "detect_voice.py", "brain_steps.py",
                  "render_engine.py"):
            p = os.path.join(pdir, f)
            out.append(f"{f} = {'CÓ' if os.path.exists(p) else 'THIẾU'}  ({p})")
        import shutil
        out.append(f"claude CLI = {shutil.which('claude') or shutil.which('claude.cmd') or '(KHÔNG THẤY — cần Claude Code)'}")
        import PySide6
        out.append(f"PySide6 OK {PySide6.__version__}")
        out.append("SELFTEST OK")
    except Exception as e:
        out.append(f"SELFTEST LỖI: {e}\n{traceback.format_exc()}")
    open(os.path.join(BASE, "selftest.log"), "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out))
    return 0


if "--selftest" in sys.argv:
    sys.exit(selftest())

import ctypes
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("H2Dev.VideoRender.1")
except Exception:
    pass

# ẨN CMD: exe --windowed KHÔNG có console → mỗi tiến trình con console (claude -p, py pipeline) và
# cháu của nó (shell claude gọi) bị Windows cấp 1 console MỚI HIỆN RA = "đống cmd". Cấp cho GUI 1
# console rồi ẩn hẳn ngay từ đầu: mọi con/cháu KẾ THỪA console ẩn này → không cửa sổ nào bật.
# (bỏ CREATE_NO_WINDOW ở các lệnh con để chúng kế thừa, không tự tạo console mới.)
try:
    _k32 = ctypes.windll.kernel32
    if not _k32.GetConsoleWindow():
        _k32.AllocConsole()
        ctypes.windll.user32.ShowWindow(_k32.GetConsoleWindow(), 0)   # SW_HIDE
except Exception:
    pass

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QPlainTextEdit, QProgressBar, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QComboBox)

QSS = """
* { font-family: "Segoe UI"; color: #e6f0ff; font-size: 12px; }
QMainWindow, QWidget { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0a1628, stop:1 #0d1f3a); }
QLabel#title { font-size: 17px; font-weight: 700; color: #7cc0ff; }
QLineEdit, QComboBox { background:#0e1f3c; border:1px solid #1f3a64; border-radius:8px; padding:0 12px; min-height:34px; }
QLineEdit:focus, QComboBox:focus { border:1px solid #2da0ff; }
QPlainTextEdit { background:#08152b; border:1px solid #1f3a64; border-radius:8px; font-family:Consolas; font-size:11px; }
QPushButton { background:#12294d; border:1px solid #244a80; border-radius:8px; padding:0 16px; min-height:34px; font-weight:600; }
QPushButton:hover { background:#183463; }
QPushButton#scan { background:#154a7a; border:none; color:white; font-weight:700; }
QPushButton#run { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #1e8fff, stop:1 #2da0ff); border:none; color:white; min-height:40px; font-size:13px; font-weight:700; }
QPushButton#stop { background:#7a1f2b; border:none; color:white; }
QPushButton:disabled { background:#16233a; color:#5a6b85; }
QProgressBar { background:#0e1f3c; border:1px solid #1f3a64; border-radius:8px; min-height:20px; text-align:center; }
QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #1e8fff, stop:1 #38d39f); border-radius:7px; }
QTableWidget { background:#08152b; border:1px solid #1f3a64; border-radius:8px; gridline-color:#16294a; }
QHeaderView::section { background:#12294d; color:#9fd0ff; border:none; padding:6px; font-weight:600; }
QTableWidget::item:selected { background:#1b3a68; }
QCheckBox { spacing:8px; }
"""


class Worker(QThread):
    """Chạy 1 lệnh pipeline (quét / phân tích giọng / render), stream stdout ra GUI."""
    line = Signal(str)
    step = Signal(int, int, str)       # [STEP i/n] của render_engine
    vid = Signal(int, int, str)        # [k/N] video thứ mấy trong lô
    voice = Signal(int, str, str, str) # VOICE idx | gender·age | name | voice_id
    scanned = Signal(object)           # dict channel_scan --json
    done = Signal(int)

    def __init__(self, cmd, cwd, mode):
        super().__init__()
        self.cmd, self.cwd, self.mode = cmd, cwd, mode
        self.proc = None

    def run(self):
        env = os.environ.copy(); env["PYTHONIOENCODING"] = "utf-8"
        try:
            self.proc = subprocess.Popen(self.cmd, cwd=self.cwd, env=env, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
            # KHÔNG CREATE_NO_WINDOW: để tiến trình con kế thừa console ẩn của GUI (xem đầu file) →
            # không con/cháu nào bật cửa sổ. Đọc output qua stdout=PIPE nên vẫn nhận log bình thường.
        except Exception as e:
            self.line.emit(f"✗ Không chạy được: {e}"); self.done.emit(-1); return
        rx_step = re.compile(r"\[STEP (\d+)/(\d+)\]\s*(.*)")
        rx_vid = re.compile(r"─+ \[(\d+)/(\d+)\]")
        buf = []
        for ln in self.proc.stdout:
            ln = ln.rstrip("\n")
            if self.mode == "scan":
                buf.append(ln)
                continue
            if ln.startswith("VOICE\t"):
                pr = ln.split("\t")
                if len(pr) >= 6:
                    self.voice.emit(int(pr[1]), f"{pr[2]}·{pr[3]}", pr[4], pr[5])
                continue
            m = rx_step.search(ln)
            if m:
                self.step.emit(int(m[1]), int(m[2]), m[3])
            mv = rx_vid.search(ln)
            if mv:
                self.vid.emit(int(mv[1]), int(mv[2]), ln)
            self.line.emit(ln)
        self.proc.wait()
        if self.mode == "scan":
            data = None
            for ln in buf:
                if ln.strip().startswith("{"):
                    try:
                        data = json.loads(ln)
                    except Exception:
                        pass
            self.scanned.emit(data)
        self.done.emit(self.proc.returncode)

    def stop(self):
        p = self.proc
        if p and p.poll() is None:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            try: p.kill()
            except Exception: pass


def _fmt_views(v):
    if v is None: return "?"
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.0f}K"
    return str(v)


def _fmt_dur(s):
    if not s: return "?"
    s = int(s); return f"{s//60}:{s%60:02d}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = load_cfg()
        self.worker = None
        self.videos = []          # danh sách video của kênh đang quét
        self.channel = None       # dict channel_scan
        self.setWindowTitle("H2Dev Video Render — NÃO = Claude")
        self.resize(1040, 760)
        root = QWidget(); self.setCentralWidget(root)
        v = QVBoxLayout(root); v.setContentsMargins(18, 16, 18, 16); v.setSpacing(10)

        v.addWidget(QLabel("🎬 H2Dev Video Render — quét KÊNH → chọn video → Claude làm từ đầu", objectName="title"))
        v.addWidget(QLabel("Não = Claude (viết kịch bản/prompt) · ảnh gpt-image-2 · giọng ElevenLabs theo TỪNG video · QC Gemini · ghép ffmpeg."))

        row = QHBoxLayout()
        self.ed_channel = QLineEdit(); self.ed_channel.setPlaceholderText("URL hoặc @handle kênh đối thủ, vd @simbot2")
        self.b_scan = QPushButton("🔍 Quét video", objectName="scan"); self.b_scan.clicked.connect(self._scan)
        row.addWidget(QLabel("Kênh:")); row.addWidget(self.ed_channel, 1); row.addWidget(self.b_scan)
        v.addLayout(row)

        row2 = QHBoxLayout()
        self.ed_profile = QLineEdit(self.cfg.get("profile", "satori-jp-obaa")); self.ed_profile.setFixedWidth(180)
        self.chk_all = QCheckBox("Chạy TẤT CẢ video (bỏ tick = chỉ video đã chọn)")
        row2.addWidget(QLabel("Profile kênh/giọng:")); row2.addWidget(self.ed_profile)
        row2.addSpacing(16); row2.addWidget(self.chk_all); row2.addStretch(1)
        v.addLayout(row2)

        self.tbl = QTableWidget(0, 6)
        self.tbl.setHorizontalHeaderLabels(["", "#", "View", "Dài", "Tên video", "Giọng (tự phát hiện)"])
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setSelectionMode(QAbstractItemView.NoSelection)
        hh = self.tbl.horizontalHeader()
        for c, mode in ((0, QHeaderView.ResizeToContents), (1, QHeaderView.ResizeToContents),
                        (2, QHeaderView.ResizeToContents), (3, QHeaderView.ResizeToContents),
                        (4, QHeaderView.Stretch), (5, QHeaderView.ResizeToContents)):
            hh.setSectionResizeMode(c, mode)
        v.addWidget(self.tbl, 1)

        rowsel = QHBoxLayout()
        b_all = QPushButton("Chọn tất cả"); b_all.clicked.connect(lambda: self._check_all(True))
        b_none = QPushButton("Bỏ chọn"); b_none.clicked.connect(lambda: self._check_all(False))
        self.b_voice = QPushButton("🎙 Phân tích giọng (đã chọn)"); self.b_voice.clicked.connect(self._analyze)
        rowsel.addWidget(b_all); rowsel.addWidget(b_none); rowsel.addStretch(1); rowsel.addWidget(self.b_voice)
        v.addLayout(rowsel)

        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet("color:#1f3a64;"); v.addWidget(line)

        rowb = QHBoxLayout()
        self.b_run = QPushButton("▶  LÀM VIDEO (Claude viết → render)", objectName="run"); self.b_run.clicked.connect(self._run)
        self.b_stop = QPushButton("■ DỪNG", objectName="stop"); self.b_stop.clicked.connect(self._stop); self.b_stop.setEnabled(False)
        self.b_open = QPushButton("📂 Mở thư mục"); self.b_open.clicked.connect(self._open)
        rowb.addWidget(self.b_run, 3); rowb.addWidget(self.b_stop, 1); rowb.addWidget(self.b_open, 1)
        v.addLayout(rowb)

        self.pbar = QProgressBar(); self.pbar.setRange(0, 9); self.pbar.setValue(0); self.pbar.setFormat("Sẵn sàng — quét 1 kênh để bắt đầu")
        v.addWidget(self.pbar)
        self.txt = QPlainTextEdit(); self.txt.setReadOnly(True); self.txt.setMaximumHeight(240); v.addWidget(self.txt)

    # ---------- helpers
    def _log(self, s): self.txt.appendPlainText(s)

    def _row_of_idx(self, idx):
        for r in range(self.tbl.rowCount()):
            if self.tbl.item(r, 1) and self.tbl.item(r, 1).text() == str(idx):
                return r
        return -1

    def _check_all(self, on):
        for r in range(self.tbl.rowCount()):
            it = self.tbl.item(r, 0)
            if it: it.setCheckState(Qt.Checked if on else Qt.Unchecked)

    def _checked_picks(self):
        picks = []
        for r in range(self.tbl.rowCount()):
            it = self.tbl.item(r, 0)
            if it and it.checkState() == Qt.Checked:
                picks.append(int(self.tbl.item(r, 1).text()))
        return picks

    def _busy(self, on):
        for b in (self.b_scan, self.b_run, self.b_voice):
            b.setEnabled(not on)
        self.b_stop.setEnabled(on)

    # ---------- quét kênh
    def _scan(self):
        url = self.ed_channel.text().strip()
        if not url:
            self._log("✗ Chưa nhập URL/@handle kênh."); return
        pdir = pipeline_dir(self.cfg)
        cmd = list(self.cfg["python_cmd"]) + [os.path.join(pdir, "channel_scan.py"), url, "--limit", "60", "--json"]
        self.txt.clear(); self._log(f"🔍 Quét kênh {url} …")
        self._busy(True); self.pbar.setFormat("Đang quét kênh…")
        self.worker = Worker(cmd, pdir, "scan")
        self.worker.scanned.connect(self._on_scanned)
        self.worker.line.connect(self._log)
        self.worker.done.connect(lambda c: self._busy(False))
        self.worker.start()

    def _on_scanned(self, data):
        if not data or not data.get("videos"):
            self._log("✗ Không quét được video (kênh sai / riêng tư / bị chặn IP)."); self.pbar.setFormat("Quét thất bại"); return
        self.channel = data; self.videos = data["videos"]
        self.tbl.setRowCount(0)
        for i, vd in enumerate(self.videos, 1):
            r = self.tbl.rowCount(); self.tbl.insertRow(r)
            chk = QTableWidgetItem(); chk.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chk.setCheckState(Qt.Unchecked); self.tbl.setItem(r, 0, chk)
            self.tbl.setItem(r, 1, QTableWidgetItem(str(i)))
            self.tbl.setItem(r, 2, QTableWidgetItem(_fmt_views(vd.get("view_count"))))
            self.tbl.setItem(r, 3, QTableWidgetItem(_fmt_dur(vd.get("duration"))))
            self.tbl.setItem(r, 4, QTableWidgetItem(vd.get("title", "")))
            self.tbl.setItem(r, 5, QTableWidgetItem("— (bấm Phân tích giọng)"))
        self._log(f"✓ Kênh: {data.get('channel_title','')} (@{data.get('handle','')}) — {len(self.videos)} video.")
        self.pbar.setFormat(f"{len(self.videos)} video — tick chọn rồi Làm video")

    # ---------- phân tích giọng
    def _analyze(self):
        picks = self._checked_picks()
        if not self.videos:
            self._log("✗ Chưa quét kênh."); return
        if not picks:
            self._log("✗ Chưa tick video nào để phân tích giọng."); return
        pdir = pipeline_dir(self.cfg)
        cmd = list(self.cfg["python_cmd"]) + [os.path.join(pdir, "brain_channel.py"),
              "--channel", self.ed_channel.text().strip(), "--profile", self.ed_profile.text().strip() or "satori-jp-obaa",
              "--limit", "60", "--pick", ",".join(map(str, picks)), "--analyze-only"]
        self._log(f"🎙 Phân tích giọng {len(picks)} video…")
        self._busy(True); self.pbar.setFormat("Phân tích giọng…")
        self.worker = Worker(cmd, pdir, "analyze")
        self.worker.voice.connect(self._on_voice)
        self.worker.line.connect(self._log)
        self.worker.done.connect(lambda c: (self._busy(False), self.pbar.setFormat("Xong phân tích giọng")))
        self.worker.start()

    def _on_voice(self, idx, ga, name, vid):
        r = self._row_of_idx(idx)
        if r >= 0:
            self.tbl.setItem(r, 5, QTableWidgetItem(f"{ga} · {name}"))

    # ---------- làm video
    def _run(self):
        if not self.videos:
            self._log("✗ Chưa quét kênh."); return
        run_all = self.chk_all.isChecked()
        picks = self._checked_picks()
        if not run_all and not picks:
            self._log("✗ Tick chọn video, hoặc bật 'Chạy TẤT CẢ'."); return
        pdir = pipeline_dir(self.cfg)
        cmd = list(self.cfg["python_cmd"]) + [os.path.join(pdir, "brain_channel.py"),
              "--channel", self.ed_channel.text().strip(),
              "--profile", self.ed_profile.text().strip() or "satori-jp-obaa", "--limit", "60"]
        cmd += ["--all"] if run_all else ["--pick", ",".join(map(str, picks))]
        self.txt.clear()
        self._log(f"▶ Làm {'TẤT CẢ' if run_all else str(len(picks))} video — não Claude viết rồi render.")
        self._busy(True); self.pbar.setValue(0); self.pbar.setFormat("Bắt đầu…")
        self.worker = Worker(cmd, pdir, "make")
        self.worker.line.connect(self._log)
        self.worker.step.connect(self._on_step)
        self.worker.vid.connect(self._on_vid)
        self.worker.done.connect(self._on_done)
        self.worker.start()

    def _on_vid(self, k, n, _):
        self.pbar.setFormat(f"Video {k}/{n} …")

    def _on_step(self, i, n, name):
        self.pbar.setRange(0, n); self.pbar.setValue(i); self.pbar.setFormat(f"[{i}/{n}] {name}")

    def _on_done(self, code):
        self._busy(False)
        self.pbar.setFormat("✅ XONG" if code == 0 else f"■ Dừng/Lỗi (code {code})")

    def _stop(self):
        if self.worker: self.worker.stop()
        self._log("… đã yêu cầu DỪNG (taskkill cây tiến trình).")

    def _open(self):
        d = os.path.join(self.cfg["project_root"], "assets")
        if os.path.isdir(d): os.startfile(d)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    w = MainWindow(); w.show(); w.raise_(); w.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
