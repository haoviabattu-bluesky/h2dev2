# SOP — LANE N: シニアの人生これから (đời sống người Nhật 60–75 sau nghỉ việc, MANGA kể chuyện, mỗi tập 1 nhân vật mới, kết nghiệm tùng)

> Kênh mẫu: シニアの人生これから (Cuộc đời người cao tuổi từ giờ trở đi) `@senior_korekara` · `UCL8PFGotC_jY_UbzfRTnnng` —
> 73 ngày tuổi, 64 video, trung vị 6.929 view, hit 443k / 242k / 142k, `trend_vpd` 14,61× (đo 2026-09-28).
> Kênh của mình: **anh TỰ setup kênh** (NOTE dòng 11), máy 1 chỉ làm nội dung.
> Profile `senior_korekara` · thư mục `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\` · tab sheet `Lane-N`.
> ⭐ **Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.** (narrative intro 16/10 + thoại xung đột/cảnh nhục 30/09 đều bỏ) — THẮNG mọi dòng hook cũ trong file này.
> Cửa vào: `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\senior_korekara.md`. Lập 2026-09-30 (Giai đoạn 2) theo **quy trình chuẩn
> mẫu Lane M** (`docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §00), khung truyện theo Lane J (lane truyện, không mục).

Nguồn nghiên cứu:
```
E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_korekara\
├── scored64.json        64 video + VPD + mô tả có timestamp chương
├── transcripts15.json   15 transcript (có mốc giây)
├── comments15.json      779 bình luận
├── hooks_n.json         15 hook đã phân loại (HOOK_LIBRARY)
├── GRID_oZatkpZ0HEc.jpg 13 khung hình thật
└── voice10\             audio 10 video top + voice_report.json + samples\ (đo 3 giọng, 2026-09-30)
E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\senior_korekara\
├── CHANNEL_DNA.md       bản sao CHANNEL_DNA_KOREKARA.md (⚠️ §3 "người thật jitter 17,56%" đo nhầm video kênh J — xem BAT_DAU §2d)
├── COMMENT_INSIGHT.md   ⭐ khối "## ĐƯA VÀO PROMPT" tự nhồi vào S2
└── _raw\transcripts.json 15 transcript — dùng làm competitor.txt
```
(Chưa có `VIDEO_ANALYSIS\` → không dùng K3; video gốc từng tập ghi ở cột K sheet.)

---

## 0. BẢNG DELTA — khác Lane J/M chỗ nào

| Khâu | Lane J (teinengo-fuufu) | Lane M (teinengo-anaba) | **Lane N (file này)** |
|---|---|---|---|
| Trục | quan hệ vợ chồng | việc làm 60+ (N選) | **toàn cảnh đời sống sau nghỉ việc, 1 nhân vật/tập** |
| Người kể | 俺 = chồng | 俺 = 田島誠 cố định | **ngôi 3 「これは…の物語です」 (mặc định) HOẶC ngôi 1 俺/私 — chọn theo tập** |
| Cấu trúc | 7 chặng | xếp hạng 第7位→第1位 | **6 chặng `sections` (đo từ chương của 10 video)** |
| Kết | thoả hiệp vợ chồng | lời khuyên chọn việc | **NGHIỆM TÙNG ấm, không quả báo** |
| Khoá mặt | @REF/@REF2 trong tập | fixed_refs xuyên tập | **@REF/@REF2 trong tập** |
| Hình | (Lane J: đúng tuổi, không già quá) | chibi | **anime bán thực, ĐÚNG tuổi nhưng khoẻ/gọn — không già hơn tuổi; nền đẹp chi tiết (điểm được khen)** |
| Giọng | chưa chốt | 7 clone | **3 clone: Nam A · Nam B · Nữ C (§0c)** |
| Thời lượng | 22' | 23' | **16'** |
| Luật riêng | — | — | **ĐỔI NGHỀ nhân vật chính so video gốc (anh chốt 2026-09-30)** |

## 0c. GIỌNG — ĐA GIỌNG, 3 CLONE TỪ KÊNH MẪU (anh chọn phương án (a) 2026-09-30)
**Anh duyệt 30/09: Nam B + Nữ C ĐẠT; Nam A CHỐT A3 `clone_2669111` (bản đầu `clone_2669054` bị chê). 3 ứng viên đã thử:**
A2 `clone_2669109` (mẫu BdLooNSganA giây 355) · A3 `clone_2669111` (mẫu G5kIPGFNKeY giây 1060) ✅ CHỐT ·
A4 `clone_2669114` (mẫu như A3, không lọc nền). Đo: mọi bản clone Nam A đều lên giọng ~129–140 Hz dù mẫu gốc 111 Hz (cùng câu, Nam B
ra 104 Hz) → lệch cao độ nằm ở bước clone của MiniMax với giọng này, đổi mẫu/lọc nền không sửa được. 
Đo 10 video (resemblyzer + F0): kênh mẫu dùng 3 giọng — Nam A dẫn ngôi 1 (#1 #2), Nam B dẫn ngôi 3 (7/10), Nữ C dẫn tập nữ + lồng
mọi thoại nữ; thoại nam phụ do người dẫn tự đổi giọng.

| Vai | voice_id | Khai ở profile | F0 mẫu → clone · giống mẫu |
|---|---|---|---|
| Dẫn ngôi 3 (mặc định) + vai nam phụ | `clone_2669055` (Nam B) | `voice.narrator` + `voice.id` | 110 → 107 Hz · 0,82 |
| Dẫn ngôi 1 nam 俺 | `clone_2669111` (Nam A, bản A3) | `cast_bank` → characters.json `{"id":"ke","voice":{...}}` | 111 → 129–140 Hz · 0,85–0,86 |
| Mọi nhân vật nữ + dẫn tập nữ ngôi 1 私 | `clone_2669056` (Nữ C) | `cast_bank` (tập nữ kể: cũng đặt vào id `ke`) | 195 → 181 Hz · 0,86 |

- Nghe lại: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\_voice_clone\compare_clone.html` (mở qua
  `py -3.13 -m http.server 8791 --bind 127.0.0.1` trong thư mục đó → `http://127.0.0.1:8791/compare_clone.html`).
- char_rate: `calibrate.py` đo Nam B = **382,8 chữ/phút** (đoạn mẫu, không nghỉ giữa câu) — số KHỞI ĐIỂM. Kênh mẫu thật 249–335
  (trung vị ~300); Lane M cùng kiểu clone đo từ video thật ra 314,6. ⇒ **Đo lại từ video thật ep01** (`char_rate_from`) như Lane M,
  kịch bản ep01 có thể ra ~18–19' thay vì 16'.
- Bình luận chê 「女性の声優…場面に合わせた感情で読んで」 (giọng nữ đọc sai cảm xúc) → thoại nữ ngắn, rõ cảm xúc trong câu chữ.

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-30)
- Model/luồng = mẫu Lane M: `flow=lean` · `engine=claude_p` · S2 `claude-fable-5-1` (05/10) · S4 `claude-opus-5` · `sol_qc=false` (S5L kiểm lời hứa
  tiêu đề vẫn bật) · `soat=gptweb` · `chan_buoc2_may1=true`.
