"""K4 — SO SÁNH GIỌNG ĐỌC GIỮA CÁC VIDEO CỦA 1 KÊNH (dùng cho mọi lane, không riêng Lane E).

Trả lời câu hỏi: kênh mẫu có dùng CHUNG 1 giọng đọc cho mọi video, hay đổi giọng theo video
(nam/nữ khác nhau, hoặc cùng giới nhưng khác người)? Việc này quyết định có nên voice-clone 1 lần
dùng chung (skill "voice_clone" — thật ra là mục "VOICE CLONE" trong CLAUDE.md, luồng OpenSpeaker
/v3/text-to-speech/voice-clone) hay phải clone RIÊNG cho từng tập/nhóm tập.

KHÔNG dùng model speaker-verification (torch/resemblyzer nặng, webrtcvad cần build C trên Windows
không có wheel sẵn cho py3.13) — dựng vân tay giọng NHẸ bằng numpy/scipy thuần:
  · F0 (cao độ) trung vị theo khung, autocorrelation — phân biệt nam/nữ RẤT đáng tin.
  · MFCC trung bình (13 hệ số, bỏ hệ số 0 vì phụ thuộc mức âm lượng ghi âm) — vân tay âm sắc THÔ,
    so sánh bằng cosine similarity. Đây là ước lượng GẦN ĐÚNG (không phải speaker-embedding chuẩn),
    dùng để phát hiện khác biệt RÕ RỆT (khác giới/khác kiểu giọng), KHÔNG đủ tinh để phân biệt
    2 giọng nam cùng chất rất giống nhau — kết quả biên giới (similarity 0.75-0.9) nên nghe tay
    xác nhận thêm.

CLI:
  py -3.13 -X utf8 voice_fingerprint.py --ids id1,id2,id3 --out-dir <thư mục scratch>
  py -3.13 -X utf8 voice_fingerprint.py --transcripts-json <path transcripts.json> --top 6 --out-dir ...
    (tự chọn N video trải đều theo view_count nếu không truyền --ids tay)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.fftpack import dct


# ---------------------------------------------------------------- tải audio
def download_audio(vid: str, workdir: Path, proxy: str | None = None) -> Path | None:
    import yt_dlp
    workdir.mkdir(parents=True, exist_ok=True)
    out_stub = workdir / f"{vid}"
    base_opts = {
        "quiet": True, "no_warnings": True, "noprogress": True,
        "format": "bestaudio/best",
        "outtmpl": str(out_stub) + ".%(ext)s",
        "postprocessors": [{"key": "FFmpegExtractAudio",
                             "preferredcodec": "mp3", "preferredquality": "5"}],
    }
    try:
        import imageio_ffmpeg
        base_opts["ffmpeg_location"] = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    if proxy:
        base_opts["proxy"] = proxy
    err = ""
    for lan_thu, client in enumerate((None, "android", "ios"), 1):
        opts = dict(base_opts)
        if client:
            opts["extractor_args"] = {"youtube": {"player_client": [client]}}
        try:
            with yt_dlp.YoutubeDL(opts) as y:
                y.download([f"https://www.youtube.com/watch?v={vid}"])
            err = ""
            break
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            if lan_thu < 3:
                cho = 8 * lan_thu
                print(f"  … tải audio {vid} lỗi ({err.splitlines()[0][:100]}), thử lại "
                      f"[{lan_thu+1}/3, client={client or 'web'}] sau {cho}s")
                time.sleep(cho)
    mp3 = next(iter(sorted(workdir.glob(f"{vid}.*"))), None)
    if not mp3:
        print(f"  ✗ {vid}: tải audio thất bại sau 3 lần — {err[-200:]}")
        return None
    return mp3


def trim_to_wav(mp3: Path, wav: Path, start_s: float = 20.0, dur_s: float = 50.0) -> bool:
    """Cắt 1 đoạn giữa (bỏ nhạc hiệu mở đầu) + hạ về 16kHz mono — chuẩn cho phân tích."""
    import subprocess
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg, "-y", "-ss", str(start_s), "-t", str(dur_s), "-i", str(mp3),
           "-ac", "1", "-ar", "16000", "-vn", str(wav)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return wav.exists() and wav.stat().st_size > 1000


def read_wav_mono(path: Path):
    import wave
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
        y = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    return y, sr


# ---------------------------------------------------------------- F0 (cao độ)
def estimate_f0_median(y: np.ndarray, sr: int, fmin=60.0, fmax=400.0,
                        frame_ms=40, hop_ms=20) -> float | None:
    frame = int(sr * frame_ms / 1000)
    hop = int(sr * hop_ms / 1000)
    min_lag, max_lag = int(sr / fmax), int(sr / fmin)
    rms_all = []
    f0s = []
    starts = list(range(0, max(0, len(y) - frame), hop))
    for start in starts:
        seg = y[start:start + frame]
        rms_all.append(float(np.sqrt(np.mean(seg ** 2)) + 1e-12))
    if not rms_all:
        return None
    thresh = np.percentile(rms_all, 55)  # chỉ lấy nửa khung "to tiếng" nhất — tránh khoảng lặng
    win = np.hanning(frame)
    for start, rms in zip(starts, rms_all):
        if rms < thresh:
            continue
        seg = (y[start:start + frame] - np.mean(y[start:start + frame])) * win
        corr = np.correlate(seg, seg, mode="full")
        corr = corr[len(corr) // 2:]
        if max_lag >= len(corr) or min_lag >= max_lag:
            continue
        window_corr = corr[min_lag:max_lag]
        if window_corr.size == 0 or corr[0] <= 0:
            continue
        peak_rel = int(np.argmax(window_corr))
        peak_lag = peak_rel + min_lag
        if corr[peak_lag] / corr[0] < 0.25:   # tương quan yếu → khung không có cao độ rõ (phụ âm/hơi thở)
            continue
        f0s.append(sr / peak_lag)
    if len(f0s) < 5:
        return None
    return float(np.median(f0s))


# ---------------------------------------------------------------- MFCC (vân tay âm sắc)
def _hz_to_mel(f):
    return 2595.0 * np.log10(1.0 + f / 700.0)


def _mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1.0)


def _mel_filterbank(nfilt, nfft, sr, low=80.0, high=None):
    high = high or sr / 2
    mel_pts = np.linspace(_hz_to_mel(low), _hz_to_mel(high), nfilt + 2)
    hz_pts = _mel_to_hz(mel_pts)
    bins = np.floor((nfft + 1) * hz_pts / sr).astype(int)
    fbank = np.zeros((nfilt, nfft // 2 + 1))
    for m in range(1, nfilt + 1):
        f_lo, f_mid, f_hi = bins[m - 1], bins[m], bins[m + 1]
        for k in range(f_lo, min(f_mid, fbank.shape[1])):
            if f_mid > f_lo:
                fbank[m - 1, k] = (k - f_lo) / (f_mid - f_lo)
        for k in range(f_mid, min(f_hi, fbank.shape[1])):
            if f_hi > f_mid:
                fbank[m - 1, k] = (f_hi - k) / (f_hi - f_mid)
    return fbank


def compute_mfcc_mean(y: np.ndarray, sr: int, nfft=2048, nfilt=26, ncoef=13,
                       frame_ms=25, hop_ms=10) -> np.ndarray | None:
    frame = int(sr * frame_ms / 1000)
    hop = int(sr * hop_ms / 1000)
    fbank = _mel_filterbank(nfilt, nfft, sr)
    window = np.hamming(frame)
    mfccs, energies = [], []
    for start in range(0, max(0, len(y) - frame), hop):
        seg = y[start:start + frame] * window
        spec = np.fft.rfft(seg, n=nfft)
        power = (np.abs(spec) ** 2) / nfft
        energies.append(float(np.sum(power)))
        mel_e = np.dot(fbank, power[:fbank.shape[1]])
        mel_e = np.where(mel_e <= 0, np.finfo(float).eps, mel_e)
        log_mel = np.log(mel_e)
        coeffs = dct(log_mel, type=2, norm="ortho")[:ncoef]
        mfccs.append(coeffs)
    if not mfccs:
        return None
    mfccs = np.array(mfccs)
    energies = np.array(energies)
    thresh = np.percentile(energies, 40)
    voiced = mfccs[energies > thresh]
    vec = voiced.mean(axis=0) if len(voiced) else mfccs.mean(axis=0)
    return vec[1:]  # bỏ hệ số 0 (phụ thuộc mức âm lượng ghi âm, không phải âm sắc)


def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


# ---------------------------------------------------------------- main
def pick_spread_ids(transcripts_json: Path, top_n: int):
    data = json.loads(transcripts_json.read_text(encoding="utf-8"))
    data = sorted(data, key=lambda v: -(v.get("view_count") or 0))
    if top_n >= len(data):
        return [(v["id"], v.get("title", "")) for v in data]
    idxs = sorted(set(int(round(i * (len(data) - 1) / (top_n - 1))) for i in range(top_n)))
    return [(data[i]["id"], data[i].get("title", "")) for i in idxs]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", default="", help="video_id1,video_id2,... (bỏ qua nếu dùng --transcripts-json)")
    ap.add_argument("--transcripts-json", default="", help="tự chọn N video trải đều theo view_count")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--proxy", default="")
    ap.add_argument("--start-s", type=float, default=20.0, help="bỏ qua N giây đầu (nhạc hiệu)")
    ap.add_argument("--dur-s", type=float, default=50.0, help="độ dài đoạn phân tích")
    args = ap.parse_args()

    if args.ids:
        pairs = [(i.strip(), "") for i in args.ids.split(",") if i.strip()]
    elif args.transcripts_json:
        pairs = pick_spread_ids(Path(args.transcripts_json), args.top)
    else:
        print("Cần --ids hoặc --transcripts-json"); sys.exit(1)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for vid, title in pairs:
        print(f"[{vid}] {title[:50]}")
        mp3 = download_audio(vid, out_dir, args.proxy or None)
        if not mp3:
            rows.append({"id": vid, "title": title, "error": "download_failed"})
            continue
        wav = out_dir / f"{vid}.wav"
        if not trim_to_wav(mp3, wav, args.start_s, args.dur_s):
            rows.append({"id": vid, "title": title, "error": "trim_failed"})
            continue
        y, sr = read_wav_mono(wav)
        f0 = estimate_f0_median(y, sr)
        mfcc = compute_mfcc_mean(y, sr)
        rows.append({"id": vid, "title": title, "f0_median_hz": f0,
                      "mfcc": mfcc.tolist() if mfcc is not None else None})
        gender = "?" if f0 is None else ("nam (thấp)" if f0 < 165 else "nữ (cao)")
        print(f"   F0 trung vị ≈ {f0:.1f} Hz ({gender})" if f0 else "   F0: không đo được (quá ồn/nhạc)")

    ok = [r for r in rows if r.get("mfcc") is not None]
    print("\n=== BẢNG F0 (cao độ) ===")
    for r in rows:
        f0 = r.get("f0_median_hz")
        print(f"  {r['id']}  F0={f0:.1f}Hz" if f0 else f"  {r['id']}  F0=? ({r.get('error', 'lỗi đo')})")

    print("\n=== MA TRẬN COSINE SIMILARITY (vân tay MFCC, 1.0=giống hệt) ===")
    if len(ok) >= 2:
        ids = [r["id"] for r in ok]
        vecs = [np.array(r["mfcc"]) for r in ok]
        header = "        " + " ".join(f"{i[:8]:>10}" for i in ids)
        print(header)
        sims = []
        for a_i, a in enumerate(ok):
            line = f"{a['id'][:8]:>8}"
            for b_i, b in enumerate(ok):
                s = cosine(vecs[a_i], vecs[b_i])
                if a_i != b_i:
                    sims.append(s)
                line += f" {s:>10.3f}"
            print(line)
        f0_vals = [r["f0_median_hz"] for r in ok if r.get("f0_median_hz")]
        f0_spread = (max(f0_vals) - min(f0_vals)) if len(f0_vals) >= 2 else 0
        min_sim = min(sims) if sims else 0
        print(f"\nF0 spread giữa các video: {f0_spread:.1f} Hz · cosine similarity thấp nhất: {min_sim:.3f}")
        if f0_spread < 20 and min_sim > 0.90:
            print("→ KẾT LUẬN (máy đo): RẤT có khả năng CÙNG 1 GIỌNG. Nên clone 1 lần dùng chung.")
        elif f0_spread > 40 or min_sim < 0.75:
            print("→ KẾT LUẬN (máy đo): NHIỀU KHẢ NĂNG KHÁC GIỌNG giữa một số video (xem F0/similarity "
                  "thấp ở cặp nào). Cần nghe tay xác nhận trước khi quyết định clone mấy giọng.")
        else:
            print("→ KẾT LUẬN (máy đo): BIÊN GIỚI — không đủ chắc chắn bằng số đo thô này. "
                  "Nghe tay 2 clip đại diện (đã lưu .mp3/.wav trong --out-dir) để xác nhận trước khi clone.")
    else:
        print("  (không đủ ≥2 clip đo được để so sánh)")

    report = out_dir / "voice_fingerprint_report.json"
    report.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nĐã lưu {report}")


if __name__ == "__main__":
    main()
