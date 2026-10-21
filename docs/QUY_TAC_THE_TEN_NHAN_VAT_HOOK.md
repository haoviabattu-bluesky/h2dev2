# ⛔ QUY TẮC THẺ TÊN ĐỘNG — giới thiệu nhân vật chính trong HOOK bằng motion graphics (anh chốt 10/10/2026, MỌI lane)

> Gốc: anh chê hook ep05 Lane O "dài dòng loằng ngoằng" vì đọc 「二十歳の新人、菊池美羽は…」. Ngày 10/10 anh chốt cho mọi lane:
> **hook KHÔNG đọc câu giới thiệu "ông X, xx tuổi, nghề Y" nữa** — thông tin đó hiện bằng **thẻ tên động** (motion graphics)
> trên hình lúc nhân vật xuất hiện. Nội dung thẻ lấy đúng khuôn Lane L đang đọc (「相葉渉、36歳。地元の…電気工事士だ。」) nhưng đưa lên hình.
> Mỗi lane 1 kiểu thẻ riêng. BẮT BUỘC cho nhân vật chính; nhân vật phụ không quan trọng thì bỏ qua.

> ⛔ **SỬA 14/10/2026 (anh chốt, MỌI lane): hook ĐƯỢC ĐỌC tên + tuổi (+ nghề) nhân vật chính, và thẻ tên động chạy SONG SONG**
> — người xem vừa thấy vừa nghe. Luật 1 cũ (cấm đọc) HẾT HIỆU LỰC; cổng `loi_gioi_thieu()` đã gỡ khỏi `the_ten_hook.kiem()`.
> Các luật thẻ (bắt buộc có thẻ, bật ngay cảnh hiện lần đầu, đóng băng, mỗi lane 1 kiểu) GIỮ NGUYÊN.

## 1. Luật
1. **(sửa 14/10) Lời hook ĐƯỢC đọc câu giới thiệu** tên-tuổi(-nghề), vd 「相葉渉、36歳。」「佐久間秀夫、62歳。経理一筋40年。」:
   1 câu ngắn, đặt ĐÚNG lúc nhân vật hiện lần đầu (khớp lúc thẻ bật), không đọc cả lý lịch dài. Thẻ tên vẫn bắt buộc, chạy song song.
   (Bản 10/10 từng cấm đọc — bỏ.)
2. **Nhân vật chính PHẢI có thẻ.** Máy tính "chính" = có tên riêng + có REF + (`main` trong characters.json | có thoại「」
   trong hook | xuất hiện ≥3 cảnh hook). Người không tên riêng (「窓口の同僚」「面会の家族」), không REF, vai lướt qua → bỏ qua.
   Máy bắt nhầm người phụ → ghi `bo_qua: {"id": "lý do"}`. Tối đa ~4 thẻ/hook (`toi_da`); nhiều hơn = hook quá nhiều người.
3. **Nội dung thẻ:** tên đầy đủ (Họ␣Tên, cách 1 dấu cách) · cách đọc kana (nên có, người xem lớn tuổi) · tuổi (CHỈ khi biết —
   không bịa; Lane I lịch sử dùng tuổi tại thời điểm cảnh hoặc bỏ) · nghề/vai ≤18 chữ, cụ thể (「勤続19年の介護福祉士」 tốt hơn 「職員」) ·
   chip tuỳ chọn (「主人公」「教育担当」「新人 ②」「語り手」). Người thay thế ghi rõ thay ai (「美羽の後任の新人」).
