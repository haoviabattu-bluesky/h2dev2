r"""drive_handoff.py — chuyen file qua Google Drive giua may 1 (viet kich ban) va may 2 (sinh anh Flow).
Dung CHUNG 1 file nay tren CA HAI may — chi khac o cach goi (upload tren may 1, download tren may 2, nguoc lai
khi tra ket qua). Doc token tu D:\CLAUDE\credentials\{credentials.json,token.json} — 2 file nay phai duoc copy
sang CUNG DUONG DAN do tren may 2 (hoac sua CRED_DIR ben duoi).

Cau truc Drive da tao san (tai khoan haoviabattu@gmail.com):
  FlowHandoff/
    jobs/     <- may 1 up ho so (img_prompts.txt, characters.json, _ref/...) vao day, theo tung slug rieng
    results/  <- may 2 up anh + manifest.json ket qua vao day, theo tung slug rieng
    shared/   <- MOI THU DUNG CHUNG khong rieng 1 job nao (skill veo3_flow_automation.md, chinh file nay...)
               KHONG chia theo slug — chi 1 kho phang, luon lay ban MOI NHAT o day.

Quy uoc: bat ky file/kien thuc nao can cho MAY 2 (khong rieng 1 job) THI LUON up vao shared/ ngay khi co
ban moi — dung doi may 2 hoi hay dung gui rieng qua kenh khac. May 2 luon `download-shared` truoc moi lan
bat dau job moi de chac chan dung ban moi nhat.

===============================================================================================
BA LOI CAM DA SUA 2026-09-11 (deu thuoc loai "nhin thi tuong xong, thuc te thieu"):

 1. KHONG PHAN TRANG. `files().list()` cua Drive API mac dinh tra TOI DA 100 file va khong bao gi
    ca. Job Loai B `ep01-valentich` co 308 anh => `download-result` chi lay ve 100 tam, may 1 ghep
    video voi 208 canh thieu anh ma khong buoc nao keu. Nay moi cho liet ke deu chay het pageToken.

 2. KHONG DE QUY THU MUC CON. Ban cu co dong `if not f.is_file(): continue` => `_ref/001.png` va
    `_ref_<ten>/001.png` (anh master REF-LOCK, BAT BUOC theo docs/GIAO_VIEC_MAY2_ANH.md muc 2)
    KHONG BAO GIO len duoc Drive. Job Loai A duy nhat chay duoc truoc day (`simbot2-11-test7`) la
    do co nguoi lam phang bang tay. Nay upload/download deu di het cay thu muc.

 3. DUT GIUA CHUNG VAN COI NHU XONG. Mot lan timeout mang lam job chi len duoc 6/9 file, thu muc
    van hien ra trong `list-jobs` nhu binh thuong. Nay: moi thao tac mang co thu lai co backoff, va
    co lenh `verify-job` doi chieu Drive voi local — CHUA verify thi CHUA duoc ghi cot STATUS-IMG.
===============================================================================================

Dung:
  py -3.13 drive_handoff.py upload-job <slug> <thu_muc_ho_so_local>
  py -3.13 drive_handoff.py verify-job <slug> <thu_muc_ho_so_local>   (exit 1 neu thieu — chay TRUOC khi ghi cot F)
  py -3.13 drive_handoff.py download-job <slug> <thu_muc_dich_local>
  py -3.13 drive_handoff.py upload-result <slug> <thu_muc_img_local>
  py -3.13 drive_handoff.py verify-result <slug> <thu_muc_img_local>
  py -3.13 drive_handoff.py download-result <slug> <thu_muc_dich_local>
  py -3.13 drive_handoff.py clean-job <slug>
      (XOA VINH VIEN jobs/<slug> + results/<slug> khoi Drive — không qua thùng rác.
       Chỉ chạy sau khi may 1 da tai du anh ve dia (bước D đạt) — xem quy tắc dưới.)
  py -3.13 drive_handoff.py upload-shared <thu_muc_local>      (up TAT CA file trong thu muc vao shared/)
  py -3.13 drive_handoff.py download-shared <thu_muc_dich_local>
  py -3.13 drive_handoff.py list-jobs | list-results | list-shared
"""

