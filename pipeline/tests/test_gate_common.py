# pipeline/tests/test_gate_common.py
import json, os, time
from pathlib import Path
import pytest
import gate_common as G


def test_ket_qua_schema():
    k = G.ket_qua("B5P", "WARN", attempt=2, warnings=["x"], metrics={"n": 1})
    assert k["gate"] == "B5P" and k["status"] == "WARN" and k["attempt"] == 2
    assert k["blocking_issues"] == [] and k["warnings"] == ["x"] and k["infra"] is False
    assert "timestamp" in k
    with pytest.raises(ValueError):
        G.ket_qua("B5P", "OK")


def test_ghi_log_khong_ghi_de(tmp_path):
    p1 = G.ghi_log(tmp_path, "B5P", G.ket_qua("B5P", "FAIL", blocking=["a"]))
    p2 = G.ghi_log(tmp_path, "B5P", G.ket_qua("B5P", "PASS"))
    assert p1.name == "B5P_attempt_001.json" and p2.name == "B5P_attempt_002.json"
    latest = json.loads((tmp_path / "logs" / "B5P_latest.json").read_text(encoding="utf-8"))
    assert latest["status"] == "PASS" and latest["attempt"] == 2


def test_goi_llm_json_boc_fence(monkeypatch):
    class R: text = "```json\n{\"a\": 1, \"b\": [1,2]}\n```"
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    assert G.goi_llm_json("x") == {"a": 1, "b": [1, 2]}


def test_goi_llm_json_loi_ha_tang(monkeypatch):
    def boom(*a, **k): raise G.llm_client.LLMError("het chuoi")
    monkeypatch.setattr(G.llm_client, "chat", boom)
    with pytest.raises(G.QcError):
        G.goi_llm_json("x")


def test_goi_llm_json_khong_phai_json(monkeypatch):
    class R: text = "toi khong biet"
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    with pytest.raises(G.QcError):
        G.goi_llm_json("x")


def test_escalation_report(tmp_path):
    att = [{"attempt": 1, "status": "FAIL", "blocking_issues": ["loi A", "loi B"]},
           {"attempt": 2, "status": "FAIL", "blocking_issues": ["loi A"]}]
    p = G.viet_escalation_report(tmp_path, "B3Q", att, goi_y="sua tay doan 3")
    t = p.read_text(encoding="utf-8")
    assert "B3Q" in t and "loi A" in t and "sua tay doan 3" in t and "attempt 2" in t.lower()
    G.viet_escalation_report(tmp_path, "B5P", att)
    assert p.read_text(encoding="utf-8").count("## ") >= 2


def test_mtime_rao(tmp_path):
    (tmp_path / "img_prompts.txt").write_text("p", encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("001.png|1", encoding="utf-8")
    time.sleep(0.05)
    (tmp_path / "script.txt").write_text("s", encoding="utf-8")
    now = time.time()
    os.utime(tmp_path / "script.txt", (now + 10, now + 10))
    loi = G.kiem_mtime_script_vs_prompts(tmp_path)
    assert len(loi) == 2 and "img_prompts.txt" in loi[0]
    os.utime(tmp_path / "img_prompts.txt", (now + 20, now + 20))
    os.utime(tmp_path / "img_doan.txt", (now + 20, now + 20))
    assert G.kiem_mtime_script_vs_prompts(tmp_path) == []


def test_phan_bo_xen_ke():
    assert G.phan_bo_xen_ke([2, 3] * 25) is True            # STT3 that: 2,3,2,3... 50 doan
    assert G.phan_bo_xen_ke([3, 2] * 10 + [5, 3]) is True     # 20/22 cap xen ke
    assert G.phan_bo_xen_ke([2, 5, 3, 3, 2, 4, 3, 2, 5, 2, 2, 3, 4, 3, 3, 2, 3, 5, 2, 3, 3, 2]) is False
    assert G.phan_bo_xen_ke([2, 3, 2, 3]) is False            # < 20 doan: khong ket luan
    assert G.phan_bo_xen_ke([3] * 30) is True                 # hang so tuyet doi cung la chia deu


def test_llm_stats_cong_don(monkeypatch):
    class R:
        text = "{\"ok\": 1}"; elapsed = 1.5
        usage = {"prompt_tokens": 100, "completion_tokens": 20}
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    truoc = G.llm_stats_snapshot()
    G.goi_llm_json("x"); G.goi_llm_json("y")
    sau = G.llm_stats_snapshot()
    assert sau["calls"] - truoc["calls"] == 2 and sau["tokens_in"] - truoc["tokens_in"] == 200
    assert sau["tokens_out"] - truoc["tokens_out"] == 40 and sau["latency_s"] - truoc["latency_s"] == 3.0
    def boom(*a, **k): raise G.llm_client.LLMError("x")
    monkeypatch.setattr(G.llm_client, "chat", boom)
    with pytest.raises(G.QcError):
        G.goi_llm_json("z")
    assert G.llm_stats_snapshot()["errors"] - sau["errors"] == 1


def _tap(tmp_path, script="s1", prompts="p1", doan="001.png|1"):
    (tmp_path / "script.txt").write_text(script, encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text(prompts, encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text(doan, encoding="utf-8")
    return tmp_path


def test_fingerprint_stamp_va_stale(tmp_path):
    d = _tap(tmp_path)
    p = G.ghi_fingerprint(d)
    meta = json.loads(p.read_text(encoding="utf-8"))
    sha_s = G.sha256_file(d / "script.txt")
    assert meta["script_sha256"] == sha_s
    assert meta["artifacts"]["img_prompts.txt"]["generated_from_script_sha256"] == sha_s
    assert meta["artifacts"]["img_doan.txt"]["sha256"] == G.sha256_file(d / "img_doan.txt")
    b, w = G.kiem_stale(d)
    assert b == [] and w == []
    (d / "script.txt").write_text("s2 da sua", encoding="utf-8")       # script doi -> STALE
    b, w = G.kiem_stale(d)
    assert len(b) == 2 and all("STALE" in x for x in b)
    G.ghi_fingerprint(d)                                                # stamp lai -> het stale
    (d / "img_doan.txt").write_text("001.png|1\n002.png|1", encoding="utf-8")   # artifact sua tay
    b, w = G.kiem_stale(d)
    assert b == [] and len(w) == 1 and "img_doan.txt" in w[0]


def test_stale_chua_co_meta_dung_mtime(tmp_path):
    d = _tap(tmp_path)
    b, w = G.kiem_stale(d)                                    # chua stamp, mtime hop le -> chi warn
    assert b == [] and any("fingerprint" in x for x in w)
    now = time.time()
    os.utime(d / "script.txt", (now + 30, now + 30))          # script moi hon -> mtime chan
    b, w = G.kiem_stale(d)
    assert len(b) == 2 and "img_prompts.txt" in b[0]


def test_fingerprint_chi_ghi_artifact_ton_tai(tmp_path):
    (tmp_path / "script.txt").write_text("s", encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("p", encoding="utf-8")
    meta = json.loads(G.ghi_fingerprint(tmp_path).read_text(encoding="utf-8"))
    assert "img_doan.txt" not in meta["artifacts"] and "img_prompts.txt" in meta["artifacts"]


def test_stamp_thieu_script_la_qcerror(tmp_path):
    with pytest.raises(G.QcError):
        G.ghi_fingerprint(tmp_path)
    assert G.main(["--slug", str(tmp_path), "--stamp"]) == 1
