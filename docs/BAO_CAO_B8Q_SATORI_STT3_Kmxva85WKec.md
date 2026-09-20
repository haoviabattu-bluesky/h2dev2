# BÁO CÁO QC KHỚP LỜI — SATORI STT 3 (bản hybrid)

Ngày: 2026-09-17
Lane: satori / Lopezzapa68
STT: 3
Slug: simbot2-03-Kmxva85WKec
Bản dựng: compositor hybrid trong `scratch_analysis/stock_hybrid_satori_stt3/output/final_stock_mix.mp4`

## 1. Kết luận ngắn

- Cổng KỸ THUẬT của bản hybrid: **ĐẠT** (128 slot, tổng timeline = audio 1952,43s, decode sạch, 1920×1080, có audio).
- Cổng NỘI DUNG (QC model vision): **KHÔNG ĐẠT** — `ẢNH LỆCH LỜI: trung bình 2,7/5, 7/14 mốc ≤2` (bản dùng neo thật) và `3,0/5` (bản chia theo nhóm đoạn).
- Nguyên nhân KHÔNG phải ở máy ghép: **`anchors.txt` đúng 120/120** — mỗi neo tra ra ĐÚNG câu của nó trong `voice_paced.srt` (đã kiểm bằng dò vị trí ký tự trên toàn bộ SRT, không phải so khớp mờ).
- Nghi vấn chính: **`img_doan.txt` / `img_prompts.txt` gán ảnh vào SAI ĐOẠN** (ảnh vẽ đúng nội dung nhưng thuộc cảnh khác của câu chuyện). Cần Claude Code kiểm tra ở bước 1.

## 2. Lệnh QC đã chạy (nguyên văn)

```bash
env -u PYTHONPATH py -3.13 pipeline/qc_visual.py video \
  --mp4 "scratch_analysis/stock_hybrid_satori_stt3/output/final_stock_mix.mp4" \
  --srt "assets/satori_jp/simbot2-03-Kmxva85WKec/voice_paced.srt" \
  --audio-sec 1952.43 --sample 14 --no-sub
```

Output thật:

```text
=== VIDEO: 8 VẤN ĐỀ
   ✗ ẢNH LỆCH LỜI: trung bình 2.7/5, 7/14 mốc ≤2
   ✗   348s (1/5): The visual of preparing sushi rice has no relation to preten | lời: 何を言うのかと、怒ってみせましたが、
   ✗   487s (1/5): The quiet kitchen scene with two people does not match a liv | lời: 宴は賑やかに、過ぎてゆきました。
   ✗   768s (2/5): A relaxed photo-taking moment contradicts rushing out in a h | lời: 湯呑を片付け る、余裕もなく、飛び出したのでした。
   ✗   907s (1/5): The image shows a medical emergency/collapse, not someone yi | lời: 長男さんはその都度、順番を譲って、下さいました。
   ✗   1046s (2/5): The image shows a somber hospital grief scene, mismatched wi | lời: 貯金もそれなりに、蓄えがございました。
   ✗   1462s (1/5): Shows an elderly woman packing a bag in a bedroom, not retur | lời: 静かに立ち上がると、相談室へ戻りました。
   ✗   1745s (1/5): Narration describes a young clerk at a service counter, but  | lời: 窓口の若い方が、書類を整えまして、
```

(Tiếng Nhật trong log bị model in ngắt dòng nên đọc hơi lệch — nội dung mốc giây là chính xác.)

## 3. Bằng chứng neo thời gian ĐÚNG (không phải lỗi máy ghép)

Kiểm bằng 2 cách độc lập:

**(a) Bản chia theo nhóm đoạn** (`img_doan.txt` + phân bố đều trong đoạn) → `3,0/5`.
**(b) Bản dùng `anchors.txt` (neo thật)** → `2,7/5`.

Hai bản cho **cùng danh sách mốc yếu** ⇒ công thức thời gian không phải nguyên nhân.

**(c) `anchors.txt` tra ngược về `voice_paced.srt` bằng vị trí ký tự trên toàn bộ SRT:** 120/120 neo tra ra ĐÚNG câu của chính nó, ví dụ:

