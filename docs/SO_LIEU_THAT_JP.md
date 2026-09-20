# DỮ LIỆU THẬT — NHẬT BẢN (dùng khi viết kịch bản, cấm quy đổi/phỏng đoán từ bản gốc)

> **Phạm vi (anh chốt 2026-09-11): KHÔNG CHỈ TIỀN.** Mọi chi tiết đời thật trong kịch bản — thủ tục hành chính, thuật ngữ y tế, lịch chi trả, phong tục, địa danh, giá cả — đều phải **tra được**. Chi tiết nào không tra được thì **viết mờ đi hoặc bỏ hẳn**, tuyệt đối không bịa cho "nghe hợp lý": một chi tiết mơ hồ mà đúng còn hơn một chi tiết cụ thể mà sai.

> **Vì sao có file này.** Đo thật 2026-09-11: bộ não nhân bản kịch bản Hàn → Nhật bằng cách **chia
> con số tiền cho 10** — `130만원 → 十三万円`, `82만원 → 八万二千円`, `3.000만원 → 三百万円`. Soi lại
> toàn dự án thấy **14 dấu vết** kiểu này, có cả trong video đã dựng xong. Đây là **dấu vân tay của
> bản sao chép**: khán giả Nhật nhìn mức lương hưu/viện phí là biết ngay không phải chuyện Nhật.
>
> **Luật (user chốt 2026-09-11):** số tiền phải là **DỮ LIỆU THẬT** — tra trong file này, không có
> thì **WebSearch** rồi ghi bổ sung vào đây kèm nguồn + ngày tra. TUYỆT ĐỐI không quy đổi theo tỉ giá,
> cũng không bịa số "cho hợp lý".
>
> Máy soi tự động: `py -3.13 pipeline\qc_tien.py --script <script.txt> --competitor <competitor.txt>`
> (tất định, 1 giây, 0 đồng — đã nối vào cổng B3Q làm tầng 0).

---

## Lương hưu (年金)

| Khoản | Mức thật | Nguồn · ngày tra |
|---|---|---|
| 老齢基礎年金 **満額** (năm tài khoá 2025) | **69.308 円/tháng** | Bộ Y tế–Lao động–Phúc lợi, +1.308円 (+1,9%) so năm trước · 2026-09-11 |
| 国民年金 **bình quân thực nhận** | **57.700 円/tháng** | 令和5年度 厚生年金保険・国民年金事業の概況 · 2026-09-11 |
| 国民年金 **tiền đóng** (từ 4/2025) | **17.510 円/tháng** | +530円 so năm trước · 2026-09-11 |
| **遺族厚生年金** vợ 65+ (夫平均標準報酬 30万) | **月額 約3万1千円** (年37万) | moneiro.jp · 2026-09-12 |
| **遺族厚生年金** vợ 65+ (夫平均標準報酬 40万) | **月額 約4万2千円** (年50万) | moneiro.jp · 2026-09-12 |
| Goá phụ điển hình (老齢基礎満額 + 遺族厚生 30万給与dạng) | **月額 8–10万円** | tổ hợp bảng trên · 2026-09-12 |

⚠️ Người chỉ có 国民年金 thì **dưới 7 万円/tháng** — đây là mức của đa số cụ bà goá trong ngách này.
Muốn cao hơn phải giải thích bằng 厚生年金 (từng đi làm công ty) hoặc 遺族年金.

## Viện dưỡng lão (老人ホーム)

| Loại | Phí vào | Phí tháng | Nguồn · ngày tra |
|---|---|---|---|
| 特別養護老人ホーム (特養, công lập) | **0 円** | **10–15 万円** | 2026-09-11 |
| 住宅型有料老人ホーム | có | bình quân **16,7 万円** · trung vị **14,1 万円** | 2026-09-11 |
| Bình quân toàn quốc mọi loại | — | **26,6 万円** | LIFULL 介護 · 2026-09-11 |

## デイサービス (通所介護) — 要介護度別 tự trả 1割/tháng

