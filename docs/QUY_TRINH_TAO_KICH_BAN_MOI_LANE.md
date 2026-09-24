# QUY TRÌNH TẠO KỊCH BẢN — ÁP DỤNG CHO MỌI LANE (`script.flow = "lean"`)

Chốt 2026-09-20 sau 2 tập Lane G đo thật (`docs/QUY_TRINH_KICH_BAN_GON.md` = thiết kế + số đo; file này = **hướng dẫn
làm**). Đọc file này là đủ để một lane bật luồng mới; không cần đọc thiết kế.

> **Một câu:** Fable viết đúng ngân sách → máy đo tất định → Sol chấm tính hợp lý (lời cuối) → Fable patch ≤2 lần,
> mỗi patch chạy lại máy + Sol → PASS thì khoá SHA256, **không ai sửa `script.txt` nữa** → Claude Code đọc bản khoá →
> ghi sheet **`Done`**. Không có trạng thái "chờ anh duyệt".

---

## 0. AI LÀM GÌ

| Việc | Ai | Ghi chú |
|---|---|---|
| S1 hồ sơ tập: `competitor.txt` · `series_ctx.txt` · `title.txt` | **Claude Code (tab lane)** — tay | việc duy nhất tốn đầu người trước khi bấm chạy |
| S2 viết khung + viết toàn văn ĐÚNG NGÂN SÁCH | **Fable 5.1** (`claude -p`, 0đ trong gói) | model duy nhất được chạm `script.txt` |
| S3 đo tất định: độ dài · phẩy/hơi/thoại · dấu 、(tự gỡ) · N mục có marker · outro (tự thay nguyên văn) · CTA giữa (nếu lane khai) · số liệu ↔ `SỐ ĐƯỢC PHÉP` (cả kanji) · phép cộng tổng tiền · tên↔tuổi nhất quán · đoạn trùng · bám gốc (WARN) | **Máy** (0 LLM) | máy kiểm hết những gì máy kiểm được — Sol không phải đếm chữ |
| S5 chấm tính hợp lý/hợp lệ: nhân quả · dòng thời gian · động cơ · câu Nhật lạ · lời hứa tiêu đề · thứ máy mù | **GPT-5.6-sol** (9router local) | lens theo lane (§1.3); PASS = 0 [NẶNG] và <3 [VỪA]; **khoá chỉ khi PASS 2 lần LIÊN TIẾP cùng bản** (`sol_pass_need`, 2026-09-22 — Sol không tất định: bản ep10 Lane G đã LOCK PASS chấm lại 2/2 ra FIX với lỗi timeline [NẶNG] thật) |
| S4 patch tại chỗ theo danh sách việc (máy hoặc Sol) | **Opus 5** (`script.patch_model`, anh chốt 2026-09-22) — không khai thì = `brain_model` | ràng buộc: MUST PRESERVE · trần 1,05×/sàn 0,9× · đổi ≤40% đoạn (nén ≤70%) · không mất số. **Fable chỉ VIẾT (S2), không sửa** — 3 vai tách: Fable=tác giả · Sol=giám khảo · Opus=thợ vá. A/B replay 9 lượt patch thật (`pipeline/bench_patch_model.py`): Opus ngang Fable (Sol PASS 7/9; 2 FIX ở ep10 mà bản Fable đã PASS chấm lại cũng FIX), số câu đổi ngoài phạm vi Sol trích tương đương, 110–180s/lượt |
| Lớp 3: đọc bản KHOÁ, đối chiếu tư liệu + luật lane | **Claude Code (tab lane)** | thấy lỗi → `viec_tay.txt`, KHÔNG sửa tay (§4) |
| Prompt ảnh · phụ đề · map ảnh↔câu · dịch · analyzer | Gemini | ngoài luồng master, **cấm ghi `script.txt`** |

### 0a. QUY TẮC PHÂN VAI MODEL — bắt buộc mọi lane dùng `engine: claude_p` (anh chốt 2026-09-22)

**Model viết (Fable) chỉ chạm kịch bản ĐÚNG MỘT LẦN — lần VIẾT. Mọi lượt SỬA sau đó là model khác.**

