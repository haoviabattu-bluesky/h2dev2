"""NẮN script.txt về đúng cổng số học BẰNG MÁY — không tiêu quota Claude.

Vì sao có file này: bộ não Claude viết văn hay nhưng **không đếm được ký tự khi đang sinh chữ**.
Đo thật 2026-09-10 trên 3 lượt liên tiếp: nháp đầu ra 20.000 / 10.906 / 16.014 chữ trong khi mục
tiêu 8.100 — và khi bảo nó tự cắt thì mất 35 phút + cạn ngân sách mà vẫn hụt (dừng ở 9.169, thừa
97 chữ). Dạy bằng lời trong prompt đã thử 2 vòng, vẫn lố: nó nhận lệnh "viết 64 đoạn" rồi viết 104.

Cách chữa là ĐỪNG bắt model tự đếm, mà nén THEO KHÚC có hạn mức — đúng kết luận đã ghi trong
`ai_steps.trim_chunked` ("nén cả bản 1 lượt thì ĐỨNG YÊN"). Chuỗi 3 bước dưới đây sao lại đúng
trình tự mà nhánh não-ramcloud đã kiểm chứng (`ai_steps.write_script`), chỉ khác là chạy trên FILE
để nhánh não-Claude gọi được từ ngoài:

    nén khúc (nếu DÀI) → tách câu (nếu NHỊP thưa) → hạ hội thoại (nếu HỘI THOẠI vượt trần)

Mỗi bước CHỈ nhận bản mới khi số lỗi gate GIẢM (bằng nhau thì lấy bản gần mục tiêu hơn) — không bao
giờ để bản sửa làm hỏng thêm.

  py -3.13 fix_gate.py --script <script.txt> --profile satori-jp-obaa [--minutes 30] [--max-trim 3]

exit 0 = ĐẠT cổng · exit 1 = còn lệch (đã ghi bản tốt nhất tìm được).
"""
import argparse
import re
import sys
import time
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


NHIP_ASK = {
    "ja": [
        "次の日本語のナレーション原稿に、読点「、」だけを追加してください。",
        "目的：高齢の語り手がゆっくり息継ぎしながら語る調子にすること。",
        "分量の目安：一文あたり読点は約{n}個。入れすぎて細切れにしないこと。",
        "絶対条件：",
        "  1. 読点「、」を足す以外、文字を一つも変えない。語句の削除・追加・言い換えは禁止。",
        "  2. 「、」は文節の切れ目にだけ置く。単語の途中で切らない。",
        "  2b. 次の位置には絶対に「、」を入れない：て形と補助動詞の間（〜て|まいる・いただく・おる・おく・くれる・しまう・いく・くる・みる）、「のでございます」「のです」の直前、動詞と「こと」の間、「〜ので」と「ございます」の間。息継ぎは助詞（は・が・を・に・で・と）の後や節の切れ目に置く。",
        "  3. 段落の数と改行はそのまま保つ。",
        "  4. 説明や前置きを書かず、原稿だけを返す。",
        "",
    ],
    "ko": [
        "다음 한국어 내레이션 원고에 쉼표만 추가하세요. 다른 글자는 절대 바꾸지 마세요.",
        "어절 경계에만 넣고, 단어 중간을 자르지 마세요. 원고만 반환하세요.",
        "",
    ],
    "en": [
        "Add commas only to the narration below, to create slow breathing pauses.",
        "Do not change, add or remove any other characters. Return only the script.",
        "",
    ],
}


