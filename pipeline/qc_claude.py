"""Cổng NỘI DUNG tầng 2 — dùng `claude -p` (PHIÊN MỚI) làm GIÁM KHẢO độc lập.

Vì sao có file này (đo thật 2026-09-11, tập simbot2-11):
  · `qc_script.py` (gemini-3.8-flash) bắt **8 lỗi**.
  · Bộ chấm Claude phiên mới bắt **22 lỗi**, gồm cả loại gemini MÙ HOÀN TOÀN: dấu vết quy đổi tiền
    Hàn→Nhật theo tỉ giá 1:10 (`八万二千円` = 82만원, `三百円のノート` = 3.000원), thuật ngữ dịch sát
    (`延命の不同意書` thay vì `事前指示書`), phong tục sai (mang 南瓜の煮物 đi thăm bệnh = 호박죽 Hàn,
    nấu 赤飯 thay cho 김장), và **9 câu dịch sát** trong khi gemini chỉ thấy 3.
  · Ngược lại gemini bắt được 2 lỗi Claude bỏ sót (ăn canh miso bằng 匙; mâu thuẫn 「八十四になる姉」).
  ⇒ HAI BÊN BÙ NHAU, không thay nhau. `brain_channel.check_b3q()` chạy CẢ HAI, chặn theo HỢP.

⚠️ ĐIỀU KIỆN SỐNG CÒN: phiên chấm phải **KHÔNG BIẾT GÌ về quá trình viết**. Cùng một phiên vừa viết
vừa chấm thì mù: đo thật, bộ não tự khai "bám gốc 83%" trong khi máy đo 100%, tự khai "lỗi hạ tầng,
không phải script sai" trong khi kịch bản có 14 lỗi. Phiên MỚI chỉ nhận (kịch bản + bản gốc) thì
bới ra 22 lỗi trên chính sản phẩm của Claude.

  py -3.13 qc_claude.py --script <script.txt> --competitor <competitor.txt> [--out <json>]

exit 0 = không lỗi chặn · exit 1 = có lỗi (in từng dòng, ghi kèm JSON để xem lại).
"""
import argparse
import json
import re
import subprocess
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


NHOM = ("VĂN_HOÁ", "DẤU_VẾT_HÀN", "MÂU_THUẪN", "SỐ_HỌC", "SAO_CHÉP")


def de_bai(script, competitor, ngon_ngu="Nhật", goc="Hàn Quốc"):
    return f"""Bạn là GIÁM KHẢO nội dung, KHÔNG phải người viết. Bạn chưa từng thấy kịch bản này.

Đây là kịch bản tiếng {ngon_ngu} cho video YouTube kể chuyện người già (ngách satori), được nhân bản
70/30 từ một video {goc}. Hãy soi thật kỹ và liệt kê LỖI CỤ THỂ theo 5 nhóm:

1. VĂN_HOÁ — sai văn hoá/đời sống {ngon_ngu}: thứ người bản xứ đọc vào là biết "không phải người
   bản xứ viết" (thói quen ăn uống, nghi lễ, xưng hô, thủ tục hành chính, lịch chi trả lương hưu,
   thuật ngữ y tế/pháp lý dịch sát thay vì dùng từ bản xứ…).
2. DẤU_VẾT_HÀN — sót dấu vết bản gốc: tên riêng, món ăn, phong tục, và ĐẶC BIỆT là **con số quy đổi
   máy móc theo tỉ giá** (tiền, giá cả giữ nguyên cấu trúc số của bản gốc).
3. MÂU_THUẪN — nhân vật/quan hệ/mốc thời gian/sự việc tự đá nhau giữa các đoạn.
4. SỐ_HỌC — cộng trừ tuổi, năm tháng, tiền bạc không khớp.
5. SAO_CHÉP — câu/đoạn dịch sát bản gốc tới mức rủi ro chính sách YouTube.

QUY TẮC TRÌNH BÀY: mỗi lỗi MỘT DÒNG theo đúng khuôn
    <MỨC> | <NHÓM>: <trích nguyên văn chỗ sai> — <sai ở chỗ nào>
Không khen, không tóm tắt, không đề xuất cách sửa. Cuối cùng in: TONG_SO_LOI=<số>

<MỨC> chỉ được là CHAN hoặc GOPY, và ranh giới này là TUYỆT ĐỐI:

  **CHAN** — chỉ dùng khi lỗi KIỂM CHỨNG ĐƯỢC, người khác soi lại cũng phải kết luận y hệt:
    · bất khả thi/sai sự thật khách quan (địa lý, thời gian, thủ tục, số tiền, phép tính, tuổi tác)
    · điều kiện pháp lý/hành chính không thoả (hưởng một khoản trợ cấp mà kịch bản không hề đặt tiền đề)
    · sót dấu vết bản gốc: tên riêng, món ăn, đơn vị tiền, con số quy đổi theo tỉ giá
    · câu dịch sát bản gốc gần như nguyên văn
    · hai đoạn trong kịch bản nói ngược nhau

  **GOPY** — mọi thứ còn lại, KỂ CẢ khi bạn rất chắc:
    · "người bản xứ thường nói/làm cách khác", "cách xưng hô này hiếm gặp", "nên chọn số tròn hơn"
    · văn phong, nhịp điệu, chọn từ, mức độ tự nhiên, thị hiếu

⚠️ ĐỌC KỸ ĐIỀU NÀY — nó quan trọng hơn việc bạn tìm được nhiều lỗi:
Kịch bản này ĐÃ qua nhiều lượt sửa. Nếu bạn xếp ý kiến văn phong vào CHAN, người viết sẽ sửa theo,
lượt sau bạn lại thấy chỗ khác chưa "thật tự nhiên" và lại chặn — vòng lặp không bao giờ dừng, đo
thật: 16 lỗi → sửa đúng 14 chỗ → 20 lỗi MỚI. Việc của bạn KHÔNG PHẢI là làm kịch bản hoàn hảo, mà
là chặn thứ SAI. Không có lỗi CHAN nào thì cứ nói thẳng là không có — đó là kết quả hợp lệ và tốt.
Thà bỏ lọt một chỗ vụng còn hơn chặn một kịch bản đúng.

=== BẢN GỐC ===
{competitor}

=== KỊCH BẢN CẦN CHẤM ===
{script}
"""


