# DANH BẠ LANE — ai là ai, gọi đúng tab, vào đúng thư mục

> Dự án `h2dev` chạy **nhiều tab chat song song, mỗi tab một kênh**. File này là **danh bạ**: tab nào
> phụ trách kênh nào, làm việc trong thư mục nào, chạy theo runbook nào.
>
> Lập 2026-09-11 sau khi phát hiện router trong `CLAUDE.md` chỉ sai profile cho lane satori (trỏ vào
> `Lopezzapa68` — một lane KHÁC) và bỏ sót profile Lane D do tab khác vừa tạo. Vào nhầm lane không
> báo lỗi gì cả: nó chạy trót lọt rồi hỏng ở sản phẩm cuối.

---

## 1. MÃ LANE = `id` TRONG PROFILE. ĐỊA CHỈ = `slug_dir`.

Không đặt mã mới. Hai thứ này **đã có sẵn** trong `profiles/profiles/<mã>.json`, code đã dùng chúng
để rẽ nhánh, nên không thể lệch nhau:

| Mã lane (`id`) | Tên kênh / ngách | Thư mục làm việc (`slug_dir`) | Runbook |
|---|---|---|---|
| `Lopezzapa68` | Sức khoẻ người già Nhật — kể chuyện đời cá nhân ngôi 1 | `assets/out/` | ⚠️ chưa có SOP riêng |
| `teinengo-real` | 定年後のリアル (Lane F) — hưu trí Nhật, manga story kịch tính tiền, 2 nhân vật đối lập | `assets/teinengo-real/` | `docs/BAT_DAU_LANE/teinengo-real.md` + `docs/SOP_LANE_F.md` (giai đoạn 2 xong 2026-09-20) |
| `teinengo-tanoshimi` | 定年後の楽しみ方 (Lane G) — hưu trí Nhật, manga list N選 lối sống vui/rẻ | `assets/teinengo-tanoshimi/` | `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` (cửa vào) · `docs/SOP_LANE_G.md` |
| `kokoro-kazoku` | 心の家族学 (Lane H) — tâm lý gia đình người già Nhật, illustration ấm + narration | `assets/kokoro-kazoku/` | `docs/BAT_DAU_LANE/kokoro-kazoku.md` (SOP chưa viết — giai đoạn 2) |
| `sengoku-uragawa` | 戦国の裏側 (Lane I) — lịch sử Chiến quốc Nhật, manga chibi, lật huyền thoại bằng sử liệu | `assets/sengoku-uragawa/` | `docs/BAT_DAU_LANE/sengoku-uragawa.md` (SOP chưa viết — giai đoạn 2) |
| `teinengo-fuufu` | 定年後の夫婦のカタチ (Lane J) — vợ chồng sau hưu trí Nhật, manga cảm xúc | `assets/J-teinengo-fuufu/` | `docs/BAT_DAU_LANE/teinengo-fuufu.md` · `docs/SOP_LANE_J.md` (2026-09-30; tên kênh mới J-rougo_futari, mã lane đổi sau) |
| `yakkyoku-sukatto` | 薬局スカッと帳 (Lane K) — công sở/nghề nghiệp Nhật, dược sĩ quả báo, clone 千種テンカ | `assets/yakkyoku-sukatto/` | `docs/BAT_DAU_LANE/yakkyoku-sukatto.md` (cửa vào) · `docs/SOP_LANE_K.md` |
| `shakai_no_naze` | 社会のなぜ研究室 (Lane L) — xã hội/tâm lý xã hội Nhật, giải thích bằng số liệu, clone 社会のウラガワ | `assets/shakai_no_naze/` | `docs/BAT_DAU_LANE/shakai_no_naze.md` (cửa vào) · `docs/SOP_LANE_L.md` |
| `teinengo-anaba` | 定年後の穴場ノート【漫画】 (Lane M) — hưu trí Nhật, manga N選 việc làm thêm/tái tuyển dụng tuổi 60, clone 大人の盲点 @otonanomouten | `assets/M-teinengo-anaba/` (tab `M-teinengo-anaba`) | `docs/BAT_DAU_LANE/teinengo-anaba.md` (cửa vào) · `docs/SOP_LANE_M.md` (runbook 2026-09-26) |
| `senior_korekara` | シニアの人生これから (Lane N) — đời sống người Nhật 60–70 tuổi **sau khi nghỉ việc**, manga ảnh AI + narration ĐA GIỌNG (3 clone), mỗi tập một nhân vật mới, kết **nghiệm tùng**, clone @senior_korekara | `assets/N-senior_korekara/` (tab `Lane-N`) | `docs/BAT_DAU_LANE/senior_korekara.md` (cửa vào) · `docs/SOP_LANE_N.md` (runbook, 2026-09-30) |
| `kaigo-sukatto` | 介護スカッと (Lane O, tên tạm, CHƯA CÓ KÊNH) — manga công sở ngành chăm sóc người cao tuổi, nhân viên có câu cửa miệng xấu nhận quả từ cơ chế, cùng kênh mẫu 千種テンカ với Lane K, đa giọng VOICEVOX | `assets/O-kaigo-sukatto/` (tab `Lane-O`) | `docs/BAT_DAU_LANE/kaigo-sukatto.md` (cửa vào) · `docs/SOP_LANE_O.md` (2026-09-30) |