- `structure_block` 6 chặng + `budget.sections` 0,17/0,18/0,19/0,16/0,17/0,13 — đo từ timestamp chương 10 video top.
- **Luật đổi nghề** (anh chốt): nghề nhân vật chính (và vợ/chồng nếu là nhân vật chính thứ hai) KHÁC video gốc; đổi luôn số năm, dụng
  cụ, thói quen, câu thoại nghề. Nghề cấm + nghề đề xuất ghi ở cột K sheet; `series_ctx.txt` mỗi tập PHẢI có dòng
  `NGHỀ CẤM: …` để S2/soát GPT đọc.
- **Bẻ góc #1, #2, #9** (anh duyệt): #1 #2 trùng Lane M (việc làm) → truyện đời 1 người, KHÔNG dạng list; #9 trùng Lane J tập 4 → không
  làm tour xe buýt mai mối.
- Kết NGHIỆM TÙNG với lựa chọn nhỏ khôn ngoan; có ≥1 người đối xử tệ (khán giả chê truyện "ai cũng tốt").
- `fact_exempt_units` (chép Lane J) miễn 万円/円/tuổi/ngày — số CÁ NHÂN hư cấu; số CHẾ ĐỘ vẫn phải có trong `series_ctx.txt` [Dn] kèm URL.
- `publish.listing_external=true`, `title_auto=false` (anh `--bat` mới chạy). Tiêu đề ở cột B là tên làm việc, TITLE-RESEARCH chốt bản đăng.
- `outro_line` = 「最後までご覧いただき、ありがとうございました。これからの暮らしを考えるきっかけになりましたら、高評価とチャンネル登録で応援していただけると嬉しいです。」
  (Cảm ơn đã xem tới cuối. Nếu video giúp anh chị nghĩ về cuộc sống sắp tới, xin ủng hộ bằng nút thích và đăng ký kênh.)

