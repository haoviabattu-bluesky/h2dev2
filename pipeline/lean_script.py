"""lean_script.py — LUỒNG KỊCH BẢN GỌN (`profile.script.flow = "lean"`), thiết kế docs/QUY_TRINH_KICH_BAN_GON.md v2.

Một câu (anh chốt 2026-09-20):
    Fable viết → máy bắt lỗi cơ học → Sol bắt lỗi nội dung → Fable patch tối đa 2 lần → mọi patch đều chạy
    lại máy + Sol → Sol PASS cuối cùng → khoá SHA256 → tuyệt đối không ai sửa script nữa.

Vì sao tách khỏi `ai_steps.write_script` + chuỗi B3Q/B3F/B3S/B3R/B3G của make_video (luồng cũ, vẫn giữ y nguyên
cho lane không khai flow): đo thật ep01 Lane G 2026-09-20 — 12 lượt LLM, 6 lượt SỬA TOÀN VĂN đổi tay Gemini↔Fable,
lỗi dữ kiện cuối (6000/8000歩 đảo nghĩa) sinh ở lượt hạ thoại SAU KHI Sol đã chấm. Mỗi cổng cũ chữa lỗi bằng một
lượt LLM viết lại → cổng sau phải bắt lỗi cổng trước sinh ra. Ở đây:
  · chỉ MỘT tác giả (Fable) chạm master text; Gemini không ghi script.txt (vẫn dùng ở B5 prompt ảnh…);
  · máy đo (0đ) sau MỌI lần văn bản đổi; Sol (lens theo lane) chỉ hỏi thứ máy mù;
  · patch có ràng buộc (danh sách việc có vị trí · MUST PRESERVE · trần/sàn chữ · diff đoạn · không mất số);
  · tối đa 2 patch → 3 trạng thái PASS / ESCALATE / BLOCK, không có "chạy tiếp";
  · Sol PASS → gate_common.ghi_lock(); pha asset gọi kiem_lock() — sha đổi = FINAL_QC_STALE.

Gọi từ make_video.Job.b3_lean(). Không import brain_channel/brain_steps (nhánh não-Claude satori tách riêng).
"""
import difflib
import json
import re
import time
from pathlib import Path

import ai_steps
import claude_p_bridge
import gate_common
import hook_stage  # H1-H4 hook thuong nguon (anh chot 2026-09-23)
import profiles
import qc_facts
import qc_loi_hua  # kiểm nhẹ lời hứa tiêu đề thay S5 Sol khi sol_qc=false (anh chốt 2026-09-29)
import qc_goi_dang  # S1L luật hook + gói đăng, chặn trước khi viết (anh chốt 2026-09-24)
import qc_numbers
import qc_script
import qc_script_sol
from llm_client import LLMError

MAX_PATCH = 2
ROOT = Path(__file__).resolve().parent.parent
KANJI_NUM = "一二三四五六七八九十"


# ============================================================ S1Q — hồ sơ đủ chưa (0 LLM)
def s1q_ho_so(d: Path, prof, competitor: str, ctx: str):
    """Trả list lỗi BLOCK (rỗng = đủ). Kiểm trước khi tốn lượt Fable nào.

    `script.ctx_required=false` (satori — kể chuyện hư cấu, không có tư liệu nguồn) → bỏ hẳn phần kiểm
    series_ctx.txt (qc_facts ở S3 tự bỏ qua khi ctx rỗng, xem do_tat_dinh: `if nguon:`).
    Dòng tư liệu chấp nhận 2 khuôn: `[Dn]` (khuôn chuẩn §2 file này) HOẶC `〔出典:` (khuôn SPACE_RESEARCH
    dùng cho Lane A/D, đã có sẵn hàng trăm hồ sơ theo khuôn này — không bắt viết lại)."""
    loi = []
    if len(competitor.replace("\n", "")) < 3000:
        loi.append(f"competitor.txt quá ngắn ({len(competitor):,} ký tự) — cần transcript kênh mẫu ≥3.000")
    if not (prof.get("script", {}) or {}).get("ctx_required", True):
        return loi
    if not ctx.strip():
        loi.append("thiếu series_ctx.txt — mọi địa điểm/giá/số liệu sẽ không có nguồn để đối chiếu")
    else:
        co_nguon = re.search(r"^\[D\d+\]", ctx, re.M) or re.search(r"出典", ctx)
        if not co_nguon:
            loi.append("series_ctx.txt không có dòng tư liệu dạng [Dn] … hoặc 〔出典: …〕")
        if "http" not in ctx:
            loi.append("series_ctx.txt không có URL nguồn nào")
        # `script.ctx_phai_co` = khối luật lane bắt buộc dán vào series_ctx (model S2/hook đọc series_ctx,
        # không đọc file quy tắc). Thêm 2026-10-14 cho Lane F khung 10 chặng; lane không khai → không đổi gì.
        for m in (prof.get("script", {}) or {}).get("ctx_phai_co") or []:
            if m not in ctx:
                loi.append(f"series_ctx.txt thiếu khối bắt buộc「{m}」(profile script.ctx_phai_co / _ctx_phai_co_note)")
    return loi


def so_duoc_phep(ctx: str):
    """Khối `SỐ ĐƯỢC PHÉP:` (1 dòng, phân cách · hoặc ,) — S1 khai; không có → dùng cả series_ctx làm nguồn."""
    m = re.search(r"SỐ ĐƯỢC PHÉP\s*[:：]\s*(.+)", ctx)
    return m.group(1).strip() if m else ""


# ============================================================ S2 — ngân sách + viết
def ngan_sach(prof, target: int):
    b = (prof.get("script", {}) or {}).get("budget") or {}
    tol = float(b.get("tol", 0.08))
    # Lane TRUYỆN (không mục/marker — Lane F 7 chặng, 2026-09-20): `budget.sections` = [{"label","ratio"}...]
    # tổng ratio ≈ 1. Có `sections` → n=0 (không kiểm marker), ngân sách chia theo từng chặng thay vì N mục đều.
    secs = b.get("sections")
    if secs:
        tong = sum(float(x.get("ratio", 0)) for x in secs) or 1.0
        parts = [{"label": x.get("label", f"部{i+1}"), "chars": int(target * float(x.get("ratio", 0)) / tong)}
                 for i, x in enumerate(secs)]
        return {"target": target, "tol": tol, "n": 0, "sections": parts,
                "mo_dau": parts[0]["chars"], "moi_muc": 0, "ket": parts[-1]["chars"],
                "lo": int(target * (1 - tol)), "hi": int(target * (1 + tol)),
                "label_mo_dau": parts[0]["label"], "label_ket": parts[-1]["label"]}
    mo = float(b.get("mo_dau", 0.22))
    ket = float(b.get("ket", 0.08))
    n = int(profiles.gate(prof).get("list_item_count") or 5)
    muc = (1.0 - mo - ket) / n
    return {"target": target, "tol": tol, "n": n,
            "mo_dau": int(target * mo), "moi_muc": int(target * muc), "ket": int(target * ket),
            "lo": int(target * (1 - tol)), "hi": int(target * (1 + tol)),
            "label_mo_dau": b.get("label_mo_dau"), "label_ket": b.get("label_ket")}


def budget_block(ns):
    if ns.get("sections"):
        chia = " · ".join(f"{x['label']}約{x['chars']:,}字" for x in ns["sections"])
        return (f"2) ĐỘ DÀI = NGÂN SÁCH CỨNG (không tính xuống dòng/khoảng trắng): TỔNG {ns['target']:,} chữ "
                f"(chấp nhận {ns['lo']:,}–{ns['hi']:,}). Chia theo CHẶNG (không đặt tiêu đề/marker chặng trong bản đọc) — {chia}. "
                f"KHÔNG có bước cắt phía sau — viết đúng độ dài ngay; viết dài hơn là lỗi, không phải an toàn. "
                f"Viết ĐỦ MẠCH, giàu chi tiết đời thường và cảm xúc trong đúng ngân sách đó.")
    lb_mo = ns.get("label_mo_dau") or "第1〜2幕（フック＋人物＋案内役）"
    lb_ket = ns.get("label_ket") or "結び（翌朝＋まとめ＋締めの一言）"
    return (f"2) ĐỘ DÀI = NGÂN SÁCH CỨNG (không tính xuống dòng/khoảng trắng): TỔNG {ns['target']:,} chữ "
            f"(chấp nhận {ns['lo']:,}–{ns['hi']:,}). Chia theo phần — {lb_mo}約{ns['mo_dau']:,}字 · "
            f"各項目 約{ns['moi_muc']:,}字 × {ns['n']} · {lb_ket}約{ns['ket']:,}字. "
            f"KHÔNG có bước cắt phía sau — viết đúng độ dài ngay; viết dài hơn là lỗi, viết NGẮN hơn cũng là lỗi (đo thật: 3/6 bản đầu thiếu 11–26%). "
            f"Mỗi mục KHÔNG DƯỚI {int(ns['moi_muc']*0.9):,} chữ — mỗi mục cần: dẫn vào (1 đoạn) · 案内役 giải thích kèm dữ kiện (1–2 đoạn) · 俺 thử/nghĩ (1–2 đoạn) · cầu nối sang mục sau (1 đoạn). "
            f"Viết ĐỦ MẠCH, giàu chi tiết đời thường và cảm xúc trong đúng ngân sách đó.")


