"""tts.py — giọng đọc + PHỤ ĐỀ .srt sync chuẩn từ script (Nhật/Hàn) bằng edge-tts (FREE).

Stream edge-tts để bắt CẢ audio LẪN WordBoundary (timing từng từ) → gom thành phụ đề câu (ngắt theo
。！？!? và độ dài tối đa) → xuất .srt khớp chính xác giọng đọc. Multi-chunk: cộng dồn offset theo độ
dài mp3 thực của từng chunk.

Dùng:
  py -3.13 tts.py --script ../assets/satori_jp/<slug>/script.txt --out ../assets/satori_jp/<slug>/voice.mp3
  → tạo voice.mp3 + voice.srt (cùng thư mục, cùng tên)
  py -3.13 tts.py --script s.txt --voice ja-JP-NanamiNeural --rate=-8% --out voice.mp3 --no-srt
  py -3.13 tts.py --script s.txt --voice ko-KR-InJoonNeural --out voice.mp3     # bản Hàn

Giọng: ja-JP-KeitaNeural / ja-JP-NanamiNeural / ko-KR-InJoonNeural / ko-KR-SunHiNeural.
LƯU Ý: --rate/--pitch phải dạng có dấu '=' (vd --rate=-8%) vì argparse hiểu -8% là flag.
Cần: edge-tts + imageio-ffmpeg.
"""
import argparse
import asyncio
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts
import imageio_ffmpeg

sys.stdout.reconfigure(encoding="utf-8")
FF = imageio_ffmpeg.get_ffmpeg_exe()

_STRIP = re.compile(r"(═══.*?═══|\[[^\]]*\]|「?(パート\d+|停止|続けて|脚本完成)」?|"
                    r"^(TITLE|字数|推定尺|STATS|WORD COUNT|ESTIMATED).*$)", re.MULTILINE)

# Hậu kỳ FX giọng — 2 CHIỀU: làm già (old-*) HOẶC làm trẻ/khoẻ/vang (young/boom/punch).
# MỌI preset giữ NGUYÊN thời lượng (asetrate×k rồi atempo×1/k) → SRT của server vẫn khớp.
# Đo thật 2026-09-07 trên 47,6s: none −18,5dB · young −18,9 · boom −17,2 · punch −16,7 (dur 47,6–47,7s).
VOICE_FX = {
    "none": "",
    # ---- làm GIÀ (cụ bà/cụ ông) — "old-med" là mức đã chốt cho ngách Satori
    "old-mild": "asetrate=44100*0.96,aresample=44100,atempo=1.0417,lowpass=f=8000",
    "old-med":  "asetrate=44100*0.94,aresample=44100,atempo=1.0638,equalizer=f=4000:t=q:w=1.2:g=-4,lowpass=f=6800",
    "old-frail": "asetrate=44100*0.92,aresample=44100,atempo=1.087,equalizer=f=3500:t=q:w=1.5:g=-5,lowpass=f=6000,tremolo=f=5.5:d=0.06",
    # ---- làm TRẺ / KHOẺ / VANG (trai trẻ, võ tướng, thuyết minh năng lượng cao)
    "young": "asetrate=44100*1.05,aresample=44100,atempo=0.9524",
    "boom": "equalizer=f=110:t=q:w=1.0:g=4,acompressor=threshold=-18dB:ratio=3:attack=8:release=180,"
            "aecho=0.8:0.85:35:0.18,loudnorm=I=-14:TP=-1.5",
    "punch": "acompressor=threshold=-20dB:ratio=4:attack=5:release=120,"
             "equalizer=f=3000:t=q:w=1.2:g=3,loudnorm=I=-13:TP=-1.0",
}
# tên cũ (--age mild/med/frail) → tên mới, để lệnh/profile cũ không vỡ
FX_ALIAS = {"mild": "old-mild", "med": "old-med", "frail": "old-frail"}
AGE_FILTERS = VOICE_FX          # tương thích code cũ import AGE_FILTERS


SPEED_MAC_DINH = 0.95


