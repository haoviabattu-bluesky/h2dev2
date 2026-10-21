"""hook_storyboard.py — chia hook đã khoá thành 4–7 shot (SOP §11–13), xuất prompt Google Flow/Grok từng shot + jobs.csv.
Claude Code (bước 1) chạy sau HOOK_LOCKED; máy 2/agent bước 3 vẽ ảnh shot + sinh clip + ghép (docs/GIAO_VIEC_BUOC3_AGENT.md).
2026-09-23: Task 11."""
import argparse, csv, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, hook_stage, profiles  # noqa: E402

PROMPT = """Chia đoạn HOOK dưới đây thành {n_shot} SHOT cho {khung_giay} đầu video (kể chuyện, ảnh AI → clip 6/10/15s).
HOOK (đã khoá, không đổi chữ): {hook}
Tốc độ đọc: {cr:.0f} chữ/phút → tổng ≈ {tong:.0f} giây.
THẾ GIỚI / NHÂN VẬT (characters.json — giữ continuity, nhân vật chính mặt khoá REF):
{chars}
{ghi_chu}Luật: mỗi shot 3–6 s, 1 ý, 1 hành động, 1 điểm nhấn; shot mới phải THÊM thông tin (reveal/reaction/detail/memory/contrast);
ưu tiên close-up ở cảm xúc (mắt, tay, vật, cửa, giấy); motion nhỏ (push-in, rack focus, tay siết, cửa mở); hình bám đúng
câu voice của shot; KHÔNG spoil reveal bằng hình; không text trên hình. Shot mà CHỮ trên đạo cụ là điểm nhấn (婚姻届/退職届/
売家 看板/通帳/màn hình tin nhắn/biên bản có tên…): vẽ mặt đạo cụ TRƠN, phẳng, gần chính diện, chiếm ≥20% khung, không tay/vật
che, viền rõ trên nền tương phản, camera gần như đứng yên (chỉ push-in rất chậm) — chữ do code chèn sau
(docs/QUY_TAC_CHU_TREN_DAO_CU_HOOK.md); ghi rõ "plain blank surface, no text" trong flow_prompt. `voice` mỗi shot = đoạn con NGUYÊN VĂN của HOOK,
ghép lại đúng thứ tự phải ra đủ HOOK. `flow_prompt` tiếng Anh, 11 mục: SUBJECT / AGE-FACE-CLOTHING / LOCATION / ACTION /
EMOTION / CAMERA / LIGHTING / MOVEMENT / DURATION / CONTINUITY / NEGATIVE (no text, no subtitles, no distorted hands).
Nếu characters.json có trường "id" (khoá mặt nhiều nhân vật): `ref_image` = các id THẤY MẶT trong shot, nối bằng dấu phẩy
(tối đa 3, vd "shu,tencho"), hoặc "none"; mỗi shot phải thấy MẶT ít nhất 1 nhân vật + cảm xúc đúng câu voice.
Trả ĐÚNG 1 JSON: {{"shots": [{{"n":1,"t0":0.0,"t1":4.0,"voice":"...","visual":"1 câu tiếng Việt","shot_type":"close-up|medium|wide|reaction|detail|establishing|memory","ref_image":"REF|REF2|none","flow_prompt":"...","continuity":"..."}}]}}"""


def gioi_han(prof):
    """(min_shot, max_shot, min_giây, max_giây). 2026-10-17 (anh duyệt): độ dài hook = độ dài hook video gốc của tập
    (hook_stage.giay_hook, Lane N ~12–20s tới Lane L ~105s) → khung chung 3–22 shot / 12–120s cho mọi lane."""
    return (3, 22, 12, 120)


