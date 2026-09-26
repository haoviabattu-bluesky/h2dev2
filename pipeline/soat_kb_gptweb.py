r"""soat_kb_gptweb.py — soát kịch bản ĐÃ KHOÁ bằng ChatGPT web, THAY chặng máy 3 (Lane M, anh chốt 2026-09-26).

Vì sao: anh muốn thử để ChatGPT (tài khoản của anh, Project riêng của lane) đọc toàn bộ kịch bản và góp ý như nhà văn,
tab lane (Claude Code) thẩm định từng góp ý — hợp lý thì nhận, chưa hợp lý thì phản biện 1 lượt — rồi tổng hợp thành
viec_tay.txt cho Opus sửa (KHÔNG sửa tay), Sol chấm lại ×2, khoá. Bản khoá đó coi như "máy 3 đã trả".

Field-driven (hàng rào #2): `profile.script.soat_gptweb = {"enabled": true, "url": "<link hội thoại ChatGPT>"}`.
Gửi vào ĐÚNG hội thoại đó (không tạo chat mới) — dùng lại hạ tầng YT-TITLE-RESEARCH\src\gpt_web_client.py
(Chrome E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE cổng 9335, khoá liên tiến trình, selector, model gpt-5-6, bóc dấu trích dẫn).

Dùng:
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-anaba --slug ep02-xxx --lan1
      → dựng tin lượt 1 (bối cảnh kênh + ràng buộc cứng + series_ctx + script.txt) → <tập>\soat_gptweb\tin_1.txt, tra_loi_1.md
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-anaba --slug ep02-xxx --tin <file phản biện>
      → gửi tiếp trong cùng hội thoại → tin_N.txt, tra_loi_N.md
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-anaba --slug ep02-xxx --dung-tin
      → chỉ in đường dẫn tin lượt 1 (không gửi) để đọc lại trước
Sau đó (tab lane): viec_tay.txt → ghi_lock ESCALATE → make_video --den B3G → BAO_CAO_SUA.md vào review\ → cột D =
"Đã sửa kịch bản" → review_may3.py --nhan. Chi tiết: docs\SOP_LANE_M.md §1e.
"""
import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\src")
import ai_steps   # noqa: E402
import profiles   # noqa: E402

LAN1 = """Đây là kịch bản tập mới của kênh {kenh}. Nhờ bạn thẩm định như một nhà văn chuyên nghiệp.

BỐI CẢNH KÊNH
- Tiêu đề tập: {title}
- Khán giả: người Nhật 60+ đang/sắp đi làm thêm, xem trên điện thoại. Video manga ~{phut} phút, đọc bằng NHIỀU GIỌNG (người kể = nhân vật chính, vợ, các vai phụ). Chữ hiện bằng bóng thoại dọc.
- Cấu trúc bắt buộc: hook ~30 giây → đếm ngược 第七位→第一位, mục đầu tiên phải vào TRƯỚC phút 4 → mỗi mục đủ: tên việc · điều kiện/con số có nguồn · ưu điểm · cái bẫy · ai hợp/không hợp → câu hỏi A/B/C giữa bài (30–55%) → kết vị tha → cảm ơn + xin 高評価/チャンネル登録.
- Cung cảm xúc: KÍCH (bị ức chế) → GIẢI TOẢ → VỊ THA.

RÀNG BUỘC CỨNG (đề xuất sửa KHÔNG được phá)
1. Mọi con số tiền/chế độ/pháp lý CHỈ được lấy từ TƯ LIỆU dưới đây. KHÔNG nêu lương giờ cụ thể từng việc (trừ khi tư liệu có).
2. Giữ đúng 7 việc và thứ tự hạng.
3. Mỗi câu thoại「…」là một câu riêng; lời dẫn là câu khác (đọc bằng giọng khác nhau).
4. Nhân vật chính không quát / nói trống không với vợ.
5. Tổng độ dài chỉ được đổi trong khoảng ±3% (hiện {chars:,} chữ, trần {tran:,}) — đề xuất thêm chữ thì chỉ ra chỗ bớt tương ứng.
6. Không sao chép nhân vật/tình tiết/cách đùa của video gốc đối thủ; không lặp lại tình tiết của các tập trước của kênh.
7. Tiêu đề hứa gì thì trong 60 giây đầu phải nói lại, và bài phải trả đủ lời hứa đó.

CẦN BẠN TRẢ LỜI (tiếng Việt; mọi chữ Nhật trích dẫn phải kèm dịch Việt trong ngoặc)
A. Nhận xét tổng: đã hấp dẫn/lôi cuốn chưa, điểm /10, 3 điểm mạnh, 3 điểm yếu nhất.
B. Hook 30 giây đầu có giữ chân người xem 60+ không? Đề xuất cụ thể nếu chưa.
C. Danh sách vấn đề cụ thể, xếp theo mức (NẶNG / VỪA / NHẸ). Mỗi mục: trích NGUYÊN VĂN câu tiếng Nhật đang có → vấn đề → câu tiếng Nhật đề xuất thay thế (viết sẵn, dùng được ngay) + dịch Việt. Tối đa 12 mục, ưu tiên thứ làm người xem bỏ video.
D. Phần kết: đã có cảm ơn + xin like + sub rõ ràng chưa? Có đoạn nào quá nặng thuật ngữ không?
E. Có chỗ nào sai sự thật (so với tư liệu), phi logic, lặp ý, hoặc nhân vật hành xử không tự nhiên không?

TƯ LIỆU ĐƯỢC PHÉP DÙNG (series_ctx của tập):
{ctx}

KỊCH BẢN:
{script}"""


