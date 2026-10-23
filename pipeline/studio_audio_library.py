r"""Gọi Thư viện âm thanh YouTube Studio (Audio Library) bằng phiên đăng nhập của 1 tab Chrome (Playwright CDP).

Không có API công khai → dùng API nội bộ Studio, ký SAPISIDHASH ngay trong tab (cookie SAPISID + ytcfg):
  creator_music/list_tracks  — danh mục, mỗi bài có genres/moods/instruments/licenseType (đo 2026-10-23: >6.000 bài,
                               ~84% giấy phép YOUTUBE, còn lại CCBY_4 phải ghi công)
  creator_music/get_tracks   — mask.includeDownloadUrl → link googlevideo mp3 320 kbps (y nút Download trên UI)
Profile mặc định (anh chốt 2026-10-23): hoangletran6868@gmail.com = D:\CLAUDE\RENDER_IMG\chrome_profile_gemini2 cổng 9339
(cũng là profile dự phòng Flow PRO của hen_gio) → chỉ MỞ THÊM 1 tab, KHÔNG đụng tab khác, người gọi tự đóng đúng tab trả về.
Kênh nào cũng thấy cùng 1 thư viện. Máy khác: dùng Chrome nào cũng được miễn tài khoản CÓ KÊNH YouTube (--port).

SỔ ĐĂNG KÝ BÀI (dùng chung MỌI dự án, 2 máy, qua Syncthing): `so_dang_ky_bai.json` trong thư mục
FlowHandoff_local\shared\nhac_audio_library — trackId -> kênh đang dùng. Mỗi kênh 1 bộ bài riêng: tool nào chọn bài
cũng phải loại bài kênh khác đã đăng ký (kenh_dung) rồi ghi bài mình chọn (dang_ky).
"""
import json, time, urllib.request
from datetime import date
from pathlib import Path

PROFILE = {9339: r"D:\CLAUDE\RENDER_IMG\chrome_profile_gemini2",      # hoangletran6868 — mặc định, CÓ kênh YouTube
           9337: r"D:\CLAUDE\RENDER_IMG\chrome_profile_ultra2"}       # nguyenquoctuan — CHƯA có kênh → không vào được Studio
GOI = [Path(__file__).resolve().parent,                                                  # khi chạy từ chính gói shared
       Path(r"E:\CLAUDE\YOUTUBE\FlowHandoff_local\shared\nhac_audio_library"),          # máy 2
       Path(r"E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\nhac_audio_library")]    # máy 1


def _so():
    for d in GOI:
        if (d / "so_dang_ky_bai.json").exists():
            return d / "so_dang_ky_bai.json"
    return None


def kenh_dung():
    """trackId -> kênh (sổ chung). Không thấy sổ → {} kèm cảnh báo (không chặn chạy)."""
    f = _so()
    if not f:
        print("  ⚠ không thấy so_dang_ky_bai.json (thư mục shared\\nhac_audio_library) — không chống trùng được giữa dự án")
        return {}
    return {k: v["kenh"] for k, v in json.loads(f.read_text(encoding="utf-8")).items()}


def dang_ky(tracks, kenh, du_an):
    """Ghi bài kênh này đang dùng; bài cũ của chính kênh đó (không còn dùng) được gỡ khỏi sổ."""
    f = _so()
    if not f:
        return
    so = {k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if v["kenh"] != kenh}
    for t in tracks:
        so[t["trackId"]] = {"kenh": kenh, "du_an": du_an, "title": t["title"],
                            "artist": (t.get("artist") or {}).get("name"), "ngay": str(date.today())}
    f.write_text(json.dumps(so, ensure_ascii=False, indent=1), encoding="utf-8")

