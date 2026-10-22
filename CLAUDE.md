# DỰ ÁN H2DEV — YouTube faceless nhiều lane (thị trường Nhật)
> Router mỏng (rút gọn 30/09/2026). File này nạp vào MỌI lượt của MỌI tab → chỉ giữ router + TÊN luật.
> Chi tiết, lý do, bài học từng luật: **`docs/QUY_TAC_CHUNG_DU_AN.md`** (bản đầy đủ cũ, nguyên văn).
> CẤM viết thêm chi tiết vận hành vào đây — viết vào SOP lane hoặc file docs rồi thêm 1 dòng trỏ.

## 🚦 ROUTER LANE (chốt lane trước mọi task sản xuất; không rõ lane → HỎI)
| Lane | Mã (= `id` profile) | Thư mục | Cửa vào / SOP |
|---|---|---|---|
| Sức khoẻ người già ngôi 1 | `Lopezzapa68` | `assets/out/` | chưa có SOP |
| F 定年後のリアル (hưu trí thực tế) | `teinengo-real` | `assets/teinengo-real/` | `docs/BAT_DAU_LANE/teinengo-real.md` · `docs/SOP_LANE_F.md` |
| G 定年後の楽しみ方 (cách vui sau hưu) | `teinengo-tanoshimi` | `assets/teinengo-tanoshimi/` | `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` · `docs/SOP_LANE_G.md` |
| H 心の家族学 (tâm lý gia đình) | `kokoro-kazoku` | `assets/kokoro-kazoku/` | `docs/BAT_DAU_LANE/kokoro-kazoku.md` |
| I 戦国の裏側 (hậu trường Chiến quốc) | `sengoku-uragawa` | `assets/sengoku-uragawa/` | `docs/BAT_DAU_LANE/sengoku-uragawa.md` |
| J 定年後の夫婦のカタチ (vợ chồng sau hưu) | `teinengo-fuufu` | `assets/J-teinengo-fuufu/` | `docs/BAT_DAU_LANE/teinengo-fuufu.md` · `docs/SOP_LANE_J.md` |
| K 薬局スカッと帳 (nhà thuốc hả giận) | `yakkyoku-sukatto` | `assets/yakkyoku-sukatto/` | `docs/BAT_DAU_LANE/yakkyoku-sukatto.md` · `docs/SOP_LANE_K.md` |
| L 社会のなぜ研究室 (phòng nghiên cứu vì sao xã hội) | `shakai_no_naze` | `assets/shakai_no_naze/` | `docs/BAT_DAU_LANE/shakai_no_naze.md` · `docs/SOP_LANE_L.md` |
| M 定年後の穴場ノート (sổ tay chỗ hay sau hưu) | `teinengo-anaba` | `assets/M-teinengo-anaba/` | `docs/BAT_DAU_LANE/teinengo-anaba.md` · `docs/SOP_LANE_M.md` |
| N シニアの人生これから (đời senior từ nay) | `senior_korekara` | `assets/N-senior_korekara/` | `docs/BAT_DAU_LANE/senior_korekara.md` · `docs/SOP_LANE_N.md` |
| O 介護スカッと (tên tạm Lane-O, chưa có kênh) | `kaigo-sukatto` | `assets/O-kaigo-sukatto/` | `docs/BAT_DAU_LANE/kaigo-sukatto.md` · `docs/SOP_LANE_O.md` |

Lane A/D/E đã BỎ 29/09, Satori (`satori-jp-obaa`) BỎ 17/10 — không tái dùng mã (dữ liệu cũ còn ở `assets/satori_jp/`, không làm tiếp). Lopezzapa68 ≠ satori.