def validate(sb, hook, char_rate, prof=None):
    loi = []
    shots = sb.get("shots") or []
    smin, smax, gmin, gmax = gioi_han(prof)
    if not smin <= len(shots) <= smax:
        loi.append(f"cần {smin}–{smax} shot, có {len(shots)}")
    # 2026-09-23 (vá review cuối, Việc 3a): model có thể trả JSON HỢP LỆ nhưng THIẾU khoá t0/t1
    # (vd chỉ có {"n":1,"voice":"…"}) — trước đây truy cập thẳng s["t0"] ném KeyError ra NGOÀI
    # vòng lặp 3 lần của sinh() (chỉ json.loads được bọc try/except), người vận hành nhận traceback
    # thay vì được thử lại kèm "LẦN TRƯỚC SAI: …". Coi thiếu khoá là 1 lỗi HỢP LỆ trong danh sách
    # trả về rồi DỪNG SỚM — mọi phép kiểm dựa trên t0/t1 bên dưới (tổng thời lượng, độ dài từng
    # shot, liên tục giữa 2 shot) không tính được khi thiếu mốc, tính bừa chỉ ra lỗi phái sinh gây
    # nhiễu (vd "tổng 0.0s ngoài khung giây").
    thieu_moc = [s for s in shots if s.get("t0") is None or s.get("t1") is None]
    if thieu_moc:
        for s in thieu_moc:
            loi.append(f"cảnh {s.get('n', '?')} thiếu trường t0/t1")
        return loi
    if shots:
        tong = shots[-1]["t1"] - shots[0]["t0"]
        if not gmin <= tong <= gmax:
            loi.append(f"tổng {tong:.1f}s ngoài {gmin}–{gmax}s")
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


def _anh_hook_da_ve_that(d):
    """2026-09-26 (vá sau sự cố ep04-jimusan-kyuka đốt 6 tài khoản Grok oan): nếu ảnh hook
    (`hook/img/*.png`) đã được máy 1 VẼ TAY và `grok_jobs.csv` đang trỏ đúng các ảnh đó (khác quy
    ước `shot_NN.png` mà `sinh()` tự tạo lúc chưa có ảnh), coi hook production của tập này ĐÃ XONG
    THỦ CÔNG — không được ghi đè `hook_storyboard.json`/`grok_jobs.csv`, vì làm vậy sẽ trỏ sang ảnh
    `shot_NN.png` không tồn tại và đốt tài khoản Grok cho job không chạy được (đã xảy ra thật)."""
    csv_p = Path(d) / "hook" / "grok_jobs.csv"
    if not csv_p.exists():
        return False
    try:
        rows = list(csv.DictReader(csv_p.open(encoding="utf-8-sig", newline="")))
    except Exception:
        return False
    if not rows:
        return False
    for row in rows:
        img = (row.get("image") or "").strip()
        if not img:
            return False
        p = Path(img)
        if not p.is_absolute():
            p = Path(d) / img
        if not p.exists():
            return False
    return True


