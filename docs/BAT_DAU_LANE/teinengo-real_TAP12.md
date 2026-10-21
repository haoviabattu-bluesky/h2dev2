# LANE F `teinengo-real` — BẮT ĐẦU TẬP 12 `ep12-mimoto-hoshou` (viết 2026-10-03)

> Anh mở tab mới, dán 1 dòng: `Làm theo E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real_TAP12.md`
> Tab mới: mở đầu báo cáo bằng `@lane:teinengo-real`, đọc HẾT file này, làm đúng thứ tự §1→§4. Chạy mọi lệnh tại `E:\CLAUDE\YOUTUBE\h2dev`.
> File này THẮNG `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\HUONG_DAN_TAP_TIEP_THEO.md` cho riêng tập 12. Tập 11 và 12 độc lập, chạy song song 2 tab được
> (khác `--slug`, không đè nhau).

## 0. THAM SỐ
| | |
|---|---|
| Thư mục `<D>` | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep12-mimoto-hoshou` |
| Dòng sheet | **13** (tab `F-teinengo-real`, STT 12) |
| Video gốc | `dY3HfjtmvXI` 【漫画】65歳、独身、年金生活…その先に待っていた衝撃の現実 (65 tuổi, độc thân, sống bằng lương hưu… hiện thực sốc phía trước) — 61.708 view, điểm 3,07 strong |
| Đề tài | 【漫画】65歳、独身の俺…入院の日「保証人は？」で147万円の契約書にサインしかけた (ngày nhập viện, chỉ vì câu "Người bảo lãnh đâu?" mà suýt ký hợp đồng 147 vạn yên) |
| Trụ cột | #4 độc thân & nhà ở + #2 bẫy thủ tục |

## 1. HỒ SƠ — ĐÃ CÓ SẴN (máy 1 làm 03/10, KHÔNG làm lại)
| File | Nội dung |
|---|---|
| `<D>\title.txt` · `<D>\promise.txt` | tiêu đề làm việc · 1 lời hứa |
| `<D>\series_ctx.txt` | **TIỀN ĐỀ** (俺 ở thuê, ngày nhập viện, báo giá 147万, người giường bên, nhân viên tư vấn bệnh viện, payoff gần như 0 đồng) + `SỐ ĐƯỢC PHÉP` + [D1]–[D6] có nguồn |
| `<D>\comment_insight.json` | rút từ 34 bình luận thật (có 2 lời chê 6 like: "lại chuyện cũ" + "chỉ gây sợ") |
| `<D>\video_goc.json` | dY3HfjtmvXI |
| `<D>\research\` | `NGHIEN_CUU.md` (ĐỌC file này), transcript gốc, bình luận, meta, phân tích K2 |
| `competitor.txt` | **CỐ Ý KHÔNG CÓ** → B2 mượn `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\_khung_nhip.txt`. Gốc đầy chi tiết trùng tập 6 (修繕積立金) + tập 7 (cô đơn) → cấm chép transcript gốc sang `competitor.txt` |

## 2. VIẾT + KHOÁ KỊCH BẢN
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile teinengo-real --slug ep12-mimoto-hoshou --den B3G
```
- KHÔNG truyền `--competitor`. Chạy lâu → Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt.
- Hook cao trào cảm xúc: gợi ý = cây bút trên tờ hợp đồng 147万円 cạnh giường bệnh, ô 「身元保証人」 trên tờ nhập viện còn trống. Bối cảnh: **gặp mặt
  tại giường bệnh** (nhân viên kinh doanh tới tận nơi), cảnh gọi xe cấp cứu là **gọi điện** — ghi rõ khi viết `<D>\hook\ghi_chu_canh.txt` sau này.
- Khoá xong máy TỰ DỪNG, tự giao máy 3 (D13 = `Chờ kiểm tra kịch bản`).

## 3. TỰ SOÁT TRƯỚC KHI BÁO (đọc `<D>\script.txt`, không sửa tay)
- Không 修繕積立金, không chung cư sở hữu, không hội mô hình tàu hoả/展示会/職業講話; không tên 高橋/宮本/佐木.
- Câu về chế độ phải ĐÚNG MỨC: "nhà nước coi việc từ chối CHỈ vì không có người bảo lãnh là không thích hợp" — KHÔNG nói "bệnh viện không được hỏi".
- Không nói xấu công ty bảo lãnh cụ thể, không gọi cả ngành là lừa đảo. 高額療養費 dùng 6万1500円 (truyện sau 8/2026).
- Y khoa nhẹ, chung chung. Sổ tiền: 年金13万, tiết kiệm ~900万, hoá đơn viện ~7–8万 cộng khớp. CTA 1 lần cuối.

## 4. BÁO ANH + DỪNG
Đường dẫn `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\F-teinengo-real\ep12-mimoto-hoshou\script.txt` + 3 dòng điểm anh nên soi. DỪNG.
Anh sửa xong (D13 = `Đã sửa kịch bản`) → `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` §1–§5.

## 5. LUẬT CỨNG (nhắc)
Máy 1 chỉ bước 1 + hình hook · không kill Chrome theo tên · không xoá dữ liệu sheet · chữ Nhật kèm dịch Việt · đường dẫn tuyệt đối ·
tiêu đề/mô tả/thumbnail TẮT toàn dự án.
