# -*- coding: utf-8 -*-
"""QC cảnh HOOK bằng vision (GPT-5.6-sol qua sol_client) — chấm ẢNH trước khi đưa Grok và CLIP sau khi Grok sinh.

Lý do có (anh chốt 2026-09-24): kenko ep01 từng ra clip chỉ có bàn tay + cái ghế, không thấy người đang khổ sở
đứng dậy — mà không cổng nào bắt. Hook phải thể hiện TRẠNG THÁI nhân vật (vui/khoẻ/khổ/lo...) theo ngữ cảnh.

    py -3.13 qc_hook_clip.py --hook <thư mục hook> --clip 5          (1 clip)
    py -3.13 qc_hook_clip.py --hook <thư mục hook> --all             (mọi clip đang có)
    py -3.13 qc_hook_clip.py --hook <thư mục hook> --anh 6           (chấm ẢNH nguồn trước khi tốn lượt Grok)

Đọc `hook_timeline.json` → shots[n].voice (lời) + shots[n].ky_vong (nội dung + CẢM XÚC bắt buộc).
Clip: cắt 4 khung (0,5s · 2s · 3,5s · cuối) ghép 1 tấm → Sol chấm 6 tiêu chí → hook/qc/clip_NN.json.
Exit code 1 nếu có cảnh FAIL (để script gọi dừng được).
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sol_client  # noqa: E402

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"

TIEU_CHI = """Chấm theo 6 tiêu chí, mỗi tiêu chí true/false:
- thay_mat: thấy rõ MẶT nhân vật chính (không phải chỉ tay/đồ vật/cảnh trống) ở phần lớn khung
- cam_xuc_dung: biểu cảm khuôn mặt đúng cảm xúc KỲ VỌNG (vd lo lắng, gắng sức, vui vẻ...)
- hanh_dong_dung: hành động/bối cảnh đúng KỲ VỌNG
- khong_meo: không méo mặt, không thừa/thiếu ngón tay/chân tay, mặt không biến dạng giữa các khung
- khong_chu: không có chữ, logo, watermark trên hình
- nhat_quan: cùng một người, cùng quần áo/tóc xuyên các khung
Trả về DUY NHẤT một JSON: {"thay_mat":bool,"cam_xuc_dung":bool,"hanh_dong_dung":bool,"khong_meo":bool,
"khong_chu":bool,"nhat_quan":bool,"ly_do":"1-2 câu tiếng Việt nêu cái sai cụ thể hoặc 'đạt'"}"""


def _khung(clip: Path, out: Path):
    dur = float(re.search(r"Duration: \d+:\d+:([\d.]+)",
                          subprocess.run([FF, "-i", str(clip)], capture_output=True, text=True,
                                         encoding="utf-8", errors="replace").stderr).group(1))
    ts = [0.5, dur * 0.35, dur * 0.6, max(0.1, dur - 0.2)]
    sel = "+".join(f"eq(n\\,{int(t * 24)})" for t in ts)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(clip), "-vf",
                    f"select='{sel}',scale=640:-1,tile=2x2", "-vsync", "0", "-frames:v", "1", str(out)], check=True)


def cham(hook: Path, n: int, anh: bool = False) -> dict:
    tl = json.loads((hook / "hook_timeline.json").read_text(encoding="utf-8"))
    s = next(x for x in tl["shots"] if x["n"] == n)
    if not s.get("ky_vong"):
        sys.exit(f"✗ shot {n} thiếu 'ky_vong' trong hook_timeline.json — khai nội dung + cảm xúc bắt buộc trước")
    if anh:
        img, loai = hook / s["img"], "ẢNH NGUỒN (sẽ đưa vào Grok làm video)"
    else:
        img = Path(tempfile.gettempdir()) / f"qc_hook_{n:02d}.jpg"
        _khung(hook / s["clip"], img)
        loai = "4 KHUNG của 1 clip video 6 giây (trái→phải, trên→dưới theo thời gian)"
    prompt = (f"Bạn là QC hình cho đoạn HOOK mở đầu video YouTube. Hình gửi kèm là {loai}.\n"
              f"Lời thoại lúc cảnh này chạy (tiếng Nhật): {s['voice']}\n"
              f"KỲ VỌNG (nội dung + cảm xúc bắt buộc): {s['ky_vong']}\n\n{TIEU_CHI}")
    text, _ = sol_client.chat(prompt, image_path=str(img), max_tokens=800)
    m = re.search(r"\{.*\}", text, re.S)
    try:
        kq = json.loads(m.group(0)) if m else {}
    except Exception:
        kq = {}
    keys = ["thay_mat", "cam_xuc_dung", "hanh_dong_dung", "khong_meo", "khong_chu", "nhat_quan"]
    thieu = [k for k in keys if k not in kq]
    kq["verdict"] = "PASS" if not thieu and all(kq[k] is True for k in keys) else "FAIL"
    if thieu:
        kq["ly_do"] = f"Sol trả thiếu tiêu chí {thieu} → coi là FAIL. Raw: {text[:200]}"
    kq.update({"n": n, "loai": "anh" if anh else "clip", "file": str(img if anh else hook / s["clip"])})
    (hook / "qc").mkdir(exist_ok=True)
    (hook / "qc" / f"{'anh' if anh else 'clip'}_{n:02d}.json").write_text(
        json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--clip", type=int)
    g.add_argument("--anh", type=int)
    g.add_argument("--all", action="store_true")
    a = ap.parse_args()
    hook = Path(a.hook)
    tl = json.loads((hook / "hook_timeline.json").read_text(encoding="utf-8"))
    if a.all:
        viec = [(s["n"], False) for s in tl["shots"] if (hook / s["clip"]).exists()]
    elif a.anh:
        viec = [(a.anh, True)]
    else:
        viec = [(a.clip, False)]
    fail = 0
    for n, anh in viec:
        kq = cham(hook, n, anh)
        fail += kq["verdict"] != "PASS"
        sai = [k for k in ("thay_mat", "cam_xuc_dung", "hanh_dong_dung", "khong_meo", "khong_chu", "nhat_quan")
               if kq.get(k) is not True]
        print(f"{'ảnh' if anh else 'clip'} {n}: {kq['verdict']}  {('sai: ' + ','.join(sai)) if sai else ''} — {kq.get('ly_do', '')}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
