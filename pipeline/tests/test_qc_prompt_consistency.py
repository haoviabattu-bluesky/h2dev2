import json, re
from pathlib import Path
import pytest
import qc_prompt_consistency as Q
import gate_common as G

CHARS = {"characters": [{"name": "Shizue", "age": 73, "gender": "F", "master": "_ref/001.png"}]}


def _rows(n, per=2):
    return [{"line_no": i, "ten": f"{i:03d}.png", "so": (i + per - 1) // per} for i in range(1, n + 1)]


def test_co_hoc_ref_va_so_luong():
    prompts = ["@REF a", "@REF2 b", "c"]
    rows = _rows(3)
    loi = Q.kiem_co_hoc(prompts, rows, CHARS)
    assert any("@REF2" in x for x in loi) and not any("@REF " in x for x in loi)
    assert Q.kiem_co_hoc(prompts, rows[:2], CHARS)[0].startswith("img_prompts.txt co 3")
    assert Q.kiem_co_hoc(prompts, None, CHARS) == [x for x in Q.kiem_co_hoc(prompts, None, CHARS) if "@REF2" in x]
    assert any("rong" in x for x in Q.kiem_co_hoc(["a", "   "], _rows(2), CHARS))


def test_sinh_facts_chunk(monkeypatch):
    doan = [f"doan {i}" for i in range(1, 24)]
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\[doan (\d+)\]", prompt)]
        return {"characters": {"Shizue": {"age": 73}},
                "timeline": [{"doan": i, "location": "home", "time": "day", "season": "", "facts": [f"f{i}"]} for i in ids if i != 5]}
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    f = Q.sinh_facts(doan, CHARS, chunk=10)
    assert len(calls) == 3 and len(f["timeline"]) == 23 and f["timeline"][22]["doan"] == 23
    assert f["timeline"][4] == {"doan": 5, "facts": []} and f["characters"]["Shizue"]["age"] == 73


def test_kiem_prompts_batch_conflict_ambiguous(monkeypatch):
    prompts = [f"p{i}" for i in range(1, 33)]
    rows = _rows(32)                                                   # doan 1..16
    facts = {"characters": {}, "timeline": [{"doan": i, "facts": [f"f{i}"]} for i in range(1, 17)]}
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        out = []
        for i in ids:
            if i == 20:
                out.append({"id": i, "status": "FAIL", "conflicts": [{"type": "character_state", "detail": "chong da mat"}]})
            elif i == 21:
                out.append({"id": i, "status": "AMBIGUOUS", "conflicts": [{"type": "object", "detail": "khong ro"}]})
            else:
                out.append({"id": i, "status": "PASS", "conflicts": []})
        return out
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    warns, conf, amb, n = Q.kiem_prompts(prompts, rows, facts, CHARS, batch=15)
    assert len(calls) == 3 and n == 32                                  # 32/15 = 3 batch
    assert "[doan 9]" in calls[1] and "[doan 4]" not in calls[1]        # batch 2 = prompt 16-30 -> doan 8-15 (+-1)
    assert len(conf) == 1 and conf[0]["id"] == 20 and conf[0]["category"] == "PROMPT_CONFLICT"
    assert len(amb) == 1 and amb[0]["id"] == 21
    assert any("020.png" in w and "PROMPT_CONFLICT" in w and "chong da mat" in w for w in warns)
    assert any("021.png" in w and "AMBIGUOUS" in w for w in warns)


def _tap(tmp_path, prompts=("@REF a", "b")):
    (tmp_path / "script.txt").write_text("d1\n\nd2", encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("\n".join(prompts), encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("001.png|1\n002.png|2", encoding="utf-8")
    (tmp_path / "characters.json").write_text(json.dumps(CHARS), encoding="utf-8")
    return tmp_path


def _latest(tmp_path):
    return json.loads((tmp_path / "logs" / "B5P_latest.json").read_text(encoding="utf-8"))


def _fake_chat(fail_ids, amb_ids=()):
    class R:
        def __init__(self, text): self.text = text
    def fake(prompt, **k):
        if "[doan" in prompt and "\"id\"" not in prompt:                 # loi goi facts
            ids = [int(x) for x in re.findall(r"\[doan (\d+)\]", prompt)]
            return R(json.dumps({"characters": {}, "timeline": [{"doan": i, "facts": []} for i in ids]}))
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return R(json.dumps([{"id": i, "status": "FAIL" if i in fail_ids else ("AMBIGUOUS" if i in amb_ids else "PASS"),
                              "conflicts": [{"type": "plot", "detail": "x"}] if i in fail_ids or i in amb_ids else []} for i in ids]))
    return fake


def test_cli_warn_only_ghi_would_block(tmp_path, monkeypatch):
    _tap(tmp_path)
    monkeypatch.setattr(Q.G.llm_client, "chat", _fake_chat({2}, {1}))
    assert Q.main(["--slug", str(tmp_path)]) == 0
    L = _latest(tmp_path); s = L["metrics"]["semantic"]
    assert L["status"] == "WARN" and s["ran"] and s["n_checked"] == 2
    assert s["n_would_block"] == 1 and s["would_block"] is True and s["n_ambiguous"] == 1 and s["n_warn"] == 2
    assert s["llm"]["calls"] >= 2 and (tmp_path / "story_facts.json").exists()
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail", "--reuse-facts"]) == 1
    assert any(b.startswith("semantic:") for b in _latest(tmp_path)["blocking_issues"])


def test_cli_ambiguous_khong_chan(tmp_path, monkeypatch):
    _tap(tmp_path)
    monkeypatch.setattr(Q.G.llm_client, "chat", _fake_chat(set(), {1, 2}))
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 0
    s = _latest(tmp_path)["metrics"]["semantic"]
    assert s["would_block"] is False and s["n_ambiguous"] == 2


def test_cli_no_llm_va_stale(tmp_path):
    _tap(tmp_path)
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 0
    assert _latest(tmp_path)["metrics"]["semantic"]["ran"] is False
    G.ghi_fingerprint(tmp_path)
    (tmp_path / "script.txt").write_text("d1 sua\n\nd2", encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("STALE" in b for b in _latest(tmp_path)["blocking_issues"])