| 要介護度 | 支給限度額 (đơn vị) | Tự trả 1割/tháng khi dùng gần trần | Nguồn · ngày tra |
|---|---|---|---|
| 要支援1 | 5,032 | ~5,032 円 | rehab.cloud · 2026-09-16 |
| 要支援2 | 10,531 | ~10,531 円 | rehab.cloud · 2026-09-16 |
| 要介護1 | 16,765 | ~16,765 円 | rehab.cloud · 2026-09-16 |
| 要介護2 | 19,705 | ~19,705 円 | rehab.cloud · 2026-09-16 |
| **要介護3** | **27,048** | **~15,000–27,000 円** (thường + 食費 ~600円/lần) | rehab.cloud · sompo · 2026-09-16 |
| 要介護4 | 30,938 | ~30,938 円 | rehab.cloud · 2026-09-16 |
| 要介護5 | 36,217 | ~36,217 円 | rehab.cloud · 2026-09-16 |

⚠️ 週3回 通所 với 要介護3 thực trả khoảng **15,000–20,000 円/tháng** (bao gồm 食費 + おやつ). "月20万円" kiểu bản gốc Hàn = SAI hoàn toàn — Nhật rẻ hơn hàng chục lần.

⚠️ 特養 **không thu tiền vào** — kịch bản nào bắt cụ bà nộp "tiền đặt cọc vào viện" là sai loại hình,
phải đổi sang 有料老人ホーム hoặc bỏ chi tiết đó.

---

## Cách dùng khi viết kịch bản

1. Cần con số tiền → **tra bảng trên trước**.
2. Không có trong bảng (giá sổ tay, tiền điện, phí tang lễ, tiền thuê nhà…) → **WebSearch số thật**,
   dùng con số đó, rồi **thêm một dòng vào file này** kèm nguồn + ngày tra.
3. Viết xong → chạy `qc_tien.py`. Nó đối chiếu từng số tiền với bản gốc; trùng đúng tỉ lệ 1:10 là
   **chặn**.

**Phép thử tự làm:** đặt từng con số tiền trong kịch bản cạnh con số tương ứng của bản gốc — nếu chỉ
khác nhau ở số 0 hoặc đúng tỉ lệ 1:10 thì **sai**, dù nghe có vẻ hợp lý.

---

## Thủ tục · lịch · phong tục (phần KHÔNG phải tiền)

