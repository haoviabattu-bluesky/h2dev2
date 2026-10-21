# LANE F `teinengo-real` — BẮT ĐẦU TẬP 8 `ep08-kodomo-enjo` (viết 2026-09-30, sau khi giao tập 7)

> ⭐ **2026-09-30 anh chốt — THẮNG mọi chỉ dẫn soát ChatGPT web bên dưới:** hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`);
> `make_video --den B3G` khoá xong là DỪNG, tự giao máy 3/anh soát (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) →
> đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` để nhận + làm hook/ảnh/giao máy 2.


> **Cách dùng (anh):** mở tab chat mới, dán đúng 1 dòng:
> `Làm tập 8 lane F theo hướng dẫn ở cột K dòng 9 tab F-teinengo-real`
> (hoặc dán thẳng đường dẫn file này).
>
> **Tab mới (Claude):** mở đầu báo cáo bằng `@lane:teinengo-real`. Đọc HẾT file này rồi đọc HẾT runbook chung
> `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real_TAP_TIEP.md` (các bước A→I + luật cứng mục 1 + bẫy mục 3 + điểm dừng mục 4).
> Làm theo runbook với `<SLUG>` = `ep08-kodomo-enjo`, dòng sheet = **9**. File NÀY chỉ ghi những gì RIÊNG tập 8 và chỗ khác tập 7.
> Không dừng hỏi giữa chừng trừ 3 điểm dừng của runbook.