## 1b. 10 TẬP ĐẦU — tab `Lane-N` (A2:B11 + K2:K11, sheet là nguồn chân lý)
Thứ tự = view video gốc giảm dần (×trung vị = view/6.929). **CHỈ tập anh chỉ định mới bắt đầu.**

| STT | Video gốc (view · ×TV) | Nghề cấm → nghề đề xuất | Ghi chú |
|---|---|---|---|
| 1 | `G5kIPGFNKeY` 443k · 64,1× | QC linh kiện điện → 市役所の水道課 (công chức cấp nước) | bẻ góc, không list |
| 2 | `BdLooNSganA` 243k · 35,0× | nhân viên công ty / vợ bếp trường → 百貨店の紳士服売り場 (bán đồ nam bách hoá) | bẻ góc, không 7選 |
| 3 | `mbRCAib7xQM` 143k · 20,6× | thợ may → 和菓子屋の職人 (thợ bánh wagashi) | nữ chính |
| 4 | `uUmbugIRmiY` 109k · 15,7× | tiệm xe đạp → 町の写真館 (tiệm ảnh) | |
| 5 | `yTH_8ls9Jgg` 87k · 12,6× | hành chính cty thực phẩm → 小学校の教員 (giáo viên tiểu học) | Karuizawa → Hokkaido |
| 6 | `qvUvnZwYR2w` 77k · 11,1× | thợ mộc → 靴の修理職人 (thợ sửa giày) | |
| 7 | `SOIklzU69fg` 69k · 10,0× | (nội trợ) → 生け花の先生 (giáo viên cắm hoa) | nữ kể ngôi 1, giọng Nữ C |
| 8 | `KY8NLrQguo0` 59k · 8,5× | GĐ linh kiện chính xác → 老舗旅館の元経営者 (cựu chủ lữ quán) | |
| 9 | `cu_DTPtgYHg` 45k · 6,4× | thợ tiện → 長距離トラック運転手 (tài xế xe tải) | bẻ góc, không tour mai mối |
| 10 | `vfe1rz99eP0` 37k · 5,4× | sales → 郵便局の配達員 (phát thư) | |

## 1d. TẬP 1 `ep01-silver-haibunkin` — chạy thật 2026-09-30 (giao máy 2 13:35)
杉浦寛治 62歳, 市役所の水道課36年, kể ngôi 1 (Nam A). Hook khoá 191 chữ (2 vòng) · S2 Opus 5.5 → 2 patch → LOCK 5.919 chữ ·
ChatGPT web 8,4/10 (hook 8,8): nhận 12 mục + lỗi gõ, phản biện thắng 1 (không nhồi bảng tiền vào hook đã khoá), lớp 3 thêm 3 sửa
(小野寺 bỏ nghề 郵便局の配達 vì là nghề chính tập 10; xoá nhịp "được việc ngồi mát rồi từ chối" chép kết video gốc; 権田 nhờ việc
phải qua センター) → viec_tay 14 thay thế → **LOCK 5.954 chữ sha a2ad433815**. 9 vai CAST · 124 prompt (B5W tự chia) · hook 6 cảnh
= 6 câu, 6 clip Grok 6s PASS (clip 4, 5 làm lại 1 lần). D2=Done, H2=cần ảnh (124 ảnh, ~12.980đ).

**LÀM LẠI 30/09 chiều theo quy trình mới** (anh đổi luật hook): `--viet-lai-kich-ban` → Fable 5.1 hook 2 PA → Opus 5.5 thân → 2 lượt viec_tay →
LOCK → máy 3; anh viết lại hook (~672 chữ, ~105s) trong chat → ghép đầu bài + 1 câu nối thân (「冒頭の、宇佐美さんの家の件は…」) → LOCK 6.246 chữ
sha c4ef6eff12 → máy 3 duyệt nguyên. Nhân vật mới 牧野正行 (13 vai, dùng lại 8 master cũ). 131 prompt · hook 18 cảnh dựng tay (`hook\_mk_hook.py`)
· 18 clip Grok · video xem thử `hook\xem_thu\hook_xem_thu_VI.mp4` + `_JP_VI.mp4`. D2=Done, H2=cần ảnh (131 ảnh, ~12.730đ).
Hướng dẫn tập 2 (gồm mọi bẫy lần này): `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\senior_korekara_TAP2.md`.