| Việc | Sự thật ở Nhật | Bẫy hay dính | Nguồn · ngày tra |
|---|---|---|---|
| **Ngày nhận lương hưu** | Trả **6 lần/năm**, ngày **15 các tháng CHẴN** (2·4·6·8·10·12), mỗi lần lĩnh **2 tháng**. Rơi vào thứ 7/CN/lễ thì trả vào **ngày làm việc liền TRƯỚC** | Bản gốc Hàn trả **hằng tháng** → bê nguyên "đầu tháng ra bưu điện lĩnh lương hưu" là sai | 日本年金機構 · 2026-09-11 |
| **認知症対応の予約型代理人サービス** | Có ở 三菱UFJ・三井住友・みずほ・りそな・イオン銀行 — người gửi tiền chỉ định trước 代理人 (thường là con), khi mất khả năng phán đoán thì 代理人 có thể giao dịch thay | Dùng tên「신탁」 thẳng dịch sang 信託 nghe cứng — người Nhật thường gọi **予約型代理人サービス** hoặc 認知症サポート信託 | moneiro.jp · aozorabank · 2026-09-12 |
| **代理人カード** (banks) | Chủ tài khoản đăng ký trước tại cửa sổ chi nhánh, cấp thẻ ATM phụ cho người thân; **限度額 rút 10–20万円/ngày** | Cho phép rút 100万 trong 1 ngày là sai | saisoncard · pay-route · 2026-09-12 |
| **預金保険制度 (ペイオフ)** | 1 người × 1 ngân hàng được bảo hiểm tối đa **1,000万円 gốc + lãi** — 30 năm không đổi | Bản gốc Hàn nói 1억원 lên → dịch thẳng thành 1億円 là sai (Nhật vẫn 1,000万円) | 全国銀行協会 · 2026-09-12 |
| **家族信託 手数料** | Setup + phí quản lý — một số hợp đồng 年間数十万円 手数料; メガバンクの認知症対策信託 rẻ hơn 家族信託 luật sư dựng | | orixbank · daylight-law · 2026-09-12 |
| Nơi hỏi việc chăm sóc người già | **地域包括支援センター** (mỗi 中学校区 một cái) — nơi đầu tiên gia đình tìm đến | Cho cụ bà tự đi thẳng đến viện hoặc đến 市役所 hỏi chung chung | 2026-09-11 |
| Xin dịch vụ chăm sóc | **介護保険** → xin 要介護認定 tại 市区町村, có 認定調査 + ý kiến bác sĩ, **kết quả ~30 ngày** | Bỏ qua hẳn khâu giám định, cho dùng dịch vụ ngay | 2026-09-11 |
| Giấy tờ cuối đời | **事前指示書** / リビング・ウィル | Dịch sát từ bản gốc thành 「延命の不同意書」 — người Nhật không nói vậy | 2026-09-11 |
| **日本尊厳死協会 入会 / リビング・ウイル 登録** | 郵送 hoặc WEB đăng ký. **正会員 年会費 2,000 円**, **終身会員 一括 70,000 円**. Không có "chi nhánh tỉnh" nơi 15 phút xong — nộp đơn qua bưu điện/web, hội gửi lại **リビング・ウイル (事前指示書)** đã ký. **法的拘束力なし** nhưng gia đình + bác sĩ tôn trọng | Bản gốc Hàn có "建康保険公団 支社 15分で登録" — dịch thẳng sang Nhật SAI (Nhật không đăng ký ở cơ quan công, hội tư nhân 45+ năm). Cũng KHÔNG phải "会員証" xuất ngay trong ngày | songenshi-kyokai.or.jp · 2026-09-18 |
| **お粥 療養用 高級 テイクアウト** | 商店街 chuyên お粥屋 hoặc デパ地下: **1,200–1,650 円 / 杯** (kèm 出汁 nhẹ, dùng cho người bệnh). Kombini お粥 パック chỉ 300–500 円 nhưng không hợp người ốm | | tabelog お粥専門店 · Hanako · 2026-09-18 |
| Báo tử | **死亡届** nộp trong **7 ngày** tại 市区町村 nơi mất/nơi cư trú | | 2026-09-11 |
| Tự trả viện phí theo tuổi | 70–74 tuổi **20%**; từ 75 tuổi (後期高齢者医療) **10%** — người thu nhập ngang người đi làm thì 30% | | 2026-09-11 |
| **遺族年金 事実婚 手続き** | Nộp **様式7「事実婚関係及び生計同一関係に関する申立書」** tại 年金事務所, kèm **2 người thứ ba làm chứng** (第三者証明 — hàng xóm/bạn/chủ nhà v.v.), thêm bằng chứng đồng cư (住民票 cùng thế đới hoặc thư từ cùng địa chỉ 5年+), 健康保険 被扶養者 nếu có | Đừng dịch thẳng "혼인신고" → 婚姻届 khi ngữ cảnh là chứng minh sự thật hôn ex-post — dùng đúng thuật ngữ 事実婚関係申立書 | 日本年金機構 · 全国遺族年金相談センター · 2026-09-16 |
| **香典 相場** — 知人・友人 | **5,000円** (2025年 相場) — thân thiết thì 10,000円. Đồng nghiệp/上司/部下 cũng ~5,000円. 4·9 tránh dùng, tiền phải là đơn cũ (không tiền mới), phong bì đúng nghi thức 宗派 | Dịch từ 부의금 50만원/10만원 → 5万円/1万円 SAI (cao gấp 10 lần thật) | 足利銀行 · 小さなお葬式 · 2026-09-16 |

