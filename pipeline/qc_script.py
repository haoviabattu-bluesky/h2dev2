"""qc_script.py — QC NỘI DUNG kịch bản SAU B3, TRƯỚC khi tiêu tiền ảnh (user chốt 2026-09-08).

Gate cũ (`ai_steps.check`) chỉ đo NHỊP + ĐỘ DÀI + ĐỘ SẠCH. Một kịch bản mâu thuẫn (75 tuổi đoạn
đầu → 80 tuổi đoạn giữa), gieo 伏線 không trả, hai khúc kể trùng một cảnh… vẫn "ĐẠT 0 lỗi".
Nguy hiểm nhất là kiến trúc nén THEO KHÚC: 6 khúc nén SONG SONG, mỗi khúc chỉ thấy đuôi khúc
trước → mất chân伏線 / trôi dữ kiện / lặp ý sinh ra đúng ở đây.

HAI TẦNG:
  A. MÁY MÓC (miễn phí, tin 100%): sót chữ nguồn (Hangul/Latin), câu trùng lặp, tuổi/số mâu thuẫn,
     mối nối khúc gãy, đoạn quá dài/ngắn.
  B. LLM (1–2 lượt, JSON schema cứng): bảng dữ kiện nhân vật · 伏線 gieo↔trả · đoạn trùng ý ·
     dấu vết văn hoá nguồn · mạch nối · chất lượng văn · so NHỊP SỰ KIỆN với bản gốc (70/30).

⚠️ BẪY ĐÃ TỪNG DÍNH (dự án thẻ): 503 làm QC bị bỏ qua IM LẶNG mà vẫn báo "0 lỗi" — số 0 ẢO.
   Nên `QcError` (hạ tầng) TÁCH HẲN khỏi phát hiện nội dung; QC không chạy được thì KHÔNG PASS.

Dùng:
  py -3.13 qc_script.py --profile satori-jp-obaa --script <file>
  py -3.13 qc_script.py --profile satori-jp-obaa --script <file> --competitor <file>  # + kiểm 70/30
  py -3.13 qc_script.py ... --json out.json
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import llm_client
import profiles
from qc_numbers import arithmetic

HANGUL = re.compile(r"[가-힣]")
LATIN_WORD = re.compile(r"[A-Za-z]{3,}")
CJK = re.compile(r"[぀-ヿ一-鿿]")
SENT_SPLIT = re.compile(r"(?<=[。！？])")


class QcError(RuntimeError):
    """Hạ tầng hỏng (mạng/model/JSON) — KHÔNG phải lỗi nội dung. Gặp cái này thì KHÔNG được PASS."""


# --------------------------------------------------------------- A. máy móc
def sentences(text, min_len=8):
    return [s.strip() for s in SENT_SPLIT.split(text) if len(s.strip()) >= min_len]


def _bigrams(t):
    t = re.sub(r"[、。！？\s「」]", "", t)
    return {t[i:i + 2] for i in range(len(t) - 1)}


# Từ quá phổ thông, chung nhau không có nghĩa là lặp ý.
_STOP_KANJI = set("私人事時年月日方母父子今前後上下中何思言見出来行気話手目声"
                  "大小長高新古一二三四五六七八九十百千万円")


def _content_words(s):
    return {w for w in re.findall(r"[一-鿿]+", s) if not (len(w) == 1 and w in _STOP_KANJI)}


def _restated(sents, window=3, need=3, min_len=14):
    """Hai câu SÁT NHAU kể lại cùng một việc bằng chữ khác — vết ghép khúc điển hình.
    Chuỗi ký tự KHÔNG bắt được (cặp thật đo ra chỉ 0,38 độ trùng bigram) vì đây là lặp Ý,
    nên dò bằng TỪ NỘI DUNG dùng chung. Đo thật: 1-4 nghi vấn/kịch bản → đủ sạch để cảnh báo."""
    T = [(_content_words(x) if len(x) >= min_len else set()) for x in sents]
    out = []
    for i in range(len(sents)):
        for j in range(i + 1, min(i + 1 + window, len(sents))):
            common = T[i] & T[j]
            if len(common) >= need:
                out.append((i + 1, j + 1, common, sents[i], sents[j]))
    return out


def _near_dupes(sents, window=6, thr=0.62, min_len=14):
    """Cặp câu gần trùng trong phạm vi `window` câu. Jaccard trên bigram ký tự."""
    hits, grams = [], [(_bigrams(x) if len(x) >= min_len else None) for x in sents]
    for i, a in enumerate(grams):
        if not a:
            continue
        for j in range(i + 1, min(i + 1 + window, len(grams))):
            b = grams[j]
            if not b:
                continue
            inter = len(a & b)
            if not inter:
                continue
            sim = inter / len(a | b)
            if sim >= thr:
                hits.append((i + 1, j + 1, sim, sents[i], sents[j]))
    return hits


NEO_SO = re.compile(r"[0-9０-９]+")
NEO_KATA = re.compile(r"[ァ-ヴー]{3,}")


def mo_dau(text, gate, marker="第1章"):
    """Đo PHẦN MỞ ĐẦU (trước chương 1) — đủ dài chưa, đủ CHI TIẾT CỤ THỂ chưa.

    VÌ SAO ĐO "NEO DỮ KIỆN" CHỨ KHÔNG ĐO CẢM GIÁC
    --------------------------------------------------------------------------------------------
    Mở đầu là chỗ người xem quyết định ở lại hay bỏ đi, mà trước 2026-09-11 không cổng nào chạm
    tới nó — `script.gate` không có một dòng nào về mở đầu. Tập 3 lọt một mở đầu 486 chữ trong đó
    11/13 câu không chứa lấy một chi tiết nào: "vì sao suốt bao năm vẫn thu hút lòng người",
    "anh cũng từng một lần tin", "mọi thứ sẽ đổi khác". Chủ dự án xem thấy ngay là lan man, máy
    thì báo ĐẠT.
    Đo bằng **neo dữ kiện** = con số + danh từ riêng katakana trên 1.000 chữ. Đây là thứ đếm
    được, và nó phân biệt đúng thứ cần phân biệt: câu có năm tháng, tên trường, tên nguyên tố là
    câu kể được một việc; câu không có gì là câu nói suông.

    NGƯỠNG ĐO TỪ 4 KÊNH ĐỐI THỦ CỦA CHÍNH LANE NÀY (2026-09-11), xếp theo lượt xem:
        145.972 view →  696 chữ · 24,4 neo/1000     ← 3 video xem nhiều nhất
        124.915 view → 1068 chữ · 21,5 neo/1000        đều nằm trong 20,6–24,4
         98.898 view →  681 chữ · 20,6 neo/1000
         99.312 view →  766 chữ ·  7,8 neo/1000     ← video ít xem nhất, nhạt hẳn
    Mở đầu cũ của tập 3: 486 chữ · 12,3 neo/1000 — dưới cả video yếu nhất của đối thủ.
    """
    # Lane không có 第1章 khai `gate.hook_marker` (1 chuỗi hoặc list, vd ["1つ目","第5位"]) — lấy
    # marker XUẤT HIỆN SỚM NHẤT làm ranh giới mở đầu. Không khai = giữ 第1章 như cũ (2026-09-20).
    marks = gate.get("hook_marker") or marker
    if isinstance(marks, str):
        marks = [marks]
    pos = [text.find(m) for m in marks if text.find(m) > 0]
    if not pos:
        return []
    i = min(pos)
    h = text[:i].strip()
    lo, hi = (gate.get("hook_chars") or [650, 1150])[:2]
    min_neo = float(gate.get("hook_anchor_per_1000") or 18.0)
    neo = len(NEO_SO.findall(h)) + len(NEO_KATA.findall(h))
    mat_do = neo / max(len(h), 1) * 1000
    ra = []
    if len(h) < lo:
        ra.append({"kind": "mo_dau_qua_ngan", "sev": "vua",
                   "msg": f"mở đầu {len(h)} chữ < {lo} (ngưỡng đo từ kênh mẫu của lane này). Mở đầu ngắn không phải "
                          f"gọn — là chưa kịp đưa lý do ở lại."})
    elif len(h) > hi:
        ra.append({"kind": "mo_dau_qua_dai", "sev": "thap",
                   "msg": f"mở đầu {len(h)} chữ > {hi} — vào chuyện quá muộn."})
    if mat_do < min_neo:
        ra.append({"kind": "mo_dau_noi_suong", "sev": "cao",
                   "msg": f"mở đầu chỉ {mat_do:.1f} neo dữ kiện/1000 chữ (cần ≥{min_neo:.0f}, "
                          f"ngưỡng đo từ kênh mẫu của lane này). Đang nói suông — "
                          f"thay câu cảm thán bằng con số, tên riêng, mốc thời gian."})
    return ra


def mechanical(text, lang="ja", gate=None):
    """Các lỗi máy đọc được chắc chắn — không tốn tiền, không cần model."""
    out = list(mo_dau(text, gate or {}))
    body = text.replace("\n", "")

    han = HANGUL.findall(body)
    if han:
        out.append({"kind": "sot_ngon_ngu_nguon", "sev": "cao",
                    "msg": f"còn {len(han)} ký tự Hàn trong bản tiếng Nhật: {''.join(han[:20])}"})

    lat = [w for w in LATIN_WORD.findall(body) if w.lower() not in ("ok", "tv", "dvd", "cd")]
    if lat:
        out.append({"kind": "sot_chu_latin", "sev": "thap",
                    "msg": f"{len(lat)} từ Latin lạ: {', '.join(dict.fromkeys(lat))[:120]}"})

    # câu trùng lặp — dấu hiệu 2 khúc cùng kể 1 cảnh
    ss = sentences(text, 12)
    dup = [(s, c) for s, c in Counter(ss).items() if c > 1]
    if dup:
        out.append({"kind": "cau_trung_lap", "sev": "cao",
                    "msg": f"{len(dup)} câu lặp nguyên văn, vd: 「{dup[0][0][:40]}」×{dup[0][1]}"})

    # câu GẦN GIỐNG nhau trong cùng vùng — vết cắt ghép của nén song song.
    # (câu lặp NGUYÊN VĂN ở trên không bắt được kiểu: "恵が…告白をいたしました。恵は…告白いたしました。")
    near = _near_dupes(ss)
    if near:
        out.append({"kind": "cau_gan_trung", "sev": "cao",
                    "msg": f"{len(near)} cặp câu gần trùng nguyên văn, vd #{near[0][0]}↔#{near[0][1]} "
                           f"({near[0][2]:.0%}): 「{near[0][3][:38]}」/「{near[0][4][:38]}」"})

    rest = _restated(ss)
    if rest:
        out.append({"kind": "lap_y_ke_lai", "sev": "vua",
                    "msg": "; ".join(f"câu {a}↔{b} (chung {'/'.join(sorted(c))[:24]}): 「{x[:26]}」/「{y[:26]}」"
                                     for a, b, c, x, y in rest[:3])})

    # cụm 12 ký tự lặp nhiều lần (lặp ý dù chữ hơi khác)
    grams = Counter(body[i:i + 12] for i in range(0, len(body) - 12, 3))
    rep = [(g, c) for g, c in grams.most_common(8) if c >= 3 and not re.fullmatch(r"[、。\s]+", g)]
    if rep:
        out.append({"kind": "cum_lap", "sev": "thap",
                    "msg": "; ".join(f"「{g}」×{c}" for g, c in rep[:4])})

    # tuổi mâu thuẫn
    ages = Counter(int(m) for m in re.findall(r"(\d{2,3})\s*歳", body) if 1 <= int(m) <= 120)
    if len(ages) > 4:
        out.append({"kind": "nhieu_moc_tuoi", "sev": "thap",
                    "msg": f"{len(ages)} mốc tuổi khác nhau: {sorted(ages)} → soi xem có lệch nhân vật không"})

    # đoạn bất thường
    paras = [p for p in text.split("\n") if p.strip()]
    huge = [i + 1 for i, p in enumerate(paras) if len(p) > 900]
    tiny = [i + 1 for i, p in enumerate(paras) if 0 < len(p) < 40]
    if huge:
        out.append({"kind": "doan_qua_dai", "sev": "thap", "msg": f"đoạn {huge} > 900 chữ"})
    if len(tiny) > 3:
        out.append({"kind": "doan_vun", "sev": "thap", "msg": f"{len(tiny)} đoạn < 40 chữ"})

    out += arithmetic(text)
    return out


# ------------------------------------------------------------------ B. LLM
def _json_only(txt):
    t = re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.MULTILINE).strip()
    m = re.search(r"\{.*\}", t, re.DOTALL)
    if not m:
        raise QcError(f"QC trả về không phải JSON: {t[:200]}")
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise QcError(f"JSON hỏng: {e}") from None


SCHEMA = """{
 "nhan_vat":[{"ten":"","tuoi":"","vai":"","mau_thuan":""}],
 "moc_thoi_gian":[""], "dia_diem":[""], "so_tien":[""],
 "mau_thuan_du_kien":[{"o_dau":"","noi_dung":""}],
 "伏線":[{"gieo":"","tra":"","da_tra":true}],
 "doan_trung_y":[{"a":"","b":"","noi_dung":""}],
 "dau_vet_van_hoa_nguon":[""],
 "mach_noi":[{"vi_tri":"","diem":0,"ly_do":""}],
 "chat_luong_van":{"diem":0,"manh":"","yeu":""},
 "loi_logic":[{"muc":"cao|vua|thap","noi_dung":""}],
 "so_hoc":[{"muc":"cao|vua|thap","cau":"","van_de":"","dung_phai_la":""}],
 "ket_luan":"DAT|SUA|HONG"
}"""


def llm_review(prof, script):
    """Đọc CẢ kịch bản 1 lượt → JSON. Ném QcError nếu hạ tầng hỏng (KHÔNG nuốt)."""
    n = prof.get("narrator", {}) or {}
    prompt = f"""Bạn là biên tập viên khó tính, kiểm tra LOGIC + MẠCH TRUYỆN của một kịch bản
