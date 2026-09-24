"""assemble.py — ghép ảnh thành video 16:9: ảnh ĐỨNG YÊN + SYNC ảnh theo câu narration (SRT) +
CROSSFADE chuyển cảnh mềm + burn phụ đề + mix nhạc nền. Thay ~toàn bộ việc dựng tay CapCut.

⛔ CẤM Ken Burns zoom/pan (chốt 2026-09-21, mọi lane, xem CLAUDE.md mục 🎞️ CHUYỂN CẢNH): ảnh phải
đứng yên hoàn toàn trong lúc hiển thị, giật/rung do zoom/pan gây nhức mắt. Chỉ hiệu ứng CHUYỂN CẢNH
(xfade/fade/cut giữa 2 ảnh) mới được dùng. `--zoom` mặc định = 1.0 (tắt hẳn zoompan, không chỉ đặt
hệ số 0). Muốn bật lại chuyển động nhẹ phải NÓI RÕ lý do và tối đa 1.03-1.04, không hơn.

Dùng (đủ bộ):
  py -3.13 assemble.py --img <dir> --audio voice.mp3 --srt voice.srt --bgm bgm.mp3 --out final.mp4
Tùy chọn:
  --transition xfade|fade|cut  (mặc định xfade = crossfade mềm)
  --xfade 0.6                  (thời lượng crossfade giây)
  --sync                       (BẬT mặc định khi có --srt: ảnh đổi đúng ranh giới câu)
  --bgm-volume 0.09 · --zoom 1.0 (đứng yên, mặc định) · --size 1920x1080 · --fps 30

Cơ chế sync: chia N ảnh theo M cue trong SRT → mỗi ảnh hiển thị đúng đoạn narration của nó (đổi cảnh
rơi vào ranh giới câu, không cắt giữa câu, nhịp bám lời đọc). Không SRT → chia đều theo audio.
"""
import argparse
import json
import os
import concurrent.futures as cf
import threading
import time
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg

sys.stdout.reconfigure(encoding="utf-8")
FF = imageio_ffmpeg.get_ffmpeg_exe()


def media_seconds(path):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise SystemExit(f"Không đọc được độ dài: {path}")
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


_HET_CAU = "。．.！!？?」』】"


def parse_srt_starts(srt_path):
    """Trả list thời điểm bắt đầu (giây) của từng cue."""
    txt = Path(srt_path).read_text(encoding="utf-8")
    starts = []
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d)[,.](\d\d\d)\s*-->", txt):
        h, mn, s, ms = map(int, m.groups())
        starts.append(h * 3600 + mn * 60 + s + ms / 1000)
    return starts


def parse_srt_cues(srt_path):
    """(thời điểm bắt đầu, lời) của từng cue — cần LỜI để biết cue nào kết thúc câu."""
    txt = Path(srt_path).read_text(encoding="utf-8")
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        L = blk.splitlines()
        tl = next((x for x in L if "-->" in x), None)
        if not tl:
            continue
        m = re.match(r"\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)", tl)
        if not m:
            continue
        h, mn, s, ms = map(int, m.groups())
        out.append((h * 3600 + mn * 60 + s + ms / 1000,
                    "".join(L[L.index(tl) + 1:]).strip()))
    return out


def _moc_het_cau(cues):
    """Cue nào ĐƯỢC PHÉP làm chỗ đổi ảnh: cue đầu, và cue mở đầu một câu mới.

    Vì sao (lỗi thật 2026-09-09, video simbot2-vU5PWT2zLDs): cue của STT bị cắt tuỳ tiện, 63%
    không kết thúc câu. Chia ảnh đều theo chỉ số cue thì cảnh đổi ngay giữa mệnh đề — cộng với
    khoảng nghỉ cũng đặt sai chỗ, xem thành ra giật cục. Đổi cảnh phải rơi vào chỗ vừa dứt câu.
    """
    ok = {0}
    for i in range(1, len(cues)):
        t = cues[i - 1][1].rstrip()
        if t and t[-1] in _HET_CAU:
            ok.add(i)
    return sorted(ok)


