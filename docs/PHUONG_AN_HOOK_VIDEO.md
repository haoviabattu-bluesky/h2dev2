# PHƯƠNG ÁN HOOK 20–30 GIÂY ĐẦU — ÁP DỤNG MỌI TẬP, MỌI LANE

> Trạng thái: **ĐÃ DUYỆT, ĐÃ TRIỂN KHAI** (2026-09-23) — xem plan `docs/superpowers/plans/2026-09-23-hook-video.md`
> (code + cổng QC + CLI + spec bước 3 + tài liệu §2b/router/SOP đã xong).
> Nguồn: `E:\CLAUDE\YOUTUBE\h2dev\HOOK_VIDEO_20_30S_GOOGLE_FLOW_SOP.md` (SOP anh đưa) + 3 quyết định anh chốt
> cùng ngày (ghi ở §0). Báo cáo hiện trạng đã làm trước đó (6 lane, 30 giây đầu thật) không lặp lại ở đây.

## 0. BA QUYẾT ĐỊNH ĐÃ CHỐT (không bàn lại)

| # | Quyết định | Hệ quả thiết kế |
|---|---|---|
| Q1 | Video nguồn hook yếu/không hook → **tự dựng hook từ climax/reveal của chính truyện** (SOP §3 H2) | H2 chỉ là *chẩn đoán*; không bao giờ đổi video nguồn vì hook |
| Q2 | **Hook = artifact thượng nguồn**, khoá TRƯỚC S2; S2 viết thân **nối từ hook**; `extract_beats` coi hook là **Beat 0 đã khoá**; thay 30s đầu ở hậu kỳ chỉ là *repair mode*; **HOOK_STALE** khi title/thumb/core event/payoff/reveal/timeline đổi | Flow: S0 → H1 → H2 → H3 → H4 LOCK → S2 → S3 → Sol → patch → LOCK SCRIPT |
| Q3 | Tập **chưa đăng** (đã có kịch bản/ảnh/voice/final.mp4): **giữ nguyên** kịch bản + ảnh, chỉ **thêm hook** dựng thành clip **ghép vào đầu** video | Cần "repair mode" riêng: hook viết từ chính tập, không đụng `script.txt`/`voice.mp3`/`img/` |

Điểm ngầm trong Q3: "ghép **video** hook" ⇒ phần hình của hook là **clip động** (không phải ảnh tĩnh) — áp cho cả tập mới
(§5) để hai loại tập ra cùng một chất lượng mở đầu.

---

## 1. NGUYÊN TẮC (áp cho mọi lane, mọi tập)

1. **Mọi tập phải có `hook/hook_locked.txt` trước khi S2 chạy.** Không có → S1Q BLOCK (chưa tốn lượt viết nào).
2. **Hook rút từ video nguồn** (3 phép kiểm H1–H3) rồi mới viết cho mình; không viết hook chỉ từ tiêu đề.
3. **Hook là pure prose** giống `script.txt` (không marker, không `[HOOK]`), độ dài = `voice.char_rate / 2` chữ ±15%
   (≈30 giây đọc: satori 135 · F 142 · E 159 · G 160 · D 140 · A 190). Marker/VISUAL/SFX nằm ở file JSON riêng.