def them_nhip(prof, text, chunk_chars=2500, workers=3, on_line=print):
    """TĂNG mật độ nhịp thở (thêm 、) — CHIỀU NGƯỢC của `ai_steps.reduce_commas` (hàm đó chỉ biết
    TÁCH CÂU để GIẢM phẩy/câu, không có hàm nào thêm nhịp).

    Vì sao cần: ngách kể chuyện người già đòi 4.5-9.0 chữ/nhịp thở; văn viết ra tự nhiên hay dính
    10-13 (câu dài liền hơi). Đo thật 2026-09-10: bộ não Claude tự chế script Python chèn 、 → ĐẶT
    SAI CHỖ, CẮT GIỮA TỪ, phải revert, mất 3,2 phút.

    CHỐT AN TOÀN: bản mới CHỈ được phép thêm 、 — bỏ hết 、 và khoảng trắng đi thì hai bản phải
    GIỐNG HỆT NHAU. Sai một chữ là BỎ khúc đó, giữ nguyên bản cũ. Nhờ vậy không bao giờ có chuyện
    LLM lén viết lại nội dung khi mình chỉ nhờ thêm dấu."""
    from concurrent.futures import ThreadPoolExecutor

    import ai_steps
    import profiles

    lang = prof.get("language", "ja")
    g = profiles.gate(prof)
    lo_p, hi_p = g["comma_per_sentence"]
    lo_h, hi_h = g.get("chars_per_breath") or [4.5, 9.0]
    giua_h = (lo_h + hi_h) / 2          # NHẮM GIỮA DẢI, không phải "càng nhiều càng tốt": đo thật
    n_phay = round((lo_p + hi_p) / 2)   # bản đầu không ghim mức → 9.0 xuống 5.4 nhưng phẩy/câu vọt
    head = [x.format(n=n_phay) if "{n}" in x else x       # lên 8.08, vượt trần 6.0 (hỏng chiều kia).
            for x in NHIP_ASK.get(lang, NHIP_ASK["en"])]
    SEP = "\n\n"
    units = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts, cur, n = [], [], 0
    for u in units:
        cur.append(u)
        n += len(u)
        if n >= chunk_chars:
            parts.append(SEP.join(cur))
            cur, n = [], 0
    if cur:
        parts.append(SEP.join(cur))
    on_line(f"  [thêm nhịp thở] {len(parts)} khúc")

    def _xuong(s):
        """Bộ xương của đoạn văn: bỏ mọi dấu ngắt nhịp + khoảng trắng."""
        return re.sub(r"[\s、,]", "", s)

    def one(i_p):
        i, part = i_p
        truoc = ai_steps.measure(part)["chars_per_breath"]
        try:
            r = ai_steps.chat("\n".join(head + [part]), task="script", temperature=0.3,
                              min_chars=int(len(part) * 0.8), verbose=False)
        except Exception as e:
            on_line(f"     khúc {i+1}: hỏng ({type(e).__name__}) → giữ nguyên")
            return i, part
        moi = ai_steps.normalize_paragraphs(ai_steps.strip_markers(r.text))
        moi, k_go = ai_steps.go_cat_cum(moi)   # LLM vẫn lỡ cắt cụm → gỡ tất định, rồi mới đo
        if k_go:
            on_line(f"     khúc {i+1}: gỡ {k_go} dấu 、 cắt cụm động từ")
        if _xuong(moi) != _xuong(part):
            on_line(f"     khúc {i+1}: ⚠️ LLM đổi cả chữ (không chỉ thêm 、) → BỎ, giữ bản cũ")
            return i, part
        do_moi = ai_steps.measure(moi)
        sau = do_moi["chars_per_breath"]
        # nhận khi GẦN GIỮA DẢI hơn VÀ không làm thủng trần phẩy/câu ở chiều ngược lại
        nhan = abs(sau - giua_h) < abs(truoc - giua_h) and do_moi["comma_per_sentence"] <= hi_p
        on_line(f"     khúc {i+1}: {truoc:.1f} → {sau:.1f} chữ/nhịp thở · "
                f"{do_moi['comma_per_sentence']:.1f} phẩy/câu ({'nhận' if nhan else 'BỎ'})")
        return i, (moi if nhan else part)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = sorted(ex.map(one, list(enumerate(parts))))
    return SEP.join(p for _, p in res)


def _tot_hon(bad_moi, do_moi, bad_cu, do_cu, target):
    """Nhận bản mới khi ít lỗi hơn; hoà thì lấy bản gần mục tiêu độ dài hơn."""
    if len(bad_moi) < len(bad_cu):
        return True
    if len(bad_moi) == len(bad_cu):
        return abs(do_moi["chars"] - target) < abs(do_cu["chars"] - target)
    return False