def sync_durations(n, audio_len, srt_cues, min_dur=2.0):
    """Chia n ảnh theo cue: ảnh i hiển thị từ cue[b_i] tới cue[b_{i+1}], HÚT về ranh giới câu.

    `srt_cues` nhận cả list thời điểm (kiểu cũ) lẫn list (thời điểm, lời). Chỉ dạng có lời mới
    hút được về cuối câu; dạng cũ giữ nguyên hành vi để không phá script gọi tay.
    """
    if not srt_cues:
        return [audio_len / n] * n
    co_loi = isinstance(srt_cues[0], (tuple, list))
    starts = [c[0] for c in srt_cues] if co_loi else list(srt_cues)
    M = len(starts)
    bounds = [round(i * M / n) for i in range(n + 1)]
    if co_loi:
        moc = _moc_het_cau(srt_cues)
        if len(moc) >= n:
            # Chọn mốc theo THỜI GIAN, không theo chỉ số. Chia đều theo SỐ CÂU nghe thì hợp lý
            # nhưng câu dài ngắn rất khác nhau → ảnh 2 giây nằm cạnh ảnh 37 giây. Bám mốc thời
            # gian lý tưởng (audio_len/n) rồi lấy ranh giới câu gần nhất thì vừa đúng chỗ dứt
            # câu vừa đều thời lượng. Có chừa mốc cho các ảnh còn lại để không bị hụt ở cuối.
            bounds, truoc = [0], 0
            for i in range(1, n):
                dich = i * audio_len / n
                con = len(moc) - (n - i)             # mốc xa nhất còn được phép lấy
                ung = [j for j in range(truoc + 1, con + 1)]
                truoc = min(ung, key=lambda j: abs(starts[moc[j]] - dich)) if ung else truoc + 1
                bounds.append(moc[min(truoc, len(moc) - 1)])
            bounds.append(M)
        else:
            # Ít câu hơn số ảnh → buộc phải có ảnh đổi giữa câu. Giữ cách chia cũ và nói rõ ra.
            print(f"  ! chỉ {len(moc)} ranh giới câu cho {n} ảnh — vài cảnh sẽ đổi giữa câu")
    bounds[-1] = M
    durs = []
    for i in range(n):
        # Ảnh đầu chạy từ giây 0 (cue 1 bắt đầu sau khoảng lặng mở đầu) — không thì tổng thời
        # lượng ảnh hụt đúng bằng khoảng lặng đó và phải co giãn bù, làm trôi mọi mốc phía sau.
        t0 = 0.0 if i == 0 else starts[min(bounds[i], M - 1)]
        t1 = starts[bounds[i + 1]] if bounds[i + 1] < M else audio_len
        durs.append(t1 - t0)
    if min(durs) >= 0.5:
        return durs          # đã khớp đúng ranh giới câu, KHÔNG co giãn → không trôi mốc nào
    # Có đoạn quá ngắn (câu cụt) → mới phải kẹp sàn rồi chuẩn hoá, chấp nhận trôi chút đỉnh.
    durs = [max(min_dur, d) for d in durs]
    scale = audio_len / sum(durs)
    return [d * scale for d in durs]