## ⚡ CÂU LỆNH
- **"anh sửa xong kịch bản <lane> <tập>"** / cột D = `Đã sửa kịch bản` → đọc ĐÚNG `docs/NHAN_KICH_BAN_MAY3.md`, làm §1–§5 (tới clip hook xem thử, DỪNG).
- **Viết/duyệt/soát kịch bản hoặc hook (mọi lane)** → gọi skill `youtube-kich-ban` (luật rút từ bản anh sửa + sổ tự học `BAI_HOC.md`).
- **"anh duyệt hook <lane> <tập>"** / cột D = `Đã duyệt hook` → `docs/NHAN_KICH_BAN_MAY3.md` §6 (giao máy 2).
- **"thực hiện lane <mã>"** → đọc HẾT `docs/BAT_DAU_LANE/<mã>.md` trước.
- **"làm tập tiếp theo"** (lane đã setup) → đọc `<slug_dir>\HUONG_DAN_TAP_TIEP_THEO.md` (ô K); chưa có thì CHỈ mục "⚡ ĐỌC NHANH" đầu `BAT_DAU_LANE/<mã>.md` + file nó trỏ; KHÔNG chain-đọc SOP/CHANNEL_DNA/profile.
- **"chạy (nội dung kịch bản) lô tập x–y lane Z"** → KHÔNG tự làm tập nào trong tab. Đổi Z sang mã ở bảng router, chạy `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_lo_tap.py --profile <mã> --tu x --den y --dry` (in kế hoạch cho anh) rồi bản thật bằng Bash `run_in_background` (mỗi tập 1 `claude -p` mới, chặng theo cột D), báo giờ dự kiến, dừng lượt. Tỉnh dậy: đọc ĐÚNG file `TONG_KET_*.txt` đường dẫn in cuối log (KHÔNG mở log .jsonl trừ tập ✗) → báo anh bảng từng tập: D mới, phút, $, đường dẫn tuyệt đối anh cần sửa KB/xem clip hook, tập dừng + lý do.
- **Nhiều lane 1 lệnh** ("chạy lô J 8–10 + M 13–15…") → `tools\chay_hang_doi.py --hang "<mã>:x-y <mã>:x-y" [--song-song 2]` (`--dry` trước; mỗi lane 1 lô tuần tự, lane song song ≤3; song song KHÔNG giảm quota). Tổng kết `TONG_KET_HANG_*.txt` (có cột ctx đỉnh).
- **"thực hiện kênh/lane mới ABC"** → nguyên quy trình mẫu Lane M: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §00; không hỏi lại, không đổi model.
- **"nghiên cứu/phân tích kênh"** → `docs/QUY_TRINH_NGHIEN_CUU_KENH.md` (bước K1/K2/K3, KHÔNG gọi B*; trạng thái: `docs/CHANNEL_ANALYZER_STATUS.md`; cấm chạy lại K1+K2 kênh máy 2 đã làm).

## TỔ CHỨC
- 1 tab chat = 1 lane; gọi `@lane:<mã>`; giao việc `docs/lane_inbox/<mã>.md`; danh bạ `docs/DANH_BA_LANE.md`. Địa chỉ giao việc = `slug_dir` đầy đủ, cấm ghi chung chung `E:\CLAUDE\YOUTUBE\h2dev`.
- Tab sheet = `{Lane}-{tên kênh}` (nguồn: profile `publish.sheet_tab`, tra `pipeline/sheet_tab.py`); `CHANEL\<kênh>` theo `publish.upload_channel`.
- Hàng rào chống lẫn lane: (1) chưa đo char_rate/khai `script.gate` → make_video DỪNG; (2) khác biệt lane CHỈ qua field profile, cấm `if profile_id ==`; (3) `skills/` chỉ bản tổng quát; (4) CLAUDE.md router mỏng.