def cham(script, competitor, model="opus", timeout=1800, on_line=None):
    """Trả (danh_sách_lỗi, raw). Lỗi rỗng = sạch."""
    import brain_steps
    emit = on_line or (lambda s: print(s, flush=True))
    claude = brain_steps.find_claude()
    if not claude:
        emit("  ✗ không tìm thấy `claude` CLI → bỏ qua tầng chấm Claude")
        return None, ""
    cmd = [claude, "-p", "--permission-mode", "bypassPermissions", "--model", model]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    try:
        raw, _ = p.communicate(de_bai(script, competitor), timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        emit(f"  ✗ giám khảo Claude quá {timeout//60} phút → bỏ qua tầng này")
        return None, ""
    return tach_muc(raw or ""), raw or ""


def tach_muc(raw):
    """Trả (chặn, góp ý). Dòng không khai mức → xếp vào GÓP Ý.

    Vì sao mặc định là GÓP Ý chứ không phải CHẶN: đo thật 2026-09-11, cổng cũ chặn theo TỔNG số lỗi
    nên không bao giờ mở được (16 → sửa 14 chỗ → 20 lỗi mới, toàn ý kiến văn phong). Mặc định nghiêm
    khắc làm hỏng cả kịch bản đúng; mặc định nới chỉ bỏ lọt một dòng khai sai khuôn."""
    chan, gopy = [], []
    for dong in raw.splitlines():
        t = dong.strip().lstrip("-•* ").strip()
        muc = ""
        if "|" in t[:12]:
            dau, sau = t.split("|", 1)
            d = dau.strip().upper().replace("Ặ", "A").replace("Ẳ", "A")
            if d in ("CHAN", "CHẶN"):
                muc, t = "CHAN", sau.strip()
            elif d in ("GOPY", "GÓP Ý", "GOP Y"):
                muc, t = "GOPY", sau.strip()
        if not any(t.startswith(n + ":") or t.startswith(n + " :") for n in NHOM):
            continue
        (chan if muc == "CHAN" else gopy).append(t)
    return chan, gopy


def main():
    _ensure_std()
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--competitor", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--max-competitor", type=int, default=24000)
    a = ap.parse_args()

    T0 = time.perf_counter()
    sf = Path(a.script)
    script = sf.read_text(encoding="utf-8")
    comp = Path(a.competitor).read_text(encoding="utf-8")[:a.max_competitor] if a.competitor and \
        Path(a.competitor).exists() else ""
    print(f"=== QC NỘI DUNG (giám khảo Claude, phiên mới · model {a.model}) ===")
    bo, raw = cham(script, comp, a.model)
    loi = None if bo is None else bo[0] + bo[1]

    if loi is None:                       # hạ tầng hỏng — KHÔNG được coi là "sạch"
        print("=== KHÔNG CHẤM ĐƯỢC (lỗi hạ tầng) — đừng coi là ĐẠT ===")
        return 2
    out = Path(a.out) if a.out else sf.with_name("_qc_claude.json")
    dem = {n: sum(1 for l in loi if l.startswith(n)) for n in NHOM}
    out.write_text(json.dumps({"so_loi_chan": len(bo[0]), "so_gop_y": len(bo[1]),
                           "theo_nhom": dem, "chan": bo[0], "gop_y": bo[1], "raw": raw},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    chan, gopy = bo
    for l in chan:
        print(f"   ✗ [CHẶN] {l}")
    for l in gopy:
        print(f"   · [góp ý] {l}")
    print(f"— theo nhóm: " + " · ".join(f"{n}={dem[n]}" for n in NHOM))
    print(f"=== {'ĐẠT' if not chan else f'{len(chan)} LỖI CHẶN'} · {len(gopy)} góp ý (không chặn) "
          f"· {(time.perf_counter()-T0)/60:.1f} phút · chi tiết: {out.name} ===")
    return 0 if not chan else 1


if __name__ == "__main__":
    raise SystemExit(main())
