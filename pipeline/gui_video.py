"""gui_video.py — GIAO DIỆN cho tool làm video Satori (PySide6). Đóng thành .exe chạy máy khác.

Cấu trúc theo skill `tao_tool_exe.md`:
  · `--selftest`  ghi selftest.log CẠNH exe — bản --windowed KHÔNG có console, mọi lỗi bị nuốt (#20)
  · `--child <script.py> ...` exe tự đóng vai Python chạy các script con của pipeline (#23):
    khi frozen, `sys.executable` là chính exe này chứ không phải python.exe.
  · BASE (ghi: settings/log, CẠNH exe) tách khỏi resource_path (đọc: bundle trong _internal) (#21)
  · nút DỪNG dùng `taskkill /F /T` giết CẢ CÂY — `proc.kill()` chỉ giết con, cháu vẫn gen ảnh
    và VẪN TỐN TIỀN (#24)
  · QSS đặt ở cấp QApplication để hộp thoại cũng ăn theme (#26)
  · KHÔNG gọi QMessageBox trong luồng tự động (#25)

Chạy:
  py -3.13 gui_video.py
  gui_video.exe --selftest
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import threading
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------- đường dẫn
if getattr(sys, "frozen", False):
    BASE = Path(sys.executable).parent          # nơi GHI: settings, log — cạnh exe
else:
    BASE = Path(__file__).resolve().parent


def resource_path(name):
    """Nơi ĐỌC tài nguyên bundle: _MEIPASS trước, rồi cạnh exe / thư mục nguồn."""
    mei = getattr(sys, "_MEIPASS", None)
    if mei and (Path(mei) / name).exists():
        return Path(mei) / name
    return BASE / name


def _settings_path():
    """Cài đặt giao diện theo THƯ MỤC DỮ LIỆU, không nằm trong thư mục cài (thay tool là mất)."""
    try:
        from paths import DATA_DIR
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DATA_DIR / "gui_settings.json"
    except Exception:
        return BASE / "gui_settings.json"


SETTINGS = _settings_path()
# Ô đổi mỗi lần chạy → KHÔNG lưu (skill #27)
KHONG_LUU = {"slug", "competitor"}


def load_settings():
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_settings(d):
    try:
        SETTINGS.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


# ------------------------------------------------- exe đóng vai Python cho script con
def run_child(argv):
    """`exe --child tts.py --script ...` → nạp module tts và gọi main() ngay trong tiến trình này.
    Khi frozen KHÔNG có python.exe để gọi, nên pipeline gọi ngược lại chính exe này."""
    import importlib
    script = argv[0]
    sys.argv = [script] + list(argv[1:])
    mod = importlib.import_module(Path(script).stem)
    fn = getattr(mod, "main", None)
    if fn is None:
        raise SystemExit(f"{script} không có main()")
    r = fn()
    return int(r or 0)


def selftest(argv):
    """Kiểm bản .exe không cần bấm chuột. Ghi selftest.log CẠNH exe."""
    out, w = [], None
    w = out.append
    w(f"BASE = {BASE}")
    w(f"frozen = {getattr(sys, 'frozen', False)}")
    w(f"_MEIPASS = {getattr(sys, '_MEIPASS', '(none)')}")
    try:
        import numpy, PIL, requests, imageio_ffmpeg          # noqa: F401
        w("numpy / PIL / requests / imageio_ffmpeg OK")
        w(f"ffmpeg = {imageio_ffmpeg.get_ffmpeg_exe()}")
        import profiles, llm_client, ai_steps, qc_script, qc_visual, storyboard   # noqa: F401
        import make_video, tts, gen_images, assemble, pace_audio, new_profile     # noqa: F401
        w("mọi module pipeline import OK")
        ids = profiles.list_ids()
        w(f"profile thấy được ({len(ids)}): {', '.join(ids)}")
        for pid in ids:
            p = profiles.load(pid)
            w(f"  {pid}: giọng={p['voice']['id']} char_rate={profiles.char_rate(p)} "
              f"target={profiles.target_chars(p)} chữ")
        import paths
        for rel in ("skills/youtube-script/SKILL.md", "skills/youtube-image-prompts/SKILL.md",
                    "assets/voice_bank.json"):
            f = paths.res(rel)
            w(f"{rel}: {'CÓ' if f.exists() else 'THIẾU'}  ({f})")
        import voice_bank
        w(f"kho giọng: {len(voice_bank.load())} giọng")
        w(f"thư mục ra video: {paths.OUT_ROOT / 'assets' / 'out'}")
        w(f"keys.json cạnh exe: {'CÓ' if (BASE / 'keys.json').exists() else 'không (dùng key mặc định)'}")
        import selftest_extra
        out += selftest_extra.lines()
        if "--ping" in argv:
            import llm_client as lc
            for prov, model in lc.CHAINS["short"][:2]:
                try:
                    r = lc.chat("ping", provider=prov, model=model, verbose=False)
                    w(f"ping {prov}:{model} OK ({r.elapsed:.1f}s)")
                except Exception as e:
                    w(f"ping {prov}:{model} LỖI {type(e).__name__} {e}")
        w("SELFTEST OK")
    except Exception as e:
        w(f"SELFTEST LỖI: {e}\n{traceback.format_exc()}")
    (BASE / "selftest.log").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    return 0


# ============================================================================ GUI
# Giao diện theo mẫu D:\CLAUDE\TIKTOKSHOP\LOGIN_US (dark-neon, thẻ nổi bo góc, cửa sổ tự vẽ).
# Điểm nhấn đổi sang ĐỎ YouTube cho hợp ngách. Chiều sâu ("3D") dựng bằng 3 lớp:
#   1. nền chuyển sắc chéo cho cả cửa sổ,
#   2. thẻ QFrame#card nền chuyển sắc dọc + viền sáng + bo 16px,
#   3. QGraphicsDropShadowEffect đổ bóng dưới mỗi thẻ (QSS KHÔNG có box-shadow).
# ⚠ QSS phải đặt ở cấp QApplication chứ không phải MainWindow, nếu không hộp thoại và menu
#   giữ nền trắng mặc định của Windows (bẫy #26 skill tao_tool_exe.md).
QSS = """
* { font-family: "Segoe UI"; color: #e8f1ff; font-size: 13px; }

QWidget#root {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #0a0a12, stop:0.45 #12111f, stop:1 #1a0d16);
}

/* ---------- thanh tiêu đề tự vẽ ---------- */
QWidget#titlebar { background: transparent; }
QLabel#brand { font-size: 21px; font-weight: 800; color: #ffffff; background: transparent; }
QLabel#brandsub { font-size: 11px; color: #8b93b0; background: transparent; }
QPushButton#winbtn {
    background: #1c1b2e; min-width: 38px; max-width: 44px; min-height: 32px;
    border: 1px solid #2e2c47; border-radius: 8px; color: #b9c2dc; font-size: 14px;
}
QPushButton#winbtn:hover { background: #292740; }
QPushButton#winclose {
    background: #1c1b2e; min-width: 38px; max-width: 44px; min-height: 32px;
    border: 1px solid #6b2029; border-radius: 8px; color: #ff9aa3; font-size: 14px;
}
QPushButton#winclose:hover { background: #cc0000; color: #ffffff; }

/* ---------- thẻ nổi ---------- */
QFrame#card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(32,31,52,0.94), stop:1 rgba(21,20,36,0.94));
    border: 1px solid #322f4d; border-radius: 16px;
}
QFrame#cardred {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(48,20,30,0.94), stop:1 rgba(26,18,32,0.94));
    border: 1px solid #5a2334; border-radius: 16px;
}
QFrame#sep { background: #322f4d; max-height: 1px; border: none; }

QLabel#h1 { font-size: 17px; font-weight: 800; color: #ffffff; background: transparent; }
QLabel#flabel { color: #cfd6ea; font-size: 13px; font-weight: 600; background: transparent; }
QLabel#hint { color: #7c85a3; font-size: 11px; background: transparent; }
QLabel#sectitle { color: #ff6b6b; font-size: 11px; font-weight: 800;
                  background: transparent; letter-spacing: 1px; }
QLabel#ico { font-size: 16px; background: transparent; }
QLabel#status { color: #8b93b0; font-size: 12px; background: transparent; }

/* ---------- ô nhập ---------- */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #14131f; border: 1px solid #34314f; border-radius: 9px;
    padding: 0 12px; min-height: 36px; color: #e8f1ff;
    selection-background-color: #cc0000;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #ff3b3b; background: #191727;
}
QLineEdit:hover, QComboBox:hover { border: 1px solid #47436b; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox::down-arrow { image: none; width: 0; height: 0;
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-top: 6px solid #9aa3c0; margin-right: 8px; }
QComboBox QAbstractItemView {
    background: #14131f; border: 1px solid #47436b; color: #e8f1ff;
    selection-background-color: #cc0000; outline: none;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 18px; background: #262340; border: none; }
QSpinBox::up-button, QDoubleSpinBox::up-button { border-top-right-radius: 8px; }
QSpinBox::down-button, QDoubleSpinBox::down-button { border-bottom-right-radius: 8px; }
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow { image: none; width: 0; height: 0;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-bottom: 5px solid #9aa3c0; }
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow { image: none; width: 0; height: 0;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-top: 5px solid #9aa3c0; }

/* ---------- nút ---------- */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a2740, stop:1 #201e33);
    border: 1px solid #3d3960; border-radius: 10px;
    padding: 0 18px; min-height: 36px; color: #dfe5f5; font-weight: 600;
}
QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #363152, stop:1 #29253f); border: 1px solid #55507f; }
QPushButton:pressed { background: #1a1829; padding-top: 2px; }
QPushButton:disabled { background: #1a1926; color: #565b74; border-color: #2a2840; }

QPushButton#primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ff0033, stop:0.55 #cc0000, stop:1 #8b0000);
    color: #ffffff; border: none; border-radius: 13px;
    font-size: 15px; font-weight: 800; min-height: 46px; padding: 0 26px;
}
QPushButton#primary:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #ff2a52, stop:0.55 #e60000, stop:1 #a80000); }
QPushButton#primary:pressed { padding-top: 2px; }
QPushButton#primary:disabled { background: #4a2430; color: #a08a90; }

QPushButton#accent {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2f2b4d, stop:1 #3a2140);
    color: #ffd0d6; border: 1px solid #6b2a44; border-radius: 12px;
    min-height: 42px; font-weight: 700; padding: 0 20px;
}
QPushButton#accent:hover { background: #43305c; color: #ffffff; }

QPushButton#danger {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7e1c2a, stop:1 #5a1420);
    border: 1px solid #9c2b3c; color: #ffd7dc; border-radius: 10px; font-weight: 700;
}
QPushButton#danger:hover { background: #a3283c; color: #ffffff; }
QPushButton#danger:disabled { background: #2a1a20; color: #6e5a60; border-color: #3a2630; }

QPushButton#scan {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff0033, stop:1 #b30000);
    color: #ffffff; border: none; border-radius: 10px;
    min-height: 38px; font-weight: 800; padding: 0 22px;
}
QPushButton#scan:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                         stop:0 #ff2a52, stop:1 #cc0000); }
QPushButton#scan:disabled { background: #4a2430; color: #a08a90; }

/* ---------- tab ---------- */
QTabWidget::pane { border: none; background: transparent; top: -1px; }
QTabBar { background: transparent; }
QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #232135, stop:1 #1a1828);
    color: #9aa3c0; padding: 10px 22px; margin-right: 6px;
    border: 1px solid #322f4d; border-bottom: none;
    border-top-left-radius: 12px; border-top-right-radius: 12px;
    font-weight: 700; font-size: 13px;
}
QTabBar::tab:hover { color: #dfe5f5; background: #2c2942; }
QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #cc0000, stop:1 #7a0014);
    color: #ffffff; border: 1px solid #ff3b3b; border-bottom: none;
}