"""
QUY TAC DON DRIVE (user chot 2026-09-14): Drive chỉ là trung gian, KHÔNG phải kho lưu trữ. Ảnh
máy 2 up lên `results/<slug>/` (mỗi tập ~1 GB = 300 ảnh x 3MB) phải được XÓA VĨNH VIỄN ngay sau
khi máy 1 đã tải về + đếm đủ (bước D đạt trong chay_buoc3.py). TUYỆT ĐỐI không để ảnh nằm lại
trên Drive — quota 16 GB sẽ cạn sau ~2 tập. Lệnh clean-job xoá cả jobs/<slug> lẫn results/<slug>
(job xong nghĩa là máy 2 đã có local + máy 1 đã có ảnh — xoá trên Drive không mất gì).
chay_buoc3.py có sẵn bước D+ gọi lệnh này tự động; chạy tay khi cần dọn lại (v.d. tập cũ từ
trước quy tắc này).
"""
import json
import os
import sys
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CRED_DIR = r"D:\CLAUDE\credentials"
TOKEN_FILE = os.path.join(CRED_DIR, "token.json")
ROOT_FOLDER_NAME = "FlowHandoff"
FOLDER_MIME = "application/vnd.google-apps.folder"

# File chi co y nghia tren may 1 (ban nhap/sao luu) — khong gui sang may 2 cho roi.
# Danh sach CO Y de NGAN va chi gom ban sao luu: loc manh tay de sot file lane khac can thi
# lai dung kieu loi cam dang muon diet.
BO_QUA = (".bak", ".pre_fix.txt", ".truoc_khi_sua_2loi")

# PHIM VA TIENG KHONG BAO GIO LA HO SO GIAO VIEC. Job sinh anh chi can chu (prompt/meta/bible) va
# anh master .png — may 2 khong mo file video/audio nao ca.
# Vi sao phai chan bang code: `upload-job <slug> <thu muc>` de quy CA CAY, nen tro no vao thu muc
# TAP (thay vi thu muc trung chuyen) la no bat dau day ca kho clip stock len Drive, khong hoi gi.
# Da dinh that 2026-09-12 voi ep02-walton: 618 MB clip da len Drive truoc khi kip dung tay; job
# ep01-valentich lam dung thi tren Drive chi co 0,3 MB. Loi nay CAM LANG — nhin log chi thay
# "dang upload", va may 2 se phai tai ve ca dong clip no khong dung toi.
# `liet_ke_local()` dung chung ham nay nen `verify-job` cung bo qua y het => khong bao thieu oan.
BO_QUA_DUOI = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v",
               ".mp3", ".wav", ".m4a", ".aac", ".flac")


def bo_qua(ten):
    t = ten.lower()
    return (any(t.endswith(x) for x in BO_QUA) or ".truoc_khi_" in t
            or any(t.endswith(x) for x in BO_QUA_DUOI))


def thu_lai(fn, mo_ta, lan=4):
    """Chay fn(), thu lai co backoff khi loi MANG tam thoi (timeout/5xx).

    Vi sao can: mot lan `TimeoutError: The read operation timed out` giua chung lam job chi len
    duoc 6/9 file, ma thu muc van hien binh thuong trong list-jobs => may 2 tai ve job hong."""
    cho = 5
    for i in range(1, lan + 1):
        try:
            return fn()
        except Exception as e:
            tam = any(k in f"{type(e).__name__} {e}".lower()
                      for k in ("timeout", "timed out", "ssl", "connection", "broken pipe",
                                "503", "500", "429", "rate limit", "backenderror"))
            if not tam or i == lan:
                raise
            print(f"     ! {mo_ta}: {type(e).__name__} — thu lai sau {cho}s [{i}/{lan - 1}]")
            time.sleep(cho)
            cho *= 2


def get_drive():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        Path(TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=creds)


def liet_ke(drive, parent_id):
    """TAT CA muc con cua parent_id — CO PHAN TRANG (mac dinh API chi tra 100, khong canh bao)."""
    ra, token = [], None
    while True:
        res = thu_lai(lambda: drive.files().list(
            q=f"'{parent_id}' in parents and trashed=false",
            fields="nextPageToken, files(id,name,mimeType,size)",
            pageSize=1000, pageToken=token).execute(), "liet ke")
        ra += res.get("files", [])
        token = res.get("nextPageToken")
        if not token:
            return ra


def find_folder(drive, name, parent_id=None):
    q = f"name='{name}' and mimeType='{FOLDER_MIME}' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    res = thu_lai(lambda: drive.files().list(q=q, fields="files(id,name)").execute(), "tim thu muc")
    files = res.get("files", [])
    return files[0]["id"] if files else None