⚠️ **Phong tục — chỗ lộ dấu vết bản gốc nhiều nhất.** Quà thăm bệnh, món ăn theo mùa, nghi lễ tang
ma của bản gốc bê nguyên sang là lỗi `DẤU_VẾT_HÀN`, kể cả khi đã dịch đúng chữ. Món/nghi lễ nào
đưa vào kịch bản đều phải là thứ người Nhật thật sự làm trong đúng hoàn cảnh đó.

**Dòng nào chưa có nguồn cụ thể ở cột cuối = do tra lúc viết tập, chưa ghi link.** Tập sau ai dùng
lại mà cần chắc thì tra lại rồi bổ sung link vào đây.

---

## Giá tiêu dùng — chi phí thường gặp trong chuyện đời

| Khoản | Mức thật (Nhật) | Nguồn · ngày tra |
|---|---|---|
| Implant **răng trước** (1本) | **40–70 万円** — phổ biến 42–55 万円 | trust-dental.jp / shimokita-dental.jp · 2026-09-12 |
| Implant **răng bình quân** (奥歯) | **30–50 万円/本** (đô thị 35–55 万円) | shangri-la-dental.com · 2026-09-12 |
| Chung cư cũ **3LDK 千葉県 郊外 築30年** (~90m²) | **1,900–2,300 万円** (習志野市 92m² 1990年築 = 2,180 万円) | daiwahouse Livness · 2026-09-12 |
| Chung cư 3LDK 千葉市稲毛区 bình quân | **2,637 万円** | rehouse 三井 · 2026-09-12 |
| カット (tiệm khu phố) | **3,500–4,500 円** | quan sát chung 2026-09-12 |
| パーマ (tiệm khu phố) | **6,000–8,500 円** | quan sát chung 2026-09-12 |
| **補聴器 片耳 相場** | **10–20 万円** (thị trường phổ biến 35%) | 日本補聴器工業会 2025 · 大塚補聴器 · miru-kiku.jp · 2026-09-18 |
| **補聴器 両耳 相場** | **20–40 万円** (高級グレード 60–100 万円) | jp.sharp/mlp · kikoe.ne.jp · 2026-09-18 |
| **銭湯 大人 東京都** | **550 円** (2025-08-01 適用; 2026-08-01 から 600 円 予定) | 東京都浴場組合 1010.or.jp · 2026-09-18 |
| **アカスリ 全身** | **3,500–4,000 円 / 30 分** (50 分は 6,000–6,500 円) | やわらかの湯 · 佐野やすらぎの湯 · 2026-09-18 |
| **耳鼻科 診察 + 純音聴力検査** (3 割) | **1,500–2,000 円** (75+ 1 割は 500–700 円) | quan sát ratio · 2026-09-18 |
| **柿の苗木** (果樹苗) ホームセンター | **1,000–2,000 円** (ジャンボ富有 998 円, 太秋 1,580 円 コメリ) — オンライン 3,000–6,000 円, 選抜大実富有 3年生大苗 5,940 円 | aichiya.jp コメリ · Yahoo!ショッピング 2026 ランキング · 2026-09-19 |
| **エンディングノート** (コクヨ LES-E101 「もしもの時に役立つノート」) | **1,400–2,180 円** (税込) — 文房具店・ロフト等で入手 | 楽天市場 シブヤ文房具 · コクヨ公式 · 価格.com · 2026-09-19 |
| **給湯器 交換 (ガス · 追い焚き機能付)** 工事費込 | **15–25 万円** (エコジョーズ 20–26 万円 · エコキュート 40–65 万円) | ミズテック / リショップナビ / くらしのマーケット · 2026-09-19 |
| **リバースモーゲージ 年金型 月々 支給額** (自宅担保, 年金として毎月受取) | **月 5–10 万円** (物件評価額 2,000–3,000 万円で借入枠 800–1,500 万円, 30 年分割の目安) | 三井住友銀行 SMBCリバース60 / 東京スター銀行 充実人生 · 2026-09-19 |
| **シルバー人材センター 平均 月配分金** (月8–10日, 1日3–4時間) | **3–5 万円/月** (時給約 1,000 円, 雑所得, 65万円まで非課税) | 全国シルバー人材センター事業協会 / ファイナンシャルフィールド 2025 · 2026-09-19 |