def anchor_durations(anchor_map, imgs, audio_len, srt_cues):
    """Chia ảnh theo ĐÚNG CÂU VĂN đã thiết kế (khác `sync_durations` chia đều mù theo số đếm).

    Vì sao cần: `sync_durations` chỉ biết CHIA N ảnh cho M cue theo tỉ lệ thời gian — không biết
    ảnh nào ứng với đoạn nào. Khi người viết kịch bản đã CHỌN đúng 1 câu neo cho mỗi ảnh (ví dụ
    ảnh "Shuri thành đổ nát" phải hiện đúng lúc đọc câu "首里城の地下に築かれていた司令部の様子を"),
    chia đều theo số đếm sẽ TRÔI dần về cuối video nếu các đoạn trước đó dài/ngắn không đều — đo
    thật (2026-09-11, ep01-ushijima-mitsuru): phục hồi đủ N ảnh KHÔNG sửa được trôi, vì gốc rễ là
    thiếu neo theo NỘI DUNG chứ không phải thiếu ảnh.

    `anchor_map`: {tên_file_ảnh: chuỗi_neo (nguyên văn/đầu câu trong script, khớp y hệt cue đã
    được `srt_from_script.py` gióng lại — nếu chưa chạy bước đó thì cue là lời STT nghe lại, tìm
    neo sẽ trật). Trả về list thời lượng (giây) theo ĐÚNG thứ tự `imgs`.
    """
    full, spans = [], []             # spans[i] = (bắt_đầu_ký_tự, cue_index)
    pos = 0
    for i, (_, txt) in enumerate(srt_cues):
        spans.append((pos, i))
        full.append(txt)
        pos += len(txt)
    full_text = "".join(full)

    starts = []
    tim_tu = 0
    for img in imgs:
        neo = anchor_map.get(img.name)
        if neo is None:
            raise SystemExit(f"--anchors thiếu dòng cho ảnh {img.name} — mỗi ảnh phải có 1 neo.")
        idx = full_text.find(neo, tim_tu)
        if idx == -1:
            idx = full_text.find(neo)      # thử lại từ đầu — neo có thể đứng trước neo trước đó do lỗi thứ tự
            if idx == -1:
                raise SystemExit(f"Không tìm thấy neo của {img.name} trong SRT: {neo[:40]!r}… "
                                 f"— SRT có khớp đúng script đã dùng để viết neo không?")
        # đổi ký tự -> cue -> thời điểm bắt đầu cue đó
        cue_i = 0
        for start_ch, ci in spans:
            if start_ch <= idx:
                cue_i = ci
            else:
                break
        starts.append(srt_cues[cue_i][0])
        tim_tu = idx + len(neo)
    starts.append(audio_len)
    durs = [starts[i + 1] - starts[i] for i in range(len(imgs))]
    xau = [(imgs[i].name, round(d, 1)) for i, d in enumerate(durs) if d < 1.0]
    if xau:
        raise SystemExit(f"Neo đặt ra thời lượng ÂM hoặc quá ngắn (<1s) — thứ tự neo bị lệch: {xau}")
    return durs


def load_anchors(path):
    """Đọc file `tên_ảnh|chuỗi neo` (1 dòng/ảnh, đúng thứ tự xuất hiện trong video)."""
    m = {}
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "|" not in ln:
            continue
        name, neo = ln.split("|", 1)
        m[name.strip()] = neo.strip()
    return m


def fit_filter(fit, sw, sh):
    """Cách đưa ảnh KHÁC TỈ LỆ về khung làm việc sw×sh.

    - `cover` (mặc định): giữ đúng tỉ lệ, cắt bớt viền dư. Ảnh 16:9 (gpti2 2560×1440) không mất gì;
      nhưng ảnh VUÔNG (nano-banana 2048×2048) bị cắt ~44% chiều cao → có thể cắt mất mặt.
    - `blur`: ảnh vừa khung + nền là bản phóng to làm mờ → KHÔNG méo, KHÔNG viền đen. Dùng cho ảnh
      vuông/dọc lỡ trộn vào.
    - `pad`: viền đen 2 bên (giữ trọn ảnh nhưng xấu, giảm retention).
    - `stretch`: kéo cạnh cho lấp khung — BIẾN DẠNG MẶT NGƯỜI (vuông→16:9 là bè 77,8%).
      Chỉ dùng khi lệch tỉ lệ <3%.
    """
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


def check_aspect(imgs, W, H, fit, tol=0.03):
    """Cảnh báo ảnh lệch tỉ lệ khung — nếu không báo thì `cover` cắt mất nội dung một cách ÂM THẦM."""
    try:
        from PIL import Image
    except ImportError:
        return
    target = W / H
    bad = []
    for p in imgs:
        try:
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            continue
        r = w / h
        if abs(r / target - 1) > tol:
            bad.append((p.name, f"{w}x{h}", round(r, 3)))
    if not bad:
        return
    loss = "cắt mất viền" if fit == "cover" else ("kéo méo mặt" if fit == "stretch" else f"xử theo --fit {fit}")
    print(f"  ⚠️ {len(bad)}/{len(imgs)} ảnh lệch tỉ lệ khung {target:.3f} → sẽ {loss}. "
          f"Ví dụ: {bad[:3]}")
    if fit == "cover":
        print("     → ảnh vuông/dọc nên dùng --fit blur (không méo, không viền đen).")


