---
title: Kênh hoạt hình Nhật — video ghép từ clip Veo 3.1 (mảng 2 của h2dev)
date: 2026-09-07
status: draft
type: brainstorm
next: /ck:plan
---

# Brainstorm — Mảng VEO ANIME JP

> Nguồn tham chiếu kỹ thuật: repo `github.com/crisng95/flowkit` (MIT, commit cuối 2026-08-18).
> Đã clone + đọc toàn bộ 2026-09-07: 12.935 dòng Python, 1.395 dòng JS extension, 35 skill `.md`.

---

## 1. Problem Statement

h2dev hiện chỉ có 1 mảng sản xuất: **ảnh tĩnh + Ken Burns** (ngách Satori JP, video 25-30 phút).
Mảng này chạy tốt nhưng bị giới hạn về định dạng nội dung — không làm được kênh có **nhân vật chuyển
động, diễn xuất, đồng nhất qua nhiều cảnh**, tức là không vào được ngách hoạt hình kể chuyện.
Cần mở mảng thứ 2: **ghép nhiều clip 8s sinh bằng Veo 3.1 thành video hoàn chỉnh**, với nhân vật giữ
nguyên diện mạo xuyên suốt. Mảng này dùng chung hạ tầng script/TTS/thumbnail JP đã có.

---

## 2. Requirements (Approved)

### Functional
- Sinh clip video 8s từ ảnh scene (i2v) và từ cặp ảnh đầu-cuối (i2v_fl) qua Google Flow / Veo 3.1
- Giữ **nhân vật đồng nhất** qua toàn bộ scene bằng hệ thống reference image có UUID
- Ghép clip thành video hoàn chỉnh, mối nối liền mạch (chain) hoặc cắt cứng (hard cut) tuỳ ngữ cảnh
- Sinh **song song 2 khung hình**: ngang (video dài) + dọc (Shorts) — T4 Parallel Orientation
- Nối vào TTS Nhật hiện có (OpenSpeaker Enishi) + phụ đề `.srt` + thumbnail JP
- QC tự động từng clip, phát hiện clip hỏng/lệch nhân vật trước khi ghép
- Resume được: chạy lại không sinh lại clip đã xong

### Non-Functional
- **Chi phí clip = 0đ** (model low-priority 0 credit); chi phí/video chỉ còn TTS
- Chạy trên **Windows 11 native** (không bắt buộc WSL) — khác repo gốc
- Chịu được đứt mạng / extension rớt giữa chừng, không mất tiến độ
- Không bị Google flag `UNUSUAL_ACTIVITY`

---

## 3. Tech Stack (Approved)

| Lớp | Chọn | Ghi chú |
|---|---|---|
| Cầu nối trình duyệt | **Chrome Extension MV3** (port từ flowkit) | bắt token, giải captcha, proxy API |
| Giao tiếp | WebSocket `127.0.0.1:9222` | agent là WS **server**, extension là client |
| Backend | **Python 3.13** + `websockets` + `aiosqlite` | khớp Python hiện dùng của h2dev |
| State | **SQLite** | vòng đời `media_id` phức tạp, JSON phẳng không đủ |
| Sinh ảnh | Google Flow `GEM_PIX_2` (Nano Banana Pro) | ảnh ref + ảnh scene, cùng hệ với video |
| Ghép video | **ffmpeg** (đã có) | tái dùng `assemble.py` |
| TTS | **OpenSpeaker Enishi** (đã có) | `pipeline/tts.py`, không đổi |
| QC | **contact sheet + `claude -p`** | 0đ, thay Gemini API |

### Tài khoản & môi trường (đã xác minh 2026-09-07)

| Hạng mục | Giá trị |
|---|---|
| Tài khoản Google | `dinhson30121963@gmail.com` — Sơn Đinh |
| Gói | **Google AI Pro** (nhãn profile "GEMINI PRO") — **KHÔNG phải Ultra** |
| Tín dụng Flow | **1.050 credit** |
| Chrome profile | **`Profile 53`** trong `C:\Users\admin\AppData\Local\Google\Chrome\User Data` (~502 MB) |
| Repo tham chiếu | `E:\CLAUDE\YOUTUBE\REPO-FLOWKIT` (296 file, git remote còn → `git pull` cập nhật được) |