## Y tế · viện phí (tự trả sau bảo hiểm)

| Khoản | Mức thật (Nhật) | Nguồn · ngày tra |
|---|---|---|
| **人工膝関節置換術** (TKR) tổng viện phí + nội trú 2–3 tuần | **180–230 万円** (tổng, chưa áp bảo hiểm) | fg-kshp.jp / clinic.adachikeiyu.com · 2026-09-12 |
| **TKR tự trả 75+ (後期高齢者 1割)** sau bảo hiểm | ~20 万円 → áp 高額療養費 còn **4–18 万円/tháng** (区分 II/III thu nhập thường ~57,600 円) | jinko-kansetsu.com · 2026-09-12 |
| **大腸内視鏡検査** quan sát (3割) | **4,000–5,000 円** | onaka-kenko.com · 2026-09-12 |
| **大腸内視鏡検査** quan sát (1割 · 75+) | **1,500–2,000 円** | ratio dẫn xuất · 2026-09-12 |
| **大腸内視鏡** + ポリープ切除 (3割) | **20,000–30,000 円** | onaka-oshiri.clinic · 2026-09-12 |

⚠️ TKR ở Nhật tổng viện phí thật là **180–230 万円**, nhưng cụ già 75+ nhờ 後期高齢者 1割 + 高額療養費 nên **thực trả ~5–15 万円/lần** (khác hẳn Hàn 300万원 = 24万円 quy đổi cứng). Kịch bản nên nói `本人負担 十万円ほど` chứ không nói `三十万円`.

## Phí giúp việc chăm bệnh (付添い介護 私費 · KHÔNG áp 介護保険 trong bệnh viện)

| Khoản | Mức thật (Nhật) | Nguồn · ngày tra |
|---|---|---|
| Giờ (時給) | **~3,000 円** | ichirou.co.jp · 2026-09-12 |
| Ngày (日給, 8–12h ban ngày) | **~15,000 円** | ichirou.co.jp · 2026-09-12 |
| 24 tiếng | **20,000–30,000 円** | ichirou.co.jp · 2026-09-12 |
| 住み込み 1 tháng | **30–70 万円** | lobby-z.co.jp · 2026-09-12 |

⚠️ Trong bệnh viện Nhật, **介護保険 gần như KHÔNG áp** cho việc trong bệnh viện — muốn thuê người trực bên giường phải **私費** qua công ty (家政婦紹介所 · イチロウ...). 10 ngày trực 24h thật ~**20–30 万円**, KHÔNG phải 130 万円 như tính theo bản gốc Hàn.

⚠️ Bản gốc Hàn thường dùng: implant 480万원 · chung cư 20평 1억9천 · 1억5천 giao cho phụ nữ · 4,200万원 rút dần · 2천만원 定期 · 700万원 phẫu thuật.
Quy đổi 1:10 sẽ ra: 48万円 · 1,900万円 · 1,500万円 · 420万円 · 200万円 · 70万円 — TRÙNG ĐÚNG TỈ LỆ 1:10 = qc_tien.py CHẶN.
Dùng con số **thật Nhật nhưng khác tỉ lệ 10:1**: 42万円 · 2,180万円 · 1,650万円 · 380万円 · 220万円 · 82万円 (đều vẫn nằm trong range thật của Nhật).

## 葬儀 · 火葬 · 死後手続き (追加 2026-09-17, tập simbot2-05)

