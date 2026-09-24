# -*- coding: utf-8 -*-
r"""goi_title.py — sau khi máy 1 giao 1 tập cho máy 2, TỰ gọi dự án YT-TITLE-RESEARCH viết
tiêu đề/mô tả/tags/thumbnail cho ĐÚNG lane của tập đó — anh không gõ tay nữa (anh chốt 2026-09-24).

VÌ SAO FILE NÀY TỒN TẠI
- Trước đây tiêu đề/mô tả/thumbnail do CHÍNH h2dev viết (B7/B9 trong make_video.py) — giờ giao HẲN
  cho dự án khác (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH), 2 dự án không được cùng ghi 1 file (đè nhau).
  Bật `publish.listing_external: true` trong profile lane là tắt B7/B9 phía h2dev — xem
  `docs/PHUONG_AN_TU_GOI_TITLE.md`.
- Dự án tự nhận LANE qua `id` profile h2dev (KHÔNG phải tên tab sheet — đổi tên được; KHÔNG phải
  upload_channel — không trùng id với satori). Hàm `_detect_lane()` dò `id` bằng cách so thư mục tập
  với `slug_dir` của MỌI profile, không suy đoán từ tên gọi.
- Cổng `_gates()` DỪNG rõ ràng khi lane thiếu cấu hình bên TITLE, thay vì để TITLE rơi về luật
  satori (`_default.json`) một cách im lặng.

CÔNG TẮC TỰ ĐỘNG THEO LANE — `publish.title_auto` (anh chốt 2026-09-24)
- Kênh MỚI mặc định TẮT: anh chạy setup TITLE tập đầu bằng tay (lane-init / lane-pilot / run), ưng rồi
  mới bật. Profile không có field này = TẮT → giao máy 2 xong chỉ in 1 dòng nhắc, không gọi TITLE.
- Bật/tắt: `py -3.13 goi_title.py --bat <lane>` / `--tat <lane>` (ghi đúng 1 field, giữ nguyên format).

NHỊP CHẠY (worker, phương án A 2026-09-24 — đo thật ep02 Lane F: nối đuôi ~35–45 phút)
  1. `run --no-thumb --no-tags --no-sol-check`  → tiêu đề + mô tả + deliver (~10 phút)
  2. `tags` ‖ `thumb`  CHẠY SONG SONG (không phụ thuộc nhau sau khi khoá tiêu đề) → bớt ~9 phút
  3. `sol-check` (cố vấn, lỗi không chặn) → `thumb-publish` (máy tự chọn) → `sheet-publish` → `view`
  Thumbnail kẹt "escalate" (Sol còn lỗi HIGH sau các vòng sửa chữ) = CHƯA có ảnh → DỪNG báo rõ, không
  ép publish. Bên TITLE có cờ `thumb --auto` (phương án B) thì worker tự truyền — cờ đó bỏ trạng thái
  dừng chờ người khi chạy tự động.

DÙNG:
  py -3.13 goi_title.py --slug <thư mục tập> [--profile <id>] [--dry] [--wait]   (3 đường giao tự gọi)
  py -3.13 goi_title.py --bat <lane> | --tat <lane> | --trang-thai
  py -3.13 goi_title.py --worker --slug <tập> --profile <id>                        (nội bộ, chạy nền)
Log sống: <tập>\research\TU_DONG_TITLE.log (+ .tags.log / .thumb.log) · trạng thái: TU_DONG_TITLE.json
"""
import argparse
import ctypes
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import profiles  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TITLE_ROOT = Path(r"E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH")
TITLE_CLI = TITLE_ROOT / "cli.py"
TITLE_CONFIG = TITLE_ROOT / "config" / "lanes"
PROFILE_DIR = ROOT / "profiles" / "profiles"


# ============================================================== nhận diện lane
def _detect_lane(job_dir: Path):
    """So job_dir với slug_dir của MỌI profile h2dev — trả (profile_id, prof) hoặc (None, None)."""
    job_dir = job_dir.resolve()
    for pid in profiles.list_ids():
        if pid.startswith("_"):
            continue
        try:
            p = profiles.load(pid)
        except Exception:
            continue
        sd = p.get("slug_dir") or ""
        if not sd:
            continue
        sd_abs = (ROOT / sd).resolve() if not Path(sd).is_absolute() else Path(sd).resolve()
        try:
            job_dir.relative_to(sd_abs)
        except ValueError:
            continue
        return pid, p
    return None, None


