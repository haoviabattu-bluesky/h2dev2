import json, re
from pathlib import Path
import pytest
import qc_img_doan as Q
import gate_common as G


def _rows(counts):
    out, i = [], 1
    for doan, n in enumerate(counts, 1):
        for _ in range(n):
            out.append({"line_no": i, "ten": f"{i:03d}.png", "so": doan}); i += 1
    return out


def _viet(tmp_path, counts, n_doan=None, prompts=None):
    n_doan = n_doan or len(counts)
    rows = _rows(counts)
    (tmp_path / "script.txt").write_text("\n\n".join(f"doan {i}。" for i in range(1, n_doan + 1)), encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("\n".join(prompts or [f"p{i}" for i in range(1, len(rows) + 1)]), encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("\n".join(f"{r['ten']}|{r['so']}" for r in rows), encoding="utf-8")
    return tmp_path


def test_doc_pairs_giu_thu_tu_va_trung(tmp_path):
    f = tmp_path / "img_doan.txt"
    f.write_text("# ghi chu\n002.png|3\n001.png|1\n002.png|3\n\nxyz\n004.png|abc\n|5\n", encoding="utf-8")
    rows, mal = Q.doc_pairs(f)
    assert [r["ten"] for r in rows] == ["002.png", "001.png", "002.png"]
    assert rows[0]["line_no"] == 2 and rows[1]["so"] == 1
    assert len(mal) == 3 and all("malformed" in m for m in mal) and "dong 6" in mal[0]


def test_co_hoc_dat():
    rows = _rows([2, 5, 3, 3, 2, 4, 3, 2, 5, 2, 2, 3, 4, 3, 3, 2, 3, 5, 2, 3, 3, 2])
    b, s, m = Q.kiem_co_hoc(rows, n_doan=22, n_prompt=len(rows))
    assert b == [] and s == [] and m["n_anh"] == len(rows) and m["chia_deu"] is False


def test_co_hoc_chia_deu_chi_suspicious():
    rows = _rows([2, 3] * 25)
    b, s, m = Q.kiem_co_hoc(rows, n_doan=50, n_prompt=125)
    assert b == [] and m["chia_deu"] is True and any("SUSPICIOUS" in x and "xen ke" in x for x in s)


def test_co_hoc_lech_bat_thuong_suspicious():
    counts = [0] * 8 + [9, 1, 2, 0, 1, 1, 1, 0, 1, 1, 1, 1]      # 10/20 doan 0 anh, 1 doan 9 anh
    b, s, m = Q.kiem_co_hoc(_rows(counts), n_doan=20, n_prompt=sum(counts))
    assert b == [] and any("lech bat thuong" in x for x in s)


def test_co_hoc_giam_ngoai_pham_vi_trung_thieu():
    rows = [{"line_no": 1, "ten": "001.png", "so": 1}, {"line_no": 2, "ten": "003.png", "so": 3},
            {"line_no": 3, "ten": "003.png", "so": 2}, {"line_no": 4, "ten": "009.png", "so": 9}]
    b, s, m = Q.kiem_co_hoc(rows, n_doan=5, n_prompt=4)
    j = " | ".join(b)
    assert "GIAM" in j and "ngoai pham vi" in j and "trung ten" in j
    assert "thieu ID" in j and "002.png" in j and "004.png" in j and "009.png" in j   # 009 ngoai tap hop le


def test_co_hoc_required_data_thieu():
    b, s, m = Q.kiem_co_hoc([], n_doan=0, n_prompt=0)
    assert any("required" in x.lower() or "thieu" in x for x in b)


def test_semantic_chunk_shortlist_va_n_checked(monkeypatch):
    doan = [f"doan {i} noi ve viec {i}" for i in range(1, 11)]
    prompts = [f"prompt {i}" for i in range(1, 21)]
    rows = [{"line_no": i, "ten": f"{i:03d}.png", "so": (i + 1) // 2} for i in range(1, 21)]
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return [{"id": i, "score": 1 if i == 7 else 5, "reason": "r", "better_doan": 6 if i == 7 else None} for i in ids]
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    warns, thap, n_checked = Q.kiem_semantic(rows, doan, prompts, chunk=8)
    assert len(calls) == 2 and n_checked == 20
    assert len(thap) == 1 and thap[0]["id"] == 7 and "007.png" in warns[0] and "doan 6" in warns[0]


def test_semantic_ha_tang_thanh_qcerror(monkeypatch):
    def boom(*a, **k): raise G.QcError("503")
    monkeypatch.setattr(Q.G, "goi_llm_json", boom)
    with pytest.raises(G.QcError):
        Q.kiem_semantic([{"line_no": 1, "ten": "001.png", "so": 1}], ["d1"], ["p1"])


def _fake_llm(sai_ids):
    def fake(prompt, **k):
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return [{"id": i, "score": 1 if i in sai_ids else 5, "reason": "sai canh", "better_doan": None} for i in ids]
    return fake


def _latest(tmp_path):
    return json.loads((tmp_path / "logs" / "B55_mapping_latest.json").read_text(encoding="utf-8"))


def test_cli_suspicious_no_llm_warn(tmp_path):
    _viet(tmp_path, [2, 3] * 25)
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 0
    L = _latest(tmp_path)
    assert L["status"] == "WARN" and L["metrics"]["chia_deu"] is True
    assert any("SUSPICIOUS" in w for w in L["warnings"]) and any("bo qua semantic" in w for w in L["warnings"])


def _fake_chat(sai_ids):
    # Mock o tang llm_client.chat (KHONG phai goi_llm_json) de LLM_STATS that su duoc cong don,
    # dung quy uoc da co trong tests/test_gate_common.py (test_llm_stats_cong_don).
    class R:
        def __init__(self, text):
            self.text = text
    def fake(prompt, **k):
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        data = [{"id": i, "score": 1 if i in sai_ids else 5, "reason": "sai canh", "better_doan": None} for i in ids]
        return R(json.dumps(data))
    return fake


def test_cli_mode_warn_ghi_would_block(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G.llm_client, "chat", _fake_chat({10, 20, 30}))
    assert Q.main(["--slug", str(tmp_path)]) == 0                      # mode warn: khong chan
    L = _latest(tmp_path)
    s = L["metrics"]["semantic"]
    assert L["status"] == "WARN" and s["would_block"] is True and s["n_would_block"] == 3
    assert s["n_checked"] == 125 and s["n_warn"] == 3 and s["llm"]["calls"] >= 7


def test_cli_mode_fail_chan_theo_semantic(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G, "goi_llm_json", _fake_llm({10, 20, 30}))
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 1
    L = _latest(tmp_path)
    assert L["status"] == "FAIL" and any(b.startswith("semantic:") for b in L["blocking_issues"])


def test_cli_khong_fail_chi_vi_histogram(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G, "goi_llm_json", _fake_llm(set()))       # semantic sach
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 0
    L = _latest(tmp_path)
    assert L["status"] == "WARN" and L["metrics"]["semantic"]["would_block"] is False


def test_cli_malformed_va_stale_la_fail(tmp_path, monkeypatch):
    _viet(tmp_path, [1] * 20)
    (tmp_path / "img_doan.txt").write_text((tmp_path / "img_doan.txt").read_text(encoding="utf-8") + "\nhong", encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("malformed" in b for b in _latest(tmp_path)["blocking_issues"])
    _viet(tmp_path, [1] * 20)
    G.ghi_fingerprint(tmp_path)
    (tmp_path / "script.txt").write_text("\n\n".join(f"doan moi {i}。" for i in range(1, 21)), encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("STALE" in b for b in _latest(tmp_path)["blocking_issues"])
