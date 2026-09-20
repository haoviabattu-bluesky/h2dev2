"""gen_images.py — batch gen ảnh WW2 B&W từ file prompt (skill image-ww2-prompt) qua gpti2.

Đọc file prompt (mỗi dòng 1 prompt, tự bỏ dòng header ═══/▶/✅ và tiền tố "N."), gen song song
nhiều luồng, lưu 001.png, 002.png... — RESUMABLE (bỏ qua ảnh đã có), ghi manifest.json.

Dùng:
  py -3.13 gen_images.py --prompts prompts.txt --out ../assets/ww2/<slug>/img --orient landscape --quality low
  py -3.13 gen_images.py --prompts thumb.txt   --out ../assets/ww2/<slug>/thumb --quality medium --limit 1

Ảnh nền video: --quality low (rẻ ~50đ/ảnh). Thumbnail: --quality medium (nét hơn).
"""
import argparse
import concurrent.futures as cf
import json
import re
import sys
import threading
import time
from pathlib import Path

import gpti2_gen
import gpti2_edit
import grok_gen

sys.stdout.reconfigure(encoding="utf-8")

_HEADER = re.compile(r"^\s*(═══|▶|✅|#|//)")
_NUM = re.compile(r"^\s*\d+[.)]\s*")
_REF_MARK = re.compile(r"^\s*@ref\b[:\s]*", re.IGNORECASE)     # \b: KHÔNG khớp @ref2
_REF2_MARK = re.compile(r"^\s*@ref2\b[:\s]*", re.IGNORECASE)
_REF12_MARK = re.compile(r"^\s*@ref12\b[:\s]*", re.IGNORECASE)   # cả 2 nhân vật trong 1 khung (Lane G, 2026-09-20)
_GROK_MARK = re.compile(r"^\s*@grok\b[:\s]*", re.IGNORECASE)
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
    ap.add_argument("--workers", type=int, default=24,
                help="3 key gpti2 xoay round-robin, 24 luong = 8 luong/key (da verify khong 429)")
    ap.add_argument("--limit", type=int, default=0, help="chỉ gen N ảnh đầu (test)")
    ap.add_argument("--start", type=int, default=1, help="bắt đầu từ prompt số mấy (1-based)")
    ap.add_argument("--ref", action="append", default=[],
                    help="ảnh master NHÂN VẬT 1 (dòng @REF). Ảnh đầu = master ưu tiên giữ.")
    ap.add_argument("--ref2", action="append", default=[],
                    help="ảnh master NHÂN VẬT 2 (dòng @REF2) — vd người kể + 1 người quan trọng.")
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

    if len(args.ref) > gpti2_edit.MAX_REFERENCE_IMAGES or len(args.ref2) > gpti2_edit.MAX_REFERENCE_IMAGES:
        log(f"gpti2 chỉ nhận tối đa {gpti2_edit.MAX_REFERENCE_IMAGES} ảnh tham chiếu / nhân vật."); return
    refs = [(Path(r).read_bytes(), Path(r).name) for r in args.ref]
    refs2 = [(Path(r).read_bytes(), Path(r).name) for r in args.ref2]
    if (refs or refs2) and args.quality != "low":
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
        if tag == "grok":
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
    mode = f"gpti2 text-only {n['plain']}"
    if n["ref"]:
        mode += f" + REF {n['ref']} (~{gpti2_edit.estimate_price_vnd(args.orient, args.quality, len(refs))}đ)"
    if n["ref2"]:
        mode += f" + REF2 {n['ref2']}"
    if n["ref12"]:
        mode += f" + REF12 {n['ref12']} (2 mặt)"
    if n["grok"]:
        mode += f" + GROK {n['grok']} (trẻ em)"
    log(f"Tổng prompt: {len(prompts)} | cần gen: {len(tasks)} | đã có: {len(prompts)-len(tasks)}"
        f" | mode={mode} quality={args.quality} orient={args.orient} workers={args.workers}")
    if not tasks:
        log("Tất cả đã có — không cần gen."); return

    t0 = time.time()
    ok = [0]
    fail = []

    def work(task):
        i, name, prompt, route = task
        try:
            if route == "grok":
                img = grok_gen.generate(prompt, orientation=args.orient)          # cảnh trẻ em → Grok
            elif route == "ref":
                img = gpti2_edit.edit(prompt, refs, orientation=args.orient, quality=args.quality)
            elif route == "ref2":
                img = gpti2_edit.edit(prompt, refs2, orientation=args.orient, quality=args.quality)
            elif route == "ref12":
                img = gpti2_edit.edit(prompt, refs + refs2, orientation=args.orient, quality=args.quality)
            else:
                img = gpti2_gen.generate(prompt, orientation=args.orient, quality=args.quality)
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
