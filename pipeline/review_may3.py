r"""review_may3.py — chặng "MÁY 3 SOÁT KỊCH BẢN" chen giữa B3 (viết + khoá) và pha asset (B4/B5W…).

Anh chốt 2026-09-26, áp dụng MỌI lane trừ 4 lane khai `script.review_may3: false` (satori-jp-obaa,
kenko-chiebukuro, toshi-densetsu-jp, irogatatarukioku). Lane KHÔNG khai field = BẬT (lane mới tự có).

Cột D/K từng mốc (2026-10-03, anh chốt — bảng đủ: docs\TRANG_THAI_COT_D_K.md):
  make_video bắt đầu chặng 1 → D "Đang chạy kịch bản bước 1" (bat_dau_b1) · share → D "Chờ kiểm tra kịch bản" + K lệnh nhận
  · --nhan xong → D "Đang làm Hook" · dong_goi_may2 --job → D "Đã giao máy 2" + K lệnh cho máy 2.

Luồng:
  B3 xong (lock PASS)  → `sau_b3()`  : chép ĐÚNG script.txt sang jobs\<tab>\<slug>\ (thư mục job của tập, chung chỗ
                                        giao máy 2 — anh chốt 2026-09-30, bỏ review\ + README/bộ đọc), ghi cột D =
                                        "Chờ kiểm tra kịch bản" + dòng 2 = đường dẫn thư mục đó, DỪNG (không xuống B4).
  máy 3 (anh) sửa tay   → ghi ĐÈ script.txt ngay tại đó (jobs 2 chiều), đổi cột D = "Đã sửa kịch bản", báo tab lane.
                                        Không sửa gì cũng được (file trùng bản gửi = nhận nguyên bản).
  máy 1 `--nhan`        → kiểm D + file về → lưu bản cũ → chép bản máy 3 vào tập (KHÔNG sửa 1 chữ) → đo tất định
                                        CHỈ ĐỌC → rút hook từ đầu kịch bản, khoá lại hook → ký lại script.lock.json
                                        (reason=may3) → ghi review_may3.json state=received. Việc từ đây trở đi là
                                        của tab lane (B5W/hook/dong_goi_may2 theo SOP lane).
  `cong()`              → gọi ở đầu mọi bước pha asset (make_video.Job.kiem_lock, dong_goi_may2 --job): lane bật
                                        review mà chưa `received` khớp sha → DỪNG. Không cửa sau (--from B4 cũng chặn).

Hook: máy 3 CHỈ sửa script.txt; hook nằm ở ĐẦU kịch bản nên máy 1 rút lại hook từ đó (anh chốt 2026-09-26, mục 3)
— không bắt máy 3 giữ nguyên văn 6 câu, không chạy lại Sol cho hook. Clip/storyboard hook sinh SAU ở B5W như cũ.

Dùng:
  py -3.13 -X utf8 pipeline\review_may3.py --share --profile <lane> --slug <tập> [--dry]
  py -3.13 -X utf8 pipeline\review_may3.py --nhan  --profile <lane> --slug <tập> [--nguon <file script>] [--dry] [--force]
  py -3.13 -X utf8 pipeline\review_may3.py --trang-thai --profile <lane>
"""
import argparse
import codecs
import datetime as _dt
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import ai_steps        # noqa: E402
import gate_common     # noqa: E402
import profiles        # noqa: E402
import tong_hop        # noqa: E402

TRANG_THAI_CHO = "Chờ kiểm tra kịch bản"          # 2026-09-30 anh đổi chữ (cũ: "Cần check kịch bản"); ô D ghi kèm dòng 2 = đường dẫn
TRANG_THAI_CHO_CU = ("Cần check kịch bản",)
TRANG_THAI_DA_SUA = "Đã sửa kịch bản"
# 2026-10-03 (anh chốt, MỌI lane): ghi chú công việc đang làm lên cột D — xem docs\TRANG_THAI_COT_D_K.md
TRANG_THAI_DANG_B1 = "Đang chạy kịch bản bước 1"     # make_video bắt đầu chặng 1 (B0–B3G)
TRANG_THAI_DANG_HOOK = "Đang làm Hook"               # --nhan xong → cast/B5W/B5P/hình hook/clip xem thử
MARKER = "review_may3.json"          # trong thư mục tập (assets\<lane>\<slug>\)
BAO_CAO_NHAN = "NHAN_MAY3.md"
JOBS = ROOT / "FlowHandoff_local" / "jobs"
SENT_END = "。！？"