4. ⛔ **Thời điểm (anh chốt 10/10): thẻ bật NGAY cảnh ảnh nhân vật hiện LẦN ĐẦU trong hook** (= shot đầu tiên có id trong `cast`).
   CẤM để tới gần cuối hook, ở cảnh tổng kết 「これは、…の話だ」 (đây là câu chuyện của…) mới đưa thẻ ra — người xem phải biết
   ai là ai ngay lúc thấy mặt. Cổng so `shot` của thẻ với cảnh xuất hiện đầu, lệch là CHẶN. Cảnh đầu nhân vật chỉ thấy lưng/nhỏ
   → sửa ảnh/thứ tự cảnh cho họ hiện rõ ở cảnh đầu, không dời thẻ. 2 nhân vật chính cùng hiện lần đầu 1 cảnh → 2 thẻ cùng cảnh
   (máy tự cho thẻ thứ 2 sang bên kia, trễ 0,6s, gộp 1 file `the_<a>__<b>.webm`); ≥3 người → tách cảnh.
   ⛔ (anh chê 10/10: hiện ngắn quá) Mặc định **6s** (profile `dur_s: 6.0`; 3,5s cũ chỉ ~2s đứng yên đọc được vì bung ~1,1s +
   rút ~0,45s). Máy lấy max(dur_s thẻ, dur_s profile) rồi CẮT cho vừa cảnh (`thoi_luong`: không trôi sang cảnh người khác),
   sàn 3s; render in `⏱ hiện Xs (đọc yên ~Ys)`. Cảnh ngắn làm thẻ bị cắt → khai `nghi_doan_sau` cho ảnh lặng 1–2s (mẫu Lane O
   ep05). Cổng chặn webm ngắn hơn thời lượng cần có (thẻ render trước 10/10 tối).
5. ⛔ **Thẻ ÔM VỪA CHỮ + đặt CẠNH ĐÚNG người (anh chốt 10/10, ảnh ep13 Lane F).** (a) Cấm khung rộng cố định — mọi kiểu
   trong `KIEU` dựng bằng flex/padding, `#wrap` = max-content: tên 3 chữ thì thẻ ngắn, không để dải màu trống. Kiểu mới
   cũng phải vậy (phần tử absolute chỉ làm nền/trang trí bám `inset`). (b) Cấm cố định 1 góc: khi render, máy lấy khung giây
   ~1,2 của clip cảnh (chưa có clip → ảnh cảnh), hỏi vision (`sol_client`) mặt + thân mọi người, người nào là nhân vật của
   thẻ, đo kích thước thẻ thật bằng Chrome, rồi chọn chỗ: KHÔNG che mặt ai · gần mặt nhân vật được giới thiệu HƠN mặt người
   khác · cùng phía với họ · trên vùng phụ đề (y<760) · không đè thẻ thứ 2 cùng cảnh (`chon_vi_tri`). Kết quả:
   `hook\the_ten\_vi_tri.json`, cache vision `hook\the_ten\_nguoi.json`; timeline ghi `the_ten.vi_tri`. Soi bằng `--snap`
   → `hook\the_ten\soi_<id>.png` (thẻ trên khung clip thật). Vision sai/lỗi → khai tay trên thẻ đó
   `"vi_tri": "tren_trai"|"tren_phai"|[x, y]` (px góc trên-trái). Thẻ render bằng bản cũ (không có `the_ten.vi_tri`) → cổng CHẶN.
   Kẻ gây chuyện có thể đổi màu riêng (`"mau": "#c1121f"`).
6. ⛔ **Mỗi lane 1 kiểu motion RIÊNG (anh chốt 10/10)** — khác LAYOUT + CHUYỂN ĐỘNG, không chỉ khác màu. Cấm 2 lane dùng
   chung 1 `kieu`; kiểu đã giữ chỗ cho lane chưa có profile (`GIU_CHO`: `tategaki`→I, `vong_song`→H) cũng không được lấy.
   Cổng `kieu_trung()` quét mọi profile, trùng là CHẶN. Lane mới → thêm kiểu MỚI vào `KIEU` (`pipeline\the_ten_hook.py`),
   soi bằng `--mau`, rồi thêm 1 dòng vào bảng §2.

