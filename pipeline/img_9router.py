r"""img_9router.py — sinh ảnh qua 9router LOCAL (tài khoản Codex/ChatGPT, 0đ) bằng Responses API + tool image_generation.

Vì sao (15/10/2026, Lane M ep12): ima2 mất OAuth, gpti2 upstream_error/502 cả 2 key, ckey 401, vilao 402 → anh bảo
"chạy ảnh qua 9router". Đo thật: `/v1/images/generations` (gpt-image-*) bị Codex-ChatGPT từ chối; chỉ đường
`/v1/responses` + model `cx/gpt-5.6-luna` + tools=[image_generation] ra ảnh (~50s/ảnh low).

Dòng prompt giống gen_images.py: `@CAST:id1,id2 <prompt>` → gửi kèm `<cast-root>/_ref_<id>/001.png` làm ảnh tham chiếu
(khoá mặt). Ảnh ra lưu `<out>/NNN.png` theo số dòng; ảnh đã có thì bỏ qua (chạy lại = resume).

    py -3.13 -X utf8 img_9router.py --prompts <file> --out <dir> [--cast-root <tập>] [--workers 4] [--quality low]
"""
import argparse
import base64
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sol_client  # noqa: E402  (dùng chung BASE_URL/API_KEY 9router)

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
MODEL = "cx/gpt-5.6-luna"
SIZE = {"landscape": "1536x1024", "portrait": "1024x1536"}
KHUNG = {"landscape": "Wide horizontal 16:9 landscape composition (NOT square).",
         "portrait": "Tall vertical portrait composition (NOT square)."}


def _data_url(p):
    return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()


def generate(prompt, refs=(), orient="landscape", quality="low", timeout=600):
    """→ bytes PNG. refs = đường dẫn ảnh tham chiếu (khoá mặt)."""
    noi = [{"type": "input_text", "text": f"Generate ONE image. {KHUNG[orient]} {prompt}"
            + (" Keep each person's face, hair and age exactly as in the attached reference images (same order as named)."
               if refs else "")}]
    noi += [{"type": "input_image", "image_url": _data_url(r)} for r in refs]
    body = {"model": MODEL, "input": [{"role": "user", "content": noi}], "stream": False,
            "tools": [{"type": "image_generation", "size": SIZE[orient], "quality": quality}],
            "tool_choice": {"type": "image_generation"}}
    req = urllib.request.Request(sol_client.BASE_URL.rstrip("/") + "/responses", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {sol_client.API_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
    for o in d.get("output", []):
        if o.get("type") == "image_generation_call" and o.get("result"):
            return base64.b64decode(o["result"])
    raise RuntimeError(f"không có ảnh trong output: {json.dumps(d, ensure_ascii=False)[:300]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cast-root", default="")
    ap.add_argument("--orient", default="landscape", choices=list(SIZE))
    ap.add_argument("--quality", default="low", choices=["low", "medium", "high"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--chi", default="", help="chỉ vẽ các số này, vd 1,5,7")
    ap.add_argument("--ten", default="", help="ghi đúng 1 file tên này (prompt 1 dòng, vd master 001.png)")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dong = [x for x in Path(a.prompts).read_text(encoding="utf-8").splitlines() if x.strip()]
    chi = {int(x) for x in a.chi.split(",") if x.strip()}
    viec = []
    for i, p in enumerate(dong, 1):
        f = out / (a.ten or f"{i:03d}.png")
        if (chi and i not in chi) or f.exists():
            continue
        refs = []
        m = re.match(r"@CAST:(\S+)\s+", p)
        if m:
            refs = [Path(a.cast_root) / f"_ref_{x}" / "001.png" for x in m.group(1).split(",")]
            thieu = [str(r) for r in refs if not r.exists()]
            if thieu:
                print(f"  ✗ {f.name}: thiếu master {thieu}")
                continue
            p = p[m.end():]
        viec.append((f, p, refs))
    print(f"9router {MODEL}: {len(viec)} ảnh cần vẽ / {len(dong)} dòng · workers={a.workers}")

    def lam(v):
        f, p, refs = v
        for lan in range(1, 4):
            t = time.time()
            try:
                f.write_bytes(generate(p, refs, a.orient, a.quality))
                return f"  ✓ {f.name} ({f.stat().st_size // 1024}KB, {time.time() - t:.0f}s, ref {len(refs)})"
            except Exception as e:
                print(f"  ! {f.name} lần {lan}: {str(e)[:200]}")
                time.sleep(20 if "reset after" in str(e) else 5)
        return f"  ✗ {f.name}: lỗi 3 lần"

    with ThreadPoolExecutor(a.workers) as ex:
        kq = list(ex.map(lam, viec))
    for k in kq:
        print(k)
    loi = sum(1 for k in kq if "✗" in k)
    print(f"Xong: {len(kq) - loi}/{len(kq)} ảnh. Lỗi: {loi}")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