JS_GOI = r"""async ({path, body}) => {
  const ck = Object.fromEntries(document.cookie.split('; ').map(s => [s.split('=')[0], s.split('=').slice(1).join('=')]));
  const sap = ck['SAPISID'] || ck['__Secure-3PAPISID'], ts = Math.floor(Date.now() / 1000), o = 'https://studio.youtube.com';
  const h = [...new Uint8Array(await crypto.subtle.digest('SHA-1', new TextEncoder().encode(`${ts} ${sap} ${o}`)))]
            .map(b => b.toString(16).padStart(2, '0')).join('');
  const c = window.ytcfg.data_, cid = body.channelId;
  body.context = {client: {clientName: 62, clientVersion: c.INNERTUBE_CLIENT_VERSION, hl: 'en', gl: 'VN'},
                  user: {delegationContext: {externalChannelId: cid, roleType: {channelRoleType: 'CREATOR_CHANNEL_ROLE_TYPE_OWNER'}}}};
  const r = await fetch(`/youtubei/v1/creator_music/${path}?alt=json&key=${c.INNERTUBE_API_KEY}`, {method: 'POST', credentials: 'include',
    headers: {'content-type': 'application/json', authorization: `SAPISIDHASH ${ts}_${h}`, 'x-origin': o,
              'x-youtube-client-name': '62', 'x-youtube-client-version': c.INNERTUBE_CLIENT_VERSION, 'x-goog-authuser': '0'},
    body: JSON.stringify(body)});
  return {status: r.status, j: await r.json()};
}"""


def mo_tab(p, port):
    """-> (page, channel id). Không có Chrome ở cổng → dừng, in lệnh mở đúng profile cũ (không tự tạo profile mới)."""
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=5)
    except Exception:
        raise SystemExit(f"✗ không có Chrome ở cổng {port}. Mở đúng lệnh cũ (chạy nền, KHÔNG tạo profile mới):\n"
                         f'  chrome.exe --user-data-dir="{PROFILE.get(port, "<profile của cổng này>")}" '
                         f'--remote-debugging-port={port} --no-first-run')
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    pg = b.contexts[0].new_page()
    try:
        pg.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_url("**/channel/UC*", timeout=90000)
        cid = pg.url.split("/channel/")[1].split("/")[0]
        pg.goto(f"https://studio.youtube.com/channel/{cid}/music", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_selector("ytmus-library-row", timeout=90000)
    except Exception as e:
        pg.close()
        raise SystemExit(f"✗ không vào được Thư viện âm thanh (profile chưa đăng nhập YouTube?): {e}")
    return pg, cid


def goi(pg, path, body):
    for lan in range(4):
        r = pg.evaluate(JS_GOI, {"path": path, "body": body})
        if r["status"] == 200:
            return r["j"]
        print(f"    {path} HTTP {r['status']} → thử lại", str(r["j"])[:150])
        time.sleep(5 * (lan + 1))
    raise SystemExit(f"✗ {path} lỗi 4 lần")


def danh_muc(pg, cid, f, lam_moi=False):
    """Toàn bộ danh mục (cache ở file f)."""
    if f.exists() and not lam_moi:
        return json.loads(f.read_text(encoding="utf-8"))
    tracks, tok = {}, None
    while True:
        pi = {"pageSize": 100, **({"pageToken": tok} if tok else {})}
        j = goi(pg, "list_tracks", {"channelId": cid, "filter": {}, "pageInfo": pi, "trackOrder": {
            "orderField": "CREATOR_MUSIC_TRACK_SORT_FIELD_RELEASE_DATE", "orderDirection": "ORDER_DIRECTION_DESC"}})
        tracks.update({t["trackId"]: t for t in j.get("tracks", [])})
        tok = (j.get("pageInfo") or {}).get("nextPageToken")
        if not tok or not j.get("tracks"):
            break
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(list(tracks.values()), ensure_ascii=False), encoding="utf-8")
    print(f"  danh mục: {len(tracks)} bài → {f}")
    return list(tracks.values())


def _url(x):
    if isinstance(x, str) and x.startswith("https://") and "videoplayback" in x:
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        if (u := _url(v)):
            return u


def tai(pg, cid, t, thu_muc):
    """mp3 gốc 320 kbps → thu_muc/<trackId>.mp3 (đã có thì dùng lại)."""
    f = thu_muc / f"{t['trackId']}.mp3"
    if not f.exists():
        u = _url(goi(pg, "get_tracks", {"channelId": cid, "trackIds": [t["trackId"]], "mask": {"includeDownloadUrl": True}}))
        if not u:
            raise RuntimeError("get_tracks không trả link tải")
        r = pg.context.request.get(u, timeout=180000)
        if not r.ok or len(r.body()) < 500_000:
            raise RuntimeError(f"HTTP {r.status} {len(r.body())} byte")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(r.body())
    return f