def nan(prof, text, minutes, max_trim=3, on_line=print):
    """Trả (text_tot_nhat, danh_sach_loi_con_lai)."""
    import ai_steps
    import profiles

    target = profiles.target_chars(prof, minutes)
    text, k_go = ai_steps.go_cat_cum(text)      # bước 0, tất định: gỡ 、 cắt cụm động từ (chỉ xoá 、)
    if k_go:
        on_line(f"  [gỡ nhịp sai chỗ] {k_go} dấu 、 cắt cụm động từ")
    bad, do = ai_steps.check(prof, text, minutes)
    on_line(f"  vào: {do['chars']:,} chữ · {do['comma_per_sentence']} phẩy/câu · "
            f"hội thoại {do['dialogue_ratio']:.0%} · {len(bad)} lỗi")

    for i in range(1, max_trim + 1):
        if not bad:
            break
        # độ dài đã ổn mà chỉ sai nhịp → GIỮ độ dài, đừng đòi nén tiếp (bài học ai_steps)
        giu_dai = not any(b.startswith(("DÀI", "NGẮN")) for b in bad)
        t0 = time.perf_counter()
        moi = ai_steps.trim_chunked(prof, text, target, minutes, keep_length=giu_dai)
        bad_moi, do_moi = ai_steps.check(prof, moi, minutes)
        on_line(f"  [{i}] {'giữ-dài' if giu_dai else 'nén'}-khúc {do['chars']:,}→{do_moi['chars']:,} chữ "
                f"({len(bad)}→{len(bad_moi)} lỗi) · {(time.perf_counter()-t0)/60:.1f}′")
        if _tot_hon(bad_moi, do_moi, bad, do, target):
            text, bad, do = moi, bad_moi, do_moi
        else:
            on_line("      ⚠️ không tốt hơn → giữ bản trước, dừng vòng nén")
            break

    # NHỊP / HƠI / HỘI THOẠI là ba lỗi RIÊNG, trim_chunked không xử được (bài học ep09).
    # ⚠️ NHỊP và HƠI có HAI CHIỀU: quá NHIỀU phẩy thì tách câu (reduce_commas), quá ÍT thì phải
    # THÊM nhịp (them_nhip). Bản đầu chỉ gọi reduce_commas cho mọi lỗi NHỊP là sai nửa số ca —
    # ngách kể chuyện người già gần như luôn thiếu nhịp chứ không thừa.
    g = profiles.gate(prof)
    for _ in range(2):
        if not bad:
            break
        viec = None
        if do["chars_per_breath"] > (g.get("chars_per_breath") or [0, 9])[1] or \
                do["comma_per_sentence"] < g["comma_per_sentence"][0]:
            viec = ("thêm nhịp thở", lambda p, t: them_nhip(p, t, on_line=on_line))
        elif do["comma_per_sentence"] > g["comma_per_sentence"][1]:
            viec = ("tách câu dài", ai_steps.reduce_commas)
        if not viec:
            break
        ten, ham = viec
        t0 = time.perf_counter()
        moi = ham(prof, text)
        bad_moi, do_moi = ai_steps.check(prof, moi, minutes)
        on_line(f"  [{ten}] {len(bad)}→{len(bad_moi)} lỗi · {(time.perf_counter()-t0)/60:.1f}′")
        if _tot_hon(bad_moi, do_moi, bad, do, target):
            text, bad, do = moi, bad_moi, do_moi
        else:
            on_line("      ⚠️ không cải thiện → giữ bản trước")
            break

    if any(b.startswith("HỘI THOẠI") for b in bad):
        t0 = time.perf_counter()
        moi = ai_steps.reduce_dialogue(prof, text)
        bad_moi, do_moi = ai_steps.check(prof, moi, minutes)
        on_line(f"  [hạ hội thoại] {len(bad)}→{len(bad_moi)} lỗi · {(time.perf_counter()-t0)/60:.1f}′")
        if _tot_hon(bad_moi, do_moi, bad, do, target):
            text, bad, do = moi, bad_moi, do_moi
        else:
            on_line("      ⚠️ không cải thiện → giữ bản trước")
    return text, bad


def main():
    _ensure_std()
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--minutes", type=float, default=0)
    ap.add_argument("--max-trim", type=int, default=3)
    a = ap.parse_args()

    import profiles

    T0 = time.perf_counter()
    prof = profiles.load(a.profile)
    f = Path(a.script)
    goc = f.read_text(encoding="utf-8")
    print(f"=== NẮN CỔNG SỐ HỌC: {f.name} (profile {a.profile}) ===")
    text, bad = nan(prof, goc, a.minutes or None, a.max_trim)

    if text != goc:
        f.write_text(text, encoding="utf-8")
        print(f"  → đã ghi đè {f.name}")
    print(f"=== {'ĐẠT' if not bad else f'CÒN {len(bad)} LỖI'} · tổng {(time.perf_counter()-T0)/60:.1f} phút ===")
    for b in bad:
        print(f"   ✗ {b}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