Lệnh mở đúng profile để chạy extension:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 53" --new-window https://labs.google/fx/tools/flow
```

> ⚠️ Gói **Pro** ⇒ service tier nhiều khả năng là `SERVICE_TIER_ADVANCED`, KHÔNG phải `SERVICE_TIER_ULTRA`.
> Đây chính là tier mà họ `*_ultra_relaxed` **trả `operations[]` rỗng im lặng** (xem R6) → bắt buộc dùng
> `veo_3_1_i2v_lite_low_priority` (D3). 1.050 credit là **ngân sách dự phòng** (~100-210 clip ở model
> trả phí 5-10 credit), không phải nguồn chính — nguồn chính là model 0 credit.

---

## 4. Evaluated Approaches

| # | Approach | Pros | Cons | Decision |
|---|---|---|---|---|
| A | **Cài FlowKit gốc, chỉ bọc thêm lớp tích hợp** | Ra kết quả nhanh nhất; có sẵn dashboard, 35 skill, YouTube SEO | Repo khuyến nghị WSL, skill toàn bash/curl → vướng Windows; kéo theo SQLite schema + FastAPI + React không dùng đến; `youtube/` bị gitignore nên vẫn phải tự viết; phụ thuộc upstream | ❌ Rejected |
| B | **Port lõi sang `pipeline/` của h2dev** | Hợp kiến trúc script phẳng hiện có; chạy Windows native; chỉ mang thứ cần dùng; tự chủ khi Flow đổi API | Tốn thời gian dựng ban đầu; phải tự đọc hiểu payload 6 endpoint | ✅ **Selected** |
| C | **Bỏ Google Flow, dùng provider video trả tiền khác** | Không cần extension/captcha/tài khoản Google | Mất hẳn 0-credit; mất `i2v_fl` (start+end frame) → **không chain liền mạch được**, đây là cơ chế lõi; chi phí/video 10' rất lớn | ❌ Rejected |
| D | **Vẽ hoạt hình bằng ảnh tĩnh + morph/Ken Burns như mảng Satori** | Rẻ nhất, hạ tầng có sẵn 100% | Không phải hoạt hình thật — nhân vật không diễn xuất; không giải quyết được bài toán đặt ra | ❌ Rejected |

**Lý do chọn B:** phần khó nhất của FlowKit là **extension MV3** (self-contained, ~1.400 dòng, đã verify
thật) và **bảng endpoint + cách dựng payload** — cả hai đều port được nguyên vẹn. Phần còn lại (FastAPI,
SQLite schema đầy đủ, dashboard React, 35 skill) là chi phí không cần trả.

---

## 5. Final Architecture

```
                 ┌───────────────────────────────┐
   Chrome        │  Extension MV3 (port flowkit)  │
   đã login  ───►│  · bắt Bearer ya29 (webRequest)│
   labs.google   │  · grecaptcha.enterprise       │
                 │    .execute() ← token 0đ       │
                 │  · fetch từ context trang      │
                 └──────────────┬────────────────┘
                                │ WebSocket :9222
                 ┌──────────────▼────────────────┐
                 │  pipeline/veo/ (Python)        │
                 │  flow_client · queue · store   │
                 │  chain · qc                    │
                 └──────────────┬────────────────┘
                                │
        ┌───────────────────────┼────────────────────────┐
        ▼                       ▼                        ▼
   ảnh ref (UUID)         clip 8s (i2v/i2v_fl)      QC contact sheet
        │                       │                        │
        └───────────────────────┴────────────────────────┘
                                ▼
              assemble.py  +  tts.py (Enishi JP)  +  thumbnail_text.py
                                ▼
                    video ngang (dài)  +  video dọc (Shorts)
```

### Data model (SQLite)

```
project(id, name, material, style_lock)
character(id, project_id, name, entity_type, description,
          voice_description, ref_media_id UUID, ref_url, uploaded_at)
scene(id, project_id, display_order, chain_type, parent_scene_id,
      prompt,            ← CHỈ tả hành động
      video_prompt,      ← chuyển động + góc máy, chia 0-3s/3-6s/6-8s
      character_names[],
      {ori}_image_media_id, {ori}_end_scene_media_id,
      {ori}_video_media_id, {ori}_video_url,
      trim_start, trim_end, qc_score)
request(id, type, scene_id, status, retry_count, error_message, next_retry_at)
```

### State machine của 1 scene

```
PENDING ─► REF_READY ─► IMAGE_READY ─► VIDEO_READY ─► QC_PASS ─► CONCAT
                │            │              │            │
                │            │              │            └─► QC_FAIL ─► regen
                │            │              └─► FAILED ─► retry/backoff
                └─ chặn cứng nếu ref thiếu media_id
