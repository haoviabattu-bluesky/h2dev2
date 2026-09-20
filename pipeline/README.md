# PIPELINE SẢN XUẤT VIDEO — NHẬT/HÀN (view ngoại, RPM cao, ít cạnh tranh)

**Hướng ACTIVE (2026-09-07): thị trường NHẬT trước** — ngách **Satori (悟り系) câu chuyện người già**
(RPM 8, view+RPM cao, khán giả già xem lâu — M4-82/84). Ngôn ngữ script/giọng đọc = **tiếng Nhật**. Sau khi
ra kết quả → nhân bản sang **Hàn Quốc** (đổi ngôn ngữ + sắc tộc nhân vật). Công thức 70/30 (xào kịch bản đối thủ).

> WW2 (English) đã dựng trước đó → **gác lại làm TEMPLATE** (`skills/*-ww2-*`). Tool pipeline dùng chung.

## KIẾN TRÚC (3 skill sáng tạo + tool nối hạ tầng — ĐÃ VERIFY END-TO-END)

```
[1] Bóc kịch bản đối thủ (JP)  → pipeline/fetch_script.py --lang ja   (youtube-transcript-api)
[2] Viết script Satori (JP, 70/30, VO-ready) → skill: script-satori-jp   (Claude, 6 phase)
[3] Prompt ảnh + thumbnail (JP)→ skill: image-satori-jp / thumbnail-satori-jp
[4] Gen ảnh cinematic MÀU      → pipeline/gen_images.py   (gpti2, 2560x1440, ~50đ/ảnh low)
[5] Giọng đọc Nhật + PHỤ ĐỀ .srt → pipeline/tts.py  (ai33/OpenSpeaker Enishi=CHÍNH chất ElevenLabs · edge=free fallback)  ✅
[6] Ghép video + audio + BURN phụ đề + NHẠC NỀN → pipeline/assemble.py (Ken Burns, --srt, --bgm)
[7] Thumbnail chữ Nhật (kiểu bản gốc) → pipeline/thumbnail_text.py (PIL, chữ to + banner đỏ)
[+] BGM Suno → openspeaker_tts.generate_music() (POST /v1s/task/music-generation)
```