| Vai | Field profile | Model | Chạm `script.txt` khi nào |
|---|---|---|---|
| TÁC GIẢ | `script.brain_model` | Fable 5.1 (hết quota → Opus 5 tạm) | **S2 duy nhất** (2 lượt kỹ thuật: khung + toàn văn; luồng cũ thêm 1 lượt "viết lại nếu ngắn" — vẫn là VIẾT, chưa phải sửa) |
| THỢ VÁ | `script.patch_model` | Opus 5 | **mọi lượt sửa tại chỗ**: S4 lean (theo máy/Sol) · B3S FIX luồng cũ · B3R FIX luồng cũ |
| GIÁM KHẢO khác hãng | `script_qc` (Sol) | GPT-5.6-sol | không chạm — chỉ chấm |
| GIÁM KHẢO cùng hãng (luồng cũ) | `script.final_review_model` | Fable/Opus | không chạm — chỉ chấm; nếu FIX thì THỢ VÁ sửa |
| Máy | — | 0 LLM | S3: 、/outro/marker tự sửa |
| Gemini | — | — | prompt ảnh/phụ đề/dịch, **cấm ghi `script.txt`** |

Lý do: (1) giảm tải quota Fable — Fable gánh cả viết + sửa + B5W là hết hạn mức giữa chừng (dính thật 21/09 cả F lẫn G);
(2) 3 vai độc lập: model tự sửa bài mình có xu hướng bảo tồn lập luận/văn phong của chính nó; (3) đo thật Opus vá ngang Fable
(§0 bảng S4). **Lane mới khai profile PHẢI có đủ `brain_model` + `patch_model`** — thiếu `patch_model` thì code mặc định
= `brain_model` (Fable sửa luôn) → vi phạm quy tắc âm thầm. Code đọc field: `claude_p_bridge.brain_model_of()` /
`patch_model_of()`; các chỗ gọi: `lean_script.patch` · `make_video.b3s_sol` (FIX) · `make_video.b3r_final_review` (FIX).
Ngoài kịch bản, B5W `prompt_doan.py` vẫn dùng `brain_model` (viết prompt ảnh là VIẾT, không phải sửa).

Kiểm tra 2026-09-22: 3 lane `claude_p` (E `kenko-chiebukuro`, F `teinengo-real`, G `teinengo-tanoshimi`) — F/G đã khai
`patch_model`; E dùng alias `opus` cho cả 2 vai (không có Fable nên không vi phạm). Lane Gemini (A/D/satori-ramcloud) không
liên quan; satori não-Claude (`brain_channel.py`) là agent riêng, không qua bảng này.

---

## 1. BẬT LEAN CHO LANE — sửa `profiles/profiles/<mã>.json` (1 lần/lane)

### 1.1 Điều kiện cứng (hàng rào #1) — thiếu là `make_video` DỪNG
- ⛔ **Khối `script.hook` — 4 field, thiếu bất kỳ cái nào là cổng S1L DỪNG.** Copy rồi sửa:
  ```json
  "hook": {
    "enabled": true,
    "visual": "<nguồn hình + cách khoá mặt của RIÊNG lane này, vd manga_ai_ref>",
    "visual_kind": "video_sinh",
    "sfx": true
  }
  ```
  | Field | Luật |
  |---|---|
  | `enabled: true` | hook 20–30 giây đầu là luật MỌI LANE (anh chốt 2026-09-23). Xem §2b. |
  | `visual` | NGUỒN HÌNH + cách khoá mặt, riêng từng lane, **cấm mượn của lane khác** — bảng ở `docs/QUY_TAC_VIDEO_HOOK.md` §5b |
  | `visual_kind: "video_sinh"` | **anh chốt 2026-09-24:** hook là **VIDEO SINH** (Google Flow / Grok Imagine), **KHÔNG còn là video ghép từ ảnh render**. Lane satori đã chạy thật clip Grok (`ep3-sougi`). Muốn ảnh tĩnh/clip stock thì đặt `"anh_tinh"` **và** khai `visual_exception` ghi RÕ LÝ DO — hiện chỉ 2 lane có ngoại lệ chính danh (`toshi-densetsu-jp`, `irogatatarukioku`: bán SỰ THẬT CÓ HỒ SƠ, clip AI phá `credits.txt`) |
  | `sfx: true` | **anh chốt 2026-09-24:** hiệu ứng âm thanh trong hook là **BẮT BUỘC**. ai33 `POST /v1/task/sound-effect`, để `duration_seconds` AUTO |

  > ⚠️ **Hook là video sinh nên KỊCH BẢN PHẢI ĐỔI THEO.** 20–30 giây đầu bị ràng buộc bởi thứ dựng
  > được thành clip 5–6 giây: một chủ thể, một chuyển động tả được bằng lời. Cấm cảnh cần ≥3 nhân vật
  > cùng hành động, cấm đổi bối cảnh giữa một cảnh, cấm chữ/biểu đồ trên hình; và chừa chỗ cho tiếng
  > thật của cảnh, đừng lấp kín 30 giây bằng lời đọc. Luật này được nhồi **tự động** vào prompt của
  > model VIẾT (`qc_goi_dang.khoi_luat_cho_prompt`) nên không phải dặn tay mỗi tập.
