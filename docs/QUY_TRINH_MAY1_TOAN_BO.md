# QUY TRÌNH MÁY 1 — TOÀN BỘ VIỆC PHẢI LÀM TRƯỚC KHI GIAO MÁY 2 (2026-09-29)

> Tài liệu này để anh NGHIÊN CỨU quyết định sửa gì, không phải quy trình vận hành hàng ngày (lệnh
> chạy thật của từng lane vẫn ở `docs/SOP_LANE_*.md` + `docs/BAT_DAU_LANE/*.md`). Nguồn: đọc trực
> tiếp `pipeline/make_video.py` (hàm `main()` dòng 2560-2707, các hàm `Job.b*_*`) + các module nó gọi.
> Áp dụng cho lane `body.mode=ai_images` dùng Flow Tool (đa số lane hiện tại); lane clip-stock
> (`toshi-densetsu-jp`) và lane KHÔNG chặn bước 2 tự vẽ ảnh có khác biệt, ghi chú riêng ở cuối.

## Bảng bước — đúng thứ tự chạy thật

Cột "Model" ghi biến profile nào chọn model đó, để anh biết sửa ở đâu nếu muốn đổi model.
Cột "Vòng lặp" là số lượt LLM có thể lặp lại — đây là nhân tố nhân token, không phải cộng.

| # | Bước | Việc làm | Model gọi | Vòng lặp tối đa | Gửi lại toàn văn hay patch |
|---|---|---|---|---|---|
| 1 | **B0** | Đo phút video gốc (đối thủ) | 0 LLM | — | — |
| 2 | **B1** | Đo char_rate giọng đọc (nếu profile chưa đo) | 0 LLM (đo âm thanh) | — | — |
| 3 | **B2** | Tải transcript đối thủ / mượn `_khung_nhip.txt` | 0 LLM | — | — |
| 4 | **B2b** | Đọc bình luận thật → rút điểm chạm (`COMMENT_INSIGHT.md`) | gemini-3.8-flash (→ deepseek → sol nếu hỏng) | 1 lượt | Toàn văn transcript+bình luận |
| 5 | **B2N** | Nhận diện người kể (giới/tuổi/vai) | gemini (chuỗi như trên) | 1 lượt | Toàn văn |
| 6 | **B4V** | Tra kho giọng khớp người kể | 0 LLM (tra từ khoá) | — | — |
| 7 | **B3 (lean)** | S2 viết → S3 đo → S4 patch → S5 Sol chấm → khoá | **S2 viết**: `script.brain_model` (mặc định Opus 5, có lane khai Fable 5.1) qua `claude -p`. **S4 sửa**: `script.patch_model` (mặc định = brain_model, nhiều lane ép Opus). **S5 chấm**: gpt-5.6-sol | S2: 1-2 lượt. **Patch tối đa `MAX_PATCH=2`**. **Sol lặp tới khi PASS đủ `sol_pass_need` (mặc định 2) lần LIÊN TIẾP** — không giới hạn cứng số vòng, hết patch mới dừng | ⚠️ **Patch gửi TOÀN VĂN kịch bản** (`lean_script.py::patch()` dòng 611-646), Sol cũng chấm toàn văn mỗi lần |
| 7b | **B3 (luồng cũ)** | PASS0 khung + PASS1 viết + gate số | gemini hoặc Opus/Fable qua `claude -p` nếu `engine=claude_p` | Vòng ngoài: `--tries` (mặc định 2) viết lại TOÀN BỘ nếu hỏng | Toàn văn |
| 7c | **B3Q** | QC nội dung (mâu thuẫn, bám gốc 70/30) | gemini chấm + gemini sửa (`repair_script`) | Tự sửa 1 lượt | Toàn văn |
| 7d | **B3F** | Đối chiếu chi tiết với `series_ctx.txt` | 0 LLM (regex/so khớp) | — | — |
| 7e | **B3S** | QC độc lập khác hãng (an toàn/khái niệm) | Chấm: gpt-5.6-sol. Sửa: `patch_model` qua `claude -p` | Chấm→FIX 1 lần→chấm lại 1 lần (không lặp vô hạn) | Toàn văn (báo cáo QC + cả kịch bản) |
| 7f | **B3R** | Nghiệm thu cuối | Chấm: `script.final_review_model` (vd Fable). Sửa: `patch_model` | FIX→sửa 1 lần→chấm lại 1 lần | Toàn văn |
| 7g | **B3G** | Đo lại gate số, tự nén/hạ thoại nếu lệch | gemini (`trim_chunked`/`reduce_dialogue`) khi cần | 1 lần nén + 1 lần hạ thoại | Toàn văn (nén theo khúc) |
| 8 | **Máy 3 soát** | Gửi/nhận bản soát qua Sheet/ChatGPT Web hoặc người | 0 LLM API (human-in-the-loop) | Chờ người, không tính token Claude | — |
| 9 | **B4** | Lồng tiếng (TTS) + SRT + giãn nhịp | 0 LLM | — | — |
| 10 | **B4Q** | QC phủ SRT + soi sóng âm | 0 LLM (tất định) | — | — |
| 11 | **B5W** | Viết `img_prompts.txt`/`characters.json` + storyboard hook | Prompt ảnh: `prompt_model` (mặc định Opus qua `claude -p`, hoặc gemini nếu không `engine=claude_p`). Hook storyboard: `brain_model` (Fable) | Storyboard thử vài lần ra JSON hợp lệ (nhỏ); idempotent theo sha | Toàn văn (đọc cả script) |
| 12 | **B5P** | QC mâu thuẫn prompt ảnh (WARN only) | gemini, chỉ khi lane bật `image.b5p_qc` | Không lặp | Toàn văn |
| — | **⛔ DỪNG Ở ĐÂY với lane Flow Tool** — `_chan_buoc2_o_may1()` chặn cứng, không chạy B5/B5K/B5Q trên máy 1 | | | | |
| 13 | **B5/B5K/B5A** *(chỉ lane KHÔNG chặn buoc2, vd toshi-densetsu-jp)* | Vẽ ảnh AI (gpti2) hoặc khớp hình stock | gpti2 (text-to-image, không phải LLM chat) | Vẽ mẫu → QC vision → có thể lặp | — |
| 14 | **B5Q** *(lane tự vẽ)* | QC loạt ảnh (thiếu/hỏng/trùng) | Vision: gemini (chuỗi ramclouds→ns24→hhtech→sol) | Vẽ lại tối đa **2 vòng** | — |
| 15 | **B7** | Sinh chữ + nền thumbnail, QC vision chọn nền | Mặc định gemini; lane `text_engine="opus_dual_qc"` → 2 lượt Opus độc lập viết+QC; nền qua gpt-5.6-sol | Thử vài nền (`cands`), không sửa sâu | — |
| 16 | **B8** *(lane tự render)* | Ghép ảnh/clip + giọng → `final.mp4` | 0 LLM (ffmpeg) | — | — |
| 17 | **B8Q** *(lane tự render)* | QC bản ghép: ảnh khớp lời đang đọc | Vision: gemini | Vẽ lại ảnh lệch + ghép lại **tối đa 2 lượt** (`for a2 in range(1,3)`) | — |
| 18 | **B9** | Sinh tiêu đề/mô tả/tag/chương/gói đăng | gemini | Không lặp | Toàn văn (rút theo mốc chương) |
| 19 | **B10** | Nghiệm thu gói giao (thumbnail/tiêu đề/mô tả/chương/phụ đề cháy) | 0 LLM (tất định) | — | — |
| 20 | **B11** *(lane tự render)* | Copy file cuối vào thư mục kênh | 0 LLM | — | — |