def find_or_create_folder(drive, name, parent_id=None):
    fid = find_folder(drive, name, parent_id)
    if fid:
        return fid
    meta = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        meta["parents"] = [parent_id]
    return thu_lai(lambda: drive.files().create(body=meta, fields="id").execute(), "tao thu muc")["id"]


def up_mot_file(drive, f, parent_id, ten=None):
    ten = ten or f.name
    for o in [x for x in liet_ke(drive, parent_id) if x["name"] == ten]:
        thu_lai(lambda: drive.files().delete(fileId=o["id"]).execute(), "xoa ban cu")
    thu_lai(lambda: drive.files().create(
        body={"name": ten, "parents": [parent_id]},
        media_body=MediaFileUpload(str(f), resumable=True), fields="id").execute(), f"up {ten}")
    print(f"  up: {ten} ({f.stat().st_size:,} bytes)")


def upload_folder_contents(drive, local_dir, parent_id, tien_to=""):
    """Up toan bo local_dir vao parent_id, DE QUY ca thu muc con (tao thu muc tuong ung tren Drive).

    Ban cu bo qua thu muc con nen anh master `_ref/001.png` khong bao gio len duoc — xem muc 2 o
    dau file."""
    local_dir = Path(local_dir)
    uploaded = []
    for f in sorted(local_dir.iterdir()):
        if f.is_dir():
            con = find_or_create_folder(drive, f.name, parent_id)
            uploaded += upload_folder_contents(drive, f, con, tien_to + f.name + "/")
        elif f.is_file() and not bo_qua(f.name):
            up_mot_file(drive, f, parent_id)
            uploaded.append(tien_to + f.name)
    return uploaded


def download_folder_contents(drive, remote_folder_id, local_dir, tien_to=""):
    """Tai ve, DE QUY, dung lai cay thu muc nhu tren Drive."""
    local_dir = Path(local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)
    ra = []
    for f in liet_ke(drive, remote_folder_id):
        if f["mimeType"] == FOLDER_MIME:
            ra += download_folder_contents(drive, f["id"], local_dir / f["name"], tien_to + f["name"] + "/")
            continue
        dest = local_dir / f["name"]

        def tai():
            with open(dest, "wb") as fh:
                dl = MediaIoBaseDownload(fh, drive.files().get_media(fileId=f["id"]))
                done = False
                while not done:
                    _, done = dl.next_chunk()
        thu_lai(tai, f"tai {f['name']}")
        print(f"  tai: {tien_to}{f['name']} -> {dest}")
        ra.append(tien_to + f["name"])
    return ra


def xoa_cay(drive, folder_id):
    """Xoá VĨNH VIỄN toàn bộ cây thư mục trên Drive (không qua thùng rác).

    Dùng cho clean-job: ảnh đã tải về + đếm đủ thì không để lại trên Drive nữa
    (user chốt 2026-09-14 — Drive là trung gian, không phải kho lưu trữ)."""
    dem = 0
    for f in liet_ke(drive, folder_id):
        if f["mimeType"] == FOLDER_MIME:
            dem += xoa_cay(drive, f["id"])
        else:
            thu_lai(lambda: drive.files().delete(fileId=f["id"]).execute(), f"xoa {f['name']}")
            dem += 1
    thu_lai(lambda: drive.files().delete(fileId=folder_id).execute(), "xoa thu muc goc")
    return dem + 1


# =======================================================================
# CHE DO LOCAL-FIRST (user chot 2026-09-14): kiem tra /CAU/ khi co FlowHandoff_local
# (thu muc dong bo qua Syncthing) thi toan bo lenh doc/ghi LOCAL, KHONG dung Drive.
# Drive chi la fallback: (a) khong co FlowHandoff_local, hoac (b) env HANDOFF_DRIVE=1.
# Cau truc giong Drive:  <goc>/jobs/<slug>  <goc>/results/<slug>  <goc>/shared
# =======================================================================
import shutil

CANDIDATE_GOC = [
    r"E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local",   # may 1
    r"E:\CLAUDE\YOUTUBE\FlowHandoff_local",          # may 2 (cung ten, khac goc)
]


