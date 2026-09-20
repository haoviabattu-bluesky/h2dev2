# -*- coding: utf-8 -*-
"""sinh_anh_canh.py — VẼ ẢNH cho những đoạn lời mà kho stock không phục vụ được.

    py -3.13 sinh_anh_canh.py --slug <thư mục tập> [--tu 0 --den 600] [--theo-qc] [--uoc-tinh]

Đọc `khop_hinh.json` (đoạn lời nào nói tới vật/nơi cụ thể + prompt tiếng Anh đã soạn sẵn), sinh ảnh
qua `gen_images.py`, gom vào `img_ai/` kèm `img_meta.json`. `stock_cut.py` tự đọc thư mục đó.

BA QUYẾT ĐỊNH CÓ CHỦ Ý
------------------------------------------------------------------------------------------------
1. **CHỈ vẽ đoạn `CU_THE`.** Đoạn `KHONG_KHI` (sa mạc, trời đêm, đường vắng) thì Pexels thừa sức
   và clip thật bao giờ cũng hơn ảnh vẽ — có chuyển động. Vẽ tất là đốt tiền để đổi lấy hình xấu
   hơn.
2. **Chạy bù, không chạy lại.** `img_meta.json` ghi đoạn nào đã có ảnh; lần chạy sau chỉ vẽ đoạn
   còn thiếu rồi đánh số tiếp. Không có cái này thì mỗi vòng sửa là trả lại tiền cho toàn bộ ảnh
   đã đạt.
3. **Prompt tiếng Anh.** gpti2 tính phụ phí theo token: tiếng Việt có dấu ~1,0 token/ký tự còn
   ascii ~0,17 → cùng một ý, prompt tiếng Anh rẻ hơn khoảng 6 lần và vẫn nằm trong 1.500 token
   miễn phí. (Xem skill `gpti2.md`.)

MỖI CẢNH MỘT GÓC MÁY KHÁC NHAU
  Một đoạn lời 15 giây phủ 3–4 cảnh. Dùng một tấm cho cả đoạn thì hình đứng chết 15 giây; sinh
  3–4 tấm cùng nội dung nhưng khác góc máy thì vẫn là một ý hình, mà nhịp cắt của video giữ nguyên.
"""
import argparse
import json
import os
import subprocess
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
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent

GOC_MAY = ["wide establishing shot", "medium shot, slightly low angle",
           "close detail shot", "high angle wide shot"]
DUOI = ("cinematic documentary photography, muted desaturated palette, deep shadows, "
        "35mm film grain, no text, no logo, no watermark, no recognizable faces, "
        "no readable registration numbers or tail numbers or serial numbers or license plates, "
        "no date stamps, no timestamp overlays, no caption text")
GIAY_MOI_CANH = 4.3      # nhịp cắt thật của lane — dùng để đoán số ảnh cần cho một đoạn
GIA_MOI_ANH = 50         # đồng, gpti2 quality=low


