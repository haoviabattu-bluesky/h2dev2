# LANE F `teinengo-real` — RUNBOOK 1 TẬP: kịch bản đã khoá → soát ChatGPT web → giao máy 2

> ⭐ **2026-09-30 anh chốt — THẮNG mọi chỉ dẫn soát ChatGPT web bên dưới:** hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`);
> `make_video --den B3G` khoá xong là DỪNG, tự giao máy 3/anh soát (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) →
> đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` để nhận + làm hook/ảnh/giao máy 2.


> **Cách dùng (anh):** mở tab chat mới, dán đúng 1 dòng:
> `Làm theo E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real_TAP_TIEP.md cho tập 7`
> (tập sau thì đổi số — bảng mục 0 đã có sẵn slug tập 7–10).
>
> **Tab mới (Claude):** mở đầu báo cáo bằng `@lane:teinengo-real`. Đọc HẾT file này, làm ĐÚNG THỨ TỰ mục 2, **không dừng hỏi
> giữa chừng**. Chỉ hỏi anh khi gặp đúng 1 trong 3 điểm dừng ở mục 4. KHÔNG cần đọc SOP đầy đủ/CHANNEL_DNA/profile — lệnh tự đọc.
> Mẫu đã chạy thật trọn bộ: tập 6 `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep06-shuuzen-tsumitate\` (30/09) — bí thì mở
> file tương ứng ở đó mà xem (báo cáo soát `soat_gptweb\BAO_CAO_SUA.md`, `characters.json`, `hook\img_prompts_hook.txt`,
> `hook\hook_timeline.json`, `HOOK_TAP.md`).

## 0. THAM SỐ TẬP

| Tập | Slug (`<SLUG>`) | Dòng sheet | Trạng thái lúc viết file (30/09) |
|---|---|---|---|
| 7 | `ep07-kodoku-kaiwa` | 8 | ✅ ĐÃ GIAO MÁY 2 30/09 (D8=Done, H8=cần ảnh) |
| 8 | `ep08-kodomo-enjo` | 9 | ✅ ĐÃ GIAO MÁY 2 01/10 (máy 3 anh sửa → nhận; D9=Done, H9=cần ảnh 136) |
| 9 | `ep09-shuu3-shigoto` | 10 | như trên |
| 10 | `ep10-souki-taishoku` | 11 | như trên |

Ký hiệu dùng bên dưới: `<D>` = `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\<SLUG>` · chạy mọi lệnh từ `E:\CLAUDE\YOUTUBE\h2dev`.

## 1. LUẬT CỨNG (vi phạm = dừng)
- Claude CHỈ làm bước 1 + hình hook. **CẤM** `make_video --from B4`, `--den B5/B5Q/B8`, `--from B5W` (vẫn chạy B4 lồng tiếng = tốn tiền,
  việc máy 2). Chỉ dùng `--den B3G` và `--only B5W` / `--only B5P`.
- **KHÔNG sửa tay `script.txt`.** Mọi sửa đi qua `viec_tay.txt` → `ghi_lock ESCALATE` → `make_video --den B3G` (Opus vá, máy đo, khoá).
- ChatGPT web: gửi xong phải CHỜ trả lời, **không bao giờ gửi lại**; chưa đọc được thì chỉ `--doc`. Thống nhất xong mới `--chot`
  (đóng cổng) rồi mới viết viec_tay. Chỉ đóng cổng do tool mở. Cả 2 tài khoản bận → chờ 20 phút.
- Grok: chỉ tài khoản **@hotmail.com**, luôn đặt `GROK_MIN_ROW=385` (dòng 141–222 là `@grischakr.shop` → trả video rác).
  Chạy **1 clip trước, xem khung hình bằng mắt**, đúng mới chạy phần còn lại. Xong phải đếm Chrome GPM còn mở = 0.
- gpti2 chỉ có 2 key — không nhắc key nào khác trong báo cáo.
- Chữ Nhật trong báo cáo gửi anh PHẢI kèm dịch Việt trong ngoặc. Đường dẫn trong báo cáo PHẢI tuyệt đối.
- Không `taskkill`/`Stop-Process` Chrome, không kill tiến trình giữ phiên `gptweb_pool.py --giu`.

## 2. CÁC BƯỚC

### A. Kiểm đầu vào (1 phút)
```
type <D>\script.lock.json          :: phải "state": "PASS"
type <D>\hook\hook_locked.txt
py -3.13 -X utf8 pipeline\gptweb_pool.py        :: xem tài khoản ChatGPT nào rảnh
```
Lock không PASS → chạy `py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <SLUG> --den B3G` cho tới khi khoá.
Không chạy chồng 2 tiến trình `make_video` cùng slug (kiểm PID trước).

### B. Soát ChatGPT web lượt 1 (~2–10 phút chờ GPT)
```
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-real --slug <SLUG> --lan1
```
In "ĐÃ gửi, chưa đọc được" → **không gửi lại**, chạy `--doc` (lặp lại được). Kết quả: `<D>\soat_gptweb\tra_loi_1.md`.

### C. Thẩm định (Claude tự làm, KHÔNG hỏi anh)
Đọc toàn bộ `tra_loi_1.md` + `<D>\script.txt` + `<D>\series_ctx.txt`. Từng góp ý:
- **Nhận** khi đúng: sổ tiền không cộng khớp, thứ tự mốc thời gian đảo, câu nói quá tư liệu/quy luật tuyệt đối, đoạn thủ tục nặng
  ở cuối, nhân vật phụ lấn chủ đề tiêu đề, CTA cứng.
- **Phản biện có lý do** khi: GPT bỏ mất "cú tát" cốt lõi trong tiền đề `series_ctx.txt`; GPT đòi bỏ số là callback/điểm mạnh
  của lane (kênh sống nhờ số tiền cụ thể); GPT tính sai sổ (tự cộng lại trước khi nhận!); đòi thêm số không có trong series_ctx;
  đề xuất làm lệch tuổi/tiêu đề.
- Có phản biện → viết `<D>\soat_gptweb\phan_bien_2.txt` (ngắn, đánh số, kèm câu thay NGUYÊN VĂN) →
  `py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-real --slug <SLUG> --tin <D>\soat_gptweb\phan_bien_2.txt`
  → đọc `tra_loi_2.md`. Tối đa 1 lượt phản biện.
- Chốt: `py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-real --slug <SLUG> --chot`

### D. Viết `viec_tay.txt` + khoá lại
1. `<D>\viec_tay.txt`: đầu file ghi "CHỈ SỬA ĐÚNG N VIỆC, thay NGUYÊN VĂN, không đổi số nào khác". Mỗi việc = `「câu cũ nguyên văn」 →
   「câu mới」` hoặc "XOÁ nguyên đoạn「…」". Tổng chữ dự kiến phải < trần ngân sách (bài ~6.250 chữ ±8%; sửa thường làm NGẮN đi là ổn).
2. ⚠️ **Nếu có việc đụng 5 câu đầu (= HOOK):** KHÔNG để trong viec_tay (S3 sẽ ép về hook cũ). Làm trước:
   ```python
   import sys; sys.path.insert(0, 'pipeline')
   from pathlib import Path; import hook_stage, profiles
   d = Path(r'<D>'); prof = profiles.load('teinengo-real')
   # backup trước: copy hook\hook_locked.txt → hook_locked.truoc_gptweb.txt, hook_lock.json → hook_lock.truoc_gptweb.json
   moi = """<5 câu hook mới, mỗi câu 1 dòng>"""
   print(hook_stage.check(moi, prof, (d/'series_ctx.txt').read_text(encoding='utf-8')))   # phải []
   old = hook_stage.doc_lock(d)
   hook_stage.khoa(d, moi, mode=old.get('mode','upstream'), extra={"source":"gptweb_soat_chot","sol_rounds":0,"patches":0,"source_video_id":old.get("source_video_id")})
   ```
   Câu hook KHÔNG ghi tuổi khác tuổi trong tiêu đề (ep06: ghi "65歳" bị cổng lời hứa tiêu đề bắt vì tiêu đề là "64歳").
3. Khoá lại:
   ```
   py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path(r'<D>'),'ESCALATE',reason='soat ChatGPT web')"
   py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <SLUG> --den B3G
   ```
   Phải thấy `[S5L] ✓ lời hứa tiêu đề được giữ` + `[LOCK] ✓`. Kiểm bằng grep từng câu mới có trong `script.txt`.
   S5L báo lỗi → sửa đúng chỗ đó (viec_tay hoặc hook như bước 2) rồi chạy lại.

### E. Lớp 3 — Claude đọc TOÀN BỘ bản khoá (bắt buộc)
Soi: sổ tiền cộng khớp qua mọi mốc; tuổi/năm nhất quán; câu `(warn) … bám bản gốc ≥60%` trong log S3 → phải đổi cách nói; câu lặp ý
do Opus vá sinh ra; tiêu đề được trả trong bài. Có lỗi → viec_tay mới → ESCALATE → `--den B3G` (như D.3).
Rồi viết `<D>\soat_gptweb\BAO_CAO_SUA.md` (khuôn: tập 6) và chốt:
```
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-real --slug <SLUG> --xong
```

### F. Nhân vật + prompt ảnh thân video
1. Viết `<D>\characters.json` theo khuôn `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\ep06-shuuzen-tsumitate\characters.json`:
   @REF = 俺 (người kể), @REF2 = nhân vật đối lập có nhiều cảnh nhất, vai phụ `NONE`. **`look` chỉ 1 bộ trang phục trung tính**
   (không ghi kiểu "(in hospital: gown)" — model vẽ chồng 2 bộ lên ảnh mẫu).
2. Vẽ + QC ảnh mẫu (tốn ~600đ):
   ```
   py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import make_video,profiles;print(make_video.Job(profiles.load('teinengo-real'),'<SLUG>').masters_from_bible())"
   ```
   Tự XEM `<D>\_ref\001.png` và `<D>\_ref2\001.png`: đúng tuổi, đúng nét anime (không ra ảnh gần như chụp thật), 1 bộ đồ. Sai → chuyển
   file lỗi sang `<D>\_ref2_bo\` rồi chạy lại lệnh (chỉ vẽ file thiếu).
3. Prompt ảnh (chạy song song với bước G được):
   ```
   py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <SLUG> --only B5W
   py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug <SLUG> --only B5P
   ```
   B5P chỉ WARN là bình thường.

### G. Hook — máy 1 làm trọn hình
1. Storyboard: nếu bước D có đổi hook → `py -3.13 -X utf8 pipeline\hook_storyboard.py --profile teinengo-real --slug <SLUG> --force`;
   không đổi → dùng `hook_storyboard.json` có sẵn (kiểm `voice` từng shot có trong `hook_locked.txt`).
2. Giọng hook (đo mốc thật, ~200 credit): chạy trong `<D>`:
   `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\tts.py --script hook\hook_locked.txt --out hook\hook_voice.mp3 --profile teinengo-real`
3. Đọc `<D>\hook\hook_voice.srt`, gán mỗi shot storyboard 1 dải cue (cắt ở cue cuối câu), rồi:
   `py -3.13 -X utf8 tools\hook_lane_f\dung_file_hook.py <D> --nhom "1-2,3,4-6,…"`
   → ra `hook_timeline.json` + `grok_jobs.csv` chuẩn (`clip_NN`, ảnh tuyệt đối `img\NNN.png`, 6s).
   Shot storyboard nào mâu thuẫn kịch bản (vd bối cảnh sai nơi) → sửa prompt dòng đó trong `grok_jobs.csv`.
4. Viết `<D>\hook\img_prompts_hook.txt` (khuôn tập 6): dòng đầu `# …`, mỗi shot 1 dòng = `@REF ` (cảnh có 俺 hiện tại) + khung/bối cảnh +
   mô tả mặt + cảm xúc + câu STRICT cấm chữ + `image.style_suffix` của profile. **Mặt phải to, thấy rõ** (cảnh toàn thân xa = vẽ lại).
   ```
   cd pipeline
   py -3.13 -X utf8 gen_images.py --prompts <D>\hook\img_prompts_hook.txt --out <D>\hook\img --ref <D>\_ref\001.png --orient landscape --quality low --workers 7
   ```
   Ghép 7 ảnh thành 1 tấm xem bằng mắt; rồi QC từng ảnh: `py -3.13 -X utf8 pipeline\qc_hook_clip.py --hook <D>\hook --anh N`.
