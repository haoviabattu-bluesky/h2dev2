"""qc_audio.py — CỔNG QC NGHE: soi thẳng sóng âm của file tiếng, không cần người nghe lại.

Vì sao phải có (user chốt 2026-09-09: "anh không thể video nào cũng kiểm tra được"):
B4Q cũ chỉ so SRT với kịch bản — bắt được "đọc THIẾU chữ", nhưng KHÔNG bắt được lỗi về NHỊP.
Tập simbot2-vU5PWT2zLDs lọt lưới toàn bộ: 52 chỗ nghỉ 1,5 giây nằm GIỮA CÂU (~78 giây im lặng
đặt sai chỗ), SRT vẫn phủ 95% kịch bản nên mọi cổng đều báo ĐẠT, chỉ tai người nghe ra.

Bảy phép soi, tất cả đều là ĐO SÓNG — không gọi AI, không tốn tiền, ~5 giây cho video 30 phút:

  1. nghỉ SAI CHỖ   — khoảng lặng dài không đứng sau một câu trọn vẹn  ← lỗi đã dính
  2. nghỉ QUÁ DÀI   — chết tiếng giữa video
  3. MẤT TIẾNG      — cue có lời trong SRT nhưng chỗ đó im: TTS rụng đoạn, lỗi CÂM LẶNG
  4. tỉ lệ NÓI      — quá dày thì nghe mệt, quá thưa thì lê thê
  5. vỡ tiếng       — biên độ chạm trần (clipping)
  6. quá nhỏ tiếng  — mức trung bình thấp, người xem phải vặn loa
  7. lệch SRT       — phụ đề không khớp độ dài tiếng thật

Chạy tay cho một tập bất kỳ:
  py -3.13 qc_audio.py --audio <slug>/voice_paced.wav --srt <slug>/voice_paced.srt
"""
import argparse
import io
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import imageio_ffmpeg

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HET_CAU = "。．.！!？?」』】"          # ký tự kết câu (gồm dấu đóng thoại)

# Ngưỡng — đặt ở một chỗ để chỉnh và để test bám vào.
LANG_DB = -45.0        # dưới mức này coi như im (nền TTS rất sạch nên không cần rộng tay)
NGHI_DAI = 0.9         # từ đây trở lên mới tính là "một chỗ nghỉ", dưới nữa là khe thở tự nhiên
# Chỉ soi SAI CHỖ với khoảng nghỉ từ mức này. Đo phân bố thật: nghỉ 0,9–1,1s phần lớn là TTS tự
# ngắt sau dấu phẩy — đó là ngữ điệu bình thường, bắt lỗi là báo oan. Từ 1,3s trở lên mới đủ dài
# để tai nghe ra "nấc" khi nó rơi vào giữa câu.
NGHI_SAI_TU = 1.3
NGHI_TOI_DA = 4.0      # dài hơn = chết tiếng
RUNG_TIENG = 0.70      # cue im quá tỉ lệ này = nghi TTS rụng mất đoạn
# Tỉ lệ nói ĐO TRÊN SÓNG (khác con số của pace_audio — nó tính theo mốc cue nên luôn cao hơn).
# Số đo thật tập 28': TTS thô 73,7% · sau khi giãn nhịp 67,8%. Dải dưới đây chỉ để bắt trường
# hợp cực đoan; muốn biết "đã giãn nhịp chưa" thì xem NGHI_MOI_PHUT chính xác hơn nhiều.
NOI_THAP, NOI_CAO = 0.55, 0.88
NGHI_MOI_PHUT_MIN = 1.0   # dưới mức này = gần như không có chỗ nghỉ (nghi chưa chạy pace_audio)
NGHI_MOI_PHUT_MAX = 8.0   # trên mức này = ngắt quá vụn
VO_TIENG_DB = -0.3     # đỉnh chạm mức này = có thể đã vỡ tiếng
NHO_TIENG_DB = -30.0   # mức trung bình dưới đây = quá nhỏ


def _sec(ts):
    h, m, s, ms = re.match(r"(\d\d):(\d\d):(\d\d)[,.](\d+)", ts).groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / (10 ** len(ms))


def doc_cues(srt):
    out = []
    for blk in re.split(r"\n\s*\n", Path(srt).read_text(encoding="utf-8").strip()):
        L = blk.splitlines()
        tl = next((x for x in L if "-->" in x), None)
        if not tl:
            continue
        a, b = tl.split("-->")
        out.append((_sec(a.strip()), _sec(b.strip()),
                    "".join(L[L.index(tl) + 1:]).strip()))
    return out


def het_cau(txt):
    return bool(txt) and txt.rstrip()[-1:] in HET_CAU


def _mmss(s):
    return f"{int(s)//60}:{int(s) % 60:02d}"