- ⛔ **`goi_dang.enabled: true`** + khối `goi_dang` khai ngưỡng **đo từ kênh mẫu CỦA CHÍNH LANE NÀY**
  kèm field `_nguon` — luật gói đăng G1–G8, xem `docs/QUY_TAC_GOI_DANG.md` §3.
  > Hai field trên do **cổng S1L** (`qc_goi_dang.cong_truoc_khi_viet`) chặn, chạy ngay sau S1Q nên
  > trượt là DỪNG **trước khi tốn lượt LLM nào**. Vì sao phải thành cổng: luật hook chốt 2026-09-23
  > và đã viết vào CLAUDE.md, nhưng đo thật ngày **2026-09-24 mới có 3/6 lane bật công tắc** — luật
  > bằng văn bản thì phải có người nhắc mới chạy (anh chốt siết mức này 2026-09-24).
- `voice.char_rate` **đo thật** bằng `calibrate.py` (không mượn lane khác).
- `script.gate` **đo từ transcript kênh mẫu** của chính lane (memory `nguong-gate-phai-do-tu-du-lieu`).
- `script.gate.list_item_count` — dạng list (N選 / countdown 第N位): máy kiểm đủ mục bằng marker `1つ目…`/`第N位`.
  **Lane thuần truyện (không mục, Lane F từ 2026-09-20)**: khai `list_item_count: 0` + `budget.sections` (danh sách chặng
  `{label, ratio}`, tổng ≈1) thay cho `mo_dau/ket` — máy chia ngân sách theo chặng, bỏ kiểm marker; kèm
  `script.fact_exempt_units: ["万円","円"]` nếu số tiền cá nhân (退職金/通帳) là hư cấu (đo thật: không miễn thì S3 bắt 30
  số "không có trong tư liệu" và vòng patch xoá sạch xương sống truyện). Mẫu: `profiles/profiles/teinengo-real.json`.

### 1.2 Khối `script` — copy rồi sửa số
```json
"script": {
  "flow": "lean",
  "budget": { "mo_dau": 0.22, "ket": 0.08, "tol": 0.08,
              "label_mo_dau": "第1〜2幕（フック＋人物＋案内役）",
              "label_ket":    "結び（翌朝＋まとめ＋締めの一言）" },
  "structure": "manga_list",
  "mode": "story",
  "engine": "claude_p",
  "brain_model": "claude-fable-5-1",
  "patch_model": "claude-opus-5",
  "final_review_model": "claude-fable-5-1",
  "outro_line": "ご視聴いただきありがとうございました。…",
  "sol_qc": true,
  "gate": { "list_item_count": 5, "list_order": "auto",
            "hook_marker": ["1つ目", "一つ目", "第5位"], "hook_chars": [1200, 2300],
            "cta_mid": [0.35, 0.70], "…": "các ngưỡng đo từ kênh mẫu" }
}
```
| Field | Ý nghĩa | Đo/chọn thế nào |
|---|---|---|
| `budget.mo_dau` / `ket` | tỉ lệ chữ phần mở đầu / kết; phần còn lại chia đều N mục | đếm chữ TRƯỚC marker mục 1 và SAU mục cuối trên 5–8 transcript kênh mẫu (Lane G: 19–29% / ~8%) |
| `budget.tol` | dung sai ±; lệch hơn → patch nén/nới (tính 1 lượt) | 0.08 mặc định |
| `budget.label_*` | tên phần mở đầu/kết **bằng tiếng Nhật** đưa vào prompt Fable | bỏ = khuôn manga Lane G; lane bác sĩ liệt kê thì ghi vd `導入（問題提起＋自己紹介）` / `まとめ（注意点＋締め）` |
| `structure` | nhánh trong `ai_steps._cau_truc_block` | có sẵn: `manga_list` (G) · `list_countdown` (E) · khối riêng qua `structure_block` (F) — thêm nhánh mới nếu khác hẳn, **không thêm `if profile_id`** |
| `budget.sections` | lane TRUYỆN: chặng + tỉ lệ (thay `mo_dau/ket`, đi cùng `list_item_count: 0`) | đếm chữ từng chặng trên transcript kênh mẫu/tập đã đạt (Lane F: 5/8/22/20/15/20/10%) |
| `fact_exempt_units` | đơn vị số được MIỄN đối chiếu tư liệu ở S3 (số hư cấu có chủ đích) | lane tiền cá nhân: `["万円","円"]`; lane khác bỏ field |
| `patch_model` | model S4 (patch tại chỗ) — tách khỏi `brain_model` (S2) | `claude-opus-5` (chốt 2026-09-22, A/B ngang Fable, giữ quota Fable cho S2); bỏ field = dùng `brain_model` |
| `sol_pass_need` | số lần Sol PASS LIÊN TIẾP trên cùng bản mới khoá | mặc định 2 (Sol không tất định); `1` = tắt (không khuyến nghị) |
| `outro_line` | câu cuối nguyên văn; máy tự thay nếu Fable viết lệch | lấy từ CHANNEL_DNA §CTA (câu lặp ở 8/8 video) |
| `gate.list_order` | `auto` / `ascending` (1つ目…) / `countdown` (第5位→第1位) | kênh mẫu dùng kiểu nào cho dạng bài nào |
| `gate.hook_marker` + `hook_chars` | ranh giới phần mở đầu để đo | marker đầu mục 1 của kênh mẫu |
| `gate.cta_mid` | **luật lane, tuỳ chọn**: phải có 1 câu mời コメント trong khoảng vị trí này (ngoài outro). Máy coi thiếu = VIỆC; Sol được báo để không dời CTA xuống cuối | kênh mẫu có CTA giữa bài thì khai; không có thì **bỏ field** |

