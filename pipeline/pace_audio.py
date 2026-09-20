"""pace_audio.py — GIÃN NHỊP lời kể cho giọng người già (chèn khoảng nghỉ giữa cue).

Vì sao (user chốt 2026-09-08, skill youtube-script §GIÃN NHỊP): TTS đọc gần như liền một mạch
(OpenSpeaker đo thật ~0,14s nghỉ/cue) → người nghe (nhất là khán giả già Satori) MỆT, không kịp
lắng nghe/suy nghĩ/nhớ. Phải có khoảng nghỉ sau mỗi câu + nghỉ dài khi chuyển đoạn/cảnh.

Khác VIDEO_VEO3 (sinh audio từng đoạn + atempo → bẫy atempo trôi SRT): pipeline này có 1 mp3 LIỀN
(đã chậm sẵn speed 0.92 ở OpenSpeaker) + voice.srt. Cách chắc: CẮT mp3 tại ranh cue, CHÈN im lặng
theo luật, ghép lại, dựng SRT từ ĐỘ DÀI ĐO ĐƯỢC (mẫu chính xác) → KHÔNG dùng atempo nên KHÔNG trôi.

Luật nghỉ (quyết định bằng CHÍNH VĂN BẢN):
  - cue text kết thúc 。？！ (hết câu)        → 0,65s
  - cue giữa câu (xuống dòng giữa chừng)      → 0,20s
  - cue là CUỐI ĐOẠN script (trước \\n\\n)    → 1,50s  (chặn trần 25% số cue)
  - 0,5s im lặng đầu video để vào nhịp
Mục tiêu tỉ lệ NÓI 82-87% (TTS thô ~96%). Chèn im lặng SẠCH thay cho khe tự nhiên (giữ đủ tiếng nói).

Dùng (SAU srt_from_script.py, TRƯỚC assemble):
  py -3.13 pace_audio.py --audio <slug>/voice.mp3 --srt <slug>/voice.srt --script <slug>/script.txt
  → voice_paced.wav + voice_paced.srt (assemble dùng 2 file này). --sentence/--mid/--para chỉnh giây.
"""
import argparse
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import imageio_ffmpeg

sys.stdout.reconfigure(encoding="utf-8")

_TS = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d+)")
_SENT_END = "。．.！!？?」』】"          # ký tự kết câu (gồm đóng ngoặc thoại)


def _sec(ts):
    h, m, s, ms = _TS.match(ts).groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / (10 ** len(ms))


def _ts(sec):
    ms = round(sec * 1000)
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(txt):
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        L = blk.splitlines()
        tl = next((x for x in L if "-->" in x), None)
        if not tl:
            continue
        a, b = tl.split("-->")
        i = L.index(tl)
        out.append((_sec(a.strip()), _sec(b.strip()), "".join(L[i + 1:]).strip()))
    return out


def _norm(s):
    return re.sub(r"\s+", "", s)


def het_cau(txt):
    """Cue này có kết thúc một câu không? Chỉ chỗ này mới được phép chèn khoảng nghỉ."""
    return bool(txt) and txt.rstrip()[-1:] in _SENT_END


def _hut_ve_het_cau(flags, ket, cua_so=8):
    """Kéo mỗi mốc nghỉ dài về cue GẦN NHẤT thật sự kết thúc câu.

    Vì sao bắt buộc (lỗi thật, video simbot2-vU5PWT2zLDs 2026-09-09): ranh đoạn được dóng theo
    TỈ LỆ ký tự nên nó rơi vào bất kỳ cue nào — mà 63% cue của STT bị cắt GIỮA CÂU. Kết quả:
    52/93 chỗ nghỉ 1,5s nằm giữa câu, ~78 giây im lặng đặt sai chỗ. Nghe đúng như nấc cụt:

        ...長年、  ][ im lặng 1,5s ][  仕立てと手芸の店を営んでいた...

    (nghỉ một giây rưỡi ngay sau dấu phẩy). Hút về cuối câu gần nhất — không tìm được trong
    cửa sổ thì BỎ mốc đó, thà thiếu một chỗ nghỉ còn hơn cắt ngang câu.
    """
    ra = [False] * len(flags)
    for i, f in enumerate(flags):
        if not f:
            continue
        if ket[i]:
            ra[i] = True
            continue
        for d in range(1, cua_so + 1):               # ưu tiên tiến tới trước, rồi mới lùi lại
            for j in (i + d, i - d):
                if 0 <= j < len(flags) and ket[j] and not ra[j]:
                    ra[j] = True
                    break
            else:
                continue
            break
    return ra