**Bẫy tập 1 (đã xử, tập sau nhớ):**
1. `soat_kb_gptweb.py` chặn vì Project tên `N-senior_korekara` ≠ tab `Lane-N` → đã vá cổng nhận thêm tên thư mục `slug_dir`
   của chính lane. Khi anh đổi tên lane: đổi Project + tab + thư mục CÙNG LÚC.
2. `gan_vai.py` gắn câu GIÁN TIẾP (không「」) cho vai phụ: lời tóm tắt 説明会 → giọng nữ nhân viên, lời thuật của 小野寺/権田 →
   giọng họ. Tập ngôi 1: sau gan_vai phải đổi mọi câu không mở bằng「 về `ke` (bản gốc giữ ở `vai.gan_vai_goc.txt`).
3. `hook_storyboard.py` gán nhầm người nói cảnh 1 và cắt giữa câu → dựng hook tay theo câu (`hook\_mk_hook.py`, khuôn Lane M
   ep04). Câu 2 hook dài ~10s → 1 clip 6s giãn chậm.
4. gpti2 30/09 trưa: đơn generate quá 420s (3 master rớt câm — log vẫn ghi "xong"!) và **edit trả `upstream_error` liên tục ~1 giờ**
   (cả prompt thử đơn giản). Master: gọi `gpti2_gen.generate` với `POLL_TIMEOUT=1500` là ra. Ảnh hook 004: cắt cận mặt từ 003
   (`hook\img\004_NGUON.txt`). ima2 (local + VPS) cùng lúc hỏng OAuth. Luôn đếm `_ref_*/001.png` thật, đừng tin chữ "xong".
5. Grok trôi trang phục trong clip (polo → áo khoác) → prompt chuyển động phải ghi rõ "ONLY the same … shirt, NO jacket ever appears".
7. (01/10) Sửa hook tập ĐÃ giao rồi chạy lại `dong_goi_may2.py --job` → tool viết lại `HUONG_DAN_TAP_TIEP_THEO.md` + cột K
   cho tập cũ (lùi về tập đã xong). Chạy xong phải gọi lại `huong_dan_tab_moi.py --loai tiep --slug <tập MỚI NHẤT đã giao>`.
6. Khung ảnh ~124 tính theo char_rate 382,8 (15,5'); video thật chậm hơn (~18') → ~9 s/ảnh thay vì 7,5. Đo char_rate thật từ ep01 rồi chỉnh.

## 2. LỆNH CHẠY — "chạy tập X" = làm HẾT máy 1 rồi giao máy 2 (giống Lane M/J §2)
Điều kiện trước tập 1: 3 giọng ✅ · 2 Project ChatGPT soát (§4) ✅.
```bat
cd E:\CLAUDE\YOUTUBE\h2dev
:: A. HỒ SƠ (tay, tab lane) — assets\N-senior_korekara\epNN-<slug>\, ghi cột C sheet ngay
::    competitor.txt (transcript video gốc cột K, lấy từ docs\channel_dna\senior_korekara\_raw\transcripts.json) ·
::    series_ctx.txt (dòng đầu: NGHỀ CẤM: … · NGHỀ MỚI: … ; rồi SỐ ĐƯỢC PHÉP + [Dn] URL chính thức: 日本年金機構/厚労省/
::       全国シルバー人材センター事業協会/自治体 cho phí viện dưỡng lão, 介護保険…) · title.txt = cột B (bỏ phần dịch) · promise.txt
::    characters.json: tập ngôi 1 → thêm {"id":"ke","voice":{"voice_id":"clone_2669111"}} (nam) / clone_2669056 (nữ)
:: B. VIẾT + KHOÁ (Fable 5.1 viết hook+thân, Opus 5 vá, S5L lời hứa) — tự dừng sau LOCK
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug epNN-<slug> --den B3G
:: C. SOÁT CHATGPT WEB
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug epNN-<slug> --lan1
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug epNN-<slug> --chot
::    viec_tay.txt (thay thế NGUYÊN VĂN, độ dài dự kiến < trần) → ghi_lock ESCALATE → chạy lại B
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path('assets/N-senior_korekara/epNN-<slug>'),'ESCALATE',reason='soat ChatGPT web')"
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug epNN-<slug> --den B3G
::    lớp 3 đọc bản khoá (§2b) → soat_kb_gptweb.py --xong
py -3.13 -X utf8 pipeline\soat_kb_gptweb.py --profile senior_korekara --slug epNN-<slug> --xong
:: D. CAST + GIỌNG: characters.json (nhân vật tập + vai phụ, voice_id từ cast_bank, id "ke" nếu tập kể ngôi 1) → gắn vai từng câu
py -3.13 -X utf8 pipeline\gan_vai.py --profile senior_korekara --slug assets\N-senior_korekara\epNN-<slug>
:: E. PROMPT ẢNH (--only, KHÔNG --from: máy 1 cấm B4/B5)
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug epNN-<slug> --only B5P
::    (21/10) Hook = bám sát cấu trúc hook video gốc — E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md; series_ctx ghi CẢNH XUNG ĐỘT (thân bài), KHÔNG còn "CẢNH XUNG ĐỘT CHO HOOK"
:: F. HOOK (máy 1 làm trọn hình): storyboard → ảnh hook → clip Grok 6s → SFX → HOOK_TAP.md
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile senior_korekara --slug epNN-<slug>
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\epNN-<slug> --profile senior_korekara
:: G. GIAO MÁY 2 (tự ghi D = Đã giao máy 2 + K = lệnh máy 2, H = cần ảnh)
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job senior_korekara epNN-<slug>
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list senior_korekara
```
Chi tiết hook/Grok/master vai phụ: làm y `SOP_LANE_M.md` §2 mục F (Grok clip **6 giây**, 10 giây ăn 429).

