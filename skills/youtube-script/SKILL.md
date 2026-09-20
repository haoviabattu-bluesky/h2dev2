---
name: youtube-script
description: Viết KỊCH BẢN VOICEOVER-READY cho video YouTube faceless kể chuyện/tư liệu — TỔNG QUÁT cho MỌI ngách, thị trường, ngôn ngữ (niche/market/language là THAM SỐ, không khoá cứng). Nhân bản 70/30 từ kịch bản đối thủ HOẶC viết mới từ chủ đề. Output pure prose sạch (KHÔNG bracket/marker/heading/「パート」) dán thẳng TTS. Trigger: "viết script/kịch bản YouTube", "script <ngách>" (satori/người già/WW2/lịch sử/tiền/kinh tế/quan hệ...), "nhân bản video <url> sang <thị trường>", "Japanese/Korean/English script", "câu chuyện cảm động", "documentary script". Input: niche + market + language + length + narrator (+ transcript đối thủ nếu clone). Áp dụng cho mọi dự án YouTube.
---

> **NGÁCH CHỐT CHO PROFILE NÀY:** niche=satori-elderly · market=JP · language=tiếng Nhật · narrator=cụ bà 70-80 ngôi 1, です・ます+ございます. Mọi tham số còn lại lấy từ  (char_rate, gate nhịp, character_sheet, style_suffix).

# YouTube Script Writer (tổng quát — mọi ngách/thị trường/ngôn ngữ)

Skill viết kịch bản **voiceover-ready** cho kênh faceless. KHÔNG khoá 1 ngách: ngách + thị trường + ngôn ngữ
là THAM SỐ. Dùng chung cho mọi dự án YouTube (Satori người già, WW2 lịch sử, tiền/hưu trí, quan hệ, kể chuyện...).

## INPUT (hỏi/nhận trước khi viết)
```
NICHE:    [satori-elderly | ww2-history | money-retirement | relationships | <ngách khác>]
MARKET:   [JP | KR | EN(US/UK/CA/AU) | ...]   LANGUAGE: [tiếng Nhật | tiếng Hàn | English | ...]
LENGTH:   [20/25/30/40 phút]   NARRATOR: [ngôi 1 / ngôi 3; TÊN + tuổi + giới]
SOURCE:   [dán transcript đối thủ (clone 70/30) | chủ đề | "tự tìm"]
```

## QUY TẮC SỐNG CÒN
1. **VOICEOVER-READY:** bản cuối là prose 100% ngôn ngữ đích, KHÔNG 「パート」/marker/heading/chú thích/ngoặc.
   Dán thẳng TTS được ngay.
2. **70/30 khi clone:** giữ ~70% cấu trúc/bài học đối thủ + 30% mới (đổi góc kể, tình tiết, tên, bối cảnh).
   **Bản địa hoá 100%** theo market (đồ vật, phong tục, luật, tiền tệ) — KHÔNG để lộ dấu vết nguồn.
3. ⚠️ **ĐỘ DÀI — dùng CHAR-RATE ĐO THẬT, đừng ước lượng mò.** Giọng ai33/openspeaker (vd ado JP + age med) ≈
   **~309 ký tự không-space (cả CJK)/phút** → 30' ≈ 9.000-9.500 ký tự. **BẮT BUỘC đếm ký tự trước khi TTS**
   (`len` bỏ \n/space) rồi chia char-rate. (Bài học thật: viết 13.700 chữ = 44' phải viết lại.) Giọng/ngôn ngữ
   khác → đo lại char-rate 1 lần, ghi cạnh entry channels.json. (Talking-head/EN tính theo wpm 130-150; visual-heavy 70-90.)
4. ⚠️ **GIỚI GIỌNG PHẢI KHỚP NGƯỜI KỂ** (bà cụ→nữ, ông cụ→nam). Bug đã dính nhiều lần: người kể nữ gán giọng nam.
5. **Nhất quán nhân vật:** đặt TÊN + tuổi rõ cho người kể + nhân vật chính (để [[youtube-image-prompts]] dựng
   character bible + REF-LOCK). Toán tuổi hợp lý (con = cha mẹ − 25..35).

## 6 PHASE
1. **Topic Lock** — chốt chủ đề + hook + bài học/悟り/twist.
2. **Research/Analyze** — nếu clone: phân tích cốt truyện/nhân vật/bài học đối thủ. Nếu lịch sử: research bank (độ chính xác).
3. **Outline** — cold open điện ảnh (thời gian+nơi+cử chỉ) → gieo伏線 → cao trào → bài học 1 câu → 3 kết + comment-bait.
4. **Draft** theo từng phần.
5. **Humanization** — nhịp tự nhiên, "you"/gần gũi, xoá giọng AI.
6. **Final Clean** — bỏ mọi marker → prose thuần ngôn ngữ đích. Đếm ký tự → xác nhận khớp LENGTH.

## HỒ SƠ NICHE (chọn theo NICHE, mở rộng khi có ngách mới)
- **satori-elderly** (悟り系, người già JP/KR): ngôi 1 người già tự kể chuyện đời, bọc 1 bài học sống; ấm áp,
  giữ nhân phẩm; RPM cao, khán giả già xem lâu → nên DÀI. JP hoá: 縁側/仏壇/四十九日/年金/相続/終活; luật chính xác.
- **ww2-history** (EN documentary): 4 title archetype, cinematic cold open 20s, 1 human anchor, chính xác lịch
  sử tuyệt đối, "you" language, show-don't-tell. Giọng nam trầm tư liệu.
- **money/retirement, relationships...**: hook "điều người ta né nói", chuyên gia/nhân vật kể, bài học tài chính/tình cảm rõ.

## SAU KỊCH BẢN
→ [[youtube-image-prompts]] (prompt ảnh + character consistency) · [[youtube-thumbnail]] · [[youtube-series-builder]]
(nếu dựng cả kênh). Tool: `pipeline/tts.py --channel <id>` (ai33/openspeaker; edge-tts fallback). Bộ pipeline
YouTube ở `pipeline/` của dự án (impl tham chiếu: e:\CLAUDE\YOUTUBE\h2dev\pipeline). Runbook: docs/SOP_SATORI_JP.md.