**Cách xưng hô giữa các tab:** `@lane:<mã>`. Ví dụ `@lane:teinengo-real`. (Lane Satori `satori-jp-obaa` đã BỎ 17/10/2026.)
Mỗi tab mở đầu báo cáo bằng mã của mình, để nhìn là biết ngay đang đứng ở đâu.

**Tuyệt đối không dùng thư mục tổng `E:\CLAUDE\YOUTUBE\h2dev` làm địa chỉ khi giao việc** — mọi lane
đều nằm trong đó, nói vậy là không chỉ được ai. Luôn dùng đường dẫn đầy đủ tới `slug_dir` của lane.

## 2. TRA MÃ BẰNG MÁY (đừng nhớ bằng đầu)

```bat
py -3.13 -c "import json,glob,os; [print('%-22s %-30s %s' % (json.load(open(f,encoding='utf-8')).get('id'), json.load(open(f,encoding='utf-8')).get('slug_dir'), os.path.basename(f))) for f in glob.glob(r'E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\*.json')]"
```
Danh bạ này có thể cũ; **profile là nguồn chân lý**. Lệch nhau thì tin profile, rồi sửa file này.

## 3. GIAO VIỆC GIỮA CÁC TAB

Cần tab khác làm gì thì ghi vào hòm thư của lane đó:

```
E:\CLAUDE\YOUTUBE\h2dev\docs\lane_inbox\<mã lane>.md
```

Mỗi mục một khối, theo khuôn:

```markdown
## [2026-09-11 · từ @lane:teinengo-real] <việc cần làm, một dòng>
- Bối cảnh: ...
- Cần gì cụ thể: ...
- File liên quan (đường dẫn ĐẦY ĐỦ): ...
- Trạng thái: MỚI | ĐANG LÀM | XONG
```

Tab nhận việc đọc hòm thư của mình khi bắt đầu phiên, làm xong thì đổi `Trạng thái: XONG` và ghi
kết quả ngay dưới — **không xoá mục cũ** (lịch sử giao việc là thứ để truy khi sai).

## 4. LUẬT CHỐNG LẪN LANE (đã có từ trước, nhắc lại)

1. `profiles.rate_measured()` + `gate_declared()` — lane chưa đo char-rate riêng hoặc chưa khai
   `script.gate` riêng thì pipeline **DỪNG**, không mượn số của lane khác.
2. `profile.body.mode` (`ai_images` | `stock_clips`) là **ngã rẽ DUY NHẤT** giữa các lane trong code.
   Cấm `if profile_id == ...` ở bất cứ đâu khác — khác biệt nào cũng phải thành field trong profile.
3. Lệnh của anh mà không rõ lane → **HỎI**, đừng đoán.

## 5. VIỆC CÒN TREO

- `CLAUDE.md` router: đã sửa lại cho trỏ đúng mã lane (2026-09-11).
- `Lopezzapa68` (ngách sức khoẻ người già) — cần xác nhận còn dùng hay đã bỏ; `slug_dir` của nó là
  `assets/out`, tên thư mục quá chung, nên đổi thành `assets/lopezzapa68` nếu còn chạy.
- **2026-09-29: Lane A (`toshi-densetsu-jp`), D (`irogatatarukioku`), E (`kenko-chiebukuro`) đã BỎ** —
  xoá toàn bộ assets/profile/SOP/channel_dna. Mã A/D/E không tái dùng cho lane mới.