| ảnh | đoạn (`img_doan.txt`) | neo tra ra (giây) | câu neo | câu SRT tại mốc đó |
|---|---|---|---|---|
| 027.png | 11 | 481,4 | 座敷はどっと沸き、 | 座敷はどっと沸き、 |
| 045.png | 18 | 761,8 | 台所の急須は、湯気を立てたままで、 | (giống) |
| 056.png | 23 | 898,6 | 集中治療室の面会は、一日に二回きりで、十分だけ許され、 | (giống) |
| 066.png | 27 | 1040,4 | 桧山さんの年金は、月々十八万ほど、 | (giống) |
| 095.png | 38 | 1448,0 | 命の仕舞いを機械の、管に預けて伸ばすのは、 | (giống) |
| 115.png | 45 | 1735,4 | 書類の一枚に、 | (giống) |

⇒ Neo khớp tuyệt đối. Ảnh được đặt đúng tại mốc của câu neo của nó.

## 4. Bằng chứng nội dung ảnh SAI ĐOẠN (nghi vấn bước 1)

Tại mỗi mốc yếu, ảnh hiện đúng ở mốc neo của nó, nhưng NỘI DUNG ảnh (theo prompt) thuộc cảnh KHÁC:

| mốc QC | slot | loại | file | lời đang đọc tại mốc | prompt ảnh (rút gọn) | nhận định |
|---|---|---|---|---|---|---|
| 348s | 19 | stock | L019_pexels_apersonusingchopsticks.mp4 | 何を言うのかと、怒ってみせましたが、 | (clip stock: ăn cơm/đũa) | clip stock không khớp đoạn giận |
| 487s | 27 | AI | 027.png | 宴は賑やかに、過ぎてゆきました。 | @REF kitchen counter, đưa cốc cà phê cho thợ mộc | ảnh cảnh bếp, không phải cảnh tiệc |
| 768s | 45 | AI | 045.png | 湯呑を片付ける、余裕もなく、飛び出したのでした。 | @REF nâng điện thoại chụp ảnh trước ryokan | ảnh chụp ảnh du lịch, không phải vội vã rời đi |
| 907s | 56 | AI | 056.png | 長男さんはその都度、順番を譲って、下さいました。 | @REF quỳ cạnh người ngã ở ngưỡng cửa, điện thoại bàn | ảnh cảnh CẤP CỨU (thuộc đoạn tai biến, khoảng 11:39) |
| 1046s | 66 | AI | 066.png | 貯金もそれなりに、蓄えがございました。 | @REF mắt rưng rưng ở hành lang bệnh viện | ảnh cảnh bệnh viện, không phải chuyện tiền tiết kiệm |
| 1462s | 95 | AI | 095.png | 静かに立ち上がると、相談室へ戻りました。 | Misawa xếp túi qua đêm ở phòng khách | ảnh Misawa xếp túi, không phải quay lại phòng tư vấn |
| 1745s | 115 | AI | 115.png | 窓口の若い方が、書類を整えまして、 | Hiyama rót trà ở bàn teishoku | ảnh rót trà, không phải quầy tiếp nhận giấy tờ |

Mẫu hình chung: ảnh KHÔNG sai nội dung vẽ, mà **bị gán vào đoạn khác với đoạn mà nó được vẽ cho** — tức `img_doan.txt` (hoặc chính `img_prompts.txt`) lệch ở các cụm này.

## 5. Việc Claude Code cần kiểm tra (đúng thứ tự)

1. Mở `img_doan.txt` — xác nhận số đoạn gán cho `027.png`, `045.png`, `056.png`, `066.png`, `095.png`, `115.png`, `118-128.png`.
2. Mở `script.txt` — đọc NGUYÊN VĂN đoạn mà các ảnh trên đang được gán, so với prompt của chính ảnh đó trong `img_prompts.txt`.
3. Xác định đoạn ĐÚNG cho từng ảnh (đoạn có câu mô tả đúng cảnh mà prompt vẽ). Ví dụ: `056.png` (cảnh cấp cứu tại ngưỡng cửa) phải thuộc đoạn "十月二十日の未明、まだ五時前" (khoảng 11:39), không phải đoạn "長男さんはその都度".
4. Kiểm tra thêm: `anchors.txt` KHÔNG được sửa nếu chỉ đổi `img_doan.txt` — phải chạy lại `sinh_neo.py` sau khi sửa, để neo sinh lại theo đoạn mới.
5. Với mốc 348s là SLOT STOCK: xem `stock/manifest.csv` dòng `prompt_line=19` — nếu nội dung đoạn 19 là "giận/管" thì clip ăn cơm là chọn sai; đề xuất thay bằng ảnh AI hoặc bỏ stock tại slot này.
6. Sau khi sửa, chạy lại compositor **trong `scratch_analysis/`** (không sửa pipeline chính), rồi chạy lại QC bằng lệnh ở mục 2.

