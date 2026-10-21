r"""xong_video.py — ghi trạng thái chặng DỰNG VIDEO khi máy 2 làm A→Z (anh chốt 2026-10-21).

Trước 21/10 máy 1 dừng ở `Đã giao máy 2`, phần dựng do máy 2 nhận việc qua jobs\ và cột D không ai ghi tiếp.
Nay CHÍNH máy 2 làm hết, nên chặng dựng cũng có mốc trên cột D/TONGHOP như các chặng trước:

  Đã duyệt hook --(dong_goi_may2 --job)--> Chờ dựng video --(--bat-dau)--> Đang dựng video --(mặc định)--> Video xong

Dùng:
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\xong_video.py --profile <lane> --slug <tập> --bat-dau
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\xong_video.py --profile <lane> --slug <tập>
Mốc cuối CHỈ ghi khi đã thấy final.mp4 thật (thư mục trả hàng của profile hoặc thư mục tập) — không tự khai xong.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DANG_DUNG = "Đang dựng video"
VIDEO_XONG = "Video xong"


def tim_final(prof, slug):
    pub = prof.get("publish") or {}
    kenh = pub.get("upload_channel") or prof["id"]
    ung_vien = []
    if pub.get("upload_dir"):
        ung_vien.append(Path(pub["upload_dir"]) / kenh / slug / "final.mp4")
    ung_vien += [HERE.parent / "FlowHandoff_local" / "results" / "video_render" / kenh / slug / "final.mp4",
                 HERE.parent / prof.get("slug_dir", f"assets/{prof['id']}") / slug / "final.mp4"]
    return next((p for p in ung_vien if p.exists()), None), ung_vien


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--bat-dau", action="store_true", help="ghi D = Đang dựng video (lúc bắt đầu chặng 1 lồng tiếng)")
    a = ap.parse_args(argv)
    import dong_goi_may2 as dg
    import profiles
    import review_may3 as rv
    import tong_hop
    prof = profiles.load(a.profile)
    if a.bat_dau:
        rv.ghi_d_neu(prof, a.slug, DANG_DUNG, (dg.CHO_DUNG,))
        tong_hop.ghi(prof, a.slug, tong_hop.CHAY_VIDEO)
        return
    f, ung_vien = tim_final(prof, a.slug)
    if not f:
        raise SystemExit("✗ chưa thấy final.mp4 ở: " + " · ".join(str(p) for p in ung_vien) + " → CHƯA ghi Video xong")
    print(f"  final.mp4: {f}")
    rv.ghi_d_neu(prof, a.slug, f"{VIDEO_XONG}\n{f.parent}", (dg.CHO_DUNG, DANG_DUNG))
    tong_hop.ghi(prof, a.slug, tong_hop.VIDEO_XONG)


if __name__ == "__main__":
    main()
