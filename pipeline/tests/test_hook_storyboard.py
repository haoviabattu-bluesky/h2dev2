import json
import hook_storyboard as SB

HOOK = "「三年前に引っ越しました」隣人は言った。五十年の友が消えた。私は箱を抱えたまま立ち尽くした。理由は後で知った。"


def _sb(n=5, total=25.0):
    step = total / n
    # 2026-09-23: fix so với brief — bản gốc lặp lại phần tử cuối ("理由は後で知った。" x2) làm
    # tổng 5 voice-part KHÔNG còn ghép đúng ra HOOK (thừa 1 câu) → test_validate_ok() sẽ luôn FAIL
    # vì cổng "ghép voice ≠ hook" tự bắt lỗi đúng như thiết kế. Sửa bằng cách tách câu 3 làm 2 mảnh
    # liền nhau ("私は箱を抱えたまま" + "立ち尽くした。") thay vì lặp câu 4 — vẫn 5 phần tử, vẫn
    # ghép nguyên văn đúng HOOK, giữ nguyên ý đồ test (n shot tối đa 5).
    voice_parts = ["「三年前に引っ越しました」隣人は言った。", "五十年の友が消えた。", "私は箱を抱えたまま", "立ち尽くした。", "理由は後で知った。"][:n]
    return {"shots": [{"n": i + 1, "t0": round(i * step, 1), "t1": round((i + 1) * step, 1), "voice": voice_parts[i % len(voice_parts)],
                       "visual": "v", "shot_type": "close-up", "ref_image": "REF", "flow_prompt": "p", "continuity": "c"} for i in range(n)]}


def test_validate_ok():
    assert SB.validate(_sb(), HOOK, 300.0) == []


def test_validate_bat_loi():
    assert any("4–7" in e for e in SB.validate(_sb(3), HOOK, 300.0))
    assert any("20–30" in e for e in SB.validate(_sb(5, 45.0), HOOK, 300.0))
    bad = _sb(); bad["shots"][0]["voice"] = "文なし"
    assert any("voice" in e for e in SB.validate(bad, HOOK, 300.0))
    bad = _sb(); bad["shots"][2]["t0"] = 99
    assert any("liên tục" in e for e in SB.validate(bad, HOOK, 300.0))


def test_jobs_csv(tmp_path):
    (tmp_path / "hook").mkdir()
    sb = _sb()
    SB.ghi_flow_prompts_va_jobs(tmp_path, sb)
    rows = (tmp_path / "hook/grok_jobs.csv").read_text(encoding="utf-8-sig").splitlines()
    assert rows[0] == "id,image,prompt,duration,resolution,aspect" and len(rows) == 6
    assert rows[1].split(",")[3] == "6"
    assert (tmp_path / "hook/flow_prompts/shot_01.txt").exists()
