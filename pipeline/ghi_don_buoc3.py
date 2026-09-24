# -*- coding: utf-8 -*-
"""ghi_don_buoc3.py — ghi ĐƠN VIỆC BƯỚC 3 vào cột H (GHI CHÚ) của trang tính.

    py -3.13 ghi_don_buoc3.py --tab A-shinya_shiryoshitsu --dong 2
    py -3.13 ghi_don_buoc3.py --tab A-shinya_shiryoshitsu --dong 1-6 --thu

VÌ SAO CÓ FILE NÀY (anh chốt 2026-09-12)
------------------------------------------------------------------------------------------------
Trước đây mỗi tập xong bước 1, chủ dự án phải TỰ NHẮN cho agent bước 3: tập nào, thư mục nào, đọc
tài liệu nào, chạy lệnh gì. Đó là việc lặp lại mà máy làm được — và làm chính xác hơn, vì mọi thông
tin trong đơn đều tra được từ profile của lane và từ thư mục tập trên đĩa.

Nay: **trang tính tự nó là bảng giao việc.** Agent bước 3 chỉ cần mở tab kênh, đọc cột H của dòng
mình phụ trách là biết đủ việc phải làm, không cần ai dặn.

Ba thứ đơn TỰ TRA, không nhận gõ tay (gõ tay là chỗ sai chính tả lọt vào trang tính rồi không ai
soát lại):
  · slug + thư mục tập  ← `<slug_dir của lane>/ep<nn>-*` với nn = STT cột A
  · số ảnh phải có      ← đếm dòng `img_ai/prompts.txt` của chính tập đó
  · lane + tên profile  ← profile có `publish.sheet_tab` == tên tab (sheet_tab.py)

RÀO CHẮN (cùng kiểu với `ghi_cot_video.py`):
  1. **Chỉ ghi được cột H.** Cột đích cố định trong code, không tham số nào đổi được. Không có
     đường nào từ file này chạm tới ô khác hay lệnh xoá — trang tính cấm tuyệt đối việc xoá.
  2. Đọc lại **tiêu đề thật** của cột H, không đúng `GHI CHÚ` thì dừng (cột từng đổi chỗ một lần
     rồi: cột VIDEO đã dời từ F sang G ngày 2026-09-12).
  3. Đối chiếu STT thật ở dòng đó, lệch là dừng.
  4. Không đè ô H đã có nội dung trừ khi `--ghi-de`.
"""
import argparse
import json
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import sheet_tab  # noqa: E402  (tên tab {Lane}-{kênh} — nguồn: profile.publish.sheet_tab)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"

COT = "H"                  # CỐ ĐỊNH — xem docstring
TIEU_DE_COT = "GHI CHÚ"
TAI_LIEU = ROOT / "docs" / "GIAO_VIEC_BUOC3_AGENT.md"   # NGUỒN CHÂN LÝ (người sửa ở đây)
BAN_GIAO = ROOT / "CLAUDE-DEEPSEEK.TXT"                 # BẢN DỰNG RA cho Deepseek đọc

# Ô H chỉ là TẤM BIỂN CHỈ ĐƯỜNG, không chứa nội dung việc: ô trang tính đọc trong cửa sổ nhỏ, dán
# cả đơn vào đó thì phải kéo mới thấy hết và không copy lệnh ra được cho tử tế.
MAU_O_H = "Claude trả lời Deepseek {gio}: vào kiểm tra câu trả lời tại {duong_dan}"


def _sang_txt(md: str) -> str:
    """Bỏ trang trí Markdown để đọc trong Notepad cho sạch. Giữ nguyên chữ, giữ nguyên xuống dòng."""
    import re as _re
    ra = []
    for d in md.splitlines():
        d = _re.sub(r"^#{1,6}\s*", "", d)          # tiêu đề
        d = d.replace("**", "").replace("`", "")
        d = _re.sub(r"^>\s?", "", d)               # trích dẫn
        d = _re.sub(r"^\s*```.*$", "", d)          # rào khối lệnh
        ra.append(d.rstrip())
    return "\n".join(ra)