def sinh(d, prof, force=False):
    d = Path(d)
    hook = hook_stage.doc_hook(d)
    lock = hook_stage.doc_lock(d)
    if not hook or not lock:
        raise SystemExit("✗ chưa có hook khoá — chạy hook_stage.py trước")
    out = d / "hook" / "hook_storyboard.json"
    if not force and _anh_hook_da_ve_that(d):
        print("  [hook] ảnh hook đã vẽ tay + grok_jobs.csv đang trỏ đúng ảnh thật → giữ nguyên, "
              "KHÔNG sinh lại storyboard (dùng --force nếu thật sự muốn làm lại từ đầu)")
        return json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    if out.exists() and not force:
        sb = json.loads(out.read_text(encoding="utf-8"))
        if sb.get("hook_sha256") == lock["sha256"]:
            return sb
    cr = profiles.char_rate(prof)
    chars = (d / "characters.json").read_text(encoding="utf-8")[:4000] if (d / "characters.json").exists() else "(chưa có characters.json — mô tả nhân vật theo hook)"
    smin, smax, gmin, gmax = gioi_han(prof)
    gc = d / "hook" / "ghi_chu_canh.txt"       # 01/10/2026: người soát ghi BỐI CẢNH THẬT từng câu (vd gọi điện thoại, không phải nói trực tiếp)
    ghi_chu = ("GHI CHÚ CẢNH BẮT BUỘC (đúng bối cảnh kịch bản, KHÔNG tự bịa khác đi):" + chr(10)
               + gc.read_text(encoding="utf-8").strip() + chr(10)) if gc.exists() else ""
    prompt = PROMPT.format(hook=hook, cr=cr, tong=ai_steps.measure(hook)["chars"] / cr * 60, chars=chars, ghi_chu=ghi_chu,
                           n_shot=f"{smin}–{smax}", khung_giay="toàn bộ hook đã khoá")
    sb = None
    r = None
    # 2026-09-23 (vá review cuối, Việc 3b): tích luỹ lỗi + phản hồi thô để có gì ghi vào
    # hook_storyboard.err.json khi hết 3 lượt vẫn không đạt (xem nhánh `else` bên dưới).
    loi_theo_lan = []
    for lan in range(3):
        r = ai_steps._writer_chat(prof, prompt, task="short", max_chars=(20000 if smax <= 7 else 70000))
        try:
            sb = json.loads(re.sub(r"^```[a-z]*\n?|\n?```$", "", r.text.strip()))
        except Exception as e:
            loi = [f"JSON hỏng: {type(e).__name__} {e}"]
            print(f"  ! JSON storyboard hỏng lần {lan+1}: {e}")
            loi_theo_lan.append({"lan": lan + 1, "loi": loi})
            prompt = prompt + "\n\nLẦN TRƯỚC SAI: " + " · ".join(loi) + " — sửa đúng."
            continue
        # Việc 3a: validate() giờ không còn ném KeyError khi thiếu t0/t1, nhưng vẫn bọc thêm 1 lớp
        # try/except ở ĐÂY (như brief gợi ý "và/hoặc") — phòng lỗi khác chưa lường hết (vd model
        # trả "shots" không phải list-of-dict) cũng không làm crash cả vòng lặp thử lại.
        try:
            loi = validate(sb, hook, cr, prof)
        except Exception as e:
            loi = [f"validate() lỗi: {type(e).__name__} {str(e)[:150]}"]
        if not loi:
            break
        print(f"  ! storyboard lần {lan+1}: " + " · ".join(loi))
        loi_theo_lan.append({"lan": lan + 1, "loi": loi})
        prompt = prompt + "\n\nLẦN TRƯỚC SAI: " + " · ".join(loi) + " — sửa đúng."
    else:
        # 2026-09-23 (vá review cuối, Việc 3b): trước đây câu thông báo nhắc mở
        # hook/hook_storyboard.err.json nhưng KHÔNG CÓ dòng code nào ghi file đó — người vận hành
        # mở ra thấy không tồn tại. Ghi THẬT: phản hồi thô của model ở LẦN CUỐI + toàn bộ lỗi đã
        # tích luỹ qua các lần, để biết chính xác model sai kiểu gì mà sửa prompt/đổi model.
        (d / "hook").mkdir(parents=True, exist_ok=True)
        err = {"hook": hook, "raw_response_lan_cuoi": r.text if r is not None else None,
               "loi_theo_lan": loi_theo_lan}
        (d / "hook" / "hook_storyboard.err.json").write_text(
            json.dumps(err, ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit("✗ storyboard không hợp lệ sau 3 lần — xem hook/hook_storyboard.err.json")
    sb["hook_sha256"] = lock["sha256"]
    sb["duration_target_s"] = round(sb["shots"][-1]["t1"], 1)
    # 2026-10-12 (Lane L ep15, đốt 32 tài khoản Grok oan): B5W gọi storyboard lúc ảnh hook đang vẽ tay → cổng ở đầu hàm
    # chưa thấy ảnh, LLM chạy ~3 phút, xong thì ĐÈ grok_jobs.csv đã trỏ ảnh thật → grok_da_luong chạy job shot_NN.png
    # không tồn tại. Kiểm LẠI ngay trước khi ghi; trúng → cất storyboard máy sang file riêng, không đụng grok_jobs.csv.
    if not force and _anh_hook_da_ve_that(d):
        alt = out.with_name("hook_storyboard.may_sinh.json")
        alt.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  [hook] trong lúc sinh, ảnh hook đã được vẽ tay → KHÔNG ghi đè grok_jobs.csv; storyboard máy cất ở {alt.name}")
        return sb
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
