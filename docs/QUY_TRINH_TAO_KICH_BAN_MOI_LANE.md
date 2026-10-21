# QUY TRÌNH TẠO KỊCH BẢN — ÁP DỤNG CHO MỌI LANE (`script.flow = "lean"`)

Chốt 2026-09-20 sau 2 tập Lane G đo thật (`docs/QUY_TRINH_KICH_BAN_GON.md` = thiết kế + số đo; file này = **hướng dẫn
làm**). Đọc file này là đủ để một lane bật luồng mới; không cần đọc thiết kế.

> **Một câu:** Fable viết đúng ngân sách → máy đo tất định → Sol chấm tính hợp lý (lời cuối) → Fable patch ≤2 lần,
> mỗi patch chạy lại máy + Sol → PASS thì khoá SHA256, **không ai sửa `script.txt` nữa** → Claude Code đọc bản khoá →
> giao máy 3 → … → giao máy 2 (cột D theo `docs/TRANG_THAI_COT_D_K.md`).

---

## 00. ⭐ QUY TRÌNH CHUẨN CHO MỌI LANE — MẪU = LANE M `teinengo-anaba` (anh chốt 2026-09-29)

**Luật cứng:** mọi lane mới BẮT BUỘC theo đúng quy trình này. Anh nói **"thực hiện kênh/lane ABC"** cho kênh mới →
Claude Code áp NGUYÊN quy trình dưới đây, KHÔNG hỏi lại từng bước, KHÔNG tự đổi model. Muốn đổi bước/model = anh phải nói.
**Khi mục này mâu thuẫn với phần còn lại của file (§0, §0a, §4c…) thì mục này THẮNG.**

