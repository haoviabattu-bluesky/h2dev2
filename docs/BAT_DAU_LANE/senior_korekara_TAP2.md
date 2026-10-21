# GIAO VIỆC TAB MỚI — LANE N `senior_korekara` · TẬP 2 (máy 1 → máy 3 soát → máy 2)

> ⛔ **LỊCH SỬ — mọi luật VIẾT hook trong file này đã XOÁ** (16/10 bỏ "câu 1 = thoại kẻ đáng ghét / nhục công khai / tên-tuổi sau
> cảnh nhục / CẢNH XUNG ĐỘT CHO HOOK"; 17/10 bỏ luôn narrative intro). Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn)
> — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`.

> Viết 2026-09-30 sau khi chạy xong tập 1 theo quy trình mới. Tab mới: đọc HẾT file này, mở đầu báo cáo bằng `@lane:senior_korekara`.
> Anh ra lệnh kiểu **"làm tập 2 lane N"** → làm liền mạch **PHẦN A** tới lúc giao máy 3 rồi DỪNG. Khi anh báo cột D = `Đã sửa kịch bản`
> → làm liền mạch **PHẦN B** tới lúc giao máy 2 + dựng video hook xem thử cho anh. Không dừng hỏi giữa chừng, trừ điểm DỪNG ở §6.
> Mọi chữ Nhật gửi anh phải kèm dịch Việt. Báo cáo ghi đường dẫn tuyệt đối. Dòng cuối báo tool nào đang chạy.

## 0. Tóm tắt 1 dòng
Hồ sơ tay → `make_video --den B3G` (Fable 5.1 viết 2 hook → Sol chọn → Opus 5.5 viết thân → khoá) → **tự giao máy 3** (D=`Chờ kiểm tra kịch bản`)
→ anh sửa → `review_may3 --nhan` → cast → B5W/B5P → hook 18±cảnh (`_mk_hook.py`) → ảnh → Grok → QC → **video hook xem thử có phụ đề Việt**
→ `HOOK_TAP.md` → `dong_goi_may2 --job` (D=`Done`, H=`cần ảnh`).

## 1. TẬP 2 LÀ GÌ (sheet `Lane-N` dòng 3 là nguồn chân lý — đọc lại B3/K3 trước khi làm)
| Mục | Giá trị |
|---|---|
| Tiêu đề làm việc (B3) | 【漫画】年金だけでは月4万円足りない。65歳で5つのバイトを渡り歩いた男が、最後に「ここだ」と思えた仕事とは？ (Chỉ lương hưu thì thiếu 4 vạn yên/tháng. Người đàn ông 65 tuổi đi qua 5 việc làm thêm — việc cuối cùng ông thấy "chính là đây" là gì?) |
| Video gốc (K3) | `BdLooNSganA` — 242.757 view · 35,0× trung vị. Transcript: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\senior_korekara\_raw\transcripts.json` khoá `BdLooNSganA` (nối `segs[].text`, bỏ `[音楽]`) |
| ⛔ Nghề CẤM | nhân viên công ty 42 năm (営業) · vợ 学校給食パート (bếp ăn trường) — cấm cả dụng cụ/câu thoại nghề đó |
| Nghề MỚI | **百貨店の紳士服売り場 38年** (bán hàng quầy đồ nam ở bách hoá): đo người bằng mắt, gấp áo sơ mi, cúi chào 45°, nhớ tên khách quen, cà vạt thắt chuẩn. Vợ: tự đặt nghề khác, KHÔNG 給食 |
| Góc (anh duyệt BẺ GÓC) | truyện đời 1 người đi qua ~5 việc làm thêm, KHÔNG xếp hạng 第N位/7選 (trùng Lane M); kết NGHIỆM TÙNG, không quả báo |
| Người kể | ngôi 1 「俺」 như video gốc → `ke` = Nam A `clone_2669111`; vai nam phụ Nam B `clone_2669055`; mọi vai nữ Nữ C `clone_2669056` |
| ⛔ Không chép gốc | tên 関口/かず子/高橋/大原/田村…, cảnh gặp cấp dưới cũ trong nhà vệ sinh, 2万1000歩, câu 「掃除のおじさんか」, tiêu đề nguyên văn (70/30) |
| ⛔ Nghề phụ cũng cấm | nghề chính của các tập khác (tab `Lane-N` K2:K11): 水道課 · 和菓子職人 · 写真館 · 小学校教員 · 靴修理 · 生け花 · 旅館経営 · 長距離トラック · 郵便配達 — vai phụ không được mang |
| Slug đề xuất | `ep02-baito-go-shoku` → `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\` |

## 2. ⭐ HOOK PHẢI GAY CẤN, KỊCH TÍNH (anh chốt 30/09 — đây là phần anh chấm kỹ nhất)
Đọc TRƯỚC khi viết hồ sơ (2 file, ~5 phút):
- `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_KIEU_ANH_VIET.md` — 10 luật "cảnh nhục trước, tên tuổi sau".
- `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAO_TRAO_CAM_XUC.md` — cao trào cảm xúc 5–15 giây đầu.
- **Mẫu thật anh duyệt** = hook tập 1: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep01-silver-haibunkin\hook\hook_locked.txt`
  (bản anh tự viết lại 30/09; video xem thử: `...\ep01-silver-haibunkin\hook\xem_thu\hook_xem_thu_VI.mp4`).

**Khung hook tập 1 anh đã duyệt (bắt chước khung, KHÔNG chép chữ):**
1. Câu 1 = câu thoại coi thường/chất vấn của kẻ đáng ghét, ngay giữa xung đột (「水漏れひとつ、直せないんですか？」).
2. Nhân vật chính đáp lễ phép, ĐÚNG luật → người xem đứng về phía ông.
3. Kẻ đáng ghét leo thang 3 nấc bằng THOẠI: coi tiền là ban ơn → cắt lời 「…――」 → ra lệnh/mỉa, kèm 1 câu hành động (「女は、それが当たり前だという顔で、俺を見た」).
4. Ông thua bằng hành động ngắn (「俺は、頭を下げた」) nhưng vẫn giữ nguyên tắc (「だが、管には触らなかった」).
5. Con số chỉ làm dao đo bất công (「日が暮れるまで、かかった。配分金は、一円も増えなかった」) — CẤM giảng chế độ.
6. Bất công LẬT NGƯỢC: chịu thiệt xong lại bị chính kẻ đó khiếu nại — 3 lời buộc tội = 3 câu thoại ngắn liền nhau.
7. Kẻ đáng ghét thứ 2 giẫm thêm TRƯỚC ĐÁM ĐÔNG (「居合わせた会員たちが、いっせいにこちらを振り向いた」).
8. CHỈ SAU cảnh nhục mới tự giới thiệu: tên · tuổi · nghề · số năm + nguyên tắc sống — chính nguyên tắc đó là thứ bị cười.
9. Câu treo cuối báo hậu quả, không lộ kết (「このときの俺は、まだ知らなかった。…ことになるとは」).
10. Câu cực ngắn, mỗi 「」 một đoạn, mỗi câu dựng được 1 hình có MẶT người. Hook dài ~100 giây (600–700 chữ) anh chấp nhận.

**Gợi ý cảnh xung đột cho tập 2** (tab tự chọn/sửa, nhưng PHẢI có kẻ đáng ghét + nhục công khai, và PHẢI nằm trong thân bài):
- Ở việc 交通誘導警備 (điều tiết xe): tài xế xe sang quát 「おい、じいさん、どこ見て旗振ってんだ」 — đúng là **khách quen 20 năm ông từng đo may
  com-lê**, không nhận ra ông. Ông vẫn cúi chào 45° đúng kiểu quầy bách hoá. Tối đó công ty bảo vệ nhận khiếu nại, đội trưởng trẻ mắng ông
  trước cả đội: 「百貨店だか何だか知らないけど、ここじゃ新人なんだよ」.
- Hoặc ở việc 品出し siêu thị sáng sớm: quản lý trẻ bắt ông xếp lại cả kệ trước mặt khách vì "gấp như bán áo sơ mi, chậm".
→ Ghi cảnh chọn vào `series_ctx.txt` mục **`CẢNH XUNG ĐỘT CHO HOOK:`** (3–5 dòng, có tên kẻ đáng ghét, câu thoại chính, người chứng kiến)
  để cả hook (Fable) lẫn thân (Opus) cùng bám một cảnh — tập 1 thiếu dòng này nên anh phải tự viết lại hook.
- Kết truyện vẫn NGHIỆM TÙNG: kẻ đáng ghét không bị quả báo kiểu スカッと; ông tìm được việc "ここだ" nhờ chính tay nghề quầy đồ nam
  (vd: sửa gấu quần/đo size cho khách ở tiệm đồ cũ, hay dạy thắt cà vạt ở hội người cao tuổi) — tab tự chốt, phải có trong `promise.txt`.

## 3. PHẦN A — viết + khoá → giao máy 3 (lệnh chạy tại `E:\CLAUDE\YOUTUBE\h2dev`)
**A1. HỒ SƠ (tay)** — tạo thư mục tập; ghi ngay **C3** sheet = đường dẫn thư mục (đọc header dòng 1 trước, cấm xoá dữ liệu).
- `competitor.txt` = transcript `BdLooNSganA`.
- `series_ctx.txt`: dòng 1 `NGHỀ CẤM: …` · dòng 2 `NGHỀ MỚI: 百貨店の紳士服売り場（38年）— …thói quen…` · dòng 3 `CẢNH XUNG ĐỘT CHO HOOK: …`
  · `SỐ ĐƯỢC PHÉP: …` · rồi `[Dn]` kèm URL CHÍNH THỨC cho mọi số chế độ (年金 日本年金機構; 在職老齢年金 nếu dùng; 最低賃金 tỉnh nhân vật ở;
  警備員の新任教育 (giờ đào tạo bắt buộc) — tra 警備業法施行規則/警察庁; 熱中症 nếu dùng). Mẫu cách viết `[Dn]`:
  `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep01-silver-haibunkin\series_ctx.txt`. Không tra được → BỎ số đó. Số cá nhân (lương hưu
  nhân vật, tiết kiệm) tự đặt nhưng cộng khớp.
- `title.txt` = B3 bỏ phần dịch. `promise.txt` = 1–2 câu Nhật: cảnh nhục + hành trình 5 việc + điều ông tìm được (mẫu: `...\ep01-silver-haibunkin\promise.txt`).
- Đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\senior_korekara\COMMENT_INSIGHT.md` (phần video `BdLooNSganA`) → đưa 1–2 nỗi lo thật vào truyện.

**A2. VIẾT + KHOÁ** (chạy nền, ~12–15 phút; tự DỪNG sau khi khoá và tự giao máy 3):
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep02-baito-go-shoku --den B3G
```
- Đọc log: dòng `[H4] HOOK_LOCKED …` → mở `assets\N-senior_korekara\ep02-baito-go-shoku\hook\hook_locked.txt` tự chấm theo §2
  (câu 1 có phải thoại kẻ đáng ghét? có nhục công khai? tên tuổi có nằm SAU cảnh nhục?). Không đạt → báo anh trong báo cáo
  (anh sửa ở máy 3 như tập 1), KHÔNG tự viết lại (luật: hook đã khoá không tự viết lại).
- **ESCALATE** (S3 còn lỗi sau 2 patch — tập 1 dính 2 lần): viết `viec_tay.txt` NGẮN, mỗi dòng 1 việc thay thế NGUYÊN VĂN, dòng đầu
  "CHỈ SỬA ĐÚNG N CHỖ, KHÔNG ĐỔI CÂU KHÁC" → rồi chạy lại đúng lệnh A2 (không `--viet-lai-kich-ban`). Thiếu chữ → một việc "NỚI: viết thêm
  X chữ vào 2–3 cảnh thân, KHÔNG số liệu mới" nêu rõ cảnh nào. Thoại dính lời dẫn (「…」 nằm giữa câu kể) → thay nguyên văn thành câu riêng.
  Opus trả "cắt giữa câu" → chạy lại là được.
- Khoá xong máy tự: chép `script.txt` → `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\Lane-N\ep02-baito-go-shoku\script.txt` + ghi D3 =
  `Chờ kiểm tra kịch bản`. Nếu log báo "ô D3 đang '…' → KHÔNG đè" thì ghi tay đúng ô D3 (xem cách ghi ở §5 bẫy 4).
- **Báo anh rồi DỪNG**: đường dẫn file máy 3 · hook nguyên văn kèm dịch Việt từng câu · số chữ/phút · điểm cần anh để ý.

## 4. PHẦN B — anh báo D3 = `Đã sửa kịch bản` → làm hết tới giao máy 2
```bat
:: B1. nhận bản anh sửa (0 LLM, không sửa 1 chữ; hook tự khoá lại nếu anh sửa đầu bài)
py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile senior_korekara --slug ep02-baito-go-shoku
```
Anh nhắn hook mới trong chat (như tập 1) thay vì sửa file → ghép vào ĐẦU `script.txt` thay hook cũ (thân giữ nguyên, chỉ khi anh cho phép),
khoá hook bằng `hook_stage.khoa(...)`, chỗ thân lệch với hook mới → `viec_tay.txt` → `gate_common.ghi_lock(...,'ESCALATE')` → lệnh A2 → giao máy 3 lại.

**B2. CAST** — viết `assets\N-senior_korekara\ep02-baito-go-shoku\characters.json` (khuôn: `...\ep01-silver-haibunkin\characters.json`):
`ke` (ref:false, clone_2669111) + nhân vật chính (`main:true`, look ĐÚNG 65 tuổi, khoẻ, gọn — ⛔ không vẽ già hơn tuổi) + mọi vai có thoại
(`ref:true`, `master:"_ref_<id>/001.png"`), vai 1 cảnh không thoại để `ref:false`. Mỗi vai có `master_prompt_<id>.txt` (chép khuôn
`...\ep01-silver-haibunkin\master_prompt_makino.txt`, thay đoạn look). Rồi:
```bat
py -3.13 -X utf8 pipeline\gan_vai.py --profile senior_korekara --slug assets\N-senior_korekara\ep02-baito-go-shoku
py -3.13 -X utf8 -c "import sys,json;sys.path.insert(0,'pipeline');import make_video as m;p=json.load(open('profiles/profiles/senior_korekara.json',encoding='utf-8'));print(m.Job(p,'ep02-baito-go-shoku').masters_from_bible())"
```
Xem bằng mắt từng `_ref_<id>\001.png` (tuổi, giới, không collage). Kể ngôi 1: câu không mở bằng 「 mà gan_vai gán cho vai phụ → đổi về `ke`.

**B3. PROMPT ẢNH THÂN** (chỉ `--only`; ⛔ máy 1 CẤM B4/B5 — tốn tiền thật):
```bat
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep02-baito-go-shoku --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep02-baito-go-shoku --only B5P
```
B5P báo "bỏ qua (đã xong)" mà img_prompts mới → xoá khoá `B5P` trong `state.json` rồi chạy lại.

**B4. HOOK — dựng tay theo CÂU** (⚠️ `hook_storyboard.py` chỉ làm được hook 20–30 giây/7 shot; hook ~100 giây của lane này nó dồn sai giờ + lệch lời → KHÔNG dùng):
1. Chép `...\ep01-silver-haibunkin\hook\_mk_hook.py` → `...\ep02-baito-go-shoku\hook\_mk_hook.py`. In số câu:
   `py -3.13 -X utf8 -c "import sys;sys.path.insert(0,r'E:\CLAUDE\YOUTUBE\h2dev\pipeline');import cau_vai;[print(i,c['text']) for i,c in enumerate(cau_vai.tach_cau(open(r'E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\script.txt',encoding='utf-8').read())[:60],1)]"`
2. Sửa hằng mô tả nhân vật + `SHOTS`: mỗi cảnh = 1–4 câu liền nhau, voice ≤ ~9 giây (~55 chữ), cảnh có MẶT + cảm xúc; thoại kẻ đáng ghét =
   cận mặt hắn; câu "cả phòng quay lại nhìn" = ông giữa khung, người sau mờ. Hồi ức nghề cũ (quầy đồ nam bách hoá) = 1–2 cảnh, ông trẻ hơn ~12 tuổi.
   Cảnh cuối (câu treo) có thể là đồ vật/ghế trống. Sửa `sfx` (số câu + tên file) và `cau_ket_hook`. Chạy → script tự assert ghép lời = hook.
   Nếu `hook\` còn `hook_storyboard.json` / `flow_prompts\` do máy tự sinh (B5W hay sinh khi chưa có ảnh hook) → dời vào `hook\_cu_<giờ>\`,
   kẻo đóng gói gửi kèm storyboard sai cho máy 2.
3. Ảnh hook + SFX + Grok (chạy nền; Grok ~2–3 phút/clip, 1 tài khoản FREE = 1 clip/24h, pool còn >100 tài khoản):
```bat
py -3.13 -X utf8 pipeline\gen_images.py --prompts E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook\img_prompts_hook.txt --out E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook\img --cast-root E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku --quality low
py -3.13 -X utf8 tools\hook_lane_g\sfx.py E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook "01_xxx.mp3|<mô tả tiếng Anh>|0" "99_nen_xxx.mp3|<nền>|1"
set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
py -3.13 -X utf8 tools\hook_lane_g\grok_1tk.py E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook 30
py -3.13 -X utf8 pipeline\qc_hook_clip.py --hook E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook --all
```
   Xem ảnh hook + khung giữa/cuối từng clip BẰNG MẮT (ghép 1 tấm lưới rồi Read). Clip lạc đề/đổi áo/đổi mặt → dời sang `clip\_sai\`, chạy
   lại `grok_1tk.py` (nó chỉ làm clip còn thiếu). Sol FAIL vì chi tiết nhỏ (vũng nước chưa rõ, tay chưa vò giấy) → giữ, ghi lý do trong báo cáo.
   Xong kiểm 0 Chrome GPM: `powershell -c "(Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | ? {$_.CommandLine -match 'GPMLogin'} | measure).Count"`.

**B5. ⭐ VIDEO HOOK XEM THỬ CÓ PHỤ ĐỀ VIỆT (anh yêu cầu mọi tập)** — máy 1 dựng để anh duyệt, KHÔNG phải bản giao:
```bat
py -3.13 -X utf8 pipeline\tts_voicevox.py --script E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook\hook_locked.txt --profile senior_korekara --out E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\hook\xem_thu\hook_voice.mp3 --vai E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\vai.txt --chars E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku\characters.json
```
Chép `...\ep01-silver-haibunkin\hook\xem_thu\_dung_xem_thu.py` sang `...\ep02-baito-go-shoku\hook\xem_thu\`, **viết lại dict `VI`** (1 câu Việt
cho mỗi câu hook, đúng số câu `hook_voice_roles.json`), chạy → ra 2 file:
`hook_xem_thu_VI.mp4` (chỉ phụ đề Việt, chữ vàng to) + `hook_xem_thu_JP_VI.mp4` (Nhật dưới + Việt trên). Trích 2 khung kiểm chữ hiện đúng.
Gửi anh đường dẫn cả 2 file.

**B6. HOOK_TAP.md** → điền hết `<<CẦN NGƯỜI>>` (dịch từng dòng = lấy từ dict `VI`, điều CẤM hứa, ảnh thumbnail mạnh nhất):
```bat
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku --profile senior_korekara
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep02-baito-go-shoku --profile senior_korekara --kiem
```

**B7. GIAO MÁY 2** (tự ghi D3=`Done`, H3=`cần ảnh (N ảnh, ~Xđ)`):
```bat
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job senior_korekara ep02-baito-go-shoku
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list senior_korekara
```
Đọc lại `_BANGIAO.txt`. TITLE: lane `title_auto=false` → không tự gọi; nhắc anh lệnh `py -3.13 -X utf8 pipeline\goi_title.py --bat senior_korekara`.

## 5. BẪY ĐÃ DÍNH Ở TẬP 1 (30/09)
1. `--viet-lai-kich-ban` CHỈ dùng khi anh bảo viết lại cả tập; nó bỏ hook đã khoá. Trước khi dùng: sao lưu `script.txt`, `hook\`, `state.json` vào `_truoc_viet_lai_<giờ>\`.
2. Tập làm lại: dời file của bản cũ (characters/vai/img_prompts/HOOK_TAP, `hook\clip|img|sfx|qc`) vào `_cu_<giờ>\` TRƯỚC khi chạy — nếu không B5W/đóng gói
   dùng nhầm đồ cũ. Thư mục giao `jobs\Lane-N\<slug>\` cũng phải dời đồ cũ vào `_cu_khong_dung_<giờ>\` (đóng gói không tự xoá file thừa).
3. `dong_goi_may2 --job` KHÔNG đè ô H đã có chữ → đóng gói lại sau khi đổi số ảnh thì tự ghi H = `cần ảnh (<N mới> ảnh, ~<tiền>đ)`.
4. Ghi 1 ô sheet an toàn (không xoá gì): `py -3.13 -X utf8 -c "import sys,json;sys.path.insert(0,'pipeline');import review_may3 as r;p=json.load(open('profiles/profiles/senior_korekara.json',encoding='utf-8'));dg,tab,d=r._sheet(p,'ep02-baito-go-shoku');r._ghi_d(dg,tab,d,r.TRANG_THAI_CHO+chr(10)+str(r.review_di(p,'ep02-baito-go-shoku')))"`.
5. Hook Sol chấm câu 「このときの俺は、まだ知らなかった」 là "câu yếu" — nhưng `style_rules` của anh BẮT kết kiểu này → giữ, báo anh 1 dòng.
6. Hook ~100 giây: một số cảnh dài hơn clip 6s → bản xem thử giãn chậm tối đa ×1,6 rồi giữ khung cuối; cảnh > 9 giây thì tách 2 cảnh.
7. Nút đăng ký (B8n) ĐÃ bật cho lane (chuông riêng `6_moc_cam`) — máy 2 tự phủ; avatar đang TẮT tới khi anh setup kênh (xem `_subscribe_note` trong profile).
8. Luôn đếm `_ref_*/001.png` thật, đừng tin chữ "xong" trong log (gpti2 từng rớt câm).

## 6. ĐIỂM DỪNG
- Sau PHẦN A (đã giao máy 3) — chờ anh.
- Hook khoá ra mà KHÔNG có kẻ đáng ghét/cảnh nhục → vẫn giao máy 3 nhưng ghi đỏ đầu báo cáo để anh sửa hook.
- Grok trả video không liên quan ảnh gốc hàng loạt / pool hết lượt → dừng, báo anh.
- Mọi lệnh xoá dữ liệu sheet: CẤM. Chrome: cấm kill chung, chỉ `gpm_grok_mo.py --close` do tool gọi.