## LUẬT KỊCH BẢN/HOOK MỌI LANE (chi tiết: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`, `docs/QUY_TAC_VIDEO_HOOK.md`, `docs/QUY_TAC_GOI_DANG.md`)
0. ⛔ (21/10) LUẬT VIẾT HOOK DUY NHẤT: hook BÁM SÁT CẤU TRÚC hook video gốc — gốc thế nào làm thế ấy (cách mở, thứ tự nhịp), NGẮN GỌN ≤60 giây (gốc dài hơn thì rút gọn; `script.hook.giay_tran`), được đổi chút cho hợp/hay hơn; đổi tên họ/nghề/câu thoại theo tập (giữ cấu trúc gốc KHÔNG tính trùng lặp). Không còn luật hook nào khác (động cơ chính, khuôn lane, mở bằng thoại, cao trào/kịch tính… đã BỎ). Máy tự tách cấu trúc (`pipeline\hook_stage.py` H3): `docs/HOOK_CAU_TRUC/00_CHUNG.md`. ⛔ Không có hook gốc → CẤM viết/dựng (`pipeline\kiem_hook_goc.py`, chặn từ bước chuẩn bị lô).
1. Luồng lean: viết S2 đúng 1 lần → máy đo → Sol chấm → sửa bằng `patch_model` → khoá SHA256.
2. (22/10) Fable 5.1 viết hook (2 phương án cùng sườn) + KHUNG SƯỜN kịch bản (`khung_suon.txt`) → Opus 5.5 viết kịch bản theo khung sườn (`script.write_model`); Opus 5 vá · 3. Viết xong → DỪNG, soát = máy 3/anh (ChatGPT web TẮT); nhận + làm tiếp: `docs/NHAN_KICH_BAN_MAY3.md`.
4. Bình luận thật + cung KÍCH → GIẢI TOẢ → VỊ THA (thân bài) · 5. Hook khoá trước S2 (`pipeline/hook_stage.py`).
6. Gói đăng 1 lời hứa ở 4 chỗ (`pipeline/qc_goi_dang.py`) · 7. ⛔ Cổng S1L trước khi viết.
8. ⛔ Hook = video sinh (Google Vids chính `tools\hook_lane_g\vids_hook.py` từ 16/10, Grok dự phòng), ảnh tĩnh phải khai `script.hook.visual_exception` · 9. ⛔ Hình hook máy 1 làm, máy 2 chỉ ghép · 10. ⛔ Có `HOOK_TAP.md` (`pipeline\hook_tap_md.py`).
12. (01/10) Hook CHỈ nhạc nền (CẤM SFX đồ vật), kiểm bối cảnh cảnh (gọi điện ≠ gặp mặt): `docs/QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md`.
13. (01/10, sửa 03/10) ⛔ Mốc giao máy 3: KHÔNG viết file riêng tập — nhận bản sửa theo 1 file chung `docs/NHAN_KICH_BAN_MAY3.md`; cột K dòng tập = lệnh nhận (tool tự ghi). Mốc giao máy 2: `HUONG_DAN_TAP_TIEP_THEO.md` + đè cột K (`pipeline\huong_dan_tab_moi.py --loai tiep`, tab bổ sung `--ghi-chu-file`).
15. (02/10) ⛔ Trước khi giao máy 2: dựng CLIP HOOK XEM THỬ có giọng + phụ đề Việt (`tools\hook_lane_g\xem_thu_hook_giong.py`) → `pipeline\duyet_hook.py --gui` (D=`Chờ duyệt hook`) → DỪNG; anh duyệt mới `--nhan` + `dong_goi_may2` (cổng chặn cứng).
14. (01/10) ⛔ Tiêu đề/mô tả/thumbnail TẮT toàn bộ lane (`goi_title.py` `TAT_TOAN_DU_AN=True`) — cấm gọi TITLE/`--bat`; chỉ anh tự mở lại.
16. (sửa 14/10) Nhân vật chính có THẺ TÊN ĐỘNG bật NGAY cảnh ảnh nhân vật hiện lần đầu (cấm dồn về cuối hook), mỗi lane 1 kiểu motion KHÁC NHAU (`script.hook.the_ten`, `pipeline\the_ten_hook.py`): `docs/QUY_TAC_THE_TEN_NHAN_VAT_HOOK.md`. (15/10 anh BỎ luật đóng băng 12/10) Nhân vật hiện → cảnh chạy ĐỦ 6s motion clip Grok (thiếu lời thì `nghi_sau_s`), thẻ tên chồng lên chính cảnh đó, KHÔNG shot LẶNG/đóng băng.
17. (10/10) ⛔ Đạo cụ có chữ là điểm nhấn trong hook (婚姻届, 売家, biên bản, màn hình…) → máy 1 CHÈN CHỮ bằng code vào ẢNH trước, RỒI mới sinh clip Grok (`pipeline\chu_dao_cu.py`; Grok làm méo chữ = giới hạn Grok, không sửa clip): `docs/QUY_TAC_CHU_TREN_DAO_CU_HOOK.md`.
18. (12/10) Anh nói **"block giới thiệu"** = freeze-frame khung lộ mặt + chữ gõ hồ sơ (không đọc, thay thẻ tên người đó): `pipeline\block_gioi_thieu.py`, `docs/QUY_TAC_BLOCK_GIOI_THIEU_NHAN_VAT.md`. Cảnh ký ức trong hook = đen trắng.