def resolve_voice_conf(args, prof_id):
    """Chốt giọng + hiệu ứng + tốc độ cho LƯỢT ĐỌC NÀY. Sửa args tại chỗ.

    Thứ tự: cờ dòng lệnh TƯỜNG MINH → hồ sơ kênh → mặc định.

    BẪY ĐÃ DÍNH (2026-09-09): bản cũ coi `fx == "none"` là "chưa chọn gì" nên rơi về fx của hồ sơ.
    Từ khi mỗi tập tự nhận người kể riêng, tool truyền `--fx none` cho người kể TRUNG NIÊN — và bị
    hồ sơ (`old-med`, dựng cho cụ bà 80) đè lên, làm ông 60 tuổi nghe như cụ già. Lỗi CÂM LẶNG:
    không báo gì, chỉ nghe ra khi mở file audio. Nay phân biệt "KHÔNG truyền" (default None/"")
    với "truyền đúng giá trị đó" — `--fx none` nghĩa là THẬT SỰ không áp hiệu ứng.
    """
    fx_tuong_minh = bool(args.fx or args.age)     # --fx thắng --age (tên cũ)
    args.age = normalize_fx(args.fx or args.age or "none")
    if prof_id:
        import profiles
        prof = profiles.load(prof_id)
        v, fx, sp = profiles.voice_conf(prof)
        if not args.voice:
            args.voice = v
        if not fx_tuong_minh:
            args.age = normalize_fx(fx)
        if args.speed is None:
            args.speed = sp
        print(f"[profile {prof_id}] voice={args.voice} fx={args.age} speed={args.speed}"
              f"{'' if fx_tuong_minh else ' (fx theo hồ sơ)'} · {profiles.narrator_line(prof)}")
    if args.speed is None:
        args.speed = SPEED_MAC_DINH
    return args


def normalize_fx(name):
    name = (name or "none").strip()
    return FX_ALIAS.get(name, name)


def apply_fx(mp3_path, fx):
    """Áp preset FX lên mp3 (in-place). Không đổi thời lượng → SRT vẫn khớp."""
    fx = normalize_fx(fx)
    if fx not in VOICE_FX:
        raise SystemExit(f"FX '{fx}' không có. Chọn: {', '.join(VOICE_FX)}")
    af = VOICE_FX[fx]
    if not af:
        return
    import imageio_ffmpeg as _iff
    ff = _iff.get_ffmpeg_exe()
    tmp_out = str(mp3_path) + ".fx.mp3"
    subprocess.run([ff, "-y", "-i", str(mp3_path), "-af", af, tmp_out],
                   check=True, capture_output=True)
    Path(tmp_out).replace(mp3_path)
    print(f"  → đã áp FX giọng (fx={fx})")


apply_age = apply_fx            # tương thích code cũ gọi apply_age(path, level)


def chuan_muc(mp3_path, I=-16.0, TP=-1.5):
    """Chuẩn hoá âm lượng + hạ trần đỉnh (in-place). KHÔNG đổi thời lượng → SRT vẫn khớp.

    Vì sao bắt buộc: file thô của ElevenLabs đo được đỉnh **−0,1 dBFS** (B4Q bắt: "chạm trần, có
    thể VỠ TIẾNG"). Preset FX làm-già có sẵn loudnorm nên kênh satori vô tình thoát; kênh nào để
    fx=none thì đi thẳng ra video với đỉnh chạm trần. Đưa về −16 LUFS / trần −1,5 dBTP: dưới ngưỡng
    YouTube tự hạ (−14 LUFS) một chút, còn chỗ cho nhạc nền trộn vào mà không vỡ.
    """
    import imageio_ffmpeg as _iff
    ff = _iff.get_ffmpeg_exe()
    tmp_out = str(mp3_path) + ".ln.mp3"
    try:
        subprocess.run([ff, "-y", "-i", str(mp3_path),
                        "-af", f"loudnorm=I={I}:TP={TP}:LRA=11", "-b:a", "192k", tmp_out],
                       check=True, capture_output=True)
        Path(tmp_out).replace(mp3_path)
        print(f"  → chuẩn hoá mức tiếng (I={I} LUFS, trần {TP} dBTP)")
    except Exception as e:
        Path(tmp_out).unlink(missing_ok=True)
        print(f"  ! không chuẩn hoá được mức tiếng ({type(e).__name__}) → giữ nguyên")
