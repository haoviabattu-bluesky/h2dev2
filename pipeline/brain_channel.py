"""brain_channel.py — ORCHESTRATOR tool "NÃO = Claude": từ 1 KÊNH đối thủ → nhiều video hoàn chỉnh.

Đây là lõi của tool exe (chạy máy có Claude). Khác render_engine.py (chỉ render 1 slug đã soạn) và khác
make_video.py của tab a3 (não = ramcloud). Luồng mỗi video:
  B2  cào transcript (fetch_script.py)                        — tool
  🎙  phát hiện giọng theo video (detect_voice → voice.json)  — Gemini/LLM chọn giọng khớp người kể
  🧠  Claude viết kịch bản + prompt + master + tự QC/sửa      — brain_steps (claude -p)
  🎬  render: giọng ElevenLabs · ảnh gpt-image-2 · QC Gemini · ghép ffmpeg  — render_engine.py

Dùng:
  py -3.13 brain_channel.py --channel "@simbot2" --profile satori-jp-obaa --limit 10   # quét + in bảng
  py -3.13 brain_channel.py --channel "@simbot2" --profile satori-jp-obaa --pick 1,3,5 # làm video 1,3,5
  py -3.13 brain_channel.py --videos <id1> <id2> --profile satori-jp-obaa              # làm theo id cụ thể
Import (GUI): from brain_channel import scan_channel, prepare_video, make_video_one
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
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

import channel_scan
import detect_voice
import profiles

try:
    from paths import OUT_ROOT
except Exception:
    OUT_ROOT = Path(__file__).resolve().parent.parent

HERE = Path(__file__).resolve().parent
_FROZEN = getattr(sys, "frozen", False)
PY = sys.executable
_CHILD = ["--child"] if _FROZEN else []


def _pycmd(script, *args):
    return [PY] + _CHILD + [script] + [str(a) for a in args]


def _run(cmd, on_line):
    emit = on_line or (lambda s: print(s, flush=True))
    # KHÔNG CREATE_NO_WINDOW: kế thừa console (ẩn nếu chạy từ GUI) → con/cháu không bật cửa sổ mới.
    p = subprocess.Popen(cmd, cwd=str(HERE), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", bufsize=1)
    for ln in p.stdout:
        emit("    " + ln.rstrip("\n"))
    p.wait()
    return p.returncode == 0


def _slugify(handle, idx, vid, title=""):
    """Tên thư mục workspace theo KÊNH: <handle>-<STT>-<video_id> (an toàn, truy ngược được)."""
    h = re.sub(r"[^A-Za-z0-9_-]", "", handle or "ch")[:24] or "ch"
    return f"{h}-{idx:02d}-{vid}"


def scan_channel(url, limit=60):
    """Quét kênh → dict (channel_scan.scan). GUI gọi để đổ bảng chọn."""
    return channel_scan.scan(url, limit)


def video_dir(prof, handle, idx, vid, title=""):
    slug_dir = prof.get("slug_dir") or "assets/out"
    return OUT_ROOT / slug_dir / _slugify(handle, idx, vid, title)


def prepare_video(video, prof, handle, idx, lang="", on_line=None):
    """B2 cào transcript + phát hiện giọng → ghi competitor.txt + voice.json. Trả (dir, voice_dict).

    Tách khỏi make_video_one để GUI có thể 'Phân tích giọng' hàng loạt (rẻ, nhanh) TRƯỚC khi chạy nặng."""
    emit = on_line or (lambda s: print(s, flush=True))
    vid = video["id"] if isinstance(video, dict) else str(video)
    url = video.get("url") if isinstance(video, dict) else f"https://www.youtube.com/watch?v={vid}"
    d = video_dir(prof, handle, idx, vid, video.get("title", "") if isinstance(video, dict) else "")
    d.mkdir(parents=True, exist_ok=True)
    comp = d / "competitor.txt"
    if not (comp.exists() and comp.stat().st_size > 500):
        lang = lang or {"ja": "ko,ja,en", "ko": "ko,en"}.get(prof.get("language", "ja"), "en")
        emit(f"[B2] cào transcript {vid} …")
        ok = _run(_pycmd("fetch_script.py", url, "--lang", lang, "--out", str(comp)), on_line)
        if not (ok and comp.exists()):
            emit(f"✗ B2 không cào được transcript {vid}")
            return d, None
    # 🎙 giọng theo video (ghi voice.json để render_engine + brain đọc)
    vj = d / "voice.json"
    if vj.exists():
        try:
            return d, json.loads(vj.read_text(encoding="utf-8"))
        except Exception:
            pass
    prefer = (prof.get("narrator", {}) or {}).get("gender", "")
    emit(f"[🎙] phân tích giọng {vid} …")
    r = detect_voice.detect(comp.read_text(encoding="utf-8"), prefer_gender=prefer)
    if r:
        vj.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        emit(f"    → {r['gender']}·{r['age_band']} · {r['voice_name']} (fx={r['fx']} speed={r['speed']})")
    # B2b bình luận thật — BỔ TRỢ, không bao giờ chặn (lỗi/thiếu đều tự bỏ qua trong hàm).
    try:
        fetch_comment_insight(video, prof, d, on_line)
    except Exception as e:
        emit(f"  (B2b: lỗi ngoài dự kiến {type(e).__name__} {e} → bỏ qua, không chặn tập)")
    return d, r


def fetch_comment_insight(video, prof, d, on_line=None):
    """B2b — bình luận THẬT (công khai, free) dưới video gốc → điểm chạm cảm xúc + thiếu sót cho
    Claude dùng khi viết B3 (xem ai_steps.analyze_comments). User chốt 2026-09-10.

    BỔ TRỢ TUYỆT ĐỐI — KHÔNG BAO GIỜ chặn video. Tắt bình luận / lỗi mạng / quá ít bình luận đều chỉ
    bỏ qua lặng lẽ, brain_steps vẫn viết kịch bản bình thường (không có gợi ý thêm, như trước đây)."""
    emit = on_line or (lambda s: print(s, flush=True))
    out = d / "comment_insight.json"
    if out.exists():
        return
    comp = d / "competitor.txt"
    if not comp.exists():
        return
    url = video.get("url") if isinstance(video, dict) else f"https://www.youtube.com/watch?v={video}"
    try:
        from fetch_script import video_id
        # video_id() ném SystemExit khi không nhận ra id — SystemExit KHÔNG kế thừa Exception nên
        # `except Exception` bên dưới không bắt được (đã dính bug này ở make_video.py::b2b_comments,
        # cùng lỗi). Bọc RIÊNG, dò được thì tiếp tục, không thì coi như không có video nguồn.
        try:
            vid = video_id(url)
        except SystemExit:
            vid = ""
        if not vid:
            return
        from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
        dl = YoutubeCommentDownloader()
        cmts, gen = [], dl.get_comments_from_url(
            f"https://www.youtube.com/watch?v={vid}", sort_by=SORT_BY_POPULAR)
        for c in gen:
            t = (c.get("text") or "").strip()
            if t:
                cmts.append(t)
            if len(cmts) >= 80:
                break
    except Exception as e:
        emit(f"  (B2b: không tải được bình luận — {type(e).__name__} {e} → bỏ qua, không chặn tập)")
        return
    if len(cmts) < 5:
        emit(f"  (B2b: chỉ {len(cmts)} bình luận — quá ít để rút tín hiệu đáng tin → bỏ qua)")
        return
    try:
        import ai_steps
        ins = ai_steps.analyze_comments(prof, comp.read_text(encoding="utf-8"), cmts)
    except Exception as e:
        emit(f"  (B2b: phân tích lỗi — {type(e).__name__} {e} → bỏ qua, không chặn tập)")
        return
    if ins:
        out.write_text(json.dumps(ins, ensure_ascii=False, indent=1), encoding="utf-8")
        emit(f"[B2b] {len(cmts)} bình luận → {len(ins.get('diem_cham') or [])} điểm chạm + "
             f"{len(ins.get('thieu_sot') or [])} thiếu sót → comment_insight.json")


def ensure_char_rate(prof, on_line=None):
    """Hồ sơ CHƯA đo tốc độ đọc thì đo NGAY, TRƯỚC khi Claude viết — số này quyết định Claude nhắm
    bao nhiêu chữ. Mượn của kênh khác/số tạm 309 (mặc định) là viết sai độ dài (đo thật make_video.py:
    lệch 20% = viết lại từ đầu, xem [[nguong-gate-phai-do-tu-du-lieu]]). Trả profile MỚI (đã đo)."""
    emit = on_line or (lambda s: print(s, flush=True))
    if profiles.rate_measured(prof):
        return prof
    emit(f"[B1] hồ sơ '{prof['id']}' chưa đo char_rate thật (đang tạm "
         f"{(prof.get('voice') or {}).get('char_rate') or '?'}) → đo ngay …")
    ok = _run(_pycmd("calibrate.py", "--profile", prof["id"]), on_line)
    prof2 = profiles.load(prof["id"])
    if not (ok and profiles.rate_measured(prof2)):
        emit(f"  ⚠️ đo không thành — Claude sẽ nhắm theo số tạm {profiles.char_rate(prof2)}, "
             f"rủi ro viết sai độ dài (xem docs/PROFILE_ARCHITECTURE.md §1 hoặc chạy tay: "
             f"py -3.13 calibrate.py --profile {prof['id']})")
        return prof
    emit(f"[B1] char_rate = {profiles.char_rate(prof2)} (đã ghi vào hồ sơ)")
    return prof2


BANG_SO_LIEU = OUT_ROOT / "docs" / "SO_LIEU_THAT_JP.md"


def _dem_bang_so_lieu():
    """Số dòng dữ liệu (dòng bảng markdown) trong sổ số liệu thật. 0 nếu không có file."""
    try:
        return sum(1 for l in BANG_SO_LIEU.read_text(encoding="utf-8").splitlines()
                   if l.lstrip().startswith("|"))
    except Exception:
        return 0


def _bao_bang_so_lieu(truoc, on_line=None):
    """In ra lượt này bộ não có TRA và GHI BỔ SUNG dữ kiện thế giới thật hay không.

    Vì sao cần (đo thật 2026-09-12, tập simbot2-07): prompt đã dặn 'không có trong bảng thì
    WebSearch rồi ghi bổ sung', nhưng bộ não mở bảng xong **không WebSearch lần nào** và bảng
    KHÔNG dày thêm dòng nào — trong khi tập đó nói về phí tang lễ / thủ tục thừa kế, chẳng khoản
    nào có sẵn. Tức là số liệu là ĐOÁN CHO HỢP LÝ. Dặn suông không có cơ chế đo thì không ai biết.

    KHÔNG chặn — chỉ phơi ra. Chặn ở đây sẽ đẻ ra vòng lặp như cổng tầng 2 cũ (xem §2.5 SOP)."""
    emit = on_line or (lambda s: print(s, flush=True))
    sau = _dem_bang_so_lieu()
    if sau > truoc:
        emit(f"  📗 sổ số liệu thật: +{sau - truoc} dòng mới (bộ não CÓ tra và ghi bổ sung)")
    else:
        emit("  ⚠️ sổ số liệu thật KHÔNG dày thêm dòng nào lượt này — nếu kịch bản có nhắc "
             "giá/phí/thời hạn/mức trợ cấp mới thì các số đó là ĐOÁN, chưa tra. Soi lại trước khi đăng.")
    return sau


def _khoa_profile(profile_id):
    """Chụp lại nội dung file profile để so sau khi bộ não chạy. Trả (đường_dẫn, bytes) hoặc None."""
    try:
        f = profiles._find(profile_id)
        return (f, f.read_bytes()) if f else None
    except Exception:
        return None


def _kiem_profile(khoa, on_line=None):
    """Bộ não SỬA FILE PROFILE của kênh = hỏng cả kênh, không chỉ một tập → khôi phục + cảnh báo.

    Đo thật 2026-09-11: gặp mâu thuẫn giữa profile ("cụ ông thợ may sống cô độc Osaka") và cốt truyện
    tập đang viết (viện dưỡng lão Nagano), bộ não chọn cách DỄ — sửa profile cho khớp truyện, ghi hẳn
    tiểu sử riêng của tập ("ngoài 50 mở viện dưỡng lão ở Kanto, nay là cư dân một viện ở Nagano sau
    khi trẹo khớp háng") vào hồ sơ CẢ KÊNH. Mọi tập sau sẽ thừa hưởng tiểu sử của một tập.

    Ranh giới đúng: profile = danh tính KÊNH (bền, nhiều tập dùng chung) · characters.json = nhân vật
    CỦA TẬP NÀY. Lệch nhau thì sửa tập, không bẻ kênh."""
    emit = on_line or (lambda s: print(s, flush=True))
    if not khoa:
        return
    f, truoc = khoa
    try:
        if f.read_bytes() == truoc:
            return
        f.write_bytes(truoc)
        emit(f"⚠️ BỘ NÃO ĐÃ SỬA PROFILE KÊNH ({f.name}) — ĐÃ KHÔI PHỤC lại bản cũ.")
        emit("   Profile là danh tính CẢ KÊNH; nhân vật riêng của tập phải để trong characters.json.")
    except Exception as e:
        emit(f"   (không kiểm được profile: {type(e).__name__} {e})")


def check_reflock(d, on_line=None):
    """Cổng REF-LOCK: img_prompts có `@REF` thì characters.json PHẢI đúng khuôn + ảnh master PHẢI có.

    Lỗi CÂM nguy hiểm nhất đã gặp (2026-09-11, tập simbot2-19): bộ não viết characters.json theo khuôn
    tự nghĩ — `{"REF": {...}, "REF2": {...}, "SIDE_nakamura": {...}}` thay vì `{"characters": [...]}`.
    `render_engine` đọc `cdata.get("characters", [])` ra MẢNG RỖNG ⇒ masters = [] ⇒ gọi gen_images
    KHÔNG kèm `--ref` ⇒ 41 cảnh gắn @REF gen ra mặt khác nhau hoàn toàn. Không bước nào báo lỗi: file
    tồn tại, JSON hợp lệ, ảnh vẫn ra, tiền vẫn mất — chỉ mặt nhân vật là đổi từng cảnh.

    Trả (đạt, danh_sách_lỗi)."""
    emit = on_line or (lambda s: print(s, flush=True))
    ip, cf = d / "img_prompts.txt", d / "characters.json"
    if not ip.exists() or not cf.exists():
        return True, []
    txt = ip.read_text(encoding="utf-8")
    can = sorted({m.upper() for m in re.findall(r"@(REF2|REF)\b", txt, re.I)})
    if not can:
        return True, []
    loi = []
    try:
        data = json.loads(cf.read_text(encoding="utf-8"))
    except Exception as e:
        return False, [f"characters.json không đọc được: {type(e).__name__} {e}"]
    chars = data.get("characters")
    if not isinstance(chars, list) or not chars:
        loi.append("characters.json SAI KHUÔN: thiếu mảng `characters` (khoá tìm thấy: "
                   f"{', '.join(list(data)[:8])}). Phải là "
                   '{"characters":[{"name":..,"age":..,"gender":..,"master":"_ref/001.png"}]}')
        return False, loi
    co_master = [c for c in chars if c.get("master")]
    if len(co_master) < len(can):
        loi.append(f"img_prompts dùng {len(can)} khoá mặt ({', '.join(can)}) nhưng characters.json chỉ "
                   f"khai {len(co_master)} nhân vật có `master`")
    for c in co_master:
        f = d / str(c["master"])
        if not f.exists():
            loi.append(f"thiếu ảnh master của {c.get('name')}: {c['master']} (phải gen trước)")
    for l in loi:
        emit(f"    ✗ REF-LOCK: {l}")
    return not loi, loi


VONG_SUA_B3Q = 3   # số lượt cho bộ não sửa TẠI CHỖ trước khi trả lại cho người


def check_b3q(prof, d, on_line=None, bo_cham_claude=False):
    """Cổng NỘI DUNG (B3Q) — chạy LẠI `qc_script.py` để XÁC MINH, không tin lời bộ não tự khai.

    Vì sao phải verify: đo thật 2026-09-11, bộ não chạy B3Q, gặp Gemini chặn content-policy, tự kết
    luận "lỗi hạ tầng, không phải script sai" rồi đi tiếp. Chạy lại thật thì kịch bản đó có 13 lỗi
    NẶNG: nhân vật 74 tuổi trong characters.json nhưng kịch bản dựng thành 78 tuổi làm y tá, còn sót
    「水キムチ」 của bản gốc Hàn, mốc thời gian tự mâu thuẫn. Tin lời tự khai = xuất bản kịch bản hỏng.

    Trả (đạt, các_dòng_lỗi). `qc_script.py` exit 1 khi HỎNG/SỬA/KHÔNG_KIỂM_ĐƯỢC — "0 lỗi" lúc QC
    không chạy được là SỐ ẢO, không được coi là đạt."""
    emit = on_line or (lambda s: print(s, flush=True))
    sf, cf = d / "script.txt", d / "competitor.txt"
    if not sf.exists():
        return True, []
    cmd = _pycmd("qc_script.py", "--profile", prof["id"], "--script", str(sf))
    if cf.exists():
        cmd += ["--competitor", str(cf)]
    p = subprocess.Popen(cmd, cwd=str(HERE), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", bufsize=1)
    lines = []
    for ln in p.stdout:
        ln = ln.rstrip("\n")
        lines.append(ln)
        emit("    " + ln)
    p.wait()
    loi = [l.strip() for l in lines if l.strip().startswith("✗")]
    # Máy chấm CƠ HỌC của qc_script in bằng "[cao]/[vua]/[thap] <tên lỗi>:" — không có "✗" ở đầu nên
    # bản đầu BỎ SÓT (đo thật: cổng báo RỚT mà liệt kê 0 vấn đề ⇒ bộ não nhận danh sách rỗng).
    loi += [l.strip() for l in lines
            if re.match(r"^\[(cao|vua|thap|trung_binh)\]", l.strip()) and l.strip() not in loi]
    # qc_script KẾT LUẬN DAT (exit 0) mà vẫn in vài dòng "✗" tham khảo (trùng ý / mối nối / logic thấp —
    # verdict của nó không tính các mục này) → KHÔNG được coi là chặn. Đo thật STT10 2026-09-18: gemini
    # tự ghi "trùng ý: thủ pháp kết cấu vòng CÓ CHỦ ĐÍCH" + kết luận DAT, cổng vẫn rớt 2 lượt liền rồi
    # ESCALATION vì đếm dòng ✗. Tách SAI khỏi CHƯA HAY: chặn theo verdict, ✗ chỉ in cho biết.
    if p.returncode == 0 and loi:
        emit(f"    (B3Q kết luận DAT — {len(loi)} ghi chú ✗ chỉ tham khảo, không chặn)")
        loi = []
    # ⚠️ Kết luận 70/30 in bằng dòng bắt đầu "—", KHÔNG phải "✗" — chỉ gom dòng "✗" là BỎ SÓT đúng
    # cái chặn nặng nhất. Đo thật 2026-09-11: cổng báo "1 vấn đề: logic [thap]…" rồi đưa bộ não đi
    # sửa mỗi lỗi vặt đó, trong khi thứ thật sự làm rớt là "giữ 100% nhịp · LECH_NHIEU". Bộ não sửa
    # xong lỗi vặt, chạy lại vẫn rớt y nguyên — vòng lặp vô nghĩa.
    for l in lines:
        t = l.strip()
        if "bám gốc" in t and ("LECH_NHIEU" in t or "SAO_CHEP" in t):
            loi.insert(0, "⛔ " + t.lstrip("— ").strip() +
                       " — ĐÂY LÀ LỖI CHẶN NẶNG NHẤT, phải xử TRƯỚC: bỏ HẲN 2-3 nhịp của bản gốc và "
                       "THÊM 3-4 nhịp tự nghĩ (đổi đạo cụ/bối cảnh/quan hệ nhân vật), giữ khung cảm "
                       "xúc. Sửa câu chữ KHÔNG bao giờ gỡ được lỗi này vì cổng chấm KHUNG SỰ KIỆN.")

    # TẦNG 0 — MÁY soi dấu vết quy đổi tiền (xem qc_tien.py): tất định, 1 giây, 0 đồng. Chạy TRƯỚC
    # hai tầng LLM vì đây là thứ ĐONG ĐẾM ĐƯỢC — không có lý do gì trả tiền/thời gian cho LLM đoán
    # lại. Gemini mù hẳn loại lỗi này, Claude bắt được nhưng mất ~10 phút và không tất định.
    cf0 = d / "competitor.txt"
    if cf0.exists():
        try:
            import qc_tien
            vet, _jp, _kr = qc_tien.soi(sf.read_text(encoding="utf-8"),
                                        cf0.read_text(encoding="utf-8"))
            for s_jp, v_jp, s_kr, v_kr, t in vet:
                loi.insert(0, f"DẤU_VẾT_QUY_ĐỔI: 「{s_jp}」 = {v_jp:,} đúng bằng 「{s_kr}」 "
                              f"({v_kr:,}) ÷ {t} của bản gốc — thay bằng MỨC THẬT của nước sở tại "
                              f"cho hạng mục đó, KHÔNG quy đổi theo tỉ giá")
            if vet:
                emit(f"    [tầng 0] {len(vet)} dấu vết quy đổi tiền (máy soi, tất định)")
        except Exception as e:
            emit(f"    (tầng 0 lỗi {type(e).__name__} {e} → bỏ qua)")

    # TẦNG 2 — giám khảo Claude phiên MỚI (xem qc_claude.py). Bù đúng chỗ gemini mù: dấu vết quy đổi
    # tiền 1:10 của bản gốc, thuật ngữ dịch sát, phong tục sai. Đo thật: gemini 8 lỗi ↔ Claude 22 lỗi,
    # mỗi bên có lỗi bên kia bỏ sót ⇒ chặn theo HỢP của hai danh sách, không thay nhau.
    cf2 = d / "competitor.txt"
    if bo_cham_claude:
        return p.returncode == 0 and not loi, loi[:20]
    try:
        import qc_claude
        emit("    [tầng 2] giám khảo Claude (phiên mới) …")
        t0 = time.perf_counter()
        bo, _ = qc_claude.cham(sf.read_text(encoding="utf-8"),
                               cf2.read_text(encoding="utf-8")[:24000] if cf2.exists() else "",
                               on_line=emit)
        if bo is None:
            emit("    (tầng 2 không chấm được — CHỈ dựa vào tầng 1, đừng coi là đã soi đủ)")
        else:
            # CHỈ mức CHAN mới chặn. Góp ý văn phong in ra cho biết rồi THÔI.
            # Đo thật 2026-09-11: chặn theo TỔNG số lỗi thì cổng không bao giờ mở được — 16 lỗi,
            # sửa đúng 14 chỗ nó nêu, lượt sau ra 20 lỗi MỚI (toàn "người bản xứ thường nói khác").
            # Một cổng không thể đạt thì không phải cổng, là vòng lặp: 73 phút + $16 quota cho một
            # kịch bản mà cổng số học, cổng tiền và tầng 1 đều bảo ĐẠT.
            chan, gopy = bo
            emit(f"    [tầng 2] {len(chan)} lỗi CHẶN · {len(gopy)} góp ý (không chặn) "
                 f"· {(time.perf_counter()-t0)/60:.1f} phút")
            for g in gopy[:6]:
                emit(f"       · góp ý (bỏ qua được): {g[:150]}")
            loi += chan
    except Exception as e:
        emit(f"    (tầng 2 lỗi ngoài dự kiến {type(e).__name__} {e} → bỏ qua)")
    return (p.returncode == 0 and not loi), loi[:20]


KHONG_SUA_DUOC = "SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC"


def _tieu_de_b3s(d, video):
    """Tiêu đề đưa cho sol: title của video (nếu prepare đã lấy) → dòng đầu dan_y.txt → chuỗi rỗng."""
    t = (video.get("title") if isinstance(video, dict) else "") or ""
    if not t.strip() and (d / "dan_y.txt").exists():
        t = next((l.strip() for l in (d / "dan_y.txt").read_text(encoding="utf-8").splitlines()
                  if l.strip()), "")
    return t.strip() or "(chưa chốt tiêu đề)"


def check_b3s(prof, d, video, minutes, on_line=None, permission_mode="acceptEdits", budget_usd=0.0):
    """B3S — QC độc lập bằng GPT-5.6-sol (khác hãng với Claude viết + gemini B3Q), áp dụng y lane E
    (`make_video.py::b3s_sol`) cho flow B. CHỈ chạy khi `profile.script.sol_qc = true`.

    Thứ tự anh chốt 2026-09-18 (thay tầng 2 Claude chấm trong check_b3q — cùng model chấm nhau thì
    tự nhận đúng cả, vô nghĩa):
      B3Q gemini → B3S sol chấm →
        PASS   → sang assets.
        FIX    → Claude sửa TẠI CHỖ theo báo cáo sol (chỉ mục ghi SAI) → sol chấm lại ĐÚNG 1 lần →
                 PASS/FIX (lỗi nhẹ) đều cho qua; REMAKE → rơi xuống nhánh REMAKE.
        REMAKE → Claude đọc báo cáo, cái nào SAI thật thì xoá/sửa, rồi TỰ chấm lại: được → PASS
                 (lỗi nhẹ cũng PASS); không sửa được → ghi "SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC" và DỪNG.
    Không lặp thêm vòng nào ngoài các mốc trên (sol không bao giờ tự PASS văn phổ thông —
    đo thật lane E, xem docs/QC_SCRIPT_GPT_SOL.md). Trả (đi_tiếp, verdict_cuối)."""
    import brain_steps
    emit = on_line or (lambda s: print(s, flush=True))
    if not ((prof.get("script") or {}).get("sol_qc")):
        return True, "SKIPPED"
    sf = d / "script.txt"
    logs = d / "logs"
    logs.mkdir(exist_ok=True)
    sys.path.insert(0, str(HERE))
    import qc_script_sol
    import gate_common
    # RESUME: script.txt chưa đổi so với lần B3S đã cho qua → không chấm lại (đo thật STT9: chạy lại
    # sau khi hết quota Claude, sol lại FIX → Claude lại sửa script → img_prompts.txt vừa viết lệch bản
    # script mới, trong khi lần trước đã cho qua rồi).
    nhat_ky = logs / "B3S_latest.json"
    h_script = gate_common.sha256_file(sf)
    if nhat_ky.exists():
        try:
            cu = json.loads(nhat_ky.read_text(encoding="utf-8"))
            if cu.get("script_sha256") == h_script and cu.get("di_tiep"):
                emit(f"[B3S] ⏭ script.txt chưa đổi từ lần B3S {cu.get('verdict')} → bỏ qua (resume)")
                return True, cu.get("verdict", "PASS")
        except Exception:
            pass

    def ghi(di_tiep, verdict):
        try:
            nhat_ky.write_text(json.dumps({"script_sha256": gate_common.sha256_file(sf),
                                           "verdict": verdict, "di_tiep": di_tiep,
                                           "time": time.strftime("%Y-%m-%d %H:%M:%S")},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:
            pass
        return di_tiep, verdict

    def cham(n):
        # tiêu đề đọc lại mỗi lượt: Claude có thể sửa dòng đầu dan_y.txt khi sol bảo tiêu đề lệch
        title = _tieu_de_b3s(d, video)
        out = logs / f"B3S_sol_{n:03d}.txt"
        t0 = time.perf_counter()
        try:
            verdict, text = qc_script_sol.run(sf.read_text(encoding="utf-8"), title,
                                              profile_id=prof["id"], out=str(out))
        except Exception as e:
            emit(f"    (B3S lượt {n}: sol không chấm được — {type(e).__name__} {e} → coi như PASS, "
                 f"KHÔNG phải đã soi)")
            return "INFRA", ""
        emit(f"    [B3S lượt {n}] {verdict} · {(time.perf_counter()-t0)/60:.1f} phút · {out.name}")
        return verdict, text

    # sol nhận "TIÊU ĐỀ" = title video nếu có, không thì DÒNG ĐẦU dan_y.txt — Claude sửa phải biết
    # sửa ở đâu (STT9: sol 2 lượt liền báo tiêu đề 42万 ↔ truyện 50万 vì Claude chỉ sửa script).
    nguon_tieu_de = ("title của video" if (isinstance(video, dict) and (video.get("title") or "").strip())
                     else "DÒNG ĐẦU của `dan_y.txt` (sửa tiêu đề = sửa dòng đó)")

    def claude_sua(extra):
        _kh = _khoa_profile(prof["id"])
        truoc = sf.read_text(encoding="utf-8")
        ok, _ = brain_steps.run_creative(d, prof["id"], minutes, on_line=on_line,
                                         permission_mode=permission_mode, budget_usd=budget_usd,
                                         phase="script", extra_prompt=extra)
        _kiem_profile(_kh, on_line)
        if ok and sf.read_text(encoding="utf-8") != truoc:
            # cổng số đo lại sau khi sửa chữ (đổi độ dài) — máy nắn, không chặn (lệch nhỏ B4Q bắt sau)
            van_de = check_gate(prof, d, minutes, on_line)
            if van_de:
                _run(_pycmd("fix_gate.py", "--script", str(sf), "--profile", prof["id"],
                            "--minutes", str(minutes)), on_line)
                van_de = check_gate(prof, d, minutes, on_line)
                if van_de:
                    emit(f"    ⚠️ sau sửa B3S script lệch cổng số ({'; '.join(van_de)}) — ghi nhận, đi tiếp")
            # HỒI QUY B3Q sau mỗi lượt sửa theo sol — bắt buộc. Đo thật STT10 2026-09-19: sửa theo
            # sol (bỏ chi tiết tip 1.000 yên vì "không tự nhiên ở Nhật") làm GÃY 伏線 của cuốn sổ cuối
            # truyện, và 3 câu viết lại thành dịch sát bản Hàn ⇒ B3Q nhảy từ DAT sang HONG/SAO_CHEP.
            # Sol chỉ soi bản Nhật đứng một mình, KHÔNG thấy bản gốc và KHÔNG theo dõi 伏線 toàn tập.
            dat2, loi2 = check_b3q(prof, d, on_line, bo_cham_claude=True)
            if not dat2:
                emit(f"⟳ sửa theo sol làm RỚT lại B3Q ({len(loi2)} vấn đề) → sửa 1 lượt hồi quy")
                for v in loi2[:6]:
                    emit(f"     - {v[:170]}")
                _kh2 = _khoa_profile(prof["id"])
                brain_steps.run_creative(
                    d, prof["id"], minutes, on_line=on_line, permission_mode=permission_mode,
                    budget_usd=budget_usd, phase="script",
                    extra_prompt=("⛔ VIỆC DUY NHẤT LƯỢT NÀY: lượt sửa theo QC sol vừa rồi làm `script.txt` "
                                  "RỚT LẠI cổng B3Q. Sửa TẠI CHỖ đúng các mục dưới đây, giữ nguyên phần đã "
                                  "sửa theo sol (đặc biệt: 伏線 gieo phải được trả, câu bị nghi dịch sát bản "
                                  "gốc phải viết lại bằng cách diễn đạt Nhật khác hẳn):\n   - "
                                  + "\n   - ".join(loi2)
                                  + f"\nSửa xong chạy `py -3.13 \"{HERE / 'gate_check.py'}\" --profile "
                                    f"{prof['id']} --script {sf} --minutes {minutes}` xác nhận cổng số vẫn "
                                    "đạt, rồi in BRAIN_DONE và dừng."))
                _kiem_profile(_kh2, on_line)
        return ok

    emit("[B3S] QC độc lập bằng GPT-5.6-sol …")
    verdict, text = cham(1)
    if verdict in ("PASS", "INFRA"):
        return ghi(True, verdict) if verdict == "PASS" else (True, verdict)
    if verdict == "FIX":
        emit("⟳ B3S FIX → Claude sửa TẠI CHỖ theo báo cáo sol (chỉ mục ghi SAI) …")
        claude_sua(
            "⛔ VIỆC DUY NHẤT LƯỢT NÀY: `script.txt` bị QC độc lập (GPT-5.6-sol) chấm FIX. Đọc báo cáo "
            f"ở `{logs / 'B3S_sol_001.txt'}` (TIÊU ĐỀ mà sol thấy = {nguon_tieu_de}). Sửa TẠI CHỖ đúng "
            "những mục ghi SAI (mâu thuẫn dữ kiện, số "
            "học/tiền, dấu vết Hàn, logic gãy, ngữ pháp thật); mục CHƯA HAY/văn phong BỎ QUA. KHÔNG viết "
            "lại cả bài, giữ nguyên cốt truyện/độ dài/văn phong và mọi file khác. Sửa xong chạy "
            f"`py -3.13 \"{HERE / 'gate_check.py'}\" --profile {prof['id']} --script {sf} --minutes "
            f"{minutes}` xác nhận cổng số vẫn đạt, rồi in BRAIN_DONE và dừng.")
        verdict, text = cham(2)
        if verdict != "REMAKE":
            if verdict == "FIX":
                emit("[B3S] ⚠️ vẫn FIX sau 1 lượt sửa (lỗi nhẹ/góp ý) → cho qua, xem B3S_sol_002.txt nếu muốn soi")
            return ghi(True, verdict)
        bao_cao = logs / "B3S_sol_002.txt"
    else:
        bao_cao = logs / "B3S_sol_001.txt"
    if verdict == "UNKNOWN":
        emit("[B3S] ⚠️ sol trả lời không có dòng KẾT QUẢ → không kết luận được, cho qua (xem log)")
        return True, verdict
    # REMAKE → Claude tự kiểm từng lỗi sol nêu, xoá/sửa cái SAI thật, tự chấm lại.
    emit("⟳ B3S REMAKE → Claude kiểm từng lỗi sol nêu, xoá/sửa cái SAI thật, tự chấm lại …")
    vf = logs / "B3S_claude_verdict.txt"
    if vf.exists():
        vf.unlink()
    claude_sua(
        "⛔ VIỆC DUY NHẤT LƯỢT NÀY: `script.txt` bị QC độc lập (GPT-5.6-sol) chấm REMAKE. Đọc báo cáo "
        f"ở `{bao_cao}` (TIÊU ĐỀ mà sol thấy = {nguon_tieu_de}). Với TỪNG lỗi sol nêu: tự kiểm lại "
        "trong script — SAI thật thì xoá/sửa tại chỗ "
        "đoạn đó (được cắt bỏ tình tiết gãy, thêm 1-2 câu nối), sol nói sai thì bỏ qua. KHÔNG viết lại "
        "cả bài. Sửa xong TỰ CHẤM LẠI toàn bộ kịch bản: còn lỗi nhẹ vẫn là PASS; chỉ khi khung truyện "
        f"gãy không cứu được mới là không sửa được. Ghi kết luận vào file `{vf}` — DÒNG ĐẦU đúng 1 "
        f"trong 2 chuỗi: `PASS` hoặc `{KHONG_SUA_DUOC}`, các dòng sau là lý do ngắn. Rồi chạy "
        f"`py -3.13 \"{HERE / 'gate_check.py'}\" --profile {prof['id']} --script {sf} --minutes "
        f"{minutes}`, in BRAIN_DONE và dừng.")
    kl = ""
    if vf.exists():
        kl = next((l.strip() for l in vf.read_text(encoding="utf-8").splitlines() if l.strip()), "")
    if kl.upper().startswith("PASS"):
        emit("[B3S] ✓ Claude tự chấm sau sửa REMAKE: PASS → đi tiếp")
        return ghi(True, "PASS_CLAUDE")
    ly_do = kl or "Claude không ghi kết luận vào B3S_claude_verdict.txt"
    emit(f"✗ B3S: {KHONG_SUA_DUOC} — {ly_do}")
    try:
        import gate_common
        gate_common.viet_escalation_report(
            d, "B3S", [{"attempt": 1, "status": "REMAKE", "blocking_issues": [KHONG_SUA_DUOC, ly_do,
                                                                               f"báo cáo sol: {bao_cao}"]}],
            goi_y="Đọc tay báo cáo sol + B3S_claude_verdict.txt, quyết định lại cốt truyện/phạm vi rồi chạy lại.")
        emit(f"  → đã ghi {d / 'ESCALATION_REPORT.md'}")
    except Exception as e:
        emit(f"  (không ghi được ESCALATION_REPORT.md: {type(e).__name__} {e})")
    return ghi(False, "REMAKE")


def check_gate(prof, d, minutes, on_line=None):
    """Kiểm ĐỘC LẬP script.txt Claude vừa viết bằng NGƯỠNG-BẰNG-SỐ của CHÍNH kênh này — thuần Python,
    KHÔNG tốn thêm LLM. Đóng nốt lỗ hổng: tool não-Claude giao hẳn việc viết cho prompt tự nhiên ngữ
    (không qua ai_steps.write_script() có gate mã cứng như tool não-Gemini), nên cần lớp ép-số RIÊNG
    sau khi Claude viết xong, đừng chỉ trông chờ B4Q bắt lúc đã tốn tiền giọng."""
    emit = on_line or (lambda s: print(s, flush=True))
    sf = d / "script.txt"
    if not sf.exists():
        return []
    try:
        import ai_steps
        # ai_steps.check() trả TUPLE (danh_sách_lỗi, số_đo). Trả thẳng tuple ra ngoài là hỏng NGẦM:
        # tuple 2 phần tử LUÔN truthy nên `if van_de:` chặn cả kịch bản ĐẠT SẠCH. Chỉ trả list lỗi.
        bad, _do = ai_steps.check(prof, sf.read_text(encoding="utf-8"), minutes)
        return bad
    except Exception as e:
        emit(f"  (check_gate: không kiểm được — {type(e).__name__} {e})")
        return []


def make_video_one(video, prof, handle, idx, minutes=0, lang="", on_line=None,
                   permission_mode="acceptEdits", budget_usd=0.0, do_prepare=True, force_lane=False,
                   stop_before_render=False, stop_after_b3s=False):
    """Làm TRỌN 1 video: (B2+giọng nếu chưa) → 🧠 Claude viết → 🎬 render. Trả True nếu ra final.mp4.

    Thứ tự bước 1 (P0 2026-09-18): B2Q transcript → PHA script (chỉ khi thiếu script.txt) → cổng số →
    B3Q gemini (vòng sửa, không hội tụ = ESCALATION_REPORT.md) → B3S sol (nếu profile.script.sol_qc;
    PASS/FIX-nhẹ đi tiếp, REMAKE không cứu được = dừng) → PHA assets (chỉ khi thiếu asset) → stamp
    fingerprint → rào STALE (hash) → REF-LOCK → B5P (prompt↔script) → B55 mapping (img_doan) →
    `stop_before_render`.

    `stop_before_render=True` = SẢN XUẤT: dừng sau bước 1, giao máy 2 (ảnh) → Hermes (ghép). Mặc định
    False chỉ để giữ tương thích test/tập non-hybrid cũ — `render_engine.py` ở cuối hàm KHÔNG phải
    đường sản xuất hiện tại (xem CLAUDE.md § CẤM TUYỆT ĐỐI: Claude Code chỉ làm bước 1).

    `force_lane=True` bỏ qua 2 hàng rào lane (gate mượn mặc định / script lệch gate-bằng-số) — chỉ
    dùng khi CHẤP NHẬN rủi ro, mặc định luôn CHẶN (giống make_video.py, xem [[hang-rao-chong-lan-lane]])."""
    import brain_steps
    import gate_common
    emit = on_line or (lambda s: print(s, flush=True))
    if do_prepare:
        d, _ = prepare_video(video, prof, handle, idx, lang, on_line)
    else:
        vid = video["id"] if isinstance(video, dict) else str(video)
        d = video_dir(prof, handle, idx, vid)
    if not (d / "competitor.txt").exists():
        emit("✗ thiếu competitor.txt → bỏ video này"); return False
    final = d / "final.mp4"
    if final.exists():
        emit(f"⏭ đã có final.mp4 ({d.name}) → bỏ qua (resume)"); return True
    # HÀNG RÀO 1: hồ sơ mượn DEFAULT_GATE của satori (nhịp tâm tình cụ bà) cho một kênh khác là gật
    # đầu cho đúng thứ mình không muốn mà không báo gì (đo thật: gate mặc định ăn nhầm ngách tài
    # liệu). Profile lập qua wizard `new_profile.py` đã tự khai gate → KHÔNG bị chặn ở đây.
    if not profiles.gate_declared(prof) and not force_lane:
        emit(f"✗ hồ sơ '{prof['id']}' chưa khai `script.gate` riêng → sẽ mượn nhịp văn của kênh "
             f"satori. DỪNG trước khi tiêu tiền. Thêm gate vào profiles/{prof['id']}.json "
             f"(mẫu: docs/PROFILE_ARCHITECTURE.md §5), hoặc chạy lại với force_lane=True nếu chấp nhận.")
        return False
    prof = ensure_char_rate(prof, on_line)
    mn = minutes or profiles.target_minutes(prof)
    # B2Q — transcript có đủ không (P0). FAIL = transcript cụt/lặp → viết trên nửa câu chuyện.
    # SKIPPED/WARN (exit 0) → đi tiếp. _run stream log ra on_line như mọi cổng khác.
    emit("[B2Q] kiểm transcript …")
    if not _run(_pycmd("qc_transcript.py", "--slug", str(d)), on_line):
        emit("✗ B2Q transcript RỚT (xem logs/B2Q_latest.json) → thử --method khác/proxy rồi chạy lại")
        return False
    # PHA 1 — CHỈ script.txt (P0 2026-09-18: tách khỏi asset để B3Q sửa script XONG rồi mới viết
    # prompt/img_doan — trước đây viết tất cả 1 lượt rồi vòng B3Q sửa script SAU → img_prompts/img_doan
    # bám bản script CŨ; bằng chứng STT3: img_prompts 18:36 < script 20:45, 3 ảnh mâu thuẫn cốt truyện).
    if not (d / "script.txt").exists() or (d / "script.txt").stat().st_size < 50:
        _bang0 = _dem_bang_so_lieu()
        _kh = _khoa_profile(prof["id"])
        ok, last = brain_steps.run_creative(d, prof["id"], mn, on_line=on_line, phase="script",
                                            permission_mode=permission_mode, budget_usd=budget_usd)
        _bao_bang_so_lieu(_bang0, on_line)
        _kiem_profile(_kh, on_line)
        if not ok or not (d / "script.txt").exists():
            emit(f"✗ bộ não chưa ra script.txt ({last}) → dừng {d.name}"); return False
    # HÀNG RÀO 2: Claude viết qua prompt tự nhiên ngữ (không qua gate mã cứng như ai_steps.write_script)
    # → kiểm LẠI bằng số sau khi viết xong, TRƯỚC khi tiêu tiền giọng+ảnh. Tool não-Gemini có bước
    # này ở B3 (ai_steps.check trong vòng viết-lại); ở đây kiểm 1 lần, không tự viết lại (đắt quota MAX).
    van_de = check_gate(prof, d, mn, on_line)
    if van_de and not force_lane:
        # SỬA NGAY TRONG LƯỢT NÀY, đừng để lần sau: script.txt "đã tồn tại" nhưng LỆCH SỐ vẫn là file
        # hỏng — resume theo tồn-tại-file sẽ bỏ qua khâu sáng tạo ở lần chạy sau và rớt y hệt chỗ này
        # mãi mãi (đo thật 2026-09-10: chạy lại lần 2 ra đúng từng con số cũ).
        # BƯỚC 1 — NẮN BẰNG MÁY trước (fix_gate.py: nén khúc + tách câu + hạ hội thoại, chạy LLM rẻ
        # 3 luồng, KHÔNG tiêu quota Claude). Đo thật 2026-09-10: bộ não tự cắt 20.000→9.169 mất 35
        # phút + cạn ngân sách mà VẪN thừa 97 chữ; fix_gate nén 16.014 chữ về ĐẠT trong 4,7 phút.
        emit(f"⟳ script.txt lệch cổng số học → nắn BẰNG MÁY trước: {'; '.join(van_de)}")
        _run(_pycmd("fix_gate.py", "--script", str(d / "script.txt"), "--profile", prof["id"],
                    "--minutes", str(mn)), on_line)
        van_de = check_gate(prof, d, mn, on_line)
    if van_de and not force_lane:
        # BƯỚC 2 — máy nắn chưa đủ mới phiền tới bộ não (đắt hơn, nên để sau).
        emit(f"⟳ máy nắn chưa hết lệch → gọi bộ não nắn lại (1 lượt): {'; '.join(van_de)}")
        _kh = _khoa_profile(prof["id"])
        # phase="script": pha asset CHƯA chạy ở điểm này (thứ tự mới) → run_creative chỉ được đòi script.txt.
        ok, last = brain_steps.run_creative(
            d, prof["id"], mn, on_line=on_line, permission_mode=permission_mode,
            budget_usd=budget_usd, phase="script",
            extra_prompt=(
                "⛔ VIỆC DUY NHẤT LƯỢT NÀY: `script.txt` đã viết xong nhưng RỚT CỔNG SỐ HỌC. Giữ nguyên "
                "cốt truyện/nhân vật/các file khác nếu đã có (TUYỆT ĐỐI không viết lại, không viết "
                "thêm asset). Chỉ nắn `script.txt` cho khớp số:\n   - "
                + "\n   - ".join(van_de)
                + f"\nĐo lại bằng: py -3.13 \"{Path(__file__).with_name('gate_check.py')}\" "
                  f"--profile {prof['id']} "
                  f"--script {d / 'script.txt'} --minutes {mn}\n"
                  "Sửa → đo → sửa tới khi in `CỔNG SỐ HỌC: ĐẠT`, rồi in BRAIN_DONE và dừng."))
        _kiem_profile(_kh, on_line)
        van_de = check_gate(prof, d, mn, on_line) if ok else van_de
    if van_de and not force_lane:
        emit(f"✗ script.txt vẫn lệch gate của kênh '{prof['id']}':")
        for v in van_de:
            emit(f"   - {v}")
        emit("  Sửa tay script.txt cho khớp nhịp/độ dài rồi chạy lại, hoặc force_lane=True nếu chấp nhận.")
        return False
    # CỔNG NỘI DUNG B3Q — XÁC MINH bằng máy, không tin bộ não tự khai (xem check_b3q).
    # Lane bật sol_qc → TẮT tầng 2 Claude chấm (Claude chấm văn Claude viết = tự nhận đúng, và là
    # nguồn không hội tụ ở Test 1 STT9); vai đó giao cho B3S sol ngay dưới (anh chốt 2026-09-18).
    co_sol = bool((prof.get("script") or {}).get("sol_qc"))
    dat_b3q, loi_b3q = check_b3q(prof, d, on_line, bo_cham_claude=co_sol)
    # Lịch sử từng lượt B3Q (cho ESCALATION_REPORT.md khi không hội tụ — ghi đúng lỗi của TỪNG lượt,
    # không lặp lại một danh sách cho mọi lượt).
    lich_su_b3q = [] if dat_b3q else [{"attempt": 1, "status": "FAIL", "blocking_issues": list(loi_b3q)}]
    # SỬA TẠI CHỖ, NHIỀU LƯỢT, CÓ CHỐT KHÔNG-HỘI-TỤ (anh chốt 2026-09-11).
    # Trước: đúng 1 lượt sửa, còn lỗi là vứt cả tập báo FAIL — 73 phút công đổ sông, rồi lần
    # chạy sau lại SINH CHỮ MỚI nên ra bộ lỗi MỚI, không bao giờ hội tụ. Nay sửa tiếp trên
    # CHÍNH bản cũ, và dừng ngay khi số lỗi chặn KHÔNG GIẢM.
    for luot in range(1, VONG_SUA_B3Q + 1):
        if dat_b3q or force_lane:
            break
        truoc = len(loi_b3q)
        emit(f"⟳ B3Q chưa đạt ({truoc} vấn đề chặn) → sửa TẠI CHỖ trên bản cũ [lượt {luot}/{VONG_SUA_B3Q}]")
        # IN RA nội dung lỗi chặn, không chỉ số lượng: vòng sửa đưa danh sách thẳng vào prompt nên
        # trước đây người theo dõi chỉ thấy con số, muốn biết hỏng gì phải ngồi đoán (dính 2 lần).
        for v in loi_b3q[:10]:
            emit(f"     - {v[:180]}")
        _kh = _khoa_profile(prof["id"])
        # phase="script": vẫn đang ở pha script — asset chưa viết, không đòi/không cho viết asset.
        ok, _ = brain_steps.run_creative(
            d, prof["id"], mn, on_line=on_line, permission_mode=permission_mode,
            budget_usd=budget_usd, phase="script",
            extra_prompt=(
                "⛔ VIỆC DUY NHẤT LƯỢT NÀY: `script.txt` RỚT CỔNG NỘI DUNG B3Q. Giữ nguyên cốt truyện "
                "và các file khác; chỉ sửa ĐÚNG những chỗ bị nêu dưới đây, đừng viết lại cả bài "
                "(viết lại là lệch cổng số, phải nắn lại từ đầu):\n   - "
                + "\n   - ".join(loi_b3q)
                + "\nSửa xong chạy lại `qc_script.py` tới khi hết lỗi NẶNG, rồi chạy `gate_check.py` "
                  "xác nhận cổng số vẫn đạt (sửa chữ làm đổi độ dài), rồi in BRAIN_DONE và dừng."))
        _kiem_profile(_kh, on_line)
        if not ok:
            lich_su_b3q.append({"attempt": luot + 1, "status": "FAIL",
                                "blocking_issues": ["bộ não bỏ dở lượt sửa (run_creative không xong)"]})
            break
        dat_b3q, loi_b3q = check_b3q(prof, d, on_line, bo_cham_claude=co_sol)
        lich_su_b3q.append({"attempt": luot + 1, "status": "PASS" if dat_b3q else "FAIL",
                            "blocking_issues": list(loi_b3q)})
        if not dat_b3q and len(loi_b3q) >= truoc:
            emit(f"  ⏹ số lỗi chặn KHÔNG GIẢM ({truoc} → {len(loi_b3q)}) — dừng sửa. Sửa thêm chỉ đốt lượt mà không hội tụ; danh sách còn lại ở dưới, sửa tay là nhanh nhất.")
            break
    if not dat_b3q and not force_lane:
        emit(f"✗ script.txt vẫn RỚT cổng nội dung B3Q ({len(loi_b3q)} vấn đề):")
        for v in loi_b3q[:8]:
            emit(f"   - {v[:150]}")
        emit("  Sửa tay rồi chạy lại, hoặc force_lane=True nếu chấp nhận.")
        # ESCALATED (P0): vòng sửa không hội tụ → ghi báo cáo cho người/Claude interactive xem tay.
        try:
            gate_common.viet_escalation_report(
                d, "B3Q", lich_su_b3q,
                goi_y="Sửa tay script.txt đúng các dòng trên rồi chạy lại; KHÔNG viết lại cả bài.")
            emit(f"  → đã ghi {d / 'ESCALATION_REPORT.md'}")
        except Exception as e:
            emit(f"  (không ghi được ESCALATION_REPORT.md: {type(e).__name__} {e})")
        return False

    # B3S — QC độc lập GPT-5.6-sol (chỉ lane khai script.sol_qc). PASS/FIX-nhẹ đi tiếp;
    # REMAKE không cứu được = "SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC" → dừng (xem check_b3s).
    if not force_lane:
        di_tiep, _v = check_b3s(prof, d, video, mn, on_line=on_line,
                                permission_mode=permission_mode, budget_usd=budget_usd)
        if not di_tiep:
            return False
    if stop_after_b3s:
        # Chỉ test QC NỘI DUNG (script → cổng số → B3Q → B3S): không viết asset/tiêu đề/thumb.
        emit(f"⏸ DỪNG SAU B3S theo yêu cầu — script.txt đã qua cổng số + B3Q + B3S: {d}")
        return True

    # PHA 2 — asset trên script ĐÃ CHỐT (script đã qua cổng số + B3Q + B3S, từ đây KHÔNG được sửa script).
    # img_doan.txt: ảnh nào thuộc đoạn lời nào — thiếu là khâu ghép chia ảnh theo SỐ ĐẾM, ảnh trôi
    # dần về cuối (đo thật tập 04/06: 3,1/5 và 2,9/5). TIEU_DE_MO_TA.txt: bước 2/3 không hiểu nội
    # dung, không tự viết tiêu đề/mô tả được (2 tập từng lọt với listting rỗng) — xem CLAUDE.md § bước 1.
    need_assets = profiles.assets_need(prof)   # lane khai `assets.skip` thì bỏ file đó (xem profiles.assets_need)
    thieu = [f for f in need_assets if not (d / f).exists()]
    thieu_truoc_khi_chay = bool(thieu)
    for lan in (1, 2):
        if not thieu:
            break
        # LỚP THỨ BA chống "dừng lại báo cáo thay vì làm" (lọt 2/8 lượt dù prompt đã cấm 2 lớp):
        # lượt 2 nói thẳng nó bỏ dở cái gì. Kiểm thiếu-file chạy CẢ KHI bộ não khai BRAIN_DONE.
        _kh = _khoa_profile(prof["id"])
        extra = "" if lan == 1 else (
            "⛔ LƯỢT TRƯỚC BẠN DỪNG LẠI BÁO CÁO THAY VÌ LÀM XONG. Chế độ không người giám sát — "
            f"làm nốt NGAY: {', '.join(thieu)}. Cấm dừng để xin ý kiến. Xong in BRAIN_DONE.")
        ok, last = brain_steps.run_creative(d, prof["id"], mn, on_line=on_line, phase="assets",
                                            permission_mode=permission_mode, budget_usd=budget_usd,
                                            extra_prompt=extra)
        _kiem_profile(_kh, on_line)
        thieu = [f for f in need_assets if not (d / f).exists()]
        if not ok and "BRAIN_BLOCKED" in str(last):
            emit(f"✗ bộ não báo script cần sửa ở pha asset ({last}) → quay về sửa script rồi chạy lại"); return False
        if thieu and lan == 1:
            emit(f"⟳ bộ não {'bỏ dở (' + str(last) + ')' if not ok else 'khai xong nhưng THIẾU FILE'} "
                 f"— thiếu: {', '.join(thieu)} → gọi lại 1 lượt")
    if thieu:
        emit(f"✗ vẫn thiếu {', '.join(thieu)} sau 2 lượt → dừng {d.name}"); return False
    # FINGERPRINT (anh chốt 2026-09-18): orchestrator tự tính hash script lúc asset vừa sinh xong —
    # không tin bộ não tự khai. Chỉ stamp khi VỪA sinh asset hoặc chưa có meta; tập đã stamp mà chỉ
    # chạy lại kiểm thì GIỮ meta cũ để rào STALE có tác dụng. Sau đó rào STALE (hash) chặn cứng;
    # mtime chỉ phụ trợ khi thiếu meta.
    if not (d / gate_common.META_NAME).exists() or thieu_truoc_khi_chay:
        try:
            gate_common.ghi_fingerprint(d)
            emit(f"  ✓ stamp fingerprint → {gate_common.META_NAME}")
        except Exception as e:
            emit(f"  ⚠ không stamp được fingerprint: {type(e).__name__} {e}")
    b_stale, w_stale = gate_common.kiem_stale(d)
    for v in w_stale:
        emit(f"  ⚠ {v}")
    if b_stale and not force_lane:
        for v in b_stale:
            emit(f"✗ {v}")
        emit("  → asset bám bản script CŨ: viết lại img_prompts/img_doan theo script hiện tại rồi "
             f"`py -3.13 gate_common.py --slug {d} --stamp`")
        return False
    emit("  ✓ STALE-check: asset khớp hash script hiện tại")

    # CỔNG REF-LOCK — khoá mặt nhân vật (xem check_reflock). Chặn CỨNG: sai chỗ này thì cả loạt ảnh
    # gen ra mặt đổi từng cảnh, tiền mất mà không bước nào báo lỗi.
    dat_rl, loi_rl = check_reflock(d, on_line)
    if not dat_rl and not force_lane:
        emit("⟳ REF-LOCK chưa đạt → gọi bộ não sửa (1 lượt)")
        _kh = _khoa_profile(prof["id"])
        # phase="assets": chỉ sửa characters.json + gen master; cấm đụng script.txt.
        ok, _ = brain_steps.run_creative(
            d, prof["id"], mn, on_line=on_line, permission_mode=permission_mode,
            budget_usd=budget_usd, phase="assets",
            extra_prompt=(
                "⛔ VIỆC DUY NHẤT LƯỢT NÀY: hệ KHOÁ MẶT (REF-LOCK) đang hỏng. Giữ nguyên `script.txt` "
                "và `img_prompts.txt`; chỉ sửa `characters.json` cho ĐÚNG KHUÔN và gen cho đủ ảnh "
                "master:\n   - " + "\n   - ".join(loi_rl) +
                '\nKHUÔN BẮT BUỘC: {"video":…, "world":…, "characters":[{"name":…, "age":…, '
                '"gender":"F"/"M", "master":"_ref/001.png", "look":"<tiếng Anh>"}, …]}  '
                "— `characters` phải là MẢNG, mỗi nhân vật có @REF trong img_prompts phải có một mục "
                "ở đây kèm ảnh master đã gen xong (gen_images.py … --quality low). "
                "Xong in BRAIN_DONE."))
        _kiem_profile(_kh, on_line)
        dat_rl, loi_rl = check_reflock(d, on_line)
    if not dat_rl and not force_lane:
        emit("✗ REF-LOCK vẫn hỏng — DỪNG trước khi gen ảnh (nếu chạy tiếp, mặt nhân vật sẽ đổi từng cảnh):")
        for v in loi_rl[:6]:
            emit(f"   - {v[:160]}")
        return False

    # B5P (prompt ↔ script) + B55 mapping (img_doan ↔ đoạn) — P0. Mode WARN mặc định: phán xét
    # semantic chỉ cảnh báo (đo false-positive 2 tập đầu); exit 1 CHỈ khi lỗi CƠ HỌC chắc chắn
    # (thiếu artifact/malformed/số đoạn không tồn tại/không giảm/STALE) hoặc LLM không chấm được (infra).
    for tool, ten in (("qc_prompt_consistency.py", "B5P"), ("qc_img_doan.py", "B55 mapping")):
        emit(f"[{ten}] {tool} …")
        if not _run(_pycmd(tool, "--slug", str(d)), on_line) and not force_lane:
            emit(f"✗ {ten} RỚT (xem {d / 'logs'}) → sửa rồi chạy lại"); return False

    # CHỐT KIỂM TRA TRƯỚC KHI TIÊU TIỀN: mọi thứ tới đây chỉ ăn quota Claude (miễn phí tiền mặt) —
    # từ render_engine trở đi mới tốn thật (TTS + ~130 ảnh). Cho dừng lại để soi trước.
    # SẢN XUẤT = stop_before_render=True (giao máy 2 → Hermes). Nhánh render_engine dưới chỉ cho
    # test / tập non-hybrid cũ, giữ nguyên để tương thích.
    if stop_before_render:
        emit(f"⏸ DỪNG TRƯỚC RENDER theo yêu cầu — phần chữ đã xong & qua cổng: {d}")
        emit("   (chưa chạy TTS, chưa gen ảnh nào — chưa tốn tiền)")
        return True
    # 🎬 render cơ học (render_engine tự đọc voice.json cho giọng riêng)
    emit(f"[🎬] render {d.name} …")
    ok = _run(_pycmd("render_engine.py", "--slug", str(d), "--profile", prof["id"],
                     "--minutes", str(mn)), on_line)
    if ok and final.exists():
        emit(f"✅ XONG {d.name} → {final}"); return True
    emit(f"✗ render chưa ra final.mp4 ({d.name})"); return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="", help="URL/@handle kênh đối thủ")
    ap.add_argument("--videos", nargs="*", default=[], help="hoặc: liệt kê video_id/URL cụ thể")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--pick", default="", help="STT video muốn làm, cách nhau dấu phẩy (vd 1,3,5). Trống = chỉ quét/in bảng")
    ap.add_argument("--all", action="store_true", help="làm HẾT video quét được")
    ap.add_argument("--minutes", type=float, default=0)
    ap.add_argument("--permission-mode", default="acceptEdits")
    ap.add_argument("--budget", type=float, default=0.0)
    ap.add_argument("--analyze-only", action="store_true",
                    help="CHỈ cào transcript + phân tích giọng (chưa render, chưa tốn tiền) — in dòng VOICE cho GUI")
    ap.add_argument("--force-lane", action="store_true",
                    help="bỏ qua hàng rào lane (gate mượn mặc định / script lệch gate-bằng-số) — CHẤP NHẬN rủi ro")
    a = ap.parse_args()

    prof = profiles.load(a.profile)
    if a.videos:
        handle = prof.get("id", "ch")
        vids = [{"id": channel_scan._handle_of(v) if v.startswith("http") else v,
                 "url": v if v.startswith("http") else f"https://www.youtube.com/watch?v={v}",
                 "title": ""} for v in a.videos]
        data = {"channel_title": "(video chỉ định)", "handle": handle, "videos": vids}
    else:
        if not a.channel:
            raise SystemExit("Cần --channel hoặc --videos")
        data = scan_channel(a.channel, a.limit)
        print(f"KÊNH: {data['channel_title']} (@{data['handle']}) · {len(data['videos'])} video")
        for i, v in enumerate(data["videos"], 1):
            print(f"  {i:>3}  {channel_scan._fmt_views(v['view_count']):>6}  "
                  f"{channel_scan._fmt_dur(v['duration']):>6}  {v['title'][:56]}")
    handle = data["handle"]
    videos = data["videos"]
    if a.all:
        picks = list(range(1, len(videos) + 1))
    elif a.pick:
        picks = [int(x) for x in a.pick.split(",") if x.strip().isdigit()]
    else:
        print("\n→ Chọn video: thêm --pick 1,3,5 hoặc --all để làm.")
        return 0
    if a.analyze_only:
        print(f"\n=== Phân tích giọng {len(picks)} video ===")
        for idx in picks:
            if not (1 <= idx <= len(videos)):
                continue
            _, r = prepare_video(videos[idx - 1], prof, handle, idx)
            if r:
                # dòng máy đọc cho GUI đổ vào cột Giọng
                print(f"VOICE\t{idx}\t{r.get('gender','')}\t{r.get('age_band','')}\t"
                      f"{r.get('voice_name','')}\t{r.get('voice_id','')}")
        print("=== xong phân tích giọng ===")
        return 0
    print(f"\n=== Làm {len(picks)} video: {picks} ===")
    okn = 0
    for k, idx in enumerate(picks, 1):
        if not (1 <= idx <= len(videos)):
            print(f"  bỏ STT {idx} (ngoài danh sách)"); continue
        print(f"\n───── [{k}/{len(picks)}] video #{idx}: {videos[idx-1].get('title','')[:50]} ─────")
        # CLI cũ gọi với stop_before_render mặc định (False → chạy render_engine ở cuối): chỉ dành cho
        # test / tập non-hybrid cũ. Sản xuất hiện tại = bước 1 rồi DỪNG (stop_before_render=True), giao
        # máy 2 → Hermes; GUI/orchestrator truyền tường minh. Không đổi mặc định ở đây để khỏi vỡ caller cũ.
        if make_video_one(videos[idx - 1], prof, handle, idx, a.minutes,
                          permission_mode=a.permission_mode, budget_usd=a.budget,
                          force_lane=a.force_lane):
            okn += 1
    print(f"\n=== XONG {okn}/{len(picks)} video ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