### 1.3 Khối `script_qc` — Sol chấm theo lens, PHẢI khai (mặc định là `medical`)
```json
"script_qc": {
  "lens": "plain",
  "domain_focus": "1 câu bối cảnh: video dạng gì, ai kể, cho ai. Đây KHÔNG phải video y khoa.",
  "lane_rules": ["luật riêng khác cần Sol biết để không đề nghị sửa nhầm (tuỳ chọn)"]
}
```
| Lane | `lens` | Ghi chú |
|---|---|---|
| Sức khoẻ (E, Lopezzapa68) | `medical` | **không tắt `sol_qc`**, không đổi lens — anh chốt |
| Manga/kể chuyện/lối sống (F, G, J) | `plain` | hỏi thẳng "đã hợp lý chưa, chỗ nào không hợp lý thì liệt kê để sửa" |
| Phóng tác từ nguồn Hàn (satori) | `story` | |
`domain_focus` là **1 câu bối cảnh**, không phải danh sách rủi ro (Lane G ep01 chạy nhầm lens medical → Sol đòi
gọi 119, sai cổng).

---

## 2. MỖI TẬP — S1 HỒ SƠ (Claude Code làm tay, ~10–15')

Thư mục `assets/<lane>/epNN-<slug>/`, 4 file:

| File | Yêu cầu | Máy kiểm ở S1Q (thiếu = BLOCK, chưa tốn Fable) |
|---|---|---|
| `competitor.txt` | transcript kênh mẫu **cùng dạng đếm** với tập (5選 ↔ 5選, countdown ↔ countdown), ≥3.000 ký tự | độ dài |
| `series_ctx.txt` | khuôn dưới | có ≥1 dòng `[Dn]` · có URL · có `SỐ ĐƯỢC PHÉP:` (không có → cả file làm nguồn số) |
| `title.txt` | 1 dòng tiêu đề đã chốt (trong `gate.title_len`) | chỉ cảnh báo — nhưng thiếu thì Sol không kiểm "lời hứa tiêu đề" (lỗi nặng nhất Sol bắt ở ep01) |
| ⛔ `promise.txt` | **ĐÚNG 1 câu** — lời hứa của tập. Tiêu đề · chữ thumbnail · câu đầu mô tả · 30–45 giây đầu hook đều phải nói lại đúng câu này (nguyên tắc 1) | **S1L: thiếu = BLOCK.** Câu này còn được nhồi thẳng vào prompt của model VIẾT (`qc_goi_dang.khoi_luat_cho_prompt`) để nó viết đúng ngay lần đầu — không có nó thì chỉ còn cách chấm-rồi-sửa, tức thêm lượt Sol + lượt patch cho mỗi tập |