_SENT_END = "。．.!?！？"          # ngắt cue ở đây
_MAX_CUE_CHARS = 24               # hoặc khi vượt độ dài này


def clean(text):
    text = _STRIP.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def ap_yomi(text, path):
    """Sidecar `yomi.txt` (mỗi dòng `表示=読み`): thay chữ hiển thị bằng cách đọc TRƯỚC khi gửi TTS.
    Vì sao: TTS đọc sai kanji hiếm/tên riêng (他人様, 満州…) mà không cổng nào bắt được — STT nghe
    lại đúng cái TTS đọc sai, srt_from_script lại nắn phụ đề về script nên mọi thứ "khớp". Sửa ở
    NGUỒN: script.txt giữ nguyên (caption ra kanji), chỉ text gửi provider đổi. Ý mượn từ Dual Text
    `<表示|読み>` của hypit, thu về sidecar để không đụng 39 file đang đọc script.txt
    (plans/260921-1415-muon-hypit-openmontage). Trả (text, {mục: số lần thay})."""
    muc = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "=" not in ln:
            continue
        a, _, b = ln.partition("=")
        if a.strip():
            muc.append((a.strip(), b.strip()))
    tk = {}
    for a, b in sorted(muc, key=lambda x: -len(x[0])):   # mục dài trước, kẻo mục ngắn cắt đôi mục dài
        tk[a] = text.count(a)
        text = text.replace(a, b)
    return text, tk


def chunks(text, max_chars=1800):
    parts, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        if len(cur) + len(para) + 2 <= max_chars:
            cur += ("\n\n" if cur else "") + para
        else:
            if cur:
                parts.append(cur)
            if len(para) <= max_chars:
                cur = para
            else:
                cur = ""
                for sent in re.split(r"(?<=[。．.!?！？])", para):
                    if len(cur) + len(sent) <= max_chars:
                        cur += sent
                    else:
                        if cur:
                            parts.append(cur)
                        cur = sent
    if cur:
        parts.append(cur)
    return [p for p in parts if p.strip()]


async def synth_chunk(text, voice, rate, pitch, out_mp3):
    """Stream → ghi mp3 + trả list boundary [(start_s, end_s, text)] (offset gốc chunk).
    Nhật/Hàn phát SentenceBoundary (câu), Anh phát WordBoundary (từ) — bắt cả hai."""
    kw = {}
    if rate:
        kw["rate"] = rate
    if pitch:
        kw["pitch"] = pitch
    words = []
    with open(out_mp3, "wb") as f:
        async for ch in edge_tts.Communicate(text, voice, **kw).stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] in ("WordBoundary", "SentenceBoundary"):
                st = ch["offset"] / 1e7
                words.append((st, st + ch["duration"] / 1e7, ch["text"]))
    return words


def mp3_seconds(path):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def _split_long(start, end, text):
    """Tách 1 câu dài thành nhiều cue ≤ _MAX_CUE_CHARS, ngắt ở 、, chia thời gian theo số ký tự."""
    if len(text) <= _MAX_CUE_CHARS:
        return [(start, end, text)]
    segs, cur = [], ""
    for part in re.split(r"(?<=、)", text):
        if len(cur) + len(part) <= _MAX_CUE_CHARS:
            cur += part
        else:
            if cur:
                segs.append(cur)
            cur = part
    if cur:
        segs.append(cur)
    if len(segs) <= 1:
        return [(start, end, text)]
    out, total, t = [], sum(len(s) for s in segs), start
    for s in segs:
        dt = (end - start) * (len(s) / total)
        out.append((t, t + dt, s.strip("、 ")))
        t += dt
    return out