## QUY TẮC CHUNG (chi tiết: `docs/QUY_TAC_CHUNG_DU_AN.md`)
- ⛔ (18/10) **LUẬT ĐƯỜNG DẪN ĐẦY ĐỦ**: mọi đường dẫn báo anh phải tuyệt đối từ ổ đĩa (`E:\CLAUDE\...\file.mp4`), cấm tên file trần/tương đối/rút gọn `...\` — chi tiết `docs/QUY_TAC_CHUNG_DU_AN.md` §LUẬT ĐƯỜNG DẪN ĐẦY ĐỦ.
- ⛔ Mọi chữ Nhật/nước ngoài gửi anh phải kèm dịch Việt trong ngoặc.
- ⛔ `video_goc.json` mọi tập (B2 tự ghi qua `pipeline\video_goc.py`; không có thì `null` + lý do, cấm bịa ID).
- ⛔ (19/10) **LINK VIDEO GỐC LÊN CỘT T**: tập nào chạy kịch bản thì link video gốc (nếu có) PHẢI có ở cột T (VIDEO GỐC) tab lane — máy tự ghi ở B2 + đóng gói + `--scan`; ghi tay `pipeline\ghi_cot_video_goc.py --tap <thư mục tập>` (chi tiết `docs/QUY_TAC_CHUNG_DU_AN.md` §0000).
- ⛔ Máy 2 trả hàng `results\{img_render|video_render}\<sheet_tab>\<slug>\` (tra `pipeline\duong_ket_qua.py`); `results\` ở máy 1 là receiveonly — cấm tự `mv`.
- ⛔ Xong phần máy 1: cột D=`Đã giao máy 2` + K=lệnh cho máy 2 + H=`cần ảnh (N ảnh, ~Xđ)` (`pipeline\dong_goi_may2.py --job` tự ghi).
- ⛔ (03/10) Cột D/K ghi công việc đang làm, tool tự ghi: `Đang chạy kịch bản bước 1` → `Chờ kiểm tra kịch bản` (+K lệnh nhận) → `Đang làm Hook` → `Đã giao máy 2` (+K lệnh máy 2): `docs/TRANG_THAI_COT_D_K.md`.
- ⛔ (03/10) Nghỉ khi đọc: câu ≥0,5s, đoạn ≥1,0s (code ghim sàn 0,5/1,1s trong `pipeline\pace_audio.py`, tự dò hệ số không kéo thấp hơn).
- ⛔ (10/10) Sinh ảnh: **ima2 trước tiên**, ima2 lỗi mới sang gpti2 → ckey/vilao/imgstudio (`docs/QUY_TAC_CHUNG_DU_AN.md` §THỨ TỰ PROVIDER ẢNH).
- ⛔ (16/10) ẢNH HOOK: Google Flow profile Ultra nguyenquoctuan (cổng 9350) → cổng bận → 9router → gpti2, 1 lệnh `pipeline\anh_hook.py <tập>\hook`; các tập KHÔNG chạy profile song song (khoá `pipeline\khoa_ultra.py`, chung với `vids_hook.py`): `docs/QUY_TRINH_ANH_HOOK_GOOGLE_FLOW.md`.
- ⛔ Ảnh đứng yên, cấm zoom/pan >1.0 (ngoại lệ Lane K + clip hook); chuyển cảnh theo skill `video-chuyen-canh`.
- (07/10) Số liệu động TRÊN ảnh (lane có `mg.so_lieu_dong`): MÁY 2 tự sinh + duyệt `so_lieu_dong.json` rồi dựng (`FlowHandoff_local\shared\motion_graphics\HUONG_DAN_MAY2.md`); máy 1 không chạy `so_lieu_dong.py`, chỉ lo `SỐ ĐƯỢC PHÉP` đúng.
- ⛔ Tạo/duyệt ảnh REF nhân vật → ĐỌC `docs/QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md` (khoá tuổi nhìn thấy + cảm xúc; QC nhìn ảnh thật, sai tuổi = REGENERATE).
- Nội dung 70/30, kịch bản voiceover-ready; né lỗi "nội dung không trung thực"/"sử dụng lại nội dung".
- Tool chạy lâu (vẽ ảnh/Grok/TTS) → chạy bằng Bash `run_in_background` (tiến trình KẾT THÚC — xong hay lỗi — thì tự đánh thức Claude đúng 1 lần), báo giờ dự kiến rồi dừng lượt. CẤM `tail` log định kỳ/vòng `sleep`; Monitor chỉ dùng với điều kiện kết thúc (xong/ERROR/log đứng im quá N phút), không phát từng dòng. Tỉnh dậy: lỗi → đọc đuôi log, sửa/chạy lại theo SOP; xong → làm bước kế. Đừng chạy tách rời (`Start-Process`/`nohup`) — sẽ không ai báo khi lỗi.

## HẠ TẦNG DÙNG CHUNG (đọc file khi cần)
TTS ai33: `docs/HA_TANG_TTS_AI33.md` · Ảnh miễn phí ima2: skill `gpt_api_codex.md` · QC thumbnail Sol: `docs/QC_THUMBNAIL_GPT_SOL.md` · QC kịch bản Sol B3S: `docs/QC_SCRIPT_GPT_SOL.md` · Gemini hỏng → dự phòng: `docs/FALLBACK_GEMINI_SANG_SOL.md` · Setup kênh/mail: `docs/QUY_TRINH_SETUP_KENH.md` · Học khoá: `docs/HOC_KHOA_H2DEV.md` · Lịch sử: `docs/LICH_SU_DU_AN.md`.

## ⛔ CẤM TUYỆT ĐỐI
- ⭐ (21/10) **MÁY 2 LÀM 100% A→Z** (kịch bản → hook → giọng → ảnh → dựng), máy 1 ngừng sản xuất. Máy có `MAY.local`=2 → luật "chỉ bước 1" + "máy 1 làm hình hook, máy 2 ghép" bên dưới KHÔNG áp dụng: `docs/MAY2_LAM_A_DEN_Z.md`.
- Claude Code CHỈ LÀM BƯỚC 1 (kịch bản, phương án, spec, nghiệm thu). Bước 2 (vẽ ảnh) / bước 3 (ghép video, `final.mp4`, ffmpeg concat) do agent khác — ngoại lệ: hình hook, 1 khung lẻ cho QC vision. Mọi NỘI DUNG (tiêu đề/mô tả/prompt) phải viết xong ở bước 1. Mốc dừng + khi nào tự giao máy 2: `docs/QUY_TAC_CHUNG_DU_AN.md` §CẤM TUYỆT ĐỐI.
- Cấm `taskkill`/`Stop-Process` chrome toàn bộ; mỗi profile `--user-data-dir` riêng.
