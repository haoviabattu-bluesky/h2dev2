import json
import pytest
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


# ---------------------------------------------------------------------------
# Vá review cuối (2026-09-23), Việc 3a+3b: model trả JSON hợp lệ nhưng THIẾU khoá t0/t1 không được
# ném KeyError ra ngoài vòng thử lại của sinh(), và hết 3 lượt vẫn sai thì phải GHI THẬT
# hook/hook_storyboard.err.json (trước đây thông báo nhắc file này nhưng không dòng code nào ghi).
# ---------------------------------------------------------------------------

def test_validate_thieu_t0_t1_khong_nem_key_error():
    """Việc 3a: JSON hợp lệ nhưng mỗi shot chỉ có {"n":.., "voice":..} — validate() phải trả về
    danh sách lỗi (không KeyError), và lỗi phải nêu đúng số cảnh thiếu trường."""
    sb = {"shots": [{"n": i + 1, "voice": "x"} for i in range(5)]}
    loi = SB.validate(sb, HOOK, 300.0)
    assert loi and all("thiếu trường t0/t1" in e for e in loi)
    assert len(loi) == 5  # đủ 5 cảnh, mỗi cảnh 1 lỗi thiếu mốc — không lẫn lỗi phái sinh khác


def test_sinh_model_thieu_moc_van_thu_lai_va_ghi_err_json(tmp_path, monkeypatch):
    """Việc 3a+3b end-to-end qua sinh(): model (giả) LUÔN trả JSON thiếu t0/t1 ở cả 3 lượt →
    không được crash bằng KeyError, phải thử đủ 3 lần (đếm số lượt gọi), rồi ném SystemExit VÀ ghi
    hook/hook_storyboard.err.json có nội dung (raw response lần cuối + lỗi từng lần)."""
    import ai_steps, hook_stage

    hook_stage.khoa(tmp_path, HOOK)  # ghi hook/hook_locked.txt + hook/hook_lock.json thật

    goi = {"n": 0}

    def _fake_writer_chat(prof, prompt, **kw):
        goi["n"] += 1
        raw = json.dumps({"shots": [{"n": 1, "voice": HOOK}]}, ensure_ascii=False)
        return type("R", (), {"text": raw})()

    monkeypatch.setattr(ai_steps, "_writer_chat", _fake_writer_chat)
    prof = {"id": "x", "voice": {"char_rate": 300.0}}

    with pytest.raises(SystemExit):
        SB.sinh(tmp_path, prof)

    assert goi["n"] == 3  # đủ 3 lượt thử lại, không dừng sớm vì KeyError
    err_f = tmp_path / "hook" / "hook_storyboard.err.json"
    assert err_f.exists()
    err = json.loads(err_f.read_text(encoding="utf-8"))
    assert err["raw_response_lan_cuoi"] and "voice" in err["raw_response_lan_cuoi"]
    assert len(err["loi_theo_lan"]) == 3
    assert all("thiếu trường t0/t1" in " ".join(x["loi"]) for x in err["loi_theo_lan"])