def _warp_clip(img, frames, W, H, fps, zoom, zoom_in, out, threads, fit):
    import numpy as np
    import cv2
    sw, sh = int(W * zoom + 3) // 2 * 2, int(H * zoom + 3) // 2 * 2
    base_png = Path(str(out) + ".base.png")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(img), "-vf", fit_filter(fit, sw, sh), "-frames:v", "1",
                    str(base_png)], check=True, capture_output=True)
    base = cv2.imread(str(base_png))
    base_png.unlink(missing_ok=True)
    cx, cy = base.shape[1] / 2, base.shape[0] / 2
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                          "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-threads", str(threads), str(out)], stdin=subprocess.PIPE)
    try:
        for k in range(frames):
            tien = k / max(1, frames - 1)
            z = 1.0 + (zoom - 1.0) * (tien if zoom_in else 1.0 - tien)
            h = z * W / base.shape[1]                     # hệ số từ ảnh nền (khổ W*zoom) ra khung W
            M = np.array([[h, 0, W / 2 - h * cx], [0, h, H / 2 - h * cy]], np.float32)
            p.stdin.write(cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_CUBIC,
                                         borderMode=cv2.BORDER_REFLECT).tobytes())
    finally:
        p.stdin.close()
        p.wait()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, "ffmpeg warp")