CUNG_CAM_XUC = """=== CUNG CẢM XÚC BẮT BUỘC — người xem phải NHỚ, không được nhẹ nhàng khô khan ===
Bằng chứng: ở kênh mẫu, video làm người xem ỨC CHẾ/GIẬN nổ gấp 10–100 lần video giải thích nhẹ nhàng; bình luận top toàn
là giận nhân vật, rồi cuối video chuyển sang thương cảm và tự soi mình. Kịch bản phải đi đúng 3 nhịp:
  · NHỊP 1 — KÍCH (hook tới khoảng 40% bài): làm người xem hưng phấn/giận/ức chế THẬT. Nhân vật gây chuyện hành xử đáng ghét
    bằng HÀNH VI + LỜI NÓI cụ thể (không tả chung chung "anh ta ích kỷ"); người tử tế chịu thiệt có tên, có chi tiết cái giá
    phải trả; bất công leo thang ít nhất 3 nấc, nấc sau nặng hơn nấc trước; ai có quyền đứng sai phe hoặc làm ngơ. KHÔNG giải
    toả sớm, KHÔNG để người kể giảng hoà, biện hộ hay giải thích cho kẻ gây chuyện ở nhịp này.
  · NHỊP 2 — GIẢI TOẢ (khoảng 40–85%): đảo chiều bằng sự thật và hệ quả tự nhiên (quy định, cơ chế, thời gian, lựa chọn của
    chính nhân vật) — khán giả thấy hả dạ, NHƯNG không nhân vật tốt nào trả thù, mắng nhiếc hay hả hê.
  · NHỊP 3 — VỊ THA (khoảng 10% cuối): đổi góc nhìn — một chi tiết cho thấy kẻ gây chuyện cũng là người đáng thương (cô đơn,
    sợ bị thay thế, từng bị đối xử như vậy), hoặc người bị hại chọn bao dung/giúp đỡ. Chốt bằng MỘT câu đạo lý ngắn, sắc,
    dễ nhớ, người xem muốn chép lại vào bình luận. Không thuyết giáo dài.
Cường độ ở nhịp 1 là do CHI TIẾT gây ức chế, không phải do chửi bới, bạo lực hay từ ngữ thô tục. Luật cấu trúc của lane ở
trên vẫn giữ nguyên — cung cảm xúc này phủ lên đúng các chặng đó.
KẾT BẮT BUỘC (anh chốt 2026-09-26): đoạn cuối cùng của bài, SAU câu đạo lý, người kể CẢM ƠN người xem đã quan tâm xem hết
video (vd 「最後までご覧いただき、本当にありがとうございました。」) rồi xin MỘT lượt thích và đăng ký kênh
(vd 「この動画が少しでも役に立ったら、高評価とチャンネル登録をお願いします。」). Viết tự nhiên theo giọng người kể, 1–3 câu,
không kéo dài. Lane có câu outro cố định thì câu outro vẫn là câu CUỐI CÙNG — lời cảm ơn đứng ngay trước nó.
CTA CHỈ MỘT LẦN (anh chốt 2026-10-01): lời cảm ơn + xin 高評価/チャンネル登録 xuất hiện ĐÚNG MỘT LẦN trong cả bài, ở cuối —
cấm CTA giữa bài, cấm viết hai đoạn CTA nối nhau. Lane có câu outro cố định mà outro ĐÃ xin 高評価/チャンネル登録 thì KHÔNG tự
viết câu xin thích/đăng ký nào (máy tự ghép outro làm câu cuối); outro chưa có lời cảm ơn thì chỉ thêm 1 câu cảm ơn ngay trước nó."""

# Máy kiểm phần KẾT (đi cùng CUNG_CAM_XUC): 15% cuối bài phải có đủ 3 ý cảm ơn · thích · đăng ký.
KET_CAM_ON = {"cảm ơn đã xem hết": r"(ありがとう|感謝)", "xin thích (高評価/いいね)": r"(高評価|いいね|グッドボタン)",
              "xin đăng ký kênh": r"(チャンネル登録)"}


def _ket_thieu(text):
    """Trả danh sách ý còn thiếu ở 15% cuối bài (tính cả outro_line nếu đã ghép)."""
    duoi = text.replace(chr(10), "")
    duoi = duoi[int(len(duoi) * 0.85):]
    return [ten for ten, pat in KET_CAM_ON.items() if not re.search(pat, duoi)]


def _khoi_insight_kenh(prof):
    """Khối '## ĐƯA VÀO PROMPT' trong <channel_dna_dir>/COMMENT_INSIGHT.md (bước 1 viết tay từ bình luận thật)."""
    dna = (prof.get("channel_dna_dir") or "").strip()
    if not dna:
        return ""
    f = ROOT / dna / "COMMENT_INSIGHT.md"
    if not f.exists():
        return ""
    m = re.search(r"^##\s*ĐƯA VÀO PROMPT\s*$(.*?)(?=^##\s|\Z)", f.read_text(encoding="utf-8"), re.M | re.S)
    body = (m.group(1).strip() if m else "")
    return ("=== KHÁN GIẢ THẬT CỦA KÊNH MẪU NÓI GÌ (chắt từ bình luận thật — viết để HỌ nhớ và muốn bình luận) ===\n" + body) if body else ""


KHOI_THE_VIET_S2 = """=== THẺ VIẾT (luật anh + số liệu thị trường, field script.the_viet) ===
THỨ TỰ ƯU TIÊN khi mâu thuẫn: QUY ƯỚC của tập/series và CUNG CẢM XÚC ở trên > thẻ PHẦN 1 > thẻ PHẦN 2.
Thẻ PHẦN 2 là số liệu thị trường: lấy chuẩn/nhịp, KHÔNG chép câu ví dụ. Hook đã khoá thì giữ nguyên, thẻ áp cho THÂN bài.
"""


def khoi_them(prof, d=None):
    """Khối thêm cho prompt S2 (anh chốt 2026-09-26): cung cảm xúc (field `script.cung_cam_xuc`, VẮNG = BẬT; satori/E/A/D
    khai false) + insight bình luận kênh mẫu (COMMENT_INSIGHT.md). Trả chuỗi rỗng khi không có gì → prompt y hệt trước."""
    sc = prof.get("script") or {}
    out = []
    if sc.get("cung_cam_xuc", True):
        out.append(CUNG_CAM_XUC)
    ins = _khoi_insight_kenh(prof)
    if ins:
        out.append(ins)
    the = ai_steps.doc_the_viet(prof)
    if the:
        out.append(KHOI_THE_VIET_S2 + the)
    return "\n\n".join(out)


def _insight_tap(d):
    """comment_insight.json của tập (B2b đọc bình luận video gốc) — trước 2026-09-26 luồng lean BỎ QUÊN file này."""
    f = Path(d) / "comment_insight.json" if d else None
    if not f or not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return None


def viet(prof, competitor: str, ctx: str, minutes: float, ns, log: list, hook: str = "", luat: str = "", d=None):
    """S2a khung (giấu bản gốc) + S2b viết đúng ngân sách. Trả text đã normalize.
    hook: đoạn mở đầu đã khoá ở H1-H4 (hook_stage.py, bám sườn hook video gốc) — S2 viết THÂN nối tiếp từ đây, không viết lại mở đầu.
    luat: khối luật gói đăng G1-G4 của lane (qc_goi_dang.khoi_luat_cho_prompt) — đưa vào ĐẦU VÀO để model
    viết đúng ngay lần đầu, thay vì để cổng bắt ở đầu ra rồi phải trả thêm lượt Sol + lượt patch."""
    skill = ai_steps._skill_text(prof, "script")
    source = competitor
    if not (prof.get("script", {}) or {}).get("use_raw_source"):
        source = ai_steps.extract_beats(prof, competitor, hook_locked=hook)
        log.append(f"S2a khung {len(source)} ký tự")
    sdp = so_duoc_phep(ctx)
    ctx_prompt = ctx
    if sdp:
        ctx_prompt = (f"⚠️ CHỈ những con số sau được xuất hiện trong kịch bản (số khác → diễn đạt định tính): {sdp}\n\n" + ctx)
    them = khoi_them(prof, d)
    ins_tap = _insight_tap(d)
    if them or ins_tap:
        log.append(f"S2 khối thêm: cung_cam_xuc={'có' if CUNG_CAM_XUC in them else 'không'} · "
                   f"insight kênh={'có' if 'KHÁN GIẢ THẬT' in them else 'không'} · insight tập={'có' if ins_tap else 'không'} · "
                   f"thẻ viết={'có' if KHOI_THE_VIET_S2 in them else 'không'}")
    prompt = ai_steps._pass1_prompt(prof, source, minutes, ctx_prompt, budget_block=budget_block(ns),
                                    hook_locked=hook, luat_goi_dang=luat, comment_insight=ins_tap, khoi_them=them)
    r = ai_steps._writer_chat(prof, prompt, system=skill, task="script",
                              min_chars=int(ns["target"] * 0.6), max_chars=int(ns["target"] * 1.45),
                              require_sentence_end=True)
    text = ai_steps.normalize_paragraphs(ai_steps.strip_markers(r.text))
    log.append(f"S2b viết {r.provider}:{r.model} {ai_steps.measure(text)['chars']:,} chữ {r.elapsed:.0f}s")
    return text


# ============================================================ S3 — đo tất định (0 LLM)
def _nums(text):
    """Tập 'số có đơn vị' để so trước–sau patch (không mất số khi nén)."""
    return set(re.findall(r"(?:\d+|[一二三四五六七八九十百千万〇・]+)(?:歩|円|時|時半|分|リットル|ミリ|ミリリットル|年|歳|キロ|回|本|杯|日|か月|ヶ月|週間|人|割|%|％)", text))


_KD = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
_KU_NHO = {"十": 10, "百": 100, "千": 1000}       # đơn vị TRONG 1 nhóm 4 chữ số (<10.000)
_KU_LON = {"万": 10000}                          # đơn vị NHÂN CẢ NHÓM — extend thêm 億 nếu cần sau


