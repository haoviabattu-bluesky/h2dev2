# -*- coding: utf-8 -*-
"""ban_xem_viet.py — BẢN XEM THỬ có phụ đề TIẾNG VIỆT, để chủ dự án soi nội dung.

    py -3.13 ban_xem_viet.py --slug <thư mục tập> --profile <lane>

Ra trong thư mục tập:  `voice.vi.srt` (phụ đề Việt) + `review_vi.mp4` (bản nhẹ, chữ cháy vào hình).

VÌ SAO CÓ FILE NÀY
------------------------------------------------------------------------------------------------
Bản đăng lên YouTube **không cháy phụ đề** (anh chốt 2026-09-11) và toàn bộ lời là tiếng Nhật —
nghĩa là không ai bên mình xem lại được nội dung thật sự nói gì. Cổng B3F chỉ trả lời "chi tiết này
có trong tư liệu không", không trả lời "đoạn này nghe có xuôi không, có đúng ý mình định kể không".
Bản xem thử này lấp đúng khoảng đó: một lần xem là biết video khớp hay lệch.

BA QUYẾT ĐỊNH CÓ CHỦ Ý
  1. **Độ phân giải thấp (854×480, crf 30)**: đây là bản để ĐỌC, không phải để đăng. Bản 1080p
     nặng ~1 GB mỗi tập, nhân với mỗi lần dựng lại là ổ cứng đầy vì một thứ xem xong thì bỏ.
     480p ra ~60–90 MB mà chữ vẫn đọc rõ.
  2. **Dịch từ chính file .srt đã bám kịch bản** (`voice.srt` sau bước B4a), không dịch từ kịch bản
     gốc: mốc thời gian phải khớp với tiếng đang phát, nếu không thì xem để đối chiếu làm gì.
  3. **Lưu lại `voice.vi.srt`**: dịch lại mỗi lần là vừa tốn vừa cho ra chữ khác nhau giữa các
     lần, không so sánh được. Muốn dịch lại thì xoá file đó hoặc chạy `--dich-lai`.
"""
import argparse
import os
import re
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent

from assemble import FF

LO_MOI = 40          # số cue dịch mỗi lượt gọi model


def doc_srt(f: Path):
    """[(số, dòng thời gian, lời)] — giữ nguyên khối thời gian, chỉ thay phần lời."""
    ra = []
    for khoi in re.split(r"\n\s*\n", f.read_text(encoding="utf-8").strip()):
        d = [x for x in khoi.splitlines() if x.strip()]
        if len(d) < 2 or "-->" not in d[1]:
            continue
        ra.append((d[0].strip(), d[1].strip(), " ".join(d[2:]).strip()))
    return ra


def dich_lo(loi: list[str]) -> list[str]:
    """Dịch một lô lời sang tiếng Việt, giữ ĐÚNG số dòng."""
    from llm_client import chat
    danh = "\n".join(f"{i+1}. {t}" for i, t in enumerate(loi))
    ask = ("Dịch các dòng phụ đề tiếng Nhật dưới đây sang TIẾNG VIỆT.\n"
           "LUẬT CỨNG:\n"
           f"· Trả ĐÚNG {len(loi)} dòng, đánh số y hệt đầu vào (1. 2. 3. …). Không gộp, không tách.\n"
           "· Mỗi dòng là một mảnh câu bị cắt giữa chừng — DỊCH ĐÚNG MẢNH ĐÓ, đừng tự nối cho "
           "thành câu hoàn chỉnh, đừng thêm chữ không có.\n"
           "· Văn kể tài liệu, gọn, không hoa mỹ. Giữ nguyên số liệu, năm, tên riêng.\n"
           "· Không thêm lời bình, không giải thích.\n\n" + danh)
    kq = chat(ask, task="short", max_tokens=8000, temperature=0.2, verbose=False)
    text = getattr(kq, "text", None) or str(kq)
    ra = {}
    for d in text.splitlines():
        m = re.match(r"\s*(\d+)\s*[.)．]\s*(.+)", d.strip())
        if m:
            ra[int(m.group(1))] = m.group(2).strip()
    # Dòng nào model bỏ sót thì GIỮ NGUYÊN tiếng Nhật — thà lẫn một dòng Nhật còn hơn lệch số dòng
    # làm mọi phụ đề phía sau chạy sai mốc thời gian.
    return [ra.get(i + 1, loi[i]) for i in range(len(loi))]


