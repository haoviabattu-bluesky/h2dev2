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


def cmd_job(profile_id, slug):
    prof = profiles.load(profile_id)
    job_dir = ROOT / prof["slug_dir"] / slug
    if not job_dir.is_dir():
        raise SystemExit(f"✗ không thấy {job_dir}")
    ok, msg, level = gate_common.kiem_lock(job_dir)
    if level == "FAIL":
        raise SystemExit(f"✗ CHƯA đóng gói — kịch bản chưa khoá đúng: {msg}")
    print(f"  lock: {msg}")
    for need in ("img_prompts.txt", "img_doan.txt", "characters.json"):
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

    n, n_face, cost = _dem_anh(job_dir)
    n_scene = n - n_face
    kenh = (prof.get("publish") or {}).get("upload_channel", profile_id)
    bg = (
        f"# ĐƠN GIAO VIỆC MÁY 2 — {profile_id} / {slug}\n"
        f"Đóng gói lúc: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"## Chặng A — VẼ ẢNH (đọc FlowHandoff_local/shared/GIAO_VIEC_MAY2_LANE_F.md VIỆC 2 trước khi chạy)\n"
        f"{n} ảnh: {n_face} khoá mặt (@REF/@REF2) + {n_scene} cảnh vật ≈ {cost - 600:,}đ"
        + (f" — ẢNH MASTER ĐÃ VẼ SẴN + QC (@REF/@REF2 trong _ref//_ref2/, ~600đ máy 1 đã tiêu) → "
           f"KHÔNG vẽ lại, gen_images tự nhận ra đã có\n" if ref_masters else " + master ×2 ≈ 600đ\n")
        + f"→ tổng ≈ {cost:,}đ\n"
        f"cd FlowHandoff_local\\shared\\buoc2_3_tool\\pipeline\n"
        f"xcopy /E /I ..\\..\\..\\jobs\\{slug} ..\\assets\\{profile_id}\\{slug}\n"
        f"py make_video.py --profile {profile_id} --slug {slug} --only B5 --sample-only\n"
        f"  (DỪNG sau mẫu dù QC PASS — chờ máy 1 xem rồi mới bỏ --sample-only ở lệnh dưới, xem VIỆC 2)\n"
        f"py make_video.py --profile {profile_id} --slug {slug} --only B5\n"
        f"py make_video.py --profile {profile_id} --slug {slug} --only B5Q\n\n"
        f"## Chặng B — GIỌNG + GHÉP VIDEO (CHỈ chạy khi dòng VOICE= dưới đây ĐÃ được máy 1 điền)\n"
        f"VOICE=\n"
        f"py make_video.py --profile {profile_id} --slug {slug} --voice <giá trị VOICE ở trên>\n\n"
        f"## 6 LUẬT CẤM — đọc đủ ở GIAO_VIEC_MAY2_LANE_F.md trước khi chạy\n"
        f"1. KHÔNG --from sớm hơn B4 (script.lock.json đã khoá — xoá lại từ B3 là mất công máy 1, và "
        f"   máy 2 không có Fable/claude -p để viết lại).\n"
        f"2. KHÔNG sửa script.txt / img_prompts.txt / img_doan.txt / characters.json / profiles/*.json.\n"
        f"3. B5S/B5Q rớt → đọc logs/*.json rồi báo lại, KHÔNG --force-qc.\n"
        f"4. Hết tiền gpti2 (402/429 cả 3 key) → DỪNG báo lại, KHÔNG tự đổi provider khác.\n"
        f"5. Mọi báo cáo kèm số đo THỜI GIAN THẬT + số ảnh/tiền THẬT đã tiêu (không ước lượng).\n"
        f"6. Xong → results/video_render/{kenh}/{slug}/ đủ 3 file (final.mp4, phude.srt, review-vi.mp4) "
        f"— Syncthing tự mang về máy 1, không cần copy đi đâu thêm.\n"
    )
    (dst / "_BANGIAO.txt").write_text(bg, encoding="utf-8")
    print(f"✓ đóng gói {dst} ({n_copied} file + logs/) · {n} ảnh ≈ {cost:,}đ")

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
