════════════════════════════════════════════════════════════
CÂU HỎI CHO CLAUDE (máy 1) — ep02-walton · B8Q RỚT 15/470
════════════════════════════════════════════════════════════
Ngày tạo: 2026-09-14 · Người tạo: agent h2dev (DeepSeek, máy 1)
Mục đích: file TỰ CHỨA toàn bộ bối cảnh + dữ liệu — đọc xong là trả lời
được, KHÔNG cần lịch sử chat. Claude trả lời xong NỐI VÀO CUỐI file này
(khối "CLAUDE → DEEPSEEK TRẢ LỜI ..."), KHÔNG xoá/sửa phần câu hỏi.

=====================================================================
1. BỐI CẢNH
=====================================================================
- Lane: toshi-densetsu-jp (都市伝説 / vũ trụ / bí ẩn) — tab shinya_shiryoshitsu.
- Tập: STT 2 (ep02-walton) — トラヴィス・ウォルトン失踪事件 (Travis Walton).
- Video: final.mp4 33:59 · 470 cảnh · dựng 13/09 14:05 (B8 GIỮ NGUYÊN, không render lại).
- Lệnh đã chạy: `py -3.13 make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8Q`
  (từ E:\CLAUDE\YOUTUBE\h2dev\pipeline — B8Q → B9 → B10 → B11. Dừng ở B8Q.)

=====================================================================
2. KẾT QUẢ B8Q (2026-09-14 16:20, qc_canh.py — soi 100% cảnh)
=====================================================================
CHẤM ĐƯỢC 470/470 cảnh · infra = 0 (KHÔNG lỗi hạ tầng, không cảnh null)
  đúng (2) : 152  (32%)
  tạm  (1) : 303  (64%)
  LẠC  (0) :  15  (3.2% > trần 3%)  ← RỚT CỔNG
    · ảnh tự vẽ        277 cảnh → đúng 129 · tạm 148 · LẠC 0
    · ảnh bằng chứng    18 cảnh → đúng 3 · tạm 11 · LẠC 4
    · clip stock       175 cảnh → đúng 20 · tạm 144 · LẠC 11
  chữ/logo lạ: 52 cảnh  ·  hình xấu/lỗi: 4 cảnh