## 0. THAM SỐ
| | |
|---|---|
| Thư mục `<D>` | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep08-kodomo-enjo` |
| Dòng sheet | 9 (tab `F-teinengo-real`) — D9 đang "Chờ check kịch bản", H9/K9 trống lúc viết |
| Tiêu đề (`title.txt`) | 【漫画】60歳で辞めた元課長…息子夫婦への援助で退職金1500万円が3年で300万円に (cựu trưởng phòng nghỉ lúc 60… vì giúp vợ chồng con trai, 15 triệu yên tiền thôi việc còn 3 triệu sau 3 năm) |
| Kịch bản | LOCK PASS 27/09 (Sol 2 lượt PASS, 0 patch), **6.724 chữ ≈ 23,7'** — sát trần ngân sách (~6.250 ±8% = 6.750): sửa phải làm NGẮN đi |
| Hook đã khoá | 「父さん、あの金、申告しなくていいの」… (Bố ơi, khoản tiền đó không phải khai báo sao…) — mở bằng thoại con trai; tuổi trong hook không được khác 60 |
| Nhân vật (đọc từ `script.txt`) | 俺 (cựu 課長, sống ở 高崎 Takasaki), vợ 千恵 (Chie), con trai 悠介 (Yūsuke, 32, ở 前橋 Maebashi), con dâu 沙織 (Saori), cháu 陽菜 (Hina, 3 tuổi — trẻ em: đọc memory content-policy trẻ em trước khi vẽ), đồng kỳ đối lập 柴田 (Shibata, ở lại công ty), 山根 (Yamane, bố của con dâu, đi xe Lexus) |

## 1. KHÁC TẬP 7 — phải làm thêm
1. **Chưa có `hook\hook_storyboard.json` và `hook\grok_jobs.csv`** (tập 7 có sẵn). Ở bước G.1 chạy
   `py -3.13 -X utf8 pipeline\hook_storyboard.py --profile teinengo-real --slug ep08-kodomo-enjo` (thêm `--force` nếu bước D đổi hook).
2. **Hook mở bằng câu thoại 「…」**: bước G.3 gán cue theo đúng ranh giới câu; ảnh shot 1 là 俺 cầm điện thoại nghe (mặt to, ngạc nhiên),
   KHÔNG vẽ con trai nói (thoại là giọng qua điện thoại).
3. **Số chế độ thuế là số THẬT** (khác tập 7 chỉ có thống kê): chỉ được dùng 110万円 · 1,000万円 · 500万円 · 令和8年12月31日 (xem `<D>\series_ctx.txt`
   [D1]–[D3]). Không nêu số thuế phải nộp cụ thể, không tư vấn thuế cho người xem.

## 2. ĐIỂM SOI KHI THẨM ĐỊNH GPT (bước C) + LỚP 3 (bước E) — riêng tập 8
- **Sổ tiền:** 1.500万 → ~300万 phải cộng khớp đúng 3 khoản cho con (đặt cọc nhà · học phí mẫu giáo cháu · tiền cưới) + sinh hoạt. Tự cộng lại
  trước khi nhận/phản biện góp ý của GPT (bài học tập 7: dự toán ghi "150万ほど" nhưng các mốc cộng ra 162万).
- **Rủi ro sai thuế dễ bị GPT bắt:** ở Nhật, tiền cha mẹ trả TRỰC TIẾP chi phí cưới/học phí "ở mức cần thiết thông thường" thường không bị
  贈与税 (thuế tặng cho); khoản bị vướng là **đưa 1 cục TIỀN MẶT lớn** vượt 110万/năm. Nếu GPT nói tiền đám cưới không chịu thuế → NHẬN hướng
  sửa câu chữ cho rõ "đưa 1 lần 1 cục tiền mặt vào tài khoản con, con tự tiêu" (giữ cú tát của tiền đề), KHÔNG đổi tiền đề.
  Nếu GPT đòi bỏ hẳn cú tát thuế → đây là **điểm dừng 3** (chạm thiết kế tập) — hỏi anh bằng 1 quyết định kèm khuyến nghị.
- **Chế độ nhà ở [D2]:** chỉ áp cho tiền MUA/XÂY/SỬA nhà và cần khai báo đúng thủ tục; 柴田 làm đúng thủ tục, 俺 thì không — kiểm bài không
  nói sai điều kiện (vd "nhà thường 1.000万" là sai, nhà thường là 500万).
- **Trùng ý tập trước:** kết bài 俺 đi làm **駐輪場 (bãi giữ xe đạp) của thành phố** — tập 6 cũng kết bằng việc trông bãi xe đạp buổi sáng.
  Nếu GPT hoặc lớp 3 thấy trùng → đổi việc nhẹ khác qua viec_tay (vd dọn dẹp/quản lý toà nhà, hướng dẫn xe ở siêu thị), giữ nguyên số tiền
  lương 6万/tháng để không vỡ sổ.
- Vợ 千恵 "không phải trọng tâm truyện" — nếu GPT muốn thêm tuyến vợ dài → phản biện, chỉ giữ ở mức 1–2 cảnh.

## 3. NHẮC LẠI BẪY VỪA GẶP Ở TẬP 7 (đã ghi ở runbook mục 3)
- viec_tay > ~9–10 việc một lượt → cổng từ chối (đổi >40% đoạn). Nhiều việc thì chia 2 lượt ngay từ đầu.
- Viết `HOOK_TAP.md` bằng Python: không nối chuỗi `rf"…" "…\006"` — ghép bằng `+` với mảnh `r"…"`, rồi kiểm không còn ký tự điều khiển.
- Storyboard đòi "cận tay / cận cực sát mắt" trái luật mặt to → sửa `ky_vong` + prompt Grok cho khớp ảnh; clip chỉ lệch chi tiết tay → duyệt tay.
- B5P WARN: sửa tay đúng dòng trong `img_prompts.txt` (backup trước); chạy lại `--only B5P` sẽ bị bỏ qua, không cần ép.

## 4. XONG THÌ
- Làm hết bước H + I của runbook (D9 = Done, H9 = cần ảnh do tool ghi).
- Sửa bảng mục 0 của runbook chung: dòng tập 8 → "✅ ĐÃ GIAO MÁY 2 <ngày>".
- Viết file hướng dẫn tập 9 theo khuôn file này (`teinengo-real_TAP09.md`) + ghi đường dẫn vào **K10** (chỉ ghi khi ô đang trống; không xoá/đè
  ghi chú có sẵn — có nội dung thì nối thêm sau dấu ` | `).
