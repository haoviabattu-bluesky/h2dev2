r"""tao_project_soat.py — tạo Project ChatGPT SOÁT KỊCH BẢN cho 1 lane trên 2 tài khoản (acc1 cổng 9335, acc2 cổng 9336).

Mỗi tài khoản: giữ phiên qua pipeline\gptweb_pool.py (khoá + chỉ đóng Chrome do mình mở) → tìm/tạo Project tên = tab sheet
(tài khoản đã có Project trùng tên mà không phải của lane này, vd của YT-TITLE-RESEARCH → dùng "<tab>-script") → Project-only
memory → đặt Instructions + tải file .md trong --dir → mở 1 hội thoại giao vai (GPT trả "Hiểu.") → in id/tên/link để điền
profile `script.soat_gptweb.{urls,projects}`. Hàm giao diện mượn CHỈ ĐỌC từ YT-TITLE-RESEARCH\src\chatgpt_project.py.

  py -3.13 -X utf8 tools\chatgpt_web\tao_project_soat.py --profile teinengo-fuufu --dir CHATGPT_PROJECTS\J-teinengo-fuufu-script
  (--acc acc1 để chỉ làm 1 tài khoản · --ghi để tự điền vào profile)
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src")
import gptweb_pool as gp   # noqa: E402
import profiles            # noqa: E402

GIAO_VAI = ("Giao vai: bạn là biên tập viên kịch bản của kênh này, làm đúng Instructions và các file trong Project. "
            "Mỗi tập tôi sẽ gửi tiêu đề + tư liệu + toàn văn kịch bản để bạn thẩm định. Lần này chỉ xác nhận, trả lời đúng một chữ: Hiểu.")


def _ids_da_gan(lane_id):
    ids = set()
    for f in (ROOT / "profiles" / "profiles").glob("*.json"):
        try:
            o = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if o.get("id") == lane_id:
            continue
        for v in (((o.get("script") or {}).get("soat_gptweb") or {}).get("projects") or {}).values():
            ids.add((v or {}).get("id"))
    return ids


def lam_1_tk(tk, prof, thu_muc, log=print):
    import chatgpt_project as cp
    import gpt_web_client as gw
    from playwright.sync_api import sync_playwright
    tab = prof["publish"]["sheet_tab"]
    ins = (thu_muc / "INSTRUCTIONS.txt").read_text(encoding="utf-8")
    files = sorted(p for p in thu_muc.glob("*.md"))
    chu = f"{prof['id']}:tao_project"
    gp.mo_phien(tk, chu, log)
    try:
        with sync_playwright() as pw:
            page = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{tk['port']}").contexts[0].new_page()
            try:
                page.goto("https://chatgpt.com/", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector(gw.COMPOSER_SEL, timeout=60000)
                ds = cp._list_projects(page)
                log(f"  [{tk['ten']}] có {len(ds)} Project: " + ", ".join(p["name"] for p in ds))
                khac = _ids_da_gan(prof["id"])
                # Anh đổi tab sheet → Project cũ của CHÍNH lane này đổi tên theo (giữ file + hội thoại), không tạo mới
                cu = (((prof.get("script") or {}).get("soat_gptweb") or {}).get("projects") or {}).get(tk["ten"]) or {}
                cu = next((p for p in ds if p["id"] == cu.get("id")), None)
                if cu and cu["name"] not in (tab, f"{tab}-script") and not any(p["name"] == tab for p in ds):
                    g = cp._gizmo(page, cu["id"])["gizmo"]
                    cp._api(page, "PATCH", f"/backend-api/projects/{cu['id']}",
                            {"name": tab, "emoji": g["display"].get("emoji"), "theme": g["display"].get("theme"),
                             "instructions": g.get("instructions")})
                    log(f"  [{tk['ten']}] đổi tên Project '{cu['name']}' → '{tab}' ({cu['id']})")
                    ds = cp._list_projects(page)
                ten = tab
                if any(p["name"] == tab and p["id"] in khac for p in ds) or \
                        (any(p["name"] == tab for p in ds) and any(p["name"] == f"{tab}-script" for p in ds)):
                    ten = f"{tab}-script"
                trung = [p for p in ds if p["name"] == ten]
                if len(trung) > 1:
                    raise SystemExit(f"✗ {tk['ten']}: có {len(trung)} Project tên '{ten}' — anh xoá bớt rồi chạy lại")
                proj = trung[0] if trung else cp._create_project(page, ten, log)
                if proj["id"] in khac:
                    raise SystemExit(f"✗ {tk['ten']}: Project '{ten}' {proj['id']} đang gán cho lane khác — không dùng")
                pid, url = proj["id"], f"https://chatgpt.com/g/{proj['short_url']}/project"
                g = cp._gizmo(page, pid)
                scope = g["gizmo"].get("memory_scope")
                cp._api(page, "PATCH", f"/backend-api/projects/{pid}",
                        {"name": g["gizmo"]["display"]["name"], "emoji": g["gizmo"]["display"].get("emoji"),
                         "theme": g["gizmo"]["display"].get("theme"), "instructions": ins})
                want = {p.name for p in files}
                co = {f["name"] for f in (g.get("files") or [])}
                thieu = [p for p in files if p.name not in co]
                if thieu:
                    cp._upload(page, url, thieu, log)
                    for _ in range(90):
                        time.sleep(2)
                        co = {f["name"] for f in (cp._gizmo(page, pid).get("files") or [])}
                        if want <= co:
                            break
                    else:
                        raise SystemExit(f"✗ {tk['ten']}: tải file chưa đủ sau 180s: thiếu {sorted(want - co)}")
                g = cp._gizmo(page, pid)
                if g["gizmo"].get("instructions") != ins:
                    raise SystemExit(f"✗ {tk['ten']}: instructions đọc lại không khớp")
                log(f"  [{tk['ten']}] Project '{ten}' {pid} · memory {scope} · {len(want)} file · instructions {len(ins)} ký tự")
            finally:
                page.close()
        tra, model, conv = gp._gui(tk, url, GIAO_VAI, log)
        log(f"  [{tk['ten']}] giao vai → {tra.strip()[:60]!r} ({model}) · {conv}")
        return {"id": pid, "ten": ten, "url": conv, "memory_scope": scope, "tra_loi": tra.strip()[:200]}
    finally:
        gp.dong_phien(tk, chu, log)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--acc", default="acc1,acc2")
    ap.add_argument("--ghi", action="store_true", help="điền kết quả vào profile script.soat_gptweb")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    thu_muc = (ROOT / a.dir) if not Path(a.dir).is_absolute() else Path(a.dir)
    kq = {}
    for acc in a.acc.split(","):
        try:
            kq[acc] = lam_1_tk(gp.tai_khoan(acc), prof, thu_muc)
        except (gp.Ban, gp.TaiKhoanHong) as e:
            print(f"  ✗ {acc}: {e}")
    print(json.dumps(kq, ensure_ascii=False, indent=1))
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / f"tao_project_{a.profile}.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.ghi and kq:
        f = ROOT / "profiles" / "profiles" / f"{a.profile}.json"
        o = json.loads(f.read_text(encoding="utf-8"))
        c = o["script"]["soat_gptweb"]
        c.setdefault("urls", {}).update({k: v["url"] for k, v in kq.items()})
        c.setdefault("projects", {}).update({k: {"id": v["id"], "ten": v["ten"]} for k, v in kq.items()})
        c["_urls_note"] = (f"Tạo {time.strftime('%Y-%m-%d')} bằng tools\\chatgpt_web\\tao_project_soat.py (Instructions + file "
                           f"{a.dir}); urls = hội thoại giao vai trong Project của lane.")
        f.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"→ đã ghi {f}")


if __name__ == "__main__":
    main()
