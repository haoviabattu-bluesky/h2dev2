# -*- coding: utf-8 -*-
r"""hook_tap_md.py — sinh + nghiệm thu `HOOK_TAP.md` (NGUỒN CHÂN LÝ hook của một tập).

Anh chốt 2026-09-24: máy 1 làm xong việc thì **phải gửi kèm file hook text** để
`E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH` (viết tiêu đề · mô tả · chữ thumbnail) và **máy 2** đọc mà làm.

Vì sao phải có tool thay vì viết tay: quy ước `HOOK_TAP.md` đã tồn tại từ 2026-09-24 (mẫu ở
`assets\kenko-chiebukuro\ep01-tento-kossetsu\HOOK_TAP.md`) nhưng **không tool nào sinh, không cổng nào
kiểm, `dong_goi_may2.py` không gói, dự án tiêu đề chưa đọc** → đúng tình trạng "phải có người nhắc mới
làm" mà anh vừa yêu cầu bỏ. Cùng bài học memory `khong-giao-viec-thu-cong-rao-nam-trong-tool`.

CHIA VIỆC (đừng trộn lại):
  · MÁY rút phần TẤT ĐỊNH — mốc giây, lời đọc JP/VI, hình từng cảnh, từ khoá đã verify grep được
    trong `script.txt`, danh sách ảnh/file. Máy không hiểu nội dung nên không đoán.
  · NGƯỜI (bước 1) viết phần cần HIỂU NỘI DUNG — lời hứa tiếng Việt, điều CẤM lộ, ảnh nào mạnh nhất.
    Tool để lại dấu `<<CẦN NGƯỜI: …>>`; `kiem()` coi dấu còn sót là CHƯA XONG và chặn giao hàng.
    Đây đúng luật CLAUDE.md: thứ cần nội dung thì bước 1 phải viết xong và để lại thành file, KHÔNG
    được để trống rồi trông chờ bước 2/3 tự sinh.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import profiles  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEN = "HOOK_TAP.md"
CAN_NGUOI = "<<CẦN NGƯỜI:"


def _doc(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _srt(p):
    """[(giây_bắt_đầu, chữ)] — dùng để ghép cột tiếng Việt vào bảng mốc giây."""
    ra = []
    for kh in re.split(r"\n\s*\n", _doc(p)):
        m = re.search(r"(\d\d):(\d\d):(\d\d)[,.](\d+)\s*-->", kh)
        if m:
            s = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000
            ra.append((s, " ".join(kh.splitlines()[2:]).strip()))
    return ra


def _vi_gan_nhat(vi_cues, t0, t1):
    """Câu Việt phủ khoảng [t0,t1) — SRT Việt không cắt trùng khít mốc cảnh nên lấy theo GIAO NHAU."""
    ra = [t for s, t in vi_cues if t0 - 0.6 <= s < t1 - 0.2]
    return " ".join(ra) if ra else ""


# ─────────────────────────────────────────────── phần TẤT ĐỊNH: từ khoá có thật
# Ứng viên "vế được phép hứa": cụm có SỐ + đơn vị · lời thoại 「…」 · chuỗi katakana · chuỗi kanji.
# Chỉ giữ cụm THỰC SỰ tìm thấy trong script.txt (dùng chuẩn hoá của qc_goi_dang nên khớp cả
# 76秒 ↔ 七十六秒) — đây chính là luật G2, nên liệt kê sẵn để bên viết tiêu đề không phải đoán.
_UNGVIEN = re.compile(r"「[^」]{2,20}」|[0-9０-９〇一二三四五六七八九十百千万]+[年月日歳円人回分秒時位つ]"
                      r"|[ァ-ヴー]{3,}|[一-龥]{2,6}")


def tu_khoa_co_that(hook_text, script_text, toi_da=24):
    """Chỉ quét CHÍNH HOOK (không quét thân bài): tiêu đề/thumbnail phải hứa đúng thứ hook đã mở.
    Bản đầu quét thêm `script[:4000]` → lọt một loạt kanji 2 chữ chung chung của thân bài
    (言葉/判断/体重/水分/不足/病気/理由) làm danh sách mất tác dụng chỉ đường."""
    import qc_goi_dang as G
    sc = G.norm(script_text)
    ra, thay = [], set()
    for m in _UNGVIEN.finditer(hook_text):
        v = m.group(0).strip("「」")
        n = G.norm(v)
        if len(n) < 2 or n in thay or n not in sc:
            continue
        thay.add(n)
        ra.append(v)
        if len(ra) >= toi_da:
            break
    return ra


def _hinh_tung_canh(hd):
    """Mô tả hình từng cảnh: ưu tiên `ky_vong` trong hook_timeline.json, thiếu thì lấy grok_jobs.csv."""
    tl = hd / "hook_timeline.json"
    if tl.exists():
        try:
            return {int(x["n"]): (x.get("ky_vong") or "").strip()
                    for x in json.loads(tl.read_text(encoding="utf-8")).get("shots", [])}
        except Exception:
            pass
    g = hd / "grok_jobs.csv"
    if g.exists():
        try:
            with g.open(encoding="utf-8-sig", newline="") as f:
                return {i: (r.get("prompt") or r.get("mo_ta") or "").strip()[:160]
                        for i, r in enumerate(csv.DictReader(f), 1)}
        except Exception:
            pass
    return {}


def sinh(d, profile_id, ghi_de=False):
    """Trả (đường_dẫn, list cảnh báo). KHÔNG ghi đè file đã có trừ khi `ghi_de` — phần người viết tay
    trong đó là thứ không sinh lại được, mất là phải viết lại từ đầu."""
    d = Path(d)
    out = d / TEN
    canh = []
    if out.exists() and not ghi_de:
        return out, [f"{TEN} đã có — giữ nguyên (dùng --ghi-de nếu thật sự muốn viết lại, "
                     f"CHÚ Ý: xoá mất phần viết tay)"]
    prof = profiles.load(profile_id)
    hd = d / "hook"
    hook = _doc(hd / "hook_locked.txt").strip()
    if not hook:
        return out, [f"chưa có {hd / 'hook_locked.txt'} — chạy hook_stage.py trước"]
    promise = _doc(d / "promise.txt").strip() or _doc(d / "hook" / "promise.txt").strip()
    script = _doc(d / "script.txt")
    vi = _srt(hd / "hook_vi.srt")
    hinh = _hinh_tung_canh(hd)
    tl = {}
    if (hd / "hook_timeline.json").exists():
        try:
            tl = json.loads((hd / "hook_timeline.json").read_text(encoding="utf-8"))
        except Exception as e:
            canh.append(f"hook_timeline.json không đọc được ({type(e).__name__}) — bảng mốc giây để trống")
    shots = tl.get("shots") or []
    g = profiles.gate(prof)
    lane_list = bool((prof.get("goi_dang") or {}).get("list_mode"))

    L = [f"# HOOK TẬP — {profile_id} / {d.name}", "",
         f"> Người đọc: **dự án tiêu đề `E:\\CLAUDE\\YOUTUBE\\YT-TITLE-RESEARCH`** (S2 tiêu đề · S4 mô tả"
         f" · S7 chữ thumbnail) **và máy 2**.",
         "> Đây là NGUỒN CHÂN LÝ của hook tập này. Tiêu đề · chữ thumbnail · câu đầu mô tả phải cùng"
         " MỘT lời hứa với hook (luật G1–G8, `docs\\QUY_TAC_GOI_DANG.md`).",
         "> Hook đã KHOÁ (`hook\\hook_lock.json`) — **không sửa chữ hook để khớp tiêu đề; sửa tiêu đề"
         " cho khớp hook.**",
         # CỐ Ý không nhắc đúng token `<<CẦN NGƯỜI:` trong dòng hướng dẫn này — `kiem()` đếm token đó
         # để biết còn chỗ nào chưa viết, nhắc nguyên văn là cổng đếm luôn chính lời dặn (đã dính:
         # khung sinh ra báo "5 chỗ" trong khi chỉ có 4).
         "> File này do `pipeline\\hook_tap_md.py` sinh phần tất định; chỗ nào còn dấu «CẦN NGƯỜI» là"
         " phần bước 1 PHẢI tự viết (máy không hiểu nội dung) — cổng chặn giao hàng khi còn sót.", "",
         "## 1. Lời hứa (1 câu)",
         f"**JP:** {promise or (CAN_NGUOI + ' chưa có promise.txt — chốt 1 câu lời hứa>>')}",
         f"**VI:** {CAN_NGUOI} dịch/diễn lại lời hứa trên bằng 1 câu tiếng Việt>>", ""]

    L += ["## 2. Hook nguyên văn (mốc giây đo trên giọng thật của kênh)"]
    if shots:
        L += ["| Giây | Tiếng Nhật | Tiếng Việt | Hình (clip) |", "|---|---|---|---|"]
        for x in shots:
            t0, t1 = float(x.get("t0", 0)), float(x.get("t1", 0))
            v = _vi_gan_nhat(vi, t0, t1) or (CAN_NGUOI + " dịch>>")
            L.append(f"| {t0:.1f}–{t1:.1f} | {(x.get('voice') or '').strip()} | {v} | "
                     f"{hinh.get(int(x.get('n', 0)), '').strip()} |")
    else:
        L += ["(chưa có `hook/hook_timeline.json` — dán nguyên văn hook, mốc giây bổ sung sau)", "",
              "```", hook, "```"]
    if tl.get("cau_ket_hook"):
        L.append("")
        L.append(f"Câu kết hook (theo `hook_timeline.json`): **{tl['cau_ket_hook']}**")
    L.append("")

    tk = tu_khoa_co_that(hook, script)
    L += ["## 3. Từ khoá CÓ THẬT (tiêu đề/thumbnail chỉ được hứa những thứ này)",
          "> Máy đã grep từng cụm trong `script.txt`, so cả chữ số ↔ chữ Hán (76秒 ↔ 七十六秒). Cụm nào"
          " KHÔNG có trong danh sách này thì cổng G2 sẽ chặn khi đưa lên tiêu đề/thumbnail.",
          ("- " + " · ".join(f"`{x}`" for x in tk)) if tk else
          "- (không rút được cụm nào — kiểm lại script.txt)", ""]

    L += ["## 4. CẤM lộ trên tiêu đề / thumbnail / câu đầu mô tả"]
    if lane_list:
        n = g.get("list_item_count") or 0
        L.append(f"- **Tên mục số 1** và tên bất kỳ mục nào trong {n} mục — hook cố ý giấu "
                 f"(luật G4; kênh mẫu không nêu tên mục trong 120 giây đầu).")
    L += [f"- {CAN_NGUOI} liệt kê điều tập này KHÔNG được hứa: chi tiết kịch bản chưa xảy ra, con số"
          f" không có trong script, tên riêng chưa được nói…>>", ""]

    anh = sorted((hd / "img").glob("*.png")) if (hd / "img").is_dir() else []
    L += ["## 5. Gợi ý hình cho thumbnail (ảnh hook đã có, cùng nét vẽ)"]
    L += [f"- `{p}`" for p in anh[:10]] or ["- (chưa có ảnh trong `hook/img/`)"]
    L += [f"- {CAN_NGUOI} chỉ ra ảnh nào MẠNH NHẤT và vì sao (mặt to, đọc được ở 360px, khớp câu 0s)>>",
          ""]

    L += ["## 6. File liên quan"]
    for ten in ("hook/hook_locked.txt", "hook/hook_timeline.json", "hook/hook_voice.mp3",
                "hook/hook_vi.srt", "hook/hook_preview_vi.mp4", "promise.txt", "script.txt"):
        if (d / ten).exists():
            L.append(f"- `{d / ten}`")
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return out, canh


# ─────────────────────────────────────────────── cổng nghiệm thu
def kiem(d):
    """Trả list lỗi CHẶN (rỗng = đủ để giao). 0 LLM.

    Hai lỗi, cả hai đều từng xảy ra thật trong dự án:
      1. thiếu hẳn file → bên viết tiêu đề phải tự đọc hook trong `hook/`, mà nó không code đường đó;
      2. còn dấu `<<CẦN NGƯỜI:` → đã sinh khung nhưng chưa ai viết phần nội dung, giao đi là bên kia
         viết tiêu đề trên một file rỗng nghĩa (đúng kiểu sự cố 2 tập satori lọt với listing rỗng).
    """
    d = Path(d)
    f = d / TEN
    if not (d / "hook" / "hook_locked.txt").exists():
        return []                            # tập chưa có hook — không phải việc của cổng này
    if not f.exists():
        return [f"thiếu {f} — máy 1 phải gửi file hook text để dự án tiêu đề (YT-TITLE-RESEARCH) và "
                f"máy 2 đọc mà làm. Sinh khung: py -3.13 pipeline\\hook_tap_md.py --slug <tập> "
                f"--profile <lane>"]
    txt = f.read_text(encoding="utf-8")
    # Bỏ dòng trích dẫn `>` — đó là khối hướng dẫn đầu file, không phải chỗ phải viết. (Đã đếm nhầm
    # chính lời dặn khi mới viết tool: khung sinh ra báo "5 chỗ" trong khi chỉ có 4.)
    con = [l.strip() for l in txt.splitlines() if CAN_NGUOI in l and not l.lstrip().startswith(">")]
    if con:
        return [f"{f} còn {len(con)} chỗ `{CAN_NGUOI}` chưa viết — bước 1 phải viết xong phần cần hiểu "
                f"nội dung trước khi giao (vd: {con[0][:90]})"]
    return []


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sinh/nghiệm thu HOOK_TAP.md — file hook text giao cho "
                                             "dự án tiêu đề + máy 2")
    ap.add_argument("--slug", required=True, help="thư mục tập")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--ghi-de", action="store_true", help="viết lại file đã có (XOÁ phần viết tay)")
    ap.add_argument("--kiem", action="store_true", help="chỉ nghiệm thu, không sinh")
    a = ap.parse_args(argv)
    if a.kiem:
        loi = kiem(a.slug)
        for x in loi:
            print("  ✗", x)
        print("=== HOOK_TAP:", "FAIL" if loi else "PASS")
        return 1 if loi else 0
    out, canh = sinh(a.slug, a.profile, ghi_de=a.ghi_de)
    for x in canh:
        print("  ⚠", x)
    loi = kiem(a.slug)
    for x in loi:
        print("  ✗", x)
    print(f"=== {out}")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
