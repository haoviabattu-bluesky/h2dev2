# -*- coding: utf-8 -*-
r"""chay_buoc3.py — bộ điều phối BƯỚC 3 (ghép video + giao hàng) cho lane satori-jp-obaa.

Thay thế agent "đọc text tự gõ lệnh" (từng trả lời RỖNG 2/2 lần) bằng script TẤT ĐỊNH:
mọi quyết định chạy tiếp / dừng / thử lại nằm CỨNG trong code. Chi tiết + rào chắn:
docs/GIAO_VIEC_VIET_CHAY_BUOC3.md (file tự chứa, đọc trước khi sửa).

Dùng:
  py -3.13 chay_buoc3.py --tab Satori-Lopezzapa68 --dong <STT>
  py -3.13 chay_buoc3.py --tab Satori-Lopezzapa68 --dong <STT> --thu     (chỉ kiểm, không chạy gì)

Chỉ nhận MỘT STT mỗi lần chạy (luật dự án: cấm tự chạy dải/tất cả). Bên gọi muốn nhiều dòng thì tự lặp.

QUY ƯỚC GIỮ DÒNG THỦ CÔNG (VÁ 2, từ 2026-09-13): muốn tạm chặn một dòng không cho bước 3 đụng vào,
ghi vào cột H (GHI CHÚ) của dòng đó một cụm bắt đầu bằng đúng chữ "TẠM DỪNG" — chay_buoc3.py sẽ coi
dòng đó KHÔNG sẵn sàng và chỉ log, không chạy, không ghi gì (tránh đè lên chính ghi chú giữ lại).

8 bước, ĐÚNG THỨ TỰ:
  A. Đọc trang tính: STATUS-IMG bắt đầu "Img done" (không phân biệt hoa/thường) VÀ VIDEO trống.
     Không thoả → DỪNG NGAY, exit 0 (trạng thái bình thường, không phải lỗi).
  B. Tìm thư mục tập trên đĩa theo `folder_pattern` của profile (gọi ghi_cot_video.thu_muc_tap).
  C. Tải ảnh:  drive_handoff.py download-result <slug> "<tập>\img"
  D. Đếm ảnh (RÀO CỨNG): .png trong img/ phải >= số dòng img_prompts.txt. Thiếu → DỪNG HẲN.
  D+. Dọn Drive:  drive_handoff.py clean-job <slug> — ảnh ĐÃ tải đủ về đĩa thì XOÁ VĨNH VIỄN
     jobs/<slug> + results/<slug> khỏi Drive (user chốt 2026-09-14: Drive là TRUNG GIAN, không
     phải kho lưu trữ; 1 tập ~1 GB, quota 16 GB cạn sau ~2 tập). Lỗi dọn → CẢNH BÁO + vẫn chạy
     tiếp (quyết định: đừng chặn sản xuất vì không xoá được rác), báo cáo ghi rõ để dọn tay sau.
     ⚠️ KHÔNG dọn sớm hơn bước D: chỉ được xoá khi đã xác nhận đủ ảnh trên đĩa (đếm đạt).
  E. Sinh img_doan.txt nếu chưa có (sinh_img_doan.py — tool tự bỏ qua nếu đã có).
  F. Ghép:  render_engine.py --slug <tập> --profile <lane> --quality low --workers 8
  G. Giao:  giao_hang.py --slug <tập> --profile <lane>
  H. Ghi cột VIDEO:  ghi_cot_video.py --tab <tab> --dong <STT>

Chính sách retry — ĐÚNG BA LOẠI, KHÔNG GỘP:
  A. Lỗi hạ tầng tạm thời (mạng/API/tiến trình con chết bất thường) → thử tối đa 3 lần,
     nghỉ 10s → 30s → 90s. Hết vẫn lỗi → coi như C (dừng hẳn).
  B. Rớt cổng NỘI DUNG (chỉ áp cho BƯỚC F: render_engine thoát ≠ 0 vì B4Q/B5Q/B8Q) →
     chạy lại tối đa 2 lần thêm (tổng 3). Vẫn rớt → dừng hẳn, báo cáo kèm trích log.
  C. Lỗi cần người quyết → DỪNG NGAY, KHÔNG retry dưới mọi hình thức.

Mỗi lần chạy ghi MỘT báo cáo vận hành mới (không đè lần chạy khác):
  E:\CLAUDE\YOUTUBE\h2dev\BAO_CAO_BUOC3\<tab>_dong<STT>_<yyyymmdd_HHMM>.txt
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

# Import chung cơ chế có sẵn — KHÔNG tự viết lại logic (luật 3.3 của hồ sơ)
import ghi_cot_video as gcv      # noqa: E402  (lane_theo_tab, thu_muc_tap — đã sửa folder_pattern)
import quet_dong_can_anh as qd   # noqa: E402  (svc() — cơ chế đọc Google Sheets dùng chung)
import sheet_tab                 # noqa: E402  (tên tab {Lane}-{kênh})

SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
TAB_MAC_DINH = "Satori-Lopezzapa68"     # tab đổi tên 2026-09-24 theo {Lane}-{kênh}
LANE_MAC_DINH = ""   # 17/10/2026: lane Satori (satori-jp-obaa) đã BỎ — không còn profile mặc định, phải khai --profile.
BAO_CAO_DIR = ROOT / "BAO_CAO_BUOC3"
KHOANG_NGHI = (10, 30, 90)          # loại A: nghỉ giữa các lần thử
COT_H_TIEU_DE = "GHI CHÚ"           # cột H phải đúng tiêu đề này trước khi ghi (rào, copy từ ghi_don_buoc3)

# Phân biệt B (rớt cổng nội dung) vs A (hạ tầng) cho render_engine — nhìn thông báo
DAU_HIEU_CONG_NOI_DUNG = ("DỪNG ở", "B4Q", "B5Q", "B8Q", "KHÔNG ĐẠT", "rớt", "RỚT")


class DungViNguyenNhan(SystemExit):
    """Loại C — lỗi cần người quyết, không retry. Mang theo lý do + exit 0 (không phải lỗi kỹ thuật)."""


def log(s):
    print(s, flush=True)


def gio():
    return time.strftime("%H:%M")


def gio_day():
    return time.strftime("%H:%M %d/%m")


def chay_lenh(ten, args, loai, slug_dir, retry_toi_da=3, trong_luong_loai_b=False):
    """Chạy 1 lệnh ngoài bằng `py -3.13`, theo chính sách retry.

    trả về (ok, lines, so_lan_thu). Loại C không bao giờ tới đây (gọi nơi khác dừng trước).
    """
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)          # venv Hermes (numpy cp311) làm vỡ py -3.13 — xoá khi gọi con
    cmd = ["py", "-3.13"] + args
    so_lan = 0
    while True:
        so_lan += 1
        t0 = time.perf_counter()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", cwd=str(slug_dir), env=env, timeout=7200)
            lines = (r.stdout or "") + (r.stderr or "")
            phut = (time.perf_counter() - t0) / 60
            ok = r.returncode == 0
        except subprocess.TimeoutExpired:
            lines, phut, ok = "TIMEOUT 2 giờ", 120.0, False
        except Exception as e:
            lines, phut, ok = f"LỖI GỌI: {type(e).__name__}: {e}", 0.0, False
        log(f"  {ten}: {'OK' if ok else 'LỖI'} [{phut:.1f}′] (lần {so_lan})")
        if ok:
            return True, lines, so_lan
        # Phân loại lỗi
        if loai == "B" and trong_luong_loai_b:
            la_b = any(d in lines for d in DAU_HIEU_CONG_NOI_DUNG)
            if la_b:
                # Rớt cổng nội dung: cho retry đến retry_toi_da (render_engine tự resume)
                if so_lan < retry_toi_da:
                    log(f"     ⚠️ rớt cổng nội dung (dấu hiệu cổng) — thử lại lần {so_lan + 1}/{retry_toi_da} ngay")
                    continue
                return False, lines, so_lan
        # Loại A: hạ tầng tạm thời — retry có nghỉ
        if so_lan < retry_toi_da:
            nghi = KHOANG_NGHI[min(so_lan - 1, len(KHOANG_NGHI) - 1)]
            log(f"     ! lỗi hạ tầng — thử lại lần {so_lan + 1}/{retry_toi_da} sau {nghi}s")
            time.sleep(nghi)
            continue
        return False, lines, so_lan


def doc_trang_tinh(tab, stt):
    """(status_img, video, de_tai, cot_h) của dòng STT. Đọc bằng cơ chế svc() của quet_dong_can_anh.

    Trả thêm cả cột H (GHI CHÚ) — BƯỚC A cần kiểm dấu 'TẠM DỪNG' do người giữ dòng thủ công
    (VÁ 2, xem docstring đầu file)."""
    dong = stt + 1                       # STT n nằm ở dòng n+1
    res = qd.svc().values().get(spreadsheetId=SHEET_ID,
                                range=f"{tab}!A{dong}:H{dong}").execute()
    hang = res.get("values", [[]])[0]
    def o(i):
        return (hang[i] if i < len(hang) else "").strip()
    return o(5), o(6), o(1), o(7)        # F STATUS-IMG · G VIDEO · B ĐỀ TÀI · H GHI CHÚ


def ghi_cot_h(tab, stt, noi_dung, ghi_de=False):
    """Ghi cột H (GHI CHÚ).

    Mặc định nối thêm sau nội dung cũ bằng ' | ' (không xoá ghi chú người khác) — dùng cho
    các trường hợp LỖI/DỪNG. `ghi_de=True` = GHI ĐÈ hẳn ô (dùng cho XONG: user chốt 2026-09-14
    — khi video xong + ghi cột G rồi thì cột H chỉ cần "Video xong - Chờ đăng", không cần
    chuỗi báo cáo dài).

    Copy đúng 2 rào từ ghi_cot_video.py: đọc lại tiêu đề cột thật; không xoá nội dung người khác.
    Trả về True nếu ghi được; False nếu không (không phải lỗi chặn — chỉ thiếu thông tin phụ).
    """
    s = gcv.svc(doc_thoi=True)
    hd = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!H1").execute().get("values", [[""]])
    ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten_cot != COT_H_TIEU_DE.upper():
        log(f"  ⚠️ cột H dòng 1 đang là '{ten_cot or '(trống)'}' — không phải '{COT_H_TIEU_DE}', bỏ ghi H")
        return False
    dong = stt + 1
    if ghi_de:
        moi = noi_dung
    else:
        cur = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!H{dong}").execute().get("values", [[]])
        cu = (cur[0][0] if cur and cur[0] else "").strip()
        moi = f"{cu} | {noi_dung}" if cu else noi_dung
    gcv.svc(doc_thoi=False).values().update(
        spreadsheetId=SHEET_ID, range=f"{tab}!H{dong}",
        valueInputOption="USER_ENTERED", body={"values": [[moi]]}).execute()
    log(f"  ✓ đã ghi cột H{dong} (GHI CHÚ)")
    return True


def viet_bao_cao(tab, stt, slug, bat_dau, ket_thuc, ket_qua, muc1, muc2, muc3=None, muc4=None):
    """Ghi file báo cáo vận hành mới (không đè). Trả về đường dẫn."""
    BAO_CAO_DIR.mkdir(parents=True, exist_ok=True)
    ten = f"{tab}_dong{stt}_{time.strftime('%Y%m%d_%H%M')}.txt"
    ra = BAO_CAO_DIR / ten
    d = [
        "=" * 80,
        "BÁO CÁO BƯỚC 3 — chay_buoc3.py",
        f"Tab: {tab} · STT: {stt} · Slug: {slug} · Bắt đầu: {bat_dau} · Kết thúc: {ket_thuc}",
        f"Kết quả: {ket_qua}",
        "=" * 80,
        "",
        "MỤC 1 — TỪNG BƯỚC ĐÃ CHẠY (thứ tự thật)",
    ]
    d += [f"  {x}" for x in muc1]
    d += ["", "MỤC 2 — SỐ LIỆU ĐO ĐƯỢC"] + [f"  {x}" for x in muc2]
    if muc3:
        d += ["", "MỤC 3 — DỪNG Ở ĐÂU / CẦN GÌ"] + [f"  {x}" for x in muc3]
    if muc4:
        d += ["", "MỤC 4 — ĐƯỜNG DẪN GIAO HÀNG"] + [f"  {x}" for x in muc4]
    d += ["", "=" * 80, "HẾT"]
    ra.write_text("\n".join(d) + "\n", encoding="utf-8")
    log(f"\n✓ báo cáo: {ra}")
    return ra


def main():
    if not LANE_MAC_DINH:
        raise SystemExit("chay_buoc3.py là bộ điều phối riêng lane Satori — lane đã BỎ 17/10/2026, không chạy nữa.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", default=TAB_MAC_DINH, help=f"tên tab kênh (mặc định {TAB_MAC_DINH})")
    ap.add_argument("--dong", required=True, type=int, help="STT ở cột A (KHÔNG phải số dòng sheet)")
    ap.add_argument("--thu", action="store_true", help="chỉ kiểm tra trạng thái, KHÔNG chạy gì")
    a = ap.parse_args()
    a.tab = sheet_tab.tab_that(a.tab)

    bat_dau = gio_day()
    t_dau = time.perf_counter()
    muc1, muc2, muc3, muc4 = [], [], [], []
    ket_qua = "ĐẠT"
    slug = "(chưa xác định)"

    try:
        # ---------- BƯỚC A — dòng sẵn sàng chưa ----------
        t0 = time.perf_counter()
        status_img, video, de_tai, cot_h = doc_trang_tinh(a.tab, a.dong)
        phut = (time.perf_counter() - t0) / 60
        tam_dung = "TẠM DỪNG" in cot_h.upper()
        san_sang = status_img.lower().startswith("img done") and not video and not tam_dung
        muc1.append(f"A. đọc trạng thái: {'OK' if san_sang else 'KHÔNG SẴN SÀNG'} ({phut:.1f}′) — "
                    f"STATUS-IMG='{status_img[:60] or '(trống)'}' · VIDEO='{video[:40] or '(trống)'}'"
                    + (f" · GHI CHÚ='{cot_h[:60] or '(trống)'}'" if tam_dung else ""))
        if not san_sang:
            if tam_dung:
                ly_do = (f"cột GHI CHÚ (H) có dấu 'TẠM DỪNG' — người khác đang giữ dòng này: "
                         f"'{cot_h[:80]}'")
            elif video:
                ly_do = "cột VIDEO đã có giá trị — tập đã giao xong"
            else:
                ly_do = f"cột STATUS-IMG chưa ghi 'Img done': '{status_img[:60] or '(trống)'}'"
            # VÁ 1: "chưa tới lượt" là trạng thái BÌNH THƯỜNG — KHÔNG ghi báo cáo, KHÔNG đụng cột H
            # (cron định kỳ chạy nhiều dòng sẽ spam rác nếu ghi). Giống hệt nhánh --thu.
            log(f"=== {a.tab} · STT {a.dong} ===")
            log(f"  BƯỚC A: {ly_do}")
            if a.thu:
                log("  (--thu) không ghi gì cả. Bỏ --thu để chạy thật.")
            return 0

        # ---------- BƯỚC B — tìm thư mục tập ----------
        prof = gcv.lane_theo_tab(a.tab)
        if not prof:
            raise DungViNguyenNhan("không profile nào khai publish.upload_channel = " + a.tab)
        t0 = time.perf_counter()
        try:
            tap = gcv.thu_muc_tap(prof, a.dong)
        except SystemExit as e:
            phut = (time.perf_counter() - t0) / 60
            muc1.append(f"B. tìm thư mục tập: LỖI ({phut:.1f}′) — {e}")
            raise DungViNguyenNhan(str(e))
        slug = tap.name
        phut = (time.perf_counter() - t0) / 60
        muc1.append(f"B. tìm thư mục tập: OK ({phut:.1f}′) — {tap}")
        muc2.append(f"- Thư mục tập: {tap}")

        if a.thu:
            log(f"=== {a.tab} · STT {a.dong} · {de_tai[:50]} ===")
            log(f"  trạng thái: STATUS-IMG='{status_img}' · VIDEO trống")
            log(f"  thư mục tập: {tap}")
            log("  (--thu) mọi thứ sẵn sàng — sẽ chạy: download-result → đếm → render → giao → ghi G.")
            log("  Chưa chạy gì cả. Bỏ --thu để chạy thật.")
            return 0

        # ---------- BƯỚC C — tải ảnh về (chỉ khi CHƯA đủ trên đĩa) ----------
        t0 = time.perf_counter()
        pf_c = tap / "img_prompts.txt"
        can_c = len([l for l in pf_c.read_text(encoding="utf-8").splitlines() if l.strip()]) if pf_c.exists() else 0
        co_local = len(list((tap / "img").glob("*.png")))
        if co_local >= can_c:
            phut = (time.perf_counter() - t0) / 60
            muc1.append(f"C. tải ảnh: BỎ QUA ({phut:.1f}′) — đã có sẵn {co_local}/{can_c} ảnh trên đĩa")
        else:
            ok, lines, lan = chay_lenh(
                "C. tải ảnh (download-result)",
                ["drive_handoff.py", "download-result", slug, str(tap / "img")],
                "A", HERE, retry_toi_da=1)   # VÁ 4: drive_handoff.py đã tự retry bên trong — gọi đúng 1 lần
            phut = (time.perf_counter() - t0) / 60
            muc1.append(f"C. tải ảnh: {'OK' if ok else 'LỖI'} ({phut:.1f}′) — thử {lan} lần")
            if not ok:
                raise DungViNguyenNhan(f"tải ảnh thất bại sau {lan} lần — trích: {lines[-300:]}")

        # ---------- BƯỚC D — đếm ảnh (RÀO CỨNG) ----------
        t0 = time.perf_counter()
        co = len(list((tap / "img").glob("*.png")))
        pf = tap / "img_prompts.txt"
        can = len([l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]) if pf.exists() else 0
        phut = (time.perf_counter() - t0) / 60
        muc2.append(f"- Số ảnh: {co}/{can} prompt")
        if co < can:
            muc1.append(f"D. đếm ảnh: LỖI ({phut:.1f}′) — có {co}, cần {can}")
            muc3 = ["Bước dừng: D (đếm ảnh — RÀO CỨNG)",
                    f"Lý do: có {co} ảnh trong img/, cần {can} dòng prompt trong img_prompts.txt",
                    "Đề xuất: việc của máy 2 — báo chủ dự án kèm số thiếu, KHÔNG tự vẽ bù, KHÔNG đổi tên ảnh."]
            ket_qua = "DỪNG Ở BƯỚC D (thiếu ảnh)"
            ra = viet_bao_cao(a.tab, a.dong, slug, bat_dau, gio(), ket_qua, muc1, muc2, muc3)
            ghi_cot_h(a.tab, a.dong, f"chay_buoc3.py chạy {gio()}: {ket_qua} — xem {ra}")
            return 0
        muc1.append(f"D. đếm ảnh: OK ({phut:.1f}′) — {co}/{can}")

        # ---------- BƯỚC D+ — dọn Drive (ảnh đã đủ trên đĩa, không cần giữ trên Drive nữa) ----------
        t0 = time.perf_counter()
        ok, lines, lan = chay_lenh(
            "D+. dọn Drive (clean-job)",
            ["drive_handoff.py", "clean-job", slug],
            "A", HERE, retry_toi_da=3)
        phut = (time.perf_counter() - t0) / 60
        if ok:
            muc1.append(f"D+. dọn Drive: OK ({phut:.1f}′) — đã xoá vĩnh viễn jobs+results/{slug}")
            muc2.append("- Đã dọn Drive (clean-job) sau khi tải đủ ảnh")
        else:
            # Quyết định (user chốt 2026-09-14): dọn là việc vệ sinh — lỗi KHÔNG chặn sản xuất,
            # chỉ cảnh báo để dọn tay sau (drive_handoff.py clean-job <slug>).
            muc1.append(f"D+. dọn Drive: LỖI ({phut:.1f}′) — {lines[-200:]}")
            muc2.append("- ⚠️ CHƯA dọn được Drive — chạy tay: py -3.13 drive_handoff.py clean-job "
                        f"{slug} (quota 16 GB cạn sau ~2 tập nếu không dọn)")

        # ---------- BƯỚC E — sinh img_doan.txt nếu chưa có ----------
        t0 = time.perf_counter()
        if (tap / "img_doan.txt").exists():
            muc1.append("E. img_doan.txt: BỎ QUA (đã có sẵn)")
        else:
            ok, lines, lan = chay_lenh(
                "E. sinh img_doan.txt",
                ["sinh_img_doan.py", "--slug", str(tap)],
                "A", HERE, retry_toi_da=3)
            phut = (time.perf_counter() - t0) / 60
            muc1.append(f"E. sinh img_doan.txt: {'OK' if ok else 'LỖI'} ({phut:.1f}′) — thử {lan} lần")
            if not ok:
                # VÁ 3: "khong xep vua" là lỗi NỘI DUNG THẬT (kịch bản quá ngắn so với số ảnh) —
                # retry vô ích, script không tự đổi, thử 3 lần vẫn y hệt. Thông báo rõ để người đọc
                # báo cáo không thắc mắc "sao thử 3 lần vẫn vậy".
                if "khong xep vua" in lines.lower() or "không xếp vừa" in lines.lower():
                    raise DungViNguyenNhan(f"sinh img_doan.txt: kịch bản quá ngắn so với số ảnh — "
                                           f"trích: {lines[-300:]}")
                raise DungViNguyenNhan(f"sinh img_doan.txt thất bại sau {lan} lần — trích: {lines[-300:]}")

        # ---------- BƯỚC F — ghép video ----------
        t0 = time.perf_counter()
        ok, lines, lan = chay_lenh(
            "F. ghép video (render_engine)",
            ["render_engine.py", "--slug", str(tap), "--profile", prof["id"],
             "--quality", "low", "--workers", "8"],
            "B", HERE, retry_toi_da=3, trong_luong_loai_b=True)
        phut = (time.perf_counter() - t0) / 60
        muc1.append(f"F. ghép video: {'OK' if ok else 'LỖI'} ({phut:.1f}′) — thử {lan} lần")
        muc2.append(f"- Số lần thử lại: bước F thử {lan}/3 lần")
        if not ok:
            muc3 = ["Bước dừng: F (ghép video)",
                    "Lý do (trích nguyên văn): " + lines[-500:],
                    "Đề xuất: rớt cổng nội dung sau 3 lần — báo chủ dự án kèm bước rớt, KHÔNG --force-qc."]
            ket_qua = f"DỪNG Ở BƯỚC F (sau {lan} lần thử)"
            ra = viet_bao_cao(a.tab, a.dong, slug, bat_dau, gio(), ket_qua, muc1, muc2, muc3)
            ghi_cot_h(a.tab, a.dong, f"chay_buoc3.py chạy {gio()}: {ket_qua} — xem {ra}")
            return 0

        # ---------- BƯỚC G — giao hàng ----------
        t0 = time.perf_counter()
        ok, lines, lan = chay_lenh(
            "G. giao hàng (giao_hang)",
            ["giao_hang.py", "--slug", str(tap), "--profile", prof["id"],
             "--ep", str(a.dong)],   # VÒNG 3: STT biết sẵn — truyền thẳng, không để tool đoán từ tên
            "A", HERE, retry_toi_da=3)
        phut = (time.perf_counter() - t0) / 60
        muc1.append(f"G. giao hàng: {'OK' if ok else 'LỖI'} ({phut:.1f}′) — thử {lan} lần")
        if not ok:
            raise DungViNguyenNhan(f"giao_hang thất bại sau {lan} lần — trích: {lines[-300:]}")

        # ---------- BƯỚC H — ghi cột VIDEO ----------
        t0 = time.perf_counter()
        ok, lines, lan = chay_lenh(
            "H. ghi cột VIDEO",
            ["ghi_cot_video.py", "--tab", a.tab, "--dong", str(a.dong)],
            "A", HERE, retry_toi_da=1)          # tool có rào riêng — không retry vô ích
        phut = (time.perf_counter() - t0) / 60
        muc1.append(f"H. ghi cột VIDEO: {'OK' if ok else 'LỖI'} ({phut:.1f}′)")
        if not ok:
            raise DungViNguyenNhan("ghi_cot_video.py thoát khác 0 — KHÔNG tự ghi bằng cách khác. " +
                                   lines[-300:])

        # ---------- XONG — báo cáo ĐẠT ----------
        pub = prof.get("publish") or {}
        # Giống giao_hang.py (anh chốt 2026-09-25): đích results\video_render\ đặt theo TÊN TAB,
        # đích CHANEL\ giữ tên kênh không tiền tố.
        _goc_giao = Path(pub.get("upload_dir") or "")
        _ten = (pub.get("sheet_tab") if "video_render" in _goc_giao.as_posix()
                else None) or pub.get("upload_channel")
        giao = _goc_giao / str(_ten) / tap.name
        muc4 = [str(giao)]
        tong = (time.perf_counter() - t_dau) / 60
        ket_qua = f"ĐẠT (tổng {tong:.1f} phút)"
        muc2.append(f"- Thư mục giao hàng: {giao}")
        ra = viet_bao_cao(a.tab, a.dong, slug, bat_dau, gio(), ket_qua, muc1, muc2, muc4=muc4)
        # user chốt 2026-09-14: xong video + ghi G rồi thì cột H CHỈ cần "Video xong - Chờ đăng"
        # (ghi đè hẳn, không nối chuỗi báo cáo dài). File báo cáo vẫn đủ chi tiết ở BAO_CAO_BUOC3/.
        ghi_cot_h(a.tab, a.dong, "Video xong - Chờ đăng", ghi_de=True)
        log(f"\n✅ XONG: {ket_qua}")
        log(f"   Giao hàng: {giao}")
        log(f"   Báo cáo:   {ra}")
        return 0

    except DungViNguyenNhan as e:
        muc3 = ["Bước dừng: (xem MỤC 1)", f"Lý do (trích nguyên văn): {e}",
                "Đề xuất: cần người quyết — báo chủ dự án, KHÔNG retry."]
        ket_qua = "LỖI CẦN NGƯỜI QUYẾT"
        ra = viet_bao_cao(a.tab, a.dong, slug, bat_dau, gio(), ket_qua, muc1, muc2, muc3)
        ghi_cot_h(a.tab, a.dong, f"chay_buoc3.py chạy {gio()}: {ket_qua} — xem {ra}")
        log(f"\n✗ {ket_qua}: {e}")
        log(f"   Báo cáo: {ra}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
