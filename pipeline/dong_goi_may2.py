# -*- coding: utf-8 -*-
r"""dong_goi_may2.py — C6 (docs/PHUONG_AN_LANE_F_BUOC2_3.md): đóng gói cho MÁY 2 vẽ ảnh + ghép video,
sau khi máy 1 đã xong phần cần NỘI DUNG (kịch bản khoá + characters.json + B5W/B5P).

HAI VIỆC, DÙNG RIÊNG:
  --bundle                          copy TOÀN BỘ pipeline/*.py + profile các lane khai + requirements.txt
                                     vào FlowHandoff_local/shared/buoc2_3_tool/ (làm 1 lần, hoặc mỗi khi
                                     pipeline/ có sửa mới muốn máy 2 dùng bản mới nhất).
  --job <profile> <slug>            đóng gói 1 TẬP cụ thể vào FlowHandoff_local/jobs/<slug>/ + ghi
                                     _BANGIAO.txt (lệnh chặng A/B, tiền dự kiến) + ghi cột H (STATUS-IMG).

VÌ SAO CÓ FILE NÀY
- Bundle máy 2 cũ (09-17) chỉ đủ cho toshi-densetsu-jp (thiếu gate_common/sinh_neo/qc_img_doan/
  prompt_doan/lean_script/tate_text/dong_goi_may2 — thiếu ~20 file) → giờ copy CẢ THƯ MỤC pipeline/,
  không tự liệt kê tay từng file (liệt kê tay là nguồn gốc lỗi thiếu file, y hệt bài học đã trả giá).
- `publish.upload_dir` trong profile ở MÁY 1 là đường tuyệt đối `E:\CLAUDE\YOUTUBE\CHANEL\...` — máy 2
  không có ổ đó. Bundle ghi ĐÈ thành đường TƯƠNG ĐỐI `../../../results/video_render` (tính từ
  pipeline/, nơi lệnh chạy) trỏ vào FlowHandoff_local/results/video_render — Syncthing tự mang về máy 1.
- Đóng gói 1 tập KHÔNG BAO GIỜ diễn ra khi kịch bản chưa khoá (gate_common.kiem_lock level=="FAIL" →
  DỪNG) — máy 2 không có Fable/claude -p để tự sửa kịch bản, giao bản chưa khoá là giao rác.

Dùng:
  py -3.13 dong_goi_may2.py --bundle
  py -3.13 dong_goi_may2.py --job teinengo-real ep01-fuufu-nenkin-sa
"""
import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import gate_common   # noqa: E402
import profiles       # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BUNDLE = ROOT / "FlowHandoff_local" / "shared" / "buoc2_3_tool"
JOBS = ROOT / "FlowHandoff_local" / "jobs"
SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"
COT_H = "H"
TIEU_DE_COT_H = "STATUS-IMG"

REQUIREMENTS = """requests
numpy
Pillow
edge-tts
imageio-ffmpeg
opencv-python-headless
httpx
scipy
PyYAML
google-auth
google-api-python-client
innertube
"""

JOB_FILES = ["script.txt", "script.lock.json", "characters.json", "img_prompts.txt",
             "img_doan.txt", "state.json", "title.txt", "series_ctx.txt", "competitor.txt"]

# 2026-09-23 (vá review HOOK, Việc 2): file TRONG thư mục con `hook/` cần cho máy 2 vẽ ẢNH SHOT HOOK
# (xem docs/GIAO_VIEC_BUOC3_AGENT.md mục 9.1 — `hook/flow_prompts/shot_NN.txt` + `hook/grok_jobs.csv`
# là đơn máy 1 để sẵn cho máy 2 vẽ CÙNG ĐỢT với ảnh thân video). JOB_FILES ở trên chỉ liệt kê file
# nằm Ở GỐC thư mục tập — không đụng thư mục con nào — nên trước bản vá này `hook/` không bao giờ
# theo gói sang máy 2: hook bị rơi mất hoàn toàn mà không cổng nào biết (giống bài học cũ ở
# drive_handoff.py về `_ref/`, xem docstring đầu file drive_handoff.py mục 2).
HOOK_FILES_GOC = ["hook_locked.txt", "hook_lock.json", "hook_storyboard.json", "grok_jobs.csv"]


