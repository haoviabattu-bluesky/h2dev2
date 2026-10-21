r"""soat_kb_gptweb.py — soát kịch bản ĐÃ KHOÁ bằng ChatGPT web (MẶC ĐỊNH mọi lane có chặng soát, anh chốt 2026-09-27;
máy 3 chỉ dùng khi anh nói — profile `script.soat: "may3"`).

Vì sao: ChatGPT (Project riêng của từng lane) đọc toàn bộ kịch bản và góp ý như nhà văn; tab lane (Claude Code) thẩm
định từng góp ý — hợp lý thì nhận, chưa hợp lý thì phản biện 1 lượt — rồi tổng hợp thành viec_tay.txt cho Opus sửa
(KHÔNG sửa tay), Sol chấm lại ×2, khoá. Không chép sang máy 3, không ghi sheet giữa chừng (D = Done do dong_goi_may2).

Hạ tầng: pipeline\gptweb_pool.py — 2 tài khoản (acc1 cổng 9335, acc2 cổng 9336). PHIÊN (anh chốt 27/09 bản 2):
tài khoản rảnh → MỞ cổng → gửi → CHỜ ChatGPT trả lời xong (không đóng cổng giữa chừng, không gửi lại — chống spam) →
tab lane thẩm định, phản biện (--tin) trong CÙNG cổng → CHỐT phương án → --chot ĐÓNG cổng → rồi mới viết lại (viec_tay →
Opus → Sol). Chỉ đóng cổng do tool mở; cổng mở sẵn từ trước giữ nguyên. Quá tải → đổi tài khoản; cả hai bận →
"GPT báo To many request- chờ 20 phút".

Profile (field-driven): `script.soat_gptweb = {"enabled": true, "urls": {"acc1": "<link>", "acc2": "<link>"},
"boi_canh": "<1 đoạn: khán giả, định dạng, giọng>", "rang_buoc": ["luật riêng lane", ...]}` — link là Project của lane
(tool mở CHAT MỚI trong Project cho mỗi tập) hoặc 1 hội thoại cố định (`/c/…`). Khoá cũ `"url": "<link>"` = acc1.

Dùng:
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --lan1      lượt 1 (mở phiên, chờ trả lời)
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --tin <file> phản biện/lượt tiếp (CÙNG cổng + hội thoại)
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --doc        chỉ ĐỌC câu trả lời lượt cuối (không gửi)
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --chot       CHỐT phương án → ĐÓNG cổng (rồi mới sửa KB)
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --dung-tin   chỉ dựng tin lượt 1, không gửi
  py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --xong       chốt chặng soát (cổng phải ĐÃ đóng)
Kết quả: <tập>\soat_gptweb\{tin_N.txt, tra_loi_N.md, phien.json, BAO_CAO_SUA.md}.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import ai_steps   # noqa: E402
import profiles   # noqa: E402

LAN1 = """Đây là kịch bản tập mới của kênh {kenh}. Nhờ bạn thẩm định như một nhà văn chuyên nghiệp.

BỐI CẢNH KÊNH
- Tiêu đề tập: {title}
- {boi_canh}
- Độ dài video: khoảng {phut} phút, đọc bằng giọng đọc AI (voiceover), khán giả xem trên điện thoại.
- Cung cảm xúc: {cung}

CẤU TRÚC BẮT BUỘC CỦA KÊNH (đề xuất sửa không được phá khung này)
{cau_truc}

RÀNG BUỘC CỨNG (đề xuất sửa KHÔNG được phá)
{rang_buoc}

CẦN BẠN TRẢ LỜI (tiếng Việt; mọi chữ Nhật trích dẫn phải kèm dịch Việt trong ngoặc)
A. Nhận xét tổng: đã hấp dẫn/lôi cuốn chưa, điểm /10, 3 điểm mạnh, 3 điểm yếu nhất.
B. Hook 30 giây đầu có giữ chân người xem không? Đề xuất cụ thể nếu chưa.
C. Danh sách vấn đề cụ thể, xếp theo mức (NẶNG / VỪA / NHẸ). Mỗi mục: trích NGUYÊN VĂN câu tiếng Nhật đang có → vấn đề → câu tiếng Nhật đề xuất thay thế (viết sẵn, dùng được ngay) + dịch Việt. Tối đa 12 mục, ưu tiên thứ làm người xem bỏ video.
D. Phần kết: {ket}
E. Có chỗ nào sai sự thật (so với tư liệu), phi logic, lặp ý, hoặc nhân vật hành xử không tự nhiên không?

