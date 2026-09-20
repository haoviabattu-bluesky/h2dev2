"""Bản xem duyệt CÓ PHỤ ĐỀ TIẾNG VIỆT — để anh soát nội dung tập có khớp ý không.

User chốt 2026-09-11: video giao đi **KHÔNG cháy phụ đề** (YouTube tự bật CC từ file .srt up kèm;
khán giả Nhật nghe hiểu, chữ cháy chỉ che hình). Nhưng mỗi tập cần THÊM một bản `final_vi.mp4` có
phụ đề TIẾNG VIỆT cháy vào hình, chỉ dùng để duyệt nội bộ — KHÔNG đăng.

  py -3.13 sub_vi.py --slug <thư mục tập> --profile satori-jp-obaa

Ra: `voice_vi.srt` (bản dịch) + `final_vi.mp4` (bản duyệt). Cả hai đều resume được.

CHỐT AN TOÀN: số cue dịch ra PHẢI khớp đúng số cue gốc — lệch một dòng là phụ đề trôi lệch giờ suốt
phần còn lại mà nhìn vẫn "có vẻ chạy". Lô nào lệch thì tự chia đôi dịch lại, vẫn lệch thì giữ
nguyên câu gốc cho lô đó (thà sót tiếng Nhật còn hơn sai giờ).
"""
import argparse
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


def _mmss(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def ghi_srt(cues, path):
    out = []
    for i, (a, b, txt) in enumerate(cues, 1):
        out.append(f"{i}\n{_mmss(a)} --> {_mmss(b)}\n{txt}\n")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def dich_lo(loi, on_line=print, sau=0):
    """Dịch một lô câu → list cùng độ dài. Lệch số dòng thì tự chia đôi; hết cách thì trả bản gốc."""
    import ai_steps

    n = len(loi)
    if n == 0:
        return []
    danh_sach = "\n".join(f"{i+1}. {t}" for i, t in enumerate(loi))
    prompt = (
        f"Dịch {n} dòng phụ đề sau sang TIẾNG VIỆT tự nhiên, giọng kể chuyện tâm tình.\n"
        f"QUY TẮC BẮT BUỘC:\n"
        f"  - Trả về ĐÚNG {n} dòng, đánh số 1..{n} y như đầu vào. Không gộp, không tách, không bỏ dòng.\n"
        f"  - Mỗi dòng dịch nghĩa của ĐÚNG dòng cùng số thứ tự.\n"
        f"  - Không thêm lời giải thích, không thêm ghi chú. Chỉ trả danh sách đánh số.\n\n"
        f"{danh_sach}"
    )
    try:
        r = ai_steps.chat(prompt, task="script", temperature=0.3, verbose=False)
        raw = r.text
    except Exception as e:
        on_line(f"    lô {n} câu: lỗi gọi LLM ({type(e).__name__}) → giữ nguyên tiếng Nhật")
        return list(loi)

    ra = {}
    for dong in raw.splitlines():
        m = re.match(r"\s*(\d+)\s*[.)、]\s*(.+)", dong.strip())
        if m:
            ra[int(m.group(1))] = m.group(2).strip()
    if len(ra) == n and set(ra) == set(range(1, n + 1)):
        return [ra[i] for i in range(1, n + 1)]

    on_line(f"    lô {n} câu: LLM trả {len(ra)}/{n} dòng → chia đôi dịch lại")
    if n <= 2 or sau >= 3:
        return list(loi)
    giua = n // 2
    return (dich_lo(loi[:giua], on_line, sau + 1) + dich_lo(loi[giua:], on_line, sau + 1))


def main():
    _ensure_std()
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", default="")
    ap.add_argument("--srt", default="")
    ap.add_argument("--mp4", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--lo", type=int, default=40, help="số cue mỗi lượt gọi LLM")
    ap.add_argument("--font", default="Yu Gothic")
    a = ap.parse_args()

    T0 = time.perf_counter()
    S = Path(a.slug)
    srt = Path(a.srt) if a.srt else (S / "voice_paced.srt" if (S / "voice_paced.srt").exists()
                                     else S / "voice.srt")
    mp4 = Path(a.mp4) if a.mp4 else S / "final.mp4"
    out = Path(a.out) if a.out else S / "final_vi.mp4"
    srt_vi = S / "voice_vi.srt"

    if not srt.exists():
        print(f"✗ không có phụ đề nguồn: {srt}")
        return 1
    if not mp4.exists():
        print(f"✗ chưa có video: {mp4}")
        return 1

    import storyboard as sb
    cues = sb.parse_cues(srt)
    if not cues:
        print(f"✗ {srt.name} rỗng")
        return 1
    print(f"=== BẢN DUYỆT PHỤ ĐỀ VIỆT: {S.name} ({len(cues)} cue) ===")

    # 1) dịch (resume: đã có bản dịch đúng số cue thì dùng lại)
    cu = sb.parse_cues(srt_vi) if srt_vi.exists() else []
    if len(cu) == len(cues):
        print(f"  ⏭ đã có {srt_vi.name} khớp {len(cu)} cue — bỏ qua dịch")
        vi = [c[2] for c in cu]
    else:
        loi = [c[2] for c in cues]
        vi, t0 = [], time.perf_counter()
        for i in range(0, len(loi), a.lo):
            lo = loi[i:i + a.lo]
            vi += dich_lo(lo)
            print(f"  dịch {min(i+a.lo, len(loi))}/{len(loi)} cue", flush=True)
        assert len(vi) == len(cues), f"lệch cue: {len(vi)} vs {len(cues)}"
        ghi_srt([(c[0], c[1], t) for c, t in zip(cues, vi)], srt_vi)
        print(f"  ✓ {srt_vi.name} ({(time.perf_counter()-t0)/60:.1f} phút)")

    # 2) cháy phụ đề Việt lên bản final.mp4 đã dựng (chỉ encode lại video, giữ nguyên tiếng)
    t0 = time.perf_counter()
    from assemble import FF
    style = (f"FontName={a.font},FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
             f"BorderStyle=1,Outline=2,Shadow=1,MarginV=45,Alignment=2")
    # ffmpeg trên Windows: đường dẫn trong filter phải là tương đối + chạy trong thư mục đó,
    # không thì dấu ':' của ổ đĩa bị hiểu là dấu phân cách tham số filter.
    cmd = [FF, "-y", "-i", str(mp4.resolve()),
           "-vf", f"subtitles={srt_vi.name}:force_style='{style}'",
           "-c:a", "copy", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-pix_fmt", "yuv420p", str(out.resolve())]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=str(S))
    if r.returncode != 0 or not out.exists():
        print("✗ ffmpeg cháy phụ đề lỗi:\n" + (r.stderr or "")[-1200:])
        return 1
    print(f"  ✓ {out.name} ({out.stat().st_size/1e6:.0f} MB · {(time.perf_counter()-t0)/60:.1f} phút)")
    print(f"=== XONG · tổng {(time.perf_counter()-T0)/60:.1f} phút ===")
    print(f"   BẢN ĐĂNG    : {mp4}   (không cháy phụ đề — up kèm {srt.name} làm CC)")
    print(f"   BẢN DUYỆT VI: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
