# -*- coding: utf-8 -*-
r"""huong_dan_tab_moi.py — viết FILE HƯỚNG DẪN cho TAB MỚI + ghi ĐÈ cột K (GHI CHÚ) trang tính (anh chốt 2026-10-01).

Hai mốc dừng của mọi lane chuẩn, tab mới mở ra chỉ cần đọc ĐÚNG 1 file, không đọc lại từ đầu:
  1. `--loai may3`   viết kịch bản xong, đã giao máy 3 (D = "Chờ kiểm tra kịch bản")
                     → <slug_dir>\<slug>\HUONG_DAN_NHAN_MAY3.md   · ghi K ở DÒNG CỦA TẬP ĐÓ.
  2. `--loai tiep`   tập xong, đã giao máy 2 (dong_goi_may2 --job)
                     → <slug_dir>\HUONG_DAN_TAP_TIEP_THEO.md       · ghi K ở DÒNG TẬP KẾ (STT+1; dòng kế chưa có gì
                       ở A/B vẫn ghi dòng kế — 04/10).
Tự gọi: dong_goi_may2 --job (mốc 2). Mốc 1 KHÔNG còn tự gọi từ 2026-10-02 (anh chốt: nhận bản máy 3 theo 1 file chung
docs\NHAN_KICH_BAN_MAY3.md, không file riêng tập/cột K) — `--loai may3` chỉ còn chạy tay. Phần máy tra được (đường dẫn, dòng
sheet, lệnh có sẵn tham số thật, số chữ bản khoá…) tool tự điền. Phần CHỈ tab đang làm mới biết (vai, chỗ cần soi,
bẫy vừa gặp) → tab viết vào 1 file rồi chạy lại với `--ghi-chu-file`; chạy lại KHÔNG có cờ đó thì giữ nguyên ghi chú cũ.

Cột K: chỉ ghi đúng 1 ô, đọc lại tiêu đề K1 phải là "GHI CHÚ" (khác → DỪNG, cột đổi chỗ). Không xoá gì.

Dùng:
  py -3.13 -X utf8 pipeline\huong_dan_tab_moi.py --loai may3 --profile <lane> --slug <tập> [--ghi-chu-file <f>] [--dry]
  py -3.13 -X utf8 pipeline\huong_dan_tab_moi.py --loai tiep --profile <lane> --slug <tập vừa giao> [--ghi-chu-file <f>] [--dry]
"""
import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import profiles  # noqa: E402

COT_K = "K"
TIEU_DE_COT_K = "GHI CHÚ"
PY = r"py -3.13 -X utf8"
P = str(HERE)                       # E:\CLAUDE\YOUTUBE\h2dev\pipeline
TEN_MAY3 = "HUONG_DAN_NHAN_MAY3.md"
TEN_TIEP = "HUONG_DAN_TAP_TIEP_THEO.md"
GC_DAU = "<!-- GHI_CHU_TAB:BAT_DAU -->"
GC_CUOI = "<!-- GHI_CHU_TAB:HET -->"


# ------------------------------------------------------------------ tra cứu
def _bat_dau(pid):
    f = ROOT / "docs" / "BAT_DAU_LANE" / f"{pid}.md"
    return f if f.exists() else None


def _sop(bat_dau):
    if not bat_dau:
        return None
    m = re.search(r"docs[\\/](SOP_[A-Za-z0-9_]+\.md)", bat_dau.read_text(encoding="utf-8"))
    f = ROOT / "docs" / m.group(1) if m else None
    return f if f and f.exists() else None


