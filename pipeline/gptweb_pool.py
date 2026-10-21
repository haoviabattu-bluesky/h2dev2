r"""gptweb_pool.py — điều phối NHIỀU tài khoản ChatGPT web cho việc soát kịch bản (anh chốt 2026-09-27, bản 2 cùng ngày).

LUẬT CỨNG (anh chốt, KHÔNG được nới):
  1. Một tài khoản = một cổng Chrome = MỘT lane tại một thời điểm. Bận = khoá liên tiến trình của tài khoản đó đang bị giữ
     (lane khác / dự án YT-TITLE-RESEARCH đang hỏi). Khoá của acc1 dùng CHUNG file khoá với YT-TITLE-RESEARCH nên hai dự án
     tự nhường nhau.
  2. PHIÊN: lane giữ tài khoản từ lúc gửi lượt 1 tới lúc CHỐT phương án. Gửi → CHỜ ChatGPT trả lời xong, KHÔNG đóng cổng giữa
     chừng, KHÔNG gửi lại (chống spam GPT) → thẩm định, phản biện (lượt tiếp) trong cùng cổng → CHỐT phương án → ĐÓNG cổng
     → rồi mới viết lại kịch bản theo hướng đã chốt.
  3. CHỈ ĐÓNG CỔNG DO MÌNH MỞ: đóng đúng PID Chrome mà tool này khởi động (kiểm lại --user-data-dir trước khi đóng). Cổng đã
     mở sẵn từ trước (dự án khác, người mở tay) → dùng nhờ khi giữ được khoá, TUYỆT ĐỐI KHÔNG đóng.
  4. Tài khoản báo quá tải (Too many requests / hết lượt) → đóng phiên tài khoản đó, thử tài khoản còn lại. Cả hai đều
     bận/quá tải → in "GPT báo To many request- chờ 20 phút", ngủ 20 phút rồi thử lại.
  5. Lượt tiếp theo của CÙNG một hội thoại phải về đúng tài khoản đã mở hội thoại đó.

Phiên sống qua nhiều lệnh CLI nhờ tiến trình GIỮ PHIÊN chạy nền (`gptweb_pool.py --giu <acc> <chủ>`): giữ khoá + Chrome,
ghi E:\CLAUDE\YOUTUBE\h2dev\logs\gptweb_phien_<acc>.json. Đóng bằng dong_phien() (soat_kb_gptweb.py --chot). Quên chốt:
PHIEN_TOI_DA_S sau tự đóng (chỉ cổng của mình).

Tài khoản khai ở DS_TK (ghi đè được bằng E:\CLAUDE\YOUTUBE\h2dev\gptweb_accounts.json). Tài khoản 2 cần anh mở
`E:\CLAUDE\YOUTUBE\h2dev\tools\chatgpt_web\mo_tai_khoan_2.bat` đăng nhập tay 1 lần.
Dùng lại helper giao diện của E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src\gpt_web_client.py (chỉ đọc, không sửa dự án đó).
"""
import ctypes
import json
import msvcrt
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOGS = ROOT / "logs"
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src")

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DS_TK = [
    {"ten": "acc1", "profile": r"E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE", "port": 9335,
     "lock": r"E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\chatgpt_web\gpt_web.lock"},     # CHUNG khoá với YT-TITLE-RESEARCH
    {"ten": "acc2", "profile": r"E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE_2", "port": 9336,
     "lock": r"E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE_2_gpt.lock"},
]
MODEL = "gpt-5-6"
CHO_QUA_TAI_S = 20 * 60
SO_VONG_CHO_TOI_DA = 9                    # 9 × 20 phút = 3 giờ rồi mới bỏ cuộc
CHO_TRA_LOI_TOI_DA_S = 2 * 3600           # chờ ChatGPT trả lời tối đa 2 giờ, CỔNG VẪN MỞ suốt lúc chờ
PHIEN_TOI_DA_S = 3 * 3600                 # quên --chot: phiên tự đóng sau 3 giờ (chỉ cổng do mình mở)
THONG_BAO_QUA_TAI = "GPT báo To many request- chờ 20 phút"
_QUA_TAI = re.compile(r"(too many requests|reached (?:our|your|the) (?:message |usage )?limit|hit your (?:usage )?limit|"
                      r"usage cap|rate limit|try again later|上限に達|しばらくしてから)", re.I)