### 2b. Lớp 3 — Claude Code đọc bản khoá, kiểm riêng lane
- Nghề nhân vật chính KHÁC nghề cấm; không sót dụng cụ/câu thoại/số năm của nghề cũ; tên nhân vật/địa điểm không trùng video gốc.
- ⭐ HOOK (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ (narrative intro 16/10, thoại xung đột/cảnh nhục 30/09) đã xoá — lớp 3 không chấm hook theo luật cũ.
- Chặng 1 sau hook: cầu nối + chi tiết MỚI, KHÔNG kể lại nguyên phần giới thiệu của hook (tuổi/nghề/con số đã nói ở hook thì không lặp nguyên câu).
- Có người đối chứng (tên + tuổi + số) và ≥1 người đối xử tệ có lý do tin được.
- Mỗi câu thoại là 1 câu「」riêng; lời dẫn không dính thoại.
- Số chế độ khớp [Dn] đúng điều kiện; số cá nhân cộng khớp mọi mốc.
- Kết nghiệm tùng + câu hỏi cho khán giả + đủ cảm ơn/高評価/チャンネル登録. Không quả báo, không trúng số, không con cái cứu.

## 3. GATE — ngưỡng đã ĐO (chi tiết trong `profile.script.gate._gate_note` + `goi_dang._nguon`)
| Chỉ số | Giá trị | Nguồn đo (15 transcript `_raw` + 64 tiêu đề) |
|---|---|---|
| target_minutes | 16 | 64 video 11,9–25,3' (trung vị 16,4); top 10 trung vị ~15,8 |
| list_item_count | 0 | lane truyện |
| câu (comma / breath) | 0,6–2 / 6–12 | câu trung bình 13,8–16,9 chữ; ASR không ghi 、 → SUY như Lane F/J, đo lại sau ep01 |
| dialogue_ratio_max · dialogue_own_sentence | 0,30 · true | câu đuôi hội thoại 5–18% (proxy); giọng nữ 10–25% thời lượng; đa giọng |
| title_len | 38–56 | 64 tiêu đề p25 37 · trung vị 41 · p75 47; nhóm VPD cao 68,8% dài >40 |
| hook_chars (120 giây đầu) | 500–720 | 509–716 chữ |
| goi_dang contradiction / title_core / promise | 60s / 60s / 60s | câu mâu thuẫn đầu tiên trung vị ~59s |
| goi_dang title_core_len | 30–46 | tiêu đề bỏ【漫画】 p25 33 – p75 43 |
| seconds_per_image | 7,5 | ĐO 30/09: G5kIPGFNKeY 154 ảnh/19,0' (TB 7,39 s, trung vị 7,0) · oZatkpZ0HEc 152 ảnh/20,2' (TB 7,98, trung vị 7,9) |
| transition | cut (cắt thẳng) | 2 video: 100% cắt thẳng, 0 hiệu ứng chuyển cảnh, 0 khung đen. Kênh mẫu có zoom chậm ~27% cảnh — Lane N KHÔNG làm (luật cấm zoom >1.0) |

## 3b. VIỆC CÒN TREO TRƯỚC KHI GIAO MÁY 2 TẬP 1 (không chặn viết kịch bản)
- ✅ **Chữ trên hình (anh chốt 2026-09-30)**: chữ DỌC như Lane M, mặc định GÓC PHẢI; lời kể = ô vuông; lời thoại = ô ELIP có ĐUÔI chỉ
  về người nói; chữ ĐẬM hơn Lane M (Yu Gothic Bold + viền chữ 1px). Cỡ chữ TẠM = Lane M (kể 72 / thoại 56), anh chốt sau khi xem ep01.
  Code: `pipeline\bong_thoai.py` thêm `shape_thoai:"elip"` + `stroke_chu`; `pipeline\tate_text.py` thêm font `yu gothic bold` (opt-in, lane
  khác không đổi). Ảnh mẫu: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\_chu_mau\`. ⚠️ Máy 2 phải có code mới (anh push git +
  `dong_goi_may2.py --bundle --profile-list senior_korekara`) — thiếu thì bóng ra kiểu cũ, KHÔNG báo lỗi.
- ✅ **Nhịp ảnh + chuyển cảnh (đo 2026-09-30, skill `video-chuyen-canh`)**: `image.seconds_per_image=7.5`, `assemble.transition="cut"`,
  `zoom=1.0`. Cách đo: `do_chuyen_canh.py` dò ranh giới → tách "đổi ẢNH" (>35% điểm ảnh đổi) khỏi "chỉ đổi CHỮ" (hộp/bóng thoại mới trên
  cùng ảnh — 8–20% số ranh giới tool dò là đổi chữ, không phải đổi ảnh). Dữ liệu + ảnh kiểm:
  `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_korekara\nhip\` (do_*.json, kiem_ranh_gioi.jpg, kiem_kb.jpg).
  Ghi nhận thêm từ khung thật: mỗi ảnh hiện NHIỀU hộp/bóng nối tiếp (chữ đổi theo câu, ảnh đứng yên) — khớp cách `bong_thoai` dựng.
- **Thumbnail**: chưa đo — TITLE-RESEARCH làm.

## 4. SOÁT CHATGPT WEB — ĐÃ DỰNG 2026-09-30 (acc1 g-p-6abc72e6…, acc2 g-p-6abc71e1…, cả 2 giao vai trả "Hiểu.")
2 Project tên `N-senior_korekara` (Instructions + 4 file `E:\CLAUDE\YOUTUBE\h2dev\CHATGPT_PROJECTS\N-senior_korekara-script\`), tạo bằng
`py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chatgpt_web\tao_project_soat.py --profile senior_korekara --dir CHATGPT_PROJECTS\N-senior_korekara-script --ghi`
— link ghi ở `profile.script.soat_gptweb.urls`. Sửa file trong thư mục đó rồi chạy lại lệnh = cập nhật, không tạo trùng.

## 5. LUẬT CỨNG LANE N
1. Mỗi tập MỘT nhân vật mới 60–75, vấn đề ở HIỆN TẠI của đời sống sau nghỉ việc.
2. ĐỔI NGHỀ so video gốc — không ngoại lệ.
3. Tiêu đề nêu TÌNH HUỐNG KẸT cụ thể + câu hỏi treo; cấm chỉ 「末路」 chung chung, cấm khoe kết quả đã đạt.
4. Số chế độ có nguồn; chi phí đời sống thật và cụ thể (khán giả tự bổ sung kinh nghiệm, bắt lỗi nhanh).
5. Kết NGHIỆM TÙNG ấm, có ≥1 người đối xử tệ; không quả báo, không phép màu, không nội dung chính trị/trợ cấp gây tranh cãi.
6. Hình: anime bán thực, nền đẹp chi tiết, người ĐÚNG tuổi nhưng khoẻ/gọn — không vẽ già hơn tuổi.
7. Không chép tên nhân vật, địa điểm, câu đặc trưng hay tiêu đề nguyên văn của kênh mẫu.
- ⚠️ 01/10 ep01 shizue: ref vẽ như ảnh thật/trẻ 35 do khung prompt §17 'Photorealistic' + 'youthful'. Đã vẽ lại manga (anime3). Ref 60+ tuổi: dùng STYLE manga ĐẦU prompt, tả tuổi bằng nét vẽ. Chi tiết: docs/QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md §17.
