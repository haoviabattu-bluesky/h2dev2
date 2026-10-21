"""gen_images.py — batch gen ảnh WW2 B&W từ file prompt (skill image-ww2-prompt) qua gpti2.

Đọc file prompt (mỗi dòng 1 prompt, tự bỏ dòng header ═══/▶/✅ và tiền tố "N."), gen song song
nhiều luồng, lưu 001.png, 002.png... — RESUMABLE (bỏ qua ảnh đã có), ghi manifest.json.

Dùng:
  py -3.13 gen_images.py --prompts prompts.txt --out ../assets/ww2/<slug>/img --orient landscape --quality low
  py -3.13 gen_images.py --prompts thumb.txt   --out ../assets/ww2/<slug>/thumb --quality medium --limit 1

Ảnh nền video: --quality low (rẻ ~50đ/ảnh). Thumbnail: --quality medium (nét hơn).

--provider ckey (2026-09-30): gen qua ckey.vn (ckey_gen.py) — 52đ/ảnh cố định kể cả có ref, ref gửi
qua `images` KHÔNG giới hạn 8 ảnh/nhân vật. Mặc định lấy từ biến môi trường IMG_PROVIDER hoặc khoá
`img_provider` trong keys.json (để máy 2 / hybrid_chuan_bi đổi provider mà không sửa lệnh gọi).
Tự chuyển (2026-09-30): provider gpti2 mà 1 ảnh lỗi (kể cả hết tiền) → gen lại ảnh đó qua ckey;
hết tiền gpti2 thì mọi ảnh sau đi thẳng ckey. Tắt: --fallback none / IMG_FALLBACK=none / "img_fallback": "none".
Dòng @GROK vẫn đi Grok như cũ.
"""
import argparse
import concurrent.futures as cf
import json
import re
import sys
import threading
import time
from pathlib import Path

import ckey_gen
import gpti2_gen
import gpti2_edit
import grok_gen
import keys

sys.stdout.reconfigure(encoding="utf-8")

_HEADER = re.compile(r"^\s*(═══|▶|✅|#|//)")
_NUM = re.compile(r"^\s*\d+[.)]\s*")
_REF_MARK = re.compile(r"^\s*@ref\b[:\s]*", re.IGNORECASE)     # \b: KHÔNG khớp @ref2
_REF2_MARK = re.compile(r"^\s*@ref2\b[:\s]*", re.IGNORECASE)
_REF12_MARK = re.compile(r"^\s*@ref12\b[:\s]*", re.IGNORECASE)   # cả 2 nhân vật trong 1 khung (Lane G, 2026-09-20)
_GROK_MARK = re.compile(r"^\s*@grok\b[:\s]*", re.IGNORECASE)
# Lane K (2026-09-24): khoá mặt N nhân vật/tập — `@CAST:shu,tencho <prompt>` → master `<cast-root>/_ref_<id>/001.png`
_CAST_MARK = re.compile(r"^\s*@cast:([A-Za-z0-9_\-]+(?:\s*,\s*[A-Za-z0-9_\-]+)*)\s+", re.IGNORECASE)
_print_lock = threading.Lock()


def parse_prompts(path):
    """Mỗi dòng không rỗng/không header = 1 prompt → trả (use_ref, use_grok, text).
    '@GROK ' = cảnh có TRẺ EM/EM BÉ → route Grok Imagine (gpti2/Azure chặn mọi minor).
    '@REF '  = cảnh THẤY MẶT nhân vật chính → REF-LOCK từ --ref  (nhân vật 1, vd người kể).
    '@REF2 ' = cảnh THẤY MẶT nhân vật phụ  → REF-LOCK từ --ref2 (nhân vật 2, vd con/bạn).
    dòng thường = gpti2 text-only (cảnh vật/phong cảnh, nét 2560x1440). Bỏ tiền tố 'N.'/'N)'.
    '@REF12 ' = cảnh THẤY MẶT CẢ HAI nhân vật → gửi cả --ref và --ref2 làm tham chiếu (gpti2 nhận tới 8 ảnh).
    Trả (tag, text) với tag ∈ {'plain','ref','ref2','ref12','grok'}."""
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or _HEADER.match(s):
            continue
        tag = "plain"
        mc = _CAST_MARK.match(s)
        if mc:
            ids = [x.strip() for x in mc.group(1).split(",") if x.strip()]
            out.append(("cast:" + ",".join(ids), _NUM.sub("", s[mc.end():].strip()).strip()))
            continue
        for mark, t in ((_GROK_MARK, "grok"), (_REF12_MARK, "ref12"), (_REF2_MARK, "ref2"), (_REF_MARK, "ref")):
            m = mark.match(s)
            if m:
                tag = t
                s = s[m.end():]
                break
        out.append((tag, _NUM.sub("", s.strip()).strip()))
    return out


