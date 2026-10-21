r"""comment_digest.py — gom BÌNH LUẬN THẬT của kênh mẫu thành 1 file đọc nhanh cho bước S1 (0 LLM, 0đ).

Anh chốt 2026-09-26: trước khi viết kịch bản phải đọc bình luận của kênh mẫu như góp ý/phản ánh THẬT của người
xem. Dữ liệu do dự án TRENDING-RESEARCH tải sẵn (`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\<kênh>\comments.json`
+ `channel.json`). Tool này KHÔNG phân tích bằng LLM — chỉ xếp hạng theo lượt thích, gắn nhãn thô bằng từ khoá,
ghi `COMMENTS_TOP.md`. Phần CHẮT LỌC (insight + khối "ĐƯA VÀO PROMPT") do bước 1 (Claude Code) viết tay vào
`COMMENT_INSIGHT.md` cùng thư mục — lean_script đọc khối đó nhồi vào prompt model VIẾT.

Dùng:
  py -3.13 -X utf8 pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\iyaku_labo --profile yakkyoku-sukatto
  (ghi vào <profile.channel_dna_dir>\COMMENTS_TOP.md; --out để ghi chỗ khác; --top N bình luận/video, mặc định 15)
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

NHAN = {  # nhãn thô bằng từ khoá — chỉ để người đọc lọc nhanh, KHÔNG dùng làm số liệu quyết định
    "kinh_nghiem": r"(私も|自分も|昔|以前|うちの|前の職場|勤務して|働いて|経験|\d+歳|還暦|定年)",
    "dinh_chinh": r"(実際は|本当は|違う|おかしい|勘違い|ありえない|基準|制度|法律|厚生労働省|みなし|契約|義務)",
    "san_xuat": r"(声|ナレーション|絵|イラスト|作画|キャラ|語尾|BGM|誤字|読み間違い)",
    "vi_tha": r"(かわいそう|気の毒|寂しい|反省|刺さ|考えさせ|許|救われ|泣|ついて行こう)",
    "gian": r"(クズ|卑怯|最低|ムカ|腹立|イラ|許せ|いらない|切ったほうが|辞めさせ|無能|バカ|馬鹿)",
}
TEN_NHAN = {"kinh_nghiem": "kể chuyện thật của mình", "dinh_chinh": "bắt lỗi/đính chính dữ kiện",
            "san_xuat": "góp ý hình/giọng/chữ", "vi_tha": "cảm động/thương/ngẫm", "gian": "giận/phán xét nhân vật"}


def so_like(c):
    s = str(c.get("votes", 0) or 0).replace(",", "")
    m = re.match(r"([\d.]+)\s*([KkMm千万]?)", s)
    return int(float(m.group(1)) * {"K": 1e3, "k": 1e3, "千": 1e3, "万": 1e4, "M": 1e6, "m": 1e6}.get(m.group(2), 1)) if m else 0


def la_chu_kenh(c, meta):
    a = str(c.get("author", "")).lstrip("@").lower()
    return bool(a) and (a == str(meta.get("handle", "")).lstrip("@").lower() or c.get("is_owner"))


def digest(src: Path, top=15):
    cm = json.loads((src / "comments.json").read_text(encoding="utf-8"))
    ch = json.loads((src / "channel.json").read_text(encoding="utf-8")) if (src / "channel.json").exists() else {}
    meta = ch.get("meta") or {}
    info = {v["id"]: v for v in (ch.get("videos") or []) if v.get("id")}
    # chủ kênh (lời cảm ơn ghim): handle trùng tên thư mục kênh, HOẶC có mặt ở ≥80% video có bình luận (≥4 video).
    # Ngưỡng cao để KHÔNG lọc nhầm fan hay bình luận nhiều video (bản đầu dùng 50% → lọc nhầm 1 khán giả thật).
    tac_gia = {}
    for cs in cm.values():
        for a in {str(c.get("author", "")) for c in cs}:
            tac_gia[a] = tac_gia.get(a, 0) + 1
    co_bl = sum(1 for cs in cm.values() if cs)
    chu = {a for a, n in tac_gia.items()
           if a.lstrip("@").lower() == src.name.lower() or (n >= 4 and n >= co_bl * 0.8)}
    rows, tong = [], {k: 0 for k in NHAN}
    n_all = 0
    for vid, cs in cm.items():
        cs = [c for c in cs if str(c.get("author", "")) not in chu and (c.get("text") or "").strip()]
        n_all += len(cs)
        for c in cs:
            for k, pat in NHAN.items():
                if re.search(pat, c["text"]):
                    tong[k] += 1
        rows.append((vid, cs))
    rows.sort(key=lambda r: int(str(info.get(r[0], {}).get("views") or 0).replace(",", "") or 0), reverse=True)
    out = [f"# BÌNH LUẬN THẬT — {meta.get('name', src.name)} ({src.name})", "",
           f"Nguồn: `{src / 'comments.json'}` · {len(cm)} video · {n_all} bình luận khán giả"
           + (f" (đã lọc chủ kênh: {', '.join(sorted(chu))})" if chu else "") + ".",
           "Sinh bằng `pipeline\\comment_digest.py` (0 LLM). Nhãn là từ khoá thô, chỉ để lọc nhanh — ĐỌC nguyên văn "
           "rồi chắt vào `COMMENT_INSIGHT.md` (bước 1 viết tay).", "",
           "| Nhãn | Số bình luận | % |", "|---|---|---|"]
    out += [f"| {TEN_NHAN[k]} | {v} | {v * 100 // max(1, n_all)}% |" for k, v in tong.items()]
    out.append("")
    for vid, cs in rows:
        v = info.get(vid, {})
        out.append(f"## {v.get('title', vid)}")
        out.append(f"`{vid}` · {v.get('views', '?')} view · {v.get('likes', '?')} like · {len(cs)} bình luận tải được")
        if not cs:
            out += ["", "_(không có bình luận)_", ""]
            continue
        out.append("")
        for c in sorted(cs, key=so_like, reverse=True)[:top]:
            tag = [TEN_NHAN[k] for k, pat in NHAN.items() if re.search(pat, c["text"])]
            rep = " ↳" if c.get("is_reply") or c.get("reply") else ""
            t = re.sub(r"\s+", " ", c["text"]).strip()
            out.append(f"- **[{so_like(c)}]**{rep} {t[:300]}" + (f"  _({', '.join(tag)})_" if tag else ""))
        out.append("")
    return "\n".join(out)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="thư mục kênh trong TRENDING-RESEARCH\\data (có comments.json)")
    ap.add_argument("--profile", help="ghi vào <channel_dna_dir>\\COMMENTS_TOP.md của profile")
    ap.add_argument("--out", help="đường dẫn file .md (thay cho --profile)")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args(argv)
    src = Path(a.src)
    if not (src / "comments.json").exists():
        raise SystemExit(f"✗ không thấy {src / 'comments.json'}")
    if a.out:
        out = Path(a.out)
    elif a.profile:
        import profiles
        dna = (profiles.load(a.profile).get("channel_dna_dir") or "").strip()
        if not dna:
            raise SystemExit(f"✗ profile {a.profile} chưa khai channel_dna_dir → dùng --out")
        out = ROOT / dna / "COMMENTS_TOP.md"
    else:
        ap.error("cần --profile hoặc --out")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(digest(src, a.top), encoding="utf-8")
    print(f"✓ {out}")


if __name__ == "__main__":
    main()
