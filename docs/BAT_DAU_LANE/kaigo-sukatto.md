# BẮT ĐẦU LANE O — `kaigo-sukatto` · 介護スカッと (tên tạm "Lane-O", dịch: "chăm sóc người già — hả dạ")

> Anh nói **"thực hiện lane O"** / **"làm tập tiếp theo lane O"** → tab đọc file này, mở đầu báo cáo bằng `@lane:kaigo-sukatto`.
> Tập 1: đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto_TAP1.md`.
> ⭐ 30/09 anh chốt: hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc:
> `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`; luật cao trào cũ đã xoá); `make_video --den B3G` khoá xong là DỪNG, giao máy 3/anh soát
> (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) → `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`.

## ⚡ ĐỌC NHANH — "làm tập tiếp theo"
⭐ Tập 11–22 (15/10): mỗi tập có `HUONG_DAN_TAP.md` riêng trong thư mục tập — anh dán "Lane O tập X đọc <file> và thực hiện"; mục lục `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\HUONG_DAN_TAP11-22.md`.
Chỉ đọc: `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_O.md` (runbook) + `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\kaigo-sukatto\COMMENT_INSIGHT.md`.
Danh sách tập = tab sheet `Lane-O` A2:B11 (cột K = ghi chú/video gốc từng tập). Không mở lại profile JSON / báo cáo nghiên cứu trừ khi lệnh báo lỗi.

## 1. ĐỊNH DANH
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `kaigo-sukatto` — `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\kaigo-sukatto.json` |
| Tên gọi | **Lane-O** (tên tạm; khi anh đặt tên kênh thì đổi id/slug_dir/tab/channel_dna_dir CÙNG LÚC, không đổi lẻ) |
| Kênh thật | **CHƯA CÓ** (anh báo sau) — chưa mail, chưa handle; `publish.title_auto=false`, nút đăng ký `assemble.subscribe` TẮT |
| Tab sheet | `Lane-O` (header A→L giống `Lane-N`: STT · NỘI DUNG · FOLDER · KỊCH BẢN · TITLE · TAGS · THUMBNAIL · STATUS-IMG · VIDEO · LIST · GHI CHÚ · ID KÊNH) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\` (tập = `ep<NN>-<slug>\`) |
| Kênh mẫu | 千種テンカ (Chigusa Tenka) `https://www.youtube.com/channel/UCEBA1RFfkXQtqgiDVLh4bcw` — CÙNG kênh mẫu Lane K, đổi nghề 薬剤師 → 介護職員 |
| Nghiên cứu (đọc 1 lần khi setup) | `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\KENH_GOC_10\PHAN_TICH_10_VIDEO_VA_AP_DUNG_KAIGO.md` (xếp hạng 10 video, 9 lý do thắng, luật áp dụng 介護, 10 tập đề xuất) |
| Kỹ thuật | Y HỆT Lane K: đa giọng VOICEVOX (người kể 玄野武宏 · nhân vật chính 黒沢冴白 · hành chính/相談員 波音リツ), khoá mặt @CAST ≤3 mặt/ảnh, bóng thoại chữ dọc do máy vẽ, mờ chồng 0,3s + phóng ×1,025, nhạc nền Lane K |

## 2. TRẠNG THÁI
- ✅ 2026-09-30 nghiên cứu 10 video kênh mẫu + khả thi nghề 介護 (báo cáo ở mục 1).
- ✅ 2026-09-30 setup: profile (lean, Fable 5.1 viết từ 05/10 / Opus 5 vá, Sol tắt, `soat:"may3"`, hook Fable + cao trào, `chan_buoc2_may1`) ·
  S1L + S1Q kiểm = 0 lỗi · `COMMENT_INSIGHT.md` · SOP `docs\SOP_LANE_O.md` · tab `Lane-O` A2:B11 + K2:K11 · router `CLAUDE.md` + `DANH_BA_LANE.md`.
- ✅ 2026-09-30 hồ sơ tập 1 `ep01-jaa-yamemasu` điền sẵn (competitor + series_ctx [D1]–[D4] có URL + title + promise).
- ⏳ Tập 1 chưa chạy — theo `kaigo-sukatto_TAP1.md`.
- ⚠️ `voice.char_rate` 316,7 MƯỢN Lane K (cùng engine/giọng/tốc độ) → đo lại từ video thật ep01.
