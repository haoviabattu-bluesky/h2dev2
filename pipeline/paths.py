r"""paths.py — một chỗ DUY NHẤT quyết định đường dẫn, để bản .exe không tìm nhầm chỗ.

Ba loại đường dẫn, đừng lẫn:

  DATA_DIR  — nơi GHI dữ liệu CỦA NGƯỜI DÙNG: hồ sơ kênh, keys.json, cài đặt, log.
  OUT_ROOT  — gốc để đặt thư mục tập (assets/out/<slug>) — video làm ra.
  res(rel)  — nơi ĐỌC tài nguyên đi kèm tool: `_MEIPASS` → cạnh exe → gốc dự án.

⚠️ BÀI HỌC ĐẮT (user chốt 2026-09-09): TUYỆT ĐỐI KHÔNG để dữ liệu người dùng trong thư mục
`dist/` cạnh exe. Cập nhật tool = thay cả thư mục đó = MẤT SẠCH hồ sơ kênh (kèm char-rate đo
bằng tiền thật) và toàn bộ video đã làm. Bản trước phải vá bằng cách "cất đi rồi trả lại" mỗi
lần build — chỉ chữa được lúc build trên máy này, không chữa được lúc user tự thay bản mới.

Nay dữ liệu nằm NGOÀI thư mục cài, mặc định `Documents\YoutubeCloneGemini`, và người dùng ĐỔI
ĐƯỢC. Chỗ đã chọn ghi vào `%APPDATA%\YoutubeCloneGemini\config.json` — thư mục này thuộc về
người dùng chứ không thuộc bản cài, nên gỡ/thay tool bao nhiêu lần cũng còn.

Bí danh env `YTCG_DATA_DIR` thắng tất cả — tiện để chạy thử hoặc chạy nhiều bản song song.
"""
import json
import os
import sys
from pathlib import Path

APP = "YoutubeCloneGemini"

FROZEN = getattr(sys, "frozen", False)
HERE = Path(__file__).resolve().parent                 # pipeline/ (hoặc _internal/ khi frozen)
MEI = Path(getattr(sys, "_MEIPASS", "")) if getattr(sys, "_MEIPASS", "") else None
EXE_DIR = Path(sys.executable).resolve().parent if FROZEN else HERE

# Nơi nhớ "người dùng chọn thư mục dữ liệu nào" — KHÔNG nằm trong thư mục cài.
CONFIG_DIR = Path(os.environ.get("APPDATA") or (Path.home() / ".config")) / APP
CONFIG_FILE = CONFIG_DIR / "config.json"


def read_config():
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def default_data_dir():
    """Mặc định: Documents\\<APP>. Chạy từ mã nguồn thì giữ nguyên thư mục dự án như cũ."""
    if not FROZEN:
        return HERE
    doc = Path.home() / "Documents"
    return (doc if doc.is_dir() else Path.home()) / APP


def resolve_data_dir():
    for nguon in (os.environ.get("YTCG_DATA_DIR"), read_config().get("data_dir")):
        if not nguon:
            continue
        p = Path(nguon).expanduser()
        try:
            p.mkdir(parents=True, exist_ok=True)
            return p
        except Exception as e:
            print(f"  ! không dùng được thư mục dữ liệu '{p}' ({e}) → dùng mặc định")
    p = default_data_dir()
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p


def set_data_dir(path):
    """Ghi nhớ thư mục dữ liệu mới. Trả (đường dẫn, lỗi) — lỗi rỗng là thành công.

    Chỉ có hiệu lực sau khi MỞ LẠI tool: nhiều module đã đọc DATA_DIR lúc nạp."""
    p = Path(str(path).strip()).expanduser()
    try:
        p.mkdir(parents=True, exist_ok=True)
        (p / ".ghi_thu").write_text("ok", encoding="utf-8")
        (p / ".ghi_thu").unlink()
    except Exception as e:
        return p, f"không ghi được vào đây: {e}"
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        d = read_config()
        d["data_dir"] = str(p)
        CONFIG_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        return p, f"không lưu được lựa chọn: {e}"
    return p, ""


DATA_DIR = resolve_data_dir()
# Nơi chứa assets/out/<slug>. Chạy từ mã nguồn thì mặc định là gốc dự án, NHƯNG nếu đã chỉ
# YTCG_DATA_DIR thì phải theo đó — không thì chạy tay để sửa/ghép lại một tập do bản .exe làm ra
# sẽ trỏ sang thư mục khác và báo "thiếu competitor.txt" dù tập nằm sờ sờ ở chỗ kia.
OUT_ROOT = DATA_DIR if (FROZEN or os.environ.get("YTCG_DATA_DIR")) else HERE.parent


def res(rel):
    """Đường dẫn tài nguyên CHỈ ĐỌC (skills/, assets/voice_bank.json, script .py bundle).

    Thứ tự: bản bundle trong _internal → bản cạnh exe → thư mục dữ liệu → gốc dự án lúc dev."""
    rel = str(rel).replace("\\", "/")
    for base in [MEI, EXE_DIR, DATA_DIR, HERE, HERE.parent]:
        if base and (base / rel).exists():
            return base / rel
    return (MEI or HERE.parent) / rel                   # trả về đường dẫn "đúng lý" để báo lỗi rõ
