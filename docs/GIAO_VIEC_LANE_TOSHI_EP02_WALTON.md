HƯỚNG DẪN ĐẦY ĐỦ — LANE TOSHI: HOÀN TẤT VIDEO STT 2 (ep02-walton)
=====================================================================
Ngày tạo: 2026-09-14 · Người tạo: agent h2dev (máy 1)
Mục đích: file này TỰ CHỨA toàn bộ chỉ dẫn — chat mới đọc xong là làm được,
KHÔNG cần lịch sử chat trước đó. Làm xong ghi báo cáo vào CUỐI file này.

=====================================================================
0. BẠN LÀ AI — BỐI CẢNH DỰ ÁN
=====================================================================
Dự án h2dev sản xuất kênh YouTube faceless tiếng Nhật. LANE = 1 kênh + 1 SOP.
- LANE NÀY: **toshi-densetsu-jp** (都市伝説 / vũ trụ / bí ẩn) — tab trang tính
  `shinya_shiryoshitsu`, kênh đăng `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\`.
  Profile: `profiles/profiles/toshi-densetsu-jp.json` (body.mode = stock_clips).
- Thân video = **CLIP STOCK** (0đ), ảnh AI CHỈ cho thumbnail. KHÔNG REF-LOCK,
  KHÔNG gen loạt ảnh AI như lane satori. KHÁC lane satori (tab Lopezzapa68)!
- SOP đầy đủ: `docs/SOP_TOSHI_DENSETSU_JP.md` (đọc §8a trước khi làm B8Q).

=====================================================================
1. VIỆC CẦN LÀM
=====================================================================
Hoàn tất video STT 2 (cột A = 2): đề tài トラヴィス・ウォルトン失踪事件
(Travis Walton mất tích) → giao hàng → ghi cột G.

TRẠNG THÁI ĐÃ KIỂM TRA (bởi agent tạo file, 2026-09-14 — đừng làm lại):
- Sheet dòng 3 (STT 2): DONE-READY · STATUS-IMG = "Img done - 300/300 ảnh" · VIDEO trống
- Thư mục tập: `E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\`
  ĐÃ CÓ: script.txt · voice.mp3 + voice.srt · img_ai (303 PNG) · stock clips ·
  **final.mp4 (33:59, dựng 13/09 14:05)** · thumbnail_final.png · state.json (B2→B8Q)
- state.json: B8Q lần cuối 13/09 14:35 = 470 cảnh, lạc 11 (2,38% ≤ 3% ĐẠT nội dung)
  NHƯNG infra=7 (7 cảnh vision API trả null lúc đó = LỖI HẠ TẦNG, không phải lỗi kho)
  → B8Q chưa ĐẠT cổng (cổng đòi 0 lỗi hạ tầng) → B9/B10/B11 chưa chạy → chưa giao.
- Profile đã đủ publish: upload_channel=shinya_shiryoshitsu, upload_dir=E:\CLAUDE\YOUTUBE\CHANEL

→ Tập gần xong: CHỈ cần chạy B8Q lại (chấm lại 7 cảnh null) rồi B9→B10→B11.

=====================================================================
2. LỆNH CHẠY (copy-paste nguyên khối)
=====================================================================
Mở terminal từ GỐC dự án `E:\CLAUDE\YOUTUBE\h2dev` (nếu dùng Hermes: thêm `env -u
PYTHONPATH` trước `py -3.13`; nếu VS Code/Claude Code: không cần, chỉ `py -3.13`):

  py -3.13 make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8Q

Giải thích: `--from B8Q` = xoá state từ B8Q trở đi rồi chạy B8Q → B9 (gói đăng tải)
→ B10 (nghiệm thu) → B11 (giao hàng). **B8/final.mp4 GIỮ NGUYÊN** (không render lại,
không tốn TTS). Chạy từ gốc dự án, thời gian ~15-40 phút (B8Q soi 470 cảnh).

KỲ VỌNG khi chạy xong:
- B8Q: `qc_canh.py` chấm lại, báo lạc ≤3% + infra = 0 → ĐẠT
- B9: tạo `TIEU_DE_MO_TA.txt` (tiêu đề + mô tả + mốc chương + hashtag)
- B10: nghiệm thu toàn tập — ĐẠT
- B11: giao hàng → tạo thư mục `E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton\`
  chứa final.mp4 · thumbnail.png · listting.txt (đúng 3 file đăng tải)

=====================================================================
2b. ÁP DỤNG ĐƯỢC TỪ BƯỚC 3 SATORI (đã kiểm chứng EP19 — dùng cho lane này)
=====================================================================
Các kỹ năng/tool của bước 3 satori dùng CHUNG được cho toshi (đã xác minh trong code):
1. **`ghi_cot_video.py`** — GOC_KENH + glob `ep<nn>-*`: ĐÃ dùng chung 2 lane; script tự
   nhận diện tab `shinya_shiryoshitsu` → profile `toshi-densetsu-jp` (đã test OK).
2. **Quy ước cột H "TẠM DỪNG"** — muốn chặn tạm 1 dòng không cho agent đụng: ghi cụm
   bắt đầu "TẠM DỪNG" vào cột H. Tìm CHUỖI CON — muốn gỡ phải XOÁ HẲN cụm đó.
3. **Báo cáo mỗi lần chạy** (kiểu `BAO_CAO_BUOC3/`) — tạo file báo cáo riêng theo giờ,
   KHÔNG đè file cũ; dán output THẬT, không tóm tắt chủ quan.
4. **Retry đúng 3 loại**: A hạ tầng (mạng/API/timeout) → nghỉ 10s→30s→90s, tối đa 3 lần ·
   B rớt cổng NỘI DUNG → chạy lại ≤2 lần · C cần người quyết → DỪNG, không retry.
5. **`env -u PYTHONPATH` khi chạy từ Hermes** — venv Hermes (numpy cp311) làm vỡ py -3.13
   (lỗi `No module named 'numpy._core._multiarray_umath'`). VS Code/Claude Code không dính.
6. **B11 giao_hang: kiểm STT đúng trang tính** — `so_tap()` với tên `ep02-walton` khớp
   regex `ep(\d+)` → trả 2 = đúng STT 2 (lane toshi KHÔNG dính lỗi `--ep` như satori vì
   satori tên `simbot2-11` thiếu "ep"). Vẫn phải xác nhận thư mục giao hàng tên `ep02-...`.
7. **Syncthing local-first (`drive_handoff.py`)** — nếu có việc giao file 2 máy: tự dùng
   `FlowHandoff_local` (máy 1 `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local`), KHÔNG cần token
   Drive; chạy in `(che do LOCAL ...)`. Bản mới sync qua `shared/`.
8. **Bước C "bỏ qua tải khi đủ ảnh trên đĩa"** — chạy lại không tải lại (resume an toàn).

⚠️ KHÔNG áp dụng cho lane này (bộ RIÊNG của satori — CẤM dùng):
   `chay_buoc3.py` · `render_engine.py` · `sinh_neo.py` · `sinh_img_doan.py` ·
   `anchors.txt`/`img_doan.txt` · `do_thoi_luong_neo.py`. Lane toshi chống lệch bằng
   B5K (`khop_hinh.py`) + B5A (`sinh_anh_canh.py`) + B8Q (`qc_canh.py` chấm 100% cảnh).

=====================================================================
3. NẾU B8Q RỚT
=====================================================================
- Rớt vì **lỗi hạ tầng** (trong `qc_canh.json` cảnh có `"ta": null`, hoặc log báo vision
  API nghẽn/chạy lâu gấp đôi): chạy lại `--from B8Q` thêm tối đa 2 lượt (tổng 3).
  Đây là lỗi API nhất thời — KHÔNG phải lỗi kho hình, KHÔNG được `--force-qc`.
- Rớt vì **lạc nội dung** > 3% (thật sự): DỪNG, ghi báo cáo kèm danh sách mốc giây +
  cảnh lạc, KHÔNG tự sửa kho/script. (Ca thật ep02-walton 12/09: 3 lượt rớt do API.)
- B8 báo lỗi anchors/neo: KHÔNG liên quan lane này (đó là cơ chế satori) — lane toshi
  không dùng sinh_neo/anchors. Nếu thấy lỗi lạ, chép log + dừng báo.

=====================================================================
4. SAU KHI B11 XONG — GHI CỘT G (bắt buộc)
=====================================================================
  py -3.13 ghi_cot_video.py --tab shinya_shiryoshitsu --dong 2

Rào của tool: chỉ ghi khi thư mục giao hàng thật tồn tại (glob `ep02-*` trong
`E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\`). Ghi xong ĐỌC LẠI sheet xác minh
(cột G dòng 3 = đường dẫn thư mục giao hàng). Rồi trả lời user kèm đường dẫn:
  E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton

=====================================================================
5. ĐIỀU CẤM
=====================================================================
1. CẤM `--force-qc` dưới mọi hình thức (bỏ cổng = tập sau sai y hệt).
2. CẤM chạy `chay_buoc3.py` / `render_engine.py` (bộ của lane SATORI — tab khác).
3. CẤM gen ảnh AI bù (B5A chỉ vẽ đoạn CU_THE thiếu, tự động trong pipeline).
4. CẤM tự đăng video lên YouTube — việc đó thuộc dự án AUTO_LIST (đọc cột G).
5. CẤM xoá/sửa nội dung phía trên file này; CẤM xoá dữ liệu Google Sheet.

=====================================================================
6. GHI BÁO CÁO (bắt buộc — nối vào CUỐI file, giữ nguyên phần trên)
=====================================================================
Dán nguyên văn output của từng lệnh (KHÔNG tóm tắt bằng lời):
  [AGENT] <giờ> B8Q: <OK/RỚT> + 1 dòng kết quả qc_canh (lạc %, infra)
  [AGENT] <giờ> B9/B10/B11: <OK/RỚT> + bước dừng nếu có
  [AGENT] <giờ> CỘT G: <đã ghi/không> + đường dẫn đọc lại được
  [AGENT] <giờ> KẾT LUẬN: <ĐÃ GIAO XONG / DỪNG Ở BƯỚC X vì lý do Y>
=====================================================================
HẾT — bắt đầu làm từ mục 2.
=====================================================================

=====================================================================
BÁO CÁO CHẠY (2026-09-14) — nối vào cuối, giữ nguyên phần trên
=====================================================================
Lệnh đã chạy (từ E:\CLAUDE\YOUTUBE\h2dev\pipeline — make_video.py nằm trong pipeline/,
KHÔNG ở gốc dự án như mục 2 ghi; chạy từ gốc sẽ lỗi "can't open file"):

  env -u PYTHONPATH py -3.13 make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8Q

Output nguyên văn (phần B8Q, bỏ qua dòng progress):

[B2] bỏ qua (đã xong 2026-09-12 11:28)
[B2b] bỏ qua (đã xong 2026-09-12 11:28)
[B3] bỏ qua (đã xong 2026-09-12 11:39)
[B3Q] bỏ qua (đã xong 2026-09-12 11:42)
[B3F] bỏ qua (đã xong 2026-09-12 11:44)
[B4] bỏ qua (đã xong 2026-09-12 11:49)
[B4Q] bỏ qua (đã xong 2026-09-12 11:49)
[B5] bỏ qua (đã xong 2026-09-12 11:59)
[B5K] bỏ qua (đã xong 2026-09-12 12:01)
[B5A] bỏ qua (đã xong 2026-09-12 22:58)
[B5Q] lane clip stock → không có ảnh AI để chấm, bỏ qua
[B7] bỏ qua (đã xong 2026-09-12 22:58)
[B8] bỏ qua (đã xong 2026-09-13 14:05)
  $ ... python.exe qc_canh.py --video ...\final.mp4 --scenes ...\scenes.json …
soi 470 cảnh · final.mp4 · lời từ voice.srt

CHẤM ĐƯỢC 470/470 cảnh
  đúng (2) : 152  (32%)
  tạm  (1) : 303  (64%)
  LẠC  (0) :  15  (3%)
    · ảnh tự vẽ        277 cảnh → đúng 129 · tạm 148 · LẠC 0
    · ảnh bằng chứng    18 cảnh → đúng 3 · tạm 11 · LẠC 4
    · clip stock       175 cảnh → đúng 20 · tạm 144 · LẠC 11
  chữ/logo lạ: 52 cảnh  ·  hình xấu/lỗi: 4 cảnh

15 CẢNH LẠC — sửa theo danh sách này:
    114.0s  pexels_3192916.mp4                 │ Hành lang bệnh viện vắng lặng  │ もし、深い森の中で起きた不可解な出来事が、
    816.3s  pexels_10867131.mp4                │ Cảnh đền Itsukushima bên bờ bi │ 面談の内容を録音することを頑なに拒みました。
    819.6s  pexels_6175427.mp4                 │ Lối đi lát đá giữa rặng tre xa │ 公的な捜査機関を遠ざける一方で、彼らの周囲には
    823.7s  pexels_29575334.mp4                │ Cổng torii lớn dẫn vào đền thờ │ 民間のUFO研究者やメディアが群がり始めていました。
    891.3s  pexels_3665210.mp4                 │ Chuông đồng lớn và chày gỗ tro │ 意識が再び闇に沈んだと主張しました。 そして気がついた時、彼は夜のハイウェイを一人で歩いており、
    895.6s  pexels_27379117.mp4                │ Máy đánh chữ cổ và sách trên b │ そして気がついた時、彼は夜のハイウェイを一人で歩いており、 頭上から飛び去る宇宙船の残光を見届けた後、
   1253.2s  ev08_fire_lookout_tower_generic.jp │ Nhân viên kiểm lâm trong tháp  │ ウォルトンが生還後に語った 体験の細部と驚くほど一致していました。
   1258.4s  ev08_fire_lookout_tower_generic.jp │ Nhân viên kiểm lâm trong tháp  │ 事件のわずか2週間前に全米へ流れたこの映像こそが、の ちに語られる体験談の下敷きになったのではないかと
   1262.4s  ev08_fire_lookout_tower_generic.jp │ Nhân viên kiểm lâm trong tháp  │ ちに語られる体験談の下敷きになったのではないかと されています。
   1329.5s  pexels_27956815.mp4                │ Ba người cầm báo che mặt ngoài │ 彼らはなぜかゲントリー・タワーの至近を通過するリム・ロードを 経由して走行していました。
   1342.6s  pexels_36107241.mp4                │ Con đường hàng tượng đá giữa r │ 暗闇の森の中に突如として巨大な発光体を演出することは
   1515.0s  ev06_tono_iwate.png                │ Bản đồ tỉnh Iwate Nhật Bản có  │ ヒーバーの公衆電話ボックスで発見され、 催眠療法士によって「非常に混乱し、
   1622.1s  ev06_tono_iwate.png                │ Bản đồ hành chính tỉnh Iwate c │ アメリカにおいては、当時全米を席巻していたUFOや宇宙人という
   1648.7s  pexels_10867131.mp4                │ Đền thờ truyền thống ven nước  │ 事件から長い歳月が流れた後も、 関係者たちの人生に重い影を落とし続けました。
   2019.8s  pexels_4828079.mp4                 │ Người đàn ông cầm cần câu trướ │ 現実よりもはるかに強固な神話を作り上げてしまうという事実です。

  🚫 CẤM THÊM 2 file (tổng cấm 123) → soi_kho.json
     pexels_3192916.mp4                     Hành lang bệnh viện vắng lặng mờ t
     pexels_36107241.mp4                    Con đường hàng tượng đá giữa rừng

→ E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep02-walton\qc_canh.json
  ✓ B8Q chấm từng cảnh xong (764s)
[B8Q] 470/470 cảnh chấm được · lạc 15 (3.2%, trần 3%)
✗ B8Q: 15 cảnh lạc lời (3.2% > 3%). Cấm file đã ghi vào soi_kho.json — chạy lại B5A rồi B8.

[AGENT] 2026-09-14 16:20 B8Q: RỚT — lạc 15/470 (3.2% > trần 3%), infra 0 (470/470 chấm được, không cảnh null). Lạc nội dung THẬT: ảnh tự vẽ 0 · ảnh bằng chứng 4 · clip stock 11. Không phải lỗi hạ tầng → KHÔNG retry theo mục 3.
[AGENT] 2026-09-14 16:20 B9/B10/B11: KHÔNG CHẠY — dừng ở B8Q (cổng nội dung rớt).
[AGENT] 2026-09-14 16:20 CỘT G: KHÔNG ghi — chưa B11 giao hàng, không có thư mục ep02-* trong E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\.
[AGENT] 2026-09-14 16:20 KẾT LUẬN: DỪNG Ở BƯỚC B8Q vì lạc nội dung 15/470 (3.2% > 3%), theo mục 3 KHÔNG tự sửa kho/script — cần người quyết hướng xử lý 15 cảnh lạc (tool gợi ý "chạy lại B5A rồi B8" sau khi đã cấm 2 file bẩn pexels_3192916.mp4 + pexels_36107241.mp4 vào soi_kho.json).
=====================================================================

=====================================================================
BÁO CÁO VÒNG 2 (2026-09-14 17:33–18:02) — XỬ LÝ THEO HƯỚNG CLAUDE MÁY 1
=====================================================================
Hướng xử lý (Claude trả lời 4 câu, ghi trong docs/CAU_HOI_CLAUDE_EP02_WALTON_B8Q.md):
- 15/15 cảnh là LẠC THẬT, chia 3 nhóm: A) 10 clip Nhật Bản bị mượn nhầm chương (chon_nguon()
  bỏ ràng buộc chương khi cạn kho — 9 file đã bị cấm sẵn trong soi_kho.json, không cần cấm tay);
  B) ev08_fire_lookout_tower_generic.jpg lặp 3 cảnh liên tiếp do gan_at_theo_chuong() chia đều
  theo chương, không đối chiếu nội dung; C) ev06_tono_iwate.png 2 lần: 1515s cửa sổ 6s tràn qua
  pivot sang Heber, 1622.1s lọt pool ảnh thường (manifest không query) → đã bị cấm trong soi_kho.
- KHÔNG cần rollback cấm nào (cả 2 file vừa cấm đều đúng luật code qc_canh.cam_them).

ĐÃ LÀM (xác minh trên đĩa trước khi sửa — code stock_cut.py đọc field "at"/"sec"):
1. Sửa assets/toshi-densetsu-jp/ep02-walton/evidence.json — thêm at/sec cho đúng 2 entry:
   - ev08_fire_lookout_tower_generic.jpg: at="22:15" (~1335s, đoạn Sheaffer/Gentry Tower), sec=5
   - ev06_tono_iwate.png: at="25:00" (~1500s, đoạn Nhật 耳嚢 trước pivot Heber), sec=4
2. Chạy lại từ B8 (không --force-qc):
   env -u PYTHONPATH py -3.13 make_video.py --profile toshi-densetsu-jp --slug ep02-walton --from B8

Output nguyên văn (phần kết):
  ⭐ bằng chứng 25:00 (4s): ev06_tono_iwate.png — 2 cảnh
  ⭐ bằng chứng 22:15 (5s): ev08_fire_lookout_tower_generic.jpg — 2 cảnh
  🎨 ảnh tự vẽ: 75 đoạn lời · 282 cảnh dùng ảnh (nhãn 「イメージ（再現）」)
  [kế hoạch] 469 cảnh / 34.0 phút = 13.8 cắt/phút (mục tiêu [12, 16]) · 370 file khác nhau
  ...
  ✓ B11a bản xem thử tiếng Việt xong (389s)
  ✓ B11 giao hàng: E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton
    mô tả 1526 ký tự (trần 5000) · final.mp4 (1210 MB) · thumbnail.png · phude.srt ·
    review-vi.mp4 (88 MB · bản xem, đừng đăng) · tomtat.txt (3 dòng)
  === XONG ep02-walton sau 28.5 phút
  B8: {"at": "2026-09-14 17:43", "mp4": "final.mp4", "mode": "stock_clips"}
  B8Q: {"at": "2026-09-14 17:55", "canh": 469, "lac": 8, "ty_le_lac": 0.0171, "infra": 0}
  B9: {"at": "2026-09-14 17:55", "by": "publish_kit"}
  B10: {"at": "2026-09-14 17:55", "findings": 0, "heavy": 0}
  B11: {"at": "2026-09-14 18:02", "kenh": "shinya_shiryoshitsu", "noi": "E:\\CLAUDE\\YOUTUBE\\CHANEL\\shinya_shiryoshitsu\\ep02-walton"}

Kết quả cuối:
- B8Q ĐẠT: lạc 8/469 = 1,71% (≤ 3%) · infra 0
- B9/B10/B11 OK: publish_kit · nghiệm thu findings=0 · giao hàng 3 file đăng tải
  (final.mp4 + thumbnail.png + listting.txt) tại E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton

CỘT G (bắt buộc sau B11) — đã chạy:
  env -u PYTHONPATH py -3.13 ghi_cot_video.py --tab shinya_shiryoshitsu --dong 2
  Output: "✓ đã ghi G3 = E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton"
  Đọc lại sheet qua service account (A1:G3) xác minh:
    dong 3: ['2', 'トラヴィス・ウォルトン失踪事件', '...', 'DONE-READY',
             'E:\\CLAUDE\\YOUTUBE\\SPACE_RESEARCH\\output\\_READY\\02-walton\\',
             'Img done - 300/300 ảnh (20:54 12/09)',
             'E:\\CLAUDE\\YOUTUBE\\CHANEL\\shinya_shiryoshitsu\\ep02-walton']  ✓

[AGENT] 2026-09-14 18:05 B8Q: OK — lạc 8/469 (1,71% ≤ trần 3%), infra 0 (lượt 2 sau khi sửa evidence.json at/sec cho ev06+ev08).
[AGENT] 2026-09-14 18:05 B9/B10/B11: OK — B9 publish_kit · B10 nghiệm thu findings=0 · B11 giao hàng 3 file tại E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton.
[AGENT] 2026-09-14 18:05 CỘT G: đã ghi — G3 = E:\CLAUDE\YOUTUBE\CHANEL\shinya_shiryoshitsu\ep02-walton (đọc lại sheet xác minh đúng).
[AGENT] 2026-09-14 18:05 KẾT LUẬN: ĐÃ GIAO XONG ep02-walton (28,5 phút, lạc 1,71%) — hướng xử lý theo Claude máy 1: sửa evidence.json ghim at/sec cho ảnh bằng chứng, chạy lại --from B8, không cần cấm thêm file.
=====================================================================