def svc(doc_thoi=True):
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    scope = "spreadsheets.readonly" if doc_thoi else "spreadsheets"
    creds = Credentials.from_service_account_file(CREDS, scopes=[f"https://www.googleapis.com/auth/{scope}"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


# ============================================================== --bundle
def _bundle_pipeline():
    dst = BUNDLE / "pipeline"
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted((ROOT / "pipeline").glob("*.py")):
        if f.name.startswith("_bak_"):
            continue
        shutil.copy2(f, dst / f.name)
        n += 1
    print(f"  pipeline/: {n} file .py")


def _bundle_profiles(profile_ids):
    # ⚠️ Cố Ý đặt ở pipeline/profiles/ (KHÔNG phải profiles/profiles/ như cấu trúc gốc máy 1) —
    # verify thật 2026-09-21: profiles.py::res("profiles") dò base theo thứ tự
    # [MEI, EXE_DIR, DATA_DIR, HERE, HERE.parent], không frozen thì EXE_DIR=DATA_DIR=HERE=pipeline/.
    # Máy 1 "ăn may" vì %APPDATA%\YoutubeCloneGemini\config.json có sẵn data_dir trỏ đúng
    # <project>/profiles (dấu vết một lần chạy .exe cũ) → DATA_DIR/"profiles" khớp cấu trúc gốc.
    # Máy 2 KHÔNG có config.json đó (máy sạch, chưa từng chạy .exe) → 3 base đầu đều trỏ pipeline/
    # (không có "profiles" con) → rơi xuống HERE.parent = bundle root, nhưng file thật nằm SÂU HƠN
    # 1 cấp (profiles/profiles/) → profiles.load() báo "Không có profile" dù file có tồn tại trên
    # đĩa (tái hiện được bằng `YTCG_DATA_DIR=<thư mục rỗng>` trên máy 1). Đặt tại pipeline/profiles/
    # khớp NGAY base đầu tiên (EXE_DIR/HERE) — không phụ thuộc config.json/env var nào của máy 2.
    dst = BUNDLE / "pipeline" / "profiles"
    dst.mkdir(parents=True, exist_ok=True)
    for pid in profile_ids:
        src = ROOT / "profiles" / "profiles" / f"{pid}.json"
        if not src.exists():
            raise SystemExit(f"✗ không thấy profile {src}")
        data = json.loads(src.read_text(encoding="utf-8"))
        pub = data.setdefault("publish", {})
        pub["upload_dir"] = "../../../results/video_render"
        pub["_note_may2"] = ("Duong dan TUONG DOI tinh tu pipeline/ (noi chay lenh) -> len 3 cap la "
                             "FlowHandoff_local/ -> results/video_render. KHONG doi thanh duong dan "
                             "tuyet doi cua may 1 — profiles bundle nay do dong_goi_may2.py --bundle "
                             "ghi tu dong, sua tay se mat khi chay lai --bundle.")
        (dst / f"{pid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (BUNDLE / "assets" / pid).mkdir(parents=True, exist_ok=True)
        print(f"  profile {pid}.json (upload_dir → relative results/video_render)")


def cmd_bundle(profile_ids):
    print(f"[dong_goi_may2 --bundle] → {BUNDLE}")
    _bundle_pipeline()
    _bundle_profiles(profile_ids)
    (BUNDLE / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    print(f"✓ bundle sẵn sàng — máy 2 chạy: cd {BUNDLE}\\pipeline && pip install -r ..\\requirements.txt")


# ============================================================== --job
def _dem_anh(job_dir):
    pf = job_dir / "img_prompts.txt"
    if not pf.exists():
        return 0, 0, 0
    lines = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
    n_face = sum(1 for l in lines if l.lower().lstrip().startswith("@ref"))
    n = len(lines)
    cost = (n - n_face) * 50 + n_face * 110 + 600      # +600 = 2 master medium
    return n, n_face, cost


def _stt_theo_slug(tab, slug):
    s = svc(doc_thoi=True)
    vals = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!A2:C300").execute().get("values", [])
    for row in vals:
        stt = (row[0] if row else "").strip()
        folder = (row[2] if len(row) > 2 else "").strip().replace("\\", "/")
        if stt and slug.lower() in folder.lower():
            return int(stt)
    raise SystemExit(f"không tìm thấy dòng nào có FOLDER chứa '{slug}' trong tab {tab} (cột C)")


def _ghi_sheet_h(prof, slug, n, cost):
    pub = prof.get("publish") or {}
    tab = pub.get("sheet_tab") or pub.get("upload_channel")
    if not tab:
        print("  (profile không khai publish.sheet_tab/upload_channel → bỏ qua ghi sheet)")
        return
    stt = _stt_theo_slug(tab, slug)
    dong = stt + 1
    s = svc(doc_thoi=True)
    hd = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!{COT_H}1").execute().get("values", [[""]])
    ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten_cot != TIEU_DE_COT_H:
        raise SystemExit(f"cột {COT_H} dòng 1 đang là '{ten_cot or '(trống)'}', không phải "
                         f"'{TIEU_DE_COT_H}' → cột đã đổi chỗ, DỪNG.")
    cur = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!{COT_H}{dong}").execute().get("values", [[]])
    cu = (cur[0][0] if cur and cur[0] else "").strip()
    gia_tri = f"cần ảnh ({n} ảnh, ~{cost:,}đ)"
    if cu:
        print(f"  ô {tab}!{COT_H}{dong} đã có '{cu}' → KHÔNG đè (đóng gói lại không tự sửa trạng thái ảnh)")
        return
    svc(doc_thoi=False).values().update(
        spreadsheetId=SHEET_ID, range=f"{tab}!{COT_H}{dong}",
        valueInputOption="USER_ENTERED", body={"values": [[gia_tri]]}).execute()
    print(f"  ✓ ghi {tab}!{COT_H}{dong} = {gia_tri}")


def _dong_goi_hook(job_dir: Path, dst: Path, _visual: str = "") -> int:
    """Copy các file trong `hook/` (nếu tập thật sự có) vào gói giao máy 2 — lý do ở HOOK_FILES_GOC.

    2026-09-23 (vá review HOOK, Việc 2): áp đúng luật "vận chuyển phải tự chứng minh" của dự án
    (xem drive_handoff.py::doi_chieu — CHƯA verify thì CHƯA coi là xong) — copy xong ĐỐI CHIẾU LẠI
    từng file vừa copy phải có mặt ở đích, đúng kích thước nguồn, không dựa vào giả định
    shutil.copy2 luôn thành công trọn vẹn. Tập KHÔNG có `hook/` (đa số tập, tính năng đang bật dần
    từng kênh) → trả 0, KHÔNG báo lỗi gì — giữ gói giao y như trước khi có tính năng hook.
    """

    # Lane khai script.hook.visual == "lien_mach_than" (vd kenko-chiebukuro): hook KHÔNG phải clip
    # riêng — nó là 30 giây ĐẦU của chính script.txt, sẽ được lồng tiếng và minh hoạ chung một lần
    # với thân video. Gửi kèm grok_jobs.csv/hook_storyboard.json sang máy 2 là mời máy 2 vẽ thêm 7
    # ảnh rồi ghép một clip 30 giây nữa vào đầu → đoạn mở đầu PHÁT HAI LẦN. Xem docs/QUY_TAC_VIDEO_HOOK.md §5b.
    if _visual == "lien_mach_than":
        print("  · hook: lane dựng LIỀN MẠCH (hook nằm trong script.txt) → KHÔNG gửi hook/ sang máy 2")
        return 0
    src_hook = job_dir / "hook"
    if not src_hook.is_dir():
        return 0
    dst_hook = dst / "hook"
    dst_hook.mkdir(parents=True, exist_ok=True)
    can_doi_chieu = []          # [(src, dst)] — dùng để tự kiểm ngay sau khi copy
    for name in HOOK_FILES_GOC:
        s = src_hook / name
        if s.exists():
            d = dst_hook / name
            shutil.copy2(s, d)
            can_doi_chieu.append((s, d))
    fp_src = src_hook / "flow_prompts"
    if fp_src.is_dir():
        fp_dst = dst_hook / "flow_prompts"
        fp_dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(fp_src.glob("*")):
            if f.is_file():
                d = fp_dst / f.name
                shutil.copy2(f, d)
                can_doi_chieu.append((f, d))
    # Tự kiểm: thiếu 1 file ở đây là máy 2 vẽ THIẾU ảnh shot hook mà không cổng nào biết cho tới
    # tận lúc nghiệm thu B10 (hoặc tệ hơn, không ai biết luôn vì B10 chỉ soi final_with_hook.mp4).
    thieu = [str(d.relative_to(dst)) for s, d in can_doi_chieu
             if not d.exists() or d.stat().st_size != s.stat().st_size]
    if thieu:
        raise SystemExit(f"✗ đóng gói hook THẤT BẠI, {len(thieu)} file không khớp sau khi copy: "
                         f"{', '.join(thieu)}")
    return len(can_doi_chieu)


def cmd_job(profile_id, slug):
    prof = profiles.load(profile_id)
    job_dir = ROOT / prof["slug_dir"] / slug
    if not job_dir.is_dir():
        raise SystemExit(f"✗ không thấy {job_dir}")
    ok, msg, level = gate_common.kiem_lock(job_dir)
    if level == "FAIL":
        raise SystemExit(f"✗ CHƯA đóng gói — kịch bản chưa khoá đúng: {msg}")
    print(f"  lock: {msg}")
    # characters.json CHỈ bắt buộc với lane có REF-LOCK. Lane không khoá mặt (vd kenko-chiebukuro:
    # mỗi mục một người khác nhau, image.ref_lock=false) không hề sinh file này — đòi vô điều kiện là
    # chặn oan cả lane, và người chạy sẽ đi tìm một bước B5W/B5P không bao giờ tạo ra nó (đã dính
    # thật 2026-09-23, lane E tập 1).
    _img_cf = (prof.get("image") or {})
    _can = ["img_prompts.txt", "img_doan.txt"]
    if _img_cf.get("ref_lock") or _img_cf.get("characters_from_bible"):
        _can.append("characters.json")
    for need in _can:
        if not (job_dir / need).exists():
            raise SystemExit(f"✗ thiếu {need} — chạy B5W/B5P trước "
                             f"(make_video.py --profile {profile_id} --slug {slug} --only B5W / --only B5P)")

    # ⭐ Anh chốt 2026-09-21: lane có REF-LOCK KHÔNG ĐƯỢC giao mặt nhân vật cho máy 2 tự vẽ mù —
    # máy 1 phải tự vẽ + QC (tuổi/giới, qc_character.py) ảnh master TRƯỚC khi đóng gói, cùng lý do
    # "vẽ 5 ảnh mẫu trước khi vẽ loạt" nhưng ở tầng SỚM HƠN: master sai lan ra cả trăm ảnh loạt.
    img_cf = (prof.get("image") or {})
    ref_masters = []
    if img_cf.get("characters_from_bible"):
        import make_video
        job = make_video.Job(prof, slug)
        print("  REF-LOCK: kiểm/vẽ ảnh master (@REF/@REF2) TRƯỚC khi đóng gói …")
        m1, m2 = job.masters_from_bible()
        ref_masters = [p for p in (m1, m2) if p]
        print(f"  ✓ master: {', '.join(str(p.relative_to(job_dir)) for p in ref_masters)}")

    dst = JOBS / slug
    dst.mkdir(parents=True, exist_ok=True)
    n_copied = 0
    for name in JOB_FILES:
        src = job_dir / name
        if src.exists():
            shutil.copy2(src, dst / name)
            n_copied += 1
    for m in ref_masters:
        rel = m.relative_to(job_dir)          # vd _ref/001.png
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(m, dst / rel)
        n_copied += 1
    if (job_dir / "logs").is_dir():
        shutil.copytree(job_dir / "logs", dst / "logs", dirs_exist_ok=True)

    n_hook = _dong_goi_hook(job_dir, dst, ((prof.get('script') or {}).get('hook') or {}).get('visual', ''))
    n_copied += n_hook

    n, n_face, cost = _dem_anh(job_dir)
    n_scene = n - n_face
    kenh = (prof.get("publish") or {}).get("upload_channel", profile_id)
    tab = (prof.get("publish") or {}).get("sheet_tab", kenh)
    visual = ((prof.get("script") or {}).get("hook") or {}).get("visual", "")
    bg = (
        f"# \u0110\u01a0N GIAO VI\u1ec6C M\u00c1Y 2 \u2014 {profile_id} / {slug}\n"
        f"\u0110\u00f3ng g\u00f3i l\u00fac: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"\u0110\u1eccC TR\u01af\u1edaC: shared\\QUY_TRINH_GIAO_VIEC_MAY2.md (ranh gi\u1edbi m\u00e1y 1 / m\u00e1y 2, 2 c\u1ed5ng b\u1eaft bu\u1ed9c)\n"
        f"M\u1ecdi \u0111\u01b0\u1eddng d\u1eabn d\u01b0\u1edbi \u0111\u00e2y T\u00cdNH T\u1eea th\u01b0 m\u1ee5c Syncthing `FlowHandoff_local\\` c\u1ee7a CH\u00cdNH M\u00c1Y B\u1ea0N\n"
        f"(m\u00e1y 1 \u0111\u1ec3 \u1edf h2dev\\FlowHandoff_local, m\u00e1y 2 \u1edf ch\u1ed7 kh\u00e1c \u2014 \u0111\u1eebng ch\u00e9p nguy\u00ean \u0111\u01b0\u1eddng d\u1eabn tuy\u1ec7t \u0111\u1ed1i c\u1ee7a nhau).\n\n"
        f"## M\u1ed8T L\u1ec6NH DUY NH\u1ea4T\n"
        f"cd shared\\buoc2_3_tool\\pipeline\n"
        f"xcopy /E /I ..\\..\\..\\jobs\\{slug} ..\\assets\\{profile_id}\\{slug}\n"
        f"py -3.13 make_video.py --profile {profile_id} --slug {slug} --from B4\n\n"
        f"L\u1ec7nh n\u00e0y t\u1ef1 l\u00e0m: l\u1ed3ng ti\u1ebfng \u2192 n\u1eafn ph\u1ee5 \u0111\u1ec1 theo k\u1ecbch b\u1ea3n \u2192 v\u1ebd {n} \u1ea3nh \u2192 d\u1ef1ng final.mp4.\n"
        f"B0\u2013B3 (k\u1ecbch b\u1ea3n) m\u00e1y 1 \u0111\u00e3 xong v\u00e0 \u0111\u00e3 kho\u00e1 sha256.\n\n"
        f"## \u1ea2NH: {n} t\u1ea5m ({n_face} kho\u00e1 m\u1eb7t + {n_scene} c\u1ea3nh v\u1eadt)\n"
        + (f"\u1ea2nh master \u0111\u00e3 v\u1ebd s\u1eb5n + QC (_ref/, _ref2/) \u2014 KH\u00d4NG v\u1ebd l\u1ea1i.\n" if ref_masters else "")
        + f"V\u1ebd b\u1eb1ng Google Flow th\u00ec 0\u0111; d\u00f9ng gpti2 th\u00ec \u2248 {cost:,}\u0111. Ch\u1ecdn c\u00e1ch n\u00e0o l\u00e0 quy\u1ec1n m\u00e1y 2, nh\u01b0ng\n"
        f"b\u00e1o l\u1ea1i s\u1ed1 ti\u1ec1n TH\u1eacT \u0111\u00e3 ti\u00eau.\n\n"
        f"## HAI C\u1ed4NG KH\u00d4NG \u0110\u01af\u1ee2C T\u1eaeT\n"
        f"1. C\u1ed5ng PH\u1ee6 CH\u1eee (tts.py::kiem_phu_chu) \u2014 so s\u1ed1 ch\u1eef ph\u1ee5 \u0111\u1ec1 server tr\u1ea3 v\u1ec1 v\u1edbi K\u1ecaCH B\u1ea2N G\u1ed0C,\n"
        f"   thi\u1ebfu qu\u00e1 5% l\u00e0 d\u1eebng. \u0110o th\u1eadt 23/09: 3/4 l\u01b0\u1ee3t ai33 NU\u1ed0T TR\u1eccN M\u1ed8T C\u00c2U, kh\u00f4ng b\u00e1o l\u1ed7i.\n"
        f"   G\u1eb7p l\u1ed7i n\u00e0y th\u00ec CH\u1ea0Y L\u1ea0I \u0111\u00fang l\u1ec7nh \u0111\u00f3 \u2014 \u0111\u1eebng \u0111em b\u1ea3n thi\u1ebfu \u0111i gh\u00e9p.\n"
        f"2. C\u1ed5ng KHO\u00c1 (gate_common.kiem_lock) \u2014 script.txt b\u1ecb s\u1eeda sau khi kho\u00e1 l\u00e0 ch\u1eb7n c\u1ee9ng.\n\n"
        f"## 5 LU\u1eacT C\u1ea4M\n"
        f"1. KH\u00d4NG --from s\u1edbm h\u01a1n B4 (m\u00e1y 2 kh\u00f4ng c\u00f3 Fable/claude -p \u0111\u1ec3 vi\u1ebft l\u1ea1i k\u1ecbch b\u1ea3n).\n"
        f"2. KH\u00d4NG s\u1eeda script.txt / img_prompts.txt / img_doan.txt / characters.json / profiles/*.json.\n"
        f"3. QC r\u1edbt \u2192 \u0111\u1ecdc logs/*.json r\u1ed3i b\u00e1o l\u1ea1i, KH\u00d4NG --force-qc.\n"
        f"4. H\u1ebft ti\u1ec1n / h\u1ebft h\u1ea1n m\u1ee9c \u2192 D\u1eeaNG b\u00e1o l\u1ea1i, KH\u00d4NG t\u1ef1 \u0111\u1ed5i provider.\n"
        f"5. B\u00e1o c\u00e1o k\u00e8m TH\u1edcI GIAN TH\u1eacT + s\u1ed1 \u1ea3nh/ti\u1ec1n TH\u1eacT (kh\u00f4ng \u01b0\u1edbc l\u01b0\u1ee3ng).\n\n"
        + (f"## HOOK\n"
           f"Lane n\u00e0y khai script.hook.visual = `{visual}`: hook l\u00e0 30 gi\u00e2y \u0110\u1ea6U c\u1ee7a ch\u00ednh script.txt,\n"
           f"l\u1ed3ng ti\u1ebfng v\u00e0 minh ho\u1ea1 chung M\u1ed8T L\u1ea6N v\u1edbi th\u00e2n video. G\u00f3i n\u00e0y C\u1ed0 \u00dd KH\u00d4NG c\u00f3 th\u01b0 m\u1ee5c hook\\\n"
           f"\u2014 \u0111\u1ec3 nguy\u00ean, \u0111\u1eebng d\u1ef1ng th\u00eam clip 30 gi\u00e2y n\u1eefa (s\u1ebd th\u00e0nh ph\u00e1t hai l\u1ea7n).\n\n"
           if visual == "lien_mach_than" else
           f"## HOOK\nLane khai script.hook.visual = `{visual}`: hook l\u00e0 CLIP RI\u00caNG, \u0111\u01a1n v\u1ebd \u1edf hook\\.\n"
           f"D\u1ef1ng xong n\u1ed1i v\u00e0o TR\u01af\u1edaC final.mp4 \u2192 final_with_hook.mp4, qua 4 ph\u00e9p ki\u1ec3m \u1edf\n"
           f"shared\\QUY_TAC_VIDEO_HOOK.md \u00a72 (m\u1ee9c ti\u1ebfng \u00b7 fps \u00b7 ki\u1ec3u ph\u1ee5 \u0111\u1ec1 \u00b7 \u0111i\u1ec3m n\u1ed1i).\n\n"
           if visual else "")
        + f"## TR\u1ea2 H\u00c0NG\n"
        f"results\\{tab}\\{slug}\\  \u2014 \u0111\u00fang c\u1ea5u tr\u00fac n\u00e0y (theo T\u00caN TAB SHEET, kh\u00f4ng ph\u1ea3i t\u00ean lane).\n"
        f"Syncthing t\u1ef1 mang v\u1ec1 m\u00e1y 1.\n"
    )
    (dst / "_BANGIAO.txt").write_text(bg, encoding="utf-8")
    print(f"✓ đóng gói {dst} ({n_copied} file + logs/) · {n} ảnh ≈ {cost:,}đ")
    if n_hook:
        print(f"  ✓ hook/: {n_hook} file đã đóng gói + đối chiếu khớp kích thước "
              f"(máy 2 vẽ ảnh shot hook cùng đợt — xem docs/GIAO_VIEC_BUOC3_AGENT.md mục 9.1)")

    try:
        _ghi_sheet_h(prof, slug, n, cost)
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột H: {e}")
    print(f"\nĐưa đường dẫn này cho anh bàn giao máy 2:\n  {dst}")
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", action="store_true", help="copy toàn bộ pipeline/ + profile vào FlowHandoff_local/shared/buoc2_3_tool/")
    ap.add_argument("--profile-list", nargs="*", default=None,
                    help="chỉ dùng với --bundle: danh sách profile id đưa vào bundle "
                         "(mặc định teinengo-real teinengo-tanoshimi)")
    ap.add_argument("--job", nargs=2, metavar=("PROFILE", "SLUG"), help="đóng gói 1 tập")
    a = ap.parse_args()
    if a.bundle:
        cmd_bundle(a.profile_list or ["teinengo-real", "teinengo-tanoshimi"])
    elif a.job:
        cmd_job(a.job[0], a.job[1])
    else:
        ap.error("cần --bundle hoặc --job PROFILE SLUG")


if __name__ == "__main__":
    main()