def _cfg(prof):
    c = (prof.get("script") or {}).get("soat_gptweb") or {}
    if not c.get("enabled") or not c.get("url"):
        raise SystemExit(f"✗ lane {prof['id']} chưa khai script.soat_gptweb {{enabled, url}}")
    return c


def gui(url, text, timeout=1200):
    """Gửi 1 tin vào hội thoại có sẵn → (câu trả lời, model thật). Ném lỗi khi hạ tầng hỏng (không rơi sang Sol)."""
    import gpt_web_client as g
    from playwright.sync_api import sync_playwright
    c = g.cfg()
    g._ensure_chrome(c)
    t0 = time.time()
    with g._Lock(c["lock_file"], wait=timeout * 2):
        with sync_playwright() as pw:
            b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{c['cdp_port']}")
            page = b.contexts[0].new_page()
            try:
                page.goto(url.split("?")[0] + f"?model={c['model']}", wait_until="domcontentloaded", timeout=60000)
                g._wait_ready(page)
                time.sleep(4)
                n0 = page.evaluate(g._JS_LAST)["n"]
                g._send(page, text, None)
                st = g._wait_answer(page, n0, timeout)
                out, model = st["text"], "?"
                r = page.evaluate(g._JS_BACKEND, url.split("?")[0].rsplit("/c/", 1)[1])
                if r.get("text", "").strip():
                    out, model = r["text"], r.get("model", "?")
            finally:
                page.close()
    out = g.clean(out)
    g._log(c, f"{round(time.time() - t0)}s · soat_kb_gptweb · model {model} · hỏi {len(text)} chữ · đáp {len(out)} chữ · {url}")
    if not out.strip():
        raise SystemExit("✗ ChatGPT trả rỗng")
    return out, model


def tin_lan1(prof, d):
    import lean_script
    script = (d / "script.txt").read_text(encoding="utf-8")
    title = (d / "title.txt").read_text(encoding="utf-8").strip() if (d / "title.txt").exists() else ""
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else "(không có)"
    m = ai_steps.measure(script)
    ns = lean_script.ngan_sach(prof, profiles.target_chars(prof, profiles.target_minutes(prof)))
    return LAN1.format(kenh=(prof.get("niche") or prof["id"]).split(" — ")[0], title=title, phut=round(profiles.target_minutes(prof)),
                       chars=m["chars"], tran=ns["hi"], ctx=ctx.strip(), script=script.strip())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--lan1", action="store_true")
    g.add_argument("--tin", help="file tin phản biện/tiếp theo")
    g.add_argument("--dung-tin", action="store_true")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    c = _cfg(prof)
    d = ROOT / (prof.get("slug_dir") or "assets/out") / a.slug
    if not (d / "script.txt").exists():
        raise SystemExit(f"✗ chưa có {d / 'script.txt'}")
    out_dir = d / "soat_gptweb"
    out_dir.mkdir(exist_ok=True)
    if a.lan1 or a.dung_tin:
        n, text = 1, tin_lan1(prof, d)
    else:
        n = len(list(out_dir.glob("tra_loi_*.md"))) + 1
        text = Path(a.tin).read_text(encoding="utf-8")
    (out_dir / f"tin_{n}.txt").write_text(text, encoding="utf-8")
    if a.dung_tin:
        print(out_dir / "tin_1.txt")
        return
    out, model = gui(c["url"], text)
    f = out_dir / f"tra_loi_{n}.md"
    f.write_text(out, encoding="utf-8")
    print(f"✓ lượt {n} · model {model} · {len(out):,} chữ → {f}")


if __name__ == "__main__":
    main()