def _json(f):
    try:
        return json.loads(Path(f).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _tab(prof):
    pub = prof.get("publish") or {}
    return pub.get("sheet_tab") or pub.get("upload_channel") or prof["id"]


def _doc_dong(dg, tab, dong):
    v = dg.svc(doc_thoi=True).values().get(spreadsheetId=dg.SHEET_ID,
                                            range=f"{tab}!A{dong}:K{dong}").execute().get("values", [[]])
    r = (v[0] if v else []) + [""] * 11
    return [str(x).strip() for x in r[:11]]


def _ghi_k(dg, tab, dong, gia_tri, dry=False):
    s = dg.svc(doc_thoi=True)
    hd = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!{COT_K}1").execute().get("values", [[""]])
    ten = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten != TIEU_DE_COT_K:
        raise SystemExit(f"cột {COT_K} dòng 1 tab {tab} là '{ten or '(trống)'}', không phải '{TIEU_DE_COT_K}' → DỪNG")
    if dry:
        print(f"  (dry) sẽ ghi đè {tab}!{COT_K}{dong} = {gia_tri!r}")
        return
    dg.svc(doc_thoi=False).values().update(spreadsheetId=dg.SHEET_ID, range=f"{tab}!{COT_K}{dong}",
                                           valueInputOption="RAW", body={"values": [[gia_tri]]}).execute()
    print(f"  ✓ ghi đè {tab}!{COT_K}{dong} (GHI CHÚ) = {gia_tri.splitlines()[0] if gia_tri else ''} …")


def _ghi_chu(f_cu, f_moi):
    """Ghi chú riêng của tab: lấy từ --ghi-chu-file, không có thì giữ khối cũ trong file đang có."""
    if f_moi:
        return Path(f_moi).read_text(encoding="utf-8").strip()
    if f_cu.exists():
        t = f_cu.read_text(encoding="utf-8")
        if GC_DAU in t and GC_CUOI in t:
            return t.split(GC_DAU, 1)[1].split(GC_CUOI, 1)[0].strip()
    return ""


def _khoi_ghi_chu(gc, loai):
    goi_y = ("vai/tên nhân vật trong bản khoá, chỗ anh nên soi, câu cửa miệng, số liệu cần giữ, bẫy hook"
             if loai == "may3" else "bài học tập vừa xong, bẫy gặp phải (Grok/ảnh/TTS), đề tài/slug tập kế nếu đã chốt")
    rong = (f"⚠ CHƯA CÓ — tab trước PHẢI bổ sung ({goi_y}) bằng:\n"
            f"`{PY} {P}\\huong_dan_tab_moi.py --loai {loai} --profile <lane> --slug <tập> --ghi-chu-file <file .md>`")
    return f"{GC_DAU}\n{gc or rong}\n{GC_CUOI}"


def _luat_chung(pid):
    return [
        "## LUẬT CỨNG (vi phạm = dừng)",
        f"- Mở đầu mọi báo cáo bằng `@lane:{pid}`. Chạy mọi lệnh tại `{ROOT}`.",
        "- Máy 1 CHỈ bước 1 + hình hook: CẤM `make_video --from B4`, `--den B5/B8`; chỉ `--den B3G`, `--only B5W`, `--only B5P`.",
        "- KHÔNG sửa tay `script.txt` (sha lệch = mọi bước sau dừng).",
        "- Tool chạy lâu (ảnh/Grok/TTS) → Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt.",
        "- Không kill Chrome theo tên; không xoá dữ liệu sheet. Chữ Nhật gửi anh kèm dịch Việt; đường dẫn ghi tuyệt đối.",
        "- Tiêu đề/mô tả/thumbnail: TẮT toàn dự án từ 01/10 — KHÔNG gọi `goi_title.py`, không làm thumbnail.",
    ]


# ------------------------------------------------------------------ mốc 1: nhận kịch bản máy 3
def viet_may3(prof, slug, ghi_chu_file=None, dry=False):
    import dong_goi_may2 as dg
    import review_may3
    pid = prof["id"]
    d = ROOT / prof["slug_dir"] / slug
    tab = _tab(prof)
    dong = dg._stt_theo_slug(tab, slug) + 1
    job = review_may3.review_di(prof, slug)
    lock = _json(d / "script.lock.json")
    hook = d / "hook" / "hook_locked.txt"
    ten_tap = (d / "title.txt").read_text(encoding="utf-8").strip() if (d / "title.txt").exists() else ""
    bd = _bat_dau(pid)
    sop = _sop(bd)
    out = d / TEN_MAY3
    gc = _ghi_chu(out, ghi_chu_file)
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# NHẬN KỊCH BẢN MÁY 3 → LÀM TIẾP — lane `{pid}` · tập `{slug}`",
        "",
        f"> Tool `huong_dan_tab_moi.py` viết {now} lúc DỪNG giao máy 3. Dùng khi anh báo \"anh sửa xong kịch bản\" hoặc ô D{dong}",
        f"> tab `{tab}` = `Đã sửa kịch bản`. **Tab mới: đọc HẾT file này rồi làm liền từ mục 1 tới mục 5, KHÔNG đọc lại",
        "> SOP/CHANNEL_DNA/profile/lịch sử chat** — chỉ mở thêm file khi lệnh báo lỗi cần quyết định.",
        "",
        "## 0. ĐANG Ở ĐÂU",
        "| Mục | Giá trị |",
        "|---|---|",
        f"| Thư mục tập | `{d}\\` |",
        f"| Bản gửi máy 3 (anh sửa thẳng) | `{job}\\script.txt` |",
        f"| Sheet | tab `{tab}` dòng {dong} (C = thư mục, D = trạng thái, K = file này) |",
        f"| Tiêu đề làm việc | {ten_tap or '(chưa có title.txt)'} |",
        f"| Bản khoá trước khi anh sửa | {lock.get('chars', '?')} chữ ≈ {lock.get('minutes', '?')}' · state {lock.get('state', '?')} · "
        f"sha `{(lock.get('script_sha256') or '')[:10]}…` · khoá {lock.get('at', '?')} |",
        f"| Hook đã khoá | `{hook}` ({len(hook.read_text(encoding='utf-8').strip()) if hook.exists() else 0} chữ) |",
        f"| Cửa vào lane (chỉ khi cần) | `{bd or '(chưa có)'}` mục ⚡ ĐỌC NHANH · SOP `{sop or '(chưa có)'}` |",
        "",
        *_luat_chung(pid),
        "",
        "## 1. KIỂM TRẠNG THÁI",
        "```bat",
        f"{PY} {P}\\review_may3.py --trang-thai --profile {pid}",
        "```",
        f"- D{dong} vẫn `Chờ kiểm tra kịch bản` → nhắc anh đổi D{dong}, DỪNG (chỉ khi anh bảo \"cứ nhận\" mới thêm `--force` ở mục 2).",
        f"- Không có `make_video` nào của `{pid}` đang chạy cùng slug (cấm chạy đè).",
        "",
        "## 2. NHẬN BẢN SỬA (0 LLM, không sửa 1 chữ)",
        "```bat",
        f"{PY} {P}\\review_may3.py --nhan --profile {pid} --slug {slug}",
        "```",
        f"- Kết quả đo: `{d}\\NHAN_MAY3.md`. CHẶN (ngắn <70% ngân sách / số liệu ngoài `series_ctx.txt`) → báo anh 1 dòng, DỪNG.",
        f"- Kiểm hook: so `{hook}` với đoạn đầu `{d}\\script.txt`; lệch ranh giới → khoá lại tay theo lệnh ở "
        f"`{ROOT}\\docs\\NHAN_KICH_BAN_MAY3.md` §2.",
        "",
        "## 3. CAST + PROMPT ẢNH THÂN",
        f"- Viết/kiểm `{d}\\characters.json` theo TÊN THẬT trong bản anh sửa (giọng lấy từ `voice` trong "
        f"`{ROOT}\\profiles\\profiles\\{pid}.json`; luật ngoại hình/tuổi: `{ROOT}\\docs\\QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md`).",
        "```bat",
        f"{PY} {P}\\gan_vai.py --profile {pid} --slug {d}",
        f"{PY} {P}\\make_video.py --profile {pid} --slug {slug} --only B5W",
        f"{PY} {P}\\make_video.py --profile {pid} --slug {slug} --only B5P",
        "```",
        "",
        "## 4. HÌNH + CLIP HOOK (theo hook ANH SỬA)",
        "```bat",
        f"{PY} {P}\\hook_storyboard.py --profile {pid} --slug {slug} --force",
        ":: ảnh hook: Google Flow Ultra (cổng 9350, 1 tập/lượt) → cổng bận thì 9router → gpti2 (chạy nền)",
        f"{PY} {P}\\anh_hook.py {d}\\hook",
        ":: → QC nhìn ảnh thật → chữ đạo cụ → clip Google Vids (tools\\hook_lane_g\\vids_hook.py) → nhạc nền (CẤM SFX đồ vật) — đúng lệnh ở SOP lane",
        f"{PY} {P}\\hook_tap_md.py --slug {d} --profile {pid}",
        "```",
        f"- Ảnh/clip hook làm theo hook CŨ mà hook đổi → làm lại. Luật nhạc nền + bối cảnh cảnh: `{ROOT}\\docs\\QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md`.",
        "",
        "## 5. GIAO MÁY 2 (tự ghi D = Đã giao máy 2 + K = lệnh cho máy 2, H = cần ảnh, tự viết hướng dẫn tập kế)",
        "```bat",
        f"{PY} {P}\\dong_goi_may2.py --job {pid} {slug}",
        "```",
        f"- Xong → bổ sung ghi chú cho file `{prof['slug_dir']}\\{TEN_TIEP}` (bài học tập này) bằng `--loai tiep --ghi-chu-file`.",
        "- KHÔNG gọi TITLE / thumbnail (đã tắt toàn dự án).",
        "",
        "## 6. GHI CHÚ RIÊNG TẬP NÀY (tab viết kịch bản để lại)",
        _khoi_ghi_chu(gc, "may3"),
        "",
    ]
    return _xuat(dg, tab, dong, out, L, "Tab mới — nhận KB máy 3", dry)


