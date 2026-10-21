# CHANNEL ANALYZER — TRẠNG THÁI TỪNG LANE (dọn từ CLAUDE.md 2026-09-29)

> Đây là bảng TRẠNG THÁI (đổi theo thời gian), không phải quy tắc — quy tắc chung (K1/K2/K3 là gì,
> cách chạy, cổng chống chạy lại) vẫn nằm ở mục "🧬 CHANNEL ANALYZER" trong `CLAUDE.md`. File này
> chỉ trả lời "lane X đã có DNA chưa, resume từ đâu" — lane mới xong K1+K2 thì tự cập nhật dòng
> tương ứng, KHÔNG cần đọc hết bảng của lane khác.

**Lane NHẬN dữ liệu (từ máy 2 hoặc tự chạy) rồi RESUME từ bước nào:**

| Lane | `docs/channel_dna/` | Kênh mẫu | SOP đã có §0b? | Resume từ |
|---|---|---|---|---|
| `satori-jp-obaa` | ✅ `simbot2` (4 video test — nên chạy lại `--n-videos 8` khi rảnh) | simbot2 `@simbot2` | ✅ `SOP_SATORI_JP.md` §0b | Chạy K3 rồi vào B1-chọn-chủ-đề như cũ |
| `yakkyoku-sukatto` (Lane K) | ✅ `yakkyoku-sukatto` (4 video, 2026-09-24) | 千種テンカ `UCEBA1RFfkXQtqgiDVLh4bcw` | ✅ `SOP_LANE_K.md` §0b | Chạy K3 rồi vào §2 của SOP |
| `shakai_no_naze` (Lane L) | ✅ `shakai-no-naze` (8 video + số đo thật, 2026-09-24) | 社会のウラガワ `UCFWFKb3Yr_1SrAT0kcvwFdw` | ✅ `SOP_LANE_L.md` §0b | Chạy K3 rồi vào §2 của SOP |
| `Lopezzapa68` | ❌ chưa chạy | **CHƯA RÕ** — chưa có kênh mẫu nào được xác nhận | ❌ chưa có SOP | Hỏi user kênh mẫu trước khi chạy `channel_analyzer.py`, đừng tự đoán/bịa URL |

> **2026-09-29: Lane A (`toshi-densetsu-jp`), D (`irogatatarukioku`), E (`kenko-chiebukuro`) đã BỎ** —
> xoá toàn bộ assets/profile/SOP/channel_dna, không còn dòng trong bảng trên. Mã A/D/E không tái dùng.

**Anh đưa 1 kênh / 1 video và bảo "làm video theo cái này" → gọi skill global `youtube-produce`**
(runbook 6 pha: nghiên cứu kênh → lập profile + đo char-rate → hồ sơ đề tài → chạy pipeline →
thumbnail theo mô-típ kênh → file đăng tải). Nội dung do dự án research bên ngoài đưa sang thì phải
đúng khuôn `docs/KHUON_HO_SO_DE_TAI.md`.

**NGUỒN TƯ LIỆU tài liệu/vũ trụ bí ẩn = dự án `E:\CLAUDE\YOUTUBE\SPACE_RESEARCH`** (chạy 24/7, đào đề tài + dữ
kiện đã kiểm chứng). Quy trình giao–nhận đầy đủ: `docs/GIAO_VIEC_SPACE_RESEARCH.md` (dùng chung cho
MỌI lane).

**NGUỒN NGÁCH MỚI (Lane E/F/G...) = dự án `TRENDING-RESEARCH` (máy khác), giao qua Syncthing — KÊNH
TRUYỀN KHÁC HẲN SPACE_RESEARCH (không qua Sheet/`_READY`).** ⚠️ Bài học trả giá thật 2026-09-16:
Syncthing ở máy này CHỈ sync đúng 4 thư mục `FlowHandoff_local\{jobs,results,shared}` + `CHANEL` —
`h2dev\docs\` KHÔNG nằm trong sync. Quy ước ĐÚNG (đã áp dụng cho E/F/G): hồ sơ NẶNG (chiều 2→1) đặt
ở `FlowHandoff_local\results\laneX_from_research\`; chỉ file tóm tắt việc cần làm đặt ở
`FlowHandoff_local\shared\GIAO_VIEC_LANE_X.md` và trỏ đường dẫn tuyệt đối vào đúng thư mục `results\`
ở trên. Nhận việc lane mới → luôn kiểm tra file tóm tắt trỏ đúng vào `results\`, đừng tin theo path
`docs\...` nếu file đó ghi vậy.

**⚡ CÂU LỆNH: "tạo nội dung gửi space research để hỗ trợ tìm kiếm thông tin"** → làm ĐỦ 3 việc:
1. Khai/kiểm khối `research` trong profile của lane đang làm (ngưỡng đo từ kênh tham chiếu của
   chính lane này, cấm chép từ lane khác).
2. `py -3.13 pipeline\don_dat_hang.py --profile <lane>`
3. Trả về ĐÚNG MỘT DÒNG đường dẫn để copy: `E:\CLAUDE\YOUTUBE\SPACE_RESEARCH\DON_DAT_HANG_<lane>.md`

Vòng nhận hàng: chờ cột D của trang tính `gid=612920013` ghi `DONE-READY` → chạy cổng B0 trước khi
động vào bất cứ thứ gì: `py -3.13 pipeline\qc_hoso.py --folder "<...>\_READY\<nn>-<slug>" --profile <lane>`.
B0 ĐẠT mới copy vào thư mục tập rồi chạy `make_video.py`. B0 TRƯỢT thì trả lại bên đó kèm danh sách,
KHÔNG tự sửa hộ. Làm xong chuyển thư mục hồ sơ sang `_DONE\`.

Hợp đồng của mỗi lane khai ở `profile.research`, cổng B0 đọc thẳng khối đó làm ngưỡng — sửa hợp đồng
là sửa JSON, không sửa `qc_hoso.py`. Lane không khai `research` = lane không nhận hàng nghiên cứu.
Ranh giới: bên đó CHỈ nghiên cứu, bên này CHỈ làm video. Lane mới thì thêm 1 dòng vào bảng resume ở
trên + 1 SOP riêng, TUYỆT ĐỐI không nhét vào SOP của lane đang có.
