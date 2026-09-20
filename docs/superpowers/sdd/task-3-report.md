# TASK 3 REPORT — `qc_prompt_consistency.py` (cổng B5P: prompt ↔ story facts, PROMPT_CONFLICT)

Ngày: 2026-09-18 · Python: `py -3.13` · Thư mục chạy: `E:\CLAUDE\YOUTUBE\h2dev\pipeline`
Trạng thái: **DONE_WITH_CONCERNS** (test 6/6, Step 5 đủ 5/5, Step 6 exit 1 vì `n_would_block=9 > 3` — 8/9 là lỗi THẬT của prompt gốc mà Step 6 không sửa, xem §6).

## 1. Files

| File | Dòng | Ghi chú |
|---|---|---|
| `pipeline/qc_prompt_consistency.py` | 224 | code Step 3 của brief + 3 câu wording thêm (§8) |
| `pipeline/tests/test_qc_prompt_consistency.py` | 117 | **giống brief 100%** (diff = rỗng, kiểm bằng script) |
| `scratch_analysis/_regress_stt3_b5p_old/` | — | bản hồi quy prompt CŨ (Step 5), dựng lại từ đầu bằng đúng lệnh brief |
| `scratch_analysis/_regress_stt3_b5p_fixed/` | — | bản hồi quy prompt ĐÃ SỬA (Step 6), dựng bằng đúng lệnh brief |
| `docs/superpowers/sdd/task-3-report.md` | — | file này |

Không sửa `gate_common.py`, `qc_img_doan.py`, `sinh_neo.py`, `llm_client.py`, `render_engine.py`, `assemble.py`, `chay_buoc3.py`, `qc_visual.py`, `qc_script.py`. Không đụng thư mục tập thật `assets/satori_jp/simbot2-03-Kmxva85WKec` (chỉ đọc).

### 1b. Hiện trạng gặp lúc bắt đầu (cần biết)
Khi mở việc, **cả 2 file đã tồn tại** (mtime 12:32–12:37 cùng ngày) do một phiên trước của chính Task 3 bị cắt giữa chừng: test giống brief; `qc_prompt_consistency.py` giống brief NGOẠI TRỪ `_prompt_facts`/`_prompt_kiem` đã bị viết lại dài hơn (liệt kê 3 loại (a)(b)(c) địa danh / đồ uống đóng gói / giấy tờ); có 1 log `B5P_attempt_001` trên `_regress_stt3_b5p_old` cho 5/5; **Step 6 chưa chạy, không có report, `progress.md` không ghi gì**.
Xử lý: lưu bản wording đó ra scratchpad, **khôi phục nguyên văn code Step 3 của brief** (diff = rỗng, kiểm bằng script), rồi chạy lại Step 5 từ wording gốc để biết có thật cần sửa wording không (kết quả: KHÔNG cần — brief gốc đã bắt đủ 5/5, xem §4 run 1). Vì vậy bản wording của phiên trước bị bỏ, không dùng.

## 2. Step 2 — test fail trước khi có code
Không tái hiện được `ModuleNotFoundError` vì file code đã tồn tại sẵn (xem §1b). Đi thẳng Step 4.

## 3. Step 4 — pytest (exact output)
```
$ cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_qc_prompt_consistency.py -q
......                                                                   [100%]
6 passed in 0.06s

$ py -3.13 -m pytest tests -q
32 passed in 0.23s
```
(6/6 pass ở cả 3 trạng thái wording: brief gốc, iter 1, iter 2 — test không phụ thuộc wording.)

## 4. Step 5 — hồi quy prompt CŨ (5 lỗi đã biết: 022, 028, 112, 113, 114)