def kanji_to_int(s):
    """一・二・三 / 千二百 / 六千 / 八千 / 一万二千 → int. Có '・' (thập phân, vd 一・二) → trả float.

    Bài học đắt (2026-09-21, phát hiện lúc ep01 teinengo-real bị ESCALATE oan bởi lỗi「SỐ HỌC」giả):
    bản CŨ gộp 十/百/千/万 vào MỘT biến `total` chung, nên số dạng "AA十B万…" (十 đứng TRƯỚC 万 trong
    cùng 1 nhóm) bị tính SAI cả bậc số — vd 「二十一万二千」(= 212.000) ra 12.020, 「十三万一千」
    (= 131.000) ra 31.010 (kiểm tay: 二十一万 bị tách thành +20 rồi +1×10.000 = 10.020 thay vì đúng
    ra (20+1)×10.000 = 210.000). Đúng phải là: 十/百/千 CỘNG DỒN vào 1 "nhóm nhỏ" (0–9.999), tới khi
    gặp 万 mới NHÂN CẢ NHÓM đó với 10.000 rồi cộng vào tổng — xem thuật toán chuẩn bên dưới."""
    if "・" in s:
        a, b = s.split("・", 1)
        try:
            return float(f"{kanji_to_int(a)}.{''.join(str(_KD.get(c, '')) for c in b)}")
        except Exception:
            return None
    if s.isdigit():
        return int(s)
    total, nhom, cur = 0, 0, 0
    for c in s:
        if c in _KD:
            cur = cur * 10 + _KD[c]
        elif c in _KU_NHO:
            nhom += (cur if cur else 1) * _KU_NHO[c]
            cur = 0
        elif c in _KU_LON:
            nhom += cur
            cur = 0
            total += (nhom if nhom else 1) * _KU_LON[c]
            nhom = 0
        else:
            return None
    return total + nhom + cur


FACT_UNITS = r"(?:歩|万円|円|リットル|ミリリットル|ミリ|キロカロリー|キロ|年間|％|%|割|度|グラム|時間)"
NUM = r"(?:\d[\d,]*(?:\.\d+)?|[一二三四五六七八九十百千万〇・]+)"


def _gia_tri_cho_phep(ctx):
    """Mọi số trong series_ctx (kèm SỐ ĐƯỢC PHÉP): arabic + kanji, thêm biến thể L↔ml (×1000) và 万円↔円."""
    vals = set()
    for m in re.finditer(r"(\d[\d,]*(?:\.\d+)?)\s*([A-Za-zＬｌ]*|[一-龥ァ-ヶ]*)", ctx):
        try:
            v = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        vals.add(v)
        u = m.group(2)
        if u.upper().startswith("L"):
            vals.add(v * 1000)
        if u.startswith("万"):
            vals.add(v * 10000)
    for m in re.finditer(r"[一二三四五六七八九十百千万〇・]{1,8}" + FACT_UNITS, ctx):
        v = kanji_to_int(re.sub(FACT_UNITS + "$", "", m.group(0)))
        if v is not None:
            vals.add(float(v))
    return vals


def _so_lieu_ngoai_tu_lieu(text, ctx, exempt_units=()):
    """Số CÓ ĐƠN VỊ DỮ KIỆN (歩/円/リットル/キロ/年間/%…) trong script mà giá trị không có trong tư liệu → việc.
    `exempt_units`: đơn vị được MIỄN đối chiếu — lane truyện về TIỀN (Lane F) khai `script.fact_exempt_units=["万円","円"]`
    vì số 通帳/退職金/貯金 là HƯ CẤU (đo ep01: 30 số cá nhân bị bắt "không có trong tư liệu" — vòng patch sẽ xoá sạch
    xương sống câu chuyện). Số chế độ (%, 歩, 年間…) và số tiền có trong tư liệu vẫn đối chiếu; nhất quán tiền cá nhân
    do `_tong_tien` + Sol lo.
    Bỏ qua số nhỏ ≤12 (一杯/二本 kiểu đếm đời thường) và 歳/時/分 (tuổi/giờ nhân vật hư cấu). Bắt cả kanji lẫn arabic —
    bài học ep01: 六千歩/八千歩 viết kanji, qc_facts chỉ soi arabic nên mù."""
    if not ctx:
        return []
    allowed = _gia_tri_cho_phep(ctx)
    ra, seen = [], set()
    for m in re.finditer(NUM + FACT_UNITS, text):
        tok = m.group(0)
        unit = re.search(FACT_UNITS + "$", tok).group(0)
        if unit in exempt_units:
            continue
        so = tok[: -len(unit)].replace(",", "")
        v = float(so) if so.replace(".", "").isdigit() else kanji_to_int(so)
        if v is None or float(v) <= 12:
            continue
        v = float(v)
        cand = {v, v * 10000 if unit == "万円" else v, v * 1000 if unit == "リットル" else v}
        if not (cand & allowed) and tok not in seen:
            seen.add(tok)
            i = text.find(tok)
            ra.append(f"DỮ KIỆN「{tok}」không có trong tư liệu/SỐ ĐƯỢC PHÉP (câu:「{text[max(0,i-25):i+len(tok)+10].replace(chr(10),' ')}」) → xoá, diễn đạt định tính, hoặc sửa đúng theo [Dn]")
    return ra


def _tong_tien(text):
    """Đoạn có 総額/合計/計/しめて X円 → cộng mọi khoản 円 đứng TRƯỚC nó trong cùng đoạn; lệch >15% → việc.
    Bài học ep02 2026-09-20: 「2袋で110円。プランターも110円。土も肥料も110円。総額600円ほど」(=440) lọt 2 vòng Sol."""
    ra = []
    pat_amt = re.compile(NUM + r"円")
    for para in text.split(chr(10)):
        m = re.search(r"(総額|合計|しめて|全部で|計)\s*(" + NUM + r")円", para)
        if not m:
            continue
        tong = kanji_to_int(m.group(2).replace(",", "")) if not m.group(2).replace(",", "").isdigit() else int(m.group(2).replace(",", ""))
        truoc = para[: m.start()]
        khoan = []
        for a in pat_amt.finditer(truoc):
            so = a.group(0)[:-1].replace(",", "")
            v = int(so) if so.isdigit() else kanji_to_int(so)
            if v:
                khoan.append(v)
        if tong and len(khoan) >= 2:
            # 「土も肥料も110円」= 2 khoản chung 1 số → thử cả cộng thô lẫn cộng có nhân đôi cho「AもBも」
            tong_tho = sum(khoan)
            them = len(re.findall(r"も[^。、]{0,6}も" + NUM + r"円", truoc))
            ung_vien = {tong_tho, tong_tho + them * khoan[-1]}
            if all(abs(u - tong) / tong > 0.15 for u in ung_vien):
                ra.append(f"SỐ HỌC: các khoản {khoan} cộng lại {sorted(ung_vien)} ≠「{m.group(0)}」— sửa tổng hoặc liệt kê đủ khoản (đoạn:「{para[:40]}…」)")
    return ra


def _tong_tien(text):
    """Đoạn có 総額/合計/計/しめて X円 → cộng mọi khoản 円 đứng TRƯỚC nó trong cùng đoạn; lệch >15% → việc.
    Bài học ep02 2026-09-20: 「2袋で110円。プランターも110円。土も肥料も110円。総額600円ほど」(=440) lọt 2 vòng Sol."""
    ra = []
    pat_amt = re.compile(NUM + r"円")
    for para in text.split("\n"):
        m = re.search(r"(総額|合計|しめて|全部で|計)\s*(" + NUM + r")円", para)
        if not m:
            continue
        so_t = m.group(2).replace(",", "")
        tong = int(so_t) if so_t.isdigit() else kanji_to_int(so_t)
        truoc = para[: m.start()]
        khoan = []
        for a in pat_amt.finditer(truoc):
            so = a.group(0)[:-1].replace(",", "")
            v = int(so) if so.isdigit() else kanji_to_int(so)
            if v:
                khoan.append(v)
        if tong and len(khoan) >= 2:
            # 「土も肥料も110円」= 2 khoản chung 1 số → thử cả cộng thô lẫn cộng có nhân đôi cho「AもBも」
            tong_tho = sum(khoan)
            them = len(re.findall(r"も[^。、]{0,6}も" + NUM + r"円", truoc))
            ung_vien = {tong_tho, tong_tho + them * khoan[-1]}
            if all(abs(u - tong) / tong > 0.15 for u in ung_vien):
                ra.append(f"SỐ HỌC: các khoản {khoan} cộng lại {sorted(ung_vien)} ≠「{m.group(0)}」— sửa tổng hoặc liệt kê đủ khoản (đoạn:「{para[:40]}…」)")
    return ra


def _nhat_quan_ten_tuoi(text):
    """Cùng tên (2–4 kanji ngay trước 、/は/が/。 và tuổi) mà gắn 2 tuổi khác nhau → lỗi máy bắt được."""
    ra = {}
    for m in re.finditer(r"([一-龥]{2,4})(?:は|が|、|。)?(?:今年で|は今年|は)?([\d" + KANJI_NUM + r"]+)歳", text):
        ten = m.group(1)
        if all(c in KANJI_NUM + "百千〇" for c in ten) or ten[-1] in KANJI_NUM:   # "六十"/"で六十" không phải tên
            continue
        ra.setdefault(ten, set()).add(m.group(2))
    return [f"nhân vật「{k}」gắn {len(v)} tuổi khác nhau: {sorted(v)} — thống nhất 1 tuổi" for k, v in ra.items() if len(v) > 1]


def _markers_thieu(text, g):
    # lane truyện khai `gate.list_item_count = 0` (đi cùng `budget.sections`) → không có mục để kiểm
    if str(g.get("list_item_count", "")).strip() == "0":
        return [], 0
    n = int(g.get("list_item_count") or 5)
    order = (g.get("list_order") or "auto").lower()
    b = text.replace("\n", "")
    co_xuoi = [k for k in range(1, n + 1) if (f"{k}つ目" in b or f"{KANJI_NUM[k-1]}つ目" in b)]
    co_nguoc = [k for k in range(1, n + 1) if f"第{k}位" in b or f"第{KANJI_NUM[k-1]}位" in b]
    if order == "ascending":
        thieu = [k for k in range(1, n + 1) if k not in co_xuoi]
    elif order == "countdown":
        thieu = [k for k in range(1, n + 1) if k not in co_nguoc]
    else:
        thieu = [] if (len(co_xuoi) == n or len(co_nguoc) == n) else \
            [k for k in range(1, n + 1) if k not in (co_xuoi if len(co_xuoi) >= len(co_nguoc) else co_nguoc)]
    return thieu, n


