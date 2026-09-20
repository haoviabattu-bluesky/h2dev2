# -*- coding: utf-8 -*-
r"""hybrid_chuan_bi.py — chay 1 lenh la lam HET phan buoc 1 cua tap hybrid (stock+AI), khong con
kieu "bao thieu roi dung lai cho hoi" nua.

BOI CANH (chot 2026-09-18, sau su co STT3 bi dung nham o cho khong can dung — anh mang vi bao
"thieu 14 slot STOCK/thieu audio/thieu anchors" ma khong tu lam):

  - buoc 2 (may 2, Google Flow) : CHI ve anh cho dong nhom AI trong stock_plan.tsv, tra ve
      FlowHandoff_local/results/<slug>/. May 2 KHONG tu copy vao img/, KHONG biet stock_plan.tsv.
  - buoc 1 (CHINH SCRIPT NAY, Claude Code chay)   :
      (a) dong STOCK nao bi audit_stock.py loai (status != OK: REJECT_FACE/REJECT_TEXT/BAD_FILE/NONE)
          -> TU DONG doi nhom sang AI_FALLBACK trong stock_plan.tsv (khong hoi lai);
      (b) TU SINH anh cho cac dong AI_FALLBACK do bang gpti2 qua gen_images.py (~50-110d/anh,
          CHO PHEP mac dinh vi re — khong con la "chua co chi dan xu ly ro" nua, chinh la chi dan);
      (c) copy anh nhom AI da xong tu FlowHandoff_local/results/<slug>/ vao img/ (day la viec
          CO HOC don gian nhung PHAI co nguoi lam — buoc 1 lam, khong doi buoc 3 tu di tim);
      (d) chay chuoi audio B4 (tts.py) -> B4.1 (srt_from_script.py) -> B4.2 (pace_audio.py) ->
          B4Q (qc_audio.py) — day la GATE CHAT LUONG that, rot thi DUNG that, khong tu sua;
      (e) sinh_neo.py -> anchors.txt (can img/ xong truoc, vi no doc so anh de chia neo).
  - buoc 3 (compositor hybrid, agent khac)   : CHI DOC input co san (muc 1 cua
      GIAO_VIEC_HYBRID_COMPOSITOR.md), KHONG duoc tu gen anh, KHONG duoc trich khung tinh tu
      stock/*.mp4 nhet vao img/ (rieng nhung dong STOCK that OK van la clip VIDEO that, do la viec
      cua compositor doc thang stock/manifest.csv, KHONG phai muc tieu cua script nay).

Neu buoc 1 chay script nay xong ma bao "DU DIEU KIEN GIAO BUOC 3" thi buoc 3 se KHONG BAO GIO gap
canh "thieu anh/thieu audio/thieu anchors" nua — gap tuc la buoc 1 CHUA chay du, khong phai loi
thiet ke.

Dung (goi lai duoc nhieu lan, tu bo qua phan da xong):
  py -3.13 hybrid_chuan_bi.py --slug ..\assets\satori_jp\<slug> --profile satori-jp-obaa
"""
import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_common   # noqa: E402  (rao STALE fingerprint, P0 2026-09-18)
import qc_img_doan   # noqa: E402  (rao invariant mapping img_doan.txt, P0 2026-09-18)


def read_tsv(path: Path):
    rows = list(csv.reader(path.open(encoding="utf-8", newline=""), delimiter="\t"))
    return rows[0], rows[1:]


def write_tsv(path: Path, header, body):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(header)
        w.writerows(body)


def manifest_status(slug: Path):
    m = slug / "stock" / "manifest.csv"
    if not m.is_file():
        return {}
    rows = list(csv.DictReader(m.open(encoding="utf-8-sig", newline="")))
    out = {}
    for r in rows:
        ln = r.get("prompt_line")
        if ln and ln != "0":
            out[int(ln)] = r["status"]
    return out