5. Clip Grok — 1 clip thử trước:
   ```
   set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
   set GROK_MIN_ROW=385
   py -3.13 -X utf8 tools\hook_lane_g\grok_1tk.py <D>\hook 1
   ```
   Trích 3 khung clip_01 bằng ffmpeg xem bằng mắt: đúng ảnh gốc → chạy tiếp `grok_da_luong.py <D>\hook` (đa luồng 5–10, chạy nền).
   Ra rừng/mèo/chợ rau = tài khoản bị chặn → DỪNG, báo anh (điểm dừng mục 4).
   Rồi `qc_hook_clip.py --hook <D>\hook --clip N` từng clip. FAIL chỉ vì lỗi nằm NGOÀI thời lượng cảnh dùng (t1−t0) → duyệt tay:
   ghi `qc_may_goc` + `duyet_tay` + `verdict: PASS` vào `hook\qc\clip_NN.json` (khuôn tập 6 clip_02). FAIL thật → sửa prompt, chạy lại đúng clip đó.
   Kiểm: `powershell "(Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | ? CommandLine -match 'GPMLogin' | Measure-Object).Count"` = 0.
6. SFX (5 tiếng + 1 nền, tả tiếng Anh theo từng cảnh):
   `py -3.13 -X utf8 tools\hook_lane_g\sfx.py <D>\hook "01_xxx.mp3|<mô tả>|0" … "99_nen_xxx.mp3|<tiếng nền phòng>|1"`
   rồi thêm vào `hook_timeline.json`: `"sfx":[{"file":"sfx/01_xxx.mp3","t":<giây>,"vol":0.3}…]`, `"nen":{"file":"sfx/99_…","vol":0.08,"fade_out_s":1.5}`.
   ⛔ KHÔNG thêm khoá `cau` vào shots (đó là chế độ lane đa giọng, máy 2 sẽ đòi `voice_roles.json` và dừng).