def doan_can_ve(slug: Path, tu, den, theo_qc):
    """Trả [(t0, t1, query, prompt, số ảnh cần)] cho các đoạn CU_THE trong khoảng thời gian."""
    kh = json.loads((slug / "khop_hinh.json").read_text(encoding="utf-8"))
    lac = None
    if theo_qc:
        f = slug / "qc_canh.json"
        if not f.exists():
            raise SystemExit("✗ --theo-qc cần qc_canh.json (chạy qc_canh.py trước)")
        lac = [x["t0"] for x in json.loads(f.read_text(encoding="utf-8")) if x.get("muc") == 0]
    ra = []
    for b in kh:
        t0, t1 = float(b["t0"]), float(b["t1"])
        if b.get("loai") != "CU_THE" or not (b.get("prompt") or "").strip():
            continue
        if den and t0 >= den or t1 <= tu:
            continue
        # --theo-qc: chỉ vẽ đoạn ĐÃ CHỨNG MINH là hỏng trên bản dựng, thay vì vẽ mọi đoạn CU_THE.
        # Nhiều đoạn CU_THE vẫn được kho phục vụ tử tế — vẽ đè lên là tiêu tiền cho thứ đã đạt.
        if lac is not None and not any(t0 <= t < t1 for t in lac):
            continue
        ra.append((t0, t1, b.get("query", ""), b["prompt"].strip(),
                   max(2, round((t1 - t0) / GIAY_MOI_CANH))))
    return ra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out", default="", help="thư mục ảnh (mặc định <slug>/img_ai)")
    ap.add_argument("--tu", type=float, default=0.0)
    ap.add_argument("--den", type=float, default=0.0, help="0 = hết tập")
    ap.add_argument("--theo-qc", action="store_true",
                    help="chỉ vẽ đoạn mà qc_canh.json chấm LẠC — rẻ hơn vẽ mọi đoạn CU_THE")
    ap.add_argument("--uoc-tinh", action="store_true", help="chỉ in số ảnh + tiền, KHÔNG sinh")
    ap.add_argument("--chi-don", action="store_true",
                    help="RA ĐƠN cho máy khác vẽ: ghi img_meta.json + prompts.txt rồi dừng, "
                         "KHÔNG gọi nhà cung cấp ảnh nào")
    ap.add_argument("--quality", default="low")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()

    slug = Path(a.slug)
    if not slug.is_absolute():
        slug = ROOT / "assets" / slug
    out = Path(a.out) if a.out else slug / "img_ai"
    out.mkdir(parents=True, exist_ok=True)
    meta_f = out / "img_meta.json"
    meta = json.loads(meta_f.read_text(encoding="utf-8")) if meta_f.exists() else []
    da_co = {(round(float(m["t0"]), 2), round(float(m["t1"]), 2)) for m in meta}
    dsanh = sorted(p for p in out.iterdir() if p.suffix.lower() == ".png")
    if len(dsanh) != len(meta):
        print(f"  ! {out.name}: {len(meta)} bản ghi nhưng {len(dsanh)} ảnh — đánh số tiếp từ "
              f"{max(len(dsanh), len(meta)) + 1:03d}")

    can = [d for d in doan_can_ve(slug, a.tu, a.den, a.theo_qc)
           if (round(d[0], 2), round(d[1], 2)) not in da_co]
    tong = sum(d[4] for d in can)
    print(f"[{slug.name}] {len(can)} đoạn cần vẽ · {tong} ảnh · ~{tong*GIA_MOI_ANH:,}đ"
          + (f" (đã có sẵn {len(meta)} ảnh, bỏ qua)" if meta else ""))
    for t0, t1, q, _, k in can:
        print(f"   {t0:7.0f}-{t1:<7.0f} {k} ảnh  \"{q}\"")
    if a.uoc_tinh or not can:
        return 0

    bat_dau = max(len(dsanh), len(meta))
    dong, moi = [], []
    for t0, t1, q, pr, k in can:
        for j in range(k):
            dong.append(f"{pr}, {GOC_MAY[j % len(GOC_MAY)]}, {DUOI}")
            moi.append({"t0": t0, "t1": t1, "query": q, "k": j})
    # Tên file ĐẶT TRƯỚC, ghi thẳng vào bản ghi. Nhờ vậy `stock_cut.gan_anh_ai()` ghép ảnh với
    # đoạn lời THEO TÊN chứ không theo thứ tự — thiếu tấm nào chỉ hụt đúng tấm đó, các tấm sau
    # không bị tụt bậc. Bắt buộc khi ảnh do máy khác vẽ rồi gửi sang.
    for i, m in enumerate(moi, bat_dau + 1):
        m["file"] = f"{i:03d}.png"
    pf = out / "_prompts.txt"
    pf.write_text("\n".join(dong) + "\n", encoding="utf-8")
    if a.chi_don:
        don = out / "prompts.txt"
        don.write_text("".join(f"{m['file']}\t{d}\n" for m, d in zip(moi, dong)), encoding="utf-8")
        meta_f.write_text(json.dumps(meta + moi, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ ĐƠN HÀNG ẢNH (chưa vẽ tấm nào):\n   {don}\n   {meta_f}")
        print(f"   {len(moi)} ảnh cần vẽ · đặt tên {moi[0]['file']} → {moi[-1]['file']} · "
              f"khung ngang 16:9 · thả vào {out}")
        return 0

    # Sinh ra thư mục TẠM rồi mới chuyển sang: `gen_images.py` luôn đánh số từ 001, đổ thẳng vào
    # `out` là ghi đè mất loạt ảnh cũ.
    tam = out / "_moi"
    tam.mkdir(exist_ok=True)
    for p in tam.glob("*.png"):
        p.unlink()
    r = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "gen_images.py"),
                        "--prompts", str(pf), "--out", str(tam), "--orient", "landscape",
                        "--quality", a.quality, "--workers", str(a.workers)],
                       cwd=str(HERE))
    ra_moi = sorted(tam.glob("*.png"))
    if r.returncode != 0 or not ra_moi:
        raise SystemExit(f"✗ sinh ảnh lỗi (mã {r.returncode}, {len(ra_moi)} ảnh)")
    if len(ra_moi) != len(moi):
        print(f"  ! xin {len(moi)} ảnh, nhận {len(ra_moi)} → chỉ ghi nhận phần có thật")
        moi = moi[:len(ra_moi)]
        ra_moi = ra_moi[:len(moi)]
    for i, (p, m) in enumerate(zip(ra_moi, moi), bat_dau + 1):
        p.replace(out / f"{i:03d}.png")
    for p in tam.glob("*"):
        p.unlink()
    tam.rmdir()
    meta += moi
    meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {len(ra_moi)} ảnh mới → {out}  (tổng {len(meta)} ảnh · {len(meta)*GIA_MOI_ANH:,}đ)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
