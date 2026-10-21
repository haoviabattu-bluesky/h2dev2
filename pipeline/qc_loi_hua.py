"""Kiểm NHẸ lời hứa tiêu đề — thay S5 Sol cho lane đã tắt `script.sol_qc` (anh chốt 2026-09-29).

Chỉ bắt 2 loại lỗi mà máy S3 không thấy và người xem thấy ngay (đo thật Lane M ep01/02/03: Sol bắt 3/3 tập):
  A. TỰ PHỦ ĐỊNH — bài nói ngược điều tiêu đề hứa (「人と話さなくていい」 mà kết bài 「一言も喋るなって意味じゃなかった」).
  B. KHÔNG TRẢ    — điều tiêu đề hứa rõ ràng không xuất hiện ở đâu trong bài.
KHÔNG chấm dòng thời gian / văn phong / chi tiết nhỏ — truyện manga giải trí không cần chặt như y khoa.

Chính sách: 1 lượt gọi, chỉ ra danh sách việc; lean_script.run() đưa cho patch_model (Opus 5) vá ĐÚNG 1 lần, S3 lại, khoá.
Không lặp, không ESCALATE. Lỗi hạ tầng → trả "LOI" (khoá vẫn đi tiếp, log ghi rõ "chưa kiểm").
Model: gpt-5.6-sol (9router → ns24 → hhtechapi); cả 3 chết → gemini-3.8-flash (ramclouds → ns24 → deepseek). Xem kiem().
"""
import re
from pathlib import Path

import llm_client

PROMPT = """Bạn là biên tập viên kiểm tra DUY NHẤT một thứ: LỜI HỨA CỦA TIÊU ĐỀ có được kịch bản giữ hay không.
Video là manga kể chuyện GIẢI TRÍ (tiếng Nhật) — KHÔNG phải y khoa/pháp lý, không cần chặt chẽ.

TIÊU ĐỀ: {title}
LỜI HỨA CỦA TẬP: {promise}

CÁCH LÀM (làm thầm, không in ra): (1) tách tiêu đề thành từng KHẲNG ĐỊNH mà người xem sẽ tin khi bấm vào (số lượng,
đối tượng, điều kiện, KẾT QUẢ/CẢM NHẬN người kể trải qua); (2) với mỗi khẳng định, tìm trong bài câu nào nói ngược hoặc
rút lại nó.

Chỉ báo lỗi khi thuộc MỘT trong 2 loại:
 A. TỰ PHỦ ĐỊNH: một câu trong bài nói NGƯỢC hoặc RÚT LẠI điều tiêu đề hứa. Ví dụ đã gặp thật:
    - Tiêu đề 「人と話さなくていい」 nhưng kết bài nói 「一言も喋るなって意味じゃなかった」 (rút lại lời hứa "không cần nói").
    - Tiêu đề 「体もラクだった」 (người kể thấy nhẹ nhàng) nhưng người kể nói 「正直に言えば体にきつかった」 (thấy mệt) và
      không bao giờ có lúc nào nhẹ nhàng như tiêu đề nói.
    - Tiêu đề 「〜でも続いた」 (đã làm lâu dài) nhưng bài chỉ kể thử vài ngày rồi bỏ.
    - Tiêu đề hứa 「週3日」 nhưng phần lớn mục trong bài là 週4日.
    Chỉ cần MỘT câu người kể thú nhận điều NGƯỢC với cảm nhận/kết quả tiêu đề hứa là đủ báo, dù phần còn lại của bài xuôi.
 B. KHÔNG TRẢ: điều tiêu đề hứa rõ ràng (số lượng, đối tượng, kết quả) không xuất hiện ở đâu trong bài.
KHÔNG báo: văn phong, dòng thời gian, chi tiết nhỏ, tiêu đề hơi phóng đại kiểu YouTube, câu tiếng Nhật chưa tự nhiên,
lặp hook, thiếu số liệu, góp ý chung chung.

Tối đa 3 việc. Không có lỗi loại A/B thì trả ĐÚNG một dòng: OK
Có lỗi thì trả đúng khuôn (không thêm lời dẫn):
VIEC
- 「câu NGUYÊN VĂN trong bài」 | vì sao mâu thuẫn tiêu đề | cách sửa: chỉ đổi cách nói câu đó (hoặc thêm 1 câu ngắn), giữ tiêu đề, KHÔNG thêm số liệu/dữ kiện mới, KHÔNG đổi cấu trúc bài

=== KỊCH BẢN ===
{script}
"""


def _norm(s):
    return re.sub(r"\s+", "", s)


def _parse(text, script):
    """→ ('OK'|'VIEC'|'LOI', [việc]). Việc có câu trích không nằm trong bài (model bịa) bị bỏ."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return "LOI", []
    items = [l[1:].strip() for l in lines if l.startswith(("-", "・", "•"))]
    if not items:
        return ("OK", []) if lines[0].upper().startswith("OK") else ("LOI", [])
    sn, keep = _norm(script), []
    for it in items[:3]:
        q = re.search(r"「(.+?)」", it)
        if q and _norm(q.group(1)) in sn:
            keep.append(it)
    return ("VIEC", keep) if keep else ("OK", [])


def kiem(script_text, title, d: Path):
    """→ (status, viec, model_name). Ném llm_client.LLMError khi hết chuỗi fallback (nơi gọi bắt → 'chưa kiểm')."""
    pf = Path(d) / "promise.txt"
    promise = pf.read_text(encoding="utf-8").strip() if pf.exists() else "(không có promise.txt — suy từ tiêu đề)"
    prompt = PROMPT.format(title=title, promise=promise, script=script_text)
    kw = dict(temperature=0.2, max_tokens=2500, timeout=300, verbose=False)
    # Sol TRƯỚC (đo 2026-09-29 trên ep02 Lane M: Sol bắt 「体にきつかった」 vs tiêu đề 「ラクだった」, Gemini 3.8 flash bỏ sót
    # 3/3 lần). llm_client provider="sol" đi qua sol_client: 9router → ns24 → hhtechapi. Cả 3 chết mới rơi xuống Gemini
    # (ramclouds → ns24 → deepseek) — yếu hơn nhưng vẫn bắt được ca tự-phủ-định rõ (ep03).
    try:
        r = llm_client.chat(prompt, provider="sol", model="gpt-5.6-sol", **kw)
    except llm_client.LLMError:
        r = llm_client.chat(prompt, task="short", **kw)
    st, viec = _parse(r.text, script_text)
    return st, viec, f"{r.provider}:{r.model}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Kiểm nhẹ lời hứa tiêu đề (chạy thử 1 tập)")
    ap.add_argument("--dir", required=True, help="thư mục tập (có title.txt, promise.txt)")
    ap.add_argument("--script", default="", help="file kịch bản (mặc định <dir>\\script.txt)")
    a = ap.parse_args()
    d = Path(a.dir)
    title = next((l.strip() for n in ("title.txt", "listting.txt") if (d / n).exists()
                  for l in (d / n).read_text(encoding="utf-8").splitlines() if l.strip()), "")
    sc = Path(a.script) if a.script else d / "script.txt"
    st, viec, mod = kiem(sc.read_text(encoding="utf-8"), title, d)
    print(f"[{mod}] {st}")
    for v in viec:
        print(" -", v)