def _outro_fix(text, outro):
    """Câu cuối phải NGUYÊN VĂN outro_line — sửa tất định (không nhờ LLM)."""
    if not outro:
        return text, False
    t = text.rstrip()
    if t.endswith(outro):
        return text, False
    # câu chào biến thể ở cuối (ご視聴… / いいね…) → thay cả đoạn cuối chứa nó
    paras = [p for p in t.split("\n")]
    last = paras[-1]
    if "ご視聴" in last or "いいね" in last:
        paras[-1] = outro
        return "\n".join(paras), True
    return t + "\n\n" + outro, True


# CTA = xin thích/đăng ký + câu cảm ơn đã xem. Không gồm câu mời bình luận (Lane M/G có cta_mid giữa bài — luật riêng).
CTA_XIN = r"(高評価|チャンネル登録|グッドボタン|いいねボタン|いいねと|いいねを)"
CTA_CAM_ON = r"(最後までご覧|ご視聴いただき|ご視聴ありがとう|ご覧いただき)"


def _cta_mot_lan(text, outro):
    """CTA chỉ MỘT lần, ở cuối (anh chốt 2026-10-01). Lane J ep03: Opus viết đoạn 「最後までご覧…高評価とチャンネル登録…」
    rồi _outro_fix ghép thêm outro (cũng xin 高評価/チャンネル登録) → 2 CTA; _go_cau_trung còn xoá mất câu cảm ơn ĐẦU của outro
    vì trùng nguyên văn câu Opus đã viết. Tất định: có outro → xoá mọi câu CTA nằm ngoài outro (giữ 1 câu cảm ơn cuối nếu outro
    không tự cảm ơn); không outro → chỉ giữ câu xin + câu cảm ơn CUỐI CÙNG. Trả (text, số câu đã xoá)."""
    t = text.rstrip()
    duoi = ""
    if outro and t.endswith(outro):
        t, duoi = t[:-len(outro)], outro
    cau = [(i, s) for i, p in enumerate(t.split("\n")) for s in re.split(r"(?<=[。！？])", p) if s.strip()]
    xin = [k for k, (_, s) in enumerate(cau) if re.search(CTA_XIN, s)]
    cam = [k for k, (_, s) in enumerate(cau) if re.search(CTA_CAM_ON, s) and k not in xin]
    if duoi:
        bo = set(xin) if re.search(CTA_XIN, duoi) else set(xin[:-1])
        bo |= set(cam) if re.search(r"(ありがとう|感謝)", duoi) else set(cam[:-1])
    else:
        bo = set(xin[:-1]) | set(cam[:-1])
    if not bo:
        return text, 0
    dong = t.split("\n")
    giu = {i: [] for i in range(len(dong))}
    for k, (i, s) in enumerate(cau):
        if k not in bo:
            giu[i].append(s)
    bi_xoa = {i for k, (i, _) in enumerate(cau) if k in bo}
    moi = [("".join(giu[i]) if i in bi_xoa else d) for i, d in enumerate(dong)]
    moi = [d for i, d in enumerate(moi) if not (i in bi_xoa and not d.strip())]   # dòng chỉ có CTA → bỏ hẳn
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(moi)).rstrip()
    if duoi:
        out = out + "\n\n" + duoi
    return out, len(bo)


def _bam_goc(text, competitor, nguong=0.72):
    """WARN: đoạn (≥60 chữ) có ≥nguong bigram nằm trong bản gốc. Chỉ cảnh báo, Sol đọc kèm."""
    comp = qc_script._bigrams(competitor)
    ra = []
    for i, p in enumerate([x for x in text.split("\n") if x.strip()], 1):
        if len(p) < 60:
            continue
        bg = qc_script._bigrams(p)
        if bg and len(bg & comp) / len(bg) >= nguong:
            ra.append(f"đoạn {i} bám bản gốc {len(bg & comp)/len(bg):.0%} bigram:「{p[:30]}…」")
    return ra


def _go_cau_trung(text, min_len=12, cho_phep=()):
    """Xoá câu lặp NGUYÊN VĂN (≥min_len chữ) lần 2 trở đi — giữ lần đầu. Tất định; ep03: 1 câu trùng sau patch Sol
    làm tốn 1 lượt Fable chỉ để xoá 1 câu → máy tự gỡ. Trả (text, số câu đã xoá).
    cho_phep: cụm được PHÉP lặp nguyên văn (profile `script.gate.repeat_ok`) — Lane K 2026-09-24: câu cửa miệng
    「それ、私の担当じゃないんで」 PHẢI lặp 3–4 lần theo luật kênh; không miễn thì máy xoá mất cả payoff lẫn câu kết
    (đo thật ep01: xoá 3 câu, cắt đôi 「主任の仕事、ですか。それ、…」 → Sol FIX 2 vòng vì đúng lỗi do máy gây ra)."""
    seen, n_xoa, out_paras = set(), 0, []
    for para in text.split("\n"):
        parts = re.split(r"(?<=[。！？])", para)
        keep = []
        for sent in parts:
            key = sent.strip()
            if cho_phep and any(c and c in key for c in cho_phep):
                keep.append(sent)
                continue
            if len(key) >= min_len and key in seen:
                n_xoa += 1
                continue
            if len(key) >= min_len:
                seen.add(key)
            keep.append(sent)
        out_paras.append("".join(keep))
    return "\n".join(out_paras), n_xoa