voiceover YouTube (không kiểm chính tả, không kiểm nhịp — cái đó máy đã đo rồi).

NGƯỜI KỂ THEO THIẾT KẾ: {n.get('persona','')} · giới {n.get('gender','')} · tuổi {n.get('age_band','')} · ngôi {n.get('point_of_view','')}
NGÔN NGỮ NGUỒN CẦN XOÁ SẠCH DẤU VẾT: tiếng Hàn (tên riêng, tiền won, phong tục kimjang/설날 gọi theo lối Hàn...)

Kiểm 8 việc:
1. Bảng dữ kiện: mọi nhân vật (tên, tuổi, vai) — ai bị nhắc với 2 giá trị khác nhau thì ghi vào "mau_thuan".
2. Mốc thời gian / địa điểm / số tiền: liệt kê, chỗ nào đá nhau ghi vào "mau_thuan_du_kien".
3. 伏線 (chi tiết gieo trước): cái nào gieo mà KHÔNG trả, hoặc trả mà chưa hề gieo.
4. Hai đoạn kể TRÙNG một cảnh/một ý (kịch bản này được nén theo khúc song song nên rất dễ trùng).
5. Dấu vết văn hoá nguồn còn sót.
6. Mạch nối: kịch bản ghép từ 4-6 khúc — chấm mỗi chỗ chuyển 1-5 điểm, chỗ nào đứt mạch/lặp lại thì nói rõ.
7. Chất lượng văn 1-5: có hay không, có cảm xúc thật không, có sáo rỗng/lặp cấu trúc câu không.
8. Lỗi logic đời thực (tuổi không khớp sự kiện, quan hệ vô lý, thời gian không thể xảy ra).
9. **SỐ HỌC — soi từng con số một** (khán giả ngách kể tài liệu bắt lỗi số rất gắt; một comment
   44 like đã hạ uy tín cả video của đối thủ vì một phép nhân sai). Với MỌI phép tính, quy đổi
   đơn vị, so sánh kích thước/khoảng cách/thời gian trong kịch bản: tự tính lại rồi đối chiếu.
   Ghi vào "so_hoc" mọi chỗ SAI hoặc không thể đúng — kèm "dung_phai_la" là con số đúng.
   Đặc biệt soi: nhân/chia có đơn vị · quy đổi km↔m↔光年 · số năm giữa hai mốc · tuổi theo năm
   sinh · phần trăm cộng quá 100 · so sánh kiểu "gấp N lần <vật quen thuộc>" (kiểm cả giá trị
   thật của vật đó). Số nào ĐÚNG thì đừng ghi vào — danh sách này chỉ chứa lỗi.

