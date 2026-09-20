# KIẾN TRÚC ĐA NHÂN VẬT / ĐA KÊNH CHO TOOL (profile-driven)

Ngày đo **2026-09-07**. Vấn đề: pipeline hiện tại đóng đinh vào **1 nhân vật duy nhất** (cụ bà Nhật, giọng
`ado`, speed 0.92, nhịp chậm). Tool phải chạy được cho **mọi nhân vật**: trai trẻ mạnh mẽ ăn to nói lớn,
nam trung niên trầm hùng, nữ sắc sảo, thiếu niên... ở mọi thị trường.

## 1. BẰNG CHỨNG SỐ: "309 CHỮ/PHÚT" KHÔNG PHẢI HẰNG SỐ

Cùng 1 đoạn 256 chữ Nhật, đổi giọng/tốc độ → đo thời lượng thật (`assets/_voice_test/*.mp3`):

| Cấu hình | speed | fx | Thời lượng | **Char-rate** | Script 30 phút cần |
|---|---|---|---|---|---|
| Ado + age=med (**đang dùng**) | 0.92 | med | 48,4s | **317,5 chữ/ph** | 9.524 chữ |
| Ado, không làm già | 0.92 | none | 49,9s | 307,7 | 9.230 |
| **Ryu-Characters (samurai hùng)** | 1.00 | none | 47,6s | 322,6 | 9.676 |
| **Ryo-maru (trai trẻ nói nhanh)** | 1.10 | none | 35,9s | **427,6** | **12.828** |
| Dominant Man (minimax) | 1.00 | none | 46,2s | 332,6 | 9.978 |

**Chênh 307 → 428 chữ/phút = 39%.** Nếu tool cứ dùng 309 cho kênh giọng trẻ, kịch bản "30 phút" thực tế
chỉ ra **~22 phút** — hụt 8 phút, mất tiền quảng cáo. ⇒ char-rate **phải thuộc profile**, và phải **đo tự động**
khi lập kênh mới (1 call TTS 250 chữ ≈ 15 giây ≈ 300 credit).

Ghi chú: `age=med` làm giọng NHANH hơn 3% (317,5 vs 307,7) vì thủ thuật `asetrate×0.94 + atempo×1.0638`.

## 2. KHO GIỌNG: 69 GIỌNG, LỌC ĐƯỢC TỰ ĐỘNG

Hút toàn bộ `GET /v3/voices` (OpenSpeaker): **33 ElevenLabs + 23 MiniMax + 11 Vbee + 2 edge**, mỗi giọng có
`gender` / `age` / `descriptives` / `description` → tool tự lọc theo persona, không cần dò tay.
Dump: `assets/voice_bank.json` (sinh lại bằng `pipeline/voice_bank.py --refresh`).

| Persona | Giọng có thật (đã xác định) |
|---|---|
| Trai mạnh mẽ, ầm vang, dữ dội | `elevenlabs_D3L9PtKnIVJXdgK444Ey` **Ryu-Characters** (samurai, deep powerful dramatic) · `minimax_209533299589246` Dominant Man · `minimax_209536448462912` Serious Commander |
| Trai trẻ nhiệt, nói nhanh | `elevenlabs_FNpElEHmcXikbgLHkDkJ` **Ryo-maru** (cheerful fast-paced high-energy) · `minimax_303592971526209` Kisakuna Takuya · Sporty Student · Optimistic Youth |
| Nam trung niên tin cậy (doc/lịch sử) | `elevenlabs_W8wofKLOWnsM57L8hIx2` Koji-Business · Enishi · Akira · Kai Sundiata (deep) |
| Nữ sắc sảo, gắt gỏng | `minimax_303591230320707` Tsuyoki na Akane (sharp, assertive) |
| Nữ trẻ ngọt / anime | Nao · Yuna · Tsuyuri · Koume |
| Thiếu niên / cậu bé | `minimax_209536448462923` Innocent Boy |
| Cụ bà / cụ ông (hiện dùng) | Ado (nữ) · Enishi/PapaJi (nam) |

## 3. FX GIỌNG: PHẢI CÓ CHIỀU NGƯỢC VỚI "LÀM GIÀ"

