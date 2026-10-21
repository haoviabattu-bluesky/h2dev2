"""B8n — phủ NÚT ĐĂNG KÝ KÊNH lên video giao (anh chốt 2026-09-30).

CHỈ LÀ LỚP PHỦ: không chèn đoạn, không dời/cắt thời gian. Sau khi phủ bắt buộc: số khung = gốc,
thời lượng lệch 0 — sai là DỪNG, giữ nguyên file gốc (không thay).

- Bật bằng profile `assemble.subscribe.enabled` (không có khối = bỏ qua). Mọi khác biệt giữa lane
  (avatar, kiểu click, kiểu chuông `bell_style`...) là field trong khối đó — cấm `if profile_id == ...`.
- File phủ = file giao (`giao_hang.chon_video_nguon`: final_with_hook.mp4, không có thì final.mp4),
  ghi `.partial.mp4` rồi `os.replace` về ĐÚNG tên cũ → B8Q / qc_final / B11 không phải sửa.
- Mốc: `start_times` [180, -120] tính trên file giao; `so_moc` chọn lại trong ±`moc_cua_so` giây
  (mặc định 60) sao cho tiếng nút rơi vào khoảng nghỉ / lúc chuyển ảnh (dò từ sóng âm + hình).
- Chống phủ 2 lần: `<video>.subscribe.json` giữ sha256 file ĐẦU RA; sha file hiện tại trùng → bỏ qua.
  B8 dựng lại từ đầu thì file mới có sha khác → phủ lại đúng 1 lần.
- Tool: `<gốc>/tools/subscribe_overlay` (h2dev hoặc bundle buoc2_3_tool), env SUBSCRIBE_TOOL_DIR ghi đè.
  Cache overlay đặt ở %LOCALAPPDATA% (không ghi vào thư mục Syncthing / dist).

Chạy tay 1 tập: py -3.13 nut_dang_ky.py --profile shakai_no_naze --slug ep07-xxx
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
KHOA_RIENG = {"moc_cua_so"}                      # khoá của pipeline, không đưa sang tool


def _tool_dir() -> Path:
    for p in (os.environ.get("SUBSCRIBE_TOOL_DIR"), HERE.parent / "tools" / "subscribe_overlay",
              Path(r"E:\CLAUDE\YOUTUBE\h2dev\tools\subscribe_overlay")):
        if p and (Path(p) / "subscribe_overlay.py").is_file():
            return Path(p)
    raise SystemExit("✗ B8n: không thấy tools/subscribe_overlay (đặt SUBSCRIBE_TOOL_DIR)")


def _nap_tool():
    td = _tool_dir()
    if str(td) not in sys.path:
        sys.path.insert(0, str(td))
    os.environ.setdefault("SUBSCRIBE_CACHE_DIR", str(Path(os.environ.get("LOCALAPPDATA") or Path.home())
                                                     / "h2dev_subscribe_cache"))
    import so_config, so_ffmpeg, so_moc, subscribe_overlay  # noqa: E401
    return so_config, so_ffmpeg, so_moc, subscribe_overlay


def _thu_muc_tam(src: Path) -> Path:
    """Chỗ làm việc NGOÀI Syncthing, cùng ổ với video (để os.replace không phải chép).
    Bẫy 2026-09-30: ghi .partial ngay trong thư mục tập (results/, shared/ = Syncthing) → Syncthing mở
    đọc file vừa ghi → os.replace ăn WinError 32 (file đang bị tiến trình khác dùng)."""
    d = Path(os.environ.get("SUBSCRIBE_WORK_DIR") or (Path(src.resolve().anchor) / "h2dev_subscribe_tmp"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _replace(a: Path, b: Path, lan: int = 60) -> None:
    """os.replace có thử lại — Syncthing/antivirus giữ file vài giây là chuyện thường trên Windows."""
    for i in range(lan):
        try:
            os.replace(a, b)
            return
        except PermissionError:
            if i == lan - 1:
                raise
            time.sleep(2)


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def _so_khung(ffmpeg: str, p: Path) -> int:
    e = subprocess.run([ffmpeg, "-hide_banner", "-i", str(p), "-map", "0:v", "-c", "copy", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = re.findall(r"frame=\s*(\d+)", e)
    return int(m[-1]) if m else -1


def chen(tap: Path, prof: dict) -> dict | None:
    blk = ((prof.get("assemble") or {}).get("subscribe") or {})
    if not blk.get("enabled"):
        return None
    import giao_hang
    src, _ = giao_hang.chon_video_nguon(tap)
    if not src.exists():
        raise SystemExit(f"✗ B8n: không có video để phủ nút: {src}")
    dau = src.with_suffix(".subscribe.json")
    if dau.exists():
        try:
            if json.loads(dau.read_text(encoding="utf-8")).get("sha_out") == _sha(src):
                print(f"  B8n: {src.name} đã có nút (khớp {dau.name}) → bỏ qua")
                return {"skipped": True}
        except Exception:
            pass
    so_config, ff, so_moc, so = _nap_tool()
    ov = {k: v for k, v in blk.items() if not k.startswith("_") and k not in KHOA_RIENG}
    cfg = so_config.load_config(None, ov)
    info = ff.probe(src)
    moc, bao = so_moc.choose_starts(src, cfg, info["duration"], float(blk.get("moc_cua_so", 60)))
    for r in bao:
        print(f"  B8n mốc {r['goc']:.1f}s → {r['chon']:.2f}s | tiếng nút đè lời {r['de_loi_giay']}s"
              f" (giữ gốc: {r.get('de_loi_giay_neu_giu_goc')}s) | chuyển ảnh {r.get('chuyen_anh')}")
    tam = _thu_muc_tam(src) / f"{src.stem}_{uuid.uuid4().hex[:8]}.mp4"
    res = so.apply_to_video(src, tam, overrides={**ov, "start_times": moc})
    k0, k1 = _so_khung(ff.ffmpeg_exe(), src), _so_khung(ff.ffmpeg_exe(), tam)
    loi = []
    if k0 != k1:
        loi.append(f"số khung {k1} ≠ gốc {k0}")
    if abs(res.get("duration_delta", 1)) > 0.0005:
        loi.append(f"thời lượng lệch {res.get('duration_delta')}s")
    if loi:
        tam.unlink(missing_ok=True)
        raise SystemExit("✗ B8n: phủ nút làm đổi video (" + "; ".join(loi) + ") → giữ nguyên bản gốc")
    _replace(tam, src)
    rec = {"video": src.name, "sha_out": _sha(src), "starts": moc, "moc": bao, "mode": res.get("mode"),
           "warnings": res.get("warnings"), "so_khung": k1, "duration": info["duration"],
           "config": {k: v for k, v in ov.items()}, "compose_seconds": res.get("compose_seconds")}
    dau.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ B8n: nút đăng ký {', '.join(f'{s:.1f}s' for s in moc)} | {res.get('mode')} | "
          f"{k1} khung = gốc | {res.get('compose_seconds')}s" + (f" | CẢNH BÁO {res['warnings']}" if res.get("warnings") else ""))
    return rec


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Phủ nút đăng ký kênh lên video giao của 1 tập")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    import profiles
    from paths import OUT_ROOT
    prof = profiles.load(a.profile)
    tap = OUT_ROOT / (prof.get("slug_dir") or "assets/out") / a.slug
    r = chen(tap, prof)
    if r is None:
        print("  B8n: profile chưa bật assemble.subscribe → không làm gì")
    return 0


if __name__ == "__main__":
    sys.exit(main())
