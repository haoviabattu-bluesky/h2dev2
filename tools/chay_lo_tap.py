#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""chay_lo_tap.py — chạy LIÊN TIẾP nhiều tập của 1 lane, MỖI TẬP 1 `claude -p` MỚI (ngữ cảnh sạch).

Vì sao (anh chốt 2026-10-05): làm tập 8→10 trong 1 tab chat thì context phình, phải nén, tốn quota.
Tool này thay tab chat: mỗi tập gọi 1 phiên `claude -p` riêng (không mang lịch sử tập trước), xong
tập → đọc lại cột D trên sheet để tự chứng minh → đúng mốc thì sang tập kế, sai thì DỪNG cả lô.

Việc của từng tập chọn theo cột D hiện tại (bảng mốc: docs\TRANG_THAI_COT_D_K.md):
  (trống) / "Đang chạy kịch bản bước 1"   → chặng 1: hồ sơ + make_video --den B3G   → chờ D "Chờ kiểm tra kịch bản"
  "Đã sửa kịch bản" / "Đang làm Hook"      → NHAN_KICH_BAN_MAY3 §1–§5 (tới clip hook) → chờ D "Chờ duyệt hook"
  "Đã duyệt hook"                          → NHAN_KICH_BAN_MAY3 §6 (giao máy 2)       → chờ D "Đã giao máy 2"
                                              (máy 2 làm A→Z từ 21/10: đích = "Chờ dựng video")
  "Chờ dựng video" / "Đang dựng video"     → CHỈ máy 2: làm hết _BANGIAO.txt tới final.mp4 → chờ D "Video xong"
  khác (đang chờ anh / đã xong)            → BỎ QUA
Chạy tuần tự (Grok/ai33/sheet dùng chung — cấm song song).

Dùng (cửa sổ cmd thường, KHÔNG cần mở tab Claude):
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_lo_tap.py --profile teinengo-fuufu --tu 8 --den 10
  ... --dry                       chỉ in tập nào sẽ làm việc gì, không gọi claude
  ... --chi-chang hook            chỉ làm tập đang ở chặng hook (bỏ qua chặng 1 / giao máy 2)
  ... --tiep-khi-loi              tập lỗi thì ghi log rồi vẫn sang tập kế (mặc định DỪNG cả lô)
  ... --tran-usd 9                trần $ quy đổi 1 phiên (0 = tắt)
Nhiều lane 1 lệnh: E:\CLAUDE\YOUTUBE\h2dev\tools\chay_hang_doi.py (gọi tool này, mỗi lane 1 lô).
Tiết kiệm quota (21/10): prompt kèm PHIẾU TẬP tra sẵn + kỷ luật ngữ cảnh, --strict-mcp-config, TONG_KET ghi ctx đỉnh.
Log từng tập: E:\CLAUDE\YOUTUBE\h2dev\logs\chay_lo_tap\<tab>_STT<n>_<chang>_<giờ>.jsonl (+ TONG_KET_<giờ>_<mã>.txt)
"""
import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

import claude_p_bridge   # noqa: E402
import dong_goi_may2 as _dg   # noqa: E402
import may_hien_tai      # noqa: E402
import kiem_hook_goc     # noqa: E402
import profiles          # noqa: E402
import review_may3 as rv  # noqa: E402

LOG_DIR = ROOT / "logs" / "chay_lo_tap"
NHAN = ROOT / "docs" / "NHAN_KICH_BAN_MAY3.md"

# chặng → (trạng thái D đầu vào, trạng thái D phải đạt khi xong)
CHANG = {
    "kichban": ({"", rv.TRANG_THAI_DANG_B1}, rv.TRANG_THAI_CHO),
    "hook": ({rv.TRANG_THAI_DA_SUA, rv.TRANG_THAI_DANG_HOOK}, "Chờ duyệt hook"),
    "giao2": ({"Đã duyệt hook"}, _dg.nhan_d_xong()),
}
if may_hien_tai.la_may2():     # 21/10 anh chốt: máy 2 làm 100% A→Z → thêm chặng dựng video ngay sau duyệt hook
    import xong_video
    CHANG["dung"] = ({_dg.CHO_DUNG, xong_video.DANG_DUNG}, xong_video.VIDEO_XONG)

HEADLESS = r"""
=== CHẾ ĐỘ CHẠY LÔ (headless) — luật này ĐÈ luật tương ứng trong CLAUDE.md/SOP ===
- Bạn chạy trong `claude -p` do E:\CLAUDE\YOUTUBE\h2dev\tools\chay_lo_tap.py gọi. KHÔNG có anh trả lời giữa chừng,
  KHÔNG có cơ chế đánh thức. Vì vậy luật "tool lâu → run_in_background rồi dừng lượt" KHÔNG áp dụng:
  tool lâu (TTS/ảnh/Grok) chạy Bash foreground với timeout 600000; dự kiến >10 phút thì chạy run_in_background
  rồi CHỜ bằng vòng `until <điều kiện xong, vd file kết quả/dòng log cuối>; do sleep 60; done` (timeout 600000,
  lặp lại tới khi xong hoặc lỗi). TUYỆT ĐỐI không kết thúc phiên khi tool còn chạy.
