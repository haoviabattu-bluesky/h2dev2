"""publish_kit.py — B9: sinh GÓI ĐĂNG TẢI (tiêu đề/mô tả/thẻ/chương/thumbnail check) cho 1 video.

Vì sao tách riêng (khác `render_engine.py`): B9 vốn chỉ có ở tool não-ramcloud (`make_video.py::
b9_publish`) — tool não-Claude (`render_engine.py`) dừng ở B8Q, video ra `final.mp4` xong là hết,
chưa có file để copy dán lên YouTube. File này VIẾT LẠI cùng logic (mốc chương bám lời đọc thật,
tiêu đề/thẻ/mô tả qua `ai_steps.publish_kit` — LLM SEO, KHÔNG phải "não sáng tạo" chính của video),
KHÔNG import/sửa `make_video.py` (2 tool tách hẳn — [[hai-tool-exe-tach-han]]).

Input (trong thư mục slug): script.txt · voice_paced.srt (hoặc voice.srt) · profile (qua --profile).
Output: DANG-TAI.txt (checklist đầy đủ) · TIEU_DE_MO_TA.txt (1 khối dán thẳng ô mô tả YouTube).

Dùng:
  py -3.13 publish_kit.py --slug <đường dẫn slug> --profile satori-jp-obaa
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()

import ai_steps
import profiles
import storyboard


def _mmss(sec):
    """Mốc thời gian kiểu YouTube. Video ≥1 giờ PHẢI ghi h:mm:ss, nếu không chương bị bỏ qua."""
    sec = max(0, int(sec))
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


_KY_HIEU_NOI_BO = re.compile(r"[⭐★☆※▲●◆→]+")


def _don_ten_chuong(marker, dong):
    """Bỏ ký hiệu NỘI BỘ khỏi tên chương trước khi đưa lên phần mô tả công khai.

    Hồ sơ đề tài đánh dấu chương quan trọng bằng ⭐ ("第4章 ⭐ MÓC VỀ NHẬT BẢN — …") để người viết
    kịch bản chú ý. Model chép nguyên cả ⭐ vào kịch bản, rồi mốc chương đọc từ kịch bản mang luôn
    ⭐ ra ô mô tả YouTube — người xem thấy 「第4章 ⭐ 日航1628便事件」, trông như ghi chú nội bộ lọt
    ra ngoài. Đã lên hình thật ở tập 2.
    Không sửa ở kịch bản vì kịch bản đã thu giọng xong; đây thuần là chuyện HIỂN THỊ.
    """
    con = _KY_HIEU_NOI_BO.sub(" ", dong[len(marker):])
    con = re.sub(r"\s{2,}", " ", con).strip(" -—–:：")
    return f"{marker} {con}".strip()


def _chuong_theo_marker(prof, script, cues):
    """Mốc chương lấy từ CHÍNH LỜI ĐỌC (profiles.gate().chapter_markers), không chia đều theo thời
    gian — kênh nào đọc rõ "第1章…" thì mô tả PHẢI trùng lúc người dẫn nói ra, kẻo mô tả ghi 第4章
    ở 12:39 trong khi video nói ở 19:31 (đo thật, xem ai_steps/make_video)."""
    marks = profiles.gate(prof).get("chapter_markers") or []
    if not marks or not cues:
        return []
    ten = {}
    for dong in script.splitlines():
        d = dong.strip()
        for m in marks:
            if d.startswith(m):
                ten[m] = _don_ten_chuong(m, d)[:60]
    out = []
    for m in marks:
        cue = next((c for c in cues if m in c[2].replace(" ", "")), None)
        if cue:
            out.append((cue[0], ten.get(m, m)))
    if not out:
        return []
    if out[0][0] > 10:
        out.insert(0, (0.0, "導入" if prof.get("language") == "ja" else "Mở đầu"))
    else:
        out[0] = (0.0, out[0][1])
    return out if len(out) >= 3 else []


def _chuong_chia_deu(cues, so_chuong):
    """[(giây, lời mẫu)] chia đều theo THỜI GIAN THẬT khi kịch bản không đánh dấu chương.

    Luật chương YouTube: mốc ĐẦU phải 0:00, ≥3 chương, mỗi chương ≥10 giây."""
    if not cues:
        return []
    tong = cues[-1][1]
    buoc = tong / so_chuong
    out = []
    for i in range(so_chuong):
        t = 0.0 if i == 0 else i * buoc
        phan = [c for c in cues if t <= c[0] < t + buoc]
        if not phan:
            continue
        if out and phan[0][0] - out[-1][0] < 10:
            continue
        out.append((0.0 if i == 0 else phan[0][0], " ".join(c[2] for c in phan[:6])))
    if out:
        out[0] = (0.0, out[0][1])
    return out if len(out) >= 3 else []


def _kiem_thumb(path):
    """Ảnh bìa có đúng chuẩn YouTube không: ≥1280×720, tỉ lệ 16:9, dưới 2 MB.

    ⚠️ render_engine.py xuất `thumb_final.png` (KHÁC make_video.py xuất `thumbnail_final.png`) —
    dò cả hai tên, đúng cái nào dùng cái đó."""
    p = Path(path)
    if not p.exists():
        return "CHƯA CÓ ảnh bìa"
    mb = p.stat().st_size / 1e6
    try:
        from PIL import Image
        w, h = Image.open(p).size
    except Exception:
        return f"{p.name} ({mb:.1f} MB) — không đọc được kích thước"
    loi = []
    if w < 1280 or h < 720:
        loi.append(f"nhỏ hơn 1280x720 (đang {w}x{h})")
    if abs(w / h - 16 / 9) > 0.02:
        loi.append(f"không phải 16:9 (đang {w}x{h})")
    if mb > 2:
        loi.append(f"nặng hơn 2 MB ({mb:.1f} MB) — YouTube sẽ từ chối")
    return f"{p.name} — {w}x{h}, {mb:.1f} MB" + (" · ⚠ " + "; ".join(loi) if loi else " · ĐẠT")


def build(slug_dir, profile_id, minutes=0.0):
    """Sinh DANG-TAI.txt + TIEU_DE_MO_TA.txt trong slug_dir. Trả True nếu ra được gói."""
    S = Path(slug_dir)
    prof = profiles.load(profile_id)
    sf = S / "script.txt"
    if not sf.exists():
        print("[B9] chưa có kịch bản → bỏ qua")
        return False
    script = sf.read_text(encoding="utf-8")
    srt_f = S / "voice_paced.srt"
    if not srt_f.exists():
        srt_f = S / "voice.srt"
    cues = storyboard.parse_cues(srt_f) if srt_f.exists() else []

    ten_that = _chuong_theo_marker(prof, script, cues)
    if ten_that:
        secs = ten_that
        print("[B9] mốc chương lấy theo lời đọc: "
              + " · ".join(f"{_mmss(t)} {n[:14]}" for t, n in ten_that))
    else:
        mn = minutes or profiles.target_minutes(prof)
        so = max(4, min(10, round((cues[-1][1] / 60 if cues else mn) / 4)))
        secs = _chuong_chia_deu(cues, so)

    kit = ai_steps.publish_kit(prof, script, secs or [(0.0, script[:400])])
    if not kit:
        print("[B9] không sinh được gói đăng tải (LLM lỗi/rỗng) → bỏ qua")
        return False

    titles = [t for t in (kit.get("titles") or []) if t][:3]
    tf = S / "title.txt"
    if tf.exists() and tf.read_text(encoding="utf-8").strip():
        chot = tf.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        titles = [chot] + [t for t in titles if t != chot]
        print(f"[B9] tiêu đề CHỐT theo title.txt ({len(chot)} ký tự): {chot[:50]}")
    if not titles:
        titles = [script.strip().splitlines()[0][:90]] if script.strip() else ["(chưa có tiêu đề)"]

    tags = [t for t in (kit.get("tags") or []) if t]
    gon, do_dai = [], 0
    for t in tags:                                    # thẻ YouTube tính TỔNG 500 ký tự
        if do_dai + len(t) + 2 > 480:
            break
        gon.append(t); do_dai += len(t) + 2

    hashtags = [h if h.startswith("#") else "#" + h for h in (kit.get("hashtags") or [])][:8]
    if ten_that:
        dong_ch = [f"{_mmss(t)} {n}" for t, n in ten_that]
    else:
        ten_ch = kit.get("chapters") or []
        dong_ch = [f"{_mmss(t)} {ten_ch[i] if i < len(ten_ch) else f'Phần {i+1}'}"
                   for i, (t, _) in enumerate(secs)]

    # TIEU_DE_MO_TA.txt — 1 khối dán thẳng, quy cách cố định (xem [[thumbnail-motip-va-file-dang-tai]])
    GACH = "-" * 100
    tu_khoa = ",".join(gon[:5])
    mo_ta_ngan = (kit.get("description") or "").strip()
    cam_on = (kit.get("loi_cam_on") or "").strip()
    (S / "TIEU_DE_MO_TA.txt").write_text("\n".join([
        titles[0], "", tu_khoa, "", mo_ta_ngan, "", GACH, "Timestamps:", "",
        "\n".join(dong_ch), GACH, "", cam_on, "", GACH, " ".join(hashtags),
    ]), encoding="utf-8")

    mo_ta = mo_ta_ngan
    if dong_ch:
        mo_ta += "\n\n" + "\n".join(dong_ch)
    if hashtags:
        mo_ta += "\n\n" + " ".join(hashtags)
    thumb = _kiem_thumb(S / "thumb_final.png")
    srt_ten = srt_f.name if srt_f.exists() else "(chưa có)"
    L = [
        "=" * 78, f"GÓI ĐĂNG TẢI — {S.name}", "=" * 78,
        "Copy từng khối bên dưới dán thẳng vào form tải lên của YouTube.", "",
        "-" * 78, "1) TIÊU ĐỀ  (chọn 1 — tối đa 100 ký tự)", "-" * 78,
    ]
    for i, t in enumerate(titles, 1):
        canh = "" if len(t) <= 100 else f"   ⚠ DÀI {len(t)} ký tự, phải cắt bớt"
        L.append(f"[{i}] {t}   ({len(t)} ký tự){canh}")
    L += ["", "-" * 78, "2) MÔ TẢ  (dán nguyên khối — đã gồm mốc chương + hashtag)", "-" * 78,
          mo_ta, "", f"   → {len(mo_ta)} ký tự" +
          (" ⚠ VƯỢT 5.000, phải cắt" if len(mo_ta) > 5000 else " (tối đa 5.000)"),
          "", "-" * 78, "3) THẺ / TAGS  (dán cả dòng)", "-" * 78,
          ", ".join(gon), "", f"   → {len(', '.join(gon))} ký tự (tối đa 500)"
          + (f" · đã bỏ bớt {len(tags) - len(gon)} thẻ cho vừa" if len(gon) < len(tags) else ""),
          "", "-" * 78, "4) ẢNH BÌA", "-" * 78, "   " + thumb,
          "", "-" * 78, "5) BÌNH LUẬN GHIM  (đăng xong thì dán rồi ghim lên đầu)", "-" * 78,
          (kit.get("pinned_comment") or "").strip(),
          "", "-" * 78, "6) CÁC MỤC PHẢI TỰ CHỌN TRONG FORM", "-" * 78,
          f"   Danh mục            : {kit.get('category') or 'People & Blogs'}",
          f"   Ngôn ngữ video      : {ai_steps.LANG_NAME.get(prof.get('language','ja'), '')}",
          f"   Phụ đề              : tải file {srt_ten} lên (cùng thư mục này)",
          "   Dành cho trẻ em     : KHÔNG  ← bắt buộc trả lời, chọn sai là bị tắt bình luận",
          "   Nội dung do AI tạo  : CÓ — khai ở mục 'Nội dung tổng hợp/đã chỉnh sửa'.",
          "                         Giọng đọc là AI nên PHẢI khai; giấu là rủi ro gậy bản quyền.",
          "   Giới hạn độ tuổi    : không",
          "   Bình luận           : bật, sắp xếp theo 'Mới nhất'",
          "   Danh sách phát      : thêm vào playlist của kênh",
          "   Màn hình kết thúc   : gắn 1 video liên quan + nút đăng ký",
          "", "-" * 78, "7) TỰ KIỂM TRƯỚC KHI BẤM ĐĂNG", "-" * 78,
          "   [ ] Nghe lại 30 giây đầu — hỏng phần mở là mất hết lượt xem",
          "   [ ] Xem thumbnail ở cỡ NHỎ, chữ còn đọc được không",
          "   [ ] Tiêu đề khớp nội dung (câu view lố bị hạ đề xuất)",
          "   [ ] Đã khai nội dung AI",
          "   [ ] Đặt lịch đăng vào khung giờ khán giả của kênh online", "",
    ]
    (S / "DANG-TAI.txt").write_text("\n".join(L), encoding="utf-8")
    print(f"[B9] gói đăng tải → DANG-TAI.txt · {len(titles)} tiêu đề · {len(gon)} thẻ · "
          f"{len(dong_ch)} chương")
    print(f"      tiêu đề gợi ý: {titles[0]}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--minutes", type=float, default=0.0)
    a = ap.parse_args()
    ok = build(a.slug, a.profile, a.minutes)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