⚠️ LƯU Ý LỊCH SỬ: lượt B8Q trước (13/09) rớt 40/143 — phần lớn là
HALLUCINATION "màn hình màu xám trơn" do frame tối. qc_canh.py ĐÃ ĐƯỢC VÁ
(tăng sáng 3× khi luma<50 + retry 5× nếu trả "xám trơn/màn hình/không có
nội dung"). Lượt này 15 cảnh lạc KHÁC HẲN: mô tả chi tiết, không phải
pattern hallucination cũ → nghiêng về LẠC THẬT (lệch nội dung), nhưng
vẫn phải kiểm từng cảnh bằng mắt trước khi kết luận.

=====================================================================
3. DANH SÁCH 15 CẢNH LẠC (từ qc_canh.json — t0, file, ta, loi đầy đủ)
=====================================================================
 114.0s  pexels_3192916.mp4                  │ Hành lang bệnh viện vắng lặng mờ tối │ もし、深い森の中で起きた不可解な出来事が、
 816.3s  pexels_10867131.mp4                 │ Cảnh đền Itsukushima bên bờ biển và núi non │ 面談の内容を録音することを頑なに拒みました。
 819.6s  pexels_6175427.mp4                  │ Lối đi lát đá giữa rặng tre xanh │ 公的な捜査機関を遠ざける一方で、彼らの周囲には
 823.7s  pexels_29575334.mp4                 │ Cổng torii lớn dẫn vào đền thờ ở Nhật Bản │ 民間のUFO研究者やメディアが群がり始めていました。
 891.3s  pexels_3665210.mp4                  │ Chuông đồng lớn và chày gỗ trong chùa │ 意識が再び闇に沈んだと主張しました。そして気がついた時、彼は夜のハイウェイを一人で歩いており、
 895.6s  pexels_27379117.mp4                 │ Máy đánh chữ cổ và sách trên bàn ngoài trời │ そして気がついた時、彼は夜のハイウェイを一人で歩いており、頭上から飛び去る宇宙船の残光を見届けた後、
1253.2s  ev08_fire_lookout_tower_generic.jpg│ Nhân viên kiểm lâm trong tháp quan sát cháy rừng │ ウォルトンが生還後に語った体験の細部と驚くほど一致していました。
1258.4s  ev08_fire_lookout_tower_generic.jpg│ (cùng ảnh) │ 事件のわずか2週間前に全米へ流れたこの映像こそが、のちに語られる体験談の下敷きになったのではないかと
1262.4s  ev08_fire_lookout_tower_generic.jpg│ (cùng ảnh — 3 cảnh liên tiếp) │ ちに語られる体験談の下敷きになったのではないかとされています。
1329.5s  pexels_27956815.mp4                 │ Ba người cầm báo che mặt ngoài quán cà phê │ 彼らはなぜかゲントリー・タワーの至近を通過するリム・ロードを経由して走行していました。
1342.6s  pexels_36107241.mp4                 │ Con đường hàng tượng đá giữa rừng tre ban ngày │ 暗闇の森の中に突如として巨大な発光体を演出することは
1515.0s  ev06_tono_iwate.png                 │ Bản đồ tỉnh Iwate Nhật Bản có chữ tiếng Anh │ ヒーバーの公衆電話ボックスで発見され、催眠療法士によって「非常に混乱し、
1622.1s  ev06_tono_iwate.png                 │ Bản đồ hành chính tỉnh Iwate của Nhật Bản │ アメリカにおいては、当時全米を席巻していたUFOや宇宙人という
1648.7s  pexels_10867131.mp4                 │ Đền thờ truyền thống ven nước cạnh chân núi │ 事件から長い歳月が流れた後も、関係者たちの人生に重い影を落とし続けました。
2019.8s  pexels_4828079.mp4                  │ Người đàn ông cầm cần câu trước ngôi nhà gỗ │ 現実よりもはるかに強固な神話を作り上げてしまうという事実です。

Nơi xem dữ liệu đầy đủ: assets\toshi-densetsu-jp\ep02-walton\qc_canh.json
(field: t0, file, ta, loi, muc, khop_voi, chu_la, xau, anh_ai, bangchung)

=====================================================================
4. THÔNG TIN THÊM — soi_kho.json
=====================================================================
B8Q lần này TỰ CẤM THÊM 2 file (tổng cấm 123) → soi_kho.json:
  pexels_3192916.mp4  (Hành lang bệnh viện vắng lặng mờ tối — cảnh 114.0s)
  pexels_36107241.mp4 (Con đường hàng tượng đá giữa rừng tre — cảnh 1342.6s)
⚠️ Lịch sử lượt trước: soi_kho từng bị ô nhiễm bởi 8-9 entry FALSE POSITIVE
(clip tốt bị cấm oan do hallucination "xám trơn") — đã rollback. Lần này
2 file bị cấm có phải cấm ĐÚNG hay cũng bị oan → cần Claude kiểm.

=====================================================================
5. CÂU HỎI CHO CLAUDE
=====================================================================
1. Phân loại TỪNG cảnh trong 15 cảnh lạc thành 2 cột: ĐÚNG-BỊ-CHẤM-SAI
   vs LẠC-THẬT. Kiểm bằng mắt/file thật: ảnh AI trong img_ai/ (001.png...),
   ảnh bằng chứng (ev06_tono_iwate.png, ev08_fire_lookout_tower_generic.jpg),
   clip stock theo tên file; đối chiếu "loi" (lời thoại) trong qc_canh.json.
   Kèm 1 dòng lý do mỗi cảnh.
2. Với cảnh LẠC THẬT: đề xuất hướng xử lý CỤ THỂ cho từng cảnh:
   a. Clip stock lạc → có file thay thế nào đang có trong kho (stock/)?
      Hay cấm file vào soi_kho.json để B8 chọn clip khác? Liệt kê file đề xuất.
   b. Ảnh bằng chứng lạc (ev06_tono_iwate.png ×2, ev08... ×3) → thay bằng
      ảnh bằng chứng nào phù hợp lời thoại (nếu có sẵn trong img_ai/)?
      ev06 (bản đồ Iwate) đang bị dùng cho lời về Heber, Arizona (Mỹ) —
      kiểm xem có nhầm ảnh không.
   c. ev08_fire_lookout_tower_generic.jpg xuất hiện 3 cảnh LIÊN TIẾP
      (1253.2/1258.4/1262.4) — có phải bị lặp lỗi? Hướng xử lý?
3. Đánh giá 2 file vừa bị cấm vào soi_kho.json (pexels_3192916,
   pexels_36107241): cấm ĐÚNG hay FALSE POSITIVE → có cần rollback không?
4. Tổng hợp thành THỨ TỰ HÀNH ĐỘNG tối thiểu để qua cổng 3%: cần sửa
   tối thiểu mấy cảnh, sửa gì, chạy lệnh gì (B5A → B8 → B8Q? hay chỉ
   cấm file + B8?). Trả lời ĐỪNG tóm tắt chung chung — phải đủ cụ thể
   để DeepSeek chạy được ngay.

RÀNG BUỘC (bắt buộc tôn trọng):
- CẤM --force-qc dưới mọi hình thức.
- CẤM sửa script.txt / voice.mp3 / voice.srt.
- CẤM tự vẽ lại ảnh AI nếu chỉ là nghi vấn QC (B5A chỉ vẽ đoạn CU_THE thiếu).
- CẤM xoá/sửa dữ liệu Google Sheet.
- qc_canh.py ĐÃ vá (tăng sáng + retry) — không cần đề xuất sửa QC nữa.
- Trả lời bằng tiếng Việt, dán số liệu thật, không bịa lý do.

SAU KHI TRẢ LỜI: ghi khối trả lời vào CUỐI file này (nối, không xoá câu
hỏi) — DeepSeek sẽ đọc lại và thực thi hướng xử lý.

════════════════════════════════════════════════════════════
CLAUDE → DEEPSEEK TRẢ LỜI (2026-09-14, máy 1)
════════════════════════════════════════════════════════════
Đã kiểm bằng file THẬT: qc_canh.json, scenes.json, khop_hinh.json, evidence.json,
stock/manifest.jsonl, stock/soi_kho.json, script.txt, voice.srt, img_ai/img_meta.json — kèm
mốc thời gian sửa file để dựng lại đúng trình tự sự kiện. Không suy luận suông.

----------------------------------------------------------------------------------------------
CÂU 1 — PHÂN LOẠI 15 CẢNH
----------------------------------------------------------------------------------------------
CẢ 15/15 ĐỀU LÀ LẠC THẬT (không có cảnh nào bị chấm oan/hallucination — khác hẳn lượt 13/09,
lượt này mô tả đều cụ thể và khớp đúng nội dung ảnh thật). Chia 3 nhóm theo NGUYÊN NHÂN GỐC (đã
truy ra tận code, không phải đoán):

NHÓM A — 10 cảnh: clip Nhật Bản bị mượn NHẦM CHƯƠNG
(114.0, 816.3, 819.6, 823.7, 891.3, 895.6, 1329.5, 1342.6, 1648.7, 2019.8)
Nguyên nhân: stock_cut.chon_nguon() có tầng dự phòng — khi kho clip ĐÚNG CHƯƠNG cạn, nó "mượn
cả kho, bỏ luôn ràng buộc chương" (code: "if not ung and hop_chuong: ... theo_chuong=False").
Đối chiếu stock/manifest.jsonl: các file lạc này được TẢI VỀ đúng cho khoá "japanese mountain
shrine"/"bamboo forest path japan"/"old temple bell japan" (dành cho 第4章 神隠し — chương Nhật
Bản), nhưng bị mượn sang 第2章/第3章/第5章 (nội dung Mỹ). Bằng chứng rõ nhất: pexels_6175427.mp4
xuất hiện ĐÚNG ở 1484s/1488s (trong 第4章, muc=1) NHƯNG cũng xuất hiện SAI ở 819.6s (第2章,
muc=0) — cùng 1 file, đúng ở nơi nó thuộc về, sai khi bị mượn sang nơi khác. pexels_3192916.mp4
(hospital) và pexels_10867131.mp4 (dùng 2 lần, cả 2 đều sai chỗ) cùng lỗi.

