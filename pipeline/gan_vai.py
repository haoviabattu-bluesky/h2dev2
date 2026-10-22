# -*- coding: utf-8 -*-
r"""gan_vai.py — gắn VAI (ai đọc) cho từng câu của script.txt đã KHOÁ → vai.txt (lane đa giọng, Lane K 2026-09-24).

Vì sao: kênh mẫu đọc mỗi vai một giọng VOICEVOX, kể cả câu nội tâm「俺…」(giọng nhân vật chính, không phải người
kể) — docs/channel_dna/yakkyoku-sukatto/GIONG_VAI.md. Quyết định "câu này ai nói" cần HIỂU NỘI DUNG → việc của
máy 1 (bước 1); tts_voicevox.py (máy 2) và bóng thoại chỉ đọc vai.txt, không đoán.

Model: script.patch_model (Opus) qua claude -p — KHÔNG chạm script.txt (chỉ đọc bản khoá).
Máy kiểm (sai → hỏi lại 1 lượt → vẫn sai thì DỪNG, không vá tay):
  - đủ số câu, đúng thứ tự (định dạng `n|id`)
  - id thuộc {"ke"} ∪ characters.json
  - câu「…」 (thoại) KHÔNG được là "ke"
  - vai có thoại phải có `voice` trong characters.json (tts cần giọng) và nên `ref: true` (bóng thoại cần mặt)

Dùng: py -3.13 gan_vai.py --profile yakkyoku-sukatto --slug <thư mục tập>
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import age_lock_guard     # noqa: E402
import cau_vai            # noqa: E402
import claude_p_bridge    # noqa: E402
import gate_common        # noqa: E402
import kho_giong          # noqa: E402
import profiles           # noqa: E402
from llm_client import LLMError  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
MAX_HOI_LAI = 1


def _prompt(prof, cau, chars, title=""):
    cast = "\n".join(f"- {c['id']}: {c.get('name','')} ({c.get('vai','')}; {c.get('gender','')}, {c.get('age','')}歳)"
                     + (f" 口ぐせ「{c['kuchiguse']}」" if c.get("kuchiguse") else "")
                     for c in chars)
    shu = next((c["id"] for c in chars if c.get("main") or c.get("id") == "shu"), chars[0]["id"] if chars else "shu")
    # Lane L (2026-09-24): câu nội tâm không phải của nhân vật chính mà của người dẫn (さくら) → khai
    # characters.json[].inner_voice = true cho vai sở hữu 心の声; không khai = nhân vật chính như Lane K.
    shu = next((c["id"] for c in chars if c.get("inner_voice")), shu)
    ds = "\n".join(f"{c['i']}. {c['text']}" for c in cau)
    return (
        "あなたは日本語の漫画動画（ナレーション＋複数キャラクターの声）の音声ディレクターです。\n"
        "下の台本の各文を『誰の声で読むか』に割り当ててください。\n"
        + (f"動画タイトル: {title}\n" if title else "")
        + "冒頭の「」の一文や、口ぐせと同じ台詞は、その口ぐせの持ち主（主人公）のもの。\n\n"
        f"話者ID:\n- ke: ナレーター（三人称の地の文。「彼は〜」「店長は〜」など）\n{cast}\n\n"
        "ルール:\n"
        "1. 「」だけの文（台詞）は、その台詞を実際に言っている登場人物のID。ke は絶対に使わない。"
        "前後の地の文・文脈から話し手を判断する（電話の相手・患者なども上の一覧から選ぶ）。\n"
        f"2. 括弧なしの一人称の心の声（「俺は〜」「自分は〜」「〜だろう。」「〜だったんだ。」など内心の独白）は {shu}。\n"
        "3. それ以外の地の文は ke。\n"
        "4. 一覧にいない人物の台詞なら、性別・立場が最も近い一覧の人物のIDを使う（新しいIDは作らない）。\n\n"
        "出力形式（厳守）: 1行に1文、`番号|ID` のみ。説明・空行・マークダウン禁止。全文を番号順に。\n\n"
        f"台本（{len(cau)}文）:\n{ds}")


def _parse(text, cau, ids_ok):
    loi, got = [], {}
    for ln in text.splitlines():
        m = re.match(r"^\s*(\d+)\s*\|\s*([A-Za-z0-9_\-]+)\s*$", ln.strip())
        if m:
            got[int(m.group(1))] = m.group(2)
    thieu = [c["i"] for c in cau if c["i"] not in got]
    if thieu:
        loi.append(f"thiếu {len(thieu)} câu: {thieu[:10]}")
    for k, c in enumerate(cau):
        v = got.get(c["i"])
        if v is None:
            continue
        # 「」 kẹp giữa câu người kể cùng dòng (特別養護老人ホーム「けやきの里」。/ 自分の「ミスほぼゼロ」は) = tên/trích dẫn, không phải thoại
        truoc = cau[k - 1] if k else None
        giua_cau = bool(truoc and truoc["para"] == c["para"] and not truoc["text"].endswith(tuple(cau_vai._END + "」』")))
        # 「」 đứng riêng nhưng chỉ là CHỮ IN (biển/tin tuyển 「年齢不問」): ngắn, không hiragana = không phải lời nói (Lane M ep15)
        chu_in = bool(re.fullmatch(r"「[^぀-ゟ。！？!?]{1,12}」", cau_vai._chuan(c["text"])))
        if v not in ids_ok:
            loi.append(f"câu {c['i']}: id lạ {v!r}")
        elif cau_vai.la_thoai(c["text"]) and v == cau_vai.KE and not giua_cau and not chu_in:
            loi.append(f"câu {c['i']} là thoại「」nhưng gán ke: {c['text'][:30]}")
    return [got.get(c["i"]) for c in cau], loi


def chay(prof, slug):
    d = Path(slug)
    ok, msg, lv = gate_common.kiem_lock(d)
    if not ok:
        raise SystemExit(f"✗ gan_vai: {msg}")
    cf = d / "characters.json"
    if not cf.exists():
        raise SystemExit(f"✗ thiếu {cf} — lớp 1 viết characters.json (id, name, vai, age, gender, look, ref, voice) trước")
    # 22/10 (anh): giọng vai lấy theo KHO GIỌNG chung theo khung tuổi — tự điền/sửa, cụ bà không được giọng trẻ
    kho_giong.chan(prof, cf)
    chars = json.loads(cf.read_text(encoding="utf-8")).get("characters") or []
    age_lock_guard.chan(chars, str(cf))
    cau = cau_vai.tach_cau((d / "script.txt").read_text(encoding="utf-8"))
    ids_ok = {cau_vai.KE} | {c["id"] for c in chars}
    title = (d / "title.txt").read_text(encoding="utf-8").strip() if (d / "title.txt").exists() else ""
    prompt = _prompt(prof, cau, chars, title)
    model = claude_p_bridge.patch_model_of(prof)
    ids, loi = [], []
    (d / "logs").mkdir(exist_ok=True)
    for luot in range(MAX_HOI_LAI + 1):
        q = prompt if not loi else prompt + "\n\n前回の回答は不合格。次をすべて直して全文を出し直すこと:\n- " + "\n- ".join(loi[:15])
        try:
            r = claude_p_bridge.ask(q, model=model, timeout=1500, min_chars=len(cau) * 3)
        except LLMError as e:
            raise SystemExit(f"✗ gan_vai: claude -p lỗi: {e}")
        (d / "logs" / f"gan_vai_raw{luot + 1}.txt").write_text(r.text, encoding="utf-8")
        ids, loi = _parse(r.text, cau, ids_ok)
        print(f"[gan_vai] lượt {luot + 1}: {len(cau)} câu · {r.elapsed:.0f}s" + (f" · {len(loi)} lỗi" if loi else " · hợp lệ"))
        if not loi:
            break
        for x in loi[:6]:
            print("   -", x)
    if loi:
        raise SystemExit(f"✗ gan_vai: sau {MAX_HOI_LAI + 1} lượt vẫn {len(loi)} lỗi → DỪNG (không vá tay)")
    # kiểm characters.json theo vai thật
    co_thoai = {v for v in ids if v != cau_vai.KE}
    by = {c["id"]: c for c in chars}
    thieu_giong = [v for v in co_thoai if not by[v].get("voice")]
    if thieu_giong:
        raise SystemExit(f"✗ characters.json: vai có lời nhưng chưa khai voice: {thieu_giong}")
    khong_ref = [v for v in co_thoai if not by[v].get("ref")]
    if khong_ref:
        print(f"  ! vai có lời nhưng ref:false (bóng thoại/ảnh sẽ không khoá mặt): {khong_ref}")
    cau_vai.ghi_vai(d / "vai.txt", cau, ids)
    dem = {v: ids.count(v) for v in dict.fromkeys(ids)}
    print(f"[gan_vai] ✓ vai.txt: " + " · ".join(f"{k} {n}" for k, n in dem.items()))
    return dem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    chay(profiles.load(a.profile), a.slug)


if __name__ == "__main__":
    main()
