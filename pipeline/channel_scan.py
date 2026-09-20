"""channel_scan.py — QUÉT 1 kênh YouTube đối thủ → danh sách video (tên · view · thời lượng · id).

Đây là BƯỚC 0 của tool "làm từ đầu": người dùng dán URL/@handle kênh (vd @simbot2), tool liệt kê video để
CHỌN (tick) rồi mới chạy. Dùng yt-dlp `extract_flat` (KHÔNG tải gì, chỉ đọc metadata playlist /videos) —
nhanh (~1-3s cho 30 video), không đụng endpoint phụ đề nên KHÔNG dính 429 timedtext.

Trả về JSON:
  {channel_title, channel_id, handle, url, scanned_at, videos:[{id,title,view_count,duration,url,upload_date}]}

Dùng:
  py -3.13 channel_scan.py "@simbot2"                       # in bảng + lưu channels/<handle>.json
  py -3.13 channel_scan.py "https://youtube.com/@simbot2" --limit 40 --json
  py -3.13 channel_scan.py "<url>" --out channels/simbot2.json

Import (GUI dùng): from channel_scan import scan  ->  dict như trên.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path


def _ensure_std():
    """BẮT BUỘC trước khi đụng sys.stdout: bản .exe --windowed không có console → sys.stdout/stderr
    là None (không phải luồng rỗng), gọi .reconfigure() lên None nổ AttributeError câm lặng (skill
    tao_tool_exe.md #30-35, đã dính thật ở gui_video.py). Chạy từ GUI/pipe thì luồng hợp lệ, nhánh
    devnull không bao giờ dùng tới."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()

try:
    from paths import OUT_ROOT
    CH_DIR = OUT_ROOT / "channels"
except Exception:
    CH_DIR = Path(__file__).resolve().parent / "channels"


def _handle_of(url):
    """Rút @handle hoặc id kênh làm TÊN THƯ MỤC workspace (an toàn cho tên file)."""
    m = re.search(r"@([A-Za-z0-9_.-]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/(channel|c|user)/([A-Za-z0-9_-]+)", url)
    if m:
        return m.group(2)
    m = re.search(r"([A-Za-z0-9_-]{6,})", url)
    return m.group(1) if m else "channel"


def _norm_url(url):
    """@simbot2 / simbot2 / UC.... / URL đầy đủ → URL trang /videos của kênh."""
    u = url.strip()
    if u.startswith("http"):
        # đảm bảo lấy tab videos để không dính trang playlist khác
        if "/videos" not in u and ("/channel/" in u or "/@" in u or "/c/" in u or "/user/" in u):
            u = u.rstrip("/") + "/videos"
        return u
    if u.startswith("UC") and len(u) >= 20:
        return f"https://www.youtube.com/channel/{u}/videos"
    h = u[1:] if u.startswith("@") else u
    return f"https://www.youtube.com/@{h}/videos"


def scan(url, limit=60):
    """Quét kênh → dict. limit = số video mới nhất lấy về (0 = hết, có thể chậm với kênh lớn)."""
    import yt_dlp
    target = _norm_url(url)
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True,
            "skip_download": True, "ignoreerrors": True}
    if limit and limit > 0:
        opts["playlistend"] = int(limit)
    t0 = time.time()
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(target, download=False)
    if not info:
        raise SystemExit(f"Không đọc được kênh: {target} (kênh sai / riêng tư / bị chặn IP)")
    # kênh có thể trả tab lồng nhau (entries chứa playlist) → làm phẳng lấy đúng video
    entries = info.get("entries") or []
    if entries and entries[0] and entries[0].get("entries") is not None:
        flat = []
        for e in entries:
            flat += (e.get("entries") or [])
        entries = flat
    videos = []
    for e in entries:
        if not e or not e.get("id"):
            continue
        videos.append({
            "id": e.get("id"),
            "title": (e.get("title") or "").strip(),
            "view_count": e.get("view_count"),
            "duration": e.get("duration"),          # giây (có thể None với short/premiere)
            "upload_date": e.get("upload_date"),
            "url": e.get("url") or f"https://www.youtube.com/watch?v={e.get('id')}",
        })
    return {
        "channel_title": info.get("title") or info.get("channel") or "",
        "channel_id": info.get("channel_id") or info.get("id") or "",
        "handle": (info.get("uploader_id") or _handle_of(target)).lstrip("@"),
        "url": target,
        "scanned_at": time.strftime("%Y-%m-%d %H:%M"),
        "took_sec": round(time.time() - t0, 1),
        "videos": videos,
    }


def _fmt_views(v):
    if v is None:
        return "?"
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v/1_000:.0f}K"
    return str(v)


def _fmt_dur(s):
    if not s:
        return "?"
    s = int(s)
    return f"{s//60}:{s%60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel", help="URL kênh / @handle / id (vd @simbot2)")
    ap.add_argument("--limit", type=int, default=60, help="số video mới nhất lấy về (0 = hết)")
    ap.add_argument("--out", default="", help="file JSON lưu (mặc định channels/<handle>.json)")
    ap.add_argument("--json", action="store_true", help="in JSON thay vì bảng")
    a = ap.parse_args()

    data = scan(a.channel, a.limit)
    out = Path(a.out) if a.out else (CH_DIR / f"{data['handle']}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    if a.json:
        print(json.dumps(data, ensure_ascii=False))
        return 0
    print(f"KÊNH: {data['channel_title']}  (@{data['handle']} · {data['channel_id']})")
    print(f"{len(data['videos'])} video · quét {data['took_sec']}s → {out}\n")
    print(f"{'#':>3}  {'VIEW':>6}  {'DÀI':>6}  TÊN VIDEO")
    print("-" * 78)
    for i, v in enumerate(data["videos"], 1):
        print(f"{i:>3}  {_fmt_views(v['view_count']):>6}  {_fmt_dur(v['duration']):>6}  "
              f"{v['title'][:56]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