def dich_srt(nguon: Path, dich: Path, lam_lai=False):
    # ⚠️ BẢN DỊCH CŨ HƠN PHỤ ĐỀ GỐC = BẢN DỊCH CỦA MỘT FILE TIẾNG KHÁC.
    # Cache ở đây vốn chỉ so "file có tồn tại không" — nên khi thu lại giọng (đổi mở đầu, đổi
    # nhịp) thì `voice.vi.srt` cũ vẫn được dùng lại, và bản xem thử hiện phụ đề của BẢN GHI CŨ
    # trên hình của BẢN MỚI. Đã dính thật ở ep01-valentich: giọng thu lại 17:47 ngày 11, bản dịch
    # từ 09:45 — lệch cả mốc thời gian lẫn nội dung mở đầu. Mà đây đúng là file dùng để soi
    # "hình có khớp lời không", nên sai ở đây là sai đúng chỗ nguy hiểm nhất: nó không báo lỗi,
    # chỉ làm người xem kết luận nhầm.
    if dich.exists() and dich.stat().st_size > 100 and not lam_lai:
        if dich.stat().st_mtime < nguon.stat().st_mtime - 1:
            print(f"  ⚠️ {dich.name} CŨ HƠN {nguon.name} → dịch lại (giọng đã thu lại sau đó)")
        else:
            print(f"  · đã có {dich.name}, dùng lại (muốn dịch lại: --dich-lai)")
            return dich
    cues = doc_srt(nguon)
    print(f"  dịch {len(cues)} dòng phụ đề …")
    loi = [c[2] for c in cues]
    ra = []
    for i in range(0, len(loi), LO_MOI):
        lo = loi[i:i + LO_MOI]
        ra += dich_lo(lo)
        print(f"    {min(i + LO_MOI, len(loi))}/{len(loi)}")
    assert len(ra) == len(cues)
    dich.write_text("\n\n".join(f"{c[0]}\n{c[1]}\n{t}" for c, t in zip(cues, ra)) + "\n",
                    encoding="utf-8")
    return dich


def chay_chu(slug: Path, srt_vi: Path, out: Path, jobs=0):
    """Cháy phụ đề Việt lên bản 480p.

    ⚠️ Bộ lọc `subtitles=` của ffmpeg hiểu dấu `:` là dấu ngăn tham số, nên đường dẫn Windows kiểu
    `E:\\...` làm nó hiểu nhầm và báo lỗi khó hiểu (cùng một bẫy đã làm `drawtext` không dùng được
    trên máy này). Cách chắc ăn: **chạy ffmpeg NGAY TRONG thư mục tập** rồi truyền tên file trần.
    """
    cmd = [FF, "-y", "-i", "final.mp4",
           "-vf", f"scale=854:-2,subtitles={srt_vi.name}:force_style="
                  f"'FontName=Arial,FontSize=16,Outline=2,Shadow=0,MarginV=18'",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "30",
           "-c:a", "aac", "-b:a", "96k", out.name]
    if jobs:
        cmd += ["-threads", str(jobs)]
    r = subprocess.run(cmd, cwd=str(slug), capture_output=True, text=True)
    if r.returncode != 0 or not (slug / out.name).exists():
        raise SystemExit(f"✗ cháy phụ đề Việt lỗi:\n{r.stderr[-900:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--dich-lai", action="store_true")
    ap.add_argument("--jobs", type=int, default=0)
    a = ap.parse_args()

    import profiles
    prof = profiles.load(a.profile)
    slug = Path(a.slug)
    if not slug.is_absolute():
        slug = ROOT / prof.get("slug_dir", "assets") / slug
    mp4 = slug / "final.mp4"
    if not mp4.exists():
        raise SystemExit(f"✗ chưa có {mp4}")
    srt = next((slug / t for t in ("voice_paced.srt", "voice.srt") if (slug / t).exists()), None)
    if srt is None:
        raise SystemExit("✗ không có file .srt để dịch")

    vi = dich_srt(srt, slug / "voice.vi.srt", a.dich_lai)
    out = slug / "review_vi.mp4"
    chay_chu(slug, vi, out, a.jobs)
    print(f"✓ bản xem thử tiếng Việt: {out} ({out.stat().st_size/1024/1024:.0f} MB)")


if __name__ == "__main__":
    main()
