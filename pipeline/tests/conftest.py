"""2026-10-21: cổng "không có cấu trúc hook gốc thì không viết/khoá hook" (hook_stage + kiem_hook_goc) chặn mọi tập thiếu
hook/source.json.cau_truc_hook. Test cũ dựng tập giả không có video gốc → mặc định cấp 1 cấu trúc giả để các test đó vẫn đo
đúng thứ chúng đo. Test kiểm CHÍNH cổng đánh dấu @pytest.mark.cong_hook_goc để chạy hành vi thật."""
import pytest

CT_GIA = {"mo_dau": "câu thoại", "nhip": [{"tu": 0, "den": 5, "vai_tro": "mở", "cach_lam": "thoại"}]}


def pytest_configure(config):
    config.addinivalue_line("markers", "cong_hook_goc: chạy hành vi THẬT của cổng hook gốc (không cấp cấu trúc giả)")


@pytest.fixture(autouse=True)
def _cau_truc_hook_gia(request, monkeypatch):
    if request.node.get_closest_marker("cong_hook_goc"):
        return
    try:
        import hook_stage as HS
    except Exception:
        return
    that_tap, that_ptich, that_suon = HS.cau_truc_cua_tap, HS.phan_tich_cau_truc, HS.khoi_suon

    def ptich(d, prof, src, force=False):
        ct = that_ptich(d, prof, src, force=force)
        if ct is None and not src.get("cau_truc_hook"):
            src["cau_truc_hook"] = ct = dict(CT_GIA)
        return ct

    monkeypatch.setattr(HS, "cau_truc_cua_tap", lambda d: that_tap(d) or dict(CT_GIA))
    monkeypatch.setattr(HS, "phan_tich_cau_truc", ptich)
    monkeypatch.setattr(HS, "khoi_suon", lambda d, src: that_suon(d, src if (src or {}).get("cau_truc_hook")
                                                                   else {**(src or {}), "cau_truc_hook": CT_GIA}))