/* ---------- bảng video ---------- */
QTableWidget {
    background: #101020; border: 1px solid #322f4d; border-radius: 12px;
    gridline-color: #262340; color: #e8f1ff; font-size: 13px;
    alternate-background-color: #15142400;
}
QTableWidget::item { padding: 6px 8px; color: #e8f1ff; }
QTableWidget::item:selected { background: #4a1020; color: #ffffff; }
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #262340, stop:1 #1c1a2c);
    color: #ffb3b3; font-weight: 800; font-size: 12px;
    border: none; border-right: 1px solid #322f4d; border-bottom: 1px solid #3d3960;
    padding: 8px;
}
QTableCornerButton::section { background: #262340; border: none; }

/* ---------- tick ---------- */
QCheckBox { color: #dfe5f5; font-size: 13px; font-weight: 600;
            background: transparent; spacing: 8px; }
/* Ô tích trong BẢNG là QTableWidget::indicator, KHÔNG phải QCheckBox::indicator
   (cột "Chọn" dùng setCheckState của item chứ không nhúng widget). Thiếu khối này
   thì ô tích ăn màu mặc định của theme tối = viền đen trên nền đen, nhìn không thấy.
   Đã tích = dấu V trắng, KHÔNG tô nền đỏ (user chốt 2026-09-09).
   ⚠ Hễ khai border/background cho ::indicator là Qt NGỪNG tự vẽ dấu tick — bắt buộc
   phải chỉ ảnh qua `image: url(...)`, nên có chỗ thay __TICK__ bằng đường dẫn thật
   lúc chạy (xem `_qss()`). Không có ảnh thì rơi về nền đỏ để đừng bao giờ vô hình. */
QCheckBox::indicator, QTableWidget::indicator {
    width: 18px; height: 18px; border-radius: 5px;
    border: 2px solid #ffffff; background: #14131f; }
QCheckBox::indicator:hover, QTableWidget::indicator:hover {
    border: 2px solid #ff5c5c; background: #201d33; }
QCheckBox::indicator:checked, QTableWidget::indicator:checked {
    background: #14131f; border: 2px solid #ffffff; image: url("__TICK__"); }

/* ---------- thanh tiến trình ---------- */
QProgressBar {
    background: #14131f; border: 1px solid #34314f; border-radius: 10px;
    min-height: 28px; text-align: center; color: #ffffff; font-weight: 700;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff0033, stop:1 #ff6b3d);
    border-radius: 9px;
}

/* ---------- log ---------- */
QPlainTextEdit {
    background: #0a0a14; border: 1px solid #262340; border-radius: 12px;
    color: #cfe4ff; font-family: "Consolas","Courier New",monospace; font-size: 12px;
    padding: 10px; selection-background-color: #cc0000;
}

QScrollBar:vertical { background: transparent; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: #3d3960; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #cc0000; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 2px; }
QScrollBar::handle:horizontal { background: #3d3960; border-radius: 5px; min-width: 30px; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

/* Hộp thoại là cửa sổ TOP-LEVEL riêng, KHÔNG ăn theo QWidget#root → phải khai riêng,
   nếu không nền trắng mặc định của Windows (bẫy đã dính ở dự án LOGIN_US). */
QDialog, QMessageBox { background: #15142a; }
QDialog QLabel, QMessageBox QLabel { background: transparent; color: #e8f1ff; }
QDialog QPushButton, QMessageBox QPushButton {
    background: #2a2740; color: #e8f1ff; border: 1px solid #3d3960;
    border-radius: 8px; padding: 4px 18px; min-height: 32px; font-weight: 600;
}
QDialog QPushButton:hover, QMessageBox QPushButton:hover { background: #cc0000; }
"""


def gui_main():
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QIcon, QPixmap
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                   QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton,
                                   QPlainTextEdit, QTabWidget, QDoubleSpinBox, QMessageBox,
                                   QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView,
                                   QCheckBox, QSpinBox, QFrame, QGraphicsDropShadowEffect,
                                   QAbstractItemView)
    import profiles

    STEPS = ["B2", "B3", "B3Q", "B4", "B4Q", "B5", "B5Q", "B7", "B8", "B8Q", "B9"]
    LOGO = resource_path("assets/youtube-logo.png")
    TICK = resource_path("assets/tick-white.png")

    def _qss():
        """Nhét đường dẫn THẬT của ảnh dấu V vào QSS.

        QSS không hiểu đường dẫn tương đối theo thư mục làm việc, và trong bản .exe ảnh nằm
        trong `_internal` — đường dẫn chỉ biết được lúc chạy. Dấu `\\` của Windows là ký tự
        thoát trong QSS nên phải đổi hết sang `/`, và cả chuỗi phải nằm trong nháy kép vì
        thư mục cài có dấu cách ("Youtube Clone-Gemini").
        Thiếu ảnh (build lỗi/xoá nhầm) → quay về tô nền đỏ, thà xấu còn hơn ô tích vô hình."""
        if TICK.exists():
            return QSS.replace("__TICK__", str(TICK).replace("\\", "/"))
        return QSS.replace('background: #14131f; border: 2px solid #ffffff; '
                           'image: url("__TICK__");',
                           'background: #cc0000; border: 2px solid #ffffff;')

    def shadow(w, blur=26, dy=6, alpha=170):
        """Đổ bóng — QSS KHÔNG có box-shadow, muốn thẻ 'nổi' lên thì phải dùng hiệu ứng này."""
        e = QGraphicsDropShadowEffect(w)
        e.setBlurRadius(blur)
        e.setOffset(0, dy)
        e.setColor(QColor(0, 0, 0, alpha))
        w.setGraphicsEffect(e)
        return w

    def card(title="", kind="card"):
        """Thẻ nổi bo góc. Trả (khung, layout dọc bên trong) để nhét nội dung vào."""
        f = QFrame(objectName=kind)
        v = QVBoxLayout(f)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(10)
        if title:
            v.addWidget(QLabel(title, objectName="h1"))
        shadow(f)
        return f, v

    class TitleBar(QWidget):
        """Thanh tiêu đề TỰ VẼ cho cửa sổ frameless: logo + tên + thu nhỏ/phóng/đóng + kéo."""

        def __init__(self, win):
            super().__init__(objectName="titlebar")
            self.setFixedHeight(64)
            self._win = win
            self._drag = None
            self._geo = None
            h = QHBoxLayout(self)
            h.setContentsMargins(16, 8, 12, 4)
            h.setSpacing(12)
            logo = QLabel()
            if LOGO.exists():
                logo.setPixmap(QPixmap(str(LOGO)).scaled(46, 46, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
            logo.setFixedSize(46, 46)
            logo.setAlignment(Qt.AlignCenter)
            h.addWidget(logo)
            box = QVBoxLayout()
            box.setSpacing(0)
            brand = QLabel('<span style="color:#ff2a52">Youtube</span> Clone-Gemini',
                           objectName="brand")
            brand.setTextFormat(Qt.RichText)
            box.addWidget(brand)
            box.addWidget(QLabel("quét kênh → viết kịch bản → giọng → ảnh → dựng video",
                                 objectName="brandsub"))
            h.addLayout(box)
            h.addStretch(1)
            for txt, obj, fn in (("—", "winbtn", win.showMinimized),
                                 ("▢", "winbtn", self._max),
                                 ("✕", "winclose", win.close)):
                b = QPushButton(txt, objectName=obj)
                b.clicked.connect(fn)
                h.addWidget(b)

        def _max(self):
            # Cửa sổ frameless: showNormal() sau showMaximized() KHÔNG tự trả lại kích thước cũ
            # trên Windows → bấm lần 2 nhìn như nút chết. Phải tự nhớ geometry.
            w = self._win
            if w.isMaximized():
                w.showNormal()
                if self._geo is not None:
                    w.setGeometry(self._geo)
            else:
                self._geo = w.geometry()
                w.showMaximized()

        def mousePressEvent(self, e):
            if e.button() == Qt.LeftButton:
                self._drag = e.globalPosition().toPoint() - self._win.frameGeometry().topLeft()

        def mouseMoveEvent(self, e):
            if self._drag and (e.buttons() & Qt.LeftButton):
                if self._win.isMaximized():
                    self._win.showNormal()
                self._win.move(e.globalPosition().toPoint() - self._drag)

        def mouseReleaseEvent(self, e):
            self._drag = None

        def mouseDoubleClickEvent(self, e):
            self._max()

    class Runner(QThread):
        """Chạy LẦN LƯỢT nhiều video. `jobs` = list các list tham số cho make_video.py.

        Chạy tuần tự chứ không song song: mỗi video đã tự dùng nhiều luồng khi gen ảnh và encode
        video, chạy 2 tập cùng lúc là tranh CPU + tranh hạn mức key ảnh, tổng thời gian không giảm.
        """
        line = Signal(str)
        done = Signal(int)
        job_begin = Signal(int, int, str)      # (số thứ tự, tổng, tên tập)
        job_end = Signal(int, str, int)        # (số thứ tự, tên tập, mã thoát)

        def __init__(self, jobs, labels=None, lanes=1, stagger=0):
            super().__init__()
            self.jobs = jobs if jobs and isinstance(jobs[0], (list, tuple)) else [jobs]
            self.labels = labels or [""] * len(self.jobs)
            self.lanes = max(1, int(lanes))
            self.stagger = max(0, int(stagger))     # giây, khoảng LỆCH giữa 2 tập khởi động
            self.procs = {}                          # {chỉ số: Popen} — để nút DỪNG giết hết
            self.proc = None                         # tương thích code cũ
            self._stop = False
            self._khoa = threading.Lock()

        def run(self):
            exe = [sys.executable] + (["--make-video"] if getattr(sys, "frozen", False)
                                      else [str(resource_path("make_video.py"))])
            worst = [0]
            n = len(self.jobs)
            batdau = threading.Semaphore(0)          # điều nhịp: mỗi tập chờ tới lượt khởi động

            def chay(i, args, lbl):
                batdau.acquire()
                if self._stop:
                    return
                self.job_begin.emit(i, n, lbl)
                if n > 1:
                    self.line.emit(f"\n{'=' * 66}\n=== [{i}/{n}] {lbl}\n{'=' * 66}")
                rc = self._one(i, exe + [str(a) for a in args])
                self.job_end.emit(i, lbl, rc)
                if rc != 0:
                    worst[0] = rc
                    # Một tập lỗi KHÔNG dừng cả lô: video sau độc lập hoàn toàn, và người dùng bấm
                    # "chạy 10 tập" rồi đi ngủ thì mất cả đêm nếu tập số 2 gãy là dừng hết.
                    self.line.emit(f"→ [{i}/{n}] {lbl}: LỖI (mã {rc}) — chuyển tập sau.")

            with cf.ThreadPoolExecutor(max_workers=self.lanes) as ex:
                fut = [ex.submit(chay, i, a, self.labels[i - 1] or f"tập {i}")
                       for i, a in enumerate(self.jobs, 1)]
                # Thả từng tập một, cách nhau `stagger` giây. Nhờ vậy tập sau còn đang bóc lời/
                # viết kịch bản (chờ mạng) trong khi tập trước đã sang ghép video (ăn CPU) —
                # hai thứ không giành nhau. Thả cùng lúc thì cả 5 cùng vẽ ảnh → gpti2 trả 429.
                for k in range(n):
                    if self._stop:
                        break
                    if k and self.stagger:
                        for _ in range(self.stagger):
                            if self._stop:
                                break
                            time.sleep(1)
                    batdau.release()
                if self._stop:                       # thả nốt để luồng nào cũng thoát được
                    for _ in range(n):
                        batdau.release()
                cf.wait(fut)
            self.done.emit(worst[0])

        def _one(self, i, cmd):
            # Lấy slug TỪ CHÍNH LỆNH (--slug ...) thay vì self.labels — cách này đúng cho cả tab
            # batch (nhiều job) lẫn tab "Làm 1 video" (labels rỗng), không phụ thuộc ai gọi.
            slug = ""
            if "--slug" in cmd:
                try:
                    slug = str(cmd[cmd.index("--slug") + 1])
                except IndexError:
                    pass
            self.line.emit("$ " + " ".join(str(c) for c in cmd[:8]) + " …")
            # make_video.py in tag "[BXX] ..." mỗi khi bắt đầu/báo tiến triển một bước. Giữ lại
            # tag GẦN NHẤT để gắn vào cả những dòng KHÔNG có tag (log của tiến trình con nó gọi,
            # vd fetch_script.py/gen_images.py) — người xem log luôn biết "đang ở bước nào", kể cả
            # dòng chỉ là tiến độ vẽ ảnh/tải phụ đề chứ không tự xưng tên bước.
            buoc_hien_tai = [""]

            def gan_nhan(ln):
                # Giữ NGUYÊN dạng "[BXX]" (có ngoặc vuông) dù đặt slug lên trước — tab "Làm 1 video"
                # dò tiếp bằng regex tìm "[BXX]" trong dòng để cập nhật thanh tiến trình theo bước,
                # đổi định dạng ở đây mà không sửa bên đó là thanh tiến trình đứng im ngay lập tức.
                m = re.match(r"^\[([A-Za-z0-9_]+)\]\s*(.*)$", ln)
                if m:
                    buoc_hien_tai[0] = m.group(1)
                    phan_tram = ""
                    if buoc_hien_tai[0] in STEPS:
                        idx = STEPS.index(buoc_hien_tai[0]) + 1
                        phan_tram = f" ({idx}/{len(STEPS)} ≈ {idx * 100 // len(STEPS)}%)"
                    rest = m.group(2)
                    dau = f"{slug} - [{buoc_hien_tai[0]}]{phan_tram}" if slug else \
                        f"[{buoc_hien_tai[0]}]{phan_tram}"
                    return dau + (f" - {rest}" if rest else "")
                if not buoc_hien_tai[0]:
                    return f"{slug} - {ln}" if slug else ln
                return f"{slug} - [{buoc_hien_tai[0]}] - {ln}" if slug else \
                    f"[{buoc_hien_tai[0]}] - {ln}"

            try:
                p = subprocess.Popen(
                    cmd, cwd=str(resource_path(".")), stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
                    bufsize=1, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                with self._khoa:
                    self.procs[i] = p
                    self.proc = p
                for ln in p.stdout:
                    ln = ln.rstrip()
                    if ln:
                        self.line.emit(gan_nhan(ln))
                p.wait()
                return p.returncode
            except Exception as e:
                self.line.emit(f"{(slug + ' - ') if slug else ''}LỖI: {type(e).__name__} {e}")
                return -1
            finally:
                with self._khoa:
                    self.procs.pop(i, None)

        def stop(self):
            self._stop = True
            with self._khoa:
                dang = [p for p in self.procs.values() if p and p.poll() is None]
            # taskkill /F /T: giết CẢ CÂY. proc.kill() chỉ giết con, cháu vẫn gen ảnh và TỐN TIỀN.
            for p in dang:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    class ScanWorker(QThread):
        """Quét kênh ở luồng riêng — gọi mạng trên luồng GUI là treo cửa sổ."""
        ok = Signal(dict)
        fail = Signal(str)

        def __init__(self, url, limit):
            super().__init__()
            self.url, self.limit = url, limit

        def run(self):
            try:
                import channel_scan
                self.ok.emit(channel_scan.scan(self.url, self.limit))
            except BaseException as e:      # SystemExit của channel_scan cũng phải bắt
                self.fail.emit(f"{type(e).__name__}: {e}")

    class Win(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Youtube Clone-Gemini")
            if LOGO.exists():
                self.setWindowIcon(QIcon(str(LOGO)))
            self.setWindowFlag(Qt.FramelessWindowHint, True)
            self.setMinimumSize(1180, 720)
            self.resize(1500, 880)
            self.worker = None
            self.st = load_settings()
            self.scan_info = {}
            self.scanner = None
            root = QWidget(objectName="root")
            outer = QVBoxLayout(root)
            outer.setContentsMargins(14, 8, 14, 12)
            outer.setSpacing(8)
            outer.addWidget(TitleBar(self))
            tabs = QTabWidget()
            self.tabs = tabs
            tabs.addTab(self._tab_channel(), "1 · Quét kênh → chạy hàng loạt")
            tabs.addTab(self._tab_run(), "2 · Làm 1 video")
            tabs.addTab(self._tab_new(), "3 · Lập kênh mới")
            outer.addWidget(tabs, 1)
            self.setCentralWidget(root)

        def _row(self, g, r, lbl, wid, hint="", w=340):
            """Một hàng của form: [nhãn] [ô nhập NGẮN] [chú thích tác dụng].

            Ô nhập kéo dài hết màn hình vừa xấu vừa vô ích (không ai gõ 100 ký tự vào ô "Thị
            trường"), lại không còn chỗ giải thích ô đó để làm gì — user phải đoán."""
            if w:
                wid.setMaximumWidth(w)
            g.addWidget(QLabel(lbl, objectName="flabel"), r, 0)
            g.addWidget(wid, r, 1)
            if hint:
                lab = QLabel(hint, objectName="hint")
                lab.setWordWrap(True)
                g.addWidget(lab, r, 2)

        CHUA_CO = "(chưa có kênh nào — lập ở tab 3)"

        def _fill_profiles(self, cb):
            """Đổ danh sách hồ sơ vào ô chọn. Máy mới CHƯA CÓ hồ sơ nào là chuyện bình thường —
            phải nói rõ phải làm gì, đừng để ô trống rồi báo lỗi khó hiểu lúc bấm Chạy."""
            cb.clear()
            try:
                ids = profiles.list_ids()
            except Exception as e:
                cb.addItem(f"(lỗi đọc hồ sơ: {e})")
                return
            cb.addItems(ids or [self.CHUA_CO])
            self._pick_profile(cb)

        def _co_profile(self):
            t = self.ch_profile.currentText().strip()
            if t and not t.startswith("("):
                return True
            QMessageBox.warning(self, "Chưa có kênh",
                                "Chưa có hồ sơ kênh nào.\n\nSang tab 3 · Lập kênh mới để tạo — "
                                "hoặc bấm 'Tạo profile từ kênh này…' sau khi quét, nó điền sẵn "
                                "ID kênh cho anh.")
            self.tabs.setCurrentIndex(2)
            return False

        def _pick_profile(self, cb):
            """Chọn sẵn profile: bản đã lưu → profile của ngách đang chạy → cái đầu danh sách.

            Không đặt gì thì Qt lấy phần tử ĐẦU BẢNG CHỮ CÁI (`samurai-history-jp`) — sai ngách,
            chạy nguyên vậy là ra kịch bản samurai cho kênh chuyện người già và mất tiền ảnh oan.
            """
            for want in (self.st.get("profile"), "satori-jp-obaa"):
                if not want:
                    continue
                i = cb.findText(want)
                if i >= 0:
                    cb.setCurrentIndex(i)
                    return

        # ---------------- tab 0: kênh → danh sách video → chạy lô
        def _tab_channel(self):
            w = QWidget()
            page = QVBoxLayout(w)
            page.setContentsMargins(4, 12, 4, 4)
            page.setSpacing(12)
            # KHÔNG đặt tiêu đề thẻ: dòng "Lấy video từ kênh đối thủ rồi chạy cả lô" lặp đúng
            # nội dung tên tab, mà mỗi dòng chữ ở đây ăn mất một dòng của BẢNG video bên dưới.
            box, v = card("", "cardred")
            page.addWidget(box)
            top = QGridLayout()
            top.setHorizontalSpacing(10)
            top.setVerticalSpacing(9)
            top.setColumnStretch(1, 0)
            top.setColumnStretch(2, 1)
            self.ch_src = QLineEdit(self.st.get("channel_src", ""),
                                    placeholderText="simbot2  ·  @simbot2  ·  URL kênh")
            self.ch_limit = QSpinBox(); self.ch_limit.setRange(1, 500)
            self.ch_limit.setValue(int(self.st.get("channel_limit") or 30))
            self.ch_limit.setMaximumWidth(80)
            self.bt_scan = QPushButton("🔍  Quét video", objectName="scan")
            self.ch_profile = QComboBox()
            self.ch_profile.setMinimumWidth(180)
            self._fill_profiles(self.ch_profile)
            # Nút này KHÔNG tạo hồ sơ — nó chỉ điền sẵn tab 3 rồi nhảy sang đó. Tên cũ
            # ("Tạo profile từ kênh này…") làm user tưởng bấm là xong, nên đổi cho đúng việc.
            self.bt_mkprof = QPushButton("Điền sẵn để lập kênh  →", objectName="accent")
            self.bt_mkprof.setToolTip("Điền sẵn ID kênh sang tab 3. Ở đó bấm 'Tạo kênh + đo giọng' "
                                      "mới thật sự lập hồ sơ.")
            self.ch_profile.setToolTip("Hồ sơ kênh CỦA MÌNH — quyết định giọng, ngách và độ dài "
                                       "video. Chưa có thì bấm 'Điền sẵn để lập kênh'.")
            self._row(top, 0, "Nguồn kênh", self.ch_src, "", w=250)
            # Cả 6 thứ dồn vào MỘT hàng: nguồn kênh · số video · quét · kênh của mình · lập kênh.
            # Trước đây tách 2 hàng kèm 3 dòng chú thích dài, ăn mất ~90px của bảng video.
            hr = QHBoxLayout(); hr.setSpacing(8)
            hr.addWidget(QLabel("Số video", objectName="flabel"))
            hr.addWidget(self.ch_limit)
            hr.addWidget(self.bt_scan)
            hr.addSpacing(18)
            hr.addWidget(QLabel("Kênh của mình", objectName="flabel"))
            hr.addWidget(self.ch_profile)
            hr.addWidget(self.bt_mkprof)
            hr.addStretch(1)
            top.addLayout(hr, 0, 2)
            self.ck_autov = QCheckBox("Nhận người kể theo từng video")
            self.ck_autov.setChecked(bool(self.st.get("auto_voice", True)))
            # Nhãn tick dài — để chung hàng với các ô trên thì nó kéo giãn cột làm cả lưới tràn
            # sang phải. Cho xuống hàng riêng, trải hết chiều ngang.
            hr3 = QHBoxLayout(); hr3.setSpacing(10)
            hr3.addWidget(self.ck_autov)
            lb2 = QLabel("Mỗi video một người kể khác nhau (bà mẹ / ông chồng / y tá…). Tool đọc "
                         "lời video gốc, nhận ra người kể rồi dùng cho CẢ BA: viết kịch bản đúng "
                         "ngôi kể · vẽ đúng mặt nhân vật chính · chọn giọng khớp.",
                         objectName="hint")
            lb2.setWordWrap(True)
            hr3.addWidget(lb2, 1)
            top.addLayout(hr3, 1, 1, 1, 2)
            # Độ dài bám theo TỪNG video gốc — trong một kênh có bài 28 phút lẫn 44 phút, ép cứng
            # một con số là bài ngắn bị kéo lê còn bài dài bị cắt cụt.
            self.ck_srcmin = QCheckBox("Độ dài bám theo video gốc")
            self.ck_srcmin.setChecked(bool(self.st.get("minutes_from_source", True)))
            hr4 = QHBoxLayout(); hr4.setSpacing(10)
            hr4.addWidget(self.ck_srcmin)
            lb3 = QLabel("Mỗi tập dài đúng bằng video đang clone (kẹp trong 8–60 phút). "
                         "Tắt thì lấy độ dài cố định trong hồ sơ kênh.", objectName="hint")
            lb3.setWordWrap(True)
            hr4.addWidget(lb3, 1)
            top.addLayout(hr4, 2, 1, 1, 2)
            # Lọc trùng khi quét kênh nhiều đợt.
            self.ck_skipdone = QCheckBox("Bỏ qua video đã clone xong")
            self.ck_skipdone.setChecked(bool(self.st.get("skip_done", True)))
            hr5 = QHBoxLayout(); hr5.setSpacing(10)
            hr5.addWidget(self.ck_skipdone)
            lb4 = QLabel("Quét lại kênh sẽ lẫn video đã làm đợt trước. Bật thì cột Tình trạng "
                         "hiện ✔ và tool tự loại chúng khỏi lượt chạy — kể cả khi bấm "
                         "Chạy TẤT CẢ.", objectName="hint")
            lb4.setWordWrap(True)
            hr5.addWidget(lb4, 1)
            top.addLayout(hr5, 3, 1, 1, 2)
            # Chạy nhiều video CÙNG LÚC, có LỆCH BƯỚC — TẠM ẨN (user chốt 2026-09-09).
            # Giữ nguyên widget + toàn bộ mã chạy đa luồng, chỉ giấu hàng này đi: ép 1 luồng để
            # thiết lập cũ (nếu từng đặt 3 luồng) không âm thầm chạy song song sau lưng.
            # Bật lại = đổi HIEN_DA_LUONG thành True, không phải viết lại gì.
            HIEN_DA_LUONG = False
            self.sp_lanes = QSpinBox(); self.sp_lanes.setRange(1, 4)
            self.sp_lanes.setValue(int(self.st.get("lanes") or 1) if HIEN_DA_LUONG else 1)
            self.sp_lanes.setMaximumWidth(70)
            self.sp_stag = QSpinBox(); self.sp_stag.setRange(0, 30); self.sp_stag.setSuffix(" phút")
            self.sp_stag.setValue(int(self.st.get("stagger") or 8))
            self.sp_stag.setMaximumWidth(110)
            self.lb_lanes = QLabel("", objectName="hint")
            self.lb_lanes.setWordWrap(True)
            self.w_lanes = QWidget()
            hr6 = QHBoxLayout(self.w_lanes); hr6.setContentsMargins(0, 0, 0, 0); hr6.setSpacing(10)
            hr6.addWidget(QLabel("Chạy cùng lúc", objectName="flabel"))
            hr6.addWidget(self.sp_lanes)
            hr6.addWidget(QLabel("video, mỗi tập lệch nhau", objectName="flabel"))
            hr6.addWidget(self.sp_stag)
            hr6.addWidget(self.lb_lanes, 1)
            self.w_lanes.setVisible(HIEN_DA_LUONG)
            if HIEN_DA_LUONG:
                top.addWidget(self.w_lanes, 4, 1, 1, 2)
            v.addLayout(top)
            self.ch_head = QLabel("Chưa quét. Nhập tên kênh rồi bấm Quét video.", objectName="hint")
            v.addWidget(self.ch_head)

            box2, v = card()
            page.addWidget(box2, 5)          # bảng video là thứ nhìn nhiều nhất → cho nhiều chỗ
            self.tbl = QTableWidget(0, 9)
            self.tbl.setHorizontalHeaderLabels(["Chọn", "Tên video", "View", "Dài",
                                                "Tên tập (sửa được)", "Tình trạng",
                                                "Người kể", "Giọng", "Output"])
            self.tbl.verticalHeader().setVisible(False)
            hh = self.tbl.horizontalHeader()
            hh.setSectionResizeMode(1, QHeaderView.Stretch)
            for c in (0, 2, 3, 5, 6, 7, 8):
                hh.setSectionResizeMode(c, QHeaderView.ResizeToContents)
            hh.setSectionResizeMode(4, QHeaderView.Interactive)
            self.tbl.setColumnWidth(4, 110)
            # Cột Output: bấm vào Ô CHỮ là mở thư mục kết quả trong Explorer — không cần widget
            # nút riêng, cellClicked bắt được click ở bất kỳ đâu trong ô.
            self.tbl.cellClicked.connect(self._mo_thu_muc_output)
            # Sàn chiều cao cho bảng. `stretch` của QVBoxLayout chỉ chia phần DƯ sau khi mọi thẻ
            # đã lấy đủ chiều cao tối thiểu — khối thông số + ô log lấy gần hết nên bảng từng bị
            # bóp còn 98px (nhìn thấy đúng 1 dòng) dù có 30 video và thanh cuộn vẫn tồn tại.
            self.tbl.setMinimumHeight(300)
            self.tbl.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.tbl.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            v.addWidget(self.tbl, 1)

            h = QHBoxLayout()
            h.setSpacing(9)
            self.bt_all = QPushButton("Tích tất cả")
            self.bt_none = QPushButton("Bỏ tích")
            self.bt_prev = QPushButton("🔎  Xem trước người kể + giọng", objectName="accent")
            self.bt_runsel = QPushButton("▶  Chạy các video ĐÃ TÍCH", objectName="primary")
            self.bt_runall = QPushButton("▶▶  Chạy TẤT CẢ video", objectName="accent")
            self.bt_dry2 = QPushButton("Chạy thử (không tốn tiền ảnh)")
            self.bt_stop2 = QPushButton("■  Dừng", objectName="danger"); self.bt_stop2.setEnabled(False)
            h.addWidget(self.bt_all); h.addWidget(self.bt_none)
            h.addWidget(self.bt_prev); h.addStretch(1)
            for b in (self.bt_runsel, self.bt_runall, self.bt_dry2, self.bt_stop2):
                h.addWidget(b)
            v.addLayout(h)

            box3, v = card()
            page.addWidget(box3, 2)
            self.bar2 = QProgressBar(); self.bar2.setRange(0, 1); self.bar2.setValue(0)
            self.bar2.setFormat("chưa chạy")
            v.addWidget(self.bar2)
            self.log0 = QPlainTextEdit(readOnly=True)
            # Chặn trần ô log: nó chỉ in tiến độ, không cần cao bằng bảng. Không chặn thì nó nở
            # theo cửa sổ và giành mất chỗ của bảng video — thứ thật sự cần nhìn.
            self.log0.setMinimumHeight(80)
            self.log0.setMaximumHeight(190)
            v.addWidget(self.log0, 1)
            v.addWidget(QLabel("Chạy lần lượt từng video. Một tập lỗi thì bỏ tập đó và làm tiếp "
                               "tập sau. Bấm Dừng là giết cả cây tiến trình để không tốn tiền ảnh.",
                               objectName="hint"))
            self.bt_scan.clicked.connect(self._scan)
            self.ch_src.returnPressed.connect(self._scan)
            self.bt_all.clicked.connect(lambda: self._tick(True))
            self.bt_none.clicked.connect(lambda: self._tick(False))
            self.bt_runsel.clicked.connect(lambda: self._run_batch(False, False))
            self.bt_runall.clicked.connect(lambda: self._run_batch(True, False))
            self.bt_dry2.clicked.connect(lambda: self._run_batch(False, True))
            self.bt_stop2.clicked.connect(self._stop_batch)
            self.bt_prev.clicked.connect(self._preview)
            self.bt_mkprof.clicked.connect(self._prefill_profile)
            # Đổi hồ sơ là đổi thư mục kết quả → phải chấm lại tình trạng từng tập.
            self.ch_profile.currentTextChanged.connect(lambda _: self._refresh_status())
            self.ck_skipdone.toggled.connect(lambda _: self._refresh_status())
            self.sp_lanes.valueChanged.connect(lambda _: self._cap_nhat_loi_khuyen())
            self._cap_nhat_loi_khuyen()
            return w

        # ---------------- tab 1
        def _tab_run(self):
            w = QWidget()
            page = QVBoxLayout(w)
            page.setContentsMargins(4, 12, 4, 4)
            page.setSpacing(12)
            box, v = card("Làm 1 video từ video đối thủ", "cardred")
            page.addWidget(box)
            g = QGridLayout()
            g.setHorizontalSpacing(10)
            g.setVerticalSpacing(9)
            g.setColumnStretch(1, 1)
            self.cb_profile = QComboBox()
            self._fill_profiles(self.cb_profile)
            self._pick_profile(self.cb_profile)
            self.ed_comp = QLineEdit(placeholderText="video_id hoặc URL YouTube của đối thủ")
            self.ed_slug = QLineEdit(placeholderText="tên thư mục tập, vd ep01")
            self.sp_min = QDoubleSpinBox(); self.sp_min.setRange(5, 90)
            self.sp_min.setValue(float(self.st.get("minutes") or 0) or 0)
            # 0 = để tool tự bám thời lượng video gốc (mặc định), gõ số là ép cứng.
            self.sp_min.setSpecialValueText("tự theo video gốc"); self.sp_min.setMinimum(0)
            self.cb_from = QComboBox(); self.cb_from.addItems([""] + STEPS)
            g.setColumnStretch(1, 0)
            g.setColumnStretch(2, 1)
            for r, (lbl, wid, hint) in enumerate([
                    ("Kênh (profile)", self.cb_profile,
                     "Hồ sơ kênh đã lập ở tab 3 — quyết định giọng, ngách, độ dài."),
                    ("Video đối thủ", self.ed_comp,
                     "Link hoặc id video muốn nhân bản. Bỏ trống nếu đã tự dán competitor.txt."),
                    ("Tên tập (slug)", self.ed_slug,
                     "Tên thư mục chứa kết quả, vd ep01. Trùng tên cũ là chạy tiếp tập đó."),
                    ("Độ dài (phút)", self.sp_min,
                     "Để trống là tập dài đúng bằng video gốc (kẹp 8–60 phút). "
                     "Gõ số để ép cứng."),
                    ("Chạy lại từ bước", self.cb_from,
                     "Để trống là chạy từ đầu. Chọn bước để làm lại từ đó — vd ảnh xấu thì chọn B5, "
                     "khỏi làm lại kịch bản.")]):
                self._row(g, r, lbl, wid, hint)
            v.addLayout(g)
            h = QHBoxLayout()
            h.setSpacing(9)
            self.bt_run = QPushButton("▶  Chạy", objectName="primary")
            self.bt_dry = QPushButton("Chạy thử (không tốn tiền ảnh)")
            self.bt_stop = QPushButton("■  Dừng", objectName="danger"); self.bt_stop.setEnabled(False)
            self.bt_save = QPushButton("Đặt làm mặc định", objectName="accent")
            h.addWidget(self.bt_run)
            for b in (self.bt_dry, self.bt_stop, self.bt_save):
                h.addWidget(b)
            h.addStretch(1)
            v.addLayout(h)

            box2, v = card()
            page.addWidget(box2, 1)
            self.bar = QProgressBar(); self.bar.setRange(0, len(STEPS)); self.bar.setValue(0)
            self.bar.setFormat("%v/%m bước")
            v.addWidget(self.bar)
            self.log = QPlainTextEdit(readOnly=True)
            v.addWidget(self.log, 1)
            v.addWidget(QLabel("Tool tự dừng ở bước nào không đạt QC — không tiêu tiền oan.",
                               objectName="hint"))
            self.bt_run.clicked.connect(lambda: self._start(False))
            self.bt_dry.clicked.connect(lambda: self._start(True))
            self.bt_stop.clicked.connect(self._stop)
            self.bt_save.clicked.connect(self._save)
            return w

        # ---------------- tab 2
        def _tab_new(self):
            w = QWidget()
            page = QVBoxLayout(w)
            page.setContentsMargins(4, 12, 4, 4)
            page.setSpacing(12)
            box, v = card("Lập kênh mới / sửa kênh đã có", "cardred")
            page.addWidget(box)
            # Chọn kênh có sẵn để NẠP toàn bộ thông số vào form — không phải gõ lại từ đầu.
            hl = QHBoxLayout(); hl.setSpacing(9)
            self.n_load = QComboBox(); self.n_load.setMaximumWidth(300)
            self.bt_load = QPushButton("Nạp vào form để sửa")
            hl.addWidget(QLabel("Sửa kênh đã có", objectName="flabel"))
            hl.addWidget(self.n_load); hl.addWidget(self.bt_load)
            hl.addWidget(QLabel("Hoặc bỏ qua dòng này để lập kênh hoàn toàn mới.",
                                objectName="hint"), 1)
            v.addLayout(hl)
            # THƯ MỤC DỮ LIỆU — đổi được, và PHẢI nằm ngoài thư mục cài.
            import paths
            hp = QHBoxLayout(); hp.setSpacing(9)
            self.n_data = QLineEdit(str(paths.DATA_DIR))
            self.bt_browse = QPushButton("Chọn…")
            self.bt_savedata = QPushButton("Lưu chỗ này", objectName="accent")
            self.bt_openp = QPushButton("Mở thư mục")
            hp.addWidget(QLabel("Thư mục dữ liệu", objectName="flabel"))
            hp.addWidget(self.n_data, 1)
            for b in (self.bt_browse, self.bt_savedata, self.bt_openp):
                hp.addWidget(b)
            v.addLayout(hp)
            v.addWidget(QLabel(
                "Nơi chứa hồ sơ kênh, keys.json, cài đặt và TOÀN BỘ video làm ra. Để NGOÀI thư "
                "mục cài tool — cập nhật tool là thay cả thư mục cài, để trong đó sẽ mất sạch. "
                "Đổi xong phải MỞ LẠI tool mới có hiệu lực.", objectName="hint"))
            g = QGridLayout()
            g.setHorizontalSpacing(10)
            g.setVerticalSpacing(9)
            g.setColumnStretch(1, 1)
            self.n_id = QLineEdit(placeholderText="samurai-history-jp")
            self.n_niche = QLineEdit(placeholderText="ngách, vd chuyện lịch sử samurai")
            self.n_persona = QLineEdit(placeholderText="tả người kể bằng tiếng Việt")
            self.n_lang = QComboBox(); self.n_lang.addItems(["ja", "ko", "en"])
            self.n_market = QLineEdit("JP")
            self.n_min = QDoubleSpinBox(); self.n_min.setRange(5, 90); self.n_min.setValue(30)
            self.n_voice = QLineEdit(placeholderText="để trống = lấy gợi ý số 1")
            # Nhãn tiếng Việt mô tả ĐÚNG thứ mỗi preset làm với âm thanh (xem tts.VOICE_FX),
            # còn giá trị thật vẫn là mã cũ — lấy bằng currentData(), KHÔNG lấy currentText().
            self.n_fx = QComboBox()
            for code, label in (
                    ("none", "none — giữ nguyên giọng gốc"),
                    ("old-mild", "old-mild — già nhẹ (trầm hơn 4%, bớt tiếng gió)"),
                    ("old-med", "old-med — già rõ (trầm 6% + đục tiếng) ★ chuẩn cho cụ ông/cụ bà"),
                    ("old-frail", "old-frail — già yếu (trầm 8% + rung giọng, nghe run run)"),
                    ("young", "young — trẻ lại (cao hơn 5%)"),
                    ("boom", "boom — vang dày (thêm bass, tiếng to đều, hợp thuyết minh hùng)"),
                    ("punch", "punch — nảy chữ (rõ tiếng, dứt khoát, hợp kể nhanh)")):
                self.n_fx.addItem(label, code)
            self.n_speed = QDoubleSpinBox(); self.n_speed.setRange(0.5, 1.5)
            self.n_speed.setSingleStep(0.02); self.n_speed.setValue(1.0)
            self.n_out = QLineEdit("assets/out")
            self.n_thumb_style = QLineEdit(
                placeholderText="để trống = ảnh thật điện ảnh (cũ). VD: Japanese manga/anime "
                                "illustration, cel-shaded flat colors, bold clean line art")
            g.setColumnStretch(1, 0)
            g.setColumnStretch(2, 1)
            rows = [
                ("Mã kênh (id)", self.n_id,
                 "Tên hồ sơ, cũng là tên thư mục. Nên đặt trùng tên kênh YouTube của anh."),
                ("Ngách", self.n_niche,
                 "Chủ đề kênh. AI bám câu này để chọn đề tài và cách kể."),
                ("Người kể (dự phòng)", self.n_persona,
                 "Chỉ dùng khi KHÔNG nhận được người kể từ video gốc. Bình thường mỗi tập tự nhận "
                 "người kể riêng (nam 60 làm tang lễ, nữ 73 về hưu…). Cứ tả một người tiêu biểu "
                 "của kênh: giới tính, tuổi, nghề, tính cách."),
                ("Ngôn ngữ", self.n_lang,
                 "Tiếng của kịch bản và giọng đọc. ja = Nhật, ko = Hàn, en = Anh."),
                ("Thị trường", self.n_market,
                 "Nước hướng tới. Quyết định bối cảnh, trang phục, kiểu nhà trong ảnh."),
                ("Độ dài (phút)", self.n_min,
                 "Chỉ là mức DỰ PHÒNG. Bình thường mỗi tập tự dài bằng video đang clone; "
                 "số này chỉ dùng khi không đo được video gốc."),
                ("Giọng", self.n_voice,
                 "Để trống là tool tự chọn giọng khớp ô Người kể. Bấm Tìm giọng để xem trước."),
                ("Hiệu ứng giọng (dự phòng)", self.n_fx,
                 "Bình thường tool tự chọn theo TUỔI người kể của từng tập: ≥75 old-frail · "
                 "68–74 old-med · 58–67 old-mild · dưới 45 none/young. Ô này chỉ dùng khi "
                 "không nhận được người kể."),
                ("Thư mục lưu video", self.n_out,
                 "Nơi đặt kết quả từng tập, tính từ thư mục chứa exe. Mỗi kênh nên một thư mục "
                 "riêng, vd assets/satori-jp."),
                ("Tốc độ (dự phòng)", self.n_speed,
                 "Cũng tự theo tuổi người kể: cụ già 0.90–0.92, trung niên 0.96–0.98, "
                 "trẻ 1.00. Ô này chỉ dùng khi không nhận được người kể."),
                ("Phong cách thumbnail", self.n_thumb_style,
                 "CỐ ĐỊNH cho cả kênh — mọi video chỉ đổi ảnh + chữ, không đổi phong cách nền. "
                 "Để trống = giữ ảnh thật điện ảnh. Đổi sau vẫn được, áp dụng từ video kế tiếp."),
            ]
            for r, (lbl, wid, hint) in enumerate(rows):
                self._row(g, r, lbl, wid, hint)
            v.addLayout(g)
            h = QHBoxLayout()
            h.setSpacing(9)
            self.bt_find = QPushButton("Tìm giọng theo mô tả", objectName="accent")
            self.bt_make = QPushButton("Tạo kênh + đo giọng", objectName="primary")
            self.bt_upd = QPushButton("💾  Cập nhật kênh này", objectName="accent")
            self.bt_recal = QPushButton("Đo lại giọng")
            h.addWidget(self.bt_make); h.addWidget(self.bt_upd)
            h.addWidget(self.bt_find); h.addWidget(self.bt_recal); h.addStretch(1)
            v.addLayout(h)
            v.addWidget(QLabel(
                "Sửa kênh đã có: chọn ở ô trên cùng → sửa các ô → bấm Cập nhật. Đổi ngách hay "
                "người kể thì GIỮ nguyên tốc độ đọc đã đo; chỉ khi đổi giọng/tốc độ/hiệu ứng/"
                "ngôn ngữ tool mới đo lại.", objectName="hint"))

            box2, v = card()
            page.addWidget(box2, 1)
            self.log2 = QPlainTextEdit(readOnly=True); v.addWidget(self.log2, 1)
            v.addWidget(QLabel("Bước đo char-rate là BẮT BUỘC — nó quyết định độ dài video.",
                               objectName="hint"))
            self._fill_profiles(self.n_load)
            self.bt_load.clicked.connect(self._load_profile)
            self.bt_openp.clicked.connect(self._open_profiles_dir)
            self.bt_browse.clicked.connect(self._browse_data)
            self.bt_savedata.clicked.connect(self._save_data_dir)
            self.bt_find.clicked.connect(self._find_voice)
            self.bt_recal.clicked.connect(self._recalibrate)
            self.bt_make.clicked.connect(lambda: self._make_profile(False))
            self.bt_upd.clicked.connect(lambda: self._make_profile(True))
            return w

        # ---------------- hành động tab quét kênh
        def _scan(self):
            src = self.ch_src.text().strip()
            if not src:
                QMessageBox.warning(self, "Thiếu", "Chưa nhập tên kênh hoặc URL kênh.")
                return
            if self.scanner and self.scanner.isRunning():
                return
            self.bt_scan.setEnabled(False)
            self.ch_head.setText(f"Đang quét {src} …")
            self.log0.appendPlainText(f"→ quét kênh: {src} (lấy {self.ch_limit.value()} video mới nhất)")
            self.scanner = ScanWorker(src, self.ch_limit.value())
            self.scanner.ok.connect(self._scan_ok)
            self.scanner.fail.connect(self._scan_fail)
            self.scanner.start()

        def _scan_fail(self, msg):
            self.bt_scan.setEnabled(True)
            self.ch_head.setText("Quét THẤT BẠI — xem log.")
            self.log0.appendPlainText(f"LỖI quét kênh: {msg}")

        # Thứ tự bước, để biết tập đang dở ở đâu.
        _BUOC = ["B2", "B3", "B3Q", "B4", "B4Q", "B5", "B5Q", "B7", "B8", "B8Q", "B9"]

        def _ep_dir(self, slug):
            """Thư mục kết quả của tập — đúng chỗ make_video ghi ra."""
            pid = self.ch_profile.currentText().strip()
            if not pid or pid.startswith("("):      # chưa có kênh nào
                return None
            try:
                import paths
                prof = profiles.load(pid)
                return paths.OUT_ROOT / (prof.get("slug_dir") or "assets/out") / slug
            except BaseException:
                # profiles.load() ném SystemExit khi không có hồ sơ — SystemExit KHÔNG phải
                # Exception, `except Exception` không bắt được và nó thoát luôn cả cửa sổ.
                return None

        def _ep_status(self, slug):
            """(chữ hiện trong bảng, đã_xong) — để quét kênh nhiều đợt không làm lại tập cũ.

            Máy vẫn tự bỏ qua bước đã xong nên chạy trùng KHÔNG tốn tiền, nhưng nó vẫn đi qua
            từng tập một; chạy 60 video mà 50 cái đã xong thì mất hàng chục phút vô ích, và
            người dùng cũng không nhìn ra cái nào còn thiếu.
            """
            d = self._ep_dir(slug)
            if not d or not d.exists():
                return "— chưa làm", False
            try:
                st = json.loads((d / "state.json").read_text(encoding="utf-8"))
            except Exception:
                st = {}
            # "Xong" = ĐĂNG ĐƯỢC NGAY: có video VÀ có gói đăng tải (tiêu đề/mô tả/thẻ).
            # Tập làm từ trước khi có bước B9 sẽ hiện "thiếu gói đăng tải" — chạy lại chỉ tốn
            # thêm ~10 giây cho riêng bước đó, không đụng gì tới ảnh hay video.
            if (d / "final.mp4").exists():
                if "B9" in st and (d / "DANG-TAI.txt").exists():
                    return "✔ đã xong", True
                return "⚠ thiếu gói đăng tải", False
            xong = [b for b in self._BUOC if b in st]
            return (f"⏳ dở ({xong[-1]})" if xong else "— chưa làm"), False

        def _slug_of(self, prefix, vid, title):
            """Tên thư mục tập. Dùng video_id nên KHÔNG đổi khi kênh đăng thêm video mới —
            chạy lại là nhận ra tập cũ và bỏ qua các bước đã xong, thay vì làm lại từ đầu.

            Bỏ dấu '-' đầu của id (id YouTube được phép bắt đầu bằng '-') kẻo ra tên hai gạch
            `simbot2--Gt6QYEFS38`."""
            return f"{prefix}-{str(vid).lstrip('-')}".strip("-")

        def _scan_ok(self, info):
            import channel_scan
            self.bt_scan.setEnabled(True)
            self.scan_info = info
            vids = info.get("videos") or []
            handle = info.get("handle") or ""
            self.ch_head.setText(
                f"{info.get('channel_title') or '(không tên)'} · @{handle} · {len(vids)} video "
                f"· quét {info.get('took_sec')}s")
            self.tbl.setRowCount(0)
            for r, e in enumerate(vids):
                self.tbl.insertRow(r)
                ck = QTableWidgetItem()
                ck.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                ck.setCheckState(Qt.Unchecked)
                ck.setData(Qt.UserRole, e.get("url"))
                self.tbl.setItem(r, 0, ck)
                for c, val in ((1, e.get("title") or ""),
                               (2, channel_scan._fmt_views(e.get("view_count"))),
                               (3, channel_scan._fmt_dur(e.get("duration")))):
                    it = QTableWidgetItem(str(val))
                    it.setFlags(Qt.ItemIsEnabled)          # chỉ đọc
                    self.tbl.setItem(r, c, it)
                slug = self._slug_of(handle or "ep", e.get("id"), e.get("title"))
                self.tbl.setItem(r, 4, QTableWidgetItem(slug))
                self._set_status(r, slug)
            n_xong = self._refresh_status()
            self.log0.appendPlainText(
                f"✓ {len(vids)} video · {n_xong} đã làm xong (bỏ tích sẵn) · "
                f"{len(vids) - n_xong} còn lại. Bấm Chạy.")
            d = load_settings()
            d.update({"channel_src": self.ch_src.text().strip(),
                      "channel_limit": self.ch_limit.value()})
            save_settings(d)

        def _o(self, r, c, txt):
            it = QTableWidgetItem(txt)
            it.setFlags(Qt.ItemIsEnabled)
            self.tbl.setItem(r, c, it)
            return it

        def _set_status(self, r, slug=None):
            slug = slug or self.tbl.item(r, 4).text().strip()
            txt, xong = self._ep_status(slug)
            self._o(r, 5, txt).setData(Qt.UserRole, xong)
            # Người kể + giọng: đọc từ hồ sơ kết quả nếu đã phân tích, chưa thì để trống.
            d = self._ep_dir(slug)
            st = {}
            if d and (d / "state.json").exists():
                try:
                    st = json.loads((d / "state.json").read_text(encoding="utf-8"))
                except Exception:
                    st = {}
            n, v = st.get("B2N") or {}, st.get("B4V") or {}
            ai = (f"{n.get('gender','')}/{n.get('age')} {n.get('role','')}".strip()
                  if n.get("gender") else "")
            self._o(r, 6, ai[:34])
            self._o(r, 7, f"{v.get('voice_name','')} {v.get('fx','')} {v.get('speed','')}".strip()
                    if v.get("voice_name") else "")
            # Cột Output: nút bấm TƯỢNG TRƯNG (nhãn cố định, không in đường dẫn ra ô cho gọn) —
            # đường dẫn thật nằm ở tooltip, `_mo_thu_muc_output` đọc tooltip để mở Explorer.
            # Chỉ hiện nút khi thư mục ĐÃ TỒN TẠI thật (`_ep_dir` chỉ TÍNH đường dẫn, không tạo).
            it = self._o(r, 8, "📂 Mở" if d and d.exists() else "—")
            if d and d.exists():
                it.setToolTip(str(d))
                f = it.font(); f.setUnderline(True); it.setFont(f)
                it.setForeground(self.tbl.palette().link())
            return xong

        def _mo_thu_muc_output(self, row, col):
            """Bấm ô Output -> mở thư mục kết quả bằng trình quản lý file mặc định của Windows.

            `os.startfile` là cách CHUẨN mở đúng ứng dụng mặc định (Explorer) mà không cần biết
            đường dẫn 'explorer.exe' nằm đâu — khác `subprocess` gọi thẳng exe (dễ lệch máy)."""
            if col != 8:
                return
            it = self.tbl.item(row, 8)
            d = it.toolTip() if it else ""
            if not d or not Path(d).exists():
                return
            try:
                os.startfile(d)                                   # noqa: Windows-only, tool chỉ chạy Windows
            except Exception as e:
                self.log0.appendPlainText(f"! Không mở được thư mục: {e}")

        def _refresh_status(self):
            """Cập nhật cột Tình trạng + BỎ TÍCH SẴN những tập đã xong. Trả về số tập đã xong.

            Quét kênh lần sau thường lẫn cả video đã clone đợt trước — không lọc thì bấm 'Chạy
            TẤT CẢ' là đi lại từng tập cũ (không mất tiền vì máy tự bỏ qua bước đã xong, nhưng
            mất hàng chục phút và làm rối log)."""
            n = 0
            for r in range(self.tbl.rowCount()):
                if self._set_status(r):
                    n += 1
                    self.tbl.item(r, 0).setCheckState(Qt.Unchecked)
            return n

        # Hạn mức đã đo trên máy này: gpti2 chỉ có 3 key, >24 lượt gọi cùng lúc là dính 429;
        # ffmpeg lúc ghép ăn ~25 GB RAM và ~16 luồng CPU nên 2 lượt ghép chồng nhau là hết máy.
        TONG_LUONG_ANH = 24
        TONG_LUONG_GHEP = 8

        def _chia_tai_nguyen(self):
            """Chia đều hạn mức cho từng luồng — chạy song song mà mỗi tập vẫn xin full là tự bóp."""
            n = max(1, self.sp_lanes.value())
            return max(4, self.TONG_LUONG_ANH // n), max(2, self.TONG_LUONG_GHEP // n)

        def _cap_nhat_loi_khuyen(self):
            n = self.sp_lanes.value()
            w, j = self._chia_tai_nguyen()
            if n == 1:
                t = "Chạy lần lượt từng tập — an toàn nhất, mỗi tập ~28 phút."
            else:
                t = (f"Mỗi tập dùng {w} luồng vẽ ảnh + {j} luồng ghép (chia từ "
                     f"{self.TONG_LUONG_ANH}/{self.TONG_LUONG_GHEP}). Lệch bước để tập này ghép "
                     f"video trong khi tập kia còn chờ mạng.")
                if n >= 4:
                    t += "  ⚠ 4 luồng dễ dính 429 ở khâu vẽ ảnh và hết RAM lúc ghép."
            self.lb_lanes.setText(t)

        def _tick(self, on):
            """Tích/bỏ tích tất cả. Khi tích, VẪN bỏ qua tập đã xong nếu đang bật lọc trùng."""
            bo_qua = self.ck_skipdone.isChecked()
            for r in range(self.tbl.rowCount()):
                xong = bool(self.tbl.item(r, 5) and self.tbl.item(r, 5).data(Qt.UserRole))
                dat = on and not (bo_qua and xong)
                self.tbl.item(r, 0).setCheckState(Qt.Checked if dat else Qt.Unchecked)

        def _rows(self, all_rows):
            """Các tập sẽ chạy. Trả thêm số tập bị loại vì đã xong, để báo cho người dùng biết."""
            out, bo = [], 0
            bo_qua = self.ck_skipdone.isChecked()
            for r in range(self.tbl.rowCount()):
                if not all_rows and self.tbl.item(r, 0).checkState() != Qt.Checked:
                    continue
                # Chặn ở ĐÂY chứ không chỉ ở ô tích: "Chạy TẤT CẢ" bỏ qua ô tích, mà đó lại
                # đúng là nút hay bấm nhất sau khi quét lại kênh.
                if bo_qua and self.tbl.item(r, 5) and self.tbl.item(r, 5).data(Qt.UserRole):
                    bo += 1
                    continue
                out.append((self.tbl.item(r, 4).text().strip(),
                            self.tbl.item(r, 0).data(Qt.UserRole),
                            self.tbl.item(r, 1).text()))
            return out, bo

        def _preview(self):
            """Chỉ chạy B2 (bóc lời) + nhận người kể + chốt giọng — KHÔNG tiêu tiền ảnh/giọng.

            Để nhìn trước cả loạt: video này ai kể, giọng nào, rồi mới quyết có chạy hay không.
            Kết quả ghi thẳng vào hồ sơ tập nên lượt chạy thật sau đó BỎ QUA hai bước này.
            """
            if self.worker and self.worker.isRunning():
                return
            if not self._co_profile():
                return
            rows, _ = self._rows(False)
            if not rows:
                rows, _ = self._rows(True)        # chưa tích gì thì phân tích cả bảng
            if not rows:
                QMessageBox.warning(self, "Chưa quét", "Hãy quét kênh trước.")
                return
            prof = self.ch_profile.currentText()
            jobs = [["--profile", prof, "--slug", s, "--competitor", u,
                     "--auto-voice", "--only", "B2"] for s, u, _ in rows]
            labels = [f"{s}  ·  {t[:46]}" for s, _, t in rows]
            self.log0.clear()
            self.log0.appendPlainText(
                f"→ XEM TRƯỚC {len(jobs)} video: bóc lời + nhận người kể + chọn giọng. "
                f"Không tốn tiền ảnh hay giọng đọc.")
            self.bar2.setRange(0, len(jobs)); self.bar2.setValue(0)
            self.worker = Runner(jobs, labels)
            self.worker.line.connect(lambda s: self.log0.appendPlainText(s))
            self.worker.job_begin.connect(
                lambda i, n, lbl: self.bar2.setFormat(f"xem trước [{i}/{n}] {lbl}"))
            self.worker.job_end.connect(self._job_end)
            self.worker.done.connect(self._batch_done)
            for b in (self.bt_runsel, self.bt_runall, self.bt_dry2, self.bt_scan, self.bt_prev):
                b.setEnabled(False)
            self.bt_stop2.setEnabled(True)
            self.worker.start()

        def _run_batch(self, all_rows, dry):
            if self.worker and self.worker.isRunning():
                return
            if not self._co_profile():
                return
            rows, da_bo = self._rows(all_rows)
            if not rows:
                QMessageBox.warning(
                    self, "Không có việc để chạy",
                    f"Đã loại {da_bo} video vì clone xong rồi." if da_bo else
                    "Chưa tích video nào. Bấm 'Tích tất cả' hoặc tích từng dòng.")
                return
            bad = [s for s, _, _ in rows if not s]
            if bad:
                QMessageBox.warning(self, "Thiếu tên tập", "Có dòng chưa có tên tập ở cột cuối.")
                return
            prof = self.ch_profile.currentText()
            jobs, labels = [], []
            for slug, url, title in rows:
                a = ["--profile", prof, "--slug", slug, "--competitor", url]
                if self.ck_autov.isChecked():
                    a.append("--auto-voice")
                if self.ck_srcmin.isChecked():
                    a.append("--minutes-from-source")
                if self.sp_lanes.value() > 1:
                    w, j = self._chia_tai_nguyen()
                    a += ["--img-workers", str(w), "--assemble-jobs", str(j)]
                if dry:
                    a.append("--dry-run")
                jobs.append(a)
                labels.append(f"{slug}  ·  {title[:46]}")
            # Tập làm dở KHÔNG chạy lại từ đầu: make_video.py đọc state.json trong thư mục tập rồi
            # bỏ qua mọi bước đã xong. Nói rõ ra đây, vì thanh tiến trình nhảy thẳng vào giữa
            # trông y như lỗi, dễ tưởng tool bỏ sót bước.
            tt = {self.tbl.item(r, 4).text().strip(): self.tbl.item(r, 5).text()
                  for r in range(self.tbl.rowCount()) if self.tbl.item(r, 4)}
            do = [s for s, _, _ in rows if tt.get(s, "").startswith("⏳")]
            self.log0.clear()
            if do:
                self.log0.appendPlainText(
                    f"↻ {len(do)} video làm dở — chạy TIẾP từ bước còn thiếu. Kịch bản/giọng/ảnh đã "
                    f"có được giữ nguyên, không làm lại, không tốn tiền lại:\n    · "
                    + "\n    · ".join(f"{s}  ({tt.get(s, '').strip()})" for s in do))
            self.log0.appendPlainText(
                f"→ {len(jobs)} video · profile {prof} · "
                f"{'giọng riêng từng video' if self.ck_autov.isChecked() else 'giọng theo profile'}"
                f" · {'độ dài bám video gốc' if self.ck_srcmin.isChecked() else 'độ dài theo hồ sơ'}"
                f"{f' · bỏ qua {da_bo} video đã clone xong' if da_bo else ''}"
                f"{f' · {self.sp_lanes.value()} luồng, lệch {self.sp_stag.value()} phút' if self.sp_lanes.value() > 1 else ' · 1 luồng'}"
                f"{' · CHẠY THỬ (không tốn tiền ảnh)' if dry else ''}")
            self.bar2.setRange(0, len(jobs)); self.bar2.setValue(0)
            self.worker = Runner(jobs, labels, lanes=self.sp_lanes.value(),
                                 stagger=self.sp_stag.value() * 60)
            self.worker.line.connect(lambda s: self.log0.appendPlainText(s))
            self.worker.job_begin.connect(
                lambda i, n, lbl: self.bar2.setFormat(f"[{i}/{n}] {lbl}"))
            self.worker.job_end.connect(self._job_end)
            self.worker.done.connect(self._batch_done)
            for b in (self.bt_runsel, self.bt_runall, self.bt_dry2, self.bt_scan,
                      self.bt_prev):
                b.setEnabled(False)
            self.bt_stop2.setEnabled(True)
            self.worker.start()

        def _job_end(self, i, lbl, rc):
            self.bar2.setValue(i)
            self.log0.appendPlainText(f"--- [{i}] {lbl}: {'XONG' if rc == 0 else f'LỖI {rc}'}")
            # Đổi cột Tình trạng NGAY khi tập đó xong, để nhìn là biết còn lại bao nhiêu.
            for r in range(self.tbl.rowCount()):
                if self.tbl.item(r, 4).text().strip() == lbl.split("·")[0].strip():
                    self._set_status(r)
                    break

        def _batch_done(self, rc):
            for b in (self.bt_runsel, self.bt_runall, self.bt_dry2, self.bt_scan,
                      self.bt_prev):
                b.setEnabled(True)
            self.bt_stop2.setEnabled(False)
            self.bar2.setFormat("xong" if rc == 0 else f"kết thúc, có tập lỗi (mã {rc})")
            self.log0.appendPlainText(f"=== KẾT THÚC CẢ LÔ (mã thoát {rc})")

        def _stop_batch(self):
            if self.worker:
                self.worker.stop()
                self.log0.appendPlainText("→ Đã bấm DỪNG (giết cả cây tiến trình).")

        def _prefill_profile(self):
            """Điền sẵn tab 'Lập kênh mới' theo kênh vừa quét — profile lấy ID/handle của kênh."""
            info = self.scan_info
            if not info:
                QMessageBox.information(self, "Quét trước", "Hãy quét kênh trước để lấy ID kênh.")
                return
            handle = (info.get("handle") or "").strip()
            self.n_id.setText(handle or "kenh-moi")
            # yt-dlp trả tên kênh kèm hậu tố tab (" - Videos") — bỏ đi kẻo lọt vào prompt ngách.
            self.n_niche.setText(re.sub(r"\s*-\s*(Videos|Shorts|Streams)$", "",
                                        info.get("channel_title") or ""))
            titles = [v.get("title", "") for v in (info.get("videos") or [])[:5]]
            self.n_persona.setText("người kể chuyện đời, giọng trầm ấm chậm rãi — theo kênh: "
                                   + " / ".join(t[:40] for t in titles[:3]))
            self.tabs.setCurrentIndex(2)
            self.log2.appendPlainText(
                f"→ Đã điền theo kênh @{handle}. Sửa lại Ngách/Người kể cho đúng rồi bấm "
                f"'Tạo kênh + đo giọng'.\n  5 video mới nhất: " + "\n    · ".join([""] + titles))

        # ---------------- hành động
        def _append(self, box, s):
            box.appendPlainText(s)
            # Dò "[BXX]" ở BẤT KỲ ĐÂU trong dòng (không chỉ đầu dòng) — từ khi Runner._one gắn
            # thêm tiền tố "slug - " trước tag để log dễ đọc, tag không còn nằm ở vị trí đầu tiên.
            m = re.search(r"\[([A-Za-z0-9_]+)\]", s)
            if m and m.group(1) in STEPS:
                self.bar.setValue(STEPS.index(m.group(1)) + 1)

        def _start(self, dry):
            if self.worker and self.worker.isRunning():
                return
            if not self.ed_slug.text().strip():
                QMessageBox.warning(self, "Thiếu", "Chưa nhập tên tập (slug).")
                return
            a = ["--profile", self.cb_profile.currentText(), "--slug", self.ed_slug.text().strip()]
            if self.ed_comp.text().strip():
                a += ["--competitor", self.ed_comp.text().strip()]
            if self.sp_min.value() > 0:
                a += ["--minutes", str(self.sp_min.value())]
            else:
                a.append("--minutes-from-source")
            if self.cb_from.currentText():
                a += ["--from", self.cb_from.currentText()]
            if dry:
                a += ["--dry-run"]
            self.log.clear(); self.bar.setValue(0)
            self.worker = Runner(a)
            self.worker.line.connect(lambda s: self._append(self.log, s))
            self.worker.done.connect(self._finished)
            self.bt_run.setEnabled(False); self.bt_dry.setEnabled(False)
            self.bt_stop.setEnabled(True)
            self.worker.start()

        def _stop(self):
            if self.worker:
                self.worker.stop()
                self._append(self.log, "→ Đã bấm DỪNG (giết cả cây tiến trình).")

        def _finished(self, rc):
            self.bt_run.setEnabled(True); self.bt_dry.setEnabled(True)
            self.bt_stop.setEnabled(False)
            self._append(self.log, f"=== KẾT THÚC (mã thoát {rc})")

        def _save(self):
            d = load_settings()
            d.update({"profile": self.cb_profile.currentText(),
                      "minutes": self.sp_min.value(),
                      "minutes_from_source": self.ck_srcmin.isChecked(),
                      "auto_voice": self.ck_autov.isChecked(),
                      "skip_done": self.ck_skipdone.isChecked(),
                      # Hàng đa luồng đang ẩn → giữ nguyên số cũ trong thiết lập, đừng ghi đè
                      # bằng số 1 ép cứng lúc dựng giao diện (bật lại là mất lựa chọn của user).
                      "lanes": (self.sp_lanes.value() if self.w_lanes.isVisible()
                                else self.st.get("lanes", 1)),
                      "stagger": self.sp_stag.value()})
            for k in KHONG_LUU:
                d.pop(k, None)
            save_settings(d)
            QMessageBox.information(self, "Đã lưu", "Đã đặt làm mặc định.")

        def _run_np(self, args, box):
            exe = [sys.executable] + (["--child", "new_profile.py"] if getattr(sys, "frozen", False)
                                      else [str(resource_path("new_profile.py"))])
            box.appendPlainText("$ " + " ".join(args))
            try:
                r = subprocess.run(exe + args, cwd=str(resource_path(".")), capture_output=True,
                                   text=True, encoding="utf-8", errors="replace",
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                box.appendPlainText((r.stdout or "") + (r.stderr or ""))
            except Exception as e:
                box.appendPlainText(f"LỖI: {e}")

        def _find_voice(self):
            self.log2.clear()
            self._run_np(["--find", self.n_persona.text().strip() or self.n_niche.text().strip()],
                         self.log2)

        def _open_profiles_dir(self):
            """Mở thư mục dữ liệu trong Explorer — hay cần để sao lưu hoặc chép sang máy khác."""
            import paths
            d = Path(self.n_data.text().strip() or str(paths.DATA_DIR))
            try:
                d.mkdir(parents=True, exist_ok=True)
                os.startfile(str(d))            # noqa: S606 — Windows, mở Explorer
            except Exception as e:
                self.log2.appendPlainText(f"Không mở được {d}: {e}")

        def _browse_data(self):
            from PySide6.QtWidgets import QFileDialog
            d = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu dữ liệu",
                                                 self.n_data.text().strip() or str(Path.home()))
            if d:
                self.n_data.setText(d)

        def _save_data_dir(self):
            """Ghi nhớ thư mục dữ liệu. Chặn chọn vào chính thư mục cài — đó là cả gốc vấn đề."""
            import paths
            moi = Path(self.n_data.text().strip() or "").expanduser()
            if not str(moi):
                return
            try:
                trong_cai = moi.resolve() == paths.EXE_DIR.resolve() or \
                    paths.EXE_DIR.resolve() in moi.resolve().parents
            except Exception:
                trong_cai = False
            if trong_cai and getattr(sys, "frozen", False):
                QMessageBox.warning(
                    self, "Chỗ này sẽ mất dữ liệu",
                    f"'{moi}' nằm TRONG thư mục cài tool.\n\nCập nhật tool = thay cả thư mục đó "
                    f"= mất hồ sơ kênh và toàn bộ video đã làm.\n\nChọn một chỗ khác, ví dụ "
                    f"{Path.home() / 'Documents' / paths.APP}.")
                return
            p, loi = paths.set_data_dir(moi)
            if loi:
                QMessageBox.warning(self, "Không lưu được", loi)
                return
            self.log2.appendPlainText(
                f"✓ Đã đặt thư mục dữ liệu: {p}\n"
                f"  Ghi nhớ ở: {paths.CONFIG_FILE}\n"
                f"  → ĐÓNG rồi MỞ LẠI tool để có hiệu lực. Dữ liệu cũ ở {paths.DATA_DIR} "
                f"KHÔNG tự chuyển — anh chép tay sang chỗ mới nếu cần giữ.")
            QMessageBox.information(self, "Đã lưu",
                                    f"Thư mục dữ liệu mới:\n{p}\n\nMở lại tool để có hiệu lực.")

        def _load_profile(self):
            """Nạp hồ sơ đã có vào form để sửa — khỏi phải gõ lại từ đầu."""
            pid = self.n_load.currentText().strip()
            if not pid or pid.startswith("("):
                return
            try:
                p = profiles.load(pid)
            except Exception as e:
                QMessageBox.warning(self, "Không đọc được", str(e))
                return
            n, vo = p.get("narrator", {}) or {}, p.get("voice", {}) or {}
            self.n_id.setText(p.get("id", pid))
            self.n_niche.setText(p.get("niche", ""))
            self.n_persona.setText(n.get("persona", ""))
            i = self.n_lang.findText(p.get("language", "ja"))
            if i >= 0:
                self.n_lang.setCurrentIndex(i)
            self.n_market.setText(p.get("market", ""))
            self.n_min.setValue(float(profiles.target_minutes(p)))
            self.n_voice.setText(vo.get("name") or vo.get("id", ""))
            j = self.n_fx.findData(vo.get("fx", "none"))
            if j >= 0:
                self.n_fx.setCurrentIndex(j)
            self.n_speed.setValue(float(vo.get("speed") or 1.0))
            self.n_out.setText(p.get("slug_dir") or "assets/out")
            self.n_thumb_style.setText((p.get("thumbnail", {}) or {}).get("art_style", ""))
            do = (f"đã đo {vo.get('char_rate')} lúc {vo['char_rate_measured_at']}"
                  if vo.get("char_rate_measured_at")
                  else f"CHƯA ĐO (đang tạm {vo.get('char_rate')})")
            self.log2.appendPlainText(
                f"→ Đã nạp '{pid}'. Tốc độ đọc: {do}.\n"
                f"  Sửa xong bấm 'Cập nhật kênh này'. Đổi giọng/tốc độ/hiệu ứng/ngôn ngữ thì "
                f"tool sẽ tự đo lại; đổi ngách hay người kể thì giữ nguyên số đã đo.")

        def _recalibrate(self):
            pid = (self.n_id.text().strip() or self.n_load.currentText().strip())
            if not pid or pid.startswith("("):
                QMessageBox.warning(self, "Chưa chọn kênh", "Chọn hoặc nhập mã kênh trước.")
                return
            self.log2.appendPlainText(f"→ Đo lại tốc độ đọc cho '{pid}' (đọc thử 1 câu) …")
            exe = [sys.executable] + (["--child", "calibrate.py"] if getattr(sys, "frozen", False)
                                      else [str(resource_path("calibrate.py"))])
            try:
                r = subprocess.run(exe + ["--profile", pid], cwd=str(resource_path(".")),
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace",
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                self.log2.appendPlainText((r.stdout or "") + (r.stderr or ""))
            except Exception as e:
                self.log2.appendPlainText(f"LỖI: {e}")

        def _make_profile(self, update=False):
            if not (self.n_id.text().strip() and self.n_niche.text().strip()
                    and self.n_persona.text().strip()):
                QMessageBox.warning(self, "Thiếu", "Cần id, ngách và mô tả người kể.")
                return
            self.log2.clear()
            a = ["--id", self.n_id.text().strip(), "--niche", self.n_niche.text().strip(),
                 "--persona", self.n_persona.text().strip(), "--lang", self.n_lang.currentText(),
                 "--market", self.n_market.text().strip() or "JP",
                 # currentData() chứ KHÔNG phải currentText(): ô đang hiện nhãn tiếng Việt dài,
                 # truyền nguyên nhãn xuống new_profile.py là báo "FX không có".
                 "--minutes", str(self.n_min.value()), "--fx", self.n_fx.currentData(),
                 "--speed", str(self.n_speed.value()),
                 "--slug-dir", self.n_out.text().strip() or "assets/out"]
            # --update GIỮ tốc độ đọc đã đo khi giọng không đổi; --yes ghi đè hẳn (đo lại từ đầu).
            a += ["--update"] if update else ["--yes"]
            if self.n_voice.text().strip():
                a += ["--voice", self.n_voice.text().strip()]
            if self.n_thumb_style.text().strip():
                a += ["--thumb-style", self.n_thumb_style.text().strip()]
            self._run_np(a, self.log2)
            for cb in (self.cb_profile, self.ch_profile, self.n_load):
                self._fill_profiles(cb)

    app = QApplication(sys.argv)
    app.setStyleSheet(_qss())           # đặt ở cấp APP để hộp thoại cũng ăn theme
    win = Win()
    win.show()
    # Móc kiểm thử: chạy không màn hình thì tự đóng sau N mili-giây. QTimer chỉ chạy được KHI ĐÃ có
    # QApplication, nên phải đặt ở đây chứ không đặt trong script test (bẫy đã dính).
    ms = os.environ.get("GUI_SELFCLOSE_MS")
    if ms:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(int(ms), lambda: (print(f"[test] cửa sổ '{win.windowTitle()}' "
                                                  f"{win.width()}x{win.height()}"), app.quit()))
    # Móc kiểm thử: lớp Win nằm TRONG hàm này (cố ý — để nhánh `--child` không phải nạp Qt), nên
    # script test bên ngoài không với tới được cửa sổ. Biến này cho nó một đường vào hợp lệ.
    hook = os.environ.get("GUI_TEST_HOOK")
    if hook:
        from PySide6.QtCore import QTimer
        import importlib

        def _run_hook():
            code = 1
            try:
                code = int(importlib.import_module(hook).run(win, app) or 0)
            except BaseException as e:
                import traceback
                print(f"[test] HOOK LỖI {type(e).__name__} {e}\n{traceback.format_exc()}")
            app.exit(code)

        QTimer.singleShot(50, _run_hook)
    return app.exec()


def _ensure_std():
    """BẮT BUỘC chạy TRƯỚC khi import bất kỳ module pipeline nào.

    Bản `--windowed` không có console, nên khi exe được mở bằng chuột (hoặc bởi một tiến trình
    cha cũng không có console) thì `sys.stdout` và `sys.stderr` là **None**, không phải luồng rỗng.
    Cả 23 module của pipeline đều gọi `sys.stdout.reconfigure(...)` ở CẤP MODULE, nên chỉ cần
    import một cái là nổ `'NoneType' object has no attribute 'reconfigure'` — và PyInstaller bản
    windowed bắt lỗi đó bằng một HỘP THOẠI MODAL, đứng chờ người bấm Close.

    Triệu chứng đã đo thật (2026-09-09, tốn gần một tiếng truy): tiến trình con 0% CPU, không log,
    không kết nối mạng, cha báo "B2 transcript lỗi (exit 1)" — nhìn y hệt TREO MẠNG, trong khi thật
    ra nó đang chờ một cú click vào hộp thoại mà chế độ windowed không cho ai thấy.

    Khi chạy từ giao diện thì `Runner` cấp `stdout=PIPE` nên luồng hợp lệ và nhánh devnull không
    bao giờ dùng tới — output vẫn về log đầy đủ.
    """
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _hide_child_windows():
    """Mọi tiến trình con chạy ẨN — không bật cửa sổ đen.

    `ffmpeg` là chương trình CONSOLE, mà một video 30 phút gọi nó hàng trăm lượt (mỗi ảnh một clip
    Ken Burns, rồi ghép, rồi cắt mẫu để QC). Không tắt cửa sổ thì màn hình nháy cửa sổ đen liên tục
    suốt buổi làm — user đã phản ánh thật 2026-09-09.

    Vá bằng cách bọc `subprocess.Popen` ngay tại cửa vào: `subprocess.run/call/check_output` đều đi
    qua Popen, nên một chỗ này che hết 12 chỗ gọi rải rác trong 6 file, và che luôn mọi chỗ viết
    thêm sau này. CHỈ thêm cờ khi lời gọi chưa tự đặt `creationflags` (nút DỪNG của giao diện dùng
    cờ riêng, không được đụng vào).
    """
    if os.name != "nt":
        return
    CREATE_NO_WINDOW = 0x08000000
    if getattr(subprocess.Popen, "_an_cua_so", False):
        return
    goc = subprocess.Popen.__init__

    def boc(self, *a, **kw):
        if not kw.get("creationflags"):
            kw["creationflags"] = CREATE_NO_WINDOW
        return goc(self, *a, **kw)

    subprocess.Popen.__init__ = boc
    subprocess.Popen._an_cua_so = True


def main():
    # Phải đứng ĐẦU TIÊN: mọi nhánh bên dưới đều import module pipeline, mà chúng nổ ngay nếu
    # sys.stdout là None (xem _ensure_std).
    _ensure_std()
    _hide_child_windows()
    try:
        return _dispatch(sys.argv[1:])
    except SystemExit:
        raise                            # thoát có chủ ý (QC không đạt, thiếu tham số…)
    except BaseException:
        # KHÔNG để lỗi thoát ra ngoài: bản windowed sẽ dựng HỘP THOẠI MODAL đứng chờ click, mà
        # tiến trình con thì không ai nhìn thấy — cả chuỗi đứng im, nhìn như treo mạng. Ghi ra
        # file cạnh exe rồi thoát bằng mã lỗi để tiến trình cha biết đường mà dừng.
        import traceback
        txt = (f"LỖI khi chạy: {' '.join(sys.argv[1:])[:300]}\n"
               f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n{traceback.format_exc()}")
        try:
            (BASE / "crash.log").write_text(txt, encoding="utf-8")
        except Exception:
            pass
        try:
            print(txt, file=sys.stderr)
        except Exception:
            pass
        return 3


def _dispatch(argv):
    if "--selftest" in argv:            # PHẢI đứng TRƯỚC khi tạo QApplication
        return selftest(argv)
    if argv and argv[0] == "--child":
        return run_child(argv[1:])
    if argv and argv[0] == "--make-video":
        import make_video
        sys.argv = ["make_video.py"] + argv[1:]
        return make_video.main() or 0
    return gui_main()


if __name__ == "__main__":
    sys.exit(main())
