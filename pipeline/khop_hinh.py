# -*- coding: utf-8 -*-
"""khop_hinh.py — nối LỜI ĐỌC với TỪ KHOÁ HÌNH theo từng đoạn ~15 giây.

    py -3.13 khop_hinh.py --slug <thư mục tập> --profile <lane>

Ra `khop_hinh.json` trong thư mục tập: `[{t0, t1, query, loi}]` — mỗi đoạn lời một từ khoá hình.
`stock_cut.py` đọc file này để chọn clip; không có file thì lùi về chọn theo chương.

VÌ SAO CÓ FILE NÀY — LỖI NGƯỜI XEM THẤY ĐẦU TIÊN
------------------------------------------------------------------------------------------------
`chon_nguon()` chọn clip theo "file nào ít dùng nhất, đủ dài, chưa dùng gần đây". **Nội dung clip
không tham gia vào quyết định.** Xem thật tập 3: đoạn kể về người tự xưng Dennis năm 1989 thì trên
hình là một phụ nữ áo hồng ngồi gõ laptop; đoạn kể vụ mất tích thì hiện máy bay Emirates.

Đã vá hai lớp, và phải hiểu rõ lớp nào chữa được gì:
  · **Kho riêng theo tập** — clip đúng ĐỀ TÀI (hàng không cho chuyện hàng không). Chưa đủ.
  · **Bám chương** — clip đúng CHƯƠNG. Vẫn chưa đủ: một chương dài 5 phút có 5–7 từ khoá và ~70
    cảnh, nên trong chương vẫn là bốc ngẫu nhiên — đang kể máy phát hiện nói dối mà hiện giảng
    đường đại học thì người xem vẫn thấy sai.
  · **File này** — clip đúng CÂU ĐANG ĐỌC. Đây mới là lớp người xem thật sự cảm nhận.

VÌ SAO CHIA ĐOẠN ~15 GIÂY, KHÔNG PHẢI TỪNG CẢNH
  Cảnh dài 4,4 giây; đổi từ khoá mỗi 4 giây thì hình nhảy chủ đề liên tục, xem rối. Một ý trong
  lời kể thường kéo 10–20 giây, nên ~15 giây là đơn vị tự nhiên: 3–4 cảnh liền nhau cùng một ý
  hình, rồi mới chuyển. Và ghim theo MỐC THỜI GIAN chứ không theo chỉ số cảnh, để dựng lại bao
  nhiêu lần vẫn dùng lại được bản đã khớp.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def _ensure_std():
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent

DOAN_GIAY = 15.0        # độ dài một đoạn lời
LO_MOI = 18             # số đoạn hỏi model mỗi lượt


def gom_doan(cues, dai=DOAN_GIAY):
    """Gom cue thành đoạn ~`dai` giây, cắt ở ranh giới cue (không cắt giữa câu)."""
    ra, cur, t0 = [], [], None
    for a, b, t in cues:
        if t0 is None:
            t0 = a
        cur.append(t)
        if b - t0 >= dai:
            ra.append((t0, b, "".join(cur)))
            cur, t0 = [], None
    if cur and t0 is not None:
        ra.append((t0, cues[-1][1], "".join(cur)))
    return ra


def chon_tu_khoa(doan, tu_khoa: list[str], ten_chuong=""):
    """Hỏi model: mỗi đoạn lời hợp với từ khoá hình nào trong danh sách."""
    from llm_client import chat
    dsk = "\n".join(f"[{i+1}] {k}" for i, k in enumerate(tu_khoa))
    dsd = "\n".join(f"{i+1}. {t[:180]}" for i, (_, _, t) in enumerate(doan))
    ask = (
        "Bạn đang chọn HÌNH MINH HOẠ cho một video tài liệu tiếng Nhật.\n"
        f"Dưới đây là danh sách từ khoá hình có sẵn{' của ' + ten_chuong if ten_chuong else ''}:\n"
        f"{dsk}\n\n"
        "Và các đoạn lời đọc. Với MỖI đoạn, chọn MỘT từ khoá hợp nhất để đặt lên hình lúc đó.\n"
        "LUẬT CỨNG:\n"
        f"· Trả ĐÚNG {len(doan)} dòng, dạng `<số đoạn>. <số từ khoá>` (ví dụ `3. 5`).\n"
        "· Chỉ dùng số từ khoá có trong danh sách. Không giải thích, không thêm chữ.\n"
        "· Chọn theo thứ ĐANG ĐƯỢC NÓI TỚI trong đoạn đó (nơi chốn, vật thể, hành động), "
        "không chọn theo cảm xúc chung chung.\n"
        "· Đoạn nào không có từ khoá nào hợp thì chọn cái ÍT LẠC NHẤT, đừng bỏ trống.\n"
        "\nSAU danh sách trên, xuống dòng ghi `---` rồi trả THÊM một danh sách nữa, mỗi đoạn một "
        "dòng, dạng `<số đoạn> | CU_THE hoặc KHONG_KHI | <prompt tiếng Anh>`:\n"
        "· CU_THE = đoạn đang nói tới một VẬT/NƠI/THIẾT BỊ xác định (biển báo, toà nhà cụ thể, "
        "máy móc, tài liệu, buồng lái, bản đồ…) — thứ kho ảnh đời thường khó có đúng.\n"
        "· KHONG_KHI = đoạn chỉ cần cảnh nền gợi không khí (bầu trời đêm, sa mạc, đường vắng, "
        "mây, biển, thành phố về đêm).\n"
        "· prompt tiếng Anh: MỘT câu tả cảnh cần vẽ, phong cách ảnh tư liệu điện ảnh, KHÔNG chữ "
        "trong ảnh, KHÔNG logo, KHÔNG khuôn mặt nhận dạng được. Đoạn KHONG_KHI để trống.\n\n"
        f"ĐOẠN LỜI:\n{dsd}")
    kq = chat(ask, task="short", max_tokens=6000, temperature=0.2, verbose=False)
    text = getattr(kq, "text", None) or str(kq)
    phan = re.split(r"^\s*-{3,}\s*$", text, maxsplit=1, flags=re.M)
    ra = {}
    for d in phan[0].splitlines():
        m = re.match(r"\s*(\d+)\s*[.)．]\s*(\d+)", d.strip())
        if m:
            i, k = int(m.group(1)), int(m.group(2))
            if 1 <= k <= len(tu_khoa):
                ra[i] = tu_khoa[k - 1]
    loai = {}
    if len(phan) > 1:
        for d in phan[1].splitlines():
            m = re.match(r"\s*(\d+)\s*\|\s*(CU_THE|KHONG_KHI)\s*\|?\s*(.*)", d.strip(), re.I)
            if m:
                loai[int(m.group(1))] = (m.group(2).upper(), m.group(3).strip())
    return [(ra.get(i + 1), *loai.get(i + 1, ("KHONG_KHI", ""))) for i in range(len(doan))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--lam-lai", action="store_true")
    a = ap.parse_args()

    import profiles, storyboard, publish_kit, stock_cut
    prof = profiles.load(a.profile)
    slug = Path(a.slug)
    if not slug.is_absolute():
        slug = ROOT / prof.get("slug_dir", "assets") / slug
    ra_f = slug / "khop_hinh.json"
    if ra_f.exists() and not a.lam_lai:
        print(f"  · đã có {ra_f.name}, dùng lại (muốn làm lại: --lam-lai)")
        return

    srt = next((slug / t for t in ("voice_paced.srt", "voice.srt") if (slug / t).exists()), None)
    if srt is None:
        raise SystemExit("✗ không có .srt")
    nhom = stock_cut.doc_tu_khoa_theo_chuong(slug / "stock_queries.txt")
    if not nhom:
        raise SystemExit("✗ stock_queries.txt chưa chia theo chương → không khớp câu được")
    cues = storyboard.parse_cues(srt)
    moc = publish_kit._chuong_theo_marker(
        prof, (slug / "script.txt").read_text(encoding="utf-8"), cues)
    bien = [m[0] for m in moc] + [10 ** 9] if moc else [0, 10 ** 9]
    doan = gom_doan(cues)
    print(f"  {len(doan)} đoạn lời (~{DOAN_GIAY:.0f}s) · {len(nhom)} nhóm từ khoá")

    ra = []

    def them(cac_doan, tu_khoa, ten, so_chuong):
        chon = []
        for i in range(0, len(cac_doan), LO_MOI):
            chon += chon_tu_khoa(cac_doan[i:i + LO_MOI], tu_khoa, ten)
        thieu = sum(1 for x in chon if not x[0])
        cu_the = sum(1 for x in chon if x[1] == "CU_THE" and x[2])
        print(f"    {ten}: {len(cac_doan)} đoạn · {len(cac_doan)-thieu} khớp từ khoá · "
              f"{cu_the} đoạn CHỦ THỂ CỤ THỂ (sẽ sinh ảnh)")
        for (t0, t1, loi), (q, lo, pr) in zip(cac_doan, chon):
            ra.append({"t0": round(t0, 2), "t1": round(t1, 2),
                       "query": q or (tu_khoa[0] if tu_khoa else ""),
                       "loai": lo if pr else "KHONG_KHI", "prompt": pr,
                       "chuong": so_chuong, "loi": loi[:70]})

    # ⚠️ PHẦN DẪN NHẬP PHẢI ĐƯỢC HỎI RIÊNG — BẢN ĐẦU BỎ SÓT HOÀN TOÀN.
    # `moc[0]` là mốc dẫn nhập, `moc[1]` mới là 第1章. Vòng lặp chương bên dưới lấy
    # `t_dau = bien[ch+1]`, nghĩa là chương 1 nhận từ lúc 第1章 bắt đầu trở đi — khoảng
    # `[0 → 第1章)` không rơi vào chương nào nên không đoạn nào được hỏi. Đo thật tập 3:
    # `khop_hinh.json` bắt đầu ở giây 81,7, tức **81 giây mở đầu không hề có khớp hình**, phải
    # lùi về tầng "bốc theo chương" — và đó đúng là chỗ người xem quyết định ở lại hay bỏ đi.
    # Dẫn nhập được chọn trong TOÀN BỘ từ khoá của mọi chương, không bó vào chương 1: nó vốn là
    # bản tóm lược cả tập (mở đầu nói cả lời khai lẫn phần bị bác bỏ ở chương cuối).
    if moc and len(bien) > 1:
        dan_nhap = [d for d in doan if d[0] < bien[1]]
        if dan_nhap:
            tat_ca = list(dict.fromkeys(k for n in nhom for k in n))
            them(dan_nhap, tat_ca, "dẫn nhập", 0)

    # Hỏi THEO TỪNG CHƯƠNG: danh sách từ khoá ngắn hơn thì model chọn chuẩn hơn, và cũng không
    # thể chọn nhầm sang từ khoá của chương khác.
    for ch in range(len(nhom)):
        t_dau = bien[ch + 1] if ch + 1 < len(bien) else 0
        t_cuoi = bien[ch + 2] if ch + 2 < len(bien) else 10 ** 9
        cua_ch = [d for d in doan if t_dau <= d[0] < t_cuoi] if moc else doan
        if not cua_ch:
            continue
        them(cua_ch, nhom[ch], f"第{ch+1}章", ch + 1)
    ra.sort(key=lambda x: x["t0"])
    # Hàng rào: sau khi vá lỗi bỏ sót dẫn nhập, đoạn đầu tiên PHẢI nằm sát đầu video. Trượt cái
    # này nghĩa là lỗi cũ quay lại — báo ngay chứ đừng để phát hiện bằng mắt sau 3 lần dựng.
    if ra and ra[0]["t0"] > 20:
        print(f"  ⚠️ đoạn khớp đầu tiên ở giây {ra[0]['t0']:.0f} — {ra[0]['t0']:.0f} giây mở đầu "
              f"KHÔNG được khớp hình. Kiểm lại mốc chương.")
    ra_f.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {ra_f} ({len(ra)} đoạn)")


if __name__ == "__main__":
    main()