Khuôn `series_ctx.txt` (Lane G ep01 làm mẫu — `assets/teinengo-tanoshimi/ep01-asa-shukan/series_ctx.txt`):
```
SỐ ĐƯỢC PHÉP: 6000歩 · 8000歩 · 65歳 · 1.2L · 6時30分 · 40年      ← MỌI số có đơn vị được xuất hiện; số khác Fable phải nói định tính
TƯ LIỆU THỰC TẾ — <tiêu đề tập> (tra <ngày>, chỉ dùng đúng những dòng dưới)
[D1] <dữ kiện 1 câu, số đúng như nguồn>
  nguồn: <URL> · <URL>
[D2] …
QUY ƯỚC:
- Nhân vật/tình tiết/số tiền cá nhân = hư cấu, không cần nguồn, nhưng hợp lý với persona.
- KHÔNG nêu: tên bác sĩ/đại học/nghiên cứu/thương hiệu/% hiệu quả…
- Gợi ý N mục (cho người viết chọn, không bắt buộc thứ tự): (1)… [D4] · (2)… [D1] · … · mục cuối = cú lật.
```
Quy tắc số: mỗi số trong `SỐ ĐƯỢC PHÉP` phải có ở một `[Dn]`; số ≤12 (số đếm nhỏ) máy bỏ qua; số tiền trong bài mà
có `総額/合計` thì máy cộng lại kiểm (lệch >15% = việc).

**Bài học 10 tập Lane G (nguồn ESCALATE lớn nhất là S1, không phải Fable/Sol):** tiêu đề hứa gì thì `QUY ƯỚC` phải ghi
**BẮT BUỘC** cách trả (夫婦 → cả 5 mục về vợ chồng; 5選 địa điểm → 5 địa danh CÓ TÊN trong [Dn]; 若返る/0円 → câu kết trả thế nào).
Viết "gợi ý" là Fable đi hướng khác và Sol FIX 3 vòng. Tiêu đề kiểu「0円」「1円も使わず」 là quy ước kênh → khai
`script_qc.lane_rules` để Sol không coi tiền tàu là mâu thuẫn.

Ghi sheet tab lane: **C = đường dẫn thư mục tập** ngay khi tạo hồ sơ.

---