TƯ LIỆU ĐƯỢC PHÉP DÙNG (series_ctx của tập):
{ctx}

KỊCH BẢN:
{script}"""

RANG_BUOC_CHUNG = [
    "Mọi con số tiền/chế độ/pháp lý/thống kê CHỈ được lấy từ TƯ LIỆU dưới đây — không thêm số mới.",
    "Mỗi câu thoại「…」là một câu riêng; lời dẫn là câu khác (đọc bằng giọng khác nhau).",
    "Tổng độ dài chỉ được đổi trong khoảng ±3% (hiện {chars:,} chữ, trần {tran:,}) — đề xuất thêm chữ thì chỉ ra chỗ bớt tương ứng.",
    "Không sao chép nhân vật/tình tiết/cách đùa của video gốc đối thủ; không lặp lại tình tiết của các tập trước của kênh.",
    "Tiêu đề hứa gì thì trong 60 giây đầu phải nói lại, và bài phải trả đủ lời hứa đó.",
]


def _cfg(prof):
    c = (prof.get("script") or {}).get("soat_gptweb") or {}
    if not c.get("enabled"):
        raise SystemExit(f"✗ lane {prof['id']} chưa bật script.soat_gptweb.enabled")
    return c


def _pid(url):
    m = re.search(r"/g/(g-p-[0-9a-f]{32})", url or "")
    return m.group(1) if m else None


def kiem_dung_project(prof, acc, url):
    """Link phải nằm trong đúng Project của lane ở tài khoản đó (projects.<acc>.id, tên = publish.sheet_tab)
    và Project đó không được gán cho lane nào khác — làm lane này mà mở Project lane khác là CẤM (anh chốt 27/09)."""
    c = _cfg(prof)
    pj = (c.get("projects") or {}).get(acc) or {}
    tab = (prof.get("publish") or {}).get("sheet_tab")
    if not pj.get("id"):
        raise SystemExit(f"✗ {prof['id']}: chưa khai script.soat_gptweb.projects.{acc} (id Project đã đối chiếu tên)")
    # "-script": tài khoản đã có Project trùng tên của YT-TITLE. Tên thư mục lane (slug_dir) cũng hợp lệ: Lane N đặt
    # Project theo thư mục `N-senior_korekara` rồi anh đổi tab thành tên tạm `Lane-N` (30/09) — vẫn là Project của lane.
    thu_muc = Path(prof.get("slug_dir") or "").name
    if pj.get("ten") not in (tab, f"{tab}-script", thu_muc):
        raise SystemExit(f"✗ {prof['id']}: Project {acc} tên '{pj.get('ten')}' ≠ tab lane '{tab}'")
    if _pid(url) != pj["id"]:
        raise SystemExit(f"✗ {prof['id']}: link {acc} {url} KHÔNG nằm trong Project {pj['ten']} ({pj['id']}) — cấm dùng")
    for f in (ROOT / "profiles" / "profiles").glob("*.json"):
        try:
            o = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if o.get("id") == prof["id"]:
            continue
        oc = (o.get("script") or {}).get("soat_gptweb") or {}
        ids = {(v or {}).get("id") for v in (oc.get("projects") or {}).values()}
        ids |= {_pid(v) for v in (oc.get("urls") or {}).values()}
        if pj["id"] in ids:
            raise SystemExit(f"✗ Project {pj['id']} ({acc}) đang gán cho CẢ lane {o.get('id')} — sửa profile trước")


def _urls(c, prof):
    u = dict(c.get("urls") or {})
    if c.get("url") and not u.get("acc1"):
        u["acc1"] = c["url"]
    u = {k: v for k, v in u.items() if v}
    if not u:
        raise SystemExit("✗ script.soat_gptweb chưa có link Project/hội thoại cho tài khoản nào (urls.acc1 / urls.acc2)")
    for acc, url in u.items():
        kiem_dung_project(prof, acc, url)
    return u


def _phut(prof, d):
    try:
        st = json.loads((d / "state.json").read_text(encoding="utf-8"))
        return (st.get("B0") or {}).get("minutes") or profiles.target_minutes(prof)
    except Exception:
        return profiles.target_minutes(prof)


def tin_lan1(prof, d):
    import lean_script
    c = (prof.get("script") or {}).get("soat_gptweb") or {}
    sc = prof.get("script") or {}
    script = (d / "script.txt").read_text(encoding="utf-8")
    title = lean_script._title(d)
    ctx = (d / "series_ctx.txt").read_text(encoding="utf-8") if (d / "series_ctx.txt").exists() else "(không có — lane hư cấu)"
    m = ai_steps.measure(script)
    phut = _phut(prof, d)
    ns = lean_script.ngan_sach(prof, profiles.target_chars(prof, phut))
    rb = [x.format(chars=m["chars"], tran=ns["hi"]) for x in RANG_BUOC_CHUNG] + list(c.get("rang_buoc") or [])
    rb += [f"(luật kênh) {x}" for x in ((prof.get("script_qc") or {}).get("lane_rules") or [])]
    cau_truc = (c.get("cau_truc") or ai_steps._cau_truc_block(prof)).strip()
    cung = ("KÍCH (người xem bị ức chế/giận) → GIẢI TOẢ (hệ quả tự nhiên, không hả hê) → VỊ THA (thương cảm + 1 câu đạo lý ngắn)."
            if sc.get("cung_cam_xuc", True) else "theo cấu trúc kênh.")
    ket = ("đã có câu đạo lý đáng nhớ + cảm ơn người xem + xin 高評価 (thích) / チャンネル登録 (đăng ký) rõ ràng chưa? Có đoạn nào quá nặng thuật ngữ không?"
           if sc.get("cam_on_cuoi", sc.get("cung_cam_xuc", True)) else "kết có tròn trịa, đúng outro của kênh không? Có đoạn nào quá nặng thuật ngữ không?")
    return LAN1.format(kenh=(prof.get("niche") or prof["id"]).split(" — ")[0], title=title, phut=round(phut),
                       boi_canh=(c.get("boi_canh") or prof.get("niche") or "").strip(), cung=cung, cau_truc=cau_truc,
                       rang_buoc="\n".join(f"{i}. {x}" for i, x in enumerate(rb, 1)), ket=ket,
                       ctx=ctx.strip(), script=script.strip())


def xong(prof, d, force=False):
    """Chốt chặng soát: bản đang khoá PASS + đã có ≥1 câu trả lời GPT + BAO_CAO_SUA.md (tab lane viết) → review_may3 ghi
    'received' (cổng B4/B5W/dong_goi cho qua), giữ hoặc khoá lại hook theo đầu kịch bản. Không ghi sheet."""
    import gate_common
    import review_may3
    out_dir = d / "soat_gptweb"
    tk_mo = _phien_mo(prof, d)
    if tk_mo:
        raise SystemExit(f"✗ cổng ChatGPT {tk_mo} VẪN MỞ cho tập này — chạy --chot trước (đóng cổng rồi mới sửa/chốt)")
    if not list(out_dir.glob("tra_loi_*.md")) and not force:
        raise SystemExit(f"✗ chưa có câu trả lời ChatGPT nào trong {out_dir} — chạy --lan1 trước")
    if not (out_dir / "BAO_CAO_SUA.md").exists():
        raise SystemExit(f"✗ thiếu {out_dir / 'BAO_CAO_SUA.md'} — tab lane ghi: nhận/phản biện góp ý nào, viec_tay gì, kết quả Sol")
    ok, msg, level = gate_common.kiem_lock(d)
    if level != "PASS":
        raise SystemExit(f"✗ kịch bản chưa khoá PASS ({msg}) — chạy lại make_video --den B3G sau khi đưa viec_tay.txt")
    review_may3.danh_dau_da_soat(prof, d, nguon="gptweb", bao_cao=out_dir / "BAO_CAO_SUA.md")


def _chu(prof, d):
    return f"{prof['id']}/{Path(d).name}"


def _phien_mo(prof, d):
    """Tên tài khoản đang giữ phiên cho ĐÚNG tập này (None nếu không có)."""
    import gptweb_pool
    for tk in gptweb_pool.ds_tai_khoan():
        ph = gptweb_pool.doc_phien(tk)
        if ph and ph.get("chu") == _chu(prof, d):
            return tk["ten"]
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--lan1", action="store_true")
    g.add_argument("--tin", help="file tin phản biện/tiếp theo (gửi vào CÙNG hội thoại, cùng tài khoản)")
    g.add_argument("--doc", action="store_true", help="chỉ ĐỌC câu trả lời cho tin cuối (không gửi)")
    g.add_argument("--chot", action="store_true", help="chốt phương án → ĐÓNG cổng của phiên tập này")
    g.add_argument("--dung-tin", action="store_true")
    g.add_argument("--xong", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    d = ROOT / (prof.get("slug_dir") or "assets/out") / a.slug
    if not (d / "script.txt").exists():
        raise SystemExit(f"✗ chưa có {d / 'script.txt'}")
    if a.xong:
        return xong(prof, d, force=a.force)
    import gptweb_pool
    if a.chot:
        tk_mo = _phien_mo(prof, d)
        if not tk_mo:
            print("  (không có cổng nào đang mở cho tập này)")
            return
        gptweb_pool.dong_phien(gptweb_pool.tai_khoan(tk_mo), _chu(prof, d))
        print("✓ ĐÃ CHỐT — cổng ChatGPT đã đóng. Giờ mới viết viec_tay.txt → Opus sửa → Sol chấm theo hướng đã chốt.")
        return
    c = _cfg(prof)
    out_dir = d / "soat_gptweb"
    out_dir.mkdir(exist_ok=True)
    pf = out_dir / "phien.json"
    if a.doc:
        ph = json.loads(pf.read_text(encoding="utf-8"))
        n = len(list(out_dir.glob("tin_*.txt")))
        text = (out_dir / f"tin_{n}.txt").read_text(encoding="utf-8")
        kiem_dung_project(prof, ph["acc"], ph["conv"])
        tk = gptweb_pool.tai_khoan(ph["acc"])
        gptweb_pool.mo_phien(tk, _chu(prof, d))
        out, model, conv = gptweb_pool.doc(tk, ph["conv"], text)
        f = out_dir / f"tra_loi_{n}.md"
        f.write_text(out, encoding="utf-8")
        print(f"✓ đọc lượt {n} · {ph['acc']} · model {model} · {len(out):,} chữ → {f}\n  (cổng VẪN MỞ — thẩm định; "
              f"phản biện bằng --tin, chốt phương án bằng --chot)")
        return
    if a.lan1 or a.dung_tin:
        n, text = 1, tin_lan1(prof, d)
    else:
        n = len(list(out_dir.glob("tra_loi_*.md"))) + 1
        text = Path(a.tin).read_text(encoding="utf-8")
    (out_dir / f"tin_{n}.txt").write_text(text, encoding="utf-8")
    if a.dung_tin:
        print(out_dir / "tin_1.txt")
        return
    import gate_common
    if a.lan1:
        try:
            out, model, acc, conv = gptweb_pool.hoi(text, _urls(c, prof), _chu(prof, d))
        except gptweb_pool.ChuaXong as e:
            acc = _phien_mo(prof, d)
            pf.write_text(json.dumps({"acc": acc, "conv": e.conv, "sha_lan1": gate_common.sha256_file(d / "script.txt")},
                                     ensure_ascii=False, indent=1), encoding="utf-8")
            raise SystemExit(f"✗ {e}\n  → KHÔNG gửi lại. Đọc tiếp bằng: --doc (cổng vẫn mở)")
        pf.write_text(json.dumps({"acc": acc, "conv": conv, "sha_lan1": gate_common.sha256_file(d / "script.txt")},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        if not pf.exists():
            raise SystemExit(f"✗ chưa có {pf} — lượt tiếp phải sau --lan1 (cần biết tài khoản + hội thoại)")
        ph = json.loads(pf.read_text(encoding="utf-8"))
        if "/c/" not in (ph.get("conv") or ""):
            raise SystemExit(f"✗ {pf} không có link hội thoại (/c/…) để gửi tiếp")
        kiem_dung_project(prof, ph["acc"], ph["conv"])
        try:
            out, model, acc, conv = gptweb_pool.hoi(text, {ph["acc"]: ph["conv"]}, _chu(prof, d), acc_co_dinh=ph["acc"])
        except gptweb_pool.ChuaXong as e:
            raise SystemExit(f"✗ {e}\n  → KHÔNG gửi lại. Đọc tiếp bằng: --doc (cổng vẫn mở)")
    f = out_dir / f"tra_loi_{n}.md"
    f.write_text(out, encoding="utf-8")
    print(f"✓ lượt {n} · {acc} · model {model} · {len(out):,} chữ → {f}\n"
          f"  (cổng {acc} VẪN MỞ cho tập này — thẩm định; cần phản biện: --tin <file>; thống nhất phương án: --chot "
          f"để ĐÓNG cổng rồi mới viết lại kịch bản)")


if __name__ == "__main__":
    main()
