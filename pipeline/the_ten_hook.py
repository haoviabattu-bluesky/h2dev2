# -*- coding: utf-8 -*-
r"""the_ten_hook.py — THẺ TÊN ĐỘNG giới thiệu nhân vật chính trong HOOK (anh chốt 10/10/2026, mọi lane).

(Sửa 14/10: hook ĐƯỢC đọc 「相葉渉、36歳。」 song song với thẻ.) Tên · tuổi (nếu có) · nghề/vai hiện bằng motion graphics
trên hình lúc nhân vật xuất hiện lần đầu. Mỗi lane 1 kiểu riêng, khai ở profile `script.hook.the_ten`
(kiểu = layout + màu). Luật đầy đủ: docs/QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md.

Dữ liệu tập: `<tập>\hook\the_ten.json`
  {"the": [{"id", "ten", "kana", "tuoi", "nghe", "chip", "shot", "dur_s", "tre_s", "mau"?, "vi_tri"?}],
   "bo_qua": {"<id>": "lý do bỏ qua"}, "cho_phep_cau": ["câu có 〜歳 được phép đọc"]}
Ra: `<tập>\hook\the_ten\the_<id>.webm` (VP9 alpha, 1920x1080) + shot `the_ten` trong hook_timeline.json
(xem_thu_hook_giong.py + ghep_hook_noi_truoc.py máy 2 tự chồng; dong_goi_may2 gửi kèm hook\the_ten\).

  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập> --nhap   # nháp từ characters.json
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập> --snap   # chụp khung soi
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập>          # render + ghi timeline
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập> --kiem   # cổng
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --mau [--nen ảnh.png] # ảnh mẫu kiểu lane
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

FPS = 30
MAU_DIR = HERE / "the_ten_mau"
FONT_NGUON = [MAU_DIR / "fonts", Path(r"C:\Users\admin\.claude\skills\motion_graphics\assets\fonts"),
              Path(r"E:\CLAUDE\YOUTUBE\THUMBNAIL\assets\fonts")]
FONTS = {"MR": "MPLUSRounded1c-Black.ttf", "NJ": "NotoSansJP.ttf", "SM": "ShipporiMinchoB1-ExtraBold.ttf"}
MAC_DINH = {"bat": False, "kieu": "vach_cheo", "mau": "#14806f", "mau_phu": "#e9c46a", "vi_tri": "tren_trai",
            "dur_s": 6.0, "toi_da": 4, "chip_mac_dinh": ""}
# ⛔ (anh chê 10/10: thẻ hiện ngắn quá) 3,5s cũ = chỉ ~2s đứng yên đọc được (bung ~1,1s + rút ~0,45s). Mặc định 6s
#    (~4,5s đọc), máy cắt theo độ dài cảnh (thoi_luong) để thẻ không trôi sang cảnh người khác; sàn 3s.
DUNG_TOI_THIEU = 3.0
SO = r"[0-9０-９〇一二三四五六七八九十百]+"
# câu kể giới thiệu nhân vật (đã bỏ phần thoại「」): 「相葉渉、36歳。」「二十歳の新人、菊池美羽は」「相葉は36歳の電気工事士だ。」
LOI_GIOI_THIEU = [re.compile(r"^[^、。]{1,14}[、，]\s*" + SO + r"歳(?:[。、，]|$)"),
                  re.compile(SO + r"歳の[^、。]{1,20}[、，][^、。]{2,10}[はが]"),
                  re.compile(r"[はが][、，]?\s*" + SO + r"歳の[^、。]{1,18}(?:だ|である|です)$")]


# ───────────────────────────── kiểu thẻ (layout) ─────────────────────────────
# Mỗi kiểu: base = cỡ chữ tên tối đa; maxw = bề rộng (dọc: bề cao) tối đa dành cho tên; css/body/tl.
# ⛔ (anh chốt 10/10, ảnh ep13 Lane F) KHUNG THẺ ÔM VỪA CHỮ: cấm khung rộng cố định (900px cho tên 4 chữ = khoảng trống to).
#    Mọi khối nằm trong luồng (flex/padding), #wrap = max-content → tên ngắn thẻ ngắn, tên dài thẻ dài. Phần tử absolute
#    chỉ được là nền/trang trí bám theo khối chứa (inset), KHÔNG được quyết định bề rộng thẻ.
# Biến: __ACC__ màu nhấn · __ACC2__ màu phụ · __TEN__ · __KANA__ · __TUOI__ · __NGHE__ · __CHIP__ · __FS__ cỡ tên
#       __D__ thời lượng · __HT__/__HK__/__HC__ = 'none' khi thiếu tuổi/kana/chip · __VAI__ = "54歳 ｜ nghề" (kiểu gộp)
KIEU = {}

KIEU["vach_cheo"] = dict(base=104, maxw=640, css="""
#grp { position: relative; display: flex; align-items: center; }
#bw { position: relative; }
#slash { position: absolute; left: -40px; right: -40px; top: 18px; bottom: 18px; background: __ACC__; transform: skewX(-14deg); opacity: 0.95; }
#box { position: relative; display: flex; flex-direction: column; align-items: flex-start; padding: 26px 56px 24px 30px; background: rgba(8, 12, 24, 0.86); border-left: 10px solid __ACC__; overflow: hidden; }
#lineT, #lineB { position: absolute; left: 0; width: 100%; height: 3px; background: __ACC2__; transform-origin: left center; }
#lineT { top: 0; } #lineB { bottom: 0; }
#chip { display: __HC__; margin: 0 0 8px 4px; padding: 6px 22px; background: __ACC__; color: #fff; font-family: "MR"; font-size: 30px; letter-spacing: 0.08em; }
#kana { display: __HK__; margin-left: 8px; color: __ACC2__; font-family: "NJ"; font-weight: 700; font-size: 26px; letter-spacing: 0.3em; }
#name { color: #fff; font-family: "MR"; font-size: __FS__px; line-height: 1.1; letter-spacing: 0.06em; white-space: nowrap; text-shadow: 0 4px 0 rgba(0,0,0,0.55); }
#role { margin: 8px 0 0 8px; color: #f1f1f1; font-family: "NJ"; font-weight: 700; font-size: 34px; letter-spacing: 0.06em; white-space: nowrap; }
#age { display: __HT__; flex: none; position: relative; z-index: 2; margin-left: -34px; width: 150px; height: 150px; border-radius: 50%; background: __ACC2__; color: #10162a; text-align: center; font-family: "MR"; box-shadow: 0 6px 0 rgba(0,0,0,0.45); }
#age b { display: block; font-size: 76px; line-height: 1; padding-top: 26px; }
#age i { display: block; font-style: normal; font-size: 26px; margin-top: 2px; }
#shine { position: absolute; top: -40px; left: 0; width: 160px; height: 400px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.28), rgba(255,255,255,0)); transform: skewX(-20deg); }
""", body="""
<div id="grp"><div id="bw"><div id="slash"></div>
  <div id="box"><div id="lineT"></div><div id="lineB"></div><div id="chip">__CHIP__</div><div id="kana">__KANA__</div>
    <div id="name">__TEN__</div><div id="role">__NGHE__</div><div id="shine" data-layout-ignore></div></div></div>
  <div id="age"><b>__TUOI__</b><i>歳</i></div></div>