def run(cmd):
    cmd = [str(c) for c in cmd]
    print("$", " ".join(cmd))
    return subprocess.run(cmd).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="thu muc tap, vd ..\\assets\\satori_jp\\simbot2-03-...")
    ap.add_argument("--profile", required=True, help="id profile giong doc (pipeline/profiles), vd satori-jp-obaa")
    ap.add_argument("--flowhandoff", default=None,
                     help="thu muc anh AI may 2 tra ve (mac dinh FlowHandoff_local/results/<ten_tap>)")
    a = ap.parse_args()

    slug = Path(a.slug).resolve()
    name = slug.name
    plan_path = slug / "stock_plan.tsv"
    prompts_path = slug / "img_prompts.txt"
    img_dir = slug / "img"
    img_dir.mkdir(exist_ok=True)

    if not plan_path.is_file():
        print(f"Khong co {plan_path} -- tap nay KHONG PHAI hybrid, dung sai tool (dung render_engine.py chuan).")
        sys.exit(1)
    if not prompts_path.is_file():
        print(f"Thieu {prompts_path}."); sys.exit(1)

    # ---- A. Dong STOCK bi audit loai -> AI_FALLBACK (tu dong, khong hoi) --------------------
    header, body = read_tsv(plan_path)
    status = manifest_status(slug)
    changed = []
    for row in body:
        ln = int(row[0])
        if row[1] == "STOCK" and status.get(ln) != "OK":
            row[1] = "AI_FALLBACK"
            changed.append(ln)
    if changed:
        write_tsv(plan_path, header, body)
        print(f"[A] Doi {len(changed)} dong STOCK bi audit loai -> AI_FALLBACK: {changed}")
    else:
        print("[A] Khong co dong nao can doi nhom (da xong tu truoc, hoac tap khong co stock bi loai).")

    header, body = read_tsv(plan_path)  # doc lai cho chac sau khi ghi
    ai_group = {int(r[0]) for r in body if r[1] == "AI"}
    fallback_group = {int(r[0]) for r in body if r[1] == "AI_FALLBACK"}
    stock_ok_lines = sorted(int(r[0]) for r in body if r[1] == "STOCK")
    ai_lines = sorted(ai_group | fallback_group)

    # ---- B. Copy anh nhom AI tu FlowHandoff (may 2) vao img/ --------------------------------
    fh = Path(a.flowhandoff) if a.flowhandoff else (HERE.parent / "FlowHandoff_local" / "results" / name)
    copied = 0
    if fh.is_dir():
        for p in fh.glob("*.png"):
            dst = img_dir / p.name
            if not dst.is_file():
                shutil.copy2(p, dst)
                copied += 1
    print(f"[B] Copy {copied} anh moi tu {fh} vao img/.")

    have = {int(p.stem) for p in img_dir.glob("*.png") if p.stem.isdigit()}
    need = sorted(set(ai_lines) - have)
    still_wait_may2 = sorted(n for n in need if n in ai_group)
    if still_wait_may2:
        print(f"[B] !! Con {len(still_wait_may2)} anh nhom AI may 2 CHUA tra ve: {still_wait_may2}")
        print("     -- day la viec BUOC 2 (may 2), buoc 1 KHONG tu ve thay.")

    # ---- C. Tu sinh AI_FALLBACK con thieu bang gpti2 (cho phep mac dinh, khong hoi) --------
    need_fallback = sorted(n for n in need if n in fallback_group)
    # Master REF: doc tu characters.json (tap moi de master o _ref/001.png + _ref_<ten>/001.png,
    # khong con _ref/002.png nhu tap cu) — fallback ve duong cu neu khong co characters.json.
    ref, ref2 = slug / "_ref" / "001.png", slug / "_ref" / "002.png"
    try:
        chars = json.loads((slug / "characters.json").read_text(encoding="utf-8")).get("characters") or []
        masters = [slug / c["master"] for c in chars if c.get("master")]
        if masters:
            ref = masters[0]
        if len(masters) > 1:
            ref2 = masters[1]
    except Exception:
        pass
    ref_args = ["--ref", ref] if ref.is_file() else []
    ref2_args = ["--ref2", ref2] if ref2.is_file() else []
    for ln in need_fallback:
        rc = run([sys.executable, HERE / "gen_images.py", "--prompts", prompts_path, "--out", img_dir,
                  "--quality", "low", "--start", ln, "--limit", 1] + ref_args + ref2_args)
        if rc != 0:
            print(f"[C] !! gen_images.py loi o dong {ln}, dung lai kiem tra."); sys.exit(1)
    if need_fallback:
        print(f"[C] Da tu sinh {len(need_fallback)} anh AI_FALLBACK bang gpti2: {need_fallback}")

    have = {int(p.stem) for p in img_dir.glob("*.png") if p.stem.isdigit()}
    missing = sorted(set(ai_lines) - have)
    extra_stock = sorted(have & set(stock_ok_lines))
    print(f"\n=== img/: co {len(have)}, can {len(ai_lines)} (AI+AI_FALLBACK) — "
          f"{len(stock_ok_lines)} dong STOCK that KHONG can nam o day ===")
    if extra_stock:
        print(f"  !! CANH BAO: {len(extra_stock)} anh dang nam TRUNG dong STOCK that (sai): {extra_stock}")
    if missing or still_wait_may2:
        print("\n>> CHUA DU anh, DUNG o day. Xem danh sach thieu o tren de biet buoc nao phai lam tiep.")
        sys.exit(1)

    # ---- D. Chuoi audio B4->B4.1->B4.2->B4Q (chi chay khi img/ da du) ----------------------
    voice = slug / "voice.mp3"
    voice_srt = slug / "voice.srt"
    paced_wav = slug / "voice_paced.wav"
    paced_srt = slug / "voice_paced.srt"
    anchors = slug / "anchors.txt"
    script_txt = slug / "script.txt"

    if not (paced_wav.is_file() and paced_srt.is_file()):
        if not voice.is_file():
            if run([sys.executable, HERE / "tts.py", "--script", script_txt, "--provider", "openspeaker",
                    "--profile", a.profile, "--out", voice]) != 0:
                print("[D] tts.py loi, dung lai."); sys.exit(1)
        if run([sys.executable, HERE / "srt_from_script.py", "--srt", voice_srt, "--script", script_txt]) != 0:
            print("[D] srt_from_script.py loi, dung lai."); sys.exit(1)
        if run([sys.executable, HERE / "pace_audio.py", "--audio", voice, "--srt", voice_srt,
                "--script", script_txt]) != 0:
            print("[D] pace_audio.py loi, dung lai."); sys.exit(1)
    else:
        print("[D] voice_paced.wav/srt da co san, bo qua B4.")

    if run([sys.executable, HERE / "qc_audio.py", "--audio", paced_wav, "--srt", paced_srt]) != 0:
        print("\n>> B4Q RUOT — cong CHAT LUONG NOI DUNG that, KHONG tu sua/gen lai. Bao lai dong tren.")
        sys.exit(1)

    # RAO INVARIANT (P0 2026-09-18): STALE (hash script khac luc sinh asset) -> FAIL; mapping vi pham
    # invariant -> FAIL. Chia deu chi la SUSPICIOUS (warn) — nhac chay semantic QC truoc khi giao.
    b_stale, w_stale = gate_common.kiem_stale(slug)
    for v in w_stale:
        print("[E] ⚠", v)
        if "chua co" in v and "fingerprint" in v:
            print(f"[E]    -> stamp: py -3.13 {HERE / 'gate_common.py'} --slug {slug} --stamp (sau khi xong B5/B5.5)")
    if b_stale:
        for v in b_stale:
            print("[E] !!", v)
        sys.exit(1)
    if qc_img_doan.main(["--slug", str(slug), "--no-llm"]) != 0:
        print("[E] !! img_doan.txt rot invariant (xem logs/B55_mapping_latest.json) — sua roi chay lai"); sys.exit(1)
    try:
        import json as _json
        _kq = _json.loads((slug / "logs" / "B55_mapping_latest.json").read_text(encoding="utf-8"))
        if (_kq.get("metrics") or {}).get("suspicious"):
            print(f"[E] ⚠ mapping SUSPICIOUS (chia deu) — chay `py -3.13 {HERE / 'qc_img_doan.py'} --slug {slug}` "
                  "(co LLM) truoc khi giao; mode warn nen KHONG chan o day.")
    except Exception:
        pass

    # ---- E. anchors.txt ---------------------------------------------------------------------
    if not anchors.is_file():
        if run([sys.executable, HERE / "sinh_neo.py", "--slug", slug]) != 0:
            print("[E] sinh_neo.py loi, dung lai."); sys.exit(1)
    else:
        print("[E] anchors.txt da co san, bo qua.")

    print("\n=== DU DIEU KIEN GIAO BUOC 3 (compositor hybrid, xem GIAO_VIEC_HYBRID_COMPOSITOR.md muc 1) ===")
    print(f"  img/*.png       : {len(list(img_dir.glob('*.png')))}")
    print(f"  voice_paced.wav : {'OK' if paced_wav.is_file() else 'THIEU'}")
    print(f"  voice_paced.srt : {'OK' if paced_srt.is_file() else 'THIEU'}")
    print(f"  anchors.txt     : {'OK' if anchors.is_file() else 'THIEU'}")
    print("  stock/manifest.csv + stock/_filler/*  : khong dong, giu nguyen cho buoc 3 doc thang.")


if __name__ == "__main__":
    main()
