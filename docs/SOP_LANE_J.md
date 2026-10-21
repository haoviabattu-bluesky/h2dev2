# SOP — LANE J: 定年後の夫婦 (hưu trí Nhật, MANGA kể chuyện ngôi 1「俺」— một cặp vợ chồng và một quyết định lớn sau hưu)

> Kênh mẫu: 老後のゴローさん (Ông Gorō tuổi già) `UCxD2Exs2Q4lf7x0Q28OuKvg` — 47 video, ~10.900 sub, trung vị 28.881 view,
> hit 985k / 852k / 571k (đo 2026-09-28).
> Kênh của mình: tên mới anh đặt **J-rougo_futari** (NOTE dòng 7, mail `wunehasneha@gmail.com`) — **anh TỰ setup kênh**, máy 1 chỉ làm nội dung.
> Profile TẠM giữ mã `teinengo-fuufu` (anh 2026-09-30: "mã lane để sau anh cho sửa") · thư mục `assets\J-teinengo-fuufu\` · tab sheet **`Lane-J`** (anh tạo 30/09, thay tab `teinengo-fuufu` cũ — tab cũ giữ, không dùng nữa).
> Cửa vào: `docs\BAT_DAU_LANE\teinengo-fuufu.md`. Lập 2026-09-30 (Giai đoạn 2) theo **quy trình chuẩn mẫu Lane M**
> (`docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §00), khung truyện chép từ Lane F (lane truyện 7 chặng, không mục).

| Anh nói | Profile | SOP |
|---|---|---|
| "hưu trí Nhật · manga kịch tính tiền · Lane F" | `teinengo-real` | `SOP_LANE_F.md` |
| "vợ chồng sau hưu · manga cảm xúc · Lane J · rougo_futari" | **`teinengo-fuufu`** | **file này** |
| "hưu trí Nhật · manga N選 việc làm · Lane M" | `teinengo-anaba` | `SOP_LANE_M.md` |

Nguồn nghiên cứu:
```
E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\
├── CHANNEL_DNA_GOLO.md                DNA 11 mục dựng từ 47/47 video (4 nguyên nhân nổ/tụt đo trên 46 hook)
├── PHAN_TICH_BINH_LUAN_15VIDEO.md     648 bình luận (vợ chồng like cao nhất 447; chê hình vẽ già 446)
├── VIDEO_ANALYSIS_GOLO\*.json          hồ sơ video (15 cũ + 4 bổ sung 2026-09-30: gpVr3OYPA-E · bZp51t9b-_g · Nu-1bKzC6tY · Hgo2qFDF0bM)
└── all47_full.json · transcripts_top15.json · comments_15videos.json
E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougo-no-goro\
├── CHANNEL_DNA.md          K1+K2 8 video (bản mỏng; mâu thuẫn thì tin CHANNEL_DNA_GOLO.md)
├── VIDEO_ANALYSIS\*.json   đầu vào K3 retrieve_videos.py (10 video top)
├── COMMENT_INSIGHT.md      ⭐ khối "## ĐƯA VÀO PROMPT" tự nhồi vào S2
├── TAG_STATS.json
└── _raw\transcripts.json   15 transcript (8 K1 + 7 bổ sung) — dùng đo gate + làm competitor.txt
```

---

## 0. BẢNG DELTA — khác Lane F/M chỗ nào

| Khâu | Lane F (teinengo-real) | Lane M (teinengo-anaba) | **Lane J (file này)** |
|---|---|---|---|
| Trục | TIỀN mất dần | việc làm 60+ (N選) | **QUAN HỆ VỢ CHỒNG sau một quyết định lớn** |
| Người kể | 俺, đổi theo tập | 俺 = 田島誠 cố định | **俺 = chồng 63–70, đổi theo tập (kênh rời rạc)** |
| Cấu trúc | 7 chặng `sections` | xếp hạng 第7位→第1位 | **7 chặng `sections`: hook → ngày quyết định → cú tát → cặp đối chứng → LỜI THẬT CỦA VỢ → dựng lại → kết** |
| Khoá mặt | @REF/@REF2 trong tập | fixed_refs xuyên tập | **@REF chồng + @REF2 vợ trong tập (+ master đối chứng)** |
| Hình | anime tỉ lệ người thật | chibi | **anime tỉ lệ người thật, vẽ ĐÚNG tuổi, không già quá tuổi** (bình luận 446👍; AGE LOCK 01/10) |
| Giọng | clone kênh mẫu F | đa giọng 7 clone | **CHƯA CHỐT** (§0c) |
| Thời lượng | 22' | 23' | **22'** |
| mode | fiction_facts | fiction_facts | **fiction_facts** (年金/年金分割/財産分与/thuế/bảo hiểm phải có nguồn) |

