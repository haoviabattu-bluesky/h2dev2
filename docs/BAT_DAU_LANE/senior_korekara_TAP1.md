# GIAO VIỆC TAB MỚI — LANE N `senior_korekara` · TẬP 1 (làm HẾT việc máy 1 → giao máy 2)

> ⭐ **2026-09-30 anh chốt — THẮNG mọi chỉ dẫn soát ChatGPT web bên dưới:** hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`);
> `make_video --den B3G` khoá xong là DỪNG, tự giao máy 3/anh soát (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) →
> đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` để nhận + làm hook/ảnh/giao máy 2.


> Viết 2026-09-30 bởi tab dựng Lane N. Tab mới: đọc HẾT file này trước, mở đầu báo cáo bằng `@lane:senior_korekara`.
> Anh ra lệnh bằng câu kiểu **"chạy tập 1 lane N"** → làm liền một mạch từ mục 3 tới mục 3-G, KHÔNG dừng hỏi giữa chừng
> (trừ các điểm DỪNG ghi rõ ở mục 5). Soát kịch bản bằng **ChatGPT web**, KHÔNG dùng máy 3.
> Tên lane tạm là **Lane N** (anh sẽ đổi tên sau — khi đổi thì id/slug_dir/tab/Project đổi CÙNG LÚC, không tự đổi lẻ).

## 0. ĐÃ KIỂM ĐỦ ĐIỀU KIỆN (2026-09-30)
Profile nạp OK · char_rate đã đo · gate khai đủ · cổng S1L (hook + gói đăng + video_sinh + sfx) không lỗi · đa giọng 3 clone · 2 Project soát
ChatGPT có link · `claude -p` gọi được `claude-opus-5-5` + `claude-opus-5` (bridge dùng bản CLI 2.1.284 trong extension VSCode — bản npm
2.1.278 KHÔNG nhận opus-5-5, đừng gọi tay bằng `claude` trên PATH) · ai33 còn ~1,53 triệu credit · tab sheet **`Lane-N`** (anh tạo; tab
`N-senior_korekara` là bản thừa, KHÔNG ghi vào). Lúc kiểm acc2 ChatGPT đang bị lane J giữ phiên — tool tự dùng acc1; cả hai bận thì chờ 20 phút.

## 1. ĐỌC TRƯỚC (đúng thứ tự, đừng đọc lan man)
1. `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_N.md` — runbook lane (đặc biệt §1, §1b, §2, §2b, §3b).
2. `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\senior_korekara\COMMENT_INSIGHT.md` — khán giả thật nói gì.
3. `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_M.md` §1e (soát ChatGPT web) + §2 mục F (hook/Grok) — Lane N chạy y quy trình Lane M.
Không cần đọc profile JSON / CHANNEL_DNA đầy đủ — các lệnh `pipeline\*.py` tự đọc.

## 2. TẬP 1 LÀ GÌ (sheet tab `Lane-N` dòng 2 là nguồn chân lý — đọc lại A2/B2/K2 trước khi làm)
| Mục | Giá trị |
|---|---|
| Tiêu đề làm việc (B2) | 【漫画】シルバー人材センターに入った62歳の1年。「配分金は時給じゃない」と知った日、残ったものとは？ (1 năm của ông 62 tuổi vào trung tâm nhân lực bạc. Ngày biết "tiền phân phối không phải lương giờ", điều còn lại là gì?) |
| Video gốc (K2) | `G5kIPGFNKeY` — 443.785 view · 64,1× trung vị. Transcript: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\senior_korekara\_raw\transcripts.json` khoá `G5kIPGFNKeY` |
| ⛔ Nghề CẤM | 電気部品会社の品質管理 38年 (QC linh kiện điện) · vợ 惣菜パート (bán thời gian quầy đồ ăn sẵn) — kèm mọi chi tiết/dụng cụ/câu thoại của nghề đó |
| Nghề MỚI (đề xuất) | 市役所の水道課 36年 (công chức phòng cấp nước) — tay nghề sửa vòi/ống nước là thứ cứu ông ở chặng 5. Vợ: tự đặt nghề khác, không phải 惣菜 |
| Góc (anh duyệt BẺ GÓC) | truyện đời MỘT người vào シルバー人材センター (trung tâm nhân lực bạc), trục cô đơn / giá trị bản thân sau nghỉ việc — **KHÔNG làm dạng list/xếp hạng** (tránh trùng Lane M) |
| Người kể | Khuyến nghị **ngôi 1 「俺」** như video gốc (video nổ nhất kênh là ngôi 1) → giọng dẫn Nam A: `characters.json` thêm `{"id":"ke","voice":{"voice_id":"clone_2669111"}}`. Vai nam phụ = `clone_2669055`, mọi vai nữ = `clone_2669056` |
| Không chép | tên 岡部/長田/中田/今日子…, cảnh cắt cỏ ở công ty cũ, 障子は角が命だ, tiêu đề nguyên văn. Đổi tên, tình tiết, địa điểm (70/30) |
| Slug đề xuất | `ep01-silver-haibunkin` → thư mục `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep01-silver-haibunkin\` |

## 3. LÀM ĐÚNG THỨ TỰ (lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev`)