Skills ở `../skills/` — gọi trong Claude Code: `/script-satori-jp`, `/image-satori-jp`, `/thumbnail-satori-jp`
(hoặc copy sang `C:\Users\admin\.claude\skills\` để dùng toàn cục).

## QUY TRÌNH 1 VIDEO
```bash
cd e:/CLAUDE/YOUTUBE/h2dev/pipeline
SLUG=chichi-no-tegami            # đặt tên video

# 1) Bóc kịch bản 1-2 video đối thủ Nhật cao view + gần đây (≤1 tháng)
py -3.13 fetch_script.py "<URL video đối thủ Nhật>" --lang ja --out ../assets/satori_jp/$SLUG/competitor.txt

# 2) Viết script: gọi skill /script-satori-jp, dán competitor.txt (Phase 1 nhân bản 70/30)
#    → lưu bản voiceover-ready (tiếng Nhật, clean) vào ../assets/satori_jp/$SLUG/script.txt

# 3) Prompt ảnh: /image-satori-jp (dán script + CHARACTER SHEET nhân vật) → img_prompts.txt
#    Thumbnail: /thumbnail-satori-jp → thumb_prompt.txt

# 4) Gen ảnh (song song, resume):
py -3.13 gen_images.py --prompts ../assets/satori_jp/$SLUG/img_prompts.txt --out ../assets/satori_jp/$SLUG/img --quality low
py -3.13 gen_images.py --prompts ../assets/satori_jp/$SLUG/thumb_prompt.txt --out ../assets/satori_jp/$SLUG/thumb --quality medium --limit 1

# 5) Giọng đọc Nhật + PHỤ ĐỀ .srt tự sync (edge-tts, free):
py -3.13 tts.py --script ../assets/satori_jp/$SLUG/script.txt --provider openspeaker --voice enishi --speed 0.95 --out ../assets/satori_jp/$SLUG/voice.mp3
#    → giọng ai33/OpenSpeaker Enishi (chất ElevenLabs) + voice.srt (server sync). Fallback free: --provider edge

# 5b) Nhạc nền BGM (Suno qua ai33) — gen 1 track instrumental rồi tái dùng:
py -3.13 -c "import openspeaker_tts as o;open('../assets/satori_jp/_bgm/bgm1.mp3','wb').write(o.generate_music('gentle emotional piano, calm nostalgic, instrumental', instrumental=True))"

# 6) Ghép + BURN phụ đề (font Meiryo):
py -3.13 assemble.py --img ../assets/satori_jp/$SLUG/img --audio ../assets/satori_jp/$SLUG/voice.mp3 --srt ../assets/satori_jp/$SLUG/voice.srt --bgm ../assets/satori_jp/_bgm/bgm1.mp3 --bgm-volume 0.09 --out ../assets/satori_jp/$SLUG/final.mp4
```

## GHI CHÚ HẠ TẦNG (đã verify thật 2026-09-07)
- **gpti2** (`gpti2_gen.py`): 3 key VND (~130k mỗi ≈ 8000 ảnh low), async jobs + poll. Ảnh **cinematic màu**
  người già Nhật (和室/縁側/ánh sáng ấm) ra rất tốt ở `low`. quality: low=nền (rẻ), medium=thumbnail.
- **edge-tts** (`tts.py`): giọng **ja-JP-KeitaNeural** (nam trầm ấm, kể chuyện) / **NanamiNeural** (nữ). Free,
  không cần key. `--rate=-8%` đọc chậm hợp khán giả già. Bản Hàn: `--voice ko-KR-InJoonNeural`.
- **Số lượng ảnh:** ~6–10s/ảnh → video 30' ≈ 180–300 ảnh. Chia phần script để gen từng đợt.
- **CHARACTER SHEET:** khi gọi image-satori-jp phải cấp mô tả cố định nhân vật chính → giữ khuôn mặt nhất
  quán qua các ảnh (gpti2 không có seed, khoá bằng mô tả lặp).
- **assemble.py**: bản nháp Ken Burns. Edit cuối qua **CapCut** (phụ đề tiếng Nhật + BGM + hiệu ứng) — tăng
  chất + chống "trùng nội dung".
- **Chính sách:** script 70/30 (giữ 70% khung + 30% sáng tạo, đổi tên/địa danh/mùa); ảnh/giọng/edit khác đối
  thủ → an toàn reused content. Giữ **nhân phẩm** người già (không bi thảm hoá quá).

## NHÂN BẢN SANG HÀN QUỐC (sau khi Nhật ra kết quả)
Copy 3 skill `*-satori-jp` → `*-satori-kr`: đổi ngôn ngữ output sang **tiếng Hàn**, sắc tộc nhân vật →
**elderly Korean** + bối cảnh Hàn (한옥/아파트), thumbnail chữ Hàn. Tool giữ nguyên: `fetch_script.py --lang ko`,
`tts.py --voice ko-KR-InJoonNeural`.

## CÒN THIẾU / TODO
- [x] **DEMO end-to-end + PHỤ ĐỀ ĐÃ CHẠY (2026-09-07):** video `assets/satori_jp/saigo-no-bento/`「最後の弁当」
      — script tự sinh ~2400 chữ Nhật → **30 ảnh** cinematic + thumbnail + giọng Keita **7:18** + **phụ đề Nhật
      130 cue tự sync (burn font Meiryo)** → `final.mp4` (7:18, 1080p, 111MB). Chi phí ảnh ≈ **~1.5k VND**, TTS+
      phụ đề+ghép = 0đ. Nhân vật nhất quán 30 ảnh. Phụ đề sync theo SentenceBoundary edge-tts.
- [ ] Chạy 1 video THẬT từ **URL đối thủ** (nhân bản 70/30) + độ dài chuẩn 20-40' (demo mới ~7').
- [ ] Lấy list **kênh đối thủ Satori Nhật** (đổi location YouTube → Nhật → đề xuất) làm nguồn key.
- [ ] Setup kênh YouTube Nhật theo M1-03 (mail cổ, ngâm kênh, SEO tiếng Nhật) trước khi đăng số lượng.
- [ ] (Sau) nhân bản sang Hàn Quốc.
- WW2 English: template ở `skills/*-ww2-*` + prompt gốc — kích hoạt lại nếu muốn thêm thị trường Âu Mỹ.


## KHOÁ NHẤT QUÁN NHÂN VẬT (REF-LOCK) — thêm 2026-09-07, đã verify
`gpti2_edit.py` + cờ `--ref` của `gen_images.py`: gửi kèm ẢNH MASTER của nhân vật làm ảnh nguồn
(`/v1/images/jobs/edits`) nên giữ được đúng KHUÔN MẶT, thứ mà lặp CHARACTER SHEET bằng chữ KHÔNG làm được
(gpti2 không có seed).

```
# 1. master portrait (1 lần / nhân vật)
py -3.13 pipeline/gen_images.py --prompts master.txt --out <slug>/master --quality medium
# 2. các cảnh, khoá theo master
py -3.13 pipeline/gen_images.py --prompts scenes.txt --out <slug>/img     --ref <slug>/master/001.png --orient landscape --quality low
```
- Tối đa **8** `--ref` (ảnh ĐẦU ưu tiên giữ) → dùng khi nhiều nhân vật cùng khung.
- Dùng `--quality low`: đo thật 2026-09-07 low giữ mặt NGANG medium (`assets/_char_test/COMPARE_FACE_LOW_MED.png`). Chỉ ảnh MASTER mới nên medium. Tránh `high` (vẽ lại → mờ + sai chi tiết).
- Giá thật (`GET /v1/pricing`, 2560x1440): low 50 · medium 350 · high 1.400, **+60đ mỗi ảnh nguồn**.
  → REF-LOCK low = **110đ/ảnh** vs text-only 50đ/ảnh.
- Prompt cảnh phải có `Place him in a completely NEW scene` — thiếu là model chỉ chỉnh nhẹ ảnh master.
- Bằng chứng: `assets/_char_test/COMPARE.png` (hàng 2 text-only = 4 người khác nhau; hàng 3 ref-lock = 1 người).
