# -*- coding: utf-8 -*-
r"""giao_hang.py — B11: gom ĐÚNG 3 FILE CẦN ĐỂ ĐĂNG vào thư mục của kênh.

    py -3.13 giao_hang.py --slug <thư mục tập> --profile <lane>
    py -3.13 giao_hang.py --slug <thư mục tập> --profile <lane> --ep 2 --ten ヴァレンティッチ失踪

Ra:  E:\CLAUDE\YOUTUBE\CHANEL\<kênh>\ep<N>-<tên tập>\
         final.mp4        ← video
         thumbnail.png    ← ảnh bìa
         listting.txt     ← tiêu đề + mô tả + mốc chương + hashtag + nguồn
         phude.srt        ← phụ đề tiếng Nhật, TỰ TẢI LÊN YouTube làm CC
         tomtat.txt       ← 2–3 dòng tiếng Việt: tập này kể chuyện gì
         review-vi.mp4    ← bản xem thử có phụ đề Việt (480p) — ĐỪNG ĐĂNG

Tên file CỐ ĐỊNH (anh chốt 2026-09-11) — thư mục đã mang tên tập nên file không cần lặp lại tên,
và tên cố định thì thao tác đăng lặp đi lặp lại không phải đọc lại tên mỗi lần.

VÌ SAO CÓ BƯỚC NÀY
------------------------------------------------------------------------------------------------
Thư mục tập chứa ~30 file (kịch bản, SRT, JSON của từng cổng QC, kho clip vài GB). Lúc ngồi đăng
video thì 27 file trong đó là nhiễu. Anh chốt: mỗi tập chỉ giữ lại 3 thứ ở nơi dễ lấy.

ĐIỀU PHẢI NGHĨ KỸ: SỔ NGUỒN KHÔNG NHÉT VỪA Ô MÔ TẢ
------------------------------------------------------------------------------------------------
`credits.txt` của một tập là **36 KB / 241 nguồn**, trong khi ô mô tả YouTube trần **5.000 ký tự**.
Dán cả vào là bị cắt cụt lặng lẽ; bỏ hẳn thì mất phần ghi nguồn.

Nên ở đây rút gọn theo ĐÚNG thứ luật đòi, chứ không phải theo thứ cho đẹp:
  · **CC BY** — giấy phép BUỘC nêu tên tác giả ⇒ liệt kê từng người. Đo thật: tập 1 có 6 file,
    tập 2 có 3 file. Vừa vặn vài dòng.
  · **Public Domain / NASA / CC0** — luật KHÔNG buộc ghi nguồn ⇒ gộp một dòng.
  · **Pexels** — giấy phép ghi thẳng "no attribution required" ⇒ gộp một dòng.
Sổ đầy đủ vẫn nằm trong thư mục tập, dùng khi bị khiếu nại.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path


def _ensure_std():
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent
TRAN_MO_TA = 5000
GOC_KENH = r"E:\CLAUDE\YOUTUBE\CHANEL"
TEN_FILE = {".mp4": "final.mp4", ".png": "thumbnail.png", ".txt": "listting.txt"}
TEN_TOM_TAT = "tomtat.txt"
TEN_SRT = "phude.srt"            # phụ đề tiếng Nhật — tự tải lên YouTube làm CC
TEN_REVIEW = "review-vi.mp4"     # bản xem thử có phụ đề Việt, KHÔNG đăng

# Ký tự Windows cấm trong tên thư mục/file (Nhật ngữ thì thoải mái, chỉ chặn mấy dấu này).
#
# XOÁ THẲNG là hỏng: đề tài 「ボブ・ラザー / エリア51」 ra 「ボブ・ラザー  エリア51」 — dính hai
# khoảng trắng giữa tên, nhìn y như lỗi gõ. Dấu `/` ở đây mang nghĩa "và/hoặc", nên đổi sang `・`
# (dấu ngăn của tiếng Nhật) mới giữ đúng ý, rồi mới xoá phần còn lại và gom khoảng trắng thừa.
def _sach_ten(x: str) -> str:
    x = re.sub(r"\s*[/\\]\s*", "・", str(x or ""))
    x = re.sub(r'[:*?"<>|]', "", x)
    return re.sub(r"\s{2,}", " ", x).strip(" ・")


def ten_de_tai(slug: Path) -> str:
    """Tên ngắn của tập, lấy từ dòng ĐỀ TÀI trong series_ctx.txt.

    Dòng đó dạng `ĐỀ TÀI: 多元宇宙 (Multiverse / 多世界解釈). Cung tiếng Nhật…` — phần cần lấy là
    cụm đầu, trước dấu `(` hoặc `.`. Không lấy title.txt vì tiêu đề YouTube dài 40+ ký tự kèm khối
    tag 【】, đặt làm tên thư mục thì vừa dài vừa khó đọc.
    """
    f = slug / "series_ctx.txt"
    if f.exists():
        for dong in f.read_text(encoding="utf-8", errors="replace").splitlines()[:5]:
            m = re.match(r"\s*ĐỀ TÀI[^:]*:\s*(.+)", dong)
            if m:
                t = re.split(r"[(（.]", m.group(1))[0].strip()
                if t:
                    return _sach_ten(t)[:60]
    return ""          # không đọc được tên đề tài — người gọi tự quyết cách đặt tên


def so_tap(slug: Path, ep=None) -> int:
    """Số tập = SỐ TRONG TÊN THƯ MỤC TẬP, và con số đó phải bằng STT trên trang tính.

    ⚠️ QUY TẮC ANH CHỐT 2026-09-11 — SỐ TẬP LẤY TỪ TRANG TÍNH, KHÔNG PHẢI ĐẾM THEO THỨ TỰ LÀM.
    Hồ sơ nghiên cứu nằm ở `_READY\\<nn>-<slug>`, và `<nn>` chính là STT của dòng trong tab của
    kênh. Đặt tên thư mục tập theo thứ tự MÌNH làm thì lệch ngay khi bỏ qua một đề tài: tập
    `01-valentich` (STT 1) từng bị đặt thành `ep02-valentich` chỉ vì nó là tập thứ hai được dựng,
    còn `ep01` đã bị một đề tài ngoài danh sách chiếm mất. Nhìn vào thư mục giao hàng là không
    truy ngược được dòng nào trên trang tính nữa.
    Đề tài KHÔNG có trong trang tính (tập thử trước khi có quy trình nghiên cứu) đánh số `ep00`.
    """
    if ep:
        return int(ep)
    m = re.search(r"ep(\d+)", slug.name, re.I)
    return int(m.group(1)) if m else 1


def khoi_nguon(slug: Path) -> str:
    """Khối ghi nguồn RÚT GỌN, đủ để dán vào ô mô tả (xem docstring đầu file)."""
    sc = slug / "scenes.json"
    if not sc.exists():
        return ""
    canh = json.loads(sc.read_text(encoding="utf-8"))
    # Gom theo FILE, không theo cảnh — một clip dùng 6 lần vẫn chỉ ghi nguồn một lần.
    theo_file = {}
    for c in canh:
        theo_file.setdefault(c["file"], (str(c.get("license") or ""), str(c.get("credit") or "")))
    ten_cc, co_pd, co_pexels = [], False, False
    for lic, credit in theo_file.values():
        if re.search(r"\bCC\s*BY\b", lic, re.I) and not re.search(r"\b(SA|NC|ND)\b", lic, re.I):
            t = credit.strip() or "(不明)"
            ten_cc.append(f"{t} / {lic}")
        elif re.search(r"pexels|pixabay|unsplash", lic, re.I):
            co_pexels = True
        else:
            co_pd = True
    ra = ["【映像・画像クレジット】"]
    if co_pd:
        ra.append("・パブリックドメイン素材（NASA / Wikimedia Commons / CC0）")
    if co_pexels:
        ra.append("・Pexels License（商用利用可・クレジット表記不要）")
    for t in sorted(set(ten_cc)):
        ra.append(f"・{t}")
    ra.append("※ 使用素材の完全な一覧は制作元で保管しています。")
    return "\n".join(ra)


def tom_tat_viet(slug: Path, tieu_de: str, force=False) -> str:
    """2–3 dòng TIẾNG VIỆT kể tập này nói về chuyện gì.

    Vì sao cần: video và mọi file đi kèm đều bằng tiếng Nhật. Nhìn thư mục `ep2-ヴァレンティッチ失踪`
    thì biết tên đề tài, nhưng không biết trong đó kể gì — lúc chọn tập để đăng, hoặc nửa năm sau
    mở lại, phải mở video ra nghe mới nhớ.

    CACHE Ở THƯ MỤC TẬP (`tomtat_vi.txt`), không sinh lại mỗi lần giao hàng: B11 chạy lại nhiều
    lần (mỗi lần dựng lại video là một lần), mà nội dung tập thì không đổi. Sinh lại là vừa tốn
    lượt gọi model vừa làm bản tóm tắt đổi chữ vô cớ giữa các lần.
    Muốn viết lại: xoá file đó, hoặc chạy với --tomtat-moi.
    """
    cache = slug / "tomtat_vi.txt"
    if cache.exists() and cache.read_text(encoding="utf-8").strip() and not force:
        return cache.read_text(encoding="utf-8").strip()

    ctx = slug / "series_ctx.txt"
    mo_ta = slug / "TIEU_DE_MO_TA.txt"
    khung = ""
    if ctx.exists():
        t = ctx.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"KHUNG \d+ CHƯƠNG:(.{0,900})", t, re.S)
        khung = (m.group(1) if m else t[:900]).strip()
    tom = mo_ta.read_text(encoding="utf-8", errors="replace")[:1800] if mo_ta.exists() else ""

    ask = "\n".join([
        "Viết TÓM TẮT TIẾNG VIỆT cho một video tài liệu tiếng Nhật, để người Việt đọc lướt là biết "
        "tập này kể chuyện gì.",
        "LUẬT: đúng 2–3 câu, mỗi câu một dòng. Văn kể gọn, KHÔNG quảng cáo, KHÔNG câu dẫn dụ, "
        "KHÔNG dùng 'video này', KHÔNG bịa thêm chi tiết ngoài tư liệu dưới đây.",
        "Câu đầu nêu SỰ VIỆC + mốc thời gian + nơi chốn. Câu sau nêu điểm gây tranh cãi và phần "
        "móc về Nhật Bản (nếu có).",
        "", f"TIÊU ĐỀ: {tieu_de}", "", "KHUNG CHƯƠNG:", khung, "", "MÔ TẢ (tiếng Nhật):", tom,
    ])
    try:
        from llm_client import chat
        kq = chat(ask, task="short", max_tokens=600, temperature=0.4, verbose=False)
    except Exception as e:
        print(f"  ⚠️ không sinh được tóm tắt tiếng Việt ({type(e).__name__}: {e})")
        return ""
    # `chat()` trả ChatResult chứ KHÔNG trả chuỗi. `str()` nó ra nguyên cả khối
    # "ChatResult(text='…', provider=…, usage=…)" — vẫn ghi ra file được, vẫn đọc được nội dung,
    # nên lỗi này KHÔNG làm chương trình chết, chỉ lặng lẽ nhét metadata vào bản tóm tắt.
    ra = getattr(kq, "text", None) or str(kq)
    ra = "\n".join(d.strip() for d in ra.strip().splitlines() if d.strip())[:900]
    cache.write_text(ra + "\n", encoding="utf-8")
    return ra


def chon_video_nguon(slug: Path):
    """(mp4: Path, co_hook: bool) — file VIDEO NGUỒN sẽ chép đi, ưu tiên `final_with_hook.mp4`.

    2026-09-23 (vá review HOOK, Việc 1): tách riêng + kiểm kích thước file hook ≥ 1 MB.
    Nếu file hook nhỏ hơn (ghi dở) thì fallback sang `final.mp4` + in cảnh báo.
    """
    mp4_hook = Path(slug) / "final_with_hook.mp4"
    mp4_normal = Path(slug) / "final.mp4"

    # 2026-09-23: chặn file video rỗng — ngưỡng an toàn 1 MB
    THRESHOLD = 1_000_000

    if mp4_hook.exists():
        kích_thước = mp4_hook.stat().st_size
        if kích_thước >= THRESHOLD:
            return mp4_hook, True
        else:
            print(f"  ⚠️ {mp4_hook.name} tồn tại nhưng chỉ {kích_thước} byte (< 1 MB) — "
                  f"hình như ghi dở. Giao bản {mp4_normal.name} thay thế.")
            return mp4_normal, False

    return mp4_normal, False


def _pad_ep(n):
    """So tap luon 2 chu so: ep7 -> ep07. Khong pad thi `ep10` sap truoc `ep7` khi liet ke thu muc,
    va lech voi cac lane dang dat ten ep01..ep04. Chuoi khong phai so thi giu nguyen."""
    t = str(n).strip()
    return f"{int(t):02d}" if t.isdigit() else t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="thư mục tập")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--ep", help="số tập (mặc định lấy từ tên thư mục epNN)")
    ap.add_argument("--ten", help="tên tập đặt cho thư mục (mặc định lấy dòng ĐỀ TÀI)")
    ap.add_argument("--kenh", help="tên kênh (mặc định profile.publish.upload_channel)")
    ap.add_argument("--tomtat-moi", action="store_true",
                    help="viết lại tóm tắt tiếng Việt (mặc định dùng bản đã lưu)")
    ap.add_argument("--out", help="thư mục gốc chứa các kênh (mặc định E:/CLAUDE/YOUTUBE/CHANEL)")
    a = ap.parse_args()

    import profiles
    prof = profiles.load(a.profile)
    slug = Path(a.slug)
    if not slug.is_absolute():
        slug = ROOT / prof.get("slug_dir", "assets") / slug
    if not slug.exists():
        raise SystemExit(f"✗ không thấy thư mục tập: {slug}")

    pub = prof.get("publish", {}) or {}
    kenh = a.kenh or pub.get("upload_channel")
    if not kenh:
        raise SystemExit("✗ chưa biết kênh. Khai `publish.upload_channel` trong profile "
                         "hoặc truyền --kenh")
    # Thư mục kênh nằm NGOÀI dự án: mỗi kênh một nơi, không lẫn vào assets của pipeline.
    goc = Path(a.out or pub.get("upload_dir") or GOC_KENH)
    # TÊN THƯ MỤC GIAO HÀNG = ĐÚNG TÊN SLUG, chữ Latin: `ep03-bob-lazar`.
    #
    # ⚠️ ANH CHỐT 2026-09-11, ĐỪNG ĐỔI LẠI SANG TÊN TIẾNG NHẬT.
    # Quy ước ban đầu là `ep<số>-<tên đề tài tiếng Nhật>` (`ep1-多元宇宙`), nhưng dùng thật thì
    # hỏng: anh gõ đường dẫn tay để vào lấy file, mà tên kiểu `ep3-ボブ・ラザー・エリア51` thì
    # **không gõ được** — phải copy-paste, và trên một số công cụ/terminal còn hiện thành dấu hỏi.
    # Tên slug đã có sẵn, đã là chữ Latin, đã trùng với thư mục trong `assets/` nên tra ngược rất
    # nhanh. Tên đề tài tiếng Nhật vẫn còn nguyên ở `listting.txt` và `tomtat.txt` bên trong.
    n = so_tap(slug, a.ep)
    if a.ten:
        nhan = f"ep{_pad_ep(n)}-{_sach_ten(a.ten)}"
    elif re.match(r"^ep\d+-(.+)$", slug.name, re.I):
        nhan = _sach_ten(slug.name)     # slug đã mang sẵn "epNN-", đừng ghép thành "ep2-ep02-…"
    else:
        # Lane chưa đặt tên slug theo dạng epNN- thì mới phải đi tìm tên khác.
        nhan = f"ep{_pad_ep(n)}-{ten_de_tai(slug) or _sach_ten(slug.name)}"
    dich = goc / kenh / nhan
    dich.mkdir(parents=True, exist_ok=True)

    # 2026-09-23 (vá review HOOK, Việc 1a): tập đã dựng xong hook (bước 3 ghép `final_with_hook.mp4`
    # ngay cạnh `final.mp4`, xem docs/GIAO_VIEC_BUOC3_AGENT.md mục 9.5) thì phải GIAO BẢN CÓ HOOK —
    # trước đây hàm này chỉ biết mỗi `final.mp4`, nên tập chạy chế độ vá (giữ nguyên video cũ, chỉ
    # thêm hook vào đầu) bị giao đi ĐÚNG bản KHÔNG có hook mà không ai hay. Tên file ĐÍCH vẫn giữ
    # nguyên `final.mp4` (quy ước cột TEN_FILE không đổi) — chỉ đổi NGUỒN chép.
    mp4, co_hook = chon_video_nguon(slug)
    if co_hook:
        print(f"  · tập có {mp4.name} → giao BẢN CÓ HOOK (nguồn = {mp4.name}, đích vẫn "
              f"tên {TEN_FILE['.mp4']})")
    png = next((slug / t for t in ("thumbnail_final.png", "thumb_final.png")
                if (slug / t).exists()), None)
    txt = slug / "TIEU_DE_MO_TA.txt"
    # publish.listing_external (Lane G, 2026-09-20): tiêu đề/mô tả/thumbnail do DỰ ÁN KHÁC lo → gói giao chỉ
    # final.mp4 + phude.srt + review-vi.mp4 (+ tomtat). Không đòi thumbnail/TIEU_DE_MO_TA.
    ngoai = bool(pub.get("listing_external"))
    can = [("final.mp4", mp4)] if ngoai else [("final.mp4", mp4), ("thumbnail", png), ("TIEU_DE_MO_TA.txt", txt)]
    thieu = [t for t, p in can if not p or not p.exists()]
    if thieu:
        raise SystemExit(f"✗ tập chưa xong, thiếu: {', '.join(thieu)}")

    # --- file mô tả: bản gốc + khối nguồn rút gọn (bỏ khi listing_external)
    noi_dung = txt.read_text(encoding="utf-8", errors="replace").rstrip() if not ngoai else ""
    ng = khoi_nguon(slug)
    if ng and "映像・画像クレジット" not in noi_dung:
        them = "\n\n" + "-" * 100 + "\n" + ng
        if len(noi_dung) + len(them) <= TRAN_MO_TA:
            noi_dung += them
        else:
            print(f"  ⚠️ mô tả {len(noi_dung)} ký tự, thêm khối nguồn sẽ vượt trần {TRAN_MO_TA} "
                  f"⇒ BỎ khối nguồn. Rút gọn mô tả rồi chạy lại.")
    if not ngoai:
        (dich / TEN_FILE[".txt"]).write_text(noi_dung + "\n", encoding="utf-8")
    else:
        print("  · listing_external: không giao thumbnail/listting (dự án khác lo)")

    for nguon, duoi in [(mp4, ".mp4")] + ([] if (ngoai or not png) else [(png, ".png")]):
        ra = dich / TEN_FILE[duoi]
        if ra.exists() and ra.stat().st_size == nguon.stat().st_size:
            print(f"  · {ra.name} đã có, bỏ qua")
            continue
        shutil.copy2(nguon, ra)
        print(f"  ✓ {ra.name}  ({ra.stat().st_size/1024/1024:.0f} MB)")

    # Phụ đề KHÔNG cháy vào hình nữa ⇒ file .srt là thứ mang phụ đề tới người xem, phải đi kèm.
    srt = next((slug / t for t in ("voice_paced.srt", "voice.srt") if (slug / t).exists()), None)
    if srt:
        shutil.copy2(srt, dich / TEN_SRT)
        print(f"  ✓ {TEN_SRT}  (tải lên YouTube làm CC)")
    # Bản xem thử tiếng Việt: để anh soi nội dung, KHÔNG phải bản đăng.
    # Hai lane dat ten khac nhau cho ban duyet tieng Viet: lane stock sinh ,
    # lane nao-Claude (render_engine + sub_vi.py) sinh . Nhan CA HAI — truoc day
    # chi tim mot ten nen ban tieng Viet cua lane kia roi mat IM LANG khi giao hang.
    rv = next((slug / t for t in ("review_vi.mp4", "final_vi.mp4") if (slug / t).exists()), slug / "review_vi.mp4")
    if rv.exists():
        ra_rv = dich / TEN_REVIEW
        if not (ra_rv.exists() and ra_rv.stat().st_size == rv.stat().st_size):
            shutil.copy2(rv, ra_rv)
        print(f"  ✓ {TEN_REVIEW}  ({ra_rv.stat().st_size/1024/1024:.0f} MB · bản xem, đừng đăng)")

    tt = tom_tat_viet(slug, noi_dung.splitlines()[0] if noi_dung else nhan, a.tomtat_moi)
    if tt:
        (dich / TEN_TOM_TAT).write_text(tt + "\n", encoding="utf-8")
        print(f"  ✓ {TEN_TOM_TAT} ({len(tt.splitlines())} dòng)")
    print(f"✓ B11 giao hàng: {dich}")
    print(f"  mô tả {len(noi_dung)} ký tự (trần {TRAN_MO_TA})")


if __name__ == "__main__":
    main()
