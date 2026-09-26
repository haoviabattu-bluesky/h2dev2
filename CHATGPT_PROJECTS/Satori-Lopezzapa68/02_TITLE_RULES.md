# 02 TITLE RULES — Satori-Lopezzapa68 · satori-jp-obaa

> Lane `satori-jp-obaa`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 40 · tối đa 48 · tối thiểu - · cảnh báo phần đầu 28
- prefix cố định: `` · suffix cố định: ``

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE SATORI (悟り系, cụ bà/cụ ông kể chuyện đời, khán giả 60-80 xem điện thoại) — chốt 2026-09-20:
1. ĐỘNG TỪ CÓ SỰ CỐ: 漏らした・うっかり明かした・バレた・笑われた・外された・消えた・終わった・切られた・届いた・解散 thay cho
   言った/口にした/話した trung tính. Phải đúng kịch bản (xem khong_duoc_noi_qua); kịch bản tự gọi là lỡ lời/hối hận thì 漏らした đúng sắc thái.
2. HẬU QUẢ CỤ THỂ: nói rõ thứ đã mất/đã xảy ra (40年の会が解散, LINE誤送信の一行, 写真16枚に私はいない) — CẤM kết bằng
   目が変わった/後悔/真実/教訓 đứng một mình.
3. ĐÚNG 1 MẢNH BỊ GIẤU: mở bằng 理由/なぜ/一行/正体 hoặc dấu … trước mảnh bị giấu; không lộ twist.
4. NHÂN VẬT CÓ VAI + CƯỢC CỤ THỂ: 73歳の元惣菜屋 / 40年の仲間 / 50年の親友 + con số (年金25万・50万円・3年).
5. ĐỘ DÀI: 30–40 ký tự (điện thoại hiện ~2 dòng), tối đa 48, móc trọn trong 28 ký tự đầu. Dữ liệu: 31–40 ký tự có views gấp đôi 41–50.
6. Bản bị anh loại làm mẫu xấu: 「年金「月25万円」と口にした途端、40年来の仲間の目が変わった…73歳の後悔」 — động từ trung tính,
   hậu quả mơ hồ, cảm xúc chung chung.

7. LUẬT SỐ (anh chốt 2026-09-23): mọi lượng viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 — KHÔNG viết 四十年, 二十五万,
   七十三歳 (thành ngữ 一言/一行/十分 giữ nguyên). Tool tự đổi ở bước lock nếu quên.
8. TIÊU ĐỀ VÀ THUMBNAIL PHẢI BÁN CÙNG MỘT XUNG ĐỘT (anh chốt 2026-09-23): chia vai, không lặp nguyên văn, nhưng phải
   cùng một biến cố/tuyến truyện. Ep01 dính đúng lỗi này (title bán 年金25万+LINE, thumb bán 親友が3年前に引っ越した) → CTR 2,3%.
9. Ưu tiên xung đột có SỚM trong video (cold open). Payoff nằm cuối video thì người xem rơi ở phút đầu (ep01 AVD 1:04/31:25).
10. CÔNG THỨC 2 VẾ CỦA KÊNH GỐC (đo thật 26 tiêu đề 노년의 마음소리, xem docs/lanes/satori-jp-obaa/CONG_THUC_TIEU_DE_KENH_GOC.md):
    VẾ 1 = sự việc/nghịch lý/câu hỏi cụ thể có con số hoặc mốc tuổi · `…` · VẾ 2 = LỜI HỨA NGƯỜI XEM HỌC ĐƯỢC GÌ
    (老後に言ってはいけない4つのこと / 〜した理由 / 〜が遺した一言). Tiêu đề chỉ có vế 1 = mới xong một nửa công thức.
    Đòn bẩy đo được: câu hỏi/từ để hỏi (lift 2,99) · lệnh cấm tuyệt đối 絶対に〜てはいけない (2,70) · dấu … (1,32).
    「N つのこと」 ĐỨNG MỘT MÌNH KHÔNG ăn (lift 0,34) — chỉ mạnh khi nằm ở vế 2 sau một vế 1 có nghịch lý/lệnh cấm.
