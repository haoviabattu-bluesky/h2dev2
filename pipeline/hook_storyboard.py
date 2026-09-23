"""hook_storyboard.py — chia hook đã khoá thành 4–7 shot (SOP §11–13), xuất prompt Google Flow/Grok từng shot + jobs.csv.
Claude Code (bước 1) chạy sau HOOK_LOCKED; máy 2/agent bước 3 vẽ ảnh shot + sinh clip + ghép (docs/GIAO_VIEC_BUOC3_AGENT.md).
2026-09-23: Task 11."""
import argparse, csv, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, hook_stage, profiles  # noqa: E402

PROMPT = """Chia đoạn HOOK dưới đây thành 4–7 SHOT cho 20–30 giây đầu video (kể chuyện, ảnh AI → clip 6/10/15s).
HOOK (đã khoá, không đổi chữ): {hook}
Tốc độ đọc: {cr:.0f} chữ/phút → tổng ≈ {tong:.0f} giây.
THẾ GIỚI / NHÂN VẬT (characters.json — giữ continuity, nhân vật chính mặt khoá REF):
{chars}
Luật: mỗi shot 3–6 s, 1 ý, 1 hành động, 1 điểm nhấn; shot mới phải THÊM thông tin (reveal/reaction/detail/memory/contrast);
ưu tiên close-up ở cảm xúc (mắt, tay, vật, cửa, giấy); motion nhỏ (push-in, rack focus, tay siết, cửa mở); hình bám đúng
câu voice của shot; KHÔNG spoil reveal bằng hình; không text trên hình. `voice` mỗi shot = đoạn con NGUYÊN VĂN của HOOK,
ghép lại đúng thứ tự phải ra đủ HOOK. `flow_prompt` tiếng Anh, 11 mục: SUBJECT / AGE-FACE-CLOTHING / LOCATION / ACTION /
EMOTION / CAMERA / LIGHTING / MOVEMENT / DURATION / CONTINUITY / NEGATIVE (no text, no subtitles, no distorted hands).
Trả ĐÚNG 1 JSON: {{"shots": [{{"n":1,"t0":0.0,"t1":4.0,"voice":"...","visual":"1 câu tiếng Việt","shot_type":"close-up|medium|wide|reaction|detail|establishing|memory","ref_image":"REF|REF2|none","flow_prompt":"...","continuity":"..."}}]}}"""


def validate(sb, hook, char_rate):
    loi = []
    shots = sb.get("shots") or []
    if not 4 <= len(shots) <= 7:
        loi.append(f"cần 4–7 shot, có {len(shots)}")
    if shots:
        tong = shots[-1]["t1"] - shots[0]["t0"]
        if not 18 <= tong <= 32:
            loi.append(f"tổng {tong:.1f}s ngoài 20–30s (dung sai ±2)")
        for i, s in enumerate(shots):
            if s["t1"] - s["t0"] < 2.5 or s["t1"] - s["t0"] > 6.5:
                loi.append(f"shot {s['n']} dài {s['t1']-s['t0']:.1f}s ngoài 3–6s")
            if i and abs(s["t0"] - shots[i - 1]["t1"]) > 0.05:
                loi.append(f"shot {s['n']} không liên tục với shot trước")
            if hook_stage._sach(s.get("voice", "")) and hook_stage._sach(s["voice"]) not in hook_stage._sach(hook):
                loi.append(f"shot {s['n']} voice không phải đoạn nguyên văn của hook")
        ghep = hook_stage._sach("".join(s.get("voice", "") for s in shots))
        if ghep != hook_stage._sach(hook):
            loi.append("ghép voice các shot ≠ hook (thiếu/thừa/lặp câu)")
    return loi


def ghi_flow_prompts_va_jobs(d, sb):
    d = Path(d); fp = d / "hook" / "flow_prompts"; fp.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in sb["shots"]:
        (fp / f"shot_{s['n']:02d}.txt").write_text(s.get("flow_prompt", ""), encoding="utf-8")
        dur = s["t1"] - s["t0"]
        rows.append({"id": f"shot_{s['n']:02d}", "image": f"hook/img/shot_{s['n']:02d}.png", "prompt": s.get("flow_prompt", ""),
                     "duration": 6 if dur <= 6 else 10 if dur <= 10 else 15, "resolution": "720p", "aspect": "16:9"})
    with (d / "hook" / "grok_jobs.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "image", "prompt", "duration", "resolution", "aspect"])
        w.writeheader(); w.writerows(rows)


def sinh(d, prof, force=False):
    d = Path(d)
    hook = hook_stage.doc_hook(d)
    lock = hook_stage.doc_lock(d)
    if not hook or not lock:
        raise SystemExit("✗ chưa có hook khoá — chạy hook_stage.py trước")
    out = d / "hook" / "hook_storyboard.json"
    if out.exists() and not force:
        sb = json.loads(out.read_text(encoding="utf-8"))
        if sb.get("hook_sha256") == lock["sha256"]:
            return sb
    cr = profiles.char_rate(prof)
    chars = (d / "characters.json").read_text(encoding="utf-8")[:4000] if (d / "characters.json").exists() else "(chưa có characters.json — mô tả nhân vật theo hook)"
    prompt = PROMPT.format(hook=hook, cr=cr, tong=ai_steps.measure(hook)["chars"] / cr * 60, chars=chars)
    sb = None
    for lan in range(3):
        r = ai_steps._writer_chat(prof, prompt, task="short", max_chars=20000)
        try:
            sb = json.loads(re.sub(r"^```[a-z]*\n?|\n?```$", "", r.text.strip()))
        except Exception as e:
            print(f"  ! JSON storyboard hỏng lần {lan+1}: {e}"); continue
        loi = validate(sb, hook, cr)
        if not loi:
            break
        print(f"  ! storyboard lần {lan+1}: " + " · ".join(loi))
        prompt = prompt + "\n\nLẦN TRƯỚC SAI: " + " · ".join(loi) + " — sửa đúng."
    else:
        raise SystemExit("✗ storyboard không hợp lệ sau 3 lần — người xem hook/hook_storyboard.err.json")
    sb["hook_sha256"] = lock["sha256"]
    sb["duration_target_s"] = round(sb["shots"][-1]["t1"], 1)
    out.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")
    ghi_flow_prompts_va_jobs(d, sb)
    print(f"[STORYBOARD] {len(sb['shots'])} shot · {sb['duration_target_s']}s → {out}")
    return sb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True); ap.add_argument("--slug", required=True); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    prof = profiles.load(a.profile)
    d = Path(__file__).resolve().parent.parent / (prof.get("slug_dir") or "assets/out") / a.slug
    sinh(d, prof, force=a.force)


if __name__ == "__main__":
    main()
