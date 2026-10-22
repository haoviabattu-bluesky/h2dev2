# -*- coding: utf-8 -*-
"""Ghép BẢN XEM THỬ hook CÓ GIỌNG (clip Grok + giọng ai33 theo vai + nhạc nền + phụ đề Nhật/Việt TỪNG CÂU)
cho ANH KIỂM giọng — KHÔNG phải hàng giao máy 2 (máy 2 vẫn tự lồng giọng hook).

Khác xem_thu_hook.py: thời lượng shot = độ dài giọng THẬT (không ước char_rate); phụ đề đổi theo từng câu
(shot gộp 2 câu không còn mất câu dịch thứ 2). Giọng mỗi câu lấy theo <tập>/vai.txt (`số|vai|câu`):
vai có voice trong characters.json → giọng đó; `ke`/vai không có voice → giọng người kể của profile.

    py -3.13 -X utf8 xem_thu_hook_giong.py --profile <lane> --hook <thư mục hook>
→ <thư mục tập>/XEM_THU_hook_giong_phude_VI.mp4 · cache giọng <thư mục tập>/_xem_thu_giong/ (chạy lại không tốn credit)
"""
import argparse, hashlib, json, shutil, sys, wave
import imageio_ffmpeg
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xem_thu_hook import FF, W, H, ROOT, ff, overlay   # noqa: E402

sys.path.insert(0, str(ROOT / "pipeline"))
import cau_vai           # noqa: E402
import openspeaker_tts   # noqa: E402