def render_clip(img, dur, W, H, fps, zoom, zoom_in, out, threads=2, fit="cover"):
    frames = max(1, int(round(dur * fps)))
    # ⛔ CẤM Ken Burns zoom/pan (chốt 2026-09-21, mọi lane): ảnh phải ĐỨNG YÊN HOÀN TOÀN, chỉ hiệu
    # ứng CHUYỂN CẢNH (xfade/fade/cut) giữa 2 ảnh mới được dùng — xem CLAUDE.md mục 🎞️ CHUYỂN CẢNH.
    # zoom<=1.0 (mặc định) → BỎ HẲN filter zoompan, không chỉ đặt hệ số 0, vì zoompan tự nó vẫn
    # resample lại từng khung (bo tròn pixel z=1.0 vẫn có thể rung nhẹ) — scale tĩnh 1 lần là sạch.
    if zoom <= 1.0:
        sw, sh = W, H
        vf = f"{fit_filter(fit, sw, sh)},format=yuv420p"
    else:
        # Ken Burns CHỈ còn cho lane khai assemble.zoom>1 (ngoại lệ anh cho Lane K 2026-09-24: kênh mẫu
        # 千種テンカ đo máy ×1,02–1,03 phóng chậm suốt cảnh, 88/91 cảnh). KHÔNG dùng zoompan: nó cắt theo
        # pixel NGUYÊN → ở tốc độ ~0,07 px/khung hình nhảy bậc = đúng cái "giật/rung" bị cấm 21/09 (đo thật:
        # độ lệch chuẩn dịch chuyển/khung 0,39 px với zoompan, 0,12 px dù phóng ảnh 4×). Dựng bằng
        # warpAffine dưới-pixel (cv2) rồi đẩy thẳng khung thô sang ffmpeg: 0,016 px — trôi mượt tuyệt đối.
        _warp_clip(img, frames, W, H, fps, zoom, zoom_in, out, threads, fit)
        return
    # Clip trung gian sẽ bị encode LẠI ở bước crossfade → preset chậm là công toi. crf thấp hơn
    # (18) để lần encode cuối không bị cộng dồn mất nét.
    subprocess.run([FF, "-y", "-loop", "1", "-i", str(img), "-t", f"{dur}",
                    "-vf", vf, "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "18", "-threads", str(threads), str(out)],
                   check=True, capture_output=True)


def xfade_chain(durs, t, n):
    """Tra ve filter_complex noi n clip bang crossfade, ket thuc o nhan [vout].
    KHONG encode o day: chuoi nay duoc gan thang vao lenh mux cuoi de chi encode 1 lan."""
    parts, prev, cum = [], "0:v", 0.0
    for i in range(1, n):
        cum += durs[i - 1]
        off = cum - i * t
        lbl = f"v{i}" if i < n - 1 else "vout"
        parts.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={t}:offset={off:.3f}[{lbl}]")
        prev = lbl
    return ";".join(parts)


def build_silent_concat(clips, out, tmp, fade_each=0.0, fps=30):
    """Nối bằng concat demuxer (cut). fade_each>0 → mỗi clip fade in/out (dip-to-black)."""
    files = clips
    if fade_each > 0:
        faded = []
        for i, c in enumerate(clips):
            d = media_seconds(c)
            fo = max(0, d - fade_each)
            f = tmp / f"f{i:04d}.mp4"
            subprocess.run([FF, "-y", "-i", str(c),
                            "-vf", f"fade=t=in:st=0:d={fade_each},fade=t=out:st={fo:.3f}:d={fade_each}",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(f)],
                           check=True, capture_output=True)
            faded.append(f)
        files = faded
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in files), encoding="utf-8")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audio", default="")
    ap.add_argument("--srt", default="")
    ap.add_argument("--anchors", default="", help="file 'tên_ảnh|câu neo trong script' — đồng bộ "
                    "ảnh theo ĐÚNG câu văn đã thiết kế thay vì chia đều mù theo số đếm. Cần --srt "
                    "đã qua srt_from_script.py (khớp y hệt script, không phải lời STT nghe lại).")
    ap.add_argument("--burn-sub", action="store_true",
                    help="CHÁY phụ đề vào hình (mặc định KHÔNG — up .srt lên YouTube làm CC)")
    ap.add_argument("--font", default="Meiryo")
    ap.add_argument("--tate", action="store_true",
                    help="cháy hộp chữ DỌC 縦書き (tate_text.py, Lane F/teinengo-real) thay vì phụ đề "
                         "ngang — cần --srt. KHÔNG dùng chung với --burn-sub trong cùng lane (2 cơ chế "
                         "khác nhau vẽ chữ vào cùng vùng hình, dễ chồng lên nhau).")
    ap.add_argument("--tate-side", default="left", choices=["left", "right"])
    ap.add_argument("--tate-font-narration", default="Yu Mincho")
    ap.add_argument("--tate-font-dialogue", default="Yu Gothic")
    ap.add_argument("--tate-size", type=int, default=42)
    ap.add_argument("--tate-max-chars", type=int, default=14)
    ap.add_argument("--tate-max-cols", type=int, default=2)
    ap.add_argument("--bubble-roles", default="",
                    help="voice_roles.json (tts_voicevox) → hộp lời kể + bóng thoại có đuôi (bong_thoai.py, Lane K)")
    ap.add_argument("--bubble-faces", default="", help="img_faces.json (bong_thoai.do_mat) — vị trí mặt/miệng từng ảnh")
    ap.add_argument("--bubble-cfg", default="", help="JSON cấu hình assemble.bubble của profile")
    ap.add_argument("--bgm", default="")
    ap.add_argument("--bgm-volume", type=float, default=0.10)
    ap.add_argument("--bgm-keep-voice", action="store_true", help="amix normalize=0: giọng giữ nguyên mức")
    ap.add_argument("--transition", default="xfade", choices=["xfade", "fade", "cut"])
    ap.add_argument("--xfade", type=float, default=0.6, help="thời lượng crossfade (giây)")
    ap.add_argument("--sec", type=float, default=8.0, help="giây/ảnh khi KHÔNG có audio")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--zoom-dir", default="alt", choices=["alt", "in"],
                    help="alt = phóng/thu xen kẽ; in = cảnh nào cũng phóng vào (kênh mẫu Lane K 88/91 cảnh)")
    ap.add_argument("--zoom", type=float, default=1.0,
                     help="1.0 = ảnh đứng yên hoàn toàn (mặc định, chốt 2026-09-21 — CẤM Ken Burns "
                          "giật/rung, chỉ dùng hiệu ứng CHUYỂN CẢNH --transition). >1.0 chỉ bật tay "
                          "khi thật sự cần, tối đa 1.03-1.04 kiểu Lane E, không hơn.")
    ap.add_argument("--fit", default="cover", choices=["cover", "blur", "pad", "stretch"],
                    help="ảnh khác tỉ lệ khung: cover=cắt viền (mặc định) · blur=nền mờ (không méo, "
                         "không viền) · pad=viền đen · stretch=kéo méo mặt, chỉ khi lệch <3%%")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 3),
                    help="số clip render song song (mặc định = cores/3)")
    ap.add_argument("--clip-threads", type=int, default=2, help="thread ffmpeg cho MỖI clip")
    args = ap.parse_args()

    imgs = sorted(Path(args.img).glob("[0-9]*.png"))
    if not imgs:
        raise SystemExit(f"Không thấy ảnh NNN.png trong {args.img}")
    n = len(imgs)
    W, H = (int(x) for x in args.size.split("x"))
    t = args.xfade if args.transition == "xfade" else 0.0

    # ---- thời lượng từng ảnh ----
    if args.audio:
        audio_len = media_seconds(args.audio)
        starts = parse_srt_cues(args.srt) if args.srt else []
        if args.anchors:
            if not starts:
                raise SystemExit("--anchors cần --srt đi kèm (để tra thời điểm theo câu).")
            segs = anchor_durations(load_anchors(args.anchors), imgs, audio_len, starts)
            mode = "sync theo NEO NỘI DUNG (--anchors, chính xác theo câu đã thiết kế)"
        else:
            segs = sync_durations(n, audio_len, starts)
            mode = "sync theo RANH GIỚI CÂU (SRT)" if starts else "chia đều audio"
        print(f"Audio {round(audio_len)}s / {n} ảnh · {mode} · transition={args.transition}")
    else:
        segs = [args.sec] * n
        audio_len = None
        print(f"{n} ảnh × {args.sec}s (chưa audio) · transition={args.transition}")

    # render duration mỗi clip: cộng thêm t để bù overlap crossfade
    render_durs = [s + t for s in segs]

    check_aspect(imgs, W, H, args.fit)
    t_all = time.time()
    tmp = Path(tempfile.mkdtemp(prefix="asm_"))
    # Render clip SONG SONG. Đo thật 2026-09-08: 123 clip tuần tự = ~18-19 phút trên máy 24 core.
    # Mỗi ffmpeg giới hạn --clip-threads (mặc định 2) để nhiều clip chạy cùng lúc không tranh CPU.
    clips = [tmp / f"c{i:04d}.mp4" for i in range(n)]
    t_clip = time.time()
    done = [0]
    lock = threading.Lock()

    def _one(i):
        render_clip(imgs[i], render_durs[i], W, H, args.fps, args.zoom,
                    zoom_in=(args.zoom_dir == "in" or i % 2 == 0), out=clips[i], threads=args.clip_threads, fit=args.fit)
        with lock:
            done[0] += 1
            print(f"  clip {done[0]}/{n}", end="\r", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(_one, range(n)))
    print(f"\n  -> {n} clip trong {time.time()-t_clip:.0f}s "
          f"({args.jobs} luong x {args.clip_threads} thread)")

    # ---- NOI + MUX TRONG 1 LAN ENCODE ----
    # Ban cu: xfade ra silent.mp4 (encode 1) roi burn phu de + mix audio (encode 2) => encode CA
    # video 30 phut HAI LAN. Gop chuoi xfade vao chinh filter_complex cua buoc mux => con 1 lan.
    fused = args.transition == "xfade" and n > 1
    t_join = time.time()
    fc = []
    if fused:
        print("  crossfade + mux (1 lan encode)...")
        fc.append(xfade_chain(render_durs, t, n))
        inputs = []
        for c in clips:
            inputs += ["-i", str(c.resolve())]
        vin, vmap, na_idx = "[vout]", "[vout]", n
    else:
        silent = tmp / "silent.mp4"
        if args.transition == "fade":
            build_silent_concat(clips, silent, tmp, fade_each=0.4, fps=args.fps)
        else:
            build_silent_concat(clips, silent, tmp)
        inputs = ["-i", str(silent.resolve())]
        vin, vmap, na_idx = "[0:v]", "0:v", 1

    if args.audio:
        inputs += ["-i", str(Path(args.audio).resolve())]
    bg_idx = na_idx + (1 if args.audio else 0)
    if args.bgm:
        inputs += ["-stream_loop", "-1", "-i", str(Path(args.bgm).resolve())]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.tate:
        # Hộp chữ dọc 縦書き (tate_text.py) — TRACK RIÊNG dựng bằng variable-duration concat (cùng kỹ
        # thuật render_clip/build_silent_concat ở trên), overlay lên video nền bằng ĐÚNG 1 filter
        # `overlay` (không chèn hàng trăm filter enable=between() vào filter_complex vốn đã lớn).
        if not args.srt:
            raise SystemExit("--tate cần --srt đi kèm (đọc cue để biết chữ + thời điểm).")
        import tate_text
        tate_path = tmp / "tate_track.mov"
        t_tate = time.time()
        tate_text.build_track(args.srt, tate_path, W, H, args.fps, args.tate_side,
                              args.tate_font_narration, args.tate_font_dialogue, args.tate_size,
                              args.tate_max_chars, args.tate_max_cols,
                              total_dur=audio_len, tmp_dir=tmp / "tate_frames")
        print(f"  -> tate track {time.time()-t_tate:.0f}s")
        tate_idx = inputs.count("-i")
        inputs += ["-i", str(tate_path.resolve())]
        fc.append(f"{vin}[{tate_idx}:v]overlay=eof_action=pass[vt]")
        vin = vmap = "[vt]"

    if args.bubble_roles:
        # Lane K (2026-09-24): mọi câu lên hình — hộp lời kể / bóng thoại có đuôi chỉ người nói. Dòng thời gian
        # ảnh = ĐÚNG segs ở trên (ảnh i hiện từ tổng segs[:i]) để bóng thoại biết lúc đó đang hiện ảnh nào.
        import bong_thoai
        tl, t0 = [], 0.0
        for i_, s_ in enumerate(segs):
            tl.append((imgs[i_].name, t0, t0 + s_))
            t0 += s_
        bt_path = tmp / "bubble_track.mov"
        t_bt = time.time()
        bong_thoai.build_track(args.bubble_roles, tl, args.bubble_faces or None, bt_path, W, H, args.fps,
                               json.loads(args.bubble_cfg) if args.bubble_cfg else {}, total_dur=audio_len,
                               tmp_dir=tmp / "bubble_frames")
        print(f"  -> bubble track {time.time()-t_bt:.0f}s")
        bt_idx = inputs.count("-i")
        inputs += ["-i", str(bt_path.resolve())]
        fc.append(f"{vin}[{bt_idx}:v]overlay=eof_action=pass[vb]")
        vin = vmap = "[vb]"

    # ⚠️ --srt có HAI vai: (1) đồng bộ đổi cảnh theo ranh giới câu — LUÔN dùng; (2) CHÁY chữ vào
    # hình — chỉ khi --burn-sub. User chốt 2026-09-11: MẶC ĐỊNH KHÔNG cháy phụ đề (YouTube tự bật
    # CC từ file .srt mình up kèm; khán giả Nhật nghe hiểu, chữ cháy chỉ che hình).
    if args.srt and args.burn_sub:
        import shutil
        shutil.copy(args.srt, tmp / "subs.srt")
        style = (f"FontName={args.font},FontSize=18,PrimaryColour=&H00FFFFFF,"
                 f"OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,MarginV=45,Alignment=2")
        fc.append(f"{vin}subtitles=subs.srt:force_style='{style}'[v]")
        vmap = "[v]"
    amap = None
    if args.audio and args.bgm:
        # --bgm-keep-voice (Lane K 2026-09-24): amix mặc định CHIA ĐÔI mọi đầu vào → giọng tụt 6 dB so với
        # bản không nhạc. normalize=0 giữ nguyên mức giọng đã loudnorm ở B4. Lane cũ không khai → như cũ.
        norm = ":normalize=0" if args.bgm_keep_voice else ""
        fc.append(f"[{na_idx}:a]volume=1.0[na];[{bg_idx}:a]volume={args.bgm_volume}[bg];"
                  f"[na][bg]amix=inputs=2:duration=first:dropout_transition=3{norm}[a]")
        amap = "[a]"
    elif args.audio:
        amap = f"{na_idx}:a"
    elif args.bgm:
        fc.append(f"[{bg_idx}:a]volume={args.bgm_volume}[a]")
        amap = "[a]"

    cmd = [FF, "-y"] + inputs
    if fc:
        cmd += ["-filter_complex", ";".join(fc)]
    cmd += ["-map", vmap]
    if amap:
        cmd += ["-map", amap, "-c:a", "aac", "-b:a", "192k"]
    # chi copy duoc khi da co san silent.mp4 va khong burn phu de
    copy_ok = (not (args.srt and args.burn_sub)) and not fused and not args.tate and not args.bubble_roles
    cmd += (["-c:v", "copy"] if copy_ok else
            ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"])
    if args.audio:
        cmd += ["-shortest"]
    cmd += [str(out.resolve())]
    subprocess.run(cmd, check=True, capture_output=True, cwd=str(tmp))
    print(f"  -> noi + mux {time.time()-t_join:.0f}s")

    print(f"✓ Video: {out} ({n} ảnh, transition={args.transition})"
          + (" + audio" if args.audio else "")
          + (" + phụ đề CHÁY" if (args.srt and args.burn_sub) else "")
          + (" + chữ dọc 縦書き" if args.tate else "")
          + (" + nhạc nền" if args.bgm else ""))
    print(f"  TONG B8: {(time.time()-t_all)/60:.1f} phut")


if __name__ == "__main__":
    main()