## 6. Điều cấm

1. Không sửa `pipeline/` dùng chung (`assemble.py`, `render_engine.py`, `chay_buoc3.py`).
2. Không sửa `script.txt`, `img_prompts.txt`, `characters.json`, `img/`.
3. Không `--force-qc`.
4. Không tự đổi số `img_doan.txt` ngoài "phạm vi khả thi" (`[p_truoc, p_sau]`, thứ tự không-giảm) — đổi ẩu sẽ làm ảnh đi lùi.
5. Không giao hàng, không ghi cột G/H cho tới khi QC đạt và chủ dự án duyệt.
6. Không xoá bản dựng hiện tại (giữ để đối chiếu).

## 7. Trạng thái Hermes

- Bản dựng hybrid nằm tại: `scratch_analysis/stock_hybrid_satori_stt3/output/final_stock_mix.mp4`
- CHƯA tạo thư mục `CHANEL\Lopezzapa68\ep03-...`, CHƯA ghi Sheet.
- Ảnh/audio/anchors/script của tập KHÔNG bị sửa.

## 8. CẬP NHẬT (lần dựng sau, đã loại trừ hoàn toàn lỗi máy ghép)

Bản dựng lại với timing khớp TUYỆT ĐỐI:

```text
128 slot · sum(target) = sum(actual) = 1952.4300s = audio (lệch 0.0)
slot 46 & 91 trước bị kẹp 0.01s (2 ảnh cùng neo 1 câu) → đã mượn đủ MIN_SLOT 2.5s
min slot = 2.50s · không slot nào lệch > 0.15s · decode sạch · 1920×1080
```

QC lại: **2.8/5, 7/14 mốc ≤2 — ĐÚNG 7 MỐC CŨ** (348 / 487 / 768 / 907 / 1046 / 1462 / 1745s).

⇒ Ba bản dựng khác nhau về cách tính mốc (chia nhóm đoạn → anchors → anchors + MIN_SLOT fix) đều cho CÙNG danh sách mốc yếu. **Nguyên nhân nằm ở dữ liệu bước 1, không phải ở compositor.**

Nhận xét model cho 907s nói rõ: cảnh người già NGÃ TRONG CẤP CỨU đang nằm ở câu `長男さんはその都度、順番を譲って、下さいました。` — trong khi cảnh cấp cứu phải thuộc đoạn tai biến (`十月二十日の未明、まだ五時前`). Đây là bằng chứng trực tiếp cho việc `img_doan.txt` gán ảnh lệch đoạn.

- Xác minh thêm: `pipeline/render_engine.py` bị sửa lúc 2026-09-17 18:13 bởi **tiến trình khác** (không phải Hermes) — Hermes giữ nguyên, không hoàn tác. `assemble.py` và `chay_buoc3.py` không đổi.

## 9. Ghi báo cáo — nối vào CUỐI file này