def dong_dau(o):
    """Dòng đầu của ô D (ô có thể kèm đường dẫn ở dòng 2)."""
    s = (o or "").strip()
    return s.splitlines()[0].strip() if s else ""


def la_cho(o):
    """Ô D đang ở trạng thái chờ máy 3 (chữ mới/cũ, có hoặc không kèm đường dẫn ở dòng sau)."""
    dau = dong_dau(o)
    return dau == TRANG_THAI_CHO or dau in TRANG_THAI_CHO_CU


# ------------------------------------------------------------------ cấu hình / trạng thái
def is_enabled(prof):
    """Field-driven (hàng rào #2): `script.review_may3`. VẮNG field = BẬT (anh chốt: mọi lane mới đều áp dụng)."""
    return bool((prof.get("script") or {}).get("review_may3", True))


def che_do(prof):
    """Cách soát kịch bản sau B3: "may3" (MẶC ĐỊNH lại từ 2026-09-30, anh chốt — anh/máy 3 sửa thẳng script.txt) |
    "gptweb" (pipeline/soat_kb_gptweb.py, mặc định 27–30/09, nay chỉ dùng khi anh nói). Field `script.soat`."""
    return (((prof.get("script") or {}).get("soat")) or "may3").strip().lower()


def giu_hoac_khoa_lai_hook(prof, d, text, nguon):
    """Đầu kịch bản vẫn TRÙNG NGUYÊN VĂN hook đã khoá → GIỮ hook cũ (ảnh/clip/storyboard đã làm theo nó không hỏng).
    Chỉ khi đầu kịch bản thật sự bị sửa mới rút hook mới (rut_hook) và khoá lại. Vá bẫy thật Lane F ep05: bản cũ luôn
    khoá lại bằng rut_hook dù không đổi chữ nào → ra hook NGẮN hơn, thiếu câu của cảnh cuối. Trả (hook_text, đổi?, việc)."""
    import hook_stage
    if not hook_stage.is_enabled(prof):
        return "", False, []
    d = Path(d)
    cu = hook_stage.doc_hook(d)
    if cu and hook_stage.bat_dau_bang_hook(text, cu):
        print(f"  ✓ đầu kịch bản vẫn trùng hook đã khoá ({len(cu)} ký tự) → GIỮ hook cũ, không khoá lại")
        return cu, False, []
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else ""
    moi = rut_hook(prof, text, cu)
    viec = hook_stage.check(moi, prof, ctx, hook_stage.muc_cua_tap(d, prof))
    old = hook_stage.doc_lock(d) or {}
    meta = hook_stage.khoa(d, moi, mode=old.get("mode", "upstream"),
                           extra={"source": f"{nguon}_script_head", "sol_rounds": 0, "patches": 0,
                                  "source_video_id": old.get("source_video_id")})
    print(f"  ✓ đầu kịch bản đã đổi → khoá lại hook từ đầu kịch bản: {meta['chars']} chữ" + (" (có cảnh báo)" if viec else ""))
    return moi, True, viec


def danh_dau_da_soat(prof, d, nguon, bao_cao=None):
    """Chốt chặng soát (dùng cho gptweb; máy 3 dùng nhan()). Bản hiện tại đã khoá PASS → giữ/khoá lại hook → marker received
    khớp sha → cổng B4/B5W/dong_goi cho qua. KHÔNG ghi sheet (D = Done do dong_goi_may2 khi giao máy 2)."""
    d = Path(d)
    text = (d / "script.txt").read_text(encoding="utf-8")
    _, doi, viec = giu_hoac_khoa_lai_hook(prof, d, text, nguon)
    ok, msg, level = gate_common.kiem_lock(d)
    if level != "PASS":
        raise SystemExit(f"✗ chốt soát: {msg}")
    ghi_marker(d, state="received", sha=_sha(d), nguon=nguon, bao_cao=str(bao_cao) if bao_cao else None,
               hook_khoa_lai=doi, hook_canh_bao=viec)
    print(f"  ✓ {MARKER} = received ({nguon}) · sha {str(_sha(d))[:10]}… — cổng B4/B5W/dong_goi_may2 cho qua")
    print(f"\nTiếp theo (tab lane, theo SOP lane): characters/B5W/hook → giao máy 2:\n"
          f"  py -3.13 -X utf8 {HERE / 'make_video.py'} --profile {prof['id']} --slug {d.name} --only B5W\n"
          f"  py -3.13 -X utf8 {HERE / 'dong_goi_may2.py'} --job {prof['id']} {d.name}")