# ============================================================== cổng trước khi chạy
def _gates(profile_id, prof, job_dir: Path):
    """Trả list lỗi (rỗng = đủ điều kiện chạy). KHÔNG tự sửa/tự đoán — thiếu gì báo đúng cái đó."""
    errs = []
    if not (job_dir / "script.txt").exists():
        errs.append(f"thiếu script.txt trong {job_dir}")
    lane_json = TITLE_CONFIG / f"{profile_id}.json"
    thumb_yaml = TITLE_CONFIG / f"{profile_id}.thumb.yaml"
    if not lane_json.exists():
        errs.append(f"lane '{profile_id}' CHƯA có cấu hình bên YT-TITLE-RESEARCH: {lane_json} "
                    f"(chưa tạo → TITLE sẽ rơi về luật satori, KHÔNG được chạy)")
    if not thumb_yaml.exists():
        errs.append(f"lane '{profile_id}' CHƯA có khuôn thumbnail bên YT-TITLE-RESEARCH: {thumb_yaml}")
    if lane_json.exists():
        try:
            lane_cf = json.loads(lane_json.read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"lane_json hỏng JSON: {e}")
            lane_cf = {}
        deliver_root = lane_cf.get("deliver_root")
        if deliver_root and not Path(deliver_root).is_dir():
            errs.append(f"deliver_root chưa tồn tại: {deliver_root} (tạo thư mục CHANEL cho lane này trước)")
    pub = prof.get("publish") or {}
    if not pub.get("listing_external"):
        errs.append(f"profile '{profile_id}' chưa bật publish.listing_external — h2dev vẫn tự viết "
                    f"tiêu đề/thumbnail (B7/B9), bật tự động TITLE lúc này sẽ đè nhau")
    hook_cf = ((prof.get("script") or {}).get("hook") or {})
    if hook_cf.get("enabled"):
        try:
            import hook_tap_md
            loi = hook_tap_md.kiem(job_dir)
            if loi:
                errs.append("HOOK_TAP.md chưa đạt: " + " · ".join(loi))
        except Exception as e:
            errs.append(f"không kiểm được HOOK_TAP.md: {e}")
    return errs


# ============================================================== khoá chống chạy đôi
def _pid_song(pid):
    """Tiến trình pid còn sống? (ctypes — KHÔNG dùng os.kill(pid, 0): trên Windows nó GIẾT tiến trình.)"""
    if pid <= 0:
        return False
    if sys.platform != "win32":
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    k32 = ctypes.windll.kernel32
    h = k32.OpenProcess(0x1000, False, pid)          # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = ctypes.c_ulong()
    ok = k32.GetExitCodeProcess(h, ctypes.byref(code))
    k32.CloseHandle(h)
    return bool(ok) and code.value == 259            # STILL_ACTIVE


def _lock_path(job_dir: Path):
    return job_dir / "research" / "TU_DONG_TITLE.lock"


def _dang_chay(job_dir: Path):
    f = _lock_path(job_dir)
    if not f.exists():
        return 0
    try:
        pid = int(f.read_text(encoding="utf-8").strip() or 0)
    except Exception:
        return 0
    return pid if _pid_song(pid) else 0


# ============================================================== worker (chạy nền thật sự)
class _Log:
    def __init__(self, path):
        self.f = open(path, "a", encoding="utf-8")

    def __call__(self, msg):
        line = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line)
        self.f.write(line + "\n")
        self.f.flush()


def _cmd(args):
    return [sys.executable, "-X", "utf8", str(TITLE_CLI), *args]


def _chay(args, log, out_path):
    """Chạy 1 lệnh cli.py, ghi THẲNG stdout vào out_path (xem được khi đang chạy). Trả exit code."""
    log(f"$ cli.py {' '.join(args)}")
    with open(out_path, "a", encoding="utf-8") as fo:
        fo.flush()
        r = subprocess.run(_cmd(args), cwd=str(TITLE_ROOT), stdout=fo, stderr=subprocess.STDOUT,
                           env={**os.environ, "PYTHONUNBUFFERED": "1"})
    return r.returncode