Tự kiểm: "Cụ bà 70 tuổi lướt YouTube trên điện thoại, đọc 2 dòng này, có bấm không? Thiếu mảnh gì?" — ghi vào ly_do_bam.

### fear_words
```
[
 "衝撃",
 "暴露",
 "残酷",
 "地獄",
 "悲劇",
 "末路",
 "貧乏",
 "破綻"
]
```

### separators_ok
False

### ctr_hint
Có động từ SỰ CỐ (漏らした/笑われた/外された/消えた…) thay vì
   言った/口にした? Có HẬU QUẢ CỤ THỂ thay vì 目が変わった/後悔/真実 chung chung? Có đúng 1 mảnh bị giấu để hỏi "rồi sao"?
   Tiêu đề chỉ tường thuật (kể lại chuyện gì xảy ra, không giấu gì, không cược) → ctr ≤ 4.

### brevity_hint
ý quan trọng trong ≤{head_warn} ký tự đầu? tổng ≤{target_chars} (điện thoại chỉ hiện ~{target_chars} ký tự)? Quá {max_chars} = 0 điểm và KHÔNG được chọn.

### length_block
ĐỘ DÀI (luật cứng, đo từ dữ liệu — khán giả xem bằng ĐIỆN THOẠI, app chỉ hiện ~2 dòng ≈ {target_chars} ký tự tiếng {lang}
rồi cắt "…"): TỔNG {target_min}–{target_chars} ký tự, TUYỆT ĐỐI không quá {max_chars}. Cú móc + cược cụ thể phải trọn vẹn
trong {head_warn} ký tự đầu. Không dùng 2 vế dài nối bằng "…" rồi thêm vế thứ 3 — một tiêu đề = MỘT lời hứa.
Dữ liệu: 31–40 ký tự có views gấp đôi 41–50, gấp 4 lần 61–80; tiêu đề thắng thật dài 32/34/37 ký tự.

## Nhịp hook kênh mẫu (tiêu đề phải khớp lời hứa hook)
- 0–10s Câu thoại nghịch lý: Người trong cuộc nói điều trái lẽ, hoặc người kể tự thú hành động lạ
- 10–25s Lật thêm một lần: Câu thứ hai làm câu đầu khó hiểu hơn
- 15–30s Giới thiệu 1 câu: Tuổi, tên, nơi ở, sống một mình bao năm
- 25–50s Hứa đúng lời tiêu đề + điều cuối khó nói: Đọc lại tiêu đề thành N điều, nhử điều cuối
- 35–60s Hỏi thẳng khán giả: Hỏi về chính cuộc sống người xem rồi 'chuyện bắt đầu từ…'

---
## CÔNG THỨC TIÊU ĐỀ KÊNH GỐC (tài liệu lane)

# Công thức tiêu đề của KÊNH GỐC — UCfB0fkB_giLFFZsmQmWgBWw

Đo bằng máy trên 20 tiêu đề thật (view trung bình nhân 165,019).
Lift = view trung bình nhân của nhóm CÓ đặc trưng chia cho nhóm KHÔNG có. Lift > 1,3 là đáng bắt chước.

| Đặc trưng | Số video có | gmean CÓ | gmean KHÔNG | Lift |
|---|---|---|---|---|
| câu hỏi / từ để hỏi | 4/20 | 396,191 | 132,569 | **2.99** |
| lệnh cấm / tuyệt đối | 3/20 | 383,882 | 142,177 | **2.7** |
| dấu … cắt câu giữa chừng | 14/20 | 179,394 | 135,799 | **1.32** |
| tuổi cụ thể (65세, 73세) | 5/20 | 165,035 | 165,014 | **1.0** |
| số tiền cụ thể | 2/20 | 118,322 | 171,232 | **0.69** |
| hậu quả nặng / mất mát | 9/20 | 117,673 | 217,615 | **0.54** |
| trích lời thoại trong ngoặc | 5/20 | 93,125 | 199,690 | **0.47** |
| người trong nghề tiết lộ | 5/20 | 83,792 | 206,844 | **0.41** |
| có bất kỳ con số nào | 16/20 | 134,364 | 375,437 | **0.36** |
| …N điều/N kiểu — hứa bài học đếm được | 6/20 | 76,845 | 228,973 | **0.34** |

