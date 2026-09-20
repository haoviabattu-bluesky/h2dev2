"""Đo phân bố thời lượng ảnh từ anchors.txt — mô phỏng đúng assemble.anchor_durations.

Dùng cho việc kiểm tra xem anchors có tấm nào đứng quá lâu (>30s) hoặc quá ngắn (<3s).
Chỉ đọc, không ghi gì.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def parse_srt(p):
    cues = []
    for blk in Path(p).read_text(encoding="utf-8").split("\n\n"):
        blk = blk.strip()
        if not blk:
            continue
        lines = blk.splitlines()
        if len(lines) < 2:
            continue
        t = lines[1]
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", t)
        if not m:
            continue
        h, mi, s, ms = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        start = h * 3600 + mi * 60 + s + ms / 1000
        txt = " ".join(lines[2:]).strip()
        cues.append((start, txt))
    return cues


def anchor_durations(anchor_map, img_names, audio_len, srt_cues):
    full, spans, pos = [], [], 0
    for _, txt in srt_cues:
        spans.append((pos, len(spans)))
        full.append(txt)
        pos += len(txt)
    full_text = "".join(full)

    starts, tim_tu = [], 0
    for name in img_names:
        neo = anchor_map.get(name)
        if neo is None:
            raise SystemExit(f"thieu neo {name}")
        idx = full_text.find(neo, tim_tu)
        if idx == -1:
            idx = full_text.find(neo)
            if idx == -1:
                raise SystemExit(f"khong tim thay neo {name}: {neo[:40]!r}")
        cue_i = 0
        for start_ch, ci in spans:
            if start_ch <= idx:
                cue_i = ci
            else:
                break
        starts.append(srt_cues[cue_i][0])
        tim_tu = idx + len(neo)
    starts.append(audio_len)
    durs = [starts[i + 1] - starts[i] for i in range(len(img_names))]
    xau = [(img_names[i].name, round(d, 1)) for i, d in enumerate(durs) if d < 1.0]
    if xau:
        raise SystemExit(f"neo <1s: {xau}")
    return durs


def main(slug):
    S = Path(slug)
    anchors = {}
    for ln in (S / "anchors.txt").read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "|" not in ln:
            continue
        n, neo = ln.split("|", 1)
        anchors[n.strip()] = neo.strip()

    img_names = sorted((S / "img").glob("*.png"), key=lambda p: int(p.stem))
    cues = parse_srt(S / "voice_paced.srt")
    audio_len = cues[-1][0] + 10 if cues else 0
    durs = anchor_durations(anchors, [p.name for p in img_names], audio_len, cues)

    ds = sorted(durs)
    n = len(ds)
    nho = [f"{img_names[i].name} {durs[i]:.1f}s" for i, d in enumerate(durs) if d < 3.0]
    lon = sorted(((durs[i], img_names[i].name) for i in range(n)), reverse=True)[:10]

    print(f"=== {slug.split(chr(92))[-1]}: {n} anh, audio {audio_len:.0f}s ===")
    print(f"  ngan nhat : {ds[0]:.1f}s  ({img_names[durs.index(ds[0])].name})")
    print(f"  trung vi  : {ds[n//2]:.1f}s")
    print(f"  dai nhat  : {ds[-1]:.1f}s  ({img_names[durs.index(ds[-1])].name})")
    print(f"  anh < 3s  : {sum(1 for d in durs if d < 3)}/{n}  {nho[:8]}")
    print(f"  anh > 30s : {sum(1 for d in durs if d > 30)}/{n}")
    tong_lon = sum(d for d, _ in lon[:10])
    print(f"  10 anh lau nhat chiem {tong_lon:.1f}s / {audio_len:.0f}s  ({(tong_lon/audio_len*100):.0f}%)")
    print("  10 lau nhat:")
    for d, name in lon:
        print(f"    {name}  {d:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
