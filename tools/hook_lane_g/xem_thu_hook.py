# -*- coding: utf-8 -*-
"""Ghép BẢN XEM THỬ hook (clip Grok + SFX + phụ đề Việt/Nhật) cho ANH KIỂM — KHÔNG phải hàng giao máy 2.

Máy 1 không lồng giọng hook (máy 2 làm) → bản này KHÔNG có giọng đọc; thời lượng mỗi shot ước theo
char_rate của profile (số chữ câu ÷ char_rate × 60 + 0,35s nghỉ), clip ngắn hơn thì giữ khung cuối.
Phụ đề: dòng Nhật (nguyên văn câu) + dòng Việt (dịch, lấy từ <hook>/phu_de_vi.json {"<số câu>": "câu dịch"}).

    py -3.13 -X utf8 xem_thu_hook.py --profile <lane> --hook <thư mục hook>
→ <thư mục tập>/XEM_THU_hook_phude_VI.mp4 (ngoài thư mục hook để dong_goi_may2 không gửi nhầm sang máy 2)
"""
import argparse, json, subprocess, sys, textwrap
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1280, 720
F_VI = r"C:\Windows\Fonts\arialbd.ttf"
F_JA = r"C:\Windows\Fonts\YuGothB.ttc"


def ff(*a):
    r = subprocess.run([FF, "-y", "-v", "error", *map(str, a)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit("ffmpeg lỗi: " + r.stderr[-800:])


def overlay(png, ja, vi):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fj, fv = ImageFont.truetype(F_JA, 26), ImageFont.truetype(F_VI, 34)
    ja_l = textwrap.wrap(ja, 40) or [""]
    vi_l = textwrap.wrap(vi, 60) or [""]
    lh_j, lh_v = 36, 44
    box_h = 24 + lh_j * len(ja_l) + 8 + lh_v * len(vi_l)
    y = H - box_h - 20
    d.rectangle([40, y, W - 40, H - 20], fill=(0, 0, 0, 165))
    y += 12
    for s in ja_l:
        d.text((W // 2, y), s, font=fj, fill=(255, 225, 120, 255), anchor="ma"); y += lh_j
    y += 8
    for s in vi_l:
        d.text((W // 2, y), s, font=fv, fill=(255, 255, 255, 255), anchor="ma", stroke_width=2, stroke_fill=(0, 0, 0, 255)); y += lh_v
    im.save(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--hook", required=True)
    a = ap.parse_args()
    hd = Path(a.hook)
    prof = json.loads((ROOT / "profiles" / "profiles" / f"{a.profile}.json").read_text(encoding="utf-8"))
    rate = float(prof["voice"]["char_rate"])
    tl = json.loads((hd / "hook_timeline.json").read_text(encoding="utf-8"))
    vi = json.loads((hd / "phu_de_vi.json").read_text(encoding="utf-8"))
    tmp = hd / "_xem_thu"; tmp.mkdir(exist_ok=True)
    segs, starts, t = [], {}, 0.0
    for s in tl["shots"]:
        n = s["n"]
        dur = max(2.2, len(s["voice"]) / rate * 60 + 0.35)
        starts[s["cau"][0]] = t
        png = tmp / f"sub_{n:02d}.png"
        overlay(png, s["voice"], vi.get(str(s["cau"][0]), "(chưa dịch)"))
        seg = tmp / f"seg_{n:02d}.mp4"
        ff("-i", hd / s["clip"], "-i", png, "-filter_complex",
           f"[0:v]scale={W}:{H},setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=10[v];[v][1:v]overlay=0:0",
           "-t", f"{dur:.2f}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", seg)
        segs.append(seg); t += dur
        print(f"shot {n} · câu {s['cau']} · {dur:.1f}s")
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    video = tmp / "video.mp4"
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video)
    # âm thanh: SFX theo câu + nền (lặp, nhỏ, tắt dần)
    ins, fl, k = ["-i", video], [], 1
    for x in []:   # 01/10/2026: cấm SFX đồ vật mọi lane — chỉ nhạc nền `nen` (docs/QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md)
        st = starts.get(x["cau"], 0.0) + float(x.get("lech", 0))
        ins += ["-i", hd / x["file"]]
        fl.append(f"[{k}:a]volume={x.get('vol', 0.5)},adelay={int(st * 1000)}:all=1[a{k}]"); k += 1
    nen = tl.get("nen")
    if nen:
        ins += ["-stream_loop", "-1", "-i", hd / nen["file"]]
        fo = float(nen.get("fade_out_s", 1.5))
        fl.append(f"[{k}:a]volume={nen.get('vol', 0.2)},atrim=0:{t:.2f},afade=t=out:st={max(0, t - fo):.2f}:d={fo}[a{k}]"); k += 1
    out = hd.parent / "XEM_THU_hook_phude_VI.mp4"
    if k == 1:
        ff("-i", video, "-c", "copy", out)
    else:
        mix = "".join(f"[a{i}]" for i in range(1, k)) + f"amix=inputs={k - 1}:normalize=0:duration=longest,atrim=0:{t:.2f}[a]"
        ff(*ins, "-filter_complex", ";".join(fl + [mix]), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out)
    import shutil; shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ {out} · {t:.1f}s")


if __name__ == "__main__":
    main()
