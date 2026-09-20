"""render_engine.py — ORCHESTRATOR render 1-click 1 video YouTube faceless từ 1 slug đã chuẩn bị.

TỔNG QUÁT cho MỌI ngách/thị trường/ngôn ngữ (Satori JP, WW2 EN, Hàn…) — niche/market/language là THAM SỐ,
không khoá cứng: profile giọng qua --profile, bối cảnh QC qua --world / field "world" trong characters.json,
nhạc nền tự dò _bgm/*.mp3. Chạy TUẦN TỰ các bước cơ học, gọi từng script pipeline bằng CHÍNH interpreter
đang chạy (py -3.13). KHÔNG viết script/prompt/master (Claude làm) — chỉ render.

Input: thư mục slug BẤT KỲ (vd assets/<market>/<slug>/) đã có:
  script.txt · characters.json (có thể "characters":[] cho ngách không khoá mặt) · img_prompts.txt ·
  thumb_text.txt · masters nếu có REF-LOCK (_ref/001.png, _ref_<x>/001.png) ·
  (tuỳ chọn) thumb_bg_prompt.txt (Claude viết theo thumbnail.art_style → sinh nền thumbnail RIÊNG,
  không dùng ảnh 001.png của thân video — xem docs/PROFILE_ARCHITECTURE.md §thumbnail)
Output: voice*.{mp3,srt,wav} · img/*.png · thumb_final.png · final.mp4 · DANG-TAI.txt +
  TIEU_DE_MO_TA.txt (gói đăng tải, B9) + log QC từng bước.

Dùng (engine gọi từ GUI hoặc tay):
  py -3.13 render_engine.py --slug <abs path slug> [--profile satori-jp-obaa] [--no-pace] [--workers 8] [--dry-run]
In "[STEP i/N] <tên>" để GUI bám tiến độ. RESUME: bỏ qua bước đã có output. Lỗi 1 bước → dừng, exit 1.

⚠️ B4Q kiểm giọng HAI TẦNG (xem `qc_audio.py`): (1) `qc_visual.py voice` — LLM so SRT với script, bắt
đọc thiếu/cắt; (2) `qc_audio.py` — soi THẲNG SÓNG ÂM, bắt nghỉ-sai-chỗ/chết-tiếng/rụng-đoạn mà tầng 1
mù hoàn toàn (đo thật simbot2-vU5PWT2zLDs: 52 chỗ nghỉ giữa câu vẫn "ĐẠT" ở tầng 1). B4Q chạy SAU B4.2
(giãn nhịp) — kiểm ĐÚNG bản audio cuối cùng được ghép vào video, không phải bản thô trước khi giãn nhịp.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import wave
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
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
HERE = Path(__file__).resolve().parent
PY = sys.executable
# WORLD mặc định TỔNG QUÁT (mọi ngách); override bằng --world hoặc field "world" trong characters.json
GENERIC_WORLD = "cinematic realistic scene, authentic period-and-region-appropriate setting"


def log(*a):
    print(*a, flush=True)


def dur_sec(path):
    """Độ dài audio (giây). WAV = stdlib wave; khác = imageio-ffmpeg (best-effort, thiếu → 0)."""
    p = Path(path)
    if not p.exists():
        return 0
    if p.suffix.lower() == ".wav":
        with wave.open(str(p), "rb") as w:
            return round(w.getnframes() / w.getframerate())
    try:
        import imageio_ffmpeg, re
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        o = subprocess.run([ff, "-i", str(p)], capture_output=True, text=True).stderr
        m = re.search(r"Duration: (\d+):(\d+):(\d+)", o)
        return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) if m else 0
    except Exception:
        return 0


def run(cmd, dry):
    """Chạy 1 script pipeline, stream stdout ra realtime. Trả (ok, lines)."""
    log("  $ " + " ".join(str(c) for c in cmd[1:]))
    if dry:
        return True, []
    # KHÔNG CREATE_NO_WINDOW: kế thừa console (ẩn nếu từ GUI) → gen_images/ffmpeg không bật cửa sổ.
    p = subprocess.Popen([PY] + cmd, cwd=HERE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                         errors="replace", bufsize=1)
    lines = []
    for line in p.stdout:
        line = line.rstrip("\n")
        lines.append(line)
        log("    " + line)
    p.wait()
    return p.returncode == 0, lines


def run_multi(cmds, dry):
    """Chạy NHIỀU lệnh tuần tự trong CÙNG 1 bước — ok = TẤT CẢ đạt (dùng cho B4Q 2 tầng: LLM + sóng
    âm). Lệnh sau vẫn chạy dù lệnh trước lỗi, để thấy đủ vấn đề của cả hai tầng trong 1 lượt."""
    all_ok, all_lines = True, []
    for cmd in cmds:
        ok, lines = run(cmd, dry)
        all_ok = all_ok and ok
        all_lines += lines
    return all_ok, all_lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="đường dẫn thư mục slug (bất kỳ ngách nào)")
    ap.add_argument("--profile", default="satori-jp-obaa", help="id profile giọng (profiles/<id>.json)")
    # Giọng RIÊNG cho video này (override giọng mặc định của profile) — do detect_voice.py phân tích
    # transcript nguồn chọn ra. Trống = dùng giọng trong profile.
    ap.add_argument("--voice-id", default="", help="ép voice_id cho video này (vd elevenlabs_...)")
    ap.add_argument("--voice-fx", default="", help="fx giọng: none/old-med/young/boom/punch...")
    ap.add_argument("--voice-speed", default="", help="tốc độ 0.5-1.5 (vd 0.92 cho giọng già)")
    ap.add_argument("--no-pace", action="store_true", help="bỏ bước giãn nhịp (dùng voice.mp3 thẳng)")
    ap.add_argument("--quality", default="low")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--world", default="", help="bối cảnh cho QC ảnh (mặc định: field 'world' trong characters.json)")
    ap.add_argument("--bgm", default="", help="file nhạc nền (mặc định: tự dò _bgm/*.mp3; không có thì bỏ BGM)")
    ap.add_argument("--bgm-volume", default="0.09")
    ap.add_argument("--minutes", type=float, default=0.0,
                    help="độ dài mục tiêu (chỉ dùng để B9 chia chương đều khi kịch bản không đánh dấu "
                         "章; 0 = tự lấy target_minutes của profile)")
    ap.add_argument("--burn-sub", action="store_true",
                    help="CHÁY phụ đề vào hình (mặc định KHÔNG — xem assemble.burn_subs trong profile)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    S = Path(a.slug).resolve()
    dry = a.dry_run
    # kiểm input bắt buộc
    need = ["script.txt", "characters.json", "img_prompts.txt", "thumb_text.txt"]
    miss = [f for f in need if not (S / f).exists()]
    if miss:
        log(f"✗ THIẾU input trong {S.name}: {', '.join(miss)}"); return 2

    cdata = json.loads((S / "characters.json").read_text(encoding="utf-8"))
    chars = cdata.get("characters", [])
    world = a.world or cdata.get("world") or GENERIC_WORLD    # TỔNG QUÁT: đọc từ slug, không hardcode ngách
    masters = [S / c["master"] for c in chars if c.get("master")]
    for m in masters:
        if not m.exists():
            log(f"✗ THIẾU master: {m} (Claude cần gen+QC+đặt master trước)"); return 2
    ref_args = []
    if masters:
        ref_args += ["--ref", str(masters[0])]
    if len(masters) > 1:
        ref_args += ["--ref2", str(masters[1])]

    # BGM TỔNG QUÁT: --bgm > slug/_bgm/*.mp3 > slug.parent/_bgm/*.mp3 > không có (bỏ BGM)
    if a.bgm:
        bgm = Path(a.bgm)
    else:
        cands = sorted((S / "_bgm").glob("*.mp3")) + sorted((S.parent / "_bgm").glob("*.mp3"))
        bgm = cands[0] if cands else Path("__no_bgm__")
    # PHỤ ĐỀ — MẶC ĐỊNH KHÔNG CHÁY VÀO HÌNH (user chốt 2026-09-11): YouTube tự bật CC từ file .srt
    # mình up kèm, khán giả Nhật nghe hiểu nên chữ cháy chỉ che hình. File .srt VẪN được sinh đầy đủ
    # để up làm CC, và .srt vẫn dùng để đồng bộ đổi cảnh theo ranh giới câu. Kênh nào thật sự cần chữ
    # cháy thì khai `assemble.burn_subs: true` trong profile (KHÔNG if profile_id — xem CLAUDE.md).
    # ⚠️ DÙNG ĐÚNG TÊN FIELD của nhánh kia (`assemble.burn_subs`): `make_video.py::burn_subs()` và
    # cổng B10 `qc_final.py` đã đọc field đó. Đặt tên khác = hai nhánh hiểu khác nhau về cùng một
    # video, B10 lại đi soi "sao chưa cháy phụ đề" trên bản cố ý không cháy.
    burn_sub = a.burn_sub
    if not burn_sub:
        try:
            import profiles as _pf
            burn_sub = bool((_pf.load(a.profile).get("assemble") or {}).get("burn_subs", False))
        except Exception:
            burn_sub = False

    # ĐẾM BẰNG CHÍNH BỘ PHÂN TÍCH CỦA gen_images: đếm "mọi dòng không rỗng" là SAI — file có dòng
    # tiêu đề chương (═══ … ═══) mà gen_images bỏ qua. Đo thật 2026-09-10: 162 dòng nhưng chỉ 127 ảnh
    # → điều kiện "B5 xong" (số_ảnh >= n_prompt) không bao giờ đúng, bước B5 không bao giờ resume được.
    try:
        import gen_images
        n_prompt = len(gen_images.parse_prompts(S / "img_prompts.txt"))
    except Exception:
        n_prompt = sum(1 for l in (S / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
                       if l.strip() and not l.strip().startswith(("═══", "▶", "✅", "#", "//")))
    paced = not a.no_pace
    audio = S / ("voice_paced.wav" if paced else "voice.mp3")
    srt = S / ("voice_paced.srt" if paced else "voice.srt")

    # Giọng RIÊNG video này: CLI > voice.json (do detect_voice ghi) > giọng profile.
    vid, vfx, vspeed = a.voice_id, a.voice_fx, a.voice_speed
    vj = S / "voice.json"
    if not vid and vj.exists():
        try:
            d = json.loads(vj.read_text(encoding="utf-8"))
            vid = d.get("voice_id", ""); vfx = vfx or d.get("fx", ""); vspeed = vspeed or str(d.get("speed", ""))
        except Exception:
            pass
    voice_over = []
    if vid:
        voice_over += ["--voice", vid]
        if vfx:
            voice_over += ["--fx", vfx]
        if vspeed:
            voice_over += ["--speed", str(vspeed)]
        log(f"  giọng riêng video: {vid} fx={vfx or '(profile)'} speed={vspeed or '(profile)'}")

    # B7: ảnh nền thumbnail RIÊNG nếu Claude đã viết thumb_bg_prompt.txt (theo thumbnail.art_style),
    # khác img/001.png của thân video — tránh bẫy "mặt luôn ở giữa khung, chữ đè lên mặt" (B7Q cũ).
    def _kiem_thumb_text():
        """Máy kiểm ĐỊNH DẠNG trước khi ghép — đo thật 2026-09-14: ep07/ep11 dùng thumb_text.txt
        kiểu dòng trơn (không có `|`), thumbnail_text.py lặng lẽ BỎ QUA mọi dòng thiếu `|` → thumbnail
        ra 0 CHỮ, không lỗi gì cả (chỉ phát hiện được bằng cách MỞ ẢNH LÊN NHÌN). Từ nay chặn cứng ở
        đây thay vì để lọt ra sản phẩm hỏng câm lặng."""
        f = S / "thumb_text.txt"
        if not f.exists():
            return "thiếu thumb_text.txt"
        dong_hop_le = [ln for ln in f.read_text(encoding="utf-8").splitlines()
                       if ln.strip() and "|" in ln]
        if not dong_hop_le:
            return (f"{f.name} không có dòng nào đúng khuôn `MÀU|chữ` (thiếu dấu `|`) — ghép sẽ ra "
                    f"thumbnail 0 CHỮ. Sửa lại đúng khuôn rồi chạy lại B7.")
        return ""

    def do_b7():
        loi = _kiem_thumb_text()
        if loi:
            return False, [f"✗ B7 dừng: {loi}"]
        bg_prompt = S / "thumb_bg_prompt.txt"
        if bg_prompt.exists():
            bg_dir, bg_file, side = S / "_thumb", S / "_thumb" / "001.png", "left"
            cmds = []
            if not bg_file.exists():
                cmds.append(["gen_images.py", "--prompts", str(bg_prompt), "--out", str(bg_dir),
                             "--quality", "medium"])
            try:
                import profiles as _pf
                th = _pf.load(a.profile).get("thumbnail") or {}
            except Exception:
                th = {}
            extra = [str(x) for x in (th.get("extra_flags") or [])]   # cờ theo lane (xem make_video._thumb_flags)
            if th.get("side_width"):
                extra += ["--side-width", str(th["side_width"])]
            if th.get("max_font"):
                extra += ["--max-size", str(int(th["max_font"]))]
            cmds.append(["thumbnail_text.py", "--bg", str(bg_file), "--text", str(S / "thumb_text.txt"),
                         "--out", str(S / "thumb_final.png"), "--side", side] + extra)
            return run_multi(cmds, dry)
        # không có prompt riêng → như cũ, dùng ảnh đầu thân video (tương thích ngược)
        return run(["thumbnail_text.py", "--bg", str(S / "img" / "001.png"),
                    "--text", str(S / "thumb_text.txt"), "--out", str(S / "thumb_final.png")], dry)

    # B4Q: HAI TẦNG — qc_visual (LLM, so SRT với script) + qc_audio (sóng âm, bắt nghỉ-sai-chỗ/rụng-
    # đoạn mà LLM mù hoàn toàn). Dùng `audio`/`srt` = bản CUỐI (paced nếu bật), chạy SAU B4.2.
    def do_b4q():
        return run_multi([
            ["qc_visual.py", "voice", "--script", str(S / "script.txt"), "--srt", str(srt),
             "--audio-sec", str(dur_sec(audio))],
            ["qc_audio.py", "--audio", str(audio), "--srt", str(srt)],
        ], dry)

    # (tên, điều kiện RESUME đã xong, hàm chạy) — hàm trả (ok, lines)
    steps = [
        ("B4 giọng (TTS)", (S / "voice.mp3").exists(),
         lambda: run(["tts.py", "--script", str(S / "script.txt"), "--out", str(S / "voice.mp3"),
                      "--profile", a.profile] + voice_over, dry)),
        ("B4.1 sửa phụ đề khớp script", (S / "voice.stt.srt").exists(),
         lambda: run(["srt_from_script.py", "--srt", str(S / "voice.srt"),
                      "--script", str(S / "script.txt")], dry)),
        ("B4.2 giãn nhịp lời kể", (not paced) or (S / "voice_paced.wav").exists(),
         lambda: run(["pace_audio.py", "--audio", str(S / "voice.mp3"), "--srt", str(S / "voice.srt"),
                      "--script", str(S / "script.txt")], dry)),
        ("B4Q QC giọng+phụ đề+nghe", False, do_b4q),
        ("B5 gen ảnh (REF-LOCK)", len(list((S / "img").glob("*.png"))) >= n_prompt,
         lambda: run(["gen_images.py", "--prompts", str(S / "img_prompts.txt"), "--out", str(S / "img"),
                      *ref_args, "--quality", a.quality, "--workers", str(a.workers)], dry)),
        ("B5Q QC ảnh", False,
         lambda: run(["qc_visual.py", "images", "--dir", str(S / "img"),
                      "--prompts", str(S / "img_prompts.txt"), "--world", world, "--sample", "20"], dry)),
        ("B7 thumbnail", (S / "thumb_final.png").exists(), do_b7),
        # B7.5 — NEO ẢNH THEO ĐOẠN LỜI. Không có bước này thì `assemble.py` chia ảnh theo SỐ ĐẾM
        # và ảnh TRÔI dần so với lời, nặng dần về cuối (đo thật tập 04: B8Q 3,1/5, 3/5 mốc lệch nằm
        # sau phút 26 trên video 32 phút). KHÔNG CHẶN: thiếu `img_doan.txt` hoặc neo sai thì bỏ qua,
        # B8 tự quay về chế độ cũ — video vẫn ra, chỉ là ảnh có thể trôi. Thà trôi còn hơn chết
        # render sau khi đã trả tiền TTS.
        ("B7.5 neo ảnh↔lời", (S / "anchors.txt").exists(),
         lambda: run(["sinh_neo.py", "--slug", str(S)], dry)),
        ("B8 ghép video", (S / "final.mp4").exists(),
         lambda: run(["assemble.py", "--img", str(S / "img"), "--audio", str(audio), "--srt", str(srt),
                      *(["--anchors", str(S / "anchors.txt")] if (S / "anchors.txt").exists() else []),
                      *(["--burn-sub"] if burn_sub else []),
                      *(["--bgm", str(bgm), "--bgm-volume", a.bgm_volume] if bgm.exists() else []),
                      "--transition", "xfade", "--size", a.size, "--out", str(S / "final.mp4")], dry)),
        ("B8Q QC video", False,
         lambda: run(["qc_visual.py", "video", "--mp4", str(S / "final.mp4"), "--srt", str(srt),
                      *([] if burn_sub else ["--no-sub"]),
                      "--audio-sec", str(dur_sec(audio)), "--sample", "14"], dry)),
        # B8V bản duyệt tiếng Việt — KHÔNG phải bản đăng. User chốt 2026-09-11: mỗi tập kèm một bản
        # phụ đề Việt để soát nội dung có khớp ý không (kịch bản tiếng Nhật, user không đọc trực tiếp
        # được). KHÔNG CHẶN: thiếu bản duyệt thì video chính vẫn dùng được.
        ("B8V bản duyệt phụ đề Việt", (S / "final_vi.mp4").exists(),
         lambda: run(["sub_vi.py", "--slug", str(S), "--profile", a.profile], dry)),
        ("B9 gói đăng tải", (S / "DANG-TAI.txt").exists(),
         lambda: run(["publish_kit.py", "--slug", str(S), "--profile", a.profile,
                      "--minutes", str(a.minutes)], dry)),
        # B10 (qc_final.py, viết bởi lane não-ramcloud nhưng ĐÃ TỔNG QUÁT — không phụ thuộc
        # make_video.py::Job, dùng thư viện chung profiles/storyboard/assemble, tự nhận cả 2 tên
        # thumbnail thumbnail_final.png/thumb_final.png). Soi GÓI GIAO cuối: thumbnail ≤2MB/16:9,
        # tiêu đề/mô tả/thẻ đúng trần YouTube, mốc chương hợp lệ (sai luật = YouTube bỏ HẾT chương
        # mà không báo), phụ đề CÓ THẬT SỰ cháy vào hình không (B8Q không biết — mp4 vẫn ĐẠT dù
        # trống trơn). BLOCKING (khác B9): đây là lỗi THẬT trên file ĐÃ CÓ, không phải nội dung
        # thiếu — đúng triết lý "cổng QC mọi bước" của dự án.
        ("B10 nghiệm thu toàn tập", False,
         lambda: run(["qc_final.py", "--slug", str(S), "--profile", a.profile], dry)),
    ]

    # B9 là BỔ TRỢ: video CHÍNH (final.mp4) đã xong ở B8Q, thiếu gói đăng tải không nên coi là
    # "render hỏng" (khác a3's B2b: cùng triết lý "bổ trợ không chặn", xem b2b_comments()).
    KHONG_CHAN = {"B9 gói đăng tải", "B8V bản duyệt phụ đề Việt", "B7.5 neo ảnh↔lời"}

    n = len(steps)
    log(f"=== RENDER {S.name} | {n_prompt} ảnh | pace={'on' if paced else 'off'} | masters={len(masters)} ===")
    summary = []
    t_dau = time.perf_counter()          # ĐO THẬT: không có đồng hồ thì không trả lời được
    for i, (name, done, fn) in enumerate(steps, 1):    # "khâu nào chậm" ngoài việc đoán mò.
        log(f"\n[STEP {i}/{n}] {name}")
        if done and not dry:
            log("  ⏭ đã có output — bỏ qua (resume)")
            summary.append(f"{i}. {name}: ⏭ skip")
            continue
        t0 = time.perf_counter()
        ok, lines = fn()
        phut = (time.perf_counter() - t0) / 60
        log(f"  ⏱ {phut:.1f} phút")
        verdict = next((l.strip() for l in reversed(lines)
                        if any(k in l for k in ("ĐẠT", "HONG", "VẤN ĐỀ", "Xong", "✓", "cues", "cue:"))), "")
        summary.append(f"{i}. {name}: {'OK' if ok else 'LỖI'} [{phut:.1f}′] {verdict[:60]}")
        if not ok:
            if name in KHONG_CHAN:
                log(f"  ⚠️ {name} lỗi nhưng KHÔNG chặn (bổ trợ) — video chính vẫn dùng được.")
                continue
            log(f"\n✗ DỪNG ở [STEP {i}] {name} (lỗi). Sửa rồi chạy lại (resume bỏ bước đã xong).")
            log(f"\n=== TÓM TẮT (tổng {(time.perf_counter()-t_dau)/60:.1f} phút) ===\n" + "\n".join(summary))
            return 1

    log(f"\n✅ XONG: {S / 'final.mp4'}")
    log(f"=== TÓM TẮT (tổng {(time.perf_counter()-t_dau)/60:.1f} phút) ===\n" + "\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
