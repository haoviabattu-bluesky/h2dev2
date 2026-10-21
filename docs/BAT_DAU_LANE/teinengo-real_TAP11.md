# LANE F `teinengo-real` — BẮT ĐẦU TẬP 11 `ep11-mie-no-okane` (viết 2026-10-03)

> Anh mở tab mới, dán 1 dòng: `Làm theo E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real_TAP11.md`
> Tab mới: mở đầu báo cáo bằng `@lane:teinengo-real`, đọc HẾT file này, làm đúng thứ tự §1→§4. Chạy mọi lệnh tại `E:\CLAUDE\YOUTUBE\h2dev`.
> File này THẮNG `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\HUONG_DAN_TAP_TIEP_THEO.md` cho riêng tập 11 (file đó vẫn đang trỏ tập 9).

## 0. THAM SỐ
| | |
|---|---|
| Thư mục `<D>` | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep11-mie-no-okane` |
| Dòng sheet | **12** (tab `F-teinengo-real`, STT 11) |
| Video gốc | `K8tTrxijqEo` 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 (6 cách tiêu tiền khiến người phá sản tuổi già nghèo đi) — 221.865 view, điểm 12,8 breakout |
| Đề tài | 【漫画】酒も博打もしない俺…退職金2800万円が5年で半分以下になった6つの見栄 (chẳng rượu chè cờ bạc, 2.800 vạn tiền nghỉ việc còn chưa nửa sau 5 năm vì 6 cái sĩ diện) |
| Trụ cột | #2 chi phí ẩn + #3 sĩ diện cựu quản lý |

## 1. HỒ SƠ — ĐÃ CÓ SẴN (máy 1 làm 03/10, KHÔNG làm lại)
| File | Nội dung |
|---|---|
| `<D>\title.txt` · `<D>\promise.txt` | tiêu đề làm việc · 1 lời hứa (cổng S1L cần) |
| `<D>\series_ctx.txt` | **TIỀN ĐỀ** (nhân vật, 6 sĩ diện theo dòng thời gian, sổ cộng khớp ≈1700万) + `SỐ ĐƯỢC PHÉP` + tư liệu [D1]–[D5] có nguồn |
| `<D>\comment_insight.json` | điểm chạm + thiếu sót rút từ 24 bình luận thật (pipeline lean tự đọc) |
| `<D>\video_goc.json` | K8tTrxijqEo (đã ghi cả `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\VIDEO_GOC.json`) |
| `<D>\research\` | `NGHIEN_CUU.md` (tóm tắt tiếng Việt — ĐỌC file này), transcript gốc, 24 bình luận, meta, phân tích K2 |
| `competitor.txt` | **CỐ Ý KHÔNG CÓ** → B2 tự mượn khung nhịp story `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\_khung_nhip.txt`. Video gốc là đếm ngược 6→1 (nhịp Lane G) — **cấm** chép `research\transcript_goc.txt` sang `competitor.txt` |

Việc tab còn làm ở §1: kiểm cột C dòng 12 đã = `<D>\` (máy 1 đã ghi 03/10); đọc `<D>\research\NGHIEN_CUU.md` + `<D>\series_ctx.txt`.

## 2. VIẾT + KHOÁ KỊCH BẢN
```bat
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile teinengo-real --slug ep11-mie-no-okane --den B3G
```
- KHÔNG truyền `--competitor` (B2b sẽ ghi "không có video nguồn" — đúng; insight đã có sẵn ở `comment_insight.json`).
- Chạy lâu → Bash `run_in_background`, báo giờ dự kiến rồi dừng lượt.
- Hook = Fable 5.1 viết 2 phương án → Sol chọn → Opus 5 vá → khoá; hook **cao trào cảm xúc** (`script.hook.cao_trao`): gợi ý cao trào = cảnh vợ lật trang
  家計簿 (sổ chi tiêu) năm thứ 5 — không có một dòng nào chi cho hai vợ chồng (sĩ diện ⑥). Hook dài tới hết cao trào (≤1'30"), chỉ nhạc nền.
- S2 Opus 5.5 viết 1 lần → máy đo → Opus 5 vá → LOCK. Khoá xong máy TỰ DỪNG, tự giao máy 3 (D12 = `Chờ kiểm tra kịch bản`).

## 3. TỰ SOÁT TRƯỚC KHI BÁO (đọc `<D>\script.txt`, không sửa tay)
- KHÔNG có 第6位…第1位 / "6選" kiểu danh sách; 6 sĩ diện là 6 cảnh theo năm 1→5, có thoại.
- KHÔNG quán nhậu + ông thầy; không tên 藤田/宮本/女将; không 四国遍路, không 温泉2泊3日.
- Sổ tiền cộng khớp: 2800万 → 1100万 sau 5 năm; số thống kê chỉ dùng số trong `SỐ ĐƯỢC PHÉP`.
- CTA chỉ 1 lần ở cuối. Có lỗi → sửa qua `viec_tay.txt`/`patch_model` theo quy trình, cấm sửa tay `script.txt`.

## 4. BÁO ANH + DỪNG
Đường dẫn bản gửi máy 3 `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\F-teinengo-real\ep11-mie-no-okane\script.txt` + 3 dòng điểm anh nên soi. DỪNG.
Anh sửa xong (D12 = `Đã sửa kịch bản`) → tab làm tiếp theo `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` §1–§5 (tới clip hook xem thử).

## 5. LUẬT CỨNG (nhắc)
Máy 1 chỉ bước 1 + hình hook (cấm `--from B4`, `--den B5/B8`) · không kill Chrome theo tên · không xoá dữ liệu sheet · chữ Nhật gửi anh kèm dịch Việt ·
đường dẫn tuyệt đối · tiêu đề/mô tả/thumbnail TẮT toàn dự án (không gọi `goi_title.py`).
