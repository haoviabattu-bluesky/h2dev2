# BIÊN BẢN DỌN LANE SATORI — 2026-09-24

Lý do: tránh lặp lại sự cố 23/09 — hook được dựng lên `ep3-sougi\final.mp4` (bản 07/09, không có
trong sheet) trong khi bản thật sẽ đăng của cùng câu chuyện là `CHANEL\Lopezzapa68\ep05-...`.
Nguyên nhân gốc: trong `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\` có **hai thế hệ thư mục** cùng
tồn tại, kể cùng những câu chuyện, và thế hệ cũ vẫn còn `final.mp4` nên bốc nhầm rất dễ.

**Đã giải phóng 27,2 GB. Lane còn 11,5 GB.**

## 1. Nguyên tắc phân loại (dùng lại cho lane khác)

| | |
|---|---|
| Giữ | thư mục **có mặt ở cột C (FOLDER) của tab sheet** = dây chuyền sản xuất chính thức |
| Xoá | thư mục thế hệ cũ, không dòng nào trong sheet trỏ tới, kể trùng câu chuyện với một thư mục `simbot2-*` |
| Xoá | bản video **trùng từng byte** với bản đã giao ở `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\<ep>\` |
| Giữ lại phần chữ | mọi `.txt/.json/.md/.srt` < 500 KB được chép sang `_LUU_TRU_KICH_BAN_CU\` trước khi xoá |

Kiểm an toàn đã chạy trước khi xoá: (a) đối chiếu 14 dòng sheet `Lopezzapa68`; (b) `grep` toàn repo
xem tên thư mục có bị code/tài liệu phụ thuộc không — `_bgm` CÓ (`pipeline\render_engine.py` tự dò
`slug.parent\_bgm\*.mp3`) nên **giữ**, `_reftest` là bằng chứng được `docs\SOP_SATORI_JP.md` §209
dẫn nên **giữ**; (c) xác nhận cả 14 video đã giao đều còn đủ ở `CHANEL\Lopezzapa68\`.

## 2. Đã xoá — 20 thư mục thế hệ cũ (18,09 GB)

`youyoin` · `ep08-nanajuu` · `ep14-kaimono` · `ep12-yokin` · `ep13-ginkou` · `ep11-saikon` ·
`tsucho-kotae` · `ep10-saigo` · `ep09-oyakoukou` · `ep3b-auto` · `nenkin-fujinkai` ·
`ep4-tabidachi` · `yokin-basho` · `roujin-home` · `yokin-tozetsu` · `saigo-no-bento` ·
`ep07b-remake` · `ep07c-beats` · `_cu_simbot2-01-KrerPxaFZdE_0914` · `_test`

Trong đó các cặp TRÙNG CÂU CHUYỆN đã đối chiếu bằng câu mở đầu `script.txt`:
`youyoin` + `roujin-home` ↔ `simbot2-04` (ra khỏi viện dưỡng lão) · `tsucho-kotae` ↔ `simbot2-11`
(sáng mồng một, sổ tiết kiệm) · `yokin-basho` ↔ `simbot2-21` (nhờ ngân hàng chặn chính mình) ·
`nenkin-fujinkai` ↔ `simbot2-01` (mang đồ ăn sang nhà bạn 50 năm) · `yokin-tozetsu` ↔ `simbot2-07`.
Nhóm `ep08…ep14` là loạt *静子の終活ノート* làm ngày 08/09 bằng nhánh não-Claude, đã bỏ giữa đường
khi kênh chuyển sang nhân bản simbot2 — không dòng sheet nào trỏ tới.

275 file chữ (kịch bản, prompt, characters.json, thumb_text) đã lưu ở
`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\_LUU_TRU_KICH_BAN_CU\` (6 MB).

## 3. Đã xoá — bản video TRÙNG TỪNG BYTE với bản đã giao (7,44 GB)

7 tập ĐÃ ĐĂNG (`simbot2-01/04/06/07/11/19/21`): xoá `final.mp4` + `final_vi.mp4` trong `assets\`,
vì `CHANEL\Lopezzapa68\<ep>\final.mp4` và `review-vi.mp4` giống **đúng từng byte** (đã so size 11/11
cặp) và video đã nằm trên YouTube.
Tập `simbot2-08` chưa đăng: **giữ `final.mp4`** (cần để ghép hook), chỉ xoá `final_vi.mp4`.
Tập `simbot2-09/10/12` chưa đăng: giữ nguyên `final.mp4`.

## 4. `ep3-sougi` — 1.677 MB → 51 MB (1,63 GB)

Đây chính là thư mục gây nhầm lẫn. Đã xoá `final.mp4`, `final_with_hook.mp4`, `voice.mp3`, `img\`,
`hook\clip\`, `hook\_seg\`, `hook\flow_prompts\` và 4 bản hook thừa.

**Giữ lại cố ý** (làm khuôn cho 6 tập tới, xem `docs\KE_HOACH_HOOK_SATORI_TAP_CHUA_DANG.md`):
`hook\hook_final_JP_lv.mp4` (26 giây, 21 MB — bản mẫu để xem lại) · `hook_locked.txt` ·
`hook_lock.json` · `hook_storyboard.json` · `hook_timeline.json` · `img_prompts_hook.txt` ·
`hook\img\` (7 ảnh) · `grok_jobs*.csv` · `GROK_HUONG_DAN.md` · `hook_voice.mp3/srt` · `script.txt`.

## 5. Rào chống lặp lại

1. **Chỉ có MỘT bản video của một tập trong máy**: bản giao ở `CHANEL\Lopezzapa68\<ep>\`. Trong
   `assets\` chỉ giữ `final.mp4` của tập **chưa đăng** (vì còn phải ghép hook / chạy B10).
2. Trước khi ghép hook cho bất kỳ tập nào: **đối chiếu slug với cột C của sheet** trước, đừng bốc
   theo tên thư mục nghe giống chủ đề.
3. Tập bỏ giữa đường thì xoá ngay trong phiên đó, đừng để lại `final.mp4` — chính cái `final.mp4`
   còn sót mới làm người sau tưởng là bản dùng được.