def goc_local():
    """Tra Path goc FlowHandoff_local neu co (env HANDOFF_GOC override), nguoc lai None."""
    env = os.environ.get("HANDOFF_GOC", "").strip()
    if env:
        p = Path(env)
        return p if p.exists() else None
    for cand in CANDIDATE_GOC:
        p = Path(cand)
        if (p / "jobs").exists() or p.exists():
            return p
    return None


def dung_local():
    """True = chay che do local (co FlowHandoff_local + khong bi ep dung Drive)."""
    if os.environ.get("HANDOFF_DRIVE") == "1":
        return False
    return goc_local() is not None


def chay_local(cmd, goc):
    """Thuc thi lenh trong che do LOCAL. Tra ve exit code."""
    jobs = goc / "jobs"
    results = goc / "results"
    shared = goc / "shared"
    for d in (jobs, results, shared):
        d.mkdir(parents=True, exist_ok=True)

    def copy_cay(src, dst):
        """Copy toan bo cay src -> dst, bo file theo BO_QUA/BO_QUA_DUOI (nhu Drive)."""
        src = Path(src)
        dst = Path(dst)
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            for child in sorted(src.iterdir()):
                copy_cay(child, dst / child.name)
        elif src.is_file() and not bo_qua(src.name):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    if cmd == "upload-job":
        slug, local_dir = sys.argv[2], sys.argv[3]
        phang = phang_master(local_dir)
        viet_ban_giao(local_dir, slug, phang)
        dst = jobs / slug
        print(f"Chuyen ho so '{slug}' -> FlowHandoff_local/jobs/{slug}/ (Syncthing tu dong gui may 2)")
        copy_cay(local_dir, dst)
        for ten, p in phang:
            shutil.copy2(p, dst / ten)
        return 0 if doi_chieu_local(dst, local_dir, f"job '{slug}'") else 1

    elif cmd == "verify-job":
        slug, local_dir = sys.argv[2], sys.argv[3]
        d = jobs / slug
        if not d.exists():
            print(f"Khong thay job '{slug}' trong FlowHandoff_local/jobs/")
            return 1
        return 0 if doi_chieu_local(d, local_dir, f"job '{slug}'") else 1

    elif cmd == "download-job":
        slug, dest_dir = sys.argv[2], sys.argv[3]
        d = jobs / slug
        if not d.exists():
            print(f"Khong thay job '{slug}' trong FlowHandoff_local/jobs/")
            return 1
        print(f"Lay ho so '{slug}' -> {dest_dir}")
        copy_cay(d, dest_dir)

    elif cmd == "upload-result":
        slug, local_dir = sys.argv[2], sys.argv[3]
        dst = results / slug
        print(f"Chuyen ket qua '{slug}' -> FlowHandoff_local/results/{slug}/ (Syncthing tu dong gui may 1)")
        copy_cay(local_dir, dst)
        return 0 if doi_chieu_local(dst, local_dir, f"ket qua '{slug}'") else 1

    elif cmd == "verify-result":
        slug, local_dir = sys.argv[2], sys.argv[3]
        d = results / slug
        if not d.exists():
            print(f"Khong thay ket qua '{slug}' trong FlowHandoff_local/results/")
            return 1
        return 0 if doi_chieu_local(d, local_dir, f"ket qua '{slug}'") else 1

    elif cmd == "download-result":
        slug, dest_dir = sys.argv[2], sys.argv[3]
        d = results / slug
        if not d.exists():
            print(f"Khong thay ket qua '{slug}' trong FlowHandoff_local/results/")
            return 1
        print(f"Lay ket qua '{slug}' -> {dest_dir}")
        copy_cay(d, dest_dir)

    elif cmd == "clean-job":
        slug = sys.argv[2]
        # ⚠️ LOCAL MODE = NO-OP (sửa 2026-09-14 sau ca thật simbot2-01): KHÔNG xoá local.
        # Lý do: (1) local không tốn quota nên không cần dọn; (2) xoá trên folder receiveonly
        # (results của máy 1) tạo `localDeleted` → Syncthing coi là local changes → KHÔNG pull
        # file mới từ máy 2 (need=0 dù global > local), job kẹt âm thầm. Dọn thật chỉ có ý
        # nghĩa ở chế độ Drive cũ (HANDOFF_DRIVE=1) — nhánh đó vẫn xoá như trước.
        print(f"Don local jobs/{slug} + results/{slug}: BỎ QUA (local mode — không tốn quota, "
              f"không xoá để tránh kẹt sync receiveonly). Muốn dọn thật: HANDOFF_DRIVE=1 "
              f"drive_handoff.py clean-job {slug}")

    elif cmd == "upload-shared":
        local_dir = sys.argv[2]
        print(f"Chuyen file dung chung -> FlowHandoff_local/shared/ (Syncthing dong bo 2 chieu)")
        copy_cay(local_dir, shared)

    elif cmd == "download-shared":
        dest_dir = sys.argv[2]
        print(f"Lay file dung chung -> {dest_dir}")
        copy_cay(shared, dest_dir)

    elif cmd in ("list-jobs", "list-results", "list-shared"):
        goc_ngan = {"list-jobs": jobs, "list-results": results, "list-shared": shared}[cmd]
        for child in sorted(goc_ngan.iterdir()) if goc_ngan.exists() else []:
            dau = "[thu muc]" if child.is_dir() else "         "
            print(f" {dau} {child.name}")

    else:
        print(__doc__)
        return 0
    return 0


