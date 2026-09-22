"""them_chuyen_canh_vao_clip.py — chồng chuyển cảnh lên CHUỖI CLIP ĐÃ DỰNG SẴN mà không đổi thời lượng.

  py -3.13 them_chuyen_canh_vao_clip.py --clips "_work/motion/*.mp4" --out body_fx.mp4 --ratio 0.70
  py -3.13 them_chuyen_canh_vao_clip.py --clips a.mp4 b.mp4 c.mp4 --audio voice.mp3 --out video.mp4

Mỗi clip = 1 cảnh (đã có chuyển động/Ken Burns riêng, vd clip Veo/Grok hoặc clip zoompan). Tổng khung
ra = tổng khung vào, đúng từng khung (bẫy #3 trong SKILL.md):
  - crossfade/đẩy ngang d khung: cảnh trước bị ăn da khung cuối, cảnh sau bị ăn db khung đầu
    (da+db = d). Trong mối nối, cảnh trước được đệm db khung ĐỨNG (clone khung cuối) và cảnh sau đệm
    da khung đứng (clone khung đầu) — bằng filter `loop` đếm theo khung (KHÔNG dùng tpad clone, xem
    ghi chú trong transition_piece) — rồi xfade. Phần chạy thật của mỗi cảnh vẫn nằm nguyên ô thời
    gian cũ.
  - zoom-từ-đen: áp lên 15 khung đầu của cảnh sau (khung 0 đen + 14 khung phóng), không ăn cảnh trước.
Các clip phải cùng khổ và fps (script kiểm, lệch là dừng). Mọi mảnh được encode lại (trim theo khung
buộc decode), nối bằng concat demuxer, đếm lại khung, lệch >2 là lỗi.
"""
import argparse
import concurrent.futures as cf
import glob
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chuyen_canh_lib as L  # noqa: E402


def trim_piece(clip, out, f0, n_out, fps, head_fx=None, threads=2):
    vf = f"trim=start_frame={f0}:end_frame={f0+n_out},setpts=PTS-STARTPTS,fps={fps}"
    if head_fx:
        vf += "," + head_fx
    vf += ",format=yuv420p"
    L.run_ff(["-i", clip, "-vf", vf, "-frames:v", n_out, "-r", fps, "-threads", threads, "-an"]
             + L.ENC + [out], f"cắt {Path(clip).name} [{f0}:{f0+n_out}]")


def transition_piece(clipA, nA, clipB, out, b, fps, threads=2):
    """d khung: A[nA-da:nA] + db khung đứng  ⨯  da khung đứng + B[0:db]."""
    d, da, db = b["d"], b["da"], b["db"]
    # Đệm khung đứng bằng `loop` (đếm theo KHUNG) chứ không phải `tpad ... clone` — đo thật ffmpeg 7.1:
    # tpad stop=9 sau trim chỉ thêm được 1 khung rồi fps= còn bỏ bớt → mối nối 9 khung thay vì 15.
    # Sau loop phải setpts=N/(fps*TB) để đánh lại mốc thời gian cho khung nhân bản.
    # Mỗi bên d+1 khung (xfade trả d-1 khung nếu đưa đúng d — xem ghép_anh_co_chuyen_canh.py).
    fc = (f"[0:v]trim=start_frame={nA-da}:end_frame={nA},setpts=PTS-STARTPTS,"
          f"loop=loop={db + 1}:size=1:start={da - 1},setpts=N/({fps}*TB),fps={fps},format=yuv420p[a];"
          f"[1:v]trim=start_frame=0:end_frame={db + 1},setpts=PTS-STARTPTS,"
          f"loop=loop={da}:size=1:start=0,setpts=N/({fps}*TB),fps={fps},format=yuv420p[b];"
          f"[a][b]xfade=transition={L.xfade_name(b)}:duration={d/fps:.6f}:offset=0,format=yuv420p[v]")
    L.run_ff(["-i", clipA, "-i", clipB, "-filter_complex", fc, "-map", "[v]", "-frames:v", d,
              "-r", fps, "-threads", threads, "-an"] + L.ENC + [out],
             f"mối nối {Path(clipA).name}→{Path(clipB).name}")