4. **Model viết chạm hook 1 lần** (brain_model = Fable), sửa = patch_model (Opus 5), Sol chỉ chấm — đúng luật phân vai
   `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §0a. Claude Code = lớp 3 đọc bản khoá, không sửa tay.
5. **Sau `HOOK_LOCKED`, `script.txt` bắt buộc bắt đầu bằng đúng chuỗi hook** (so sau khi normalize) — máy đo ở S3, sai = việc.
6. **Khác biệt lane chỉ qua field profile** (`script.hook.*`), cấm `if profile_id`. Lane không khai khối `hook` = chạy mặc định (vẫn bắt buộc, không có cách tắt).

---

## 2. ARTIFACT TRONG THƯ MỤC TẬP — `assets/<lane>/epNN-<slug>/hook/`

| File | Ai sinh | Nội dung |
|---|---|---|
| `source.json` | máy (H1–H3) | `video_id`, URL, `transcript_0_30s` (nguyên văn + mốc giây), `title`, `description`, `thumb_path`, `hook_4_nhip` (event/contradiction/stake/open_loop — chuỗi hoặc null), `hook_type` (A–E theo SOP §3), `score_0_12`, `video_hook_verdict` (`manh`/`yeu`/`khong`), `promise_match` (title/thumb/desc ↔ hook: PASS/FAIL + lý do) |
| `frames/` | máy (H2) | 6–8 khung hình 0–30s video nguồn (chỉ để soi, không dùng lại) |
| `hook_candidates.txt` | brain_model | 3 hook (Q2 anh chốt 3, không 5), mỗi hook kèm tự chấm 6 tiêu chí + loại A–E + 1 dòng "promise" |
| `hook_qc.json` | máy + Sol | tất định (§4.3) + Sol lens `hook`: chọn 1, PASS/FIX + lý do từng ô checklist SOP §16 |
| `hook_locked.txt` | máy ghi sau PASS | pure prose, 1 đoạn hoặc 2 đoạn, câu cuối = open loop |
| `hook_lock.json` | máy | `sha256(hook_locked.txt)`, `promise:{title, thumb_text, core_event, payoff, reveal, timeline_start}` (rút từ hồ sơ tại thời điểm khoá), `stale:false`, `source:"hook_locked.txt"`, `mode:"upstream"|"repair"` |
| `hook_storyboard.json` | Claude Code (bước 1) sau LOCK | 4–7 shot: `t0,t1,voice,visual,shot_type,ref_image,flow_prompt` (11 field SOP §13), `continuity` nối `characters.json` |
| `flow_prompts/shot_NN.txt` | máy từ storyboard | 1 file/shot, dán thẳng Grok/Flow |
| `hook_voice.mp3` + `.srt` | bước 2/3 (TTS cùng `voice.id`) | chỉ **repair mode** (tập mới: hook đã nằm trong `voice.mp3` chung) |
| `hook_final.mp4` | bước 3 | 20–30s, 4–7 clip + voice + nhạc/SFX (§5) |

---

## 3. PIPELINE TẬP MỚI (lean flow)

```
S0  hồ sơ tập: competitor.txt(+segments) · series_ctx.txt · title.txt (promise) · [A/D] HOOK 30 GIÂY ĐẦU của hồ sơ
H1  máy: cắt 0–30s transcript nguồn theo giây · lấy title/description/thumbnail gốc · tách 4 nhịp · loại · điểm
H2  máy+vision: 6–8 khung 0–30s video nguồn → verdict mạnh/yếu/không
H3  LLM: promise_match nguồn (title↔thumb↔desc↔hook nguồn) PASS/FAIL
H2' brain_model viết 3 hook cho TẬP MÌNH (đầu vào: source.json + hồ sơ + title.txt + outline/payoff)
H3' máy tất định + Sol lens hook → chọn 1 · PASS/FIX (FIX → patch_model ≤2 lượt; FIX×3 = PASS theo luật lean)
H4  HOOK_LOCKED: hook_locked.txt + hook_lock.json (sha256 + promise) · Claude Code lớp 3 đọc 2 phút, ghi sheet cột HOOK
S2  Fable viết TOÀN VĂN — prompt có khối "PHẦN MỞ ĐẦU ĐÃ KHOÁ" (§3.2) · extract_beats Beat 0 = hook (§3.3)
S3  máy đo cũ + phép mới: script bắt đầu bằng hook nguyên văn · hook không bị kể lại trong 20% đầu thân
S5  Sol lens lane + mục "NỐI TỪ HOOK" (§4.4)
patch tại chỗ · LOCK SCRIPT (sha256) — hook_lock.json không đổi
B5W storyboard hook → flow_prompts (Claude Code) · giao bước 2/3 cùng gói tập
```

### 3.1 Vị trí trong code (không viết code ở phương án này — chỉ điểm neo)
- `pipeline/lean_script.py::run()` — chèn H1–H4 giữa S1Q và S2 (sau dòng `[S1Q] ✓ hồ sơ đủ`). Module mới `pipeline/hook_stage.py` giữ toàn bộ H1–H4 để `lean_script.py` chỉ gọi 1 hàm `hook_stage.ensure_locked(d, prof, ...)`.
- `pipeline/ai_steps.py::_pass1_prompt()` — thêm khối §3.2 khi có `hook_locked.txt`.
- `pipeline/ai_steps.py::extract_beats()` — §3.3.
- `pipeline/lean_script.py::do_tat_dinh()` — thêm phép "bắt đầu bằng hook" + "không kể lại".
- `pipeline/lean_script.py::PRESERVE` — thêm "đoạn mở đầu đã khoá (hook) — giữ nguyên từng chữ".
- `pipeline/qc_script_sol.py` — lens mới `hook` (chấm hook) + 1 mục chung "NỐI TỪ HOOK" chèn vào cả 3 lens cũ.
- `pipeline/gate_common.py` — `hook_lock.json` vào cơ chế STALE hiện có (cùng kiểu `generated_from_script_sha256`).
- `pipeline/qc_script.py::mo_dau()` — vá `return []` thành cảnh báo "lane không có marker → cổng mở đầu do hook_stage đảm nhận" (không còn ĐẠT giả).
- Luồng cũ B3 (`make_video.py::b3_script`, lane chưa lean như `Lopezzapa68`): chỉ chèn khối §3.2 vào prompt; không wire đầy đủ (lane này chưa hoạt động).

### 3.2 Khối prompt S2 (nguyên văn dự kiến)
```
PHẦN MỞ ĐẦU ĐÃ KHOÁ — chép NGUYÊN VĂN làm đoạn đầu tiên của bản kể, không đổi một chữ:
<hook_locked.txt>
Viết phần còn lại NỐI TỰ NHIÊN từ câu cuối của đoạn trên: không kể lại thông tin đoạn trên vừa nói,
không mở lại câu chuyện từ đầu (không tả thời tiết/mùa/giới thiệu kênh), không giới thiệu tên-tuổi-nghề
người kể trước khi trả câu hỏi mà đoạn trên đã mở — trả lời câu hỏi đó ở đúng chỗ khung sự kiện quy định.
```
Ngân sách `ngan_sach()` trừ số chữ hook khỏi `mo_dau` để tổng không phình.

### 3.3 `extract_beats` — Beat 0
- Output PASS 0 thành: `N00. [HOOK — ĐÃ KHOÁ] <hook_locked.txt nguyên văn>` rồi `N01…N10` như cũ, kèm dòng luật cho PASS 0:
  "N01 là SETUP nối từ N00; không mô tả lại sự kiện N00; nếu transcript nguồn mở bằng đúng sự kiện đó thì N01 bắt đầu từ *sau* nó".
- `beats.txt` ghi thêm header JSON 1 dòng: `{"beat0":{"beat_type":"hook","locked":true,"source":"hook_locked.txt","sha256":...}}`.
- Lý do giữ nguyên "giấu bản gốc": bài học 2026-09-08 (dịch sát) vẫn đúng; hook mình đã là văn bản của mình nên đưa nguyên văn không vi phạm.

### 3.4 HOOK_STALE
`hook_lock.json.promise` chụp 6 giá trị lúc khoá. Trước S2 và trước B4/B5/B7, máy so lại:
`title.txt` (title_promise) · `thumb_text.txt` (thumb_promise) · `core_event/payoff/reveal/timeline_start` (rút từ `series_ctx.txt`
+ `story_facts.json` nếu có; lane không có thì hash `series_ctx.txt`). Lệch → `stale:true` → BLOCK với thông báo "quay lại H1–H4".
Sửa câu giữa bài / độ dài / hơi văn / thoại phụ → không đụng hook (hash hook không đổi, S3 vẫn kiểm "bắt đầu bằng hook").

### 3.5 Hai kiểu nguồn
| Kiểu | Lane | H1 lấy từ | H2 | H3 |
|---|---|---|---|---|
| Nhân bản 1 video | satori, F, G, E, H, I, J | `competitor.segments.json` (bắt buộc có — `fetch_script.py` đã sinh; lane dán transcript từ research phải giữ timestamp) | tải 30s đầu video nguồn | title/desc/thumb video nguồn |
| Hồ sơ đề tài | A, D | trường `HOOK 30 GIÂY ĐẦU` của hồ sơ (`docs/KHUON_HO_SO_DE_TAI.md` dòng 51) + `hook_type` của video mẫu gần nhất do K3 `retrieve_videos.py` chọn | video mẫu K3 chọn | title/thumb video mẫu đó (mô tả nếu có) |
`qc_hoso.py` thêm phép: trường HOOK 30 GIÂY ĐẦU phải có ≥1 neo (số/tên/nơi) — hiện không kiểm.

---

## 4. CỔNG QC HOOK

### 4.1 Đầu vào H2' (viết hook) — thiếu 1 = không viết
`source.json` · `title.txt` · outline/payoff (lean: `series_ctx.txt` + "Gợi ý N mục"/"mục cuối = cú lật"; hồ sơ: KHUNG N CHƯƠNG + CTA) · `characters.json` nếu đã có (để hook nhắc đúng nhân vật).

### 4.2 Prompt viết hook (rút từ SOP §18, giữ đúng thứ tự)
H1 đọc toàn bộ → 3 candidate (mỗi cái ghi loại A–E) → tự chấm 6 tiêu chí 0–2 → chọn → viết 4 nhịp trong `char_rate/2` chữ → 1 câu chuyển vào setup. Cấm: chào hỏi, giới thiệu kênh, CTA, spoil reveal, fake drama, dữ kiện không có trong hồ sơ, tả thời tiết mở màn, tên-tuổi-nghề trước giây 30. Ngôn ngữ đích, câu ngắn, có chỗ nghỉ (lane người già).

### 4.3 Tất định (0 LLM, `hook_stage.check()`)
- Độ dài trong `[0.85, 1.15] × char_rate/2`.
- ≥1 neo cụ thể (số / tên riêng / thoại「」) trong 40% đầu.
- Không chứa từ cấm theo ngôn ngữ (`こんにちは`, `皆さん`, `チャンネル登録`, `今日は…お話し`, `私の名前は` …) — danh sách khai `script.hook.banned_openers` mặc định theo `language`.
- Câu cuối kết bằng dạng mở (`…`, câu hỏi, `のは、後になってからだった` …) — máy chỉ WARN, Sol quyết.
- Mọi số trong hook ∈ `SỐ ĐƯỢC PHÉP` (dùng lại `_so_lieu_ngoai_tu_lieu`).

### 4.4 Sol lens `hook` (PASS/FIX; không có REMAKE — hook ngắn, FIX là đủ)
Checklist SOP §16 nội dung + nhịp: khớp title · khớp thumb (nếu có `thumb_text.txt`) · sự kiện có trong hồ sơ · không fake · không spoil · có open loop · có stake · hiểu được không cần setup · 3–5s đầu đã có sự kiện · không câu thừa · ≥4 nhịp thông tin · retention test ("tắt title/thumb, muốn xem tiếp không?"). Chọn 1 trong 3 candidate, nêu vì sao.
Mục chung thêm vào 3 lens cũ khi chấm toàn văn: **"NỐI TỪ HOOK"** — thân có kể lại hook không, có reset không, câu hỏi hook có được trả đúng chỗ không, có phá promise không.

### 4.5 Cổng đồng bộ ra ngoài (B7/B10)
`title.txt` · `thumb_text.txt` · `TIEU_DE_MO_TA.txt` sinh **sau** HOOK_LOCKED; `qc_final.py` thêm phép 3 chiều hook ↔ title ↔ chữ thumbnail (LLM 1 lượt). Lane G ep09 (title 図書館, 30s đầu không nhắc 図書館) làm bài test hồi quy.

---

## 5. PHẦN HÌNH CỦA HOOK (SOP §10–14) — 3 đường, kèm lợi/hại

| Đường | Cách | Mạnh | Yếu / rủi ro | Chi phí/tập | Luật dự án |
|---|---|---|---|---|---|
| **V1 — Grok Imagine (khuyến nghị)** | 4–7 ảnh AI theo storyboard (ima2/gpti2, REF-LOCK từ `characters.json`) → image-to-video 6/10/15s → ghép | 0 watermark; 15s/clip nên 2–3 clip đủ 30s; mặt bám ảnh nguồn (không trôi); profile Pro sẵn `E:\CLAUDE\YOUTUBE\GROK_PROFILE` port 9334; runner `E:\CLAUDE\YOUTUBE\GROK_VIDEO\grok_batch.py --jobs jobs.csv` resume được | 720p (1080p khoá theo gói) → phải upscale/hoặc chấp nhận; tiếng Grok gần như câm → voice/nhạc ghép sau; bẫy `x-statsig-id` theo endpoint đã ghi ở skill | ảnh 0đ (ima2) hoặc ~50đ×6 (gpti2); clip tính vào gói Pro đã trả; ~1–2 phút/clip | bước 2/3 (máy 2/agent) — Claude Code chỉ giao storyboard + jobs.csv |
| V2 — Veo 3.1 (Flow, gói Ultra) | Frame-to-video 8s/clip ×4 | có audio/SFX sẵn; 1080p | có watermark phải delogo (mờ 1 góc); 8s/clip = nhiều clip hơn; UI robot dễ gãy selector | gói Ultra đã trả; 63–85s/clip | bước 2/3 |
| V3 — ảnh tĩnh mật độ cao | 6–7 ảnh trong 30s + chuyển cảnh `video-chuyen-canh` (mờ-vào/zoom-đen), `--zoom 1.0` | không tooling mới, 0đ, cùng chất với thân video | vi phạm tinh thần SOP §10 ("motion nhỏ nhưng thật"), yếu hơn V1 về giữ chân; ảnh đứng 4–5s/ảnh | 0đ | đúng luật ảnh tĩnh |

Khuyến nghị **V1**, giữ **V3 làm fallback** khi Grok hết lượt/lỗi (storyboard dùng chung, chỉ đổi bước dựng).
Luật "ảnh đứng yên, cấm Ken Burns" **không bị phá**: đó là luật cho ảnh tĩnh của thân video; hook là clip sinh sẵn chuyển
động thật, không phải zoom/pan giả trên ảnh. Ghi 1 dòng ngoại lệ này vào `CLAUDE.md` mục chuyển cảnh khi triển khai.
Nối hook → thân: crossfade 17–18 khung hoặc mờ-vào (công thức đã đo ở `video-chuyen-canh/references`), nhạc hook nhẹ tension
rồi hạ về nhạc nền thân.

---

## 6. REPAIR MODE — TẬP CHƯA ĐĂNG (Q3)

Nguyên tắc: **không đụng** `script.txt` · `voice.mp3` · `img/` · `final.mp4`. Chỉ thêm `hook/` và xuất `final_with_hook.mp4` cạnh `final.mp4`.

1. H1–H3 chạy như tập mới (nguồn = video kênh mẫu của tập đó nếu truy được; không truy được → bỏ H1–H3, ghi `source.json.video_id=null`).
2. H2'/H3'/H4 với đầu vào = **chính `script.txt` đã có** (climax/reveal/payoff rút từ nó) + `title.txt`/`thumb_text.txt` đã có. `hook_lock.json.mode="repair"`.
3. **Câu cuối hook = câu cầu nối** vào đoạn 1 cũ của script (hook_stage đưa đoạn 1 cũ vào prompt, yêu cầu "câu chuyển sao cho đoạn sau đây nghe như setup, không như bắt đầu lại"). Rủi ro anh đã nêu ("giây 31 như sang bài khác") giảm nhưng không hết — tập nào đoạn 1 cũ là tả thời tiết (satori ep13/14) sẽ vẫn hơi gãy; **tuỳ chọn opt-in từng tập**: cắt đoạn 1 cũ khỏi audio bằng mốc `voice.srt` (không sửa script.txt, chỉ cắt `voice.mp3` + dịch mốc `anchors`/`img_doan`) — mặc định KHÔNG bật, chỉ khi anh chỉ định tập.
4. `hook_voice.mp3` TTS cùng `voice.id`/speed của profile → `hook_final.mp4` (V1) → `final_with_hook.mp4 = hook_final + chuyển cảnh + final.mp4` (bước 3; A tự làm).
5. Title/thumb: giữ nếu H3' PASS khớp; **nếu Sol báo lệch promise thì được sửa title/thumb_text** (chưa đăng nên không phá gì) — giả định của em, anh xác nhận.
6. Ứng viên (có `final.mp4`, cần đối chiếu cột trạng thái sheet để loại tập đã đăng): satori ep08–ep14 (7) · Lane D ep01–ep11 (11) · Lane A ep01–ep08 (7) · Lane E ep01 · Lane G ep01. Tập chưa render (F/G toàn bộ, E ep02+) đi đường tập mới **nhưng giữ nguyên script** (Q3): hook viết repair-mode, S2 không chạy lại; storyboard + ảnh + clip hook thêm vào gói giao máy 2.

---

## 7. HẠ TẦNG LÀM 1 LẦN

| Việc | File | Ghi chú |
|---|---|---|
| Lấy **mô tả** + **thumbnail** gốc | `pipeline/yt_tags.py` (đã đọc `ytInitialPlayerResponse` → thêm `shortDescription`), `pipeline/channel_analyzer.py` K1 (tải `i.ytimg.com/vi/<id>/maxresdefault.jpg` → `_raw/thumbs/<rank>_<view>_<id>.jpg` như lane I đã làm tay), `pipeline/fetch_script.py` (ghi thêm `title/description/thumb` vào `competitor.segments.json`) | tải bù 6 kênh mẫu đang thiếu ảnh; rate-limit YouTube thấp hơn Wikimedia nhưng vẫn `--gap` |
| K2 `hook_type` → khối có cấu trúc | `channel_analyzer.py` VIDEO_PROMPT | thêm `hook_0_30s_verbatim`, `hook_4_nhip`, `hook_kind`, `promise_match` — chạy lại K2 khi cần, cũ vẫn đọc được |
| H0 ghi nguồn | `state.json` thêm `source:{video_id,url}`; `fetch_script.py` ghi sẵn; hồ sơ A/D ghi `hoso_id` | 0/41 tập hiện có |
| Sheet | tab lane thêm cột **HOOK** (`Locked hh:mm` / `STALE` / `Repair`) — không đổi cột D | tool tự tạo cột như channel_branding |
| Tài liệu | `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` thêm §2b "H1–H4"; mỗi `docs/SOP_<LANE>.md` 1 dòng trỏ; `CLAUDE.md` 1 dòng router + 1 dòng ngoại lệ clip hook | tuân hàng rào #4 (router mỏng) |

---

## 8. CHI PHÍ & THỜI GIAN ƯỚC (mỗi tập)

| Khoản | Tập mới | Repair |
|---|---|---|
| LLM | H1–H3: 2 lượt Gemini/Sol (~0) · hook: 1 Fable (0đ OAuth) + 1–2 Sol + ≤2 patch Opus | như tập mới |
| TTS | 0 (nằm trong voice chung) | ~150 chữ ≈ 200 credit ≈ 0,001$ |
| Ảnh hook | 4–7 ảnh: ima2 0đ / gpti2 ≈ 300đ | như tập mới |
| Clip | 2–3 clip Grok (gói Pro) | như tập mới |
| Máy | +6–10 phút trước S2 | 15–20 phút/tập (không re-render thân) |
| Claude Code (lớp 3) | +3–5 phút đọc hook khoá + viết storyboard | +10 phút (đọc script cũ chọn climax) |

Rủi ro chính: (1) Sol chấm hook không tất định (đã thấy ở S4 A/B) → áp luật FIX×3=PASS; (2) Grok 429/statsig — đã có cách lấy id
miễn phí ở skill; (3) repair mode giây 31 gãy nhịp với tập mở bằng thời tiết — có opt-in cắt đoạn 1; (4) HOOK_STALE báo động
giả khi `series_ctx.txt` chỉ sửa chính tả → so theo 6 trường promise trước, hash cả file chỉ khi lane không khai được trường.

---

## 9. THỨ TỰ TRIỂN KHAI (đề xuất; kế hoạch chi tiết viết sau khi anh duyệt)

| Pha | Việc | Nghiệm thu |
|---|---|---|
| P0 | Hạ tầng §7 (desc/thumb/segments/H0) | 7 kênh mẫu có `_raw/thumbs` + description; 1 tập test có `competitor.segments.json` đủ title/desc/thumb |
| P1 | `hook_stage.py` H1–H4 + artifact §2 + cổng §4.3–4.4 + STALE + wire `lean_script.py`/`_pass1_prompt`/`extract_beats` Beat 0 | **Pilot 1 tập mới Lane G** (kịch bản xong nhanh, Sol/Fable đã quen): `hook_locked.txt` PASS, script bắt đầu đúng hook, Sol mục "nối từ hook" PASS; test hồi quy Lane G ep09 (promise lệch phải FAIL) |
| P2 | Storyboard + `flow_prompts` + gói giao bước 2/3 (`docs/GIAO_VIEC_BUOC3_AGENT.md` thêm mục hook; `jobs.csv` Grok) | 1 `hook_final.mp4` 20–30s, 4–7 shot, nối được vào thân, QC visual SOP §16 |
| P3 | Repair mode §6 — **pilot satori ep14** (tập tệ nhất: 30s thời tiết) | `final_with_hook.mp4`; retention test tay 30s |
| P4 | Chạy repair cho danh sách §6.6 (sau khi đối chiếu sheet) + tài liệu §7 | sheet cột HOOK đủ; SOP mỗi lane có 1 dòng |

Việc **bước 2/3** (TTS hook repair, sinh clip Grok, ghép `hook_final.mp4`, `final_with_hook.mp4`) do máy 2/agent bước 3 làm theo
`docs/GIAO_VIEC_BUOC3_AGENT.md`; Lane A theo ngoại lệ tự render. Claude Code dừng ở `hook_locked.txt` + storyboard + flow_prompts + jobs.csv.

---

## 10. ĐIỂM CÒN CHỜ ANH CHỐT

1. Phần hình hook: **V1 Grok** (khuyến nghị) / V2 Veo / V3 ảnh tĩnh.
2. Repair mode: được **sửa title/thumb_text** của tập chưa đăng khi lệch promise? (em giả định CÓ.)
3. Opt-in "cắt đoạn 1 cũ khỏi audio" cho tập mở bằng thời tiết — mặc định TẮT, anh muốn bật cho satori ep13/ep14?
4. Pilot: 1 tập mới Lane G + repair satori ep14 — đồng ý thì em viết kế hoạch triển khai chi tiết (task/file/test) và bắt đầu P0.