### 2b. H1–H4 HOOK 20–30 GIÂY — bắt buộc TRƯỚC S2 (anh chốt 2026-09-23, mọi lane)
`lean_script.run()` tự gọi `hook_stage.ensure_locked()` sau S1Q. Cần thêm trong thư mục tập:
| File | Bắt buộc | Ghi chú |
|---|---|---|
| `competitor.segments.json` | lane nhân bản 1 video | `fetch_script.py` sinh kèm `competitor.txt` (có title/description/thumbnail nguồn) |
| `hook/promise.txt` | khuyến nghị | 4–6 dòng `core_event:/payoff:/reveal:/timeline_start:` — HOOK_STALE so theo file này thay vì hash cả `series_ctx.txt` |
| `thumb_text.txt` | nếu đã có | Sol chấm THUMB_MATCH |
Sinh ra: `hook/source.json` (H1–H3) · `hook_candidates.txt` · `hook_qc.json` · `hook_locked.txt` + `hook_lock.json` (H4) ·
`hook_storyboard.json` + `flow_prompts/` + `grok_jobs.csv`. Storyboard NAY TỰ SINH trong luồng bình thường, không cần gọi
tay: `make_video.py` tự gọi `hook_storyboard.sinh()` ở bước ghi tài sản B5W (`_sinh_hook_storyboard_neu_can()`, ngay sau khi
có `characters.json`, cần continuity nhân vật cho @REF/@REF2); nếu chạy CLI `hook_stage.py` trực tiếp thì lệnh đó cũng tự
gọi luôn `hook_storyboard.sinh()` sau khi khoá xong (Task 12). Lệnh
`py -3.13 pipeline\hook_storyboard.py --profile <lane> --slug <tập> [--force]` giờ CHỈ dùng khi cần **sinh lại tay**
(storyboard cũ lỗi, muốn ép sinh lại, hoặc đang gỡ lỗi riêng bước này).
Lớp 3 (Claude Code) đọc `hook_locked.txt` 2 phút trước khi S2 chạy tiếp: kiểm 4 nhịp + khớp title. Sửa hook = sửa TRƯỚC S2;
sau khi script đã LOCK mà đổi title/thumb/promise → HOOK_STALE chặn ở pha asset (`Job.kiem_lock` gọi `hook_stage.kiem_stale()`),
chạy `py -3.13 pipeline\hook_stage.py --profile <lane> --slug <tập> --force` rồi S2 lại.
⚠️ **Công tắc bật/tắt THEO TỪNG KÊNH, mặc định TẮT** (`hook_stage.MAC_DINH["enabled"] = False`) — kênh nào muốn
dùng hook PHẢI tự khai tường minh `script.hook.enabled: true` trong profile, không có gì tự bật khi vào lean flow.
Kênh chưa khai coi như chưa bật: `lean_script.run()`/`make_video.py`/`qc_final.py` đều đi qua đúng
`hook_stage.is_enabled(prof)` (không tự suy theo tên/`id` kênh) và im lặng chạy như trước khi có tính năng hook.
Field profile đầy đủ (mặc định trong `hook_stage.MAC_DINH`): `script.hook = {"enabled": false, "model": "",
"patterns": [], "closer": "", "ratio_30s":0.5,"tol":0.15,"neo_ratio":0.4,"banned_openers":[...]}` — bật cho lane
thì thêm `"enabled": true`.
`script.hook.model` (2026-09-23, mặc định `""` = dùng `script.brain_model`): ghim model VIẾT riêng cho hook khi cần
khác model viết thân — chỉ áp cho lượt viết 3 phương án (`viet_candidates`), mọi lượt SỬA vẫn dùng `patch_model`.
Từng dùng cho 3 kênh (`teinengo-tanoshimi`/`teinengo-real`/`kenko-chiebukuro`) lúc `brain_model` của các kênh đó tạm là
Opus (Fable hết quota): A/B thật cùng hồ sơ, Opus viết hook vượt trần độ dài cả 3 phương án (259/232/221 chữ, trần
185) → 2 vòng chấm + 2 lượt vá; Fable viết qua cổng ngay lần đầu (1 vòng chấm, 0 lượt vá, hook 158 chữ). 2026-09-23:
cả 3 kênh đổi lại `brain_model = claude-fable-5-1` nên trường này thành thừa (2 nguồn chân lý cho cùng 1 model) —
đã XOÁ khỏi 3 profile trên; field vẫn tồn tại trong code cho kênh nào SAU NÀY brain_model khác Fable mà muốn hook
riêng vẫn dùng Fable.

`script.hook.patterns` (danh sách id) và `script.hook.closer` (1 id) — nối **KHO KIỂU HOOK** của dự án nghiên cứu
`E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\patterns.json` (23 kiểu mở đầu H01–H23 + 12 thiết bị khoá hook K01–K12, đo từ video
thật, bản người đọc `HOOK_LIBRARY.md`) thẳng vào `PROMPT_VIET` — model chọn 1 kiểu/phương án và bám đúng khuôn +
điều cấm của kiểu đó, thay vì chỉ có 4 nhịp chung chung. Không khai (mặc định `[]`/`""`) = prompt y hệt trước khi có
2 field này, không thêm dòng nào. Kho nằm ở DỰ ÁN KHÁC nên thiếu/hỏng file chỉ in 1 dòng cảnh báo (`hook_stage.doc_kho_hook`),
KHÔNG chặn pipeline. Bảng "kênh của mình → kiểu hook nên dùng" nằm trong `HOOK_LIBRARY.md` (cột `lanes_fit` của mỗi
kiểu); ví dụ đã bật: `satori-jp-obaa` dùng `patterns: ["H22","H23"]` + `closer: "K12"` (khớp DNA 15/15 video của
kênh mẫu @simbot2, xem `_hook_note` trong `profiles/profiles/satori-jp-obaa.json`).
Tập đã có script (chưa đăng): `py -3.13 pipeline\hook_stage.py --profile <lane> --slug <tập> --mode repair` — không đụng script/voice/img;
bước 3 dựng `hook_final.mp4` + `final_with_hook.mp4` theo `docs/GIAO_VIEC_BUOC3_AGENT.md` §9.

---