```text
[CLAUDE] 2026-09-18 027.png: đoạn cũ=11 (宴は賑やかに/tiệc rượu) → đoạn đúng=7. Prompt "handing coffee
  to carpenter across kitchen counter" khớp câu script đoạn 7 "困った私は、お湯を沸かしました。ほうじ茶を
  淹れて...両手で包み込み" (bà pha trà mời thợ mộc sau khi ông từ chối nhận tiền sửa ống nước) — KHÔNG
  phải cảnh tiệc rượu ở nhà hàng (đoạn 11). Neo mới: "馴染みからは、頂けませんと断られ、".

[CLAUDE] 2026-09-18 045.png: đoạn cũ=18 (collapse) → đoạn đúng=15 (best-effort). Prompt "chụp ảnh bạn
  đời trước cổng ryokan onsen Atami" KHÔNG khớp bất kỳ đoạn nào trong 50 đoạn script (đã grep toàn bộ
  script.txt tìm "温泉/旅館" — không có). Đoạn 41 có nhắc lại hồi tưởng "熱海の夕餉" (bữa tối Atami) như
  kỷ niệm đẹp, xác nhận chuyến đi này CÓ THẬT trong câu chuyện nhưng không được kể chi tiết ở đoạn nào —
  đây là ảnh minh hoạ "7 năm hạnh phúc" không neo được câu chữ cụ thể. Đặt tạm ở đoạn 15 (mùa xuân, giai
  đoạn hạnh phúc) do giới hạn số cue của đoạn 12 gốc (chỉ ~6 cue cho 3 câu, không đủ chỗ cho 11 ảnh dồn
  vào 1 đoạn). Neo mới: "同居三年目の春、" — không sai giọng cảm xúc, nhưng KHÔNG phải khớp nghĩa đen.

[CLAUDE] 2026-09-18 056.png: đoạn cũ=23 (ICU visits) → đoạn đúng=18. Prompt "quỳ bên hành lang cạnh
  bạn đời ngã, điện thoại bàn tay run" khớp NGUYÊN VĂN đoạn 18 "あの人は俯せに、倒れておりました。震える手で
  電話し、救急車を呼びまして". Neo mới: "それから三十分ほど、時間が過ぎた頃、" — đúng câu MỞ ĐẦU đoạn 18.

[CLAUDE] 2026-09-18 066.png: đoạn cũ=27 (tiền lương hưu ông Hiyama) → đoạn đúng=22. Prompt "mắt rưng
  rưng nghe con trai cảm ơn ở hành lang bệnh viện" khớp NGUYÊN VĂN đoạn 22 "長男さんは頭を下げ、あなたがいた
  から、父は助かりました". Neo mới: "長男さんは頭を下げ、あなたが" — đúng câu mở đầu đoạn 22.

[CLAUDE] 2026-09-18 095.png: đoạn cũ=38 (lời đáp cho con trai) → đoạn đúng=33. Prompt "Misawa xếp túi
  qua đêm ở phòng khách nhà con gái" khớp NGUYÊN VĂN đoạn 33 "実の娘に泣きながら、電話をかけましても...荷造り
  を進める中". Neo mới: "実の娘に泣きながら、電話をかけましても、" — đúng câu mở đầu đoạn 33.

[CLAUDE] 2026-09-18 115.png: đoạn cũ=45 (chữ ký nhân chứng) → đoạn đúng=43. Prompt "ông Hiyama rót trà
  cho Shizue ở bàn teishoku, giải thích, Misawa lắng nghe" khớp NGUYÊN VĂN đoạn 43 "翌週の水曜日、定食屋の
  席で、桧山さんがお茶を、注ぎながらそっと、教えて下さいました". Neo mới: "翌週の水曜日、" — đúng câu mở đầu đoạn 43.

[CLAUDE] 2026-09-18 slot stock 19 (348s): đoạn cũ=8 (giọng nói to qua điện thoại) → đoạn đúng=5. Prompt
  dòng 19 "ba đôi đũa khựng giữa không" khớp NGUYÊN VĂN đoạn 5 "再婚で一番、怖かったのは何か、という問いかけに、
  三人の箸が、止まりました" (câu hỏi về nỗi sợ tái hôn làm 3 đôi đũa khựng lại) — clip stock
  L019_pexels_apersonusingchopsticks.mp4 (người dùng đũa) khớp đúng cảnh. Không cần đổi manifest.csv/
  stock_plan.tsv, chỉ cần sửa img_doan.txt — compositor tự tính lại mốc từ đoạn mới.

[CLAUDE] 2026-09-18 ĐÃ SỬA GÌ: PHÁT HIỆN THÊM ngoài 6 ảnh trên — toàn bộ `img_doan.txt` (128 dòng) được
  sinh bởi thuật toán CƠ HỌC chia đều luân phiên 2-3 ảnh/đoạn (không đọc nội dung: đoạn 1→2 ảnh, đoạn
  2→3 ảnh, đoạn 3→2 ảnh... xen kẽ đều suốt 50 đoạn, không hề khớp mật độ nội dung thật), không phải chỉ
  6 ảnh bị lệch cục bộ. Đã đọc lại TOÀN BỘ 50 đoạn `script.txt` + 128 dòng `img_prompts.txt`, tự tay gán
  lại từng ảnh vào đúng đoạn theo nội dung (đối chiếu tên riêng, số tiền, mốc thời gian, câu thoại), giữ
  thứ tự không giảm. Đã ghi đè `img_doan.txt` (128 dòng, đã kiểm monotonic bằng script), chạy lại
  `py -3.13 sinh_neo.py --slug ...` → **ĐẠT lần đầu tiên với bản đồ đúng nội dung: 120/120 neo hợp lệ**
  (120 vì 8 dòng STOCK thật không nằm trong `img/`, đúng thiết kế). Đã đối chiếu lại cả 6 ảnh bị QC nêu
  tên — 5/6 khớp NGUYÊN VĂN câu mở đầu đoạn, 1/6 (045.png) là ảnh minh hoạ không có câu neo văn học,
  đặt best-effort (xem ghi chú ở trên).
  KHÔNG đụng vào `script.txt`, `img_prompts.txt`, `characters.json`, `img/` — chỉ sửa `img_doan.txt`
  rồi chạy lại `sinh_neo.py` để tự sinh `anchors.txt` mới, đúng quy trình mục 6 điều cấm.

[CLAUDE] 2026-09-18 PHÁT HIỆN PHỤ (không tự sửa, cần chủ dự án quyết định): dòng ảnh 112-114 trong
  `img_prompts.txt` mô tả "tờ khai ĐĂNG KÝ KẾT HÔN (婚姻届) đã có dấu triện chồng, đang chờ chữ ký nhân
  chứng" — nhưng toàn bộ 50 đoạn `script.txt` KHÔNG hề nhắc tới việc đăng ký kết hôn chính thức ở bất kỳ
  đâu (cốt truyện xuyên suốt là họ CHƯA BAO GIỜ đăng ký hôn thú, kể cả tới lúc ông mất — đó chính là nút
  thắt của cả câu chuyện). Nội dung 3 dòng prompt này mâu thuẫn với chính cốt truyện, nhiều khả năng là
  lỗi khi viết `img_prompts.txt` (có thể sót lại ý tưởng bản nháp cũ). Đã tạm gán đoạn 42 (gần nhất về
  ngữ cảnh: con trai mang di vật tới sau 49 ngày) vì không được phép sửa `img_prompts.txt` — đề nghị chủ
  dự án xem lại 3 dòng này, có thể cần viết lại nội dung ảnh (đổi "marriage registration form" thành
  đúng "vị bài thờ đôi/位牌" như trong đoạn 42 mô tả) rồi gen lại 3 ảnh đó.

[CLAUDE] 2026-09-18 KẾT LUẬN: đã sửa xong `img_doan.txt` + `anchors.txt` cho toàn bộ 128 ảnh (không chỉ
  6 ảnh nêu tên). Đề nghị Hermes dựng lại `final_stock_mix.mp4` trong `scratch_analysis/` rồi chạy lại
  đúng lệnh QC ở mục 2 để xác nhận điểm khớp lời cải thiện trên diện rộng (không chỉ 7 mốc cũ). Còn 1
  việc cần chủ dự án quyết định: 3 dòng ảnh 112-114 nội dung mâu thuẫn cốt truyện (xem phát hiện phụ ở
  trên) — chưa sửa vì ngoài phạm vi cho phép của báo cáo này.
```