`tts.py` hiện chỉ có `AGE_FILTERS` = 4 mức **làm già** (hạ pitch, cắt treble, rung). Đã test 3 preset mới
trên chính file samurai (`assets/_voice_test/fx_*.mp3`), **thời lượng không đổi → SRT vẫn khớp**:

| Preset | Chuỗi ffmpeg | mean dB | max dB | Thời lượng |
|---|---|---|---|---|
| none | — | −18,5 | −0,6 | 47,6s |
| `young` | `asetrate=44100*1.05,aresample,atempo=0.9524` | −18,9 | −1,0 | 47,6s |
| `boom` | `equalizer=f=110:g=+4, acompressor 3:1, aecho 0.18, loudnorm I=-14` | −17,2 | −2,4 | 47,7s |
| `punch` | `acompressor 4:1, equalizer=f=3000:g=+3, loudnorm I=-13` | **−16,7** | −1,4 | 47,6s |

⇒ Đổi `AGE_FILTERS` thành `VOICE_FX` gồm: `none · old-mild · old-med · old-frail · young · boom · punch`.

## 4. CÁI QUYẾT ĐỊNH "CHẤT NHÂN VẬT" TRONG VĂN LÀ 2 CON SỐ

Từ A/B (xem `docs/AB_SCRIPT_MODELS.md` §2): thứ làm giọng nghe **già/chậm/tâm tình** hay
**trẻ/dồn dập/hùng hồn** không phải model, mà là:

| Knob | Cụ bà tâm tình (hiện tại) | Trai trẻ ầm vang (mới) |
|---|---|---|
| Dấu phẩy / câu | **3–5** (băm nhịp thở) | **0,8–1,5** (câu liền hơi, dồn) |
| Chữ / câu | 24–28 | 18–24 (câu ngắn, đánh nhịp) |
| Hội thoại 「」 | 0–10% | 15–30% (kịch tính, đối đáp) |
| Câu cảm thán / hô | không | có (だが！ · そのとき！) |
| Ngôi kể | 私 nữ, けんじょう語 | 俺/私 nam, ですます hoặc だ・である |

Đây là **ngưỡng của gate**, hiện đang là hằng số trong đầu em → phải chuyển vào profile.

## 5. SCHEMA PROFILE (1 nguồn chân lý cho cả 7 bước)

`pipeline/profiles/<id>.json` — mở rộng từ `channels.json` hiện có:

```json
{
  "id": "samurai-history-jp",
  "market": "JP", "language": "ja",
  "niche": "Lịch sử samurai / chiến trận",
  "competitor": "https://www.youtube.com/@...",

  "narrator": {
    "gender": "male", "age_band": "40s", "persona": "võ tướng trầm hùng, ăn to nói lớn",
    "point_of_view": "第三者・語り部", "register": "だ・である体"
  },
  "voice": { "id": "elevenlabs_D3L9PtKnIVJXdgK444Ey", "speed": 1.0, "fx": "boom",
             "char_rate": 322.6, "char_rate_measured_at": "2026-09-07" },

  "script": { "skill": "skills/youtube-script-samurai-jp/SKILL.md",
              "target_minutes": 25,
              "gate": { "comma_per_sentence": [0.8, 1.6], "chars_per_sentence": [18, 26],
                        "dialogue_ratio_max": 0.30, "require_next_ep_teaser": true } },

  "image": { "skill": "skills/youtube-image-samurai-jp/SKILL.md",
             "character_sheet": "a Japanese samurai general in his 40s, weathered face, topknot, dark armor...",
             "style_suffix": "cinematic ultra-realistic color, dramatic side light, 16:9, no text",
             "seconds_per_image": 12, "ref_lock": true, "ref_quality": "medium" },

  "thumbnail": { "skill": "skills/youtube-thumbnail-samurai-jp/SKILL.md",
                 "font": "assets/fonts/NotoSansJP-Black.otf", "palette": ["RED","YELLOW","WHITE"] },

  "assemble": { "zoom": 1.18, "transition": "cut", "xfade": 0.25, "bgm": "assets/bgm/war_drums.mp3",
                "bgm_volume": 0.12 },

  "blocklist": ["gore", "severed", "blood spray", "child soldier"]
}
```