def para_end_flags(cues, script):
    """Cue nào là CUỐI 1 ĐOẠN script.

    ⚠️ KHÔNG so offset ký tự tuyệt đối: voice.srt do STT sinh nên NGẮN HƠN kịch bản (đo thật ep10:
    7.614 vs 8.353 = −8,8%) → offset trôi 3-12 ký tự, dung sai 2 ký tự KHÔNG BAO GIỜ khớp, kết quả
    0/11 ranh đoạn được nhận ra. So theo TỈ LỆ thì miễn nhiễm với sai lệch đó.

    Dóng theo tỉ lệ vẫn còn sai vài cue, nên bước cuối PHẢI hút về cuối câu (`_hut_ve_het_cau`).
    """
    paras = [p for p in re.split(r"\n\s*\n", script) if p.strip()]
    n_sc = sum(len(_norm(p)) for p in paras) or 1
    acc, fr_ends = 0, []
    for p in paras[:-1]:                             # bỏ đoạn cuối: hết bài, không cần nghỉ dài
        acc += len(_norm(p))
        fr_ends.append(acc / n_sc)
    n_srt = sum(len(_norm(t)) for _, _, t in cues) or 1
    flags = [False] * len(cues)
    acc, k = 0, 0
    for i, (_, _, t) in enumerate(cues):
        acc += len(_norm(t))
        while k < len(fr_ends) and acc / n_srt >= fr_ends[k]:   # cue đầu tiên chạm ranh đoạn
            flags[i] = True
            k += 1
    return _hut_ve_het_cau(flags, [het_cau(t) for _, _, t in cues])