# 2026-09-23 (vá review HOOK, Việc 2): `cay_local()`/`cay_drive()` đệ quy MỌI thư mục con (không
# lọc theo tên thư mục, chỉ lọc theo đuôi file) nên `hook/` đã tự động nằm trong phép đối chiếu
# CÂY chung — không cần sửa 2 hàm đó. Cái còn THIẾU là một dòng KHẲNG ĐỊNH RIÊNG cho hook, đúng
# luật "vận chuyển phải tự chứng minh" của dự án (xem docstring đầu file, mục 3 — verify-job có
# rồi nhưng gộp chung vào danh sách thiếu dài, dễ đọc lướt qua đúng lúc thiếu đúng phần hook).
def _kiem_hook_trong_goi(duoi, thieu):
    """Lọc riêng phần `hook/` trong phép đối chiếu CÂY đã có ở doi_chieu_local()/doi_chieu(), in
    một dòng RÕ RÀNG thay vì để lẫn vào danh sách thiếu chung chung. Tập không có `hook/` ở nguồn
    (đa số tập, tính năng đang bật dần từng kênh) → không in gì, không báo lỗi gì cả."""
    hook_co = sorted(t for t in duoi if t == "hook" or t.startswith("hook/"))
    if not hook_co:
        return
    hook_thieu = [t for t in thieu if t == "hook" or t.startswith("hook/")]
    if hook_thieu:
        print(f"\n⚠️  RIÊNG hook/: THIẾU {len(hook_thieu)}/{len(hook_co)} file — máy 2 sẽ KHÔNG vẽ "
              f"được ảnh shot hook nếu gửi gói này:")
        for t in hook_thieu:
            print("   -", t)
    else:
        print(f"  ✓ hook/: {len(hook_co)} file đã đối chiếu khớp — máy 2 đủ đơn vẽ ảnh shot hook.")


def doi_chieu_local(remote_dir, local_dir, ten_goi="job"):
    """So cay LOCAL voi cay LOCAL (thay cho doi_chieu tren Drive)."""
    tren = set(cay_local(remote_dir))
    duoi = set(cay_local(local_dir))
    thieu = sorted(duoi - tren)
    them = sorted(tren - duoi)
    print(f"Local: {len(tren)} file · Nguon: {len(duoi)} file")
    for t in them:
        print(f"   + chi co trong thu muc dong bo (khong sao): {t}")
    _kiem_hook_trong_goi(duoi, thieu)
    if thieu:
        print(f"\n✗ THIEU {len(thieu)} file — {ten_goi} CHUA san sang:")
        for t in thieu:
            print("   -", t)
        return False
    print(f"\n✓ DAT — thu muc dong bo co du moi file cua {ten_goi}.")
    return True


def cay_local(local_dir, tien_to=""):
    """Danh sach duong dan tuong doi cua MOI file trong local_dir (da bo file bi BO_QUA)."""
    ra = []
    for f in sorted(Path(local_dir).iterdir()):
        if f.is_dir():
            ra += cay_local(f, tien_to + f.name + "/")
        elif f.is_file() and not bo_qua(f.name):
            ra.append(tien_to + f.name)
    return ra


def cay_drive(drive, folder_id, tien_to=""):
    ra = []
    for f in liet_ke(drive, folder_id):
        if f["mimeType"] == FOLDER_MIME:
            ra += cay_drive(drive, f["id"], tien_to + f["name"] + "/")
        else:
            ra.append(tien_to + f["name"])
    return ra


