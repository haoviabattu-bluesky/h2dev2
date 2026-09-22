"""qc_visual.py — QC HÌNH ẢNH + VIDEO. Chặn lỗi ở TỪNG bước, không để dồn tới cuối.

User chốt 2026-09-08: "phải có QC sau mỗi bước … sản phẩm đầu ra phải hoàn hảo".
Chuỗi QC của tool:
  B3Q  kịch bản        → qc_script.py (logic, 伏線, lặp ý, bám gốc 70/30)
  B4Q  giọng + SRT     → qc_voice()      : SRT có phủ hết kịch bản không, thời lượng khớp không
  B5RQ ảnh master      → qc_master()     : tuổi/giới/trang phục/thời đại/phong cách có đúng thiết kế
  B5Q  loạt ảnh        → qc_images()     : hỏng/đen/trùng + vision soi mẫu (khớp prompt, đúng thời đại)
  B8Q  video hoàn chỉnh→ qc_video()      : luồng/thời lượng/khung đen + ẢNH CÓ KHỚP LỜI ĐANG ĐỌC không

⚠️ Nguyên tắc chung (bẫy 503 đã dính ở dự án thẻ): lỗi HẠ TẦNG (mạng/model) ném `QcError`, KHÔNG
được nuốt thành "không có lỗi". Mọi hàm trả về `infra` riêng; QC không chạy được thì KHÔNG PASS.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import qc_character as qcc

FF = None


def _ff():
    global FF
    if FF is None:
        import imageio_ffmpeg
        FF = imageio_ffmpeg.get_ffmpeg_exe()
    return FF


class QcError(RuntimeError):
    """Hạ tầng hỏng — KHÔNG phải lỗi nội dung."""


def _vision(prompt, img_path, model="gemini-3.8-flash"):
    try:
        b64 = base64.b64encode(Path(img_path).read_bytes()).decode()
        return qcc._parse_json(qcc._chat(model, prompt, b64))
    except Exception as e:
        raise QcError(f"{type(e).__name__}: {str(e)[:120]}") from None


# ============================================================ B4Q — giọng/SRT
def _norm(t):
    return re.sub(r"[\s、。「」．,.!?！？…・ー－-]", "", t)


def qc_voice(script_path, srt_path, audio_sec, target_minutes=None):
    """SRT do server sinh từ CHÍNH file audio → so với kịch bản là cách duy nhất phát hiện
    TTS đọc thiếu/đọc sai/cắt giữa chừng (lỗi câm lặng: file mp3 vẫn có, vẫn nghe xuôi)."""
    import storyboard as sb
    out = {"problems": [], "infra": []}
    script = Path(script_path).read_text(encoding="utf-8")
    cues = sb.parse_cues(srt_path)
    if not cues:
        out["problems"].append("SRT rỗng / không đọc được")
        return out
    srt_text = _norm("".join(c[2] for c in cues))
    src = _norm(script)
    cover = len(srt_text) / max(len(src), 1)
    out["coverage"] = round(cover, 3)
    out["cues"] = len(cues)
    out["audio_sec"] = round(audio_sec, 1)
    # SRT do STT nên không bao giờ khớp 100%; dưới 85% là đọc THIẾU thật sự.
    if cover < 0.85:
        out["problems"].append(f"SRT chỉ phủ {cover:.0%} kịch bản → giọng có thể đọc THIẾU/bị cắt")
    if cover > 1.25:
        out["problems"].append(f"SRT dài hơn kịch bản {cover:.0%} → nghi lặp đoạn")
    # Phụ đề có ĐÚNG CHỮ của kịch bản không. `coverage` chỉ so ĐỘ DÀI nên mù hoàn toàn với
    # chuyện chữ sai: SRT do server STT nghe lại audio, sai đồng âm đầy ra mà độ dài vẫn khớp.
    # Đo thật tập simbot2-vU5PWT2zLDs: coverage 95% trong khi có 70 chỗ sai chữ + 517 dấu phẩy
    # mất (終の棲家 → 衆の成果). Bước B4a `srt_from_script.py` nắn lại; chốt này canh xem nó có
    # thật sự chạy không.
    import difflib
    giong = difflib.SequenceMatcher(None, srt_text, src, autojunk=False).quick_ratio()
    out["srt_khop_script"] = round(giong, 3)
    if giong < 0.99:
        out["problems"].append(
            f"phụ đề chỉ khớp {giong:.1%} chữ của kịch bản (cần ≥99%) → bước B4a "
            f"'srt_from_script.py' chưa chạy hoặc hỏng; phụ đề cháy vào video sẽ SAI CHỮ")
    last = cues[-1][1]
    if audio_sec and last < audio_sec * 0.9:
        out["problems"].append(f"cue cuối ở {last:.0f}s nhưng audio dài {audio_sec:.0f}s → thiếu đuôi")
    starts = [c[0] for c in cues]
    if any(b < a for a, b in zip(starts, starts[1:])):
        out["problems"].append("timestamp SRT không tăng dần")
    if target_minutes:
        d = abs(audio_sec / 60 - target_minutes) / target_minutes
        if d > 0.15:
            out["problems"].append(f"thời lượng {audio_sec/60:.1f}' lệch {d:.0%} so mục tiêu {target_minutes}'")
    return out


# ====================================================== B5RQ — ảnh master
MASTER_SCHEMA = ('{"apparent_age":<int>,"gender":"M"|"F","era_ok":<bool>,"costume_ok":<bool>,'
                 '"style_ok":<bool>,"matches_description":<bool>,"face_clear":<bool>,"issues":["..."]}')


def qc_master(img_path, spec, world="", models=("gemini-3.8-flash",)):
    """Soi ảnh master TRƯỚC khi gen cả loạt: tuổi · giới · TRANG PHỤC · THỜI ĐẠI · PHONG CÁCH.

    Master sai thì 80-90 ảnh khoá mặt theo nó đều sai — sửa ở đây rẻ hơn 100 lần."""
    look = spec.get("look") or spec.get("character_sheet") or ""
    prompt = (
        "You are a strict visual QC for character casting in a narrated story video. "
        "Look at the MAIN person and judge honestly.\n"
        f"DESIGN: age {spec.get('age','?')}, gender {spec.get('gender','?')}, "
        f"description: {look[:400]}\n"
        f"WORLD (era, region, clothing, technology): {world[:400] or 'contemporary, unspecified'}\n"
        "era_ok = clothing/hair/props match that era. costume_ok = clothing matches the description. "
        "style_ok = photoreal cinematic portrait, no illustration/anime/3D-render look. "
        "face_clear = face fully visible, front-facing, evenly lit, usable as a face reference.\n"
        f"Reply ONLY compact JSON: {MASTER_SCHEMA}")
    res, infra = [], []
    for m in models:
        try:
            res.append(_vision(prompt, img_path, m))
        except QcError as e:
            infra.append(f"{m}: {e}")
    if not res:
        return {"problems": [], "infra": infra, "raw": []}
    d = res[0]
    probs = []
    want = spec.get("age")
    got = d.get("apparent_age")
    if want and isinstance(got, int) and abs(got - int(want)) > qcc.AGE_TOL:
        probs.append(f"tuổi nhìn ~{got} nhưng thiết kế {want} (lệch {abs(got-int(want))} > {qcc.AGE_TOL})")
    g = (d.get("gender") or "").upper()[:1]
    if spec.get("gender") and g and g != str(spec["gender"]).upper()[:1]:
        probs.append(f"giới nhìn {g} nhưng thiết kế {spec['gender']}")
    for k, msg in (("era_ok", "TRANG PHỤC/BỐI CẢNH sai thời đại"),
                   ("costume_ok", "trang phục không khớp mô tả nhân vật"),
                   ("style_ok", "phong cách ảnh sai (không phải ảnh thật điện ảnh)"),
                   ("matches_description", "không khớp mô tả nhân vật"),
                   ("face_clear", "mặt không rõ/không chính diện → làm ảnh khoá mặt sẽ kém")):
        if d.get(k) is False:
            probs.append(msg)
    probs += [f"vision: {x}" for x in (d.get("issues") or [])[:3] if x]
    return {"problems": probs, "infra": infra, "raw": d,
            "apparent_age": got, "gender": g}


# ========================================================= B5Q — loạt ảnh
def _dhash(path, size=8):
    from PIL import Image
    im = Image.open(path).convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(im.getdata())
    bits = 0
    for r in range(size):
        row = px[r * (size + 1):(r + 1) * (size + 1)]
        for c in range(size):
            bits = (bits << 1) | (row[c] < row[c + 1])
    return bits


def mech_images(imgdir, n_expected=0, min_kb=120):
    """Lỗi máy đọc chắc chắn: thiếu ảnh · file hỏng · quá nhỏ · gần như đen · TRÙNG ảnh."""
    from PIL import Image, ImageStat
    imgs = sorted(Path(imgdir).glob("*.png"))
    out = {"problems": [], "n": len(imgs), "flagged": []}
    if n_expected and len(imgs) != n_expected:
        out["problems"].append(f"có {len(imgs)} ảnh, cần {n_expected} → thiếu {n_expected-len(imgs)}")
    hashes = {}
    for f in imgs:
        try:
            if f.stat().st_size < min_kb * 1024:
                out["flagged"].append((f.name, f"file quá nhỏ {f.stat().st_size//1024}KB"))
            im = Image.open(f)
            im.verify()
            im = Image.open(f).convert("L")
            st = ImageStat.Stat(im)
            if st.mean[0] < 18:
                out["flagged"].append((f.name, f"gần như ĐEN (mean {st.mean[0]:.0f})"))
            elif st.stddev[0] < 8:
                out["flagged"].append((f.name, f"gần như phẳng/trống (stddev {st.stddev[0]:.0f})"))
            hashes[f.name] = _dhash(f)
        except Exception as e:
            out["flagged"].append((f.name, f"ảnh HỎNG: {type(e).__name__}"))
    names = list(hashes)
    dup = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if bin(hashes[a] ^ hashes[b]).count("1") <= 4:
                dup.append((a, b))
    if dup:
        out["problems"].append(f"{len(dup)} cặp ảnh gần TRÙNG nhau: " +
                               ", ".join(f"{a}≈{b}" for a, b in dup[:4]))
    out["dup"] = dup
    if out["flagged"]:
        out["problems"].append(f"{len(out['flagged'])} ảnh có vấn đề: " +
                               "; ".join(f"{n} ({w})" for n, w in out["flagged"][:5]))
    return out


IMG_SCHEMA = ('{"matches_prompt":<bool>,"era_ok":<bool>,"people_count":<int>,'
              '"readable_text":<bool>,"artifacts":<bool>,"single_scene":<bool>,"note":"<= 15 words"}')


def qc_images(imgdir, prompts, world="", sample=12, workers=4):
    """Máy đo TOÀN BỘ + vision soi MẪU (đủ để bắt lỗi hệ thống mà không tốn 126 lượt gọi)."""
    imgs = sorted(Path(imgdir).glob("*.png"))
    res = mech_images(imgdir, len(prompts) if prompts else 0)
    res["infra"] = []
    if not imgs:
        return res
    idx = sorted({round(i * (len(imgs) - 1) / max(sample - 1, 1)) for i in range(sample)})
    tasks = [(i, imgs[i], prompts[i] if prompts and i < len(prompts) else "") for i in idx]

    def one(t):
        i, f, pr = t
        pr_sach = re.sub(r"^@\w+ ", "", pr)[:400]
        ask = ("You are a strict QC for AI-generated story images. Judge this image.\n"
               f"It was generated from this prompt: {pr_sach}\n"
               f"WORLD it must fit: {world[:300] or 'unspecified'}\n"
               "matches_prompt = the image really shows what the prompt asks. "
               "era_ok = nothing anachronistic vs the world. readable_text = any legible words/signs "
               "visible. artifacts = deformed hands/faces/objects. "
               "single_scene = this is ONE continuous illustrated scene (false if it looks like a "
               "comic/manga PAGE with multiple panels, a grid of smaller images, a character "
               "reference sheet with several poses, or any visible panel borders/gutters).\n"
               f"Reply ONLY compact JSON: {IMG_SCHEMA}")
        try:
            return i, f.name, _vision(ask, f)
        except QcError as e:
            return i, f.name, {"_err": str(e)}

    bad = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, name, d in ex.map(one, tasks):
            if "_err" in d:
                res["infra"].append(f"{name}: {d['_err']}")
                continue
            why = []
            if d.get("matches_prompt") is False:
                why.append("không khớp prompt")
            if d.get("era_ok") is False:
                why.append("LẠC THỜI ĐẠI")
            if d.get("artifacts") is True:
                why.append("méo mó/dị dạng")
            if d.get("readable_text") is True:
                why.append("có chữ đọc được")
            if d.get("single_scene") is False:
                why.append("NHIỀU Ô/collage (không phải 1 cảnh liền)")
            if why:
                bad.append((name, ", ".join(why), (d.get("note") or "")[:60]))
    res["vision_checked"] = len(tasks)
    res["vision_bad"] = bad
    if bad:
        res["problems"].append(f"{len(bad)}/{len(tasks)} ảnh mẫu có vấn đề: " +
                               "; ".join(f"{n}({w})" for n, w, _ in bad[:5]))
    return res


# ========================================================= B7Q — thumbnail
THUMB_SCHEMA = ('{"face_visible":<bool>,"face_covered_by_text":<bool>,"text_readable":<bool>,'
                '"contrast_ok":<bool>,"emotional":<bool>,"issues":["..."]}')


def qc_thumb(img_path, lines="", doi_mat=True):
    """Thumbnail là thứ quyết định người ta có bấm vào không — chữ phải đọc được trên màn hình nhỏ.
    Bẫy hay gặp: chữ to đè đúng lên mặt → mất cả hai (đo thật ep08).

    `doi_mat=False`: kênh KHÔNG lấy mặt người làm nền. Đòi "phải có mặt cảm xúc" là luật của kênh
    kể chuyện đời người; ngách 都市伝説/vũ trụ thì NGƯỢC LẠI — đo thật 11/12 thumbnail top của ngách
    KHÔNG có mặt người thật, nền là cảnh vũ trụ tối. Bật cờ này lên là đánh trượt đúng thứ đang làm
    đúng công thức.
    """
    ask = ("You are a strict QC for a YouTube thumbnail"
           + (" (story channel for older viewers). " if doi_mat else
              " (documentary channel about space and unexplained mysteries; the background is a "
              "cinematic scene and a human face is NOT required). ") +
           "Judge honestly, as it will look on a small phone screen.\n"
           f"The overlaid text is: {lines[:200]}\n"
           "face_visible = a human face with readable emotion is clearly visible. "
           "face_covered_by_text = the overlaid text covers the face (eyes/mouth) so the emotion is lost. "
           "text_readable = the text is high-contrast and easy to read at small size. "
           "contrast_ok = the background is dark/blurred enough for the text to pop. "
           "emotional = the image conveys a feeling, not an empty scene.\n"
           f"Reply ONLY compact JSON: {THUMB_SCHEMA}")
    try:
        d = _vision(ask, img_path)
    except QcError as e:
        return {"problems": [], "infra": [str(e)]}
    p = []
    if d.get("face_visible") is False and doi_mat:
        p.append("KHÔNG thấy mặt người → nền chọn sai (phải là ảnh có mặt cảm xúc)")
    if d.get("face_covered_by_text") is True and doi_mat:
        p.append("chữ ĐÈ LÊN MẶT → mất cả mặt lẫn chữ, phải đổi nền hoặc dịch chữ")
    if d.get("text_readable") is False:
        p.append("chữ khó đọc ở cỡ nhỏ")
    if d.get("contrast_ok") is False:
        p.append("nền chưa đủ tối/mờ để chữ nổi")
    if d.get("emotional") is False:
        p.append("ảnh nền vô cảm, không gợi tò mò")
    bo_qua = ("face", "facial", "expression", "silhouett", "from behind")
    issues = [x for x in (d.get("issues") or []) if x
              and not (not doi_mat and any(k in str(x).lower() for k in bo_qua))]
    p += [f"vision: {x}" for x in issues[:2]]
    return {"problems": p, "infra": [], "raw": d}


# ========================================================= B8Q — video cuối
def probe(mp4):
    r = subprocess.run([_ff(), "-i", str(mp4)], capture_output=True, text=True, errors="replace")
    txt = r.stderr
    d = {}
    m = re.search(r"Duration: (\d\d):(\d\d):(\d\d)\.(\d\d)", txt)
    if m:
        d["duration"] = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 100
    m = re.search(r"Video: (\w+).*?, (\d+)x(\d+)", txt)
    if m:
        d["vcodec"], d["w"], d["h"] = m[1], int(m[2]), int(m[3])
    m = re.search(r"Audio: (\w+).*?(\d+) Hz", txt)
    if m:
        d["acodec"], d["hz"] = m[1], int(m[2])
    return d


def _frame(mp4, t, out):
    subprocess.run([_ff(), "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", str(out)],
                   capture_output=True)
    return out.exists() and out.stat().st_size > 2000


# Ngưỡng tiếng BẢN GHÉP (khác qc_audio đo trên voice.mp3 TRƯỚC khi trộn BGM — xem plans/260921-1415).
VO_GHEP_DB = -0.5      # đỉnh chạm mức này sau amix = vỡ tiếng do BGM cộng dồn
NHO_GHEP_DB = -30.0
MAT_TIENG_S = 8.0      # im lâu hơn mức này GIỮA video = rụng tiếng (nghỉ cố ý sau pace ≤ ~3 s)
BGM_LAN_DB = 3.0       # bản ghép to hơn giọng gốc quá mức này = BGM lấn


def kiem_tieng_ghep(mp4, voice=None):
    """Đo TIẾNG của final.mp4 SAU khi trộn BGM. Mọi phép đo âm khác của dự án (qc_audio) chạy ở
    B4Q trên voice.mp3, tức là trước amix (assemble.py:470) — vỡ tiếng/BGM lấn/mất tiếng sinh ra ở
    chính bước trộn thì không cổng nào bắt. Tất định, 0 đồng; lỗi ffmpeg → infra, không PASS ảo."""
    import numpy as np
    import qc_audio
    out = {"problems": [], "infra": []}
    try:
        mx, mean = qc_audio.do_muc(mp4)
        a, sr = qc_audio.doc_song(mp4)
    except Exception as e:
        out["infra"].append(f"không đo được tiếng bản ghép: {type(e).__name__} {e}")
        return out
    out["max_db"], out["mean_db"] = mx, mean
    if mx is None or mean is None:
        out["infra"].append("volumedetect không trả số")
        return out
    if mx >= VO_GHEP_DB:
        out["problems"].append(f"VỠ TIẾNG bản ghép: đỉnh {mx:+.1f} dB (BGM cộng dồn lên giọng)")
    if mean < NHO_GHEP_DB:
        out["problems"].append(f"tiếng bản ghép quá nhỏ: trung bình {mean:.1f} dB")
    # Mất tiếng: có BGM nền thì im KHÔNG BAO GIỜ xuống -45 dB, nên ngưỡng phải tương đối — lấy
    # mức "đang nói" (p90 đường bao) trừ 25 dB, không thấp hơn ngưỡng tuyệt đối của qc_audio.
    dur = len(a) / sr
    win = max(1, int(sr * 0.02))
    env = np.abs(a[: len(a) // win * win]).reshape(-1, win).max(axis=1)
    p90 = 20 * np.log10(max(float(np.percentile(env, 90)), 1e-6))
    th = max(qc_audio.LANG_DB, p90 - 25)
    out["nguong_lang_db"] = round(th, 1)
    lang = [(t, d) for t, d in qc_audio.khoang_lang(a, sr, nguong_db=th)
            if d >= MAT_TIENG_S and t > 5 and t + d < dur - 5]
    out["lang_dai"] = [(round(t, 1), round(d, 1)) for t, d in lang]
    for t, d in lang[:5]:
        out["problems"].append(f"MẤT TIẾNG {d:.0f}s: {t:.0f}s→{t + d:.0f}s (im dưới {th:.0f} dB)")
    if voice and Path(voice).exists():
        try:
            _, mv = qc_audio.do_muc(voice)
        except Exception as e:
            out["infra"].append(f"không đo được voice gốc: {e}")
            mv = None
        if mv is not None:
            out["voice_mean_db"] = mv
            if mean - mv > BGM_LAN_DB:
                out["problems"].append(f"BGM LẤN GIỌNG: bản ghép {mean:.1f} dB vs giọng gốc "
                                       f"{mv:.1f} dB (+{mean - mv:.1f} dB)")
    return out


SYNC_SCHEMA = ('{"matches":<bool>,"score":<1-5>,"subtitle_visible":<bool>,"why":"<= 15 words"}')


def qc_video(mp4, srt=None, audio_sec=0, samples=8, workers=4, want_sub=True, voice=None):
    """QC bản GHÉP: luồng/thời lượng/khung đen + **ẢNH CÓ KHỚP LỜI ĐANG ĐỌC KHÔNG**.

    Đây là câu hỏi cuối cùng người xem đặt ra. Cách kiểm: lấy k mốc thời gian, trích khung hình,
    lấy lời SRT đúng mốc đó, hỏi vision xem hình có ăn với lời không."""
    import storyboard as sb
    from PIL import Image, ImageStat
    out = {"problems": [], "infra": [], "samples": []}
    info = probe(mp4)
    out["info"] = info
    if not info.get("duration"):
        out["problems"].append("không đọc được video")
        return out
    if not info.get("acodec"):
        out["problems"].append("KHÔNG có luồng âm thanh")
    if audio_sec and abs(info["duration"] - audio_sec) > 3:
        out["problems"].append(f"video {info['duration']:.0f}s vs giọng {audio_sec:.0f}s → lệch "
                               f"{info['duration']-audio_sec:+.0f}s")
    t = kiem_tieng_ghep(mp4, voice)
    out["tieng"] = {k: v for k, v in t.items() if k not in ("problems", "infra")}
    out["problems"] += t["problems"]
    out["infra"] += t["infra"]
    cues = sb.parse_cues(srt) if srt and Path(srt).exists() else []
    dur = info["duration"]
    times = [dur * (i + 0.5) / samples for i in range(samples)]
    # HÚT mẫu vào GIỮA cue gần nhất. Sau khi giãn nhịp, ~16% thời lượng là khoảng lặng KHÔNG có
    # phụ đề; lấy mốc cách đều thì rơi vào đó là chuyện thường → bộ chấm báo "thiếu phụ đề" oan
    # (đo thật ep14: 6/12 mốc, cả 6 đều nằm trong khoảng lặng, video hoàn toàn đúng).
    if cues:
        mids = [(a + b) / 2 for a, b, _ in cues]
        times = sorted({min(mids, key=lambda m: abs(m - t)) for t in times})
    tmp = Path(tempfile.mkdtemp(prefix="qcv_"))

    def one(k):
        t = times[k]
        f = tmp / f"f{k:02d}.png"
        if not _frame(mp4, t, f):
            return {"t": t, "err": "không trích được khung hình"}
        st = ImageStat.Stat(Image.open(f).convert("L"))
        if st.mean[0] < 10:
            return {"t": t, "err": "KHUNG ĐEN"}
        line = " ".join(c[2] for c in cues if c[0] <= t <= c[1]) or \
               (" ".join(c[2] for c in cues if abs(c[0] - t) < 6))
        if not line:
            return {"t": t, "ok": True, "note": "không có lời ở mốc này"}
        # Bộ chấm cũ quá chữ nghĩa: nó trừ điểm cả khi hình quay NGƯỜI KỂ trong lúc bà nói về con
        # cái, hay khi lời là câu nhắn gửi khán giả mà hình là cảnh làng. Soi tay 4 mốc bị chấm 2/5
        # thì chỉ 1 mốc lệch thật (ep09) → phải nói rõ thế nào là chấp nhận được.
        ask = ("A narrated story video. This frame is on screen while the narrator says the line "
               "below. Judge whether the picture BELONGS TO THIS MOMENT of the story.\n"
               "Be fair, not literal:\n"
               "- The narrator is telling her own story. A shot of HER while she speaks — even when "
               "the sentence mentions other people — is acceptable.\n"
               "- A line addressed to the audience (advice, a question, a moral) may be illustrated "
               "by an atmospheric shot of the setting.\n"
               "- If the line describes several things, illustrating ONE of them is fine.\n"
               "- Mark it wrong only when the picture belongs to a clearly different moment, place "
               "or set of people than the line describes.\n"
               f"NARRATION: {line[:300]}\n"
               "subtitle_visible = burned-in subtitle text is visible in the frame.\n"
               f"Reply ONLY compact JSON: {SYNC_SCHEMA}")
        try:
            d = _vision(ask, f)
        except QcError as e:
            return {"t": t, "infra": str(e)}
        return {"t": t, "score": d.get("score"), "matches": d.get("matches"),
                "sub": d.get("subtitle_visible"), "why": (d.get("why") or "")[:60], "line": line[:60]}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        out["samples"] = list(ex.map(one, range(samples)))
    for s in out["samples"]:
        if s.get("infra"):
            out["infra"].append(f"{s['t']:.0f}s: {s['infra']}")
        elif s.get("err"):
            out["problems"].append(f"{s['t']:.0f}s: {s['err']}")
    scored = [s for s in out["samples"] if isinstance(s.get("score"), int)]
    if scored:
        avg = sum(s["score"] for s in scored) / len(scored)
        out["sync_score"] = round(avg, 2)
        weak = [s for s in scored if s["score"] <= 2]
        out["weak"] = [{"t": s["t"], "score": s["score"], "why": s["why"], "line": s["line"]}
                       for s in weak]
        # Vài mốc lệch lẻ tẻ là bình thường (model chấm khắt khe: lời nhắc 2 vật, ảnh vẽ 1 vật →
        # bị chấm 2/5 dù đúng). Chỉ coi là HỎNG khi trung bình thấp hoặc lệch thành hệ thống.
        if avg < 3.2 or len(weak) >= max(2, round(len(scored) * 0.3)):
            out["problems"].append(f"ẢNH LỆCH LỜI: trung bình {avg:.1f}/5, "
                                   f"{len(weak)}/{len(scored)} mốc ≤2")
            for s in weak:
                out["problems"].append(f"  {s['t']:.0f}s ({s['score']}/5): {s['why']} | lời: {s['line']}")
        else:
            for s in weak:
                print(f"   · (cảnh báo) {s['t']:.0f}s {s['score']}/5: {s['why']}")
        if want_sub:
            nosub = [s for s in scored if s.get("sub") is False]
            if len(nosub) > len(scored) * 0.4:
                out["problems"].append(f"{len(nosub)}/{len(scored)} khung KHÔNG thấy phụ đề")
    return out


def report(title, res):
    n = len(res.get("problems", []))
    print(f"\n=== {title}: {'ĐẠT' if not n else str(n) + ' VẤN ĐỀ'}")
    if res.get("infra"):
        print(f"  ⚠️ {len(res['infra'])} lượt QC KHÔNG chạy được (hạ tầng) — 'sạch' lúc này là số ảo:")
        for e in res["infra"][:4]:
            print("     !", str(e)[:140])
    for p in res.get("problems", []):
        print("   ✗", str(p)[:190])
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["voice", "master", "images", "video", "thumb"])
    ap.add_argument("--dir", default="")
    ap.add_argument("--img", default="")
    ap.add_argument("--script", default="")
    ap.add_argument("--srt", default="")
    ap.add_argument("--mp4", default="")
    ap.add_argument("--prompts", default="")
    ap.add_argument("--age", type=int, default=0)
    ap.add_argument("--gender", default="")
    ap.add_argument("--look", default="")
    ap.add_argument("--world", default="")
    ap.add_argument("--audio-sec", type=float, default=0)
    ap.add_argument("--voice", default="", help="voice.mp3 gốc để so BGM lấn (chỉ what=video)")
    ap.add_argument("--sample", type=int, default=12)
    # Video KHÔNG cháy phụ đề (mặc định của dự án từ 2026-09-11: up .srt lên YouTube làm CC thay vì
    # đốt chữ vào hình). Không có cờ này thì tiêu chí "khung có thấy phụ đề không" báo lỗi OAN cho
    # mọi video sạch chữ — hàm qc_video đã có sẵn want_sub nhưng trước đây CLI không mở ra được.
    ap.add_argument("--no-sub", action="store_true",
                    help="video cố ý KHÔNG cháy phụ đề → bỏ tiêu chí 'khung phải thấy chữ'")
    a = ap.parse_args()
    if a.what == "voice":
        r = qc_voice(a.script, a.srt, a.audio_sec)
    elif a.what == "master":
        r = qc_master(a.img, {"age": a.age, "gender": a.gender, "look": a.look}, a.world)
    elif a.what == "thumb":
        r = qc_thumb(a.img, a.look)
    elif a.what == "images":
        pr = [l for l in Path(a.prompts).read_text(encoding="utf-8").splitlines() if l.strip()] \
            if a.prompts else []
        r = qc_images(a.dir, pr, a.world, a.sample)
    else:
        r = qc_video(a.mp4, a.srt or None, a.audio_sec, a.sample, want_sub=not a.no_sub,
                     voice=a.voice or None)
    report(a.what.upper(), r)
    print(json.dumps({k: v for k, v in r.items() if k != "samples"}, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