def decode_pcm(mp3, sr=44100, ch=2):
    """Giữ nguyên STEREO: ép mono làm nhạc nền trộn ở bước ghép mất bề rộng âm thanh."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.run([ff, "-v", "error", "-i", str(mp3), "-ac", str(ch), "-ar", str(sr),
                        "-f", "wav", "-"], capture_output=True)
    import io
    w = wave.open(io.BytesIO(p.stdout), "rb")
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return a.reshape(-1, ch), sr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out-audio", default="")
    ap.add_argument("--out-srt", default="")
    ap.add_argument("--sentence", type=float, default=0.65)
    # 0 = KHÔNG chèn gì vào giữa câu (user chốt 2026-09-09: chỉ ngắt nghỉ ở chỗ chấm câu).
    # Cue của STT bị cắt tuỳ tiện — 63% cue không kết thúc câu — nên mọi khoảng nghỉ ở đó đều
    # rơi vào giữa mệnh đề, nghe như hụt hơi. Muốn thở nhẹ giữa câu thì tự đặt --mid 0.15.
    ap.add_argument("--mid", type=float, default=0.0)
    ap.add_argument("--para", type=float, default=1.50)
    ap.add_argument("--lead", type=float, default=0.50)
    ap.add_argument("--para-cap", type=float, default=0.25, help="trần tỉ lệ cue được nghỉ dài (1,5s)")
    ap.add_argument("--target-hi", type=float, default=0.87,
                    help="tỉ lệ NÓI tối đa; vượt thì tự nhân mức nghỉ lên cho tới khi đạt (0 = tắt)")
    ap.add_argument("--target-lo", type=float, default=0.82,
                    help="tỉ lệ NÓI tối thiểu; THẤP hơn thì tự CHIA mức nghỉ xuống cho tới khi đạt "
                         "(0 = tắt). Đối xứng với --target-hi — thiếu nhánh này thì script dài/nhiều "
                         "cue kết câu (nhiều 。) cộng dồn quá nhiều nghỉ mà không có gì kéo lại "
                         "(đo thật simbot2-02-vU5PWT2zLDs: speak_ratio 65% dù mức nghỉ vẫn ở k=1.0).")
    args = ap.parse_args()

    cues = parse_srt(Path(args.srt).read_text(encoding="utf-8"))
    script = Path(args.script).read_text(encoding="utf-8")
    audio, sr = decode_pcm(args.audio)
    nch = audio.shape[1]
    total_speak_in = sum(e - s for s, e, _ in cues)

    para = para_end_flags(cues, script)
    # chặn trần số cue nghỉ dài: nếu > cap, chỉ giữ những đoạn dài nhất (ở đây giữ hết vì đoạn ít)
    if sum(para) > len(cues) * args.para_cap:
        keep = int(len(cues) * args.para_cap)
        idx = [i for i, f in enumerate(para) if f][:keep]
        para = [i in set(idx) for i in range(len(cues))]

    def pause_for(i, txt, k):
        """Khoảng nghỉ MỤC TIÊU sau cue i, đã nhân hệ số k.

        LUẬT CỨNG: cue không kết thúc câu thì KHÔNG chèn gì (trừ khi user tự đặt --mid > 0).
        Đây là chốt chặn cuối — dù `para` có lỡ đánh dấu sai chỗ thì cũng không cắt ngang câu."""
        if i == len(cues) - 1:
            return 0.0
        if not het_cau(txt):
            return args.mid * k
        return (args.para if para[i] else args.sentence) * k

    def extras_for(k):
        out = []
        for i, (s, e, txt) in enumerate(cues):
            seg_end = cues[i + 1][0] if i + 1 < len(cues) else e
            out.append(max(0.0, pause_for(i, txt, k) - max(0.0, seg_end - e)))
        return out

    span = (cues[-1][1] if cues else 0) - (cues[0][0] if cues else 0)

    def ratio_for(k):
        return total_speak_in / (args.lead + span + sum(extras_for(k)))

    # TỰ DÒ hệ số nghỉ để tỉ lệ NÓI rơi vào dải mong muốn. Mức mặc định (0,65/0,20/1,50) chỉ đưa
    # ep10 về 90% vì khe TTS vốn đã 0,11s và chỉ 46% cue kết bằng dấu câu → phải nhân lên.
    # Trần hệ số: từ khi bỏ nghỉ giữa câu, mọi khoảng nghỉ dồn hết vào chỗ chấm câu — thả tự do
    # tới ×8 thì mỗi dấu chấm nghỉ hơn 5 giây, nghe như video bị đơ. Thà tỉ lệ NÓI cao hơn mục
    # tiêu một chút còn hơn ngắt quãng lê thê.
    K_TRAN = 2.2
    # Sàn hệ số CHIỀU NGƯỢC LẠI: script dài/nhiều cue kết câu (nhiều 。／／！／？) cộng dồn quá nhiều
    # nghỉ NGAY Ở k=1.0 mà không hề vượt target_hi — nhánh trên không bắt được vì nó chỉ kiểm tra
    # "vượt trần", không kiểm "dưới sàn". K_SAN=0.3 vẫn giữ chút nghỉ nghe được (0,65s→0,2s), không
    # về 0 hẳn — mất nghỉ hoàn toàn lại quay về đúng vấn đề gốc "TTS đọc liền một mạch".
    K_SAN = 0.3
    k = 1.0
    r1 = ratio_for(1.0)
    if args.target_hi and r1 > args.target_hi:
        lo, hi = 1.0, K_TRAN
        for _ in range(24):
            k = (lo + hi) / 2
            if ratio_for(k) > args.target_hi:
                lo = k
            else:
                hi = k
        k = hi
        print(f"  tự dò hệ số nghỉ ×{k:.2f} (THIẾU nghỉ) → câu {args.sentence*k:.2f}s · "
              f"giữa câu {args.mid*k:.2f}s · đoạn {args.para*k:.2f}s")
    elif args.target_lo and r1 < args.target_lo:
        # ratio_for(k) GIẢM khi k TĂNG (nghỉ nhiều hơn = nói ít lại theo tỉ lệ) → tìm k CÀNG GẦN
        # 1.0 CÀNG TỐT (giữ đúng tinh thần mức nghỉ gốc) mà vẫn đạt SÀN target_lo.
        lo, hi = K_SAN, 1.0
        for _ in range(24):
            k = (lo + hi) / 2
            if ratio_for(k) >= args.target_lo:
                lo = k                # vẫn đạt sàn → thử k lớn hơn (gần 1.0 hơn)
            else:
                hi = k                # dưới sàn → phải giảm k nữa
        k = lo
        print(f"  tự dò hệ số nghỉ ×{k:.2f} (THỪA nghỉ, {r1:.0%} < sàn {args.target_lo:.0%}) → "
              f"câu {args.sentence*k:.2f}s · giữa câu {args.mid*k:.2f}s · đoạn {args.para*k:.2f}s")

    def sil(sec):
        return np.zeros((int(sec * sr), nch), dtype=np.int16)

    def diem_cat_an_toan(t_khai_bao, tim_lui=0.4, buoc=0.01, nguong_db=-40.0):
        """STT khai bao cue MOI bat dau MUON HON luc tu do THAT SU vang len.

        Lỗi thật (2026-09-09, user nghe ra: "chữ bị cắt làm đôi, kẹp im lặng ở giữa"). Đo trực
        tiếp mức âm thanh từng 20ms: STT khai cue "長年、" bắt đầu lúc 14.24s, nhưng âm lượng đã
        vọt từ -59dB (im lặng) lên -14dB (đang nói to) ngay từ 14.10s — **STT trễ 140ms so với
        âm thanh thật**. Cắt đúng lúc STT khai (14.24s) để chèn khoảng nghỉ nghĩa là 140ms đầu
        của từ đã bị nuốt vào cuối đoạn TRƯỚC khi im lặng ập vào, rồi đoạn SAU phát tiếp phần còn
        lại — nghe đúng như một từ bị cắt làm đôi, kẹp im lặng ở giữa. Đo lại ở mốc 24.00s (khác
        hẳn vị trí) ra cùng hiện tượng — không phải trường hợp lẻ, là lệch hệ thống của STT.

        Fix: CHỈ cắt ở đây khi thật sự sắp chèn thêm im lặng (ex[i] > 0). Tìm ngược từ mốc STT
        khai về một khoảng (mặc định 0,4s) để lấy điểm GẦN NHẤT âm thanh THẬT SỰ im lặng — dùng
        chính sóng âm làm trọng tài, không tin timestamp STT. Không tìm được (nói liền không có
        khe) thì giữ nguyên mốc cũ, không tệ hơn trước."""
        win = max(1, int(sr * buoc))
        nguong = 10 ** (nguong_db / 20) * 32768.0
        i_khai = int(t_khai_bao * sr)
        i_lui = max(0, i_khai - int(tim_lui * sr))
        i = i_khai
        while i - win >= i_lui:
            doan = audio[i - win:i]
            if doan.size and np.abs(doan).max() < nguong:
                return i / sr
            i -= win
        return t_khai_bao

    def vuot(seg, dau, cuoi, ms=12):
        """Vuốt êm mép đoạn tiếng trước/sau chỗ chèn im lặng.

        Cắt thẳng giữa lúc sóng đang dao động rồi dán im lặng tuyệt đối vào là tạo bậc biên độ —
        tai nghe ra tiếng 'tách', cộng dồn với nghỉ sai chỗ thành cảm giác nấc. 12ms đủ êm mà
        không nuốt mất phụ âm đầu/cuối."""
        n = int(sr * ms / 1000)
        if len(seg) < 2 * n or n < 2:
            return seg
        seg = seg.astype(np.float32)
        if dau:
            seg[:n] *= np.linspace(0.0, 1.0, n, dtype=np.float32)[:, None]
        if cuoi:
            seg[-n:] *= np.linspace(1.0, 0.0, n, dtype=np.float32)[:, None]
        return seg.astype(np.int16)

    ex = extras_for(k)
    out = [sil(args.lead)]
    new_cues = []
    t = args.lead
    # con_tro = vị trí ĐANG ĐỌC thật trong audio gốc — KHÔNG lấy lại từ cues[i][0] mỗi vòng, vì
    # mốc đó có thể đã bị đẩy sớm hơn ở vòng trước (diem_cat_an_toan cắt SỚM HƠN mốc STT khai để
    # tránh cắt dở dang từ trước) → đoạn sau phải đọc tiếp TỪ ĐÚNG chỗ đoạn trước dừng, không thì
    # mất tiếng (đọc trật khỏi audio) hoặc lặp tiếng (đọc chồng lên đoạn trước).
    con_tro = cues[0][0] if cues else 0.0
    for i, (s, e, txt) in enumerate(cues):
        seg_end_khai_bao = cues[i + 1][0] if i + 1 < len(cues) else e
        # CHỈ tìm điểm cắt an toàn khi thật sự sắp chèn im lặng — không thì giữ nguyên mốc STT,
        # khỏi tốn công dò mà cũng không có gì để tránh (không cắt gì ở đây).
        diem_cat = diem_cat_an_toan(seg_end_khai_bao) if ex[i] > 0 else seg_end_khai_bao
        # Vuốt mép ở ĐÚNG chỗ giáp im lặng chèn thêm: cuối đoạn này nếu sắp chèn, đầu đoạn này
        # nếu đoạn trước vừa chèn. Chỗ nối liền mạch thì để nguyên, đừng đụng vào tiếng nói.
        seg = vuot(audio[int(con_tro * sr): int(diem_cat * sr)],
                   dau=i > 0 and ex[i - 1] > 0, cuoi=ex[i] > 0)
        out.append(seg)
        new_cues.append((t, t + (e - s), txt))
        if ex[i] > 0:
            out.append(sil(ex[i]))
        t += (diem_cat - con_tro) + ex[i]
        con_tro = diem_cat

    paced = np.concatenate(out, axis=0)
    dur = len(paced) / sr
    speak_ratio = total_speak_in / dur

    out_a = Path(args.out_audio) if args.out_audio else Path(args.audio).with_name("voice_paced.wav")
    out_s = Path(args.out_srt) if args.out_srt else Path(args.srt).with_name("voice_paced.srt")
    w = wave.open(str(out_a), "wb")
    w.setnchannels(nch); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(paced.tobytes()); w.close()
    out_s.write_text("\n\n".join(f"{i}\n{_ts(a)} --> {_ts(b)}\n{txt}"
                                 for i, (a, b, txt) in enumerate(new_cues, 1)) + "\n", encoding="utf-8")
    n_para = sum(para)
    lo_tx = f"{args.target_lo:.0%}" if args.target_lo else "tắt"
    hi_tx = f"{args.target_hi:.0%}" if args.target_hi else "tắt"
    dat = (not args.target_lo or speak_ratio >= args.target_lo - 0.005) and \
          (not args.target_hi or speak_ratio <= args.target_hi + 0.005)
    print(f"cue: {len(cues)} | nghỉ dài(1,5s): {n_para} | dài audio {total_speak_in/60:.1f}'→{dur/60:.1f}' "
          f"(+{(dur/max(1,total_speak_in)-1)*100:.0f}%) | tỉ lệ NÓI {speak_ratio:.0%} "
          f"(mục tiêu {lo_tx}-{hi_tx}){'' if dat else '  ⚠️ VẪN LỆCH dải mục tiêu dù đã dò hệ số'}")
    print(f"✓ {out_a.name} + {out_s.name}")


if __name__ == "__main__":
    main()
