"""ai_steps.py — 3 bước SÁNG TẠO (thay Claude): viết kịch bản · viết prompt ảnh · viết chữ thumbnail.

Mọi tham số nhân vật/nhịp/ảnh lấy từ PROFILE (`profiles.py`) — không hằng số ẩn, nên đổi kênh
(cụ bà tâm tình → võ tướng ầm vang) chỉ là đổi `--profile`.

Kiến trúc bước script = **2 PASS** (đo thật 2026-09-07, `docs/AB_SCRIPT_MODELS.md`):
  PASS 1  viết bản giàu chi tiết (gemini bỏ ngoài tai mọi chỉ tiêu số chữ → luôn dài ~1,7 lần)
  PASS 2  nén về đúng target_chars + ÉP nhịp (phẩy/câu, tỉ lệ hội thoại, câu hé tập sau)
  GATE    đếm chữ · marker · ngôn ngữ · nhịp · phải kết bằng dấu câu → chưa đạt thì nén thêm (≤2 lượt)

Dùng (test từng bước trên tập đã có):
  py -3.13 ai_steps.py script  --profile satori-jp-obaa --competitor ../assets/satori_jp/ep3-sougi/competitor.txt --out /tmp/s.txt
  py -3.13 ai_steps.py imgs    --profile satori-jp-obaa --script ../assets/satori_jp/ep3-sougi/script.txt --n 40 --out /tmp/p.txt
  py -3.13 ai_steps.py thumb   --profile satori-jp-obaa --script ../assets/satori_jp/ep3-sougi/script.txt
  py -3.13 ai_steps.py measure --profile satori-jp-obaa --script ../assets/satori_jp/ep3-sougi/script.txt
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import profiles
from llm_client import chat, LLMError

from paths import res, OUT_ROOT


def _writer_chat(prof, prompt, **kwargs):
    """'Não viết' của B3 — Gemini (mặc định) hoặc Claude qua `claude -p` khi profile khai
    `script.engine = "claude_p"` (field-driven — xem CLAUDE.md hàng rào #2, cấm `if profile_id==`).
    CHỈ áp cho lượt THỰC SỰ SÁNG TẠO (PASS 0 bóc khung + PASS 1 viết nháp) — nén khúc/hội thoại/
    phẩy và MỌI QC (`qc_script.py`, `qc_facts.py`) vẫn luôn Gemini dù engine là gì, đúng tinh thần
    "Claude viết — Gemini chấm độc lập" (satori cũng vậy: `qc_script.py` bên đó là Gemini, không
    phải Claude tự chấm bài mình). Xem `claude_p_bridge.py` để biết lý do kiến trúc."""
    if (prof.get("script", {}) or {}).get("engine") == "claude_p":
        import claude_p_bridge
        keep = {k: v for k, v in kwargs.items()
                if k in ("system", "model", "timeout", "min_chars", "require_sentence_end", "max_chars")}
        keep.setdefault("model", claude_p_bridge.brain_model_of(prof))
        return claude_p_bridge.ask(prompt, **keep)
    return chat(prompt, **kwargs)
ROOT = OUT_ROOT
LANG_NAME = {"ja": "Japanese (日本語)", "ko": "Korean (한국어)", "en": "English"}

# Marker/rác tuyệt đối không được lọt vào bản đọc (narrator sẽ đọc cả marker).
# ⚠️ 停止/続けて là TỪ TIẾNG NHẬT BÌNH THƯỜNG (「続けてきた」…) → chỉ tính là marker khi nằm trong
# 「」 hoặc đứng một mình cả dòng. Không có luật này thì gate báo sai mọi kịch bản tốt.
MARKER_PAT = re.compile(r"(「\s*(?:パート\s*\d+|停止|続けて)\s*」|^\s*(?:停止|続けて)\s*$|"
                        r"パート\s*\d+\s*[:：]|脚本完成|SCRIPT COMPLETED|IMAGE PROMPTS READY|"
                        r"^#{1,6}\s|\*\*|:::|^\s*\d+[\.、)]\s|【|】|\[[^\]]{0,40}\])",
                        re.MULTILINE)


# ============================================================ ĐO & GATE
# Dấu 、 CẮT CỤM động từ/ngữ pháp — tất định, 0 LLM. Bài học 2026-09-18 (STT10, sol lens #6): cổng số
# chỉ ĐẾM 、 (chars_per_breath 4,5–9) nên fix_gate/gemini nhét 、 vào giữa て+trợ động từ để đủ mật độ:
# 「塞いで、まいりました」「語らせて、いただきます」「挟まれていたので、ございます」 — không ai đọc mà
# ngắt hơi ở đó, TTS đọc nghe gãy. Đo lại: STT9 32+61 chỗ, STT7/11 (đã đăng) 13+16 / 13+20.
CAT_CUM_PATS = [
    # て/で + trợ động từ (まいる/いただく/おる/おく/くる/くれる/しまう/いく/ゆく/みる/ある/いる/ほしい/ください)
    re.compile(r"([てで])、(?=まい|いただ|おり|おる|おき|おく|おい|くる|きた|きて|くれ|くだ|しま|いき|いく|いっ|ゆ|み|あり|ある|あっ|い[たるて]|ほし)"),
    # 「〜ので、ございます」 / 「〜た、のでございます」 / 「〜て、ございます」 (「が、ございます」 giữ — ngắt sau trợ từ)
    re.compile(r"(ので|[たてでる])、(?=ございま)"),
    re.compile(r"([たるうくすつぬぶむぐいで])、(?=ので(?:ございま|す|した|しょう))"),
    # động từ + 、+ こと (danh hoá) : 「気をつける、ことがある」
    re.compile(r"([たるうくすつぬぶむぐ])、(?=こと[がをもにでは]|ことでした|ことです)"),
    # 「させて、いただ」 đã nằm ở mẫu 1; 「〜に、なる」 bỏ qua (ngắt sau trợ từ là chấp nhận được)
]


def dem_cat_cum(text):
    """Số dấu 、 đặt sai chỗ (cắt cụm động từ / のでございます / こと)."""
    return sum(len(p.findall(text)) for p in CAT_CUM_PATS)


def go_cat_cum(text):
    """Gỡ các dấu 、 sai chỗ (CHỈ xoá 、, không đổi chữ nào). Trả (text_mới, số_đã_gỡ)."""
    n = 0
    for p in CAT_CUM_PATS:
        text, k = p.subn(r"\1", text)
        n += k
    return text, n


def _go_cat_neu_ja(prof, text):
    """Gỡ TẤT ĐỊNH dấu 、 cắt cụm (chỉ xoá 、) cho lane tiếng Nhật — chạy ngay trong vòng B3.
    Bài học 2026-09-20 (Lane G ep01): `check()` báo "NHỊP SAI CHỖ: 1 dấu 、 … fix_gate.py tự gỡ" nhưng
    write_script KHÔNG gọi go_cat_cum → nhờ Gemini viết lại khúc vì 1 ký tự, làm tệ hơn, rồi VỨT bản
    7.005 chữ đã đạt mọi thứ khác và viết lại từ đầu. Lỗi 1 ký tự tất định thì máy xoá, không hỏi LLM."""
    if prof.get("language", "ja") != "ja":
        return text
    moi, k = go_cat_cum(text)
    if k:
        print(f"  · gỡ tất định {k} dấu 、 cắt cụm (go_cat_cum)")
    return moi


def measure(text, char_rate=309.0):
    body = text.replace("\n", "").replace(" ", "").replace("\u3000", "")
    n = len(body)
    sents = [s for s in re.split(r"[。．.!?！？]", text) if s.strip()]
    ns = max(len(sents), 1)
    commas = text.count("、")
    quote = sum(len(m) for m in re.findall(r"「[^」]*」", text))
    return {
        "chars": n,
        "minutes": round(n / char_rate, 1) if char_rate else 0,
        "sentences": len(sents),
        "chars_per_sentence": round(n / ns, 1),
        # chữ giữa 2 lần ngắt hơi (dấu phẩy HOẶC hết câu) = thước đo NHỊP THỞ thật sự.
        # Đo thật: bản Claude đã lên video 5,6 · bản nén tốt 7,4 · bản dài lê thê 14,5.
        "chars_per_breath": round(n / max(ns + commas, 1), 1),
        "comma_per_sentence": round(commas / ns, 2),
        "dialogue_ratio": round(quote / max(n, 1), 3),
        "markers": sorted(set(m[0] if isinstance(m, tuple) else m
                              for m in MARKER_PAT.findall(text)))[:6],
        "hangul": sum(1 for c in body if "\uac00" <= c <= "\ud7a3"),
        "latin": sum(1 for c in body if "a" <= c.lower() <= "z"),
        "ends_ok": bool(text.strip()) and text.strip()[-1] in "。．.!?！？」』",
    }


def check(prof, text, minutes=None, tol=0.12):
    """Trả list vấn đề (rỗng = đạt). Ngưỡng lấy từ profile, KHÔNG phải hằng số."""
    g = profiles.gate(prof)
    rate = profiles.char_rate(prof)
    target = profiles.target_chars(prof, minutes)
    m = measure(text, rate)
    bad = []
    if m["chars"] > target * (1 + tol):
        bad.append(f"DÀI: {m['chars']:,} chữ ({m['minutes']}') > mục tiêu {target:,} (+{tol:.0%})")
    if m["chars"] < target * (1 - tol):
        bad.append(f"NGẮN: {m['chars']:,} chữ ({m['minutes']}') < mục tiêu {target:,} (−{tol:.0%})")
    lo, hi = g["comma_per_sentence"]
    if not lo <= m["comma_per_sentence"] <= hi:
        bad.append(f"NHỊP: {m['comma_per_sentence']} phẩy/câu, cần {lo}–{hi}")
    if g.get("chars_per_breath"):
        lo, hi = g["chars_per_breath"]
        if not lo <= m["chars_per_breath"] <= hi:
            bad.append(f"HƠI: {m['chars_per_breath']} chữ/nhịp thở, cần {lo}–{hi}")
    if m["dialogue_ratio"] > g["dialogue_ratio_max"]:
        bad.append(f"HỘI THOẠI: {m['dialogue_ratio']:.0%} > tối đa {g['dialogue_ratio_max']:.0%}")
    if prof.get("language", "ja") == "ja":
        k = dem_cat_cum(text)
        if k:
            bad.append(f"NHỊP SAI CHỖ: {k} dấu 、 cắt cụm động từ/のでございます/こと — fix_gate.py tự gỡ (go_cat_cum)")
    if m["markers"]:
        bad.append(f"MARKER lọt vào bản đọc: {m['markers']}")
    if prof.get("language") == "ja" and m["hangul"]:
        bad.append(f"SÓT tiếng Hàn: {m['hangul']} ký tự (chưa Nhật hoá hết)")
    if m["latin"] > m["chars"] * 0.02:
        bad.append(f"LATIN nhiều: {m['latin']} ký tự")
    if not m["ends_ok"]:
        bad.append("CẮT GIỮA CÂU (không kết bằng dấu câu)")
    bad += _gate_ngach(prof, text, m, g, rate)
    return bad, m


def _gate_ngach(prof, text, m, g, rate):
    """Gate RIÊNG của ngách kể tài liệu — chỉ chạy khi profile khai các ngưỡng này.

    Bốn con số dưới đây là thứ phân biệt một video "nghe như đã nghiên cứu kỹ" với một bài đọc
    Wikipedia. Không khai thì không kiểm — kênh satori chạy qua đây không đổi hành vi.

    ⚠️ NGƯỠNG LẤY TỪ PHÂN BỐ THẬT, KHÔNG ĐOÁN. Bản đầu em đặt theo câu chữ trong tài liệu bàn
    giao ("しかし mỗi ≤90 giây") và nó CHẶT HƠN CẢ KÊNH MẪU → đánh trượt hai bản kịch bản tốt.
    Đo lại chính 4 transcript đối thủ (2026-09-10, tính theo mốc thời gian thật của cue):

        video          phút   đảo chiều/phút   gap lớn nhất   gap p90   lá chắn/10'   neo/phút
        OU1r2W68F0Y    66,6        0,74           351s         179s        1,4          1,55
        GTwoNSPbEv8    51,2        1,01           200s         101s        5,1          2,23
        saIym-x8dPc    75,8        0,66           307s         176s        3,4          1,11
        HqaY3BLROJU    58,4        0,55           560s         222s        3,8          0,87

    ⇒ "≤90 giây" là mô tả CẢM GIÁC nhịp, không phải trần thật. Trần thật nên đặt ~300s (giữa p90
    và gap xấu nhất), kèm ràng buộc MẬT ĐỘ ≥0,5 lần/phút — hai cái đi cùng mới chặn được kiểu
    "dồn cục 20 lần rồi im 6 phút". Lá chắn: sàn 2,0/10 phút (video thấp nhất của họ là 1,4).
    """
    bad, body = [], text.replace("\n", "")
    if g.get("chapter_markers"):
        thieu = [c for c in g["chapter_markers"] if c not in body]
        if thieu:
            bad.append(f"THIẾU CHƯƠNG: {', '.join(thieu)}")
    if (g.get("reversal_max_gap_sec") or g.get("reversal_per_min")) and rate:
        moc = [mm.start() for mm in re.finditer(r"しかし|だが|ところが|けれど", body)]
        phut = len(body) / rate
        khe = [0] + moc + [len(body)]
        rong = max((khe[i + 1] - khe[i]) for i in range(len(khe) - 1)) if len(khe) > 1 else len(body)
        if g.get("reversal_max_gap_sec") and rong > rate * g["reversal_max_gap_sec"] / 60:
            bad.append(f"ĐỨT NHỊP ĐẢO CHIỀU: có khoảng {int(rong)} chữ (~{rong/rate*60:.0f}s) "
                       f"không một lần しかし/だが — trần {g['reversal_max_gap_sec']}s")
        if g.get("reversal_per_min") and phut and len(moc) / phut < g["reversal_per_min"]:
            bad.append(f"ĐẢO CHIỀU THƯA: {len(moc)/phut:.2f} lần/phút < sàn "
                       f"{g['reversal_per_min']} (đối thủ 0,55–1,01)")
    if g.get("fact_anchor_per_min") and rate:
        neo = len(re.findall(r"\d{3,4}\s*年|\d+\s*(?:キロ|km|メートル|人|年間|か月|パーセント|%)", body))
        phut = len(body) / rate
        if phut and neo / phut < g["fact_anchor_per_min"] * 0.7:
            bad.append(f"THIẾU MỐC SỰ THẬT: {neo/phut:.2f} mốc/phút < mục tiêu "
                       f"{g['fact_anchor_per_min']} (năm, số có đơn vị)")
    if g.get("hedge_min_per_10min") and rate:
        hedge = len(re.findall(r"という説|とされて|かもしれ|だとすれば|もし本当", body))
        chuc = max(len(body) / rate / 10, 0.1)
        if hedge / chuc < g["hedge_min_per_10min"]:
            bad.append(f"THIẾU MẪU CÂU LÁ CHẮN: {hedge} lần / {chuc*10:.0f} phút — cần "
                       f"≥{g['hedge_min_per_10min']} mỗi 10 phút (〜という説がある…)")
    return bad


def strip_markers(text):
    text = MARKER_PAT.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def normalize_paragraphs(text):
    """Gom các dòng bị xé giữa câu thành đoạn tử tế.

    Khi ép nhịp "ngắt hơi 7-9 chữ", model hay xuống dòng sau MỖI cụm → ra 193 "đoạn" (đo thật).
    Luật gom: dòng nào KHÔNG kết bằng 。！？」』 thì nối tiếp với dòng sau.
    """
    out = []
    for raw in [l.strip() for l in text.splitlines()]:
        if not raw:
            if out and out[-1] != "":
                out.append("")
            continue
        if out and out[-1] and out[-1][-1] not in "。．.!?！？」』":
            out[-1] += raw
        else:
            out.append(raw)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


# ============================================================ B3 — KỊCH BẢN
def _ap_ngach(txt, prof):
    """Thay dòng "NGÁCH CHỐT CHO PROFILE NÀY" trong skill bằng ngách THẬT của hồ sơ đang chạy.

    Các file skill được viết tổng quát (ngách/thị trường/ngôn ngữ là THAM SỐ), nhưng dòng số 6
    lại ghim cứng `niche=satori-elderly · narrator=cụ bà 70-80` từ hồi chỉ có một kênh. Kênh mới
    ngách khác (samurai, tiền hưu trí…) mà đọc phải dòng đó là bị kéo lệch ngay từ đầu, trong khi
    nhìn file thì tưởng skill trung lập.
    """
    n = prof.get("narrator", {}) or {}
    moi = (f"> **NGÁCH CHỐT CHO PROFILE NÀY:** niche={prof.get('niche', '?')} · "
           f"market={prof.get('market', '?')} · language={prof.get('language', '?')} · "
           f"narrator={n.get('persona', '?')} ({n.get('gender', '?')}, {n.get('age_band', '?')}, "
           f"{n.get('register', '')}). Mọi tham số còn lại lấy từ profile.")
    return re.sub(r"^>\s*\*\*NGÁCH CHỐT CHO PROFILE NÀY:\*\*.*$", moi.replace("\\", r"\\"),
                  txt, count=1, flags=re.M)


def _skill_text(prof, key="script"):
    rel = (prof.get(key, {}) or {}).get("skill", "")
    if not rel:
        return ""
    f = res(rel)
    if not f.exists():
        # Kênh mới chưa có skill riêng → dùng SKILL CHUNG (bản tổng quát, ngách là tham số).
        generic = {"script": "skills/youtube-script/SKILL.md",
                   "image": "skills/youtube-image-prompts/SKILL.md",
                   "thumbnail": "skills/youtube-thumbnail/SKILL.md"}.get(key, "")
        g = res(generic) if generic else None
        if g and g.exists():
            print(f"  (dùng skill chung {generic} — ngách lấy từ hồ sơ kênh)")
            return _ap_ngach(g.read_text(encoding="utf-8"), prof)
        print(f"⚠️ Chưa có skill {rel} → chạy bằng luật trong profile thôi (chất lượng sẽ kém hơn).")
        return ""
    return _ap_ngach(f.read_text(encoding="utf-8"), prof)


def _comment_insight_block(insight):
    """Chèn tín hiệu từ bình luận thật vào prompt viết kịch bản — user chốt 2026-09-10.

    Đặt NGAY SAU khối cấu trúc để model đọc "cao trào là đâu" (khối cấu trúc) xong thấy luôn
    "cao trào nên NHẤN CÁI GÌ" (khối này) — hai khối cùng chỗ, không tách rời để đọc mạch lạc."""
    if not insight or not (insight.get("diem_cham") or insight.get("thieu_sot")):
        return []
    out = []
    if insight.get("diem_cham"):
        out.append("KHÁN GIẢ BẢN GỐC NHẮC LẠI/XÚC ĐỘNG NHIỀU NHẤT Ở NHỮNG CHỖ SAU (rút từ bình "
                   "luận thật dưới video) — đào sâu cảm xúc đúng CHỖ TƯƠNG ỨNG trong bản MỚI, nhất "
                   "là ở đoạn cao trào:")
        out += [f"  · {x}" for x in insight["diem_cham"]]
    if insight.get("thieu_sot"):
        out.append("KHÁN GIẢ BẢN GỐC CÒN TIẾC/HỎI THÊM NHỮNG ĐIỀU SAU — cân nhắc đưa vào PHẦN 30% "
                   "SÁNG TẠO THÊM của bản mới (tham khảo, không bắt buộc dùng hết):")
        out += [f"  · {x}" for x in insight["thieu_sot"]]
    return out


def _pass1_prompt(prof, competitor, minutes, series_ctx, ask_chars=0, comment_insight=None, budget_block=None):
    n = prof.get("narrator", {}) or {}
    lang = LANG_NAME.get(prof.get("language", "ja"), prof.get("language"))
    mode = ((prof.get("script", {}) or {}).get("mode") or "").lower()
    doc = mode == "documentary"
    # fiction_facts (lane hưu trí/tiền, 2026-09-20): NHÂN VẬT hư cấu như satori, nhưng mọi con số
    # CHẾ ĐỘ (năm金/税/保険/給付金, tuổi nhận, tỉ lệ) phải lấy từ tư liệu — khán giả 60+ biết rõ
    # chế độ của chính họ, sai một con số là mất uy tín cả kênh. B3F (qc_facts) chạy cho mode này.
    if mode == "fiction_facts":
        nhiem_vu = (
            "NHIỆM VỤ: viết MỘT CÂU CHUYỆN MỚI (nhân vật HƯ CẤU) đi theo KHUNG SỰ KIỆN cho sẵn bên "
            "dưới. Tên người, nghề, vùng, đồ vật, tình tiết đời thường là của BẠN — tự nghĩ ra, đừng "
            "dùng lại thứ quen thuộc. NHƯNG mọi con số về CHẾ ĐỘ (年金 nhận bao nhiêu ở tuổi nào, "
            "繰上げ/繰下げ tăng giảm bao nhiêu %, 住民税/国民健康保険/介護保険 tính thế nào, "
            "高年齢求職者給付金, 再雇用 lương giảm bao nhiêu...) PHẢI LẤY ĐÚNG từ TƯ LIỆU kèm theo — "
            "không tự nghĩ ra, không làm tròn khác đi. Số tiền CÁ NHÂN của nhân vật (退職金, 貯金, "
            "chi tiêu tháng) do bạn đặt nhưng phải hợp lý với các mức trong tư liệu và phải xuất "
            "hiện dày đặc, cụ thể đến đơn vị 万円, lặp lại theo mốc thời gian để người xem theo dõi "
            "được tiền tụt dần.")
    elif doc:
        nhiem_vu = (
            "NHIỆM VỤ: viết BẢN KỂ TÀI LIỆU cho một câu chuyện CÓ THẬT (hoặc một giả thuyết đã được "
            "công bố), theo KHUNG cho sẵn bên dưới và TƯ LIỆU kèm theo. Mọi tên người, ngày tháng, "
            "địa danh, con số phải LẤY ĐÚNG từ tư liệu — không được tự nghĩ ra. Cái bạn sáng tạo là "
            "CÁCH KỂ, thứ tự dẫn dắt và phần liên hệ về Nhật Bản.")
    else:
        nhiem_vu = (
            "NHIỆM VỤ: viết MỘT CÂU CHUYỆN MỚI đi theo KHUNG SỰ KIỆN cho sẵn bên dưới. Khung chỉ nói "
            "mỗi nhịp làm gì; toàn bộ tên người, nghề, vùng, đồ vật, con số, tình tiết đời thường là "
            "của BẠN — hãy tự nghĩ ra, đừng dùng lại thứ quen thuộc.")
    parts = [
        nhiem_vu,
        f"LENGTH: {minutes} phút · NGÔN NGỮ OUTPUT: {lang}",
        f"NGƯỜI KỂ: {n.get('persona','')} · giới {n.get('gender','')} · tuổi {n.get('age_band','')} · "
        f"ngôi kể {n.get('point_of_view','')} · văn thể {n.get('register','')}",
        "",
        "YÊU CẦU BẮT BUỘC:",
        "1) Chỉ xuất BẢN CUỐI. Không lời dẫn, không giải thích, không tiêu đề, không 「パート」, "
        "không số thứ tự, không [ ], không ký hiệu trang trí.",
        # flow=lean (lean_script.py): viết ĐÚNG ngân sách từng phần, KHÔNG xin dài rồi nén.
        (budget_block if budget_block else
         f"2) Viết ĐỦ MẠCH, giàu chi tiết đời thường và cảm xúc. ĐỘ DÀI: viết DÀI HƠN mục tiêu — "
         f"tối thiểu {ask_chars:,} ký tự (không tính xuống dòng/khoảng trắng). Bước sau sẽ nén lại, "
         f"nên thiếu thì hỏng, dài thì không sao."),
        f"3) BẢN ĐỊA HOÁ 100% sang văn hoá của ngôn ngữ đích ({lang}): không để sót tên riêng, "
        "chế độ, tiền tệ, cách gọi của nguồn gốc.",
        _cau_truc_block(prof),
        "5) Giữ nhân phẩm nhân vật. Không tả bạo lực máu me, không tả thân thể trẻ nhỏ, không cảnh tắm.",
        _chong_trung_block(prof),
    ]
    parts += _comment_insight_block(comment_insight)
    if series_ctx:
        nhan = ((prof.get("script", {}) or {}).get("ctx_label")
                or "MẠCH SERIES (phải nhắc lại tập trước + hé tập sau)")
        parts += ["", nhan + ":", series_ctx]
    # Luật NHỊP phải viết bằng NGÔN NGỮ ĐÍCH mới ăn (bài học 2026-09-08: luật tiếng Việt bị bỏ qua
    # → ra 25% hội thoại, 1,6 phẩy/câu, PASS 2 phải sửa lại toàn bộ).
    parts += ["", _pacing_block(prof)]
    parts += ["", "KHUNG SỰ KIỆN CẦN ĐI THEO:", competitor]
    return "\n".join(parts)


# ------------------------------------------------------------- khối theo NGÁCH
# Hai khối dưới đây TỪNG là chữ ghim cứng trong _pass1_prompt từ hồi dự án chỉ có một kênh
# (satori: truyện đời cụ bà, hư cấu, được phép đổi tên/nghề/vùng). Đem nguyên sang ngách kể
# TÀI LIỆU thì hỏng cả hai đầu: cấu trúc ra 悟り thay vì 5 chương, còn luật "đổi tên nhân vật,
# đổi địa danh" là ĐANG BẢO MODEL BỊA DỮ KIỆN CÓ THẬT — đúng thứ khiến ngách này bị gắn cờ và
# bị khán giả bắt lỗi. Nay chọn theo profile.script.structure / profile.script.mode.

def _cau_truc_block(prof):
    sc = prof.get("script", {}) or {}
    g = profiles.gate(prof)
    # Lane khai `script.structure_block` (văn bản tự do) thì dùng NGUYÊN VĂN — cách thêm cấu trúc
    # mới cho một lane mà KHÔNG phải thêm nhánh if vào đây (hàng rào #2 CLAUDE.md). Thêm 2026-09-20
    # cho lane teinengo-real (7 chặng manga story); lane không khai field → không đổi gì.
    if (sc.get("structure_block") or "").strip():
        return "4) Cấu trúc BẮT BUỘC —\n" + sc["structure_block"].strip()
    if (sc.get("structure") or "").lower() == "manga_list":
        # Lane G (teinengo-tanoshimi, 2026-09-20): MANGA STORY ngôi 1 + list N選. KHÁC list_countdown
        # (Lane E, bác sĩ giải thích ngôi 2, mỗi mục 1 người ẩn danh) ở 4 chỗ: 1 nhân vật chính xuyên
        # tập kể "俺" · người dẫn đường (mentor) khai sáng · mỗi mục là 1 cảnh nhân vật TỰ THỬ có thoại ·
        # mục cuối là cú lật tư duy hướng nội. Cấu trúc 5 hồi đo từ 8 transcript kênh mẫu
        # (docs/channel_dna/rougo-money-story/CHANNEL_DNA.md §Story structure). Mọi con số
        # (số mục, thứ tự đếm, câu outro) lấy từ profile, không ghim theo lane.
        n = g.get("list_item_count") or 5
        order = (g.get("list_order") or "auto").lower()
        if order == "countdown":
            dem = f"đếm NGƯỢC 第{n}位→第1位 (xếp hạng, mục cuối = hạng 1)"
        elif order == "ascending":
            dem = f"đếm XUÔI 1つ目→{n}つ目"
        else:
            dem = (f"đếm XUÔI 1つ目→{n}つ目 nếu là THÓI QUEN/cách làm; đếm NGƯỢC 第{n}位→第1位 nếu là "
                   f"XẾP HẠNG địa điểm/đồ vật (kênh mẫu dùng cả hai, chọn theo đề tài)")
        outro = sc.get("outro_line") or "ご視聴いただきありがとうございました。いいねとコメントもお待ちしています。"
        return (f"4) Cấu trúc BẮT BUỘC — MANGA STORY ngôi thứ nhất + danh sách {n}選, {dem}. Đúng 5 hồi:\n"
                "   · HỒI 1 — HOOK + BẾ TẮC (0–2 phút): câu ĐẦU TIÊN là 1 nghịch lý/con số gây sốc/câu "
                "thoại bất ngờ liên quan tiền–thời gian–quan hệ sau nghỉ hưu (KHÔNG chào hỏi, KHÔNG dạo "
                "đầu). Rồi nhân vật chính tự giới thiệu: tên, tuổi (60–67), số năm đi làm, tình trạng gia "
                "đình, và NỖI ĐAU cụ thể đang mắc (sáng dậy không biết làm gì / tiêu tiền cho đỡ buồn / "
                "cơ thể nặng nề / không ai gọi). Kết hồi bằng câu điềm báo kiểu「この時の俺はまだ知らな"
                "かった…」.\n"
                "   · HỒI 2 — NGƯỜI DẪN ĐƯỜNG (2–3,5 phút): gặp 1 nhân vật phụ an nhiên (bạn cũ trẻ lạ, "
                "sếp cũ đã nghỉ, người lạ ở công viên/quán/tàu…) — người này 'chẩn đoán' sai lầm của "
                f"nhân vật chính bằng 1 câu thoại đắt, rồi hé「{n}つある」→ open loop 'đó là gì?'.\n"
                f"   · HỒI 3 — BODY đúng {n} mục ĐỀU NHAU (tới ~70% thời lượng), mỗi mục ĐỦ 4 phần:\n"
                "     a) tên mục ngắn gọn CỤ THỂ (hành động/địa điểm, không khái niệm trừu tượng)\n"
                "     b) ĐỐI THOẠI 2 người: nhân vật chính hỏi ngây ngô/bảo thủ → mentor phản biện mở "
                "mang (lý do + ví dụ đời thường)\n"
                "     c) nhân vật chính TỰ THỬ ngay trong chuyện, ghi nhận đổi thay tâm lý/cơ thể tại chỗ\n"
                "     d) 1 câu mini-chốt chiêm nghiệm, rồi 1 câu hỏi ngắn giữ nhịp dẫn sang mục sau "
                "(「じゃあ次は？」「本当に効くのか？」)\n"
                "     Tên địa điểm / mức giá / thông tin thực tế Nhật Bản CHỈ lấy từ TƯ LIỆU kèm theo — "
                "không tự bịa giá vé, tên chùa, số liệu.\n"
                "   · MID-ROLL CTA (ở khoảng 45–55% video, giữa 2 mục): 1 câu mời bình luận đúng giọng đời "
                "thường (「あなたなら何から始めますか？コメントで教えてください」).\n"
                "   · HỒI 4 — MỤC CUỐI = CÚ LẬT TƯ DUY (70–90%): mục cuối cùng luôn là giải pháp HƯỚNG NỘI "
                "(không làm gì cả / chấp nhận bản thân / làm quen với một mình / buông kỳ vọng), đối lập "
                "với các mục tốn tiền bên ngoài. Nhân vật chính thừa nhận định kiến cũ đã sai.\n"
                "   · HỒI 5 — KẾT (90–100%): sáng hôm sau nhân vật thức dậy với tâm thế mới, làm 1 việc "
                "nhỏ (uống nước, đi dạo 5 phút, ngắm trời, mua vé tàu) — KHÉP LẠI cảnh mở đầu. Tóm tắt "
                f"nhanh {n} mục bằng 1–2 câu. Câu cuối cùng nguyên văn:「{outro}」\n"
                "   · GIỌNG: nam trung niên xưng「俺」, câu ngắn, trầm tĩnh, dùng từ vựng サラリーマン "
                "(現役時代/定年退職/再雇用…). Thoại để trong「」. Mọi chủ đề đều quy về 2 giá trị: bảo vệ "
                "老後資金 + 本当の自由. Hướng VUI/RẺ — KHÔNG kịch tính mất tiền, KHÔNG lên lớp.")
    if (sc.get("structure") or "").lower() == "list_countdown":
        n = g.get("list_item_count") or 5
        return (f"4) Cấu trúc BẮT BUỘC — video liệt kê đếm ngược kiểu bác sĩ giải thích, đúng {n} mục:\n"
                "   · HOOK (0–2 phút): khen/đồng cảm với người xem trước → đặc tả nỗi đau/nỗi lo CỤ "
                "THỂ (không trừu tượng) → 1 SỐ LIỆU gây lo (có nguồn, không bịa %) → hé lộ 'nguyên "
                "nhân không phải như bạn nghĩ' (mở open loop) → hứa 'hôm nay sẽ nói rõ N điều'.\n"
                f"   · PROMISE (2–4 phút): liệt kê nhanh mục lục {n} điều sắp nói (không đi sâu).\n"
                f"   · BODY — đúng {n} khối ĐỀU NHAU, đếm ngược 第{n}位→第1位, mỗi khối gồm ĐỦ 4 phần "
                "theo thứ tự:\n"
                "     a) cơ chế khoa học, giải thích bằng 1 ví von đời thường dễ hiểu\n"
                "     b) MỘT câu chuyện minh hoạ: một người ẩn danh có tuổi/nghề cụ thể (vd '68歳の"
                "元スーパー店員の女性') — đây là VÍ DỤ ĐẠI DIỆN, KHÔNG phải nhân vật có thật xác định "
                "danh tính; không gắn họ tên thật, không tuyên bố đây là câu chuyện xác thực\n"
                "     c) số liệu nghiên cứu (năm + tên tổ chức + %) — CHỈ dùng số có trong tư liệu "
                "đưa vào, KHÔNG bịa % hay tên viện nghiên cứu mới\n"
                "     d) 1 câu mini-chốt bắt đầu bằng 'つまり' rồi chuyển ý bằng 'さて、では次の…'\n"
                "   · MID-ROLL CTA (ở khoảng 50–60% video): 1 câu hỏi mời bình luận, đúng giọng đời "
                "thường ('〜を試したことはありますか？コメント欄で教えてください').\n"
                "   · PAYOFF (80–90%): tóm tắt nhanh lại toàn bộ danh sách → câu động viên dạng "
                "'これはあなたのせいではありません、誰も教えてくれなかっただけです'.\n"
                "   · ENDING: đúng 4 bước hành động CỤ THỂ có thể bắt đầu 'TỐI NAY', càng nhỏ/dễ càng "
                "tốt, rồi mời đăng ký kênh nhẹ nhàng, không ép.\n"
                "   · Ở BẤT KỲ chỗ nào có tuyên bố về sức khoẻ: PHẢI có ít nhất 1 câu dạng "
                "'一般的な健康情報です。持病のある方は医師にご相談ください' — không tuyên bố chữa khỏi "
                "bệnh tuyệt đối, không thay thế chỉ định của bác sĩ.")
    if (sc.get("structure") or "").lower() == "chapters5":
        marks = g.get("chapter_markers") or ["第1章", "第2章", "第3章", "第4章", "第5章"]
        jp = g.get("require_japan_hook_chapter") or 4
        return ("4) Cấu trúc BẮT BUỘC — phim tài liệu 5 chương:\n"
                "   · HOOK 30 giây đầu: nói thẳng KẾT LUẬN gây sốc, neo vào NGÀY/NƠI/NGƯỜI cụ thể. "
                "Không dạo đầu, không chào hỏi.\n"
                "   · 30–75 giây: leo thang + HỨA phần thưởng cho người xem hết video.\n"
                f"   · {marks[0]} sự kiện gốc (tường thuật, dày mốc năm) · {marks[1]} nhân vật/tài "
                f"liệu trung tâm và vì sao đáng tin · {marks[2]} bằng chứng và phản bác chính thống\n"
                f"   · {marks[jp-1]} ⭐ MÓC CÂU CHUYỆN VỀ NHẬT BẢN — bắt buộc, đây là giá trị gia "
                f"tăng của kênh, không phải phần phụ\n"
                f"   · {marks[4]} diễn giải lớn: điều này nghĩa gì với người xem hôm nay\n"
                "   · KẾT 90 giây: khung triết lý + nói thẳng với người xem + câu hỏi gọi comment.\n"
                "   Tên chương viết đúng dạng 第◯章 trên một dòng riêng, kèm tiêu đề ngắn.")
    return ("4) Cấu trúc: mở cảnh điện ảnh (mùa + nơi + cử chỉ) → gieo伏線 → cao trào → 1 câu悟り "
            "(bài học) → 3 tầng kết → câu hỏi gọi comment.")


def _chong_trung_block(prof):
    mode = ((prof.get("script", {}) or {}).get("mode") or "").lower()
    if mode == "fiction_facts":
        return ("6) BẮT BUỘC KHÁC BẢN GỐC (YouTube phạt 'sử dụng lại nội dung') NHƯNG KHÔNG BỊA CHẾ ĐỘ:\n"
                "   · Đổi TÊN nhân vật, NGHỀ, VÙNG, VẬT TRUNG TÂM, và các mốc tiền CÁ NHÂN (退職金/貯金/"
                "chi tiêu) sang con số KHÁC bản gốc nhưng cùng tầm.\n"
                "   · TUYỆT ĐỐI KHÔNG đổi/không tự nghĩ ra con số CHẾ ĐỘ (年金 theo tuổi, % 繰上げ/繰下げ, "
                "税/保険 năm đầu sau nghỉ, 給付金...) — chỉ dùng số có trong TƯ LIỆU; không có trong "
                "tư liệu thì DIỄN ĐẠT ĐỊNH TÍNH, đừng nêu số.\n"
                "   · Không gắn họ tên người thật, không nói đây là chuyện có thật.\n"
                "   · THÊM ít nhất 3 tình tiết MỚI; BỎ hoặc GỘP ít nhất 2 tình tiết của bản gốc.\n"
                "   · Không dịch sát câu biểu tượng nào của bản gốc.")
    if mode == "documentary":
        return ("6) KHÁC BẢN GỐC nhưng KHÔNG ĐƯỢC BỊA DỮ KIỆN — hai điều này đi cùng nhau:\n"
                "   · TUYỆT ĐỐI KHÔNG đổi, không sáng tác tên người thật, ngày tháng, địa danh, "
                "số liệu, tên tài liệu. Sai một con số là mất uy tín cả video.\n"
                "   · Chỗ được phép khác: THỨ TỰ kể, GÓC NHÌN, cách đặt câu hỏi, chi tiết bối cảnh "
                "lịch sử thêm vào, và đặc biệt là chương móc về Nhật Bản (bản gốc không có).\n"
                "   · THÊM ít nhất 3 dữ kiện có thật mà bản gốc không nhắc tới; BỎ hoặc GỘP ít nhất "
                "2 đoạn của bản gốc.\n"
                "   · Không dịch sát câu nào của bản gốc.\n"
                "   · Con số nào không chắc thì DIỄN ĐẠT ĐỊNH TÍNH, đừng nêu số. Thà mờ còn hơn sai.")
    return ("6) BẮT BUỘC KHÁC BẢN GỐC — đây là điều kiện SỐNG CÒN (YouTube phạt lỗi 'sử dụng lại "
            "nội dung'):\n"
            "   · Đổi TÊN nhân vật, NGHỀ NGHIỆP, VÙNG/ĐỊA DANH, và VẬT TRUNG TÂM của câu chuyện sang "
            "thứ KHÁC nhưng mang cùng sức nặng cảm xúc (vd sổ tay → hộp thư cũ / tạp dề vá).\n"
            "   · TUYỆT ĐỐI không dịch sát câu biểu tượng nào của bản gốc.\n"
            "   · THÊM ít nhất 3 tình tiết MỚI hoàn toàn không có trong bản gốc.\n"
            "   · BỎ hoặc GỘP ít nhất 2 tình tiết của bản gốc.\n"
            "   Giữ nguyên: khung cảm xúc, kiểu nhân vật, bài học cuối. Đổi hết phần bề mặt.")


def _pacing_block(prof):
    """Khối luật nhịp/hội thoại bằng ngôn ngữ đích, dùng chung cho PASS 1."""
    g = profiles.gate(prof)
    lo, hi = g["comma_per_sentence"]
    blo, bhi = g.get("chars_per_breath", [4.5, 9.0])
    dmax = int(g["dialogue_ratio_max"] * 100)
    persona = (prof.get("narrator", {}) or {}).get("persona", "")
    lang = prof.get("language", "ja")
    if lang == "ja":
        # Lane có thoại 2 nhân vật (manga, dialogue_ratio_max ≥ 25%) thì KHÔNG được dặn "đừng dựa vào
        # hội thoại" — câu đó viết cho satori/toshi (thoại ≤15%). Rẽ theo ngưỡng, không theo lane.
        if g["dialogue_ratio_max"] >= 0.25:
            kaiwa = (f"・「」の会話は全体の{dmax}%以下。会話は登場人物の掛け合いとして活かすが、"
                     f"1つの発話は短く、地の文（心の声・状況描写）で前後をつなぐ。\n")
        else:
            kaiwa = f"・「」の会話は全体の{dmax}%以下。会話に頼らず、地の文の語りで進める。\n"
        s = (f"【語りのリズム（厳守）】\n"
             f"・語り手（{persona}）の息づかいに合わせ、読点「、」で{int(blo)}〜{int(bhi)}字ごとに区切る。"
             f"1文あたり読点{int(lo)}〜{int(hi)}個、一文は短く。\n"
             + kaiwa +
             f"・段落は意味のまとまりごと（1段落＝3〜6文）。1文ごとに改行しない。文の途中で改行しない。")
        if g.get("require_next_ep_teaser"):
            s += "\n・最後に、視聴者へコメントを促す問いかけと、次回作を予告する一文を必ず入れる。"
        # Nhịp RIÊNG của ngách kể tài liệu — đo thật trên 4 video top của kênh mẫu. Ba con số này
        # là thứ tạo cảm giác "đã nghiên cứu kỹ" và giữ chân người xem CHỦ ĐỘNG (khác hẳn ngách
        # người già: 0/190 comment nhắc chuyện "nghe khi ngủ").
        if g.get("reversal_max_gap_sec"):
            rate = profiles.char_rate(prof)
            moi = int(rate * g["reversal_max_gap_sec"] / 60)
            s += (f"\n・「しかし」「だが」「ところが」のような'どんでん返し'の一言を、"
                  f"最低でも{moi}字に一度は入れる。これが動画全体のメトロノームになる。")
        if g.get("fact_anchor_per_min"):
            rate = profiles.char_rate(prof)
            moi = int(rate / max(g["fact_anchor_per_min"], 0.01))
            s += (f"\n・約{moi}字ごとに、西暦の年号・地名・単位つきの数字のいずれかを必ず置く。"
                  f"ただし資料にある事実だけを使い、数字を創作しない。")
        if g.get("hedge_min_per_10min"):
            s += ("\n・断定を避ける言い回し（〜という説がある／〜とされています／〜かもしれません／"
                  "もし本当だったら）を各章に必ず入れる。これは弱さではなく、この題材で必要な盾。")
        if g.get("chapter_markers"):
            s += ("\n・視聴者への呼びかけ「あなた」は冒頭と結びだけ。本編の途中では使わない。")
        return s
    if lang == "ko":
        s = (f"【말의 리듬(반드시 지킬 것)】\n"
             f"・화자({persona})의 호흡에 맞춰 쉼표로 {int(blo)}〜{int(bhi)}자마다 끊고, 문장당 쉼표 "
             f"{int(lo)}〜{int(hi)}개.\n・대화문은 전체의 {dmax}% 이하, 서술 중심.")
        if g.get("require_next_ep_teaser"):
            s += "\n・마지막에 댓글 유도 질문과 다음 편 예고 문장을 넣으세요."
        return s
    s = (f"[RHYTHM — strict]\n- Match the breathing of the narrator ({persona}): a comma break every "
         f"{int(blo)}–{int(bhi)} characters, {int(lo)}–{int(hi)} commas per sentence, short sentences.\n"
         f"- Quoted dialogue at most {dmax}% of the text; narration carries the story.")
    if g.get("require_next_ep_teaser"):
        s += "\n- End with a question inviting comments plus one sentence teasing the next episode."
    return s


def _chunk_prompt(prof, part, i, n_parts, budget, prev_tail, keep_length=False):
    """Prompt viết lại 1 KHÚC với hạn mức chữ cụ thể — viết bằng ngôn ngữ đích.

    `keep_length=True`: độ dài ĐÃ đạt, chỉ cần sửa NHỊP/hội thoại → giữ nguyên số chữ.
    (Không có nhánh này thì tool cứ đòi nén một bản đã đúng độ dài → guard loại bản mới →
    nhịp vĩnh viễn không được sửa. Đã dính thật 2026-09-08.)
    """
    g = profiles.gate(prof)
    blo, bhi = g.get("chars_per_breath", [4.5, 9.0])
    lo, hi = g["comma_per_sentence"]
    dmax = int(g["dialogue_ratio_max"] * 100)
    cur = len(part.replace("\n", "").replace(" ", "").replace("　", ""))
    cut = max(3, int(round((1 - budget / max(cur, 1)) * 100)))
    persona = (prof.get("narrator", {}) or {}).get("persona", "")
    lang = prof.get("language", "ja")
    ctx = ""
    # Bước nén vốn được dặn "không viết tiêu đề/số" — với ngách 5 chương thì câu dặn đó XOÁ LUÔN
    # các dòng 第◯章 của bản gốc, và gate lập tức báo THIẾU CHƯƠNG (đo thật 2026-09-10: nén xong
    # mất sạch 5/5 mốc chương). Kênh nào khai chapter_markers thì phải dặn ngược lại.
    giu = "・出力は原稿本文のみ。見出し・番号・説明・字数の記載を書かない。"
    if g.get("chapter_markers") and lang == "ja":
        giu = ("・原稿にある「第◯章」の見出し行は必ずそのまま残す（削除も改変もしない）。\n"
               "・出力は原稿本文のみ。番号・説明・字数の記載を書かない。")
    # Câu LÁ CHẮN (〜という説がある…) là thứ bước nén XOÁ ĐẦU TIÊN — nhìn nó giống lời rào đón thừa.
    # Đo thật ep03: nén 12.110 → 9.026 chữ làm lá chắn rụng từ **6 xuống 1**, gate lập tức báo
    # THIẾU LÁ CHẮN dù trước khi nén đang đủ. Cùng một lớp lỗi với 第◯章 ở trên: câu dặn "cắt chỗ
    # thừa" không biết cái gì là thừa THEO LUẬT CỦA NGÁCH, nên phải dặn ngược lại cho rõ.
    if g.get("hedge_min_per_10min") and lang == "ja":
        giu += ("\n・「〜という説がある」「〜とされています」「〜かもしれません」「もし本当だったら」"
                "などの断定を避ける言い回しは、冗長に見えても削らない。この題材で必要な盾である。")
    if lang == "ja":
        if prev_tail:
            ctx = f"\n【直前の部の末尾（重複させないための参考。書き写さない）】\n{prev_tail}\n"
        # Lane thoại nhiều (manga, dialogue_ratio_max ≥ 25%): CẤM nén xoá「」/đổi sang gián tiếp — đo thật
        # Lane G ep01 2026-09-20: Fable viết ~26% thoại, Gemini nén còn 8% (toàn "〜と言った"), mất chất manga.
        if g["dialogue_ratio_max"] >= 0.25:
            kaiwa_nen = (f"・「」の会話は登場人物の掛け合いなので削らない・間接話法（〜と言った）に直さない。"
                         f"凝縮するのは地の文だけ（会話は全体の{dmax}%以下なら十分）。\n")
        else:
            kaiwa_nen = (f"・「」の会話は全体の{dmax}%以下。会話が多すぎる部分は地の文の語りに書き換える"
                         f"（「〜と申しました」「〜とおっしゃいました」の形にする）。\n")
        if keep_length:
            return (f"以下はナレーション原稿の第{i}部（全{n_parts}部）です。**長さはほぼそのまま"
                    f"（{int(cur*0.95):,}〜{int(cur*1.05):,}字）**で、語りのリズムだけを直して"
                    f"書き直してください。内容・筋・出来事は一切変えないこと。\n"
                    f"・語り手（{persona}）の息づかい：読点で{int(blo)}〜{int(bhi)}字ごとに区切り、"
                    f"1文あたり読点{int(lo)}〜{int(hi)}個。一文は短く。\n"
                    + kaiwa_nen +
                    f"・段落は意味のまとまりごと。文の途中で改行しない。\n"
                    f"{giu}{ctx}\n"
                    f"【第{i}部の原稿】\n{part}")
        return (f"以下はナレーション原稿の第{i}部（全{n_parts}部）です。筋・人物・重要な台詞は変えずに、"
                f"**改行と空白を除いて{int(budget*0.95):,}〜{int(budget*1.05):,}字**に凝縮して"
                f"書き直してください（現在{cur:,}字 → 約{cut}%削減）。\n"
                f"・冗長な描写・重複する説明・同義の場面だけを削る。新しい出来事は足さない。\n"
                + kaiwa_nen +
                f"・語り手（{persona}）の息づかい：読点で{int(blo)}〜{int(bhi)}字ごとに区切り、"
                f"1文あたり読点{int(lo)}〜{int(hi)}個。\n"
                f"・段落は意味のまとまりごと。文の途中で改行しない。\n"
                f"{giu}{ctx}\n"
                f"【第{i}部の原稿】\n{part}")
    if prev_tail:
        ctx = f"\n[Tail of the previous part — for continuity only, do not copy]\n{prev_tail}\n"
    return (f"This is part {i} of {n_parts} of a narration script. Rewrite it condensed to "
            f"**{int(budget*0.95):,}–{int(budget*1.05):,} characters** excluding line breaks and spaces "
            f"(currently {cur:,} → cut about {cut}%). Keep the plot, characters and key lines; cut only "
            f"redundancy. Narrator: {persona}. Break breath every {int(blo)}–{int(bhi)} characters with "
            f"commas, {int(lo)}–{int(hi)} commas per sentence. Never break a line mid-sentence. "
            f"Output the script text only.{ctx}\n[PART {i}]\n{part}")


def trim_chunked(prof, draft, target, minutes, chunk_chars=4500, workers=3, keep_length=False):
    """Nén THEO KHÚC với hạn mức chữ từng khúc — cách DUY NHẤT ép được độ dài (đo thật 2026-09-08).

    Nén cả bản 1 lượt: 13.108 → 11.953 chữ (+25% so mục tiêu) rồi ĐỨNG (lượt 2 ra 12.052).
    Nén 3 khúc có hạn mức: 13.108 → 9.975 chữ (31,4') → GATE ĐẠT.
    """
    from concurrent.futures import ThreadPoolExecutor

    def nchar(s):
        return len(s.replace("\n", "").replace(" ", "").replace("　", ""))

    total = nchar(draft)
    # Dư CÀNG ÍT thì phải chia CÀNG NHỎ. Đo thật: dư 17% mà chia 2 khúc to (5.744+5.357) → mỗi khúc
    # chỉ phải cắt 15%, model bỏ qua, bản mới ĐỨNG YÊN ở 11.101 chữ. Khúc nhỏ = lệnh cắt cụ thể hơn.
    if not keep_length and target < total:
        over = total / max(target, 1)
        chunk_chars = 2200 if over < 1.35 else (3200 if over < 2.0 else 4500)
    n_parts = max(2, min(8, round(total / chunk_chars)))
    # Đơn vị chia: ĐOẠN nếu có đủ đoạn, không thì CÂU.
    # (Đã dính: sau normalize_paragraphs bản nháp không còn dòng trắng → split theo đoạn chỉ ra
    #  1 đoạn khổng lồ + 1 khúc RỖNG → model trả rỗng → LLMError.)
    units = [p for p in re.split(r"\n\s*\n", draft) if p.strip()]
    sep = "\n\n"
    if len(units) < n_parts * 3:
        units = [s for s in re.split(r"(?<=[。！？])", draft.replace("\n", "")) if s.strip()]
        sep = ""
    parts, cur, acc = [], [], 0
    for u in units:
        cur.append(u)
        acc += nchar(u)
        if acc >= total / n_parts and len(parts) < n_parts - 1:
            parts.append(sep.join(cur))
            cur, acc = [], 0
    if cur:
        parts.append(sep.join(cur))
    parts = [p for p in parts if nchar(p) > 200]          # bỏ khúc rỗng/vụn
    mode = "GIỮ độ dài, chỉ sửa nhịp" if keep_length else f"nén về {target:,}"
    print(f"[B3 chỉnh khúc] {total:,} chữ → {len(parts)} khúc {[nchar(p) for p in parts]} · {mode}")

    if not keep_length and target >= total:
        # Nới dài KHÔNG đáng tin (đo thật: xin +22% thì model trả +55%) → chỉ sửa nhịp, giữ độ dài.
        print("  (mục tiêu ≥ bản hiện tại → chuyển sang chế độ GIỮ độ dài, chỉ sửa nhịp)")
        keep_length = True

    def do(idx_part):
        i, part = idx_part
        budget = nchar(part) if keep_length else int(target * nchar(part) / max(total, 1))
        tail = parts[i - 2][-250:] if i >= 2 else ""
        prompt = _chunk_prompt(prof, part, i, len(parts), budget, tail, keep_length)
        # RÀO CHẶN LLM LẶP/PHÌNH TO (đo thật ep03-eiyou-machigai 2026-09-18): 1 khúc xin nén về
        # ngân sách 2.288 chữ trả về 26.816 chữ (model rơi vào lặp lại nội dung tới khi chạm trần
        # token) — chat() chỉ có min_chars/require_sentence_end, KHÔNG có trần trên, nên câu trả lời
        # lặp bị chấp nhận thẳng vào bản ghép cuối, đẻ ra kịch bản dán trùng lặp 4-5 lần cùng 1 đoạn.
        # Với tác vụ NÉN, output vượt xa ngân sách là bất thường (khác PASS1 viết nháp, ở đó dài hơn
        # có thể chấp nhận được) — thử lại 1 lần, vẫn hỏng thì dừng hẳn thay vì âm thầm nhận rác.
        tran_tren = max(int(budget * 1.6), budget + 500)
        for lan in (1, 2):
            r = chat(prompt, task="script", temperature=0.6, min_chars=int(budget * 0.6),
                      require_sentence_end=True, verbose=False)
            t = normalize_paragraphs(strip_markers(r.text))
            n = nchar(t)
            if n <= tran_tren:
                break
            print(f"   khúc {i}: lần {lan} trả {n:,} chữ (vượt trần {tran_tren:,}, hạn mức {budget:,}) "
                  f"— nghi model lặp/phình, thử lại" + ("" if lan == 1 else " KHÔNG khá hơn"))
            if lan == 2:
                raise LLMError(f"khúc {i}: 2 lần đều trả {n:,} chữ vượt xa hạn mức {budget:,} "
                               f"(nghi model lặp lại nội dung) — dừng thay vì ghép rác vào kịch bản")
        print(f"   khúc {i}: {nchar(part):,} → {nchar(t):,} chữ (hạn mức {budget:,}) {r.elapsed:.0f}s")
        return i, t

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = sorted(ex.map(do, [(i, p) for i, p in enumerate(parts, 1)]))
    return "\n\n".join(t for _, t in res)


REPAIR_HEAD = {
 "ja": ["以下の台本には、編集者が指摘した不整合があります。指摘された箇所だけを直してください。",
        "・全文をそのまま出力すること。長さ・語り口・段落構成は変えない。",
        "・指摘のない文は一字も変えない。",
        "・矛盾（年数・年齢・関係・金額）は、作品全体で一つの値に統一する。",
        "・同じ出来事を二度語っている箇所は、一方を削るか別の内容に書き換える。",
        "・説明や前置きは書かず、直した台本本文だけを出力する。"],
 "ko": ["아래 대본에는 편집자가 지적한 모순이 있습니다. 지적된 부분만 고쳐 주세요.",
        "・전문을 그대로 출력하고 길이와 문체는 바꾸지 마세요.",
        "・모순되는 수치는 작품 전체에서 하나로 통일하세요.",
        "・설명 없이 고친 본문만 출력하세요."],
 "en": ["The script below has inconsistencies flagged by an editor. Fix ONLY those.",
        "- Output the FULL script, same length, same voice, same paragraphs.",
        "- Leave untouched sentences byte-identical.",
        "- Make every contradicted fact consistent across the whole script.",
        "- Output the corrected script only, no preamble."],
}


def repair_script(prof, text, issues, minutes=None):
    """Sửa ĐÚNG các lỗi QC chỉ ra, giữ nguyên độ dài và giọng văn.

    Lệnh sửa viết bằng NGÔN NGỮ ĐÍCH (bài học: luật viết tiếng Việt bị model bỏ qua); danh sách lỗi
    giữ nguyên tiếng Việt để anh đọc được — model đọc hiểu được cả hai."""
    lang = prof.get("language", "ja")
    head = REPAIR_HEAD.get(lang, REPAIR_HEAD["en"])
    body = head + ["", "【指摘 / ISSUES】"] + [f"{i+1}. {x}" for i, x in enumerate(issues)] +            ["", "【台本 / SCRIPT】", text]
    n = measure(text)["chars"]
    r = chat("\n".join(body), task="script", temperature=0.4,
             min_chars=int(n * 0.75), require_sentence_end=True)
    out = normalize_paragraphs(strip_markers(r.text))
    print(f"  [sửa] {n:,} → {measure(out)['chars']:,} chữ · {r.provider}:{r.model} {r.elapsed:.0f}s")
    return out


def issues_of(qc):
    """Rút danh sách lỗi NỘI DUNG (bỏ mục chỉ để tham khảo) từ kết quả qc_script.run()."""
    rv = qc.get("review") or {}
    out = []
    for c in rv.get("mau_thuan_du_kien", []) or []:
        out.append(f"Mâu thuẫn dữ kiện @{c.get('o_dau','')}: {c.get('noi_dung','')}")
    for l in rv.get("loi_logic", []) or []:
        if (l.get("muc") or "").lower() in ("cao", "vua"):
            out.append(f"Lỗi logic: {l.get('noi_dung','')}")
    for d in rv.get("doan_trung_y", []) or []:
        out.append(f"Hai chỗ kể trùng một ý: {d.get('noi_dung','')}")
    for f in rv.get("伏線", []) or []:
        if f.get("da_tra") is False:
            out.append(f"Chi tiết gieo mà không trả: {f.get('gieo','')}")
    for v in rv.get("dau_vet_van_hoa_nguon", []) or []:
        out.append(f"Còn sót phong tục/cách nói của nước gốc, phải thay bằng thứ bản địa: {v}")
    for m in qc.get("mechanical", []) or []:
        if m.get("sev") in ("cao", "vua"):
            out.append(f"{m['kind']}: {m['msg']}")
    return [x for x in out if len(x) > 15][:12]


_NARRATOR_SCHEMA = """{"gender":"male|female",
 "age":"số tuổi, vd 73",
 "age_band":"young|middle_aged|old",
 "role":"vai trò/nghề của người kể trong câu chuyện, vd y tá viện dưỡng lão, giám đốc nhà tang lễ",
 "persona":"1 câu tiếng Việt tả người kể để viết kịch bản, gồm tuổi + giới + nghề + tính cách",
 "tone":"3-6 từ tiếng Việt tả sắc thái giọng, vd trầm ấm chậm rãi tâm tình",
 "character_sheet":"mô tả NGOẠI HÌNH người kể bằng TIẾNG ANH cho AI vẽ ảnh: tuổi, giới, DÂN TỘC THEO THỊ TRƯỜNG ĐÍCH, kiểu tóc, kính, trang phục thường ngày, nét mặt — 15-30 từ, không tên riêng",
 "confidence":"cao|vừa|thấp",
 "reason":"1 câu vì sao"}"""


def detect_narrator(transcript, lang="", market=""):
    """Đọc lời kể video gốc → NGƯỜI KỂ của RIÊNG tập này.

    Vì sao phải làm: hồ sơ kênh chỉ có MỘT người kể, nhưng một kênh có rất nhiều video và mỗi
    video một người kể khác nhau — video này là bà mẹ kể, video kia là ông chồng, video khác là
    y tá hay giám đốc nhà tang lễ. Khoá cứng theo hồ sơ thì kịch bản viết sai ngôi kể VÀ ảnh vẽ
    sai mặt nhân vật chính, trong khi giọng đọc lại đúng — thành ra lệch hẳn nhau.

    Một lần gọi này nuôi CẢ BA chỗ: kịch bản (persona/giới/tuổi), ảnh (mặt nhân vật chính),
    và giọng (giới/tuổi/sắc thái) — nên ba thứ luôn tả cùng một người.
    """
    sample = (transcript or "").strip()[:4000]
    if len(sample) < 200:
        return None
    ask = "\n".join([
        "Đây là TRANSCRIPT lời kể (voiceover) của một video kể chuyện faceless.",
        "Hãy suy ra NGƯỜI KỂ là ai: ngôi thứ nhất thì chính là nhân vật xưng 'tôi'.",
        "Căn cứ: cách xưng hô, nghề nghiệp/vai trò tự nhận, tuổi tự nhận, trải nghiệm kể lại.",
        "Nếu người kể KHÔNG tự nói tuổi thì ước lượng theo nội dung.",
        # Nguồn là kênh nước khác (vd Hàn) nhưng bản làm ra là cho thị trường đích (vd Nhật) —
        # tả nhân vật theo dân tộc của NGUỒN thì ảnh vẽ ra sai hẳn người.
        f"QUAN TRỌNG: bản làm ra dành cho thị trường {market or 'đích'}"
        f"{' (' + LANG_NAME.get(lang, lang) + ')' if lang else ''}, nên `character_sheet` phải tả "
        f"người {market or 'của thị trường đích'} — KHÔNG theo dân tộc của video nguồn.",
        "",
        "Trả về DUY NHẤT JSON đúng khuôn (không thêm chữ nào):",
        _NARRATOR_SCHEMA,
        "",
        "TRANSCRIPT:",
        sample,
    ])
    try:
        r = chat(ask, task="short", max_tokens=500, min_chars=20, verbose=False)
    except Exception as e:
        print(f"  (nhận diện người kể: LLM lỗi {type(e).__name__} {e})")
        return None
    m = re.search(r"\{.*\}", r.text, re.DOTALL)
    if not m:
        print(f"  (nhận diện người kể: không trả JSON: {r.text[:120]})")
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    if not d.get("gender") or not d.get("persona"):
        return None
    band = str(d.get("age_band") or "").lower()
    d["age_band"] = ("old" if "old" in band or "eld" in band or "senior" in band
                     else "young" if "young" in band or "teen" in band else "middle_aged")
    return d


def apply_narrator(prof, det):
    """Bản SAO của hồ sơ với người kể thay bằng người kể của tập này.

    Chỉ thay phần THUỘC VỀ TẬP (persona/giới/tuổi). Giữ nguyên phần THUỘC VỀ KÊNH: ngôi kể và
    văn thể (vd です・ます体) — đó là giọng văn chung của kênh, không đổi theo từng video.
    """
    import copy
    if not det:
        return prof
    p = copy.deepcopy(prof)
    n = p.setdefault("narrator", {})
    age = str(det.get("age") or "").strip()
    n["gender"] = det.get("gender") or n.get("gender", "")
    n["age_band"] = f"{age} tuổi" if age else (det.get("age_band") or n.get("age_band", ""))
    n["persona"] = det.get("persona") or n.get("persona", "")
    # ẢNH cũng phải đổi theo. `character_sheet` là mô tả MẶT NHÂN VẬT CHÍNH dùng cho ảnh master
    # và mọi prompt @REF — để nguyên của hồ sơ thì kịch bản kể chuyện ông 60 tuổi mà ảnh vẫn vẽ
    # cụ bà 80, sai người suốt cả video.
    cs = (det.get("character_sheet") or "").strip()
    if cs:
        p.setdefault("image", {})["character_sheet"] = cs
    return p


_COMMENT_SCHEMA = ('{"diem_cham":["<đoạn nào được khán giả nhắc/xúc động/đồng cảm nhiều nhất, 1 câu>"],'
                   ' "thieu_sot":["<điều khán giả tiếc/hỏi thêm/mong muốn mà video CHƯA có, 1 câu>"]}')


def analyze_comments(prof, transcript, comments):
    """Đọc BÌNH LUẬN THẬT (công khai) dưới video gốc + transcript → rút 2 việc (user chốt 2026-09-10):

    1. `diem_cham` — đoạn nào khán giả nhắc lại/xúc động/đồng cảm nhiều nhất → dùng để NHẤN đúng
       chỗ đó ở cao trào bản mới (khác hẳn khung cố định "mở→伏線→cao trào→kết" cũ: đó là KHUÔN
       chung cho mọi video, cái này là TÍN HIỆU THẬT của đúng video đang clone).
    2. `thieu_sot` — điều khán giả tiếc/hỏi thêm/mong muốn mà bản gốc CHƯA có → gợi ý cho phần
       "30% sáng tạo thêm" của công thức 70/30.

    Vì sao chỉ dùng bình luận, KHÔNG dùng biểu đồ giữ chân (Audience Retention): dữ liệu giữ chân
    là RIÊNG TƯ trong YouTube Studio, chỉ chủ kênh xem được — không có API lấy được của kênh đối
    thủ. Bình luận công khai là tín hiệu GẦN NHẤT có thể lấy hợp pháp.

    Trả None nếu không đủ dữ liệu/LLM lỗi — đây là tín hiệu BỔ TRỢ, KHÔNG được chặn cả video."""
    lang = LANG_NAME.get(prof.get("language", "ja"), prof.get("language"))
    danh_sach = "\n".join(f"- {c[:220]}" for c in comments[:80])
    ask = "\n".join([
        "Bạn đọc BÌNH LUẬN THẬT của khán giả dưới một video kể chuyện, cùng TRANSCRIPT gốc.",
        "Rút ra đúng 2 việc từ bình luận (KHÔNG suy đoán chung chung, phải bám vào bình luận thật "
        "bên dưới), trả DUY NHẤT JSON đúng khuôn, tối đa 5 mục mỗi loại:",
        _COMMENT_SCHEMA,
        f"Viết bằng {lang}.",
        "", "TRANSCRIPT (rút gọn):", transcript[:4000],
        "", f"BÌNH LUẬN ({len(comments)} bình luận, đã sắp theo mức phổ biến):", danh_sach,
    ])
    try:
        r = chat(ask, task="short", max_tokens=1200, min_chars=30)
    except Exception as e:
        print(f"  (B2b bình luận: LLM lỗi {type(e).__name__} {e} → bỏ qua, không chặn tập)")
        return None
    m = re.search(r"\{.*\}", r.text, re.DOTALL)
    if not m:
        print(f"  (B2b bình luận: LLM không trả JSON — {r.text[:120]})")
        return None
    try:
        d = json.loads(m.group(0))
    except Exception as e:
        print(f"  (B2b bình luận: JSON hỏng {e})")
        return None
    d["diem_cham"] = [x for x in (d.get("diem_cham") or []) if x][:5]
    d["thieu_sot"] = [x for x in (d.get("thieu_sot") or []) if x][:5]
    print(f"[B2b] {len(d['diem_cham'])} điểm chạm · {len(d['thieu_sot'])} thiếu sót · "
          f"{r.provider}:{r.model} {r.elapsed:.0f}s")
    return d if (d["diem_cham"] or d["thieu_sot"]) else None


def extract_beats(prof, competitor, n=10):
    """PASS 0 — bóc KHUNG SỰ KIỆN trừu tượng từ bản gốc.

    ⚠️ BÀI HỌC 2026-09-08 (đo 2 lần): đưa NGUYÊN VĂN transcript cho PASS 1 thì model DỊCH SÁT, dù
    prompt cấm rõ ràng và bắt đổi tên/nghề/vùng. QC chấm bám gốc 100% + SAO_CHEP cả 2 lần → rủi ro
    lỗi "sử dụng lại nội dung" của YouTube. Cách duy nhất ăn: **giấu hẳn bản gốc khỏi PASS 1**,
    chỉ đưa khung chức năng (nhịp nào làm gì) — không câu thoại, không tên, không vật đặc trưng.
    """
    rules = [
        "Đọc transcript dưới đây và rút ra KHUNG SỰ KIỆN để người khác viết một câu chuyện MỚI cùng kiểu cảm xúc.",
        f"Trả ĐÚNG {n} nhịp, mỗi nhịp 1 dòng, dạng: 'Nn. <chức năng của nhịp>'.",
        "LUẬT CỨNG khi viết mỗi nhịp:",
        "· Chỉ mô tả CHỨC NĂNG và CẢM XÚC (vd 'người kể bị con hỏi một câu chạm nọc, né tránh').",
        "· TUYỆT ĐỐI KHÔNG chép câu thoại, KHÔNG nêu tên riêng, KHÔNG nêu con số cụ thể, "
        "KHÔNG nêu vật/tục lệ đặc trưng của bản gốc (đó là thứ người viết mới phải TỰ NGHĨ RA).",
        "· Sau danh sách, thêm đúng 2 dòng: 'BÀI HỌC: <một câu>' và 'CẢM XÚC CHÍNH: <vài từ>'.",
        "",
        "TRANSCRIPT:",
        competitor,
    ]
    ask = "\n".join(rules)
    r = _writer_chat(prof, ask, task="short", max_tokens=2000, min_chars=150)
    beats = r.text.strip()
    print(f"[B3 PASS 0] khung {len(beats)} ký tự · {r.provider}:{r.model} {r.elapsed:.0f}s "
          f"(bản gốc {len(competitor):,} chữ được GIẤU khỏi PASS 1)")
    return beats


# Lane thoại nhiều (manga, dmax ≥ 25%): KHÔNG "chỉ giữ câu đắt" — chỉ hạ về gần ngưỡng, giữ掛け合い.
# Đo thật Lane G ep01 2026-09-20: prompt satori hạ 49% → 13% (2 khúc còn 2–5%), mất chất manga.
DIALOG_ASK_MANGA_JA = (
        "次の台本は登場人物2人の掛け合いが多すぎます。「」の会話の割合を全体の約{dtarget}%（{dlo}〜{dmax}%）まで"
        "減らしてください。",
        "・掛け合いのテンポは残す。削るのは【説明的な長い台詞】だけで、それを短い地の文（心の声・状況描写）に"
        "置き換える。短い一言の応酬はそのまま「」で残す。",
        "・長さは変えない（増減5%以内）。語り口・段落構成・出来事の順序はそのまま。",
        "・説明や前置きを書かず、書き換えた本文だけを出力する。")

DIALOG_ASK = {
 "ja": ("次の台本の「」の会話を、意味を変えずに【地の文の語り】へ書き換えてください。",
        "・会話文の割合を全体の{dmax}%以下にすること。重要な一言だけ「」で残し、残りは"
        "「〜と言われました」「〜と告げたのです」のような間接話法にする。",
        "・長さは変えない（増減5%以内）。語り口・段落構成・出来事の順序はそのまま。",
        "・説明や前置きを書かず、書き換えた本文だけを出力する。"),
 "ko": ("아래 대본의 대화문을 뜻을 바꾸지 말고 서술문으로 고쳐 주세요.",
        "・대화문 비율을 전체의 {dmax}% 이하로.",
        "・길이는 그대로(±5%). 사건 순서와 문체는 유지.",
        "・설명 없이 본문만 출력."),
 "en": ("Rewrite the quoted dialogue below into narration, keeping the meaning.",
        "- Quoted dialogue must be at most {dmax}% of the text; keep only the most important line "
        "in quotes and turn the rest into reported speech.",
        "- Keep the same length (within 5%), same voice, same order of events.",
        "- Output the rewritten text only."),
}


def reduce_dialogue(prof, text, chunk_chars=2500, workers=3):
    """Hạ tỉ lệ hội thoại mà GIỮ nguyên độ dài — việc mà `trim_chunked` không làm nổi.

    Đo thật 2026-09-08 (ep09): bản nháp 21% hội thoại, chế độ 'giữ độ dài sửa nhịp' chia 2 khúc to
    trả về bản TỆ HƠN → gate mãi không qua. Ở đây tách riêng đúng một việc, khúc nhỏ, và chỉ nhận
    khúc nào thật sự giảm được hội thoại."""
    from concurrent.futures import ThreadPoolExecutor
    g = profiles.gate(prof)
    dmax = int(g["dialogue_ratio_max"] * 100)
    lang = prof.get("language", "ja")
    if lang == "ja" and g["dialogue_ratio_max"] >= 0.25:
        head = [x.format(dmax=dmax, dtarget=int(dmax * 0.85), dlo=int(dmax * 0.7)) for x in DIALOG_ASK_MANGA_JA]
    else:
        head = [x.format(dmax=dmax) for x in DIALOG_ASK.get(lang, DIALOG_ASK["en"])]

    SEP = "\n\n"
    units = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts, cur = [], []
    n = 0
    for u in units:
        cur.append(u)
        n += len(u)
        if n >= chunk_chars:
            parts.append(SEP.join(cur))
            cur, n = [], 0
    if cur:
        parts.append(SEP.join(cur))
    print(f"[B3 hạ hội thoại] {len(parts)} khúc · mục tiêu ≤{dmax}%")

    def one(i_p):
        i, part = i_p
        before = measure(part)["dialogue_ratio"]
        if before * 100 <= dmax:
            return i, part, before, before
        try:
            r = chat("\n".join(head + ["", part]), task="script", temperature=0.4,
                     min_chars=int(len(part) * 0.75), require_sentence_end=True, verbose=False)
        except Exception as e:
            print(f"   khúc {i+1}: hỏng ({type(e).__name__}) → giữ nguyên")
            return i, part, before, before
        new = normalize_paragraphs(strip_markers(r.text))
        after = measure(new)["dialogue_ratio"]
        keep = after < before and 0.8 <= len(new) / max(len(part), 1) <= 1.2
        print(f"   khúc {i+1}: hội thoại {before:.0%} → {after:.0%} "
              f"({'nhận' if keep else 'BỎ'}), {len(part)}→{len(new)} chữ")
        return i, (new if keep else part), before, (after if keep else before)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = sorted(ex.map(one, list(enumerate(parts))))
    return SEP.join(p for _, p, _, _ in res)


COMMA_ASK = {
 "ja": ["次の台本は一文が長く、読点が多すぎます。読点の多い長文を【短い文に分割】してください。",
        "・1文あたりの読点を{hi}個以下にする。意味・順序・語り口は変えない。",
        "・「、」を「。」に替えて文を切る、または一文を二文に分ける。語尾は です・ます 調のまま。",
        "・長さは変えない（増減5%以内）。説明を書かず、直した本文だけを出力する。"],
 "ko": ["아래 대본은 한 문장이 너무 길고 쉼표가 많습니다. 긴 문장을 짧은 문장으로 나눠 주세요.",
        "・문장당 쉼표 {hi}개 이하. 뜻과 순서는 그대로.",
        "・길이는 그대로(±5%). 설명 없이 본문만 출력."],
 "en": ["The script below has long sentences with too many commas. Split them into shorter sentences.",
        "- At most {hi} commas per sentence. Keep meaning, order and voice unchanged.",
        "- Keep the same length (within 5%). Output the rewritten text only."],
}


def reduce_commas(prof, text, chunk_chars=2500, workers=3):
    """Hạ số phẩy/câu bằng cách TÁCH CÂU DÀI — việc mà chế độ 'giữ độ dài sửa nhịp' không làm nổi.

    Cùng căn bệnh với hội thoại (đo thật ep12: 6,92 phẩy/câu, chia 2 khúc to → model làm ngơ, gate
    trượt, tool dừng). Ở đây tách riêng đúng một việc, khúc nhỏ, chỉ nhận khúc nào thật sự giảm."""
    from concurrent.futures import ThreadPoolExecutor
    g = profiles.gate(prof)
    hi = int(g["comma_per_sentence"][1])
    lang = prof.get("language", "ja")
    head = [x.format(hi=hi) for x in COMMA_ASK.get(lang, COMMA_ASK["en"])]

    SEP = "\n\n"
    units = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts, cur, n = [], [], 0
    for u in units:
        cur.append(u); n += len(u)
        if n >= chunk_chars:
            parts.append(SEP.join(cur)); cur, n = [], 0
    if cur:
        parts.append(SEP.join(cur))
    print(f"[B3 tách câu dài] {len(parts)} khúc · mục tiêu ≤{hi} phẩy/câu")

    def one(i_p):
        i, part = i_p
        before = measure(part)["comma_per_sentence"]
        if before <= hi:
            return i, part
        try:
            r = chat("\n".join(head + ["", part]), task="script", temperature=0.4,
                     min_chars=int(len(part) * 0.75), require_sentence_end=True, verbose=False)
        except Exception as e:
            print(f"   khúc {i+1}: hỏng ({type(e).__name__}) → giữ nguyên")
            return i, part
        new = normalize_paragraphs(strip_markers(r.text))
        after = measure(new)["comma_per_sentence"]
        keep = after < before and 0.8 <= len(new) / max(len(part), 1) <= 1.2
        print(f"   khúc {i+1}: {before:.2f} → {after:.2f} phẩy/câu ({'nhận' if keep else 'BỎ'}), "
              f"{len(part)}→{len(new)} chữ")
        return i, (new if keep else part)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = sorted(ex.map(one, list(enumerate(parts))))
    return SEP.join(p for _, p in res)


def write_script(prof, competitor, minutes=None, series_ctx="", on_chunk=None, max_trim=2,
                 comment_insight=None):
    """2 PASS + gate. Trả dict(text, passes, gate_problems, metrics).

    `comment_insight` — kết quả `analyze_comments()` (B2b), None nếu tập không có/lỗi. Chỉ ảnh
    hưởng PASS 1 (định hướng viết); các gate/QC phía sau không đổi."""
    minutes = minutes or profiles.target_minutes(prof)
    target = profiles.target_chars(prof, minutes)
    skill = _skill_text(prof, "script")
    two_pass = (prof.get("script", {}) or {}).get("two_pass", True)
    log = []

    # PASS 0: bóc khung rồi GIẤU bản gốc. Tắt bằng script.use_raw_source=true trong profile.
    source = competitor
    if not (prof.get("script", {}) or {}).get("use_raw_source"):
        try:
            source = extract_beats(prof, competitor)
            log.append(f"pass0 khung {len(source)} ký tự")
        except Exception as e:
            print(f"  ⚠️ PASS 0 hỏng ({type(e).__name__}) → đành dùng bản gốc (RỦI RO sao chép)")
    ask = int(target * 1.3)          # xin dài hơn 30% vì chỉ chiều NÉN là đáng tin
    print(f"[B3 PASS 1] {prof['id']} · mục tiêu {minutes}' = {target:,} chữ "
          f"(char_rate {profiles.char_rate(prof)}) · xin bản nháp ≥ {ask:,} chữ")
    r1 = _writer_chat(prof, _pass1_prompt(prof, source, minutes, series_ctx, ask, comment_insight), system=skill, task="script",
              min_chars=int(target * 0.5), require_sentence_end=True, on_chunk=on_chunk)
    text = normalize_paragraphs(strip_markers(r1.text))
    log.append(f"pass1 {r1.provider}:{r1.model} {r1.chars:,} chữ {r1.elapsed:.0f}s")
    text = _go_cat_neu_ja(prof, text)
    pass1_raw = text
    # PASS 1 dao động mạnh (đo thật: 7.769 / 9.388 / 13.108 / 14.480 chữ cùng 1 nguồn).
    # Ngắn thì KHÔNG nới được → viết lại 1 lần, xin dài hơn nữa, giữ bản dài hơn.
    if measure(text)["chars"] < target:
        print(f"  ↻ bản nháp ngắn ({measure(text)['chars']:,} < {target:,}) → viết lại 1 lần, "
              f"xin ≥ {int(target*1.6):,} chữ")
        r1b = _writer_chat(prof, _pass1_prompt(prof, source, minutes, series_ctx, int(target * 1.6), comment_insight),
                   system=skill, task="script", min_chars=int(target * 0.5),
                   require_sentence_end=True, temperature=1.0, on_chunk=on_chunk)
        alt = _go_cat_neu_ja(prof, normalize_paragraphs(strip_markers(r1b.text)))
        log.append(f"pass1b {r1b.provider}:{r1b.model} {r1b.chars:,} chữ {r1b.elapsed:.0f}s")
        if measure(alt)["chars"] > measure(text)["chars"]:
            text = alt
            pass1_raw = alt

    if two_pass:
        for i in range(1, max_trim + 1):
            bad, m = check(prof, text, minutes)
            if not bad:
                break
            print(f"[B3 PASS {i+1}] chưa đạt → " + " | ".join(bad))
            # độ dài đã ổn mà chỉ sai nhịp → GIỮ độ dài, chỉ viết lại nhịp (đừng đòi nén nữa)
            keep_len = not any(b.startswith(("DÀI", "NGẮN")) for b in bad)
            try:
                new = _go_cat_neu_ja(prof, trim_chunked(prof, text, target, minutes, keep_length=keep_len))
            except LLMError as e:
                # Bài học 2026-09-20 (Lane G ep01): khúc nén phình gấp đôi → LLMError văng cả B3, MẤT bản nháp
                # 6.913 chữ chỉ còn 1 lỗi 、. Nén hỏng thì giữ bản đang có, không vứt.
                print(f"  ⚠️ nén khúc hỏng ({e}) → giữ bản trước, dừng vòng nén")
                log.append(f"pass{i+1} nén hỏng: {str(e)[:80]}")
                break
            new_bad, nm = check(prof, new, minutes)
            log.append(f"pass{i+1} {'giữ-dài' if keep_len else 'nén'}-khúc {nm['chars']:,} chữ "
                       f"({len(bad)}→{len(new_bad)} lỗi)")
            # nhận bản mới nếu ÍT LỖI GATE HƠN; bằng nhau thì lấy bản gần mục tiêu hơn
            better = (len(new_bad) < len(bad) or
                      (len(new_bad) == len(bad) and
                       abs(nm["chars"] - target) < abs(measure(text)["chars"] - target)))
            # ⚠️ ĐỘ DÀI LÀ ĐƯỜNG MỘT CHIỀU. Công cụ duy nhất ở đây là bước NÉN — nó rút ngắn được,
            # không nới dài được (`trim_chunked` gặp target ≥ hiện tại là tự chuyển sang giữ nguyên
            # độ dài). Nên một khi bản mới TỤT XUỐNG DƯỚI mục tiêu thì không còn đường quay lại.
            # Đo thật ep03: bản 12.110 chữ có 3 lỗi, nén ra 9.026 chữ còn 2 lỗi ⇒ "ít lỗi hơn" nên
            # được nhận — đổi 3.000 chữ lấy một lỗi nhịp, rồi mắc kẹt ở NGẮN −12% không gỡ được,
            # cả lượt B3 hỏng. Đếm lỗi coi "DÀI +12%" ngang một lỗi nhịp, trong khi hai thứ đó
            # KHÔNG cùng hạng: lỗi nhịp còn sửa được ở lượt sau, thiếu chữ thì không.
            if better and nm["chars"] < target * 0.98 <= measure(text)["chars"]:
                # Nén hụt tay thì ĐỪNG BỎ CUỘC — nén lại với hạn mức đã bù đúng phần hụt đo được.
                # (Xin 10.634 mà ra 9.026 ⇒ model cắt quá tay 15% ⇒ lượt sau xin 10.634×1,18.)
                bu = min(1.35, target / max(nm["chars"], 1))
                print(f"  ⚠️ bản mới {nm['chars']:,} chữ TỤT DƯỚI mục tiêu {target:,} "
                      f"(bản cũ {measure(text)['chars']:,}) → nén lại, bù hạn mức ×{bu:.2f}")
                try:
                    new2 = _go_cat_neu_ja(prof, trim_chunked(prof, text, int(target * bu), minutes))
                except LLMError as e:
                    print(f"  ⚠️ nén bù hỏng ({e}) → bỏ lượt bù")
                    better = False
                    continue
                nb2, nm2 = check(prof, new2, minutes)
                log.append(f"pass{i+1}b nén-bù {nm2['chars']:,} chữ ({len(nb2)} lỗi)")
                if nm2["chars"] >= target * 0.98 and len(nb2) <= len(bad):
                    new, new_bad, nm = new2, nb2, nm2
                else:
                    print(f"     lượt bù ra {nm2['chars']:,} chữ / {len(nb2)} lỗi → vẫn không dùng")
                    better = False
            if better:
                text, bad = new, new_bad
                print(f"  → nhận bản mới: {nm['chars']:,} chữ, còn {len(new_bad)} lỗi")
            else:
                print(f"  ⚠️ bản mới KHÔNG tốt hơn ({len(new_bad)} lỗi) → giữ bản trước, dừng")
                break

    # Hội thoại quá nhiều là lỗi RIÊNG, `trim_chunked` không xử được (đo thật ep09: 21% đứng yên).
    bad, m = check(prof, text, minutes)
    if any(b.startswith("NHỊP") for b in bad):
        alt = reduce_commas(prof, text)
        alt_bad, am = check(prof, alt, minutes)
        log.append(f"tách-câu {m['comma_per_sentence']}→{am['comma_per_sentence']} phẩy/câu "
                   f"({len(bad)}→{len(alt_bad)} lỗi)")
        if len(alt_bad) < len(bad):
            text, bad, m = alt, alt_bad, am
            print(f"  → nhận bản tách câu: {am['comma_per_sentence']} phẩy/câu, còn {len(alt_bad)} lỗi")
        else:
            print(f"  ⚠️ tách câu không cải thiện ({len(alt_bad)} lỗi) → giữ bản trước")

    bad, m = check(prof, text, minutes)
    if any(b.startswith("HỘI THOẠI") for b in bad):
        alt = reduce_dialogue(prof, text)
        alt_bad, am = check(prof, alt, minutes)
        log.append(f"hạ-hội-thoại {m['dialogue_ratio']:.0%}→{am['dialogue_ratio']:.0%} "
                   f"({len(bad)}→{len(alt_bad)} lỗi)")
        if len(alt_bad) < len(bad):
            text, bad, m = alt, alt_bad, am
            print(f"  → nhận bản hạ hội thoại: {am['dialogue_ratio']:.0%}, còn {len(alt_bad)} lỗi")
        else:
            print(f"  ⚠️ hạ hội thoại không cải thiện ({len(alt_bad)} lỗi) → giữ bản trước")

    bad, m = check(prof, text, minutes)
    print(f"[B3 GATE] {m['chars']:,} chữ ≈ {m['minutes']}' · {m['comma_per_sentence']} phẩy/câu · "
          f"hội thoại {m['dialogue_ratio']:.0%} · " + ("ĐẠT" if not bad else "CÒN: " + " | ".join(bad)))
    return {"text": text, "passes": log, "gate_problems": bad, "metrics": m,
            "beats": source if source is not competitor else "", "pass1_raw": pass1_raw}


# ============================================================ B5 — PROMPT ẢNH
STOP_W = {"with", "and", "the", "her", "his", "into", "from", "that", "wearing"}


def _sheet_tokens(sheet):
    """Token đặc trưng của CHARACTER SHEET. Dùng TOKEN chứ không ghép chuỗi — sheet trong prompt
    luôn bị chèn dấu phẩy/đổi thứ tự nên so khớp cả cụm sẽ luôn trượt (đã dính: báo 0/30)."""
    toks = [w.strip(",.;:'\"").lower() for w in re.split(r"\s+", sheet) if len(w) > 3]
    return [t for t in toks if t and t not in STOP_W][:8]


def _has_character(line, tokens, need=3):
    low = line.lower()
    return sum(1 for t in tokens if t in low) >= need


# ---------------------------------------------------------------- WORLD LOCK
# Lỗi đã thấy ở dự án khác (user chỉ ra 2026-09-08): cùng 1 video mà cảnh này nhà hiện đại, cảnh kia
# cổ trang samurai, cảnh khác xe tải Thế chiến 2 → xem như 3 phim khác nhau. REF-LOCK chỉ khoá KHUÔN
# MẶT, KHÔNG khoá bối cảnh. Nên phải có WORLD LOCK: 1 câu mô tả thế giới, DÁN BẰNG CODE vào mọi
# prompt (không nhờ model tự nhớ — nó quên từ dòng thứ 20 trở đi).
ERA_BREAKERS = (
    "samurai", "kimono wedding", "feudal", "edo period", "meiji", "taisho", "shogun", "geisha",
    "ronin", "katana", "castle town", "thatched village", "oil lamp street", "horse cart",
    "ox cart", "world war", "wwii", "ww2", "1940s", "1930s", "wartime", "soldier", "military truck",
    "steam train", "victorian", "medieval", "ancient",
)


def world_lock(prof, script):
    """Câu khoá thế giới cho CẢ video. Ưu tiên profile; không có thì đọc kịch bản suy ra 1 lần."""
    img = prof.get("image", {}) or {}
    if img.get("world_lock"):
        return img["world_lock"]
    ask = ("Read the story below and state the ONE consistent visual world it happens in. "
           "Reply ONLY compact JSON: "
           '{"era":"","region":"","season":"","home":"","clothing":"","tech":""} '
           "— era like 'contemporary 2020s', region like 'rural Nagano, Japan', home like "
           "'post-war wooden house with tatami and shoji', clothing like 'modern everyday clothes', "
           "tech like 'smartphones, small modern cars'. English, short noun phrases."
           "\n\nSTORY:\n" + script[:6000])
    try:
        r = chat(ask, task="short", max_tokens=400, min_chars=20)
        d = json.loads(re.search(r"\{.*\}", r.text, re.DOTALL).group(0))
    except Exception as e:
        print(f"  ⚠️ không suy được WORLD LOCK ({type(e).__name__}) → dùng mặc định của profile")
        return img.get("world_lock_fallback", "")
    w = (f"consistent world: {d.get('era','')}, {d.get('region','')}, {d.get('season','')}; "
         f"{d.get('home','')}; {d.get('clothing','')}; {d.get('tech','')}; "
         f"no period costume, no historical or wartime elements")
    return re.sub(r"\s*,\s*,", ",", re.sub(r"\s{2,}", " ", w)).strip(" ,;")


def _apply_world(line, world):
    if not world:
        return line
    return line if world[:28].lower() in line.lower() else f"{line}, {world}"


def era_violations(lines, world=""):
    """Dòng nào lạc thời đại → bắt TRƯỚC khi tiêu tiền ảnh."""
    ok = world.lower()
    out = []
    for i, l in enumerate(lines):
        low = l.lower()
        hit = [w for w in ERA_BREAKERS if w in low and w not in ok]
        if hit:
            out.append((i + 1, hit, l[:80]))
    return out


GUARD_MINORS = ("Children: gpti2/Azure rejects EVERY prompt containing a child, baby, toddler "
                "or schoolchild. So when the line really needs a child on screen, tag that "
                "block CHILD instead of REF/SCENE — a different image service draws it. "
                "Never put a child inside a REF or SCENE prompt.")


def _sb_batch_prompt(prof, bl, sheet, style, n_total, world):
    n0 = prof.get("narrator", {}) or {}
    head = [
        "You write image prompts for an AI image generator, for a narrated story video.",
        "Below are NUMBERED NARRATION BLOCKS. The video shows image #k exactly while block #k is read,",
        "so each prompt MUST depict what THAT block says — same moment, same place, same action.",
        f"Reply with EXACTLY {len(bl)} lines, format: '<number>| REF, SCENE or CHILD | <prompt>'.",
        "Put REF **only** when the MAIN CHARACTER below is the visible subject of that block.",
        "Put SCENE for everything else — and SCENE does NOT mean 'empty picture':",
        "  · if the line is about OTHER PEOPLE (a son, a daughter, a nurse, two people arguing), "
        "SHOW THOSE PEOPLE doing exactly what the line says — generic and unnamed, but clearly "
        "present, with the right age, number and action. Do NOT replace them with the main "
        "character and do NOT fall back to an empty room or street.",
        "  · only when the line truly has no person (an object, weather, a place) make it people-free.",
        "Put CHILD when the block needs a child/baby/schoolchild visible on screen.",
        "Judge this from the narration itself, never by a quota. Getting this wrong is the worst "
        "possible error: a REF line always renders the main character, so a block about someone "
        "else marked REF will show the wrong person entirely.",
        "Each prompt: 25-45 words, STARTS with the shot type (WIDE/MEDIUM/CLOSE-UP/DETAIL),",
        f"ENDS with this style tail: '{style}'.",
        f"MAIN CHARACTER: '{sheet}'.",
        "Every REF prompt MUST repeat that character description VERBATIM.",
        "Only blocks that truly have no person (objects, rooms, weather, hands) stay people-free.",
        "Other people are generic and unnamed but must be SHOWN when the line is about them "
        "(right age, right number, doing the action described) — never swapped for the main "
        "character, never replaced by an empty scene.",
        f"Never depict: {', '.join(prof.get('blocklist') or []) or 'gore, nudity, children'}.",
        GUARD_MINORS,
        "Do NOT render readable text, signs, or phone screens unless the block explicitly describes them.",
    ]
    if world:
        head.append(f"EVERY prompt must fit this one consistent world: {world}")
    body = [f"{i}| {t}" for i, _, _, t in bl]
    return "\n".join(head + ["", "NARRATION BLOCKS:"] + body)


def write_storyboard_prompts(prof, srt_path, sheet, style, world, n=None, batch=25, workers=3):
    """1 prompt cho MỖI KHỐI CUE — ảnh #i chắc chắn khớp lời #i (skill youtube-image-prompts §ĐỒNG BỘ).

    Thay cho cách cũ 'đưa cả kịch bản, bảo rải đều': cách cũ để model tự quyết mật độ nên ảnh trôi
    trễ so với lời ở khúc giữa (đo thật). Ở đây chia cue GIỐNG HỆT assemble rồi bám từng khối."""
    from concurrent.futures import ThreadPoolExecutor
    import storyboard as sb

    cues = sb.parse_cues(srt_path)
    if not cues:
        return None
    img = prof.get("image", {}) or {}
    if not n:
        spi = float(img.get("seconds_per_image", 15) or 15)
        n = max(20, int(round((cues[-1][1] - cues[0][0]) / spi)))
    bl = sb.blocks(cues, n)
    groups = [bl[i:i + batch] for i in range(0, len(bl), batch)]
    print(f"[B5] STORYBOARD: {len(cues)} cue → {len(bl)} khối ảnh · {len(groups)} lô × {batch}")

    def do(g):
        r = chat(_sb_batch_prompt(prof, g, sheet, style, len(bl), world), task="short",
                 temperature=0.7, max_tokens=9000, min_chars=len(g) * 40, verbose=False)
        out = {}
        for line in r.text.splitlines():
            m = re.match(r"\s*\[?(\d{1,4})\]?\s*[|.):]\s*(REF|SCENE|CHILD)?\s*\|?\s*(.+)", line, re.I)
            if m and len(m.group(3).split()) >= 8:
                out[int(m.group(1))] = ((m.group(2) or "SCENE").lower(), m.group(3).strip())
        return out

    got = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for d in ex.map(do, groups):
            got.update(d)
    miss = [i for i, _, _, _ in bl if i not in got]
    if miss:
        print(f"  ⚠️ thiếu {len(miss)} khối → điền bằng cảnh trung tính")
        for i in miss:
            got[i] = ("scene", f"WIDE atmospheric establishing shot of the setting, no readable text, {style}")
    return [got[i] for i, _, _, _ in bl]


PAT = r"\s*\[?(\d{1,4})\]?\s*\|\s*(OK|FIX)\s*\|?\s*(REF|SCENE|CHILD)?\s*\|?\s*(.*)"


def qc_prompts(prof, bl, prompts, tags, sheet, batch=20, workers=3):
    """QC PROMPT ↔ LỜI ngay ở B5 — bằng CHỮ, TRƯỚC khi tiêu tiền ảnh.

    Rẻ hơn mọi cách khác: soi ảnh sau khi gen thì tiền đã mất; chấm khung hình sau khi dựng thì
    còn mất thêm 7 phút encode. Ở đây chỉ là văn bản, gemini-3.8-flash, ~1 phút cho 126 khối.
    Kiểm 2 việc: (1) prompt có tả đúng việc lời đang kể không, (2) khối này có ĐÁNG thấy mặt nhân
    vật chính không (cờ REF sai = vẽ ra nhầm người, lỗi nặng nhất — đo thật ep08 khớp 2,2/5).
    Trả (prompts_mới, refs_mới, báo cáo)."""
    from concurrent.futures import ThreadPoolExecutor
    groups = []
    for i in range(0, len(bl), batch):
        groups.append([(j + 1, bl[j][3], prompts[j], tags[j]) for j in range(i, min(i + batch, len(bl)))])

    def do(g):
        body = []
        for n, line, pr, rf in g:
            body.append(f"{n}| NARRATION: {line[:180]}")
            body.append(f"{n}| PROMPT ({str(rf).upper()}): "
                        f"{re.sub(r'^@REF ', '', pr)[:260]}")
        ask = "\n".join([
            "You check image prompts against the narration line they will be shown with.",
            f"MAIN CHARACTER of this video: {sheet[:200]}",
            "For each numbered pair judge two things:",
            "  (a) does the PROMPT depict what the NARRATION says — same moment, place, subject?",
            "  (b) is the tag right? REF = the MAIN CHARACTER is the visible subject of that line. "
            "SCENE = anything else.",
            "  (c) if the line is about OTHER PEOPLE, does the prompt actually SHOW those people "
            "doing that action (right number and age)? An empty room/street, or the main character "
            "standing in for them, is WRONG — mark FIX and rewrite it to show them.",
            "A wrong REF tag is the worst error: it renders the main character in a scene that is "
            "about someone else.",
            "Reply one line per pair, nothing else:",
            "  '<n>| OK'                                   if both are right",
            "  '<n>| FIX | REF, SCENE or CHILD | <corrected English prompt, 25-45 words>'   otherwise.",
            "Keep the corrected prompt in the same style; start with the shot type.",
            GUARD_MINORS,
            "", *body])
        r = chat(ask, task="short", temperature=0.3, max_tokens=8000,
                 min_chars=len(g) * 5, verbose=False)
        out = {}
        for line in r.text.splitlines():
            m = re.match(PAT, line.strip(), re.I)
            if not m:
                continue
            n, verdict = int(m.group(1)), m.group(2).upper()
            if verdict == "OK":
                out[n] = None
            elif len(m.group(4).split()) >= 8:
                out[n] = ((m.group(3) or "SCENE").lower(), m.group(4).strip())
        if not out:
            # Không đọc được dòng nào = lô này CHƯA HỀ được kiểm. Im lặng ở đây sẽ thành
            # "0 lỗi" giả — đúng bẫy đã dính ở dự án thẻ. Phải kêu to.
            ls = r.text.splitlines()
            print(f"  ⚠️ lô {g[0][0]}-{g[-1][0]}: QC trả về định dạng lạ, KHÔNG kiểm được. "
                  f"dòng0={ls[0]!r} khớp={bool(re.match(PAT, ls[0].strip(), re.I)) if ls else None}")
        return out

    got = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for d in ex.map(do, groups):
            got.update(d)
    newp, newr = list(prompts), list(tags)
    fixed, flag = 0, 0
    for n, v in got.items():
        i = n - 1
        if v is None or not (0 <= i < len(newp)):
            continue
        rf, txt = v
        if rf != newr[i]:
            flag += 1
        newr[i] = rf
        newp[i] = txt
        fixed += 1
    checked = len(got)
    print(f"[B5Q-prompt] soi {checked}/{len(bl)} khối · sửa {fixed} prompt "
          f"(trong đó {flag} khối đổi cờ REF/SCENE = suýt vẽ nhầm người)")
    return newp, newr, {"checked": checked, "fixed": fixed, "reflip": flag}


def write_img_prompts(prof, script, n=None, duration_sec=None, sheet=None, face_share=0.6,
                     srt=None):
    """Sinh N prompt ảnh (mỗi dòng 1 prompt) + tách nhóm cần REF-LOCK. Trả dict.

    `sheet`: CHARACTER SHEET của TẬP này (ghi đè sheet HOST trong profile). Cần vì nhiều tập kể về
    nhân vật khác HOST — không ép thì model tả mỗi cảnh một người, REF-LOCK vô dụng (đo thật: chỉ
    4/30 prompt giữ sheet khi để model tự quyết).
    `face_share`: tỉ lệ tối thiểu prompt phải có nhân vật chính (để đủ ảnh dùng REF-LOCK).
    """
    img = prof.get("image", {}) or {}
    sheet = sheet or img.get("character_sheet", "")
    style = img.get("style_suffix", "")
    spi = float(img.get("seconds_per_image", 15) or 15)
    if not n:
        secs = duration_sec or profiles.target_minutes(prof) * 60
        n = max(20, int(round(secs / spi)))
    n_face = int(round(n * face_share))
    prompt = (
        f"You write image prompts for an AI image generator, for a narrated story video.\n"
        f"Write EXACTLY {n} prompts, ONE PER LINE, no numbering, no markdown, no blank lines.\n"
        f"Each line = one self-contained English prompt of 25–45 words that STARTS with the shot type "
        f"(WIDE/MEDIUM/CLOSE-UP/DETAIL) and ENDS with this exact style suffix: '{style}'.\n\n"
        f"MAIN VISIBLE CHARACTER of this episode (the person the audience must recognise in every "
        f"scene she/he appears in): '{sheet}'.\n"
        f"HARD RULE: AT LEAST {n_face} of the {n} prompts must show this character, and EVERY prompt "
        f"showing them must repeat that character description VERBATIM, word for word. Do not invent "
        f"other described people: secondary people must stay generic and unnamed "
        f"(e.g. 'a funeral director in a dark suit', seen from behind or out of focus).\n"
        f"The remaining prompts are scenery/object shots with no people.\n\n"
        f"Follow the story order of the script below, spreading the {n} shots evenly across it.\n"
        f"Never depict: {', '.join(prof.get('blocklist') or []) or 'gore, nudity, babies'}.\n\n"
        f"SCRIPT:\n{script}")
    world = world_lock(prof, script)
    if world:
        print(f"[B5] WORLD LOCK: {world[:120]}")
    lines, sb_ref, sb_tag = None, None, None
    if srt and Path(srt).exists():
        try:
            pairs = write_storyboard_prompts(prof, srt, sheet, style, world, n)
            if pairs:
                sb_tag = [a for a, _ in pairs]
                sb_ref = [a == "ref" for a in sb_tag]
                lines = [t for _, t in pairs]
                if (prof.get("image", {}) or {}).get("qc_prompts", True):
                    import storyboard as _sb
                    _bl = _sb.blocks(_sb.parse_cues(srt), len(pairs))
                    if len(_bl) == len(pairs):
                        lines, sb_tag, _ = qc_prompts(prof, _bl, lines, sb_tag, sheet or "")
                        sb_ref = [a == "ref" for a in sb_tag]
        except Exception as e:
            print(f"  ⚠️ storyboard hỏng ({type(e).__name__} {e}) → quay về cách rải đều")
    if not lines:
        r = chat(prompt, task="short", temperature=0.8, max_tokens=24000, min_chars=n * 40)
        lines = [l.strip() for l in r.text.splitlines() if l.strip()]
        lines = [re.sub(r"^\s*\d+[\.\)]\s*", "", l) for l in lines]
        lines = [l for l in lines if len(l.split()) >= 10]

    keep_child = set(i for i, a in enumerate(sb_tag or []) if a == "child")
    fixed = list(lines)
    if keep_child:
        idx = [i for i in range(len(fixed)) if i not in keep_child]
        sub = _fix_policy(prof, [fixed[i] for i in idx])
        for k, i in enumerate(idx):
            fixed[i] = sub[k]
    else:
        fixed = _fix_policy(prof, fixed)
    fixed = [_ascii_prompt(l) for l in fixed]          # bỏ chữ Nhật lọt vào prompt tiếng Anh
    if world:
        fixed = [_apply_world(l, world) for l in fixed]
    bad_era = era_violations(fixed, world)
    if bad_era:
        print(f"  ⚠️ {len(bad_era)} prompt LẠC THỜI ĐẠI (bối cảnh sẽ nhảy phim) → nhờ viết lại:")
        for i, hit, txt in bad_era[:5]:
            print(f"     dòng {i}: {'/'.join(hit)} — {txt}")
        fixed = _rewrite_era(prof, fixed, bad_era, world)
    # Khối nào THẤY MẶT nhân vật chính: ưu tiên cờ REF do storyboard quyết theo LỜI KỂ.
    # (Cách cũ đo token trên prompt + ép face_share cứng → cảnh kể về NGƯỜI KHÁC cũng bị gắn @REF,
    #  mà @REF thì luôn vẽ ra nhân vật chính → sai hẳn người. Đo thật ep08: khớp ảnh-lời 2,2/5.)
    if sb_ref and len(sb_ref) == len(fixed):
        face = [l for l, r in zip(fixed, sb_ref) if r]
    else:
        toks = _sheet_tokens(sheet) if sheet else []
        face = [l for l in fixed if toks and _has_character(l, toks)]
    scene = [l for l in fixed if l not in face]
    # Đánh dấu '@REF ' đầu dòng cho cảnh THẤY MẶT — gen_images.py đọc marker này để khoá mặt
    # (110đ/ảnh) còn cảnh vật đi text-only (50đ). 1 file duy nhất, không tách 2 file.
    # ⚠️ Ảnh @REF đi qua chế độ EDIT của gpti2 → nó bê luôn BỐI CẢNH của ảnh master, không chỉ khuôn
    # mặt (đo thật ep08: prompt 'waiting in hospital' vẫn ra đúng căn nhà của ảnh master). Phải nói
    # thẳng: giữ MẶT, đổi HẲN cảnh. (Skill youtube-image-prompts đã dặn, tool trước đây bỏ sót.)
    REF_TAIL = ("the SAME person as the reference image with an identical face, "
                "but in a COMPLETELY NEW scene: do not reuse the background, room, furniture or "
                "framing of the reference image")
    marked = []
    for i, l in enumerate(fixed):
        if sb_tag and i < len(sb_tag) and sb_tag[i] == "child":
            marked.append("@GROK " + l)      # trẻ em → Grok Imagine (gpti2/Azure chặn mọi minor)
        elif l in face:
            marked.append("@REF " + l + ", " + REF_TAIL)
        else:
            marked.append(l)
    ratio = len(face) / max(len(fixed), 1)
    print(f"[B5] {len(fixed)} prompt · {len(face)} có mặt nhân vật ({ratio:.0%}, @REF) · "
          f"{len(scene)} cảnh vật")
    if not sb_ref and ratio < face_share * 0.6:
        print(f"  ⚠️ quá ít prompt giữ CHARACTER SHEET ({ratio:.0%} < {face_share:.0%} yêu cầu) → "
              f"nhân vật sẽ KHÔNG nhất quán. Kiểm lại: nhân vật chính của tập này có đúng là "
              f"'{sheet[:40]}...' không? Nếu không, truyền --sheet của tập.")
    return {"prompts": marked, "raw": fixed, "face": face, "scene": scene, "n_requested": n,
            "face_ratio": round(ratio, 2), "sheet": sheet, "world": world,
            "storyboard": bool(sb_ref)}


_CJK_IN_PROMPT = re.compile(r"[぀-ヿ㐀-䶿一-鿿]+")


def _ascii_prompt(line):
    """Prompt ảnh phải 100% tiếng Anh: ký tự Nhật lọt vào vừa tính token đắt gấp ~6 lần
    (skill gpti2) vừa làm model hiểu lệch. Đã dính: 'old惣菜deli counter'."""
    return re.sub(r"\s{2,}", " ", _CJK_IN_PROMPT.sub(" ", line)).strip()


def _rewrite_era(prof, lines, bad, world):
    """Viết lại các dòng lạc thời đại, giữ nguyên bố cục cảnh."""
    idx = [i - 1 for i, _, _ in bad]
    joined = "\n".join(lines[i] for i in idx)
    ask = (f"Rewrite each image prompt below so it fits STRICTLY this world: {world}\n"
           f"Keep the same shot type, same subject and same emotional beat; only replace the "
           f"anachronistic elements with everyday modern equivalents. "
           f"Reply with EXACTLY {len(idx)} lines, one rewritten prompt per line, nothing else."
           f"\n\n{joined}")
    try:
        r = chat(ask, task="short", max_tokens=4000, min_chars=len(idx) * 30)
        new = [l.strip() for l in r.text.splitlines() if len(l.split()) >= 8]
    except Exception as e:
        print(f"     (viết lại thất bại: {e} → giữ nguyên)")
        return lines
    if len(new) != len(idx):
        print(f"     (trả về {len(new)}/{len(idx)} dòng → giữ nguyên)")
        return lines
    out = list(lines)
    for k, i in enumerate(idx):
        out[i] = _apply_world(_ascii_prompt(new[k]), world)
    print(f"     ✓ đã viết lại {len(idx)} dòng")
    return out


def _fix_policy(prof, lines):
    """Quét blocklist TRƯỚC khi tốn tiền gen ảnh; dòng vi phạm → nhờ model viết lại."""
    block = [b.lower() for b in (prof.get("blocklist") or [])]
    if not block:
        return lines
    bad_idx = [i for i, l in enumerate(lines) if any(b in l.lower() for b in block)]
    if not bad_idx:
        return lines
    print(f"  ! {len(bad_idx)} prompt chạm blocklist → viết lại (né trước khi gen, đỡ tốn tiền)")
    payload = "\n".join(f"{i+1}. {lines[i]}" for i in bad_idx)
    r = chat(
        "Rewrite each numbered image prompt so it does NOT depict any of these: "
        f"{', '.join(block)}. Keep the same scene, mood, shot type and the trailing style suffix; "
        "replace forbidden subjects with symbolic objects or fully-clothed adults. "
        "Output the SAME numbering, one prompt per line, nothing else.\n\n" + payload,
        task="short", temperature=0.5, max_tokens=8000, verbose=False)
    for line in r.text.splitlines():
        m = re.match(r"\s*(\d+)[\.\)]\s*(.+)", line.strip())
        if not m:
            continue
        i = int(m.group(1)) - 1
        if 0 <= i < len(lines):
            lines[i] = m.group(2).strip()
    return lines


# ============================================================ B7 — CHỮ THUMBNAIL
_PUBLISH_SCHEMA = """{
 "titles": ["3 tiêu đề khác nhau, MỖI CÁI DƯỚI 100 KÝ TỰ, viết bằng NGÔN NGỮ ĐÍCH"],
 "description": "mô tả 900-1400 ký tự bằng NGÔN NGỮ ĐÍCH, CHIA THÀNH 2-4 ĐOẠN cách nhau 1 dòng trống. 2 DÒNG ĐẦU là phần người xem thấy khi chưa bấm 'xem thêm' nên phải tự nó gây tò mò. KHÔNG chèn mốc thời gian, KHÔNG chèn hashtag, KHÔNG chèn câu cảm ơn ở đây — ba thứ đó có chỗ riêng.",
 "tags": ["12-18 thẻ tìm kiếm bằng ngôn ngữ đích, mỗi thẻ 2-5 từ, TỔNG dưới 450 ký tự, XẾP THEO ĐỘ QUAN TRỌNG GIẢM DẦN (5 thẻ đầu là quan trọng nhất)"],
 "hashtags": ["6-8 hashtag ngắn, có dấu #, bằng ngôn ngữ đích, XẾP THEO ĐỘ QUAN TRỌNG GIẢM DẦN (YouTube chỉ hiện 3 cái ĐẦU phía trên tiêu đề, còn lại chỉ để tìm kiếm)"],
 "chapters": ["tên từng chương theo ĐÚNG THỨ TỰ và ĐÚNG SỐ LƯỢNG đoạn cho bên dưới, mỗi tên dưới 40 ký tự, bằng ngôn ngữ đích"],
 "pinned_comment": "1 bình luận ghim bằng ngôn ngữ đích, hỏi khán giả một câu để họ trả lời",
 "loi_cam_on": "1 câu cảm ơn ngắn, chân thành gần gũi, bằng NGÔN NGỮ ĐÍCH, có thể kèm 1 emoji ở đầu",
 "category": "một trong: People & Blogs | Education | Entertainment | Howto & Style"}"""


def publish_kit(prof, script, sections):
    """Sinh TOÀN BỘ phần chữ cần để đăng video: tiêu đề, mô tả, thẻ, hashtag, chương, bình luận ghim.

    `sections` = [(giây_bắt_đầu, đoạn_lời_mẫu)] để đặt tên chương đúng nội dung từng khúc.
    Trả dict, hoặc None nếu LLM không trả JSON dùng được.
    """
    lang = LANG_NAME.get(prof.get("language", "ja"), prof.get("language"))
    n = prof.get("narrator", {}) or {}
    doan = "\n".join(f"[{i+1}] {t[:220]}" for i, (_, t) in enumerate(sections))
    ask = "\n".join([
        f"Bạn là chuyên gia SEO YouTube. Viết phần ĐĂNG TẢI cho một video kể chuyện faceless.",
        f"NGÔN NGỮ OUTPUT: {lang} (mọi trường đều bằng ngôn ngữ này, KHÔNG dịch sang tiếng Việt).",
        f"Ngách: {prof.get('niche','')} · Người kể: {n.get('persona','')}",
        "",
        "Nguyên tắc: tiêu đề gợi tò mò nhưng KHÔNG giật gân sai sự thật (câu view lố bị YouTube "
        "hạ đề xuất). Không hứa điều video không có. Không dùng CHỮ HOA toàn bộ.",
        "",
        f"Có {len(sections)} đoạn, hãy đặt {len(sections)} tên chương theo đúng thứ tự:",
        doan,
        "",
        "TÓM TẮT NỘI DUNG (đầu kịch bản):",
        script.strip()[:2500],
        "",
        "Trả về DUY NHẤT JSON đúng khuôn (không thêm chữ nào):",
        _PUBLISH_SCHEMA,
    ])
    try:
        r = chat(ask, task="long", max_tokens=2600, min_chars=200, verbose=False)
    except Exception as e:
        print(f"  (gói đăng tải: LLM lỗi {type(e).__name__} {e})")
        return None
    m = re.search(r"\{.*\}", r.text, re.DOTALL)
    if not m:
        print(f"  (gói đăng tải: LLM không trả JSON: {r.text[:120]})")
        return None
    try:
        d = json.loads(m.group(0))
    except Exception as e:
        print(f"  (gói đăng tải: JSON hỏng {e})")
        return None
    return d if d.get("titles") and d.get("description") else None


def _thumb_rang_buoc(prof):
    """Ràng buộc SỰ THẬT cho chữ thumbnail của kênh kể tài liệu.

    Dính thật 2026-09-10 (video 多元宇宙): model tự viết BANNER 「抹殺された天才物理学者」
    ("nhà vật lý thiên tài BỊ THỦ TIÊU") trong khi kịch bản nói rõ Everett chết vì nhồi máu cơ tim.
    Thumbnail là chỗ dễ buột ra câu sai nhất — nó được viết rời khỏi kịch bản, không đi qua gate
    nào, mà lại là thứ 100% người xem nhìn thấy. Ở ngách này một câu bịa trên thumbnail vừa mời
    gọi cờ "nội dung không trung thực", vừa cho nhóm khán giả phản biện đúng cái cớ họ đang chờ.
    """
    if ((prof.get("script", {}) or {}).get("mode") or "").lower() != "documentary":
        return ""
    return ("RÀNG BUỘC SỰ THẬT (bắt buộc):\n"
            "· Mọi chữ trên thumbnail phải có căn cứ TRONG kịch bản. Không thêm cái chết bí ẩn, "
            "vụ thủ tiêu, âm mưu che giấu, cơ quan bí mật... nếu kịch bản không hề nói.\n"
            "· Được phép gây tò mò bằng: câu hỏi, dấu …, che đáp án bằng ●●, trích lời trong 「」.\n"
            "· KHÔNG dùng động từ khẳng định về việc chưa được chứng minh (「証明された」「判明」).\n"
            "  Thay bằng 「〜という説」「〜が認めた」「本当なら」.\n\n")


def write_thumb_text(prof, script):
    """Chữ overlay cho thumbnail — theo MÔ-TÍP CỐ ĐỊNH của kênh nếu profile khai `thumbnail.template`.

    Vì sao có nhánh template (user chốt 2026-09-10): thumbnail của một kênh phải nhận ra được ngay
    từ xa — cùng bố cục, cùng bảng màu, cùng số tầng chữ, **chỉ đổi ẢNH và CHỮ**. Thả cho LLM tự
    chọn 3 dòng + banner thì mỗi tập một kiểu, lướt trang kênh trông như 20 người khác nhau đăng.
    """
    th = prof.get("thumbnail", {}) or {}
    mau = th.get("template") or {}
    pal = th.get("palette") or ["WHITE", "YELLOW", "RED"]
    lang = LANG_NAME.get(prof.get("language", "ja"), prof.get("language"))
    if mau.get("tiers"):
        dong = [f"{t['color']}|<{t.get('role', '')}, tối đa {t.get('max_chars', 14)} ký tự>"
                for t in mau["tiers"]]
        yeu_cau = (f"Xuất ĐÚNG {len(dong)} dòng, mỗi dòng dạng MÀU|nội dung, không gì khác "
                   f"(KHÔNG thêm dòng BANNER, KHÔNG đổi tên màu):\n" + "\n".join(dong) + "\n\n"
                   "Các tầng chữ phải ĐỌC LIỀN thành một câu có nghĩa: tầng trên là tiền đề, "
                   "tầng dưới là cú sốc.\n\n")
    else:
        yeu_cau = (f"Xuất ĐÚNG 4 dòng, mỗi dòng dạng MÀU|nội dung, không gì khác:\n"
                   f"{pal[0]}|<hook dòng 1, tối đa 12 ký tự>\n"
                   f"{pal[1] if len(pal)>1 else 'YELLOW'}|<hook dòng 2, tối đa 12 ký tự>\n"
                   f"{pal[2] if len(pal)>2 else 'RED'}|<câu hỏi/từ khoá gây sốc, tối đa 14 ký tự>\n"
                   f"BANNER|<phụ đề kiểu 'sự thật ... người X tiết lộ', tối đa 22 ký tự>\n\n")
    r = chat(
        f"Đọc kịch bản dưới đây rồi viết chữ overlay cho thumbnail YouTube bằng {lang}.\n"
        + yeu_cau + _thumb_rang_buoc(prof) +
        f"KỊCH BẢN:\n{script[:6000]}",
        task="short", temperature=0.9, max_tokens=2000)
    n_dong = len(mau.get("tiers") or []) or 4
    lines = [l.strip() for l in r.text.splitlines() if "|" in l][:n_dong]
    print(f"[B7] {len(lines)} dòng · {r.provider}:{r.model} {r.elapsed:.0f}s")
    return "\n".join(lines)


# ============================================================ CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["script", "imgs", "thumb", "measure"])
    ap.add_argument("--profile", required=True)
    ap.add_argument("--competitor", default="")
    ap.add_argument("--script", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--minutes", type=float, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--series", default="", help="file mạch series (tóm tắt tập trước + hé tập sau)")
    ap.add_argument("--sheet", default="", help="CHARACTER SHEET của TẬP này (ghi đè sheet HOST trong profile)")
    args = ap.parse_args()
    prof = profiles.load(args.profile)

    if args.step == "measure":
        text = Path(args.script).read_text(encoding="utf-8")
        bad, m = check(prof, text, args.minutes or None)
        for k, v in m.items():
            print(f"  {k:20s} {v}")
        print("GATE:", "ĐẠT" if not bad else "\n  - " + "\n  - ".join(bad))
        return

    if args.step == "script":
        comp = Path(args.competitor).read_text(encoding="utf-8")
        ctx = Path(args.series).read_text(encoding="utf-8") if args.series else ""
        res = write_script(prof, comp, args.minutes or None, ctx)
        out = Path(args.out or "script_out.txt")
        out.write_text(res["text"], encoding="utf-8")
        print(f"✓ {out} · " + " → ".join(res["passes"]))
        return

    script = Path(args.script).read_text(encoding="utf-8")
    if args.step == "imgs":
        res = write_img_prompts(prof, script, args.n or None, sheet=args.sheet or None)
        out = Path(args.out or "img_prompts_out.txt")
        out.write_text("\n".join(res["prompts"]), encoding="utf-8")
        print(f"✓ {out} ({len(res['prompts'])} prompt)")
        return
    txt = write_thumb_text(prof, script)
    print(txt)
    if args.out:
        Path(args.out).write_text(txt, encoding="utf-8")


if __name__ == "__main__":
    main()