- Chỉ làm ĐÚNG tập STT {stt} (sheet tab {tab} dòng {dong}). Không đụng tập/dòng khác.
- Mọi luật cứng khác giữ nguyên ({vai_may}, không sửa tay script.txt, không kill Chrome,
  không xoá dữ liệu sheet, TITLE/thumbnail TẮT).
- Chỗ nào luật bảo hỏi/báo anh mà không tự quyết an toàn được → DỪNG phiên, không đoán.
- ⛔ HOOK GỐC (anh chốt 21/10): hook PHẢI bám cấu trúc hook video gốc do hook_stage tách. Tool báo "KHÔNG CÓ CẤU TRÚC
  HOOK GỐC" / "KHÔNG khoá hook" → DỪNG phiên (KET_QUA: DUNG — không có hook gốc). CẤM tự viết hook tay, cấm khoá tay
  hook_lock.json, cấm tự bịa nhịp. Họ nhân vật vai mới cấm trùng tập trước (xem PHIẾU TẬP).
- Chất lượng: nếu log make_video/lean có "TỪ CHỐI" (lượt vá hỏng), model rơi sang dự phòng (Gemini/llm_client
  thay Fable/Opus), hoặc Sol chấm bằng nhà cung cấp dự phòng → GHI RÕ 1 dòng trong báo cáo (tập vẫn tính xong).
- KỶ LUẬT NGỮ CẢNH (21/10 — đo lô cũ: phiên tự đi lục code/log/tập cũ → 180–310K token, 17 triệu token đọc lại/tập):
  * PHIẾU TẬP bên dưới đã tra sẵn thư mục tập, tập mẫu, video gốc, tên nhân vật đã dùng → dùng luôn, KHÔNG tự tra lại.
  * CẤM đọc mã nguồn `pipeline\*.py` / `tools\*.py` (chạy tool theo lệnh trong SOP; lỗi thì đọc thông báo lỗi, không đọc code).
  * Log: chỉ `tail -40` (hoặc `grep` đúng dòng cần); CẤM `cat`/`head -150` cả log, CẤM Read lại file dump `tool-results`.
  * Tập cũ: chỉ được đọc TẬP MẪU trong phiếu (và chỉ file cần chép mẫu); CẤM `ls -la`/đọc các tập khác.
  * Doc dài (SOP/BAT_DAU_LANE/skill): `grep -n` tiêu đề rồi đọc đúng mục cần, không đọc cả file.