""", tl="""
tl.fromTo("#slash", { x: -980, opacity: 0.95 }, { x: 0, duration: 0.32, ease: "power4.out" }, 0);
tl.fromTo("#box", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.42, ease: "power3.out" }, 0.12);
tl.fromTo("#slash", { opacity: 0.95 }, { opacity: 0, duration: 0.3, ease: "power1.in", immediateRender: false }, 0.42);
tl.fromTo(["#lineT", "#lineB"], { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.3);
tl.fromTo("#chip", { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }, 0.38);
tl.fromTo("#name", { clipPath: "inset(0 100% 0 0)", x: -30 }, { clipPath: "inset(0 0% 0 0)", x: 0, duration: 0.45, ease: "power3.out" }, 0.45);
tl.fromTo("#kana", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.6);
tl.fromTo("#role", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }, 0.7);
tl.fromTo("#age", { scale: 0, rotation: -25 }, { scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.4)" }, 0.62);
tl.fromTo("#shine", { x: -220 }, { x: 1000, duration: 0.7, ease: "power1.inOut" }, 0.95);
tl.fromTo("#wrap", { x: 0, opacity: 1 }, { x: -120, opacity: 0, duration: 0.35, ease: "power2.in", immediateRender: false }, D - 0.4);
""")

# Hồ sơ điều tra (調査ファイル): tờ giấy ngà rơi xuống, tên gõ ra từng nhịp, con dấu tuổi đóng "cộp".
KIEU["ho_so"] = dict(base=100, maxw=540, css="""
/* ⛔ 18/10 (anh chốt): BỎ NỀN CẢ THẺ — chỉ làm nền cho TỪNG KHỐI TEXT rồi viết text lên đó.
   #paper chỉ còn là khung định vị trong suốt (không giấy, không viền, không đổ bóng). */
#paper { position: relative; padding: 0; background: transparent; border: none; box-shadow: none; transform: rotate(-1.2deg); }
#tab { display: inline-block; margin: 0 0 10px 0; padding: 7px 22px; background: __ACC__; color: #fff; font-family: "NJ"; font-weight: 700; font-size: 26px; letter-spacing: 0.2em; white-space: nowrap; }
#head { display: flex; align-items: flex-start; gap: 20px; }
#kana { display: __HK__; width: max-content; margin: 0 0 6px 0; padding: 4px 14px; background: #121216; color: #efe7d4; font-family: "NJ"; font-weight: 700; font-size: 24px; letter-spacing: 0.3em; }
#name { display: inline-block; padding: 4px 20px 10px 16px; background: #14141a; color: #fff; font-family: "SM"; font-size: __FS__px; line-height: 1.15; letter-spacing: 0.04em; white-space: nowrap; }
#rule { display: none; }
#role { display: inline-block; margin: 8px 0 0 0; padding: 6px 18px; background: __ACC__; color: #fff; font-family: "NJ"; font-weight: 700; font-size: 34px; letter-spacing: 0.05em; white-space: nowrap; }
/* nền PHẢI ĐỤC + chữ đỏ đậm: nền bán trong suốt/đỏ tươi → check tương phản WCAG báo 1.6:1 (fail)
   ⛔ 18/10: BỎ transform rotate — bỏ nền card rồi thì 4 góc hộp xoay lộ video tối → check đo ra 1.77:1 */
#stamp { display: __HT__; flex: none; width: 190px; height: 118px; background: #ffffff; border: 7px solid __ACC2__; border-radius: 10px; color: #7b0c14; font-family: "SM"; font-size: 70px; line-height: 104px; text-align: center; }
""", body="""
<div id="paper"><div id="tab">__CHIP__</div>
  <div id="head"><div><div id="kana">__KANA__</div><div id="name">__TEN__</div></div><div id="stamp">__TUOI__歳</div></div>
  <div id="rule"></div><div id="role">__NGHE__</div></div>
""", tl="""
tl.fromTo("#paper", { y: -60, opacity: 0, rotation: -5 }, { y: 0, opacity: 1, rotation: -1.2, duration: 0.45, ease: "power3.out" }, 0);
tl.fromTo("#tab", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }, 0.25);
tl.fromTo("#name", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.6, ease: "power2.inOut" }, 0.4);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 0.55);
tl.fromTo("#rule", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, 0.75);
tl.fromTo("#role", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.6, ease: "power1.inOut" }, 0.9);
tl.fromTo("#stamp", { scale: 2.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 1.25);
// 16/10 (Lane L ep19, anh: motion giới thiệu bị GIẬT): bỏ steps(6)/steps(10) (chữ hiện cắt nửa nét, giật cục) + bỏ rung giấy 6px
// sau con dấu → lộ chữ bằng quét mượt.
tl.fromTo("#wrap", { y: 0, opacity: 1 }, { y: -50, opacity: 0, duration: 0.35, ease: "power2.in", immediateRender: false }, D - 0.4);
""")

# Chữ dọc (縦書き) kiểu Chiến quốc: dải mực đổ từ trên xuống, nét cọ đỏ, tên vàng từng chữ rơi, ấn triện.
KIEU["tategaki"] = dict(base=112, maxw=520, doc=True, css="""
#col { position: relative; display: flex; flex-direction: column; align-items: center; padding: 40px 34px 30px 58px; }
#ink { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,8,6,0.9), rgba(10,8,6,0.8)); }
#brush { position: absolute; left: 30px; top: 0; bottom: 0; width: 12px; background: __ACC2__; transform-origin: center top; }
#cols { position: relative; display: flex; flex-direction: row-reverse; align-items: flex-start; gap: 22px; }
#kana { display: __HK__; margin-top: 20px; writing-mode: vertical-rl; color: #d8c9a0; font-family: "NJ"; font-weight: 700; font-size: 24px; letter-spacing: 0.3em; }
#name { writing-mode: vertical-rl; color: __ACC__; font-family: "SM"; font-size: __FS__px; line-height: 1.2; letter-spacing: 0.1em; }
#name span { display: inline-block; }
#role { margin-top: 20px; writing-mode: vertical-rl; color: #f2e8d0; font-family: "NJ"; font-weight: 700; font-size: 34px; letter-spacing: 0.12em; white-space: nowrap; }
#role .tcy { text-combine-upright: all; }
#seal { display: __HC__; position: relative; margin-top: 24px; padding: 0 14px; min-width: 116px; height: 90px; background: __ACC2__; color: #fff; font-family: "SM"; font-size: 32px; line-height: 90px; text-align: center; white-space: nowrap; transform: rotate(-6deg); }
""", body="""
<div id="col"><div id="ink"></div><div id="brush"></div>
  <div id="cols"><div id="kana">__KANA__</div><div id="name" data-layout-allow-occlusion>__TEN_SPANS__</div><div id="role">__VAI_DOC__</div></div>
  <div id="seal">__CHIP__</div></div>
""", tl="""
tl.fromTo("#ink", { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 0.5, ease: "power3.out" }, 0);
tl.fromTo("#brush", { scaleY: 0 }, { scaleY: 1, duration: 0.55, ease: "power2.out" }, 0.1);
tl.fromTo("#name span", { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power2.out", stagger: 0.09 }, 0.35);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.7);
tl.fromTo("#role", { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 0.5, ease: "power2.out" }, 0.8);
tl.fromTo("#seal", { scale: 1.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 1.15);
tl.fromTo("#wrap", { x: 0, opacity: 1 }, { x: 60, opacity: 0, duration: 0.4, ease: "power2.in", immediateRender: false }, D - 0.45);
""")

# Thẻ tròn mềm (cho lane người già, ấm): viên thuốc trắng, chấm tròn chữ đầu họ, bật nhẹ.
KIEU["mem"] = dict(base=84, maxw=600, css="""
#row { position: relative; display: flex; align-items: center; height: 210px; padding: 0 52px 0 20px; }
#pill { position: absolute; inset: 0; background: rgba(255,255,255,0.95); border-radius: 105px 36px 36px 105px; box-shadow: 0 8px 24px rgba(0,0,0,0.35); }
#dot { position: relative; flex: none; width: 170px; height: 170px; border-radius: 50%; background: __ACC__; color: #fff; font-family: "MR"; font-size: 92px; line-height: 170px; text-align: center; }
#txt { position: relative; display: flex; flex-direction: column; align-items: flex-start; margin-left: 26px; }
#chip { display: __HC__; padding: 3px 18px; background: __ACC2__; color: #2a2a2a; font-family: "MR"; font-size: 26px; border-radius: 20px; white-space: nowrap; }
#name { color: #2a2a2a; font-family: "MR"; font-size: __FS__px; line-height: 1.15; letter-spacing: 0.05em; white-space: nowrap; }
#role { margin-left: 4px; color: #444; font-family: "NJ"; font-weight: 700; font-size: 32px; letter-spacing: 0.04em; white-space: nowrap; }
#role b { color: __ACC__; }
""", body="""
<div id="row"><div id="pill"></div><div id="dot">__DAU__</div>
  <div id="txt"><div id="chip">__CHIP__</div><div id="name">__TEN__</div><div id="role">__VAI__</div></div></div>
""", tl="""
tl.fromTo("#pill", { scale: 0.6, opacity: 0, transformOrigin: "105px 105px" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }, 0);
tl.fromTo("#dot", { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }, 0.15);
tl.fromTo("#chip", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.4);
tl.fromTo("#name", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 0.45);
tl.fromTo("#role", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.7);
tl.fromTo("#wrap", { y: 0, opacity: 1, scale: 1 }, { y: 20, opacity: 0, scale: 0.95, duration: 0.4, ease: "power2.in", immediateRender: false }, D - 0.45);
""")

# Nét mảnh thanh lịch (gia đình/vợ chồng): bóng tối mờ, 1 nét kẻ vẽ ra, tên trồi lên từ sau nét kẻ.
KIEU["net_manh"] = dict(base=96, maxw=820, css="""
#blk { position: relative; padding: 0 10px 0 0; }
#shade { position: absolute; left: -60px; top: -20px; right: -120px; bottom: -20px; background: linear-gradient(90deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.42) 60%, rgba(0,0,0,0) 100%); }
#chip { display: __HC__; position: relative; margin-left: 4px; color: __ACC__; font-family: "NJ"; font-weight: 700; font-size: 24px; letter-spacing: 0.25em; white-space: nowrap; }
#kana { display: __HK__; position: relative; margin: 4px 0 0 6px; color: rgba(255,255,255,0.82); font-family: "NJ"; font-weight: 700; font-size: 24px; letter-spacing: 0.35em; white-space: nowrap; }
#mask { position: relative; overflow: hidden; }
#name { position: relative; color: #fff; font-family: "SM"; font-size: __FS__px; line-height: 1.2; letter-spacing: 0.06em; white-space: nowrap; }
#line { position: relative; margin-top: 2px; width: 100%; height: 3px; background: __ACC__; transform-origin: left center; }
#role { position: relative; margin: 12px 0 0 4px; color: #f3f3f3; font-family: "NJ"; font-weight: 700; font-size: 34px; letter-spacing: 0.06em; white-space: nowrap; }
#role b { color: __ACC2__; }
""", body="""
<div id="blk"><div id="shade"></div><div id="chip">__CHIP__</div><div id="kana">__KANA__</div>
  <div id="mask" data-layout-allow-overflow><div id="name" data-layout-allow-occlusion data-layout-allow-overflow>__TEN__</div></div><div id="line"></div><div id="role">__VAI__</div></div>
""", tl="""
tl.fromTo("#shade", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.out" }, 0);
tl.fromTo("#line", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.inOut" }, 0.1);
tl.fromTo("#name", { yPercent: 105 }, { yPercent: 0, duration: 0.55, ease: "power3.out" }, 0.4);
tl.fromTo(["#chip", "#kana"], { opacity: 0 }, { opacity: 1, duration: 0.35, stagger: 0.1 }, 0.6);
tl.fromTo("#role", { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 0.75);
tl.fromTo("#wrap", { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power1.in", immediateRender: false }, D - 0.5);
""")

# Bảng tên đeo ngực (名札) kiểu quầy thuốc: kẹp kim loại, đung đưa rơi xuống rồi đứng yên.
KIEU["bang_ten"] = dict(base=92, maxw=600, css="""
#wrap { transform-origin: 50% -40px; }
#badge { position: relative; min-width: 440px; padding-bottom: 22px; background: #fff; border-radius: 22px; border: 6px solid __ACC__; box-shadow: 0 12px 26px rgba(0,0,0,0.42); overflow: hidden; }
#head { height: 74px; padding: 0 30px; background: __ACC__; color: #fff; font-family: "MR"; font-size: 34px; line-height: 74px; letter-spacing: 0.15em; white-space: nowrap; }
#kana { display: __HK__; margin: 12px 0 0 34px; color: #777; font-family: "NJ"; font-weight: 700; font-size: 22px; letter-spacing: 0.3em; white-space: nowrap; }
#name { margin: 0 40px 0 28px; color: #1d1d1d; font-family: "MR"; font-size: __FS__px; line-height: 1.15; letter-spacing: 0.05em; white-space: nowrap; }
#foot { display: flex; align-items: center; justify-content: space-between; gap: 24px; margin: 8px 26px 0 34px; }
#role { color: #333; font-family: "NJ"; font-weight: 700; font-size: 32px; white-space: nowrap; }
#age { display: __HT__; flex: none; padding: 4px 20px; background: __ACC2__; color: #fff; font-family: "MR"; font-size: 36px; border-radius: 30px; white-space: nowrap; }
#clip { position: absolute; left: 50%; top: -46px; margin-left: -40px; width: 80px; height: 62px; background: linear-gradient(180deg, #e3e7eb, #9aa3ab); border-radius: 10px 10px 4px 4px; box-shadow: 0 3px 6px rgba(0,0,0,0.4); }
""", body="""
<div id="badge"><div id="head">__CHIP__</div><div id="kana">__KANA__</div><div id="name">__TEN__</div>
  <div id="foot"><div id="role">__NGHE__</div><div id="age">__TUOI__歳</div></div></div><div id="clip"></div>
""", tl="""
tl.fromTo("#wrap", { y: -460, rotation: -16 }, { y: 0, rotation: 0, duration: 0.9, ease: "elastic.out(1, 0.45)" }, 0);
tl.fromTo("#name", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }, 0.55);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.65);
tl.fromTo("#role", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.75);
tl.fromTo("#age", { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(2.4)" }, 0.85);
tl.fromTo("#wrap", { y: 0, opacity: 1 }, { y: -80, opacity: 0, duration: 0.35, ease: "power2.in", immediateRender: false }, D - 0.4);
""")

# Telop bản tin (ニューステロップ) 2 tầng cho lane số liệu đời thật: thanh tên quét ra, ô tuổi lật, thanh nghề dưới.
KIEU["ban_tin"] = dict(base=86, maxw=760, css="""
#tag { display: __HC__; width: max-content; height: 42px; padding: 0 20px; background: __ACC2__; color: #fff; font-family: "NJ"; font-weight: 700; font-size: 24px; line-height: 42px; letter-spacing: 0.12em; white-space: nowrap; }
#r1 { display: flex; height: 122px; }
#nm { position: relative; padding: 0 44px 0 34px; }
#bar1 { position: absolute; inset: 0; background: __ACC__; transform-origin: left center; box-shadow: 0 6px 14px rgba(0,0,0,0.35); }
#name { position: relative; color: #fff; font-family: "NJ"; font-weight: 900; font-size: __FS__px; line-height: 122px; letter-spacing: 0.05em; white-space: nowrap; }
#age { display: __HT__; flex: none; width: 130px; height: 122px; background: #fff; color: __ACC__; font-family: "NJ"; font-weight: 900; font-size: 50px; line-height: 122px; text-align: center; }
#rl { position: relative; width: max-content; height: 60px; padding: 0 34px; }
#bar2 { position: absolute; inset: 0; background: rgba(12,12,12,0.86); transform-origin: left center; }
#role { position: relative; color: #fff; font-family: "NJ"; font-weight: 700; font-size: 32px; line-height: 60px; white-space: nowrap; }
""", body="""
<div id="tag">__CHIP__</div>
<div id="r1"><div id="nm"><div id="bar1"></div><div id="name">__TEN__</div></div><div id="age">__TUOI__歳</div></div>
<div id="rl"><div id="bar2"></div><div id="role">__NGHE__</div></div>
""", tl="""
tl.fromTo("#bar1", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, 0);
tl.fromTo("#name", { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power2.out" }, 0.25);
tl.fromTo("#age", { rotationX: 90, opacity: 0 }, { rotationX: 0, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }, 0.4);
tl.fromTo("#bar2", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, 0.5);
tl.fromTo("#role", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, 0.7);
tl.fromTo("#tag", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, 0.6);
tl.fromTo("#wrap", { x: 0, opacity: 1 }, { x: __RA_X__, opacity: 0, duration: 0.4, ease: "power3.in", immediateRender: false }, D - 0.42);
""")

# Giấy nhớ (付箋) dán băng keo cho lane vui/sở thích: tờ note xoay bật vào, vòng tròn tuổi khoanh bút.
KIEU["giay_note"] = dict(base=92, maxw=440, css="""
#note { position: relative; min-width: 420px; padding: 34px 36px 28px 32px; background: __ACC__; box-shadow: 0 10px 18px rgba(0,0,0,0.35); transform: rotate(-3deg); }
#top { display: flex; align-items: center; gap: 28px; }
#kana { display: __HK__; margin-left: 6px; color: #6b5a2a; font-family: "NJ"; font-weight: 700; font-size: 22px; letter-spacing: 0.3em; white-space: nowrap; }
#name { color: #3a2e14; font-family: "MR"; font-size: __FS__px; line-height: 1.15; letter-spacing: 0.04em; white-space: nowrap; }
#age { display: __HT__; flex: none; width: 128px; height: 128px; border-radius: 50%; border: 6px solid __ACC2__; color: __ACC2__; font-family: "MR"; font-size: 44px; line-height: 116px; text-align: center; transform: rotate(8deg); }
#dash { margin-top: 14px; width: 100%; border-top: 4px dashed rgba(58,46,20,0.35); }
#role { margin: 14px 0 0 6px; color: #3a2e14; font-family: "NJ"; font-weight: 700; font-size: 32px; white-space: nowrap; }
#tape { position: absolute; left: 50%; top: -24px; margin-left: -80px; width: 160px; height: 48px; background: rgba(255,255,255,0.6); transform: rotate(2deg); transform-origin: left center; }
""", body="""
<div id="note"><div id="top"><div><div id="kana">__KANA__</div><div id="name">__TEN__</div></div><div id="age">__TUOI__歳</div></div>
  <div id="dash"></div><div id="role">__NGHE__</div></div><div id="tape"></div>
""", tl="""
tl.fromTo("#note", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }, 0);
tl.fromTo("#tape", { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power2.out" }, 0.35);
tl.fromTo("#name", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.45);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.55);
tl.fromTo("#age", { scale: 0, rotation: -40 }, { scale: 1, rotation: 8, duration: 0.4, ease: "back.out(2.2)" }, 0.65);
tl.fromTo("#dash", { scaleX: 0, transformOrigin: "left center" }, { scaleX: 1, duration: 0.35 }, 0.7);
tl.fromTo("#role", { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, 0.85);
tl.fromTo("#wrap", { y: 0, rotation: 0, opacity: 1 }, { y: 40, rotation: 8, opacity: 0, duration: 0.4, ease: "power2.in", immediateRender: false }, D - 0.45);
""")

# Dải ruy băng + huy chương tuổi (đời senior "từ nay"): ruy băng mở ngang, huy chương xoay vào.
KIEU["ruy_bang"] = dict(base=76, maxw=520, css="""
/* 10/10 anh (Lane N ep08): thẻ to che mặt → thu nhỏ, ruy băng ôm vừa tên, huy chương tuổi đặt SÁT ngay sau tên */
#kana { display: __HK__; width: max-content; margin-left: 58px; padding: 2px 12px; background: rgba(0,0,0,0.62); border-radius: 6px; color: #fff; font-family: "NJ"; font-weight: 700; font-size: 21px; letter-spacing: 0.28em; white-space: nowrap; }
#row { display: flex; align-items: center; margin-top: 4px; }
#rib { position: relative; height: 112px; padding: 0 64px 0 54px; background: __ACC__; clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 26px 50%); }
#name { color: #fff; font-family: "MR"; font-size: __FS__px; line-height: 112px; letter-spacing: 0.05em; white-space: nowrap; text-shadow: 0 3px 0 rgba(0,0,0,0.3); }
#medal { display: __HT__; flex: none; margin-left: -40px; width: 136px; height: 136px; border-radius: 50%; background: __ACC2__; border: 6px solid #fff; color: #3b1f12; font-family: "MR"; text-align: center; box-shadow: 0 6px 14px rgba(0,0,0,0.4); position: relative; z-index: 2; }
#medal b { display: block; font-size: 58px; line-height: 1; padding-top: 22px; }
#medal i { display: block; font-style: normal; font-size: 22px; }
#role { width: max-content; margin: 6px 0 0 58px; padding: 5px 16px; background: rgba(0,0,0,0.62); color: #fff; font-family: "NJ"; font-weight: 700; font-size: 29px; border-radius: 6px; white-space: nowrap; }
""", body="""
<div id="kana">__KANA__</div>
<div id="row"><div id="rib"><div id="name">__TEN__</div></div><div id="medal" data-layout-allow-overlap><b>__TUOI__</b><i>歳</i></div></div>
<div id="role">__NGHE__</div>
""", tl="""
tl.fromTo("#rib", { clipPath: "polygon(0 0, 0% 0, 0% 100%, 0 100%, 26px 50%)" }, { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%, 26px 50%)", duration: 0.5, ease: "power3.out" }, 0);
tl.fromTo("#name", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.35);
tl.fromTo("#medal", { scale: 0, rotation: 180 }, { scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, 0.45);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.6);
tl.fromTo("#role", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.75);
tl.fromTo("#wrap", { scale: 1, opacity: 1 }, { scale: 0.92, opacity: 0, duration: 0.4, ease: "power2.in", immediateRender: false }, D - 0.45);
""")

# Cuộn thư (巻物) cho kể chuyện người già/悟り: 2 trục gỗ, giấy washi mở ra giữa, tên Minchō mực, nét cọ gạch dưới.
KIEU["cuon_thu"] = dict(base=92, maxw=560, css="""
#scroll { position: relative; padding: 10px 22px; }
#paper { position: relative; padding: 18px 70px 22px 42px; background: linear-gradient(180deg, #f7f0dc, #efe3c4); box-shadow: 0 8px 20px rgba(0,0,0,0.45); }
#rodL, #rodR { position: absolute; top: 0; bottom: 0; width: 26px; background: linear-gradient(90deg, #4a2c17, #8a5a33, #4a2c17); border-radius: 8px; }
#rodL { left: 0; } #rodR { right: 0; }
#rail { position: absolute; inset: 0; }
#kana { display: __HK__; margin-left: 6px; color: #7a6a52; font-family: "NJ"; font-weight: 700; font-size: 22px; letter-spacing: 0.35em; white-space: nowrap; }
#name { color: #1e1a14; font-family: "SM"; font-size: __FS__px; line-height: 1.15; letter-spacing: 0.08em; white-space: nowrap; }
#brushU { margin-top: 4px; width: 100%; height: 8px; background: __ACC__; border-radius: 4px; transform-origin: left center; }
#role { margin: 8px 0 0 6px; color: #3a3228; font-family: "NJ"; font-weight: 700; font-size: 32px; white-space: nowrap; }
#role b { color: __ACC__; }
""", body="""
<div id="scroll"><div id="paper"><div id="kana">__KANA__</div><div id="name">__TEN__</div><div id="brushU"></div><div id="role">__VAI__</div></div>
  <div id="rodL"></div><div id="rail"><div id="rodR"></div></div></div>
""", tl="""
tl.fromTo("#rail", { xPercent: -100, x: 26 }, { xPercent: 0, x: 0, duration: 0.6, ease: "power2.out" }, 0);   // trục phải chạy theo bề rộng thật của giấy
tl.fromTo("#paper", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.6, ease: "power2.out" }, 0);
tl.fromTo("#name", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power1.out" }, 0.45);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.6);
tl.fromTo("#brushU", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.inOut" }, 0.75);
tl.fromTo("#role", { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.95);
tl.fromTo("#wrap", { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power1.in", immediateRender: false }, D - 0.5);
""")

# Gợn sóng tròn (tâm lý gia đình): vòng tròn mờ nở ra, 2 gợn lan, tên ở giữa, vai bên dưới.
KIEU["vong_song"] = dict(base=78, maxw=400, css="""
#ball { position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 340px; aspect-ratio: 1 / 1; padding: 40px 54px; }
#disc, #ring1, #ring2 { position: absolute; inset: 0; border-radius: 50%; }
#disc { background: radial-gradient(circle, rgba(20,14,20,0.82) 0%, rgba(20,14,20,0.7) 70%, rgba(20,14,20,0.55) 100%); }
#ring1, #ring2 { border: 4px solid __ACC__; }
#kana { display: __HK__; position: relative; color: __ACC2__; font-family: "NJ"; font-weight: 700; font-size: 22px; letter-spacing: 0.3em; white-space: nowrap; }
#name { position: relative; color: #fff; font-family: "SM"; font-size: __FS__px; line-height: 1.2; white-space: nowrap; }
#role { position: relative; margin-top: 6px; color: #f3e9ee; font-family: "NJ"; font-weight: 700; font-size: 28px; white-space: nowrap; }
#role b { color: __ACC2__; }
""", body="""
<div id="ball"><div id="ring1" data-layout-ignore></div><div id="ring2" data-layout-ignore></div><div id="disc"></div>
  <div id="kana">__KANA__</div><div id="name">__TEN__</div><div id="role">__VAI__</div></div>
""", tl="""
tl.fromTo("#disc", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }, 0);
tl.fromTo("#ring1", { scale: 0.9, opacity: 0.9 }, { scale: 1.35, opacity: 0, duration: 1.1, ease: "power1.out" }, 0.2);
tl.fromTo("#ring2", { scale: 0.9, opacity: 0.9 }, { scale: 1.35, opacity: 0, duration: 1.1, ease: "power1.out" }, 0.6);
tl.fromTo("#name", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power2.out" }, 0.4);
tl.fromTo("#kana", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.55);
tl.fromTo("#role", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.7);
tl.fromTo("#wrap", { scale: 1, opacity: 1 }, { scale: 0.9, opacity: 0, duration: 0.4, ease: "power2.in", immediateRender: false }, D - 0.45);
""")

# Kiểu đã GIỮ CHỖ cho lane chưa có profile — lane khác không được lấy (luật: mỗi lane 1 kiểu riêng).
GIU_CHO = {"tategaki": "sengoku-uragawa", "vong_song": "kokoro-kazoku"}

HTML = r"""<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face { font-family: "MR"; src: url("assets/fonts/MPLUSRounded1c-Black.ttf"); }
@font-face { font-family: "NJ"; src: url("assets/fonts/NotoSansJP.ttf"); }
@font-face { font-family: "SM"; src: url("assets/fonts/ShipporiMinchoB1-ExtraBold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1920px; height: 1080px; overflow: hidden; background: __BG__; }
#root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: __BG__; }
#card { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
#sc { position: absolute; __POS__ width: max-content; height: max-content; transform: scale(__ZOOM__); transform-origin: left top; }
#wrap { position: relative; width: max-content; height: max-content; }
__CSS__
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__D__" data-width="1920" data-height="1080">
  __NEN__
  <div id="card" class="clip" data-start="0" data-duration="__D__" data-track-index="1">
    <div id="sc"><div id="wrap">__BODY__</div></div>
  </div>
</div>
<script>
const D = __D__;
const tl = gsap.timeline({ paused: true });
__TL__
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""


def cau_hinh(prof):
    c = dict(MAC_DINH)
    c.update(((prof.get("script") or {}).get("hook") or {}).get("the_ten") or {})
    return c


def is_enabled(prof):
    return bool(cau_hinh(prof).get("bat"))


def _esc(s):
    return (str(s or "")).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _so_dong(s):
    """Số ngang trong chữ dọc: bọc 2 chữ số vào tate-chu-yoko."""
    return re.sub(r"[0-9]{1,3}", lambda m: f'<span class="tcy">{m.group(0)}</span>', s)


def _vi_tri_tay(t):
    """vi_tri khai tay trên 1 thẻ: "tren_trai"/"tren_phai" (neo góc) hoặc [x, y] (px góc trái-trên #wrap). Không khai /
    "tu_dong" → None = máy tự đặt cạnh nhân vật (chon_vi_tri)."""
    v = t.get("vi_tri")
    if not v and isinstance(t.get("xy"), (list, tuple)) and len(t["xy"]) == 2:   # field cũ: tỉ lệ 0–1 góc trên-trái
        v = [round(float(t["xy"][0]) * 1920), round(float(t["xy"][1]) * 1080)]
    if isinstance(v, (list, tuple)) and len(v) == 2:
        return [int(v[0]), int(v[1])]
    return v if v in ("tren_trai", "tren_phai") else None


def html_the(prof, t, nen="", xy=None, zoom=None):
    """xy = (x, y) góc trái-trên #wrap (px khung 1920x1080) do chon_vi_tri tính; None → neo góc theo vi_tri.
    zoom = tỉ lệ thu nhỏ thẻ (1.0 = cỡ gốc); None → lấy c["zoom"] (profile) → thẻ nhỏ, sát một bên, không che mặt."""
    c = cau_hinh(prof)
    # 1 thẻ được đổi màu (vd kẻ gây chuyện màu đỏ) / neo tay 1 góc
    c.update({x: t[x] for x in ("mau", "mau_phu") if t.get(x)})
    tay = _vi_tri_tay(t)
    if isinstance(tay, list):
        xy = xy or tay
    elif tay:
        c["vi_tri"] = tay
    k = KIEU.get(c["kieu"])
    if not k:
        raise SystemExit(f"✗ kiểu thẻ '{c['kieu']}' không có — chọn: {', '.join(KIEU)}")
    z = float(zoom if zoom is not None else (t.get("zoom") or c.get("zoom") or 1.0))
    d = round(float(t.get("dur_s") or c["dur_s"]) * FPS) / FPS
    ten = str(t.get("ten") or "").strip()
    n = max(1, len(ten.replace(" ", "")))
    fs = min(k["base"], int(k["maxw"] / (n * 1.12)))
    tuoi = str(t.get("tuoi") or "").strip()
    nghe = str(t.get("nghe") or "").strip()
    chip = str(t.get("chip") or c.get("chip_mac_dinh") or "").strip()
    if c["kieu"] == "ho_so" and not chip:
        chip = f"FILE {int(t.get('_i') or 1):02d}"
    vai = (f"<b>{_esc(tuoi)}歳</b>　｜　" if tuoi else "") + _esc(nghe)
    if xy:
        pos = f"left: {int(xy[0])}px; top: {int(xy[1])}px;"
        phai = int(xy[0]) > 760
    else:
        phai = c["vi_tri"] == "tren_phai"
        pos = f"{'right' if phai else 'left'}: 96px; top: {60 if k.get('doc') else 84}px;"
    s = (HTML.replace("__CSS__", k["css"]).replace("__BODY__", k["body"]).replace("__TL__", k["tl"])
         .replace("__BG__", "#000" if nen else "transparent")
         .replace("__NEN__", f'<img class="clip" data-start="0" data-duration="__D__" data-track-index="0" src="{nen}" '
                             f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />' if nen else ""))
    rep = {"__D__": f"{d}", "__POS__": pos, "__ZOOM__": f"{z:g}", "__RA_X__": "1200" if phai else "-1200",
           "__ACC2__": c["mau_phu"], "__ACC__": c["mau"], "__FS__": str(fs),
           "__TEN_SPANS__": "".join(f"<span data-layout-allow-occlusion>{_esc(ch)}</span>" for ch in ten.replace(" ", "")),
           "__TEN__": _esc(ten).replace(" ", "&#8202;"), "__KANA__": _esc(t.get("kana")), "__TUOI__": _esc(tuoi),
           "__NGHE__": _esc(nghe), "__CHIP__": _esc(chip), "__VAI__": vai,
           "__VAI_DOC__": _so_dong((f"{_esc(tuoi)}歳　" if tuoi else "") + _esc(nghe)),
           "__DAU__": _esc(ten[:1]),
           "__HT__": "block" if tuoi else "none", "__HK__": "block" if t.get("kana") else "none",
           "__HC__": "block" if chip else "none"}
    for a, b in rep.items():
        s = s.replace(a, b)
    return s, d


# ───────────────────────────── dữ liệu tập ─────────────────────────────
def _doc(p, mac=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return mac


def _shots(hd):
    tl = _doc(hd / "hook_timeline.json", {}) or {}
    return tl, (tl.get("shots") if isinstance(tl, dict) else tl) or []


def _so(s, i):
    """Số cảnh: field n, shot không có n thì lấy thứ tự (1-based)."""
    return int(s.get("n") or i + 1)


def _cast(s):
    return [x.strip() for x in str(s.get("cast") or "").split(",") if x.strip()]


def _ten_rieng(c):
    ten = re.sub(r"[（(].*?[）)]", "", str(c.get("name") or "")).strip()
    return ten if ten and "の" not in ten else ""


def nhan_vat_chinh(d):
    """Nhân vật PHẢI có thẻ: có tên riêng + có REF + (main | có thoại「」trong hook | xuất hiện ≥3 cảnh hook)."""
    d = Path(d)
    chars = (_doc(d / "characters.json", {}) or {}).get("characters") or []
    _, shots = _shots(d / "hook")
    ra = []
    for c in chars:
        ten = _ten_rieng(c)
        if not ten or not c.get("ref"):
            continue
        sh = [dict(s, n=_so(s, i)) for i, s in enumerate(shots) if c["id"] in _cast(s)]
        thoai = any("「" in str(s.get("voice") or "") and _cast(s)[:1] == [c["id"]] for s in sh)
        if sh and (c.get("main") or thoai or len(sh) >= 3):
            ra.append((c, sh))
    return ra


def nhap(prof, d, force=False):
    d = Path(d)
    p = d / "hook" / "the_ten.json"
    if p.exists() and not force:
        raise SystemExit(f"✗ đã có {p} — sửa tay hoặc --force để nháp lại")
    c = cau_hinh(prof)
    the, bo, dem = [], {}, {}
    for i, (ch, sh) in enumerate(nhan_vat_chinh(d), 1):
        vai = re.split(r"[（(—]", str(ch.get("vai") or ""))[0].strip()
        # LUẬT (anh chốt 10/10): thẻ bật ở cảnh ẢNH NHÂN VẬT HIỆN LẦN ĐẦU — không dời về cảnh sau/cảnh tổng kết cuối hook
        n = sh[0]["n"]
        k = dem.get(n, 0)
        dem[n] = k + 1
        t = {"id": ch["id"], "ten": _ten_rieng(ch), "kana": "", "tuoi": ch.get("age") or "",
             "nghe": vai[:18], "chip": "", "shot": n, "tre_s": 0.0}
        if k:   # người thứ 2 cùng cảnh: bật trễ 0,6s (vị trí máy tự đặt cạnh người đó, tránh thẻ thứ nhất)
            t.update(tre_s=0.6)
        the.append(t)
    the.sort(key=lambda t: t["shot"])
    for n, k in dem.items():
        if k > 2:
            print(f"  ⚠ cảnh {n} có {k} nhân vật chính xuất hiện lần đầu — tối đa 2 thẻ/cảnh: tách cảnh hoặc bo_qua người phụ")
    if len(the) > c["toi_da"]:
        print(f"  ⚠ {len(the)} nhân vật đủ điều kiện > toi_da {c['toi_da']} — chuyển người ít quan trọng sang bo_qua kèm lý do")
    p.write_text(json.dumps({"_doc": "Thẻ tên động hook — docs/QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md. ten = 'Họ Tên' (cách 1 dấu cách), "
                                     "kana = cách đọc, tuoi bỏ trống nếu không rõ, nghe ≤18 chữ, shot = số cảnh xuất hiện lần đầu.",
                             "the": the, "bo_qua": bo, "cho_phep_cau": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ nháp {p} ({len(the)} thẻ) — SỬA kana/nghe/chip cho đúng rồi chạy render")
    for t in the:
        print(f"   · {t['id']}: {t['ten']} {t['tuoi']}歳 {t['nghe']} → cảnh {t['shot']}")


def _ws(hd):
    ws = hd / "mg_the_ten"
    (ws / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    for f in FONTS.values():
        dst = ws / "assets" / "fonts" / f
        if not dst.exists():
            src = next((g / f for g in FONT_NGUON if (g / f).exists()), None)
            if not src:
                raise SystemExit(f"✗ thiếu font {f} (tìm ở {FONT_NGUON})")
            shutil.copy2(src, dst)
    if not (ws / "hyperframes.json").exists():
        (ws / "hyperframes.json").write_text(json.dumps({
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
            "media": {"autoProxy": True}}, indent=2), encoding="utf-8")
        (ws / "meta.json").write_text(json.dumps({"id": "mg_the_ten", "name": "mg_the_ten"}, indent=2), encoding="utf-8")
    return ws


def npx(ws, *a):
    exe = "npx.cmd" if os.name == "nt" else "npx"
    r = subprocess.run([exe, "--yes", "hyperframes@0.8.144", *a], cwd=ws, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(f"✗ hyperframes {a[0]} lỗi")
    return r.stdout


# ───────────────────────────── vị trí thẻ ─────────────────────────────
# ⛔ (anh chốt 10/10, ảnh ep13 cảnh 2: thẻ 三上 nằm bên trái cạnh người đang cười, còn 三上 ngồi bên phải → người xem
#    tưởng thẻ là của người đang cười). Thẻ KHÔNG cố định 1 góc: máy tìm mặt mọi người trong ảnh cảnh (vision), rồi đặt thẻ
#    GẦN mặt nhân vật được giới thiệu nhất, KHÔNG che mặt ai, KHÔNG gần người khác hơn, và trên vùng phụ đề.
#    Khai tay `"vi_tri": "tren_trai"|"tren_phai"|[x, y]` trên 1 thẻ trong the_ten.json để ép (vision sai).
SUB_Y = 760          # mép trên vùng phụ đề (clip xem thử + máy 2) — thẻ không được thò xuống dưới
LE = 36              # lề khung


def do_khung(ws, html):
    """Đo hộp chữ nhật thật của thẻ (mọi phần tử hiện ra, lúc thẻ đã bung hết) bằng Chrome headless — font thật, nên
    tên dài/ngắn ra đúng bề rộng. Trả (w, h, dx, dy): dx/dy = lệch mép hộp so với góc #wrap (slash/tab thò ra ngoài)."""
    from playwright.sync_api import sync_playwright
    f = ws / "_do.html"
    f.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(f.as_uri())
        pg.wait_for_function("window.__timelines && window.__timelines.main && document.fonts.status === 'loaded'",
                             timeout=60000)
        r = pg.evaluate("""() => {
          const tl = window.__timelines.main; tl.seek(Math.min(1.9, tl.duration() - 0.6), false);
          const sc = document.getElementById('sc'), w = document.getElementById('wrap');
          const o = (sc || w).getBoundingClientRect();
          let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
          for (const e of [w, ...w.querySelectorAll('*')]) {
            if (e.closest('[data-layout-ignore]')) continue;
            const cs = getComputedStyle(e);
            if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) continue;
            const r = e.getBoundingClientRect();
            if (r.width < 1 || r.height < 1) continue;
            x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
          }
          return [x1 - x0, y1 - y0, x0 - o.left, y0 - o.top];
        }""")
        b.close()
    f.unlink()
    return [round(v) for v in r]


def _anh_shot(hd, s):
    """Khung hình người xem THẬT thấy lúc thẻ bung: khung giây ~1,2 của clip Grok (clip hay zoom/xê dịch so với ảnh gốc
    — ep13 cảnh 2 người to gấp rưỡi ảnh) → hook/the_ten/_khung_<n>.jpg; chưa có clip thì ảnh cảnh."""
    clip = hd / str(s.get("clip") or "")
    if s.get("clip") and clip.exists():
        out = hd / "the_ten" / f"_khung_{clip.stem}.jpg"
        if not out.exists() or out.stat().st_mtime < clip.stat().st_mtime:
            import imageio_ffmpeg
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-ss", "1.2", "-i", str(clip),
                            "-frames:v", "1", "-vf", "scale=1920:1080", "-q:v", "3", str(out)], check=False)
        if out.exists():
            return out
    p = hd / str(s.get("img") or "")
    return p if s.get("img") and p.exists() else None


def _mo_ta(ch, tuoi):
    """Ngoại hình đúng tuổi trên thẻ (look_48 cho cảnh hồi tưởng 48 tuổi…)."""
    return str(ch.get(f"look_{tuoi}") or ch.get("look") or ch.get("role") or "")[:600]


def tim_nguoi(hd, s, t, chars):
    """Hỏi vision: mọi người trong ảnh cảnh + ai là nhân vật của thẻ. Trả list {"mat":[x0,y0,x1,y1], "than":[…], "dich":bool}
    theo px khung 1920x1080 (ảnh phủ kín khung kiểu cover). Cache theo ảnh + id ở hook/the_ten/_nguoi.json."""
    anh = _anh_shot(hd, s)
    if not anh:
        return None
    cache_p = hd / "the_ten" / "_nguoi.json"
    cache = _doc(cache_p, {}) or {}
    khoa = f"{anh.name}|{anh.stat().st_mtime_ns}|{t['id']}"
    if khoa in cache:
        return cache[khoa]
    from PIL import Image
    im = Image.open(anh).convert("RGB")
    W0, H0 = im.size
    nho = hd / "the_ten" / f"_nho_{anh.stem}.jpg"
    im.resize((1280, round(1280 * H0 / W0))).save(nho, quality=88)
    by = {c.get("id"): c for c in chars}
    dich = by.get(t["id"], {})
    khac = [by[x] for x in _cast(s) if x != t["id"] and x in by]
    hoi = ("Ảnh minh hoạ 1 cảnh phim. Liệt kê MỌI người nhìn thấy mặt hoặc thân trong ảnh (kể cả người phụ, người mờ phía sau).\n"
           "Toạ độ chuẩn hoá 0–1000 theo bề ngang/bề dọc ảnh (0,0 = góc trên-trái).\n"
           f"NHÂN VẬT CẦN TÌM: {t.get('ten')} ({t.get('tuoi') or '?'} tuổi) — ngoại hình: {_mo_ta(dich, t.get('tuoi'))}\n"
           + "".join(f"Người khác có thể trong cảnh: {c.get('name')} — {_mo_ta(c, t.get('tuoi'))}\n" for c in khac)
           + f"Mô tả cảnh: {str(s.get('ky_vong') or '')[:500]}\n"
           "Đúng 1 người có la_nhan_vat=true (người khớp NHÂN VẬT CẦN TÌM nhất).\n"
           'Trả DUY NHẤT JSON: {"nguoi":[{"ai":"mô tả 5-10 chữ","mat":[x0,y0,x1,y1],"than":[x0,y0,x1,y1],"la_nhan_vat":true}]}')
    try:
        import sol_client
        txt, _ = sol_client.chat(hoi, str(nho), max_tokens=1500, timeout=120)
        m = re.search(r"\{.*\}", txt, re.S)
        ng = json.loads(m.group(0))["nguoi"]
    except Exception as e:
        print(f"  ⚠ vision tìm người cảnh {s.get('n')} lỗi ({type(e).__name__}: {str(e)[:160]}) → neo góc theo profile")
        return None
    finally:
        nho.unlink(missing_ok=True)
    # ảnh phủ kín khung 1920x1080 (object-fit cover) → đổi toạ độ ảnh sang toạ độ khung
    k = max(1920 / W0, 1080 / H0)
    ox, oy = (W0 * k - 1920) / 2, (H0 * k - 1080) / 2

    def box(b):
        return [round(b[0] / 1000 * W0 * k - ox), round(b[1] / 1000 * H0 * k - oy),
                round(b[2] / 1000 * W0 * k - ox), round(b[3] / 1000 * H0 * k - oy)]
    ra = [{"ai": str(p.get("ai") or ""), "mat": box(p["mat"]), "than": box(p.get("than") or p["mat"]),
           "dich": bool(p.get("la_nhan_vat"))} for p in ng if len(p.get("mat") or []) == 4]
    if ra and sum(p["dich"] for p in ra) != 1:
        if len(ra) == 1:
            ra[0]["dich"] = True
        else:
            print(f"  ⚠ vision không chỉ ra đúng 1 người là {t['ten']} ở cảnh {s.get('n')} → neo góc theo profile")
            return None
    cache[khoa] = ra
    cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return ra


def _chong(a, b):
    """Diện tích giao 2 hộp [x0,y0,x1,y1]."""
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def _no(b, r):
    w, h = b[2] - b[0], b[3] - b[1]
    return [b[0] - w * r, b[1] - h * r, b[2] + w * r, b[3] + h * r]


def chon_vi_tri(kt, nguoi, chan=()):
    """kt = (w, h, dx, dy) từ do_khung; nguoi = tim_nguoi; chan = hộp thẻ khác cùng cảnh. Trả ((x, y) #wrap, hộp, điểm).
    Điểm phạt: che mặt ai (nặng nhất) > nằm gần người KHÁC hơn người được giới thiệu > xa mặt người được giới thiệu
    > đè thân người khác > đè thân chính họ. Thẻ phải nằm trên vùng phụ đề."""
    w, h, dx, dy = kt
    dich = next(p for p in nguoi if p["dich"])
    khac = [p for p in nguoi if not p["dich"]]
    tam = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    md = tam(dich["mat"])
    y_max = max(SUB_Y, h + 2 * LE) - h
    tot = None
    for bx in range(LE, 1920 - LE - w + 1, 16):
        for by in range(LE, y_max + 1, 16):
            b = [bx, by, bx + w, by + h]
            c = tam(b)
            # khoảng cách tới MÉP hộp (thẻ to thì tâm xa dù mép sát mặt)
            gan = lambda m: max(0, b[0] - m[2], m[0] - b[2]) + max(0, b[1] - m[3], m[1] - b[3])
            diem = 0.0
            for p in nguoi:
                diem += 4000 * _chong(b, _no(p["mat"], 0.18)) / max(1, (p["mat"][2] - p["mat"][0]) * (p["mat"][3] - p["mat"][1]))
            for o in chan:
                diem += 5000 * (_chong(b, _no(o, 0.04)) > 0)
            g_dich = gan(dich["mat"])
            diem += g_dich / 6
            for p in khac:
                g = gan(p["mat"])
                if g < g_dich + 60:
                    diem += 300 + (g_dich + 60 - g) / 2
                diem += 150 * _chong(b, p["than"]) / (w * h)
            diem += 40 * _chong(b, dich["than"]) / (w * h)
            # ⛔ (anh chốt 18/10, nhấn 2 lần) THẺ PHẢI NẰM SÁT MỘT BÊN, KHÔNG LƠ LỬNG GIỮA KHUNG:
            #    cùng phía ngang với nhân vật (trái/phải) + càng sát mép khung càng tốt. Bỏ hẳn kiểu kéo về
            #    tâm mặt nhân vật (abs(c[0]-md[0])/40 cũ) vì thẻ toàn đáp giữa khung.
            if (c[0] >= 960) != (md[0] >= 960):
                diem += 220                          # khác phía ngang với nhân vật → phạt nặng
            diem += min(b[0], 1920 - b[2]) / 1.2      # (18/10) sát mép: /2.5 quá nhẹ → thẻ đứng cách lề 198px
            # ⛔ (18/10, anh nhấn lần 3) CLIP CÓ PAN/ZOOM → mặt nhân vật TRÔI khỏi vị trí trong ảnh tĩnh,
            #    thẻ đặt ngang tầm đầu sẽ bị mặt trôi vào. Ép thẻ lên SÁT MÉP TRÊN (trên đỉnh đầu) để
            #    dù clip pan dọc thì mặt vẫn không chạm thẻ.
            diem += b[1] / 1.2
            if tot is None or diem < tot[2]:
                tot = ((bx - dx, by - dy), b, diem)
    return tot


def dat_vi_tri(prof, d, cfg, ws):
    """Tính xy cho mọi thẻ chưa neo tay → {id: {"xy":[x,y], "hop":[…], "ly_do":…}}."""
    hd = Path(d) / "hook"
    _, shots = _shots(hd)
    theo_n = {_so(s, i): s for i, s in enumerate(shots)}
    chars = (_doc(Path(d) / "characters.json", {}) or {}).get("characters") or []
    ra, da_dat = {}, {}
    for i, t in enumerate(cfg.get("the") or [], 1):
        tay = _vi_tri_tay(t)
        if tay:
            ra[t["id"]] = {"tay": tay}
            continue
        s = theo_n.get(int(t.get("shot") or -1))
        if not s:
            continue
        html, _ = html_the(prof, dict(t, _i=i), xy=(0, 0))
        kt = do_khung(ws, html)
        nguoi = tim_nguoi(hd, s, t, chars)
        if not nguoi:
            ra[t["id"]] = {"tay": None, "kt": kt, "ly_do": "không tìm được người trong ảnh → neo góc profile"}
            continue
        xy, hop, diem = chon_vi_tri(kt, nguoi, da_dat.get(t["shot"], []))
        da_dat.setdefault(t["shot"], []).append(hop)
        dich = next(p for p in nguoi if p["dich"])
        ra[t["id"]] = {"xy": list(xy), "hop": hop, "kt": kt, "mat_dich": dich["mat"], "diem": round(diem, 1),
                       "so_nguoi": len(nguoi)}
        che = [p["ai"] for p in nguoi if _chong(hop, p["mat"]) > 0]
        print(f"  ⌖ {t['id']}: thẻ {kt[0]}x{kt[1]} đặt ({hop[0]},{hop[1]}) cạnh mặt {dich['mat']} · {len(nguoi)} người trong cảnh"
              + (f" · ⚠ CHE MẶT {che} — soi --snap, cần thì khai vi_tri tay" if che else ""))
    return ra


def thoi_luong(prof, t, shots):
    """Thời lượng thẻ = dur_s khai tay trên thẻ (nếu có), không thì dur_s profile — riêng 3.5 là số --nhap cũ tự ghi
    (không phải anh chọn) → coi như không khai. Có t0/t1 thì cắt cho vừa phần cảnh còn lại sau tre_s; KHÔNG có t0/t1
    (lane nhiều giọng: độ dài cảnh chỉ biết sau TTS) thì xem_thu_hook_giong + ghep_hook_noi_truoc tự cắt ở cuối cảnh
    + mờ dần. Sàn DUNG_TOI_THIEU."""
    tay = float(t.get("dur_s") or 0)
    muon = tay if tay and abs(tay - 3.5) > 0.01 else float(cau_hinh(prof)["dur_s"])
    s = next((x for i, x in enumerate(shots) if _so(x, i) == int(t.get("shot") or -1)), None)
    # (15/10) thẻ giữ tới hết cảnh "giu_den_shot" (luật đóng băng + cảnh đó) → cắt theo t1 cảnh cuối, không theo cảnh đầu
    e = next((x for i, x in enumerate(shots) if _so(x, i) == int(t.get("giu_den_shot") or -1)), None) or s
    if s and s.get("t0") is not None and e.get("t1") is not None:
        muon = min(muon, float(e["t1"]) - float(s["t0"]) - float(t.get("tre_s") or 0) - 0.1)
    return round(max(DUNG_TOI_THIEU, muon), 2)


def _cfg_thuc(prof, d, cfg):
    _, shots = _shots(Path(d) / "hook")
    return dict(cfg, the=[dict(t, dur_s=thoi_luong(prof, t, shots)) for t in cfg.get("the") or []])


def render(prof, d, chi=None, snap=False):
    d = Path(d)
    hd = d / "hook"
    cfg = _doc(hd / "the_ten.json")
    if not cfg:
        raise SystemExit(f"✗ chưa có {hd / 'the_ten.json'} → chạy --nhap trước")
    cfg = _cfg_thuc(prof, d, cfg)
    for t in cfg["the"]:
        print(f"  ⏱ {t['id']}: hiện {t['dur_s']}s (đọc yên ~{max(0, t['dur_s'] - 1.6):.1f}s)"
              + ("  ⚠ cảnh ngắn → thẻ bị cắt; muốn lâu hơn: khai nghi_doan_sau cho cảnh này" if t["dur_s"] < cau_hinh(prof)["dur_s"] - 0.05 else ""))
    ws = _ws(hd)
    (hd / "the_ten").mkdir(exist_ok=True)
    vt = dat_vi_tri(prof, d, cfg, ws)
    (hd / "the_ten" / "_vi_tri.json").write_text(json.dumps(vt, ensure_ascii=False, indent=1), encoding="utf-8")
    _, shots = _shots(hd)
    theo_n = {_so(s, i): s for i, s in enumerate(shots)}
    for i, t in enumerate(cfg.get("the") or [], 1):
        if chi and t["id"] not in chi:
            continue
        xy = (vt.get(t["id"]) or {}).get("xy")
        nen = ""
        if snap:   # soi trên CHÍNH ảnh cảnh để thấy thẻ có che mặt / có nằm cạnh đúng người không
            anh = _anh_shot(hd, theo_n.get(int(t.get("shot") or -1)) or {})
            if anh:
                shutil.copy2(anh, ws / "assets" / "nen.png")
                nen = "assets/nen.png"
        s, dur = html_the(prof, dict(t, _i=i), nen=nen, xy=xy)
        (ws / "index.html").write_text(s, encoding="utf-8")
        npx(ws, "check")
        if snap:
            shutil.rmtree(ws / "snapshots", ignore_errors=True)
            npx(ws, "snapshot", "--at", f"{min(1.9, dur - 0.6):.2f}", "--no-end", "--describe", "false")
            png = sorted((ws / "snapshots").glob("*.png"))[0]
            dst = hd / "the_ten" / f"soi_{t['id']}.png"
            shutil.copy2(png, dst)
            (ws / "assets" / "nen.png").unlink(missing_ok=True)
            print(f"  📷 {t['id']}: {dst}")
            continue
        out = hd / "the_ten" / f"the_{t['id']}.webm"
        npx(ws, "render", "--format", "webm", "--fps", str(FPS), "-q", "delivery", "-o", str(out))
        print(f"  ✓ {out} ({dur}s)")
    if not snap:
        ghi_timeline(d, cfg, vt)


def _theo_shot(cfg):
    g = {}
    for t in cfg.get("the") or []:
        if t.get("shot") is not None:
            g.setdefault(int(t["shot"]), []).append(t)
    return g


def _file_shot(ts):
    return f"the_ten/the_{'__'.join(t['id'] for t in ts)}.webm"


def gop_webm(hd, ts):
    """2 thẻ cùng cảnh → 1 webm alpha (timeline 1 shot chỉ chứa 1 thẻ): mỗi thẻ trễ đúng tre_s của nó."""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    dur = max(float(t.get("tre_s") or 0) + float(t.get("dur_s") or 3.5) for t in ts) + 0.1
    ins, fl, cur = [], [f"color=c=black@0.0:s=1920x1080:r={FPS}:d={dur:.2f},format=yuva420p[b0]"], "[b0]"
    for j, t in enumerate(ts):
        ins += ["-c:v", "libvpx-vp9", "-i", str(hd / "the_ten" / f"the_{t['id']}.webm")]
        fl.append(f"[{j}:v]format=yuva420p,setpts=PTS-STARTPTS+{float(t.get('tre_s') or 0):.3f}/TB[t{j}];"
                  f"{cur}[t{j}]overlay=0:0:eof_action=pass:format=auto[b{j + 1}]")
        cur = f"[b{j + 1}]"
    out = hd / _file_shot(ts)
    r = subprocess.run([ff, "-y", "-v", "error", *ins, "-filter_complex", ";".join(fl), "-map", cur, "-t", f"{dur:.2f}",
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "28", "-auto-alt-ref", "0", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"✗ gộp thẻ {out.name} lỗi: {r.stderr[-800:]}")
    print(f"  ✓ gộp {len(ts)} thẻ cùng cảnh → {out}")


def ghi_timeline(d, cfg, vt=None):
    hd = Path(d) / "hook"
    tl, shots = _shots(hd)
    g = _theo_shot(cfg)
    for n, ts in g.items():
        if len(ts) > 1:
            gop_webm(hd, ts)
    for i, s in enumerate(shots):
        ts = g.get(_so(s, i))
        if ts:
            s["the_ten"] = {"id": ",".join(t["id"] for t in ts), "file": _file_shot(ts),
                            "tre_s": 0.0 if len(ts) > 1 else float(ts[0].get("tre_s") or 0),
                            # dấu vết bản đặt-vị-trí-tự-động (10/10): thiếu = thẻ render bằng bản cũ cố định góc
                            "vi_tri": {t["id"]: ((vt or {}).get(t["id"]) or {}).get("xy")
                                       or ((vt or {}).get(t["id"]) or {}).get("tay") or "goc" for t in ts}}
            # 2026-10-12 (anh chốt Lane L ep15): thẻ bật ở cảnh ĐÓNG BĂNG rồi GIỮ tới hết cảnh nhân vật nói ngay sau
            # (thời gian thẻ = đóng băng + cảnh đó) → khai "giu_den_shot": <số cảnh cuối> trên thẻ (the_ten.json).
            den = max(int(t.get("giu_den_shot") or 0) for t in ts)
            if den:
                s["the_ten"]["den_shot"] = den
        else:
            s.pop("the_ten", None)
    (hd / "hook_timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ ghi the_ten vào {hd / 'hook_timeline.json'} ({len(g)} cảnh)")


# ───────────────────────────── cổng ─────────────────────────────
def loi_gioi_thieu(text, cho_phep=()):
    """Câu KỂ (ngoài「」) giới thiệu nhân vật bằng tên-tuổi → phải chuyển lên thẻ tên."""
    ke = re.sub(r"「[^」]*」", "。", text)
    ra = []
    for cau in re.split(r"[。\n]", ke):
        cau = cau.strip()
        if cau and not any(cau in x or x in cau for x in cho_phep) and any(p.search(cau) for p in LOI_GIOI_THIEU):
            ra.append(cau)
    return ra


def kiem(prof, d):
    if not is_enabled(prof):
        return []
    d = Path(d)
    hd = d / "hook"
    loi = []
    cfg = _doc(hd / "the_ten.json") or {}
    if not cfg:
        loi.append(f"thiếu {hd / 'the_ten.json'} (chạy --nhap)")
    the = {t["id"]: t for t in cfg.get("the") or []}
    bo = cfg.get("bo_qua") or {}
    for c, _ in nhan_vat_chinh(d):
        if c["id"] not in the and c["id"] not in bo:
            loi.append(f"nhân vật chính '{c['id']}' ({_ten_rieng(c)}) chưa có thẻ tên (hoặc ghi bo_qua kèm lý do)")
    _, shots = _shots(hd)
    gan = {x for s in shots for x in str((s.get("the_ten") or {}).get("id") or "").split(",") if x}
    lan_dau = {}
    for i, s in enumerate(shots):
        for x in _cast(s):
            lan_dau.setdefault(x, _so(s, i))
    for k, t in the.items():
        # 2026-10-12 (anh chốt Lane L ep15): anh chỉ định thẻ bật ở cảnh ĐÓNG BĂNG giới thiệu riêng (sau/trước câu thoại),
        # không phải cảnh hiện mặt đầu tiên → khai "anh_chi_dinh_canh": "<lý do>" trên thẻ đó (chỉ khi anh yêu cầu).
        if k in lan_dau and int(t.get("shot") or -1) != lan_dau[k] and not t.get("anh_chi_dinh_canh"):
            loi.append(f"thẻ '{k}' gắn cảnh {t.get('shot')} nhưng ảnh nhân vật hiện LẦN ĐẦU ở cảnh {lan_dau[k]} → thẻ phải "
                       f"bật ngay cảnh {lan_dau[k]} (cấm dời về sau/cảnh 「これは…の話だ」 cuối hook)")
        f = hd / "the_ten" / f"the_{k}.webm"
        if not f.exists():
            loi.append(f"chưa render thẻ {f}")
        elif f.stat().st_mtime < (hd / "the_ten.json").stat().st_mtime:
            loi.append(f"thẻ {f.name} CŨ hơn the_ten.json → render lại")
        if k not in gan:
            loi.append(f"thẻ '{k}' chưa gắn vào shot nào trong hook_timeline.json")
        if thoi_luong(prof, t, shots) < DUNG_TOI_THIEU:
            loi.append(f"thẻ '{k}' hiện < {DUNG_TOI_THIEU}s (người xem lớn tuổi đọc không kịp)")
        f_ = hd / "the_ten" / f"the_{k}.webm"
        if f_.exists():
            import imageio_ffmpeg
            co = imageio_ffmpeg.count_frames_and_secs(str(f_))[1]
            if co < thoi_luong(prof, t, shots) - 0.15:
                loi.append(f"thẻ {f_.name} dài {co:.1f}s < {thoi_luong(prof, t, shots)}s cần có → render lại (thẻ cũ hiện quá ngắn)")
    for s in shots:
        if s.get("the_ten") and "vi_tri" not in s["the_ten"]:
            loi.append(f"thẻ cảnh {_so(s, 0) if s.get('n') else '?'} render bằng bản cũ (khung cứng + cố định 1 góc) → render lại "
                       "để thẻ ôm vừa chữ + đặt cạnh đúng nhân vật")
        f = (s.get("the_ten") or {}).get("file")
        if f and not (hd / f).exists():
            loi.append(f"hook_timeline.json trỏ tới thẻ chưa có {hd / f} → render lại")
    loi += kieu_trung(prof)
    # (anh sửa 14/10) hook ĐƯỢC đọc tên-tuổi song song thẻ tên → không còn chặn câu giới thiệu (loi_gioi_thieu giữ để tham khảo)
    return loi


def kieu_trung(prof):
    """LUẬT (anh chốt 10/10): mỗi lane 1 kiểu motion thẻ tên RIÊNG — trùng lane khác / lấy kiểu giữ chỗ → lỗi."""
    import profiles
    k = cau_hinh(prof)["kieu"]
    loi = []
    if GIU_CHO.get(k) and GIU_CHO[k] != prof.get("id"):
        loi.append(f"kiểu thẻ '{k}' đã giữ chỗ cho lane {GIU_CHO[k]} — chọn kiểu khác/thêm kiểu mới")
    for pid in profiles.list_ids():
        if pid == prof.get("id") or pid.startswith(("_", "zz-")):
            continue
        try:
            p = profiles.load(pid)
        except Exception:
            continue
        if is_enabled(p) and cau_hinh(p)["kieu"] == k:
            loi.append(f"kiểu thẻ '{k}' TRÙNG lane {pid} — mỗi lane 1 kiểu motion riêng (thêm kiểu mới vào KIEU)")
    return loi


def cong(prof, d, buoc):
    loi = kiem(prof, d)
    if loi:
        raise SystemExit(f"✗ {buoc}: THẺ TÊN NHÂN VẬT hook chưa đạt (docs/QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md):\n  - "
                         + "\n  - ".join(loi) + f"\n  → py -3.13 -X utf8 {HERE / 'the_ten_hook.py'} --profile {prof['id']} --slug {Path(d).name}")


def mau(prof, nen=None):
    """Ảnh mẫu kiểu thẻ của lane (soi trước) → docs/the_ten_mau/<lane>.png (+ .webm)."""
    c = cau_hinh(prof)
    import tempfile
    out = ROOT / "docs" / "the_ten_mau"
    out.mkdir(parents=True, exist_ok=True)
    ws = _ws(Path(tempfile.gettempdir()) / f"the_ten_mau_{prof['id']}")
    t = dict({"ten": "相葉 渉", "kana": "あいば わたる", "tuoi": 36, "nghe": "地元の電気工事士", "chip": c.get("chip_mac_dinh") or ""},
             **(c.get("vi_du") or {}))
    src = ""
    if nen:
        shutil.copy2(nen, ws / "assets" / "nen.png")
        src = "assets/nen.png"
    s, dur = html_the(prof, dict(t, _i=1), nen=src)
    (ws / "index.html").write_text(s, encoding="utf-8")
    npx(ws, "check")
    shutil.rmtree(ws / "snapshots", ignore_errors=True)
    npx(ws, "snapshot", "--at", f"{min(2.0, dur - 0.6):.2f}", "--no-end", "--describe", "false")
    png = sorted((ws / "snapshots").glob("*.png"))[0]
    dst = out / f"{prof['id']}_{c['kieu']}.png"
    shutil.copy2(png, dst)
    print(f"  ✓ {dst}")
    return dst


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    import profiles
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile")
    ap.add_argument("--kieu", help="--mau cho lane CHƯA có profile: kiểu thẻ (kèm --mau-chinh/--mau-phu/--vi-tri)")
    ap.add_argument("--mau-chinh", default="#b5536b")
    ap.add_argument("--mau-phu", default="#f2c6d0")
    ap.add_argument("--vi-tri", default="tren_trai")
    ap.add_argument("--slug")
    ap.add_argument("--nhap", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--snap", action="store_true")
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--mau", action="store_true")
    ap.add_argument("--nen", help="--mau: ảnh nền 1920x1080 để soi")
    ap.add_argument("--chi", nargs="*", help="chỉ render các id này")
    a = ap.parse_args(argv)
    if a.mau and a.kieu:
        prof = {"id": a.profile or "_thu", "script": {"hook": {"the_ten": {
            "bat": True, "kieu": a.kieu, "mau": a.mau_chinh, "mau_phu": a.mau_phu, "vi_tri": a.vi_tri}}}}
    elif not a.profile:
        raise SystemExit("✗ cần --profile")
    else:
        prof = profiles.load(a.profile)
    if a.mau:
        mau(prof, a.nen)
        return
    if not a.slug:
        raise SystemExit("✗ cần --slug")
    import review_may3
    d = review_may3.thu_muc_tap(prof, a.slug)
    if not is_enabled(prof):
        print(f"  (lane {prof['id']} chưa bật script.hook.the_ten.bat)")
    if a.nhap:
        nhap(prof, d, force=a.force)
    elif a.kiem:
        loi = kiem(prof, d)
        print("✓ thẻ tên đạt" if not loi else "✗ " + "\n✗ ".join(loi))
        sys.exit(1 if loi else 0)
    else:
        render(prof, d, chi=a.chi, snap=a.snap)


if __name__ == "__main__":
    main()