def _thumb_co_auto():
    """Bên TITLE đã có cờ `thumb --auto` (phương án B) chưa — có thì dùng, chưa thì chạy như cũ."""
    try:
        r = subprocess.run(_cmd(["thumb", "--help"]), cwd=str(TITLE_ROOT), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
        return "--auto" in (r.stdout or "")
    except Exception:
        return False


def worker(profile_id, job_dir: Path):
    research = job_dir / "research"
    research.mkdir(parents=True, exist_ok=True)
    if _dang_chay(job_dir):
        print(f"[goi_title] tập {job_dir.name} đang có tiến trình TITLE khác chạy — bỏ qua")
        return
    _lock_path(job_dir).write_text(str(os.getpid()), encoding="utf-8")
    status_f = research / "TU_DONG_TITLE.json"
    main_log = research / "TU_DONG_TITLE.log"
    log = _Log(main_log)
    sl = ["--slug", str(job_dir), "--profile", profile_id]

    def status(state, note=""):
        status_f.write_text(json.dumps(
            {"state": state, "note": note, "profile": profile_id, "pid": os.getpid(),
             "at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        log(f"===== goi_title worker — lane={profile_id} tập={job_dir.name} =====")
        # 1) tiêu đề + mô tả + deliver
        status("running:title")
        rc = _chay(["run", *sl, "--no-thumb", "--no-tags", "--no-sol-check"], log, main_log)
        if rc != 0:
            log(f"✗ phần tiêu đề/mô tả lỗi (exit {rc}) — DỪNG, xem log phía trên")
            status("error:title", f"exit {rc}")
            return

        # 2) tags ‖ thumb song song — mỗi cái 1 file log riêng để khỏi xen dòng
        status("running:tags+thumb")
        thumb_args = ["thumb", *sl] + (["--auto"] if _thumb_co_auto() else [])
        log(f"$ cli.py tags … ‖ cli.py {' '.join(thumb_args[:1] + thumb_args[5:])} … (song song)")
        env = {**os.environ, "PYTHONUNBUFFERED": "1"}
        with open(research / "TU_DONG_TITLE.tags.log", "a", encoding="utf-8") as ft, \
                open(research / "TU_DONG_TITLE.thumb.log", "a", encoding="utf-8") as fh:
            p_tags = subprocess.Popen(_cmd(["tags", *sl, "--write"]),   # --write: ghi cột F khi PASS (thiếu cờ này ep04 lane E không lên Sheet, sửa 2026-09-24)
                                      cwd=str(TITLE_ROOT), stdout=ft,
                                      stderr=subprocess.STDOUT, env=env)
            p_thumb = subprocess.Popen(_cmd(thumb_args), cwd=str(TITLE_ROOT), stdout=fh,
                                       stderr=subprocess.STDOUT, env=env)
            rc_thumb = p_thumb.wait()
            rc_tags = p_tags.wait()
        log(f"  tags exit {rc_tags} · thumb exit {rc_thumb}")
        if rc_tags != 0:
            log("  ⚠ tags lỗi — tiêu đề/thumbnail vẫn đi tiếp; chạy lại riêng: cli.py tags " + " ".join(sl))

        # 3) sol-check (cố vấn — lỗi không chặn)
        if _chay(["sol-check", *sl], log, main_log) != 0:
            log("  ⚠ sol-check lỗi — bỏ qua (chỉ là cố vấn)")

        th = {}
        try:
            th = json.loads((research / "THUMB.json").read_text(encoding="utf-8"))
        except Exception:
            pass
        th_state = th.get("state") or th.get("status") or ""
        if rc_thumb != 0 or th_state in ("escalate", "error"):
            note = th.get("note") or th.get("message") or ""
            log(f"✗ thumbnail chưa có ảnh để chọn (state={th_state or 'lỗi'}) {note[:160]} — DỪNG trước publish")
            status("escalate:thumb" if th_state == "escalate" else "error:thumb", note[:300])
            return

        # 3b) chế độ --auto bên TITLE KHÔNG dừng khi Sol còn lỗi HIGH — nó ghi vào strategy.json
        #     text_lock.auto_unresolved rồi vẫn vẽ. Kéo ra đây để trạng thái cuối BÁO cho người xem lại
        #     (nghiệm thu ep03 Lane F: còn 2 HIGH "SPOILER" + "FACTUAL" mà vẫn publish được).
        con_loi = []
        try:
            sj = json.loads((research / "thumb" / "strategy.json").read_text(encoding="utf-8"))
            con_loi = (sj.get("text_lock") or {}).get("auto_unresolved") or []
        except Exception:
            pass
        ghi_chu_auto = ""
        if con_loi or th.get("chosen_by") == "auto":
            loai = ", ".join(sorted({str(x.get("type", "?")) for x in con_loi if isinstance(x, dict)}))
            ghi_chu_auto = (f"thumbnail máy tự chọn ({th.get('chosen', '?')}); còn {len(con_loi)} lỗi chữ Sol chưa sửa"
                            + (f" [{loai}]" if loai else "") + " — xem research\\thumb\\strategy.json text_lock.auto_unresolved")
            log("  ⚠ " + ghi_chu_auto)

        # 4) publish thumbnail — máy tự chọn (verdict accept thì khỏi --choose)
        status("running:thumb-publish")
        if th_state in ("published", "skipped"):
            log(f"  thumbnail đã {th_state} từ trước (Sheet G có link) — không publish lại")
        elif _chay(["thumb-publish", *sl], log, main_log) != 0:
            chosen = None
            try:
                chosen = json.loads((research / "thumb" / "final_set" / "fable_review.json")
                                    .read_text(encoding="utf-8")).get("chosen")
            except Exception:
                pass
            if not chosen:
                log("✗ thumb-publish lỗi và không có bản Opus đề xuất để ép chọn — DỪNG")
                status("error:thumb-publish")
                return
            log(f"  Opus chưa 'accept' → máy tự chọn bản {chosen} (Opus xếp đầu)")
            if _chay(["thumb-publish", *sl, "--choose", chosen], log, main_log) != 0:
                log("✗ thumb-publish vẫn lỗi — DỪNG, cần người kiểm")
                status("error:thumb-publish")
                return

        # 5) Sheet
        status("running:sheet-publish")
        if _chay(["sheet-publish", *sl], log, main_log) != 0:
            log("✗ sheet-publish lỗi — tiêu đề/thumbnail đã xong, chỉ Sheet chưa ghi")
            status("error:sheet-publish")
            return
        _chay(["view", *sl, "--no-open"], log, main_log)        # dựng lại BAO_CAO/XEM sau 2 nhánh song song
        log("===== XONG — tiêu đề · mô tả · tags · thumbnail đã giao, Sheet đã ghi =====")
        status("done:can-xem-thumb" if con_loi else "done", ghi_chu_auto)
    except BaseException as e:  # noqa: BLE001
        log(f"✗ worker chết bất ngờ: {type(e).__name__}: {e}")
        status("error:worker", str(e)[:300])
        raise
    finally:
        try:
            _lock_path(job_dir).unlink(missing_ok=True)
        except Exception:
            pass


# ============================================================== entrypoint gọi từ đường giao máy 2
def goi(job_dir_str, profile_id=None, dry=False, wait=False):
    job_dir = Path(job_dir_str).resolve()
    if not job_dir.is_dir():
        print(f"[goi_title] ✗ không thấy thư mục tập: {job_dir}")
        return False
    det_id, det_prof = _detect_lane(job_dir)
    if profile_id and det_id and profile_id != det_id:
        print(f"[goi_title] ✗ --profile {profile_id} lệch với lane dò được từ đường dẫn ({det_id}) — DỪNG")
        return False
    profile_id = profile_id or det_id
    if not profile_id:
        print(f"[goi_title] ✗ không dò được lane nào có slug_dir chứa {job_dir} — DỪNG, không đoán")
        return False
    prof = det_prof or profiles.load(profile_id)
    if not (prof.get("publish") or {}).get("title_auto"):
        print(f"[goi_title] lane '{profile_id}' CHƯA mở tự động TITLE (publish.title_auto) — không gọi. "
              f"Chạy setup TITLE tập đầu bằng tay, ưng rồi: py -3.13 pipeline\\goi_title.py --bat {profile_id}")
        return False
    errs = _gates(profile_id, prof, job_dir)
    if errs:
        print(f"[goi_title] ✗ lane '{profile_id}' CHƯA đủ điều kiện tự gọi TITLE — DỪNG:")
        for e in errs:
            print(f"  - {e}")
        return False
    pid = _dang_chay(job_dir)
    if pid:
        print(f"[goi_title] tập {job_dir.name} đang chạy TITLE (pid {pid}) — không bắn thêm")
        return True
    if dry:
        print(f"[goi_title] --dry: lane='{profile_id}' tập='{job_dir}' → đủ điều kiện, sẽ chạy "
              f"tiêu đề → (tags ‖ thumbnail) → publish (máy tự chọn) → Sheet")
        return True
    if wait:
        worker(profile_id, job_dir)
        return True
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--worker",
                      "--slug", str(job_dir), "--profile", profile_id],
                     cwd=str(HERE), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, close_fds=True, **kwargs)
    print(f"[goi_title] ✓ đã bắn nền TITLE cho lane '{profile_id}' — theo dõi "
          f"{job_dir / 'research' / 'TU_DONG_TITLE.log'}")
    return True


# ============================================================== bật/tắt công tắc lane
def dat_cong_tac(profile_id, bat):
    f = PROFILE_DIR / f"{profile_id}.json"
    if not f.exists():
        raise SystemExit(f"✗ không thấy profile {f}")
    raw = f.read_text(encoding="utf-8")
    d = json.loads(raw)
    if json.dumps(d, ensure_ascii=False, indent=1) + "\n" != raw and json.dumps(d, ensure_ascii=False, indent=1) != raw:
        raise SystemExit(f"✗ {f} không theo format chuẩn (indent 1) — sửa tay field publish.title_auto")
    pub = d.setdefault("publish", {})
    if bat:
        pub["title_auto"] = True
        pub["_title_auto_note"] = (f"{datetime.date.today()}: bat tu dong goi YT-TITLE-RESEARCH sau khi giao "
                                   f"may 2 (goi_title.py --bat). Tat: --tat {profile_id}")
    else:
        pub.pop("title_auto", None)
        pub.pop("_title_auto_note", None)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    print(f"✓ {profile_id}: tự động TITLE = {'BẬT' if bat else 'TẮT'}")
    if bat and not (pub.get("listing_external")):
        print("  ⚠ lane chưa bật publish.listing_external — cổng sẽ vẫn chặn cho tới khi bật")


def trang_thai():
    for pid in profiles.list_ids():
        if pid.startswith("_"):
            continue
        try:
            p = profiles.load(pid)
        except Exception:
            continue
        pub = p.get("publish") or {}
        cf = "có" if (TITLE_CONFIG / f"{pid}.json").exists() and (TITLE_CONFIG / f"{pid}.thumb.yaml").exists() else "THIẾU"
        print(f"  {pid:22s} tự động={'BẬT' if pub.get('title_auto') else 'tắt':4s} "
              f"listing_external={'có' if pub.get('listing_external') else 'không':5s} cấu hình TITLE={cf}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="đường dẫn tuyệt đối thư mục tập")
    ap.add_argument("--profile", help="mã lane h2dev — không truyền thì TỰ DÒ theo slug_dir")
    ap.add_argument("--dry", action="store_true", help="chỉ kiểm cổng, không chạy")
    ap.add_argument("--wait", action="store_true", help="chạy CHẶN (để test), không bắn nền")
    ap.add_argument("--worker", action="store_true", help="[nội bộ] tiến trình nền thật sự chạy TITLE")
    ap.add_argument("--bat", metavar="LANE", help="BẬT tự động gọi TITLE cho lane")
    ap.add_argument("--tat", metavar="LANE", help="TẮT tự động gọi TITLE cho lane")
    ap.add_argument("--trang-thai", action="store_true", help="liệt kê công tắc mọi lane")
    a = ap.parse_args()
    if a.bat or a.tat:
        dat_cong_tac(a.bat or a.tat, bool(a.bat))
        return
    if a.trang_thai:
        trang_thai()
        return
    if not a.slug:
        ap.error("cần --slug (hoặc --bat/--tat/--trang-thai)")
    if a.worker:
        if not a.profile:
            raise SystemExit("--worker cần --profile")
        worker(a.profile, Path(a.slug).resolve())
        return
    ok = goi(a.slug, a.profile, dry=a.dry, wait=a.wait)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