**A. HỒ SƠ (tay)** — tạo thư mục tập, ghi ngay **cột C2** sheet = đường dẫn thư mục (tab `Lane-N`; đọc header dòng 1 trước khi ghi, cấm xoá dữ liệu).
- `competitor.txt` = transcript video gốc (nối `segs[].text`, bỏ `[音楽]`).
- `series_ctx.txt`: dòng đầu `NGHỀ CẤM: 電気部品会社の品質管理（38年）・妻の惣菜パート` + `NGHỀ MỚI: 市役所の水道課（36年）`; rồi **SỐ ĐƯỢC PHÉP** + `[Dn]` kèm URL
  CHÍNH THỨC cho mọi số chế độ: シルバー人材センター (配分金 là thù lao theo hợp đồng giao việc, không phải lương; 会費 năm; giới hạn giờ
  làm theo quy định — tra 全国シルバー人材センター事業協会 / 厚生労働省 / trang 1 trung tâm địa phương), 年金 (日本年金機構), 再雇用. Không tra
  được thì BỎ số đó, cấm bịa. Số cá nhân (退職金/貯金) tự đặt nhưng cộng khớp.
- `title.txt` = B2 bỏ phần dịch. `promise.txt` = lời hứa tiêu đề (1–2 câu: người xem sẽ biết 配分金 khác lương giờ thế nào + điều ông giữ lại được).
- Đọc lại `COMMENT_INSIGHT.md`: bình luận thật video gốc 120👍 「1回も仕事の依頼無しです。会費の無駄でした」 (không có việc nào, phí hội viên phí công)
  và 90👍 「最低賃金の保証もない」 (không bảo đảm lương tối thiểu) → đưa vào truyện như sự thật trung lập, không kích động.

**B. VIẾT + KHOÁ** (Opus 5.5 viết hook + thân, Opus 5 vá, S5L kiểm lời hứa tiêu đề) — tự dừng sau LOCK:
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep01-silver-haibunkin --den B3G
```

**C. SOÁT CHATGPT WEB** (Project `N-senior_korekara` đã dựng sẵn trên acc1 + acc2, link trong profile):
```bat
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug ep01-silver-haibunkin --lan1
::  thẩm định từng góp ý: hợp lý → nhận; chưa hợp lý → phản biện 1 lượt bằng --tin <file>
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug ep01-silver-haibunkin --chot
::  viết viec_tay.txt (thay thế NGUYÊN VĂN; ước độ dài sau sửa < trần) → ESCALATE → Opus vá
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path('assets/N-senior_korekara/ep01-silver-haibunkin'),'ESCALATE',reason='soat ChatGPT web')"
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep01-silver-haibunkin --den B3G
::  LỚP 3: tự đọc bản khoá theo SOP_LANE_N §2b (nhất là: không sót nghề cũ; mỗi câu thoại 1 câu「」riêng) → rồi:
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug ep01-silver-haibunkin --xong
```

**D. CAST + GIỌNG** — `characters.json` (nhân vật chính + vai phụ; `voice_id` từ `voice.cast_bank`; thêm id `ke` = `clone_2669111` nếu kể ngôi 1;
look các vai khác nhau rõ, KHÔNG vẽ già hơn tuổi) →
```bat
py -3.13 -X utf8 pipeline\gan_vai.py --profile senior_korekara --slug assets\N-senior_korekara\ep01-silver-haibunkin
```

**E. PROMPT ẢNH** — chỉ `--only`, KHÔNG `--from`/`--den B5Q`/`--den B8` (máy 1 CẤM B4/B5 — tốn tiền thật, code chặn cứng):
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep01-silver-haibunkin --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep01-silver-haibunkin --only B5P
```
Kiểm `img_prompts.txt` có dòng `@CAST:` cho cảnh có người (máy 2 cần để định vị miệng → đuôi bóng thoại).

**F. HOOK** (máy 1 làm trọn hình) — y `SOP_LANE_M.md` §2 mục F: storyboard → master vai → ảnh hook → **clip Grok 6 giây** (10 giây ăn 429) → QC clip → SFX →
```bat
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile senior_korekara --slug ep01-silver-haibunkin
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep01-silver-haibunkin --profile senior_korekara
```
Viết hết các chỗ `<<CẦN NGƯỜI>>` trong `HOOK_TAP.md` rồi chạy lại với `--kiem`. Xem clip Grok BẰNG MẮT (tài khoản @grischakr.shop từng trả video
không liên quan ảnh gốc — gặp là DỪNG). Xong kiểm 0 Chrome GPM còn sống.