class ChuaXong(RuntimeError):
    """ĐÃ gửi vào hội thoại `conv` nhưng chưa lấy được câu trả lời. Cổng VẪN MỞ; chỉ được ĐỌC tiếp, CẤM gửi lại."""
    def __init__(self, msg, conv):
        super().__init__(msg)
        self.conv = conv


class QuaTai(RuntimeError):
    """Tài khoản bị ChatGPT giới hạn (quá nhiều yêu cầu / hết lượt)."""


class TaiKhoanHong(RuntimeError):
    """Tài khoản không dùng được lúc này (chưa đăng nhập, cổng bị Chrome khác chiếm…) — bỏ qua, thử tài khoản khác."""


class Ban(RuntimeError):
    """Tài khoản đang bị lane/dự án khác giữ."""


def ds_tai_khoan():
    f = ROOT / "gptweb_accounts.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! {f} hỏng ({e}) — dùng danh sách mặc định")
    return DS_TK


def tai_khoan(ten):
    for tk in ds_tai_khoan():
        if tk["ten"] == ten:
            return tk
    raise SystemExit(f"✗ không có tài khoản {ten}")


# ------------------------------------------------------------------ khoá (không chờ)
class Khoa:
    def __init__(self, path):
        self.path, self.f = Path(path), None

    def thu(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(self.path, "a+")
        try:
            self.f.seek(0)
            msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
            return True
        except OSError:
            self.f.close()
            self.f = None
            return False

    def nha(self):
        if not self.f:
            return
        try:
            self.f.seek(0)
            msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            self.f.close()
            self.f = None


# ------------------------------------------------------------------ Chrome của đúng profile
def _cdp_song(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def _pid_song(pid):
    if not pid:
        return False
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))     # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    try:
        code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
        return code.value == 259                                          # STILL_ACTIVE
    finally:
        ctypes.windll.kernel32.CloseHandle(h)