def doc_song(audio, sr=8000):
    """Giải mã về mono 8kHz — đủ để đo cấu trúc im/nói mà chỉ tốn ~1/40 bộ nhớ.

    Video 28 phút ở dạng gốc là 295 MB stereo 44.1kHz; nạp nguyên vào RAM chỉ để đếm khoảng
    lặng là phí. Đỉnh biên độ (vỡ tiếng) thì đo riêng trên bản GỐC bằng ffmpeg, vì hạ tần số
    lấy mẫu sẽ bào mòn đỉnh và giấu mất lỗi clipping.
    """
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.run([ff, "-v", "error", "-i", str(audio), "-ac", "1", "-ar", str(sr),
                        "-f", "wav", "-"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"ffmpeg không đọc được {audio}: {p.stderr[-200:].decode('utf8', 'ignore')}")
    w = wave.open(io.BytesIO(p.stdout), "rb")
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    return a, sr


def do_muc(audio):
    """Đỉnh và mức trung bình trên file GỐC, lấy từ ffmpeg volumedetect."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.run([ff, "-v", "info", "-i", str(audio), "-af", "volumedetect",
                        "-f", "null", "-"], capture_output=True)
    txt = p.stderr.decode("utf8", "ignore")
    def lay(ten):
        m = re.search(rf"{ten}:\s*(-?[\d.]+) dB", txt)
        return float(m.group(1)) if m else None
    return lay("max_volume"), lay("mean_volume")


def khoang_lang(a, sr, nguong_db=LANG_DB, toi_thieu=0.05):
    """Các đoạn im: (bắt đầu, độ dài). Đo trên đường bao 20ms cho khỏi vụn."""
    win = max(1, int(sr * 0.02))
    n = len(a) // win * win
    if n == 0:
        return []
    env = np.abs(a[:n]).reshape(-1, win).max(axis=1)
    im = env < (10 ** (nguong_db / 20))
    d = np.diff(im.astype(np.int8))
    b = list(np.where(d == 1)[0] + 1)
    e = list(np.where(d == -1)[0] + 1)
    if im[0]:
        b = [0] + b
    if im[-1]:
        e = e + [len(im)]
    ra = [(x * win / sr, (y - x) * win / sr) for x, y in zip(b, e)]
    return [(t, d_) for t, d_ in ra if d_ >= toi_thieu]


def qc_audio(audio, srt, dung_sai_sai_cho=0.03, doi_nghi=True):
    """Trả {"problems": [...], "infra": [...]} + các số đo, đúng khuôn của qc_visual.report.

    `doi_nghi=False`: KHÔNG đòi phải có chỗ nghỉ rõ mỗi phút. Luật "≥1 chỗ nghỉ/phút" sinh ra cho
    giọng cụ già kể chuyện (đã giãn nhịp bằng pace_audio) — đem áp cho kênh kể tài liệu nhịp chặt
    là báo lỗi oan cho đúng thứ mình cố ý làm: khán giả ngách đó XEM CHỦ ĐỘNG (0/190 comment nhắc
    "nghe khi ngủ"), nhịp phải liền. Bên gọi truyền theo profile.voice.pace.
    """
    out = {"problems": [], "infra": []}
    try:
        a, sr = doc_song(audio)
    except Exception as e:
        out["infra"].append(f"không giải mã được tiếng: {e}")
        return out
    tong = len(a) / sr
    out["seconds"] = round(tong, 1)
    if tong < 30:
        out["problems"].append(f"file tiếng chỉ dài {tong:.0f}s — nghi đọc hỏng")
        return out

    lang = khoang_lang(a, sr)
    im_tong = sum(d for _, d in lang)
    ti_le_noi = 1 - im_tong / tong
    out["speak_ratio"] = round(ti_le_noi, 3)

    dai = [(t, d) for t, d in lang if d >= NGHI_DAI]
    out["pauses"] = len(dai)
    # Đếm theo chỗ nghỉ THẬT SỰ DÀI: khe 0,9s là TTS tự ngắt sau dấu phẩy, có sẵn kể cả khi
    # chưa giãn nhịp (đo thật: bản TTS thô có 0 khoảng ≥1,3s, bản đã giãn có 56).
    nghi_ro = [x for x in dai if x[1] >= NGHI_SAI_TU]
    out["pauses_per_min"] = round(len(nghi_ro) / (tong / 60), 2)

    try:
        cues = doc_cues(srt) if srt and Path(srt).exists() else []
    except Exception as e:
        cues = []
        out["infra"].append(f"không đọc được SRT: {e}")

    # ---- 1. nghỉ SAI CHỖ (lỗi đã dính thật) ----
    if cues:
        # Cue nào đang được ĐỌC lúc khoảng lặng bắt đầu — phải tra theo THỜI ĐIỂM BẮT ĐẦU của
        # cue, không phải thời điểm kết thúc. Mốc kết thúc trong SRT luôn dôi ra sau tiếng nói
        # thật vài phần mười giây, nên tra theo nó sẽ nhặt nhầm cue TRƯỚC ĐÓ NỮA và báo oan
        # (đo thật: 39 báo động giả, trong đó chỗ 3:54 thực ra nằm sau «…しまいました。»).
        sai, vd = 0, []
        for t, d in [x for x in dai if x[1] >= NGHI_SAI_TU]:
            truoc = [c for c in cues if c[0] <= t + 0.05]
            if not truoc:
                continue                       # khoảng lặng mở đầu, không tính
            if not het_cau(truoc[-1][2]):
                sai += 1
                if len(vd) < 3:
                    vd.append(f"{_mmss(t)} nghỉ {d:.1f}s sau «…{truoc[-1][2][-18:]}»")
        out["pause_misplaced"] = sai
        cho_phep = max(2, int(len(dai) * dung_sai_sai_cho))
        if sai > cho_phep:
            out["problems"].append(
                f"{sai}/{len(dai)} chỗ nghỉ nằm GIỮA CÂU (nghe như nấc cụt) — " + " · ".join(vd))

    # ---- 2. nghỉ QUÁ DÀI ----
    qua = [(t, d) for t, d in dai if d > NGHI_TOI_DA]
    if qua:
        out["problems"].append(
            f"{len(qua)} chỗ im quá {NGHI_TOI_DA}s (chết tiếng): "
            + " · ".join(f"{_mmss(t)} {d:.1f}s" for t, d in qua[:3]))

    # ---- 3. MẤT TIẾNG: SRT bảo có lời mà chỗ đó im ----
    if cues:
        win = max(1, int(sr * 0.02))
        env = np.abs(a[:len(a) // win * win]).reshape(-1, win).max(axis=1)
        im = env < (10 ** (LANG_DB / 20))
        rung = []
        for s, e, txt in cues:
            if e - s < 1.5 or not txt:
                continue
            i0, i1 = int(s * sr / win), min(int(e * sr / win), len(im))
            if i1 <= i0:
                continue
            if im[i0:i1].mean() >= RUNG_TIENG:
                rung.append((s, txt))
        out["dropouts"] = len(rung)
        if rung:
            out["problems"].append(
                f"{len(rung)} đoạn CÓ LỜI trong phụ đề nhưng KHÔNG có tiếng (TTS rụng đoạn): "
                + " · ".join(f"{_mmss(s)} «{t[:16]}…»" for s, t in rung[:3]))

    # ---- 4. tỉ lệ NÓI ----
    if ti_le_noi > NOI_CAO and doi_nghi:
        out["problems"].append(
            f"nói liền mạch {ti_le_noi:.0%} (>{NOI_CAO:.0%}) — thiếu chỗ nghỉ, người già nghe mệt")
    elif ti_le_noi < NOI_THAP:
        out["problems"].append(
            f"chỉ nói {ti_le_noi:.0%} (<{NOI_THAP:.0%}) — im lặng quá nhiều, video lê thê")
    npm = out["pauses_per_min"]
    if npm < NGHI_MOI_PHUT_MIN and doi_nghi:
        out["problems"].append(
            f"chỉ {npm}/phút chỗ nghỉ rõ — nghe liền mạch, nghi CHƯA chạy bước giãn nhịp")
    elif npm > NGHI_MOI_PHUT_MAX:
        out["problems"].append(f"{npm}/phút chỗ nghỉ — ngắt quá vụn, lời kể bị băm nát")

    # ---- 5+6. mức tiếng ----
    try:
        dinh, tb = do_muc(audio)
        out["peak_db"], out["mean_db"] = dinh, tb
        if dinh is not None and dinh >= VO_TIENG_DB:
            out["problems"].append(f"đỉnh {dinh:.1f} dB — chạm trần, có thể VỠ TIẾNG")
        if tb is not None and tb < NHO_TIENG_DB:
            out["problems"].append(f"mức trung bình {tb:.1f} dB — quá nhỏ, người xem phải vặn loa")
    except Exception as e:
        out["infra"].append(f"không đo được mức tiếng: {e}")

    # ---- 7. lệch SRT ----
    if cues:
        lech = abs(cues[-1][1] - tong)
        out["srt_drift"] = round(lech, 2)
        if lech > 2.5:
            out["problems"].append(
                f"phụ đề lệch {lech:.1f}s so với tiếng (cue cuối {_mmss(cues[-1][1])} / "
                f"tiếng {_mmss(tong)}) — phụ đề sẽ chạy sai")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--srt", default="")
    args = ap.parse_args()
    r = qc_audio(args.audio, args.srt)
    n = len(r["problems"])
    print(f"=== QC NGHE: {'ĐẠT' if not n else str(n) + ' VẤN ĐỀ'}")
    for k in ("seconds", "speak_ratio", "pauses", "pauses_per_min", "pause_misplaced",
              "dropouts", "peak_db", "mean_db", "srt_drift"):
        if k in r:
            print(f"  {k:16s} {r[k]}")
    for e in r["infra"]:
        print("   !", e)
    for p in r["problems"]:
        print("   ✗", p)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
