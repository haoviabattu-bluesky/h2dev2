"""selftest_extra.py — phần kiểm tra bản .exe nằm NGOÀI gui_video.py.

Vì sao tách file: nhánh `--selftest` trong `gui_video.py` là thứ duy nhất đọc được lỗi của bản
`--windowed` (không có console, mọi lỗi bị nuốt — bẫy #20 skill tao_tool_exe.md). Nhưng gui_video.py
đang được viết lại ở luồng khác. Tách ra đây thì thêm phép kiểm KHÔNG cần chạm vào file đó:
gui_video.py chỉ cần một dòng

    import selftest_extra; out += selftest_extra.lines()

Chạy tay lúc dev:  py -3.13 selftest_extra.py
"""


def _key_lines():
    """Key nào đang lấy từ ĐÂU (chỉ nguồn + 6 ký tự đầu — không bao giờ in cả key ra log).

    Lưu ý đọc kết quả: `keys.py` chỉ giữ phần GHI ĐÈ. Giá trị mặc định nằm trong từng module
    provider, nên "mac dinh trong code" KHÔNG có nghĩa là thiếu key — số key thật xem khối dưới.
    """
    out = []
    try:
        import keys
    except Exception as e:
        return [f"keys.py LOI: {type(e).__name__} {e}"]
    for name, env in (("ramclouds", "RAMCLOUDS_API_KEY"), ("ns24", "NS24_API_KEY"),
                      ("gpti2", "GPTI2_API_KEYS"), ("grok", "GROK_API_KEY"),
                      ("openspeaker", "AI33_API_KEY")):
        src = keys.source(name, env)
        got = [g for g in (keys.get_list(name, env=env) if name == "gpti2"
                           else [keys.get(name, env=env)]) if g]
        if got:
            head = ", ".join(g[:6] + "..." for g in got)
            out.append(f"key {name:12s} ghi de {len(got)} cai [{head}] tu {src}")
        else:
            out.append(f"key {name:12s} khong ghi de -> dung mac dinh trong code")
    return out


def _provider_lines():
    """Key thực sự tới được module provider chưa (nơi tiêu tiền), không chỉ đọc được file."""
    out = []
    for mod, attr in (("gpti2_gen", "API_KEYS"), ("grok_gen", "API_KEY"),
                      ("openspeaker_tts", "API_KEY")):
        try:
            m = __import__(mod)
            v = getattr(m, attr)
            n = len(v) if isinstance(v, (list, tuple)) else (1 if v else 0)
            out.append(f"{mod}.{attr}: {n} key {'OK' if n else 'THIEU'}")
        except Exception as e:
            out.append(f"{mod}: LOI {type(e).__name__} {e}")
    return out


def _scan_lines():
    """2 module front-end mới (quét kênh + chọn giọng theo video) có nạp được trong bản frozen."""
    out = []
    for mod in ("channel_scan", "detect_voice"):
        try:
            __import__(mod)
            out.append(f"{mod}: import OK")
        except Exception as e:
            out.append(f"{mod}: LOI {type(e).__name__} {e}")
    try:
        import yt_dlp
        # Bẫy frozen: import yt_dlp chạy được nhưng danh sách extractor nạp ĐỘNG có thể rỗng
        # → mọi lệnh quét kênh / bóc transcript bảo "no suitable extractor".
        from yt_dlp.extractor import gen_extractors
        n = len(gen_extractors())
        out.append(f"yt_dlp {yt_dlp.version.__version__}: {n} extractor "
                   f"{'OK' if n > 100 else 'NGHI THIEU - them --collect-submodules yt_dlp'}")
    except Exception as e:
        out.append(f"yt_dlp: LOI {type(e).__name__} {e}")
    return out