def log(*a):
    with _print_lock:
        print(*a, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", required=True, help="file prompt (mỗi dòng 1 prompt)")
    ap.add_argument("--out", required=True, help="thư mục lưu ảnh")
    ap.add_argument("--orient", default="landscape", choices=["landscape", "portrait"])
    ap.add_argument("--quality", default="low", choices=["low", "medium", "high"])
    ap.add_argument("--provider", choices=["gpti2", "ckey"],
                    default=keys.get("img_provider", env="IMG_PROVIDER", default="gpti2").lower(),
                    help="gpti2 (mặc định) | ckey = ckey.vn 52đ/ảnh, ref không giới hạn 8")
    ap.add_argument("--fallback", choices=["ckey", "none"],
                    default=keys.get("img_fallback", env="IMG_FALLBACK", default="ckey").lower(),
                    help="gpti2 lỗi/hết tiền → tự gen lại ảnh đó qua ckey (mặc định) | none = tắt")
    ap.add_argument("--workers", type=int, default=8,
                help="1 key gpti2 (10/10), 8 luong/key (da verify khong 429); them key thi tang 8/key")
    ap.add_argument("--limit", type=int, default=0, help="chỉ gen N ảnh đầu (test)")
    ap.add_argument("--start", type=int, default=1, help="bắt đầu từ prompt số mấy (1-based)")
    ap.add_argument("--ref", action="append", default=[],
                    help="ảnh master NHÂN VẬT 1 (dòng @REF). Ảnh đầu = master ưu tiên giữ.")
    ap.add_argument("--ref2", action="append", default=[],
                    help="ảnh master NHÂN VẬT 2 (dòng @REF2) — vd người kể + 1 người quan trọng.")
    ap.add_argument("--cast-root", default="",
                    help="thư mục tập chứa _ref_<id>/001.png — cho dòng @CAST:id1,id2 (khoá mặt N nhân vật, Lane K)")
    ap.add_argument("--skip-stock-plan", default="",
                    help="đường dẫn stock_plan.tsv (lane hybrid) — dòng nào group=STOCK thì BỎ QUA "
                         "hoàn toàn (không gen AI cho dòng đó), giữ đúng số thứ tự ảnh còn lại.")
    args = ap.parse_args()

    skip_lines = set()
    if args.skip_stock_plan:
        for ln in Path(args.skip_stock_plan).read_text(encoding="utf-8").splitlines()[1:]:
            cols = ln.split("\t")
            if len(cols) >= 2 and cols[0].strip().isdigit() and cols[1].strip().upper() == "STOCK":
                skip_lines.add(int(cols[0].strip()))
        log(f"skip-stock-plan: bỏ {len(skip_lines)} dòng STOCK, không gen AI cho các dòng đó.")

    ckey = args.provider == "ckey"
    if not ckey and (len(args.ref) > gpti2_edit.MAX_REFERENCE_IMAGES
                     or len(args.ref2) > gpti2_edit.MAX_REFERENCE_IMAGES):
        log(f"gpti2 chỉ nhận tối đa {gpti2_edit.MAX_REFERENCE_IMAGES} ảnh tham chiếu / nhân vật "
            f"(--provider ckey thì không giới hạn)."); return
    refs = [(Path(r).read_bytes(), Path(r).name) for r in args.ref]
    refs2 = [(Path(r).read_bytes(), Path(r).name) for r in args.ref2]
    if (refs or refs2) and args.quality != "low" and not ckey:
        log(f"⚠ REF-LOCK: --quality low đã đủ giữ khuôn mặt (đo thật 2026-09-07). "
            f"Đang dùng '{args.quality}' = đắt hơn ~4-28 lần mà không giữ mặt tốt hơn.")

    prompts = parse_prompts(args.prompts)
    if args.start > 1:
        prompts = prompts[args.start - 1:]
    if args.limit:
        prompts = prompts[:args.limit]
    if not prompts:
        log("Không có prompt nào."); return

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = outdir / "manifest.json"
    done = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}

    any_ref_mark = any(tag in ("ref", "ref2", "ref12") for tag, _ in prompts)  # có marker khoá mặt nào không
    tasks = []
    for i, (tag, p) in enumerate(prompts, start=args.start):
        name = f"{i:03d}.png"
        if i in skip_lines:
            continue   # dòng STOCK (hybrid) — không gen AI
        if (outdir / name).exists():
            continue   # resume: bỏ ảnh đã có
        if tag.startswith("cast:"):
            route = tag if args.cast_root else "plain"
        elif tag == "grok":
            route = "grok"
        elif tag == "ref12" and refs and refs2:
            route = "ref12"
        elif tag == "ref12" and refs:
            route = "ref"      # thiếu master 2 → khoá mặt nhân vật 1 thôi, còn hơn plain
        elif tag == "ref2" and refs2:
            route = "ref2"
        elif tag == "ref" and refs:
            route = "ref"
        elif refs and not any_ref_mark:
            route = "ref"      # hành vi cũ: có --ref + KHÔNG marker nào → khoá mặt cả batch (nhân vật 1)
        else:
            route = "plain"
        tasks.append((i, name, p, route))

    n = {r: sum(1 for *_, x in tasks if x == r) for r in ("grok", "ref", "ref2", "ref12", "plain")}
    mode = f"{args.provider} text-only {n['plain']}"
    if n["ref"]:
        gia = ckey_gen.PRICE_VND if ckey else gpti2_edit.estimate_price_vnd(args.orient, args.quality, len(refs))
        mode += f" + REF {n['ref']} (~{gia}đ)"
    if n["ref2"]:
        mode += f" + REF2 {n['ref2']}"
    if n["ref12"]:
        mode += f" + REF12 {n['ref12']} (2 mặt)"
    n_cast = sum(1 for *_, x in tasks if x.startswith("cast:"))
    if n_cast:
        mode += f" + CAST {n_cast} (khoá mặt theo id)"
    if n["grok"]:
        mode += f" + GROK {n['grok']} (trẻ em)"
    if not ckey and args.fallback == "ckey":
        mode += " | gpti2 lỗi → ckey"
    log(f"Tổng prompt: {len(prompts)} | cần gen: {len(tasks)} | đã có: {len(prompts)-len(tasks)}"
        f" | mode={mode} quality={args.quality} orient={args.orient} workers={args.workers}")
    if not tasks:
        log("Tất cả đã có — không cần gen."); return

    t0 = time.time()
    ok = [0]
    fail = []

    gpti2_het = [False]   # gpti2 hết tiền 1 lần → các ảnh sau đi thẳng ckey, khỏi gọi gpti2 vô ích

    def gen(name, prompt, imgs=None):
        """imgs=None → text-only. gpti2 lỗi/hết tiền và --fallback ckey → gen lại ảnh đó qua ckey."""
        if ckey or gpti2_het[0]:
            return ckey_gen.generate(prompt, orientation=args.orient, refs=imgs)
        try:
            if imgs:
                return gpti2_edit.edit(prompt, imgs, orientation=args.orient, quality=args.quality)
            return gpti2_gen.generate(prompt, orientation=args.orient, quality=args.quality)
        except Exception as e:
            if args.fallback != "ckey":
                raise
            if isinstance(e, gpti2_gen.QuotaExhaustedError) and not gpti2_het[0]:
                gpti2_het[0] = True
                log(f"  ⚠ gpti2 HẾT TIỀN — các ảnh còn lại chuyển hẳn sang ckey ({ckey_gen.PRICE_VND}đ/ảnh).")
            log(f"  ↪ {name} gpti2 lỗi ({str(e)[:120]}) → gen lại qua ckey")
            return ckey_gen.generate(prompt, orientation=args.orient, refs=imgs)

    def work(task):
        i, name, prompt, route = task
        try:
            if route == "grok":
                img = grok_gen.generate(prompt, orientation=args.orient)          # cảnh trẻ em → Grok
            elif route == "ref":
                img = gen(name, prompt, refs)
            elif route == "ref2":
                img = gen(name, prompt, refs2)
            elif route.startswith("cast:"):
                ms = [Path(args.cast_root) / f"_ref_{x}" / "001.png" for x in route[5:].split(",")]
                thieu = [str(m) for m in ms if not m.exists()]
                if thieu:
                    raise RuntimeError(f"thiếu master khoá mặt: {thieu}")
                img = gen(name, prompt, [(m.read_bytes(), m.name) for m in ms])
            elif route == "ref12":
                img = gen(name, prompt, refs + refs2)
            else:
                img = gen(name, prompt)
            (outdir / name).write_bytes(img)
            with _print_lock:
                done[name] = {"idx": i, "prompt": prompt}
                manifest.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
                ok[0] += 1
            log(f"  ✓ {name} ({len(img)//1024}KB) [{ok[0]}/{len(tasks)}]")
        except gpti2_gen.QuotaExhaustedError as e:
            log(f"  ✗ {name} HẾT TIỀN KEY: {e}")
            fail.append((name, str(e)))
        except Exception as e:
            log(f"  ✗ {name} lỗi: {e}")
            fail.append((name, str(e)))

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, tasks))

    log(f"\nXong: {ok[0]} ảnh trong {round(time.time()-t0)}s. Lỗi: {len(fail)}")
    if fail:
        for n, e in fail[:10]:
            log(f"   - {n}: {e}")
        log("→ Chạy lại lệnh cũ để retry (resume tự bỏ ảnh đã có).")


if __name__ == "__main__":
    main()
