# -*- coding: utf-8 -*-
"""qc_facts.py — CỔNG KIỂM DỮ KIỆN: chi tiết nào trong kịch bản KHÔNG có trong tư liệu?

Đây là cổng bắt loại lỗi nguy hiểm nhất của kênh kể chuyện có thật, và là loại mà mọi cổng khác
đều mù:

    Kịch bản viết「1989年、日本の埼玉県にある日立製作所の研究所で、外村彰のチームが…」
    Tư liệu KHÔNG hề nói phòng thí nghiệm ở đâu.

Mô hình tự điền `埼玉県` vào chỗ trống. Tra lại (2026-09-10): Wikipedia ghi Tonomura ở
**Hitachi Central Research Laboratory**, Physics World ghi *"the Advanced Research Laboratory in
Hitachi, **Tokyo**"* — không nguồn nào nói Saitama.

Tệ hơn: bản nháp đầu điền HAI kiểu khác nhau (chương 1 ghi 埼玉県, chương 4 ghi 東京の西). QC nội
dung (`qc_script`) bắt được mâu thuẫn rồi "sửa" bằng cách chọn một cái cho nhất quán — và chọn
phải cái nhiều khả năng sai.

    ⇒ QC nội dung làm cho NHẤT QUÁN. Cổng này làm cho ĐÚNG NGUỒN.
      Nó không hỏi "chi tiết này có thật không" (trong máy không có cách nào biết),
      nó hỏi "chi tiết này ở ĐÂU ra" — không có trong tư liệu thì không được lên hình.

Hai tầng, đều TẤT ĐỊNH và MIỄN PHÍ:
  A. Kịch bản ⟶ tư liệu : mọi năm · địa danh · tên riêng katakana · số có đơn vị · cơ quan
                          xuất hiện trong kịch bản mà KHÔNG có trong tư liệu ⇒ báo.
  B. Tư liệu tự nó       : dòng dữ kiện nào không kèm nguồn tra lại được ⇒ báo.

Dùng:
  py -3.13 qc_facts.py --script script.txt --dossier series_ctx.txt
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

# 47 tỉnh thành — địa danh là thứ mô hình bịa nhiều nhất vì nó làm câu văn "nghe có tra cứu".
TINH_THANH = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県",
    "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県",
    "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府",
    "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県",
    "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県",
    "鹿児島県", "沖縄県",
]

DON_VI = (r"キロ|km|メートル|m|センチ|光年|天文単位|億|兆|万|人|名|年間|か月|ヶ月|カ月|日間|"
          r"パーセント|%|歳|度|倍|回|機|隻|台|ページ|ドル|円")

# Katakana hay gặp mà KHÔNG phải tên riêng — không lọc thì báo động giả ngập mặt.
KATAKANA_THUONG = {
    "データ", "エネルギー", "テーマ", "レベル", "パターン", "システム", "スクリーン", "スリット",
    "イメージ", "メッセージ", "ケース", "グループ", "モデル", "タイプ", "ポイント", "コンピュータ",
    "コンピューター", "スピード", "バランス", "リスト", "ページ", "シリーズ", "ルール", "チーム",
    "アイデア", "ストーリー", "シーン", "コメント", "チャンネル", "ネット", "メートル", "センチ",
    "キロ", "パーセント", "プロセス", "ドラマ", "リアル", "シンプル", "クリア", "スケール",
    "ゼロ", "プラス", "マイナス", "ノート", "カメラ", "フィルム", "ガラス", "エラー", "ヒント",
    "ボタン", "ドア", "ベル", "テレビ", "ラジオ", "ニュース", "レポート", "ファイル", "コード",
}


def chuan(s):
    """Bỏ khoảng trắng + đưa số/chữ full-width về half-width để so cho khớp."""
    s = unicodedata.normalize("NFKC", str(s or ""))
    return re.sub(r"\s+", "", s)


def _cau_chua(text, token):
    for cau in re.split(r"[。\n]", text):
        if token in chuan(cau):
            return cau.strip()[:70]
    return ""


def _them(ra, kind, sev, token, text, gt=""):
    ra.append({"kind": kind, "sev": sev, "token": token,
               "cau": _cau_chua(text, token), "goi_y": gt})


def chi_tiet_thieu_nguon(script, dossier):
    """Tầng A — chi tiết CỤ THỂ có trong kịch bản mà KHÔNG có trong tư liệu."""
    s, d = chuan(script), chuan(dossier)
    ra = []

    # 1) MỐC NĂM — thứ tạo cảm giác "đã nghiên cứu kỹ", nên bịa ở đây là đắt nhất.
    #    ⚠️ Phải tách MỐC NĂM khỏi KHOẢNG THỜI GIAN. 「1000年以上前」 và 「180年以上が経過」 là độ dài
    #    thời gian, không phải năm dương lịch — bản đầu báo oan cả hai.
    for m in re.finditer(r"(\d{3,4})年(以上|以前|間|余り|ほど|近く|後|ぶり|にわた)?", s):
        if m.group(2):                       # có đuôi ⇒ là khoảng thời gian, bỏ qua
            continue
        nam = m.group(1)
        if not (1000 <= int(nam) <= 2100):
            continue
        if f"{nam}年" not in d:
            _them(ra, "nam_khong_co_trong_tu_lieu", "cao", f"{nam}年", script,
                  "bỏ mốc năm này, hoặc bổ sung vào tư liệu kèm nguồn")

    # 2) ĐỊA DANH hành chính Nhật — chỗ mô hình bịa nhiều nhất.
    for tinh in TINH_THANH:
        if tinh in s and tinh not in d:
            _them(ra, "dia_danh_khong_co_trong_tu_lieu", "cao", tinh, script,
                  "bỏ tên tỉnh/thành, chỉ nói tên cơ quan — hoặc tra nguồn rồi ghi vào tư liệu")
    # thành phố/quận/thị trấn: <kanji>市 / 区 / 町
    # `(?!民)` chặn 一般市民, nhưng chưa chặn được DANH TỪ CHUNG kết thúc bằng 区/町 rồi còn chữ
    # phía sau: 「立ち入り禁止区域」 bị cắt thành 「禁止区」 và báo là địa danh bịa (đo thật tập 3).
    # Chặn bằng cách nhìn chữ NGAY SAU: 区域/区分/区間/町並み… đều là danh từ chung, không phải nơi chốn.
    SAU_CHUNG = ("域", "分", "間", "画", "並", "内", "外", "別")
    for mm in re.finditer(r"([一-鿿]{2,4}[市区町村])(?!民)", s):
        m = mm.group(1)
        if mm.end() < len(s) and s[mm.end()] in SAU_CHUNG:
            continue
        if m.startswith(("一般", "各", "同", "都", "全", "禁止", "立入")):   # danh từ chung
            continue
        if m not in d:
            _them(ra, "dia_danh_khong_co_trong_tu_lieu", "cao", m, script, "như trên")

    # 3) CƠ QUAN / TỔ CHỨC
    #    Regex tham ăn nuốt cả tính từ đứng trước (「名門プリンストン大学」). Nên phải cắt dần đầu
    #    chuỗi rồi mới kết luận — nếu không, tên CÓ trong tư liệu vẫn bị báo là bịa.
    CHUNG = ("当局", "関係当局", "政府", "官庁", "各局", "放送局", "気象庁")
    # Tư liệu hay ghi TÊN VIẾT TẮT (MIT, CIA) còn kịch bản đọc thành tên đầy đủ tiếng Nhật —
    # cùng một tổ chức, khác cách gọi. Đo thật tập 3: 「マサチューセッツ工科大学」và「中央情報局」
    # đều bị báo bịa trong khi tư liệu có đủ "MIT" và "CIA".
    # Bảng này CHỈ nhận cặp mà cái tên viết tắt đã nằm sẵn trong tư liệu — không phải phép miễn trừ.
    VIET_TAT = {"マサチューセッツ工科大学": "MIT", "カリフォルニア工科大学": "カルテック",
                "中央情報局": "CIA", "連邦捜査局": "FBI", "米航空宇宙局": "NASA",
                "国家安全保障局": "NSA", "日本航空": "JAL", "国防総省": "ペンタゴン"}
    for m in set(re.findall(r"([一-鿿ァ-ヴー・]{2,12}(?:大学|研究所|研究センター|省|庁|局|財団|協会|学会))", s)):
        if any(m.endswith(x) for x in CHUNG):        # 「オーストラリア当局」 = "nhà chức trách", chung chung
            continue
        if any(m[i:] in d for i in range(0, min(len(m) - 2, 6))):
            continue
        if any(m.endswith(k) and v in d for k, v in VIET_TAT.items()):
            continue
        if len(m) <= 4:            # 「名門大学」「私立大学」… danh từ chung, không phải tên riêng
            continue
        _them(ra, "co_quan_khong_co_trong_tu_lieu", "cao", m, script,
              "tên cơ quan phải có trong tư liệu kèm nguồn")

    # 4) TÊN RIÊNG katakana (nhân vật nước ngoài)
    #    ⚠️ Chỉ bắt thứ CHẮC là tên người: tiếng Nhật viết tên nước ngoài có dấu ・ ngăn giữa họ và
    #    tên (ヒュー・エヴェレット), hoặc đi kèm chức danh (博士/教授/氏/三世). Quét mọi chuỗi katakana
    #    thì báo oan cả コーヒーカップ・ベッド・サイコロ・レンズ — và một cổng kêu oan là một cổng bị tắt.
    ung_vien = set(re.findall(r"[ァ-ヴー]{2,}・[ァ-ヴー・]{2,}", s))
    ung_vien |= {m.group(1) for m in
                 re.finditer(r"([ァ-ヴー]{3,})\s*(?:博士|教授|氏|三世|二世|の理論|の仮説)", s)}
    for goc in {x.strip("・ー") for x in ung_vien}:
        if len(goc) < 3 or goc in KATAKANA_THUONG or goc in d:
            continue
        manh = [p for p in goc.split("・") if len(p) >= 3]
        if manh and all(p in d for p in manh):   # đủ mảnh trong tư liệu, chỉ khác cách ghép
            continue
        _them(ra, "ten_rieng_khong_co_trong_tu_lieu", "vua", goc, script,
              "tên riêng phải lấy từ tư liệu — sai một chữ là sai người")

    # 5) SỐ CÓ ĐƠN VỊ
    #
    # ⚠️ Ba nguồn BÁO OAN đã đo thật trên tập 2 (6/8 lỗi "nặng" đầu tiên đều là oan):
    #   · **Đơn vị viết khác nhau**: tư liệu ghi 「約125海里（約232km）」, kịch bản viết
    #     「232キロメートル」 — CÙNG MỘT SỐ. Phải quy đơn vị về một mối trước khi so.
    #   · **Khoảng số**: tư liệu ghi 「3〜4倍」, kịch bản viết 「3倍から4倍」 — cùng dữ kiện.
    #   · **Từ đếm**: 「1機のセスナ」「3名の乗員」 là đếm chuyện, không phải số liệu nghiên cứu.
    # Cổng kêu oan là cổng bị tắt — mà tắt rồi thì chi tiết bịa thật cũng lọt luôn.
    DEM = "機|名|人|隻|台|回|通|冊"          # từ đếm — hạ mức, không chặn
    #    「100パーセント」「ゼロパーセント」 là lối nói nhấn mạnh, không phải số liệu nghiên cứu →
    #    hạ xuống mức "vừa" cho khỏi chặn oan. Mọi con số khác vẫn là mức nặng.
    TU_TU = {"100パーセント", "100%", "0パーセント", "0%"}
    # Quy đơn vị về một mối: キロメートル/キロ/km là một; メートル/m là một; パーセント/% là một.
    DONG_NGHIA = [("キロメートル", "km"), ("キロ", "km"), ("メートル", "m"),
                  ("パーセント", "%"), ("ヶ月", "か月"), ("カ月", "か月")]

    def _quy(x):
        x = chuan(x)
        for a_, b_ in DONG_NGHIA:
            x = x.replace(a_, b_)
        # Dấu phân cách hàng nghìn: tư liệu ghi 「罰金7,500ドル」, kịch bản viết 「7500ドル」 —
        # CÙNG MỘT SỐ, khác đúng một dấu phẩy. Đã báo oan thật ở tập 3.
        x = re.sub(r"(?<=\d),(?=\d)", "", x)
        # 「3年間」 vs 「保護観察3年」 — 間 chỉ là hậu tố khoảng thời gian, không đổi con số.
        x = re.sub(r"(年|か月|週|日|時間|分)間", r"\1", x)
        return x

    d_quy = _quy(d)
    # Khoảng số 「3〜4倍」 phải phủ được cả 「3倍」 lẫn 「4倍」.
    for mm in re.finditer(r"(\d[\d,\.]*)\s*[〜~～-]\s*(\d[\d,\.]*)\s*([^\s\d]{1,6})", d):
        d_quy += _quy(f" {mm.group(1)}{mm.group(3)} {mm.group(2)}{mm.group(3)} ")

    for m in set(re.findall(r"(\d[\d,\.]*\s*(?:" + DON_VI + r"))", s)):
        if _quy(m) in d_quy:
            continue
        so = re.match(r"[\d,\.]+", chuan(m)).group(0).replace(",", "")
        dv = chuan(m)[len(re.match(r"[\d,\.]+", chuan(m)).group(0)):]
        if re.fullmatch(DEM, dv) and float(so or 0) <= 20:
            sev = "thap"                       # 1機 · 3名 — đếm chuyện, không phải dữ kiện
        elif chuan(m) in TU_TU:
            sev = "vua"
        else:
            sev = "cao"
        _them(ra, "so_lieu_khong_co_trong_tu_lieu", sev, m.strip(), script,
              "số liệu phải có trong tư liệu; không chắc thì diễn đạt định tính")
    return ra


_NGUON = re.compile(r"〔[^〕]*〕|https?://|出典|nguồn", re.I)


def tu_lieu_thieu_nguon(dossier):
    """Tầng B — dòng dữ kiện trong hồ sơ có nguồn tra lại được không.

    ⚠️ Tính theo **KHỐI**, không theo từng dòng. Hồ sơ thật của SPACE_RESEARCH ghi một dòng
    〔出典: <URL> — 原文: "..."〕 ở CUỐI mỗi nhóm dữ kiện, kèm nguyên văn câu gốc để đối chiếu —
    cách đó tốt hơn nhét URL vào từng dòng. Bản đầu của cổng này đếm theo dòng nên báo
    **0/47 dòng có nguồn** cho một hồ sơ thực ra đã dẫn nguồn đầy đủ. Cổng kêu oan là cổng bị tắt,
    nên phải đếm đúng cách người ta ghi.

    Khối = đoạn giữa hai tiêu đề 【…】 (hoặc giữa hai dòng trống nếu hồ sơ không dùng tiêu đề).
    """
    ra, co, tong = [], 0, 0
    khoi, cur = [], []
    for dong in dossier.splitlines():
        if dong.strip().startswith("【") or (not dong.strip() and cur and cur[-1] == ""):
            khoi.append(cur)
            cur = []
        cur.append(dong)
    khoi.append(cur)

    for k in khoi:
        text = "\n".join(k)
        co_nguon = bool(_NGUON.search(text))
        dong_dk = [d.strip() for d in k
                   if d.strip().startswith(("・", "-", "•")) and len(d.strip()) >= 25]
        tong += len(dong_dk)
        if co_nguon:
            co += len(dong_dk)
        else:
            for d in dong_dk:
                ra.append({"kind": "khoi_du_kien_khong_co_nguon", "sev": "vua",
                           "token": d[:52], "cau": "",
                           "goi_y": "thêm 〔出典: URL〕 cho khối này"})
    return ra, co, tong


def kiem(script, dossier):
    ra = chi_tiet_thieu_nguon(script, dossier)
    thieu, co, tong = tu_lieu_thieu_nguon(dossier)
    ra += thieu
    return {"phat_hien": ra, "nguon_co": co, "nguon_tong": tong,
            "nang": [x for x in ra if x["sev"] == "cao"]}


def bao_cao(kq):
    n = kq["phat_hien"]
    print(f"\n=== B3F KIỂM DỮ KIỆN: {len(n)} phát hiện "
          f"({len(kq['nang'])} nặng) · dòng tư liệu có nguồn: "
          f"{kq['nguon_co']}/{kq['nguon_tong']} ===")
    for x in n[:40]:
        print(f"   [{x['sev']}] {x['kind']}: 「{x['token']}」")
        if x["cau"]:
            print(f"        trong câu: {x['cau']}")
        if x["goi_y"]:
            print(f"        → {x['goi_y']}")
    if len(n) > 40:
        print(f"   … và {len(n) - 40} phát hiện nữa")
    return len(n)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--dossier", required=True, help="series_ctx.txt (tư liệu sự thật)")
    a = ap.parse_args()
    kq = kiem(Path(a.script).read_text(encoding="utf-8"),
              Path(a.dossier).read_text(encoding="utf-8"))
    bao_cao(kq)
    return 1 if kq["nang"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