## 3. CHẠY (1 lệnh, ~3–20' máy)
```
py -3.13 -X utf8 pipeline\make_video.py --profile <mã lane> --slug epNN-<slug> --den B3G
```
Log đọc theo nhãn:
```
[S1Q] ✓ hồ sơ đủ · ngân sách 6,474 chữ = mở đầu 1,424 + 5×906 + kết 517 (±8%)
[S2]  Fable viết đúng ngân sách …            (2 lượt: khung + viết; ~7')
[S3]  6,580 chữ ≈ 20.3' · phẩy/câu 1.2 · hơi 11 · thoại 27%  [FACT]… [LEN/STRUCT]… (warn)…
[S4]  patch máy (nen|noi|sua) …               chỉ khi S3 có việc
[S5]  Sol lần 1 (lens plain) …                → PASS | FIX → [S4] patch theo Sol → [S3] → [S5] lần 2 …
[LOCK] ✓ Sol PASS lần k · N chữ · sha xxxxxxxxxx · n patch · m'ss · KHÔNG AI SỬA script.txt NỮA
```
Kết thúc **chỉ có 3 trạng thái** (ghi `script.lock.json`):

| state | Khi nào | Việc tiếp |
|---|---|---|
| `PASS` | Sol PASS và S3 sạch ở cùng bản | → §4 lớp 3 |
| `ESCALATE` | hết 2 patch vẫn FIX · Sol REMAKE · patch bị từ chối 2 lần · S3 không nắn được | đọc `ESCALATION_REPORT.md` + `qc_sol_report_k.txt` → §4 xử theo kênh `viec_tay.txt`; pha asset BLOCK |
| `BLOCK` | S1Q thiếu hồ sơ · hạ tầng (Sol/Fable lỗi) | bổ hồ sơ / sửa hạ tầng, chạy lại; chưa tốn lượt viết |

Chạy lại khi đã có `script.txt` + lock: lean **dùng lại bản có sẵn** (không viết lại từ đầu), đi thẳng S3 → Sol.
Muốn viết lại hẳn từ đầu (bỏ bản cũ + lock): thêm `--force-qc` (cùng cờ này cũng bỏ qua lock PASS và không dừng ở ESCALATE — chỉ dùng khi cố ý).

---

## 4. LỚP 3 — CLAUDE CODE ĐỌC BẢN KHOÁ (bắt buộc, ~5')
Máy + Sol chưa phải "đã duyệt". Đọc **toàn bộ** `script.txt` sau LOCK (không chỉ phần đổi), đối chiếu:
1. `series_ctx.txt`: dữ kiện có bị diễn giải sai ý không (số đúng nhưng nghĩa đảo — vd 6000/8000歩 ai là ai).
2. **Luật lane** mà Sol không biết (CTA giữa, hướng vui/rẻ, cấm chủ đề trừu tượng, disclaimer…) — xem `_note` profile
   + handoff của lane.
