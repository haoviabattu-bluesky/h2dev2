# -*- coding: utf-8 -*-
r"""prompt_doan.py — B5W nhánh `image.prompts_by = "fable_doan"`: bộ não (Fable, claude -p) viết prompt ảnh
THEO ĐOẠN kịch bản, một lượt ra cả `img_prompts.txt` (marker @REF/@REF2/@REF12/@GROK) + `img_doan.txt`
(ảnh ↔ số đoạn) để `sinh_neo.py` đặt neo → ảnh hiện đúng lúc câu của nó vang lên.

VÌ SAO CÓ FILE NÀY (anh duyệt phương án 2026-09-20, docs/PHUONG_AN_LANE_G_BUOC2_3.md C1)
- Nhánh B5W cũ (`ai_steps.write_img_prompts`) dựng storyboard TỪ voice.srt → bắt buộc có giọng TRƯỚC ảnh.
  Anh muốn giọng là bước CUỐI (chọn sau khi xem video) → nội dung ảnh phải bám KỊCH BẢN, không bám SRT.
- Satori đã chứng minh: "não ghi MỘT CON SỐ (ảnh thuộc đoạn nào) → máy đặt neo" khớp lời hơn chia đều
  (memory anh-lech-loi-neo-theo-doan). Ở đây gộp luôn vào lúc viết prompt — 1 lượt LLM, không phải 2.
- Fable 0đ (gói), thay Gemini.

ĐẦU VÀO: script.txt (LOCK PASS) · characters.json {"characters":[{name,age,gender,look,ref_marker}]} ·
profile.image (style_suffix, seconds_per_image, blocklist) · voice.char_rate (ước thời lượng, KHÔNG cần audio).
ĐẦU RA: img_prompts.txt · img_doan.txt · artifact_meta.json (fingerprint theo sha script).

KHÔNG sửa script.txt (NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS). Field-driven — lane không khai prompts_by
đi nhánh cũ y nguyên.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claude_p_bridge  # noqa: E402
import gate_common      # noqa: E402
import profiles         # noqa: E402
import sinh_neo         # noqa: E402
from llm_client import LLMError  # noqa: E402

TAGS = ("MAIN", "MENTOR", "BOTH", "NONE", "CHILD")
# gpti2 edit bê cả bối cảnh master → phải nói thẳng "giữ mặt, đổi cảnh" (cùng câu ai_steps đang dùng)
REF_TAIL = ("the SAME person as the reference image with an identical face, but in a COMPLETELY NEW scene: "
            "do not reuse the background, room, furniture or framing of the reference image")
# mỗi ảnh cần ≥ ~4 s lời để neo không dính nhau (sinh_neo đòi ≥1 s, assemble chuyển cảnh 0,5 s)
GIAY_TOI_THIEU_MOI_ANH = 4.0
MAX_HOI_LAI = 1


def _n_anh(prof, script_text):
    chars = len("".join(script_text.split()))
    secs = chars / profiles.char_rate(prof) * 60
    spi = float((prof.get("image", {}) or {}).get("seconds_per_image", 14) or 14)
    return max(20, int(round(secs / spi))), secs


def _tran_anh_moi_doan(doan, prof):
    """Số ảnh tối đa mỗi đoạn để mỗi ảnh còn ≥ GIAY_TOI_THIEU_MOI_ANH giây lời."""
    cr = profiles.char_rate(prof) / 60.0          # chữ / giây
    return [max(1, int(len("".join(d.split())) / (cr * GIAY_TOI_THIEU_MOI_ANH))) for d in doan]


def _la_cast(chars):
    """characters.json kiểu MỚI (Lane K, 2026-09-24): {id, ref} không ref_marker → khoá mặt N nhân vật."""
    return bool(chars) and all("id" in c and "ref" in c and not c.get("ref_marker") for c in chars)


def _doc_characters(d: Path):
    f = d / "characters.json"
    if not f.exists():
        raise SystemExit(f"✗ B5W(fable_doan): thiếu {f} — lớp 1 phải viết hồ sơ nhân vật trước (name/age/gender/look/ref_marker)")
    data = json.loads(f.read_text(encoding="utf-8"))
    chars = data.get("characters") or []
    if _la_cast(chars):
        return None, None, chars
    main = next((c for c in chars if c.get("ref_marker") == "@REF"), None)
    mentor = next((c for c in chars if c.get("ref_marker") == "@REF2"), None)
    if not main:
        raise SystemExit("✗ characters.json: cần 1 nhân vật ref_marker=\"@REF\" (nhân vật chính 俺)")
    return main, mentor, chars


def _tate_note(prof):
    """C5 (docs/PHUONG_AN_LANE_F_BUOC2_3.md): lane khai assemble.tate.enabled → dặn Fable chừa 1
    bên khung trống cho hộp chữ dọc 縦書き (tate_text.py overlay sau, KHÔNG phải model tự vẽ chữ).
    Lane không khai → chuỗi rỗng, không đổi hành vi."""
    tt = (prof.get("assemble", {}) or {}).get("tate") or {}
    if not tt.get("enabled"):
        return ""
    ben = "LEFT" if (tt.get("side") or "left").lower() != "right" else "RIGHT"
    return (f" Keep the {ben} third of the frame visually simple and uncluttered (no face, no busy "
            f"detail there) — a vertical text caption box will be overlaid there afterwards.")


def _prompt(prof, doan, n, main, mentor, tran, others=()):
    img = prof.get("image", {}) or {}
    style = img.get("style_suffix", "")
    block = ", ".join(prof.get("blocklist") or []) or "gore, nudity, babies"
    tate = _tate_note(prof)
    ds = "\n".join(f"[{i}] ({tran[i-1]} max) {p}" for i, p in enumerate(doan, 1))
    men = (f"MENTOR (tag MENTOR): '{mentor.get('look')}'" if mentor else "MENTOR: (none in this episode — never use tag MENTOR/BOTH)")
    # Nhân vật lặp lại KHÔNG khoá mặt (vợ, bạn cũ...): không có master REF nên tag NONE, nhưng vẫn bắt Fable dùng
    # cùng một mô tả mỗi lần xuất hiện — kẻo vợ 62 tuổi tập này ra 5 khuôn mặt khác nhau (ep05 Lane G, 2026-09-21).
    kh = "".join(f"OTHER RECURRING PERSON (no face lock → tag NONE, prefer from behind/side/far, but ALWAYS reuse this "
                 f"exact description): {c.get('name')} — '{c.get('look')}'" + chr(10)
                 for c in others if c.get("look"))
    return (
        "You write image prompts for an AI image generator, for a narrated Japanese manga-style story video.\n"
        f"The script below is split into {len(doan)} numbered paragraphs. Each paragraph shows in parentheses the MAXIMUM "
        f"number of images it may receive (a hard cap — the narration is too short for more).\n"
        f"Write EXACTLY {n} lines total, in paragraph order (paragraph numbers must never decrease), covering the story "
        f"from the first paragraph to the last; every paragraph with real action or a new place should get at least one "
        f"image, short transitional paragraphs may get zero.\n\n"
        "LINE FORMAT (strict, no numbering, no markdown, no blank lines):\n"
        "<paragraph number>|<TAG>|<English prompt 25-45 words starting with WIDE/MEDIUM/CLOSE-UP/DETAIL>\n"
        "TAG is exactly one of: MAIN (the narrator's face is clearly visible), MENTOR (the mentor's face is visible, "
        "narrator not visible), BOTH (both faces visible in one frame), NONE (scenery / objects / hands / people from "
        "behind or far away — no recognisable face), CHILD (any child or baby visible).\n"
        f"MAIN CHARACTER (tag MAIN): '{main.get('look')}'\n{men}\n{kh}"
        "Rules: when a tagged person appears, describe them with the SAME wording as above (age, hair, glasses, clothes). "
        "Prefer NONE for wide establishing shots and objects (cheaper), use MAIN/MENTOR/BOTH for emotional beats and dialogue. "
        f"Keep faces to at most 40% of all lines. Do NOT put any text, letters, numbers, signs or speech bubbles in the image. "
        f"Never depict: {block}.{tate}\n"
        f"Every prompt must END with this exact style suffix: '{style}'.\n\n"
        f"SCRIPT PARAGRAPHS:\n{ds}")


# ------------------------------------------------ nhánh CAST (khoá mặt N nhân vật/tập — Lane K 2026-09-24)
def _prompt_cast(prof, doan, n, chars, tran):
    img = prof.get("image", {}) or {}
    style = img.get("style_suffix", "")
    block = ", ".join(prof.get("blocklist") or []) or "gore, nudity, babies"
    toi_da = int(img.get("cast_max_per_image", 3))
    ds = "\n".join(f"[{i}] ({tran[i-1]} max) {p}" for i, p in enumerate(doan, 1))
    khoa = "\n".join(f"- {c['id']}: {c.get('name','')} ({c.get('vai','')}) — '{c.get('look')}'" for c in chars if c.get("ref"))
    tu_do = "".join(f"- (no face lock, tag NONE when only they appear) {c.get('name','')}: '{c.get('look')}'\n"
                    for c in chars if not c.get("ref") and c.get("look"))
    return (
        "You write image prompts for an AI image generator, for a narrated Japanese workplace manga story video "
        "(a small Japanese pharmacy). Several recurring characters have LOCKED faces (listed below by id).\n"
        f"The script below is split into {len(doan)} numbered paragraphs. Each paragraph shows in parentheses the MAXIMUM "
        f"number of images it may receive (hard cap).\n"
        f"Write EXACTLY {n} lines total, in paragraph order (paragraph numbers must never decrease), covering the story "
        f"from the first paragraph to the last; every paragraph with real action or dialogue should get at least one image.\n\n"
        "LINE FORMAT (strict, no numbering, no markdown, no blank lines):\n"
        "<paragraph number>|<CAST>|<English prompt 25-45 words starting with WIDE/MEDIUM/CLOSE-UP/DETAIL>\n"
        f"CAST = comma-separated ids of the locked characters whose FACE is clearly visible (1 to {toi_da} ids, e.g. "
        "shu,tencho), or NONE (no recognisable locked face: building exterior, objects, hands, people from behind), or CHILD "
        "(a child is visible).\n"
        f"LOCKED CHARACTERS:\n{khoa}\n{tu_do}"
        "Rules: describe every listed person with the SAME wording as above (age, hair, glasses, uniform) each time. "
        "When a paragraph contains a spoken line, show the SPEAKER's face (and the listener if it fits) — the viewer must "
        f"see who talks. Never more than {toi_da} locked faces in one image; extra people must be from behind or far away. "
        "Leave some open space beside the speaker's head (a speech balloon is added later). "
        "Do NOT put any text, letters, numbers, signs or speech bubbles in the image. "
        f"Never depict: {block}.\n"
        f"Every prompt must END with this exact style suffix: '{style}'.\n\n"
        f"SCRIPT PARAGRAPHS:\n{ds}")


def _parse_cast(text, n_doan, chars, toi_da):
    ids_ok = {c["id"] for c in chars if c.get("ref")}
    rows, loi = [], []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"^\s*\[?(\d+)\]?\s*\|\s*([A-Za-z0-9_,\-\s]+)\s*\|\s*(.+)$", s)
        if not m:
            loi.append(f"dòng không đúng khuôn: {s[:80]}")
            continue
        d, tag, p = int(m.group(1)), re.sub(r"\s", "", m.group(2)), m.group(3).strip()
        if tag.upper() in ("NONE", "CHILD"):
            tag = tag.upper()
        else:
            ids = [x for x in tag.split(",") if x]
            la = [x for x in ids if x not in ids_ok]
            if la:
                loi.append(f"id lạ {la}: {s[:60]}")
            if len(ids) > toi_da:
                loi.append(f"{len(ids)} mặt khoá > tối đa {toi_da}: {s[:60]}")
            tag = ",".join(ids)
        if not 1 <= d <= n_doan:
            loi.append(f"số đoạn {d} ngoài 1..{n_doan}: {s[:60]}")
        if len(p.split()) < 12:
            loi.append(f"prompt quá ngắn: {s[:60]}")
        rows.append((d, tag, p))
    return rows, loi


def _kiem_cast(rows, n, tran, face_max):
    loi = []
    if len(rows) != n:
        loi.append(f"cần ĐÚNG {n} dòng, nhận {len(rows)}")
    for i in range(1, len(rows)):
        if rows[i][0] < rows[i - 1][0]:
            loi.append(f"số đoạn giảm ở dòng {i+1}: {rows[i-1][0]} → {rows[i][0]}")
            break
    dem = {}
    for d, _, _ in rows:
        dem[d] = dem.get(d, 0) + 1
    loi += [f"đoạn {d}: {c} ảnh > trần {tran[d-1]}" for d, c in dem.items() if 1 <= d <= len(tran) and c > tran[d - 1]][:8]
    face = sum(1 for _, t, _ in rows if t not in ("NONE", "CHILD"))
    if rows and face / len(rows) > face_max:
        loi.append(f"quá nhiều cảnh thấy mặt: {face}/{len(rows)} (> {face_max:.0%})")
    return loi


def _ghi_cast(d: Path, rows, prof):
    style = (prof.get("image", {}) or {}).get("style_suffix", "")
    prompts, doan_lines = [], []
    tail = REF_TAIL.replace("the SAME person as the reference image", "the SAME people as the reference images, each face identical")
    for i, (dn, tag, p) in enumerate(rows, 1):
        p = p.rstrip(" .")
        if style and style.lower() not in p.lower():
            p = f"{p}, {style}"
        if tag == "CHILD":
            line = f"@GROK {p}"
        elif tag == "NONE":
            line = p
        else:
            line = f"@CAST:{tag} {p}, {tail}"
        prompts.append(line)
        doan_lines.append(f"{i:03d}.png|{dn}")
    (d / "img_prompts.txt").write_text("\n".join(prompts) + "\n", encoding="utf-8")
    (d / "img_doan.txt").write_text("\n".join(doan_lines) + "\n", encoding="utf-8")
    gate_common.ghi_fingerprint(d)
    return prompts


def viet_cast(prof, d, doan, chars, n, tran):
    img = prof.get("image", {}) or {}
    toi_da = int(img.get("cast_max_per_image", 3))
    face_max = float(img.get("face_ratio_max", 0.85))
    print(f"[B5W] fable_doan CAST: {len(doan)} đoạn · {n} ảnh · khoá mặt {sum(1 for c in chars if c.get('ref'))} "
          f"nhân vật · ≤{toi_da} mặt/ảnh")
    prompt = _prompt_cast(prof, doan, n, chars, tran)
    model = claude_p_bridge.brain_model_of(prof)
    rows, loi = [], []
    (d / "logs").mkdir(exist_ok=True)
    for luot in range(MAX_HOI_LAI + 1):
        q = prompt if not loi else (prompt + "\n\nYOUR PREVIOUS ANSWER WAS REJECTED — fix ALL of these and return the "
                                    "full list again:\n- " + "\n- ".join(loi[:12]))
        try:
            r = claude_p_bridge.ask(q, model=model, timeout=1500, min_chars=n * 30)
        except LLMError as e:
            raise SystemExit(f"✗ B5W(fable_doan): claude -p lỗi: {e}")
        (d / "logs" / f"B5W_raw_attempt{luot + 1}.txt").write_text(r.text, encoding="utf-8")
        rows, loi = _parse_cast(r.text, len(doan), chars, toi_da)
        loi += _kiem_cast(rows, n, tran, face_max)
        print(f"   lượt {luot+1}: {len(rows)} dòng · {r.elapsed:.0f}s" + (f" · {len(loi)} lỗi" if loi else " · hợp lệ"))
        if not loi:
            break
        for x in loi[:6]:
            print("     -", x)
    if loi:
        raise SystemExit(f"✗ B5W(fable_doan): sau {MAX_HOI_LAI+1} lượt vẫn {len(loi)} lỗi khuôn → BLOCK (không tự vá tay).")
    prompts = _ghi_cast(d, rows, prof)
    face = sum(1 for _, t, _ in rows if t not in ("NONE", "CHILD"))
    print(f"[B5W] ghi img_prompts.txt + img_doan.txt: {len(prompts)} ảnh · thấy mặt {face} · NONE "
          f"{sum(1 for _, t, _ in rows if t == 'NONE')} · CHILD {sum(1 for _, t, _ in rows if t == 'CHILD')}")
    return len(prompts), {"FACE": face}


def _parse(text, n_doan):
    rows, loi = [], []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"^\s*\[?(\d+)\]?\s*\|\s*([A-Z]+)\s*\|\s*(.+)$", s)
        if not m:
            loi.append(f"dòng không đúng khuôn: {s[:80]}")
            continue
        d, tag, p = int(m.group(1)), m.group(2).upper(), m.group(3).strip()
        if tag not in TAGS:
            loi.append(f"tag lạ {tag!r}: {s[:60]}")
        if not 1 <= d <= n_doan:
            loi.append(f"số đoạn {d} ngoài 1..{n_doan}: {s[:60]}")
        if len(p.split()) < 12:
            loi.append(f"prompt quá ngắn: {s[:60]}")
        rows.append((d, tag, p))
    return rows, loi


def _kiem(rows, n, tran, mentor):
    loi = []
    if len(rows) != n:
        loi.append(f"cần ĐÚNG {n} dòng, nhận {len(rows)}")
    for i in range(1, len(rows)):
        if rows[i][0] < rows[i - 1][0]:
            loi.append(f"số đoạn giảm ở dòng {i+1}: {rows[i-1][0]} → {rows[i][0]}")
            break
    dem = {}
    for d, _, _ in rows:
        dem[d] = dem.get(d, 0) + 1
    qua = [f"đoạn {d}: {c} ảnh > trần {tran[d-1]}" for d, c in dem.items() if 1 <= d <= len(tran) and c > tran[d - 1]]
    loi += qua[:8]
    if not mentor and any(t in ("MENTOR", "BOTH") for _, t, _ in rows):
        loi.append("dùng tag MENTOR/BOTH nhưng tập không khai mentor")
    face = sum(1 for _, t, _ in rows if t in ("MAIN", "MENTOR", "BOTH"))
    if rows and face / len(rows) > 0.5:
        loi.append(f"quá nhiều cảnh thấy mặt: {face}/{len(rows)} (> 50%) — đổi cảnh xa/đồ vật sang NONE")
    return loi


def _ghi(d: Path, rows, prof):
    style = (prof.get("image", {}) or {}).get("style_suffix", "")
    prompts, doan_lines = [], []
    for i, (dn, tag, p) in enumerate(rows, 1):
        p = p.rstrip(" .")
        if style and style.lower() not in p.lower():
            p = f"{p}, {style}"
        if tag == "MAIN":
            line = f"@REF {p}, {REF_TAIL}"
        elif tag == "MENTOR":
            line = f"@REF2 {p}, {REF_TAIL}"
        elif tag == "BOTH":
            line = f"@REF12 {p}, {REF_TAIL.replace('the SAME person', 'the SAME two people')}"
        elif tag == "CHILD":
            line = f"@GROK {p}"
        else:
            line = p
        prompts.append(line)
        doan_lines.append(f"{i:03d}.png|{dn}")
    (d / "img_prompts.txt").write_text("\n".join(prompts) + "\n", encoding="utf-8")
    (d / "img_doan.txt").write_text("\n".join(doan_lines) + "\n", encoding="utf-8")
    gate_common.ghi_fingerprint(d)
    return prompts


def viet(prof, slug_dir):
    """Trả (số prompt, thống kê). Ném SystemExit khi Fable không ra bản hợp lệ sau MAX_HOI_LAI lượt hỏi lại."""
    d = Path(slug_dir)
    script = (d / "script.txt").read_text(encoding="utf-8")
    doan = sinh_neo.doc_doan(d / "script.txt")
    main, mentor, chars = _doc_characters(d)
    n, secs = _n_anh(prof, script)
    tran = _tran_anh_moi_doan(doan, prof)
    if sum(tran) < n:
        n = sum(tran)          # kịch bản nhiều đoạn ngắn → hạ số ảnh, không ép nhồi
    if main is None:           # characters.json kiểu CAST (N nhân vật khoá mặt)
        return viet_cast(prof, d, doan, chars, n, tran)
    print(f"[B5W] fable_doan: {len(doan)} đoạn · ≈{secs/60:.1f}' · {n} ảnh · nhân vật: {main.get('name')}"
          + (f" + {mentor.get('name')}" if mentor else " (không mentor)"))
    others = [c for c in chars if c.get("ref_marker") not in ("@REF", "@REF2")]
    prompt = _prompt(prof, doan, n, main, mentor, tran, others)
    model = claude_p_bridge.brain_model_of(prof)
    rows, loi = [], []
    for luot in range(MAX_HOI_LAI + 1):
        q = prompt if not loi else (prompt + "\n\nYOUR PREVIOUS ANSWER WAS REJECTED — fix ALL of these and return the "
                                    "full list again:\n- " + "\n- ".join(loi[:12]))
        try:
            r = claude_p_bridge.ask(q, model=model, timeout=1500, min_chars=n * 30)
        except LLMError as e:
            raise SystemExit(f"✗ B5W(fable_doan): claude -p lỗi: {e}")
        # Lưu bản thô MỌI lượt (kể cả lượt hỏng) — trước đây chỉ ghi khi thành công nên lượt hỏng
        # KHÔNG có gì để soi lại tại sao (đo thật ep01 teinengo-real 2026-09-21: BLOCK sau 2 lượt mà
        # không biết model trả gì). logs/ đã tồn tại từ B55 (qc_img_doan) nên mkdir an toàn ở đây.
        logdir = d / "logs"
        logdir.mkdir(exist_ok=True)
        (logdir / f"B5W_raw_attempt{luot + 1}.txt").write_text(r.text, encoding="utf-8")
        rows, loi = _parse(r.text, len(doan))
        loi += _kiem(rows, n, tran, mentor)
        print(f"   lượt {luot+1}: {len(rows)} dòng · {r.elapsed:.0f}s" + (f" · {len(loi)} lỗi" if loi else " · hợp lệ"))
        if not loi:
            break
        for x in loi[:6]:
            print("     -", x)
    if loi:
        raise SystemExit(f"✗ B5W(fable_doan): sau {MAX_HOI_LAI+1} lượt vẫn {len(loi)} lỗi khuôn → BLOCK (không tự vá tay).")
    prompts = _ghi(d, rows, prof)
    tk = {t: sum(1 for _, x, _ in rows if x == t) for t in TAGS}
    print(f"[B5W] ghi img_prompts.txt + img_doan.txt: {len(prompts)} ảnh · MAIN {tk['MAIN']} · MENTOR {tk['MENTOR']} · "
          f"BOTH {tk['BOTH']} · NONE {tk['NONE']} · CHILD {tk['CHILD']} · đoạn có ảnh {len({r[0] for r in rows})}/{len(doan)}")
    return len(prompts), tk


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True, help="thư mục tập")
    a = ap.parse_args()
    viet(profiles.load(a.profile), a.slug)