def dung_ban_giao(don_list, gio):
    """Dựng CLAUDE-DEEPSEEK.TXT = việc phải làm NGAY + toàn văn tài liệu bước 3.

    Thân file lấy THẲNG từ `docs/GIAO_VIEC_BUOC3_AGENT.md` chứ không chép tay sang đây — hai bản
    song song là mời sai lệch: sửa một bên, bên kia âm thầm khác đi, mà bên Deepseek đọc lại đúng
    là bản không ai sửa.
    """
    d = [
        "=" * 96,
        "CLAUDE  →  DEEPSEEK     (bản dựng lúc " + gio + ")",
        "=" * 96,
        "",
        "File này tự chứa. Đọc hết rồi làm, không cần hỏi ai, không cần đọc lịch sử chat.",
        "",
        "-" * 96,
        f"PHẦN 1 — VIỆC PHẢI LÀM NGAY ({len(don_list)} tập)",
        "-" * 96,
        "",
    ]
    if don_list:
        for stt, don in don_list:
            d += [f"### STT {stt} (dòng {stt+1} của trang tính)", "", don, ""]
    else:
        d += ["(không có tập nào đang chờ — chưa cần làm gì)", ""]
    d += [
        "-" * 96,
        "PHẦN 2 — TÀI LIỆU ĐẦY ĐỦ: giải thích vì sao, và rớt cổng thì làm gì",
        "-" * 96,
        "",
        _sang_txt(TAI_LIEU.read_text(encoding="utf-8")) if TAI_LIEU.exists()
        else f"(!) thiếu {TAI_LIEU}",
        "",
        "=" * 96,
        "HẾT. Vướng thứ gì không có trong file này: DỪNG và hỏi, đừng tự quyết.",
        "=" * 96,
    ]
    return "\n".join(d) + "\n"


