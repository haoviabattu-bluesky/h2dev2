# -*- coding: utf-8 -*-
"""Giữ chốt Lane K (2026-09-24): cắt câu dùng chung, khớp vai, nhãn @CAST, khuôn prompt CAST, bóng thoại."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cau_vai        # noqa: E402
import gen_images     # noqa: E402
import prompt_doan    # noqa: E402
import bong_thoai     # noqa: E402

KB = "「じゃあ、辞めます」\nそれが口ぐせの薬剤師がいた。その一言で、彼は八年間通してきた。\n俺はこの店で一番長い。「分かりました。退職届を出しておいてください」店長はそう言った。"


def test_tach_cau_thoai_la_mot_don_vi():
    c = cau_vai.tach_cau(KB)
    assert [x["text"] for x in c] == ["「じゃあ、辞めます」", "それが口ぐせの薬剤師がいた。", "その一言で、彼は八年間通してきた。",
                                      "俺はこの店で一番長い。", "「分かりました。退職届を出しておいてください」", "店長はそう言った。"]
    assert [x["para"] for x in c] == [1, 2, 2, 3, 3, 3]
    assert cau_vai.la_thoai(c[4]["text"]) and not cau_vai.la_thoai(c[5]["text"])


def test_khop_vai_doan_hook_trong_ca_tap():
    ca = cau_vai.tach_cau(KB)
    vai = [{"i": x["i"], "id": v, "text": x["text"]} for x, v in zip(ca, ["shu", "ke", "ke", "shu", "tencho", "ke"])]
    hook = cau_vai.tach_cau("「じゃあ、辞めます」\nそれが口ぐせの薬剤師がいた。")
    assert cau_vai.khop_vai(hook, vai) == ["shu", "ke"]


def test_khop_vai_cau_la_thi_dung():
    import pytest
    with pytest.raises(SystemExit):
        cau_vai.khop_vai(cau_vai.tach_cau("「知らない台詞」"), [{"i": 1, "id": "ke", "text": "別の文。"}])


def test_gen_images_nhan_cast(tmp_path):
    p = tmp_path / "p.txt"
    p.write_text("@CAST:shu,tencho MEDIUM two pharmacists\n@REF x\nplain\n", encoding="utf-8")
    assert gen_images.parse_prompts(p)[0] == ("cast:shu,tencho", "MEDIUM two pharmacists")
    assert gen_images.parse_prompts(p)[1][0] == "ref"


def test_prompt_cast_chan_qua_3_mat_va_id_la():
    chars = [{"id": i, "ref": True, "look": "x"} for i in ("shu", "tencho", "jimu", "part")]
    rows, loi = prompt_doan._parse_cast("1|shu,tencho,jimu,part|" + "word " * 20 + "\n2|abc|" + "w " * 20, 3, chars, 3)
    assert any("> tối đa 3" in x for x in loi) and any("id lạ" in x for x in loi)


def test_chia_cot_khong_de_dau_cau_dau_cot():
    for col in bong_thoai.chia_cot("その日、店長が昼ごはんを食べたのは、午後三時を過ぎてからだった。", 11, 3)[1:]:
        assert col[0] not in "、。ゃゅょっ"


def test_tach_loi_ke_chia_doi_theo_so_chu():
    import bong_thoai as bt
    c = {"vai": "ke", "text": "向かいの雑居ビルに内科と整形外科が入っていて、処方箋のほとんどは、そこから流れてくる。",
         "start": 10.0, "end": 18.0}
    ps = bt.tach_loi_ke(c, 24)
    assert len(ps) == 2 and "".join(p["text"] for p in ps) == c["text"]
    assert ps[0]["text"].endswith("、") and ps[0]["start"] == 10.0 and ps[-1]["end"] == 18.0
    assert abs(ps[0]["end"] - ps[1]["start"]) < 1e-9
    thoai = {"vai": "shu", "text": "「" + "あ" * 40 + "」", "start": 0, "end": 5}
    assert bt.tach_loi_ke(thoai, 24) == [thoai]


def test_hop_loi_ke_sat_mep_phai_tranh_mat():
    import bong_thoai as bt
    box = bt._dat_mep(1920, 1080, 300, 500, [])
    assert box[3][2] == 1920 - 24                     # không người → sát mép phải
    mat_phai = [[1500, 50, 1800, 400]]
    box = bt._dat_mep(1920, 1080, 300, 500, mat_phai)
    assert box[3][0] == 24                            # mép phải có người → sang mép trái
