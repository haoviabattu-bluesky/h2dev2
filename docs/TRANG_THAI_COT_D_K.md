# TRẠNG THÁI CỘT D (KỊCH BẢN) + CỘT K (GHI CHÚ) — MỌI LANE
> Anh chốt 2026-10-03. Áp mọi lane bật soát máy 3 (`script.review_may3`, vắng field = BẬT; satori không áp).
> Tool TỰ GHI — tab lane không ghi tay. Ô D chỉ bị đè khi đang ở trạng thái liền trước (hoặc trống / ESCALATE / BLOCK);
> chữ lạ → tool không đè, in cảnh báo. Ô K: ghi đè đúng 1 ô dòng của tập (tiêu đề K1 phải là `GHI CHÚ`). Không xoá gì.

| # | Lúc nào | Cột D (dòng đầu) | Cột K dòng tập | Ai ghi |
|---|---|---|---|---|
| 1 | Anh giao chạy kịch bản tập X lane Y — `make_video.py --den B3G` bắt đầu chặng 1 | `Đang chạy kịch bản bước 1` | (giữ nguyên) | `review_may3.bat_dau_b1` (make_video gọi) |
| 2 | Kịch bản khoá xong, chép `script.txt` sang `FlowHandoff_local\jobs\<tab>\<slug>\` | `Chờ kiểm tra kịch bản` (+ dòng 2 = thư mục) | thư mục anh sửa + câu anh báo + lệnh `review_may3.py --nhan …` + file làm tiếp `docs\NHAN_KICH_BAN_MAY3.md` | `review_may3.share` |
| — | Anh sửa xong | `Đã sửa kịch bản` | | anh |
| 3 | Tab nhận bản sửa (`review_may3.py --nhan`) xong → đi làm cast / B5W / B5P / hình + clip hook | `Đang làm Hook` | (giữ nguyên) | `review_may3.nhan` |
| — | Clip hook xem thử gửi anh (`duyet_hook.py --gui`) / anh duyệt | `Chờ duyệt hook` → `Đã duyệt hook` | | tool / anh |
| 4 | Giao máy 2 (`dong_goi_may2.py --job`) | `Đã giao máy 2` (thay `Done` cũ) + H = `cần ảnh (N ảnh, ~Xđ)` | `Lane X tập N - giao máy 2 thực hiện` + `Làm theo FlowHandoff_local\jobs\<tab>\<slug>\_BANGIAO.txt` + lệnh chặng 1 (cd / xcopy / make_video) + đường dẫn máy 1 (KHÔNG kèm hướng dẫn tập kế) | `dong_goi_may2._ghi_cot_d_done` + `_k_giao_may2` |
| 4' | (21/10, MÁY 2 làm A→Z) `dong_goi_may2.py --job` trên máy có `MAY.local`=2 | `Chờ dựng video` | `Lane X tập N - máy 2 tự dựng A→Z` + `_BANGIAO.txt` trong thư mục tập + lệnh chặng 1 | `dong_goi_may2` |
| 5 | Bắt đầu dựng / có `final.mp4` thật | `Đang dựng video` → `Video xong` (+ dòng 2 = thư mục video) | | `pipeline\xong_video.py` (`--bat-dau` / không cờ) |

Ví dụ ô K mốc 2 (Lane L tập 9):
```
Chờ kiểm tra kịch bản 03/10 10:21
Anh sửa: E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\L-shakai-no-naze\ep09-tenkin-kotowaru\script.txt (hook = đoạn đầu)
Anh sửa xong thì đổi D = "Đã sửa kịch bản" và báo "anh sửa xong kịch bản L ep09". Em sẽ chạy:
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile shakai_no_naze --slug ep09-tenkin-kotowaru
rồi làm tiếp theo E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md.
```

Ghi chú:
- Mốc 4 đè cột K **dòng tập kế** = `Tab mới — làm tập tiếp theo …: Làm theo <slug_dir>\HUONG_DAN_TAP_TIEP_THEO.md` (`huong_dan_tab_moi.py --loai tiep`);
  (04/10) LUÔN ghi ở dòng tập kế, kể cả khi dòng đó chưa có STT/đề tài — ô K tập vừa giao không lặp lại dòng này.
- Tập giao trước 03/10 có D = `Done`: đóng gói lại → tool đổi sang `Đã giao máy 2`.
- Lane không có chặng duyệt hook: `dong_goi_may2` nhận thẳng từ `Đang làm Hook`.
- Xem trạng thái cả lane: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --trang-thai --profile <lane>`.

## TAB TONGHOP (bảng tổng quan mọi lane, anh chốt 04/10)
Dòng 1 = tên tab lane, cột A = `Ep01…`. Tool tự ghi ô (tập, lane) qua `pipeline\tong_hop.py` (gọi kèm 5 mốc trên):
`Chạy kịch bản` (mốc 1) → `Chờ duyệt kịch bản` (mốc 2) → `Chạy Hook` (mốc 3) → `Chờ duyệt Hook` (`duyet_hook --gui`) → `Giao máy 2` (mốc 4).
`Chạy ảnh + video` / `Done` / `Listed` = máy 2/anh ghi, tool không đè. Lane chưa có cột → tool thêm tên tab vào ô trống đầu dòng 1;
tập chưa có dòng → thêm `EpNN` nối cột A. Ghi tay: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\tong_hop.py --profile <lane> --slug <tập> --trang-thai "Chạy Hook"`.
