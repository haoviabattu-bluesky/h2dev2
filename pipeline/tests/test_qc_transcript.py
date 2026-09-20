# pipeline/tests/test_qc_transcript.py
import json
from pathlib import Path
import qc_transcript as Q


def _seg(n, step=10.0, dup=False):
    # Cau day du ~27 ky tu/10s (~160 ky tu/phut) — ban brief goc "문장 {i} 입니다" chi ~7 ky tu/10s
    # = 41 ky tu/phut, tu vi pham nguong cpm<120 WARN cua chinh no nen test_pass khong bao gio PASS.
    segs = [{"start": i * step, "duration": step,
             "text": ("같은 문장 반복" if dup else f"문장 {i} 입니다. 오늘은 날씨가 참 좋아서 산책을 나갔습니다.")}
            for i in range(n)]
    return {"video_id": "x", "source": "api", "video_duration_sec": n * step, "segments": segs}


def test_pass():
    s, b, w, m = Q.do(_seg(100))
    assert s == "PASS" and b == [] and m["coverage"] >= 0.99


def test_cut_som_fail():
    d = _seg(100); d["video_duration_sec"] = 100 * 10 / 0.7
    s, b, _, m = Q.do(d)
    assert s == "FAIL" and any("coverage" in x for x in b) and m["coverage"] < 0.8


def test_gap_warn():
    d = _seg(100); d["segments"][50]["start"] += 60; d["segments"][50]["duration"] = 10
    for k in range(51, 100): d["segments"][k]["start"] += 60
    d["video_duration_sec"] = d["segments"][-1]["start"] + 10
    s, b, w, m = Q.do(d)
    assert s == "WARN" and m["max_gap_sec"] >= 60 and any("gap" in x for x in w)


def test_trung_lap_fail():
    s, b, _, m = Q.do(_seg(100, dup=True))
    assert s == "FAIL" and m["duplicate_ratio"] > 0.15


def test_khong_co_thoi_luong_warn():
    d = _seg(100); d["video_duration_sec"] = 0
    s, b, w, m = Q.do(d)
    assert s == "WARN" and m["coverage"] is None


def test_cli_skip_khi_khong_sidecar(tmp_path):
    assert Q.main(["--slug", str(tmp_path)]) == 0
    latest = json.loads((tmp_path / "logs" / "B2Q_latest.json").read_text(encoding="utf-8"))
    assert latest["status"] == "SKIPPED"
