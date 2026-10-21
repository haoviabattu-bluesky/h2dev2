# HƯỚNG DẪN CHẠY TẬP 15 — lane N (`senior_korekara`) · `ep15-home-7-omoikomi`

> Viết 18/10/2026 ngay khi ghi dòng 16 lên tab `Lane-N`.
> **Agent đọc HẾT file này rồi mới chạy.** Không đọc lại SOP / CHANNEL_DNA / profile / lịch sử chat.
> Mở đầu mọi báo cáo bằng `@lane:senior_korekara`.

---

## 0. ĐANG Ở ĐÂU

| Mục | Giá trị |
|---|---|
| Lane | `senior_korekara` — tab trang tính `Lane-N`, dòng **16** |
| Tập | **15** · slug `ep15-home-7-omoikomi` |
| Thư mục tập (đã dựng, 10 file) | `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep15-home-7-omoikomi\` |
| Hồ sơ bàn giao | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneN_home_omoikomi_inryFzntZa4_2026-10-18\HO_SO_BAN_GIAO_LANE_N_HOME.md` |
| Bằng chứng verify | `TRENDING-RESEARCH\data\deep_inryFzntZa4\verify_handoff_pkg.log` — **76 PASS / 0 FAIL** |
| Bằng chứng ghi sheet | `TRENDING-RESEARCH\data\deep_inryFzntZa4\verify_ep15_sheet.log` — **45 PASS / 0 FAIL** |
| Video nguồn | `inryFzntZa4` · kênh 源さん `UCOkbo1BhQw1NhMj1sBdkt6w` · 109.316 views · 55:20 |
| Việc của agent này | **CHẶNG 1: viết hook + kịch bản rồi khoá.** KHÔNG vẽ ảnh, KHÔNG dựng video |
| Tập mẫu để soi khi bí | `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\ep14-saikoyou-sukima\` |

---

## 1. LỆNH CHẠY — đúng 2 dòng, không thêm bớt

Mở `cmd` tại `E:\CLAUDE\YOUTUBE\h2dev`:

```bat
set PYTHONPATH=
py -3.13 -X utf8 pipeline\make_video.py --profile senior_korekara --slug ep15-home-7-omoikomi --den B3G
```

**`set PYTHONPATH=` là bắt buộc.** PYTHONPATH bẩn làm numpy hỏng (`No module named
'numpy._core._multiarray_umath'`, nạp file `.cp311` trong khi chạy 3.13).

---

## 2. LỆNH NÀY LÀM GÌ

| Bước | Nội dung | Ai làm |
|---|---|---|
| B2 | Đọc `competitor.txt` (transcript video gốc) | máy |
| B3 | **Hook**: Fable 5.1 viết 2 phương án → Sol chọn → Opus 5 vá → **khoá** | máy |
| B3Q | QC nội dung hook (bắt chép quá sát câu gốc) | máy |
| B3G | **Kịch bản thân bài**: Fable 5.1 viết 1 lần → máy đo → Opus 5 vá → **LOCK sha256** | máy |

Xong thì máy **TỰ DỪNG**. Ghi:
- cột **D** dòng 16 = `Chờ kiểm tra kịch bản`
- cột **K** dòng 16 = thư mục `script.txt` cho anh sửa + lệnh `review_may3.py --nhan`

---

## 3. RÀNG BUỘC CỨNG

**Tiêu đề — GIỮ NGUYÊN `title.txt`, không được đổi:**
```
【漫画】給食室38年の74歳。「いざとなったら施設」と8年言った私が、7つの思い込みを数えた日
```
47 ký tự (core 43). Đã PASS 2 gate (`title_len` 38–56 · `title_core_len` 30–46) + LUẬT TIÊU ĐỀ
lane N rule 1 (nghề cụ thể trong ~20 ký tự đầu) + rule 7 (cấm 「Nつの思い込み」 trừu tượng
khi không có nghề cụ thể).

**Số liệu — chỉ dùng 4 nguồn `[D1]`–`[D4]` trong `series_ctx.txt`**, tất cả là URL chính phủ thật:
- `[D1]` `https://www.mhlw.go.jp/toukei/saikin/hw/life/life25/index.html`
- `[D2]` `https://www.mhlw.go.jp/toukei/list/24-22-2.html`
- `[D3]` `https://www.mhlw.go.jp/jinkou/kakutei25/index.html`
- `[D4]` `https://www.mhlw.go.jp/topics/kaigo/kentou/15kourei/zuhyou19.html`