def do_tat_dinh(prof, text, ctx, competitor, minutes, hook="", title=""):
    """Trả (text_sau_tu_sua, metrics, viec_fact[], viec_len[], warn[]). Tự sửa tất định: 、cắt cụm, outro.
    hook: đoạn mở đầu đã khoá (H1-H4) — rỗng thì hành xử y hệt luồng cũ (tập chưa có hook / lane chưa bật hook)."""
    g = dict(profiles.gate(prof))
    sc = prof.get("script", {}) or {}
    tu_sua = []
    # Lane K (2026-09-24): câu cửa miệng của TẬP = cụm「…」đầu tiên trong tiêu đề → được phép lặp nguyên văn
    # (gate.repeat_title_quote), cộng với gate.repeat_ok cố định. Đổi theo tập mà không phải sửa profile.
    if g.get("repeat_title_quote") and title:
        mq = re.search(r"「([^」]{4,})」", title)
        if mq:
            g["repeat_ok"] = list(g.get("repeat_ok") or []) + [mq.group(1)]
    # 2026-09-23: giữ bản GỐC (trước mọi tự-sửa) riêng cho 2 phép kiểm hook bên dưới — _go_cau_trung (dedup câu
    # trùng) chạy TRƯỚC và xoá y hệt đoạn "kể lại hook" (>=12 chữ trùng nguyên văn) nếu Fable chép lại hook,
    # làm ke_lai_hook() đo trên `text` cuối luôn ra ~0 dù Fable THẬT SỰ đã kể lại — đo trên bản gốc mới đúng ý đồ.
    text_goc = text
    text = ai_steps._go_cat_neu_ja(prof, text)
    text, doi = _outro_fix(text, sc.get("outro_line") or "")
    if doi:
        tu_sua.append("outro thay nguyên văn")
    text, n_cta = _cta_mot_lan(text, sc.get("outro_line") or "")
    if n_cta:
        tu_sua.append(f"xoá {n_cta} câu CTA thừa (CTA chỉ 1 lần ở cuối)")
    text, n_trung = _go_cau_trung(text, cho_phep=tuple(g.get("repeat_ok") or ()))
    if n_trung:
        tu_sua.append(f"xoá {n_trung} câu lặp nguyên văn")
    target = profiles.target_chars(prof, minutes)
    bad, m = ai_steps.check(prof, text, minutes)
    viec_len, viec_fact, warn = [], [], []
    for b in bad:
        if b.startswith("DÀI"):
            over = m["chars"] - target
            viec_len.append(f"NÉN: rút {over:,}–{int(over*1.25):,} chữ (đang {m['chars']:,}, mục tiêu {target:,}±{int(target*0.08):,})")
        elif b.startswith("NGẮN"):
            under = target - m["chars"]
            viec_len.append(f"NỚI: viết thêm {under:,}–{int(under*1.2):,} chữ vào phần THÂN (các mục/chặng giữa, không thêm vào mở đầu), giữ mọi dữ kiện")
        elif b.startswith("HỘI THOẠI ÍT"):
            viec_len.append(f"THOẠI {m['dialogue_ratio']:.0%} < {g['dialogue_ratio_min']:.0%}: đổi các đoạn người kể TÓM TẮT "
                            f"cuộc nói chuyện/hành động giữa người với người thành đối đáp 「」 ngắn (mỗi 「…」 1 câu riêng, "
                            f"trước lượt mới có câu người kể nêu ai nói); giữ nguyên hook, số liệu và độ dài")
        elif b.startswith("HỘI THOẠI"):
            viec_len.append(f"THOẠI {m['dialogue_ratio']:.0%} > {g['dialogue_ratio_max']:.0%}: đổi các câu thoại GIẢI THÍCH dài sang địa văn (心の声/状況), giữ đối đáp ngắn")
        elif b.startswith(("NHỊP", "HƠI")):
            viec_len.append(f"NHỊP: {b} — tách câu >40 chữ / thêm 、 đúng chỗ ngắt hơi")
        elif b.startswith("NHỊP SAI CHỖ"):
            pass  # đã go_cat_cum
        else:
            viec_len.append(b)
    # Ngân sách ±tol (8%) chặt hơn gate cũ (12%) — ep07 lock 5.732 chữ (−11,5%) vì chỉ ai_steps.check kiểm → S3 phải kiểm theo budget
    ns_ = ngan_sach(prof, target)
    if not any(v.startswith(("NÉN", "NỚI")) for v in viec_len):
        if m["chars"] < ns_["lo"]:
            under = ns_["target"] - m["chars"]
            viec_len.append(f"NỚI: viết thêm {under:,}–{int(under*1.2):,} chữ vào các MỤC (không thêm vào mở đầu), giữ mọi dữ kiện (đang {m['chars']:,} < sàn ngân sách {ns_['lo']:,})")
        elif m["chars"] > ns_["hi"]:
            over = m["chars"] - ns_["target"]
            viec_len.append(f"NÉN: rút {over:,}–{int(over*1.25):,} chữ (đang {m['chars']:,} > trần ngân sách {ns_['hi']:,})")
    # Lane ĐA GIỌNG (Lane K, 2026-09-24): mỗi câu thoại phải là 1 câu「…」đứng riêng để gan_vai.py gắn đúng giọng
    # và bóng thoại. Đơn vị câu (cau_vai.tach_cau) không phải thoại mà không kết thúc bằng dấu câu = mảnh lời dẫn
    # dính ngoặc (「…」と彼は言った / 彼は「…」と言った). Lane không khai field = không kiểm.
    if g.get("dialogue_own_sentence"):
        import cau_vai
        _cs = cau_vai.tach_cau(text)
        manh = [c["text"] for k, c in enumerate(_cs)
                if not cau_vai.la_thoai(c["text"]) and (
                    not re.search(r"[。！？!?」]$", c["text"].strip())                 # 彼は「…」 → mảnh "彼は"
                    or (k and cau_vai.la_thoai(_cs[k - 1]["text"]) and _cs[k - 1]["para"] == c["para"]
                        and re.match(r"^[とっ、]", c["text"].strip())))]                # 「…」と彼は言った
        if manh:
            viec_len.append(f"THOẠI DÍNH LỜI DẪN: {len(manh)} chỗ, vd「{manh[0][:30]}」— tách mỗi câu「…」thành câu riêng, "
                            f"lời dẫn (ai nói) viết thành câu người kể riêng trước/sau, kết bằng 。")
    if sc.get("cam_on_cuoi", sc.get("cung_cam_xuc", True)):
        kt = _ket_thieu(text)
        if kt:
            viec_len.append("KẾT THIẾU: 15% cuối bài chưa có " + " · ".join(kt) + " — thêm 1–3 câu người kể SAU câu đạo lý: "
                            "cảm ơn đã xem hết video (「最後までご覧いただき、ありがとうございました。」) + xin 高評価 và "
                            "チャンネル登録 — CHỈ bổ sung đúng ý còn thiếu, CTA chỉ 1 lần trong cả bài; lane có outro cố định thì "
                            "đặt ngay TRƯỚC câu outro và không lặp ý outro đã có")
    thieu, n = _markers_thieu(text, g)
    if thieu:
        viec_len.append(f"THIẾU MỤC: không thấy marker mục {thieu}/{n} (1つ目…/第N位…) — mỗi mục phải mở bằng marker")
    b_all = text.replace(chr(10), "")
    outro_txt = sc.get("outro_line") or ""
    b_cta = b_all.replace(outro_txt, "")          # outro có chữ コメント — không tính
    vi_tri = [m.start() / max(len(b_cta), 1) for m in re.finditer("コメント", b_cta)]
    cta_rng = g.get("cta_mid")                    # [lo, hi] tỉ lệ vị trí; lane không khai = không có luật này
    giua = [v for v in vi_tri if cta_rng and cta_rng[0] <= v <= cta_rng[1]]
    if cta_rng and not giua:
        # LUẬT CỨNG LANE (handoff §3.6, kênh mẫu like-rate 0,3–1,6%): phải có 1 câu CTA GIỮA video. Bài học ep02:
        # Sol dời CTA xuống cuối vì "chưa biết đủ 5 mục" — đúng logic, sai luật lane → máy bắt, Sol được báo (extra_note).
        viec_len.append("THIẾU CTA GIỮA VIDEO: cần 1 câu mời bình luận ở 40–65% (sau mục 2 hoặc 3), hỏi điều khán giả ĐÃ biết tới lúc đó "
                        "(vd 「ここまでの中で、あなたなら何から始めますか」 hoặc hỏi về thói quen/kinh nghiệm của họ) — CTA cuối video giữ nguyên nếu đã có")
    # FACT ↔ tư liệu (tầng A qc_facts; bỏ tên riêng katakana — nhân vật hư cấu)
    nguon = (so_duoc_phep(ctx) + "\n" + ctx) if ctx else ""
    if nguon:
        for x in qc_facts.chi_tiet_thieu_nguon(text, nguon):
            if x["kind"] == "ten_rieng_khong_co_trong_tu_lieu":
                continue
            if x["kind"] == "dia_danh_khong_co_trong_tu_lieu" and (sc.get("mode") or "").lower() != "documentary":
                warn.append(f"địa danh「{x['token']}」không có trong tư liệu — quê nhân vật hư cấu thì được; nơi GIỚI THIỆU cho người xem thì phải thêm vào series_ctx")
                continue
            if x["kind"] == "so_lieu_khong_co_trong_tu_lieu":
                continue   # thay bằng _so_lieu_ngoai_tu_lieu (bắt cả kanji, lọc số nhỏ)
            viec_fact.append(f"DỮ KIỆN「{x['token']}」không có trong tư liệu (câu:「{(x['cau'] or '')[:40]}」) → xoá, diễn đạt định tính, hoặc sửa đúng theo dòng [Dn]")
        viec_fact += _so_lieu_ngoai_tu_lieu(text, nguon, tuple(sc.get("fact_exempt_units") or ()))
    viec_fact += _nhat_quan_ten_tuoi(text)
    viec_fact += _tong_tien(text)
    # Số học tất định (qc_numbers: phép nhân/cộng, khoảng năm/tháng, %, tuổi theo năm sinh) — bài học ep02 2026-09-20:
    # 「2袋110円+プランター110円+土110円+肥料110円 → 総額600円」 lọt qua S3, Sol lần 3 mới bắt. Máy phải bắt trước.
    for x in qc_numbers.arithmetic(text):
        if x.get("sev") in ("cao", "vua"):
            viec_fact.append(f"SỐ HỌC: {x['msg'][:160]}")
        else:
            warn.append(f"số học: {x['msg'][:120]}")
    # máy móc qc_script: trùng/lặp → việc; mở đầu → warn
    # 2026-09-23 (vá review cuối, Việc 1): `warn_no_marker` KHÔNG được truyền vô điều kiện — mục
    # `mo_dau_khong_do` chỉ có nghĩa khi cổng mở đầu THẬT SỰ do hook_stage canh (script.hook.enabled=
    # true). 4 kênh irogatatarukioku/satori-jp-obaa/teinengo-real/toshi-densetsu-jp chưa bật hook
    # (không khai gate.hook_marker) nhưng vẫn bị bật cảnh báo này ở MỌI tập, rồi `warn` bị ghi thẳng
    # vào do.json/escalation — báo sai "mở đầu do hook_stage kiểm" trong khi không có cổng nào đang
    # canh. Dòng print tương ứng (bên dưới, ~462) đã được đóng công tắc ở lần vá trước, dòng này bị
    # sót — sửa cho khớp: chỉ warn khi hook_stage.is_enabled(prof).
    for x in qc_script.mechanical(text, prof.get("language", "ja"), g, warn_no_marker=hook_stage.is_enabled(prof)):
        if x["kind"] in ("cau_trung_lap", "cau_gan_trung"):
            viec_len.append(f"TRÙNG: {x['msg'][:120]}")
        elif x["kind"] in ("mo_dau_qua_dai", "mo_dau_qua_ngan", "mo_dau_noi_suong", "mo_dau_khong_do", "lap_y_ke_lai", "cum_lap", "doan_vun", "nhieu_moc_tuoi"):
            warn.append(x["msg"][:140])
        elif x["kind"] in ("sot_ngon_ngu_nguon",):
            viec_len.append(x["msg"][:120])
    warn += _bam_goc(text, competitor)
    if hook:
        if not hook_stage.bat_dau_bang_hook(text_goc, hook):
            # 2026-09-26 (Lane M ep01): kèm NGUYÊN VĂN hook vào việc — patch_model chạy claude -p KHÔNG có quyền đọc file,
            # trước đây chỉ được bảo "chép lại hook" mà không được đưa hook → 2 patch liền tự bịa một đoạn "gần giống",
            # S3 vẫn báo lệch → ESCALATE oan (đo thật: patch2 đổi 0% đoạn).
            viec_len.append("HOOK: script không bắt đầu bằng đoạn mở đầu đã khoá — thay đoạn đầu bằng NGUYÊN VĂN đoạn dưới "
                            "(không đổi 1 chữ, không thêm câu vào giữa), xoá mọi đoạn đứng trước nó; đoạn thứ hai nối tiếp, "
                            "không kể lại hook:\n" + hook.strip())
        kl = hook_stage.ke_lai_hook(text_goc, hook)
        if kl > 0.5:
            warn.append(f"thân kể lại hook ({kl:.0%} bigram hook xuất hiện lại ngay sau hook) — nối tiếp, đừng nhắc lại")
    if not hook and hook_stage.is_enabled(prof):
        # 2026-09-23 (patch review Task 9, Minor V3 + vá thêm cùng ngày): KHÔNG append vào `warn` —
        # `warn` được ghi vào do.json/ESCALATION_REPORT. Trước đây dòng print này chạy VÔ ĐIỀU KIỆN
        # mỗi khi `hook` rỗng — vì công tắc `script.hook.enabled` mặc định TẮT cho cả 6 kênh đang
        # sản xuất, `hook` luôn rỗng ⇒ dòng nhắc này in ra ở MỌI tập của MỌI kênh (trái với cam kết
        # "hook='' hành xử y hệt trước khi có tính năng hook", tức im lặng khi công tắc tắt). Giờ chỉ
        # in khi CÔNG TẮC ĐANG BẬT cho kênh này (qua hook_stage.is_enabled — không tự suy luận theo
        # tên/id kênh) mà tập vẫn chưa có hook đã khoá; công tắc tắt thì im lặng hoàn toàn như cũ.
        print("   (warn) chưa có hook đã khoá (tập cũ?) — cổng mở đầu do hook_stage đảm nhận, chạy `hook_stage.py --mode repair`")
    m["tu_sua"] = tu_sua
    return text, m, viec_fact, viec_len, warn