def blurin_piece(clipB, out, d, fps, W, H, sigma, zoom, threads=2):
    """d khung đầu của clip: xfade từ bản mờ+phóng nhẹ sang bản nét của chính nó."""
    fc = (f"[0:v]trim=start_frame=0:end_frame={d + 1},setpts=PTS-STARTPTS,"
          f"{L.blur_filter(W, H, sigma, zoom)},fps={fps},format=yuv420p[a];"
          f"[1:v]trim=start_frame=0:end_frame={d + 1},setpts=PTS-STARTPTS,fps={fps},format=yuv420p[b];"
          f"[a][b]xfade=transition=fade:duration={d/fps:.6f}:offset=0,format=yuv420p[v]")
    L.run_ff(["-i", clipB, "-i", clipB, "-filter_complex", fc, "-map", "[v]", "-frames:v", d,
              "-r", fps, "-threads", threads, "-an"] + L.ENC + [out], f"mờ-vào {Path(clipB).name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clips", nargs="+", required=True, help="glob hoặc danh sách clip theo thứ tự")
    ap.add_argument("--out", required=True)
    ap.add_argument("--audio", default="", help="mux audio (nếu clip đầu vào không có tiếng)")
    ap.add_argument("--ratio", type=float, default=0.70)
    ap.add_argument("--mix", default="0.55,0.35,0.10,0", help="xfade,zoomblack,push,blurin")
    ap.add_argument("--blur-frames", type=int, default=12)
    ap.add_argument("--blur-sigma", type=float, default=L.BLUR_SIGMA)
    ap.add_argument("--blur-zoom", type=float, default=L.BLUR_ZOOM)
    ap.add_argument("--xfade-frames", type=int, default=15)
    ap.add_argument("--black-frames", type=int, default=14)
    ap.add_argument("--black-start", type=float, default=0.544)
    ap.add_argument("--push-frames", type=int, default=11)
    ap.add_argument("--min-scene", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--srt", default="", help="cháy phụ đề (lớp riêng, chồng SAU hiệu ứng)")
    ap.add_argument("--font", default="Yu Gothic")
    ap.add_argument("--sub-size", type=int, default=18)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--plan-out", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    clips = []
    for c in args.clips:
        if any(ch in c for ch in "*?["):
            clips += sorted(Path(p) for p in glob.glob(c))
        else:
            clips.append(Path(c))
    if len(clips) < 2:
        raise SystemExit(f"cần ≥2 clip, có {len(clips)}")

    # ---- đo từng clip: fps/khổ phải đồng nhất, số khung đếm bằng demux ----
    fps0, W, H, _ = L.media_info(clips[0])
    fps = int(round(fps0))
    frames = []
    for c in clips:
        f, w, h, _ = L.media_info(c)
        if int(round(f)) != fps or (w, h) != (W, H):
            raise SystemExit(f"{c.name}: {w}x{h}@{f} ≠ clip đầu {W}x{H}@{fps0}")
        frames.append(L.count_video_frames(c))
    total = sum(frames)
    n = len(clips)
    mix = tuple(float(x) for x in args.mix.split(","))
    plan = L.lap_ke_hoach(frames, fps, ratio=args.ratio, mix=mix, d_xfade=args.xfade_frames,
                          d_black=args.black_frames, d_push=args.push_frames, d_blur=args.blur_frames,
                          seed=args.seed, min_scene_s=args.min_scene)
    print(f"{n} clip · {total} khung = {total/fps:.2f}s @ {fps}fps · {W}x{H}")
    print("  " + L.tom_tat_ke_hoach(plan))
    plan_dump = {"fps": fps, "size": [W, H], "total_frames": total, "frames": frames,
                 "clips": [c.name for c in clips], "ratio": args.ratio, "mix": mix, "boundaries": plan,
                 "boundary_frames": [sum(frames[:i + 1]) for i in range(n - 1)],
                 "n_black_frames": sum(b.get("black", 0) for b in plan if b["type"] == "zoomblack")}
    if args.plan_out:
        L.ghi_json(args.plan_out, plan_dump)
    if args.dry_run:
        for i, b in enumerate(plan):
            print(f"   #{i+1:3d} @khung {plan_dump['boundary_frames'][i]:6d}  {b['type']:9s} d={b['d']}")
        return

    tmp = Path(tempfile.mkdtemp(prefix="ccl_"))
    jobs, order = [], []
    for i in range(n):
        left = plan[i - 1] if i > 0 else None
        right = plan[i] if i < n - 1 else None
        f0 = left["db"] if left else 0
        f1 = frames[i] - (right["da"] if right else 0)
        head_fx = None
        if left and left["type"] == "zoomblack":
            head_fx = L.zoomblack_filter(W, H, black=left["black"], ramp=left["ramp"], start=args.black_start)
        if left and left["type"] == "blurin":
            ob = tmp / f"b{i:04d}.mp4"
            jobs.append(("blurin", ob, i, left["d"]))
            order.append(ob)
            f0 = left["d"]
        om = tmp / f"m{i:04d}.mp4"
        jobs.append(("main", om, i, f0, f1 - f0, head_fx))
        order.append(om)
        if right and right["type"] in ("xfade", "push"):
            ot = tmp / f"t{i:04d}.mp4"
            jobs.append(("trans", ot, i, right))
            order.append(ot)

    done, lock, t0 = [0], threading.Lock(), time.time()

    def _run(job):
        if job[0] == "main":
            _, out, i, f0, n_out, head_fx = job
            trim_piece(clips[i], out, f0, n_out, fps, head_fx, threads=args.threads)
        elif job[0] == "blurin":
            _, out, i, d = job
            blurin_piece(clips[i], out, d, fps, W, H, args.blur_sigma, args.blur_zoom, threads=args.threads)
        else:
            _, out, i, b = job
            transition_piece(clips[i], frames[i], clips[i + 1], out, b, fps, threads=args.threads)
        with lock:
            done[0] += 1
            print(f"  mảnh {done[0]}/{len(jobs)}", end="\r", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(_run, jobs))
    print(f"\n  → {len(jobs)} mảnh trong {time.time()-t0:.0f}s")

    sai = []
    for job in jobs:
        e = job[4] if job[0] == "main" else (job[3] if job[0] == "blurin" else job[3]["d"])
        g = L.count_video_frames(job[1])
        if g != e:
            sai.append((job[1].name, g, e))
    if sai:
        raise SystemExit(f"Mảnh sai số khung (được/kế hoạch): {sai[:8]}")

    L.noi_va_mux(order, args.out, tmp, fps, audio=args.audio or None, srt=args.srt or None,
                 font=args.font, sub_size=args.sub_size, expect_frames=total)
    print(f"✓ xong {(time.time()-t0)/60:.1f} phút · tạm: {tmp}")


if __name__ == "__main__":
    main()