**`[D4]` — cấm nói 「平均3年余り」.** Trung bình thật 1.445,3 日 ≈ 3,96 năm. Phải nói:
「3年未満が半分、5年以上が3割」 (<3 năm 51,8% · 3–<5 19,4% · ≥5 28,2%).

**Nhân vật** (đã khai trong `characters.json`):
| id | Tên | Tuổi | Vai | Giọng |
|---|---|---|---|---|
| `ke` | 林房江 | 74 | **chính, kể ngôi 1 「私」** | `clone_2669056` (Nữ C) speed 0.85 |
| `midori` | 佐伯みどり | 49 | con gái | speed 1.0 |
| `kiyo` | キヨ | 76 | bạn, voice-only | — |

**`id` phải là `ke`.** Thiếu `ke` là pipeline đè giọng narrator mặc định (Nam B) → cả tập
giọng đàn ông đọc lời bà cụ 74.

**Motif CẤM dùng lại** (đã có trong tập khác): 封筒にパンフレット三冊 · バス停で世話役 ·
夜中の2時に階段を滑る · 手すり工事9万円/自己負担90%.

---

## 4. CẤM

1. **CẤM `--dry`** — `make_video.py` **không có cờ này**. Argparse khớp viết tắt `--dry-run` và
   **chạy y như thật**: gọi `claude -p`, sinh `hook/` + `state.json`. Đã dính 18/10, phải xoá đi.
2. **CẤM `--from B4` / `--den B5` / `--den B8`** — máy 1 chỉ bước 1 + hình hook.
3. **CẤM sửa tay `script.txt`** sau khi khoá — sha lệch là mọi bước sau dừng.
4. **CẤM gọi `goi_title.py`, cấm làm thumbnail** — toàn dự án tắt từ 01/10.
5. **CẤM xoá / ghi đè dòng khác trên tab** — chỉ đụng dòng 16.

---

## 5. HAI CỔNG KHÔNG ĐƯỢC TẮT

1. **Cổng PHỦ CHỮ** (`tts.py::kiem_phu_chu`) — so số chữ phụ đề server trả về với kịch bản gốc,
   thiếu quá 5% là dừng. Đo thật 23/09: 3/4 lượt ai33 **nuốt trọn một câu** mà không báo lỗi.
2. **Cổng KHOÁ** (`gate_common.kiem_lock`) — `script.txt` sửa sau khi khoá là chặn cứng.

---

## 6. XONG THÌ BÁO ANH

Gửi: đường dẫn `script.txt` + nội dung ô K dòng 16. **DỪNG, chờ anh sửa kịch bản.**

Sau khi anh sửa xong (D = `Đã sửa kịch bản`), chạy:
```bat
py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile senior_korekara --slug ep15-home-7-omoikomi
```
rồi làm tiếp theo `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md`.

---

## 7. RỦI RO CHƯA VERIFY ĐƯỢC (nói trước, đừng phát hiện muộn)

Kịch bản dự kiến **7 mục × ~2,3 phút ≈ 16 phút**, nhưng video gốc 55:20 chia 7 mục ra
**6,2 phút/mục** → phải cắt 63% nội dung mỗi mục. **Chưa có bản nháp kịch bản thật nào để chứng
minh nhịp 2,3 phút/mục đủ giữ chân.** Nếu bản nháp đầu ra loãng, xử lý theo thứ tự:
1. giảm còn 5–6 mục (bỏ mục yếu nhất, giữ mục có số liệu `[Dn]`),
2. giữ 7 mục nhưng nâng lên ~20 phút,
3. **không** nhồi thêm chi tiết vụn để đủ độ dài.