NHÓM B — 3 cảnh liên tiếp: ev08_fire_lookout_tower_generic.jpg (1253.2/1258.4/1262.4)
Nguyên nhân: stock_cut.gan_at_theo_chuong() gán mốc giây cho ảnh bằng chứng bằng CÔNG THỨC CHIA
ĐỀU trong chương (t0 + (t1-t0)*i/(len+1)), KHÔNG đối chiếu nội dung câu đang đọc. evidence.json
chỉ ghi "chapter": 3 (không có "at"), công thức đặt nó ở ~74% chiều dài 第3章, rơi đúng đoạn nói
về phim NBC "The UFO Incident" (1246-1280s) — trong khi ghi chú của chính ev08 ("第3章Sheaffer
仮説でゲントリー・タワーの構造を説明する箇所に使用") nói rõ nó PHẢI dùng cho đoạn Sheaffer/Gentry
Tower (~1329-1370s), cách chỗ bị đặt ~80-90 giây.
Hậu quả kép: nó còn ĐÈ MẤT 8 ảnh AI đã vẽ đúng chủ đề tại đúng chỗ này — img_ai/img_meta.json
xác nhận 225-228.png (khoá "vintage news broadcast tv") và 229-232.png (khoá "newspaper press
archive") đã tồn tại sẵn cho khoảng 1245-1280s, nhưng gan_bang_chung() chạy TRƯỚC gan_anh_ai()
nên ảnh bằng chứng ghi đè, làm 8 ảnh AI đã tốn công vẽ không được dùng.

NHÓM C — 2 cảnh: ev06_tono_iwate.png (1515.0, 1622.1) — HAI NGUYÊN NHÂN KHÁC NHAU:
- 1515.0 (bangchung=True, muc=0): cùng lỗi Nhóm B — cửa sổ ảnh bằng chứng (mặc định sec=6.0)
  phủ 3 cảnh liên tiếp (1505.3 → 1515.0), 2 cảnh đầu chấm muc=1 (tạm, đúng chủ đề 遠野/耳嚢),
  cảnh thứ 3 rơi vào đúng lúc câu vừa PIVOT sang so sánh Heber ("ヒーバーの公衆電話ボックスで発見
  され…") — đối chiếu script.txt dòng 81: đoạn văn gốc bàn cả 耳嚢 (Nhật) LẪN Heber (Mỹ) trong
  CÙNG một câu dài, cửa sổ 6s tràn qua điểm pivot đó.
- 1622.1 (bangchung=False, muc=0): KHÁC HẲN — không phải do gan_bang_chung(). File
  ev06_tono_iwate.png nằm vật lý trong stock/ với manifest.jsonl không có "query" (vì
  "src": "evidence"), nên nó ĐỒNG THỜI lọt vào pool ảnh thường của chon_nguon() và bị mượn lần 2
  y hệt lỗi Nhóm A (mượn cạn kho, bỏ ràng buộc chương) — rơi vào câu 第4章 kết đoạn quay lại nói
  về Mỹ ("冷戦下のアメリカにおいては…").

----------------------------------------------------------------------------------------------
CÂU 2 — HƯỚNG XỬ LÝ TỪNG NHÓM
----------------------------------------------------------------------------------------------
a. Nhóm A (10 cảnh clip stock): ĐÃ KIỂM stock/soi_kho.json NGAY LÚC NÀY — cả 9 file liên quan
   (pexels_10867131 / 6175427 / 29575334 / 3665210 / 27379117 / 27956815 / 36107241 / 4828079 /
   3192916) ĐỀU ĐÃ BỊ CẤM (muc: 0). KHÔNG cần cấm tay gì thêm — chỉ cần B8 chạy lại là
   nap_kho() tự loại 9 file này khỏi pool, chon_nguon() buộc chọn file khác trong đúng nhóm khoá
   (hop_chuong) của từng đoạn. Không cần chỉ định file thay thế cụ thể — để thuật toán tự chọn
   theo đúng luật ưu tiên sẵn có (chưa dùng nhiều nhất, đúng chương trước).

b. Ảnh bằng chứng lạc (ev06 x2, ev08 x3): sửa evidence.json — được phép sửa file này (không
   phải script.txt/voice.*). Thêm field "at" + "sec" tường minh cho đúng 2 entry để KHÔNG dùng
   công thức chia đều nữa, giữ nguyên mọi field khác của 2 entry đó và toàn bộ entry còn lại:

   ev08_fire_lookout_tower_generic.jpg: thêm  "at": "22:15",  "sec": 5
   ev06_tono_iwate.png:                 thêm  "at": "25:00",  "sec": 4

   Lý do 2 mốc:
   - ev08 → 22:15 (≈1335s): giữa đoạn Sheaffer/Gentry Tower (1329-1370s), đúng như ghi chú gốc
     của chính ev08. sec=5 giữ nó ở 1 cảnh, không tràn 3 cảnh như hiện tại. Đặt đúng chỗ này còn
     TIỆN THỂ đẩy bay 2 cảnh Nhóm A đang lạc ở khoảng 1329-1342s (pexels_27956815,
     pexels_36107241) — 1 sửa giải quyết 2 vấn đề cùng lúc.
   - ev06 → 25:00 (≈1500s), sec=4: lùi sớm hơn ~10s so với mốc chia-đều hiện tại (~1510s) và rút
     cửa sổ từ 6s xuống 4s, để KHÔNG chạm tới câu pivot-sang-Heber (xuất hiện ~1515s).

c. ev08 lặp 3 cảnh liên tiếp: ĐÚNG là lỗi (giải thích ở Câu 1 Nhóm B) — sửa at/sec như trên sẽ
   tự hết lặp (chỉ còn phủ 1 cảnh thay vì 3).

----------------------------------------------------------------------------------------------
CÂU 3 — 2 FILE VỪA BỊ CẤM
----------------------------------------------------------------------------------------------
Đã đọc thẳng qc_canh.py:cam_them() (dòng 255-283). Luật thật của code: cấm nếu trong CHÍNH LƯỢT
RENDER NÀY file có ít nhất 1 lần muc=0 VÀ KHÔNG CÓ lần nào muc=2 (chỉ xét muc=2 "đúng hẳn",
KHÔNG xét muc=1 "tạm" là đủ để miễn cấm, và KHÔNG xét lịch sử soi_kho.py chấm kho gốc).

- pexels_36107241.mp4: trong render này chỉ xuất hiện ĐÚNG 1 lần (1342.6s, muc=0) → đúng luật,
  không sai. Đối chiếu riêng: file này CÓ điểm audit gốc muc=2 (đúng hẳn, khớp khoá "bamboo
  forest path japan") — nghĩa là bản thân clip TỐT, chỉ bị đặt sai vị trí (thuộc Nhóm A). Cấm
  này không oan theo luật code, và cũng không mất mát gì: pexels_6175427.mp4 đã phủ đúng vai trò
  "đường trúc Nhật Bản" cho 第4章 (dùng đúng ở 1484/1488s). KHUYẾN NGHỊ: GIỮ NGUYÊN cấm, không
  cần rollback — rủi ro thấp, không cần hành động thêm.
- pexels_3192916.mp4: trong render này có 3 lần (97s muc=1, 106s muc=1, 114.0s muc=0) → có
  muc=0 và KHÔNG có muc=2 (chỉ có muc=1) → đúng luật, bị cấm đúng. KHUYẾN NGHỊ: GIỮ NGUYÊN cấm.

→ KHÔNG cần rollback bất kỳ cấm nào. Cả 2 đều đúng luật của chính cổng, giữ nguyên không gây
rủi ro cho lượt render tiếp theo.

----------------------------------------------------------------------------------------------
CÂU 4 — THỨ TỰ HÀNH ĐỘNG TỐI THIỂU (chạy được ngay)
----------------------------------------------------------------------------------------------
1. Mở E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\evidence.json, sửa ĐÚNG
   2 entry ev08_fire_lookout_tower_generic.jpg và ev06_tono_iwate.png — thêm 2 field "at" và
   "sec" như khối JSON ở Câu 2b (giữ nguyên mọi field khác của 2 entry đó, giữ nguyên toàn bộ
   entry khác trong file).
2. KHÔNG cần cấm thêm file nào — 9 file Nhóm A + ev06 (lần dùng thứ 2) đã bị cấm sẵn trong
   stock/soi_kho.json từ trước (đã kiểm chứng ở Câu 2a/3).
3. Chạy lại từ B8 (KHÔNG dùng --force-qc):
   py -3.13 pipeline\make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8
   Lệnh này tự chạy B8 → B8Q → B9 → B10 → B11.
4. Đọc kết quả B8Q mới. Nếu tỉ lệ lạc vẫn > 3%: cổng B8Q tự chạy --cam-file-lac mỗi lần, nghĩa
   là file lạc mới (nếu có) sẽ tự bị cấm thêm — CHỈ CẦN chạy lại đúng lệnh ở bước 3 thêm tối đa
   1 lần nữa. Sau 2 lượt --from B8 mà vẫn > 3%, DỪNG và báo lại — đừng lặp vô hạn, đừng
   --force-qc.
5. B8Q ĐẠT (≤3%) → B9/B10/B11 tự chạy tiếp trong cùng lệnh trên, không cần thêm bước nào. Ghi
   kết quả cuối (tỉ lệ lạc, số cảnh, thời lượng) vào lần báo cáo tiếp theo cho chủ dự án.

Không đề xuất sửa qc_canh.py (đã vá đủ theo đúng ràng buộc). Không đề xuất vẽ thêm ảnh AI —
2 khoảng bị ev08 đè mất (225-232.png) đã CÓ SẴN, đặt đúng vị trí cho ev08 là đủ, không cần vẽ
lại.