def _whisper_lines():
    """Tầng 3 bóc transcript (nghe lại) — thứ hay thiếu ÂM THẦM nhất trong bản đóng gói.

    Ba thứ phải đủ CẢ BA mới chạy được: faster_whisper + ctranslate2 (giải mã) · onnxruntime (lọc
    VAD) · model bản địa (khỏi tải 142MB từ HuggingFace ở lần chạy đầu).
    """
    out = []
    for mod in ("faster_whisper", "ctranslate2", "onnxruntime"):
        try:
            m = __import__(mod)
            out.append(f"{mod}: OK {getattr(m, '__version__', '')}")
        except Exception as e:
            out.append(f"{mod}: THIEU ({type(e).__name__}) -> khong nghe lai duoc")
    try:
        import paths
        found = []
        for size in ("tiny", "base", "small", "medium"):
            d = paths.res(f"models/faster-whisper-{size}")
            if (d / "model.bin").exists():
                mb = (d / "model.bin").stat().st_size / 1e6
                found.append(f"{size} ({mb:.0f}MB)")
        out.append("model ban dia: " + (", ".join(found) if found
                                        else "KHONG CO -> lan chay dau se tai tu HuggingFace"))
    except Exception as e:
        out.append(f"model ban dia: LOI {type(e).__name__} {e}")
    return out


def _env_lines():
    """Hai thứ chỉ sai KHI ĐÓNG GÓI, và sai thì im lặng chứ không báo lỗi."""
    out = []
    try:
        import profiles
        same = profiles.DIR.resolve() == profiles.BUNDLED.resolve()
        out.append(f"profile ghi vao : {profiles.DIR}")
        out.append(f"profile di kem  : {profiles.BUNDLED}")
        import paths
        out.append(f"thu muc du lieu : {paths.DATA_DIR}")
        out.append(f"nho lua chon o  : {paths.CONFIG_FILE}"
                   f"{'' if paths.CONFIG_FILE.exists() else '  (chua doi, dang dung mac dinh)'}")
        # Nam trong thu muc CAI (_internal hoac canh exe) = cap nhat tool la mat sach.
        s = str(profiles.DIR).lower()
        trong_cai = "_internal" in s or (paths.FROZEN
                                        and str(paths.EXE_DIR).lower() in s)
        out.append("noi ghi profile : " + ("SAI - nam trong thu muc cai, cap nhat tool la MAT"
                                           if trong_cai else
                                           ("cung cho (chay tu ma nguon)" if same
                                            else "OK - ngoai thu muc cai, cap nhat tool van con")))
    except Exception as e:
        out.append(f"profiles: LOI {type(e).__name__} {e}")
    import subprocess
    out.append("an cua so con  : " + ("OK" if getattr(subprocess.Popen, "_an_cua_so", False)
                                      else "CHUA BAT - ffmpeg se nhay cua so den"))
    return out


def lines():
    out = ["--- key & module front-end ---"]
    for fn in (_key_lines, _provider_lines, _scan_lines, _whisper_lines, _env_lines):
        try:
            out += fn()
        except Exception as e:
            out.append(f"{fn.__name__} LOI: {type(e).__name__} {e}")
    return out


def whisper_test(audio, model_size="base", lang="ja"):
    """NGHE THẬT một file audio ngay trong bản .exe.

    Kiểm import là chưa đủ: ctranslate2 và onnxruntime nạp DLL nặng LÚC CHẠY, mà build này đã cắt
    hết DLL CUDA (device="cpu" không cần) — phải nghe thật một lần mới biết có cắt lố hay không.
    Ép offline luôn để chắc model bản địa được dùng chứ không lặng lẽ tải từ HuggingFace.
    """
    import os
    import time
    os.environ["HF_HUB_OFFLINE"] = "1"
    import paths
    from faster_whisper import WhisperModel
    d = paths.res(f"models/faster-whisper-{model_size}")
    target = str(d) if (d / "model.bin").exists() else model_size
    print(f"model: {target}")
    t0 = time.time()
    m = WhisperModel(target, device="cpu", compute_type="int8",
                     cpu_threads=max(4, min(16, os.cpu_count() or 8)), num_workers=2)
    t1 = time.time()
    segs = list(m.transcribe(audio, language=lang, vad_filter=True, beam_size=1,
                             condition_on_previous_text=False)[0])
    print(f"nap {t1 - t0:.1f}s | nghe {time.time() - t1:.1f}s | {len(segs)} doan")
    for s in segs[:3]:
        print(f"  [{s.start:5.1f}] {s.text.strip()[:70]}")
    print("WHISPER TRONG EXE: OK" if segs else "WHISPER TRONG EXE: HONG (0 doan)")
    return 0 if segs else 1


def main():
    import sys
    argv = sys.argv[1:]
    if "--audio" in argv:
        return whisper_test(argv[argv.index("--audio") + 1])
    print("\n".join(lines()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