```

### Bảng endpoint Flow (copy nguyên từ flowkit, base `aisandbox-pa.googleapis.com`)

| Việc | Endpoint |
|---|---|
| Sinh ảnh | `/v1/projects/{pid}/flowMedia:batchGenerateImages` |
| Upload ảnh | `/v1/flow/uploadImage` |
| Video i2v | `/v1/video:batchAsyncGenerateVideoStartImage` |
| Video i2v_fl | `/v1/video:batchAsyncGenerateVideoStartAndEndImage` |
| Video r2v | `/v1/video:batchAsyncGenerateVideoReferenceImages` |
| Check status | `/v1/video:batchCheckAsyncVideoGenerationStatus` |
| Credits/tier | `/v1/credits` |

---

## 6. Project Structure

```
e:/CLAUDE/YOUTUBE/h2dev/
├── pipeline/
│   ├── (giữ nguyên) fetch_script.py · gen_images.py · gpti2_gen.py
│   │                tts.py · openspeaker_tts.py · assemble.py · thumbnail_text.py
│   └── veo/                        ← MỚI
│       ├── bridge/                 ← extension MV3 (port từ flowkit)
│       │   ├── manifest.json
│       │   ├── background.js       ← WS client + proxy API + bắt token
│       │   ├── content.js
│       │   ├── injected.js         ← grecaptcha.enterprise.execute
│       │   └── rules.json          ← DNR set Referer/Origin
│       ├── flow_client.py          ← WS server :9222, ghép request↔response
│       ├── flow_api.py             ← dựng payload 6 endpoint + models.json
│       ├── queue.py                ← 5 concurrent + cooldown 10s + backoff
│       ├── store.py                ← SQLite
│       ├── refs.py                 ← sinh + upload ảnh ref, ép UUID
│       ├── scenes.py               ← sinh ảnh scene (nạp toàn bộ ref)
│       ├── chain.py                ← endImage = ảnh scene SAU + trim gap
│       ├── qc.py                   ← contact sheet + claude -p
│       ├── models.json             ← tách riêng, Flow đổi model chỉ sửa file này
│       └── run_anime.py            ← CLI orchestrator
├── skills/
│   ├── script-anime-jp/            ← MỚI (fork từ script-satori-jp)
│   ├── image-anime-jp/             ← MỚI — sinh entity table + prompt hành động
│   └── video-prompt-anime-jp/      ← MỚI — video_prompt + góc máy
└── plans/260907-1351-veo-anime-jp/
```

---

## 7. Implementation Phasing

| Phase | Deliverable |
|---|---|
| **P1** | Cầu nối sống: extension + WS + bắt token + giải captcha → gọi được `/v1/credits` ra đúng tier |
| **P2** | Ảnh ref có UUID + ảnh scene nạp đủ ref (chặn cứng khi thiếu) |
| **P3** | Clip video i2v + i2v_fl + queue/retry → 8 clip chain, concat liền mạch |
| **P4** | Ghép hoàn chỉnh: TTS Enishi + srt + thumbnail → **1 Shorts 60s** |
| **P5** | QC contact-sheet qua CLI + chính sách retry theo chuỗi lỗi |
| **P6** | Video dài 5-10 phút + T4 sinh song song dọc/ngang → cắt Shorts từ video dài |

---

## 8. Risks & Mitigations

| # | Rủi ro | Mức | Cách giảm thiểu |
|---|---|---|---|
| R1 | `PUBLIC_ERROR_UNUSUAL_ACTIVITY` — Google flag bot | **Cao** | ≤5 concurrent, gap ≥1s, không chạy 2 phiên song song; dính thì dừng submit, xoá cookie `google.com`+`labs.google`, login lại |
| R2 | Nhân vật drift qua nhiều scene | **Cao** | Ref UUID nạp vào MỌI scene + material khoá style + QC `character_consistency` ≥7.5 mới cho ghép |
| R3 | Concat gap 0.8-1.4s frame tĩnh tại mỗi mối nối chain | Trung bình | Trim 0.4-0.7s mỗi đầu; chỉ chain khi cùng bối cảnh, đổi cảnh thì hard cut |
| R4 | Close-up macro → AI bịa nhân vật khác khi zoom out | Trung bình | Pattern B: `endImage` = ảnh wide của scene cha làm mỏ neo |
| R5 | `media_id` hết hạn ~1h giữa lô dài | Trung bình | Bắt chuỗi `"not found"` → tự re-upload từ `image_url`, re-queue |
| R6 | Model `*_ultra_relaxed` trả operations RỖNG im lặng trên tier ADVANCED | Trung bình | Mặc định `veo_3_1_i2v_lite_low_priority`; validate operations rỗng = lỗi, không phải thành công |
| R7 | Timeout oan: `VIDEO_POLL_TIMEOUT` mặc định 420s quá ngắn cho low-priority | Thấp | Nâng lên 1200s |
| R8 | `os.symlink` của contact sheet fail trên Windows | Thấp | Đổi sang copy file |
| R9 | Ô trống trong lưới contact sheet → model chấm nhầm là lỗi video | Thấp | Số cột phải là **ước số** của số frame trong chunk |
| R10 | Flow đổi tên model/endpoint | Thấp | Tách `models.json` + bảng endpoint ra file riêng |

---

## 9. Success Criteria (đo được)

- [ ] **S1** — 1 Shorts 60s (8 clip) từ script JP → mp4 hoàn chỉnh trong **≤ 25 phút**, chi phí clip **= 0đ**
- [ ] **S2** — QC `character_consistency` **≥ 7.5/10** trên **≥ 90%** clip của 1 video
- [ ] **S3** — Mối nối chain sau trim: **≤ 0.2s** frame tĩnh (đo bằng ffprobe scene-change)
- [ ] **S4** — Video 10 phút (~75 clip): tỉ lệ clip FAIL cuối cùng **≤ 10%**, tổng thời gian **≤ 3 giờ**
- [ ] **S5** — Chi phí/video 10 phút **≤ 2.000đ** (chỉ TTS; clip 0đ, QC 0đ)
- [ ] **S6** — Ngắt mạng/tắt extension giữa lô → chạy lại **không sinh lại** clip đã xong
- [ ] **S7** — 0 lần dính `UNUSUAL_ACTIVITY` trong 3 video liên tiếp

---

## 10. Decisions Locked

| # | Quyết định | Lý do |
|---|---|---|
| D1 | **Port lõi sang `pipeline/veo/`**, KHÔNG cài FlowKit gốc | Windows native, chỉ mang thứ cần dùng |
| D2 | Extension MV3 **tái dùng gần nguyên vẹn** | Phần khó nhất, self-contained, đã verify thật |
| D3 | Model mặc định `veo_3_1_i2v_lite_low_priority` (**0 credit**) | Chạy được mọi tier kể cả `SERVICE_TIER_ADVANCED` |
| D4 | Trần độ dài **10 phút/video** (~75 clip); dài hơn thì cắt tập | >225 clip đẩy rủi ro R1 lên quá cao |
| D5 | Thị trường **Nhật**, tái dùng voice Enishi + skill JP | Nối tiếp Satori, không dựng lại hạ tầng |
| D6 | Sinh **song song ngang + dọc** (T4) | Video dài + Shorts từ cùng một lô |
| D7 | State bằng **SQLite**, không JSON phẳng | Vòng đời `media_id` + retry cần quan hệ |
| D8 | QC bằng **contact sheet + `claude -p`**, không Gemini API | 0đ, và thấy được diễn biến theo thời gian |
| D9 | `prompt` = **CHỈ hành động**; ngoại hình chỉ nằm ở `description` của entity | Luật cốt lõi giữ nhân vật đồng nhất |
| D10 | `endImage` = ảnh scene **SAU** (không phải scene trước) | Đặt nhầm là mất hết tác dụng chain |

---

## 11. Out of Scope

Cố tình **KHÔNG** làm trong mảng này:

- Video dài hơn 10 phút trong một mạch (mảng Satori ảnh tĩnh vẫn lo phần 25-30 phút)
- Upload YouTube tự động — giai đoạn sau, mở rộng từ `tools/channel_setup.py`
- Upscale 4K (`UPSCALE_VIDEO`) — cần tier cao, chưa cần cho Shorts/10 phút
- Nhạc nền Suno — đã có sẵn qua OpenSpeaker, không dựng lại
- Dashboard React + FastAPI REST của FlowKit
- Thị trường Hàn / tiếng Anh — nhân bản sau khi Nhật ra số
- Kỹ thuật r2v (T3), branching (T5) — để dành sau khi P1-P6 chạy ổn

---

## 12. Next Step

`/ck:plan` → viết `plan.md` (index 6 phase) → anh duyệt → viết `phase-01-cau-noi-extension.md`.
