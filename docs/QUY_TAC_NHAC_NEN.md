# QUY TẮC NHẠC NỀN — MỌI LANE (anh chốt 2026-10-23)

> Người đọc: Hermes và mọi phiên `claude -p` chạy tập trên máy này (h2dev + MG_STUDIO).
> Đọc hết file này trước khi đụng tới nhạc nền, thêm lane mới, hoặc xử lỗi "thiếu nhạc".

## 1. Luật cứng

| # | Luật |
|---|---|
| 1 | **CẤM nhạc Suno / ai33 / OpenSpeaker** cho mọi lane, mọi tập, kể cả hook. Lý do: tài khoản Suno là của bên bán lại → mình không có chứng từ giấy phép → bị claim là không kháng được. |
| 2 | Nhạc nền **CHỈ lấy từ Thư viện âm thanh YouTube Studio (Audio Library)**, và **CHỈ bài giấy phép YouTube** (`CREATOR_MUSIC_LICENSE_TYPE_YOUTUBE`, không cần ghi công). **Không** dùng bài Creative Commons (CC-BY), **không** lấy nhạc từ web/kênh "no copyright" khác. |
| 3 | **Mỗi kênh 1 bộ bài riêng** — tool tự chặn không cho 2 lane dùng chung 1 bài. |
| 4 | **Không tải tay, không tự viết code tải nhạc mới** — dùng đúng tool ở mục 3. |
| 5 | Không SFX (luật 01/10 vẫn giữ). Ngoại lệ: tiếng click + chuông của nút đăng ký **giữ nguyên**. |
| 6 | Không sửa mức nhạc trong profile/lane.json khi anh chưa yêu cầu (mức hiện tại anh đã chỉnh nhiều lần). |
| 7 | Không xoá file nhạc cũ (`piano_nen_suno_bak.mp3`, `hook_cand*.mp3`, `than_*.mp3`) — chỉ để làm bản lưu. |

## 2. Nhạc đang dùng ở đâu

| Lane (tên tab) | File nhạc máy đọc | Chứng từ |
|---|---|---|
| F-teinengo-real · L-shakai-no-naze · M-teinengo-anaba · Lane-N · Lane-O | `E:\CLAUDE\YOUTUBE\FlowHandoff_local\shared\buoc2_3_tool\assets\_bgm_kenh\<mã lane>\piano_nen.mp3` (2 bài piano nối mờ 5 s, −20 LUFS) | `nguon.json` cùng thư mục |
| X (MG_STUDIO) | `E:\CLAUDE\YOUTUBE\MG_STUDIO\assets\nhac\x\al_hook.mp3` + `al_than_1.mp3` + `al_than_2.mp3`, trỏ trong `lanes\x\lane.json` khoá `"nhac"` | `assets\nhac\x\nguon.json` |
| Lane-P · Lane-Q (MG_STUDIO) | Nhạc do code tự tổng hợp (`render\engine\tron_am.py`), không lấy từ đâu → **không đụng** | — |

Mã lane: F=`teinengo-real` · L=`shakai_no_naze` · M=`teinengo-anaba` · N=`senior_korekara` · O=`kaigo-sukatto`.
Các bước dựng (`ghep_hook_noi_truoc.py`, `mg.py`) **tự đọc** các file trên — chạy tập bình thường là đã dùng đúng nhạc mới.

## 3. Tool tải nhạc (chỉ khi cần)

```
cd E:\CLAUDE\YOUTUBE\FlowHandoff_local\shared\buoc2_3_tool\pipeline
py -3.13 -X utf8 bgm_audio_library.py --dry-run                 # xem bài sẽ chọn, KHÔNG tải/ghi gì
py -3.13 -X utf8 bgm_audio_library.py                           # tải cho mọi lane chưa có nguon.json
py -3.13 -X utf8 bgm_audio_library.py --only <mã lane> --force  # chọn lại cho 1 lane
```

- **Profile dùng để tải (anh chốt 2026-10-23): `hoangletran6868@gmail.com`** = `D:\CLAUDE\RENDER_IMG\chrome_profile_gemini2`,
  cổng **9339** (mặc định của tool). Chưa mở thì mở đúng lệnh `D:\CLAUDE\RENDER_IMG\mo-chrome-profile-gemini2.bat`; mình mở thì
  xong việc mình đóng lại (profile này cũng là dự phòng Flow PRO của hẹn giờ). **Không** dùng `nguyenquoctuan` (9337) — tài khoản
  đó chưa có kênh YouTube nên không vào được Thư viện âm thanh.
