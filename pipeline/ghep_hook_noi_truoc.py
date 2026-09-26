# -*- coding: utf-8 -*-
"""Hook NỐI LÊN TRƯỚC final.mp4 (tập mà script.txt KHÔNG chứa hook — vd kenko ep02 trở đi, satori ep3).

Khác `ghep_hook_thay_hinh.py` (tập mà hook nằm sẵn trong script → đè hình, giữ tiếng). Ở đây hook có
GIỌNG RIÊNG (`hook/hook_voice.mp3`, máy 1 lồng sẵn) → dựng đoạn hook từ clip + giọng + SFX rồi đặt TRƯỚC thân.

    py -3.13 ghep_hook_noi_truoc.py --tap <thư mục tập>             → <tập>/final_with_hook.mp4
    py -3.13 ghep_hook_noi_truoc.py --tap <thư mục tập> --profile teinengo-real   → + hộp chữ dọc như thân (assemble.tate)
    py -3.13 ghep_hook_noi_truoc.py --tap <thư mục tập> --xem-thu   → <tập>/hook/hook_preview_vi.mp4 (cháy phụ đề Việt hook_vi.srt, không cần final.mp4)

Tự làm 4 thứ phải khớp (docs/QUY_TAC_VIDEO_HOOK.md §2): khổ + fps theo final.mp4 · mức tiếng hook hạ/nâng bằng
đúng mức thân (đo ebur128 180 giây đầu final) · điểm nối không khung đen (concat filter, clip cắt đúng mốc) ·
xoá metadata (chữ ký "Signature:" Grok). Tiếng riêng của clip bị bỏ. Thiếu clip → DỪNG (hook bắt buộc là video).
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path


def _ff():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        f = shutil.which("ffmpeg")
        if not f:
            sys.exit("✗ không tìm thấy ffmpeg (pip install imageio-ffmpeg)")
        return f


FF = _ff()


def _run_err(args):
    return subprocess.run([FF, *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr


def probe(p):
    err = _run_err(["-i", str(p)])
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    v = re.search(r"Video:.*?(\d{3,5})x(\d{3,5}).*?([\d.]+) fps", err)
    return int(h) * 3600 + int(m) * 60 + float(s), int(v.group(1)), int(v.group(2)), float(v.group(3))


def lufs(p, giay=None):
    args = ["-hide_banner", "-nostats"] + (["-t", str(giay)] if giay else []) + ["-i", str(p), "-vn", "-af", "ebur128", "-f", "null", "-"]
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", _run_err(args))
    return float(m[-1]) if m else None


def _giua(roles, i):
    """Điểm cắt sau câu i: giữa khoảng lặng tới câu i+1 (không có câu sau → +0,3s)."""
    e, nxt = roles[i]["end"], roles.get(i + 1)
    return round((e + nxt["start"]) / 2 if nxt else e + 0.3, 3)


def neo_lai_theo_cau(tap: Path) -> bool:
    """Lane L 2026-09-25: hook ghi mốc theo SỐ CÂU (`shots[].cau=[a,b]`, `sfx[].cau` + `lech`) thay vì giây.

    Vì sao: giọng thân do MÁY 2 lồng lại bằng ai33 — không tất định, mỗi lượt đọc dài ngắn khác nhau — nên mốc giây
    máy 1 đo trên giọng thử sẽ lệch hình/lời 1–2s. Ở đây tính lại giây từ `voice_roles.json` của CHÍNH giọng thân,
    rồi cắt `hook_voice.mp3`/`.srt`/`_roles.json` từ giọng thân (THAY HÌNH giữ tiếng thân, file cắt chỉ để đo mức
    tiếng + dựng bóng thoại hook). Timeline không có `cau` → không đụng gì (lane khác giữ nguyên hành vi cũ).
    """
    hook = tap / "hook"
    f = hook / "hook_timeline.json"
    tl = json.loads(f.read_text(encoding="utf-8"))
    shots = tl["shots"]
    if not shots or not all("cau" in s for s in shots):
        return False
    rf = tap / "voice_roles.json"
    if not rf.exists():
        sys.exit(f"✗ hook neo theo câu cần {rf} (B4 lồng tiếng đa giọng chưa chạy)")
    roles = {int(r["i"]): r for r in json.loads(rf.read_text(encoding="utf-8"))}
    truoc = 0
    for k, s in enumerate(shots):
        a, b = int(s["cau"][0]), int(s["cau"][1])
        if a != truoc + 1 or b < a or b not in roles:
            sys.exit(f"✗ hook cảnh {s.get('n')}: cau={s['cau']} không nối tiếp cảnh trước / vượt số câu thân")
        truoc = b
        s["t0"] = 0.0 if k == 0 else shots[k - 1]["t1"]
        s["t1"] = _giua(roles, b)
        if s["t1"] - s["t0"] < 0.5:
            sys.exit(f"✗ hook cảnh {s.get('n')} chỉ {s['t1'] - s['t0']:.2f}s — gộp câu lại ở máy 1")
    for x in tl.get("sfx", []):
        if "cau" in x:
            x["t"] = round(roles[int(x["cau"])]["start"] + float(x.get("lech", 0)), 3)
    T = shots[-1]["t1"]
    tl["hook_voice_end_s"] = T
    f.write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    voice = tap / "voice.mp3"
    if not voice.exists():
        sys.exit(f"✗ thiếu {voice}")
    subprocess.run([FF, "-y", "-v", "error", "-i", str(voice), "-t", f"{T:.3f}", "-c:a", "libmp3lame", "-q:a", "2",
                    str(hook / "hook_voice.mp3")], check=True)
    r_hook = [dict(r, end=min(r["end"], T)) for r in roles.values() if r["start"] < T]
    (hook / "hook_voice_roles.json").write_text(json.dumps(r_hook, ensure_ascii=False, indent=1), encoding="utf-8")
    srt = next((tap / t for t in ("voice.srt", "voice_paced.srt") if (tap / t).exists()), None)
    if srt:
        cues = [(a, min(b, T), t) for a, b, t in _doc_cue(srt) if a < T]
        (hook / "hook_voice.srt").write_text(
            "\n".join(f"{i}\n{_tc(a)} --> {_tc(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)), encoding="utf-8")
    print(f"hook neo theo câu: {len(shots)} cảnh = câu 1–{truoc} của giọng thân → T = {T:.2f}s "
          f"(cắt hook_voice.mp3/srt/roles từ voice.mp3)")
    return True


def dung(tap: Path, xem_thu: bool, tate=None, bubble=None):
    hook = tap / "hook"
    if not xem_thu:
        neo_lai_theo_cau(tap)
    tl = json.loads((hook / "hook_timeline.json").read_text(encoding="utf-8"))
    shots = tl["shots"]
    thieu = [s["clip"] for s in shots if not (hook / s["clip"]).exists()]
    if thieu:
        sys.exit(f"✗ thiếu {len(thieu)} clip {thieu} — hook BẮT BUỘC là video, máy 1 phải gửi đủ")
    voice = hook / "hook_voice.mp3"
    if not voice.exists():
        sys.exit(f"✗ thiếu {voice}")
    T = shots[-1]["t1"]
    if xem_thu:
        W, H, fps, final, gain = 1920, 1080, 30.0, None, 0.0
    else:
        final = tap / "final.mp4"
        if not final.exists():
            sys.exit(f"✗ thiếu {final}")
        _, W, H, fps = probe(final)
        lf, lh = lufs(final, 180), lufs(voice)
        gain = round((lf - lh), 2) if (lf is not None and lh is not None) else 0.0
        print(f"mức tiếng: thân {lf} LUFS · giọng hook {lh} LUFS → chỉnh hook {gain:+.2f} dB")
    COVER = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={fps:g}"
    ins, vf = [], []
    for i, s in enumerate(shots):
        d = round(s["t1"] - s["t0"], 3)
        c = hook / s["clip"]
        k = max(1.0, d / (probe(c)[0] - 0.05))   # clip ngắn hơn đoạn cần → giãn chậm, không đóng khung
        ins += ["-i", str(c)]
        vf.append(f"[{i}:v]setpts={k:.4f}*PTS,{COVER},trim=duration={d},setpts=PTS-STARTPTS[v{i}]")
    n = len(shots)
    vf.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vh0]")
    if bubble and not xem_thu:
        # Lane K (2026-09-24): thân video dùng hộp lời kể + BÓNG THOẠI có đuôi (bong_thoai.py) → hook cùng kiểu.
        # Vị trí mặt: hỏi vision trên chính ảnh hook (hook/img/NNN.png), cast lấy từ shot["cast"] của timeline.
        import bong_thoai
        roles = hook / "hook_voice_roles.json"
        if not roles.exists():
            sys.exit("✗ bubble cần hook/hook_voice_roles.json (lồng tiếng hook bằng tts_voicevox)")
        chars = {c["id"]: c for c in json.loads((tap / "characters.json").read_text(encoding="utf-8")).get("characters", [])}
        viec = {s["img"]: (hook / s["img"], [x for x in (s.get("cast") or "").split(",") if x]) for s in shots}
        fj = hook / "img_faces_hook.json"
        bong_thoai.do_mat_ds(viec, chars, fj)
        tl_anh = [(s["img"], s["t0"], s["t1"]) for s in shots]
        tp = hook / "_bubble_hook.mov"
        bong_thoai.build_track(roles, tl_anh, fj, tp, W, H, int(round(fps)), bubble, total_dur=T,
                               tmp_dir=hook / "_bubble_frames")
        ins += ["-i", str(tp)]
        vf.append(f"[vh0][{n}:v]overlay=eof_action=pass[vh]")
        n_extra = 1
    elif tate and not xem_thu:
        # Thân video cháy hộp chữ dọc (assemble.tate) → đoạn hook PHẢI cùng kiểu chữ (QUY_TAC_VIDEO_HOOK §2).
        import tate_text
        tp = hook / "_tate_hook.mov"
        tate_text.build_track(hook / "hook_voice.srt", tp, W, H, int(round(fps)), tate.get("side", "left"),
                              tate.get("font_narration", "Yu Mincho"), tate.get("font_dialogue", "Yu Gothic"),
                              tate.get("font_size", 42), tate.get("max_chars_per_col", 14), tate.get("max_cols", 2),
                              total_dur=T, tmp_dir=hook / "_tate_frames")
        ins += ["-i", str(tp)]
        vf.append(f"[vh0][{n}:v]overlay=eof_action=pass[vh]")
        n_extra = 1
    elif xem_thu:
        vf.append("[vh0]subtitles=hook_vi.srt:force_style='FontName=Segoe UI,FontSize=20,Bold=1,Outline=2,Shadow=0,MarginV=40'[vh]")
        n_extra = 0
    else:
        vf.append("[vh0]null[vh]")
        n_extra = 0
    n += n_extra
    ai = n
    ins += ["-i", str(voice)]
    au, mix = [f"[{ai}:a]apad=whole_dur={T}[a0]"], ["[a0]"]
    for j, s in enumerate(tl.get("sfx", []), 1):
        ins += ["-i", str(hook / s["file"])]
        ms = int(s["t"] * 1000)
        au.append(f"[{ai + j}:a]volume={s['vol']},adelay={ms}|{ms}[a{j}]"); mix.append(f"[a{j}]")
    j = len(tl.get("sfx", [])) + 1
    nen = tl.get("nen")
    if nen:
        ins += ["-stream_loop", "-1", "-i", str(hook / nen["file"])]
        au.append(f"[{ai + j}:a]volume={nen['vol']},atrim=duration={T},"
                  f"afade=t=out:st={max(0, T - nen['fade_out_s'])}:d={nen['fade_out_s']}[a{j}]")
        mix.append(f"[a{j}]")
    au.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,atrim=duration={T},"
              f"volume={gain}dB,aresample=48000,aformat=channel_layouts=stereo[ah]")
    thay_hinh = (not xem_thu) and _script_mo_bang_hook(tap)
    if xem_thu:
        out = hook / "hook_preview_vi.mp4"
        maps = ["-map", "[vh]", "-map", "[ah]"]
        cmd_cwd = hook
        # đường dẫn subtitles= tương đối → chạy trong thư mục hook
    elif thay_hinh:
        # CHẾ ĐỘ THAY HÌNH (Lane K 2026-09-24): script.txt ĐÃ mở bằng hook → thân video đã ĐỌC hook ở 0..T.
        # Nối trước sẽ nghe hook 2 lần → thay vào đó PHỦ đoạn hook (clip + bóng thoại) lên T giây đầu của final.mp4,
        # giữ tiếng thân (giọng hook trong thân trùng mốc tuyệt đối vì cùng engine), chỉ trộn thêm SFX/nền.
        # Tổng độ dài = đúng độ dài final.mp4.
        fi = len([x for x in ins if x == "-i"])
        ins += ["-i", str(final)]
        vf.append(f"[{fi}:v]{COVER}[vb];[vb][vh]overlay=eof_action=pass:enable='lte(t,{T})'[vout]")
        au[0] = f"[{fi}:a]aresample=48000,aformat=channel_layouts=stereo[a0]"   # tiếng THÂN thay giọng hook riêng
        au[-1] = ("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,"
                  f"aresample=48000,aformat=channel_layouts=stereo[aout]")
        out = tap / "final_with_hook.mp4"
        maps = ["-map", "[vout]", "-map", "[aout]"]
        cmd_cwd = hook
        print(f"chế độ THAY HÌNH: script.txt đã mở bằng hook → phủ clip lên {T:.2f}s đầu, giữ tiếng thân")
    else:
        fi = len([x for x in ins if x == "-i"])
        ins += ["-i", str(final)]
        vf.append(f"[{fi}:v]{COVER}[vb]")
        au.append(f"[{fi}:a]aresample=48000,aformat=channel_layouts=stereo[ab]")
        vf.append("[vh][ah][vb][ab]concat=n=2:v=1:a=1[vout][aout]")
        out = tap / "final_with_hook.mp4"
        maps = ["-map", "[vout]", "-map", "[aout]"]
        cmd_cwd = hook
    subprocess.run([FF, "-y", "-v", "error", *ins, "-filter_complex", ";".join(vf + au), *maps,
                    "-map_metadata", "-1", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True, cwd=str(cmd_cwd))
    d_out = probe(out)[0]
    if xem_thu:
        print(f"✓ {out} · {d_out:.2f}s")
        return
    d_final = probe(final)[0]
    ky_vong = d_final if thay_hinh else d_final + T
    print(f"✓ {out} · {d_out:.2f}s (kỳ vọng {ky_vong:.2f}s = "
          + (f"đúng độ dài thân, hook phủ {T:.2f}s đầu)" if thay_hinh else f"hook {T:.2f}s + thân {d_final:.2f}s)"))
    if abs(d_out - ky_vong) > 0.5:
        sys.exit("✗ độ dài lệch > 0,5s — KHÔNG giao, báo máy 1")
    lh2 = lufs(out, T)
    print(f"  nghiệm thu mức tiếng: đoạn hook {lh2} LUFS (thân gốc {lufs(final, 180)} LUFS)")
    # B10 (qc_final.kiem_hook) đòi bản ghi này — ghi ngay khi ghép xong, không để người chạy tự ghi.
    (hook / "render_info.json").write_text(json.dumps({
        "mode": "thay_hinh" if thay_hinh else "noi_truoc", "T_hook": round(T, 3), "shots": len(shots),
        "out": out.name, "dur_out": round(d_out, 3), "dur_final": round(d_final, 3), "fps": fps, "w": W, "h": H},
        ensure_ascii=False, indent=1), encoding="utf-8")
    if thay_hinh:
        print("  phụ đề: dùng nguyên voice.srt (mốc không đổi vì hook nằm trong thân)")
        return
    # Phụ đề đi kèm final_with_hook.mp4: hook_voice.srt + (srt thân dời +T). File srt cũ GIỮ NGUYÊN cho final.mp4.
    for ten in ("voice_paced.srt", "voice.srt", "phude.srt"):
        src = tap / ten
        if src.exists():
            dst = tap / (Path(ten).stem + "_with_hook.srt")
            dst.write_bytes(noi_srt(hook / "hook_voice.srt", src, T).encode("utf-8"))
            print(f"  ✓ {dst.name} (hook + {ten} dời +{T:.2f}s)")


def _script_mo_bang_hook(tap):
    """script.txt đã chứa hook ở đầu (lean flow chép nguyên văn hook làm đoạn đầu) → True."""
    s, h = tap / "script.txt", tap / "hook" / "hook_locked.txt"
    if not (s.exists() and h.exists()):
        return False
    chuan = lambda t: re.sub(r"\s", "", t)
    return chuan(s.read_text(encoding="utf-8")).startswith(chuan(h.read_text(encoding="utf-8"))[:60])


def _doc_cue(p):
    out = []
    for blk in re.split(r"\n\s*\n", Path(p).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").strip()):
        ln = blk.strip().split("\n")
        i = next((k for k, x in enumerate(ln) if "-->" in x), None)
        if i is None:
            continue
        a, b = [x.strip() for x in ln[i].split("-->")]
        out.append((_giay(a), _giay(b), "\n".join(ln[i + 1:])))
    return out


def _giay(s):
    h, m, r = s.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(r)


def _tc(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def noi_srt(hook_srt, than_srt, T):
    cues = [(a, b, t) for a, b, t in _doc_cue(hook_srt)] + [(a + T, b + T, t) for a, b, t in _doc_cue(than_srt)]
    return "\n".join(f"{i}\n{_tc(a)} --> {_tc(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tap", required=True)
    ap.add_argument("--xem-thu", action="store_true")
    ap.add_argument("--profile", default="", help="id lane; profile khai assemble.tate.enabled → hook cháy cùng hộp chữ dọc với thân")
    a = ap.parse_args()
    tate = None
    if a.profile:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import profiles
        t = (profiles.load(a.profile).get("assemble") or {}).get("tate") or {}
        tate = t if t.get("enabled") else None
        b = (profiles.load(a.profile).get("assemble") or {}).get("bubble") or {}
        bubble = b if b.get("enabled") else None
        print(f"profile {a.profile}: chữ dọc hook = {'BẬT' if tate else 'tắt'} · bóng thoại hook = {'BẬT' if bubble else 'tắt'}")
    else:
        bubble = None
    # resolve(): ffmpeg chạy với cwd=hook\ → đường dẫn tương đối (vd ..\assets\...) hỏng (Lane L ep01 2026-09-24)
    dung(Path(a.tap).resolve(), a.xem_thu, tate, bubble)


if __name__ == "__main__":
    main()
