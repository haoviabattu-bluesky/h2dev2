# -*- coding: utf-8 -*-
"""Lane F (teinengo-real) — dựng hook_timeline.json + grok_jobs.csv chuẩn cho 1 tập, sau khi đã có
hook_storyboard.json (hook_storyboard.py) + hook_voice.mp3/.srt (tts.py) — viết 2026-09-30 từ ep06.

Vì sao có tool này: hook_storyboard.py ghi grok_jobs.csv với id `shot_NN` + đường dẫn ảnh TƯƠNG ĐỐI, còn
tools/hook_lane_g/grok_1tk.py lại cần id `clip_NN` + ảnh `img/NNN.png` tuyệt đối (lệch là mở profile Grok,
không thấy ảnh → khoá oan tài khoản 24h — dính thật ep05). Và hook_timeline.json phải cắt theo RANH GIỚI CÂU
thật của hook_voice.srt, không theo giây storyboard ước lượng.

    py -3.13 -X utf8 dung_file_hook.py <thư mục tập> --nhom "1-2,3,4-6,7-9,10-11,12,13"

--nhom: mỗi cảnh storyboard = 1 dải số CUE trong hook_voice.srt (đọc srt rồi tự chia, cảnh nào cũng phải
kết thúc ở cue cuối câu). Số dải PHẢI = số shot trong hook_storyboard.json.
Tuỳ chọn --ky-vong <file.json> = {"3": "kỳ vọng tiếng Việt"...} để ghi đè `visual` của storyboard.
Không sinh ảnh, không gọi mạng. Ra: hook/hook_timeline.json · hook/grok_jobs.csv (bản cũ giữ .bak_storyboard).
SFX (`sfx`, `nen`) thêm sau bằng tay/tool khác — tool này giữ nguyên nếu timeline cũ đã có.
"""
import argparse, csv, json, re
from pathlib import Path


def doc_srt(p):
    cues = []
    for blk in re.split(r"\n\s*\n", p.read_text(encoding="utf-8-sig").strip()):
        ln = blk.strip().splitlines()
        a, b = ln[1].split(" --> ")
        f = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + float(s[6:].replace(",", "."))
        cues.append((f(a), f(b), "".join(ln[2:])))
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tap")
    ap.add_argument("--nhom", required=True)
    ap.add_argument("--ky-vong", default="")
    a = ap.parse_args()
    d = Path(a.tap).resolve(); H = d / "hook"
    sb = json.loads((H / "hook_storyboard.json").read_text(encoding="utf-8"))["shots"]
    cues = doc_srt(H / "hook_voice.srt")
    nhom = []
    for part in a.nhom.split(","):
        x, _, y = part.strip().partition("-")
        nhom.append((int(x), int(y or x)))
    if len(nhom) != len(sb):
        raise SystemExit(f"✗ --nhom có {len(nhom)} dải nhưng storyboard có {len(sb)} shot")
    if nhom[0][0] != 1 or nhom[-1][1] != len(cues) or any(nhom[i + 1][0] != nhom[i][1] + 1 for i in range(len(nhom) - 1)):
        raise SystemExit(f"✗ --nhom phải phủ liền mạch cue 1..{len(cues)} (srt có {len(cues)} cue)")
    kv = json.loads(Path(a.ky_vong).read_text(encoding="utf-8")) if a.ky_vong else {}
    locked = (H / "hook_locked.txt").read_text(encoding="utf-8")
    bounds = [0.0]
    for k in range(len(nhom) - 1):
        bounds.append(round((cues[nhom[k][1] - 1][1] + cues[nhom[k + 1][0] - 1][0]) / 2, 3))
    bounds.append(round(cues[-1][1] + 0.4, 3))
    shots = []
    for i, s in enumerate(sb):
        n = i + 1
        v = s.get("voice", "")
        if v and v not in locked:
            print(f"  ! shot {n}: voice storyboard không nằm nguyên văn trong hook_locked.txt — kiểm lại: {v}")
        dai = bounds[i + 1] - bounds[i]
        if dai > 6.5:
            print(f"  ! shot {n} dài {dai:.1f}s > clip Grok 6s — máy 2 sẽ giãn chậm (chấp nhận được tới ~8s)")
        shots.append({"n": n, "t0": bounds[i], "t1": bounds[i + 1], "voice": v, "img": f"img/{n:03d}.png",
                      "clip": f"clip/clip_{n:02d}.mp4", "ky_vong": kv.get(str(n)) or s.get("visual", "")})
    cu = {}
    if (H / "hook_timeline.json").exists():
        cu = json.loads((H / "hook_timeline.json").read_text(encoding="utf-8"))
    tl = {"_doc": "mốc = giữa 2 cue hook_voice.srt (ranh giới câu). Lane F 1 giọng → mốc GIÂY (KHÔNG dùng 'cau').",
          "hook_voice_end_s": round(cues[-1][1], 3), "tong_s": bounds[-1],
          "cau_ket_hook": locked.strip().splitlines()[-1].strip(), "shots": shots}
    for k in ("sfx", "nen"):
        if k in cu:
            tl[k] = cu[k]
    (H / "hook_timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    rows = list(csv.DictReader(open(H / "grok_jobs.csv", encoding="utf-8-sig")))
    bak = H / "grok_jobs.csv.bak_storyboard"
    if not bak.exists():
        bak.write_bytes((H / "grok_jobs.csv").read_bytes())
    if len(rows) != len(sb):
        raise SystemExit(f"✗ grok_jobs.csv có {len(rows)} dòng ≠ {len(sb)} shot — chạy lại hook_storyboard.py --force")
    for i, r in enumerate(rows):
        n = i + 1
        r["id"] = f"clip_{n:02d}"; r["image"] = str(H / "img" / f"{n:03d}.png"); r["duration"] = "6"
        r["prompt"] = r["prompt"].replace("face locked to @REF2", "same face as the image").replace("face locked to @REF", "same face as the image")
    with open(H / "grok_jobs.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"✓ hook_timeline.json {len(shots)} cảnh · {bounds[-1]}s · mốc {bounds}")
    print(f"✓ grok_jobs.csv: id clip_NN, ảnh tuyệt đối {H / 'img'}\\NNN.png, 6s")


if __name__ == "__main__":
    main()
