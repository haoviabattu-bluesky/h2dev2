"""srt_from_script.py — SỬA phụ đề cho KHỚP KỊCH BẢN (không phải STT nghe lại).

Vì sao: OpenSpeaker sinh voice.srt bằng cách STT NGHE LẠI audio → sai vài chỗ đồng âm
(他人様→しとぎ様, 満州→銃で, 灯→智仁...). Audio đọc ĐÚNG (đọc từ script) nhưng phụ đề cháy bị
sai chữ. Đây là lỗi câm ảnh hưởng MỌI video (đo thật youyoin 2026-09-08).

Cách chắc: GIỮ NGUYÊN timestamp của mỗi cue SRT (căn theo audio) nhưng THAY nội dung bằng đúng
đoạn tương ứng trong script — dò bằng difflib (STT ≈ script ~95%) rồi ánh xạ vị trí cue → vị trí
script. Kết quả: phụ đề = chữ script chính xác, timestamp vẫn khớp giọng.

Dùng:
  py -3.13 srt_from_script.py --srt <slug>/voice.srt --script <slug>/script.txt   # ghi đè (backup .stt.srt)
  py -3.13 srt_from_script.py --srt voice.srt --script script.txt --out voice_fix.srt
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

_TS = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d+)\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d+)")


def parse_srt(txt):
    """→ [(start_str, end_str, text)]. Giữ nguyên chuỗi timestamp gốc."""
    cues = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = block.splitlines()
        ts_line = next((l for l in lines if "-->" in l), None)
        if not ts_line:
            continue
        i = lines.index(ts_line)
        body = "".join(lines[i + 1:]).strip()
        a, b = [s.strip() for s in ts_line.split("-->")]
        cues.append((a, b, body))
    return cues


def _norm(s):
    """Bỏ mọi khoảng trắng/xuống dòng để ánh xạ theo ký tự nội dung."""
    return re.sub(r"\s+", "", s)


def reflow(cues, script):
    """Trả cues mới với text lấy từ script theo ánh xạ difflib. Timestamp giữ nguyên."""
    stt_parts = [_norm(c[2]) for c in cues]
    stt = "".join(stt_parts)
    scr = _norm(script)
    # ánh xạ từng vị trí trong stt -> vị trí trong scr (dài len(stt)+1, gồm mốc cuối)
    m = [0] * (len(stt) + 1)
    sm = difflib.SequenceMatcher(None, stt, scr, autojunk=False)
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(a2 - a1):
                m[a1 + k] = b1 + k
        elif tag == "replace":
            span = max(1, a2 - a1)
            for k in range(a2 - a1):
                m[a1 + k] = b1 + round(k * (b2 - b1) / span)
        elif tag == "delete":          # stt có, script không → dồn về b1
            for k in range(a2 - a1):
                m[a1 + k] = b1
        # insert: không có vị trí stt; ký tự script chèn sẽ được gộp qua mốc cue kế
    m[len(stt)] = len(scr)

    # mốc cue theo offset ký tự trong stt
    offs, acc = [], 0
    for p in stt_parts:
        offs.append(acc)
        acc += len(p)
    offs.append(len(stt))

    out = []
    for i, (a, b, _) in enumerate(cues):
        s0 = m[offs[i]]
        s1 = m[offs[i + 1]]
        if s1 < s0:
            s1 = s0
        out.append((a, b, scr[s0:s1]))
    # cue cuối nuốt phần script dư (nếu có)
    if out and out[-1][2] != scr[m[offs[-2]]:]:
        a, b, _ = cues[-1]
        out[-1] = (a, b, scr[m[offs[-2]]:])
    return out


def to_srt(cues):
    blocks = []
    for i, (a, b, text) in enumerate(cues, 1):
        blocks.append(f"{i}\n{a} --> {b}\n{text}")
    return "\n\n".join(blocks) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", default="", help="mặc định: ghi đè --srt (backup .stt.srt)")
    args = ap.parse_args()

    srt_path = Path(args.srt)
    cues = parse_srt(srt_path.read_text(encoding="utf-8"))
    script = Path(args.script).read_text(encoding="utf-8")
    new = reflow(cues, script)

    # đo tỉ lệ cue bị đổi
    old_txt = [_norm(c[2]) for c in cues]
    new_txt = [_norm(c[2]) for c in new]
    changed = sum(1 for a, b in zip(old_txt, new_txt) if a != b)
    cov = sum(len(t) for t in new_txt) / max(1, len(_norm(script)))
    print(f"cues: {len(new)} | sửa: {changed} ({changed/max(1,len(new)):.0%}) | phủ script: {cov:.1%}")

    out_path = Path(args.out) if args.out else srt_path
    if not args.out:
        bak = srt_path.with_suffix(".stt.srt")
        if not bak.exists():
            bak.write_text(srt_path.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"backup STT gốc → {bak.name}")
    out_path.write_text(to_srt(new), encoding="utf-8")
    print(f"✓ {out_path}")


if __name__ == "__main__":
    main()
