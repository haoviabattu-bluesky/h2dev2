# FILE BÀN GIAO STOCK MEDIA — SATORI EP1

> Mục đích: giao cho dự án chính dùng video/ảnh thật làm B-roll khi dựng `simbot2-01-vU5PWT2zLDs`. 
> **Phạm vi:** chỉ bàn giao asset và metadata; không sửa code cũ, không thay `script.txt`, `img_prompts.txt`, `img/` hoặc master REF-LOCK.

## 1. Kết quả đã xác minh

- Tập: `simbot2-01-vU5PWT2zLDs`
- Thư mục asset: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-01-vU5PWT2zLDs\stock`
- Manifest: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-01-vU5PWT2zLDs\stock\manifest.csv`
- Tổng: **38 scene stock** — **33 video**, **5 ảnh tĩnh**.
- Nguồn: Pexels; license ghi theo từng record trong manifest.
- Độ phân giải: toàn bộ asset đạt từ 1920px ngang trở lên; video đều landscape.
- Kiểm tra file: 38/38 record `OK`, 38/38 file tồn tại trên đĩa, không trùng `asset_id`.

## 2. Quy tắc dùng khi dựng

1. Dùng stock cho đúng `prompt_line`/scene được chỉ định bên dưới; không tự đổi sang scene có `@REF`/`@REF2`.
2. Cảnh có nhân vật REF-LOCK hoặc cần đúng mặt/biểu cảm vẫn bắt buộc dùng ảnh AI trong `img/`; stock chỉ là B-roll.
3. Video stock phải cắt theo thời lượng neo của scene, không kéo một clip quá lâu. Nếu scene cần dài hơn clip, dùng nhiều góc/asset khác, không lặp vô hạn một đoạn.
4. Ảnh tĩnh stock cần pan/zoom nhẹ; không nhân bản thành nhiều scene.
5. Giữ subtitle/voice timing theo script hiện tại. Stock chỉ thay hình, không thay cue lời.
6. Có thể color-grade nhẹ để footage thật hòa với ảnh AI; không làm mất chi tiết hoặc đổi nội dung.

## 3. Mapping scene → asset

| Prompt line | Loại | File cục bộ | Thời lượng | Kích thước | Nội dung/ghi chú |
|---:|---|---|---:|---|---|
| 2 | video | `stock/L002_pexels_suburbanjapanesestreetonaclearday3511117.mp4` | 12s | 1920×1080 | video_id:35111174 |
| 5 | video | `stock/L005_pexels_autumnyellowmapleleafflutterslonelyinthe.mp4` | 14s | 2048×1080 | video_id:19537974 |
| 11 | image | `stock/L011_pexels_facadeofasmallclosedstore22882019.jpg` | ảnh | 6240×4160 | japanese shop shutter closed |
| 13 | video | `stock/L013_pexels_traditionaljapanesehouseinterior31387301.mp4` | 8s | 1920×1080 | video_id:31387301 |
| 14 | video | `stock/L014_pexels_anemptybench8301731.mp4` | 17s | 1920×1080 | video_id:8301731 |
| 15 | image | `stock/L015_pexels_ahandnearaglassonawoodensurface11713103.jpg` | ảnh | 7952×5304 | spilled water wooden floor |
| 16 | video | `stock/L016_pexels_slowdripmetalfaucetc.mp4` | 20s | 1920×1080 | kitchen sink dripping water tap |
| 17 | image | `stock/L017_pexels_rainyschoolplaygroundinsetagayatokyo2924.jpg` | ảnh | 6240×4160 | japanese school building gate |
| 18 | video | `stock/L018_pexels_aerialviewofgovernmentbuildingatsunset32.mp4` | 6s | 1920×1080 | video_id:32790345 |
| 20 | video | `stock/L020_pexels_tranquilnarrowstreetintraditionaljapanes.mp4` | 5s | 1920×1080 | video_id:37420657 |
| 24 | video | `stock/L024_pexels_asewingmachineisbeingusedinafactory46224.mp4` | 19s | 2048×1080 | video_id:4622442 |
| 35 | video | `stock/L035_pexels_abowlofnoodles810757.mp4` | 11s | 2048×1080 | soba noodle bowl steam chopsticks |
| 37 | video | `stock/L037_pexels_cozywinterteaexperiencewithagoodbook2987.mp4` | 10s | 1920×1080 | video_id:29875836 |
| 42 | video | `stock/L042_pexels_deliciousjapaneseram.mp4` | 11s | 1920×1080 | ramen broth green onion steam close up |
| 43 | video | `stock/L043_pexels_personstirringacupof.mp4` | 27s | 1920×1080 | spoon stirring coffee cup cream |
| 47 | video | `stock/L047_pexels_vibrantnightlifearou.mp4` | 14s | 1920×1080 | japanese vending machine night |
| 52 | image | `stock/L052_pexels_entrancetorailwaystationintokyo22882159.jpg` | ảnh | 6240×4160 | japanese public building entrance |
| 54 | video | `stock/L054_pexels_puttingcashtoenvelop.mp4` | 21s | 1920×1080 | envelope money cash hand close up |
| 56 | video | `stock/L056_pexels_japaneselanternhangingbythestoreentrance.mp4` | 8s | 1920×1080 | video_id:3177520 |
| 62 | video | `stock/L062_pexels_highangleviewofakitc.mp4` | 13s | 1920×1080 | kitchen sink night water running |
| 65 | video | `stock/L065_pexels_apileoflettersonatable6306128.mp4` | 8s | 1920×1080 | video_id:6306128 |
| 67 | video | `stock/L067_pexels_videoofadentalclinic.mp4` | 15s | 1920×1080 | empty clinic examination room |
| 68 | video | `stock/L068_pexels_apersontakingoutanotefromanenvelope68516.mp4` | 24s | 2048×1080 | video_id:6851679 |
| 74 | video | `stock/L074_pexels_personpinningpaperon.mp4` | 19s | 2048×1080 | bulletin board pinned photos wall |
| 83 | video | `stock/L083_pexels_nightviewofasianrestaurantwithlanterns32.mp4` | 9s | 1920×1080 | video_id:32201483 |
| 86 | video | `stock/L086_pexels_closeupshotofusingchopsticksonnoodlesoup.mp4` | 9s | 1920×1080 | video_id:6645673 |
| 87 | video | `stock/L087_pexels_ignitingahandheldsti.mp4` | 13s | 2048×1080 | birthday cake candle lit small |
| 90 | video | `stock/L090_pexels_aringingvintagetelep.mp4` | 6s | 1920×1080 | vintage landline telephone old phone |
| 92 | video | `stock/L092_pexels_facadeofamultistoreyapartment4693666.mp4` | 17s | 1920×1080 | video_id:4693666 |
| 93 | video | `stock/L093_pexels_closeupshotofahumanh.mp4` | 25s | 2048×1080 | elderly hand sweater sleeve fabric close up |
| 102 | video | `stock/L102_pexels_greywoolfabric7792708.mp4` | 13s | 1920×1080 | video_id:7792708 |
| 103 | video | `stock/L103_pexels_aroomwithmanyboxeson.mp4` | 8s | 2048×1080 | empty room floor moving boxes keys |
| 104 | video | `stock/L104_pexels_handholdingkeysovermoneyandminihousemode.mp4` | 15s | 1920×1080 | video_id:31400388 |
| 105 | video | `stock/L105_pexels_traditionalkyotostreetwithwoodenhouses32.mp4` | 8s | 1920×1080 | video_id:32111766 |
| 108 | video | `stock/L108_pexels_efficientsurfacecleaningwithspraybottle3.mp4` | 21s | 2048×1080 | video_id:32727110 |
| 110 | image | `stock/L110_pexels_boxesonwallinsideroom2302995.jpg` | ảnh | 5460×3640 | small japanese room interior night |
| 113 | video | `stock/L113_pexels_tranquilbambooforestinsunlight31387305.mp4` | 6s | 1920×1080 | video_id:31387305 |
| 118 | video | `stock/L118_pexels_aparkbenchinthefallwithleavesontheground.mp4` | 10s | 1920×1080 | video_id:19456234 |