def tab_cua(prof):
    pub = prof.get("publish") or {}
    return pub.get("sheet_tab") or pub.get("upload_channel") or ""


def thu_muc_tap(prof, slug):
    return ROOT / (prof.get("slug_dir") or "assets/out") / slug


def review_di(prof, slug):
    # 2026-09-30 (anh chốt): bỏ thư mục con review\ — script nằm thẳng trong thư mục job của tập (chung chỗ giao máy 2).
    return JOBS / (tab_cua(prof) or prof["id"]) / slug


def review_ve(prof, slug):
    """Chỗ máy 3 trả bản sửa = CHÍNH thư mục review đã gửi (jobs 2 chiều, anh chốt 2026-09-26)."""
    return review_di(prof, slug)


def doc_marker(d):
    p = Path(d) / MARKER
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def ghi_marker(d, **kv):
    m = doc_marker(d)
    m.update(kv, at=_dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    (Path(d) / MARKER).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    return m


def _sha(d):
    s = Path(d) / "script.txt"
    return gate_common.sha256_file(s) if s.exists() else None


def trang_thai(prof, d):
    """'off' (lane tắt) | 'chua' | 'shared' | 'received' | 'stale' (received nhưng script đã đổi sau đó)."""
    if not is_enabled(prof):
        return "off"
    m = doc_marker(d)
    st = m.get("state")
    if st == "received":
        return "received" if m.get("sha") == _sha(d) else "stale"
    return st or "chua"


# ------------------------------------------------------------------ sheet (cột D)
def _sheet(prof, slug):
    import dong_goi_may2 as dg
    tab = tab_cua(prof)
    if not tab:
        raise SystemExit(f"profile {prof['id']} chưa khai publish.sheet_tab/upload_channel → không biết tab nào")
    stt = dg._stt_theo_slug(tab, slug)
    return dg, tab, stt + 1


def _doc_d(dg, tab, dong):
    s = dg.svc(doc_thoi=True)
    hd = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!{dg.COT_D}1").execute().get("values", [[""]])
    ten = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if not ten.startswith(dg.TIEU_DE_COT_D):
        raise SystemExit(f"cột {dg.COT_D} dòng 1 là '{ten or '(trống)'}', không phải '{dg.TIEU_DE_COT_D}' → cột đổi chỗ, DỪNG.")
    cur = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!{dg.COT_D}{dong}").execute().get("values", [[]])
    return (cur[0][0] if cur and cur[0] else "").strip()


def _ghi_d(dg, tab, dong, gia_tri):
    dg.svc(doc_thoi=False).values().update(spreadsheetId=dg.SHEET_ID, range=f"{tab}!{dg.COT_D}{dong}",
                                           valueInputOption="USER_ENTERED", body={"values": [[gia_tri]]}).execute()
    print(f"  ✓ ghi {tab}!{dg.COT_D}{dong} = {gia_tri}")


def ghi_d_neu(prof, slug, gia_tri, cho_phep):
    """Ghi ô D khi dòng đầu ô hiện tại nằm trong `cho_phep` (hoặc trống / ESCALATE / BLOCK). Khác → không đè, chỉ báo.
    Lỗi sheet KHÔNG chặn bước chính (ghi chú trạng thái, không phải cổng)."""
    try:
        dg, tab, dong = _sheet(prof, slug)
        cu = _doc_d(dg, tab, dong)
        dau = dong_dau(cu)
        if cu == gia_tri:
            print(f"  ô {tab}!D{dong} đã '{dau}'")
        elif (dau == "" or dau.lower().startswith(("escalate", "block")) or dau in cho_phep
              or (TRANG_THAI_CHO in cho_phep and la_cho(dau))):
            _ghi_d(dg, tab, dong, gia_tri)
        else:
            print(f"  ⚠️ ô {tab}!D{dong} đang '{dau}' → KHÔNG đè thành '{dong_dau(gia_tri)}', anh xem lại")
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột D: {e}")


def ghi_k(prof, slug, gia_tri):
    """Ghi đè ô K (GHI CHÚ) dòng của tập. Lỗi sheet không chặn bước chính."""
    try:
        import huong_dan_tab_moi
        dg, tab, dong = _sheet(prof, slug)
        huong_dan_tab_moi._ghi_k(dg, tab, dong, gia_tri)
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột K: {e}")


def ma_tap(prof, slug):
    """('L', 'ep09') từ tên tab `{Lane}-{kênh}` + slug — để in câu lệnh anh báo ("anh sửa xong kịch bản L ep09")."""
    p = (tab_cua(prof) or prof["id"]).split("-")
    lane = p[1] if len(p) > 1 and p[0].lower() == "lane" else p[0]      # tab "Lane-J" → J
    m = re.match(r"(ep\d+)", slug)
    return lane, (m.group(1) if m else slug)


def bat_dau_b1(prof, d, dry=False):
    """make_video gọi trước chặng 1: lane bật soát máy 3 + tập chưa gửi máy 3 → D = "Đang chạy kịch bản bước 1"."""
    if dry or not is_enabled(prof) or "buoc2_3_tool" in str(HERE):
        return
    if trang_thai(prof, d) != "chua":
        return
    ghi_d_neu(prof, Path(d).name, TRANG_THAI_DANG_B1, (TRANG_THAI_DANG_B1,))
    tong_hop.ghi(prof, Path(d).name, tong_hop.CHAY_KB)


# ------------------------------------------------------------------ --share
def share(prof, slug, dry=False, force=False):
    d = thu_muc_tap(prof, slug)
    if not d.is_dir():
        raise SystemExit(f"✗ không thấy thư mục tập {d}")
    if not is_enabled(prof):
        print(f"[review] lane {prof['id']} khai review_may3=false → không share")
        return None
    ok, msg, level = gate_common.kiem_lock(d)
    if level == "FAIL" and not force:
        raise SystemExit(f"✗ share: {msg} — kịch bản chưa PASS thì chưa gửi máy 3")
    st = trang_thai(prof, d)
    if st == "received" and not force:
        print(f"[review] tập {slug} ĐÃ nhận bản máy 3 (sha khớp) → không share lại")
        return None
    # 2026-09-30 (anh chốt): máy 3 kiểm THỦ CÔNG → chỉ chép ĐÚNG script.txt vào thư mục job của tập
    # (jobs\<tab>\<slug>\, chung chỗ giao máy 2), không thư mục review\, không README/bộ đọc kèm.
    dst = review_di(prof, slug)
    print(f"[review] share {slug} → {dst}\\script.txt")
    if not dry:
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(d / "script.txt", dst / "script.txt")
        ghi_marker(d, state="shared", sha=_sha(d), review_di=str(dst), review_ve=str(dst))
        print("  ✓ script.txt · anh sửa thẳng file này")
    else:
        print(f"  (dry) sẽ chép script.txt → {dst}")
    # sheet D
    # 2026-09-30 (anh chốt): ô D = "Chờ kiểm tra kịch bản" + dòng 2 = đường dẫn thư mục job chứa script.txt.
    # 2026-10-03 (anh chốt): cột K dòng tập = thư mục anh sửa + câu anh báo + lệnh nhận + file làm tiếp.
    o_d = f"{TRANG_THAI_CHO}\n{dst}"
    o_k = k_cho_kiem_tra(prof, slug, dst)
    if dry:
        print(f"  (dry) sẽ ghi cột D = {o_d!r}\n  (dry) sẽ ghi cột K = {o_k!r}")
        return dst
    ghi_d_neu(prof, slug, o_d, (TRANG_THAI_CHO, TRANG_THAI_DANG_B1))
    ghi_k(prof, slug, o_k)
    tong_hop.ghi(prof, slug, tong_hop.CHO_KB)
    return dst


def k_cho_kiem_tra(prof, slug, dst):
    lane, ep = ma_tap(prof, slug)
    return (f"{TRANG_THAI_CHO} {_dt.datetime.now():%d/%m %H:%M}\n"
            f"Anh sửa: {Path(dst) / 'script.txt'} (hook = đoạn đầu)\n"
            f"Anh sửa xong thì đổi D = \"{TRANG_THAI_DA_SUA}\" và báo \"anh sửa xong kịch bản {lane} {ep}\". Em sẽ chạy:\n"
            f"py -3.13 -X utf8 {HERE / 'review_may3.py'} --nhan --profile {prof['id']} --slug {slug}\n"
            f"rồi làm tiếp theo {ROOT / 'docs' / 'NHAN_KICH_BAN_MAY3.md'}.")


# ------------------------------------------------------------------ --nhan
def _cau(text):
    return [s for s in re.findall(rf"[^{SENT_END}\n]+[{SENT_END}]?", text) if s.strip()]


def _doan(text):
    return [x.strip() for x in text.split("\n") if x.strip()]


def rut_hook(prof, script, hook_cu=""):
    """Hook mới = phần đầu kịch bản đã sửa. Không LLM.
    2026-09-30 (anh chốt — anh sửa hook NGAY TRONG script.txt): hook luôn là (các) ĐOẠN đầu kịch bản (S2 đặt hook đã khoá
    thành đoạn riêng) → lấy đúng SỐ ĐOẠN của hook cũ, nên anh viết dài/ngắn hơn cũng không bị cắt sai. Chỉ khi độ dài lệch
    phi lý (<0,4× hoặc >2,5× mục tiêu — anh nhập hook vào đoạn 2) mới rơi về cách cũ: cộng dồn câu tới gần ~30 giây."""
    import hook_stage
    # 2026-10-17: độ dài hook nay theo hook video gốc của từng tập → mốc so = độ dài hook đã khoá (nếu có), không phải 30s.
    muc = ai_steps.measure(hook_cu)["chars"] if hook_cu else hook_stage.so_chu_muc_tieu(prof)
    # 2026-10-14 (Lane L ep18): hook nay mỗi câu 1 dòng, không dòng trống bên trong → _doan đếm DÒNG, anh viết hook
    # ít dòng hơn bản cũ (23 vs 35) thì lấy lố 12 dòng thân bài. Ưu tiên khối đầu tới DÒNG TRỐNG đầu tiên.
    khoi_dau = re.split(r"\n\s*\n", script.strip(), maxsplit=1)[0].strip()
    if khoi_dau != script.strip() and 0.4 * muc <= ai_steps.measure(khoi_dau)["chars"] <= 2.5 * muc:
        return khoi_dau
    n_doan = len(_doan(hook_cu)) if hook_cu else 1
    theo_doan = "\n".join(_doan(script)[:n_doan])
    if theo_doan and 0.4 * muc <= ai_steps.measure(theo_doan)["chars"] <= 2.5 * muc:
        return theo_doan
    cau = _cau(script)
    best, best_d = "", None
    acc = ""
    for s in cau:
        acc += s.strip()
        n = ai_steps.measure(acc)["chars"]
        dlt = abs(n - muc)
        if best_d is None or dlt < best_d:
            best, best_d = acc, dlt
        if n > muc * 1.5:
            break
    return best


def nhan(prof, slug, nguon=None, dry=False, force=False):
    d = thu_muc_tap(prof, slug)
    if not d.is_dir():
        raise SystemExit(f"✗ không thấy thư mục tập {d}")
    if not is_enabled(prof):
        raise SystemExit(f"lane {prof['id']} khai review_may3=false — không có chặng máy 3")
    import lean_script
    # 1) cột D phải là "Đã sửa kịch bản" (trừ --force / --dry)
    if not dry and not force:
        dg, tab, dong = _sheet(prof, slug)
        cu = _doc_d(dg, tab, dong)
        if dong_dau(cu) not in (TRANG_THAI_DA_SUA, TRANG_THAI_DANG_HOOK):   # "Đang làm Hook" = chạy --nhan lại
            raise SystemExit(f"✗ ô {tab}!D{dong} đang '{cu or '(trống)'}', chưa phải '{TRANG_THAI_DA_SUA}' → máy 3 chưa trả, DỪNG (hoặc --force)")
    # 2) file về
    src = Path(nguon) if nguon else review_ve(prof, slug) / "script.txt"
    if not src.exists():
        raise SystemExit(f"✗ chưa thấy bản máy 3: {src}")
    # 2026-10-03 (Lane O ep01): Notepad máy 3 lưu kèm BOM → hook dính U+FEFF, vai.txt câu 1 rỗng. BOM không phải nội dung → bỏ.
    text = src.read_text(encoding="utf-8-sig")
    if not text.strip():
        raise SystemExit(f"✗ {src} rỗng")
    # 2026-09-30 (anh chốt): máy 3 kiểm thủ công, không bắt BAO_CAO_SUA.md. Cột D = "Đã sửa kịch bản" là tín hiệu duy
    # nhất; file trùng bản đã gửi = anh đọc xong không sửa gì → nhận như thường, chỉ in 1 dòng cho tab lane biết.
    if gate_common.sha256_file(src) == doc_marker(d).get("sha"):
        print(f"  ℹ️ {src} trùng bản đã gửi — anh không sửa chữ nào, nhận nguyên bản")
    # 3) đo CHỈ ĐỌC — không sửa 1 chữ
    minutes = profiles.target_minutes(prof)
    try:
        st = json.loads((d / "state.json").read_text(encoding="utf-8"))
        minutes = (st.get("B0") or {}).get("minutes") or minutes
    except Exception:
        pass
    ns = lean_script.ngan_sach(prof, profiles.target_chars(prof, minutes))
    m = ai_steps.measure(text)
    chan, canh_bao = [], []
    if m["chars"] < ns["target"] * 0.7:
        chan.append(f"kịch bản quá ngắn: {m['chars']:,} chữ < 70% mục tiêu {ns['target']:,}")
    elif not (ns["lo"] <= m["chars"] <= ns["hi"]):
        canh_bao.append(f"độ dài {m['chars']:,} ngoài ngân sách {ns['lo']:,}–{ns['hi']:,} (giọng đọc sẽ lệch thời lượng)")
    try:
        bad, _ = ai_steps.check(prof, text, minutes)
        canh_bao += [f"gate: {b}" for b in bad if not b.startswith(("DÀI", "NGẮN"))]
    except Exception as e:
        canh_bao.append(f"không đo được gate: {type(e).__name__} {e}")
    if ai_steps.MARKER_PAT.search(text):
        canh_bao.append("còn marker/ký hiệu không phải prose (TTS sẽ đọc ra)")
    ctx_f = d / "series_ctx.txt"
    ctx = ctx_f.read_text(encoding="utf-8") if ctx_f.exists() else ""
    mode = ((prof.get("script") or {}).get("mode") or "").lower()
    if ctx and mode in ("documentary", "fiction_facts"):
        exempt = tuple((prof.get("script") or {}).get("fact_exempt_units") or ())
        so_la = lean_script._so_lieu_ngoai_tu_lieu(text, lean_script.so_duoc_phep(ctx) + "\n" + ctx, exempt)
        if so_la:
            chan.append("số liệu KHÔNG có trong series_ctx.txt: " + ", ".join(str(x) for x in so_la[:8]))
    # 4) hook rút từ đầu kịch bản
    import hook_stage
    hook_txt, hook_viec = "", []
    if hook_stage.is_enabled(prof):
        cu_hook = hook_stage.doc_hook(d)
        if not (cu_hook and hook_stage.bat_dau_bang_hook(text, cu_hook)):
            hook_txt = rut_hook(prof, text, cu_hook)
            hook_viec = hook_stage.check(hook_txt, prof, ctx, hook_stage.muc_cua_tap(d, prof))
            canh_bao += [f"hook: {v}" for v in hook_viec]
    bao = [f"# NHẬN BẢN MÁY 3 · {slug} · {_dt.datetime.now():%Y-%m-%d %H:%M}", "",
           f"- nguồn: `{src}`", f"- {m['chars']:,} chữ ≈ {m['minutes']}' · thoại {m['dialogue_ratio']:.0%} · "
           f"phẩy/câu {m['comma_per_sentence']} · ngân sách {ns['lo']:,}–{ns['hi']:,}", ""]
    if chan:
        bao += ["## ✗ CHẶN — trả lại máy 3, máy 1 KHÔNG tự sửa"] + [f"- {x}" for x in chan] + [""]
    if canh_bao:
        bao += ["## ⚠️ Cảnh báo (đi tiếp, ghi lại để tab lane biết)"] + [f"- {x}" for x in canh_bao] + [""]
    if hook_txt:
        bao += ["## Hook rút từ đầu kịch bản (khoá lại, không Sol)", "", hook_txt, ""]
    (d / BAO_CAO_NHAN).write_text("\n".join(bao), encoding="utf-8")
    print("\n".join(bao[2:]))
    if chan and not force:
        raise SystemExit(f"✗ nhận: {len(chan)} điểm CHẶN — xem {d / BAO_CAO_NHAN}. Trả lại máy 3 (README đã ghi luật), không sửa hộ.")
    if dry:
        print(f"(dry) sẽ: lưu script.txt cũ → chép bản máy 3 → khoá hook → ký lock PASS reason=may3 → {MARKER} received")
        return
    # 5) chép vào tập, giữ bản cũ
    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M")
    cu = d / "script.txt"
    if cu.exists():
        shutil.copy2(cu, d / f"script.truoc_may3_{ts}.txt")
    shutil.copy2(src, cu)
    raw = cu.read_bytes()
    if raw.startswith(codecs.BOM_UTF8):
        cu.write_bytes(raw[len(codecs.BOM_UTF8):])
    bc = src.parent / "BAO_CAO_SUA.md"
    if bc.exists():
        shutil.copy2(bc, d / f"BAO_CAO_SUA_MAY3_{ts}.md")
    # 6) hook: đầu kịch bản vẫn trùng hook cũ → GIỮ; đổi thật mới khoá lại (vá bẫy F ep05, xem giu_hoac_khoa_lai_hook)
    giu_hoac_khoa_lai_hook(prof, d, (d / "script.txt").read_text(encoding="utf-8"), "may3")
    # 7) ký lại lock
    old_lock = {}
    try:
        old_lock = json.loads((d / gate_common.LOCK_NAME).read_text(encoding="utf-8"))
    except Exception:
        pass
    meta = gate_common.ghi_lock(d, "PASS", reason="may3", may3_nguon=str(src), truoc_may3=f"script.truoc_may3_{ts}.txt",
                                chars=m["chars"], minutes=m["minutes"], patches=old_lock.get("patches", 0),
                                log=(old_lock.get("log") or []) + [f"may3 nhận {ts} · {m['chars']:,} chữ"])
    ghi_marker(d, state="received", sha=meta["script_sha256"], nguon=str(src))
    print(f"  ✓ lock PASS (may3) sha {meta['script_sha256'][:10]}… · {MARKER} = received")
    # 2026-10-03 (anh chốt): nhận xong, tab đi làm hook → D = "Đang làm Hook"
    ghi_d_neu(prof, slug, TRANG_THAI_DANG_HOOK, (TRANG_THAI_DA_SUA, TRANG_THAI_CHO, TRANG_THAI_DANG_HOOK))
    tong_hop.ghi(prof, slug, tong_hop.CHAY_HOOK)
    print(f"\nTiếp theo: {ROOT / 'docs' / 'NHAN_KICH_BAN_MAY3.md'} (cast → B5W/B5P → hình hook → clip hook xem thử → ANH DUYỆT → dong_goi_may2), ví dụ:\n"
          f"  py -3.13 -X utf8 {HERE / 'make_video.py'} --profile {prof['id']} --slug {slug} --only B5W\n"
          f"  py -3.13 -X utf8 {HERE / 'make_video.py'} --profile {prof['id']} --slug {slug} --only B5P\n"
          f"  py -3.13 -X utf8 {HERE / 'duyet_hook.py'} --gui --profile {prof['id']} --slug {slug}")


# ------------------------------------------------------------------ cổng + móc vào make_video
def cong(prof, d, buoc):
    """Gọi ở đầu pha asset. Lane bật review mà chưa nhận bản máy 3 (hoặc script đổi sau khi nhận) → DỪNG."""
    st = trang_thai(prof, d)
    if st in ("off", "received"):
        return
    if st == "stale":
        raise SystemExit(f"✗ {buoc}: script.txt đã đổi SAU khi chốt soát → chốt lại (gptweb: soat_kb_gptweb.py --xong · "
                         f"máy 3: review_may3.py --nhan)")
    if che_do(prof) == "gptweb":
        raise SystemExit(f"✗ {buoc}: tập chưa soát xong bằng ChatGPT web (đang '{st}') → py -3.13 -X utf8 "
                         f"{HERE / 'soat_kb_gptweb.py'} --profile {prof['id']} --slug {Path(d).name} --lan1 … rồi --xong")
    raise SystemExit(f"✗ {buoc}: lane {prof['id']} bật soát máy 3 nhưng tập chưa 'received' (đang '{st}') → "
                     f"chờ cột D = '{TRANG_THAI_DA_SUA}' rồi chạy: py -3.13 -X utf8 {HERE / 'review_may3.py'} --nhan --profile {prof['id']} --slug {Path(d).name}")


def sau_b3(prof, d, dry=False):
    """Gọi ngay sau khối B3 của make_video (cả lean lẫn cũ). Lane bật review: chưa nhận → share (nếu chưa) rồi DỪNG."""
    if not is_enabled(prof):
        return
    d = Path(d)
    st = trang_thai(prof, d)
    if st == "received":
        return
    # 2026-09-26 (máy 2 báo): máy 2 chạy từ cây bundle FlowHandoff_local\shared\buoc2_3_tool — KHÔNG được đóng vai
    # "gửi máy 3" (share() ghi vào thư mục lồng ngoài Syncthing). Chưa received ở máy 2 = gói job thiếu marker → DỪNG báo máy 1.
    if "buoc2_3_tool" in str(HERE):
        raise SystemExit(f"✗ tập {d.name}: chưa có review_may3.json state=received khớp sha (đang '{st}') — máy 2 KHÔNG tự share/nhận. "
                         f"Báo máy 1: chạy review_may3.py --nhan rồi dong_goi_may2.py --job {prof['id']} {d.name}")
    ok, msg, level = gate_common.kiem_lock(d)
    if level != "PASS":
        return      # chưa khoá (ESCALATE/BLOCK/luồng cũ chưa B3G) — chưa có gì để gửi
    if che_do(prof) == "gptweb":
        # 2026-09-27 (anh chốt): MẶC ĐỊNH soát bằng ChatGPT web — KHÔNG chép sang máy 3, KHÔNG ghi sheet giữa chừng.
        sg = HERE / "soat_kb_gptweb.py"
        sd = d / "soat_gptweb"
        raise SystemExit(f"⏸ DỪNG SAU B3 — soát kịch bản bằng ChatGPT web (tab lane thẩm định, không sửa tay):\n"
                         f"  1) py -3.13 -X utf8 {sg} --profile {prof['id']} --slug {d.name} --lan1\n"
                         f"  2) đọc {sd / 'tra_loi_1.md'} → nhận/phản biện (--tin <file>, cổng VẪN MỞ) → thống nhất phương án → "
                         f"--chot (ĐÓNG cổng) → rồi mới viec_tay.txt → ghi_lock ESCALATE → make_video --den B3G\n"
                         f"  3) viết {sd / 'BAO_CAO_SUA.md'} → py -3.13 -X utf8 {sg} --profile {prof['id']} --slug {d.name} --xong")
    m = doc_marker(d)
    if st == "shared" and m.get("sha") == _sha(d):
        print(f"[review] tập {d.name} đã gửi máy 3 ({m.get('at')}), đang chờ cột D = '{TRANG_THAI_DA_SUA}'")
    else:
        share(prof, d.name, dry=dry)
    # 2026-10-02 (anh chốt): BỎ file hướng dẫn riêng từng tập — nhận bản sửa thì tab đọc ĐÚNG 1 file chung
    # docs\NHAN_KICH_BAN_MAY3.md. 2026-10-03: cột K dòng tập ghi lại câu lệnh nhận (share() → k_cho_kiem_tra).
    raise SystemExit(f"⏸ DỪNG SAU B3 — cột D = '{TRANG_THAI_CHO}' · thư mục anh sửa: {review_di(prof, d.name)} "
                     f"(file script.txt, hook = đoạn đầu). Khi anh báo cột D = '{TRANG_THAI_DA_SUA}':\n"
                     f"  py -3.13 -X utf8 {HERE / 'review_may3.py'} --nhan --profile {prof['id']} --slug {d.name}\n"
                     f"  rồi làm tiếp theo ĐÚNG file {ROOT / 'docs' / 'NHAN_KICH_BAN_MAY3.md'}")


# ------------------------------------------------------------------ --trang-thai
def trang_thai_lane(prof):
    dg, tab = None, tab_cua(prof)
    import dong_goi_may2 as dg
    s = dg.svc(doc_thoi=True)
    vals = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!A2:D300").execute().get("values", [])
    print(f"tab {tab}:")
    for row in vals:
        dcol = (row[3] if len(row) > 3 else "").strip()
        if la_cho(dcol) or dong_dau(dcol) in (TRANG_THAI_DANG_B1, TRANG_THAI_DA_SUA, TRANG_THAI_DANG_HOOK,
                                               "Chờ duyệt hook", "Đã duyệt hook"):   # 2026-10-02 + chặng duyệt hook
            print(f"  STT {row[0]:>3} · D='{dcol}' · {row[2] if len(row) > 2 else ''}")


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--share", action="store_true")
    g.add_argument("--nhan", action="store_true")
    g.add_argument("--trang-thai", action="store_true")
    ap.add_argument("--nguon", help="--nhan: file script máy 3 (mặc định jobs\\<tab>\\<slug>\\review\\script.txt)")
    ap.add_argument("--dry", action="store_true", help="không ghi sheet/không ghi file")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    if a.trang_thai:
        return trang_thai_lane(prof)
    if not a.slug:
        ap.error("cần --slug")
    if a.share:
        share(prof, a.slug, dry=a.dry, force=a.force)
    else:
        nhan(prof, a.slug, nguon=a.nguon, dry=a.dry, force=a.force)


if __name__ == "__main__":
    main()