# ------------------------------------------------------------------ mốc 2: làm tập tiếp theo
def viet_tiep(prof, slug, ghi_chu_file=None, dry=False):
    import dong_goi_may2 as dg
    pid = prof["id"]
    goc = ROOT / prof["slug_dir"]
    d = goc / slug
    tab = _tab(prof)
    stt = dg._stt_theo_slug(tab, slug)
    dong = stt + 1
    ke = _doc_dong(dg, tab, dong + 1)
    # 2026-10-12 (Lane L ep15 giao SAU ep16/ep17): dòng kế đã có cột D (tập kế đã bắt đầu/xong) → KHÔNG ghi đè
    # hướng dẫn + ô K dòng đó (đã đè mất lệnh máy 2 của ep16 ở K17). Hướng dẫn tập kế đúng đã được tập mới hơn viết.
    if (ke[3] if len(ke) > 3 else "").strip():
        print(f"  · dòng {dong + 1} đã có D = {ke[3].splitlines()[0]!r} (tập kế đã chạy) → giữ nguyên "
              f"{goc / TEN_TIEP} + ô K dòng đó")
        return None
    co_ke = bool(ke[0] or ke[1])
    m = re.match(r"ep(\d+)", slug)
    nn = (int(m.group(1)) + 1) if m else stt + 1
    slug_ke = Path(ke[2].replace("\\", "/")).name if ke[2] else f"ep{nn:02d}-<slug>"
    job = ROOT / "FlowHandoff_local" / "jobs" / tab / slug
    bd = _bat_dau(pid)
    sop = _sop(bd)
    out = goc / TEN_TIEP
    gc = _ghi_chu(out, ghi_chu_file)
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# LÀM TẬP TIẾP THEO — lane `{pid}` · tập {nn} (`{slug_ke}`)",
        "",
        f"> Tool `huong_dan_tab_moi.py` viết {now} ngay sau khi giao máy 2 tập `{slug}`. Anh mở tab mới, dán 1 dòng:",
        f"> `Làm theo {out}`",
        "> **Tab mới: đọc HẾT file này, làm đúng thứ tự mục 1→4, không đọc lại SOP/CHANNEL_DNA/profile/lịch sử chat.**",
        "",
        "## 0. ĐANG Ở ĐÂU",
        "| Mục | Giá trị |",
        "|---|---|",
        f"| Tập vừa xong (mẫu chạy thật — bí thì mở xem) | `{d}\\` · job máy 2 `{job}\\` |",
        f"| Tập kế | sheet tab `{tab}` dòng {dong + 1} · STT `{ke[0] or '(chưa có)'}` · đề tài: {ke[1] or '(cột B CHƯA CÓ — hỏi anh đề tài, DỪNG)'} |",
        f"| Thư mục tập kế | `{goc}\\{slug_ke}\\` {'(cột C đã có)' if ke[2] else '(chưa tạo — đặt slug theo mẫu tập trước)'} |",
        f"| Trạng thái ô D tập kế | `{ke[3] or '(trống)'}` |",
        f"| Cửa vào lane | `{bd or '(chưa có)'}` — CHỈ đọc mục ⚡ ĐỌC NHANH + đúng file nó trỏ · SOP `{sop or '(chưa có)'}` |",
        "",
        *_luat_chung(pid),
        "",
        "## 1. HỒ SƠ TẬP",
        f"- Tạo `{goc}\\{slug_ke}\\` + hồ sơ tập (competitor.txt / series_ctx.txt / title.txt / promise.txt …) đúng như tập mẫu "
        f"`{d}\\`, nguồn video gốc ghi `video_goc.json` (`{P}\\video_goc.py`, cấm bịa ID). Ghi cột C dòng {dong + 1} = thư mục tập.",
        # 2026-10-21 (anh chốt): luật hook duy nhất = bám sát cấu trúc hook video gốc (không khuôn lane, không luật khác).
        (f"- Cổng S1L + hook BÁM SÁT CẤU TRÚC hook video gốc (máy tự tách, được đổi chút cho hợp/hay hơn): "
         f"`{ROOT}\\docs\\HOOK_CAU_TRUC\\00_CHUNG.md`."),
        "",
        "## 2. VIẾT + KHOÁ KỊCH BẢN",
        "```bat",
        f"{PY} {P}\\make_video.py --profile {pid} --slug {slug_ke} --den B3G",
        "```",
        "- Hook = Fable 5.1 viết 2 phương án → Sol chọn → Opus 5 vá → khoá; S2 Fable 5.1 viết 1 lần → máy đo → Opus 5 vá → LOCK.",
        "- Bắt đầu chạy: tool tự ghi D = `Đang chạy kịch bản bước 1`. Khoá xong máy TỰ DỪNG, tự giao máy 3: "
        f"D = `Chờ kiểm tra kịch bản` + ghi đè cột K dòng {dong + 1} = thư mục anh sửa + lệnh `review_may3.py --nhan` "
        f"+ file làm tiếp `{ROOT}\\docs\\NHAN_KICH_BAN_MAY3.md` (bảng mốc: `{ROOT}\\docs\\TRANG_THAI_COT_D_K.md`).",
        "",
        "## 3. (bỏ từ 02/10 — không còn file hướng dẫn riêng từng tập)",
        "",
        "## 4. BÁO ANH",
        f"Đường dẫn `script.txt` gửi máy 3 + nội dung ô K dòng {dong + 1}. DỪNG, chờ anh sửa.",
        "",
        "## 5. GHI CHÚ TỪ TAB TRƯỚC (bài học tập vừa xong)",
        _khoi_ghi_chu(gc, "tiep"),
        "",
    ]
    # 2026-10-04 (anh chốt): K dòng tập vừa xong CHỈ có lệnh máy 2; hướng dẫn tập kế LUÔN ghi ở K DÒNG TẬP KẾ
    # (kể cả khi dòng đó chưa có STT/đề tài) — không lặp ở 2 ô.
    if not co_ke:
        print(f"  ⚠ dòng {dong + 1} tab {tab} chưa có STT/đề tài — vẫn ghi K dòng đó; anh điền A/B trước khi mở tab mới")
    return _xuat(dg, tab, dong + 1, out, L, "Tab mới — làm tập tiếp theo", dry)