def svc(ghi=False):
    scope = "spreadsheets" if ghi else "spreadsheets.readonly"
    creds = Credentials.from_service_account_file(
        CREDS, scopes=[f"https://www.googleapis.com/auth/{scope}"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


def doc_dai(s):
    """'2' -> [2] · '1-6' -> [1..6] · '2,4' -> [2,4]."""
    ra = []
    for phan in str(s).split(","):
        phan = phan.strip()
        if not phan:
            continue
        if "-" in phan:
            a, b = phan.split("-", 1)
            ra += list(range(int(a), int(b) + 1))
        else:
            ra.append(int(phan))
    return sorted(set(ra))


def lane_theo_tab(tab):
    return sheet_tab.lane_theo_tab(tab)        # tab mới / tab cũ / thư mục kênh / mã lane (2026-09-24)


def thu_muc_tap(prof, stt):
    """Số tập đánh RIÊNG TỪNG LANE nên phải khoanh trong `slug_dir` của lane, không quét assets/*."""
    goc = ROOT / (prof.get("slug_dir") or "assets")
    m = sorted(p for p in goc.glob(f"ep{stt:02d}-*") if p.is_dir())
    return m[0] if len(m) == 1 else None


def soan_don(prof, tap, tab, stt):
    """Dựng nội dung ô H. Mọi con số đều lấy từ đĩa, không viết sẵn trong code."""
    pf = tap / "img_ai" / "prompts.txt"
    n_anh = len([l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]) \
        if pf.exists() else 0
    pub = prof.get("publish") or {}
    giao = Path(pub.get("upload_dir") or "") / str(pub.get("upload_channel")) / tap.name
    d = [
        "BƯỚC 3 — GHÉP VIDEO & GIAO HÀNG.",
        "Giải thích + cách xử lý khi rớt cổng: xem PHẦN 2 ngay bên dưới trong chính file này.",
        "",
        "Chỉ làm khi cột F = 'Img done - n/m ảnh' VÀ cột G còn trống.",
        f"Thư mục tập: {tap}",
        f"Ảnh phải có: {n_anh} tấm (001.png → {n_anh:03d}.png) trong {tap}\\img_ai",
        f"Giao hàng về: {giao}",
        "",
        f"1) py -3.13 pipeline\\drive_handoff.py download-result {tap.name} \"{tap}\\img_ai\"",
        "2) đếm .png trong img_ai phải BẰNG số dòng img_ai\\prompts.txt — thiếu thì DỪNG, báo,",
        "   KHÔNG tự vẽ bù và KHÔNG đổi tên ảnh khác thay vào.",
        f"3) py -3.13 pipeline\\make_video.py --profile {prof['id']} --slug {tap.name} --from B8",
        f"4) py -3.13 pipeline\\ghi_cot_video.py --tab {tab} --dong {stt}",
        "5) đưa đường dẫn thư mục giao hàng cho chủ dự án, kèm số đo thời gian + kết quả cổng.",
        "",
        "CỔNG: B8Q lạc phải ≤3% (rớt thì chạy lại lệnh 3, tối đa 2 lượt rồi báo) · B10 phải 0 lỗi nặng.",
        "CẤM: vẽ lại ảnh bằng gpti2/sinh_anh_canh (tốn tiền) · sửa script.txt/voice.* · --force-qc ·",
        "     --from sớm hơn B8 (xoá mất kịch bản) · xoá dòng/cột trang tính · taskkill chrome.",
        "Vướng gì ngoài danh sách trên: DỪNG và hỏi, đừng tự quyết.",
    ]
    return "\n".join(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", required=True)
    ap.add_argument("--dong", required=True,
                    help="STT o cot A: '2' hoac '1-6' hoac '2,4'. BAT BUOC — cam chay ca tab")
    ap.add_argument("--ghi-de", action="store_true", help="cho phep de len o H da co noi dung")
    ap.add_argument("--thu", action="store_true", help="in ra xem truoc, KHONG ghi")
    a = ap.parse_args()

    stt_list = doc_dai(a.dong)
    if not stt_list:
        raise SystemExit("✗ --dong không đọc được")
    a.tab = sheet_tab.tab_that(a.tab)
    prof = lane_theo_tab(a.tab)
    if not prof:
        raise SystemExit(f"✗ không profile nào khai publish.upload_channel = '{a.tab}'")

    s = svc()
    hd = s.values().get(spreadsheetId=SHEET_ID,
                        range=f"{a.tab}!{COT}1").execute().get("values", [[""]])
    ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten_cot != TIEU_DE_COT.upper():
        raise SystemExit(f"✗ cột {COT} dòng 1 là '{ten_cot or '(trống)'}', không phải "
                         f"'{TIEU_DE_COT}' → cột đã đổi chỗ, DỪNG.")

    d1, d2 = min(stt_list) + 1, max(stt_list) + 1
    rows = s.values().get(spreadsheetId=SHEET_ID,
                          range=f"{a.tab}!A{d1}:{COT}{d2}").execute().get("values", [])

    def o(r, i):
        return (r[i] if i < len(r) else "").strip()

    ghi, bo = [], []
    for stt in stt_list:
        idx = stt + 1 - d1
        r = rows[idx] if 0 <= idx < len(rows) else []
        if o(r, 0) != str(stt):
            bo.append((stt, f"dòng {stt+1} có STT='{o(r, 0)}' — trang tính xê dịch")); continue
        # Đã có cột G = tập đã giao xong. Dán đơn bước 3 lên đó là mời agent làm lại việc đã xong
        # (ghép lại 30 phút video, rồi kẹt ở `ghi_cot_video.py` vì ô G không cho đè).
        if o(r, 6):
            bo.append((stt, f"đã giao video rồi — cột G: {o(r, 6)[:48]}")); continue
        tap = thu_muc_tap(prof, stt)
        if not tap:
            bo.append((stt, f"chưa có thư mục tập ep{stt:02d}-* (bước 1 chưa xong)")); continue
        if not (tap / "img_ai" / "prompts.txt").exists():
            bo.append((stt, "chưa có img_ai\\prompts.txt (bước 1 chưa ra đơn ảnh)")); continue
        # Ô H do CHÍNH công cụ này ghi thì được làm mới tự do (đơn cần cập nhật giờ + nội dung).
        # Ghi chú do NGƯỜI viết thì không được đè im lặng — phải xin `--ghi-de`.
        cu = o(r, 7)
        cua_minh = cu.startswith("Claude trả lời Deepseek") or cu.startswith("BƯỚC 3 —")
        if cu and not cua_minh and not a.ghi_de:
            bo.append((stt, f"ô H có ghi chú của người: {cu[:40]}… (thêm --ghi-de nếu muốn đè)"))
            continue
        ghi.append((stt, soan_don(prof, tap, a.tab, stt)))

    print(f"=== tab {a.tab} · STT {a.dong} · lane {prof['id']} ===")
    for stt, ly_do in bo:
        print(f"  – STT {stt}: bỏ qua — {ly_do}")
    if not ghi:
        print("\n✗ Không có dòng nào ghi được.")
        return 1

    # ⚠️ FILE DÙNG CHUNG CHO CẢ TAB, LỆNH CHỈ NHẬN ĐÚNG MỘT --dong: `dung_ban_giao()` viết ĐÈ
    # TOÀN BỘ file từ con số 0. Gọi `--dong 5` xong thì mọi STT khác đang chờ trong cùng file
    # (ô H của chúng vẫn trỏ đúng đường dẫn này) bị XOÁ MẤT khỏi nội dung — ô H không đổi chữ nên
    # nhìn Sheet không thấy gì sai, nhưng agent bước 3 mở file ra không còn thấy việc của mình.
    # Đã dính thật 2026-09-16: chạy `--dong 5` (bermuda) làm bay mất đơn STT 4 (fermi) dù cột G4
    # còn trống (fermi chưa xong) và ô H4 vẫn ghi "vào kiểm tra tại CLAUDE-DEEPSEEK.TXT".
    # Vá: trước khi dựng file, QUÉT LẠI CẢ TAB tìm mọi dòng KHÁC (không nằm trong --dong lần này)
    # mà cột G còn trống VÀ cột H đã trỏ đúng file này → dựng lại đơn MỚI cho chúng (đọc thẳng đĩa,
    # không chép lại chữ cũ) rồi GỘP vào file, KHÔNG ghi đè ô H của chúng (đã đúng sẵn, khỏi đụng).
    da_xin = set(stt_list)
    toan_bo = s.values().get(spreadsheetId=SHEET_ID, range=f"{a.tab}!A2:H500").execute().get("values", [])
    giu_nguyen = []
    for i, r in enumerate(toan_bo):
        try:
            stt_khac = int(o(r, 0))
        except (ValueError, TypeError):
            continue
        if stt_khac in da_xin or o(r, 6):                     # đã xin lần này, hoặc đã giao xong
            continue
        h_cu = o(r, 7)
        if not (h_cu.startswith("Claude trả lời Deepseek") and BAN_GIAO.name in h_cu):
            continue                                          # H không trỏ file này → không liên quan
        tap_khac = thu_muc_tap(prof, stt_khac)
        if tap_khac and (tap_khac / "img_ai" / "prompts.txt").exists():
            giu_nguyen.append((stt_khac, soan_don(prof, tap_khac, a.tab, stt_khac)))
    if giu_nguyen:
        print(f"\n  ↻ giữ lại {len(giu_nguyen)} đơn đang chờ của STT khác (ô H đã trỏ file này, "
              f"cột G còn trống): " + ", ".join(str(s) for s, _ in giu_nguyen))

    import time
    gio = time.strftime("%H:%M")
    o_h = MAU_O_H.format(gio=gio, duong_dan=BAN_GIAO)
    van_ban = dung_ban_giao(sorted(ghi + giu_nguyen), gio)

    print(f"\n--- {BAN_GIAO.name} ({len(van_ban):,} ký tự) ---")
    print("\n".join(van_ban.splitlines()[:16]) + "\n  …")
    for stt, _ in ghi:
        print(f"--- ô {COT}{stt+1} (STT {stt}) ---\n{o_h}")
    if a.thu:
        print(f"\n(--thu) chưa ghi gì cả. Bỏ --thu để ghi thật: 1 file + {len(ghi)} ô.")
        return 0

    BAN_GIAO.write_text(van_ban, encoding="utf-8")
    print(f"\n✓ đã ghi {BAN_GIAO}")
    w = svc(ghi=True)
    for stt, _ in ghi:
        w.values().update(spreadsheetId=SHEET_ID, range=f"{a.tab}!{COT}{stt+1}",
                          valueInputOption="USER_ENTERED",
                          body={"values": [[o_h]]}).execute()
        print(f"✓ đã ghi {COT}{stt+1} (STT {stt})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