def doi_chieu(drive, folder_id, local_dir, ten_goi="job"):
    """So Drive voi local. exit 1 neu thieu — CHUA DAT thi CHUA duoc ghi cot STATUS-IMG.

    Co cong nay vi mot lan upload dut giua chung van de lai thu muc trong `list-jobs` y nhu da
    xong; khong doi chieu thi khong the biet."""
    tren = set(cay_drive(drive, folder_id))
    duoi = set(cay_local(local_dir))
    thieu = sorted(duoi - tren)
    them = sorted(tren - duoi)
    print(f"Drive: {len(tren)} file · Local: {len(duoi)} file")
    for t in them:
        print(f"   + chi co tren Drive (khong sao): {t}")
    _kiem_hook_trong_goi(duoi, thieu)
    if thieu:
        print(f"\n✗ THIEU {len(thieu)} file tren Drive — {ten_goi} CHUA san sang:")
        for t in thieu:
            print("   -", t)
        print("   → chay lai lenh upload roi verify lai. CHUA verify DAT thi CHUA ghi cot STATUS-IMG.")
        return False
    print(f"\n✓ DAT — Drive co du moi file cua {ten_goi}.")
    return True


def phang_master(local_dir):
    """[(ten_phang, Path)] cho anh master REF-LOCK, doc tu characters.json (Loai A).

    De THEM ban phang o goc job ben canh cay `_ref/...`: may 2 chay ban drive_handoff CU (khong de
    quy) van tim thay master, khoi phai cap nhat dong bo hai may moi chay duoc. ~4 MB/anh, khong
    dang so voi rui ro 121 anh sai mat."""
    cf = Path(local_dir) / "characters.json"
    if not cf.exists():
        return []
    try:
        chars = json.loads(cf.read_text(encoding="utf-8")).get("characters", [])
    except Exception:
        return []
    ra = []
    for i, c in enumerate(chars[:2]):
        m = c.get("master")
        if not m:
            continue
        p = Path(local_dir) / m
        if p.exists():
            mk = "REF" if i == 0 else "REF2"
            ra.append((f"{mk}_{c.get('name', 'nhanvat')}_master{p.suffix}", p))
    return ra