**G. GIAO MÁY 2** (tự ghi D2 = `Done`, H2 = `cần ảnh (N ảnh, ~Xđ)`):
```bat
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job senior_korekara ep01-silver-haibunkin
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list senior_korekara
```
Đọc lại `_BANGIAO.txt`. Sau đó tự gọi dự án tiêu đề theo memory "TU goi TITLE" (kênh mới `title_auto=false` → chỉ chạy khi anh `--bat`).

## 4. ĐÃ SETUP SẴN — KHÔNG LÀM LẠI
- Profile `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\senior_korekara.json` (luồng lean, Opus 5.5/Opus 5, Sol tắt, `soat:"gptweb"`, `chan_buoc2_may1:true`).
- 3 giọng anh đã duyệt: Nam B `clone_2669055` (dẫn ngôi 3, mặc định) · Nam A `clone_2669111` (dẫn ngôi 1) · Nữ C `clone_2669056` (mọi vai nữ).
  char_rate khởi điểm 382,8 (đo đoạn mẫu) — video thật có nghỉ câu sẽ chậm hơn (~315 như Lane M) → tập 1 có thể ra ~18–19'; đo lại từ video thật ep01.
- Chữ trên hình (anh chốt 30/09): chữ dọc, mặc định góc PHẢI, lời kể = ô vuông, thoại = ô ELIP có ĐUÔI chỉ về người nói, chữ đậm (Yu Gothic Bold +
  viền 1px); cỡ chữ tạm = Lane M (72/56), anh chốt sau khi xem ep01. Mẫu: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\_chu_mau\`.
- **Nhịp ảnh + chuyển cảnh ĐÃ ĐO (30/09) — KHÔNG đo lại**: `image.seconds_per_image = 7.5` (kênh mẫu 7,4–8,0 s/ảnh trên 2 video, ~150 ảnh/19–20
  phút) · `assemble.transition = "cut"` (kênh mẫu 100% cắt thẳng, 0 hiệu ứng) · `zoom = 1.0` (kênh mẫu có zoom chậm ~27% cảnh nhưng luật
  CLAUDE.md cấm → không làm). Hệ quả cho tập 1: kịch bản ~16–19' → **~130–150 ảnh thân video**; B5W tự chia theo 7,5 s — đừng ép số ảnh tay.
  Mỗi ảnh đứng yên, chữ (hộp/bóng) đổi theo câu trên cùng ảnh. Chi tiết: `SOP_LANE_N.md` §3 + §3b.
- 2 Project ChatGPT `N-senior_korekara` (acc1 + acc2), file nạp ở `E:\CLAUDE\YOUTUBE\h2dev\CHATGPT_PROJECTS\N-senior_korekara-script\`.
- Tab sheet `Lane-N` 10 tập (A2:B11 + K2:K11).

## 5. ĐIỂM DỪNG / BẪY (đã trả giá ở lane khác)
- **Code bóng thoại mới chưa lên máy 2**: `pipeline\bong_thoai.py` + `pipeline\tate_text.py` sửa 30/09 ở máy 1. Trước khi giao máy 2 phải nhắc anh
  **push git** (máy 2 nhận code qua GitHub) và chạy `--bundle`; thiếu thì B8 vẽ bóng kiểu cũ mà KHÔNG báo lỗi.
- ChatGPT web: chờ GPT trả lời, CẤM gửi lại; `--chot` rồi mới sửa; cả 2 tài khoản bận → chờ 20 phút; chỉ đóng cổng do tool mở; treo thì `--doc` chỉ đọc.
- GPT sửa hook → phải khoá hook mới TRƯỚC khi chạy lại B3G (memory `gptweb-doi-hook-phai-khoa-lai-truoc`).
- Bản soát bổ sung nội dung → ước độ dài < trần TRƯỚC khi chạy; đừng để S3 tự NÉN (nén từng xoá mất dữ kiện ở Lane M ep01).
- Cấm chạy 2 tiến trình `make_video` cùng slug — kiểm PID trước khi chạy lại.
- Không sửa tay `script.txt` sau khi khoá — mọi sửa qua `viec_tay.txt` → Opus.
- Không tự chạy `channel_branding.py`/setup kênh — anh tự setup kênh.
- Báo cáo gửi anh: mọi chữ Nhật kèm dịch Việt; đường dẫn tuyệt đối; dòng cuối nói tool nào đang chạy + dự kiến xong.