def _xuat(dg, tab, dong, out, L, nhan, dry):
    txt = "\n".join(L)
    if dry:
        print(f"  (dry) sẽ viết {out} ({len(txt)} ký tự)")
    else:
        out.write_text(txt, encoding="utf-8")
        print(f"  ✓ hướng dẫn tab mới: {out}")
    if dong:
        o_k = f"{nhan} {_dt.datetime.now().strftime('%d/%m %H:%M')}: Làm theo\n{out}"
        _ghi_k(dg, tab, dong, o_k, dry=dry)
    return out


def an_toan(loai, prof, slug, **kw):
    """Gọi từ review_may3 / dong_goi_may2: lỗi ở đây KHÔNG được làm hỏng bước chính, chỉ báo to."""
    try:
        return (viet_may3 if loai == "may3" else viet_tiep)(prof, slug, **kw)
    except BaseException as e:  # noqa: BLE001 — SystemExit của cổng cột K cũng chỉ báo
        print(f"  ⚠️ CHƯA viết được hướng dẫn tab mới ({loai}): {e} — chạy tay: "
              f"{PY} {P}\\huong_dan_tab_moi.py --loai {loai} --profile {prof['id']} --slug {slug}")
        return None


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--loai", choices=["may3", "tiep"], required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--ghi-chu-file", help="file .md ghi chú riêng của tab (thay khối ghi chú cũ)")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    f = viet_may3 if a.loai == "may3" else viet_tiep
    f(prof, a.slug, ghi_chu_file=a.ghi_chu_file, dry=a.dry)


if __name__ == "__main__":
    main()