3. Câu bám gốc kênh mẫu (S3 chỉ WARN bigram): đọc `do.json → warn`, câu nào >60% trùng thì đổi cách nói.
4. Tiêu đề có được trả trong bài; mục cuối có "cú lật"/payoff.
5. Đạo cụ/tình tiết mới sinh sau patch (mỗi patch có thể sinh lỗi ở chỗ khác — rủi ro #3 đã xảy ra thật ở ep02).
6. **Địa danh/số MỚI Fable đưa vào khi patch** mà không có trong `series_ctx` (ep10: 城崎温泉 800円 — số trùng `SỐ ĐƯỢC PHÉP` nên máy không bắt): tra nguồn chính thức; đúng → bổ [Dn] vào `series_ctx.txt` (không đổi script); sai → `viec_tay.txt`.

**Có lỗi → KHÔNG sửa `script.txt`** (sha lệch = `FINAL_QC_STALE`, mọi bước sau dừng). Làm đúng kênh:
```
# 1 dòng / việc, trích câu để Fable tìm đúng chỗ
echo "- Câu「…」bám gốc 73% → đổi cách nói, giữ ý" >> assets/<lane>/epNN/viec_tay.txt
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,'pipeline');import gate_common;from pathlib import Path;gate_common.ghi_lock(Path('assets/<lane>/epNN'),'ESCALATE',reason='lop3: 2 loi lane')"
py -3.13 -X utf8 pipeline\make_video.py --profile <mã> --slug epNN --den B3G      # việc vào vòng patch → S3 → Sol → LOCK mới
```
`viec_tay.txt` đọc 1 lần rồi đổi tên `.done.txt`. ESCALATE do máy sinh cũng xử y vậy: đọc báo cáo → viết việc cụ thể
vào `viec_tay.txt` → chạy lại. Chỉ hỏi anh khi lỗi là **thiết kế/phạm vi** (đề tài không đủ tư liệu, tiêu đề hứa điều
không thể trả…) — hỏi bằng 1 quyết định cụ thể.

---

## 5. GHI KẾT QUẢ — sheet tab lane, cột KỊCH BẢN (D)
**Anh chốt 2026-09-20: xong tập nào ghi đúng chữ `Done`. Không dài dòng, không sha, không "chờ anh duyệt".**

| Ô D | Khi nào |
|---|---|
| `Done` | lock PASS **và** lớp 3 đọc xong không còn việc |
| `escalate` | lớp 3 kết luận cần anh quyết (kèm 1 câu lý do ở cột K) |
| `block` | thiếu hồ sơ/hạ tầng, ghi thiếu gì ở K |

Số đo chi tiết đã có sẵn trong `bench.jsonl` + `script.lock.json` của tập, không chép lên sheet.

---

## 6. SAU KHOÁ — luật `NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS`
- Mọi bước sau (B5W prompt ảnh, B5P, B7, drive_handoff…) gọi `gate_common.kiem_lock()`: không lock / state ≠ PASS /
  sha lệch → `FINAL_QC_STALE` **FAIL** (lane lean) hoặc WARN (lane cũ không có lock).
- Muốn đổi 1 chữ sau khoá → §4 (`viec_tay.txt` + ESCALATE + chạy lại), không có đường khác.

---

## 7. FILE SINH RA TRONG THƯ MỤC TẬP
`script.txt` (master) · `script_pass1_raw.txt` (bản Fable thô) · `script.pre_patchN.txt` · `do.json` (S3 lần cuối) ·
`qc_sol_report_k.txt` · `script.lock.json` · `bench.jsonl` (1 dòng/lần chạy) · `ESCALATION_REPORT.md` (khi có) ·
`viec_tay.done.txt`.

---

## 8. BENCHMARK & KHI NÀO SỬA QUY TRÌNH
Mỗi tập 1 dòng `bench.jsonl`: `fable_calls · sol_calls · patch_count · final_char_deviation · final_state ·
total_time_s`. Tiêu chí thắng (10 tập/lane): ≥80% PASS với 0–1 patch · median ≤20' · |deviation| ≤8% ở ≥70% tập ·
0 ca STALE. Không đạt → **sửa prompt writer/patch trong `lean_script.py`**, không thêm model, không đưa Gemini nén
trở lại. Lane G sau 2 tập: S2 viết đúng ngân sách +1,6%; mỗi patch Fable +100–300 chữ → bản cuối +10–11%.

## 9. LỖI ĐÃ GẶP → CÁCH XỬ (đừng dính lại)
| Triệu chứng | Nguyên nhân | Xử |
|---|---|---|
| Sol FIX 7→6→4 không bao giờ PASS | lens không có sàn mức độ | đã thêm [NẶNG]/[VỪA]/[NHẸ]; PASS = 0 NẶNG & <3 VỪA |
| Sol đòi triệu chứng/119 cho manga | lens mặc định `medical` | khai `script_qc.lens` (§1.3) |
| Sol dời CTA xuống cuối | Sol không biết luật lane | `gate.cta_mid` + `script_qc.lane_rules` |
| 110×4=600円 lọt 2 vòng Sol | LLM không cộng | máy `_tong_tien` bắt; S1 ghi đủ số vào `SỐ ĐƯỢC PHÉP` |
| 七千五百歩 không bị bắt | FACT chỉ đọc số Ả Rập | `kanji_to_int` — đã vá |
| Bản viết tốt bị vứt vì 1 dấu 、 | gate trước tự gỡ | S3 tự gỡ 、 và tự thay outro, không tính lỗi |
| Chạy lại viết lại từ đầu, mất bản đã sửa | không có lock | lean dùng lại `script.txt` khi có lock; `--force-qc` mới viết lại |
| Cột D dài dòng / "chờ anh duyệt" | đẩy việc lên anh | §5: `Done` |
| Bản đã LOCK PASS vẫn còn lỗi timeline [NẶNG] (ep10 G) | Sol không tất định — 1 lần PASS có phần may | `sol_pass_need`=2: khoá chỉ khi PASS 2 lần liên tiếp; đừng kết luận model patch kém chỉ vì 1 lần Sol FIX |
| Fable hết quota giữa chừng (`You've reached your Fable limit`) | 1 model gánh cả S2+S4+B5W | S4 = Opus 5 qua `patch_model`; Fable chỉ giữ S2 |
