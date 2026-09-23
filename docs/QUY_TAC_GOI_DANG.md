# QUY TẮC GÓI ĐĂNG — một lời hứa, bốn chỗ nói cùng một câu (chốt 2026-09-23)

Nguồn luật: bàn giao TRENDING-RESEARCH 2026-09-23 (đúc kết từ **9 kênh mẫu · 93 video · 56 tập của
mình**) —
`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\hook_from_research\NGUYEN_TAC_HOOK_GOI_DANG.md`
(10 nguyên tắc) · `...\HOOK_AUDIT_KENH_CLONE.md` (satori · toshi · iro, từng tập) ·
`...\results\hook_lane_EFG_2026-09-23\HOOK_AUDIT_LANE_EFG.md` (kenko · real · tano, từng tập).

File này là **SOP dùng chung mọi lane**. Ngưỡng riêng của từng lane nằm ở `profile.goi_dang`, KHÔNG
nằm ở đây.

---

## 1. Tám luật (G1–G8)

| Mã | Luật | Ai kiểm |
|---|---|---|
| G1 | **MỘT LỜI HỨA.** Mỗi tập có `promise.txt` (1 câu) ở gốc thư mục tập. Tiêu đề · chữ thumbnail · câu đầu mô tả · và `promise_window_s` giây đầu lời đọc đều phải nói lại lời hứa đó. | `qc_goi_dang.py` |
| G2 | **LỜI HỨA GIỮ ĐƯỢC.** Mọi vế tiêu đề và mọi dòng chữ thumbnail phải tìm thấy trong `script.txt` (so cả chữ số ↔ chữ Hán: 76秒 ↔ 七十六秒). Vế LÕI phải xuất hiện trước giây 90. Vế bị script phủ định → chặn. | `qc_goi_dang.py` |
| G3 | **THỨ TỰ 60–90 GIÂY ĐẦU.** Câu đầu không chào / cảm ơn / tự giới thiệu / đọc to chữ 「タイトル」; câu mâu thuẫn ≤ ngưỡng lane; lõi tiêu đề ≤ 30–45s; câu "nghi thức" của kênh có mặt. | `qc_goi_dang.py` |
| G4 | **VIDEO DANH SÁCH.** Không đọc trước danh sách trong 2 phút đầu; đếm mục thật khớp `gate.list_item_count`; mục 1 để cuối; thumbnail hiện mục GIỮA (`thumb_rank.txt`), giấu mục 1; bỏ câu tự tháo đếm ngược. | `qc_goi_dang.py` |
| G5 | **TIÊU ĐỀ.** Treo một ẩn số; không dùng chữ sợ đứng một mình; không rào (かもしれない・可能性・知っておきたい); lõi trong dải đã đo của kênh mẫu. | `qc_goi_dang.py` |
| G6 | **THUMBNAIL.** Mỗi tập CHỈ 1 file thumbnail được `DANG-TAI.txt` trỏ tới; `thumb_text.txt` phải khớp CHỮ TRÊN ẢNH. | `qc_goi_dang.py` (phần file) + `qc_thumbnail_sol.py` (phần đọc ảnh) |
| G7 | **CHANNEL_ANALYZER.** K2 phải NHÌN ảnh thumbnail thật và chép chữ từng dòng (cấm suy luận), phải có mục "lời hứa của video" và chấm tiêu đề↔thumbnail↔mô tả↔hook. | `channel_analyzer.py` |
| G8 | **KHÔNG CHÉP NHAU.** Chép CƠ CHẾ của video hit, không chép CÂU; các tập trong cùng lane không mở giống nhau. | `qc_goi_dang.py` |

---

## 2. Chạy cổng

```
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\qc_goi_dang.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\<lane>\<epNN-slug> --profile <mã lane>
```

Cổng **0 LLM, 0 mạng, 0 đồng** — chạy lại bao nhiêu lần cũng được. Kết quả ghi
`<thư mục tập>\logs\B7G_attempt_NNN.json` (thêm `--no-log` để không ghi).

Cổng cũng đã được nối vào **B10** (`pipeline\qc_final.py::kiem_goi_dang`), nhưng cố ý để mức
`vua` chứ không phải `cao` — xem §5.

### Mốc giây lấy ở đâu
Có `voice.srt` → dùng mốc THẬT. Chưa thu giọng → suy ra từ `voice.char_rate` của profile. Cổng in ra
nó đang dùng nguồn nào ở dòng `mốc_giây_từ`, đừng đoán.

---

## 3. Lane mới phải khai gì

