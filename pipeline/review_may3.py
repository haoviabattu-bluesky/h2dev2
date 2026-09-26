r"""review_may3.py — chặng "MÁY 3 SOÁT KỊCH BẢN" chen giữa B3 (viết + khoá) và pha asset (B4/B5W…).

Anh chốt 2026-09-26, áp dụng MỌI lane trừ 4 lane khai `script.review_may3: false` (satori-jp-obaa,
kenko-chiebukuro, toshi-densetsu-jp, irogatatarukioku). Lane KHÔNG khai field = BẬT (lane mới tự có).

Luồng:
  B3 xong (lock PASS)  → `sau_b3()`  : chép bộ đọc sang jobs\<tab>\<slug>\review\ + README_MAY3.md,
                                        ghi sheet cột D = "Cần check kịch bản", DỪNG (không xuống B4).
  máy 3 sửa xong        → trả script.txt + BAO_CAO_SUA.md về results\review\<tab>\<slug>\ (chiều về máy 1 —
                                        `jobs` là sendonly nên ghi vào jobs\…\review\ KHÔNG về tới máy 1),
                                        tự ghi cột D = "Đã sửa kịch bản". Anh báo tay cho tab lane.
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

TRANG_THAI_CHO = "Cần check kịch bản"
TRANG_THAI_DA_SUA = "Đã sửa kịch bản"
MARKER = "review_may3.json"          # trong thư mục tập (assets\<lane>\<slug>\)
BAO_CAO_NHAN = "NHAN_MAY3.md"
JOBS = ROOT / "FlowHandoff_local" / "jobs"
RESULTS_REVIEW = ROOT / "FlowHandoff_local" / "results" / "review"
FILE_DOC = ["script.txt", "script.lock.json", "do.json", "bench.jsonl", "ESCALATION_REPORT.md",
            "promise.txt", "competitor.txt", "series_ctx.txt", "title.txt", "listting.txt", "video_goc.json"]
HOOK_DOC = ["hook_locked.txt", "promise.txt", "hook_lock.json"]
SENT_END = "。！？"


# ------------------------------------------------------------------ cấu hình / trạng thái
def is_enabled(prof):
    """Field-driven (hàng rào #2): `script.review_may3`. VẮNG field = BẬT (anh chốt: mọi lane mới đều áp dụng)."""
    return bool((prof.get("script") or {}).get("review_may3", True))


def tab_cua(prof):
    pub = prof.get("publish") or {}
    return pub.get("sheet_tab") or pub.get("upload_channel") or ""


def thu_muc_tap(prof, slug):
    return ROOT / (prof.get("slug_dir") or "assets/out") / slug


def review_di(prof, slug):
    return JOBS / (tab_cua(prof) or prof["id"]) / slug / "review"


def review_ve(prof, slug):
    return RESULTS_REVIEW / (tab_cua(prof) or prof["id"]) / slug


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


# ------------------------------------------------------------------ --share
def _tap_truoc_da_khoa(prof, d):
    """1 tập anh em gần nhất có lock PASS (khác tập này) — làm mẫu giọng văn cho máy 3."""
    cha = Path(d).parent
    ung = []
    for x in sorted(cha.iterdir(), reverse=True):
        if not x.is_dir() or x == Path(d) or x.name.startswith("_"):
            continue
        lk = x / gate_common.LOCK_NAME
        if lk.exists() and (x / "script.txt").exists():
            try:
                if json.loads(lk.read_text(encoding="utf-8")).get("state") == "PASS":
                    ung.append(x)
            except Exception:
                pass
    return ung[0] if ung else None


def _readme(prof, d, slug, ve, tham_khao):
    sc = prof.get("script") or {}
    import lean_script
    minutes = profiles.target_minutes(prof)
    try:
        st = json.loads((Path(d) / "state.json").read_text(encoding="utf-8"))
        minutes = (st.get("B0") or {}).get("minutes") or minutes
    except Exception:
        pass
    ns = lean_script.ngan_sach(prof, profiles.target_chars(prof, minutes))
    g = profiles.gate(prof)
    ctx_co = (Path(d) / "series_ctx.txt").exists()
    hook_co = (Path(d) / "hook" / "hook_locked.txt").exists()
    title = lean_script._title(Path(d))
    promise = (Path(d) / "promise.txt").read_text(encoding="utf-8").strip() if (Path(d) / "promise.txt").exists() else "(chưa có)"
    tab = tab_cua(prof)
    sol = sorted(Path(d).glob("qc_sol_report_*.txt"))
    return f"""# MÁY 3 — SOÁT & SỬA KỊCH BẢN · lane `{prof['id']}` (tab `{tab}`) · tập `{slug}`

Gửi từ máy 1 lúc {_dt.datetime.now():%Y-%m-%d %H:%M}. Kịch bản đã qua Fable viết → máy đo → Opus vá → Sol chấm
(xem `script.lock.json`, `do.json`, `{sol[-1].name if sol else 'qc_sol_report_*.txt'}`). Máy 1 ĐÃ DỪNG, KHÔNG làm giọng/ảnh
cho tới khi anh trả kịch bản về.

## Tập này
- Tiêu đề làm việc: {title}
- Lời hứa (promise.txt): {promise}
- Ngách: {prof.get('niche', '')}
- Thời lượng mục tiêu: {minutes} phút ≈ {ns['target']:,} chữ (chấp nhận {ns['lo']:,}–{ns['hi']:,}, không tính xuống dòng)
- Tỉ lệ thoại tối đa (gate lane): {g.get('dialogue_ratio_max', '—')}

## File trong thư mục này
| File | Là gì |
|---|---|
| `script.txt` | **Bản cần soát/sửa** (bản chép — bản thật ở máy 1) |
| `hook/hook_locked.txt` | {'Hook 20–30s đang khoá — nằm nguyên văn ở ĐẦU script.txt' if hook_co else '(tập không có hook khoá)'} |
| `promise.txt` / `title.txt` | Lời hứa + tiêu đề — kịch bản phải TRẢ đúng lời hứa này |
| `competitor.txt` | Transcript video gốc (nhân bản 70/30 — KHÔNG được chép câu chữ) |
| `series_ctx.txt` | {'Dữ kiện có nguồn — mọi con số/địa danh CHỈ được lấy từ đây' if ctx_co else '(lane hư cấu, không có tư liệu nguồn)'} |
| `do.json` · `script.lock.json` · `bench.jsonl` | Số đo máy + trạng thái khoá |
| `qc_sol_report_*.txt` | Sol (GPT-5.6) chấm — tham khảo, không bắt buộc theo |
| `{tham_khao.name if tham_khao else '(không có)'}` | Tập trước ĐÃ KHOÁ — mẫu giọng văn/nhịp của lane |

## Việc nhờ máy 3
Đọc kỹ toàn bộ, sửa TRỰC TIẾP thành bản cuối cùng (không phải góp ý) — máy 1 sẽ dùng NGUYÊN VĂN bản anh trả,
không sửa lại một chữ nào. Luật:
1. **Hook nằm ở đầu kịch bản** — sửa được, nhưng 20–30 giây đầu phải là 1 sự kiện cụ thể + câu hỏi mở, không chào hỏi,
   không giới thiệu kênh. Máy 1 sẽ rút lại hook từ phần đầu bản anh trả.
2. Độ dài giữ trong {ns['lo']:,}–{ns['hi']:,} chữ (giọng đọc đã đo theo số này).
3. {'Con số/địa danh/tên thật CHỈ lấy từ series_ctx.txt — số mới không có nguồn sẽ bị máy 1 trả lại.' if ctx_co else 'Số tiền/giá cả phải là mức THẬT ở Nhật, không quy đổi máy móc từ bản gốc.'}
4. Pure prose cho TTS: không heading/marker/ngoặc vuông, thoại trong「」, mỗi câu kết bằng 。！？
5. Không chép nguyên câu của `competitor.txt` hay của tập trước.
6. Trích chữ Nhật trong báo cáo thì kèm dịch tiếng Việt.

## Trả kết quả (chiều VỀ máy 1 — bắt buộc đúng chỗ)
Thư mục này (`jobs\\`) là MỘT CHIỀU máy 1 → máy khác: ghi vào đây KHÔNG về tới máy 1. Ghi vào:
`{ve}\\`
- `script.txt` — bản cuối cùng (nguyên văn sẽ được dùng)
- `BAO_CAO_SUA.md` — sửa gì, vì sao (ngắn gọn)
Xong thì ghi Google Sheet tab `{tab}`, dòng của tập này, cột D (KỊCH BẢN) = **`{TRANG_THAI_DA_SUA}`** và báo anh.
Thư mục `review\\` KHÔNG phải lệnh giao máy 2 (máy 2 chỉ nhận việc khi cột H ghi "cần ảnh").
"""


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
    dst = review_di(prof, slug)
    ve = review_ve(prof, slug)
    tham_khao = _tap_truoc_da_khoa(prof, d)
    print(f"[review] share {slug} → {dst}")
    if not dry:
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in FILE_DOC:
            p = d / f
            if p.exists():
                shutil.copy2(p, dst / f); n += 1
        for p in sorted(d.glob("qc_sol_report_*.txt")):
            shutil.copy2(p, dst / p.name); n += 1
        if (d / "hook").is_dir():
            (dst / "hook").mkdir(exist_ok=True)
            for f in HOOK_DOC:
                p = d / "hook" / f
                if p.exists():
                    shutil.copy2(p, dst / "hook" / f); n += 1
        if tham_khao:
            shutil.copy2(tham_khao / "script.txt", dst / f"tham_khao_{tham_khao.name}_script_da_khoa.txt"); n += 1
        (dst / "README_MAY3.md").write_text(_readme(prof, d, slug, ve, tham_khao), encoding="utf-8")
        ghi_marker(d, state="shared", sha=_sha(d), review_di=str(dst), review_ve=str(ve))
        print(f"  ✓ {n} file + README_MAY3.md · máy 3 trả về: {ve}")
    else:
        print(f"  (dry) sẽ chép {len(FILE_DOC)} loại file + hook + README → {dst}; trả về {ve}")
    # sheet D
    if dry:
        print(f"  (dry) sẽ ghi cột D = {TRANG_THAI_CHO}")
        return dst
    try:
        dg, tab, dong = _sheet(prof, slug)
        cu = _doc_d(dg, tab, dong)
        if cu == TRANG_THAI_CHO:
            print(f"  ô {tab}!D{dong} đã '{cu}'")
        elif cu == "" or cu.lower() in ("escalate", "block") or cu.lower().startswith(("escalate", "block")):
            _ghi_d(dg, tab, dong, TRANG_THAI_CHO)
        else:
            print(f"  ⚠️ ô {tab}!D{dong} đang '{cu}' → KHÔNG đè, anh xem lại")
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột D: {e}")
    return dst


# ------------------------------------------------------------------ --nhan
def _cau(text):
    return [s for s in re.findall(rf"[^{SENT_END}\n]+[{SENT_END}]?", text) if s.strip()]


def rut_hook(prof, script):
    """Hook = các câu đầu kịch bản, cộng dồn tới khi đủ số chữ ~30 giây (hook_stage.so_chu_muc_tieu). Cắt ở ranh giới
    câu; chọn số câu cho |chữ − mục tiêu| nhỏ nhất. Không LLM."""
    import hook_stage
    muc = hook_stage.so_chu_muc_tieu(prof)
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
        if cu != TRANG_THAI_DA_SUA:
            raise SystemExit(f"✗ ô {tab}!D{dong} đang '{cu or '(trống)'}', chưa phải '{TRANG_THAI_DA_SUA}' → máy 3 chưa trả, DỪNG (hoặc --force)")
    # 2) file về
    src = Path(nguon) if nguon else review_ve(prof, slug) / "script.txt"
    if not src.exists():
        raise SystemExit(f"✗ chưa thấy bản máy 3: {src}\n   (máy 3 phải ghi vào results\\review\\<tab>\\<slug>\\script.txt — jobs\\ là một chiều)")
    text = src.read_text(encoding="utf-8")
    if not text.strip():
        raise SystemExit(f"✗ {src} rỗng")
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
        hook_txt = rut_hook(prof, text)
        hook_viec = hook_stage.check(hook_txt, prof, ctx)
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
    bc = src.parent / "BAO_CAO_SUA.md"
    if bc.exists():
        shutil.copy2(bc, d / f"BAO_CAO_SUA_MAY3_{ts}.md")
    # 6) hook khoá lại theo bản mới (mode giữ như cũ)
    if hook_txt:
        old = hook_stage.doc_lock(d) or {}
        meta = hook_stage.khoa(d, hook_txt, mode=old.get("mode", "upstream"),
                               extra={"source": "may3_script_head", "sol_rounds": 0, "patches": 0,
                                      "source_video_id": old.get("source_video_id")})
        print(f"  ✓ hook khoá lại từ đầu kịch bản: {meta['chars']} chữ" + (" (có cảnh báo, xem báo cáo)" if hook_viec else ""))
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
    print(f"\nTiếp theo (tab lane, theo SOP của lane): B5W/hook/dong_goi_may2 — ví dụ:\n"
          f"  py -3.13 -X utf8 {HERE / 'make_video.py'} --profile {prof['id']} --slug {slug} --from B5W --den B5P\n"
          f"  py -3.13 -X utf8 {HERE / 'dong_goi_may2.py'} --job {prof['id']} {slug}")


# ------------------------------------------------------------------ cổng + móc vào make_video
def cong(prof, d, buoc):
    """Gọi ở đầu pha asset. Lane bật review mà chưa nhận bản máy 3 (hoặc script đổi sau khi nhận) → DỪNG."""
    st = trang_thai(prof, d)
    if st in ("off", "received"):
        return
    if st == "stale":
        raise SystemExit(f"✗ {buoc}: script.txt đã đổi SAU khi nhận bản máy 3 → chạy lại `review_may3.py --nhan` (hoặc --share)")
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
    ok, msg, level = gate_common.kiem_lock(d)
    if level != "PASS":
        return      # chưa khoá (ESCALATE/BLOCK/luồng cũ chưa B3G) — chưa có gì để gửi
    m = doc_marker(d)
    if st == "shared" and m.get("sha") == _sha(d):
        print(f"[review] tập {d.name} đã gửi máy 3 ({m.get('at')}), đang chờ cột D = '{TRANG_THAI_DA_SUA}'")
    else:
        share(prof, d.name, dry=dry)
    raise SystemExit(f"⏸ DỪNG SAU B3 — chờ máy 3 soát kịch bản. Khi anh báo cột D = '{TRANG_THAI_DA_SUA}':\n"
                     f"  py -3.13 -X utf8 {HERE / 'review_may3.py'} --nhan --profile {prof['id']} --slug {d.name}")


# ------------------------------------------------------------------ --trang-thai
def trang_thai_lane(prof):
    dg, tab = None, tab_cua(prof)
    import dong_goi_may2 as dg
    s = dg.svc(doc_thoi=True)
    vals = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!A2:D300").execute().get("values", [])
    print(f"tab {tab}:")
    for row in vals:
        dcol = (row[3] if len(row) > 3 else "").strip()
        if dcol in (TRANG_THAI_CHO, TRANG_THAI_DA_SUA):
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
    ap.add_argument("--nguon", help="--nhan: file script máy 3 (mặc định results\\review\\<tab>\\<slug>\\script.txt)")
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