7. `py -3.13 -X utf8 pipeline\hook_tap_md.py --slug <D> --profile teinengo-real` → tự viết hết chỗ `<<CẦN NGƯỜI>>` trong `<D>\HOOK_TAP.md`
   (dịch Việt từng câu, lời hứa, điều CẤM lộ, ảnh thumbnail mạnh nhất — đường dẫn tuyệt đối) → chạy lại với `--kiem` phải PASS.
   ⚠️ Viết bằng Python thì dùng chuỗi `r"..."` cho đường dẫn (`"\003"` trong chuỗi thường bị hiểu thành ký tự lạ — đã dính ở tập 6).

### H. Video gốc + giao máy 2
```
py -3.13 -X utf8 pipeline\video_goc.py --scan --profile teinengo-real --channel-dna-dir docs\channel_dna\rougonokurashi --channel "老後の暮らし研究所"
```
Nếu `<D>\video_goc.json` chưa có → ghi bằng `video_goc.ghi_video_goc(...)` lấy đúng mục của tập trong
`E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\VIDEO_GOC.json` (không bịa ID).
```
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job teinengo-real <SLUG>
```
Tool tự ghi H = "cần ảnh (N ảnh, ~Xđ)" và tự bắn TITLE nền. Nó KHÔNG đè D khi D đang "Chờ check kịch bản" → vì máy 3 đã được thay
bằng soát GPT web, tự ghi D = `Done` (ghi 1 ô, không xoá gì):
```
cd pipeline
py -3.13 -X utf8 -c "import dong_goi_may2 as d;s=d.svc(doc_thoi=False);s.values().update(spreadsheetId=d.SHEET_ID,range='F-teinengo-real!D<dòng>',valueInputOption='USER_ENTERED',body={'values':[['Done']]}).execute()"
```
Kiểm thư mục giao `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\F-teinengo-real\<SLUG>\` có đủ: `script.txt`, `review_may3.json`,
`_ref\`, `_ref2\`, `img_prompts.txt`, `HOOK_TAP.md`, `video_goc.json`, `hook\clip\clip_01..NN.mp4`.

### I. Cập nhật + báo cáo
- Thêm 1 dòng trạng thái tập vào mục 2 của `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-real.md`.
- Bẫy MỚI gặp (chưa có trong file này) → ghi thêm vào mục 3 dưới đây.
- Báo anh (ngắn): điểm GPT + nhận/phản biện gì, số chữ bản khoá, số prompt ảnh, hook N ảnh + N clip (clip nào duyệt tay), đường dẫn
  gói giao, ô sheet đã ghi, dòng cuối: tool nào đang chạy nền (TITLE) + log ở đâu.

## 3. BẪY ĐÃ TRẢ GIÁ (tập 5–6)
| Triệu chứng | Xử |
|---|---|
| `--lan1`/`--doc` treo dù GPT đã trả lời | đã vá hàm chung `gptweb_pool._JS_TRA_LOI` 30/09; vẫn treo → chỉ `--doc`, xem `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §4b |
| Sửa hook trong viec_tay, chạy xong hook lại về bản cũ | khoá hook mới trước (bước D.2) |
| Opus giữ câu cũ + thêm câu mới → lặp ý | lớp 3 bắt, viec_tay xoá câu thừa |
| Ảnh mẫu @REF2 mặc chồng 2 bộ đồ / ra ảnh gần như chụp thật | `look` 1 bộ trang phục; vẽ lại |
| Grok mở profile nhưng "THIEU ANH", khoá oan tài khoản | `grok_jobs.csv` phải qua `dung_file_hook.py` (ảnh tuyệt đối) |
| Grok trả clip không liên quan ảnh | tài khoản grischakr → `GROK_MIN_ROW=385` |
| Clip hook 10 giây → 429 mất tài khoản | luôn 6 giây |
| `python -c` in chữ Nhật lỗi cp1252 | luôn `py -3.13 -X utf8` |
| B3G: `patch 1 (sua) đổi 42% đoạn > trần 40% — từ chối` → ESCALATE, script không đổi (tập 7, 18 việc) | viec_tay đã bị đổi tên `.doneN` → chia thành 2 file ~9 việc, chạy D.3 hai lần (lượt 2 chép vào `viec_tay.txt` rồi ESCALATE lại) |
| `--only B5P` chạy lại sau khi sửa tay prompt → in lại kết quả cũ (bỏ qua vì đã xong) | B5P chỉ WARN, không chặn: sửa thẳng dòng trong `img_prompts.txt` (backup trước) là đủ, không cần ép chạy lại |
| HOOK_TAP viết bằng Python: `rf"...{D}\005" "..." "\006.png"` → chuỗi nối liền sau KHÔNG còn raw → ký tự lạ | ghép bằng `+` với từng mảnh `r"\006.png"`, rồi `grep -cP "[\x00-\x08]"` phải = 0 |
| `grok_1tk.py assets\...\hook 1` (đường dẫn TƯƠNG ĐỐI) → grok_batch chạy với cwd `GROK_VIDEO` không thấy `grok_jobs.csv`, vẫn mở + đóng profile và ghi cột E = mất 1 tài khoản/24h (tập 8, 01/10) | luôn truyền đường dẫn TUYỆT ĐỐI `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\<SLUG>\hook` |
| `tts.py` hook báo "ĐỌC THIẾU 146/157" 2 lần liền | gọi thẳng `openspeaker_tts.synthesize(...)` lưu mp3+srt rồi tự `kiem_phu_chu` (lượt 3 ra 157/157) + `tts.chuan_muc` (tập 8) |
| B5W `claude -p trả quá ngắn 3351 < 3690` 2 lần liền (tập 9, ~10'/lượt) | câu trả lời 444 dòng vượt trần output → CLI tự "continue", `--output-format text` chỉ in khúc cuối (bắt đầu dòng 400). Đã vá `claude_p_bridge.ask` đặt `CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000` (03/10) — gặp lại thì kiểm biến này |
| qc_hook_clip ảnh FAIL `khong_chu` hàng loạt (biển 居酒屋, đồng hồ treo tường, màn TV, logo áo) | prompt ảnh hook: bỏ "wall clock", lồng đèn/bảng trơn không chữ, TV chỉ ánh xanh mờ, áo "plain … no logo" + câu STRICT no text/no clock faces; sửa luôn `grok_jobs.csv` cho khớp (tập 9) |
| `grok_1tk` "thu het ung vien" — GPM trả `ProfileUsingByOther` cho các dòng rảnh (vd 565–580) dù máy này không mở | `pick_free(need=5)` chỉ lấy 5 ứng viên đầu → bị kẹt; đặt `GROK_MIN_ROW` lên trên dải bị khoá (tập 9: `582`) để tool lấy tài khoản mới hơn |
| Lane F không có `vai.txt` + timeline cấm khoá `cau` → `xem_thu_hook_giong.py` lỗi | đã vá 03/10: tự cắt câu từ `hook_locked.txt` (cau_vai), mọi câu = người kể; KHÔNG tạo vai.txt/`cau` cho Lane F |
| qc_hook_clip ảnh/clip FAIL `hanh_dong_dung` vì storyboard đòi cận tay/cận mắt (trái luật "mặt to") | sửa `ky_vong` trong `hook_timeline.json` + prompt Grok cho khớp ảnh; clip chỉ lệch chi tiết tay → duyệt tay |

## 4. ĐIỂM DỪNG — chỉ 3 trường hợp được hỏi anh
1. Cả 2 tài khoản ChatGPT không dùng được (chưa đăng nhập/lỗi) quá 1 giờ.
2. Grok trả clip sai nội dung ở tài khoản hotmail (nghi bị chặn cả domain).
3. Góp ý GPT chạm vào THIẾT KẾ tập (đổi tiêu đề, đổi kết cục, đề tài thiếu tư liệu) — hỏi bằng 1 quyết định cụ thể kèm khuyến nghị.
