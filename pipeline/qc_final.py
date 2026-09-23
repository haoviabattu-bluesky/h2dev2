# -*- coding: utf-8 -*-
"""qc_final.py — B10: NGHIỆM THU TOÀN TẬP, soi GÓI GIAO chứ không chỉ file MP4.

Vì sao cần dù đã có B8Q: B8Q chỉ soi **bản ghép** (có luồng tiếng không · độ dài có khớp giọng
không · khung có đen không · vài khung có khớp lời không). Nó KHÔNG biết gì về những thứ người xem
gặp đầu tiên và những thứ làm hỏng buổi đăng:

  · thumbnail vượt trần 2 MB của YouTube ⇒ **không tải lên được**, phát hiện lúc đang đăng
  · tiêu đề lệch dải đã đo của ngách (30–45 ký tự) ⇒ mất tới 2,4 lần lượt xem
  · mô tả vượt 5.000 ký tự / thẻ vượt 500 ⇒ YouTube **cắt cụt lặng lẽ**
  · mốc chương sai luật (không mở bằng 0:00 · dưới 3 chương · hai mốc cách nhau <10 giây)
    ⇒ YouTube **bỏ toàn bộ chương** chứ không báo lỗi
  · quên cháy phụ đề ⇒ mp4 vẫn hợp lệ, B8Q vẫn ĐẠT
  · sổ nguồn thiếu file ⇒ không truy ngược được khi bị khiếu nại
  · B3F còn lỗi nặng ⇒ video vẫn dựng ra bình thường, chỉ là có chi tiết bịa

Toàn bộ phép kiểm ở đây **tất định và miễn phí** — không gọi model, không tốn tiền.

  py -3.13 qc_final.py --slug <thư mục tập> --profile <id>
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                    # sys.stdout is None trong .exe --windowed
    pass

from assemble import FF, media_seconds

TRAN_THUMB_MB = 2.0          # YouTube từ chối ảnh bìa > 2 MB
TRAN_MO_TA = 5000
TRAN_THE = 500
CHUONG_TOI_THIEU = 3         # dưới 3 chương ⇒ YouTube bỏ hết chương
CACH_NHAU_TOI_THIEU = 10     # hai mốc gần nhau hơn 10 giây ⇒ cũng bỏ hết


def _loi(ra, muc, ten, msg, sua=""):
    ra.append({"muc": muc, "sev": ten, "msg": msg, "sua": sua})


def _probe(mp4):
    r = subprocess.run([FF, "-i", str(mp4)], capture_output=True, text=True).stderr
    wh = re.search(r"(\d{3,5})x(\d{3,5})", r)
    fps = re.search(r"(\d+(?:\.\d+)?) fps", r)
    return {"w": int(wh.group(1)) if wh else 0, "h": int(wh.group(2)) if wh else 0,
            "fps": float(fps.group(1)) if fps else 0.0,
            "co_tieng": "Audio:" in r, "raw": r}


def kiem_video(S: Path, ra):
    mp4 = S / "final.mp4"
    if not mp4.exists():
        _loi(ra, "video", "cao", "KHÔNG có final.mp4", "chạy lại B8")
        return None
    info = _probe(mp4)
    dur = media_seconds(mp4)
    if not info["co_tieng"]:
        _loi(ra, "video", "cao", "video KHÔNG có luồng âm thanh", "chạy lại B8")
    if info["h"] < 1080:
        _loi(ra, "video", "vua", f"khung ra {info['w']}x{info['h']} (dưới 1080p)")
    for ten in ("voice_paced.wav", "voice.mp3"):
        f = S / ten
        if f.exists():
            lech = dur - media_seconds(f)
            if abs(lech) > 3:
                _loi(ra, "video", "cao", f"video lệch giọng {lech:+.0f}s ({ten})", "dựng lại B8")
            break
    return {"dur": dur, **{k: v for k, v in info.items() if k != "raw"}}


def kiem_phu_de_chay(S: Path, dur, ra, so_mau=6, chay=True):
    """Phụ đề CÓ THẬT SỰ cháy vào hình không — đếm điểm ảnh sáng ở dải đáy khung.

    Quên bật burn-in là lỗi câm hoàn hảo: mp4 vẫn chạy, vẫn có tiếng, B8Q vẫn ĐẠT, chỉ khán giả
    Nhật mở lên mới thấy trống trơn. Ở đây lấy mốc GIỮA cue (lúc chắc chắn đang có lời) rồi đo dải
    25% đáy khung; chữ trắng viền đen nên ngưỡng >235 là đủ tách khỏi nền.
    """
    srt = S / "voice_paced.srt"
    if not srt.exists():
        srt = S / "voice.srt"
    if not srt.exists():
        _loi(ra, "phụ đề", "vua", "không có file .srt để đối chiếu")
        return
    import storyboard as sb
    cues = sb.parse_cues(srt)
    if not cues:
        _loi(ra, "phụ đề", "vua", "file .srt rỗng")
        return
    if cues[-1][1] > dur + 2:
        _loi(ra, "phụ đề", "cao",
             f"phụ đề kéo tới {cues[-1][1]:.0f}s trong khi video dài {dur:.0f}s")
    from PIL import Image
    import numpy as np
    tmp = Path(tempfile.mkdtemp(prefix="qcf_"))
    moc = [cues[int(len(cues) * (i + 0.5) / so_mau)] for i in range(so_mau)]
    trong = 0
    for k, (a, b, _) in enumerate(moc):
        t = (a + b) / 2
        f = tmp / f"{k}.png"
        subprocess.run([FF, "-y", "-ss", f"{t:.2f}", "-i", str(S / "final.mp4"),
                        "-vframes", "1", str(f)], capture_output=True)
        if not f.exists():
            continue
        a_ = np.asarray(Image.open(f).convert("L"))
        day = a_[int(a_.shape[0] * 0.75):, :]
        if (day > 235).sum() < day.size * 0.002:      # gần như không có điểm sáng ⇒ không thấy chữ
            trong += 1
    if chay and trong >= max(2, so_mau // 2):
        _loi(ra, "phụ đề", "cao",
             f"{trong}/{len(moc)} mốc có lời mà đáy khung KHÔNG thấy chữ — nghi CHƯA cháy phụ đề",
             "kiểm --srt ở bước ghép")
    # ⚠️ KHÔNG lật ngược phép đo này để bắt "cháy nhầm". Nó đếm ĐIỂM SÁNG ở đáy khung — vắng điểm
    # sáng thì chắc chắn không có chữ trắng, nhưng CÓ điểm sáng thì chưa chắc là chữ. Đã thử và sai:
    # tập 1 (cảnh vũ trụ có dải chân trời sáng) bị báo "5/6 mốc vẫn thấy chữ" trong khi cắt khung ra
    # nhìn thì sạch trơn. Việc bắt "cháy nhầm" giao cho `kiem_render_info()` — đọc thẳng bản ghi của
    # bước ghép, tất định, không phải đoán.


def kiem_thumbnail(S: Path, ra):
    for ten in ("thumbnail_final.png", "thumb_final.png"):
        f = S / ten
        if f.exists():
            break
    else:
        _loi(ra, "thumbnail", "cao", "KHÔNG có ảnh bìa", "chạy lại B7")
        return
    mb = f.stat().st_size / 1024 / 1024
    if mb > TRAN_THUMB_MB:
        _loi(ra, "thumbnail", "cao", f"ảnh bìa {mb:.1f} MB > trần {TRAN_THUMB_MB} MB của YouTube",
             "lưu lại dạng JPEG chất lượng 90")
    from PIL import Image
    w, h = Image.open(f).size
    if w < 1280 or h < 720:
        _loi(ra, "thumbnail", "cao", f"ảnh bìa {w}x{h} nhỏ hơn 1280x720")
    if abs(w / h - 16 / 9) > 0.02:
        _loi(ra, "thumbnail", "vua", f"ảnh bìa tỉ lệ {w/h:.2f} ≠ 16:9")


def _mmss_to_sec(s):
    p = [int(x) for x in s.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def kiem_goi_dang_tai(S: Path, prof, dur, ra):
    f = S / "TIEU_DE_MO_TA.txt"
    if not f.exists():
        _loi(ra, "đăng tải", "cao", "KHÔNG có TIEU_DE_MO_TA.txt", "chạy lại B9")
        return
    khoi = [k.strip() for k in re.split(r"^-{20,}\s*$", f.read_text(encoding="utf-8"),
                                        flags=re.MULTILINE)]
    dau = khoi[0].splitlines() if khoi else []
    dong = [d for d in dau if d.strip()]
    if not dong:
        _loi(ra, "đăng tải", "cao", "TIEU_DE_MO_TA.txt rỗng")
        return
    tieu_de = dong[0].strip()
    lo, hi = (prof.get("script", {}).get("gate", {}) or {}).get("title_len") or [0, 100]
    if len(tieu_de) > 100:
        _loi(ra, "đăng tải", "cao", f"tiêu đề {len(tieu_de)} ký tự > trần 100 của YouTube")
    elif not (lo <= len(tieu_de) <= hi):
        _loi(ra, "đăng tải", "vua",
             f"tiêu đề {len(tieu_de)} ký tự, ngoài dải đã đo {lo}–{hi} của ngách")
    tu_khoa = dong[1] if len(dong) > 1 else ""
    if tu_khoa.count(",") + 1 < 5:
        _loi(ra, "đăng tải", "thap", f"chỉ {tu_khoa.count(',')+1} từ khoá SEO, quy cách cần 5")
    if " " in tu_khoa.replace(", ", ",").split(",")[0].strip() and "," in tu_khoa:
        pass                                          # từ khoá nhiều chữ là bình thường
    if len(f.read_text(encoding="utf-8")) > TRAN_MO_TA:
        _loi(ra, "đăng tải", "vua", f"khối mô tả {len(f.read_text(encoding='utf-8'))} ký tự "
                                    f"> {TRAN_MO_TA}")
    # ---- mốc chương: sai luật là YouTube BỎ HẾT chương, không báo gì
    moc = [(_mmss_to_sec(m.group(1)), m.group(2).strip())
           for m in re.finditer(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$",
                                f.read_text(encoding="utf-8"), re.MULTILINE)]
    if moc:
        if moc[0][0] != 0:
            _loi(ra, "đăng tải", "cao", f"chương đầu ở {moc[0][0]}s, YouTube đòi 0:00",
                 "YouTube bỏ TOÀN BỘ chương nếu sai")
        if len(moc) < CHUONG_TOI_THIEU:
            _loi(ra, "đăng tải", "cao", f"chỉ {len(moc)} chương < {CHUONG_TOI_THIEU}")
        for i in range(len(moc) - 1):
            if moc[i + 1][0] - moc[i][0] < CACH_NHAU_TOI_THIEU:
                _loi(ra, "đăng tải", "cao",
                     f"chương {i+2} chỉ cách chương trước {moc[i+1][0]-moc[i][0]}s (<10s)")
        if dur and moc[-1][0] > dur:
            _loi(ra, "đăng tải", "cao",
                 f"chương cuối ở {moc[-1][0]}s vượt quá độ dài video {dur:.0f}s")
    else:
        _loi(ra, "đăng tải", "vua", "không thấy mốc thời gian nào trong TIEU_DE_MO_TA.txt")
    d = S / "DANG-TAI.txt"
    if d.exists():
        m = re.search(r"3\) THẺ / TAGS.*?\n-+\n(.+?)\n", d.read_text(encoding="utf-8"), re.S)
        if m and len(m.group(1)) > TRAN_THE:
            _loi(ra, "đăng tải", "vua", f"chuỗi thẻ {len(m.group(1))} ký tự > {TRAN_THE}")


def kiem_nguon(S: Path, ra):
    sc, cr = S / "scenes.json", S / "credits.txt"
    if not sc.exists():
        return
    dung = {c["file"] for c in json.loads(sc.read_text(encoding="utf-8"))}
    if not cr.exists():
        _loi(ra, "nguồn", "cao", f"dùng {len(dung)} file tư liệu mà KHÔNG có credits.txt",
             "chạy lại B8")
        return
    txt = cr.read_text(encoding="utf-8")
    thieu = [f for f in dung if f not in txt]
    if thieu:
        _loi(ra, "nguồn", "cao", f"{len(thieu)} file dùng trong video KHÔNG có trong credits.txt "
                                 f"(vd {thieu[0][:40]})")


def kiem_bang_chung(S: Path, ra):
    """Số ảnh dẫn nguồn ĐỊNH dùng (evidence.json) phải bằng số THẬT SỰ lên hình (scenes.json).

    ⚠️ `kiem_nguon()` ở trên chỉ soi chiều ngược lại: file nào ĐÃ dùng thì phải có trong
    credits.txt. Nó hoàn toàn mù với tấm bị BỎ QUA — tấm không lên hình thì cũng không cần ghi
    nguồn, nên mọi phép đếm vẫn khớp.

    Đo thật ở tập 2: `ev06c_bass_strait_chart.jpg` là file tự cắt ra nên thiếu dòng trong
    `manifest.jsonl`; khâu ghim bỏ qua nó (đúng luật — không đoán bản quyền), video mất một
    trong tám ảnh bằng chứng, mà **B10 vẫn báo 0 phát hiện**. Phát hiện được là nhờ đếm tay.
    Cổng chỉ biết những gì đã xảy ra thì không bao giờ thấy thứ lẽ ra phải xảy ra.
    """
    ev, sc = S / "evidence.json", S / "scenes.json"
    if not ev.exists() or not sc.exists():
        return
    try:
        muc = json.loads(ev.read_text(encoding="utf-8"))
        canh = json.loads(sc.read_text(encoding="utf-8"))
    except Exception as e:
        _loi(ra, "bằng chứng", "vua", f"không đọc được evidence.json/scenes.json: {e}")
        return
    len_hinh = {c["file"] for c in canh if c.get("bangchung")}
    thieu = [m.get("file") for m in muc if m.get("file") not in len_hinh]
    if thieu:
        _loi(ra, "bằng chứng", "cao",
             f"{len(thieu)}/{len(muc)} ảnh dẫn nguồn KHÔNG lên hình: {', '.join(t[:34] for t in thieu[:3])}",
             "thường do thiếu dòng trong stock/manifest.jsonl, sai mốc chương, hoặc giấy phép "
             "ngoài chính sách 'pd' — xem lại log B8")


def kiem_du_kien(S: Path, ra):
    f = S / "qc_facts.json"
    if not f.exists():
        _loi(ra, "dữ kiện", "vua", "chưa chạy B3F (kiểm dữ kiện) cho tập này")
        return
    # Kết quả QC CŨ HƠN kịch bản = con số ảo. Đây đúng là bẫy dự án đã dính nhiều lần: đọc một
    # file .json còn nằm đó rồi tưởng là tình trạng hiện tại. Đo thật lần đầu chạy B10: script đã
    # bỏ chữ 埼玉県 nhưng qc_facts.json vẫn còn báo lỗi đó.
    sc = S / "script.txt"
    if sc.exists() and sc.stat().st_mtime > f.stat().st_mtime + 1:
        _loi(ra, "dữ kiện", "cao", "kết quả B3F CŨ HƠN kịch bản → số liệu không còn đúng",
             "chạy lại: py -3.13 qc_facts.py --script script.txt --dossier series_ctx.txt")
        return
    kq = json.loads(f.read_text(encoding="utf-8"))
    if kq.get("nang"):
        _loi(ra, "dữ kiện", "cao",
             f"B3F còn {len(kq['nang'])} chi tiết KHÔNG có trong tư liệu "
             f"(vd 「{kq['nang'][0]['token']}」)", "sửa tư liệu hoặc kịch bản rồi dựng lại")


def kiem_hook(S: Path, prof, ra):
    """Mọi tập phải có hook khoá (anh chốt 2026-09-23). upstream: script bắt đầu bằng hook; repair: có hook_final.mp4.

    Cố ý CHẠY BẤT KỂ `publish.listing_external` — hook là NỘI DUNG của chính video (nằm trong
    final.mp4), không phải phần đóng gói đăng tải (thumbnail/tiêu đề/mô tả) mà dự án khác lo.
    Tập LÀM TRƯỚC khi có tính năng hook (chưa từng chạy hook_stage) cũng bị báo `cao` ở đây —
    cố ý, vì luật mới (2026-09-23) là MỌI tập giao đều phải có hook; sửa qua `--mode repair`.
    """
    import hook_stage
    m = hook_stage.doc_lock(S)
    if not m:
        _loi(ra, "hook", "cao", "thiếu hook/hook_lock.json — tập chưa có hook 20–30s", "chạy hook_stage.py (--mode repair nếu tập đã có script)")
        return
    stale, ly_do = hook_stage.kiem_stale(S)
    if stale:
        _loi(ra, "hook", "cao", "HOOK_STALE: " + " · ".join(ly_do), "chạy lại H1–H4 (hook_stage.py --force)")
    hook = hook_stage.doc_hook(S)
    if m.get("mode") == "repair":
        if not (S / "hook" / "hook_final.mp4").exists():
            _loi(ra, "hook", "cao", "repair mode nhưng chưa có hook/hook_final.mp4", "bước 3 dựng hook_final.mp4 rồi final_with_hook.mp4")
    else:
        sc = (S / "script.txt").read_text(encoding="utf-8") if (S / "script.txt").exists() else ""
        if not hook_stage.bat_dau_bang_hook(sc, hook):
            _loi(ra, "hook", "cao", "script.txt không bắt đầu bằng hook đã khoá", "S3 phải bắt lỗi này — kiểm lại lean_script")
    t = hook_stage._title(S)
    if t and (m.get("promise") or {}).get("title") not in ("", t):
        _loi(ra, "hook", "cao", f"title.txt ≠ title lúc khoá hook ({(m.get('promise') or {}).get('title')!r})", "HOOK_STALE — khoá lại")


def kiem(slug_dir, profile_id):
    import profiles
    S = Path(slug_dir)
    prof = profiles.load(profile_id)
    ra = []
    v = kiem_video(S, ra)
    dur = (v or {}).get("dur", 0)
    chay_sub = bool((prof.get("assemble", {}) or {}).get("burn_subs", False))
    if v:
        kiem_phu_de_chay(S, dur, ra, chay=chay_sub)
    if not chay_sub:
        # Không cháy vào hình ⇒ file .srt là thứ DUY NHẤT mang phụ đề tới người xem. Thiếu nó thì
        # video câm chữ hoàn toàn, mà mp4 vẫn hợp lệ nên B8Q chẳng thấy gì.
        srt = next((S / t for t in ("voice_paced.srt", "voice.srt") if (S / t).exists()), None)
        if srt is None:
            _loi(ra, "phụ đề", "cao", "lane không cháy phụ đề mà cũng KHÔNG có file .srt để tải lên",
                 "chạy lại B4/B4a")
        # Bản ghi của chính bước ghép — tất định, khác hẳn suy đoán từ điểm ảnh.
        ri = S / "render_info.json"
        if ri.exists():
            try:
                if json.loads(ri.read_text(encoding="utf-8")).get("burned_subs"):
                    _loi(ra, "phụ đề", "cao",
                         "bước ghép ghi nhận ĐÃ CHÁY chữ vào hình, nhưng lane khai không cháy",
                         "thêm --khong-chay-phu-de rồi dựng lại B8")
            except Exception:
                pass
    if (prof.get("publish", {}) or {}).get("listing_external"):
        # Tiêu đề/mô tả/thumbnail do DỰ ÁN KHÁC lo (Lane G, anh chốt 2026-09-20) → gói giao chỉ có video + phụ đề.
        print("  (publish.listing_external: bỏ kiểm ảnh bìa + gói đăng tải — dự án khác lo)")
    else:
        kiem_thumbnail(S, ra)
        kiem_goi_dang_tai(S, prof, dur, ra)
    kiem_nguon(S, ra)
    kiem_bang_chung(S, ra)
    kiem_du_kien(S, ra)
    kiem_hook(S, prof, ra)
    return {"phat_hien": ra, "nang": [x for x in ra if x["sev"] == "cao"], "video": v}


def bao_cao(kq):
    n = kq["phat_hien"]
    v = kq.get("video") or {}
    print(f"\n=== B10 NGHIỆM THU TOÀN TẬP: {len(n)} phát hiện ({len(kq['nang'])} nặng) ===")
    if v:
        print(f"   video {v.get('w')}x{v.get('h')} · {v.get('fps')}fps · "
              f"{v.get('dur', 0)/60:.1f} phút · tiếng: {'có' if v.get('co_tieng') else 'KHÔNG'}")
    for x in n:
        print(f"   [{x['sev']}] {x['muc']}: {x['msg']}")
        if x["sua"]:
            print(f"        → {x['sua']}")
    if not n:
        print("   ✓ không thấy vấn đề nào — gói giao đủ và hợp lệ")
    return len(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="thư mục tập")
    ap.add_argument("--profile", required=True)
    a = ap.parse_args()
    kq = kiem(a.slug, a.profile)
    bao_cao(kq)
    return 1 if kq["nang"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