**Đóng gói giao máy 2** (`dong_goi_may2.py --job`, lane Flow Tool dừng ở B5P): copy `script.txt`,
`script.lock.json`, `characters.json`, `img_prompts.txt`, `img_doan.txt`, `state.json`, `title.txt`,
`series_ctx.txt`, `competitor.txt`, `HOOK_TAP.md`, `promise.txt`, `video_goc.json`, `review_may3.json`,
`vai.txt`, `yomi.txt`, `sfx_plan.txt` + toàn bộ `hook/{flow_prompts,img,clip,sfx,qc}` + ảnh master
`_ref/`, `_ref2/`, `_ref_*/` → ghi sheet cột D=`Đã giao máy 2` + K=lệnh máy 2, H=`cần ảnh`.

**0 LLM khác đối chiếu** (không tốn token model): `qc_goi_dang.py`, `qc_numbers.py`, `video_goc.py`,
`gate_check.py`, `gate_common.py` — toàn regex/số học tất định.

## Bước nào tốn token nặng nhất (xếp theo mức độ)

1. **Cụm B3 (viết + 4 lớp QC: B3Q/B3S/B3R/B3G) là nơi tốn nhất tuyệt đối.** Lý do cộng dồn:
   - Model đắt nhất trong toàn pipeline là **Opus/Fable qua `claude -p`** (S2 viết, S4 patch, B3R
     nghiệm thu, B5W viết prompt ảnh) — nhánh này KHÔNG đi qua chuỗi rẻ gemini/deepseek.
   - **`lean_script.py::patch()` gửi TOÀN VĂN kịch bản mỗi lần sửa** (dòng 611-646), dù chỉ sửa vài
     câu — kịch bản ~6.000-9.000 chữ Nhật lặp lại nguyên trong request MỖI patch.
   - **Vòng Sol (S5) không tất định**: phải PASS đủ `sol_pass_need` (mặc định 2) lần LIÊN TIẾP —
     Sol chấm lại từ đầu mỗi lần dù bản trước đã PASS 1 lần, mỗi FIX kéo theo 1 patch (toàn văn) +
     1 vòng đo lại + 1 lượt Sol chấm lại (toàn văn).
   - Lane KHÔNG dùng `flow="lean"` còn cộng dồn thêm B3Q + B3S + B3R + B3G như 4 lớp QC riêng biệt
     trên CÙNG kịch bản, mỗi lớp tự gửi/nhận toàn văn.