## 4. Nguồn và bản quyền

- Tất cả record hiện tại: **Pexels License** — `https://www.pexels.com/license/`.
- `source_url`, creator, ngày tải, loại media và dung lượng nằm trong `stock/manifest.csv`.
- Khi xuất bản, vẫn kiểm tra lại license tại thời điểm sử dụng; nếu cần credit thì lấy tên creator từ manifest.
- Không phân phối lại asset như một gói stock độc lập; asset được dùng như thành phần của video có voice-over, script, subtitle và dựng mới.

## 5. Cách dự án chính nhận asset

1. Đọc file này và `stock/manifest.csv` trước.
2. Dựng thử ở thư mục output riêng, không ghi đè `assets/satori_jp/simbot2-01-vU5PWT2zLDs/img/`.
3. Cần một bước tích hợp riêng để timeline có thể đọc cả `.mp4` và `.jpg`; bản `assemble.py` Satori hiện tại đang quét ảnh `.png`, vì vậy **không được tự coi thư mục `stock/` là đầu vào tương thích ngay**.
4. Với mỗi prompt line có stock, map file theo `prompt_line`; với các line không có stock, tiếp tục dùng ảnh AI đánh số hiện hành.
5. Sau khi dựng, kiểm tra: không khung đen, đúng voice cue, đúng nội dung scene, subtitle không đổi, stock không có logo/chữ gây hiểu sai.

## 6. Cấm thay đổi

- Không sửa bất kỳ file nào trong `pipeline/` trong phạm vi bàn giao này.
- Không sửa hoặc xóa `script.txt`, `img_prompts.txt`, `img_doan.txt`, `anchors.txt`, `characters.json`, `_ref/`, `_ref_mitsue/`, `img/`.
- Không thay stock vào scene nhân vật chỉ vì asset có người tương tự; nhân vật REF-LOCK phải giữ ảnh AI.

## 7. Trạng thái bàn giao

**ĐÃ SẴN SÀNG CHO DỰ ÁN CHÍNH DÙNG Ở GIAI ĐOẠN DỰNG THỬ.**
Chưa chạy dựng lại video và chưa thay đổi pipeline.