## 0b. CHANNEL ANALYZER — K1+K2 ĐÃ CHẠY (8 video) + bổ sung tay lên 10 video top
K1+K2 chạy 2026-09-16 (8 video) ở máy 2 → copy `results\channel_dna\rougo-no-goro\` sang `docs\channel_dna\rougo-no-goro\` (2026-09-30).
TRENDING-RESEARCH làm tiếp 47/47 video bằng tay (scratch_golo). 2026-09-30 bổ sung: 7 transcript vào `_raw\transcripts.json`
và hồ sơ phân tích cho 4 video top 10 còn thiếu. **Không chạy lại K1+K2** (cổng `channel_analyzer.py` sẽ chặn — đúng thiết kế).

Mỗi tập chọn `competitor.txt` = video gốc ghi ở cột T (VIDEO GỐC) tab `Lane-J` (§1b). Muốn thêm 1–2 video cùng dạng thì dùng K3 (0 LLM, 0 mạng):
```bat
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 retrieve_videos.py --dna-dir ..\docs\channel_dna\rougo-no-goro --topic "<đề tài tập, tiếng Nhật>" --top-n 3
```

## 0c. GIỌNG — ĐÃ CLONE 7 LOẠI × 2 MẪU, CHỜ ANH CHỌN (2026-09-30)
Kênh mẫu (Gemini nghe 20 đoạn × 5 phút của 4 video top): **2–4 diễn viên thật cho mọi vai** — 1 nam chính đọc người kể + phần lớn
vai nam (kể cả giả giọng trẻ), 1 nữ đọc mọi vai nữ; ông lão/nam trẻ/người dẫn kết đôi khi là người khác. Mình tách theo VAI để đa giọng:
1 chồng-người kể · 2 vợ · 3 ông lão/người đi trước · 4 nam đồng niên/bạn · 5 nam trẻ · 6 nữ phụ · 7 người dẫn ngôi 3 (lời kết).
14 bản clone + mẫu gốc: `E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\_voice_clone\compare_clone.html` (`mau_goc.json` · `clone_ket_qua.json`).
**Chốt 2026-09-30:** người kể/chồng = `1b_chong_saeki` → `clone_2669068` (`voice.id` + `voice.narrator`, speed 1.0, **char_rate 331,0 đo
calibrate** → 22' = 7.282 chữ). 1a Fujisawa bị loại (nghe trẻ) → 3 ứng viên già hơn 1c Suzuki `clone_2669121` · 1d Tetsuo `clone_2669122` · 1e Sato
`clone_2669120` → **anh chọn 1c** (vào `cast_bank`: chồng cặp đối chứng / nam 65–70). Nhóm 2–7 anh để em chọn: giữ cả a+b ở 2 (vợ dịu/vợ cứng),
3 (ông lão), 4 (bạn hào sảng / chồng cộc), 6 (nữ lớn tuổi / nữ nhân viên); nhóm 5 giữ 5a, nhóm 7 giữ 7a. **Đã xoá trên ai33** 1a/1d/1e/5b/7b.
Bảng vai → voice_id: `profile.voice.cast_bank`. Lane đa giọng (`voice.provider=ai33` → tts_voicevox + `gan_vai.py`, `gate.dialogue_own_sentence=true`).
Bẫy: ai33 `voice-clone` trả `Something went wrong` (không nói lý do) khi mẫu >30 giây → cắt 28 giây. Anh chọn xong → khai
`voice.narrator` + `voice.fixed_cast`/`cast_bank` như Lane M, XOÁ clone không dùng (`DELETE /v3/text-to-speech/voice-clone/{id}`), rồi calibrate.

(Ghi chú cũ lúc chưa làm:)
Kênh mẫu: 1 người kể NAM thật xuyên 7 tháng (jitter 26–33%, F0 132–150 Hz). Hai đường, **anh chọn**:
- (a) clone giọng kênh mẫu từ 20–30s sạch của `Scnn76gZ8E8` (skill `openspeaker_voice_clone.md`) — giọng người thật, phải hỏi anh trước khi giữ voice_id;
- (b) giọng kho ai33 nam trung niên (`py -3.13 pipeline\voice_bank.py --find ...`).
KHÔNG dùng lại `clone_2658911` (Lane F) hay 7 clone Lane M. Chốt xong:
`py -3.13 -X utf8 pipeline\calibrate.py --profile teinengo-fuufu` → ghi `voice.id`, `voice.char_rate`, `voice.char_rate_measured_at`.
Chưa có char_rate đo thật thì `make_video` DỪNG (hàng rào #1).

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-30)
- Model/luồng = mẫu Lane M: `flow=lean` · `engine=claude_p` · S2 `claude-fable-5-1` (05/10) · S4 `claude-opus-5` · `sol_qc=false` (S5L kiểm lời hứa tiêu đề vẫn bật) · `soat=gptweb` · `chan_buoc2_may1=true`.
- `structure_block` 7 chặng + `budget.sections` (hook 6% · ngày quyết định 12% · cú tát 22% · đối chứng 18% · lời thật của vợ 14% · dựng lại 18% · kết 10%).
  Tỉ lệ ước từ hồ sơ video — **đo lại sau ep01**.
- 4 luật nổ/tụt của kênh mẫu (DNA 4C, đo 46 hook) viết thẳng vào `structure_block`: mở bằng CẢNH · có ĐỐI CHỨNG · ngôi 俺 (cấm 彼 ở 150 chữ đầu) · cấm chủ ngữ chung chung.
- Kênh mẫu có 1 nhân vật cố định **五郎さん** (Ông Gorō) nói đạo lý qua 1 ẩn dụ ở ~55–70% bài — **CẤM chép nhân vật/tên này**. Lane J dùng người đối chứng của TẬP.
- Nhân vật chồng 63–70, vợ 60–68 (cấm trẻ hơn khán giả — video 58 tuổi rel_VPD 0,10); **HÌNH cũng vẽ ĐÚNG tuổi** (AGE LOCK 01/10, cấm làm trẻ; chỉ tránh già quá tuổi).
- `fact_exempt_units` miễn 万円/円/tuổi/ngày — số CÁ NHÂN hư cấu; số CHẾ ĐỘ vẫn phải có trong `series_ctx.txt` [Dn] kèm URL, kiểm ở lớp soát GPT web + lớp 3.
- `publish.listing_external=true` (TITLE-RESEARCH làm tiêu đề/mô tả/thumbnail), `title_auto=false` (anh `--bat` mới chạy).
- `outro_line` = 「最後までご覧いただき、本当にありがとうございました。ご夫婦で話すきっかけになりましたら、高評価とチャンネル登録で応援していただけると嬉しいです。」
  (Cảm ơn đã xem tới cuối. Nếu video thành dịp để hai vợ chồng nói chuyện với nhau, xin ủng hộ bằng nút thích và đăng ký kênh.)

## 1b. 10 TẬP ĐẦU + CỘT SHEET TAB `teinengo-fuufu`
Cột A STT · B NỘI DUNG (tựa Nhật + dịch) · C FOLDER · D KỊCH BẢN · E TITLE-DESCRIPTION · F TAGS · G THUMBNAIL · H STATUS-IMG · I VIDEO · J LIST · K GHI CHÚ (video gốc).
**Thứ tự = view video gốc giảm dần** (anh 2026-09-30: "ưu tiên điểm view + điểm trung vị cao"). Mỗi tập bám 1 video gốc (70/30), đổi
nhân vật/tình tiết/địa điểm, bẻ về trục VỢ CHỒNG kể cả khi video gốc không phải chuyện vợ chồng. **CHỈ tập anh chỉ định mới bắt đầu.**
Danh sách đầy đủ ghi trên sheet tab `Lane-J` (A2:B11 tiêu đề · K2:K11 ghi chú, K2 = hướng dẫn chạy tập 1 · T2:T11 link video gốc) — sheet là nguồn chân lý, bảng dưới là bản sao lúc lập:

| STT | Video gốc (view · ×trung vị) | Góc của mình |
|---|---|---|
| 1 | `Scnn76gZ8E8` 985k · 34,1× (du thuyền bằng 退職金) | chuyến đi xa bằng 退職金 → im lặng giữa hai người → lời thật của vợ |
| 2 | `xxMKVprVh-I` 852k · 29,5× (熟年離婚 VS 家庭内別居) | 卒婚 vs 熟年離婚 — 2 lựa chọn, 5 năm sau |
| 3 | `r4jNE1oTv8Q` 571k · 19,8× (70 tuổi còn làm vs nghỉ 65) | chồng làm tới 70 vs đồng kỳ nghỉ 65 — nhìn qua mắt 2 người vợ |
| 4 | `gpVr3OYPA-E` 356k · 12,3× (婚活バスツアー) | tái hôn tuổi 60+ — 1 năm sống chung đầu tiên |
| 5 | `hyLpBbmnvIA` 324k · 11,2× (年金額 và bữa ăn) | 2 cặp vợ chồng khác mức thu, cùng 1 siêu thị |
| 6 | `OIeZvtYreOg` 246k · 8,5× (thói quen "não trẻ") | vợ chồng mỗi ngày nói chuyện 3 phút → thói quen buổi sáng chung |
| 7 | `bZp51t9b-_g` 221k · 7,6× (移住 về quê) | chuyển về quê của VỢ (đảo chiều video gốc) |
| 8 | `Nu-1bKzC6tY` 178k · 6,2× (熟年離婚 5 năm sau) | bị vợ đề nghị ly hôn — 5 năm sống một mình |
| 9 | `Hgo2qFDF0bM` 177k · 6,1× (持ち家 vs 賃貸) | bán nhà chuyển gần con vs ở lại nhà cũ — 2 cặp đồng kỳ |
| 10 | `B9BIhRhlAU4` 168k · 5,8× (việc làm tuổi 50–60) | chồng xin làm cùng chỗ part-time của vợ |
Tránh trùng: Lane F ep01 (chồng nghỉ 60/vợ làm tiếp) · F ep06 (bán chung cư vì 修繕積立金) · G ep01/ep05 (習慣, 夫婦の距離 dạng list).

## 2. LỆNH CHẠY — "chạy tập X" = làm HẾT máy 1 rồi giao máy 2 (giống Lane M §2)
Điều kiện trước tập 1: §0c giọng + char_rate ✅ · 2 Project ChatGPT soát (§4) ✅.
```bat
cd E:\CLAUDE\YOUTUBE\h2dev
:: A. HỒ SƠ (tay, tab lane) — assets\J-teinengo-fuufu\epNN-<slug>\, ghi cột C sheet ngay
::    competitor.txt (transcript video gốc cột K, lấy từ docs\channel_dna\rougo-no-goro\_raw\transcripts.json) ·
::    series_ctx.txt (SỐ ĐƯỢC PHÉP + [Dn] URL chính thức: 日本年金機構/厚労省/国税庁/裁判所 cho 年金分割・財産分与) ·
::    title.txt = cột B (bỏ phần dịch) · promise.txt
:: B. VIẾT + KHOÁ (Fable 5.1 viết hook+thân, Opus 5 vá, S5L lời hứa) — tự dừng sau LOCK
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-fuufu --slug epNN-<slug> --den B3G
:: C. SOÁT CHATGPT WEB
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-fuufu --slug epNN-<slug> --lan1
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-fuufu --slug epNN-<slug> --chot
::    viec_tay.txt (thay thế NGUYÊN VĂN, độ dài dự kiến < trần) → ghi_lock ESCALATE → chạy lại B
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path('assets/J-teinengo-fuufu/epNN-<slug>'),'ESCALATE',reason='soat ChatGPT web')"
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-fuufu --slug epNN-<slug> --den B3G
::    lớp 3 đọc bản khoá (§2b) → soat_kb_gptweb.py --xong
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile teinengo-fuufu --slug epNN-<slug> --xong
:: D. PROMPT ẢNH (--only, KHÔNG --from: máy 1 cấm B4/B5)
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-fuufu --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-fuufu --slug epNN-<slug> --only B5P
:: E. HOOK (máy 1 làm trọn hình): storyboard → ảnh hook → clip Grok 6s → SFX → HOOK_TAP.md
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile teinengo-fuufu --slug epNN-<slug>
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\epNN-<slug> --profile teinengo-fuufu
:: F. GIAO MÁY 2 (tự ghi D = Đã giao máy 2 + K = lệnh máy 2, H = cần ảnh)
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job teinengo-fuufu epNN-<slug>
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list teinengo-fuufu
```
Chi tiết hook/Grok/master vai phụ: làm y `SOP_LANE_M.md` §2 mục F (Grok clip **6 giây**, 10 giây ăn 429).

### 2b. Lớp 3 — Claude Code đọc bản khoá, kiểm riêng lane
- Hook đã khoá theo luật 21/10 (bám sát cấu trúc hook video gốc) — lớp 3 không chấm hook theo luật cũ (mở bằng CẢNH / câu khoá).
- Thân: không 彼/男性/高齢者/多くの人 làm chủ ngữ chung chung; có cặp/người ĐỐI CHỨNG có tên + tuổi + số.
- Câu vợ ở chặng 2 được lật ở chặng 5; nỗi đau vợ là việc CỤ THỂ; chồng không quát/không "tao nuôi mày".
- Số chế độ khớp [Dn] đúng điều kiện (額面/手取り, trả 2 tháng/lần, phải làm thủ tục, 年金分割 chỉ phần 厚生年金); số cá nhân cộng khớp mọi mốc.
- Kết: thoả hiệp thực tế + câu hỏi 2–3 ngã rẽ + đủ cảm ơn/高評価/チャンネル登録. Không 五郎さん, không câu đặc trưng kênh mẫu.

## 3. GATE — ngưỡng đã ĐO (chi tiết trong `profile.script.gate._gate_note` + `goi_dang._nguon`)
| Chỉ số | Giá trị | Nguồn đo (15 transcript `_raw` + 47 tiêu đề) |
|---|---|---|
| target_minutes | 22 | 47 video 20,6–26,8' (trung vị ~23,3'); top 3 = 21,3' / 20,6' / 23,2' |
| list_item_count | 0 | lane truyện |
| câu (comma / breath) | 0,6–2 / 6–12 | câu trung bình 13,9–23,5 chữ (12/15 video 15–18); ASR không ghi 、 → SUY như Lane F, đo lại sau ep01 |
| dialogue_ratio_max | 0,30 | câu đuôi hội thoại 10–24% (proxy) — nới hơn F (0,20) vì trục vợ chồng |
| title_len | 30–48 | 47 tiêu đề p25 36 · trung vị 42 · p75 45 (kể cả【漫画】) |
| hook_chars (120 giây đầu) | 500–720 | 550–693 chữ ở tốc độ đọc 275–347 chữ/phút |
| goi_dang contradiction / title_core / promise | 40s / 45s / 60s | câu mâu thuẫn đầu tiên trung vị 25s (10/15 ≤36s); câu khoá 17–45s; mốc thời gian + tuổi ≤45s ở 7/7 video VPD cao |
| goi_dang title_core_len | 26–44 | tiêu đề bỏ【漫画】 |
| seconds_per_image | **13,6** | ĐO 30/09 trên `Scnn76gZ8E8`: 94 ảnh thật / 21,3' (trung vị 14,0 · 5 phút đầu 12) — xem §7 |

## 4. SOÁT CHATGPT WEB — ĐÃ DỰNG 2026-09-30
2 Project tên `teinengo-fuufu` (Project-only memory, Instructions + 4 file `E:\CLAUDE\YOUTUBE\h2dev\CHATGPT_PROJECTS\J-teinengo-fuufu-script\`),
mỗi tài khoản 1 hội thoại giao vai (GPT trả "Hiểu.") — link ở `profile.script.soat_gptweb.urls`. Tạo bằng
`py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chatgpt_web\tao_project_soat.py --profile teinengo-fuufu --dir CHATGPT_PROJECTS\J-teinengo-fuufu-script --ghi`
(dùng được cho lane khác; chạy lại = cập nhật Instructions/file, không tạo trùng). acc2 có sẵn Project `J-teinengo-fuufu` của YT-TITLE-RESEARCH — KHÁC cái này.

(Ghi chú cũ:)
Cần 2 Project ChatGPT (tên = `publish.sheet_tab`) trên 2 tài khoản, mỗi Project 1 hội thoại đã giao vai nhà văn; điền
`script.soat_gptweb.urls.acc1/acc2` + `projects.<acc>{id,ten}`. Cách làm + luật cổng: `SOP_LANE_M.md` §1e + `pipeline\gptweb_pool.py`.
`boi_canh` / `cau_truc` / `rang_buoc` đã khai sẵn trong profile.

## 5. LUẬT CỨNG LANE J
1. Trục VỢ CHỒNG — không trượt sang F (tiền mất dần) hay G (list vui/rẻ).
2. Có ĐỐI CHỨNG · ngôi 俺 · cấm chủ ngữ chung chung (DNA 4C: 3,18× / 2,09× / 13,5× / 3,7×). Hook: luật 17/10 (`E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`).
3. Nhân vật là KHÁN GIẢ (chồng 63–70), vấn đề ở HIỆN TẠI, không tương lai xa.
4. Số chế độ có nguồn — rủi ro số 1 (khán giả bắt lỗi lương hưu 3 lần trong 648 bình luận).
5. Kết thoả hiệp thực tế, không phép màu. Câu hỏi 2–3 ngã rẽ cho vợ chồng khán giả.
6. Hình: vẽ ĐÚNG tuổi (cấm “N but looks M”), cấm già quá tuổi: tóc bạc trắng toàn đầu/lưng còng/đồ tối kiểu 昭和.
7. Không chép 五郎さん, tên nhân vật, câu đặc trưng hay tiêu đề nguyên văn của kênh mẫu.

## 6. HOOK
> Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

| | |
|---|---|
| Cách dựng hình | `manga_anime_ref_grok`: ảnh anime khoá mặt chồng/vợ của tập → clip Grok 6s + SFX |
| Công tắc | BẬT (`enabled:true`, `visual_kind:video_sinh`, `sfx:false`, `nhac_nen:true`, độ dài hook ≈ hook gốc, chỉ nhạc nền: `docs/QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md`) |

## 7. CÒN TREO (nói thẳng)
- ~~Giọng + char_rate (§0c)~~ XONG 30/09 (11 clone, char_rate 331).
- ~~2 Project ChatGPT soát (§4)~~ XONG 30/09, đã đổi tên Project thành `Lane-J` theo tab mới (`tao_project_soat.py` tự đổi tên Project cũ khi tab đổi).
- ~~Đo khung hình kênh mẫu~~ XONG 30/09 (skill video-chuyen-canh trên `Scnn76gZ8E8`, số liệu `E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\_do_khung\`):
  - `do_chuyen_canh.py` dò 253 "ranh giới" nhưng **160 cái chỉ là đổi hộp chữ trên CÙNG 1 ảnh** (bẫy: kênh này đổi chữ ~2,7 lần/ảnh; so điểm ảnh
    ngoài hộp chữ trắng thì tách 2 cụm rõ, <0,02 vs >0,05) → **94 ảnh thật, 13,6 s/ảnh** (trung vị 14,0 · p25 10,7 · p75 17,7 · 5 phút đầu 12 s)
    → `image.seconds_per_image = 13.6`.
  - Chuyển cảnh: 100% cắt thẳng (1 lần mờ-vào), không Ken Burns.
  - Chữ: **dọc (縦書き)**, gothic đậm đen; lời kể = hộp chữ nhật trắng viền đen; thoại「」= **ellipse trắng KHÔNG đuôi** cạnh người nói; không phụ đề đáy
    → cùng kiểu Lane M/L → `assemble.bubble` chép nguyên khối Lane M + `hook_tu_ghep=true` (đa giọng như M).
  - Hình kênh mẫu: tóc bạc trắng/hói, áo sọc — đúng thứ khán giả chê (446👍) → Lane J vẽ ĐÚNG tuổi nhưng không già quá, KHÔNG chép ngoại hình.
- Mã lane/tên tab/thư mục mới `J-rougo_futari` — anh chốt sau; đổi cùng lúc profile id + slug_dir + publish + tab sheet + 2 file tài liệu.
- Kênh chưa có handle/ID (anh tự setup) → `publish.handle`, `channel_id`.