def viet_ban_giao(local_dir, slug, phang):
    """Ghi `_BANGIAO.txt` vao ho so: job tu mo ta minh, may 2 khong can doc chat cua may 1."""
    d = Path(local_dir)
    loai = "B (plain prompt, khong REF-LOCK)" if (d / "img_ai" / "prompts.txt").exists() else "A (REF-LOCK)"
    dong = []
    pf = d / "img_prompts.txt"
    if pf.exists():
        dong = [l for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
    doi = [i for i, l in enumerate(dong, 1) if l.upper().count("@REF") > 1]
    t = [f"BAN GIAO SINH ANH — {slug}", f"Loai job: {loai}", f"So dong prompt: {len(dong)}", ""]
    if phang:
        t += ["ANH MASTER (marker -> nhan vat -> file):"]
        for ten, p in phang:
            mk = ten.split("_")[0]
            t += [f"  @{mk} = {ten.split('_')[1]}  ->  {ten}   (ban trong cay: {p.parent.name}/{p.name})"]
        t += ["", "Tao Character tren Flow bang UPLOAD dung file tren, KHONG mo ta lai bang chu."]
    if doi:
        t += ["", f"CANH BAO — {len(doi)} canh CO HAI NHAN VAT tren mot dong (dong {', '.join(map(str, doi))}):",
              "  phai mention DU CA HAI Character, thieu mot cai la Flow bia nguoi la (skill §11.3c)."]
    t += ["", "Xong thi upload-result + ghi cot STATUS-IMG. Thieu/hong >=20% thi DUNG, ghi 'LOI:' (muc 5/6)."]
    (d / "_BANGIAO.txt").write_text("\n".join(t) + "\n", encoding="utf-8")
    return d / "_BANGIAO.txt"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]

    # CHE DO LOCAL-FIRST: co FlowHandoff_local thi chay local, khong can Drive/token
    goc = goc_local()
    if goc is not None and not os.environ.get("HANDOFF_DRIVE") == "1":
        print(f"(che do LOCAL — FlowHandoff_local: {goc})")
        return chay_local(cmd, goc)

    drive = get_drive()
    root_id, jobs_id, results_id, shared_id = None, None, None, None
    root_id = find_folder(drive, ROOT_FOLDER_NAME)
    if not root_id:
        raise RuntimeError(f"Khong thay thu muc {ROOT_FOLDER_NAME} tren Drive — chay tao truoc.")
    jobs_id = find_or_create_folder(drive, "jobs", root_id)
    results_id = find_or_create_folder(drive, "results", root_id)
    shared_id = find_or_create_folder(drive, "shared", root_id)

    if cmd == "upload-job":
        slug, local_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_or_create_folder(drive, slug, jobs_id)
        phang = phang_master(local_dir)
        viet_ban_giao(local_dir, slug, phang)
        print(f"Upload ho so '{slug}' -> FlowHandoff/jobs/{slug}/")
        upload_folder_contents(drive, local_dir, slug_folder)
        for ten, p in phang:      # ban phang o goc, cho may 2 chay ban cu (xem phang_master)
            up_mot_file(drive, p, slug_folder, ten)
        print()
        return 0 if doi_chieu(drive, slug_folder, local_dir, f"job '{slug}'") else 1

    elif cmd == "verify-job":
        slug, local_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_folder(drive, slug, jobs_id)
        if not slug_folder:
            print(f"Khong thay job '{slug}' trong jobs/")
            return 1
        return 0 if doi_chieu(drive, slug_folder, local_dir, f"job '{slug}'") else 1

    elif cmd == "download-job":
        slug, dest_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_folder(drive, slug, jobs_id)
        if not slug_folder:
            print(f"Khong thay job '{slug}' trong jobs/")
            return 1
        print(f"Tai ho so '{slug}' -> {dest_dir}")
        download_folder_contents(drive, slug_folder, dest_dir)

    elif cmd == "upload-result":
        slug, local_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_or_create_folder(drive, slug, results_id)
        print(f"Upload ket qua '{slug}' -> FlowHandoff/results/{slug}/")
        upload_folder_contents(drive, local_dir, slug_folder)
        print()
        return 0 if doi_chieu(drive, slug_folder, local_dir, f"ket qua '{slug}'") else 1

    elif cmd == "verify-result":
        slug, local_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_folder(drive, slug, results_id)
        if not slug_folder:
            print(f"Khong thay ket qua '{slug}' trong results/")
            return 1
        return 0 if doi_chieu(drive, slug_folder, local_dir, f"ket qua '{slug}'") else 1

    elif cmd == "download-result":
        slug, dest_dir = sys.argv[2], sys.argv[3]
        slug_folder = find_folder(drive, slug, results_id)
        if not slug_folder:
            print(f"Khong thay ket qua '{slug}' trong results/")
            return 1
        print(f"Tai ket qua '{slug}' -> {dest_dir}")
        download_folder_contents(drive, slug_folder, dest_dir)

    elif cmd == "clean-job":
        slug = sys.argv[2]
        print(f"XOA VINH VIEN jobs/{slug} + results/{slug} khoi Drive (khong qua thung rac)...")
        for ten_ngan, pid in (("jobs", jobs_id), ("results", results_id)):
            f = find_folder(drive, slug, pid)
            if not f:
                print(f"  {ten_ngan}/{slug}: khong ton tai — bo qua")
                continue
            dem = xoa_cay(drive, f)
            print(f"  ✓ da xoa {ten_ngan}/{slug}: {dem} muc")
        print("Xong — nho kiem tra lai bang list-jobs / list-results.")

    elif cmd == "upload-shared":
        local_dir = sys.argv[2]
        print("Upload file dung CHUNG (skill/tai lieu) -> FlowHandoff/shared/")
        upload_folder_contents(drive, local_dir, shared_id)

    elif cmd == "download-shared":
        dest_dir = sys.argv[2]
        print(f"Tai toan bo file dung chung -> {dest_dir}")
        download_folder_contents(drive, shared_id, dest_dir)

    elif cmd in ("list-jobs", "list-results", "list-shared"):
        pid = {"list-jobs": jobs_id, "list-results": results_id, "list-shared": shared_id}[cmd]
        for f in liet_ke(drive, pid):
            dau = "[thu muc]" if f["mimeType"] == FOLDER_MIME else "         "
            print(f" {dau} {f['name']}")

    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