Lệnh dựng + stamp đúng như brief (chạy trong Bash nên `--slug` dùng `/` thay `\`; script Python bên trong giữ nguyên). Mỗi lần chạy lại đều xoá `logs/` + `story_facts.json` của bản copy để không dùng lại facts cũ.

### Run 1 — wording NGUYÊN VĂN brief (baseline)
```
=== B5P: WARN · 128 prompt / 50 doan · checked=128 warn=30 would_block=15 ambiguous=15 · llm calls=14 tok_in=39085 tok_out=10716 latency=190s err=0
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: Prompt ghi 5.000 yên trong khi truyện nêu rõ ba vạn yên (30.000 yên)
  ⚠ 022.png (doan 6) PROMPT_CONFLICT: location: Prompt ve sa mac Saudi Arabia, truyen noi lam o Kawaguchi va Tohoku
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: Prompt ve ca phe goi/instant coffee, truyen noi pha tra houjicha
  ⚠ 028.png (doan 7) PROMPT_CONFLICT: object: Prompt ve goi ca phe instant coffee, truyen noi tra houjicha va banh yokan
  ⚠ 039.png (doan 12) PROMPT_CONFLICT: season: Prompt ghi chiều mùa thu, truyện là mùa hè (ruộng lúa xanh non)
  ⚠ 042.png (doan 13) AMBIGUOUS: plot: Làm dưa yuzu-daikon là chi tiết đời thường thêm vào, truyện không nhắc
  ⚠ 043.png (doan 13) AMBIGUOUS: object: Lọ dưa yuzu-daikon là chi tiết minh họa thêm, truyện không nhắc
  ⚠ 044.png (doan 13) PROMPT_CONFLICT: location: Prompt ở quán trọ Atami, truyện ở nhà chung cư Chiba; season: Prompt ghi mùa thu, truyện là tháng Chạp mùa đông
  ⚠ 045.png (doan 15) PROMPT_CONFLICT: location: Prompt ở lối vào onsen ryokan, truyện ở tòa thị chính Inzai
  ⚠ 046.png (doan 15) AMBIGUOUS: 
  ⚠ 047.png (doan 15) AMBIGUOUS: 
  ⚠ 048.png (doan 16) AMBIGUOUS: 
  ⚠ 049.png (doan 16) AMBIGUOUS: 
  ⚠ 054.png (doan 17) PROMPT_CONFLICT: object: Prompt ve tim dau phu (tofu) thay vi mo muoi (umeboshi)
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: Prompt ghi can of coffee trong khi truyen la lon tra nong
  ⚠ 075.png (doan 26) AMBIGUOUS: 
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: plot: Yasuko để giấy gấp tư kê khai thu nhập 4 vạn 8, không phải 3 sổ ngân hàng
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Cảnh này là giấy gấp tư lót dưới bát miso, không phải 3 sổ ngân hàng
  ⚠ 089.png (doan 30) AMBIGUOUS: object: Chi tiết 3 sổ ngân hàng dán nhãn mục đích không có trong truyện
  ⚠ 095.png (doan 33) AMBIGUOUS: location: Truyen khong noi ro don do o phong nha con gai
  ⚠ 096.png (doan 33) PROMPT_CONFLICT: object: Prompt ve tin nhan smartphone, truyen la mau giay viet tay
  ⚠ 098.png (doan 34) AMBIGUOUS: plot: Canh hop hai nha dat to giay khong co trong truyen
  ⚠ 099.png (doan 34) AMBIGUOUS: object: Ban thoa thuan 3 dong khong co trong truyen
  ⚠ 100.png (doan 34) AMBIGUOUS: plot: Chi tiet cao dau cho chong khong co trong truyen
  ⚠ 111.png (doan 42) AMBIGUOUS: object: Truyện nói phong bì giấy washi, prompt ghi ziplock envelope
  ⚠ 112.png (doan 42) PROMPT_CONFLICT: object: Truyện là giấy hẹn bài vị phu thê, prompt ghi tờ khai kết hôn
  ⚠ 113.png (doan 42) PROMPT_CONFLICT: object: Truyện là giấy hẹn bài vị, prompt ghi tờ khai kết hôn
  ⚠ 114.png (doan 42) PROMPT_CONFLICT: object: Truyện là giấy hẹn bài vị, prompt ghi tờ khai kết hôn
  ⚠ 124.png (doan 49) AMBIGUOUS: object: Truyen noi ghi bia sau so tay, prompt ve giay dan tu lanh
  ⚠ 126.png (doan 50) AMBIGUOUS: object: Truyen khong nhac den to giay dan tu lanh
```
→ **5/5 bắt được ngay với wording gốc**: 022 (location), 028 (object), 112/113/114 (object) đều `PROMPT_CONFLICT`. `n_would_block=15`, `n_ambiguous=15`, 14 lời gọi.
Ngoài 5 lỗi đã biết, cổng còn bắt 10 prompt khác; đối chiếu tay với `script.txt` (xem §6) → 002/027/054/074 là lỗi THẬT, 044/045 là false positive kiểu "chi tiết nằm ở đoạn khác của truyện" (Atami có ở đoạn 41「熱海の夕餉」, ngoài lát facts ±1).

### Run 2 — wording iter 1 (sau khi thấy false positive ở Step 6 run 1, xem §5)
```
=== B5P: WARN · 128 prompt / 50 doan · checked=128 warn=32 would_block=15 ambiguous=17 · llm calls=14 tok_in=40288 tok_out=10854 latency=235s err=0
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: Prompt ve to 5000 yen, truyen noi ba van yen (30.000 yen)
  ⚠ 022.png (doan 6) PROMPT_CONFLICT: location: Prompt ve sa mac Saudi Arabia trong khi truyen noi cong truong Kawaguchi va Tohoku
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: Prompt ve ca phe goi/instant coffee trong khi truyen noi tra houjicha kem yokan
  ⚠ 028.png (doan 7) PROMPT_CONFLICT: object: Prompt ve goi ca phe instant coffee trong khi truyen noi tra houjicha kem yokan
  ⚠ 029.png (doan 7) AMBIGUOUS: 
  ⚠ 030.png (doan 7) AMBIGUOUS: 
  ⚠ 042.png (doan 13) AMBIGUOUS: 
  ⚠ 043.png (doan 13) AMBIGUOUS: 
  ⚠ 044.png (doan 13) AMBIGUOUS: 
  ⚠ 045.png (doan 15) AMBIGUOUS: 
  ⚠ 046.png (doan 15) AMBIGUOUS: 
  ⚠ 047.png (doan 15) AMBIGUOUS: 
  ⚠ 048.png (doan 16) AMBIGUOUS: 
  ⚠ 049.png (doan 16) AMBIGUOUS: 
  ⚠ 054.png (doan 17) PROMPT_CONFLICT: object: Prompt tìm tofu trong khi truyen noi tim qua mo muoi
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: Prompt ve lon ca phe trong khi truyen noi lon tra am
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: object: Truyen: Yasuko dat to giay gap 4 khong tai san; Prompt: Yasuko dat 3 so tiet kiem
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Truyen: to giay gap 4 duoi bat miso; Prompt: 3 so tiet kiem va con dau do
  ⚠ 098.png (doan 34) AMBIGUOUS: 
  ⚠ 099.png (doan 34) AMBIGUOUS: 
  ⚠ 100.png (doan 34) AMBIGUOUS: 
  ⚠ 108.png (doan 40) AMBIGUOUS: 
  ⚠ 109.png (doan 40) AMBIGUOUS: 
  ⚠ 111.png (doan 42) AMBIGUOUS: 
  ⚠ 112.png (doan 42) PROMPT_CONFLICT: object: to khai ket hon khong co trong truyen, truyen la bien nhan phat cu
  ⚠ 113.png (doan 42) PROMPT_CONFLICT: object: to khai ket hon khong co trong truyen, truyen la bien nhan phat cu
  ⚠ 114.png (doan 42) PROMPT_CONFLICT: object: to khai ket hon khong co trong truyen, truyen la bien nhan phat cu
  ⚠ 115.png (doan 43) AMBIGUOUS: 
  ⚠ 118.png (doan 45) PROMPT_CONFLICT: plot: prompt Misawa ky lam chung vs truyen Uy vien dan sinh ky
  ⚠ 124.png (doan 49) PROMPT_CONFLICT: object: Prompt ve note dan tu lanh, truyen ghi mat trong bia sau so tay
```
(console chỉ in 30 warning đầu theo thiết kế `warnings[:30]`; log `B5P_latest.json` có đủ 32.) → vẫn 5/5.

### Run 3 — wording iter 2 (BẢN CUỐI)
```
=== B5P: WARN · 128 prompt / 50 doan · checked=128 warn=41 would_block=16 ambiguous=25 · llm calls=14 tok_in=39945 tok_out=10799 latency=207s err=0
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: truyện nêu ba vạn yên nhưng prompt vẽ tờ năm nghìn yên
  ⚠ 022.png (doan 6) PROMPT_CONFLICT: location: Prompt vẽ sa mạc Saudi Arabia, truyện nói làm ở Kawaguchi và Tohoku
  ⚠ 026.png (doan 7) AMBIGUOUS: object: Truyện không nhắc việc đưa phong bì tiền trả công sửa vòi
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: Prompt vẽ cà phê hòa tan, truyện nói pha trà houjicha
  ⚠ 028.png (doan 7) PROMPT_CONFLICT: object: Prompt vẽ gói cà phê hòa tan, truyện nói pha trà houjicha
  ⚠ 029.png (doan 7) AMBIGUOUS: object: Truyện không nhắc chi tiết danh thiếp của Kokichi
  ⚠ 030.png (doan 7) AMBIGUOUS: object: Truyện không nhắc chi tiết danh thiếp của Kokichi
  ⚠ 031.png (doan 8) AMBIGUOUS: plot: Truyện không nhắc cảnh gọi điện thoại không dây; có thể là minh họa con gái gọi về.
  ⚠ 032.png (doan 8) AMBIGUOUS: plot: Truyện không nhắc Shizue ngồi kotatsu nghe điện thoại; chi tiết minh họa thêm không mâu thuẫn.
  ⚠ 042.png (doan 13) AMBIGUOUS: object: Truyện không nhắc làm dưa muối yuzu-daikon; chi tiết đời thường không mâu thuẫn.
  ⚠ 043.png (doan 13) AMBIGUOUS: object: Truyện không nhắc hũ dưa muối yuzu-daikon; chi tiết đời thường không mâu thuẫn.
  ⚠ 044.png (doan 13) AMBIGUOUS: location: Truyện không nhắc chuyến đi ryokan Atami; không đủ dữ kiện kết luận mâu thuẫn.
  ⚠ 045.png (doan 15) AMBIGUOUS: location: Truyện không nhắc cảnh chụp ảnh trước onsen ryokan; không đủ dữ kiện kết luận.
  ⚠ 046.png (doan 15) AMBIGUOUS: plot: Ảnh nền điện thoại đi onsen không có trong truyện nhưng không mâu thuẫn
  ⚠ 047.png (doan 15) AMBIGUOUS: plot: Chi tiết sửa xe đạp cho trẻ em không có trong truyện nhưng không mâu thuẫn
  ⚠ 048.png (doan 16) AMBIGUOUS: plot: Cậu bé ôm người thợ mộc không có trong truyện nhưng không mâu thuẫn
  ⚠ 049.png (doan 16) AMBIGUOUS: plot: Chi tiết cảm xúc trong cảnh với cậu bé không có trong văn bản truyện
  ⚠ 054.png (doan 17) AMBIGUOUS: object: Truyện nói hỏi ochazuke và umeboshi, chi tiết tìm đậu phụ không nhắc tới
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: Prompt ghi lon ca phe; truyen noi ro la lon tra nong
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: object: Prompt: Yasuko dat 3 so tiet kiem; Truyen: dat to giay gap duoi bat miso ghi thu nhap
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Prompt: 3 so tiet kiem va con dau; Truyen: to giay gap duoi bat miso ghi thu nhap
  ⚠ 084.png (doan 28) AMBIGUOUS: object: Giay bao gia nha khoa 42 van yen khong xuat hien truc tiep nhung hop boi canh
  ⚠ 089.png (doan 30) AMBIGUOUS: object: 3 so tiet kiem co tag giay ghi muc dich khong neu trong truyen nhung hop boi canh
  ⚠ 095.png (doan 33) AMBIGUOUS: location: Truyện nói thu dọn hành lý tại nhà, prompt ghi ở phòng khách nhà con gái
  ⚠ 096.png (doan 33) AMBIGUOUS: object: Truyện nói bức thư ngắn, prompt thể hiện tin nhắn trên màn hình smartphone
  ⚠ 098.png (doan 34) AMBIGUOUS: plot: Cảnh họp hai bên gia đình đặt tờ giấy không được nêu rõ trong truyện
  ⚠ 099.png (doan 34) AMBIGUOUS: object: Chi tiết bản thoả thuận 3 dòng có đóng dấu không được nêu trong truyện
  ⚠ 100.png (doan 34) AMBIGUOUS: plot: Chi tiết cạo đầu cho chồng ở hiên engawa không có trong truyện
  ⚠ 108.png (doan 40) AMBIGUOUS: plot: truyện không nhắc tin nhắn cáo phó trên điện thoại hay tên cháu nội
  ⚠ 109.png (doan 40) AMBIGUOUS: plot: truyện ghi Shizue ngồi ghế sát tường hàng cuối, prompt vẽ đứng ở phía sau
--- (from logs/B5P_latest.json) warnings 31..41:
  ⚠ 111.png (doan 42) PROMPT_CONFLICT: object: prompt ghi túi ziplock trong suốt, truyện ghi phong bì giấy washi
  ⚠ 112.png (doan 42) PROMPT_CONFLICT: object: prompt ghi tờ khai kết hôn, truyện là cuống giấy tiệm đồ thờ
  ⚠ 113.png (doan 42) PROMPT_CONFLICT: object: prompt ghi tờ khai kết hôn, truyện là cuống giấy tiệm đồ thờ
  ⚠ 114.png (doan 42) PROMPT_CONFLICT: object: prompt ghi tờ khai kết hôn, truyện là cuống giấy tiệm đồ thờ
  ⚠ 115.png (doan 43) AMBIGUOUS: plot: truyện đoạn 43 chỉ nhắc Hiyama rót trà nói chuyện, không nhắc Misawa
  ⚠ 118.png (doan 45) PROMPT_CONFLICT: plot: prompt ghi Misawa ký tên, truyện ghi ủy viên dân sinh ký cùng Hiyama
  ⚠ 122.png (doan 48) AMBIGUOUS: plot: truyen noi dong dau o phong cong chung, prompt ve viet tai ban thap
  ⚠ 124.png (doan 49) PROMPT_CONFLICT: object: truyen viet vao bia sau so tay, prompt ve giay dan tu lanh
  ⚠ 125.png (doan 49) PROMPT_CONFLICT: object: truyen ghi 3 so o bia sau so tay, prompt ve giay dan tu lanh
  ⚠ 126.png (doan 50) PROMPT_CONFLICT: object: truyen ghi so tay mang theo, prompt ve giay dan tu lanh
  ⚠ 128.png (doan 50) PROMPT_CONFLICT: location: truyen Shizue chuan bi 3 chen tra, prompt ve quan teishoku cho khach
conflict files: ['002.png', '022.png', '027.png', '028.png', '074.png', '081.png', '082.png', '111.png', '112.png', '113.png', '114.png', '118.png', '124.png', '125.png', '126.png', '128.png']
5 known: {'022.png': True, '028.png': True, '112.png': True, '113.png': True, '114.png': True}
empty-reason ambiguous: 0
```
→ **5/5 PROMPT_CONFLICT** (kiểm bằng máy từ log: `022.png: True, 028.png: True, 112.png: True, 113.png: True, 114.png: True`), **0 AMBIGUOUS thiếu lý do**.
Số đo bản cuối: `calls=14 · tok_in=39945 · tok_out=10799 · latency=207s · n_checked=128 · n_warn=41 · n_would_block=16 · n_ambiguous=25 · err=0`.

## 5. Step 6 — bản ĐÃ SỬA (`--mode fail`)

### Run 1 — wording NGUYÊN VĂN brief
```
=== B5P: FAIL · 128 prompt / 50 doan · checked=128 warn=31 would_block=8 ambiguous=23 · llm calls=14 tok_in=51752 tok_out=10600 latency=169s err=0
  ✗ semantic: 8 prompt PROMPT_CONFLICT (mode fail)
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: Prompt vẽ tờ 5.000 yên trong khi truyện là 30.000 yên
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: Prompt vẽ cà phê hòa tan, truyện nói pha trà houjicha
  ⚠ 029.png (doan 7) AMBIGUOUS: object: Danh thiếp thợ mộc không nhắc trong truyện nhưng không mâu thuẫn
  ⚠ 030.png (doan 7) AMBIGUOUS: object: Cầm danh thiếp không có trong truyện nhưng không mâu thuẫn
  ⚠ 042.png (doan 13) AMBIGUOUS: plot: Làm dưa muối yuzu-daikon là chi tiết đời thường không có trong truyện
  ⚠ 043.png (doan 13) AMBIGUOUS: plot: Đóng lọ dưa yuzu-daikon là chi tiết đời thường không có trong truyện
  ⚠ 044.png (doan 13) AMBIGUOUS: plot: Chuyến đi suối nước nóng Atami không được nhắc trong truyện
  ⚠ 045.png (doan 15) AMBIGUOUS: plot: Chụp ảnh trước ryokan onsen không được nhắc trong truyện
  ⚠ 046.png (doan 15) AMBIGUOUS: 
  ⚠ 047.png (doan 15) AMBIGUOUS: 
  ⚠ 048.png (doan 16) AMBIGUOUS: 
  ⚠ 049.png (doan 16) AMBIGUOUS: 
  ⚠ 054.png (doan 17) AMBIGUOUS: 
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: lon cà phê vs truyện là lon trà nóng
  ⚠ 079.png (doan 27) AMBIGUOUS: object: Phiếu lương hưu trong túi áo không nhắc trực tiếp trong truyện
  ⚠ 080.png (doan 27) AMBIGUOUS: object: Cặp tài liệu giấy nhỏ không nhắc trực tiếp trong truyện
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: plot: Prompt: Yasuko đưa 3 sổ ngân hàng; Truyện: lót giấy gấp tư thu nhập 4 vạn
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Prompt: 3 sổ ngân hàng và con dấu; Truyện: giấy gấp tư dưới bát miso
  ⚠ 084.png (doan 28) AMBIGUOUS: object: Giấy báo giá nha khoa 42 vạn không nhắc trực tiếp trong truyện
  ⚠ 089.png (doan 30) AMBIGUOUS: object: Nhãn giấy viết tay dán trên sổ không nhắc trực tiếp trong truyện
  ⚠ 095.png (doan 33) AMBIGUOUS: location: Prompt ve o phong con gai, truyen chi noi goi dien cho con gai
  ⚠ 096.png (doan 33) PROMPT_CONFLICT: object: Prompt ve tin nhan smartphone, truyen noi chong gui mau giay
  ⚠ 098.png (doan 34) AMBIGUOUS: plot: Chi tiet hop gia dinh dat to giay khong neu ro trong doan
  ⚠ 099.png (doan 34) AMBIGUOUS: object: To thoa thuan ba dong dong dau khong neu ro trong doan
  ⚠ 100.png (doan 34) AMBIGUOUS: plot: Canh Misawa cao dau cho chong la chi tiet doi thuong minh hoa
  ⚠ 113.png (doan 42) AMBIGUOUS: object: Truyện chỉ đưa biên lai, prompt vẽ cả bài vị hoàn chỉnh trên bàn
  ⚠ 118.png (doan 45) PROMPT_CONFLICT: plot: Truyện: ủy viên dân sinh và Hiyama ký; Prompt: Hiyama và Misawa cùng ký
  ⚠ 124.png (doan 49) AMBIGUOUS: object: giay dan tu lanh khong co trong truyen
  ⚠ 125.png (doan 49) AMBIGUOUS: object: giay ghi so dan bep khong co trong truyen
  ⚠ 126.png (doan 50) AMBIGUOUS: plot: nhin giay dan tu lanh khong co trong truyen
```
Log đủ 31 warning; danh sách conflict: `002, 027, 074, 081, 082, 096, 118, 128`. **Không có 022/028/112/113/114 trong PROMPT_CONFLICT** (113 = AMBIGUOUS). Nhưng `n_would_block=8 > 3` → exit 1.
Đối chiếu tay với script: 002/027/074/118 là lỗi thật; 081/082 gần như chắc là lỗi thật (Yasuko đặt 3 sổ ngân hàng vs truyện「四つ折りの紙」lót dưới bát miso; sổ ngân hàng chỉ xuất hiện ở đoạn 29–30 do Hiyama bày); **096 và 128 là false positive**:
- 096: LLM "Prompt vẽ tin nhắn smartphone, truyện nói chồng gửi mẩu giấy" — script chỉ viết「短い便りが届き」(một tin ngắn), bước rút facts tự suy diễn thành "mẩu giấy viết tay".
- 128: LLM "prompt vẽ quán ăn teishoku vs truyện là nhà Shizue" — script đoạn 50 không nêu địa điểm (「湯呑を三つ揃えて」), bước facts tự điền location=nhà.
→ đúng ca brief cho phép: siết ranh giới AMBIGUOUS vs FAIL (iter 1, §8).

### Run 2 — wording iter 1
```
=== B5P: FAIL · 128 prompt / 50 doan · checked=128 warn=25 would_block=7 ambiguous=18 · llm calls=14 tok_in=51378 tok_out=10453 latency=159s err=0
  ✗ semantic: 7 prompt PROMPT_CONFLICT (mode fail)
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: prompt ghi 5 nghìn yên, truyện ghi ba vạn yên
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: Prompt vẽ cà phê trong khi truyện nêu rõ pha trà houjicha
  ⚠ 042.png (doan 13) AMBIGUOUS: 
  ⚠ 043.png (doan 13) AMBIGUOUS: 
  ⚠ 044.png (doan 13) AMBIGUOUS: 
  ⚠ 045.png (doan 15) AMBIGUOUS: 
  ⚠ 046.png (doan 15) AMBIGUOUS: 
  ⚠ 047.png (doan 15) AMBIGUOUS: 
  ⚠ 048.png (doan 16) AMBIGUOUS: 
  ⚠ 049.png (doan 16) AMBIGUOUS: 
  ⚠ 054.png (doan 17) AMBIGUOUS: 
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: Prompt ghi can of coffee, truyen la lon tra am
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: object: Yasuko lót giấy gấp 4 dưới bát miso, không có tài sản hay 3 sổ ngân hàng
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Truyện là tờ giấy gấp 4 dưới bát miso, không có 3 sổ ngân hàng và con dấu
  ⚠ 095.png (doan 33) AMBIGUOUS: 
  ⚠ 098.png (doan 34) AMBIGUOUS: 
  ⚠ 099.png (doan 34) AMBIGUOUS: 
  ⚠ 100.png (doan 34) AMBIGUOUS: 
  ⚠ 108.png (doan 40) AMBIGUOUS: 
  ⚠ 109.png (doan 40) AMBIGUOUS: 
  ⚠ 111.png (doan 42) PROMPT_CONFLICT: object: truyện là phong bì giấy washi, prompt là túi ziplock
  ⚠ 113.png (doan 42) AMBIGUOUS: 
  ⚠ 118.png (doan 45) PROMPT_CONFLICT: plot: truyện: Ủy viên dân sinh và Hiyama ký; prompt: Misawa ký
  ⚠ 124.png (doan 49) AMBIGUOUS: 
  ⚠ 126.png (doan 50) AMBIGUOUS:
```
→ 096 và 128 hết bị FAIL (đúng mục tiêu); `n_would_block=7` = `002, 027, 074, 081, 082, 111, 118` — **toàn bộ là prompt gốc chưa được Step 6 sửa**, và 111 cũng là lỗi thật (script「和紙の封筒」washi vs prompt "clear ziplock envelope"). Nhược điểm: nhiều AMBIGUOUS có lý do RỖNG (LLM trả `conflicts: []` cho AMBIGUOUS) → danh sách ⚠ vô dụng với người đọc → iter 2.

### Run 3 — wording iter 2 (BẢN CUỐI)
```
=== B5P: FAIL · 128 prompt / 50 doan · checked=128 warn=26 would_block=9 ambiguous=17 · llm calls=14 tok_in=40386 tok_out=10853 latency=181s err=0
  ✗ semantic: 9 prompt PROMPT_CONFLICT (mode fail)
  ⚠ 002.png (doan 1) PROMPT_CONFLICT: money: Prompt vẽ tờ 5.000 yên, truyện ghi rõ bên trong có ba vạn yên.
  ⚠ 027.png (doan 7) PROMPT_CONFLICT: object: prompt vẽ cà phê hòa tan trong khi truyện nêu rõ pha trà houjicha
  ⚠ 042.png (doan 13) AMBIGUOUS: plot: Truyện không nhắc việc làm dưa muối yuzu-daikon, chỉ là chi tiết đời thường
  ⚠ 043.png (doan 13) AMBIGUOUS: plot: Truyện không nhắc việc muối dưa yuzu-daikon vào lọ thủy tinh
  ⚠ 044.png (doan 13) AMBIGUOUS: plot: Truyện không nhắc chuyến đi ryokan suối nước nóng Atami
  ⚠ 045.png (doan 15) AMBIGUOUS: plot: Truyện không nhắc việc chụp ảnh trước cổng onsen ryokan
  ⚠ 046.png (doan 15) AMBIGUOUS: plot: Ảnh nền đôi ở onsen không được nhắc trong truyện
  ⚠ 047.png (doan 15) AMBIGUOUS: plot: Truyện không nhắc việc sửa xe đạp trẻ em trong vườn
  ⚠ 048.png (doan 16) AMBIGUOUS: character_state: Nhân vật bé trai ôm Kokichi không xuất hiện trong truyện
  ⚠ 054.png (doan 17) AMBIGUOUS: object: Truyện chỉ nói xin ochazuke và umeboshi, không nhắc tofu
  ⚠ 074.png (doan 25) PROMPT_CONFLICT: object: prompt vẽ lon cà phê trong khi truyện nói lon trà ấm
  ⚠ 081.png (doan 27) PROMPT_CONFLICT: object: Truyện là tờ giấy gấp tư dưới bát súp miso, không phải 3 sổ ngân hàng và con dấu
  ⚠ 082.png (doan 27) PROMPT_CONFLICT: object: Truyện là tờ giấy gấp tư dưới bát súp miso, không phải 3 sổ ngân hàng và con dấu
  ⚠ 089.png (doan 30) AMBIGUOUS: object: Truyện không nói rõ số lượng sổ ngân hàng và nhãn dán mục đích
  ⚠ 095.png (doan 33) AMBIGUOUS: location: Truyện không nói rõ Misawa dọn hành lý ở phòng con gái
  ⚠ 098.png (doan 34) AMBIGUOUS: location: Truyện nói tập hợp tại Tòa thị chính, không rõ ở phòng khách
  ⚠ 099.png (doan 34) AMBIGUOUS: object: Truyện chỉ nhắc tờ giấy, không mô tả thỏa thuận 3 dòng đóng dấu
  ⚠ 100.png (doan 34) AMBIGUOUS: plot: Cảnh cạo đầu ngoài hiên là chi tiết minh họa thêm, truyện không nêu
  ⚠ 108.png (doan 40) AMBIGUOUS: plot: Truyện chỉ nhắc con trai gọi điện, không nhắc tin nhắn cáo phó trên điện thoại
  ⚠ 109.png (doan 40) AMBIGUOUS: plot: Truyện nói Shizue ngồi ghế sát tường, prompt mô tả bà đứng ở phía sau
  ⚠ 111.png (doan 42) PROMPT_CONFLICT: object: Prompt nói túi ziplock trong suốt, truyện nói phong bì giấy washi
  ⚠ 113.png (doan 42) PROMPT_CONFLICT: plot: Prompt vẽ bài vị gỗ hoàn chỉnh, truyện chỉ có giấy biên nhận đặt làm bài vị
  ⚠ 118.png (doan 45) PROMPT_CONFLICT: plot: Ủy viên dân sinh và Hiyama ký tên đóng dấu, prompt vẽ Misawa ký
  ⚠ 124.png (doan 49) AMBIGUOUS: object: truyện không nhắc giấy note dán tủ lạnh, không đủ dữ kiện
  ⚠ 125.png (doan 49) PROMPT_CONFLICT: object: truyện viết 3 số đt vào bìa sau sổ tay, prompt vẽ giấy note
  ⚠ 126.png (doan 50) AMBIGUOUS: object: truyện không nhắc nhìn note tủ lạnh, đoạn 50 nhắc bìa sổ tay
conflict files: ['002.png', '027.png', '074.png', '081.png', '082.png', '111.png', '113.png', '118.png', '125.png']
5 known as conflict: {'022.png': False, '028.png': False, '112.png': False, '113.png': True, '114.png': False}
empty-reason ambiguous: 0
keys: ['ambiguous', 'batch', 'chunk', 'conflicts', 'llm', 'n_ambiguous', 'n_checked', 'n_warn', 'n_would_block', 'ran', 'would_block']
```
→ exit 1, `n_would_block=9` = `002, 027, 074, 081, 082, 111, 113, 118, 125`. 0 AMBIGUOUS thiếu lý do. **022/028/112/114 không bị PROMPT_CONFLICT.**
**113.png (prompt ĐÃ SỬA) bị FAIL ở run này** (run 1, run 2 đều AMBIGUOUS) — lý do LLM: *"Prompt vẽ bài vị gỗ hoàn chỉnh, truyện chỉ có giấy biên nhận đặt làm bài vị"*. Prompt 113 đã sửa: *"carved wooden Buddhist memorial tablet (ihai) inscription column showing two names carved side by side in gold lettering"*; script đoạn 42:「封筒の中には、仏具店の控えがあり…彫り字の欄には、竹下幸吉と、藤田静江と、二人の名前が、あの人の手で、並んでおりました」— tức hai tên viết TAY trong cột khắc chữ của TỜ ĐẶT HÀNG, bài vị chưa xuất hiện. Lý do LLM có cơ sở, không phải false positive rõ ràng; ca này nằm đúng biên AMBIGUOUS/FAIL nên lật qua lại giữa các run (temperature=0 nhưng gemini vẫn không tất định + facts mỗi run khác). **Không chạy iter 3** — sửa wording thêm để ép 1 ca đang lật ngẫu nhiên là overfit vào tập này, và không giải quyết nguyên nhân chính (8 lỗi thật).
Số đo bản cuối: `calls=14 · tok_in=40386 · tok_out=10853 · latency=181s · n_checked=128 · n_warn=26 · n_would_block=9 · n_ambiguous=17 · err=0`.

Ghi chú: sau run 3 có chạy thêm `--no-llm` trên bản fixed để kiểm khoá `metrics.semantic` (§7) nên `logs/B5P_latest.json` của bản fixed hiện là bản `--no-llm`; kết quả Step 6 run 3 nằm ở `logs/B5P_attempt_001.json`.

## 6. Kết luận về ngưỡng `n_would_block ≤ 3` của Step 6
Không đạt được và **không nên** đạt bằng cách sửa wording: brief giả định file prompt thật chỉ có 5 lỗi (022/028/112-114), nhưng B5P tìm thêm **8 lỗi thật khác** trong `img_prompts.txt` của STT3 mà Step 6 không sửa (đã đối chiếu tay từng cái với `script.txt`):

| Prompt | Prompt vẽ | Script nói | Loại |
|---|---|---|---|
| 002 | tờ 5.000 yên | 三万円 trong phong bì 香典 (đoạn 1) | money |
| 027 | instant coffee (anh em của 028) | ほうじ茶 + 羊羹 (đoạn 7) | object |
| 054 | tìm đậu phụ | 梅干し / お茶漬け (đoạn 17) | object (run cuối chấm AMBIGUOUS) |
| 074 | lon cà phê | 温かいお茶の缶 từ máy bán (đoạn 25) | object |
| 081/082 | Yasuko đặt 3 sổ ngân hàng + con dấu | 四つ折りの紙 lót dưới bát miso (đoạn 27) | object |
| 111 | clear ziplock envelope | 和紙の封筒 (đoạn 42) | object |
| 118 | Hiyama + Misawa ký làm chứng | 民生委員 + Hiyama ký (đoạn 45) | plot/count |
| 124/125/126 | note dán tủ lạnh | 手帳の裏表紙 bìa sau sổ tay (đoạn 49–50) | object (lật FAIL/AMBIGUOUS) |

Đây là **việc nội dung của lane** (sửa prompt trong file thật STT3), ngoài phạm vi task này — giống như brief đã nói về 022/028. Sau khi lane sửa các prompt trên, kỳ vọng `n_would_block ≤ 3` là hợp lý.

## 7. Self-review
- `kiem_prompts` không chấm mapping (code giữ nguyên brief; prompt LLM nói rõ "KHONG cham viec prompt co dung doan da gan hay khong"). AMBIGUOUS không bao giờ vào `would_block` (`would_block=bool(conflicts)`, test `test_cli_ambiguous_khong_chan`).
- `metrics.semantic` luôn có đủ 11 khoá `ran, n_checked, n_warn, n_would_block, n_ambiguous, would_block, batch, chunk, conflicts, ambiguous, llm` — kiểm bằng máy cả với `--no-llm` (`missing: set()`, `ran=False`, `llm={calls:0,...}`).
- **Số lời gọi LLM thật cho tập 128 prompt / 50 đoạn: 14** (= 5 lời gọi facts [50/10] + 9 lời gọi kiểm prompt [128/15]) — ổn định ở cả 6 lần chạy; tok_in 39–52k, tok_out ≈10.5–11.9k, latency 159–235 s, err=0.
- Không làm gì ngoài brief; không sửa test; không hạ ngưỡng; không sửa file dùng chung.

## 8. Wording iterations (before → after) — chỉ trong `_prompt_facts` / `_prompt_kiem`
Tổng cộng **2** lần (giới hạn 3). Diff đầy đủ so với brief (`difflib` brief → final):

**Iter 1a — `_prompt_facts` (chống suy diễn ở bước rút facts; gây ra 096/128):**
```
- "Tohoku') vi anh minh hoa se bi doi chieu tung chi tiet.\n"
+ "Tohoku') vi anh minh hoa se bi doi chieu tung chi tiet. CHI ghi dung nhung gi van ban NOI; KHONG "
+ "suy dien them chat lieu/hinh thuc/dia diem/mua ma van ban khong neu (vd van ban chi noi 'tin nhan "
+ "ngan' thi ghi 'tin nhan ngan', khong tu them 'giay viet tay'; doan khong neu dia diem thi de "
+ "location rong).\n"
```
**Iter 1b — `_prompt_kiem` (ranh giới AMBIGUOUS vs FAIL: facts im lặng ≠ mâu thuẫn):**
```
  "sai mua/thoi diem; sai so nguoi/quan he.\n"
+ "CHI FAIL khi facts NOI RO mot gia tri KHAC cho CUNG chi tiet do (cung mot canh/do vat/giay to/dia "
+ "diem/nguoi thuc hien). Neu facts IM LANG ve chi tiet do (khong nhac toi; location rong hoac chi la "
+ "suy doan tu boi canh; chi tiet co the thuoc doan khac cua truyen) thi la AMBIGUOUS, KHONG FAIL.\n"
  "AMBIGUOUS khi prompt co chi tiet khong xuat hien trong truyen nhung KHONG mau thuan (minh hoa "
```
**Iter 2 — `_prompt_kiem` (bắt buộc có lý do cho FAIL/AMBIGUOUS; trước đó ~50% AMBIGUOUS trả `conflicts: []` → dòng ⚠ rỗng):**
```
- "\"detail\": \"<=20 tu, neu ro prompt noi gi vs truyen noi gi>\"}]}]\n"
+ "\"detail\": \"<=20 tu, neu ro prompt noi gi vs truyen noi gi>\"}]}]. Voi FAIL va AMBIGUOUS, "
+ "conflicts LUON co it nhat 1 phan tu neu ly do (AMBIGUOUS: vi sao khong ket luan duoc); "
+ "PASS thi conflicts = [].\n"
```
Recall 5/5 ở Step 5 được kiểm lại sau MỖI iteration (run 2, run 3) — không mất ca nào.

## 9. Deviations / typos brief
- Brief không có typo phải sửa. Lệnh `--slug ..\scratch_analysis\...` chạy trong Bash bị nuốt `\` → dùng `/` (không phải lỗi brief; PowerShell/cmd chạy nguyên văn được).
- Step 2 (thấy `ModuleNotFoundError`) không tái hiện vì file đã có sẵn từ phiên trước (§1b).
- Bỏ wording của phiên trước (không có bằng chứng nó cần thiết; brief gốc đã đủ recall). Bản đó lưu ở scratchpad phiên này, không nằm trong project.
- Không tạo `_bak_` vì không sửa file có sẵn nào của project (file B5P là deliverable của chính task này).

## 10. Concerns
1. **`n_would_block ≤ 3` ở Step 6 không đạt (9)** — nguyên nhân chính là 8 lỗi thật khác trong prompt gốc STT3 (§6), không phải cổng chấm sai. Cần lane sửa nội dung `img_prompts.txt` của tập thật (002, 022, 027, 028, 054, 074, 081, 082, 111, 118, 124–126) rồi chạy lại để có số false-positive thật.
2. **Kết quả không tất định giữa các run** dù `temperature=0`: cùng wording, 044/045/054/096/113/124–126/128 lật giữa FAIL↔AMBIGUOUS. Đúng tinh thần brief "WARN-only 2 tập đầu để đo false-positive" — chưa nên bật `--mode fail` cho B5P.
3. **False positive cấu trúc còn lại**: prompt minh hoạ chi tiết nằm ở ĐOẠN KHÁC của truyện (Atami ở đoạn 41, sổ ngân hàng ở đoạn 29–30) trong khi LLM chỉ thấy lát facts ±1 quanh đoạn được map. Iter 1b đẩy phần lớn về AMBIGUOUS nhưng không triệt để. Hướng sau (ngoài brief): thêm 1 danh sách "địa danh/đồ vật toàn truyện" rút từ `story_facts.json` vào mỗi batch, giá ~vài trăm token/batch.
4. Console chỉ in 30 warning đầu (`warnings[:30]` theo brief) — với tập 41 warning thì 112–114 rơi ra ngoài console; phải đọc `logs/B5P_latest.json`. Không sửa vì brief quy định vậy, chỉ lưu ý.
5. 113 (prompt "đã sửa") vẫn bị FAIL 1/3 run với lý do có cơ sở (§5 run 3) — bản thân prompt 113 sửa lại chưa sát script (vẽ bài vị hoàn chỉnh khắc chữ vàng trong khi truyện chỉ có tờ đặt làm với tên viết tay). Đề xuất lane sửa prompt thay vì nới cổng.