> ⭐ **SỬA 2026-09-30 (anh chốt):** (a) H4 = **Fable 5.1 viết 2 phương án hook** (`script.hook.model: "claude-fable-5-1"`,
> `hook.so_ung_vien` mặc định 2) → máy đo → Sol chọn 1 → Opus 5 vá, FIX lần 3 = đạt; **KHÔNG khớp tiêu đề ở bước hook**
> (`hook.khop_tieu_de` mặc định false — tiêu đề làm SAU khi kịch bản xong). (b) Viết xong + LOCK → **DỪNG, giao máy 3/anh soát**
> (`script.soat: "may3"`), TẮT soát ChatGPT web; bỏ lớp 3 đọc bản khoá trước khi gửi. (c) Anh sửa thẳng `script.txt` trong
> `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\<tab>\<slug>\script.txt` (thư mục job chung chỗ giao máy 2, không còn `review\`; hook = đoạn đầu) → tab mới nhận + làm tiếp theo
> **`E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`** (hook khoá lại từ đoạn đầu → ảnh + clip hook theo bản anh sửa).

**Cách dựng lane mới:** copy `profiles/profiles/teinengo-anaba.json` → sửa `id`, giọng, `structure_block`, `gate` (đo từ kênh mẫu
của CHÍNH lane), `script_qc.lane_rules`, `soat_gptweb.{urls,projects,boi_canh,cau_truc,rang_buoc}`, `image.*`. **GIỮ NGUYÊN** các field
model/luồng ở bảng dưới. Rồi viết `docs/BAT_DAU_LANE/<mã>.md` + SOP riêng (CLAUDE.md chỉ thêm 1 dòng router).

| # | Bước | Ai / model | Field profile |
|---|---|---|---|
| 1 | Hồ sơ tập: `competitor.txt` · `series_ctx.txt` · `title.txt` · `promise.txt`; đọc `COMMENT_INSIGHT.md` | Claude Code (tab lane), tay | — |
| 2 | S1Q + S1L: kiểm hồ sơ, hook, gói đăng | Máy (0 LLM) | `hook.enabled`, `goi_dang.enabled` |
| 3 | H1–H3 phân tích hook video gốc | Đọc chữ **Opus 5** · nhìn khung hình **GPT-5.6-sol** | `hook.analysis_model` (vắng = Opus 5) |
| 4 | H4 viết **2** phương án hook → máy đo → Sol chọn 1 (không xét tiêu đề) → Opus 5 vá (FIX×3 = đạt) → khoá | **Fable 5.1** viết · Sol chấm · Opus 5 vá | `hook.model: "claude-fable-5-1"` · `hook.so_ung_vien` (vắng=2) · `hook.khop_tieu_de` (vắng=false) |
| 5 | **S2 viết kịch bản** (khung + toàn văn, `two_pass`) — chỉ 1 lần | **Fable 5.1** `claude-fable-5-1` (anh chốt 05/10 — không dùng Opus để viết) | `script.brain_model` |
| 6 | S3 đo tất định (độ dài, số liệu↔`SỐ ĐƯỢC PHÉP`, 、, marker, CTA giữa, kết cảm ơn, tổng tiền) | Máy (0 LLM) | `script.gate`, `budget` |
| 7 | S4 vá tại chỗ (≤2 lượt) | **Opus 5** `claude-opus-5` | `script.patch_model` |
| 8 | S5 Sol chấm | **TẮT** (`sol_qc:false`). Thay bằng **S5L kiểm NHẸ lời hứa tiêu đề** (`pipeline/qc_loi_hua.py`): 1 lượt chấm **GPT-5.6-sol** (9router → ns24 → hhtech), cả 3 chết → **Gemini 3.8 flash** (ramclouds → ns24 → deepseek); có lỗi → **Opus 5** vá ĐÚNG 1 lần (ngoài trần MAX_PATCH) → S3 → khoá. Không lặp, không ESCALATE; vá làm S3 trượt thì giữ bản trước; hạ tầng chết thì khoá không có bước này (log "chưa kiểm"). Mỗi bản (sha) chỉ kiểm 1 lần (`loi_hua_da_kiem.json`); việc ghi ở `loi_hua_tieu_de.txt` | `script.sol_qc: false` · `script.kiem_loi_hua` (vắng = BẬT) |
| 9 | LOCK SHA256 → **DỪNG**, tự chép ĐÚNG `script.txt` vào `jobs\<tab>\<slug>\` + cột D = `Chờ kiểm tra kịch bản` (dòng 2 = đường dẫn) | Máy | `script.soat: "may3"` |
| 10 | Anh/máy 3 sửa thẳng `jobs\<tab>\<slug>\script.txt` (hook = đoạn đầu, không cần báo cáo) → cột D = `Đã sửa kịch bản` | Anh | — |
| 11 | ~~Soát ChatGPT web / lớp 3~~ — **TẮT từ 30/09** (chỉ khi anh nói: `soat:"gptweb"`, §4b) | — | — |
| 12 | Tab mới: `review_may3.py --nhan` → hook khoá lại từ đoạn đầu → theo `docs\NHAN_KICH_BAN_MAY3.md` | Claude Code | — |
| 13 | B5W prompt ảnh theo đoạn | **Opus 5** | `image.prompt_model` (vắng = Opus 5) |
| 14 | Hook: storyboard → ảnh hook → clip Grok → **clip hook xem thử có giọng + phụ đề Việt** (`xem_thu_hook_giong.py`) → `duyet_hook.py --gui` (D=`Chờ duyệt hook`) → DỪNG · anh duyệt (D=`Đã duyệt hook`) → `duyet_hook.py --nhan` → `dong_goi_may2.py --job` → D=`Đã giao máy 2` + K=lệnh máy 2, H=cần ảnh (03/10) | `brain_model` (Fable 5.1) · Flow Tool · Grok | `body.chan_buoc2_may1: true` (máy 1 CẤM chạy B4/B5) |

Bắt buộc khai đủ trong profile lane mới: `flow:"lean"` · `engine:"claude_p"` · `brain_model:"claude-fable-5-1"` · `patch_model:"claude-opus-5"` ·
`final_review_model:"claude-opus-5-5"` · `sol_qc:false` · `sol_pass_need:2` · `soat:"may3"` · `hook{enabled,visual,visual_kind:"video_sinh",sfx:false,nhac_nen:true,model:"claude-fable-5-1"}` ·
`goi_dang.enabled:true` · `script_qc{lens,domain_focus,lane_rules}` · `body.chan_buoc2_may1:true`.
Không khai `review_may3:false` (máy 3 là đường mặc định từ 30/09, §4c).
Ngoại lệ chính danh (KHÔNG áp bảng này): `satori-jp-obaa` (não riêng, `review_may3:false`).

⚠️ **Hệ quả của `sol_qc:false`:** không còn vòng Sol chấm toàn diện — lỗi nhân quả/timeline/động cơ chỉ còn S3 (máy, chỉ bắt lỗi
đếm được) + bước 10 (ChatGPT web) + bước 12 (Claude Code) bắt; riêng LỜI HỨA TIÊU ĐỀ có S5L (bước 8). Anh chốt 2026-09-29: truyện
manga giải trí không cần chặt như y khoa — 3 loại lỗi Sol từng bắt (dòng thời gian, hook bị kể lại, câu Nhật chưa tự nhiên) coi là nhẹ.
Vì vậy **bước 10 và 12 KHÔNG được bỏ**. Đo 2026-09-29 (ep02/ep03 Lane M): Sol bắt cả 2 ca tự-phủ-định tiêu đề, Gemini 3.8 flash chỉ bắt
ca ep03 và bỏ sót ep02 3/3 lần → Sol đứng đầu, Gemini chỉ là lưới rơi.
`lane_rules` viết cứng quá vẫn gây vòng lặp ở lane có Sol (bài học Lane M ep01); ở lane tắt Sol nó chỉ còn vào prompt soát GPT web.

---

## 0. AI LÀM GÌ

| Việc | Ai | Ghi chú |
|---|---|---|
| S1 hồ sơ tập: `competitor.txt` · `series_ctx.txt` · `title.txt` | **Claude Code (tab lane)** — tay | việc duy nhất tốn đầu người trước khi bấm chạy |
| S2 viết khung + viết toàn văn ĐÚNG NGÂN SÁCH | **Fable 5.1** (anh chốt 2026-10-05; 29/09–04/10 là Opus 5.5) | model duy nhất được chạm `script.txt` |
| S3 đo tất định: độ dài · phẩy/hơi/thoại · dấu 、(tự gỡ) · N mục có marker · outro (tự thay nguyên văn) · CTA giữa (nếu lane khai) · số liệu ↔ `SỐ ĐƯỢC PHÉP` (cả kanji) · phép cộng tổng tiền · tên↔tuổi nhất quán · đoạn trùng · bám gốc (WARN) | **Máy** (0 LLM) | máy kiểm hết những gì máy kiểm được — Sol không phải đếm chữ |
| S5 ⛔ **TẮT từ 2026-09-29 (`sol_qc:false`, mọi lane) — bỏ qua, khoá PASS sau S3**; mô tả dưới chỉ còn giá trị lịch sử/khi anh bật lại. Chấm tính hợp lý/hợp lệ: nhân quả · dòng thời gian · động cơ · câu Nhật lạ · lời hứa tiêu đề · thứ máy mù | **GPT-5.6-sol** (9router local) | lens theo lane (§1.3); PASS = 0 [NẶNG] và <3 [VỪA]; **khoá chỉ khi PASS 2 lần LIÊN TIẾP cùng bản** (`sol_pass_need`, 2026-09-22 — Sol không tất định: bản ep10 Lane G đã LOCK PASS chấm lại 2/2 ra FIX với lỗi timeline [NẶNG] thật) |
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
Ngoài kịch bản (anh chốt 2026-09-26): **B5W** `prompt_doan.py` (prompt ảnh theo đoạn) = **Opus 5** qua `claude_p_bridge.prompt_model_of()` (field `image.prompt_model`, vắng = `claude-opus-5`) — dành hạn mức Fable (tính riêng) cho S2. **Kịch bản quay hook** `hook_storyboard.py` GIỮ **Fable** (`brain_model`) vì quan trọng. **H1–H3** phân tích hook video gốc: đọc chữ = **Opus** (`script.hook.analysis_model`, vắng = `claude-opus-5`, claude -p lỗi thì rơi về Gemini), nhìn khung hình = **GPT-5.6-sol** (lỗi thì rơi về thang Gemini).

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
    "sfx": false,
    "nhac_nen": true
  }
  ```
  | Field | Luật |
  |---|---|
  | `enabled: true` | hook đầu video là luật MỌI LANE (anh chốt 2026-09-23); độ dài ≈ hook video gốc (kẹp `script.hook.giay`). Xem §2b. |
  | `visual` | NGUỒN HÌNH + cách khoá mặt, riêng từng lane, **cấm mượn của lane khác** — bảng ở `docs/QUY_TAC_VIDEO_HOOK.md` §5b |
  | `visual_kind: "video_sinh"` | **anh chốt 2026-09-24:** hook là **VIDEO SINH** (Google Flow / Grok Imagine), **KHÔNG còn là video ghép từ ảnh render**. Lane satori đã chạy thật clip Grok (`ep3-sougi`). Muốn ảnh tĩnh/clip stock thì đặt `"anh_tinh"` **và** khai `visual_exception` ghi RÕ LÝ DO — hiện chỉ 2 lane có ngoại lệ chính danh (`toshi-densetsu-jp`, `irogatatarukioku`: bán SỰ THẬT CÓ HỒ SƠ, clip AI phá `credits.txt`) |
  | `sfx: false` + `nhac_nen: true` | **anh chốt 01/10/2026 (thay luật 24/09):** CẤM hiệu ứng âm thanh đồ vật; hook chỉ có NHẠC NỀN. Chi tiết: `docs/QUY_TAC_HOOK_DAI_VA_NHAC_NEN.md` |

  > ⚠️ **Hook là video sinh nên KỊCH BẢN PHẢI ĐỔI THEO.** Lời hook bị ràng buộc bởi thứ dựng
  > được thành clip 5–6 giây: một chủ thể, một chuyển động tả được bằng lời. Cấm cảnh cần ≥3 nhân vật
  > cùng hành động, cấm đổi bối cảnh giữa một cảnh, cấm chữ/biểu đồ trên hình; và chừa chỗ cho tiếng
  > thật của cảnh, đừng lấp kín hook bằng lời đọc. Luật này được nhồi **tự động** vào prompt của
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
  "the_viet": "~/.claude/skills/youtube-kich-ban/market/THE_VIET_STORY.md",
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
| `the_viet` | **BẮT BUỘC mọi lane (anh chốt 05/10/2026, cổng S1L chặn nếu thiếu)** — thẻ viết VIRAL_LAB (luật anh sửa tay + số liệu thị trường, VIRAL_LAB ghi đè mỗi ngày, h2dev CẤM sửa) chèn vào prompt Fable hook + S2 | lane truyện → `THE_VIET_STORY.md` · lane giải thích → `THE_VIET_INFO.md` · lane danh sách → `THE_VIET_LIST.md` (cùng thư mục `~/.claude/skills/youtube-kich-ban/market/`) |
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
| ⛔ `promise.txt` | **ĐÚNG 1 câu** — lời hứa của tập. Tiêu đề · chữ thumbnail · câu đầu mô tả đều phải nói lại đúng câu này; lời đọc phải nói được lời hứa **trước khi hết hook đã khoá** (17/10: cửa sổ giây G1/G2/G3 tự kéo tới hết hook — hook dài theo hook video gốc, `qc_goi_dang.cau_hinh_tap`; thiếu câu mâu thuẫn/câu nghi thức chỉ còn cảnh báo) | **S1L: thiếu = BLOCK.** Câu này còn được nhồi thẳng vào prompt của model VIẾT (`qc_goi_dang.khoi_luat_cho_prompt`) để nó viết đúng ngay lần đầu — không có nó thì chỉ còn cách chấm-rồi-sửa, tức thêm lượt Sol + lượt patch cho mỗi tập |

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

### 2a. ĐỌC BÌNH LUẬN THẬT TRƯỚC KHI VIẾT (anh chốt 2026-09-26, mọi lane)
Bình luận dưới video kênh mẫu = góp ý/phản ánh THẬT của người xem. Bắt buộc đọc TRƯỚC khi viết `series_ctx.txt`/QUY ƯỚC:
1. **Một lần cho mỗi kênh** — dữ liệu do dự án TRENDING-RESEARCH tải sẵn ở `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\<kênh>\comments.json`
   (+ `channel.json`). Gom thành file đọc nhanh (0 LLM, xếp theo lượt thích, nhãn thô):
   `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\<kênh> --profile <lane>`
   → `<channel_dna_dir>\COMMENTS_TOP.md`. Rồi Claude Code ĐỌC nguyên văn và viết tay `<channel_dna_dir>\COMMENT_INSIGHT.md`:
   video nào nổ + vì sao · khán giả giận/thương cái gì · chuyện thật họ kể · lỗi dữ kiện họ bắt · góp ý sản xuất · và khối
   **`## ĐƯA VÀO PROMPT`** (≤8 gạch đầu dòng, tiếng Việt, trích tiếng Nhật kèm dịch) — `lean_script.khoi_them()` tự nhồi khối này
   vào prompt S2 của MỌI tập lane đó. Mẫu đã làm: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\COMMENT_INSIGHT.md`
   (Lane K) · `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\shakai-no-naze\COMMENT_INSIGHT.md` (Lane L).
2. **Mỗi tập** — đọc bình luận của đúng video gốc tập này trong `COMMENTS_TOP.md` (hoặc `comment_insight.json` nếu B2b đã chạy
   với URL nguồn; nay lean cũng đưa file này vào prompt). Dùng để: (a) **chọn video gốc** — video ít view/0 bình luận là nguồn
   yếu (L ep04 nhân bản video 2.324 view, 0 bình luận — yếu nhất kênh); (b) lỗi dữ kiện khán giả đã bắt ở bản gốc → ghi vào
   QUY ƯỚC để không lặp lại; (c) chuyện thật khán giả kể → nguyên liệu chi tiết đời thường (không chép nguyên văn, không nêu tên).
3. Bỏ qua bình luận chính trị/kỳ thị — không đưa quan điểm đó vào kịch bản.

### 2c. CUNG CẢM XÚC — kịch bản phải làm người xem NHỚ (anh chốt 2026-09-26)
Nhẹ nhàng, khô khan = không ai để ý. Bằng chứng đo thật: Lane K kênh mẫu video gây giận nhất 307.286 view vs nhẹ nhất 20.261;
Lane L chủ đề có phe để giận 431.117 view vs chủ đề ngẫm nhẹ 1.026–5.075 view; bình luận top toàn là giận nhân vật, cuối video
chuyển sang thương cảm + chép lại câu đạo lý. Luật (text đầy đủ ở `lean_script.CUNG_CAM_XUC`, tự nhồi vào prompt S2):
| Nhịp | Vị trí | Việc |
|---|---|---|
| 1 KÍCH | sau hook → ~40% (hook KHÔNG theo cung này — viết theo luật hook 17/10) | người xem hưng phấn/giận/ức chế THẬT: kẻ gây chuyện đáng ghét qua hành vi + lời nói cụ thể; người tử tế chịu thiệt có tên, có cái giá cụ thể; bất công leo thang ≥3 nấc; người có quyền đứng sai phe/làm ngơ; KHÔNG giải toả sớm, người kể KHÔNG biện hộ |
| 2 GIẢI TOẢ | ~40–85% | đảo chiều bằng sự thật + hệ quả tự nhiên (quy định, cơ chế, thời gian) — hả dạ nhưng không ai trả thù/mắng/hả hê |
| 3 VỊ THA | ~10% cuối | đổi góc nhìn: kẻ gây chuyện cũng đáng thương, hoặc người bị hại bao dung; chốt 1 câu đạo lý ngắn, sắc, đáng chép lại |
| 4 KẾT CẢM ƠN (anh chốt 2026-09-26) | 1–3 câu CUỐI | SAU câu đạo lý: cảm ơn người xem đã quan tâm xem hết video + xin 1 lượt thích (高評価) + đăng ký kênh (チャンネル登録); lane có `outro_line` thì outro vẫn là câu cuối, lời cảm ơn đứng ngay trước. **(01/10) CTA CHỈ 1 LẦN DUY NHẤT ở cuối** — cấm CTA giữa bài/2 đoạn CTA; outro đã xin 高評価/チャンネル登録 thì model KHÔNG viết thêm; máy tự xoá câu CTA thừa (`lean_script._cta_mot_lan`) |
Cường độ đến từ CHI TIẾT, không từ chửi bới/bạo lực/thô tục. Cung này PHỦ LÊN cấu trúc chặng của lane, không thay.
Nhịp 4 máy kiểm tất định ở S3 (`lean_script._ket_thieu`: 15% cuối bài phải có đủ ありがとう/感謝 · 高評価/いいね · チャンネル登録,
thiếu = việc `KẾT THIẾU` cho patch_model). Field `script.cam_on_cuoi` (vắng = theo `cung_cam_xuc`) — lane nào đã có outro
chỉ xin đăng ký mà không cảm ơn (vd Lane L) sẽ được patch thêm câu cảm ơn ngay trước outro.
Field `script.cung_cam_xuc` — **vắng = BẬT** (lane mới tự có); satori/E/A/D khai `false` (để nguyên). Sol được báo trong
`extra_note` rằng độ gắt nửa đầu là CỐ Ý (không đề nghị làm dịu), chỉ bắt khi phi lý/không nhất quán.
Lớp 3 (đọc bản khoá) kiểm thêm: nửa đầu có thật sự làm mình bực không · có câu đạo lý đáng nhớ ở kết không.

---

### 2b. H1–H4 HOOK — bắt buộc TRƯỚC S2 (anh chốt 2026-09-23, mọi lane)
> ⛔ **LUẬT VIẾT:** Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.
> H1–H3 nay tách **sườn hook gốc** (`cau_truc_hook` trong `hook/source.json`); H4 viết cùng 1 sườn; Sol chấm BAM_SUON/DONG_CO_CHINH….
**2026-09-26 — nguồn H1–H3 không còn rỗng âm thầm:** tập không có `competitor.segments.json` thì `hook_stage._nguon_tu_video_goc()` lấy mã video từ `video_goc.json`, đọc lời có mốc thời gian ở bản TRENDING-RESEARCH đã tải (`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\<kênh>	ranscripts\<id>.json`, không mạng), không có thì tải mạng (api → phụ đề yt-dlp), cache `hook\source_segments.json` (không cache khi rỗng lời). Trước bản vá 4/6 tập gần nhất ra phân tích rỗng.
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
Lớp 3 (Claude Code) đọc `hook_locked.txt` 2 phút trước khi S2 chạy tiếp: kiểm hook có bám cấu trúc hook gốc (cách mở, thứ tự nhịp, độ dài ≈ gốc; lệch nhẹ cho hợp/hay hơn là được) — KHÔNG xét khớp tiêu đề. Sửa hook = sửa TRƯỚC S2;
sau khi script đã LOCK mà đổi title/thumb/promise → HOOK_STALE chặn ở pha asset (`Job.kiem_lock` gọi `hook_stage.kiem_stale()`),
chạy `py -3.13 pipeline\hook_stage.py --profile <lane> --slug <tập> --force` rồi S2 lại.
⚠️ **Công tắc bật/tắt THEO TỪNG KÊNH, mặc định TẮT** (`hook_stage.MAC_DINH["enabled"] = False`) — kênh nào muốn
dùng hook PHẢI tự khai tường minh `script.hook.enabled: true` trong profile, không có gì tự bật khi vào lean flow.
Kênh chưa khai coi như chưa bật: `lean_script.run()`/`make_video.py`/`qc_final.py` đều đi qua đúng
`hook_stage.is_enabled(prof)` (không tự suy theo tên/`id` kênh) và im lặng chạy như trước khi có tính năng hook.
Field profile đầy đủ: xem `hook_stage.MAC_DINH`; field luật viết hiện hành = `script.hook.huong_dan_cau_truc` (file lane) · `giay` [min,max] ·
`giay_mac_dinh` · `so_ung_vien` (`E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md` §2). Bật cho lane thì thêm `"enabled": true`.
`script.hook.model` (2026-09-23, mặc định `""` = dùng `script.brain_model`): ghim model VIẾT riêng cho hook khi cần
khác model viết thân — chỉ áp cho lượt viết 3 phương án (`viet_candidates`), mọi lượt SỬA vẫn dùng `patch_model`.
Từng dùng cho 3 kênh (`teinengo-tanoshimi`/`teinengo-real`/`kenko-chiebukuro`) lúc `brain_model` của các kênh đó tạm là
Opus (Fable hết quota): A/B thật cùng hồ sơ, Opus viết hook vượt trần độ dài cả 3 phương án (259/232/221 chữ, trần
185) → 2 vòng chấm + 2 lượt vá; Fable viết qua cổng ngay lần đầu (1 vòng chấm, 0 lượt vá, hook 158 chữ). 2026-09-23:
cả 3 kênh đổi lại `brain_model = claude-fable-5-1` nên trường này thành thừa (2 nguồn chân lý cho cùng 1 model) —
đã XOÁ khỏi 3 profile trên; field vẫn tồn tại trong code cho kênh nào SAU NÀY brain_model khác Fable mà muốn hook
riêng vẫn dùng Fable.

~~`script.hook.patterns` / `script.hook.closer` (KHO KIỂU HOOK `HOOK_LIBRARY`)~~ — KHÔNG còn là luật viết hook (17/10/2026); hook (21/10) bám sát cấu trúc hook video gốc của tập.
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

## 4b. SOÁT KỊCH BẢN BẰNG CHATGPT WEB — ⏸ TẮT từ 2026-09-30 (chỉ khi anh nói `soat:"gptweb"`; mặc định nay là máy 3 §4c)
Field `script.soat`: `"gptweb"` (vắng = gptweb) | `"may3"` (§4c, chỉ khi anh nói). Không chép sang máy 3, KHÔNG ghi sheet giữa chừng
(cột D = `Đã giao máy 2` do `dong_goi_may2.py --job` ghi khi giao máy 2).
1. `make_video.py --den B3G` khoá xong thì **DỪNG** và in 3 lệnh dưới.
2. `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\soat_kb_gptweb.py --profile <lane> --slug <tập> --lan1` — tin lượt 1 = khuôn chung +
   `script.soat_gptweb.{boi_canh, cau_truc, rang_buoc}` + luật kênh (`script_qc.lane_rules`) + ràng buộc cứng (số chỉ từ tư liệu, thoại tách
   câu, ±3% độ dài, không chép video gốc, trả đủ lời hứa tiêu đề) + series_ctx + script. Mở CHAT MỚI trong Project của lane.
3. Cổng VẪN MỞ sau khi nhận trả lời (phiên giữ cho đúng tập). Tab lane thẩm định: hợp lý → nhận; sai luật lane → phản biện có lý do
   (`--tin <file>`, CÙNG cổng + hội thoại, ghi ở `soat_gptweb\phien.json`) → CHỜ trả lời. Thống nhất phương án → **`--chot` ĐÓNG cổng**
   → RỒI MỚI tổng hợp `viec_tay.txt` (thay thế NGUYÊN VĂN, ước lượng độ dài < trần) → `ghi_lock ESCALATE` → `make_video --den B3G`
   (Opus vá → Sol ×2 → khoá). KHÔNG sửa tay.
4. Viết `<tập>\soat_gptweb\BAO_CAO_SUA.md` → `soat_kb_gptweb.py ... --xong` (chặn nếu cổng còn mở; kiểm lock PASS + có trả lời + báo cáo →
   giữ hook nếu đầu kịch bản trùng hook đã khoá, đổi thật mới khoá lại → marker received) → cổng B4/B5W/dong_goi cho qua.

⛔ **LUẬT CỨNG CỔNG CHATGPT** (anh chốt 2026-09-27 bản 2; `pipeline\gptweb_pool.py`, 2 tài khoản: acc1 `E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE`
cổng 9335 — khoá CHUNG với YT-TITLE-RESEARCH; acc2 `E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE_2` cổng 9336):
- 1 tài khoản chỉ 1 lane tại 1 lúc. Lane giữ PHIÊN (tiến trình nền giữ khoá + cổng, `logs\gptweb_phien_<acc>.json`) từ `--lan1` tới `--chot`.
- Gửi xong phải **CHỜ ChatGPT trả lời** (tối đa 2 giờ) — KHÔNG đóng cổng giữa chừng, **KHÔNG BAO GIỜ gửi lại** (chống spam GPT).
  Chưa đọc được trả lời → cổng vẫn mở, dùng `--doc` để chỉ đọc tiếp.
- Thống nhất phương án → `--chot` đóng cổng → rồi mới viết lại kịch bản theo hướng đã chốt.
- **Chỉ đóng cổng DO TOOL MỞ** (đúng PID Chrome tool khởi động). Cổng mở sẵn từ trước (dự án khác, mở tay) → dùng nhờ, TUYỆT ĐỐI KHÔNG
  đóng. Tool không có lệnh đóng cổng của người khác.
- Quá tải → đóng phiên tài khoản đó, thử tài khoản kia; cả hai bận/quá tải → `GPT báo To many request- chờ 20 phút`, ngủ 20 phút
  (tối đa 9 vòng). Lượt tiếp của 1 hội thoại chỉ về đúng tài khoản đã mở nó.
- Quên `--chot`: sau 3 giờ phiên tự đóng (chỉ cổng do tool mở). CẤM `Stop-Process` tiến trình tool/tiến trình giữ phiên.
- Xem trạng thái (ai đang giữ phiên nào): `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\gptweb_pool.py`.
- ⚠️ **ĐỌC TRẢ LỜI — đã vá tận gốc 2026-09-30 trong `E:\CLAUDE\YOUTUBE\h2dev\pipeline\gptweb_pool.py` (`_JS_TRA_LOI`), MỌI lane dùng chung
  tự có, KHÔNG được chép bản riêng hàm đọc sang tool khác của lane.** Hai lỗi cũ (dính thật Lane F ep06 — `--lan1`/`--doc` treo tới 2 giờ
  dù GPT đã trả lời xong): (1) ChatGPT lưu tin mình gửi có escape markdown (`- ` → `\- `) nên so khớp 150 ký tự đầu luôn trượt → nay bỏ
  mọi dấu `\` hai phía trước khi so; (2) câu trả lời gồm NHIỀU tin assistant (lời dẫn → tool đọc file Project → bài chấm chính), code
  cũ lấy tin SỚM NHẤT (chỉ lời dẫn) → nay gom hết theo thứ tự. **Nếu vẫn treo:** cổng còn mở thì CHỈ chạy `--doc` (không bao giờ gửi
  lại); tự kiểm bằng cách gọi `gptweb_pool._JS_TRA_LOI` qua Playwright CDP cổng 9335/9336 — trả `{err:'không thấy tin mình gửi'}` là
  lỗi so khớp (vá hàm chung, không vá riêng lane), trả `{cho:true}` là GPT chưa xong.
- ⚠️ **Góp ý GPT đụng 5 câu đầu = đụng HOOK:** S3 ép đầu kịch bản về hook đã khoá, nên viec_tay sửa hook sẽ bị Opus đổi ngược lại.
  Phải khoá hook mới TRƯỚC (`hook_stage.khoa(d, text_moi, mode=cu['mode'], extra={...})`, backup `hook_locked.txt`/`hook_lock.json`)
  → `ghi_lock ESCALATE` → `make_video --den B3G` (S3 tự sinh việc thay đầu bài).
Link: `script.soat_gptweb.urls.{acc1, acc2}` = Project riêng của lane ở từng tài khoản (thiếu link tài khoản nào thì không dùng tài khoản đó).

## 4c. CHẶNG MÁY 3 SOÁT KỊCH BẢN — giữa B3 và pha asset (anh chốt 2026-09-26, MỌI lane trừ 4 lane cũ)
> ⭐ 30/09 (2): bảng dưới còn nói `review\` + bộ đọc — ĐÃ BỎ: chỉ chép `script.txt` vào `jobs\<tab>\<slug>\`, không bắt `BAO_CAO_SUA.md`.
> ✅ **MẶC ĐỊNH LẠI từ 2026-09-30** (`script.soat: "may3"`, 7 lane chuẩn đã khai). Nhận + làm tiếp: `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`.
> Hook = đoạn đầu `script.txt`; `--nhan` lấy đúng số đoạn của hook cũ (không cắt theo số chữ nữa) rồi khoá lại.
Áp dụng khi `script.review_may3` ≠ `false` (**vắng field = BẬT** — lane mới tự có; `satori-jp-obaa`, `kenko-chiebukuro`,
`toshi-densetsu-jp`, `irogatatarukioku` khai `false`, để nguyên luồng cũ). Tool: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py`.

| Bước | Ai | Việc |
|---|---|---|
| Sau LOCK PASS | máy 1, **tự động** trong `make_video.py` (cả lean lẫn cũ, kể cả `--den B3G`) | chép bộ đọc → `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\<tab>\<slug>\review\` + `README_MAY3.md` · ghi `review_may3.json` state=shared · **cột D = `Chờ kiểm tra kịch bản`** · **DỪNG** (không xuống B4/B5W) |
| Soát/sửa | máy 3 (người) | ghi ĐÈ `script.txt` thành bản cuối (hook ở ĐẦU kịch bản, sửa được) **ngay trong `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\<tab>\<slug>\review\`** (+ `BAO_CAO_SUA.md`) — anh đã đổi `jobs` thành 2 chiều 2026-09-26 · tự ghi **cột D = `Đã sửa kịch bản`** · báo anh |
| Nhận | máy 1, khi anh báo: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\review_may3.py --nhan --profile <lane> --slug <slug>` | kiểm D = `Đã sửa kịch bản` → lấy `jobs\<tab>\<slug>\review\script.txt` (chặn nếu vẫn trùng bản đã gửi = máy 3 chưa ghi đè) → lưu `script.truoc_may3_<ts>.txt` → chép bản máy 3 **nguyên văn, không sửa 1 chữ** → đo CHỈ ĐỌC (`NHAN_MAY3.md`: CHẶN nếu <70% ngân sách hoặc số liệu ngoài `series_ctx.txt` ở lane tài liệu; còn lại chỉ CẢNH BÁO) → **rút hook từ đầu kịch bản** (`so_chu_muc_tieu`, cắt ranh giới câu, không Sol) và khoá lại `hook/` → ký lại `script.lock.json` PASS `reason=may3` → `review_may3.json` state=received |
| Tiếp | tab lane, theo SOP lane | B5W/B5P → hook storyboard/clip → `dong_goi_may2.py --job` (D → `Đã giao máy 2` + K, H = cần ảnh) → TITLE |

Cổng: `make_video.Job.kiem_lock` (B4/B5W…) và `dong_goi_may2 --job` gọi `review_may3.cong()` — chưa `received` hoặc script đổi
sau khi nhận (sha lệch) → DỪNG, không có `--from B4` cửa sau. Không tự poll sheet: anh báo tay khi máy 3 xong.

## 5. GHI KẾT QUẢ — sheet tab lane, cột KỊCH BẢN (D)
**Anh chốt 2026-09-20: không dài dòng, không sha. 2026-10-03: chữ xong máy 1 = `Đã giao máy 2` (thay `Done`) + các trạng thái "đang làm" — bảng gốc `docs/TRANG_THAI_COT_D_K.md`.**
**2026-09-26 thêm 2 trạng thái trung gian của chặng máy 3 (§4c) — chỉ 2 chuỗi này, máy đọc so khớp nguyên văn.**

| Ô D | Khi nào | Ai ghi |
|---|---|---|
| `Đang chạy kịch bản bước 1` | `make_video.py` bắt đầu chặng 1 (tập chưa gửi máy 3) — 03/10 | máy 1 (`review_may3.bat_dau_b1`) |
| `Chờ kiểm tra kịch bản` (+ dòng 2 = đường dẫn) | máy 1 vừa chép `script.txt` vào `jobs\<tab>\<slug>\` cho máy 3 (lane có `review_may3`); **K = thư mục anh sửa + lệnh `--nhan` + file làm tiếp** (03/10) | máy 1 (`review_may3.share`, tự động sau B3) |
| `Đã sửa kịch bản` | máy 3 đã sửa (hoặc duyệt nguyên) `jobs\<tab>\<slug>\script.txt` | máy 3 |
| `Đang làm Hook` | `review_may3.py --nhan` xong, tab làm cast/B5W/B5P/hình + clip hook — 03/10 | máy 1 (`review_may3.nhan`) |
| `Chờ duyệt hook` → `Đã duyệt hook` | clip hook xem thử gửi anh / anh duyệt (02/10) | máy 1 (`duyet_hook --gui`) / anh |
| `Đã giao máy 2` (cũ `Done`) | lock PASS **và** đã `--nhan` + duyệt hook, đóng gói máy 2; **K = câu anh dán cho máy 2** (03/10) | máy 1 (`dong_goi_may2 --job`) |
| `escalate` | lớp 3 kết luận cần anh quyết (kèm 1 câu lý do ở cột K) | máy 1 |
| `block` | thiếu hồ sơ/hạ tầng, ghi thiếu gì ở K | máy 1 |

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
| Cột D dài dòng / "chờ anh duyệt" | đẩy việc lên anh | §5: bảng trạng thái |
| Bản đã LOCK PASS vẫn còn lỗi timeline [NẶNG] (ep10 G) | Sol không tất định — 1 lần PASS có phần may | `sol_pass_need`=2: khoá chỉ khi PASS 2 lần liên tiếp; đừng kết luận model patch kém chỉ vì 1 lần Sol FIX |
| Fable hết quota giữa chừng (`You've reached your Fable limit`) | 1 model gánh cả S2+S4+B5W | S4 = Opus 5 qua `patch_model`; Fable chỉ giữ S2 |
| `soat_kb_gptweb --lan1/--doc` treo dù ChatGPT đã trả lời xong | tin gửi bị ChatGPT escape `\-` + trả lời nhiều tin assistant | đã vá hàm chung `gptweb_pool._JS_TRA_LOI` 2026-09-30 (§4b) — mọi lane tự có |
| Sửa hook theo góp ý GPT xong chạy B3G, hook lại về bản cũ | S3 ép đầu kịch bản = hook đã khoá | `hook_stage.khoa()` bản mới TRƯỚC khi chạy lại (§4b) |