| Việc | Sự thật ở Nhật | Bẫy hay dính | Nguồn · ngày tra |
|---|---|---|---|
| **一般葬 相場** | 全国平均 **約110–190万円** (通夜+告別式+火葬+飲食+返礼品込) | | 鎌倉新書 いい葬儀 相場調査 · 2026-09-17 (cutoff 2026-01) |
| **家族葬 相場** | **約40–90万円** (少人数のみ、宗教儀式簡素、飲食少) — 近年比率が急上昇 | 韓国式 1,400–1,500 만원 → 140–150 万円 dịch thẳng sai | 鎌倉新書 · 2026-09-17 |
| **一日葬 相場** | **約30–50万円** (通夜省略、告別式+火葬 1日で) | | 鎌倉新書 · 2026-09-17 |
| **直葬・火葬式 相場** | **約10–30万円** (通夜・告別式なし、火葬のみ) — 首都圏で急増 | 「無祭壇葬」というのは韓国用語、Nhật thường dùng **直葬** hoặc **火葬式** | 鎌倉新書 · 小さなお葬式 · 2026-09-17 |
| **死後24時間 火葬制限** | **墓地埋葬法 第3条**: 死亡・死産から24時間経過するまで火葬・埋葬不可 (伝染病を除く) | 「亡くなったその日に火葬」は不可 — 何時に亡くなっても丸一日待つ | 墓地埋葬法 第3条 · 2026-09-17 |
| **火葬場 予約 混雑** | 都市部 **7–10日待ち** も普通 (東京23区)。田舎は当日〜2日。冬場は全国的に長い | 「明日火葬」を前提にした韓国式段取りは Nhật 都市部で機能しない | 業界慣行 · 2026-09-17 |
| **死亡届 + 火葬許可証** | 死亡診断書と共に **7日以内** に 市区町村役場に届出、同時に **火葬許可証** を受け取る | 火葬許可証なしでは火葬場は受け付けない | 戸籍法86条 · 墓地埋葬法 · 2026-09-17 |
| **事前指示書 / リビング・ウィル** | 尊厳死協会が推奨する書式が一般的。**法的拘束力はない** が家族への意思伝達として有効 | 韓国「사전 장례 의향서」を直訳 → 通じない、正しくは **事前指示書** | 日本尊厳死協会 · 2026-09-17 |

⚠️ **Ngành栗農家 岐阜県中津川市**: 栗きんとん発祥地、栗農家が実在、山間部で 3月頭に **剪定 (せんてい・pruning)** が農事暦上正しい (雪が完全に溶ける前、樹液が動き出す直前)。Story satori dùng bối cảnh 山間 栗農家 hợp lý.

## 消費者・金融トラブル 相談窓口 (追加 2026-09-17, tập simbot2-08)

| Việc | Sự thật ở Nhật | Bẫy hay dính | Nguồn · ngày tra |
|---|---|---|---|
| **消費者ホットライン 188** (「いやや」) | 局番なし **188** で最寄りの消費生活センター/消費生活相談窓口へ自動接続。金融商品トラブルも一次相談窓口として案内可 | Bản gốc Hàn dùng 「1332 (금감원)」= Hàn — dịch thẳng số điện thoại là sai, Nhật dùng **188** | 消費者庁 · 2026-09-17 |
| **金融サービス利用者相談室** (金融庁) | **0570-016811** (IP電話 03-5251-6811, 平日10-17時) — 銀行・証券・投資信託等の苦情・相談 | 3桁ではないので視聴者向けCTAに使いにくい → 188に繋いでもらう案内が優しい | 金融庁 · 2026-09-17 |
| **全国銀行協会 相談室** | **0570-017109** (IP電話 03-5252-3772) — 銀行取引の苦情・あっせん (金融ADR無料) | | 全銀協 · 2026-09-17 |
| **仕組み債 高齢者被害 2022-2024年** | 「EB債 (他社株転換社債)」等の複雑仕組み債を退職金世代に不適切販売した銀行に金融庁が業務改善命令 (千葉銀行・武蔵野銀行 2023年6月ほか) | 「元本非保障」の説明が不十分なまま定期預金の代替として販売、下落で元本毀損多発 | 金融庁業務改善命令 · 2026-09-17 |
| **補聴器 補助金** | 中等度・高度以上で **身体障害者手帳** 交付 → 補装具費支給制度 (原則 1 割自己負担)。手帳の交付基準に達しない軽度・中等度は **市区町村独自の助成** (自治体差大、1/3〜2/3 補助) — 購入前申請が必須 | 「軽度難聴 = 全額補助」は誤り。都市部でも制度がない自治体あり | 厚労省 · 各補聴器店 · 2026-09-18 |
| **地域包括支援センター** | 中学校区に 1 か所、65 歳以上の相談窓口 (介護・医療・生活支援・虐待防止) — 無料、電話 or 来所 | 「市役所へ行く」より地域包括の方が具体的 | 2026-09-18 |

