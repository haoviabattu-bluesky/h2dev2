# SOP LANE O — `kaigo-sukatto` · 介護スカッと (tên tạm Lane-O)

Runbook 1 tập. Cửa vào: `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kaigo-sukatto.md`. Kỹ thuật giống Lane K → chỗ nào file này không nói,
làm theo `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_K.md` (thay `yakkyoku-sukatto` → `kaigo-sukatto`, `assets\yakkyoku-sukatto` → `assets\O-kaigo-sukatto`).

## §0 KHÁC LANE K Ở ĐÂU
| Mục | Lane O | Lane K |
|---|---|---|
| Nghề/bối cảnh | cơ sở chăm sóc người cao tuổi (1 loại/tập: ユニット型特養 / 有料老人ホーム / グループホーム / デイサービス) | nhà thuốc |
| Câu cửa miệng | ĐƯỢC dùng câu phổ biến của kênh mẫu (「じゃあ、辞めます」…) — CẤM chép tình tiết/tên/câu kết video gốc | cấm dùng 4 câu của kênh mẫu |
| Nạn nhân phụ | cụ già + người nhà: tối đa ヒヤリハット (suýt sự cố), không ngã/thương tích/ngược đãi; người nhà là người NHÌN THẤY sự thật | bệnh nhân |
| Người thế chỗ | bắt buộc cài sớm, hợp lý với ngành thiếu người (中途の介護福祉士 / điều chuyển nội bộ / 夜勤専従) | tuỳ tập |
| Soát kịch bản | máy 3/anh (`soat:"may3"`), ChatGPT web TẮT (lane chưa có Project) | — |
| Kênh | chưa có → `title_auto=false`, nút đăng ký TẮT | có |

## §1 CHỌN TẬP (từ báo cáo KENH_GOC_10 §3.1)
Câu cửa miệng phải qua 4 phép thử: (1) mọi nghề đều gặp kiểu người này · (2) là VŨ KHÍ nói thẳng vào mặt người khác · (3) lặp được 3 lần
mức cược tăng · (4) quay ngược được vào chính hắn. Danh sách 10 tập = tab `Lane-O` A2:B11; cột K ghi video gốc làm khung.

## §2 MỘT TẬP — MÁY 1
```bat
cd /d E:\CLAUDE\YOUTUBE\h2dev
:: A. HỒ SƠ (tay): assets\O-kaigo-sukatto\epNN-<slug>\ gồm
::    competitor.txt + competitor.segments.json (video gốc ghi ở cột K; transcript: docs\channel_dna\yakkyoku-sukatto\KENH_GOC_10\<id>\transcript.txt
::      hoặc FlowHandoff_local\results\laneK_from_research\data\transcripts\<id>.json) · series_ctx.txt ([Dn] + URL chính thức + SỐ ĐƯỢC PHÉP
::      + QUY ƯỚC: 3 lần câu cửa miệng / người thế chỗ / hậu quả từ cơ chế / cụ không bị hại) · title.txt (B bỏ phần dịch) · promise.txt (1 câu)
::    Ghi ngay cột C = đường dẫn thư mục tập.
:: B. VIẾT + KHOÁ → tự DỪNG, D = "Chờ kiểm tra kịch bản" (chạy nền, ~20–40')
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug epNN-<slug> --den B3G
:: C. Anh/máy 3 sửa jobs\Lane-O\<slug>\script.txt → D = "Đã sửa kịch bản" → theo docs\NHAN_KICH_BAN_MAY3.md:
py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile kaigo-sukatto --slug epNN-<slug>
:: D. characters.json (tay, đọc kịch bản): MỌI vai có thoại hoặc ≥2 cảnh = {id,name,vai,age,gender,look,ref:true,voice:{speaker,style}};
::    nhân vật chính id "shu" + "kuchiguse"; giọng lấy voice.fixed_cast / voice.cast_bank; look khác nhau rõ (đồng phục chăm sóc màu khác,
::    tóc, kính); cụ già trông sạch sẽ, đàng hoàng. Bà cụ chưa có giọng trong kho → chọn 1 giọng VOICEVOX nữ trầm, ghi rõ trong báo cáo.
py -3.13 -X utf8 pipeline\gan_vai.py --profile kaigo-sukatto --slug assets\O-kaigo-sukatto\epNN-<slug>
:: E. PROMPT ẢNH — chỉ --only (máy 1 CẤM B4/B5, code chặn cứng)
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile kaigo-sukatto --slug epNN-<slug> --only B5P
:: F. HOOK (máy 1 làm trọn hình) — y SOP_LANE_M.md §2 mục F:
py -3.13 -X utf8 pipeline\hook_storyboard.py --profile kaigo-sukatto --slug epNN-<slug> --force
::    master vai: make_video.Job(...).masters_from_bible() · ảnh hook: anh_hook.py <tập>\hook (Google Flow Ultra → 9router → gpti2)
::    QC ảnh: qc_hook_clip.py --hook <tập>\hook --anh N · clip Grok 6s: set GROK_SHEET_ID=1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
::    py -3.13 -X utf8 tools\hook_lane_g\grok_da_luong.py <tập TUYỆT ĐỐI>\hook (đa luồng 5–10) · QC clip: qc_hook_clip.py --clip N · SFX: tools\hook_lane_g\sfx.py
py -3.13 -X utf8 pipeline\hook_tap_md.py --slug E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\epNN-<slug> --profile kaigo-sukatto
:: G. GIAO MÁY 2 (tự ghi D = Đã giao máy 2 + K = lệnh máy 2, H = cần ảnh) + bundle profile cho máy 2
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job kaigo-sukatto epNN-<slug>
py -3.13 -X utf8 pipeline\dong_goi_may2.py --bundle --profile-list kaigo-sukatto
```

## §3 GATE (profile)
title 31–46 ký tự (kể cả【漫画】) · 17,5' · 7 chặng `budget.sections` · thoại ≤45% · `dialogue_own_sentence` · câu cửa miệng được lặp (`repeat_title_quote`)
· hook: Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

## §5 LUẬT CỨNG (đọc khi soi bản khoá/bản anh sửa)
1. Hậu quả đến từ CƠ CHẾ (xét chọn リーダー/主任, không gia hạn hợp đồng, phỏng vấn trượt) — không mắng, không trả thù, không hả hê.
2. Câu cửa miệng đúng 3 lần, lần 3 trong chuyện đời hắn; câu CUỐI lặp câu cửa miệng với nghĩa đổi (tự viết, không chép câu kết video gốc).
3. Mỗi lần câu cửa miệng: 1 người tốt CỤ THỂ gánh thay, cho thấy bằng chi tiết đời thường.
4. Cụ già/người nhà không vô lý; cụ tối đa ヒヤリハット. Nghiệp vụ 介護 đúng [Dn].
5. Mỗi lượt thoại mới phải rõ ai nói.
6. Ảnh: không cảnh ngã/thương tích/trói/tắm lộ thân; nhân viên mặc đồng phục chăm sóc/áo polo, không áo blouse trắng (trừ y tá).

## §9 BẪY
Xem bảng bẫy `SOP_LANE_K.md` §9 (cùng kỹ thuật). Riêng Lane O: nhạc nền đang mượn `assets\yakkyoku-sukatto\_bgm\bgm_lane_k.mp3`
(`--bundle` tự chép cho máy 2); nút đăng ký TẮT tới khi có kênh + avatar `assets\avatars\kaigo-sukatto.png`.
