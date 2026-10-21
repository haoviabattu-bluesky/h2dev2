# -*- coding: utf-8 -*-
r"""dong_goi_may2.py — C6 (docs/PHUONG_AN_LANE_F_BUOC2_3.md): đóng gói cho MÁY 2 vẽ ảnh + ghép video,
sau khi máy 1 đã xong phần cần NỘI DUNG (kịch bản khoá + characters.json + B5W/B5P).

HAI VIỆC, DÙNG RIÊNG:
  --bundle                          copy TOÀN BỘ pipeline/*.py + profile các lane khai + requirements.txt
                                     vào FlowHandoff_local/shared/buoc2_3_tool/ (làm 1 lần, hoặc mỗi khi
                                     pipeline/ có sửa mới muốn máy 2 dùng bản mới nhất).
  --job <profile> <slug>            đóng gói 1 TẬP cụ thể vào FlowHandoff_local/jobs/<tên tab>/<slug>/ + ghi
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
import re
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
             "img_doan.txt", "state.json", "title.txt", "series_ctx.txt", "competitor.txt",
             # 2026-09-24 (anh chốt): máy 1 xong việc PHẢI gửi kèm FILE HOOK TEXT để dự án
             # tiêu đề YT-TITLE-RESEARCH + máy 2 đọc mà làm (tiêu đề/mô tả/chữ thumbnail phải
             # cùng MỘT lời hứa với hook). `promise.txt` đi kèm vì nó là lời hứa gốc mà cả hai
             # bên phải bám — thiếu là bên kia viết tiêu đề trên file rỗng nghĩa.
             "HOOK_TAP.md", "promise.txt",
             # 2026-09-26 (máy 2 báo thiếu ở gốc tập, CLAUDE.md quy tắc 0000): ID video gốc đi kèm job.
             "video_goc.json",
             # 2026-09-26 (máy 2 báo ep01 Lane M): marker chặng máy 3 — thiếu là cổng review_may3.cong() ở máy 2 coi
             # tập "chưa soát" và DỪNG trước B4 (lại còn tự share sang thư mục lồng ngoài Syncthing).
             "review_may3.json",
             # 2026-09-24 Lane K (đa giọng): vai.txt = câu nào ai đọc (máy 1 gắn, máy 2 lồng tiếng + vẽ bóng thoại theo đó)
             "vai.txt", "yomi.txt",
             # 2026-09-24 Lane L: chỗ đặt hiệu ứng âm thanh thân video (máy 1 chọn theo nội dung, máy 2 B8 trộn)
             "sfx_plan.txt",
             # 2026-10-06 (anh chốt, skill motion_graphics): số liệu động TRÊN ảnh. Từ 2026-10-07 máy 2 tự sinh +
             # duyệt file này (shared\motion_graphics\HUONG_DAN_MAY2.md); máy 1 có sẵn bản cũ thì vẫn gửi kèm.
             "so_lieu_dong.json",
             # 2026-10-11 (anh: "áp dụng thật nhiều motion graphic"): ý đồ motion giải thích (bảng/sơ đồ/timeline)
             # máy 1 viết ở bước 1 theo cụm neo trong kịch bản; máy 2 dựng sau final.mp4, cụm neo mất thì bỏ mục.
             "mg_y_do.md",
             # 2026-10-11 (anh chốt Lane L ep14): thẻ tên động ở THÂN bài + giây nghỉ sau câu neo (tts_voicevox đọc file này)
             "the_ten_than.json"]

# 2026-09-23 (vá review HOOK, Việc 2): file TRONG thư mục con `hook/` cần cho máy 2 vẽ ẢNH SHOT HOOK
# (xem docs/GIAO_VIEC_BUOC3_AGENT.md mục 9.1 — `hook/flow_prompts/shot_NN.txt` + `hook/grok_jobs.csv`
# là đơn máy 1 để sẵn cho máy 2 vẽ CÙNG ĐỢT với ảnh thân video). JOB_FILES ở trên chỉ liệt kê file
# nằm Ở GỐC thư mục tập — không đụng thư mục con nào — nên trước bản vá này `hook/` không bao giờ
# theo gói sang máy 2: hook bị rơi mất hoàn toàn mà không cổng nào biết (giống bài học cũ ở
# drive_handoff.py về `_ref/`, xem docstring đầu file drive_handoff.py mục 2).
HOOK_FILES_GOC = ["hook_locked.txt", "hook_lock.json", "hook_storyboard.json", "grok_jobs.csv",
                  # 2026-09-25 (vá theo YEU_CAU_MAY1_..._thieu_hook_promise.md): thiếu file này làm
                  # hook_stage.promise_snapshot() không tìm thấy hash gốc → mọi tập kẹt HOOK_STALE ở B4.
                  "promise.txt",
                  # 2026-09-24 (anh chốt, MỌI lane): MÁY 1 tự vẽ ảnh hook + sinh clip hook, máy 2 CHỈ GHÉP
                  # → gói phải mang đủ ảnh + clip + SFX + mốc cắt + công cụ ghép (xem docs/QUY_TAC_VIDEO_HOOK.md §0).
                  "hook_timeline.json", "img_prompts_hook.txt", "GROK_HUONG_DAN.md", "hook_voice.mp3",
                  "hook_voice.srt", "hook_vi.srt", "ghep_hook_thay_hinh.py", "dung_hook_preview.py", "ghep_hook_noi_truoc.py",
                  # 2026-09-24 Lane G ep01: phụ đề Nhật đã nắn (cháy chữ) + script dựng/nối riêng lane cháy phụ đề
                  "hook_jp.srt", "dung_hook.py", "hook_tts.txt"]
HOOK_DIRS = ["flow_prompts", "img", "clip", "sfx", "qc",   # thư mục con của hook/ gửi kèm (bỏ qua _cu/)
             "the_ten"]   # 10/10 Lane O ep05: thẻ tên động (webm alpha) shot `the_ten` trong hook_timeline.json


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
    # 2026-09-25: don_flow_tool.py doc khuon tu 2 file .txt nay luc chay (KHONG phai .py nen vong lap
    # tren khong bat) + README lam tai lieu tra cuu cho may 2 — thieu la don_flow_tool.py sys.exit
    # ngay khi may 2 chay lo dau tien, bat ngo vi cac lenh .py khac deu chay binh thuong.
    _them = ["flow_tool_template_va3.txt", "flow_tool_template_plain.txt", "README_flow_tool.md"]
    n_them = 0
    for ten in _them:
        f = ROOT / "pipeline" / ten
        if f.is_file():
            shutil.copy2(f, dst / ten)
            n_them += 1
    print(f"  pipeline/: {n_them} file .txt/.md phu (khuon Flow Tool + README)")


def _bundle_tools():
    # 2026-09-30 (máy 2 giao, anh chốt): B8n nut_dang_ky.py tìm tool ở <gốc bundle>/tools/subscribe_overlay —
    # thiếu là B8 dừng "không thấy tools/subscribe_overlay". Bỏ cache (tool tự tạo) + _nghe_chuong (file nghe thử).
    src = ROOT / "tools" / "subscribe_overlay"
    if not src.is_dir():
        raise SystemExit(f"✗ không thấy {src} — B8n (nút đăng ký) cần tool này")
    dst = BUNDLE / "tools" / "subscribe_overlay"
    shutil.copytree(src, dst, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("cache", "_nghe_chuong", "__pycache__"))
    print(f"  tools/subscribe_overlay → {dst}")


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
        (BUNDLE / data.get("slug_dir", f"assets/{pid}")).mkdir(parents=True, exist_ok=True)   # Lane M: slug_dir ≠ id
        # Nhạc nền lane (assemble.bgm, đường dẫn tính từ ROOT): make_video máy 2 tra ROOT/<bgm> = gốc bundle,
        # không có file là B8 LẶNG LẼ dựng video KHÔNG nhạc (nhánh `if ... exists()`) → phải chép kèm.
        bgm = (data.get("assemble") or {}).get("bgm")
        if bgm and (ROOT / bgm).exists():
            (BUNDLE / bgm).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / bgm, BUNDLE / bgm)
            print(f"  nhạc nền {bgm}")
        # Lane L 2026-09-25: kho hiệu ứng âm thanh lane (assemble.sfx, sfx_than.kho_dir = <slug_dir>/_sfx) — chép kèm
        # để máy 2 dùng ĐÚNG bộ tiếng tập trước (ai33 sinh lại là ra tiếng khác, mất nhất quán giữa các tập).
        kho = ROOT / data.get("slug_dir", f"assets/{pid}") / "_sfx"
        if ((data.get("assemble") or {}).get("sfx") or {}).get("enabled") and kho.is_dir():
            dk = BUNDLE / data.get("slug_dir", f"assets/{pid}") / "_sfx"
            dk.mkdir(parents=True, exist_ok=True)
            n_sfx = 0
            for f_ in kho.glob("*.mp3"):
                shutil.copy2(f_, dk / f_.name)
                n_sfx += 1
            print(f"  kho SFX lane: {n_sfx} file → {dk}")
        print(f"  profile {pid}.json (upload_dir → relative results/video_render)")


def cmd_bundle(profile_ids):
    print(f"[dong_goi_may2 --bundle] → {BUNDLE}")
    _bundle_pipeline()
    _bundle_tools()
    _bundle_profiles(profile_ids)
    (BUNDLE / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    print(f"✓ bundle sẵn sàng — máy 2 chạy: cd {BUNDLE}\\pipeline && pip install -r ..\\requirements.txt")


# ============================================================== --job
def _dem_anh(job_dir):
    pf = job_dir / "img_prompts.txt"
    if not pf.exists():
        return 0, 0, 0
    lines = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
    n_face = sum(1 for l in lines if l.lower().lstrip().startswith(("@ref", "@cast:")))
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


COT_D = "D"
TIEU_DE_COT_D = "KỊCH BẢN"
DA_GIAO = "Đã giao máy 2"      # 2026-10-03 anh chốt thay "Done" (docs\TRANG_THAI_COT_D_K.md)
CHO_DUNG = "Chờ dựng video"    # 2026-10-21: máy 2 làm A→Z — hook duyệt xong thì chính máy 2 dựng luôn, không giao ai


def tai_cho():
    """21/10 (anh chốt): máy 2 làm 100% A→Z từ checkout git h2dev (MAY.local=2) → --job KHÔNG đóng gói sang jobs\\,
    viết _BANGIAO.txt ngay trong thư mục tập với lệnh chạy TẠI CHỖ. Bundle cũ buoc2_3_tool không dùng nhánh này."""
    import may_hien_tai
    return may_hien_tai.la_may2() and "buoc2_3_tool" not in str(HERE)


def nhan_d_xong():
    return CHO_DUNG if tai_cho() else DA_GIAO


def _ghi_cot_d_done(s, tab, dong):
    """Anh chốt 2026-09-24 (MỌI lane): máy 1 làm xong tập (kịch bản khoá + hook + prompt ảnh) → cột D báo đã xong
    phần máy 1 (2026-10-03: chữ `Đã giao máy 2`, cũ `Done`); cột H = "cần ảnh" là LỆNH GIAO VIỆC cho máy 2. Hai ô ghi
    CÙNG lúc đóng gói, không để ai nhớ tay. D đã có chữ khác (vd ESCALATE) thì KHÔNG đè — in ra để người xem."""
    hd = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!{COT_D}1").execute().get("values", [[""]])
    ten = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if not ten.startswith(TIEU_DE_COT_D):
        raise SystemExit(f"cột {COT_D} dòng 1 đang là '{ten or '(trống)'}', không phải '{TIEU_DE_COT_D}' → cột đã đổi chỗ, DỪNG.")
    cur = s.values().get(spreadsheetId=SHEET_ID, range=f"{tab}!{COT_D}{dong}").execute().get("values", [[]])
    cu = (cur[0][0] if cur and cur[0] else "").strip()
    dau = cu.splitlines()[0].strip() if cu else ""      # ô có thể kèm đường dẫn ở dòng 2
    nhan = nhan_d_xong()
    if dau == nhan:
        print(f"  ô {tab}!{COT_D}{dong} đã '{nhan}'")
        return
    # 2026-09-26: chặng máy 3 — "Đã sửa kịch bản" là trạng thái đúng ngay trước khi giao máy 2.
    # 2026-10-02: thêm chặng anh duyệt hook — "Đã duyệt hook". 2026-10-03: "Đang làm Hook" (lane không có chặng duyệt
    # hook) + "Done" (tập giao trước 03/10, đóng gói lại → đổi sang chữ mới).
    if dau and dau not in ("Đã sửa kịch bản", "Đang làm Hook", "Đã duyệt hook", "Done", DA_GIAO):
        print(f"  ⚠️ ô {tab}!{COT_D}{dong} đang là '{cu}' → KHÔNG đè thành {nhan}, người xem quyết")
        return
    svc(doc_thoi=False).values().update(spreadsheetId=SHEET_ID, range=f"{tab}!{COT_D}{dong}",
                                        valueInputOption="USER_ENTERED", body={"values": [[nhan]]}).execute()
    print(f"  ✓ ghi {tab}!{COT_D}{dong} = {nhan}")


def _ghi_sheet_h(prof, slug, n, cost):
    pub = prof.get("publish") or {}
    tab = pub.get("sheet_tab") or pub.get("upload_channel")
    if not tab:
        print("  (profile không khai publish.sheet_tab/upload_channel → bỏ qua ghi sheet)")
        return
    stt = _stt_theo_slug(tab, slug)
    dong = stt + 1
    s = svc(doc_thoi=True)
    _ghi_cot_d_done(s, tab, dong)
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


def _dong_goi_hook(job_dir: Path, dst: Path, _visual: str = "", chi_kiem: bool = False) -> int:
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
    if chi_kiem:          # 21/10 máy 2 làm A→Z tại chỗ: không chép đi đâu, chỉ giữ cổng "đủ clip hook"
        _kiem_clip_hook(src_hook)
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
    for sub in HOOK_DIRS:
        fp_src = src_hook / sub
        if not fp_src.is_dir():
            continue
        fp_dst = dst_hook / sub
        fp_dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(fp_src.glob("*")):
            if f.is_file():
                d = fp_dst / f.name
                shutil.copy2(f, d)
                can_doi_chieu.append((f, d))
    _kiem_clip_hook(src_hook)
    # Tự kiểm: thiếu 1 file ở đây là máy 2 vẽ THIẾU ảnh shot hook mà không cổng nào biết cho tới
    # tận lúc nghiệm thu B10 (hoặc tệ hơn, không ai biết luôn vì B10 chỉ soi final_with_hook.mp4).
    thieu = [str(d.relative_to(dst)) for s, d in can_doi_chieu
             if not d.exists() or d.stat().st_size != s.stat().st_size]
    if thieu:
        raise SystemExit(f"✗ đóng gói hook THẤT BẠI, {len(thieu)} file không khớp sau khi copy: "
                         f"{', '.join(thieu)}")
    return len(can_doi_chieu)


def _kiem_clip_hook(src_hook: Path):
    # 2026-09-24: hook = VIDEO sinh sẵn TRƯỚC khi dựng thân. Có hook_timeline.json mà thiếu clip nào → KHÔNG giao
    # (giao thiếu = tự vẽ bù, hoặc thay ảnh tĩnh — cả hai đều sai luật).
    tl_f = src_hook / "hook_timeline.json"
    if tl_f.exists():
        import json as _json
        shots = _json.loads(tl_f.read_text(encoding="utf-8")).get("shots", [])
        thieu_clip = [x["clip"] for x in shots if x.get("clip") and not (src_hook / x["clip"]).exists()]
        if thieu_clip:
            raise SystemExit(f"✗ hook THIẾU {len(thieu_clip)} clip {thieu_clip} — máy 1 phải sinh đủ clip hook "
                             f"(grok_batch.py) TRƯỚC khi giao máy 2 (docs/QUY_TAC_VIDEO_HOOK.md §0)")
        qc_fail = []
        for x in shots:
            q = src_hook / "qc" / f"clip_{x['n']:02d}.json"
            if not q.exists() or _json.loads(q.read_text(encoding="utf-8")).get("verdict") != "PASS":
                qc_fail.append(x["n"])
        if qc_fail:
            print(f"  ⚠ hook: cảnh {qc_fail} chưa có QC PASS (pipeline/qc_hook_clip.py) — giao kèm, nhưng phải được anh duyệt")


def _k_giao_may2(dst, tab, slug, lenh, prof):
    """Ô K dòng tập vừa giao: anh chép nguyên ô này dán cho máy 2. Đường dẫn máy 2 tính từ FlowHandoff_local của máy 2.
    2026-10-04 (anh chốt): KHÔNG kèm dòng hướng dẫn tập kế — cái đó nằm ở ô K DÒNG TẬP KẾ (huong_dan_tab_moi)."""
    import review_may3
    lane, ep = review_may3.ma_tap(prof, slug)
    so = re.match(r"ep(\d+)", ep)
    if tai_cho():
        L = [f"Lane {lane} tập {int(so.group(1)) if so else ep} - máy 2 tự dựng A→Z (21/10)",
             f"Làm theo {Path(dst) / '_BANGIAO.txt'}"]
        return "\n".join(L + (["Lệnh chặng 1:"] + lenh if lenh else []))
    L = [f"Lane {lane} tập {int(so.group(1)) if so else ep} - giao máy 2 thực hiện",
         f"Làm theo FlowHandoff_local\\jobs\\{tab}\\{slug}\\_BANGIAO.txt (đọc trước shared\\QUY_TRINH_GIAO_VIEC_MAY2.md).",
         ]
    if lenh:
        L += ["Lệnh chặng 1 (chạy trong thư mục FlowHandoff_local của máy 2):"] + lenh
    else:
        L += ["Tập đã có final.mp4 — chỉ làm mục HOOK trong _BANGIAO.txt, KHÔNG chạy lại make_video."]
    L += [f"Máy 1: {Path(dst) / '_BANGIAO.txt'}"]
    return "\n".join(L)


def cmd_job(profile_id, slug, no_title=False):
    prof = profiles.load(profile_id)
    job_dir = ROOT / prof["slug_dir"] / slug
    if not job_dir.is_dir():
        raise SystemExit(f"✗ không thấy {job_dir}")
    # 2026-09-26 (anh chốt): lane bật soát máy 3 (`script.review_may3`, mặc định BẬT) mà tập chưa nhận bản
    # máy 3 → KHÔNG được giao máy 2 (giọng/ảnh dựng trên kịch bản chưa soát). Xem pipeline/review_may3.py.
    import review_may3
    review_may3.cong(prof, job_dir, "dong_goi_may2 --job")
    # ⭐ anh chốt 2026-09-25: jobs/ PHẢI chia theo TÊN TAB TRANG TÍNH (publish.sheet_tab), không để
    # phẳng theo slug — slug trùng giữa 2 lane khác nhau (vd 2 lane cùng đặt "ep01-...") từng có nguy
    # cơ đè job của nhau vì jobs/<slug>/ không phân biệt lane. Một nguồn chân lý DUY NHẤT: sheet_tab.py.
    tab = (prof.get("publish") or {}).get("sheet_tab") or (prof.get("publish") or {}).get("upload_channel") or profile_id
    # 2026-10-02 (anh chốt): clip hook đầy đủ (giọng + phụ đề Việt) phải được anh DUYỆT rồi mới giao máy 2.
    import duyet_hook
    duyet_hook.cong(prof, job_dir, "dong_goi_may2 --job", dst=JOBS / tab / slug)
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

    # ⭐ Anh chốt 2026-09-24: xong việc máy 1 thì PHẢI gửi kèm FILE HOOK TEXT. Cổng ở đây vì đây là
    # cửa DUY NHẤT hàng đi ra khỏi máy 1 — `HOOK_TAP.md` là thứ dự án tiêu đề (YT-TITLE-RESEARCH) và
    # máy 2 đọc để viết tiêu đề/mô tả/chữ thumbnail cùng MỘT lời hứa với hook. Thiếu file, hoặc còn
    # chỗ chưa viết, thì giao đi là bên kia làm trên dữ liệu rỗng nghĩa (đúng kiểu sự cố 2 tập satori
    # lọt tới người xem với listing rỗng — memory tieu-de-mo-ta-phai-o-buoc-1).
    import hook_tap_md
    loi_ht = hook_tap_md.kiem(job_dir)
    if loi_ht:
        raise SystemExit("✗ " + "\n✗ ".join(loi_ht))
    # 2026-09-24 Lane L: lane bật hiệu ứng âm thanh thân video → chỗ đặt tiếng là việc NỘI DUNG của máy 1
    if (((prof.get("assemble") or {}).get("sfx") or {}).get("enabled")) and not (job_dir / "sfx_plan.txt").exists():
        raise SystemExit(f"✗ thiếu sfx_plan.txt — máy 1 chạy: py -3.13 pipeline\\sfx_than.py --profile {profile_id} "
                         f"--slug {job_dir} --plan")

    # ⭐ Anh chốt 2026-09-21: lane có REF-LOCK KHÔNG ĐƯỢC giao mặt nhân vật cho máy 2 tự vẽ mù —
    # máy 1 phải tự vẽ + QC (tuổi/giới, qc_character.py) ảnh master TRƯỚC khi đóng gói, cùng lý do
    # "vẽ 5 ảnh mẫu trước khi vẽ loạt" nhưng ở tầng SỚM HƠN: master sai lan ra cả trăm ảnh loạt.
    img_cf = (prof.get("image") or {})
    ref_masters = []
    cast_lane = False
    if img_cf.get("characters_from_bible"):
        import make_video
        job = make_video.Job(prof, slug)
        print("  REF-LOCK: kiểm/vẽ ảnh master (@REF/@REF2 hoặc _ref_<id>) TRƯỚC khi đóng gói …")
        cast_lane = job.cast_mode()
        if cast_lane:
            # Lane K: N nhân vật/tập — dict id → master; lane đa giọng còn phải có vai.txt (giọng từng câu)
            ref_masters = list(job.masters_from_bible().values())
            if profiles.da_giong(prof) and not (job_dir / "vai.txt").exists():
                raise SystemExit(f"✗ thiếu vai.txt — chạy gan_vai.py --profile {profile_id} --slug {job_dir} trước")
        else:
            m1, m2 = job.masters_from_bible()
            ref_masters = [p for p in (m1, m2) if p]
        print(f"  ✓ master: {', '.join(str(p.relative_to(job_dir)) for p in ref_masters)}")

    # 2026-09-24: lane KHÔNG bật characters_from_bible (vd kenko) vẫn có thể có master khoá mặt làm tay cho vài ảnh
    # @REF (kenko ep02: bà 68 tuổi của hook xuất hiện lại ở thân bài) → có file thì gửi kèm, không thì máy 2 vẽ @REF mù mặt.
    for sub in ("_ref", "_ref2"):
        m = job_dir / sub / "001.png"
        if m.exists() and m not in ref_masters:
            ref_masters.append(m)

    o_cho = tai_cho()
    dst = job_dir if o_cho else JOBS / tab / slug
    dst.mkdir(parents=True, exist_ok=True)
    n_copied = 0
    for name in ([] if o_cho else JOB_FILES):
        src = job_dir / name
        if src.exists():
            shutil.copy2(src, dst / name)
            n_copied += 1
    for m in ([] if o_cho else ref_masters):
        rel = m.relative_to(job_dir)          # vd _ref/001.png
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(m, dst / rel)
        n_copied += 1
    if (job_dir / "logs").is_dir() and not o_cho:
        shutil.copytree(job_dir / "logs", dst / "logs", dirs_exist_ok=True)

    n_hook = _dong_goi_hook(job_dir, dst, ((prof.get('script') or {}).get('hook') or {}).get('visual', ''),
                            chi_kiem=o_cho)
    n_copied += n_hook

    n, n_face, cost = _dem_anh(job_dir)
    n_scene = n - n_face
    kenh = (prof.get("publish") or {}).get("upload_channel", profile_id)
    # `tab` đã tính ở đầu hàm (dùng để đặt thư mục jobs/<tab>/<slug>/) — dùng lại, không tính lại.
    visual = ((prof.get("script") or {}).get("hook") or {}).get("visual", "")
    # \u26a0\ufe0f 2026-09-24 (ph\u00e1t hi\u1ec7n th\u1eadt khi v\u00e1 hook Lane F): job \u0111\u00f3ng g\u00f3i L\u1ea0I cho t\u1eadp \u0110\u00c3 C\u00d3 final.mp4
    # (ki\u1ec3m th\u1eb3ng ROOT/FlowHandoff_local/results/video_render/<upload_channel>/<slug>/final.mp4 \u2014
    # \u0111\u01b0\u1eddng TH\u1eacT giao_hang.py ghi, KH\u00d4NG ph\u1ea3i results/<sheet_tab>/ m\u00e0 b\u1ea3n c\u0169 c\u1ee7a kh\u1ed1i "TR\u1ea2 H\u00c0NG" b\u00ean
    # d\u01b0\u1edbi t\u1eebng ghi nh\u1ea7m) v\u1eabn generate "M\u1ed8T L\u1ec6NH DUY NH\u1ea4T" b\u1ea3o m\u00e1y 2 ch\u1ea1y `--from B4` \u2014 t\u1ee9c B\u1eaeT V\u1ebc
    # L\u1ea0I TO\u00c0N B\u1ed8 gi\u1ecdng+\u1ea3nh+video \u0111\u00e3 xong, \u0111\u1ed1t ti\u1ec1n oan l\u1ea7n 2. Ch\u1ec9 \u0111\u00fang khi \u0110ANG \u0111\u00f3ng g\u00f3i job M\u1edaI.
    # Lane M (2026-09-26): slug_dir = tên tab (assets/M-teinengo-anaba) ≠ id → đường xcopy trong cây bundle phải theo slug_dir,
    # không theo id (make_video máy 2 tìm tập ở ROOT/slug_dir/<slug>).
    adir = (prof.get("slug_dir") or f"assets/{profile_id}").replace("/", "\\")
    da_xong = (ROOT / "FlowHandoff_local" / "results" / "video_render" / kenh / slug / "final.mp4").exists()
    # 21/10 tại chỗ (máy 2 A→Z): đứng ở h2dev\\pipeline của CHÍNH máy này, tập nằm sẵn trong slug_dir — không xcopy.
    cd_lenh = f"cd /d {HERE}" if o_cho else "cd shared\\buoc2_3_tool\\pipeline"
    tap_rel = str(job_dir) if o_cho else f"..\\{adir}\\{slug}"
    _pub = prof.get("publish") or {}
    tra_hang = (Path(_pub["upload_dir"]) / kenh / slug if o_cho and _pub.get("upload_dir")
                else ROOT / "FlowHandoff_local" / "results" / "video_render" / kenh / slug)
    da_xong = da_xong or (tra_hang / "final.mp4").exists()
    chep = [] if o_cho else [f"xcopy /E /I ..\\..\\..\\jobs\\{tab}\\{slug} ..\\{adir}\\{slug}"]
    lenh_may2 = []        # 2026-10-03: các dòng lệnh chính, chép lên cột K cho anh đưa máy 2
    if da_xong:
        khoi_lenh = (
            "## ⚠️ TẬP NÀY ĐÃ CÓ final.mp4 (chặng A+B đã xong) — ĐỪNG chạy lại make_video.py\n"
            "Đóng gói lại lần này CHỈ để thêm hook/ (xem mục HOOK bên dưới). KHÔNG có việc gì khác\n"
            "cần chạy ở đây — giọng/ảnh/video giữ nguyên bản đã giao trước.\n\n")
    else:
        _img_flow = (prof.get("image") or {}).get("flow_tool", True)
        _dung_flow_tool = _img_flow and n > 0
        if _dung_flow_tool:
            lenh_may2 = [cd_lenh] + chep + [
                         f"py -3.13 make_video.py --profile {profile_id} --slug {slug} --redo-voice --den B4Q"]
            khoi_lenh = (
                "## CHẶNG 1 — LỒNG TIẾNG (DỪNG TRƯỚC khi vẽ ảnh)\n"
                + "\n".join(lenh_may2) + "\n\n"
                "Lệnh này CHỈ lồng tiếng → nắn phụ đề theo kịch bản rồi DỪNG "
                "(KHÔNG vẽ ảnh, KHÔNG dựng video).\n"
                "B0–B3 (kịch bản) máy 1 đã xong và đã khoá sha256.\n"
                + ("GIỌNG ĐA VAI: lane này lồng tiếng bằng VOICEVOX engine (0đ, KHÔNG dùng ai33). "
                   "Máy 2 cài 1 lần theo shared\\GIAO_VIEC_MAY2_CAI_VOICEVOX.md; B4 tự đọc vai.txt. "
                   "Mô tả video PHẢI chép credits_giong.txt (▼素材).\n"
                   if (prof.get("voice") or {}).get("provider") == "voicevox" else "")
                + ("GIỌNG ĐA VAI: lane này lồng tiếng ĐA GIỌNG bằng ai33 (mỗi câu 1 task, "
                   "cần AI33_API_KEY như mọi lane). B4 tự đọc vai.txt + characters.json; "
                   "hết credit là B4 DỪNG trước khi gửi (không lồng tiếng cụt).\n"
                   if (prof.get("voice") or {}).get("provider") == "ai33" else "")
                + "\n"
                + f"## CHẶNG 2 — VẼ {n} ẢNH BẰNG FLOW TOOL (Google Flow > Create Tool, 0đ)\n"
                + ("Ảnh master đã vẽ sẵn + QC (_ref/, _ref2/) — KHÔNG vẽ lại, chỉ vẽ ảnh còn thiếu.\n"
                   if ref_masters else "")
                + ("KHOÁ MẶT THEO ID: mỗi thư mục _ref_<id>\\001.png = 1 nhân vật. Trong Flow Tool "
                   "KHÔNG dùng tính năng Character của Flow — dùng Ô ẢNH THAM CHIẾU "
                   "(≤ 5 ô/project, tên ô = id viết HOA, do don_flow_tool.py tự tính theo TỪNG LÔ). "
                   "Dòng prompt dùng `@CAST:id1,id2 <mô tả>` (id lấy trong characters.json), "
                   "don_flow_tool.py tự đọc — KHÔNG tự tạo Character.\n"
                   "1 tập có nhiều nhân vật hơn 5 thì phải chia nhiều LÔ (--dong), "
                   "mỗi lô ≤ 5 nhân vật xuất hiện trong lô đó — vượt là "
                   "don_flow_tool.py tự dừng và in danh sách id, tách --dong nhỏ hơn là xong.\n"
                   if cast_lane else "")
                + (f"py -3.13 don_flow_tool.py --job {tap_rel} --dong <lô> --ten {slug}-lo<k> [--kiem]\n"
                   "py -3.14 chay_flow_tool.py --bo3 \"<thư mục bộ 3 của lô>\" --port <cổng lấy từ sổ cổng>\n"
                   f"py -3.13 nghiemthu_flow_tool.py <zip> --bo3 \"<bộ 3>\" --giao \"{tap_rel}\\img\"\n"
                   f"→ lặp lại cho từng lô, đếm đủ {n} ảnh NNN trong img\\ mới sang CHẶNG 3\n\n")
                + f"gpti2 chỉ là dự phòng khi Flow Tool hỏng (≈ {cost:,}đ). Báo lại cách đã dùng + "
                  "số tiền THẬT đã tiêu nếu phải sa về gpti2.\n\n"
                + "## CHẶNG 3 — DỰNG + GIAO\n"
                + f"py -3.13 make_video.py --profile {profile_id} --slug {slug} --dry-run   ← PHẢI in B5 = 0 ảnh cần vẽ / 0đ "
                  f"(đủ {n} ảnh NNN trong img\\ rồi)\n"
                + f"py -3.13 make_video.py --profile {profile_id} --slug {slug}\n\n"
            )
        else:
            lenh_may2 = [cd_lenh] + chep + [
                         f"py -3.13 make_video.py --profile {profile_id} --slug {slug} --redo-voice"]
            khoi_lenh = (
                "## MỘT LỆNH DUY NHẤT (lane này không dùng Flow Tool — xem image.flow_tool trong profile)\n"
                + "\n".join(lenh_may2) + "\n\n"
                "Lệnh này tự làm: lồng tiếng → nắn phụ đề theo kịch bản"
                + (f" → vẽ {n} ảnh" if n > 0 else "") + " → dựng final.mp4.\n"
                "B0–B3 (kịch bản) máy 1 đã xong và đã khoá sha256.\n\n"
                + (f"## ẢNH: {n} tấm ({n_face} khoá mặt + {n_scene} cảnh vật)\n" if n > 0 else "")
                + (f"Ảnh master đã vẽ sẵn + QC (_ref/, _ref2/) — KHÔNG vẽ lại.\n" if ref_masters else "")
            )
    # Lane L 2026-09-25: assemble.hook_tu_ghep \u2192 B8 t\u1ef1 gh\u00e9p hook (m\u1ed1c t\u00ednh l\u1ea1i theo c\u00e2u t\u1eeb gi\u1ecdng th\u00e2n m\u00e1y 2 l\u1ed3ng)
    tu_ghep = bool((prof.get("assemble") or {}).get("hook_tu_ghep")) and (job_dir / "hook" / "hook_timeline.json").exists()
    khoi_tu_ghep = (
        f"## HOOK \u2014 M\u00c1Y 1 \u0110\u00c3 L\u00c0M XONG H\u00ccNH, make_video.py T\u1ef0 GH\u00c9P (KH\u00d4NG ch\u1ea1y gh\u00e9p tay)\n"
        f"hook\\ \u0111\u00e3 c\u00f3 \u0111\u1ee7: img\\ \u00b7 clip\\ (clip Grok, QC PASS) \u00b7 sfx\\ \u00b7 hook_timeline.json (m\u1ed1c theo S\u1ed0 C\u00c2U).\n"
        f"KH\u00d4NG v\u1ebd \u1ea3nh, KH\u00d4NG sinh clip, KH\u00d4NG thay clip b\u1eb1ng \u1ea3nh t\u0129nh. Thi\u1ebfu g\u00ec \u2192 D\u1eeaNG, b\u00e1o m\u00e1y 1.\n"
        f"B8 t\u1ef1: d\u1ef1ng th\u00e2n \u2192 tr\u1ed9n SFX \u2192 t\u00ednh l\u1ea1i m\u1ed1c hook t\u1eeb voice_roles.json (gi\u1ecdng m\u00e1y 2 v\u1eeba l\u1ed3ng) \u2192 ph\u1ee7 clip hook\n"
        f"l\u00ean \u0111o\u1ea1n m\u1edf \u0111\u1ea7u (gi\u1eef ti\u1ebfng th\u00e2n) \u2192 B10 nghi\u1ec7m thu \u2192 B11 giao. \u0110\u1eebng ch\u1ea1y ghep_hook_noi_truoc.py b\u1eb1ng tay.\n"
        f"T\u1ef1 ki\u1ec3m: xem 40 gi\u00e2y \u0111\u1ea7u final.mp4 trong th\u01b0 m\u1ee5c tr\u1ea3 h\u00e0ng \u2014 clip hook c\u00f3 b\u00f3ng tho\u1ea1i, h\u00ecnh kh\u1edbp l\u1eddi, kh\u00f4ng khung \u0111en.\n"
        f"Xong ghi c\u1ed9t I (VIDEO) d\u00f2ng t\u1eadp n\u00e0y: Video done - {slug} + xu\u1ed1ng d\u00f2ng + \u0111\u01b0\u1eddng d\u1eabn th\u01b0 m\u1ee5c tr\u1ea3 h\u00e0ng.\n\n")
    # 2026-10-07 (anh chốt): chọn + duyệt số chuyển hẳn sang máy 2 (so_lieu_dong.py chạy ở bundle) để mọi tập
    # của lane bật mg.so_lieu_dong đi cùng một đường QC — máy 1 không sinh/duyệt, không chặn ở đây.
    import so_lieu_dong
    khoi_mg = (
        f"## SỐ LIỆU ĐỘNG (lane bật mg.so_lieu_dong) — LÀM SAU KHI ĐÃ CÓ final.mp4\n"
        f"Đọc shared\\motion_graphics\\HUONG_DAN_MAY2.md (cài skill motion_graphics 1 lần). Gọi Claude máy 2:\n"
        f"  \"Dùng skill motion_graphics, làm số liệu động cho tập {slug} lane {profile_id} theo "
        f"shared\\motion_graphics\\HUONG_DAN_MAY2.md mục 2 (bước 0 tự sinh + duyệt so_lieu_dong.json).\"\n"
        f"Chỉ hiện ĐÚNG các số trong so_lieu_dong.json đã duyệt, không thêm số. Trả thêm final_mg.mp4 + "
        f"mg_so_sanh_*.mp4 cạnh final.mp4 (final.mp4 GIỮ NGUYÊN).\n"
        + (f"CÓ mg_y_do.md (ý đồ motion giải thích máy 1 viết): làm thêm các mục trong đó theo skill motion_graphics "
           f"references/mg_giai_thich.md, cùng lượt ghép final_mg.mp4; cụm neo không còn trong script.txt thì bỏ mục, ghi lý do.\n"
           if (job_dir / "mg_y_do.md").exists() else "")
        + (f"CÓ the_ten_than.json (thẻ tên nhân vật ở THÂN bài, không đọc bằng lời): giọng đã tự nghỉ thêm sau câu neo; "
           f"chồng thẻ cùng kiểu thẻ hook của lane (pipeline\\the_ten_hook.py html_the) đúng câu neo, hiện suốt khoảng nghỉ, "
           f"không che mặt — làm cùng lượt final_mg.mp4.\n"
           if (job_dir / "the_ten_than.json").exists() else "")
        + "\n"
    ) if so_lieu_dong.bat(prof) else ""
    dau_bg = (
        f"# VI\u1ec6C D\u1ef0NG VIDEO (m\u00e1y 2 t\u1ef1 l\u00e0m A\u2192Z, 21/10) \u2014 {profile_id} / {slug}\n"
        f"Vi\u1ebft l\u00fac: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"K\u1ecbch b\u1ea3n + hook \u0111\u00e3 duy\u1ec7t xong NGAY TR\u00caN M\u00c1Y N\u00c0Y. Ch\u1ea1y t\u1ea1i ch\u1ed7 trong {HERE} \u2014 kh\u00f4ng xcopy, kh\u00f4ng bundle.\n"
        f"Quy tr\u00ecnh \u0111\u1ee7: {ROOT / 'docs' / 'MAY2_LAM_A_DEN_Z.md'}\n\n"
    ) if o_cho else (
        f"# \u0110\u01a0N GIAO VI\u1ec6C M\u00c1Y 2 \u2014 {profile_id} / {slug}\n"
        f"\u0110\u00f3ng g\u00f3i l\u00fac: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"\u0110\u1eccC TR\u01af\u1edaC: shared\\QUY_TRINH_GIAO_VIEC_MAY2.md (ranh gi\u1edbi m\u00e1y 1 / m\u00e1y 2, 2 c\u1ed5ng b\u1eaft bu\u1ed9c)\n"
        f"M\u1ecdi \u0111\u01b0\u1eddng d\u1eabn d\u01b0\u1edbi \u0111\u00e2y T\u00cdNH T\u1eea th\u01b0 m\u1ee5c Syncthing `FlowHandoff_local\\` c\u1ee7a CH\u00cdNH M\u00c1Y B\u1ea0N\n"
        f"(m\u00e1y 1 \u0111\u1ec3 \u1edf h2dev\\FlowHandoff_local, m\u00e1y 2 \u1edf ch\u1ed7 kh\u00e1c \u2014 \u0111\u1eebng ch\u00e9p nguy\u00ean \u0111\u01b0\u1eddng d\u1eabn tuy\u1ec7t \u0111\u1ed1i c\u1ee7a nhau).\n\n")
    bg = (
        dau_bg
        + khoi_lenh
        + f"## HAI C\u1ed4NG KH\u00d4NG \u0110\u01af\u1ee2C T\u1eaeT\n"
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
        + (khoi_tu_ghep if tu_ghep else
           f"## HOOK\n"
           f"Lane n\u00e0y khai script.hook.visual = `{visual}`: hook l\u00e0 30 gi\u00e2y \u0110\u1ea6U c\u1ee7a ch\u00ednh script.txt,\n"
           f"l\u1ed3ng ti\u1ebfng v\u00e0 minh ho\u1ea1 chung M\u1ed8T L\u1ea6N v\u1edbi th\u00e2n video. G\u00f3i n\u00e0y C\u1ed0 \u00dd KH\u00d4NG c\u00f3 th\u01b0 m\u1ee5c hook\\\n"
           f"\u2014 \u0111\u1ec3 nguy\u00ean, \u0111\u1eebng d\u1ef1ng th\u00eam clip 30 gi\u00e2y n\u1eefa (s\u1ebd th\u00e0nh ph\u00e1t hai l\u1ea7n).\n\n"
           if visual == "lien_mach_than" else
           f"## HOOK — MÁY 1 ĐÃ LÀM XONG HÌNH, MÁY 2 CHỈ GHÉP\n"
            f"hook\\ đã có đủ: img\\ (ảnh) · clip\\ (clip Grok, QC PASS) · sfx\\ · hook_voice.mp3 · hook_timeline.json.\n"
            f"KHÔNG vẽ ảnh, KHÔNG sinh clip, KHÔNG thay clip bằng ảnh tĩnh. Thiếu gì → DỪNG, báo máy 1.\n"
            + (f"1. Chép nguyên thư mục hook\\ sang CẠNH final.mp4 (chỗ trả hàng thân video):\n"
               f"   xcopy /E /I /Y {job_dir}\\hook {tra_hang}\\hook\n"
               f"2. Chạy tại chỗ:\n"
               f"   {cd_lenh}\n"
               f"   py -3.13 ghep_hook_noi_truoc.py --tap {tra_hang} --profile {profile_id}\n"
               if o_cho else
               f"1. Chép nguyên thư mục hook\\ sang CẠNH final.mp4 (chỗ máy 2 đã trả hàng thân video):\n"
               f"   xcopy /E /I /Y FlowHandoff_local\\jobs\\{tab}\\{slug}\\hook FlowHandoff_local\\results\\video_render\\{kenh}\\{slug}\\hook\n"
               f"2. Chạy TỪ CÂY BUNDLE (không phải h2dev\\pipeline):\n"
               f"   cd FlowHandoff_local\\shared\\buoc2_3_tool\\pipeline\n"
               f"   py -3.13 ghep_hook_noi_truoc.py --tap ..\\..\\..\\results\\video_render\\{kenh}\\{slug} --profile {profile_id}\n")
            +
            f"   → final_with_hook.mp4 + phude_with_hook.srt, tự khớp khổ/fps/mức tiếng, nối không khung đen,\n"
            f"     hộp chữ dọc cho đoạn hook nếu lane bật assemble.tate. final.mp4 + phude.srt cũ GIỮ NGUYÊN.\n"
            f"3. Tự kiểm: công cụ in độ dài = hook + thân (lệch > 0,5s là nó tự DỪNG) và mức tiếng đoạn hook ≈ thân.\n"
            f"   Xem 40 giây đầu final_with_hook.mp4: hình hook có hộp chữ dọc bên trái giống thân, không khung đen ở điểm nối.\n"
            f"4. Xong ghi cột I (VIDEO) dòng tập này: Video+hook done - {slug} + xuống dòng + đường dẫn thư mục.\n\n"
            if (job_dir / "hook" / "clip").is_dir() and any((job_dir / "hook" / "clip").glob("clip_*.mp4")) else
           f"## HOOK\nLane khai script.hook.visual = `{visual}`: hook l\u00e0 CLIP RI\u00caNG, \u0111\u01a1n v\u1ebd \u1edf hook\\.\n"
           f"D\u1ef1ng xong n\u1ed1i v\u00e0o TR\u01af\u1edaC final.mp4 \u2192 final_with_hook.mp4, qua 4 ph\u00e9p ki\u1ec3m \u1edf\n"
           f"shared\\QUY_TAC_VIDEO_HOOK.md \u00a72 (m\u1ee9c ti\u1ebfng \u00b7 fps \u00b7 ki\u1ec3u ph\u1ee5 \u0111\u1ec1 \u00b7 \u0111i\u1ec3m n\u1ed1i).\n\n"
           if visual else "")
        + khoi_mg
        + f"## TR\u1ea2 H\u00c0NG\n"
        + (f"\u0110\u00daNG 2 VIDEO (anh ch\u1ed1t 2026-09-25): final.mp4 = b\u1ea3n \u0110\u0102NG, \u0110\u00c3 C\u00d3 HOOK (100% video giao b\u1eaft bu\u1ed9c c\u00f3 hook\n"
           f"n\u00ean KH\u00d4NG c\u00f2n file t\u00ean final_with_hook) + final-vietsub.mp4 = c\u00f9ng video, ch\u00e1y ph\u1ee5 \u0111\u1ec1 TI\u1ebeNG VI\u1ec6T cho anh \u0111\u1ecdc.\n"
           f"B11 t\u1ef1 \u0111\u1eb7t t\u00ean + ch\u00e9p c\u1ea3 hai (k\u00e8m phude.srt, tomtat.txt). Th\u1ea5y file t\u00ean *with_hook* trong th\u01b0 m\u1ee5c tr\u1ea3 h\u00e0ng = SAI.\n"
           if tu_ghep else "")
        + (f"{tra_hang}\\ \u2014 \u0111\u00fang ch\u1ed7 giao_hang.py (B11) t\u1ef1 ghi theo publish.upload_dir/upload_channel c\u1ee7a profile.\n"
           if o_cho else "")
        + ("" if o_cho else
        f"results\\video_render\\{kenh}\\{slug}\\ \u2014 \u0111\u00fang \u0111\u01b0\u1eddng gi\u00e1o_hang.py t\u1ef1 ghi (theo publish.upload_channel\n"
        f"= `{kenh}`, KH\u00d4NG ph\u1ea3i t\u00ean tab sheet `{tab}` \u2014 2 c\u00e1i kh\u00e1c nhau, \u0111\u1eebng nh\u1ea7m; \u0111\u00e3 verify th\u1eadt\n"
        f"tr\u00ean 3 t\u1eadp Lane F 2026-09-24). Syncthing t\u1ef1 mang v\u1ec1 m\u00e1y 1.\n")
    )
    (dst / "_BANGIAO.txt").write_text(bg, encoding="utf-8")
    print(f"✓ đóng gói {dst} ({n_copied} file + logs/) · {n} ảnh ≈ {cost:,}đ")
    if n_hook:
        print(f"  ✓ hook/: {n_hook} file đã đóng gói + đối chiếu khớp kích thước "
              f"(máy 1 làm hình hook, máy 2 CHỈ GHÉP — docs/QUY_TAC_VIDEO_HOOK.md §0)")

    try:
        _ghi_sheet_h(prof, slug, n, cost)
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột H: {e}")

    # 2026-10-19 (anh chốt): tập nào chạy kịch bản thì link VIDEO GỐC phải nằm ở CỘT T của tab lane.
    # B2 đã ghi rồi (video_goc.ghi_video_goc), đây là lần ghi lại lúc đóng gói — idempotent (ô đã
    # đúng link thì thôi), phòng trường hợp tập cũ chưa qua B2 mới. Lỗi KHÔNG chặn giao hàng.
    try:
        import ghi_cot_video_goc
        r = ghi_cot_video_goc.ghi_tu_ep(job_dir)
        print(f"  cột T (video gốc): {r['ly_do']}")
    except Exception as e:
        print(f"  ⚠️ chưa ghi được cột T (video gốc): {type(e).__name__} {e}")

    # 2026-10-01 (anh chốt): giao máy 2 xong thì ĐỒNG THỜI viết file hướng dẫn cho tab mới làm tập kế
    # (<slug_dir>\HUONG_DAN_TAP_TIEP_THEO.md) + ghi đè cột K (GHI CHÚ) dòng tập kế. Lỗi ở đây không chặn giao hàng.
    try:
        import huong_dan_tab_moi
        huong_dan_tab_moi.an_toan("tiep", prof, slug)
    except ImportError as e:
        print(f"  ⚠️ thiếu huong_dan_tab_moi.py — CHƯA viết hướng dẫn tập kế: {e}")

    # 2026-10-03 (anh chốt, mọi lane): cột K DÒNG TẬP NÀY = câu lệnh + đường dẫn để anh đưa sang máy 2.
    try:
        import review_may3
        review_may3.ghi_k(prof, slug, _k_giao_may2(dst, tab, slug, lenh_may2, prof))
    except Exception as e:
        print(f"  ⚠️ chưa ghi được cột K (lệnh máy 2): {e}")
    import tong_hop
    tong_hop.ghi(prof, slug, tong_hop.GIAO_MAY2)

    # 2026-09-24 (anh chốt): giao máy 2 xong thì TỰ gọi dự án YT-TITLE-RESEARCH viết tiêu đề/mô
    # tả/tags/thumbnail cho ĐÚNG lane — không cần anh gõ tay. Chạy NỀN (không chặn lệnh này); lane
    # chưa đủ điều kiện (thiếu cấu hình TITLE, chưa bật listing_external...) thì goi_title.py tự
    # DỪNG và in rõ lý do, KHÔNG chặn việc đóng gói giao máy 2 ở trên (đã xong rồi).
    # 2026-09-24 (YT-TITLE-RESEARCH yêu cầu): bước deliver bên đó dò thư mục CHANEL\<kênh>\<slug>\ và KHÔNG
    # tự tạo — thiếu là dừng cả chuỗi (Lane E ep03). Máy 1 tạo sẵn thư mục RỖNG (không chép video vào đây).
    pub = prof.get("publish") or {}
    if pub.get("listing_external") and pub.get("upload_dir") and Path(pub["upload_dir"]).is_absolute():
        ch = Path(pub["upload_dir"]) / pub.get("upload_channel", profile_id) / slug
        ch.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ thư mục giao TITLE: {ch}")

    if not no_title:
        try:
            import goi_title
            goi_title.goi(str(job_dir), profile_id)
        except Exception as e:
            print(f"  ⚠️ goi_title lỗi khi bắn nền TITLE: {e}")

    print(f"\nĐưa đường dẫn này cho anh bàn giao máy 2:\n  {dst}")
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", action="store_true", help="copy toàn bộ pipeline/ + profile vào FlowHandoff_local/shared/buoc2_3_tool/")
    ap.add_argument("--profile-list", nargs="*", default=None,
                    help="chỉ dùng với --bundle: danh sách profile id đưa vào bundle "
                         "(mặc định teinengo-real teinengo-tanoshimi)")
    ap.add_argument("--job", nargs=2, metavar=("PROFILE", "SLUG"), help="đóng gói 1 tập")
    ap.add_argument("--no-title", action="store_true",
                    help="không tự bắn nền dự án YT-TITLE-RESEARCH sau khi đóng gói xong")
    a = ap.parse_args()
    if a.bundle:
        cmd_bundle(a.profile_list or ["teinengo-real", "teinengo-tanoshimi"])
    elif a.job:
        cmd_job(a.job[0], a.job[1], no_title=a.no_title)
    else:
        ap.error("cần --bundle hoặc --job PROFILE SLUG")


if __name__ == "__main__":
    main()