- Báo cáo cuối NGẮN (≤10 dòng, đường dẫn tuyệt đối). Dòng CUỐI CÙNG đúng 1 trong 2 dạng:
  KET_QUA: XONG
  KET_QUA: DUNG — <lý do 1 dòng>
"""


def doc_tab(tab):
    import dong_goi_may2 as dg
    s = dg.svc(doc_thoi=True)
    vals = s.values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!A2:K300").execute().get("values", [])
    out = {}
    for i, row in enumerate(vals):
        row = row + [""] * (11 - len(row))
        stt = row[0].strip()
        if stt.isdigit():
            out[int(stt)] = {"dong": i + 2, "de_tai": row[1].strip(), "folder": row[2].strip(),
                             "d": row[3].strip(), "k": row[10].strip()}
    return out


def chon_chang(d):
    dau = rv.dong_dau(d)
    for ten, (vao, _) in CHANG.items():
        if dau in vao:
            return ten
    return None


def _thu_muc(folder):
    if not folder:
        return None
    p = Path(folder.replace("/", "\\"))
    return p if p.is_absolute() else ROOT / p


def phieu_tap(prof, stt, r):
    """Tra sẵn bằng Python những thứ phiên claude -p trước đây tự đi lục (ls tập cũ, cat log, đọc code) — bước 2
    tiết kiệm quota anh duyệt 21/10. Lỗi tra cứu không chặn lô: thiếu mục nào thì phiên tự tra mục đó."""
    sd = ROOT / prof.get("slug_dir", "assets/out")
    tap = _thu_muc(r["folder"])
    dong = [f"=== PHIẾU TẬP (Python tra sẵn — dùng luôn, không tra lại) ===",
            f"- Thư mục lane: {sd}",
            f"- Thư mục tập: {tap if tap else '(chưa có — tạo mới ' + str(sd) + chr(92) + f'ep{stt:02d}-<slug>)'}"]
    try:
        locks = sorted((p for p in sd.glob("*/script.lock.json") if not tap or p.parent != tap),
                       key=lambda p: p.stat().st_mtime)
        du = [p for p in locks if (p.parent / "series_ctx.txt").exists()]   # tập mẫu phải có series_ctx để chép QUY ƯỚC
        if du or locks:
            mau = (du or locks)[-1].parent
            co = [f for f in ("series_ctx.txt", "characters.json", "video_goc.json", "HOOK_TAP.md", "promise.txt")
                  if (mau / f).exists()]
            dong.append(f"- TẬP MẪU (khoá kịch bản gần nhất): {mau} — file mẫu có: {', '.join(co)}")
        ten = {}                           # tên → các tập dùng (bỏ vai tập thể kiểu 女性たち)
        for p in locks[-6:]:
            try:
                cs = json.loads((p.parent / "characters.json").read_text(encoding="utf-8")).get("characters", [])
                for c in cs:
                    n = (c.get("name") or "").strip()
                    if n and not n.endswith("たち"):
                        ten.setdefault(n, []).append(p.parent.name.split("-")[0])
            except (OSError, ValueError, AttributeError):
                pass
        if ten:
            dong.append("- Tên nhân vật 6 tập gần nhất (vai MỚI cấm trùng; nhân vật cố định của lane giữ nguyên): "
                        + ", ".join(f"{n}({','.join(e)})" for n, e in ten.items()))
        cam = kiem_hook_goc.ho_da_dung(tap, sd)   # mọi tập của lane, không chỉ 6 tập (ep23 dùng lại 佐野 của ep04)
        if cam:
            dong.append("- HỌ CẤM cho vai mới (đã dùng ở tập khác; hook_stage chặn cứng): " + "、".join(sorted(cam)))
    except OSError as e:
        dong.append(f"- (không tra được tập mẫu: {e})")
    vg = (tap / "video_goc.json") if tap else None
    if vg and vg.exists():
        try:
            v = json.loads(vg.read_text(encoding="utf-8")).get("video_goc") or {}
            dong.append(f"- Video gốc (video_goc.json): {v.get('url') or v.get('id') or 'null'} · {v.get('tieu_de', '')}")
        except (OSError, ValueError):
            dong.append(f"- Video gốc: {vg} (đọc lỗi)")
    else:
        dong.append(f"- Video gốc: theo cột K ở trên (chưa có video_goc.json)")
    hd = sd / "HUONG_DAN_TAP_TIEP_THEO.md"
    if tap and (tap / "HUONG_DAN_TAP.md").exists():   # lô đề tài mới: mỗi tập có hướng dẫn riêng → ưu tiên
        hd = tap / "HUONG_DAN_TAP.md"
    dong.append(f"- Hướng dẫn tập: {hd if hd.exists() else ROOT / 'docs' / 'BAT_DAU_LANE' / (prof['id'] + '.md')}")
    return "\n".join(dong)


def kiem_truoc(prof, stt, r, chang, whisper=True):
    """BƯỚC CHUẨN BỊ (anh chốt 21/10, Lane L ep23 佐野稔): kiểm hook gốc TRƯỚC khi mở claude -p — thiếu thì tập không chạy.
    Chặng kịch bản: phải có lời 0–150s video gốc (tách được cấu trúc hook). Chặng hook/giao máy 2: hook đã khoá phải bám
    cấu trúc gốc + không dùng lại họ nhân vật tập trước. Trả '' = đạt, ngược lại = lý do."""
    tap = _thu_muc(r["folder"])
    if chang == "kichban":
        if tap and (tap / "hook" / "hook_locked.txt").exists():
            loi = kiem_hook_goc.kiem_hook_da_khoa(tap)
            if loi:
                return " · ".join(loi)
        k = kiem_hook_goc.kiem_nguon(tap, r["k"], r["de_tai"], whisper=whisper)
        return "" if k["ok"] else f"{k['ly_do']} (video {k['video_id'] or 'không có'})"
    if not tap:
        return "chưa có thư mục tập ở cột C"
    return " · ".join(kiem_hook_goc.kiem_hook_da_khoa(tap))


def lam_prompt(prof, tab, stt, r, chang):
    lane = rv.ma_tap(prof, "x")[0]
    slug = Path(r["folder"].replace("\\", "/")).name if r["folder"] else ""
    tap = rv.ma_tap(prof, slug)[1] if slug else f"ep{stt:02d}"
    hd = ROOT / prof.get("slug_dir", "") / "HUONG_DAN_TAP_TIEP_THEO.md" if prof.get("slug_dir") else None
    rieng = _thu_muc(r["folder"])
    if rieng and (rieng / "HUONG_DAN_TAP.md").exists():
        hd = rieng / "HUONG_DAN_TAP.md"
    if chang == "kichban":
        body = (f"@lane:{prof['id']} — làm CHẶNG 1 (hồ sơ + viết + khoá kịch bản) cho tập STT {stt} "
                f"(sheet tab {tab} dòng {r['dong']}).\n"
                f"Đề tài cột B: {r['de_tai']}\nGhi chú cột K (nguồn video gốc nếu có): {r['k'] or '(trống)'}\n"
                f"Thư mục tập hiện ghi ở cột C: {r['folder'] or '(chưa có — tạo mới epNN-<slug> theo mẫu tập trước)'}\n"
                f"Quy trình: làm đúng mục 1→2→4 của "
                f"{hd if hd and hd.exists() else 'docs/BAT_DAU_LANE/' + prof['id'] + '.md (mục ⚡ ĐỌC NHANH)'} "
                f"NHƯNG thay số tập/dòng/đề tài bằng STT {stt} ở trên (file đó có thể đang viết cho tập khác). "
                f"Tập mẫu = tập gần nhất của lane đã có script.lock.json. Dừng ở mốc D = 'Chờ kiểm tra kịch bản'.\n"
                f"⛔ BẮT BUỘC gọi skill `youtube-kich-ban` TRƯỚC khi viết (model S2/hook KHÔNG tự đọc skill + "
                f"C:\\Users\\admin\\.claude\\skills\\youtube-kich-ban\\BAI_HOC.md — bài học chỉ vào kịch bản qua tay bạn): "
                f"làm đúng §4 của skill — nhồi luật §2 + BAI_HOC liên quan vào khối QUY ƯỚC của series_ctx.txt (gồm tên "
                f"nhân vật đã dùng ở tập trước), duyệt 2 phương án hook theo references/HOOK.md §4, soát bản S2 bằng "
                f"CHECKLIST.md → lỗi thì viec_tay.txt theo đúng mẫu skill. Báo cáo cuối ghi 1 dòng 'skill: đã áp N luật'.")
    elif chang == "hook":
        body = (f"anh sửa xong kịch bản {lane} {tap}\n"
                f"(@lane:{prof['id']}, thư mục tập {ROOT / prof.get('slug_dir', '')}\\{slug}) — đọc ĐÚNG {NHAN}, "
                f"làm §1–§5 tới clip hook xem thử rồi DỪNG ở mốc D = 'Chờ duyệt hook'.")
    elif chang == "dung":
        tap_dir = ROOT / prof.get("slug_dir", "") / slug
        body = (f"@lane:{prof['id']} — CHẶNG DỰNG VIDEO (máy 2 làm A→Z, anh chốt 21/10) cho tập STT {stt} "
                f"(sheet tab {tab} dòng {r['dong']}), thư mục tập {tap_dir}.\n"
                f"1) py -3.13 -X utf8 {ROOT / 'pipeline' / 'xong_video.py'} --profile {prof['id']} --slug {slug} --bat-dau\n"
                f"2) Làm ĐÚNG và HẾT {tap_dir / '_BANGIAO.txt'} (lồng tiếng → vẽ ảnh → dựng → giao; số liệu động nếu có mục đó). "
                f"Quy trình chung + bẫy: {ROOT / 'docs' / 'MAY2_LAM_A_DEN_Z.md'} §4.\n"
                f"3) Có final.mp4 rồi: py -3.13 -X utf8 {ROOT / 'pipeline' / 'xong_video.py'} --profile {prof['id']} --slug {slug} "
                f"→ D = 'Video xong'. Báo cáo: đường dẫn final.mp4 + final-vietsub.mp4, thời gian thật, số ảnh/tiền thật.")
    else:
        body = (f"anh duyệt hook {lane} {tap}\n"
                f"(@lane:{prof['id']}, thư mục tập {ROOT / prof.get('slug_dir', '')}\\{slug}) — đọc ĐÚNG {NHAN} §6, "
                + (f"chạy dong_goi_may2 --job (máy 2: viết _BANGIAO.txt tại chỗ) rồi DỪNG ở mốc D = '{_dg.CHO_DUNG}'."
                   if may_hien_tai.la_may2() else "giao máy 2 rồi DỪNG ở mốc D = 'Đã giao máy 2'."))
    vai_may = ("máy 2 làm A→Z: kịch bản + hook + giọng + ảnh + dựng" if may_hien_tai.la_may2()
               else "máy 1 chỉ bước 1 + hình hook")
    return body + "\n" + HEADLESS.format(stt=stt, tab=tab, dong=r["dong"], vai_may=vai_may) + "\n" + phieu_tap(prof, stt, r) + "\n"


def chay_claude(prompt, model, log, timeout, tran_usd=0.0):
    exe = claude_p_bridge.find_claude()
    if not exe:
        raise SystemExit("không tìm thấy claude CLI (đặt env CLAUDE_CLI=<đường dẫn claude.exe>)")
    cmd = [exe, "-p", "--model", model, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "bypassPermissions", "--no-session-persistence",
           "--strict-mcp-config"]          # bỏ MCP (AdsPower/Gmail/nanobanana…): log lô cũ không gọi mcp__ lần nào
    if tran_usd > 0:                   # trần chống phiên lạc (CLI 2.1.x không có --max-turns)
        cmd += ["--max-budget-usd", f"{tran_usd:.2f}"]
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    ket = {}
    ctx_dinh = 0
    with open(log, "w", encoding="utf-8") as f:
        p = subprocess.Popen(cmd, cwd=str(ROOT), env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        p.stdin.write(prompt)
        p.stdin.close()
        bat_dau = _dt.datetime.now()
        for line in p.stdout:
            f.write(line)
            f.flush()
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "assistant":   # context đỉnh — thước đo bước 2 (mục tiêu < 120K)
                u = (ev.get("message") or {}).get("usage") or {}
                ctx_dinh = max(ctx_dinh, u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                               + u.get("cache_creation_input_tokens", 0))
            if ev.get("type") == "result":
                ket = ev
            if (_dt.datetime.now() - bat_dau).total_seconds() > timeout:
                p.kill()
                ket = {"result": f"KET_QUA: DUNG — quá {timeout // 60} phút, đã dừng phiên"}
                break
        p.wait()
    ket["ctx_dinh"] = ctx_dinh
    return ket


def bao_dang_chay(prof, tab, stt, r, chang):
    """Ghi trạng thái NGAY lúc mở phiên (anh chốt 05/10): trước đây chỉ make_video ghi, mà phiên lô mất ~20 phút
    làm hồ sơ S1 trước khi gọi make_video → suốt quãng đó TONGHOP/cột D trống, anh không biết lô đang chạy tập nào.
    Lỗi sheet không chặn lô (cùng triết lý tong_hop.ghi)."""
    import tong_hop
    slug = Path(r["folder"].replace("\\", "/")).name if r["folder"] else f"ep{stt:02d}"
    if chang == "kichban":
        if not rv.dong_dau(r["d"]):
            try:
                import dong_goi_may2 as dg
                rv._ghi_d(dg, tab, r["dong"], rv.TRANG_THAI_DANG_B1)
            except BaseException as e:  # noqa: BLE001
                print(f"  ⚠️ chưa ghi được cột D: {e}")
        tong_hop.ghi(prof, slug, tong_hop.CHAY_KB)
    elif chang == "hook":
        tong_hop.ghi(prof, slug, tong_hop.CHAY_HOOK)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--tu", type=int, required=True, help="STT đầu (cột A)")
    ap.add_argument("--den", type=int, required=True, help="STT cuối (gồm cả)")
    ap.add_argument("--chi-chang", choices=list(CHANG), help="chỉ làm tập đang ở chặng này")
    ap.add_argument("--model", default="opus", help="model điều phối mỗi phiên (mặc định opus)")
    ap.add_argument("--timeout-phut", type=int, default=240, help="trần 1 tập (mặc định 240 phút)")
    ap.add_argument("--tiep-khi-loi", action="store_true")
    ap.add_argument("--tran-usd", type=float, default=9.0,
                    help="trần $ quy đổi 1 phiên (mặc định 9 — tập đắt nhất lô cũ $7.20); 0 = tắt")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--ghi-chu", default="", help="lời dặn thêm của anh, nối vào cuối prompt mỗi tập (vd yêu cầu riêng cho hook)")
    a = ap.parse_args(argv)

    prof = profiles.load(a.profile)
    tab = rv.tab_cua(prof)
    if not tab:
        raise SystemExit(f"profile {a.profile} chưa khai publish.sheet_tab")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not a.dry:                          # cấm 2 lô CÙNG lane chạy song song (đè dòng/tập của nhau); khác lane thì được
        import msvcrt
        _khoa = open(LOG_DIR / f"{a.profile}.lock", "a+")
        try:
            msvcrt.locking(_khoa.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise SystemExit(f"lane {a.profile} đang có lô khác chạy → DỪNG (đợi lô đó xong)")
    gio =_dt.datetime.now().strftime("%m%d_%H%M")
    tong = []

    def ghi(s):
        print(s, flush=True)
        tong.append(s)

    ghi(f"LÔ {tab} STT {a.tu}→{a.den} · model {a.model} · {gio}")
    for stt in range(a.tu, a.den + 1):
        r = doc_tab(tab).get(stt)          # đọc lại mỗi tập: tập trước có thể vừa ghi cột C/D
        if not r:
            ghi(f"STT {stt}: không có dòng trên tab {tab} → DỪNG lô")
            break
        chang = chon_chang(r["d"])
        if not chang or (a.chi_chang and chang != a.chi_chang):
            ghi(f"STT {stt}: D='{rv.dong_dau(r['d']) or '(trống)'}' → bỏ qua")
            continue
        muc_tieu = CHANG[chang][1]
        loi_goc = kiem_truoc(prof, stt, r, chang, whisper=not a.dry)   # --dry: bỏ đường whisper (vài phút/video)
        if loi_goc:
            ghi(f"STT {stt}: ✗ CHẶN TRƯỚC KHI CHẠY (chặng {chang}) — {loi_goc} · thư mục {_thu_muc(r['folder']) or '(chưa có)'}")
            if not a.dry and not a.tiep_khi_loi:
                ghi("  → DỪNG lô (thiếu hook gốc = không dựng). Bổ sung lời gốc rồi chạy lại cùng lệnh.")
                break
            continue
        if a.dry:
            ghi(f"STT {stt}: D='{rv.dong_dau(r['d']) or '(trống)'}' → sẽ chạy chặng {chang} (đích D='{muc_tieu}')")
            continue
        log = LOG_DIR / f"{tab}_STT{stt}_{chang}_{_dt.datetime.now().strftime('%m%d_%H%M')}.jsonl"
        ghi(f"STT {stt}: chặng {chang} → claude -p mới · log {log}")
        bao_dang_chay(prof, tab, stt, r, chang)
        t0 = _dt.datetime.now()
        dan = f"\n=== ANH DẶN THÊM (THẮNG luật mặc định khi mâu thuẫn) ===\n{a.ghi_chu}\n" if a.ghi_chu else ""
        ket = chay_claude(lam_prompt(prof, tab, stt, r, chang) + dan, a.model, log, a.timeout_phut * 60, a.tran_usd)
        phut = (_dt.datetime.now() - t0).total_seconds() / 60
        cuoi = (ket.get("result") or "").strip().splitlines()
        d_moi = rv.dong_dau(doc_tab(tab).get(stt, {}).get("d", ""))
        dat = d_moi == muc_tieu
        ghi(f"  {'✓' if dat else '✗'} D='{d_moi or '(trống)'}' (đích '{muc_tieu}') · {phut:.0f} phút · "
            f"{ket.get('num_turns', '?')} lượt · ${ket.get('total_cost_usd', 0):.2f} · "
            f"ctx đỉnh {ket.get('ctx_dinh', 0) // 1000}K · "
            f"{cuoi[-1] if cuoi else '(không có kết quả)'}")
        for dong in cuoi[-12:-1]:            # báo cáo ngắn của phiên (đường dẫn, việc anh cần làm) → vào TONG_KET
            ghi(f"    | {dong}")
        if not dat and not a.tiep_khi_loi:
            ghi("  → DỪNG lô (tập này chưa tới mốc). Xem log trên, sửa xong chạy lại cùng lệnh — tập đã xong tự bỏ qua.")
            break
    bao = LOG_DIR / f"TONG_KET_{gio}_{a.profile}.txt"   # kèm mã lane: chay_hang_doi.py mở nhiều lane cùng phút
    bao.write_text("\n".join(tong) + "\n", encoding="utf-8")
    print(f"Tổng kết: {bao}")


if __name__ == "__main__":
    main()
