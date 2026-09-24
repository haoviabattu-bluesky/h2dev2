# -*- coding: utf-8 -*-
r"""qc_goi_dang.py — CỔNG GÓI ĐĂNG (lời hứa · tiêu đề · thumbnail · thứ tự 60–90s), 0 LLM.

Nguồn luật: bàn giao TRENDING-RESEARCH 2026-09-23
  `FlowHandoff_local\results\hook_from_research\NGUYEN_TAC_HOOK_GOI_DANG.md` (10 nguyên tắc)
  + phiếu việc `FlowHandoff_local\shared\PROMPT_H2DEV_AP_DUNG_HOOK_2026-09-23.txt` (mục 2: G1–G8).

Cổng này hiện thực G1–G6 + G8. G7 (channel_analyzer đọc ảnh thumbnail) nằm ở
`pipeline/channel_analyzer.py`, KHÔNG ở đây — đó là việc CẤP KÊNH, không phải cấp tập.

    G1  MỘT LỜI HỨA — `promise.txt` (1 câu) phải có mặt ở tiêu đề · chữ thumbnail · câu đầu mô tả
        · và trong `promise_window_s` giây đầu lời đọc.
    G2  LỜI HỨA GIỮ ĐƯỢC — mọi vế tiêu đề + mọi dòng chữ thumbnail phải grep được trong script.txt
        (so cả chữ số ↔ chữ Hán: 76秒 ↔ 七十六秒). Vế LÕI phải xuất hiện trước giây 90.
        Vế chỉ xuất hiện trong ngữ cảnh PHỦ ĐỊNH → chặn.
    G3  THỨ TỰ 60–90 GIÂY ĐẦU — câu đầu không chào/cảm ơn/tự giới thiệu/đọc chữ 「タイトル」;
        câu mâu thuẫn ≤ ngưỡng lane; lõi tiêu đề ≤ `title_core_max_s`; câu "nghi thức" của kênh có mặt.
    G4  VIDEO DANH SÁCH — không đọc trước danh sách trong `list_preview_ban_s` giây đầu; đếm mục
        thật khớp `gate.list_item_count`; mục 1 để cuối (countdown); bỏ câu tự tháo đếm ngược.
    G5  TIÊU ĐỀ — phải treo một ẩn số; không dùng chữ sợ đứng một mình; không rào.
    G6  THUMBNAIL — mỗi tập CHỈ 1 file thumbnail và `DANG-TAI.txt` phải trỏ đúng file đó.
    G8  KHÔNG CHÉP NHAU — hook/tiêu đề của tập này không được trùng lặp tập khác CÙNG lane.

NGUYÊN TẮC THIẾT KẾ (đọc trước khi sửa):
  * 0 LLM, tất định. Phần cần đọc ẢNH (chữ thumbnail có đúng như `thumb_text.txt` không) KHÔNG làm
    được ở đây — cổng chỉ ra WARN trỏ sang `qc_thumbnail_sol.py`. Đừng nhét vision vào file này.
  * Mọi NGƯỠNG đi qua `profile["goi_dang"]` (hàng rào chống lẫn lane #2 của CLAUDE.md) — CẤM thêm
    `if profile_id == ...` ở bất cứ đâu trong file này. Lane không khai `goi_dang.enabled` = cổng
    chạy ở chế độ WARN-only (không chặn) để bật dần từng lane, giống `script.hook.enabled`.
  * Thiếu artifact (chưa có title/thumb/mô tả) KHÔNG phải FAIL — là SKIP kèm ghi chú, vì cổng này
    chạy được ở nhiều mốc khác nhau của pipeline (sau B3, sau B7, sau B9).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_common  # noqa: E402
import profiles  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

GATE = "B7G"          # tên cổng trong logs/<gate>_attempt_NNN.json

# ──────────────────────────────────────────────────────────── ngưỡng mặc định
# Đây là MẶC ĐỊNH CHUNG rút từ mục A của NGUYEN_TAC_HOOK_GOI_DANG.md (số đếm trên 93 video của 9
# kênh mẫu). Lane nào đã đo riêng thì đè trong `profile["goi_dang"]` — vd toshi hạ
# `contradiction_max_s` vì kênh mẫu 今夜も都市伝説 mở bằng tít trước rồi mới tới bất thường.
MAC_DINH = {
    "enabled": False,                 # False = chạy WARN-only, không chặn (bật dần từng lane)
    "promise_window_s": 45,           # G1/nguyên tắc 4: lời hứa phải nói trong 30–45s
    "contradiction_max_s": 25,        # G3/nguyên tắc 2: câu mâu thuẫn ≤15–25s
    "title_core_max_s": 45,           # G3/nguyên tắc 4
    "promise_giu_duoc_max_s": 90,     # G2: vế lõi tiêu đề phải xuất hiện trước giây 90
    "ritual": [],                     # G3/nguyên tắc 5: câu nghi thức của kênh (rỗng = không kiểm)
    "ritual_max_s": 150,
    "title_core_len": [0, 100],       # G5: độ dài lõi tiêu đề (bỏ đuôi cố định)
    "title_suffix_ignore": [],        # đuôi cố định của lane, không tính là "vế" (vd 実際の写真をAIフルカラー復元)
    "title_an_so": ["本当の理由", "真相", "正体", "秘密", "真実", "答え", "なぜ", "とは", "どっち",
                    "違い", "差", "選", "つの", "理由", "の心理", "？", "?"],
    # Có lane KHÔNG treo ẩn số bằng TỪ HỎI mà bằng một con số/nghịch lý cụ thể — 色でたどる戦争の記録
    # là ví dụ: 9/9 tiêu đề kênh mẫu có số trong phần lõi và 0/9 có 真相/なぜ/とは. Bật cờ này cho
    # lane đó, nếu không cổng báo sai 11/11 tập (đã đo thật khi chạy lần đầu 2026-09-23).
    "title_an_so_chap_nhan_so": False,
    "title_chu_so": ["衝撃", "暴露", "残酷", "地獄", "悲劇", "末路", "貧乏", "破綻"],
    "title_rao": ["かもしれない", "可能性", "知っておきたい", "ことがある", "検討"],
    "mo_dau_cam": ["タイトル"],       # thêm vào banned_openers của hook_stage
    "contradiction_marker": ["だが", "しかし", "ところが", "ではない", "ではありません", "のに",
                             "なのに", "はずだった", "と思っていた", "けれど"],
    "list_mode": False,               # G4: video danh sách
    "list_preview_ban_s": 120,
    "list_marker": r"第\s*([0-9０-９一二三四五六七八九十]+)\s*位|([0-9０-９一二三四五六七八九十]+)\s*つ目",
    "list_order": "countdown",        # countdown = mục 1 ở CUỐI; ascending = mục 1 ở ĐẦU
    "cau_tu_thao": ["この順位は", "順位は重要度", "順番は重要", "証明されたわけでは"],
    "thumb_item_rank": 0,             # >0 = thumbnail hiện mục thứ mấy (phải là mục GIỮA)
    "chep_nhau_max": 0.55,            # G8: tỉ lệ bigram trùng tối đa với tập khác cùng lane
    "chep_nhau_cua_so": 700,          # so trên bao nhiêu ký tự đầu
    # G2 — ngưỡng "diễn đạt khác chứ không phải hứa suông". Chữ trên thumbnail và vế tiêu đề gần
    # như KHÔNG BAO GIỜ trùng nguyên văn lời đọc (tiêu đề phải gọn, thumbnail còn gọn hơn): quét
    # thật 56 tập của 6 lane bằng phép so NGUYÊN VĂN cho ra ~5 lỗi/tập ở gần như mọi tập — con số
    # đó không phân biệt được tập hỏng với tập lành, tức là cổng vô dụng. Nên chia 2 bậc:
    #   phủ ≥ ve_phu_canh  → chỉ CẢNH BÁO (cùng ý, khác chữ — người đọc tự quyết)
    #   phủ <  ve_phu_canh → CHẶN (không có chỗ nào trong script nói ý đó)
    "ve_phu_canh": 0.62,
    # G1 — độ phủ tối thiểu của lời hứa trong cửa sổ mở đầu (xem g1_mot_loi_hua).
    "promise_phu_min": 0.6,
}


def cau_hinh(prof):
    c = dict(MAC_DINH)
    c.update(prof.get("goi_dang") or {})
    return c


def is_enabled(prof):
    """NGÃ RẼ DUY NHẤT giữa lane đã bật / chưa bật cổng này. Mọi nơi gọi phải đi qua hàm này."""
    return bool(cau_hinh(prof).get("enabled"))


# ──────────────────────────────────────────────────────────── chuẩn hoá chuỗi
_KANJI_NUM = re.compile(r"[〇零一二三四五六七八九十百千万]{1,12}")
_BO = re.compile(r"[\s、。「」『』・…ー－―—～〜,.!?！？\"'（）()\[\]【】｜|:：;；/\\　]+")


def _zen2han(t):
    """Chữ số/ký tự toàn rộng → nửa rộng (７→7, Ａ→A). NFKC đủ và không phá chữ Nhật."""
    return unicodedata.normalize("NFKC", t or "")


def _kanji_ra_so(t):
    """Mọi cụm chữ Hán chỉ số → chữ số Ả Rập, để 76秒 và 七十六秒 quy về CÙNG một chuỗi.

    Cố ý ĐỔI CẢ những cụm không phải con số (一番 → 1番, 一緒 → 1緒): phép so sánh chỉ cần hai vế
    được chuẩn hoá GIỐNG NHAU, không cần đúng ngữ nghĩa. Đổi nửa vời (chỉ đổi khi có đơn vị đằng
    sau) mới là chỗ sinh lỗi — 「五つの話」 ở tiêu đề vs 「5つの話」 ở script sẽ không khớp.
    """
    from lean_script import kanji_to_int

    def thay(m):
        v = kanji_to_int(m.group(0))
        return str(int(v)) if isinstance(v, (int, float)) and v == int(v) else m.group(0)
    return _KANJI_NUM.sub(thay, t or "")


def norm(t):
    """Dạng chuẩn để grep: NFKC → chữ Hán số ra Ả Rập → bỏ mọi dấu câu/khoảng trắng."""
    return _BO.sub("", _kanji_ra_so(_zen2han(t or "")))


# ──────────────────────────────────────────────────────────── đọc artifact của tập
def _doc(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def doc_promise(d):
    """G1: `promise.txt` ở GỐC thư mục tập (đúng phiếu việc mục 2). Bản cũ nằm trong `hook/` —
    vẫn đọc được để không làm gãy tập đã có, nhưng chỗ CHUẨN là gốc thư mục."""
    for p in (Path(d) / "promise.txt", Path(d) / "hook" / "promise.txt"):
        t = _doc(p).strip()
        if t:
            return t, p
    return "", None


def doc_tieu_de(d):
    """title.txt → listting.txt → dòng 1 của TIEU_DE_MO_TA.txt (thứ tự này khớp hook_stage._title)."""
    for ten in ("title.txt", "listting.txt", "TIEU_DE_MO_TA.txt"):
        for l in _doc(Path(d) / ten).splitlines():
            if l.strip():
                return l.strip(), ten
    return "", ""


def doc_mo_ta_dong_dau(d):
    """Câu đầu MÔ TẢ = dòng không rỗng thứ 2 của TIEU_DE_MO_TA.txt (dòng 1 là tiêu đề)."""
    dong = [l.strip() for l in _doc(Path(d) / "TIEU_DE_MO_TA.txt").splitlines() if l.strip()]
    return dong[1] if len(dong) > 1 else ""


def doc_thumb_text(d):
    """thumb_text.txt dạng `MÀU|chữ` (hoặc chữ trần). Trả list dòng chữ, bỏ nhãn màu."""
    ra = []
    for l in _doc(Path(d) / "thumb_text.txt").splitlines():
        l = l.strip()
        if not l:
            continue
        ra.append(l.split("|", 1)[1].strip() if "|" in l else l)
    return ra


def doc_loi_doc(d):
    """LỜI ĐỌC đầy đủ = hook đã khoá (nếu có, và script chưa bắt đầu bằng nó) + script.txt.

    Vì sao phải ghép: chế độ `repair` của hook_stage giữ hook ở file RIÊNG (`hook/hook_locked.txt`)
    và không viết lại script.txt — đo mốc giây chỉ trên script.txt sẽ lệch đúng 20–30 giây đầu,
    tức lệch đúng phần cổng này đang soi.
    """
    sc = _doc(Path(d) / "script.txt")
    hk = _doc(Path(d) / "hook" / "hook_locked.txt").strip()
    if hk and not norm(sc).startswith(norm(hk)):
        return (hk + "\n\n" + sc), hk
    return sc, hk


# ──────────────────────────────────────────────────────────── mốc giây
class Moc:
    """Đổi VỊ TRÍ KÝ TỰ trong lời đọc → GIÂY.

    Ưu tiên `voice.srt` (mốc thật). Chưa thu giọng thì suy ra từ `char_rate` của profile — đây là
    chỗ hàng rào #1 của CLAUDE.md có tác dụng: kênh chưa đo char_rate thì `profiles.char_rate` tự
    nói lên điều đó, không được mượn số của kênh khác.
    """

    def __init__(self, d, prof, loi_doc):
        self.rate = profiles.char_rate(prof)          # ký tự / phút
        self.cues = self._doc_srt(Path(d) / "voice.srt")
        self.text_norm = norm(loi_doc)

    @staticmethod
    def _doc_srt(p):
        if not p.exists():
            return []
        ra = []
        for kh in re.split(r"\n\s*\n", p.read_text(encoding="utf-8")):
            m = re.search(r"(\d\d):(\d\d):(\d\d)[,.](\d\d\d)\s*-->", kh)
            if not m:
                continue
            s = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000
            chu = norm(" ".join(kh.splitlines()[2:]))
            ra.append((s, chu))
        return ra

    def giay(self, vi_tri_norm):
        """vi_tri_norm = chỉ số ký tự trong chuỗi ĐÃ chuẩn hoá của cả lời đọc."""
        if self.cues:
            đa = 0
            for s, chu in self.cues:
                if đa + len(chu) > vi_tri_norm:
                    return s
                đa += len(chu)
            return self.cues[-1][0]
        return vi_tri_norm / (self.rate / 60.0) if self.rate else 0.0

    def nguon(self):
        return f"voice.srt ({len(self.cues)} cue)" if self.cues else f"char_rate {self.rate:.0f} chữ/phút"

    def tim(self, cum):
        """Trả (giây, vị_trí) lần xuất hiện ĐẦU TIÊN của `cum` trong lời đọc, hoặc (None, -1)."""
        n = norm(cum)
        if not n:
            return None, -1
        i = self.text_norm.find(n)
        return (self.giay(i), i) if i >= 0 else (None, -1)

    def cua_so(self, giay):
        """Chuỗi chuẩn hoá của `giay` giây ĐẦU — dùng để hỏi 'trong 120s đầu có X không'."""
        if self.cues:
            đa, ra = 0, []
            for s, chu in self.cues:
                if s >= giay:
                    break
                ra.append(chu)
                đa += len(chu)
            return "".join(ra)
        return self.text_norm[:int(giay * self.rate / 60.0)] if self.rate else ""


# ──────────────────────────────────────────────────────────── tách vế tiêu đề
# Dấu ngắt vế. `\.{2,}` là BẮT BUỘC: tiêu đề thật của toshi/tano dùng ba chấm ASCII "..." chứ
# không phải 「…」 (vd 「テスラの死から61年後...米海軍が撮った76秒の映像」) — thiếu nó thì cả tiêu đề
# thành MỘT vế dài, phép so bigram bị loãng và báo "không có trong script" cho vế thật ra có.
_NGAT_VE = re.compile(r"[｜|…‥]+|——|\.{2,}|--|~~|、|。|！|？|\?|!")


def tach_ve_tieu_de(title, bo_qua=()):
    """Tách tiêu đề thành các VẾ để grep riêng từng vế.

    Ngắt ở dấu MẠNH (｜ … —— 、 ？) và tách riêng nội dung trong 【】. Bỏ các vế nằm trong
    `bo_qua` (đuôi cố định của lane: 実際の写真をAIフルカラー復元 · 【都市伝説 ミステリー 怖い話】…)
    và bỏ vế quá ngắn (<4 ký tự chuẩn hoá) — 2–3 ký tự thì grep gần như luôn trúng, kiểm vô nghĩa.
    """
    t = _zen2han(title or "")
    for x in bo_qua:
        t = t.replace(_zen2han(x), "｜")
    phan = []
    for khoi in re.split(r"【(.*?)】", t):
        phan += [x for x in _NGAT_VE.split(khoi) if x and x.strip()]
    ra, thay = [], set()
    for v in phan:
        # 「N選」 là QUY ƯỚC ĐẶT TÊN của lane list (7/10 tiêu đề kênh mẫu tano), không phải một câu
        # phải có trong lời đọc — script viết 「五つ」/「1つ目」 chứ không ai đọc to chữ 「5選」. Số N có
        # được giữ hay không đã do G4 đếm mục thật kiểm rồi; để nguyên ở đây là phạt hai lần.
        v = _N_CHON.sub("", v).strip()
        n = norm(v)
        if len(n) < 4 or n in thay:
            continue
        thay.add(n)
        ra.append(v)
    return ra


_N_CHON = re.compile(r"[0-9０-９〇一二三四五六七八九十]+\s*選")


_PHU_DINH = ("ではない", "ではありません", "ではなかった", "わけではない", "ものではない",
             "とは限らない", "していない", "ありません", "できません", "誤り", "嘘", "事実ではない")


def bi_phu_dinh(loi_doc_norm, cum_norm, cua_so=45):
    """True khi MỌI lần xuất hiện của `cum` đều nằm sát một dấu phủ định.

    Vì sao 'MỌI lần' chứ không phải 'có một lần': tập nào cũng có thể nhắc lại một ý rồi bác bỏ nó
    ở chỗ khác; chỉ khi KHÔNG CÒN chỗ nào khẳng định thì lời hứa của tiêu đề mới thật sự không giữ.
    """
    if not cum_norm:
        return False
    pd = [norm(x) for x in _PHU_DINH]
    thay, tat_ca_bi = False, True
    i = loi_doc_norm.find(cum_norm)
    while i >= 0:
        thay = True
        sau = loi_doc_norm[i + len(cum_norm): i + len(cum_norm) + cua_so]
        if not any(p in sau for p in pd):
            tat_ca_bi = False
            break
        i = loi_doc_norm.find(cum_norm, i + 1)
    return thay and tat_ca_bi


# ──────────────────────────────────────────────────────────── G1 … G8
def g1_mot_loi_hua(d, c, moc, title, thumb, mo_ta):
    chan, canh = [], []
    promise, p = doc_promise(d)
    if not promise:
        chan.append("G1: THIẾU promise.txt (1 câu lời hứa của tập) ở gốc thư mục tập")
        return chan, canh, ""
    if len([x for x in promise.splitlines() if x.strip()]) > 1:
        canh.append(f"G1: promise.txt có nhiều dòng ({p}) — lời hứa phải gói trong ĐÚNG 1 câu")
    pn = norm(promise)
    # Lời hứa hiếm khi được chép NGUYÊN VĂN sang tiêu đề/thumbnail (tiêu đề còn phải gọn). Luật của
    # nguyên tắc 1 là "chứa được câu đó HOẶC MỘT NỬA của nó" → đo bằng tỉ lệ bigram phủ.
    for ten, val in (("tiêu đề", title), ("chữ thumbnail", " ".join(thumb)), ("câu đầu mô tả", mo_ta)):
        if not val:
            canh.append(f"G1: chưa có {ten} — chưa kiểm được lời hứa ở chỗ này")
            continue
        if _phu(pn, norm(val)) < 0.4:
            chan.append(f"G1: {ten} KHÔNG nói lại lời hứa 「{promise[:40]}」 (phủ <40%)")
    # Lời hứa gần như KHÔNG BAO GIỜ nằm nguyên văn trong lời đọc (nó là câu tóm tắt của người làm,
    # không phải một câu thoại) — nên đo bằng ĐỘ PHỦ trong cửa sổ `promise_window_s` giây đầu, và
    # nếu chưa đủ thì nói rõ tới giây bao nhiêu mới đủ, để người sửa biết phải kéo câu nào lên.
    nguong = c["promise_phu_min"]
    if _phu(pn, norm(moc.cua_so(c["promise_window_s"]))) < nguong:
        du = next((s for s in range(int(c["promise_window_s"]) + 15, 601, 15)
                   if _phu(pn, norm(moc.cua_so(s))) >= nguong), None)
        chan.append(f"G1: trong {c['promise_window_s']:.0f}s đầu, lời đọc mới nói được "
                    f"{_phu(pn, norm(moc.cua_so(c['promise_window_s']))):.0%} lời hứa (cần ≥{nguong:.0%})"
                    + (f" — phải tới giây ~{du} mới đủ; kéo câu đó lên hook" if du
                       else " — cả bài không nói đủ lời hứa, sửa lời hứa hoặc sửa script")
                    + f" (đo bằng {moc.nguon()})")
    return chan, canh, promise


def _bigrams(t):
    return {t[i:i + 2] for i in range(len(t) - 1)}


def _phu(a, b):
    """Tỉ lệ bigram của `a` có mặt trong `b` (0..1)."""
    ba = _bigrams(a)
    return len(ba & _bigrams(b)) / len(ba) if ba else 0.0


def doc_mien(d):
    """`goi_dang_ok.txt` — các vế NGƯỜI ĐÃ ĐỌC TAY và xác nhận script có giữ, kèm lý do.

    Khuôn mỗi dòng: `<vế> | <lý do, phải nêu bằng chứng>`; dòng bắt đầu bằng # là chú thích.
    Đây KHÔNG phải cửa sau để tắt cổng: nó chỉ hạ một vế CỤ THỂ từ CHẶN xuống CẢNH BÁO, vẫn in ra
    mỗi lần chạy kèm lý do, và không đụng tới G1/G3/G4/G5/G6/G8. Có nó vì phép so bigram không phân
    biệt được 'script diễn đạt khác' với 'script không hề nói' khi vế ghép 2–3 mảnh nằm xa nhau
    (đo thật: tano ep02 「月1000円以下の過ごし方」 55% — script có 「予算枠は月に1000円まで」 ở giây 264
    và 「金のかからない過ごし方が、五つある」 ở 254, tức lời hứa CÓ giữ).
    """
    ra = {}
    for l in _doc(Path(d) / "goi_dang_ok.txt").splitlines():
        l = l.strip()
        if not l or l.startswith("#"):
            continue
        ve, _, ly_do = l.partition("|")
        ra[norm(ve)] = ly_do.strip() or "(không ghi lý do)"
    return ra


def g2_loi_hua_giu_duoc(d, c, moc, title, thumb):
    chan, canh = [], []
    mien = doc_mien(d)
    ve = tach_ve_tieu_de(title, c["title_suffix_ignore"])
    if not ve and title:
        canh.append("G2: không tách được vế nào từ tiêu đề (tiêu đề quá ngắn?)")
    muc = [("tiêu đề", v) for v in ve] + [("thumbnail", t) for t in thumb]
    lõi = max(ve, key=lambda v: len(norm(v))) if ve else ""
    for loai, v in muc:
        n = norm(v)
        giay, i = moc.tim(v)
        if i < 0:
            phu = _phu(n, moc.text_norm)
            if n in mien:
                canh.append(f"G2: vế {loai} 「{v}」 ({phu:.0%} trùng) — ĐÃ ĐỌC TAY, chấp nhận: "
                            f"{mien[n]}")
            elif phu >= c["ve_phu_canh"]:
                canh.append(f"G2: vế {loai} 「{v}」 không có NGUYÊN VĂN trong lời đọc nhưng script "
                            f"nói cùng ý ({phu:.0%} trùng) — đọc tay xem có đúng ý không")
            else:
                chan.append(f"G2: vế {loai} 「{v}」 KHÔNG có trong lời đọc (chỉ {phu:.0%} trùng, đã so "
                            f"cả chữ số ↔ chữ Hán) — sửa {loai} hoặc viết thêm câu đó vào script")
            continue
        if bi_phu_dinh(moc.text_norm, n):
            chan.append(f"G2: vế {loai} 「{v}」 bị chính script PHỦ ĐỊNH ở MỌI chỗ nó xuất hiện "
                        f"— hứa điều script không giữ")
        if v == lõi and giay is not None and giay > c["promise_giu_duoc_max_s"]:
            chan.append(f"G2: vế LÕI của tiêu đề 「{v}」 mãi giây {giay:.0f} mới xuất hiện "
                        f"(> {c['promise_giu_duoc_max_s']}s) — đưa một câu hé vào hook")
    return chan, canh


def g3_thu_tu(d, c, moc, prof, title, loi_doc):
    chan, canh = [], []
    import hook_stage
    cam = list(hook_stage.cau_hinh(prof).get("banned_openers") or []) + list(c["mo_dau_cam"])
    dau = loi_doc.strip()[:80]
    for w in cam:
        if w.lower() in dau.lower():
            chan.append(f"G3: 80 ký tự đầu lời đọc có 「{w}」 — cấm chào/cảm ơn/tự giới thiệu/"
                        f"đọc to chữ tiêu đề ở câu mở (nguyên tắc 3)")
    # câu mâu thuẫn: câu ĐẦU TIÊN chứa một dấu hiệu đảo ý
    gm = None
    for mk in c["contradiction_marker"]:
        g, i = moc.tim(mk)
        if i >= 0 and (gm is None or g < gm):
            gm = g
    if gm is None:
        chan.append(f"G3: không tìm thấy câu mâu thuẫn nào (dấu hiệu: "
                    f"{'・'.join(c['contradiction_marker'][:4])}…) — hook đang kể suông")
    elif gm > c["contradiction_max_s"]:
        chan.append(f"G3: câu mâu thuẫn đầu tiên ở giây {gm:.0f} > {c['contradiction_max_s']}s "
                    f"(nguyên tắc 2)")
    # lõi tiêu đề ≤ title_core_max_s
    ve = tach_ve_tieu_de(title, c["title_suffix_ignore"])
    if ve:
        lõi = max(ve, key=lambda v: len(norm(v)))
        g, i = moc.tim(lõi)
        if i >= 0 and g > c["title_core_max_s"]:
            chan.append(f"G3: lõi tiêu đề 「{lõi}」 mãi giây {g:.0f} mới nói "
                        f"(> {c['title_core_max_s']}s — nguyên tắc 4)")
    # câu nghi thức của kênh
    for r in c["ritual"]:
        g, i = moc.tim(r)
        if i < 0:
            chan.append(f"G3: THIẾU câu nghi thức của kênh 「{r}」 (nguyên tắc 5)")
        elif g > c["ritual_max_s"]:
            canh.append(f"G3: câu nghi thức 「{r}」 ở giây {g:.0f} > {c['ritual_max_s']}s")
    return chan, canh


def dem_muc(c, text):
    """Trả list số thứ tự các mục theo thứ tự XUẤT HIỆN trong text."""
    from lean_script import kanji_to_int
    ra = []
    for m in re.finditer(c["list_marker"], _zen2han(text)):
        s = next((g for g in m.groups() if g), None)
        if not s:
            continue
        v = int(s) if s.isdigit() else kanji_to_int(s)
        if v is not None:
            ra.append(int(v))
    return ra


def g4_danh_sach(d, c, moc, prof, loi_doc, thumb):
    chan, canh = [], []
    if not c["list_mode"]:
        return chan, canh
    muc = dem_muc(c, loi_doc)
    can = ((prof.get("script", {}).get("gate") or {}).get("list_item_count")) or 0
    if can and len(set(muc)) != can:
        chan.append(f"G4: đếm được {len(set(muc))} mục ({sorted(set(muc))}) ≠ "
                    f"gate.list_item_count = {can}")
    dau = moc.cua_so(c["list_preview_ban_s"])
    n_dau = len(dem_muc(c, dau))
    if n_dau:
        chan.append(f"G4: {c['list_preview_ban_s']}s đầu đã nêu {n_dau} mục — cấm đọc trước "
                    f"danh sách (nguyên tắc 7)")
    if muc:
        if c["list_order"] == "countdown" and muc[-1] != 1:
            chan.append(f"G4: đếm ngược nhưng mục CUỐI là 第{muc[-1]}位, không phải 第1位 "
                        f"— mục 1 phải để cuối")
        if c["list_order"] == "ascending" and muc[0] != 1:
            chan.append(f"G4: đếm xuôi nhưng mục ĐẦU là {muc[0]}, không phải 1")
    for p in c["cau_tu_thao"]:
        if norm(p) in moc.text_norm:
            chan.append(f"G4: có câu tự tháo đếm ngược 「{p}」 — bỏ đi, nó xoá lý do xem tới cuối")
    # Thứ hạng mục nằm trên thumbnail đổi theo TỪNG TẬP, nên chỗ khai đúng là file trong thư mục
    # tập (`thumb_rank.txt`, 1 con số); giá trị trong profile chỉ là dự phòng khi cả lane dùng
    # chung một quy ước.
    rf = _doc(Path(d) / "thumb_rank.txt").strip()
    r = int(rf) if rf.isdigit() else int(c["thumb_item_rank"] or 0)
    if r:
        if r == 1 or (can and r == can):
            chan.append(f"G4: thumbnail đang hiện mục {r} — phải là mục GIỮA danh sách, "
                        f"giấu mục 1 (nguyên tắc 7)")
    elif thumb:
        canh.append("G4: chưa khai `goi_dang.thumb_item_rank` — không kiểm được thumbnail có "
                    "đang lộ mục 1 hay không")
    return chan, canh


def g5_tieu_de(c, title):
    chan, canh = [], []
    if not title:
        return chan, ["G5: chưa có tiêu đề"]
    t = _zen2han(title)
    lõi = t
    for x in c["title_suffix_ignore"]:
        lõi = lõi.replace(_zen2han(x), "")
    lõi = lõi.strip(" ｜|　")
    lo, hi = c["title_core_len"]
    if not (lo <= len(lõi) <= hi):
        chan.append(f"G5: lõi tiêu đề {len(lõi)} ký tự, ngoài dải {lo}–{hi} đã đo của kênh mẫu")
    co_so = bool(re.search(r"\d", _kanji_ra_so(lõi)))
    if not any(x in t for x in c["title_an_so"]) and not (c["title_an_so_chap_nhan_so"] and co_so):
        chan.append(f"G5: tiêu đề KHÔNG treo ẩn số nào (thiếu cả "
                    f"{'/'.join(c['title_an_so'][:5])}…) — đang kể luôn kết cục")
    for w in c["title_rao"]:
        if w in t:
            chan.append(f"G5: tiêu đề có chữ RÀO 「{w}」 — kênh mẫu 0/9 dùng")
    for w in c["title_chu_so"]:
        if w in t:
            (chan if not co_so else canh).append(
                f"G5: tiêu đề có chữ sợ 「{w}」" + ("" if co_so else " mà KHÔNG có con số/việc cụ thể "
                                                   "nào đi kèm — chữ sợ đứng một mình"))
    return chan, canh


_ANH_THUMB = ("thumbnail_final.png", "thumb_final.png", "thumbnail.png", "thumb.png",
              "thumbnail_final.jpg", "thumb_final.jpg")


def g6_thumbnail(d, c, thumb):
    chan, canh = [], []
    d = Path(d)
    co = [p for p in d.iterdir() if p.is_file() and p.name in _ANH_THUMB]
    dt = _doc(d / "DANG-TAI.txt")
    if not co:
        return chan, ["G6: chưa có file thumbnail nào"]
    tro = [p for p in co if p.name in dt] if dt else []
    if len(co) > 1:
        if not dt:
            chan.append(f"G6: có {len(co)} file thumbnail ({', '.join(p.name for p in co)}) mà "
                        f"KHÔNG có DANG-TAI.txt để chốt file nào được đăng")
        elif len(tro) != 1:
            chan.append(f"G6: có {len(co)} file thumbnail, DANG-TAI.txt trỏ tới {len(tro)} file "
                        f"— phải chốt đúng 1")
        else:
            canh.append(f"G6: {len(co)} file thumbnail, đang đăng {tro[0].name}; xoá/đổi tên các "
                        f"file còn lại để lần sau không chọn nhầm")
    anh = tro[0] if len(tro) == 1 else co[0]
    if not thumb:
        canh.append("G6: chưa có thumb_text.txt — không đối chiếu được chữ trên ảnh")
    elif (d / "thumb_text.txt").stat().st_mtime < anh.stat().st_mtime - 2:
        canh.append(f"G6: {anh.name} MỚI HƠN thumb_text.txt — chữ trong file có thể không còn "
                    f"giống chữ trên ảnh; đọc lại chữ TỪ ẢNH (qc_thumbnail_sol.py)")
    return chan, canh


def g8_khong_chep_nhau(d, c, prof, loi_doc, title):
    chan, canh = [], []
    d = Path(d)
    me = norm(loi_doc)[:c["chep_nhau_cua_so"]]
    for anh_em in sorted(d.parent.iterdir()):
        if not anh_em.is_dir() or anh_em.resolve() == d.resolve() or anh_em.name.startswith("_"):
            continue
        khac, _ = doc_loi_doc(anh_em)
        if not khac:
            continue
        r = _phu(me, norm(khac)[:c["chep_nhau_cua_so"]])
        if r > c["chep_nhau_max"]:
            chan.append(f"G8: {c['chep_nhau_cua_so']} ký tự đầu trùng {r:.0%} với {anh_em.name} "
                        f"(> {c['chep_nhau_max']:.0%}) — chép CƠ CHẾ, đừng chép CÂU (nguyên tắc 6)")
        t2, _ = doc_tieu_de(anh_em)
        if title and t2 and _phu(norm(title), norm(t2)) > 0.8:
            canh.append(f"G8: tiêu đề gần trùng {anh_em.name} 「{t2}」")
    return chan, canh


# ───────────────────────────────── CỔNG THƯỢNG NGUỒN: chặn TRƯỚC KHI VIẾT (anh chốt 2026-09-24)
# Vì sao có hàm này thay vì thêm một dòng vào tài liệu: luật hook + gói đăng đã được chốt 2026-09-23
# và viết vào CLAUDE.md, nhưng đo thật ngày 24/09 thì `script.hook.enabled` mới BẬT ở 3/6 lane
# (satori · kenko · toshi) — 3 lane còn lại (iro · real · tano) vẫn TẮT, tức luật "hook bắt buộc mọi
# tập" chỉ chạy khi có người nhớ ra mà bật. Luật nằm trong VĂN BẢN thì phải có người đọc; luật nằm
# trong CỔNG thì không ai đi qua được mà không làm. Đây là cùng bài học đã ghi ở memory
# `khong-giao-viec-thu-cong-rao-nam-trong-tool`.
#
# Gọi ở `lean_script.run()` NGAY SAU S1Q, trước H1–H4 và trước S2 — nghĩa là trượt cổng này thì
# CHƯA TỐN LƯỢT LLM NÀO.
# Hook có HAI chiều thông tin, cố ý tách làm 2 field — trộn vào 1 field là chỗ sinh lỗi (đã dính thật
# 2026-09-24: đổi `visual` cho gọn thì (a) chết nhánh `visual == "lien_mach_than"` trong
# dong_goi_may2.py, (b) mất thông tin REF-LOCK mà tên `anh_ai_ref_grok`/`manga_ai_ref` đang mang, mà
# SOP từng lane + memory đang trỏ vào):
#   · `script.hook.visual`      = NGUỒN HÌNH + cách khoá mặt (riêng từng lane, có code đọc)
#   · `script.hook.visual_kind` = hook là VIDEO SINH hay ẢNH TĨNH (luật của anh, cổng này kiểm)
VISUAL_KIND_VIDEO = "video_sinh"


def cong_truoc_khi_viet(d, prof):
    """Trả list lỗi BLOCK (rỗng = được viết). 0 LLM, 0 mạng.

    Năm điều kiện, đều là điều kiện THƯỢNG NGUỒN (phải có TRƯỚC khi viết, không phải sửa sau):
      1. `script.hook.enabled` — hook 20–30s là luật MỌI LANE.
      2. `goi_dang.enabled` — lane phải khai ngưỡng gói đăng ĐO TỪ KÊNH MẪU CỦA CHÍNH NÓ.
      3. `promise.txt` — MỘT lời hứa, 1 câu. Đây là thứ model VIẾT cần để viết đúng ngay lần đầu
         (xem `khoi_luat_cho_prompt`); thiếu nó thì chỉ còn cách chấm-rồi-sửa, tốn lượt Sol.
      4. `script.hook.visual_kind == "video_sinh"` (Flow/Grok) — hoặc khai `visual_exception` ghi lý do.
      5. `script.hook.sfx` — hiệu ứng âm thanh BẮT BUỘC.
    Điều 4–5 anh chốt 2026-09-24: hook ghép từ ảnh tĩnh nhìn ra ngay là video AI rẻ ở đúng 20 giây
    quyết định người xem ở lại hay thoát; lane satori đã chạy thật clip Grok nên không còn là giả
    thiết. Ngoại lệ chính danh hiện có: `toshi-densetsu-jp` và `irogatatarukioku` bán SỰ THẬT CÓ HỒ SƠ
    — đưa clip AI vào hook là tự phá thứ kênh đang bán, chưa kể phá quy ước credits.txt.
    """
    import hook_stage
    loi = []
    h = (prof.get("script", {}) or {}).get("hook") or {}
    if not hook_stage.is_enabled(prof):
        loi.append("profile chưa khai `script.hook.enabled: true` — hook 20–30s đầu là luật MỌI LANE "
                   "(chốt 2026-09-23). Đọc docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §2b")
    if not is_enabled(prof):
        loi.append("profile chưa khai `goi_dang.enabled: true` — ngưỡng gói đăng phải ĐO TỪ KÊNH MẪU "
                   "của chính lane này rồi khai vào `profile.goi_dang` kèm `_nguon`. "
                   "Đọc docs/QUY_TAC_GOI_DANG.md §3")
    kind = str(h.get("visual_kind") or "")
    if kind != VISUAL_KIND_VIDEO and not str(h.get("visual_exception") or "").strip():
        loi.append(f"`script.hook.visual_kind` = {kind!r} — mặc định MỌI LANE hook phải là "
                   f"{VISUAL_KIND_VIDEO!r} (video sinh từ Google Flow hoặc Grok Imagine, như "
                   f"satori-jp-obaa đã chạy thật ở ep3-sougi), KHÔNG còn là video ghép từ ảnh render. "
                   f"Muốn dùng ảnh tĩnh/clip stock thì khai `script.hook.visual_exception` ghi RÕ LÝ "
                   f"DO. Đọc docs/QUY_TAC_VIDEO_HOOK.md §5b")
    if not h.get("sfx", False):
        loi.append("profile chưa khai `script.hook.sfx: true` — hiệu ứng âm thanh trong hook là BẮT "
                   "BUỘC (anh chốt 2026-09-24). Sinh bằng ai33 `POST /v1/task/sound-effect`, để "
                   "`duration_seconds` AUTO (memory sfx-ai33-mac-dinh-auto)")
    promise, _ = doc_promise(d)
    if not promise:
        loi.append(f"thiếu {Path(d) / 'promise.txt'} — chốt MỘT lời hứa (1 câu) TRƯỚC khi viết; tiêu đề, "
                   f"chữ thumbnail, câu đầu mô tả và 30–45s đầu hook đều phải nói lại đúng câu đó "
                   f"(nguyên tắc 1). Đọc docs/QUY_TAC_GOI_DANG.md §1")
    elif len([x for x in promise.splitlines() if x.strip()]) > 1:
        loi.append(f"{Path(d) / 'promise.txt'} có nhiều dòng — lời hứa phải gói trong ĐÚNG 1 câu, "
                   f"vì nó sẽ được nhồi vào prompt viết và vào 4 chỗ của gói đăng")
    return loi


def khoi_luat_cho_prompt(d, prof):
    """Khối chữ chèn vào PROMPT của model VIẾT. Rỗng nếu lane chưa bật (không đổi hành vi cũ).

    Đây là nửa còn lại của rào: cổng ở trên chỉ CHẶN, khối này mới làm model viết ĐÚNG NGAY LẦN ĐẦU.
    Trước đây `qc_goi_dang.py` chỉ chấm SAU khi viết xong — mà chấm sau nghĩa là phải sửa, tức thêm
    lượt Sol + lượt patch cho mỗi tập. Luật rẻ nhất là luật model đọc trước khi đặt bút.
    """
    if not is_enabled(prof):
        return ""
    c = dict(cau_hinh(prof))
    # `sfx` sống ở `script.hook` (cùng chỗ với enabled/visual), không phải trong `goi_dang` — đọc từ
    # đúng nguồn rồi mới đưa vào c, để chỗ khai và chỗ dùng không lệch nhau.
    _h = (prof.get("script", {}) or {}).get("hook") or {}
    c["hook_sfx"] = bool(_h.get("sfx", False))
    c["hook_kind"] = str(_h.get("visual_kind") or "")
    promise, _ = doc_promise(d)
    dong = [
        "LỜI HỨA CỦA TẬP NÀY (luật G1 — bắt buộc):",
        f"   「{promise}」" if promise else "   (chưa chốt)",
        "   Lời hứa này phải được nói lại trong "
        f"{c['promise_window_s']:.0f} GIÂY ĐẦU của bản đọc. Tiêu đề, chữ thumbnail và câu đầu mô tả "
        "cũng nói đúng lời hứa đó — nên đừng viết một câu chuyện đi chỗ khác.",
        "",
        "THỨ TỰ BẮT BUỘC CỦA MỞ ĐẦU (luật G3, đo từ kênh mẫu của chính kênh này):",
        f"   · Câu MÂU THUẪN/nghịch lý chính phải nằm trong {c['contradiction_max_s']:.0f} giây đầu.",
        f"   · Câu hỏi/lời hứa của TIÊU ĐỀ phải nói ra trong {c['title_core_max_s']:.0f} giây đầu.",
        "   · CẤM mở bằng chào hỏi, cảm ơn, tự giới thiệu tên-tuổi, tiểu sử, năm sinh, hay đọc to "
        "chữ 「タイトル」. Tên-tuổi đến SAU câu mâu thuẫn, đúng 1 câu.",
    ]
    if c["ritual"]:
        dong.append("   · Câu NGHI THỨC của kênh phải có mặt (trong "
                    f"{c['ritual_max_s']:.0f} giây đầu): " + " · ".join(f"「{r}」" for r in c["ritual"]))
    dong += [
    ]
    # anh chốt 2026-09-24: hook là VIDEO SINH → 20–30s đầu bị ràng buộc bởi thứ dựng được thành clip.
    # Phải nói cho model VIẾT biết TRƯỚC, vì nó là bên duy nhất quyết định đoạn mở có dựng nổi hay
    # không; phát hiện ở khâu dựng thì đã phải viết lại đoạn mở (tốn lượt patch). Lane có ngoại lệ
    # ảnh tĩnh (toshi/iro) KHÔNG được nhận khối này — dặn sai là model viết cảnh không có tư liệu thật.
    if c.get("hook_kind") == VISUAL_KIND_VIDEO:
        dong += [
            "",
            "20–30 GIÂY ĐẦU SẼ ĐƯỢC DỰNG THÀNH VIDEO SINH (Flow/Grok), không phải ảnh tĩnh:",
            "   · Mỗi 5–6 giây là MỘT cảnh dựng được: một chủ thể, một chuyển động tả được bằng lời "
            "(cúi xuống, mở phong bì, quay đầu lại). CẤM cảnh cần ≥3 nhân vật cùng hành động, cấm đổi "
            "bối cảnh giữa một cảnh, cấm chữ/biểu đồ trên hình.",
            "   · Viết sao cho mỗi câu mở neo vào MỘT hình cụ thể — câu bình luận trừu tượng không "
            "dựng được thành clip, để dành cho thân bài.",
        ]
    if c.get("hook_sfx", True):
        dong.append("   · Hook sẽ có HIỆU ỨNG ÂM THANH (bắt buộc) — viết chừa chỗ cho tiếng thật của "
                    "cảnh (tiếng cửa, tiếng mưa, tiếng bước chân), đừng lấp kín 30 giây bằng lời đọc.")
    dong += [
        "",
        "LỜI HỨA PHẢI GIỮ ĐƯỢC (luật G2):",
        "   Mọi vế của tiêu đề và mọi dòng chữ thumbnail sẽ được máy grep lại trong bản đọc này (so cả "
        "chữ số lẫn chữ Hán: 76秒 ↔ 七十六秒). Đừng để tiêu đề hứa một điều mà bản đọc không nói, và "
        "TUYỆT ĐỐI đừng viết câu PHỦ ĐỊNH chính điều tiêu đề đang hứa.",
    ]
    if c["list_mode"]:
        dong += [
            "",
            "VIDEO DANH SÁCH (luật G4):",
            f"   · CẤM đọc trước danh sách: {c['list_preview_ban_s']:.0f} giây đầu KHÔNG được nêu tên "
            "hay số thứ tự của bất kỳ mục nào. Chỉ được nhử bằng đặc điểm.",
            "   · CẤM các câu tự tháo đếm ngược kiểu 「この順位は重要度を示すものではありません」 — nó xoá "
            "lý do xem tới cuối.",
        ]
        # Chỉ dặn thứ tự khi lane CHỐT HẲN một kiểu. `list_order: "auto"` = kênh mẫu dùng CẢ HAI
        # (第N位 đếm ngược cho video xếp hạng, 1つ目 đếm xuôi cho video thói quen) — ở đó cổng G4 cố ý
        # BỎ QUA phép kiểm thứ tự, nên prompt cũng phải im: dặn một kiểu là dạy model sai một nửa số
        # tập, mà cổng lại không bắt được (đo thật khi nghiệm thu prompt lane tano 2026-09-24).
        if c["list_order"] == "countdown":
            dong.append("   · Đếm NGƯỢC: mục số 1 để CUỐI cùng.")
        elif c["list_order"] == "ascending":
            dong.append("   · Đếm XUÔI: mục số 1 mở đầu danh sách.")
    return "\n".join(dong)


# ──────────────────────────────────────────────────────────── chạy cả cổng
def kiem(slug_dir, profile_id):
    d = Path(slug_dir)
    prof = profiles.load(profile_id)
    c = cau_hinh(prof)
    loi_doc, _hook = doc_loi_doc(d)
    if not loi_doc.strip():
        return gate_common.ket_qua(GATE, "SKIPPED", warnings=[f"{d} chưa có script.txt"])
    title, nguon_tt = doc_tieu_de(d)
    thumb = doc_thumb_text(d)
    mo_ta = doc_mo_ta_dong_dau(d)
    moc = Moc(d, prof, loi_doc)

    chan, canh = [], []
    c1, w1, promise = g1_mot_loi_hua(d, c, moc, title, thumb, mo_ta)
    for fn in (lambda: (c1, w1),
               lambda: g2_loi_hua_giu_duoc(d, c, moc, title, thumb),
               lambda: g3_thu_tu(d, c, moc, prof, title, loi_doc),
               lambda: g4_danh_sach(d, c, moc, prof, loi_doc, thumb),
               lambda: g5_tieu_de(c, title),
               lambda: g6_thumbnail(d, c, thumb),
               lambda: g8_khong_chep_nhau(d, c, prof, loi_doc, title)):
        a, b = fn()
        chan += a
        canh += b

    metrics = {"mốc_giây_từ": moc.nguon(), "tiêu_đề_nguồn": nguon_tt, "số_vế_tiêu_đề":
               len(tach_ve_tieu_de(title, c["title_suffix_ignore"])), "số_dòng_thumbnail": len(thumb),
               "có_promise": bool(promise), "enabled": c["enabled"]}
    if not c["enabled"]:
        # Lane chưa bật: mọi phát hiện hạ xuống cảnh báo — thấy được mà không chặn dây chuyền.
        canh = [f"(sẽ CHẶN khi bật goi_dang.enabled) {x}" for x in chan] + canh
        chan = []
    status = "FAIL" if chan else ("WARN" if canh else "PASS")
    return gate_common.ket_qua(GATE, status, blocking=chan, warnings=canh, metrics=metrics)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cổng GÓI ĐĂNG G1–G6/G8 (0 LLM)")
    ap.add_argument("--slug", required=True, help="thư mục tập, vd assets/kenko-chiebukuro/ep03-...")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--json", action="store_true", help="in JSON thay vì bản đọc")
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args(argv)
    kq = kiem(a.slug, a.profile)
    if not a.no_log:
        gate_common.ghi_log(a.slug, GATE, kq)
    if a.json:
        print(json.dumps(kq, ensure_ascii=False, indent=1))
    else:
        for x in kq["blocking_issues"]:
            print("  ✗", x)
        for x in kq["warnings"]:
            print("  ⚠", x)
        print(f"=== GÓI ĐĂNG ({a.slug}): {kq['status']} — "
              f"{len(kq['blocking_issues'])} chặn, {len(kq['warnings'])} cảnh báo")
    return 1 if kq["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
