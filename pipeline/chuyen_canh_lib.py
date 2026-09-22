"""chuyen_canh_lib.py — phần dùng chung của 3 script trong skill video-chuyen-canh.

Mọi mốc thời gian trong đây tính bằng SỐ KHUNG (int), không bao giờ bằng giây thập phân.
Giây chỉ xuất hiện đúng lúc phải ghi vào tham số ffmpeg (duration của xfade), và luôn quy đổi
từ số khung: f / fps.
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------- ffmpeg ---------------------

def find_ffmpeg():
    """imageio_ffmpeg trước (máy này có sẵn qua pip), rồi tới PATH."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    p = shutil.which("ffmpeg")
    if not p:
        raise SystemExit("Không tìm thấy ffmpeg (pip install imageio-ffmpeg hoặc thêm vào PATH)")
    return p


FF = find_ffmpeg()


def run_ff(args, desc=""):
    r = subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error"] + [str(a) for a in args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg lỗi {desc}:\n{r.stderr[-3000:]}")
    return r


def media_info(path):
    """(fps, w, h, dur_giây_luồng_hình, dur_giây_container). Đọc từ banner `ffmpeg -i`."""
    r = subprocess.run([FF, "-hide_banner", "-i", str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    err = r.stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", err)
    dur = None
    if m:
        h, mn, s = m.groups()
        dur = int(h) * 3600 + int(mn) * 60 + float(s)
    fps = w = hh = None
    for line in err.splitlines():
        if "Video:" in line:
            m2 = re.search(r"(\d+(?:\.\d+)?) fps", line)
            if m2:
                fps = float(m2.group(1))
            m3 = re.search(r" (\d{2,5})x(\d{2,5})[ ,]", line)
            if m3:
                w, hh = int(m3.group(1)), int(m3.group(2))
            break
    return fps, w, hh, dur


def count_video_frames(path):
    """Đếm khung của luồng hình bằng cách demux (không decode) — nhanh, và KHÔNG dựa vào
    format=duration (bẫy #1 trong SKILL.md: nó trả về luồng dài nhất, có thể là audio)."""
    r = subprocess.run([FF, "-hide_banner", "-i", str(path), "-map", "0:v:0", "-c", "copy",
                        "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    ms = re.findall(r"frame=\s*(\d+)", r.stderr)
    if not ms:
        raise SystemExit(f"Không đếm được khung: {path}\n{r.stderr[-1500:]}")
    return int(ms[-1])


def audio_seconds(path):
    _, _, _, dur = media_info(path)
    if dur is None:
        raise SystemExit(f"Không đọc được độ dài audio: {path}")
    return dur


# ---------------------------------------------------------------- kế hoạch ranh giới ---------

LOAI = ("cut", "xfade", "zoomblack", "push", "blurin")


def doc_timeline(csv_path, fps):
    """timeline.csv: STT_ANH,BAT_DAU,KET_THUC,THOI_LUONG_S (có header, phân cách , hoặc ;).
    Trả (keys, frames_moi_canh, tong_khung). Ranh giới = round(BAT_DAU * fps); cảnh cuối
    kết thúc ở round(KET_THUC * fps). Tổng khung = tổng các cảnh, đúng bằng KET_THUC cuối."""
    txt = Path(csv_path).read_text(encoding="utf-8-sig")
    rows = []
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        sep = ";" if line.count(";") > line.count(",") else ","
        cols = [c.strip().strip('"') for c in line.split(sep)]
        rows.append(cols)
    if not rows:
        raise SystemExit(f"timeline rỗng: {csv_path}")
    hdr = [c.upper() for c in rows[0]]
    def col(name, default):
        return hdr.index(name) if name in hdr else default
    i_stt, i_bd, i_kt = col("STT_ANH", 0), col("BAT_DAU", 1), col("KET_THUC", 2)
    body = rows[1:] if any(not _is_num(c) for c in rows[0][1:3]) else rows
    keys, starts, ends = [], [], []
    for cols in body:
        keys.append(cols[i_stt])
        starts.append(_to_sec(cols[i_bd]))
        ends.append(_to_sec(cols[i_kt]))
    sf = [int(round(s * fps)) for s in starts]
    end_last = int(round(ends[-1] * fps))
    frames = [sf[i + 1] - sf[i] for i in range(len(sf) - 1)] + [end_last - sf[-1]]
    bad = [(k, f) for k, f in zip(keys, frames) if f <= 0]
    if bad:
        raise SystemExit(f"timeline có cảnh ≤0 khung (BAT_DAU không tăng dần?): {bad[:5]}")
    return keys, frames, sum(frames)


def _is_num(s):
    try:
        float(s.replace(":", ""))
        return True
    except ValueError:
        return False


def _to_sec(s):
    """'12.5' | '00:01:23.400' | '1:23.4' → giây."""
    s = s.strip()
    if ":" in s:
        parts = s.split(":")
        sec = 0.0
        for p in parts:
            sec = sec * 60 + float(p.replace(",", "."))
        return sec
    return float(s.replace(",", "."))


def ghep_key_voi_anh(keys, imgs):
    """STT_ANH có thể là tên file, hoặc số thứ tự (0- hay 1-based tuỳ số nhỏ nhất)."""
    by_name = {p.name: p for p in imgs}
    by_stem = {p.stem: p for p in imgs}
    out = []
    nums = [int(k) for k in keys if k.isdigit()]
    base = min(nums) if nums else 0
    for k in keys:
        if k in by_name:
            out.append(by_name[k])
        elif k in by_stem:
            out.append(by_stem[k])
        elif k.isdigit():
            idx = int(k) - base
            if idx < 0 or idx >= len(imgs):
                raise SystemExit(f"STT_ANH={k} vượt số ảnh ({len(imgs)})")
            out.append(imgs[idx])
        else:
            raise SystemExit(f"Không ghép được STT_ANH={k!r} với ảnh nào trong thư mục")
    return out


def lap_ke_hoach(frames, fps, ratio=0.70, mix=(0.55, 0.35, 0.10, 0.0), d_xfade=15, d_black=14,
                 d_push=11, d_blur=12, seed=0, min_scene_s=1.0):
    """Sinh danh sách ranh giới (len = số cảnh - 1). Mỗi phần tử:
        {"type": cut|xfade|zoomblack|push|blurin, "d": số khung hiệu ứng, "da": phần ăn vào cảnh
         trước, "db": phần ăn vào cảnh sau, "dir": left|right (push)}
    - ratio: tỉ lệ ranh giới CÓ hiệu ứng. mix: tỉ lệ (xfade, zoomblack, push, blurin) trong phần có
      hiệu ứng (3 số cũng nhận — blurin = 0).
    - Bẫy #4: ranh giới chạm cảnh ngắn hơn min_scene_s → ép cắt thẳng.
    - xfade/push ăn vào cả 2 cảnh (da/db) nên còn phải chừa mỗi cảnh ít nhất d khung thật.
    - zoomblack / blurin chỉ ăn vào cảnh SAU (hiệu ứng VÀO), cảnh trước kết thúc gọn.
    Dùng rng có seed để lặp lại được; chọn theo "xô" (bucket) để tỉ lệ đúng dù ít ranh giới."""
    n = len(frames)
    nb = n - 1
    if nb <= 0:
        return []
    rng = random.Random(seed)
    min_f = int(round(min_scene_s * fps))
    # Ranh giới đủ điều kiện có hiệu ứng
    ok = []
    for i in range(nb):
        ok.append(frames[i] >= min_f and frames[i + 1] >= min_f)
    n_eff = int(round(ratio * nb))
    cand = [i for i in range(nb) if ok[i]]
    rng.shuffle(cand)
    chosen = set(cand[:n_eff])
    # Chia loại theo xô để tỉ lệ pha trộn đúng
    mix = tuple(mix) + (0.0,) * (4 - len(mix))
    mx, mz, mp, mb = mix[:4]
    tot = mx + mz + mp + mb
    ch = sorted(chosen)
    k_eff = len(ch)
    nx = int(round(k_eff * mx / tot))
    nz = int(round(k_eff * mz / tot))
    nb_ = int(round(k_eff * mb / tot))
    npu = max(0, k_eff - nx - nz - nb_)
    kinds = ["xfade"] * nx + ["zoomblack"] * nz + ["blurin"] * nb_ + ["push"] * npu
    rng.shuffle(kinds)
    kind_of = dict(zip(ch, kinds))
    plan = []
    push_dir = "left"
    for i in range(nb):
        t = kind_of.get(i, "cut")
        if t == "xfade":
            d = d_xfade
            da, db = d // 2, d - d // 2
            if frames[i] < d or frames[i + 1] < d:
                t = "cut"
        elif t == "push":
            d = d_push
            da, db = d // 2, d - d // 2
            if frames[i] < d or frames[i + 1] < d:
                t = "cut"
        elif t == "zoomblack":
            d = 1 + d_black
            da, db = 0, 0
            if frames[i + 1] < d + 2:
                t = "cut"
        elif t == "blurin":
            d = d_blur
            da, db = 0, 0
            if frames[i + 1] < d + 2:
                t = "cut"
        if t == "cut":
            plan.append({"type": "cut", "d": 0, "da": 0, "db": 0})
        elif t == "push":
            plan.append({"type": "push", "d": d, "da": da, "db": db, "dir": push_dir})
            push_dir = "right" if push_dir == "left" else "left"
        elif t == "zoomblack":
            plan.append({"type": "zoomblack", "d": d, "da": 0, "db": 0, "black": 1, "ramp": d_black})
        elif t == "blurin":
            plan.append({"type": "blurin", "d": d, "da": 0, "db": 0})
        else:
            plan.append({"type": "xfade", "d": d, "da": da, "db": db})
    return plan


def tom_tat_ke_hoach(plan):
    c = {k: 0 for k in LOAI}
    for b in plan:
        c[b["type"]] += 1
    nb = len(plan) or 1
    eff = nb - c["cut"]
    return (f"{nb} ranh giới: cắt {c['cut']} · crossfade {c['xfade']} · zoom-từ-đen {c['zoomblack']}"
            f" · đẩy ngang {c['push']} · mờ-vào {c['blurin']}  (có hiệu ứng {eff}/{nb} = {100*eff/nb:.0f}%)")


# ---------------------------------------------------------------- filter ffmpeg --------------

def fit_filter(fit, sw, sh):
    """Đưa ảnh về khổ sw×sh. Chép nguyên logic của h2dev/pipeline/assemble.py:
    cover (cắt viền) | blur (nền mờ, cho ảnh vuông/dọc) | pad (viền đen) | stretch (kéo méo)."""
    if fit == "stretch":
        return f"scale={sw}:{sh}:flags=lanczos"
    if fit == "pad":
        return (f"scale={sw}:{sh}:force_original_aspect_ratio=decrease:flags=lanczos,"
                f"pad={sw}:{sh}:(ow-iw)/2:(oh-ih)/2:black")
    if fit == "blur":
        return (f"split[_bg][_fg];"
                f"[_bg]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
                f"gblur=sigma=28[_bgb];"
                f"[_fg]scale={sw}:{sh}:force_original_aspect_ratio=decrease:flags=lanczos[_fgs];"
                f"[_bgb][_fgs]overlay=(W-w)/2:(H-h)/2")
    return f"scale={sw}:{sh}:force_original_aspect_ratio=increase:flags=lanczos,crop={sw}:{sh}"


def pulse_plan(n_total, fps, step=1.053, pulse_len=8, every_s=4.07, first_s=3.7, zoom_out=True,
               drift=1.01):
    """Kế hoạch 'đợt zoom' cho một cảnh n_total khung (kênh POV Hàn đo thật 2026-09-20: cảnh đứng yên,
    cứ ~4 s lại phóng/thu ~5 % trong ~8 khung — 80 % là thu nhỏ — rồi đứng tiếp; giữa các đợt chỉ trôi
    rất nhẹ). Trả dict cho zoom_expr: đợt k bắt đầu ở khung first_s + k·every_s."""
    frames = []
    t = first_s
    while int(round(t * fps)) + pulse_len < n_total - 3:
        frames.append(int(round(t * fps)))
        t += every_s
    dz = (step - 1.0) * (-1 if zoom_out else 1)
    z0 = 1.0 + len(frames) * (step - 1.0) if zoom_out else 1.0
    return {"frames": frames, "len": pulse_len, "dz": dz, "z0": z0, "drift": drift - 1.0}


def zoom_expr(z_start, z_end, n_total, f0=0, pulse=None):
    """Biểu thức z cho zoompan theo khung. Tuyến tính z_start→z_end, hoặc theo đợt (pulse) =
    z0 + dz·Σ smoothstep((f - p_k)/len) + drift·f/n. f = on + f0 (on = khung ra của zoompan)."""
    var = f"(on+{f0})"
    if pulse is None:
        if n_total <= 1:
            return f"{z_start:.6f}"
        step = (z_end - z_start) / (n_total - 1)
        return f"{z_start:.6f}+({step:.9f})*{var}"
    parts = [f"{pulse['z0']:.6f}"]
    for pk in pulse["frames"]:
        c = f"clip(({var}-{pk})/{pulse['len']},0,1)"
        parts.append(f"({pulse['dz']:.6f})*pow({c},2)*(3-2*{c})")
    if pulse.get("drift"):
        parts.append(f"({pulse['drift']:.6f})*{var}/{max(1, n_total - 1)}")
    return "+".join(parts)


def kenburns_filter(W, H, fps, n_out, z_start, z_end, f0=0, n_total=None, fit="cover", pulse=None):
    """Chuỗi filter dựng n_out khung Ken Burns từ 1 ảnh tĩnh, bắt đầu ở khung thứ f0 của
    một chuyển động dài n_total khung (để cắt cảnh thành nhiều mảnh mà zoom vẫn liền mạch).
    Zoom tuyến tính z_start→z_end theo khung, quanh tâm ảnh.
    Ảnh được đưa lên khổ W*(zmax+0.13) trước (zoompan chạy theo pixel nguyên, đưa đúng 1080p
    vào thì zoom ra ảnh mềm + pan giật — ghi chú đo thật trong assemble.py của h2dev)."""
    n_total = n_total or n_out
    zmax = max(z_start, z_end, 1.0, (pulse or {}).get("z0", 1.0) + (pulse or {}).get("drift", 0) + 0.02)
    sw, sh = int(W * (zmax + 0.13)) // 2 * 2, int(H * (zmax + 0.13)) // 2 * 2
    zexpr = zoom_expr(z_start, z_end, n_total, f0, pulse)
    return (f"{fit_filter(fit, sw, sh)},"
            f"zoompan=z='{zexpr}':d={n_out}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"s={W}x{H}:fps={fps}")


def zoomblack_filter(W, H, black=1, ramp=14, start=0.544):
    """Hiệu ứng VÀO 'zoom-từ-đen' áp lên đầu một cảnh: `black` khung đen, rồi `ramp` khung ảnh
    phóng từ start→1.0 giữa nền đen. eval=frame bắt buộc ở CẢ scale lẫn pad (SKILL.md)."""
    # ⚠️ Đo thật ffmpeg 7.1: biến `n` trong scale eval=frame đếm từ 1, còn `n` trong `enable=` của
    # drawbox đếm từ 0 (cùng một chuỗi filter!). Không bù (n-1) thì khung phóng đầu tiên đã ở
    # 0.579 thay vì 0.544 và chỉ còn 13 khung phóng. Script đo sẽ bắt được nếu ffmpeg khác đổi cách đếm.
    end = black + ramp
    k = "(n-1)"
    r = (f"if(lt({k},{black}),{start},if(lt({k},{end}),"
         f"{start}+{1-start:.6f}*({k}-{black})/{max(1, ramp-1)},1))")
    return (f"scale=w='trunc(iw*({r})/2)*2':h='trunc(ih*({r})/2)*2':eval=frame,"
            f"pad={W}:{H}:x='(ow-iw)/2':y='(oh-ih)/2':color=black:eval=frame,"
            f"drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='lt(n,{black})'")


BLUR_SIGMA = 9       # độ mờ bản "mờ" trong mờ-vào (px ở 1080p); 9 ↔ độ nét đầu ≈0.16 như kênh POV Hàn
BLUR_ZOOM = 1.06     # bản mờ phóng thêm chút cho giống rack-focus


def blur_filter(W, H, sigma=BLUR_SIGMA, zoom=BLUR_ZOOM):
    """Bản 'mờ' cho hiệu ứng mờ-vào: gblur + phóng nhẹ rồi cắt về W×H."""
    zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    return f"gblur=sigma={sigma},scale={zw}:{zh},crop={W}:{H}"


def xfade_name(b):
    if b["type"] == "push":
        return "slideleft" if b.get("dir", "left") == "left" else "slideright"
    return "fade"


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]


# ---------------------------------------------------------------- nối + mux + kiểm -----------

def noi_va_mux(pieces, out, tmp, fps, audio=None, srt=None, font="Yu Gothic", sub_size=18,
               expect_frames=None, bgm=None, bgm_volume=0.09):
    """Nối các mảnh (đã cùng codec/khổ/fps) bằng concat demuxer. Mặc định -c copy (nhanh, không
    mất nét); nếu số khung lệch quá 2 hoặc phải cháy chữ thì encode lại 1 lần.
    Kiểm bằng count_video_frames + so với expect_frames (bẫy #1: không tin format=duration)."""
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{Path(p).resolve().as_posix()}'\n" for p in pieces),
                   encoding="utf-8")
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    need_encode = bool(srt)
    silent = tmp / "silent.mp4"
    run_ff(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart",
            silent], "nối mảnh (copy)")
    got = count_video_frames(silent)
    if expect_frames is not None and abs(got - expect_frames) > 2:
        print(f"  ⚠️ concat -c copy ra {got} khung, kế hoạch {expect_frames} → encode lại để sửa")
        need_encode = True
    if need_encode:
        vf = f"fps={fps}"
        if srt:
            shutil.copy(srt, tmp / "subs.srt")
            style = (f"FontName={font},FontSize={sub_size},PrimaryColour=&H00FFFFFF,"
                     f"OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,MarginV=45,"
                     f"Alignment=2")
            vf += f",subtitles=subs.srt:force_style='{style}'"
        silent2 = tmp / "silent2.mp4"
        subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe",
                        "0", "-i", str(lst), "-vf", vf, "-c:v", "libx264", "-preset", "medium",
                        "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        str(silent2)] + (["-frames:v", str(expect_frames)] if expect_frames else []),
                       check=True, cwd=str(tmp))
        silent = silent2
        got = count_video_frames(silent)
    if expect_frames is not None and abs(got - expect_frames) > 2:
        raise SystemExit(f"LỆCH KHUNG: dựng ra {got}, kế hoạch {expect_frames} "
                         f"(lệch {got-expect_frames}) — dừng, không xuất file.")
    # mux audio
    cmd = ["-i", silent]
    if audio:
        cmd += ["-i", Path(audio).resolve()]
    if bgm:
        cmd += ["-stream_loop", "-1", "-i", Path(bgm).resolve()]
    cmd += ["-map", "0:v:0"]
    if audio and bgm:
        cmd += ["-filter_complex", f"[1:a]volume=1.0[na];[2:a]volume={bgm_volume}[bg];"
                f"[na][bg]amix=inputs=2:duration=first:dropout_transition=3[a]", "-map", "[a]",
                "-c:a", "aac", "-b:a", "192k"]
    elif audio:
        cmd += ["-map", "1:a:0", "-c:a", "aac", "-b:a", "192k"]
    elif bgm:
        cmd += ["-filter_complex", f"[1:a]volume={bgm_volume}[a]", "-map", "[a]", "-c:a", "aac",
                "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "copy", "-movflags", "+faststart", out]
    run_ff(cmd, "mux")
    final_frames = count_video_frames(out)
    fps_o, w, h, dur_c = media_info(out)
    print(f"  ✓ {out}: {final_frames} khung @ {fps_o:g} fps = {final_frames/fps:.3f}s "
          f"(container {dur_c:.3f}s)")
    if audio:
        a = audio_seconds(audio)
        print(f"    audio {a:.3f}s → lệch hình-tiếng {final_frames/fps - a:+.3f}s")
    return final_frames


def ghi_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