Mỗi field chảy vào đúng 1 bước — không chỗ nào còn hằng số ẩn:

| Field | Dùng ở bước |
|---|---|
| `narrator.*` + `script.gate` | B3 viết script (system prompt + gate kiểm) |
| `voice.*` | B4 TTS (+ `char_rate` để tính số chữ mục tiêu ở B3) |
| `image.*` | B5 prompt ảnh + gen (CHARACTER SHEET, style, mật độ ảnh, REF-LOCK) |
| `thumbnail.*` | B7 chữ + font |
| `assemble.*` | B8 nhịp dựng (kênh hùng: cắt cứng nhanh; kênh tâm tình: crossfade mềm) |
| `blocklist` | prefilter content-policy trước khi gen ảnh |

## 6. WIZARD "LẬP KÊNH MỚI" (nút trong exe)

1. Nhập: thị trường/ngôn ngữ · ngách · link kênh đối thủ · mô tả nhân vật bằng tiếng Việt
   ("trai 30 tuổi mạnh mẽ ăn to nói lớn").
2. Tool lọc `voice_bank.json` theo gender/age/descriptives → **hiện 5 giọng gợi ý + nút Nghe thử**
   (đọc sẵn 1 câu mẫu, ~5s/giọng).
3. Anh chọn giọng + fx (`none/young/boom/punch`) + speed → tool **tự đo char-rate** (250 chữ, ~15s)
   và ghi vào profile.
4. LLM sinh sẵn: `narrator` block, `script.gate` (ngưỡng nhịp theo persona), `image.character_sheet`,
   `blocklist` → anh sửa nếu muốn.
5. Ghi `pipeline/profiles/<id>.json`. Từ đó mọi video của kênh chỉ cần `--profile <id>`.

Skill script/ảnh/thumb cho **ngách mới** vẫn phải viết 1 lần (copy skill Satori rồi đổi genre) — tool tạo
sẵn bộ khung + để LLM điền, nhưng đây là chỗ duy nhất còn cần người xem lại.

## 7. VIỆC PHẢI SỬA (checklist)

- [ ] `pipeline/voice_bank.py` — hút `/v3/voices` → `assets/voice_bank.json`, hàm `suggest(gender, age, tags)`.
- [ ] `pipeline/tts.py` — `AGE_FILTERS` → `VOICE_FX` (+`young/boom/punch`); `--fx` thay `--age` (giữ alias cũ);
      `--profile` đọc profile JSON; bỏ `_OS_VOICES` cứng, tra voice_bank.
- [ ] `pipeline/calibrate.py` — đo char-rate 1 giọng → ghi vào profile.
- [ ] `pipeline/ai_steps.py` — mọi prompt nạp `narrator/script.gate/image` từ profile; gate dùng **ngưỡng
      của profile**, không phải hằng số.
- [ ] `skills/*` — bỏ CHARACTER SHEET "elderly Japanese man" khỏi skill, chuyển thành biến `{{character_sheet}}`.
- [ ] `pipeline/make_video.py` + GUI — nhận `--profile`, dropdown chọn kênh, nút "Lập kênh mới".
- [ ] Chuyển `channels.json` → `profiles/satori-jp-obaa.json` (giữ tương thích: đọc được cả 2).

## 8. GHI CHÚ THẬT

- Char-rate của **cùng 1 giọng** còn lệch theo mật độ kanji (kanji đọc lâu hơn kana) — sai số ~±3%. Đo bằng
  chính đoạn văn của ngách đó thì sát hơn; sai 3% trên 30 phút = 54 giây, chấp nhận được.
- `voice.fx` giữ nguyên thời lượng (đã verify 47,6s → 47,6/47,7s) nên **SRT của OpenSpeaker vẫn khớp** — đừng
  đổi sang filter làm thay đổi tempo mà không đo lại.
- Đừng cho 1 kênh 2 giọng khác nhau giữa các tập: khán giả nhận ra ngay. `profile` = 1 nhân vật = 1 kênh.