7. ⛔ **ĐÓNG BĂNG 2–3 giây + thẻ GIỮ HẾT CẢNH (anh chốt 12/10/2026, Lane L ep15, MỌI lane).** Nhân vật chính hiện → hình
   **ĐÓNG BĂNG 2–3s** (mặc định 3s) để giới thiệu, thẻ bật trong lúc đóng băng; **thời gian thẻ = thời gian đóng băng + thời gian
   cảnh nhân vật đó** (thẻ KHÔNG tắt khi hết đóng băng, giữ tới hết cảnh nhân vật đó nói, sang cảnh khác mới tắt).
   - Đóng băng TRƯỚC câu nói (kiểu さくら/浅見/三國 ep15) = shot LẶNG `"lang_s": 3.0` ngay trước shot có lời, clip = khung ĐẦU
     của clip shot nói (ảnh tĩnh, `img/NNN.png` = khung đó). Đóng băng SAU câu đầu (kiểu 小坂 mở hook) = shot lặng ngay sau, clip =
     khung tĩnh ~cuối câu của clip trước. Máy 2 tự chèn đúng khoảng lặng vào giọng thân (`cau_vai.lang_hook`).
   - Trên thẻ (`the_ten.json`): `"shot"` = cảnh đóng băng, `"giu_den_shot"` = cảnh cuối của nhân vật, `"dur_s"` ≥ tổng 2 cảnh
     (đặt 12), `"anh_chi_dinh_canh"` = lý do (cổng luật 4 cho phép thẻ ở cảnh đóng băng thay vì cảnh hiện mặt đầu).
     `the_ten_hook.py` ghi `den_shot` vào timeline; `xem_thu_hook_giong.py` + `ghep_hook_noi_truoc.py` (máy 2) giữ thẻ tới hết cảnh đó.
   - Soi khung TRONG SUỐT thời gian thẻ (cả cảnh nói sau đóng băng), không chỉ khung đóng băng: thẻ không che mặt ai.
   - Mẫu chạy thật: `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep15-tedori-heru\hook\_mk_hook2.py` + `hook\the_ten.json`.
   - Bẫy (đo thật 12/10): chồng ≥3 thẻ trong CÙNG 1 lệnh ffmpeg → thẻ muộn không hiện/ffmpeg treo → 2 tool đã đổi sang chồng từng thẻ 1 lượt.

## 2. Kiểu thẻ từng lane (profile `script.hook.the_ten`; khác biệt lane CHỈ qua field này — 11 lane = 11 kiểu khác nhau)
| Lane | Mã | Kiểu (`kieu`) | Màu chính / phụ | Chất |
|---|---|---|---|---|
| O 介護スカッと | `kaigo-sukatto` | `vach_cheo` | #14806f / #e9c46a | hộp tối + vệt chéo quét + huy hiệu tuổi tròn bật, vệt sáng lướt |
| L 社会のなぜ研究室 | `shakai_no_naze` | `ho_so` | #1d3557 / #c1121f | tờ hồ sơ điều tra rơi xuống, tên gõ từng nhịp, dấu đỏ tuổi đóng "cộp" |
| K 薬局スカッと帳 | `yakkyoku-sukatto` | `bang_ten` | #1f8a8a / #e4572e | bảng tên đeo ngực 名札 có kẹp, đung đưa rơi xuống |
| F 定年後のリアル | `teinengo-real` | `ban_tin` | #1f4e79 / #d9480f | telop bản tin 2 tầng, thanh quét, ô tuổi lật |
| G 定年後の楽しみ方 | `teinengo-tanoshimi` | `giay_note` | #ffe680 / #d6336c | giấy nhớ 付箋 dán băng keo, vòng tròn tuổi khoanh bút |
| N シニアの人生これから | `senior_korekara` | `ruy_bang` | #c8553d / #ffd166 | ruy băng mở ngang + huy chương tuổi xoay vào |
| M 定年後の穴場ノート | `teinengo-anaba` | `mem` | #2b7bb9 / #bfe3ff | thẻ tròn mềm, chấm tròn chữ đầu họ, bật nhẹ |
| J 定年後の夫婦のカタチ | `teinengo-fuufu` | `net_manh` | #c08552 / #f6d7a7 | nét kẻ mảnh vẽ ra, tên Minchō trồi lên sau nét kẻ |
| Satori người già | `satori-jp-obaa` | `cuon_thu` | #7b4fa0 / #f1d9a6, `tren_phai` | cuộn thư 巻物: 2 trục gỗ, giấy washi mở ra, tên Minchō hiện từ nhoè, nét cọ gạch dưới |
| H 心の家族学 | `kokoro-kazoku` | `vong_song` (GIỮ CHỖ) | #b5536b / #f2c6d0 | đĩa tròn mờ nở ra, 2 vòng gợn lan, tên giữa — khai khi lane có profile |
| I 戦国の裏側 | `sengoku-uragawa` | `tategaki` (GIỮ CHỖ) | #d4af37 / #9b1c1c, `tren_phai` | chữ dọc, dải mực, nét cọ đỏ, ấn triện — khai khi lane có profile |