2. **B5W (viết prompt ảnh)** đọc lại toàn bộ script để viết `img_prompts.txt` — 1 lượt nhưng dùng
   model đắt (Opus) trên input dài.
3. **B8Q/B5Q (vòng vẽ lại ảnh lệch, tối đa 2 lượt)** — không phải LLM văn bản, nhưng vision QC
   (gemini) chạy trên toàn bộ loạt ảnh mỗi vòng, cộng thêm tiền vẽ lại gpti2. Chỉ áp dụng cho lane tự
   render (thiểu số).
4. Toàn bộ B0/B1/B2/B3F/B4/B4Q/B8/B10/B11/qc_goi_dang/qc_numbers/gate_check **0 LLM** — không đóng
   góp chi phí model, dù chiếm nhiều dòng code.

## Phương án chỉnh sửa để anh cân nhắc (chưa làm, chỉ đề xuất)

| # | Phương án | Giảm được gì | Rủi ro / đánh đổi |
|---|---|---|---|
| A | **Đổi `lean_script.py::patch()` sang gửi diff/vị trí lỗi thay vì toàn văn** (đúng nguyên tắc PATCH của tài liệu transcript-to-outline anh gửi hôm trước) | Giảm ~70-80% token mỗi lượt patch — đây là điểm bẩy lớn nhất vì patch có thể lặp tới `MAX_PATCH=2` × mỗi lớp QC | Cần code ghép lại đoạn thay thế đúng vị trí trong `script.txt`; rủi ro ghép sai vị trí nếu model trả lệch format — cần test kỹ trước khi đổi lane đang chạy thật |
| B | **Gộp bớt lớp QC dư thừa cho lane KHÔNG lean** (B3Q + B3S + B3R đang QC gần như cùng 1 việc ở 3 model khác nhau) — có thể bỏ B3Q (gemini) khi B3S (Sol) đã đủ nghiêm, giữ Sol làm lớp QC chính | Giảm 1 lượt gọi toàn văn/tập | Mất góc nhìn "khác hãng" mà CLAUDE.md từng nhấn mạnh (Gemini + Sol độc lập nhau); cần anh quyết định lane nào chấp nhận bỏ |
| C | **Giới hạn cứng số lượt Sol lặp lại** (hiện "tới khi PASS đủ N lần liên tiếp" không giới hạn tổng số vòng, chỉ giới hạn patch=2) — thêm trần tổng số lượt gọi Sol/tập, hết trần thì ESCALATE cho người quyết thay vì tự lặp | Chặn trường hợp xấu nhất (Sol thất thường chấm đi chấm lại nhiều vòng) | Cần thêm field profile + test — không đổi hành vi lane đang PASS bình thường |
| D | **B5W chỉ gửi phần script cần thiết** (đoạn có ảnh, không phải toàn bộ script) khi viết `img_prompts.txt` | Giảm input dài cho model đắt (Opus) | Cần đảm bảo prompt ảnh vẫn nắm được ngữ cảnh xuyên suốt (nhân vật, mốc thời gian) — rủi ro mất mạch nếu cắt quá tay |
| E | **Router mỏng CLAUDE.md + BAT_DAU_LANE đã làm ở lượt trước** — vẫn còn dư địa: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` (40K ký tự) + `docs/QUY_TAC_VIDEO_HOOK.md` (19K) vẫn bị đọc TOÀN VĂN mỗi khi setup lane mới (Giai đoạn 2) — có thể tách thêm bản "tóm tắt cho lane đã quen quy trình" khỏi bản "đầy đủ cho lane hoàn toàn mới" | Giảm tiếp phần "đọc tài liệu" (không phải phần LLM sản xuất) | Thấp — chỉ là tách tài liệu thêm 1 lớp, không đụng logic |

Em khuyến nghị làm **(A)** trước — đây là đòn bẩy lớn nhất và đã có tiền lệ trong tài liệu
`HUONG_DAN_TRANSCRIPT_TO_SUON_MOI_H2DEV.md` anh gửi (mục 33 "PATCH RULE": sửa tại chỗ, không viết lại
toàn bộ). Cần anh xác nhận trước khi động vào `lean_script.py` vì đây là code đang chạy sản xuất thật
cho nhiều lane cùng lúc.