## Toàn bộ tiêu đề (view giảm dần)

| View | Tiêu đề |
|---|---|
| 1,000,000 | 연금 310만 원을 말한 뒤 40년 계모임이 깨졌습니다… 노후에 말하면 안 되는 4가지 |
| 725,000 | 만약 어느 날 갑자기 세상을 떠난다면… 은행 예금 전액을 자녀가 받을 수 있을까? 은행 지점장이 밝힌 충격적인 진실 |
| 669,000 | 요양원에서 진짜 무서운 건 학대가 아니었습니다… 74세 노인이 석 달을 못 버티고 짐을 싼 이유 |
| 657,000 | 60세 이후, 절대 가까이하면 안 되는 여자 4부류… 잘못 만나면 말년이 처참합니다 |
| 536,000 | The astonishing answer an 81-year-old gave when her children asked, "How much money is in your ba... |
| 478,000 | 70세가 넘은 여성들이 여전히 남자를 찾는 진짜 이유… 예상 밖이었습니다 |
| 431,000 | 나이 들수록 예금은 어디에 둬야 할까? 73세 노인의 방법이 너무 현명했습니다 |
| 415,000 | 노년 재혼·동거, 무엇이 가장 무서울까요? 직접 겪은 세 사람의 이야기｜많은 분들이 "진작 볼 걸" 후회합니다 |
| 327,000 | 부모님이 오래 살수록 자식의 삶까지 무너질 수 있습니다. 부모와 함께 지옥으로 끌려가지 않으려면 절대 잊지 말아야 할 3가지 |
| 319,000 | 【Warning from a Former Banker】Stop doing this immediately if you still keep your money here after... |
| 241,000 | 나이 들어 돈이 있다면 가장 먼저 사야 할 3가지… 늦으면 반드시 후회합니다 |
| 207,000 | 죽기 한 달 전부터 몸에 나타나는 변화｜간호사가 알려줬습니다 |
| 190,000 | 70세를 막 넘겼는데 몇 년 안 돼 세상을 떠나는 노인이 많습니다… 대체 왜일까요? |
| 173,000 | "절대 장례식을 치르지 마라" 갈수록 늘어나는 노인들의 유언… 장례지도사가 털어놓은 가슴 찢어지는 3가지 진실 |
| 155,000 | 65세에 ‘이만큼의 돈’이 있는 사람은… 노후의 승자입니다｜이 기준, 놀랄 만큼 정확합니다 |
| 37,000 | 15년 경력 요양보호사의 고백, 편안히 떠난 어르신들이 끝까지 지킨 두 가지 |
| 20,000 | 일흔이 넘어서야 알았습니다... 자식에게 이 4가지를 해주면, 돈이 아무리 많아도 노후가 무너집니다 |
| 14,000 | "노후에 10억 필요 없습니다" 돈 없이도 평안하게 늙어가는 사람들의 3가지 공통점 |
| 13,000 | 70세가 넘으면 '진짜 지옥'이 시작됩니다... 아무도 피해갈 수 없는 노년의 4가지 비극 |
| 4,300 | [충격] 차라리 집에서 죽을란다... 10년 차 요양보호사가 폭로한 요양원의 참혹한 진실 |

## Đọc số cho đúng (bẫy tuổi video)
6 video MỚI NHẤT của kênh (30k–101k view) chưa đủ tuổi để so — bảng trên đã bỏ chúng ra. Nếu để lại thì
đặc trưng nào hay xuất hiện ở video mới cũng bị chấm oan là "tiêu đề dở".