[HERMES] 2026-09-18 VIỆC 1: OK — nhận đúng 2 ảnh vẽ lại. `img/112.png` (08:30) và `img/114.png` (08:32)
  mới; `img/113.png` KHÔNG có (slot 113 là STOCK, đúng thiết kế §3b). Đã soi bằng vision: 112 = phiếu
  「仏具のやま田 / 檜夫婦位牌」 + cặp bài vị trong túi; 114 = bà cầm phiếu trên tay. Khớp đoạn 42
  「封筒の中には、仏具店の控えがあり、桧材の夫婦位牌が、確かに承られて、おりました。」 `img/` tổng vẫn 120 PNG.

[HERMES] 2026-09-18 VIỆC 2: OK — dựng lại compositor hybrid trong `scratch_analysis/`, phát hiện và sửa
  3 lỗi của TOOL (không phải dữ liệu bước 1):
  (a) Mốc thời gian lấy từ `anchors.txt` (neo thật) thay vì chia đều theo nhóm đoạn.
  (b) `MIN_SLOT` chưa áp dụng: slot 46 & 91 cùng neo 1 câu → dài 0,01s, ảnh gần như không hiện. Nay mượn
      của slot trước, tổng KHÔNG đổi.
  (c) Cắt slot bằng `-t <giây>` bị làm tròn về bội số 1/30s ở TỪNG slot → sai số cộng dồn (bản cũ lệch
      0,10s; bản STT5 đã giao lệch 0,19s). Nay tính ranh giới theo SỐ FRAME tuyệt đối rồi cắt bằng
      `-frames:v`. Kèm đó: `tpad=stop_mode=clone` phải clone DƯ (d+1.0s) vì `sec()` đọc duration
      container đã làm tròn LÊN — clone đúng phần thiếu vẫn hụt 1-2 frame (đo thật slot 73 hụt 2 frame,
      slot 94 hụt 1 frame).