Ảnh mẫu từng kiểu: `E:\CLAUDE\YOUTUBE\h2dev\docs\the_ten_mau\TONG_HOP_KIEU_THE_TEN.jpg` (+ từng file `<lane>_<kieu>.png`).
Field: `{"bat": true, "kieu", "mau", "mau_phu", "vi_tri": "tren_trai|tren_phai", "dur_s": 6.0, "toi_da": 4, "chip_mac_dinh"?}` — `vi_tri` profile giờ chỉ là DỰ PHÒNG khi vision không tìm được người (luật 5b).
Lane mới: BẮT BUỘC kiểu chưa lane nào dùng/giữ chỗ (luật 6) — thêm kiểu mới vào `KIEU` trong `pipeline\the_ten_hook.py`, soi bằng `--mau`.
Lopezzapa68 (ngôi 1, không hook kể chuyện) không áp dụng.

## 3. Quy trình (máy 1, sau khi có clip hook, TRƯỚC clip xem thử — `docs\NHAN_KICH_BAN_MAY3.md` §5)
```bat
:: 1) nháp thẻ từ characters.json + hook_timeline.json → <tập>\hook\the_ten.json (sửa tay: Họ␣Tên, kana, nghề, chip, bo_qua)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập> --nhap
:: 2) render webm VP9 alpha → <tập>\hook\the_ten\the_<id>.webm + tự ghi shot "the_ten" vào hook_timeline.json (~20s/thẻ)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập>
:: 3) cổng (duyet_hook --gui cũng tự chạy)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\the_ten_hook.py --profile <lane> --slug <tập> --kiem
```
Rồi dựng clip xem thử (`xem_thu_hook_giong.py` tự chồng thẻ) → trích khung soi thẻ không che mặt, chữ đúng → `duyet_hook.py --gui`.
Máy 2: `ghep_hook_noi_truoc.py` tự chồng; `dong_goi_may2` gửi kèm `hook\the_ten\`. Máy 2 KHÔNG tự làm thẻ.

Hook đã khoá còn câu giới thiệu (bản anh sửa trước 10/10, hoặc anh viết lại) → bỏ câu đó khỏi lời hook (`hook_locked.txt`
+ đầu `script.txt` + `vai.txt`) rồi khoá lại như `docs\NHAN_KICH_BAN_MAY3.md` §1; ghi `bo câu` vào HOC_BAN_SUA.md của tập.

## 4. Cổng (máy chặn, không dựa trí nhớ)
- `hook_stage.check()`: lane bật `the_ten` → ứng viên hook có câu giới thiệu = việc phải sửa (patch/khóa lại).
- Prompt viết hook (Fable): khối `KHOI_THE_TEN` chỉ lo chuyện giới thiệu tên-tuổi; sườn hook theo luật 17/10 `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md` (style_rules/hook mẫu cũ đã xoá).
- `duyet_hook.py --gui` → `the_ten_hook.cong()`: thiếu thẻ nhân vật chính / thẻ chưa render / cũ hơn the_ten.json / chưa gắn shot
  / **thẻ không ở cảnh ảnh nhân vật hiện lần đầu** / hiện <3s / **kiểu thẻ trùng lane khác** / lời hook còn câu giới thiệu → DỪNG. Thẻ mới hơn clip xem thử → bắt dựng lại clip xem thử.
