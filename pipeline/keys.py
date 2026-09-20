"""keys.py — một chỗ DUY NHẤT đọc API key, để đổi key ở máy khác KHÔNG phải build lại exe.

Vì sao cần: `llm_client.load_key()` chỉ phủ key LLM (ramclouds/ns24). Key ẢNH (gpti2 3 key,
Grok) và key TTS (OpenSpeaker) trước đây nằm CỨNG trong code — một key gpti2 hết tiền (402) ở
máy khách là phải build lại exe mới đổi được. Nay mọi key đều tra qua đây.

Thứ tự tra (dừng ở nơi đầu tiên có giá trị):
  1. biến môi trường          — tiện chạy CI / thử nhanh, không để lại dấu trên đĩa
  2. keys.json CẠNH exe       — cách người dùng cuối đổi key (sửa file, chạy lại, khỏi build)
  3. keys.txt CẠNH exe        — dạng `ten=giatri` cho người không quen JSON
  4. keys.json ở gốc dự án    — lúc dev
  5. mặc định trong code      — để bản gửi đi vẫn chạy được ngay khi chưa có keys.json

Khoá trong keys.json (xem keys.sample.json):
  ramclouds · ns24 · gpti2 (chuỗi HOẶC danh sách nhiều key) · grok · openspeaker ·
  sol/sol_base_url/sol_model (9router local, QC thumbnail GPT-5.6-sol) ·
  sol_backup/sol_backup_base_url/sol_backup_model (dự phòng ns24 khi 9router lỗi, xem sol_client.py)
"""
import json
import os
import sys
from pathlib import Path

_cache = {}


def _files():
    """Nơi tìm key, ưu tiên giảm dần.

    THƯ MỤC DỮ LIỆU đứng trước thư mục cài: key người dùng tự đặt phải sống sót qua mỗi lần
    cập nhật tool, còn bản cạnh exe chỉ là bản phát kèm."""
    here = Path(__file__).resolve().parent
    exe_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else here
    try:
        from paths import DATA_DIR
        data = [DATA_DIR / "keys.json", DATA_DIR / "keys.txt"]
    except Exception:
        data = []
    return data + [exe_dir / "keys.json", exe_dir / "keys.txt",
                   here.parent / "keys.json", here / "keys.json"]


def _read_all():
    """Gộp mọi file key thành 1 dict. Đọc 1 lần rồi nhớ — mỗi ảnh gọi 1 lần thì tốn I/O vô ích."""
    if "_d" in _cache:
        return _cache["_d"]
    d = {}
    for f in reversed(_files()):          # file ưu tiên CAO đọc SAU để ghi đè file ưu tiên thấp
        if not f.exists():
            continue
        try:
            if f.suffix == ".json":
                got = json.loads(f.read_text(encoding="utf-8"))
                if isinstance(got, dict):
                    d.update({str(k).strip().lower(): v for k, v in got.items()})
            else:
                for line in f.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    d[k.strip().lower()] = v.strip()
        except Exception as e:
            print(f"  ! doc {f.name} loi: {type(e).__name__} {e}")
    _cache["_d"] = d
    return d


def _split(v):
    """Giá trị trong file có thể là danh sách, hoặc 1 chuỗi nhiều key cách nhau bằng , ; hay dòng."""
    if isinstance(v, (list, tuple)):
        items = [str(x) for x in v]
    else:
        s = str(v)
        for sep in (",", ";"):
            s = s.replace(sep, "\n")
        items = s.splitlines()
    return [x.strip() for x in items if x.strip()]


def get(name, env="", default=""):
    """Một key dạng chuỗi. `name` là khoá trong keys.json, `env` là tên biến môi trường."""
    if env:
        v = os.environ.get(env)
        if v and v.strip():
            return v.strip()
    v = _read_all().get(name.lower())
    if v:
        got = _split(v)
        if got:
            return got[0]
    return default


def get_list(name, env="", default=()):
    """Nhiều key cùng loại (gpti2 luân phiên 3 key vì RPM tính THEO TỪNG key)."""
    if env:
        v = os.environ.get(env)
        if v and v.strip():
            return _split(v)
    v = _read_all().get(name.lower())
    if v:
        got = _split(v)
        if got:
            return got
    return list(default)


def source(name, env=""):
    """Key đang lấy từ đâu — để --selftest in ra mà KHÔNG in giá trị key."""
    if env and os.environ.get(env, "").strip():
        return f"bien moi truong {env}"
    if _read_all().get(name.lower()):
        return "keys.json/keys.txt"
    return "mac dinh trong code"


def reset():
    """Xoá bộ nhớ tạm — dùng trong test khi vừa ghi keys.json mới."""
    _cache.clear()
