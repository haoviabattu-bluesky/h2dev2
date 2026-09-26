r"""Nơi máy 2 trả kết quả về — MỘT chỗ tra duy nhất cho cả pipeline.

Vì sao có file này (2026-09-25): `FlowHandoff_local\results\` từng dùng 3 quy ước khác nhau
(`<slug>` phẳng → `<tên tab>\<slug>` → `video_render\<upload_channel>\<slug>`) mà không bên nào
dọn bản cũ, nên tới 2026-09-25 thư mục có 20 thư mục slug phẳng không biết của lane nào.
Quy ước CHỐT, mọi nhánh đều có tầng `<upload_channel>`:

    results\img_render\<sheet_tab>\<slug>\     ảnh AI máy 2 vẽ xong
    results\video_render\<sheet_tab>\<slug>\   video máy 2 dựng xong
    results\channel_dna\<slug kênh mẫu>\             Channel DNA (K1+K2)
    results\nghien_cuu\<mã lane>\                    hồ sơ nghiên cứu ngách

`dich_*()` trả chỗ PHẢI ghi từ nay. `tim_*()` còn dò cả 2 quy ước cũ để tập đã trả về trước
2026-09-25 vẫn đọc được — bỏ nhánh dò đó khi máy 2 đã chạy xong đơn
`shared\YEU_CAU_MAY2_2026-09-25_sap_xep_results_theo_lane.md`.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC_MAC_DINH = HERE.parent / "FlowHandoff_local" / "results"


def _goc(goc=None):
    return Path(goc) if goc else GOC_MAC_DINH


def dich_anh(slug, ten_tab, goc=None):
    """Chỗ PHẢI ghi ảnh. `ten_tab` = profile.publish.sheet_tab (vd E-70dai-kenko)."""
    return _goc(goc) / "img_render" / ten_tab / slug


def dich_video(slug, ten_tab, goc=None):
    """Chỗ PHẢI ghi video. `ten_tab` = profile.publish.sheet_tab (vd E-70dai-kenko)."""
    return _goc(goc) / "video_render" / ten_tab / slug


def _dau_tien_co(ung_vien):
    for p in ung_vien:
        if p.is_dir():
            return p
    return None


def tim_anh(slug, ten_tab=None, upload_channel=None, goc=None):
    """Tìm thư mục ảnh của tập, ưu tiên quy ước mới rồi mới tới 2 quy ước cũ.

    Trả None nếu chưa có chỗ nào — gọi `dich_anh()` để biết chỗ đúng mà báo người dùng."""
    g = _goc(goc)
    ung_vien = []
    for ten in (ten_tab, upload_channel):
        if ten:
            ung_vien.append(g / "img_render" / ten / slug)
            ung_vien.append(g / ten / slug)                  # quy ước giữa (vd 70dai-kenko/<slug>)
    ung_vien.append(g / slug)                                # quy ước cũ nhất: slug phẳng
    return _dau_tien_co(ung_vien)


def tim_video(slug, ten_tab=None, upload_channel=None, goc=None):
    g = _goc(goc)
    ung_vien = []
    for ten in (ten_tab, upload_channel):
        if ten:
            ung_vien.append(g / "video_render" / ten / slug)
            ung_vien.append(g / ten / slug)
    ung_vien.append(g / "video_render" / slug)                # thiếu tầng kênh (đã gặp thật)
    return _dau_tien_co(ung_vien)


def thu_muc_nghien_cuu(goc=None):
    r"""Mọi thư mục hồ sơ nghiên cứu — cả tên mới `nghien_cuu\<lane>` lẫn tên cũ
    `<lane>_from_research` ở gốc, để cổng chống-chạy-lại-K1K2 không phụ thuộc thứ tự dọn."""
    g = _goc(goc)
    ra = []
    nc = g / "nghien_cuu"
    if nc.is_dir():
        ra += [d for d in sorted(nc.glob("*")) if d.is_dir()]
    ra += [d for d in sorted(g.glob("*_from_research")) if d.is_dir()]
    return ra


def kiem_ten_thu_muc(goc=None, thu_muc_profile=None):
    r"""Cổng LUẬT CỨNG (anh chốt 2026-09-25): tên thư mục trong `img_render\` và `video_render\`
    BẮT BUỘC = `publish.sheet_tab`. Trả list dict {duong_dan, ten_hien_tai, ten_dung, lane}
    của những thư mục sai tên — list rỗng nghĩa là ĐẠT.

    Đối chiếu bằng cách: gom mọi bí danh đã từng dùng của 1 lane (`upload_channel`, `sheet_tab`,
    `id`) rồi xem tên thư mục rơi vào bí danh nào. Thư mục không khớp lane nào thì bỏ qua (không
    đoán bừa) nhưng vẫn báo ở khoá `lane=None` để người đọc tự quyết."""
    import json
    g = _goc(goc)
    tmp = Path(thu_muc_profile) if thu_muc_profile else (HERE.parent / "profiles" / "profiles")
    bi_danh = {}          # tên bất kỳ -> (lane_id, sheet_tab đúng)
    for f in sorted(tmp.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        pub = d.get("publish") or {}
        tab = pub.get("sheet_tab")
        if not tab:
            continue      # lane chưa có tab (vd Lane D) — không có gì để ép
        for ten in (pub.get("upload_channel"), pub.get("sheet_tab"), d.get("id")):
            if ten:
                bi_danh[ten] = (d.get("id"), tab)

    sai = []
    for nhanh in ("img_render", "video_render"):
        thu_muc = g / nhanh
        if not thu_muc.is_dir():
            continue
        for d in sorted(thu_muc.iterdir()):
            if not d.is_dir():
                continue
            lane_tab = bi_danh.get(d.name)
            if lane_tab is None:
                sai.append({"duong_dan": d, "ten_hien_tai": d.name, "ten_dung": None, "lane": None})
            elif d.name != lane_tab[1]:
                sai.append({"duong_dan": d, "ten_hien_tai": d.name,
                            "ten_dung": lane_tab[1], "lane": lane_tab[0]})
    return sai
