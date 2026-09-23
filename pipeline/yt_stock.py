"""yt_stock.py — lấy B-ROLL TƯ LIỆU từ YouTube, CHỈ những video Creative Commons BY.

VÌ SAO CÓ FILE NÀY
    Kho stock hiện chỉ có NASA / Wikimedia / Pexels — toàn ảnh & clip hiện đại. Phim tư liệu
    lịch sử (1940s–1970s: tàu chiến, máy bay, tin thời sự) gần như chỉ còn ở YouTube, và YouTube
    CÓ một lớp video được chính chủ kênh khai giấy phép "Creative Commons Attribution (reuse
    allowed)" — dùng lại hợp pháp, điều kiện duy nhất là GHI NGUỒN.

RÀNG BUỘC CỨNG (lý do tool tồn tại — đây là phép kiểm bằng MÁY, không phải khuyến nghị)
    1. Chỉ tải video có `license` == LICENSE_CC_BY, đúng từng ký tự, do chính yt-dlp đọc ra.
       Mọi giá trị khác — kể cả None (= "Giấy phép YouTube tiêu chuẩn") — thì BỎ, in lý do.
       Bộ lọc CC của trang tìm kiếm YouTube (sp=EgIwAQ%3D%3D) KHÔNG được tin: `extract_flat`
       không trả trường `license` nên phải gọi `extract_info` lần hai cho TỪNG video.
       Đã verify thật 2026-09-23: yP0Ias0Jcek → None (từ chối) · DtpAIIVCMQw, YH7f8WiGjys,
       jx5GQIn47Ko → CC BY (nhận).
    2. CC BY bắt buộc ghi nguồn ⇒ KHÔNG dựng được dòng credit đầy đủ (tên video + kênh + URL +
       giấy phép) thì KHÔNG tải. Xem `dong_credit()`.
    3. B-roll không được mang chữ nước ngoài trên hình (luật dự án, memory
       `broll-khong-duoc-mang-chu-la`). Video YouTube hay có thanh chú thích/watermark ở đáy ⇒
       `--crop-bottom <tỉ lệ>` cắt đáy khi chuẩn hoá. Tool CẢNH BÁO chứ không tự soi được —
       người dùng vẫn phải xem lại clip tải về.

KHỚP HẠ TẦNG SẴN CÓ (không phát minh lại)
    - Manifest: `<tập>\\stock\\manifest.jsonl`, mỗi dòng 1 JSON, đúng schema `stock_cut.py` đang
      đọc: src/id/url/title/duration_s/license/credit/query/chapter (+ file/bytes như stockfetch).
      Bản ghi của tool này mang `src="youtube_cc"`.
    - Tên file: `yt_<video_id>_<chỉ số đoạn>.mp4` (kho đang có `nasa_*`, `pexels_*`, `ev0*`).
    - ffmpeg: TÁI DÙNG `hook_stage._ffmpeg_tren_path()` (4 bẫy lồng nhau đã ghi ở docstring bên đó).
    - player_client thử theo thứ tự android → web → ios (memory `ytdlp-tai-nguon-thu-lai`).

CLI
    py -3.13 yt_stock.py tim --query "declassified navy footage 1945" --n 15
    py -3.13 yt_stock.py tai --id DtpAIIVCMQw --ranges 120-128,300-306 \\
        --out "E:\\CLAUDE\\YOUTUBE\\h2dev\\assets\\toshi-densetsu-jp\\ep05-bermuda-triangle\\stock" \\
        --chapter 2 --crop-bottom 0.17
    py -3.13 yt_stock.py credits --tap "E:\\CLAUDE\\YOUTUBE\\h2dev\\assets\\toshi-densetsu-jp\\ep05-bermuda-triangle"
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LICENSE_CC_BY = "Creative Commons Attribution license (reuse allowed)"
SRC = "youtube_cc"
# Bộ lọc "Creative Commons" của chính trang kết quả YouTube (đã chạy thật). Vẫn phải kiểm lại
# từng video — bộ lọc này chỉ thu hẹp, không phải bằng chứng.
SEARCH_URL = "https://www.youtube.com/results?search_query={q}&sp=EgIwAQ%3D%3D"
# android đứng ĐẦU: 'web' hay trả "Requested format is not available" cho video mà android tải
# được (memory `ytdlp-tai-nguon-thu-lai`, và đo lại ở hook_stage.KHUNG_HINH_THU).
TAI_THU = (
    ("android", "bv*[height<=1080]/b[height<=1080]/b"),
    ("web", "bv*[height<=1080]+ba/b[height<=1080]/b"),
    ("ios", "bv*[height<=1080]/best"),
)
FMT_MAC_DINH = "bv*[height<=1080]/b[height<=1080]/b"
# ⚠ ĐỘ PHÂN GIẢI (đo thật 2026-09-23): máy này CHƯA có JS runtime (Deno) nên yt-dlp không giải được
# `nsig` ⇒ các format adaptive (720p+) KHÔNG hiện ra; client `android` chỉ còn đúng 1 format 360p, các
# client `web`/`ios`/`mweb` trả thẳng "No video formats found". Client **`tv_embedded` cho tới 480p** —
# cao nhất lấy được trong tình trạng hiện tại. Với phim tư liệu B&W thập niên 1940 thì 480p chấp nhận
# được (hạt phim che bớt), nhưng cần nét hơn thì phải cài Deno rồi bỏ `--clients` đi.
CLIENT_NET_NHAT = "tv_embedded,android"
CANH_BAO_CHU = ("⚠ B-roll KHÔNG được mang chữ nước ngoài trên hình — xem lại từng clip đã tải; "
                "còn thanh chú thích/watermark ở đáy thì tải lại với --crop-bottom lớn hơn.")


class KhongDuocPhep(RuntimeError):
    """Video không đủ điều kiện dùng lại (sai giấy phép / không ghi được nguồn)."""


# ---------------------------------------------------------------------------- tra giấy phép


def _opts_co_ban(proxy=None):
    o = {"quiet": True, "no_warnings": True, "noprogress": True}
    if proxy:
        o["proxy"] = proxy
    import fetch_script
    fetch_script._ap_cookies(o)          # cùng cookie với mọi lời gọi YouTube khác của dự án
    return o


def lay_thong_tin(video_id, proxy=None):
    """Metadata ĐẦY ĐỦ của 1 video (có trường `license`). Lỗi mạng → ném ra cho người gọi xử."""
    import yt_dlp
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(_opts_co_ban(proxy)) as y:
        info = y.extract_info(url, download=False)
    return {
        "id": info.get("id") or video_id,
        "url": info.get("webpage_url") or url,
        "title": (info.get("title") or "").strip(),
        "channel": (info.get("uploader") or info.get("channel") or "").strip(),
        "channel_url": info.get("uploader_url") or info.get("channel_url") or "",
        "duration_s": int(info.get("duration") or 0),
        "license": info.get("license"),
    }


def la_cc_by(info):
    """Phép kiểm bằng MÁY. So khớp ĐÚNG chuỗi — None (giấy phép YouTube tiêu chuẩn) là False."""
    return (info.get("license") or "") == LICENSE_CC_BY


def dong_credit(info):
    """Dòng ghi nguồn CC BY. Thiếu kênh hoặc URL ⇒ '' (người gọi phải từ chối tải)."""
    if not info.get("channel") or not info.get("url"):
        return ""
    return f"{info['channel']} · {info['url']}"


def kiem_dung_duoc(info):
    """Ném KhongDuocPhep kèm lý do tiếng Việt nếu video không đủ điều kiện. Trả dòng credit."""
    if not la_cc_by(info):
        lic = info.get("license") or "None (Giấy phép YouTube tiêu chuẩn)"
        raise KhongDuocPhep(f"giấy phép '{lic}' ≠ CC BY → KHÔNG tải")
    if not (info.get("title") or "").strip():
        raise KhongDuocPhep("không đọc được tên video → không ghi nổi nguồn → KHÔNG tải")
    credit = dong_credit(info)
    if not credit:
        raise KhongDuocPhep("thiếu tên kênh hoặc URL → không ghi nổi nguồn → KHÔNG tải")
    return credit


# ---------------------------------------------------------------------------- tìm


def tim(query, n=15, proxy=None, nghi=0.4):
    """Liệt kê video trong bộ lọc CC của YouTube, mỗi video kiểm lại giấy phép LẦN HAI.

    Trả list dict {id,title,channel,url,duration_s,license,ok,ly_do}. KHÔNG tải gì cả.
    """
    import yt_dlp
    from urllib.parse import quote_plus
    url = SEARCH_URL.format(q=quote_plus(query))
    opts = dict(_opts_co_ban(proxy), extract_flat=True, playlistend=int(n))
    with yt_dlp.YoutubeDL(opts) as y:
        flat = y.extract_info(url, download=False)
    ra = []
    for e in (flat.get("entries") or [])[:int(n)]:
        vid = e.get("id")
        if not vid:
            continue
        try:
            info = lay_thong_tin(vid, proxy=proxy)
        except Exception as ex:
            ra.append({"id": vid, "title": e.get("title") or "", "channel": "", "url": "",
                       "duration_s": 0, "license": None, "ok": False,
                       "ly_do": f"không tra được giấy phép: {type(ex).__name__} {str(ex)[:80]}",
                       "query": query})
            continue
        try:
            kiem_dung_duoc(info)
            info.update(ok=True, ly_do="CC BY — dùng được")
        except KhongDuocPhep as ex:
            info.update(ok=False, ly_do=str(ex))
        info["query"] = query
        ra.append(info)
        time.sleep(nghi)                 # 1 request/lượt, đừng đấm YouTube
    return ra


# ---------------------------------------------------------------------------- tải


def doc_ranges(s):
    """'120-128,300-306' hoặc '2:00-2:08' → [(120.0,128.0), ...]. Sai cú pháp → ValueError."""
    ra = []
    for phan in str(s).split(","):
        phan = phan.strip()
        if not phan:
            continue
        m = re.match(r"^([\d:.]+)\s*-\s*([\d:.]+)$", phan)
        if not m:
            raise ValueError(f"đoạn '{phan}' sai cú pháp (đúng: 120-128 hoặc 2:00-2:08)")
        a, b = _giay(m.group(1)), _giay(m.group(2))
        if b <= a:
            raise ValueError(f"đoạn '{phan}' có mốc kết thúc ≤ mốc bắt đầu")
        ra.append((a, b))
    if not ra:
        raise ValueError("--ranges rỗng")
    return ra


def _giay(v):
    if ":" in v:
        h = [float(x) for x in v.split(":")]
        return sum(p * 60 ** i for i, p in enumerate(reversed(h)))
    return float(v)


def _thu_client(clients):
    """Đổi chuỗi '--clients' thành danh sách (client, format) để thử theo thứ tự. Rỗng → TAI_THU."""
    if not clients:
        return TAI_THU
    co = dict(TAI_THU)
    return tuple((c.strip(), co.get(c.strip(), FMT_MAC_DINH)) for c in clients.split(",") if c.strip())


def _tai_doan(video_id, a, b, tho: Path, proxy=None, clients=""):
    """Tải đúng đoạn [a,b) ra file tạm `tho.<ext>`. Trả Path file tải được, hoặc None."""
    import hook_stage
    import qc_visual
    shim = hook_stage._ffmpeg_tren_path()      # 4 bẫy ffmpeg đã vá ở đó, đừng viết lại
    import yt_dlp
    from yt_dlp.utils import download_range_func
    base = dict(_opts_co_ban(proxy),
                download_ranges=download_range_func(None, [(a, b)]),
                force_keyframes_at_cuts=True,
                outtmpl=str(tho) + ".%(ext)s",
                ffmpeg_location=str(shim) if shim else str(Path(qc_visual._ff()).parent))
    err = ""
    thu = _thu_client(clients)
    for i, (client, fmt) in enumerate(thu):
        opts = dict(base, format=fmt, extractor_args={"youtube": {"player_client": [client]}})
        try:
            with yt_dlp.YoutubeDL(opts) as y:
                y.download([f"https://www.youtube.com/watch?v={video_id}"])
            err = ""
            break
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            if i < len(thu) - 1:
                time.sleep(3)
    # format video-only có thể ra .webm → không giả định đuôi file
    got = next((f for f in sorted(tho.parent.glob(tho.name + ".*")) if f.stat().st_size > 10_000), None)
    if not got and err:
        print(f"  ! không tải được đoạn {a:.0f}-{b:.0f}s: {err[:150]}")
    return got


def _chuan_hoa(src: Path, dest: Path, crop_bottom=0.0, fps=30):
    """Cắt đáy (chống chữ/watermark) + xuất mp4 h264 không tiếng. Lỗi ffmpeg → ném CalledProcess."""
    import qc_visual
    r = max(0.0, min(float(crop_bottom), 0.5))
    vf = []
    if r > 0:
        vf.append(f"crop=iw:floor(ih*{1 - r:.4f}/2)*2:0:0")
    vf += [f"fps={fps}", "setsar=1", "format=yuv420p"]
    subprocess.run([qc_visual._ff(), "-y", "-i", str(src), "-an", "-vf", ",".join(vf),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(dest)],
                   check=True, capture_output=True)


def ghi_manifest(stock_dir: Path, rec: dict):
    """Ghi 1 dòng sổ giấy phép + flush/fsync ngay (giống stockfetch: sổ là lý do tồn tại)."""
    man = stock_dir / "manifest.jsonl"
    with man.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def tai(video_id, ranges, out_dir, chapter="", crop_bottom=0.0, query="", proxy=None, fps=30,
        clients=""):
    """Tải các đoạn của MỘT video CC BY về kho stock + ghi manifest.

    Từ chối (ném KhongDuocPhep, KHÔNG tải byte nào) khi giấy phép ≠ CC BY hoặc không dựng nổi
    dòng credit. Trả list bản ghi manifest đã ghi.
    """
    info = lay_thong_tin(video_id, proxy=proxy)
    credit = kiem_dung_duoc(info)                     # ← cổng cứng, đứng TRƯỚC mọi lệnh tải
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ra = []
    for i, (a, b) in enumerate(ranges, 1):
        tho = out_dir / f".tmp_yt_{info['id']}_{i:02d}"
        dest = out_dir / f"yt_{info['id']}_{i:02d}.mp4"
        try:
            got = _tai_doan(info["id"], a, b, tho, proxy=proxy, clients=clients)
            if not got:
                continue
            _chuan_hoa(got, dest, crop_bottom=crop_bottom, fps=fps)
        except Exception as e:
            print(f"  ! đoạn {i} ({a:.0f}-{b:.0f}s) hỏng: {type(e).__name__} {str(e)[:120]}")
            dest.unlink(missing_ok=True)
            continue
        finally:
            for f in out_dir.glob(tho.name + ".*"):
                f.unlink(missing_ok=True)
        rec = {"src": SRC, "id": f"{info['id']}_{i:02d}", "url": info["url"],
               "title": info["title"], "duration_s": round(b - a, 2),
               "license": LICENSE_CC_BY, "credit": credit, "query": query,
               "chapter": str(chapter), "file": dest.name, "bytes": dest.stat().st_size,
               "doan": f"{a:.1f}-{b:.1f}", "crop_bottom": round(float(crop_bottom), 3),
               "accessed": time.strftime("%Y-%m-%d")}
        ghi_manifest(out_dir, rec)
        ra.append(rec)
        print(f"  ✓ {dest.name:<28} {rec['bytes']//1024:>7} KB  [{a:.0f}-{b:.0f}s]")
    return ra


# ---------------------------------------------------------------------------- credits


def viet_credits(tap_dir: Path, stock_dir=None, ra_file=None):
    """Sinh lại `credits.txt` của một tập TỪ MANIFEST (sổ giấy phép = nguồn chân lý).

    `scenes.json` chỉ dùng để ĐẾM số cảnh mỗi file. Title/credit/license LUÔN lấy từ manifest —
    đúng lỗi đã xảy ra ở ep05-bermuda-triangle: ảnh bằng chứng `ev0*.jpg` mang title/credit của
    clip Pexels mà nó thay thế (ev01 máy bay TBM Avenger 1945 ghi thành "the sun setting over the
    ocean… — Manav ."). Gốc rễ nằm ở `stock_cut.gan_bang_chung` (đã vá cùng đợt); hàm này chữa
    những tập ĐÃ dựng mà không phải render lại.
    """
    tap_dir = Path(tap_dir)
    stock_dir = Path(stock_dir) if stock_dir else tap_dir / "stock"
    ra_file = Path(ra_file) if ra_file else tap_dir / "credits.txt"
    import stock_cut
    man = stock_cut.doc_manifest(stock_dir)
    # `evidence.json` của tập là nơi ghi CHÚ THÍCH tiếng Nhật của từng ảnh bằng chứng; một số bản
    # ghi trong manifest (src="commons", tải tay) không có `title` lẫn `caption` — không có tầng
    # này thì credits.txt tụt xuống in TÊN FILE (vd "ev03c_cessna182_reference.jpg"), đúng nhưng
    # vô nghĩa với người đọc. KHÔNG bao giờ lùi tiếp xuống title của scene: với file bằng chứng,
    # title trong scene chính là thứ đã bị gán nhầm (xem docstring).
    cap_ev = {}
    ev_f = tap_dir / "evidence.json"
    if ev_f.exists():
        try:
            for e in json.loads(ev_f.read_text(encoding="utf-8")):
                if e.get("file") and e.get("caption"):
                    cap_ev[Path(e["file"]).name] = e["caption"]
        except Exception as ex:
            print(f"  ! đọc evidence.json lỗi, bỏ qua: {type(ex).__name__} {str(ex)[:80]}")
    scenes_f = next((tap_dir / t for t in ("scenes.json", "scenes_test.json")
                     if (tap_dir / t).exists()), None)
    if not scenes_f:
        raise FileNotFoundError(f"không thấy scenes.json trong {tap_dir}")
    scenes = json.loads(scenes_f.read_text(encoding="utf-8"))
    # HOOK 20–30s đầu video dùng tư liệu RIÊNG, không nằm trong `scenes.json` của thân video —
    # bỏ qua là thiếu hẳn phần ghi nguồn của 20–30 giây mà người xem gặp ĐẦU TIÊN, và với CC BY
    # thì thiếu ghi nguồn là vi phạm giấy phép. Script dựng hook ghi lại danh sách file đã dùng ở
    # `hook/hook_shots.json` ([{file, n}] hoặc [{file}]), hàm này gộp vào như cảnh thường.
    hook_f = tap_dir / "hook" / "hook_shots.json"
    if hook_f.exists():
        try:
            for h in json.loads(hook_f.read_text(encoding="utf-8")):
                scenes += [{"file": h["file"], "hook": True}] * int(h.get("n", 1))
        except Exception as ex:
            print(f"  ! đọc hook/hook_shots.json lỗi, bỏ qua: {type(ex).__name__} {str(ex)[:80]}")
    dung, thieu = {}, []
    for c in scenes:
        f = c.get("file")
        if not f:
            continue
        d = dung.get(f)
        if d is None:
            rec = man.get(f)
            if rec is None:
                # Ảnh AI tự vẽ nằm ngoài kho stock → không có trong sổ, nhưng vẫn phải ghi nguồn
                # (chính mình). Lấy theo scene, và ghi nhận để in cảnh báo.
                if not c.get("anh_ai"):
                    thieu.append(f)
                rec = {"title": c.get("title") or f, "credit": c.get("credit") or "",
                       "license": c.get("license") or "?"}
            d = dung[f] = {"n": 0,
                           "title": rec.get("title") or rec.get("caption") or cap_ev.get(f) or f,
                           "credit": rec.get("credit") or "", "license": rec.get("license") or "?"}
        d["n"] += 1
    # Một dòng = một nguồn. Credit lấy từ Commons có thể chứa XUỐNG DÒNG (vd credit của bản đồ
    # Flight 19: "NASA, Landsat image" + "Modified by Marikanto" cách nhau bằng dòng trống) — để
    # nguyên là dòng đó vỡ làm đôi, nửa sau mất cả dấu "-" lẫn tên nguồn, đọc ra như một mục lạc
    # loài. Ép mọi khoảng trắng về 1 dấu cách.
    # lẫn tên nguồn, đọc ra như một mục lạc loài. Ép mọi khoảng trắng về 1 dấu cách.
    def _1dong(x):
        return re.sub(r"\s+", " ", str(x or "")).strip()

    dong = ["【出典 / Sources】", ""]
    for f, d in sorted(dung.items(), key=lambda x: -x[1]["n"]):
        dong.append(f"- {_1dong(d['title'])[:70]} — {_1dong(d['credit']) or '—'} "
                    f"[{_1dong(d['license'])}] ({d['n']} cảnh · {f})")
    ra_file.write_text("\n".join(dong) + "\n", encoding="utf-8")
    return {"file": ra_file, "n_nguon": len(dung), "thieu_manifest": sorted(set(thieu))}


# ---------------------------------------------------------------------------- CLI


def main():
    ap = argparse.ArgumentParser(description="B-roll YouTube Creative Commons BY (hợp pháp, có ghi nguồn)")
    sub = ap.add_subparsers(dest="lenh", required=True)

    p1 = sub.add_parser("tim", help="liệt kê video CC BY theo từ khoá (KHÔNG tải)")
    p1.add_argument("--query", required=True)
    p1.add_argument("--n", type=int, default=15)
    p1.add_argument("--proxy", default="")
    p1.add_argument("--json", default="", help="ghi kết quả ra file JSON")

    p2 = sub.add_parser("tai", help="tải các đoạn của 1 video CC BY vào kho stock")
    p2.add_argument("--id", required=True, help="video_id YouTube")
    p2.add_argument("--ranges", required=True, help="vd 120-128,300-306 (giây) hoặc 2:00-2:08")
    p2.add_argument("--out", required=True, help="thư mục kho stock của tập (…\\<tập>\\stock)")
    p2.add_argument("--chapter", default="", help="chương của tập, ghi vào manifest")
    p2.add_argument("--crop-bottom", type=float, default=0.0,
                    help="cắt bỏ tỉ lệ đáy khung (0.17 = bỏ 17%% dưới) — chống chữ/watermark")
    p2.add_argument("--query", default="", help="từ khoá đã dùng để tìm (stock_cut đọc field này)")
    p2.add_argument("--fps", type=int, default=30)
    p2.add_argument("--proxy", default="")
    p2.add_argument("--clients", default="",
                    help=f"thứ tự player_client, vd '{CLIENT_NET_NHAT}' (nét nhất khi máy chưa có Deno)")

    p3 = sub.add_parser("credits", help="sinh lại credits.txt của 1 tập từ manifest + scenes.json")
    p3.add_argument("--tap", required=True, help="thư mục tập")
    p3.add_argument("--stock", default="", help="kho stock (mặc định <tập>\\stock)")
    p3.add_argument("--out", default="", help="file ra (mặc định <tập>\\credits.txt)")

    a = ap.parse_args()

    if a.lenh == "tim":
        kq = tim(a.query, n=a.n, proxy=a.proxy or None)
        for r in kq:
            dau = "✓" if r["ok"] else "⤫"
            print(f"{dau} {r['id']}  {(r['title'] or '')[:58]:<60} {r['ly_do']}")
        print(f"\n[xong] {sum(1 for r in kq if r['ok'])}/{len(kq)} video dùng được (CC BY).")
        print(CANH_BAO_CHU)
        if a.json:
            Path(a.json).write_text(json.dumps(kq, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  → {a.json}")
        return 0

    if a.lenh == "tai":
        try:
            recs = tai(a.id, doc_ranges(a.ranges), a.out, chapter=a.chapter,
                       crop_bottom=a.crop_bottom, query=a.query, proxy=a.proxy or None, fps=a.fps,
                       clients=a.clients)
        except KhongDuocPhep as e:
            print(f"⤫ {a.id}: {e}")
            return 2
        print(f"[xong] {len(recs)} đoạn → {a.out} (sổ giấy phép: manifest.jsonl)")
        if recs:
            print(f"  ghi nguồn: {recs[0]['title']} — {recs[0]['credit']} [{LICENSE_CC_BY}]")
        if not a.crop_bottom:
            print("  ⚠ chưa cắt đáy (--crop-bottom 0) — video YouTube hay có thanh chú thích ở đáy.")
        print(CANH_BAO_CHU)
        return 0 if recs else 1

    kq = viet_credits(a.tap, a.stock or None, a.out or None)
    print(f"[xong] {kq['n_nguon']} nguồn → {kq['file']}")
    if kq["thieu_manifest"]:
        print(f"  ⚠ {len(kq['thieu_manifest'])} file KHÔNG có trong manifest (giấy phép không rõ): "
              f"{', '.join(kq['thieu_manifest'][:8])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