# ============================================================ S4 — patch có ràng buộc (model = script.patch_model, mặc định = brain_model)
PRESERVE = ("PHẢI GIỮ NGUYÊN: mọi con số/địa điểm/thông tin thực tế · trình tự thời gian · quan hệ nhân–quả · các bước "
            "ngoặt cảm xúc · mục cuối (cú lật) và kết/payoff · các câu thoại ngắn đối đáp · câu CTA mời bình luận · câu "
            "outro nguyên văn ở cuối · marker mục (1つ目…/第N位) nếu bài có · ĐOẠN MỞ ĐẦU ĐÃ KHOÁ (hook, đoạn đầu tiên) — "
            "giữ nguyên từng chữ, không thêm gì phía trước. KHÔNG thêm tình tiết, dữ kiện, lời khuyên, cảnh báo mới.")


def _tyle_doan_doi(a, b):
    pa = [p.strip() for p in a.split("\n") if p.strip()]
    pb = set(p.strip() for p in b.split("\n") if p.strip())
    if not pa:
        return 1.0
    return sum(1 for p in pa if p not in pb) / len(pa)


def patch(prof, text, viec, kieu, ns, log, n_patch):
    """kieu ∈ nen | noi | sua (máy) | sol. Trả text mới hoặc ném LLMError khi bản patch bị từ chối."""
    cur = ai_steps.measure(text)["chars"]
    ds = "\n".join(f"- {v}" for v in viec)
    if kieu == "nen":
        over = cur - ns["target"]
        nv = (f"NHIỆM VỤ: rút ngắn {over:,}–{int(over*1.25):,} chữ (không tính xuống dòng). KHÔNG viết lại toàn bài — chỉ cắt/gọn tại chỗ.\n"
              f"{PRESERVE}\nƯU TIÊN CẮT THEO THỨ TỰ: (1) giải thích lặp lại · (2) cảm xúc tả hai lần · (3) câu chuyển đoạn dư · "
              f"(4) tả cảnh trang trí · (5) câu tu từ lặp. Cắt đều — không xoá trọn 1 mục.")
        lo, hi, diff_max = ns["lo"], ns["hi"], 0.70
    elif kieu == "noi":
        nv = (f"NHIỆM VỤ: viết THÊM để đạt {ns['lo']:,}–{ns['hi']:,} chữ (đang {cur:,}). Thêm vào phần THÂN — các mục/chặng giữa "
              f"(chi tiết đời thường, đối đáp ngắn), KHÔNG thêm vào mở đầu, KHÔNG thêm dữ kiện/số liệu mới.\n{PRESERVE}")
        lo, hi, diff_max = ns["lo"], ns["hi"], 0.70
    else:
        nv = (f"NHIỆM VỤ: SỬA TẠI CHỖ đúng các điểm dưới đây — mọi thứ khác giữ nguyên từng chữ. Không viết lại toàn bài, "
              f"không đổi văn phong, tổng độ dài trong khoảng {max(int(cur * 0.90), 0):,}–{max(int(cur * 1.05), ns['hi']):,} chữ.\n{PRESERVE}\nCÁC ĐIỂM PHẢI SỬA:\n{ds}")
        # Trần = max(1,05× hiện tại, trần ngân sách); sàn = min(0,9×, sàn ngân sách) khi đang dưới mục tiêu. Bản DƯỚI mục tiêu mà
        # Sol yêu cầu bổ sung (trả lời hứa tiêu đề) thì thêm chữ là hợp lệ — ep03: 2 patch tốt bị từ chối vì 6.585 > 6.561 (1,05×)
        # trong khi ngân sách cho tới 6.991 → ESCALATE oan.
        lo = min(int(cur * 0.90), ns["lo"]) if cur < ns["target"] else int(cur * 0.90)
        hi, diff_max = max(int(cur * 1.05), ns["hi"]), 0.40
    prompt = (nv + "\n\nOUTPUT: toàn văn kịch bản sau khi sửa, tiếng Nhật, không lời dẫn/giải thích/tiêu đề, "
              "giữ nguyên cách chia đoạn.\n\n=== KỊCH BẢN ===\n" + text)
    r = claude_p_bridge.ask(prompt, model=claude_p_bridge.patch_model_of(prof), timeout=1500,
                            min_chars=lo, max_chars=hi, require_sentence_end=True)
    new = ai_steps.normalize_paragraphs(ai_steps.strip_markers(r.text))
    ty = _tyle_doan_doi(text, new)
    if ty > diff_max:
        raise LLMError(f"patch {n_patch} ({kieu}) đổi {ty:.0%} đoạn > trần {diff_max:.0%} — viết lại quá tay, từ chối")
    if kieu in ("nen", "noi"):
        mat = _nums(text) - _nums(new)
        if mat:
            raise LLMError(f"patch {n_patch} ({kieu}) làm MẤT số: {sorted(mat)[:6]} — từ chối")
    log.append(f"patch{n_patch} {kieu} {r.model} {ai_steps.measure(new)['chars']:,} chữ đổi {ty:.0%} đoạn {r.elapsed:.0f}s")
    return new


# ============================================================ S5 — Sol (lời cuối)
def sol_qc(prof, text, title, out, ns, m, hook=""):
    muc_txt = f"đủ {ns['n']} mục" if ns.get("n") else f"đủ {len(ns.get('sections') or [])} chặng theo ngân sách"
    note = (f"(Máy đã kiểm và ĐẠT: tổng {m['chars']:,} chữ trong {ns['lo']:,}–{ns['hi']:,} · {muc_txt} · nhịp/phẩy/thoại · "
            f"mọi số liệu/địa danh khớp tư liệu · outro/CTA có. Đừng lặp lại các mục đó — tập trung vào tính hợp lý của "
            f"câu chuyện, nhân quả, dòng thời gian, động cơ nhân vật, câu tiếng Nhật không tự nhiên, lời hứa tiêu đề có được trả. ")
    if (prof.get("script") or {}).get("cung_cam_xuc", True):
        # 2026-09-26: không có dòng này Sol sẽ coi nhân vật "quá đáng ghét" là thiếu cân bằng và đề nghị làm dịu → vòng
        # patch xoá đúng thứ anh muốn giữ. Sol vẫn bắt khi hành vi PHI LÝ/mâu thuẫn, chỉ không được bắt vì "quá gắt".
        note += ("LUẬT LANE: nửa đầu bài CỐ Ý làm người xem ức chế/giận (nhân vật gây chuyện đáng ghét, bất công leo thang, "
                 "chưa giải toả) rồi mới giải toả và kết bằng vị tha — đừng đề nghị làm dịu, cân bằng hay giải thích sớm cho "
                 "nhân vật đó; chỉ nêu khi hành vi phi lý, không nhất quán hoặc người bị hại cư xử vô lý. ")
    if profiles.gate(prof).get("cta_mid"):
        note += "LUẬT LANE: câu mời bình luận GIỮA video là bắt buộc — không đề nghị dời nó xuống cuối; nếu câu hỏi chưa hợp lúc đó thì đề nghị ĐỔI CÂU HỎI. "
    # luật riêng khác của lane (profile script_qc.lane_rules: list câu) → Sol biết, không "sửa" nhầm thành lỗi
    for r in ((prof.get("script_qc") or {}).get("lane_rules") or []):
        note += f"LUẬT LANE: {r} "
    note = note.rstrip() + ")"
    return qc_script_sol.run(text, title, profile_id=prof["id"], out=str(out), extra_note=note,
                              hook_block=(qc_script_sol.NOI_TU_HOOK.format(hook=hook) if hook else ""))


def _title(d: Path):
    for name in ("title.txt", "listting.txt"):
        f = d / name
        if f.exists():
            for l in f.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    return l.strip()
    return "(chưa chốt tiêu đề)"