def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--hook", required=True)
    ap.add_argument("--out", default="", help="tên file mp4 ra (mặc định XEM_THU_hook_giong_phude_VI.mp4; dùng khi file cũ đang mở bị khoá)")
    a = ap.parse_args()
    hd = Path(a.hook); tap = hd.parent
    prof = json.loads((ROOT / "profiles" / "profiles" / f"{a.profile}.json").read_text(encoding="utf-8"))
    v = prof["voice"]
    if (tap / "characters.json").exists():   # 22/10: giọng vai theo kho chung khung tuổi (y máy 2 lồng thân bài) trước khi đọc thử
        import kho_giong
        kho_giong.chan(dict(prof, id=prof.get("id") or a.profile), tap / "characters.json")
    speed = float(v.get("speed", 1.0))
    # 2026-10-03 (Lane O ep01): lane VOICEVOX (voice.provider) không có voice_id ai33 → đọc bằng engine local :50021,
    # giọng theo speaker/style của characters.json (tts_voicevox.giong_cua_vai), y như máy 2 lồng giọng thân.
    vvx = (v.get("provider") or "").lower() == "voicevox"
    if vvx:
        import tts_voicevox
        import numpy as np
        ban, sty = tts_voicevox.giong_cua_vai(prof, tap / "characters.json"), tts_voicevox._style_map()
        ke_voice = cau_vai.KE
        voice_of = {r: r for r in ban}
    else:
        ke_voice = (v.get("narrator") or {}).get("voice_id") or v["id"]
        chars = json.loads((tap / "characters.json").read_text(encoding="utf-8"))["characters"]
        voice_of = {c["id"]: (c.get("voice") or {}).get("voice_id") for c in chars if c.get("id")}
        # 2026-10-04 (Lane L ep09): speed/fx RIÊNG từng vai (characters.json voice.speed/.fx) y như máy 2 lồng giọng thân
        # (tts_voicevox: g.get("speed", speed) + ap_fx) — vd giọng trưởng phòng QUÁT.
        rieng = {c["id"]: c.get("voice") or {} for c in chars if c.get("id")}
    vai = {}
    if (tap / "vai.txt").exists():
        for ln in (tap / "vai.txt").read_text(encoding="utf-8").splitlines():
            if ln.count("|") >= 2:
                n, r, t = ln.split("|", 2)
                vai[int(n)] = (r.strip(), t.strip())
    tl = json.loads((hd / "hook_timeline.json").read_text(encoding="utf-8"))
    if not vai:   # lane 1 giọng (vd Lane F): không có vai.txt → câu hook cắt theo cau_vai, mọi câu = người kể
        # 2026-10-03 (Lane F ep10): shot có thể cắt GIỮA câu (ranh giới ở dấu 、) → tách câu trong TỪNG shot, không tách cả hook.
        for s in tl["shots"]:
            for c in cau_vai.tach_cau(s["voice"]):
                vai[len(vai) + 1] = (cau_vai.KE, c["text"])
    vi = json.loads((hd / "phu_de_vi.json").read_text(encoding="utf-8"))
    # tach_cau bỏ dấu 。 sau 」 (「…」。) → so khớp không tính 。
    _so = lambda x: cau_vai._chuan(x).replace("。", "")
    k = 1
    for s in tl["shots"]:
        if "cau" not in s and s.get("lang_s"):   # 12/10 (Lane L ep15): shot LẶNG — chỉ hình + motion, không câu
            continue
        if "cau" not in s:   # lane 1 giọng cấm khoá `cau` trong timeline (máy 2 sẽ đòi voice_roles) → tự suy theo voice, chỉ trong RAM
            a_, gop = k, ""
            while _so(gop) != _so(s["voice"]) and k in vai:
                gop += vai[k][1]; k += 1
            s["cau"] = [a_, k - 1]
        a_, b_ = s["cau"]; k = b_ + 1
        assert _so("".join(vai[i][1] for i in range(a_, b_ + 1))) == _so(s["voice"]), f"vai.txt lệch hook ở shot {s['n']}"
    caus = [i for s in tl["shots"] if "cau" in s for i in range(s["cau"][0], s["cau"][1] + 1)]
    # 2026-10-06 (Lane O ep04, anh: "chưa có dừng nghỉ / nghỉ quá ngắn"): bỏ GAP cố định 0,35s → khoảng lặng theo
    # ĐÚNG luật giọng thân máy 2 (cau_vai.khe_nghi: câu ≥0,5s · đoạn ≥1,1s · mảnh câu 0,2s · `nghi_doan_sau`).
    nghi_cau, nghi_doan = float(v.get("pause_sentence_ms", 350)) / 1000, float(v.get("pause_para_ms", 700)) / 1000
    hk = cau_vai.tach_cau((hd / "hook_locked.txt").read_text(encoding="utf-8")) if (hd / "hook_locked.txt").exists() else []
    if [_so(c["text"]) for c in hk] == [_so(vai[i][1]) for i in caus]:
        meta = {i: dict(c, i=i) for i, c in zip(caus, hk)}
    else:   # hook_locked lệch số câu (hook nối trước tự cắt) → mỗi câu 1 dòng, cùng khối
        meta = {i: {"i": i, "para": i, "khoi": 1, "text": vai[i][1]} for i in caus}
    doan_them = {int(x) for x in tl.get("nghi_doan_sau") or []}
    khe = {i: cau_vai.khe_nghi(meta[i], meta.get(caus[j + 1]) if j + 1 < len(caus) else None, nghi_cau, nghi_doan,
                               doan_them=doan_them) for j, i in enumerate(caus)}
    # 12/10: shot có lời khai `nghi_sau_s` = giữ hình sau câu cuối (dừng ngắn cho thẻ tên) — y máy 2 (cau_vai.lang_hook).
    for s in tl["shots"]:
        if "cau" in s and s.get("nghi_sau_s"):
            khe[s["cau"][1]] += float(s["nghi_sau_s"])

    cache = tap / "_xem_thu_giong"; cache.mkdir(exist_ok=True)
    tmp = hd / "_xem_thu_g"; tmp.mkdir(exist_ok=True)

    def tts(i):
        role, text = vai[i]
        vid = voice_of.get(role) or ke_voice
        wav = tmp / f"cau_{i:02d}.wav"
        # 2026-10-05 Lane O ep04: lane VOICEVOX có vai lẻ đọc bằng ai33 (voice.voice_id + speed/fx) — y tts_voicevox
        if vvx and not ban[vid].get("voice_id"):
            g = ban[vid]
            pcm, sr = tts_voicevox._tong_hop(text, sty[(g["speaker"], g.get("style") or "ノーマル")],
                                             float(g.get("speed") or speed), float(v.get("pre_s", 0.1)), float(v.get("post_s", 0.1)))
            raw = tmp / f"cau_{i:02d}_raw.wav"
            with wave.open(str(raw), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.asarray(pcm, dtype=np.int16).tobytes())
            ff("-i", raw, "-ar", "44100", "-ac", "1", wav)
            return i, role, g["speaker"], wav
        if vvx:
            g = ban[vid]
            if not v.get("ai33_cho_vai"):
                raise SystemExit(f"✗ lane VOICEVOX chưa bật voice.ai33_cho_vai mà vai {role} khai voice_id ai33")
            vid = g["voice_id"]
        else:
            g = rieng.get(role) or {}
        sp = float(g.get("speed") or speed)
        # 2026-10-04 (Lane F ep12 đổi cách tách câu khi sang đa giọng): khoá cache theo CẢ chữ câu — chỉ theo số câu
        # thì câu đánh số lại sẽ lấy nhầm giọng câu cũ (đo thật: câu 11 ngắn ra 6,9s).
        mp3 = cache / f"cau_{i:02d}_{vid}_{sp}_{hashlib.md5(text.encode('utf-8')).hexdigest()[:8]}.mp3"
        if not mp3.exists():
            audio, _ = openspeaker_tts.synthesize(text, vid, sp, with_transcript=False, file_name=f"hook_cau{i}")
            mp3.write_bytes(audio)
        wav = tmp / f"cau_{i:02d}.wav"
        ff("-i", mp3, *(["-af", g["fx"]] if g.get("fx") else []), "-ar", "44100", "-ac", "1", wav)
        return i, role, vid, wav

    with ThreadPoolExecutor(int(v.get("workers", 6))) as ex:
        res = {i: (r, vid, w) for i, r, vid, w in ex.map(tts, caus)}

    # 16/10 (Lane L ep19, anh: thẻ tên giật/mất đoạn hiện ra): mỗi seg encode -t loc ở 30fps bị làm tròn khung → cộng dồn
    # float loc lệch dần với video thật (tới cảnh 8 lệch ~0,25s) → thẻ tên/giọng đặt sai khung. Cộng ĐỘ DÀI THẬT (số khung/30).
    def _dai_that(seg, loc):
        try:
            return imageio_ffmpeg.count_frames_and_secs(str(seg))[0] / 30
        except Exception:
            return loc
    t, segs, voice_in, voice_fl = 0.0, [], [], []
    the = []   # (file thẻ tên, giây bắt đầu)
    het = {}   # số cảnh → giây kết thúc cảnh
    for s in tl["shots"]:
        if "cau" not in s:   # shot LẶNG: lang_s giây của clip (motion đã cháy sẵn trong clip), không giọng, không phụ đề
            loc = float(s["lang_s"])
            seg = tmp / f"seg_{s['n']:02d}.mp4"
            ff("-i", hd / s["clip"], "-vf", f"scale={W}:{H},setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=30",
               "-t", f"{loc:.3f}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", seg)
            if (s.get("the_ten") or {}).get("file"):
                tre = float(s["the_ten"].get("tre_s") or 0)
                the.append((hd / s["the_ten"]["file"], t + tre, loc - tre, s["the_ten"].get("den_shot")))
            print(f"  → shot {s['n']} · LẶNG {loc:.1f}s")
            segs.append(seg); t += _dai_that(seg, loc); het[s["n"]] = t
            continue
        n, (a_, b_) = s["n"], s["cau"]
        loc, filt, ins = 0.0, "", ["-i", hd / s["clip"]]
        # 2026-10-10 (Lane O ep05): shot dài hơn clip → GIÃN CHẬM clip như máy 2 dựng thật (ghep_hook_noi_truoc:
        # setpts=k*PTS, k = độ dài shot / (độ dài clip − 0,05)) thay vì đứng khung cuối — bản duyệt giống bản giao.
        dai = sum(wav_len(res[i][2]) + khe[i] for i in range(a_, b_ + 1))
        k_ = max(1.0, dai / (imageio_ffmpeg.count_frames_and_secs(str(hd / s["clip"]))[1] - 0.05))
        filt = f"[0:v]setpts={k_:.4f}*PTS,scale={W}:{H},setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=30[v0]"
        for k, i in enumerate(range(a_, b_ + 1), 1):
            role, vid, wav = res[i]
            d = wav_len(wav)
            png = tmp / f"sub_{i:02d}.png"
            overlay(png, vai[i][1], vi.get(str(i), "(chưa dịch)"))
            ins += ["-i", png]
            end = loc + d + khe[i]
            filt += f";[v{k-1}][{k}:v]overlay=0:0:enable='between(t,{loc:.3f},{end:.3f})'[v{k}]"
            voice_in += ["-i", wav]
            voice_fl.append((len(voice_fl) + 1, t + loc))
            print(f"câu {i:2d} · {role:8s} · {vid} · {d:4.1f}s +nghỉ {khe[i]:.2f}s · {vai[i][1]}")
            loc = end
        if (s.get("the_ten") or {}).get("file"):
            tre = float(s["the_ten"].get("tre_s") or 0)
            the.append((hd / s["the_ten"]["file"], t + tre, loc - tre, s["the_ten"].get("den_shot")))   # (file, giây bắt đầu, phần cảnh còn lại, giữ tới cảnh)
        seg = tmp / f"seg_{n:02d}.mp4"
        ff(*ins, "-filter_complex", filt, "-map", f"[v{b_ - a_ + 1}]", "-t", f"{loc:.3f}", "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", seg)
        print(f"  → shot {n} · {loc:.1f}s{'  · clip giãn chậm x' + format(k_, '.2f') if k_ > 1 else ''}{'  ⚠ giãn >1,6 lần — cân nhắc tách cảnh' if k_ > 1.6 else ''}")
        segs.append(seg); t += _dai_that(seg, loc); het[s["n"]] = t
    # 12/10: thẻ khai `den_shot` → giữ tới hết cảnh đó (đóng băng + cảnh nhân vật nói), không cắt ở cuối cảnh đóng băng
    the = [(f, st, (het[den] - st) if den in het else con) for f, st, con, den in the]
    for f, st, con in the:
        print(f"  ▣ thẻ {f.name}: {st:.1f}s → {st + con:.1f}s")
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    video = tmp / "video.mp4"
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video)
    # 2026-10-10 (Lane O ep05, anh: giới thiệu nhân vật bằng thẻ chữ trên ảnh, không đọc): shot có `the_ten.file`
    # = thẻ tên động nền trong suốt (webm VP9 alpha, render HyperFrames) chồng lên CẢ video từ đầu shot (+tre_s),
    # được phép kéo sang shot sau — y cách máy 2 chồng trong ghep_hook_noi_truoc.py. Giải mã bằng libvpx-vp9
    # (bộ giải mã mặc định bỏ alpha → hộp đen).
    if the:
        # 2026-10-12 (Lane L ep15): nhiều thẻ trong CÙNG 1 đồ thị ffmpeg → thẻ thứ 3–4 (giây 30–40) không hiện / ffmpeg treo
        # (đo thật) → chồng TỪNG thẻ một lượt riêng, y máy 2 (ghep_hook_noi_truoc).
        for j, (f, st, con) in enumerate(the, 1):
            # 10/10 (Lane O ep06: thẻ 6s tràn sang cảnh sau, chồng thẻ người khác): thẻ dài hơn phần cảnh còn lại → cắt
            # ở cuối cảnh + mờ dần 0,35s — y máy 2 (ghep_hook_noi_truoc).
            dai_the = imageio_ffmpeg.count_frames_and_secs(str(f))[1]
            # 17/10 (Lane M ep15): `trim` trong nhánh thẻ làm ffmpeg 7.1 TREO vĩnh viễn ở giây thẻ bắt đầu (0% CPU, đo thật)
            # → bỏ trim, chỉ mờ dần alpha về 0 (sau mốc cắt thẻ trong suốt hoàn toàn = như đã cắt).
            cat = (f"fade=t=out:st={max(0, con - 0.35):.3f}:d=0.35:alpha=1,"
                   if con < dai_the - 0.05 else "")
            # 16/10 (Lane L ep19, anh: motion thẻ tên bị GIẬT): webm 30fps tb 1/1000 (pts 33/67ms làm tròn) chồng lên video 30fps
            # → overlay lấy lệch khung (lặp 1 khung, bỏ 1 khung). Ép thẻ về đúng lưới fps của video TRƯỚC khi dời giờ.
            video2 = tmp / f"video_the{j % 2}.mp4"
            ff("-i", video, "-c:v", "libvpx-vp9", "-i", f, "-filter_complex",
               f"[1:v]scale={W}:{H},format=yuva420p,{cat}setpts=PTS-STARTPTS,fps=30,setpts=PTS+{st:.3f}/TB[tt];[0:v][tt]overlay=0:0:eof_action=pass[v]",
               "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", video2)
            video = video2

    ins, fl = ["-i", video] + voice_in, []
    for k, st in voice_fl:
        fl.append(f"[{k}:a]adelay={int(st * 1000)}:all=1[a{k}]")
    k = len(voice_fl) + 1
    nen = tl.get("nen")
    if nen:
        ins += ["-stream_loop", "-1", "-i", hd / nen["file"]]
        fo = float(nen.get("fade_out_s", 1.5))
        fl.append(f"[{k}:a]volume={nen.get('vol', 0.2)},atrim=0:{t:.2f},afade=t=out:st={max(0, t - fo):.2f}:d={fo}[a{k}]"); k += 1
    mix = "".join(f"[a{i}]" for i in range(1, k)) + f"amix=inputs={k - 1}:normalize=0:duration=longest,atrim=0:{t:.2f}[a]"
    out = tap / (a.out or "XEM_THU_hook_giong_phude_VI.mp4")
    ff(*ins, "-filter_complex", ";".join(fl + [mix]), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-shortest", out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ {out} · {t:.1f}s")


if __name__ == "__main__":
    main()