## Công thức THẬT của kênh gốc (đọc từ 10 video top, không phải suy diễn)

Mỗi tiêu đề thắng đều gồm **2 VẾ nối bằng `…`**:

```
VẾ 1: sự việc/nghịch lý/câu hỏi CỤ THỂ (có con số hoặc mốc tuổi)
   …
VẾ 2: LỜI HỨA NGƯỜI XEM HỌC ĐƯỢC GÌ (N điều cấm / lý do thật / sự thật bị giấu)
```

| View | VẾ 1 | VẾ 2 |
|---|---|---|
| 1.000.000 | Nói ra lương hưu 3,1 triệu won → hội 40 năm tan vỡ | **4 điều không được nói khi về già** |
| 725.000 | Nếu đột ngột qua đời… con có nhận được toàn bộ tiền gửi không? | sự thật sốc do **giám đốc chi nhánh ngân hàng** tiết lộ |
| 669.000 | Thứ đáng sợ ở viện dưỡng lão **không phải** là ngược đãi | **lý do** cụ 74 tuổi chưa đầy 3 tháng đã dọn đồ về |
| 657.000 | Sau 60 tuổi, **tuyệt đối không được** lại gần 4 kiểu phụ nữ | gặp nhầm thì cuối đời thê thảm |
| 478.000 | Vì sao phụ nữ ngoài 70 vẫn đi tìm đàn ông | **lý do thật** — ngoài dự đoán |
| 431.000 | Càng già thì gửi tiền ở đâu? | cách của cụ 73 tuổi khôn ngoan đến mức nào |

Ba thứ kéo view mạnh nhất (đo bằng máy): **câu hỏi/từ để hỏi (lift 2,99)** · **lệnh cấm tuyệt đối (2,70)** ·
**dấu `…` cắt giữa câu (1,32)**.

**"N điều" một mình KHÔNG cứu được tiêu đề** (lift 0,34): 3/6 video thua nhất đều có N điều. Nó chỉ mạnh khi
đứng ở VẾ 2 SAU một VẾ 1 có nghịch lý/lệnh cấm (video 1 triệu: `…노후에 말하면 안 되는 4가지`).

## 5 mẫu chuyển sang tiếng Nhật cho lane satori

| Mẫu | Khuôn | Ví dụ |
|---|---|---|
| A — sự việc + điều cấm N mục | `{sự việc có số}…{老後に言ってはいけない}N{つのこと}` | `年金「月25万」と答えた日、40年の講が消えた…老後に言ってはいけない4つのこと` |
| B — giả định + câu hỏi có/không | `もし{tình huống}たら…{câu hỏi}のでしょうか` | `夫が先に逝ったら…通帳のお金は本当に妻のものでしょうか` |
| C — phủ định kỳ vọng | `{nơi/việc}で本当に怖いのは{X}ではありませんでした…{lý do}` | `特養で本当に怖いのは虐待ではなかった…元看護婦が遺した四文字` |
| D — mốc tuổi + cấm tuyệt đối | `{N}歳を過ぎたら、絶対に{hành động}てはいけない{N}つの{loại}` | `70歳を過ぎたら、絶対に話してはいけない3つのこと` |
| E — câu hỏi tiền/quan hệ + người trả lời | `{câu hỏi}？{tuổi}歳の{người}の答えが{đánh giá}` | `老後のお金はどこに置く？73歳の元郵便屋の答えが賢すぎた` |

**Luật rút ra cho lane:** tiêu đề chỉ kể CÂU CHUYỆN (vế 1) mà không hứa NGƯỜI XEM HỌC ĐƯỢC GÌ (vế 2) là thiếu
một nửa công thức của kênh gốc. Kênh mình đang mắc đúng lỗi này — ep01 bản gốc đã bỏ mất vế
`노후에 말하면 안 되는 4가지` của video 1 triệu view mà thay bằng một sự việc thứ ba.

<!-- export a6309bdfb1be · 2026-09-26 -->