- Tool mở **thêm 1 tab** trong Chrome đó, gọi Thư viện
  âm thanh, lọc theo nhạc cụ/tâm trạng/thể loại, tự loại bài có đoạn im > 3 s, ghép, chuẩn hoá −20 LUFS, ghi `nguon.json`.
  Xong tự đóng đúng tab của nó. **Cấm** đóng/kill Chrome đó (dùng chung với Flow/Vids/AUTO_LIST).
- Lane X: tool tự cập nhật `lanes\x\lane.json` (bản cũ lưu `lane.truoc_<ngày>-audiolib.json`).

## 4. Khi nào phải chạy tool

| Tình huống | Làm gì |
|---|---|
| Log báo `✗ lane chưa có bài nhạc riêng ...` | Lane chưa khai trong bảng `DICH` của `bgm_audio_library.py` → **báo anh**, ghi rõ mã lane + ngách. Không tự bịa tâm trạng nhạc. Anh duyệt rồi mới thêm 1 dòng `DICH` và chạy `--only <mã lane>`. |
| Anh nói "đổi nhạc lane X" / "nhạc lane này không hợp" | `--only <mã lane> --force` → báo tên bài mới + tác giả. Tool sẽ chọn bài kế tiếp chưa lane nào dùng. |
| Tool báo `✗ không vào được Thư viện âm thanh` | Tài khoản của Chrome đó chưa có kênh YouTube hoặc chưa đăng nhập → **dừng, báo anh**. Không tự tạo kênh. |
| Tool báo `✗ không có Chrome ở cổng ...` | Mở lại đúng lệnh tool in ra (cùng `--user-data-dir` cũ), chạy nền, rồi chạy lại. Không tạo profile mới. |
| Có tập đang dùng ffmpeg | Tool cũng đi qua cổng ffmpeg — thấy `⏳ [ffgate] … chờ` là bình thường, cứ đợi. |

## 4b. Máy 1 (repo h2dev2, nhánh hook-video)

| Việc | Làm thế nào |
|---|---|
| Nhạc HOOK từng tập (trước đây sinh Suno → `hook\sfx\99_nhac_piano.mp3`) | `py -3.13 -X utf8 pipeline\nhac_hook_tu_thu_vien.py --tap <thư mục tập> --lane <mã lane> --giay <độ dài hook>` — cắt 1 đoạn liền từ bài lane, −16 LUFS, kèm `99_nhac_piano.nguon.json`. `openspeaker_tts.generate_music()` đã khoá (ném lỗi). |
| Bài nhạc của lane ở đâu | Tool tự tìm theo thứ tự: `<repo>\assets\_bgm_kenh\<lane>\` → `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\buoc2_3_tool\assets\_bgm_kenh\<lane>\` (máy 2 tải, Syncthing đưa sang). Không cần tải lại. |
| Lane chưa có bài | `py -3.13 -X utf8 pipeline\bgm_audio_library.py --only <mã lane> --port <cổng Chrome có kênh YouTube>` (thêm 1 dòng `DICH` trước). Máy 1 dùng Chrome nào cũng được, miễn tài khoản CÓ KÊNH YouTube và mở cổng CDP riêng. |
| Chống trùng bài giữa kênh/dự án/2 máy | Sổ chung `FlowHandoff_local\shared\nhac_audio_library\so_dang_ky_bai.json` — cả `bgm_audio_library.py` lẫn `tai_nhac.py` (MG_STUDIO, GEO) đều đọc + ghi sổ này. Không sửa tay. |

## 5. Video đã đăng dùng nhạc Suno bị claim

Vào YouTube Studio → video đó → **Trình chỉnh sửa → Âm thanh → thay** bằng 1 bài trong Thư viện âm thanh
(không cần dựng lại video). Đây là thao tác trên kênh → **báo anh làm, không tự làm**.

## 6. Báo cáo sau khi chạy tool

`| Lane | Bài mới (tác giả) | LUFS | Trạng thái |` — kèm đường dẫn đầy đủ tới `piano_nen.mp3` / `al_*.mp3`.