## 統計 · 現状 (老老介護)

| Việc | Sự thật ở Nhật | Nguồn · ngày tra |
|---|---|---|
| 65歳以上同士の介護 (老老介護) | **63,5%** (2022 国民生活基礎調査) — tăng từ 40,6% năm 2001 | 大和ネクスト銀行 · 2026-09-16 |
| 75歳以上同士の介護 | **35,7%** — cứ 3 hộ có người già chăm nhau là 1 hộ đều ≥75 tuổi | 大和ネクスト銀行 · 2026-09-16 |
| 60歳以上同士 | **77,1%** | 大和ネクスト銀行 · 2026-09-16 |
| 65歳以上高齢者 (2024) | **3,625万人** — 総人口の **29,3%** (kỷ lục) | 総務省 · 2026-09-16 |

⚠️ Trong ngách satori (JP), lời của cụ bà nói "娘も六十を過ぎて自分も介護される歳になったのに、私を見ている" — đây chính là bối cảnh 老老介護 điển hình, KHÔNG cần bịa số.

## Bối cảnh lịch sử

| Việc | Sự thật ở Nhật | Nguồn · ngày tra |
|---|---|---|
| **中東建設ブーム 1970年代** — thợ Nhật sang サウジアラビア | Có thật; sau khủng hoảng dầu 1973, gulf-states dùng lao động ngoại quốc quy mô lớn cho các dự án hạ tầng. Công ty Nhật (清水建設・大成・鹿島 v.v.) đưa kỹ sư sang các công trường sa mạc; thợ về nước sau 2–3 năm với khoản dồn đủ mua nhà ngoại ô | JIIA "出稼ぎ労働者" · 國學院大學 "アラブの大富豪" · 2026-09-12 |

## Luật · pháp lý dân sự

| Việc | Sự thật ở Nhật | Bẫy hay dính |
|---|---|---|
| **民事不介入** — cảnh sát Nhật không can thiệp tranh chấp dân sự thuần | Người già tự tay ký giấy, tự chuyển tiền cho bạn gái → cảnh sát nói "không cấu thành 詐欺" trừ khi chứng minh được ý đồ lừa đảo từ đầu. Phải kiện dân sự (民事) → tốn thời gian, khó thu hồi | Bản gốc Hàn nói y hệt luật Hàn — Nhật thực sự cũng vậy, dùng đúng từ 民事不介入 |
| Cáo giác 詐欺 (156条 & 246条 hình sự) | Chứng minh "欺罔行為" (hành vi gạt) + "錯誤" của nạn nhân + "処分行為" — nếu ông cụ tự ký thì "処分行為" bị coi là 自らの意思 | |

---

## Nguồn

- [国民年金保険料 2025年4月から月17,510円 — ライフィ](https://lify.jp/column/insurance-news/article-80742/)
- [【2025年最新データ】国民年金・厚生年金はみんないくらもらっている？ — Mocha](https://fpcafe.jp/mocha/4575)
- [2025年度の年金額は3年連続の上昇 — 未来をはぐくむ研究所](https://www.am-one.co.jp/hagukumu/article/column-20250131-2.html)
- [【2025年最新】老人ホームの費用相場 — SAGASIX](https://www.sagasix.jp/knowledge/cost/)
- [全国の老人ホーム・介護施設の費用相場 月額料金26.6万円 — LIFULL 介護](https://kaigo.homes.co.jp/market_price/)
- [年金はいつ支払われますか。— 日本年金機構](https://www.nenkin.go.jp/section/faq/jukyu/uketori/uketori/shiharaiduki/20140421-01.html)