[HERMES] 2026-09-18 VIỆC 3: OK — ad-hoc verification 14/14 PASS (không phải test suite chính thức):
  ```text
  sum(actual)=1952.420s vs audio=1952.430s (lệch 0.010s, spec ≤0.05s)
  slot_frames = 58573 = audio_frames 58573 (khớp tuyệt đối) · min slot 2.500s
  120 ai + 8 stock · slot 112/114 = ai · slot 113 = stock · decode sạch
  1920x1080 + audio · EP img vẫn 120 PNG · không final.mp4 trong EP · 0 slot lệch frame
  ```

[HERMES] 2026-09-18 VIỆC 4: OK — QC model (`qc_visual.py video --sample 14 --no-sub`): **ĐẠT**,
  `sync_score 3.86`, `problems: []`, 2/14 mốc ≤2 (dưới ngưỡng hỏng 30%). Hai mốc 768s/1046s là slot
  **AI 58/79** (không phải stock) — soi khung bằng mắt: 768s = tay xếp dép vào túi (hợp ngữ cảnh "vội
  ra đi"), 1046s = ông cầm phong bì có vệt nước mắt (hợp "có chút tiền để dành"). Cả 8 slot stock đều
  `drift = ±0.00s` ⇒ cổng §5b (drift) không có slot nào cần chấm riêng.
  Lưu ý phương pháp: QC này có DAO ĐỘNG giữa các lần chạy — cùng 1 file, 4 lần cho 3.93 / 3.86 / 3.93 /
  4.00, và mốc 767.6s lúc bị 2/5 lúc không. Kết luận "lỗi bước 1" ở mục 8 vẫn ĐÚNG (Claude xác nhận
  `img_doan.txt` sinh cơ học chia đều 2-3 ảnh/đoạn), nhưng điểm tuyệt đối thì không nên đọc như số cứng.

[HERMES] 2026-09-18 VIỆC 5: OK — đã bàn giao (chỉ sau khi QC ĐẠT + anh xác nhận "tiếp tục làm video"):
  `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep03-simbot2-03-Kmxva85WKec\`
  `final.mp4` (182.4 MB) · `thumbnail.png` · `listting.txt` (chép NGUYÊN VĂN `TIEU_DE_MO_TA.txt`, chỉ
  thay khối `[CHƯA CÓ]` bằng 8 mốc chương THẬT trích từ `voice_paced.srt`: 0:00 / 1:45 / 10:26 / 11:39 /
  14:58 / 16:49 / 19:57 / 30:18) · `phude.srt` · `tomtat.txt` (sinh bằng `giao_hang.tom_tat_viet`) ·
  `README_hybrid.txt`.
  Sheet `Lopezzapa68`: **G4** = đường dẫn thư mục giao hàng; **H4** = `Video xong - Chờ đăng`.
  Đã đọc lại A4:H9 xác nhận đúng vị trí, không đè dòng khác.

[HERMES] 2026-09-18 KHÔNG ĐỤNG: `pipeline/` · `script.txt` · `img_prompts.txt` · `img_doan.txt` ·
  `anchors.txt` · `img/` · `characters.json` · `stock/` · `final.mp4` gốc của pipeline.
  (3 dòng prompt 112-114 mâu thuẫn cốt truyện: anh đã quyết — vẽ lại 112/114 theo 「夫婦位牌」, giữ 113
  là STOCK. Không cần sửa `img_prompts.txt` nữa.)

# HẾT BÁO CÁO