Thêm khối `goi_dang` vào `profiles\profiles\<lane>.json`. Mọi con số phải ĐO TỪ KÊNH MẪU CỦA CHÍNH
LANE ĐÓ và ghi nguồn vào field `_nguon` — cấm chép ngưỡng của lane khác (hàng rào chống lẫn lane #1).

```json
"goi_dang": {
  "enabled": true,
  "promise_window_s": 45,
  "contradiction_max_s": 25,
  "title_core_max_s": 45,
  "ritual": ["câu nghi thức của kênh"],
  "title_suffix_ignore": ["đuôi cố định của lane"],
  "title_core_len": [35, 65],
  "list_mode": false,
  "_nguon": "đo từ N video kênh mẫu <URL>: …"
}
```

Lane KHÔNG khai `enabled: true` → cổng chạy **WARN-only**, in ra mọi phát hiện kèm tiền tố
`(sẽ CHẶN khi bật goi_dang.enabled)` nhưng không chặn gì. Đây là cách bật dần từng lane, giống
`script.hook.enabled`.

Toàn bộ danh sách field + mặc định: đọc `MAC_DINH` ở đầu `pipeline\qc_goi_dang.py`.

---

## 4. Hai lối thoát hợp lệ (và một lối KHÔNG hợp lệ)

**Hợp lệ 1 — `goi_dang_ok.txt`** trong thư mục tập: ghi lại vế đã ĐỌC TAY và xác nhận script có giữ,
kèm bằng chứng. Cổng hạ đúng vế đó từ CHẶN xuống CẢNH BÁO và vẫn in lý do mỗi lần chạy.

```
# khuôn: <vế> | <lý do, phải nêu bằng chứng>
月1000円以下の過ごし方 | script giây ~254 「金のかからない過ごし方が、五つある」 + giây ~264 「予算枠は月に1000円まで」
```

**Hợp lệ 2 — sửa ngưỡng trong profile**, kèm `_nguon` nói rõ đo ở đâu.

**KHÔNG hợp lệ:** thêm `if profile_id == ...` vào `qc_goi_dang.py`, hoặc nới ngưỡng chung (`MAC_DINH`)
để một lane qua cổng. Khác biệt giữa các lane chỉ đi qua field profile.

---

## 5. Vì sao B10 để mức `vua` chứ không phải `cao`

Quét thật 52 tập của 6 lane ngày 2026-09-23 ra **236 phát hiện** (G1 52 · G3 97 · G2 45 · G5 30 ·
G4 14 · G6 2). Để mức `cao` là B10 của MỌI tập cũ đỏ ngay, kể cả tập đã đăng và không định sửa.
Nâng lên `cao` là **một dòng** trong `qc_final.py::kiem_goi_dang` — làm sau khi dọn xong tồn kho
(danh sách ở `FlowHandoff_local\shared\BAO_CAO_H2DEV_HOOK_2026-09-23.md`).

---

## 6. Cổng đã được hiệu chuẩn thế nào (đừng chỉnh mù)

Cổng tái lập ĐÚNG các con số mà bên nghiên cứu đếm tay — đây là cách kiểm nó có đo đúng thứ cần đo:

| Bên nghiên cứu đếm tay | Cổng đo được |
|---|---|
| iro: 「この写真をカラー化してみる」 0/11 tập | G3 báo thiếu ở đúng 11 tập |
| iro: 「N枚の写真で辿っていく」 0/11 tập | G3 báo thiếu ở đúng 11 tập |
| iro: tiêu đề lõi 66–77 ký tự, 11/11 dài hơn kênh mẫu | G5 báo 10 tập lõi 66–77 |
| toshi: 「それでは…最初から辿っていこう」 thiếu ở phần lớn tập | G3 báo thiếu ở 8 tập |
| kenko: đọc to chữ 「タイトル」 ở giây 0,3 | G3 bắt 6 tập (đã vá, xem §7) |
| tano: 7/10 tự giới thiệu 「俺の名前は」 quá sớm | G3 bắt 6 tập |

Hai chỗ đã phải nới sau khi chạy thật (ghi lại để đừng siết lại mù):
1. **G2 không so NGUYÊN VĂN được.** Chữ thumbnail và vế tiêu đề gần như không bao giờ trùng nguyên
   văn lời đọc. So nguyên văn cho ~5 lỗi/tập ở gần như MỌI tập — con số không phân biệt được tập
   hỏng với tập lành. Nay chia 2 bậc theo độ phủ bigram (`ve_phu_canh`, mặc định 0,62).
2. **G5 "treo ẩn số" không phải lane nào cũng dùng TỪ HỎI.** Lane iro: 9/9 tiêu đề kênh mẫu có SỐ
   trong phần lõi và 0/9 có 真相/なぜ/とは. Không có cờ `title_an_so_chap_nhan_so` là cổng báo sai
   11/11 tập.

---

## 7. Bẫy đã vá cùng đợt này

**Dòng 「タイトル：…」 ở đầu bản thảo bị TTS đọc to.** Model hay mở bản thảo bằng một dòng tiêu đề;
`script.txt` đi thẳng vào TTS nên máy đọc to luôn chữ 「タイトル」 ở giây 0,3. Đo thật: **6/8 tập lane
kenko-chiebukuro** dính, trong đó ep01–04 đã ra tới người xem. `MARKER_PAT` không bắt được vì đây là
một dòng bình thường, không có ký hiệu markdown nào. Đã vá bằng `ai_steps.TITLE_LINE_PAT` (gỡ dòng
đầu khớp `タイトル|題名|表題|Title` + `:`), test ở `pipeline\tests\test_strip_title_line.py`.

---

## 8. Việc còn lại, làm ở đâu

- **G7 (channel_analyzer)** — xem §7 của `docs\QUY_TRINH_NGHIEN_CUU_KENH.md`.
- **Tập cần sửa cụ thể từng lane** — `FlowHandoff_local\shared\BAO_CAO_H2DEV_HOOK_2026-09-23.md`.
- **Hook 20–30s đầu** — `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b (`hook_stage.py`), khác việc
  của file này: hook là NỘI DUNG mở đầu, gói đăng là LỜI HỨA bao quanh nó.