def _tien_trinh_profile(profile):
    """Mọi chrome.exe có --user-data-dir = đúng profile này → [(pid, parent, cmdline)]."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
          "Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=60, creationflags=0x08000000)
    try:
        ds = json.loads(r.stdout or "[]")
    except Exception:
        return []
    ds = ds if isinstance(ds, list) else [ds]
    want = profile.rstrip("\\").lower()
    out = []
    for p in ds:
        cl = (p.get("CommandLine") or "")
        m = re.search(r'--user-data-dir=(?:"([^"]+)"|(\S+))', cl)
        if m and (m.group(1) or m.group(2)).rstrip("\\").lower() == want:
            out.append((int(p["ProcessId"]), int(p.get("ParentProcessId") or 0), cl))
    return out


def _dong_chrome_cua_minh(tk, pid):
    """Đóng ĐÚNG tiến trình Chrome mà tool này đã khởi động (pid), cả cây con — chỉ khi pid đó vẫn là tiến trình chính của
    đúng profile tài khoản này. Không bao giờ đóng Chrome nào khác."""
    chinh = {p for p, _, cl in _tien_trinh_profile(tk["profile"]) if "--type=" not in cl}
    if not pid or pid not in chinh:
        print(f"  [gpt-web] {tk['ten']}: không thấy Chrome do mình mở (pid {pid}) — không đóng gì")
        return
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, creationflags=0x08000000)
    for _ in range(15):
        if not _pid_song(pid) and not _cdp_song(tk["port"]):
            break
        time.sleep(1)
    print(f"  [gpt-web] đóng cổng {tk['ten']}:{tk['port']} (Chrome pid {pid} do mình mở) — "
          + ("xong" if not _cdp_song(tk["port"]) else "⚠ cổng vẫn sống"))


# ------------------------------------------------------------------ PHIÊN (giữ khoá + cổng qua nhiều lệnh)
def _f_phien(tk):
    return LOGS / f"gptweb_phien_{tk['ten']}.json"


def _f_dung(tk):
    return LOGS / f"gptweb_phien_{tk['ten']}.stop"


def doc_phien(tk):
    """Phiên đang SỐNG của tài khoản (tiến trình giữ phiên còn chạy) → dict, không có → None."""
    try:
        ph = json.loads(_f_phien(tk).read_text(encoding="utf-8"))
    except Exception:
        return None
    return ph if ph.get("trang_thai") == "mo" and _pid_song(ph.get("holder_pid")) else None


def _ghi(tk, **kw):
    LOGS.mkdir(exist_ok=True)
    _f_phien(tk).write_text(json.dumps(kw, ensure_ascii=False), encoding="utf-8")


def _giu(ten, chu):
    """Tiến trình GIỮ PHIÊN (chạy nền): giữ khoá, mở cổng nếu chưa mở, chờ lệnh đóng; khi thoát chỉ đóng Chrome do mình mở."""
    tk = tai_khoan(ten)
    k = Khoa(tk["lock"])
    if not k.thu():
        _ghi(tk, trang_thai="ban")
        return
    chrome_pid, mo_boi_minh = None, False
    try:
        if _cdp_song(tk["port"]):
            if not any(f"--remote-debugging-port={tk['port']}" in cl for _, _, cl in _tien_trinh_profile(tk["profile"])):
                _ghi(tk, trang_thai="hong", ly_do=f"cổng {tk['port']} bị một Chrome KHÁC chiếm — không đụng vào")
                return
        else:
            Path(tk["profile"]).mkdir(parents=True, exist_ok=True)
            p = subprocess.Popen([CHROME, f"--user-data-dir={tk['profile']}", f"--remote-debugging-port={tk['port']}",
                                  "--no-first-run", "--no-default-browser-check", "--new-window", "https://chatgpt.com/"],
                                 creationflags=0x00000008 | 0x00000200)
            chrome_pid, mo_boi_minh = p.pid, True
            for _ in range(40):
                time.sleep(1)
                if _cdp_song(tk["port"]):
                    break
            else:
                _ghi(tk, trang_thai="hong", ly_do=f"Chrome không mở được cổng {tk['port']}")
                return
            time.sleep(3)
        _ghi(tk, trang_thai="mo", holder_pid=os.getpid(), chu=chu, mo_boi_minh=mo_boi_minh, chrome_pid=chrome_pid,
             bat_dau=time.strftime("%Y-%m-%d %H:%M:%S"))
        t0 = time.time()
        while not _f_dung(tk).exists() and time.time() - t0 < PHIEN_TOI_DA_S:
            if not _cdp_song(tk["port"]) and (not mo_boi_minh or not _pid_song(chrome_pid)):
                break                                                     # Chrome đã tắt từ ngoài → hết phiên
            time.sleep(2)
    finally:
        if mo_boi_minh:
            _dong_chrome_cua_minh(tk, chrome_pid)
        else:
            print(f"  [gpt-web] {tk['ten']}: cổng {tk['port']} KHÔNG do mình mở → giữ nguyên, chỉ nhả khoá")
        try:
            ph = json.loads(_f_phien(tk).read_text(encoding="utf-8"))
            if ph.get("holder_pid") == os.getpid():
                _f_phien(tk).unlink()
        except Exception:
            pass
        try:
            _f_dung(tk).unlink()
        except Exception:
            pass
        k.nha()


def mo_phien(tk, chu, log=print):
    """Giữ tài khoản cho `chu` (lane/tập). Đã có phiên của chính `chu` → dùng tiếp. Ném Ban / TaiKhoanHong."""
    ph = doc_phien(tk)
    if ph:
        if ph.get("chu") == chu:
            return ph
        raise Ban(f"{tk['ten']} đang được {ph.get('chu')} giữ")
    k = Khoa(tk["lock"])                                  # hỏi nhanh trước khi dựng tiến trình giữ phiên
    if not k.thu():
        raise Ban(f"{tk['ten']} bận (lane/dự án khác đang dùng)")
    k.nha()
    LOGS.mkdir(exist_ok=True)
    for f in (_f_phien(tk), _f_dung(tk)):
        try:
            f.unlink()
        except FileNotFoundError:
            pass
    with open(LOGS / f"gptweb_phien_{tk['ten']}.log", "a", encoding="utf-8") as lf:
        subprocess.Popen([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--giu", tk["ten"], chu],
                         stdout=lf, stderr=lf, stdin=subprocess.DEVNULL, creationflags=0x00000008 | 0x00000200)
    for _ in range(90):
        time.sleep(1)
        try:
            ph = json.loads(_f_phien(tk).read_text(encoding="utf-8"))
        except Exception:
            continue
        if ph.get("trang_thai") == "mo":
            log(f"  [gpt-web] {tk['ten']}: phiên MỞ cho {chu} — cổng {tk['port']} "
                + ("(do mình mở)" if ph.get("mo_boi_minh") else "(mở sẵn từ trước — dùng nhờ, sẽ KHÔNG đóng)"))
            return ph
        if ph.get("trang_thai") == "ban":
            raise Ban(f"{tk['ten']} bận (vừa bị lane/dự án khác giữ)")
        if ph.get("trang_thai") == "hong":
            raise TaiKhoanHong(f"{tk['ten']}: {ph.get('ly_do')}")
    raise TaiKhoanHong(f"{tk['ten']}: tiến trình giữ phiên không báo trạng thái sau 90 giây")


def dong_phien(tk, chu=None, log=print):
    """Đóng phiên (chỉ phiên do tool này giữ; chu khác → không đụng). Tiến trình giữ phiên tự đóng Chrome CỦA MÌNH."""
    ph = doc_phien(tk)
    if not ph:
        log(f"  [gpt-web] {tk['ten']}: không có phiên đang mở")
        return True
    if chu and ph.get("chu") != chu:
        log(f"  [gpt-web] {tk['ten']}: phiên đang là của {ph.get('chu')} — KHÔNG đóng")
        return False
    _f_dung(tk).write_text("dung", encoding="utf-8")
    for _ in range(60):
        time.sleep(1)
        if not _pid_song(ph["holder_pid"]):
            break
    ok = not _pid_song(ph["holder_pid"])
    log(f"  [gpt-web] {tk['ten']}: " + ("ĐÃ ĐÓNG phiên" + (" + cổng" if ph.get("mo_boi_minh") else " (cổng mở sẵn, giữ nguyên)")
                                         if ok else "⚠ tiến trình giữ phiên chưa thoát"))
    return ok


# ------------------------------------------------------------------ hỏi trong phiên
def _qua_tai_tren_trang(page):
    try:
        return bool(_QUA_TAI.search(page.evaluate("document.body.innerText") or ""))
    except Exception:
        return False


def _cho_san_sang(tk, page):
    """Chờ ô nhập. Không thấy → tải lại 1 lần. Vẫn không thấy → hỏi /api/auth/session để phân biệt:
    có phiên = đã đăng nhập, trang chậm/kẹt (lỗi TẠM); không phiên = CHƯA ĐĂNG NHẬP thật.
    (27/09: K ep05 báo acc2 'chưa đăng nhập' lúc Chrome vừa mở nguội, 5 phút sau cùng link vào ngay 0,4 giây.)"""
    import gpt_web_client as g
    for lan in (1, 2):
        try:
            g._wait_ready(page)
            return
        except Exception as e:
            loi = e
            if lan == 1:
                try:
                    page.reload(wait_until="domcontentloaded", timeout=60000)
                except Exception:
                    pass
    anh = LOGS / f"gptweb_{tk['ten']}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    try:
        LOGS.mkdir(exist_ok=True)
        page.screenshot(path=str(anh))
    except Exception:
        anh = None
    try:
        email = page.evaluate("async () => { try { const s = await (await fetch('/api/auth/session')).json();"
                              " return (s && s.user && s.user.email) || ''; } catch (e) { return '?'; } }")
    except Exception:
        email = "?"
    if email == "":
        raise TaiKhoanHong(f"{tk['ten']}: CHƯA ĐĂNG NHẬP (không có phiên) — ảnh {anh}")
    raise RuntimeError(f"{tk['ten']}: đã đăng nhập ({email}) nhưng 2 lần không thấy ô nhập ở {page.url} "
                       f"({type(loi).__name__}) — lỗi tạm; ảnh {anh}")


# Câu trả lời cho ĐÚNG tin mình gửi (tin user gần nhất bắt đầu bằng `dau`), đọc từ backend — không phụ thuộc giao diện.
_JS_TRA_LOI = """async ([cid, dau]) => {
  const s = await (await fetch('/api/auth/session')).json();
  const r = await fetch('/backend-api/conversation/' + cid, {headers: {Authorization: 'Bearer ' + s.accessToken}});
  if (!r.ok) return {err: 'HTTP ' + r.status};
  const j = await r.json();
  // ChatGPT lưu tin user có thể đã escape markdown (vd "\\- Tiêu đề") → bỏ mọi dấu \\ trước khi so khớp
  const norm = t => (t || '').replace(/\\\\/g, '').replace(/\\s+/g, ' ').trim();
  const want = norm(dau);
  // Trả lời có thể gồm NHIỀU tin assistant (lời dẫn → gọi tool đọc file Project → bài chấm chính): gom hết theo thứ tự
  let node = j.mapping[j.current_node], parts = [], model = '';
  while (node) {
    const m = node.message;
    if (m && m.author && m.content) {
      const txt = (m.content.parts || []).filter(p => typeof p === 'string').join(String.fromCharCode(10));
      if (m.author.role === 'assistant' && m.content.content_type === 'text' && (m.recipient === 'all' || !m.recipient)
          && txt.trim()) { parts.unshift(txt); model = model || (m.metadata || {}).model_slug || ''; }
      if (m.author.role === 'user') {
        if (norm(txt).startsWith(want))
          return parts.length ? {text: parts.join(String.fromCharCode(10) + String.fromCharCode(10)), model} : {cho: true};
        parts = []; model = '';
      }
    }
    node = node.parent ? j.mapping[node.parent] : null;
  }
  return {err: 'không thấy tin mình gửi trong hội thoại'};
}"""


def _doc_tra_loi(page, conv, text, cho_s):
    """Đọc câu trả lời cho tin `text` trong `conv` qua backend; đứng yên 2 lần đọc liền (cách 15s) mới coi là xong."""
    cid, dau = conv.rsplit("/c/", 1)[1], " ".join(text[:150].split())
    t0, truoc = time.time(), None
    while time.time() - t0 < cho_s:
        try:
            r = page.evaluate(_JS_TRA_LOI, [cid, dau])
        except Exception:
            r = {}
        if r.get("text"):
            if truoc == r["text"]:
                return r["text"], r.get("model") or "?"
            truoc = r["text"]
        time.sleep(15)
    return None, None


def _cho_tra_loi(page, st0, text, cho_s, log=print):
    """Chờ ChatGPT trả lời xong tin `text` vừa gửi. KHÔNG đếm số khối trả lời trên DOM như `g._wait_answer`:
    hội thoại cố định dài (Lane M dùng 1 hội thoại cho mọi tập) chỉ render vài tin cuối → số khối đứng yên
    (đo thật ep04 30/09: n=4 trước và sau khi GPT đã trả lời) → treo tới hết 2 giờ dù GPT xong từ lâu.
    Xong = không còn nút stop + (backend có trả lời cho ĐÚNG tin mình, HOẶC chữ tin cuối trên DOM đã khác lúc
    trước khi gửi) + chữ đứng yên 2 lượt đọc liền (cách 10s)."""
    import gpt_web_client as g
    dau = " ".join(text[:150].split())
    t0, truoc, lan_log = time.time(), None, 0
    while time.time() - t0 < cho_s:
        time.sleep(10)
        try:
            if page.locator(g.STOP_SEL).count():
                truoc = None
                continue
            out = ""
            if "/c/" in page.url:
                r = page.evaluate(_JS_TRA_LOI, [page.url.split("?")[0].rsplit("/c/", 1)[1], dau]) or {}
                out = r.get("text") or ""
            if not out:
                st = page.evaluate(g._JS_LAST)
                if st["text"].strip() and (st["n"] > st0["n"] or st["text"] != st0["text"]):
                    out = st["text"]
        except Exception:
            continue
        if out and out == truoc:
            return True
        truoc = out or None
        if time.time() - t0 > lan_log + 300:
            lan_log = time.time() - t0
            log(f"  [gpt-web] … vẫn chờ ({int(lan_log // 60)} phút, {'đã có chữ' if out else 'chưa có chữ'})")
    raise ChuaXong(f"ChatGPT chưa trả lời xong sau {cho_s}s", page.url.split("?")[0])


def _trang(pw, tk, url):
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{tk['port']}")
    page = b.contexts[0].new_page()
    page.goto(url.split("?")[0] + f"?model={MODEL}", wait_until="domcontentloaded", timeout=60000)
    _cho_san_sang(tk, page)
    time.sleep(4)
    pid = re.search(r"/g/(g-p-[0-9a-f]{32})", url)
    if pid and f"/g/{pid.group(1)}" not in page.url:     # hội thoại không thuộc tài khoản này → ChatGPT nhảy ra ngoài
        den = page.url
        page.close()
        raise TaiKhoanHong(f"{tk['ten']}: mở {url} nhưng trang nhảy sang {den} — KHÔNG gửi (sai Project/tài khoản)")
    return page


def _gui(tk, url, text, log=print):
    """Gửi 1 lần rồi CHỜ tới khi ChatGPT trả lời xong (cổng vẫn mở suốt lúc chờ). Sau khi đã bấm gửi, mọi lỗi đều thành
    ChuaXong (chỉ được ĐỌC tiếp, cấm gửi lại)."""
    import gpt_web_client as g
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        page = _trang(pw, tk, url)
        try:
            if _qua_tai_tren_trang(page):
                raise QuaTai(f"{tk['ten']} đang bị giới hạn trước khi gửi")
            st0 = page.evaluate(g._JS_LAST)
            g._send(page, text, None)
            log(f"  [gpt-web] {tk['ten']}: đã gửi {len(text):,} chữ — CHỜ ChatGPT trả lời (cổng giữ nguyên, không gửi lại)")
            try:
                _cho_tra_loi(page, st0, text, CHO_TRA_LOI_TOI_DA_S, log)
            except Exception:
                if _qua_tai_tren_trang(page):
                    raise QuaTai(f"{tk['ten']} báo quá tải khi đang trả lời")
            conv = page.url.split("?")[0]
            if "/c/" not in conv:
                raise ChuaXong(f"{tk['ten']}: đã gửi nhưng không lấy được link hội thoại ({page.url})", conv)
            out, model = _doc_tra_loi(page, conv, text, 120)
            if not out:
                raise ChuaXong(f"{tk['ten']}: ĐÃ gửi, chưa đọc được câu trả lời ở {conv} — cổng VẪN MỞ, chỉ ĐỌC tiếp", conv)
            if len(out) < 400 and _QUA_TAI.search(out):
                raise QuaTai(f"{tk['ten']}: {out[:120]}")
            return g.clean(out), model, conv
        finally:
            try:
                page.close()
            except Exception:
                pass


def doc(tk, conv, text, cho_s=CHO_TRA_LOI_TOI_DA_S):
    """Chỉ ĐỌC câu trả lời cho tin `text` trong `conv` (không gửi gì). Cần phiên đang mở."""
    import gpt_web_client as g
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        page = _trang(pw, tk, conv)
        try:
            out, model = _doc_tra_loi(page, conv, text, cho_s)
        finally:
            page.close()
    if not out:
        raise ChuaXong(f"{tk['ten']}: vẫn chưa có câu trả lời ở {conv}", conv)
    return g.clean(out), model, conv


def hoi(text, urls, chu, acc_co_dinh=None, log=print):
    """Giữ phiên 1 tài khoản rảnh cho `chu`, gửi `text`, CHỜ trả lời. Trả (trả lời, model, tên tk, link hội thoại).
    Phiên + cổng VẪN MỞ sau khi trả về — người gọi thẩm định, phản biện, rồi dong_phien() khi chốt phương án."""
    ds = [tk for tk in ds_tai_khoan() if urls.get(tk["ten"])]
    if acc_co_dinh:
        ds = [tk for tk in ds if tk["ten"] == acc_co_dinh]
    if not ds:
        raise SystemExit(f"✗ không có tài khoản ChatGPT nào có link cho việc này (urls={list(urls)}, cố định={acc_co_dinh})")
    for vong in range(1, SO_VONG_CHO_TOI_DA + 1):
        ly_do, dang_cho = [], False   # dang_cho = có tk BẬN/QUÁ TẢI (chờ 20 phút có ích); chỉ hỏng thì chờ vô ích
        for tk in ds:
            try:
                mo_phien(tk, chu, log=log)
            except Ban as e:
                ly_do.append(str(e))
                dang_cho = True
                continue
            except TaiKhoanHong as e:
                ly_do.append(f"{tk['ten']} không dùng được ({e})")
                continue
            try:
                out, model, conv = _gui(tk, urls[tk["ten"]], text, log=log)
                if not out.strip():
                    raise ChuaXong(f"{tk['ten']}: ChatGPT trả rỗng", conv)
                return out, model, tk["ten"], conv
            except ChuaXong:
                raise                                    # đã gửi: giữ phiên, không thử tài khoản khác, không gửi lại
            except QuaTai as e:
                ly_do.append(f"{tk['ten']} quá tải ({e})")
                dang_cho = True
                dong_phien(tk, chu, log=log)
            except TaiKhoanHong as e:
                ly_do.append(f"{tk['ten']} không dùng được ({e})")
                dong_phien(tk, chu, log=log)
            except Exception as e:                       # lỗi TRƯỚC khi gửi (trang/mạng) — đóng phiên, vòng sau thử lại
                ly_do.append(f"{tk['ten']} lỗi {type(e).__name__}: {str(e)[:120]}")
                dang_cho = True
                dong_phien(tk, chu, log=log)
        log("  [gpt-web] " + " · ".join(ly_do))
        if not dang_cho:
            raise SystemExit("✗ ChatGPT web: không tài khoản nào dùng được — " + " · ".join(ly_do))
        if vong == SO_VONG_CHO_TOI_DA:
            break
        log(THONG_BAO_QUA_TAI)
        time.sleep(CHO_QUA_TAI_S)
    raise SystemExit(f"✗ ChatGPT web: hết {SO_VONG_CHO_TOI_DA} vòng chờ vẫn không tài khoản nào dùng được")


def trang_thai():
    """In tình trạng từng tài khoản: phiên / khoá / cổng / số tiến trình Chrome."""
    for tk in ds_tai_khoan():
        ph = doc_phien(tk)
        k = Khoa(tk["lock"])
        ranh = k.thu()
        k.nha()
        s = (f"{tk['ten']}: profile {tk['profile']} · cổng {tk['port']} {'SỐNG' if _cdp_song(tk['port']) else 'đóng'} · "
             f"khoá {'rảnh' if ranh else 'BẬN'} · {len(_tien_trinh_profile(tk['profile']))} tiến trình Chrome")
        if ph:
            s += (f" · PHIÊN của {ph.get('chu')} từ {ph.get('bat_dau')} "
                  + ("(cổng do tool mở)" if ph.get("mo_boi_minh") else "(cổng mở sẵn, tool không đóng)"))
        print(s)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 4 and sys.argv[1] == "--giu":
        _giu(sys.argv[2], sys.argv[3])
    else:
        trang_thai()