"ket_luan": DAT = dùng được ngay · SUA = còn lỗi vừa, nên sửa · HONG = mâu thuẫn nặng, phải viết lại.

CHỈ trả JSON đúng khuôn sau, không thêm chữ nào:
{SCHEMA}

=== KỊCH BẢN ===
{script}"""
    try:
        r = llm_client.chat(prompt, task="script", min_chars=80, verbose=False)
    except llm_client.LLMError as e:
        raise QcError(f"gọi QC thất bại: {e}") from None
    d = _json_only(r.text)
    d["_model"] = f"{r.provider}:{r.model}"
    return d


BEAT_SCHEMA = """{
 "nhip_goc":[""], "nhip_ban_moi":[""],
 "nhip_thieu":[""], "nhip_them_moi":[""],
 "ty_le_bam_goc": 0,
 "sao_chep_nguyen_van":[""],
 "ket_luan":"DAT|LECH_NHIEU|SAO_CHEP"
}"""


def llm_beats(script, competitor):
    """So NHỊP SỰ KIỆN với bản gốc — đo 70/30 bằng khung sự kiện, KHÔNG so câu chữ."""
    prompt = f"""So hai kịch bản theo KHUNG SỰ KIỆN, không so câu chữ.
1. Liệt kê 8-12 nhịp chính của BẢN GỐC theo thứ tự.
2. Liệt kê nhịp chính của BẢN MỚI.
3. Nhịp gốc nào bản mới THIẾU; nhịp nào bản mới TỰ THÊM.
4. "ty_le_bam_goc" = % nhịp gốc được giữ (0-100). Mục tiêu công thức 70/30 là khoảng 60-80.
5. "sao_chep_nguyen_van": câu/đoạn nào dịch sát tới mức coi là sao chép (rủi ro chính sách YouTube).
ket_luan: DAT (60-80% + không sao chép) · LECH_NHIEU (<50% hoặc >90%) · SAO_CHEP.