# ============================================================ ORCHESTRATOR
def run(job, force=False):
    """job = make_video.Job. Ghi script.txt · script.pre_patchN.txt · do.json · qc_sol_report_k.txt · script.lock.json
    · bench.jsonl. Ném SystemExit khi BLOCK/ESCALATE (trừ force)."""
    prof, d = job.p, job.dir
    t0 = time.time()
    log, bench = [], {"slug": job.slug, "lens": qc_script_sol.load_lens(prof["id"]), "fable_calls": 0, "sol_calls": 0,
                      "patch_count": 0, "s3_fail_count": 0, "sol_fail_count": 0, "manual_intervention": False}
    competitor = (d / "competitor.txt").read_text(encoding="utf-8") if (d / "competitor.txt").exists() else ""
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else ""
    minutes = job.minutes
    ns = ngan_sach(prof, profiles.target_chars(prof, minutes))

    def ket(state, **info):
        bench.update(total_time_s=round(time.time() - t0), final_state=state, **{k: v for k, v in info.items() if k != "sol_report"})
        meta = gate_common.ghi_lock(d, state, patches=bench["patch_count"], log=log, **info)
        with (d / "bench.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(bench, ensure_ascii=False) + "\n")
        return meta

    # ---- S1Q
    loi = s1q_ho_so(d, prof, competitor, ctx)
    if loi:
        print("[S1Q] hồ sơ THIẾU:"); [print("   -", x) for x in loi]
        ket("BLOCK", reason="S1Q", issues=loi)
        raise SystemExit("✗ S1Q: hồ sơ chưa đủ → BLOCK (chưa tốn lượt viết nào).")
    # ---- S1L: LUẬT HOOK + GÓI ĐĂNG (anh chốt 2026-09-24) — chặn TRƯỚC khi tốn lượt LLM nào.
    # Đặt Ở ĐÂY (sau S1Q, trước H1–H4/S2) là có chủ ý: đây là cửa DUY NHẤT mà cả 6 lane đều đi qua
    # trước khi viết. Trước đó luật chỉ nằm trong CLAUDE.md + docs/QUY_TAC_GOI_DANG.md nên đo thật
    # 2026-09-24: `script.hook.enabled` mới bật ở 3/6 lane dù luật đã chốt từ 23/09 — tức luật bằng
    # văn bản thì phải có người nhắc mới chạy. Cùng bài học memory
    # `khong-giao-viec-thu-cong-rao-nam-trong-tool`: rào phải nằm trong TOOL.
    loi_luat = qc_goi_dang.cong_truoc_khi_viet(d, prof)
    if loi_luat:
        print("[S1L] LUẬT HOOK + GÓI ĐĂNG chưa đủ điều kiện để viết:")
        [print("   -", x) for x in loi_luat]
        ket("BLOCK", reason="S1L", issues=loi_luat)
        raise SystemExit("✗ S1L: chưa đủ điều kiện luật hook/gói đăng → BLOCK (chưa tốn lượt viết nào).")
    print("[S1L] ✓ luật hook + gói đăng: hook bật · goi_dang bật · promise.txt đã chốt")
    if not (d / "title.txt").exists() and not (d / "listting.txt").exists():
        print("[S1Q] ⚠️ chưa có title.txt — Sol sẽ không kiểm 'lời hứa tiêu đề có được trả' (ep01: đây là lỗi nặng nhất Sol bắt)")
    print(f"[S1Q] ✓ hồ sơ đủ · ngân sách {ns['target']:,} chữ = mở đầu {ns['mo_dau']:,} + {ns['n']}×{ns['moi_muc']:,} + kết {ns['ket']:,} (±{int(ns['tol']*100)}%)")

    # ---- H1–H4 (hook thượng nguồn, anh chốt 2026-09-23) — chỉ khi S2 sắp VIẾT MỚI; tập đã có script + lock → repair mode riêng
    sf = d / "script.txt"
    co_lock = (d / gate_common.LOCK_NAME).exists()
    se_viet_moi = force or not (sf.exists() and ((job.state.get("B3") or {}).get("flow") == "lean" or co_lock))
    # 2026-09-23 (vá review dọn hook, V2): (a) dùng hook_stage.doc_lock(d) thay vì kiểm cứng đường
    # dẫn "hook/hook_lock.json" — đổi tên file lock thì cảnh báo này không được lặng lẽ biến mất;
    # (b) bỏ vế `se_viet_moi and` thừa: se_viet_moi = force or (...) nên `force` đã hàm ý se_viet_moi.
    # 2026-09-23 (Việc 2, vá review cuối): công tắc BẬT THEO KÊNH — `script.hook.enabled` mặc định
    # False (hook_stage.MAC_DINH). Kênh CHƯA bật: hook="" và toàn bộ khối này lặng thinh, chạy y hệt
    # trước khi có tính năng hook (không in thêm dòng nào mỗi tập) — hàng rào #2 của CLAUDE.md, khác
    # biệt lane chỉ đi qua field profile, cấm if theo id kênh.
    hook = ""
    if hook_stage.is_enabled(prof):
        if force and hook_stage.doc_lock(d):
            print("[H1-H4] ⚠️ --force: bỏ qua hook đã khoá, viết hook MỚI (tốn lượt LLM + gọi lại H1–H3)")
        if se_viet_moi:
            hook = hook_stage.ensure_locked(d, prof, ctx=ctx, title=_title(d), mode="upstream", force=force)
            bench["hook_sol_rounds"] = (hook_stage.doc_lock(d) or {}).get("sol_rounds", 0)
        else:
            hook = hook_stage.doc_hook(d)
            if not hook:
                print("[H4] ⚠️ tập đã có script.txt mà chưa có hook — dùng `py -3.13 hook_stage.py --profile … --slug … --mode repair`")

    # ---- S2
    # 2026-09-23: PHẢI dùng đúng `se_viet_moi` (đã tính ở khối H1-H4 trên) — KHÔNG chép lại biểu thức. Hai nhánh này
    # là phủ định của nhau theo thiết kế (viết mới ⟺ không dùng script.txt cũ); chép tay 2 lần từng lệch nhau âm thầm
    # nếu chỉ sửa 1 chỗ, rơi vào 1 trong 2 trạng thái tệ nhất: chạy lại H1-H4 tốn tiền cho tập đã xong, hoặc S2 viết
    # mới mà hook="" (patch review Task 9, Important finding V1).
    if not se_viet_moi:
        # có lock (kể cả ESCALATE): bản đã qua vòng trước và/hoặc người đã sửa tay → chấm lại, KHÔNG viết lại từ đầu
        text = sf.read_text(encoding="utf-8")
        print(f"[S2] dùng script.txt đã có ({ai_steps.measure(text)['chars']:,} chữ) — chạy tiếp S3→Sol (không viết lại)")
    else:
        print(f"[S2] Fable viết đúng ngân sách …")
        text = viet(prof, competitor, ctx, minutes, ns, log, hook=hook,
                    luat=qc_goi_dang.khoi_luat_cho_prompt(d, prof), d=d)
        bench["fable_calls"] += 2 if not (prof.get("script", {}) or {}).get("use_raw_source") else 1
        (d / "script_pass1_raw.txt").write_text(text, encoding="utf-8")
        sf.write_text(text, encoding="utf-8")
    title = _title(d)

    def do_va_ghi(text):
        text, m, vf, vl, warn = do_tat_dinh(prof, text, ctx, competitor, minutes, hook=hook, title=title)
        (d / "do.json").write_text(json.dumps({"metrics": {k: v for k, v in m.items() if k != "markers"}, "viec_fact": vf, "viec_len": vl, "warn": warn},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[S3] {m['chars']:,} chữ ≈ {m['minutes']}' · phẩy/câu {m['comma_per_sentence']} · hơi {m['chars_per_breath']} · thoại {m['dialogue_ratio']:.0%}"
              + (f" · tự sửa: {', '.join(m['tu_sua'])}" if m.get("tu_sua") else ""))
        for x in vf: print("   [FACT]", x)
        for x in vl: print("   [LEN/STRUCT]", x)
        for x in warn: print("   (warn)", x)
        return text, m, vf, vl, warn

    def thu_patch(text, viec, kieu, mien_tran=False):
        n = bench["patch_count"] + 1
        if n > MAX_PATCH and not mien_tran:
            return None
        (d / f"script.pre_patch{n}.txt").write_text(text, encoding="utf-8")
        try:
            try:
                new = patch(prof, text, viec, kieu, ns, log, n)
            except LLMError as e1:
                # 05/10: nhiều lane chạy lô song song → claude -p có thể nghẽn/quá tải thoáng qua. Thử lại 1 lần
                # sau 90s để lỗi tạm KHÔNG ăn mất 1 trong MAX_PATCH lượt vá (mất lượt = khoá bản chưa sửa).
                print(f"   ! patch{n} lỗi ({str(e1)[:80]}) → thử lại sau 90s")
                time.sleep(90)
                new = patch(prof, text, viec, kieu, ns, log, n)
        except LLMError as e:
            print(f"   ✗ {e}")
            log.append(f"patch{n} {kieu} TỪ CHỐI: {str(e)[:100]}")
            bench["patch_count"] = n
            bench["fable_calls"] += 1
            return text  # giữ bản trước, vẫn tính lượt
        bench["patch_count"] = n
        bench["fable_calls"] += 1
        sf.write_text(new, encoding="utf-8")
        return new

    # ---- S3 (+ patch máy). `viec_tay.txt` = việc do Claude Code (lớp 3) đưa vào sau khi đọc bản khoá/ESCALATE —
    # đi qua đúng vòng patch→S3→Sol, không sửa tay. Đọc 1 lần rồi đổi tên .done.
    vt = d / "viec_tay.txt"
    viec_tay = [l.strip("- ").strip() for l in vt.read_text(encoding="utf-8").splitlines() if l.strip()] if vt.exists() else []
    if viec_tay:
        print(f"[S3] + {len(viec_tay)} việc từ viec_tay.txt (lớp 3)")
        k, done = 1, d / "viec_tay.done.txt"
        while done.exists():                      # lớp 3 có thể ra việc nhiều lần cho 1 tập (ep03: 3 lần) — Windows rename không ghi đè
            k += 1
            done = d / f"viec_tay.done{k}.txt"
        vt.rename(done)
    text, m, vf, vl, warn = do_va_ghi(text)
    vl = vl + viec_tay
    if text != sf.read_text(encoding="utf-8"):
        sf.write_text(text, encoding="utf-8")
    while vf or vl:
        bench["s3_fail_count"] += 1
        kieu = "nen" if any(v.startswith("NÉN") for v in vl) and not vf else ("noi" if any(v.startswith("NỚI") for v in vl) and not vf else "sua")
        print(f"[S4] patch máy ({kieu}) …")
        new = thu_patch(text, vf + vl, kieu)
        if new is None:
            gate_common.viet_escalation_report(d, "S3", [{"attempt": bench["patch_count"], "status": "FAIL", "blocking_issues": vf + vl, "warnings": warn}],
                                               "gate số/dữ kiện không nắn được sau 2 patch — người đọc do.json và quyết")
            ket("ESCALATE", reason="S3", issues=vf + vl)
            raise SystemExit("✗ S3: còn lỗi cơ học/dữ kiện sau 2 patch → ESCALATE (ESCALATION_REPORT.md), pha asset BLOCK.")
        if new == text:  # patch bị từ chối
            continue
        text, m, vf, vl, warn = do_va_ghi(new)
        sf.write_text(text, encoding="utf-8")

    # ---- S5 Sol (lời cuối) + vòng patch Sol
    # Anh chốt 2026-09-29: bỏ kênh sức khoẻ (Lane E) — lớp Sol khác hãng vốn BẮT BUỘC cho kênh y khoa
    # (rủi ro an toàn thật) không còn lý do bắt buộc cho lane manga/lifestyle còn lại. `script.sol_qc=false`
    # (mặc định true = giữ nguyên hành vi cũ) → khoá PASS thẳng sau S3, không gọi Sol, không tốn patch/token
    # ở bước này. Bật lại cho lane nào cần thì xoá field hoặc đặt true.
    if (prof.get("script") or {}).get("sol_qc", True) is False:
        # Kiểm NHẸ lời hứa tiêu đề (anh chốt 2026-09-29, thay Sol): 1 lượt chấm → nếu có việc thì patch_model (Opus 5) vá
        # ĐÚNG 1 lần (không tính vào trần MAX_PATCH) → S3 lại → khoá. KHÔNG lặp, KHÔNG ESCALATE; patch làm S3 trượt thì
        # giữ bản trước. Lỗi hạ tầng → khoá không có bước này, log ghi "chưa kiểm". Mỗi bản (sha) chỉ kiểm 1 lần.
        if (prof.get("script") or {}).get("kiem_loi_hua", True):
            sha_f = d / "loi_hua_da_kiem.json"
            sha_now = gate_common.sha256_file(sf)
            da = json.loads(sha_f.read_text(encoding="utf-8")).get("sha") if sha_f.exists() else None
            if da == sha_now:
                print("[S5L] bản này đã kiểm lời hứa tiêu đề rồi — bỏ qua")
            else:
                print("[S5L] kiểm lời hứa tiêu đề (1 lượt, chỉ cảnh báo) …")
                try:
                    st, viec_h, mod_h = qc_loi_hua.kiem(text, title, d)
                except Exception as e:
                    st, viec_h, mod_h = "LOI", [], ""
                    print(f"   ⚠️ chưa kiểm được lời hứa tiêu đề ({str(e)[:100]}) — khoá KHÔNG có bước này")
                    log.append("loi_hua CHUA_KIEM")
                if st == "VIEC":
                    (d / "loi_hua_tieu_de.txt").write_text(f"[{mod_h}]\n" + "\n".join(f"- {v}" for v in viec_h) + "\n", encoding="utf-8")
                    print(f"   [{mod_h}] {len(viec_h)} việc → patch_model vá 1 lần:")
                    for v in viec_h:
                        print("   -", v[:160])
                    text_truoc = text
                    new = thu_patch(text, ["LỜI HỨA TIÊU ĐỀ: sửa đúng câu nêu, mọi thứ khác giữ nguyên. Tiêu đề: " + title] + viec_h,
                                    "sua", mien_tran=True)
                    ok = False
                    if new and new != text_truoc:
                        n2, m2, vf2, vl2, _w = do_va_ghi(new)
                        if vf2 or vl2:
                            print("   ⚠️ bản vá làm S3 trượt → giữ bản trước, việc còn ghi ở loi_hua_tieu_de.txt")
                            log.append("loi_hua VA_TRUOT_S3 giu ban truoc")
                        else:
                            text, m, ok = n2, m2, True
                            sf.write_text(text, encoding="utf-8")
                            log.append(f"loi_hua {mod_h} VIEC={len(viec_h)} da va")
                    else:
                        print("   ⚠️ patch bị từ chối → giữ bản trước, việc còn ghi ở loi_hua_tieu_de.txt")
                        log.append("loi_hua VA_TU_CHOI giu ban truoc")
                    if not ok:
                        sf.write_text(text_truoc, encoding="utf-8")
                        text, m, _a, _b, _c = do_va_ghi(text_truoc)
                elif st == "OK":
                    print(f"   [{mod_h}] ✓ lời hứa tiêu đề được giữ")
                    log.append(f"loi_hua {mod_h} OK")
                if st != "LOI":
                    sha_f.write_text(json.dumps({"sha": gate_common.sha256_file(sf), "status": st}), encoding="utf-8")
        meta = ket("PASS", sol_report="skipped_sol_qc_false", sol_rounds=0, chars=m["chars"], minutes=m["minutes"],
                   final_char_deviation=round((m["chars"] - ns["target"]) / ns["target"] * 100, 1))
        job.state["B3"] = {"at": time.strftime("%Y-%m-%d %H:%M"), "flow": "lean", "chars": m["chars"], "minutes": m["minutes"],
                           "passes": log, "gate": [], "patches": bench["patch_count"], "sol_rounds": 0}
        job.state["B3S"] = {"at": job.state["B3"]["at"], "verdict": "SKIPPED", "flow": "lean", "reason": "profile.script.sol_qc=false"}
        for s in ("B3Q", "B3F", "B3R", "B3G"):
            job.state[s] = {"at": job.state["B3"]["at"], "skipped": "lean_flow"}
        job.state_f.write_text(json.dumps(job.state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[LOCK] ✓ S3 PASS (Sol TẮT theo profile) · {m['chars']:,} chữ · sha {meta['script_sha256'][:10]}… · "
              f"{bench['patch_count']} patch · {bench['total_time_s']//60}'{bench['total_time_s']%60:02d} · KHÔNG AI SỬA script.txt NỮA")
        return "PASS"
    # Sol KHÔNG tất định: 2026-09-22 chấm lại bản ep10 Lane G đã LOCK PASS → 2/2 lần ra FIX với 1 lỗi [NẶNG] timeline
    # thật. Khoá chỉ khi PASS `sol_pass_need` lần LIÊN TIẾP trên cùng bản (mặc định 2; profile script.sol_pass_need=1 tắt).
    need = int((prof.get("script") or {}).get("sol_pass_need") or 2)
    k, streak = 0, 0
    while True:
        k += 1
        out = d / (f"qc_sol_report_{k}.txt")
        print(f"[S5] Sol lần {k} (lens {bench['lens']}) …")
        v, rep = sol_qc(prof, text, title, out, ns, m, hook=hook)
        bench["sol_calls"] += 1
        log.append(f"sol{k} {v}")
        streak = streak + 1 if v == "PASS" else 0
        if v == "PASS" and streak < need:
            print(f"   PASS {streak}/{need} — chấm lại cùng bản để chắc (Sol không tất định)")
            continue
        if v == "PASS":
            meta = ket("PASS", sol_report=out.name, sol_rounds=k, chars=m["chars"], minutes=m["minutes"],
                       final_char_deviation=round((m["chars"] - ns["target"]) / ns["target"] * 100, 1))
            job.state["B3"] = {"at": time.strftime("%Y-%m-%d %H:%M"), "flow": "lean", "chars": m["chars"], "minutes": m["minutes"],
                               "passes": log, "gate": [], "patches": bench["patch_count"], "sol_rounds": k}
            job.state["B3S"] = {"at": job.state["B3"]["at"], "verdict": "PASS", "flow": "lean", "rounds": k}
            for s in ("B3Q", "B3F", "B3R", "B3G"):
                job.state[s] = {"at": job.state["B3"]["at"], "skipped": "lean_flow"}
            job.state_f.write_text(json.dumps(job.state, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[LOCK] ✓ Sol PASS lần {k} · {m['chars']:,} chữ ({bench['final_state']}) · sha {meta['script_sha256'][:10]}… · "
                  f"{bench['patch_count']} patch · {bench['total_time_s']//60}'{bench['total_time_s']%60:02d} · KHÔNG AI SỬA script.txt NỮA")
            return "PASS"
        bench["sol_fail_count"] += 1
        if v == "REMAKE" or v == "UNKNOWN":
            gate_common.viet_escalation_report(d, "SOL", [{"attempt": k, "status": v, "blocking_issues": [rep[:800]]}],
                                               "Sol REMAKE/không đọc được — lỗi thiết kế/phạm vi, người quyết")
            ket("ESCALATE", reason=f"SOL_{v}", sol_report=out.name)
            if not force:
                raise SystemExit(f"✗ S5: Sol {v} → ESCALATE, pha asset BLOCK. Đọc {out.name}.")
            return "ESCALATE"
        # FIX → patch theo Sol (nếu còn lượt) → S3 → Sol lại
        print(f"[S4] patch theo Sol (FIX) …")
        new = thu_patch(text, [f"Theo báo cáo Sol dưới đây, sửa TẠI CHỖ từng điểm KHÔNG HỢP LÝ được đánh số (bỏ qua mục GÓP Ý THÊM):\n{rep}"], "sol")
        if new is None:
            gate_common.viet_escalation_report(d, "SOL", [{"attempt": k, "status": "FIX", "blocking_issues": [rep[:800]]}],
                                               "hết 2 patch mà Sol vẫn FIX — người đọc qc_sol_report và quyết")
            ket("ESCALATE", reason="SOL_FIX_after_2_patch", sol_report=out.name)
            if not force:
                raise SystemExit(f"✗ S5: Sol vẫn FIX sau {MAX_PATCH} patch → ESCALATE, pha asset BLOCK. Đọc {out.name}.")
            return "ESCALATE"
        if new == text:
            print("   patch bị từ chối → chấm lại bản cũ không có ý nghĩa; tiếp lượt patch còn lại nếu có")
            if bench["patch_count"] >= MAX_PATCH:
                gate_common.viet_escalation_report(d, "SOL", [{"attempt": k, "status": "PATCH_REJECTED", "blocking_issues": [rep[:800]]}], "patch bị từ chối 2 lần")
                ket("ESCALATE", reason="patch_rejected", sol_report=out.name)
                raise SystemExit("✗ S4: patch bị từ chối tới hạn → ESCALATE.")
            continue
        text, m, vf, vl, warn = do_va_ghi(new)
        sf.write_text(text, encoding="utf-8")
        if vf or vl:
            new2 = thu_patch(text, vf + vl, "sua")
            if new2 is None or new2 == text:
                gate_common.viet_escalation_report(d, "S3", [{"attempt": bench["patch_count"], "status": "FAIL", "blocking_issues": vf + vl}], "patch Sol sinh lỗi cơ học mới, hết lượt")
                ket("ESCALATE", reason="S3_after_sol_patch", issues=vf + vl)
                raise SystemExit("✗ S3 sau patch Sol: còn lỗi cơ học, hết lượt → ESCALATE.")
            text, m, vf, vl, warn = do_va_ghi(new2)
            sf.write_text(text, encoding="utf-8")
            if vf or vl:
                ket("ESCALATE", reason="S3_still_fail", issues=vf + vl)
                raise SystemExit("✗ S3: vẫn lỗi sau patch cuối → ESCALATE.")