def build_cues(words):
    """Boundary → cue. Nhật/Hàn: mỗi event là 1 câu → tách nếu quá dài. Anh: gom từ theo dấu câu."""
    is_sentence = any(len(tok) > 6 or (tok and tok[-1] in _SENT_END) for _, _, tok in words[:5])
    cues = []
    if is_sentence:
        for st, en, tok in words:
            cues.extend(_split_long(st, en, tok.strip()))
        return cues
    buf, start, end = "", None, 0
    for st, en, tok in words:
        if start is None:
            start = st
        buf += tok
        end = en
        if tok and tok[-1] in _SENT_END or len(buf) >= _MAX_CUE_CHARS:
            cues.append((start, end, buf.strip("、 ")))
            buf, start = "", None
    if buf.strip():
        cues.append((start, end, buf.strip("、 ")))
    return cues


def _ts(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")


def write_srt(cues, path):
    lines = []
    for i, (st, en, txt) in enumerate(cues, 1):
        lines.append(f"{i}\n{_ts(st)} --> {_ts(en)}\n{txt}\n")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


# Giọng OpenSpeaker (ai33) — voice CHÍNH trả phí (chất ElevenLabs). Tên tắt → voice_id.
# ⚠️ CHỌN GIỌNG KHỚP GIỚI TÍNH NGƯỜI KỂ (ngôi 1): bà cụ kể → giọng NỮ; ông cụ kể → giọng NAM.
_OS_VOICES = {
    # NAM (người kể là ông cụ)
    "enishi": "elevenlabs_7arouBAZXrSnH9IwDlWQ",   # Deep Japanese Storyteller
    "papaji": "elevenlabs_rDiGqdvxRVKhplqZE31x",   # Deep, Wise
    "akira": "elevenlabs_JKne0OHHjFFwcwWzlGj0",    # Calm Deep
    "garyu": "elevenlabs_xeizJaHsHrlfQdJJQmlK",    # Calm mature male
    "senior": "minimax_209533299589242",           # Intellectual Senior (minimax)
    # NỮ (người kể là bà cụ) — CHÍNH cho câu chuyện giọng bà cụ
    "ado": "elevenlabs_jWxWvPtq4PJFwe66Y9xi",      # Mature & Soothing (bà cụ trầm ấm — MẶC ĐỊNH nữ)
    "naomi": "elevenlabs_JGDwW9z83vZudMiOzzS9",    # Natural & Calm
    "hikari": "elevenlabs_tTLw7unlQfMjcUKIUVzS",   # Japan narration
    "kindlady": "minimax_209536448462916",         # Kind Lady (minimax)
    "calmlady": "minimax_209536448462918",         # Calm Lady (minimax)
}


def resolve_voice(voice):
    """Tên tắt cũ (ado/enishi) → voice_id; nếu không có thì tra KHO GIỌNG theo tên; cuối cùng để nguyên."""
    v = str(voice or "").strip()
    if v.lower() in _OS_VOICES:
        return _OS_VOICES[v.lower()]
    try:
        import voice_bank
        return voice_bank.resolve(v)
    except Exception:
        return v


CREDIT_MOI_CHU = 62 / 49        # đo thật: 49 chữ Nhật = 62 credit (docs/CLAUDE.md § ai33)


def kiem_credit(osp, text):
    """CỔNG CREDIT — chặn TRƯỚC khi gửi bài đọc dài.

    Đo thật STT13 2026-09-19: tài khoản còn 4.597 credit trong khi bài cần ~10.707. Server KHÔNG
    báo lỗi mà **đọc tới đâu trả tới đó**: mp3 dài 16:05 trong khi phụ đề nó tự khai 29:32 (54% —
    khớp tỉ lệ credit còn lại). Hai lượt chạy lại đều cụt y hệt nên nhìn như 'server lỗi tất định',
    mất gần một giờ dò tìm. Từ nay hỏi số dư trước, thiếu là dừng ngay và nói rõ thiếu bao nhiêu."""
    try:
        con = int(osp.get_credits().get("credits", 0))
    except Exception as e:
        print(f"  ! không đọc được số dư credit ({type(e).__name__}) → chạy tiếp, nhớ kiểm audio bằng qc_audio")
        return
    n = len(text.replace("\n", "").replace(" ", ""))
    can = n * CREDIT_MOI_CHU
    print(f"  credit: còn {con:,} · bài này cần ~{can:,.0f} ({n:,} chữ)")
    if con < can:
        raise SystemExit(
            f"✗ HẾT CREDIT ai33: còn {con:,}, cần ~{can:,.0f} (thiếu ~{can-con:,.0f}).\n"
            f"  Nạp thêm tại ai33.pro rồi chạy lại. KHÔNG chạy tiếp — server sẽ trả audio CỤT "
            f"mà không báo lỗi (đo thật STT13: mp3 16:05 trong khi phụ đề khai 29:32).")


# -- CONG PHU CHU (2026-09-23): server DOC THIEU nguyen mot cau, im lang -----------------------
# Do that tren hook ep05-bermuda-triangle (208 chu): 4 luot TTS cung mot doan text -> 3 luot NUOT
# tron mot cau, moi luot nuot mot cau KHAC nhau (luot 1 va 3 mat cau cuoi, luot 2 mat cau ap cuoi,
# luot 4 du). Cong DO DAI o duoi KHONG bat duoc: no so mp3 voi SRT, ma ca hai deu do CUNG server
# sinh ra nen khop nhau trong cai sai - mp3 ngan dung bang phan bi nuot, SRT cung ngan y het.
# Cach bat duy nhat: so SRT voi KICH BAN GOC. Day la ly do cong nay ton tai.
PHU_CHU_TOI_THIEU = 0.95
_BO_DAU = re.compile(r"[\s、。,.!?！？「」『』・…ー]")


def _chu_trong_srt(srt):
    """Gom toan bo chu trong SRT, bo so thu tu / moc thoi gian / dau cau / khoang trang."""
    ra = []
    for khoi in re.split(r"\n\s*\n", (srt or "").strip()):
        dong = khoi.split("\n")
        ra.append("".join(dong[2:]) if len(dong) >= 3 else "")
    return _BO_DAU.sub("", "".join(ra))


def kiem_phu_chu(text, srt):
    """Tra (ti_le, so_chu_srt, so_chu_goc). Goi TRUOC khi ghi file de chan ban doc thieu cau."""
    goc = _BO_DAU.sub("", text or "")
    doc = _chu_trong_srt(srt)
    return (len(doc) / len(goc) if goc else 1.0), len(doc), len(goc)


def run_openspeaker(text, out, voice, speed, want_srt, age="none"):
    """Provider trả phí ai33/OpenSpeaker (chất ElevenLabs) — gửi CẢ kịch bản 1 lần, có SRT sẵn."""
    import openspeaker_tts as osp
    vid = resolve_voice(voice)
    print(f"[openspeaker] voice={vid} speed={speed} fx={normalize_fx(age)} · {len(text)} ký tự (gửi 1 lần)")
    kiem_credit(osp, text)
    audio, srt = osp.synthesize(text, voice_id=vid, speed=speed, with_transcript=want_srt,
                                file_name=out.stem)
    out.write_bytes(audio)
    apply_age(out, age)   # hậu kỳ làm già giọng (không đổi thời lượng → SRT vẫn khớp)
    chuan_muc(out)        # hạ trần đỉnh chống vỡ tiếng (B4Q bắt đỉnh -0,1 dB của bản thô)
    dur = mp3_seconds(out)
    print(f"✓ Voice: {out} (dài {int(dur//60)}:{int(dur%60):02d}) [ai33/{voice}]")
    # CỔNG ĐỘ DÀI (đo thật STT13 2026-09-19): server khai SRT 29:32 nhưng mp3 tải về chỉ 16:05 →
    # audio chết tiếng từ phút 18, phụ đề lệch 808s, chỉ qc_audio mới bắt được sau khi đã pace xong.
    # SRT của server là lời khai ĐỘ DÀI THẬT của bản đọc ⇒ so ngay, thiếu >5% là file hỏng.
    if srt:
        import re as _re
        moc = _re.findall(r"(\d\d):(\d\d):(\d\d),(\d+)\s*-->", srt)
        if moc:
            h, m, s, ms = moc[-1]
            can = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            if dur < can * 0.95:
                raise SystemExit(f"✗ TTS HỎNG: mp3 chỉ {dur/60:.1f}′ nhưng phụ đề server khai "
                                 f"{can/60:.1f}′ — file tải về bị ĐỨT. Chạy lại lệnh TTS này "
                                 f"(đừng pace/ghép bản hỏng).")
    if srt:
        ti_le, n_doc, n_goc = kiem_phu_chu(text, srt)
        if ti_le < PHU_CHU_TOI_THIEU:
            raise SystemExit(
                f"\u2717 TTS \u0110\u1eccC THI\u1ebeU: ph\u1ee5 \u0111\u1ec1 server ch\u1ec9 c\u00f3 {n_doc}/{n_goc} ch\u1eef c\u1ee7a k\u1ecbch b\u1ea3n "
                f"({ti_le*100:.1f}%, c\u1ea7n \u2265{PHU_CHU_TOI_THIEU*100:.0f}%) \u2014 server NU\u1ed0T M\u1ea4T m\u1ed9t \u0111o\u1ea1n. "
                f"\u0110\u00e2y l\u00e0 l\u1ed7i ng\u1eabu nhi\u00ean c\u1ee7a ai33 (\u0111o th\u1eadt: 3/4 l\u01b0\u1ee3t), CH\u1ea0Y L\u1ea0I \u0110\u00daNG L\u1ec6NH N\u00c0Y l\u00e0 th\u01b0\u1eddng h\u1ebft. "
                f"TUY\u1ec6T \u0110\u1ed0I \u0111\u1eebng \u0111em b\u1ea3n n\u00e0y \u0111i gh\u00e9p: n\u00f3 thi\u1ebfu nguy\u00ean m\u1ed9t c\u00e2u m\u00e0 nghe kh\u00f4ng ra.")
        print(f"  \u2713 ph\u1ee7 ch\u1eef {ti_le*100:.1f}% ({n_doc}/{n_goc}) \u2014 kh\u00f4ng nu\u1ed1t c\u00e2u n\u00e0o")
    if want_srt and srt:
        srt_path = out.with_suffix(".srt")
        srt_path.write_text(srt, encoding="utf-8")
        print(f"✓ Phụ đề (server sync): {srt_path}")
        print(f"→ Ghép + burn: py -3.13 assemble.py --img <img_dir> --audio {out} --srt {srt_path} --out draft.mp4")
    else:
        print(f"→ Ghép: py -3.13 assemble.py --img <img_dir> --audio {out} --out draft.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True, help="file mp3 (srt cùng tên .srt)")
    ap.add_argument("--provider", default="openspeaker", choices=["openspeaker", "edge"],
                    help="openspeaker=ai33 trả phí (chất ElevenLabs, CHÍNH) · edge=free fallback")
    ap.add_argument("--voice", default="", help="openspeaker: enishi/papaji/akira/senior hoặc voice_id; "
                                                "edge: ja-JP-KeitaNeural...")
    # default=None chứ KHÔNG phải giá trị thật: cần phân biệt "người dùng KHÔNG truyền" với
    # "người dùng truyền đúng giá trị đó". Xem resolve_voice_conf().
    ap.add_argument("--speed", type=float, default=None, help="openspeaker: 0.5-1.5 (chậm cho khán giả già)")
    ap.add_argument("--fx", default="", help="FX giọng: none/old-mild/old-med/old-frail/young/boom/punch "
                                             "(xem: py -3.13 voice_bank.py --list-fx)")
    ap.add_argument("--age", default="", help="[tên cũ của --fx] none/mild/med/frail")
    ap.add_argument("--rate", default="-8%", help='edge: vd --rate=-8% (dạng có dấu =)')
    ap.add_argument("--pitch", default="")
    ap.add_argument("--no-srt", action="store_true", help="không xuất phụ đề")
    ap.add_argument("--yomi", default="", help="file 表示=読み; mặc định yomi.txt cạnh --script nếu có")
    ap.add_argument("--profile", default="", help="id profile trong pipeline/profiles/<id>.json (nhân vật+giọng+fx)")
    ap.add_argument("--channel", default="", help="[cũ] id kênh trong channels.json")
    args = ap.parse_args()

    prof_id = args.profile or args.channel
    # Lane ĐA GIỌNG (profiles.da_giong: voice.provider "voicevox"/"ai33"): mọi nơi gọi tts.py --profile (hook, dung_hook, calibrate…) tự
    # chuyển sang tts_voicevox.py — giọng từng câu lấy từ vai.txt của tập (dò lên từ thư mục script).
    if prof_id:
        try:
            import profiles as _pf
            _p = _pf.load(prof_id)
        except Exception:
            _p = {}
        if _p and _pf.da_giong(_p):          # voicevox (Lane K) | ai33 đa giọng (Lane L)
            import tts_voicevox
            tts_voicevox.chay(args.script, args.out, _p)
            return
    resolve_voice_conf(args, prof_id)

    text = clean(Path(args.script).read_text(encoding="utf-8"))
    yomi = Path(args.yomi) if args.yomi else Path(args.script).parent / "yomi.txt"
    if yomi.exists():
        text, tk = ap_yomi(text, yomi)
        khong = [a for a, n in tk.items() if n == 0]
        print(f"[yomi] {len(tk)} mục · thay {sum(tk.values())} lần" +
              (f" · ⚠️ 0 lần (không có trong script): {', '.join(khong)}" if khong else ""))
    if not text:
        raise SystemExit("Script rỗng.")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.provider == "openspeaker":
        try:
            run_openspeaker(text, out, args.voice or "enishi", args.speed, not args.no_srt, args.age)
            return
        except Exception as e:
            print(f"⚠️ openspeaker lỗi ({e}) → fallback edge-tts free")
    # ---- edge-tts (free fallback) ----
    if not args.voice or args.voice.startswith("elevenlabs") or args.voice in _OS_VOICES:
        args.voice = "ja-JP-KeitaNeural"
    parts = chunks(text)
    print(f"Script {len(text)} ký tự → {len(parts)} chunk · voice={args.voice} rate={args.rate}")

    tmp = Path(tempfile.mkdtemp(prefix="tts_"))
    mp3s, all_words, offset = [], [], 0.0
    for i, part in enumerate(parts):
        f = tmp / f"{i:03d}.mp3"
        words = asyncio.run(synth_chunk(part, args.voice, args.rate, args.pitch, f))
        for st, en, tok in words:
            all_words.append((st + offset, en + offset, tok))
        offset += mp3_seconds(f)            # cộng dồn theo độ dài thực chunk
        mp3s.append(f)
        print(f"  ✓ chunk {i+1}/{len(parts)} ({len(part)} ký tự, {len(words)} từ)")

    # ghép mp3
    if len(mp3s) == 1:
        out.write_bytes(mp3s[0].read_bytes())
    else:
        lst = tmp / "list.txt"
        lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in mp3s), encoding="utf-8")
        subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(out)], check=True, capture_output=True)

    apply_age(out, args.age)   # làm già giọng (không đổi thời lượng)
    chuan_muc(out)             # hạ trần đỉnh chống vỡ tiếng
    dur = mp3_seconds(out)
    print(f"✓ Voice: {out} (dài {int(dur//60)}:{int(dur%60):02d})")

    if not args.no_srt and all_words:
        cues = build_cues(all_words)
        srt = out.with_suffix(".srt")
        write_srt(cues, srt)
        print(f"✓ Phụ đề: {srt} ({len(cues)} cue)")
        print(f"→ Ghép + burn phụ đề: py -3.13 assemble.py --img <img_dir> --audio {out} --srt {srt} --out draft.mp4")
    else:
        print(f"→ Ghép: py -3.13 assemble.py --img <img_dir> --audio {out} --out draft.mp4")


if __name__ == "__main__":
    main()