CHỈ trả JSON đúng khuôn:
{BEAT_SCHEMA}

=== BẢN GỐC (ngôn ngữ nguồn) ===
{competitor[:24000]}

=== BẢN MỚI ===
{script}"""
    try:
        r = llm_client.chat(prompt, task="script", min_chars=60, verbose=False)
    except llm_client.LLMError as e:
        raise QcError(f"gọi QC nhịp thất bại: {e}") from None
    d = _json_only(r.text)
    d["_model"] = f"{r.provider}:{r.model}"
    return d


# ------------------------------------------------------------------- tổng
def run(prof, script, competitor="", do_beats=True):
    """Trả dict {mechanical, review, beats, infra_errors[], verdict}.

    verdict: DAT / SUA / HONG / KHONG_KIEM_DUOC. KHÔNG BAO GIỜ trả DAT khi có infra_errors —
    "0 lỗi" lúc QC không chạy được là SỐ ẢO (bài học dự án thẻ)."""
    res = {"mechanical": mechanical(script, gate=(prof.get("script") or {}).get("gate") or {}),
           "review": None, "beats": None, "infra_errors": []}

    try:
        res["review"] = llm_review(prof, script)
    except QcError as e:
        res["infra_errors"].append(str(e))

    if do_beats and competitor:
        try:
            res["beats"] = llm_beats(script, competitor)
        except QcError as e:
            res["infra_errors"].append(str(e))

    if res["infra_errors"] and not res["review"]:
        res["verdict"] = "KHONG_KIEM_DUOC"
        return res

    hard = [m for m in res["mechanical"] if m["sev"] == "cao"]
    rv = res["review"] or {}
    kl = (rv.get("ket_luan") or "").upper()
    heavy = [l for l in rv.get("loi_logic", []) if (l.get("muc") or "").lower() == "cao"]
    # Số sai không phải lỗi vặt ở ngách kể tài liệu: nó phá đúng thứ cả video đang bán — cảm giác
    # "đã nghiên cứu kỹ". Mức cao ⇒ HỎNG, mức nào cũng ⇒ ít nhất phải SỬA.
    so_hoc = rv.get("so_hoc", []) or []
    so_hoc_nang = [x for x in so_hoc if (x.get("muc") or "").lower() == "cao"]
    unpaid = [f for f in rv.get("伏線", []) if f.get("da_tra") is False]
    bad_seam = [s for s in rv.get("mach_noi", []) if (s.get("diem") or 5) <= 2]
    bk = ((res["beats"] or {}).get("ket_luan") or "").upper()

    if kl == "HONG" or heavy or so_hoc_nang or bk == "SAO_CHEP":
        res["verdict"] = "HONG"
    elif kl == "SUA" or hard or unpaid or bad_seam or so_hoc or bk == "LECH_NHIEU" or \
            (rv.get("chat_luong_van", {}).get("diem") or 5) <= 2:
        res["verdict"] = "SUA"
    else:
        res["verdict"] = "DAT"
    return res


def report(res):
    """In người đọc được. Trả về số vấn đề đáng chú ý."""
    n = 0
    print(f"\n=== QC NỘI DUNG: {res['verdict']} ===")
    if res["infra_errors"]:
        print(f"⚠️ QC KHÔNG CHẠY ĐƯỢC {len(res['infra_errors'])} lượt (lỗi hạ tầng, KHÔNG phải nội dung sạch):")
        for e in res["infra_errors"]:
            print("   !", e[:160])
    if res["mechanical"]:
        print("— máy đo:")
        for m in res["mechanical"]:
            print(f"   [{m['sev']}] {m['kind']}: {m['msg'][:160]}")
            n += m["sev"] == "cao"
    rv = res["review"]
    if rv:
        cv = rv.get("chat_luong_van", {}) or {}
        print(f"— đọc hiểu ({rv.get('_model','?')}): kết luận {rv.get('ket_luan')} · "
              f"văn {cv.get('diem','?')}/5 — mạnh: {str(cv.get('manh',''))[:70]} · yếu: {str(cv.get('yeu',''))[:70]}")
        for c in rv.get("mau_thuan_du_kien", []) or []:
            print(f"   ✗ mâu thuẫn @{c.get('o_dau','')}: {c.get('noi_dung','')[:120]}"); n += 1
        for f in rv.get("伏線", []) or []:
            if f.get("da_tra") is False:
                print(f"   ✗ 伏線 gieo không trả: {str(f.get('gieo',''))[:110]}"); n += 1
        for d in rv.get("doan_trung_y", []) or []:
            print(f"   ✗ trùng ý: {str(d.get('noi_dung',''))[:120]}"); n += 1
        for s in rv.get("mach_noi", []) or []:
            if (s.get("diem") or 5) <= 2:
                print(f"   ✗ mối nối yếu @{s.get('vi_tri','')} ({s.get('diem')}/5): {str(s.get('ly_do',''))[:100]}"); n += 1
        for v in rv.get("dau_vet_van_hoa_nguon", []) or []:
            print(f"   ✗ sót văn hoá nguồn: {str(v)[:110]}"); n += 1
        for l in rv.get("loi_logic", []) or []:
            print(f"   ✗ logic [{l.get('muc')}]: {str(l.get('noi_dung',''))[:130]}"); n += 1
        for x in rv.get("so_hoc", []) or []:
            print(f"   ✗ SỐ HỌC [{x.get('muc')}] 「{str(x.get('cau',''))[:44]}」: "
                  f"{str(x.get('van_de',''))[:80]} → đúng phải là {str(x.get('dung_phai_la',''))[:40]}")
            n += 1
    b = res["beats"]
    if b:
        print(f"— bám gốc 70/30 ({b.get('_model','?')}): giữ {b.get('ty_le_bam_goc','?')}% nhịp · {b.get('ket_luan')}")
        for x in (b.get("nhip_thieu") or [])[:5]:
            print(f"   · thiếu nhịp: {str(x)[:110]}")
        for x in (b.get("sao_chep_nguyen_van") or [])[:3]:
            print(f"   ✗ nghi sao chép: {str(x)[:110]}"); n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--competitor", default="")
    ap.add_argument("--json", default="", help="lưu kết quả thô ra file")
    ap.add_argument("--no-beats", action="store_true")
    args = ap.parse_args()

    prof = profiles.load(args.profile)
    script = Path(args.script).read_text(encoding="utf-8")
    comp = Path(args.competitor).read_text(encoding="utf-8") if args.competitor else ""
    res = run(prof, script, comp, do_beats=not args.no_beats)
    report(res)
    if args.json:
        Path(args.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {args.json}")
    sys.exit(0 if res["verdict"] == "DAT" else 1)


if __name__ == "__main__":
    main()
