"""qc_script_sol.py — QC ĐỘC LẬP kịch bản bằng GPT-5.6-sol (khác hẳn Gemini/ramclouds đang dùng ở
B3Q/B3F — xem sol_client.py để biết TẠI SAO cần model thứ 2, và qc_thumbnail_sol.py — file này dựng
theo ĐÚNG khuôn đó cho kịch bản).

BÀI HỌC XÂY TOOL NÀY (kenko-chiebukuro ep02-sarukopenia-sign, 2026-09-18): lần đầu KHÔNG có prompt cố
định, chỉ hỏi sol 1 câu mở "kiểm tra hợp lý không" — mất tới 4 vòng qua lại mới sạch, vì 3 lý do khác
nhau: (1) câu hỏi mở không ép model chủ động đối chiếu số liệu với chuẩn tham chiếu phù hợp đối tượng
(vd dùng chuẩn châu Âu EWGSOP2 cho video hướng người Nhật, đáng lẽ phải dùng chuẩn châu Á AWGS2019),
(2) khi Claude tự sửa bằng 1 lệnh viết-lại-toàn-bộ, bản mới TỰ SINH lỗi ngữ pháp mới (dấu phẩy chèn
giữa cụm động từ ghép) mà vòng sau mới bắt được, (3) một số lỗi an toàn tinh vi chỉ lộ ra sau vài lượt
đọc kỹ. ⚠️ Bài học SUÝT LÀM SAI: định đóng gói thành 1 CHECKLIST SỰ KIỆN CỤ THỂ của tập sarcopenia đó
(kiểu "phải so AWGS vs EWGSOP2") — user chỉ ra đúng: làm vậy thì tập sau (bệnh thận, tiểu đường, mất
trí nhớ...) sol sẽ CHỈ trả lời đúng mấy mục cứng đó, không tổng quát được. Sửa lại đúng hướng: đóng
gói thành 6 LĂNG KÍNH PHÂN TÍCH TỔNG QUÁT (áp dụng được cho MỌI chủ đề y khoa người già, không khoá
cứng vào 1 bệnh cụ thể) + ép sol làm HẾT SỨC KỸ NGAY LẦN ĐẦU (không giữ lại lỗi chờ vòng sau).

Dùng:
  py -3.13 qc_script_sol.py --script script.txt --title-file listting.txt --profile kenko-chiebukuro
  py -3.13 qc_script_sol.py --script script.txt --title "..." --out qc_sol_report.txt
"""
import argparse
import json
import re
import sys
from pathlib import Path

import sol_client

sys.stdout.reconfigure(encoding="utf-8")

PROMPT_TMPL = """Bạn là biên tập viên y khoa, kiểm tra LẦN CUỐI một kịch bản voiceover YouTube tiếng
Nhật cho người cao tuổi (phong cách bác sĩ giải thích, danh sách đếm ngược N dấu hiệu/mục). Đây là
LƯỢT DUY NHẤT — sẽ không có vòng hỏi lại, nên hãy đọc THẬT KỸ và liệt kê HẾT mọi vấn đề bạn tìm thấy
ngay trong lượt này, đừng giữ lại phần nào "để sau".

TIÊU ĐỀ VIDEO: {title}

Hãy áp dụng đúng 6 LĂNG KÍNH PHÂN TÍCH sau cho TOÀN BỘ kịch bản — đây là khung tổng quát dùng được
cho MỌI chủ đề y khoa người già (không riêng chủ đề của tập này), hãy tự vận dụng kiến thức y khoa
của bạn cho ĐÚNG chủ đề đang đọc, đừng chỉ so khớp với danh sách có sẵn:

1. ĐỘ CHÍNH XÁC & CHUẨN THAM CHIẾU PHÙ HỢP ĐỐI TƯỢNG
   - Với MỌI con số/ngưỡng/tiêu chuẩn chẩn đoán được nêu: có tồn tại một bộ chuẩn khác PHÙ HỢP HƠN
     với đối tượng video (vd chuẩn châu Á thay vì châu Âu cho khán giả Nhật, số liệu Nhật Bản thay vì
     số liệu quốc tế chung) mà kịch bản đang dùng nhầm/dùng chuẩn kém phù hợp hơn không?
   - Định nghĩa của khái niệm y khoa trung tâm (bệnh/tình trạng chính của video) đã đủ đầy đủ chưa,
     hay bị đơn giản hoá tới mức sai lệch?
   - Số liệu tỷ lệ mắc/rủi ro có được trình bày kèm mức độ chắc chắn phù hợp không (tuyệt đối hoá một
     con số dao động theo nghiên cứu/tiêu chuẩn là một lỗi)?

2. AN TOÀN VẬT LÝ CỦA MỌI HƯỚNG DẪN HÀNH ĐỘNG
   - Với MỌI đoạn mời/hướng dẫn người xem TỰ LÀM một động tác (đứng dậy, đi, đo, tự kiểm tra...): nếu
     người xem đang yếu, chóng mặt, từng ngã, cao tuổi ở một mình — hướng dẫn này có an toàn không?
   - Điều kiện an toàn (ghế/chỗ vịn chắc chắn, có người giám sát, dừng ngay khi khó chịu) có được nêu
     TRƯỚC khi mời thử, hay chỉ nêu sau khi có thể đã xảy ra sự cố?

3. NHÂN QUẢ & CHẨN ĐOÁN QUÁ MỨC
   - Kịch bản có ngụ ý rằng quan sát thấy 1 dấu hiệu ĐỒNG NGHĨA với mắc bệnh chính của video không,
     trong khi dấu hiệu đó thực ra có thể do nhiều nguyên nhân khác (bệnh khác, thuốc, tuổi tác đơn
     thuần)? Có phân biệt rõ "gợi ý/sàng lọc" với "chẩn đoán xác định" không?

4. TRIỆU CHỨNG KHẨN CẤP BỊ GỘP NHẦM MỨC ĐỘ
   - Có triệu chứng nào được nhắc tới (dù thoáng qua) thuộc nhóm CẤP CỨU thật sự (dấu hiệu đột quỵ,
     khó thở, đau ngực, ngất...) đang bị gộp chung với nhóm "đi khám sau/khám định kỳ" không? Hai mức
     độ này PHẢI tách rõ ràng, mức cấp cứu phải nói rõ "gọi cấp cứu ngay".

5. NGÔN NGỮ TUYỆT ĐỐI HOÁ / QUẢNG CÁO QUÁ MỨC
   - Có cụm nào kiểu "chắc chắn", "duy nhất đáng tin", "không gì tốt hơn", "hoàn toàn phù hợp", xếp
     hạng "quan trọng nhất" không có căn cứ y khoa (chỉ là thứ tự trình bày)... cần làm mềm không?

6. LOGIC NỘI BỘ & ĐỘ TỰ NHIÊN CỦA VĂN BẢN
   - Có mâu thuẫn nội bộ, đoạn lặp ý, câu hứa nội dung nhưng không thực hiện không?
   - Riêng về NGỮ PHÁP tiếng Nhật: có chỗ nào dấu phẩy bị chèn SAI VỊ TRÍ (cắt giữa một cụm động từ
     ghép như て+しまう/ていく/てくる/てきている, hoặc cắt giữa định ngữ và danh từ nó bổ nghĩa) làm câu
     mất tự nhiên khi đọc thành tiếng không? Liệt kê CHÍNH XÁC từng câu bị lỗi kiểu này nếu có.

{domain_focus}{hook_block}

QUY TẮC ĐÁNH GIÁ:
PASS = dùng được ngay, không có lỗi đáng kể ở cả 6 lăng kính trên.
FIX = có lỗi cần sửa trước khi thu âm/đăng (liệt kê cụ thể).
REMAKE = vấn đề nội dung/cấu trúc quá lớn, nên viết lại phần lớn.

OUTPUT BẮT BUỘC — mỗi mục 1-6 ở trên đều phải có mặt trong output dù không có lỗi (ghi "không phát
hiện vấn đề" nếu sạch), hễ trích câu/đoạn tiếng Nhật thì đặt ngay nghĩa tiếng Việt sau dấu |:

KẾT QUẢ: [PASS / FIX / REMAKE]

1. ĐỘ CHÍNH XÁC & CHUẨN THAM CHIẾU:
[...]

2. AN TOÀN HƯỚNG DẪN HÀNH ĐỘNG:
[...]

3. NHÂN QUẢ & CHẨN ĐOÁN QUÁ MỨC:
[...]

4. TRIỆU CHỨNG KHẨN CẤP:
[...]

5. NGÔN NGỮ TUYỆT ĐỐI HOÁ:
[...]

6. LOGIC & NGỮ PHÁP:
[...]

KẾT LUẬN: [2-4 câu: vấn đề quan trọng nhất là gì, có dùng được ngay không]

=== KỊCH BẢN ===
{script}
"""

DEFAULT_DOMAIN_FOCUS = """LƯU Ý RIÊNG CHO NGÁCH SỨC KHOẺ NGƯỜI GIÀ: đây là nội dung có rủi ro y khoa
thật (khán giả cao tuổi có thể hành động theo lời video) — ưu tiên nghiêm ngặt nhất cho lăng kính #2
(an toàn vật lý) và #4 (triệu chứng khẩn cấp), vì sai sót ở 2 mục này có thể gây hại trực tiếp."""


# Bộ lăng kính thứ 2 cho lane KỂ CHUYỆN (satori/người già kể đời mình) — thêm 2026-09-18 khi áp GPT-sol
# làm trọng tài B3Q cho lane satori: 6 lăng kính y khoa ở trên KHÔNG áp được cho truyện cảm xúc (không
# có chẩn đoán/triệu chứng), nhưng lỗi thật của lane này lại nằm ở: mâu thuẫn dữ kiện giữa các đoạn,
# dấu vết bản gốc Hàn (quy đổi tiền 1:10, dịch sát, phong tục Hàn), thủ tục/giá cả Nhật sai, hành vi
# nhân vật tự mâu thuẫn, số học tiền, nhịp đọc. Chọn bằng `profile.script_qc.lens = "story"`; không khai
# → "medical" (giữ nguyên hành vi cũ cho lane sức khoẻ).
STORY_TMPL = """Bạn là biên tập viên cao cấp kiểm tra LẦN CUỐI một kịch bản voiceover YouTube tiếng Nhật:
NGƯỜI GIÀ NHẬT kể lại chuyện đời mình (ngôi thứ nhất, văn tâm tình, bối cảnh đời sống Nhật hiện đại).
Đây là LƯỢT DUY NHẤT — không có vòng hỏi lại — hãy đọc THẬT KỸ và liệt kê HẾT mọi vấn đề ngay lượt này.
Kịch bản này là bản PHÓNG TÁC 70/30 từ một video Hàn Quốc; nó PHẢI đọc như chuyện của người Nhật thật,
không được để lộ dấu vết bản gốc.

TIÊU ĐỀ VIDEO: {title}

Áp dụng đúng 6 LĂNG KÍNH sau cho TOÀN BỘ kịch bản (khung tổng quát cho mọi tập của lane kể chuyện):

1. MÂU THUẪN DỮ KIỆN GIỮA CÁC ĐOẠN
   - Tuổi, năm, mốc thời gian, mùa, nơi ở, nghề nghiệp, quan hệ gia đình, tên người: có chi tiết nào
     ở đoạn sau đá đoạn trước không (vd chồng làm ở Kawaguchi nhưng nhà ở Inage "gần nơi làm"; mùa
     đông chí + nửa năm mà kể là mùa thu)? Nêu RÕ đoạn nào ↔ đoạn nào.
   - Cùng một sự việc có bị kể hai lần ở hai chỗ xa nhau theo hai cách khác nhau không?

2. SỐ HỌC & TIỀN BẠC
   - Mọi con số tiền, khoản rút/trả/còn lại có khớp nhau xuyên suốt không (rút 60万 nhưng mua 50万 thì
     10万 còn lại đi đâu)?
   - Có con số nào là QUY ĐỔI MÁY MÓC từ won Hàn theo tỉ giá (≈ ×0,1) thay vì mức giá THẬT ở Nhật
     không? Giá/mức phí ở Nhật (máy trợ thính, viện phí, tiền tàu, lương hưu, tang lễ…) có hợp thực tế
     Nhật không? Nếu nghi ngờ, nêu con số và mức bạn cho là hợp lý.

3. DẤU VẾT BẢN GỐC HÀN / BẢN ĐỊA HOÁ
   - Từ ngữ dịch sát không phải tiếng Nhật tự nhiên (vd 「人代」 thay vì 交際費), phong tục/món ăn/nghi lễ
     Hàn bê nguyên sang, cách xưng hô hay thủ tục hành chính KHÔNG tồn tại ở Nhật.
   - Địa lý/giao thông Nhật sai (tuyến tàu, ga, khoảng cách, tên cơ quan).

4. LOGIC HÀNH VI NHÂN VẬT & QUY TRÌNH ĐỜI THẬT
   - Nhân vật có hành động trái với tính cách/thái độ đã kể ở đoạn khác không (vd chồng chê đắt rồi
     ngay sau lại tự đi mua)? Cơ quan/ngân hàng/bệnh viện có hành xử đúng quy trình Nhật không?
   - Chỉ nêu khi mâu thuẫn RÕ RÀNG; tình tiết hư cấu hợp lý thì không phải lỗi.

5. NGÔN NGỮ TUYỆT ĐỐI HOÁ / LỜI KHUYÊN SAI
   - Câu kết luận/bài học có khẳng định tuyệt đối hoặc lời khuyên tài chính/pháp lý/y tế sai hay có
     thể gây hại nếu người già làm theo không?

6. NHỊP ĐỌC & NGỮ PHÁP (voiceover)
   - Dấu 、 chèn sai chỗ cắt cụm động từ ghép (て+しまう/ていく/てくる) hoặc cắt giữa định ngữ và danh từ;
     đoạn lặp ý; câu hứa mà không thực hiện. Liệt kê CHÍNH XÁC từng câu nếu có.

{domain_focus}{hook_block}

QUY TẮC ĐÁNH GIÁ — tách SAI khỏi CHƯA HAY:
PASS = không còn lỗi SAI (mâu thuẫn dữ kiện, số học, dấu vết Hàn, logic gãy); góp ý văn phong không tính.
FIX = có lỗi SAI cụ thể cần sửa tại chỗ (liệt kê từng câu + cách sửa ngắn), nhưng khung truyện dùng được.
REMAKE = khung truyện/cốt truyện gãy hoặc bám bản gốc quá lộ, phải viết lại phần lớn.

OUTPUT BẮT BUỘC — đủ 6 mục dù không lỗi (ghi "không phát hiện vấn đề"); trích câu tiếng Nhật thì đặt
nghĩa tiếng Việt ngay sau dấu |; mỗi lỗi ghi rõ SAI hay CHƯA HAY:

KẾT QUẢ: [PASS / FIX / REMAKE]

1. MÂU THUẪN DỮ KIỆN:
[...]

2. SỐ HỌC & TIỀN:
[...]

3. DẤU VẾT HÀN / BẢN ĐỊA HOÁ:
[...]

4. LOGIC HÀNH VI & QUY TRÌNH:
[...]

5. TUYỆT ĐỐI HOÁ / LỜI KHUYÊN:
[...]

6. NHỊP ĐỌC & NGỮ PHÁP:
[...]

KẾT LUẬN: [2-4 câu: lỗi SAI quan trọng nhất là gì, có thu âm được ngay không]

=== KỊCH BẢN ===
{script}
"""

# Lens thứ 3 — "plain" (anh chốt 2026-09-20 khi test Lane F): GPT-sol chỉ là MỘT MODEL ĐỌC KỊCH BẢN, hỏi
# sao nó trả lời vậy. Lane không y khoa, không phóng tác từ Hàn thì đừng ép nó đeo lăng kính y khoa/Hàn
# (đo thật ep01 Lane F: lens medical → REMAKE vì "không có list N mục/bác sĩ/gọi 119" — toàn lỗi ảo).
# Câu hỏi đúng chỉ là: "kịch bản này đã hợp lý chưa, chỗ nào không hợp lý thì liệt kê ra để sửa."
# {domain_focus} vẫn chèn được 1-2 câu bối cảnh lane (thể loại, ngôi kể) — KHÔNG phải danh sách rủi ro.
PLAIN_TMPL = """Bạn là biên tập viên kịch bản. Hãy đọc TOÀN BỘ kịch bản voiceover YouTube tiếng Nhật dưới đây
và trả lời một câu hỏi duy nhất: **kịch bản này đã hợp lý chưa?**

Bối cảnh: {domain_focus}
Tiêu đề video (nếu có): {title}

Soi mọi khía cạnh khiến người xem thấy "không hợp lý": mạch truyện đứt/nhảy, nhân vật hành xử trái tính cách,
mốc thời gian/tuổi/năm đá nhau, con số tiền không cộng lại được hoặc lệch giữa các đoạn, chi tiết đời sống/thủ
tục Nhật sai thực tế, câu chữ tối nghĩa, lặp ý, câu hứa mà không trả, kết luận không đi ra từ câu chuyện.
Chỉ liệt kê điểm KHÔNG HỢP LÝ (phải sửa) — góp ý "có thể hay hơn" ghi riêng ở cuối, ngắn gọn, không tính vào verdict.
Không đòi hỏi thể loại/cấu trúc khác với thứ kịch bản đang là (đây không phải video y khoa hay video danh sách).{hook_block}

MỨC ĐỘ — gắn cho TỪNG điểm, đây là thứ quyết định verdict (sàn hội tụ, thêm 2026-09-20 sau khi đo 3 lượt 7→6→4 điểm
mà không lượt nào PASS vì mỗi lần đọc lại tìm ra điểm nhỏ hơn):
  [NẶNG] người xem bình thường sẽ thấy VÔ LÝ hoặc SAI: mâu thuẫn dữ kiện/dòng thời gian/nhân vật, số liệu tự đá nhau,
         lời hứa tiêu đề không được trả, nhân quả gãy, gợi ý có thể gây hại.
  [VỪA]  người xem chăm chú mới thấy: chi tiết thiết lập bị bỏ dở, đạo cụ/hành động thiếu mắt xích, lẫn thông tin 2 nhân vật.
  [NHẸ]  chỉ "có thể tự nhiên/chặt hơn": cách kết hợp từ, chuyển biến hơi nhanh, ước lượng số (二十年 vs 二十年近く), câu nối.
Điểm NHẸ KHÔNG ghi vào danh sách — đưa xuống GÓP Ý THÊM.

OUTPUT BẮT BUỘC:

KẾT QUẢ: [PASS / FIX / REMAKE]
(PASS = không có điểm NẶNG và ít hơn 3 điểm VỪA; FIX = có ≥1 NẶNG hoặc ≥3 VỪA, sửa tại chỗ được; REMAKE = mạch truyện/cốt
truyện gãy đến mức phải viết lại phần lớn)

ĐIỂM KHÔNG HỢP LÝ (đánh số; mỗi điểm: [NẶNG/VỪA] trích câu tiếng Nhật | nghĩa tiếng Việt → vì sao không hợp lý → cách sửa ngắn):
[...]

GÓP Ý THÊM (không bắt buộc sửa, tối đa 5 dòng):
[...]

KẾT LUẬN: [1-2 câu]

=== KỊCH BẢN ===
{script}
"""

# Lens thứ 4 — "hook" (thêm 2026-09-23, dự án HOOK VIDEO 20-30s): hook được viết và KHOÁ
# TRƯỚC KHI viết thân kịch bản (xem docs/PHUONG_AN_HOOK_VIDEO.md) — nên nó cần MỘT lượt
# chấm RIÊNG, không đợi tới lúc script xong mới soi. Khác 3 lens trên (REMAKE tồn tại vì
# viết lại cả kịch bản không phải chuyện nhỏ), hook chỉ ~150 chữ nên KHÔNG CÓ REMAKE — dở
# tệ tới đâu thì cũng chỉ "sửa tại chỗ" (FIX), không có lý do viết lại từ đầu ở quy mô này.
# run_hook() chấm 3 ỨNG VIÊN cùng lúc (không phải 1) vì hook là chỗ quyết định giữ/bỏ
# người xem trong vài giây đầu — so sánh chéo 3 bản ra được ứng viên tốt nhất, chấm rời
# từng cái một sẽ mất khả năng so sánh này.
#
# NOI_TU_HOOK là khối CHÈN ĐƯỢC vào 3 lens cũ (qua tham số hook_block của run(), xem dưới)
# để khi sol chấm TOÀN VĂN kịch bản (sau khi thân đã viết xong), nó soi thêm: thân bài có
# kể lại hook không (lặp ý), có RESET câu chuyện ngay sau hook không (tả lại thời tiết/giới
# thiệu kênh — lỗi thật thường gặp khi model viết thân không nhớ hook đã nói gì), và câu
# hỏi/lời hứa hook mở ra có được trả đúng chỗ không. Đây là bài toán "hook + thân phải khớp
# nhau" — không đưa riêng cho lens hook (lens hook chấm khi CHƯA có thân) mà đưa vào 3 lens
# CŨ (chấm sau khi có thân) qua {hook_block} nhét vào giữa template, KHÔNG tự .format() ở
# đây vì bản thân NOI_TU_HOOK còn chứa {hook} — Task 9 (lean_script.py) sẽ tự
# NOI_TU_HOOK.format(hook=hook) trước khi truyền hook_block cho run().
NOI_TU_HOOK = """
7. NỐI TỪ HOOK (đoạn mở đầu đã KHOÁ trước khi viết thân — nguyên văn dưới đây):
{hook}
   - Thân bài có KỂ LẠI thông tin hook vừa nói không (lặp sự kiện/câu thoại)? Có RESET câu chuyện (tả thời tiết,
     giới thiệu kênh, mở lại từ đầu) ngay sau hook không?
   - Câu hỏi/lời hứa hook mở ra có được TRẢ đúng chỗ trong thân không? Có phá promise của hook không?
   - Lỗi ở mục này = SAI (không phải chưa hay)."""

HOOK_TMPL = """Bạn là biên tập viên chấm HOOK 20–30 GIÂY ĐẦU của video YouTube kể chuyện tiếng Nhật. Có 3 ứng viên;
hãy chọn 1 và chấm. Đây là LƯỢT DUY NHẤT.

TIÊU ĐỀ (promise): {title}
CHỮ THUMBNAIL (promise): {thumb_text}
LỜI HỨA/SỰ THẬT CỦA TẬP (core_event · payoff · reveal · timeline — hook KHÔNG được bịa ngoài đây, KHÔNG spoil reveal):
{promise_text}

3 ỨNG VIÊN:
{candidates}

Chấm TỪNG ứng viên theo checklist (mỗi ô PASS/FAIL):
TITLE_MATCH · THUMB_MATCH · STORY_TRUTH (sự kiện có trong lời hứa/sự thật ở trên) · NO_FAKE_DRAMA · NO_SPOILER ·
OPEN_LOOP (câu cuối để ngỏ) · EMOTIONAL_STAKE · KHONG_CAN_SETUP (hiểu được ngay) · SU_KIEN_0_5S (3–5 giây đầu đã có
sự kiện) · KHONG_CHAO_HOI · KHONG_CAU_THUA · DU_4_NHIP (event → contradiction → stake → open loop) ·
RETENTION ("tắt title/thumb, chỉ nghe 30s: có muốn biết chuyện gì tiếp không?").

OUTPUT BẮT BUỘC:
KẾT QUẢ: [PASS / FIX]   (PASS = ứng viên được chọn không FAIL ô nào; FIX = ứng viên tốt nhất còn FAIL ≤3 ô, sửa tại chỗ được)
CHỌN: [1 / 2 / 3]
LÝ DO CHỌN: [1–2 câu]
CHECKLIST ỨNG VIÊN ĐƯỢC CHỌN: [mỗi ô 1 dòng: TÊN_Ô: PASS/FAIL — lý do ngắn]
VIỆC PHẢI SỬA (nếu FIX): [đánh số; mỗi việc: trích câu tiếng Nhật | nghĩa Việt → sửa thành gì, ngắn]
"""

LENS_TMPL = {"medical": PROMPT_TMPL, "story": STORY_TMPL, "plain": PLAIN_TMPL}


def _load_profile(profile_id):
    if not profile_id:
        return {}
    p = Path(__file__).resolve().parent.parent / "profiles" / "profiles" / f"{profile_id}.json"
    if not p.exists():
        print(f"  ! khong thay profile {p}, dung mac dinh", file=sys.stderr)
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def load_lens(profile_id):
    """`script_qc.lens` = "medical" (mặc định, giữ hành vi cũ) | "story" (satori, phóng tác từ Hàn) |
    "plain" (hỏi thẳng 'đã hợp lý chưa' — lane không y khoa/không Hàn, vd teinengo-real)."""
    lens = ((_load_profile(profile_id).get("script_qc") or {}).get("lens") or "medical").lower()
    if lens not in LENS_TMPL:
        print(f"  ! lens {lens!r} khong ton tai, dung medical", file=sys.stderr)
        lens = "medical"
    return lens


def load_domain_focus(profile_id):
    """Đọc `script_qc.domain_focus` trong profiles/profiles/<id>.json nếu có — mỗi lane/ngách tự
    khai trọng tâm rủi ro riêng (sức khỏe khác truyền thuyết đô thị khác lịch sử chiến tranh), CÙNG
    một khuôn 6 lăng kính tổng quát ở trên không đổi. Không khai thì dùng mặc định sức khỏe."""
    focus = (_load_profile(profile_id).get("script_qc") or {}).get("domain_focus")
    return focus.strip() if focus else DEFAULT_DOMAIN_FOCUS


def parse_verdict(text):
    m = re.search(r"KẾT QUẢ\s*[:：]\s*(PASS|FIX|REMAKE)", text, re.IGNORECASE)
    return m.group(1).upper() if m else "UNKNOWN"


def run(script_text, title, profile_id=None, out=None, extra_note="", hook_block=""):
    """`extra_note` (flow=lean): 1 đoạn nói rõ máy ĐÃ kiểm gì (độ dài/số mục/số liệu) để sol không tốn chỗ lặp lại.
    `hook_block` (2026-09-23, dự án HOOK VIDEO): NOI_TU_HOOK đã .format(hook=...) sẵn từ nơi gọi (lean_script.py) —
    truyền chuỗi RỖNG (mặc định) thì 3 template không đổi MỘT KÝ TỰ nào so với trước khi có tính năng hook, vì
    {hook_block} chỉ thế chỗ bằng rỗng, không kèm dòng trống thừa nào khác."""
    domain_focus = load_domain_focus(profile_id)
    if extra_note:
        domain_focus = (domain_focus + chr(10) + extra_note).strip()
    lens = load_lens(profile_id)
    print(f"[qc_script_sol] lens={lens} profile={profile_id or '-'}", file=sys.stderr)
    prompt = LENS_TMPL[lens].format(title=title, domain_focus=domain_focus, script=script_text, hook_block=hook_block)
    text, usage = sol_client.chat(prompt, max_tokens=6000, timeout=300)
    verdict = parse_verdict(text)
    print(text)
    print(f"\n[verdict={verdict}] usage={json.dumps(usage)}", file=sys.stderr)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return verdict, text


def run_hook(candidates_text, title, thumb_text, promise_text, profile_id=None, out=None):
    """Chấm 3 ứng viên HOOK 20-30s (lens riêng, KHÔNG đi qua LENS_TMPL/load_lens vì hook được chấm
    TRƯỚC khi có kịch bản, không phải theo profile.script_qc.lens của toàn văn). Không có REMAKE —
    xem lý do ở comment khối NOI_TU_HOOK/HOOK_TMPL phía trên. `profile_id` nhận cho ĐỒNG NHẤT chữ ký
    với run() (Task 7 gọi cả 2 hàm cùng chỗ) nhưng hiện chưa dùng — hook không có domain_focus riêng."""
    prompt = HOOK_TMPL.format(title=title or "(chưa chốt)", thumb_text=thumb_text or "(chưa có)",
                              promise_text=promise_text or "(không có — dùng tư liệu tập)", candidates=candidates_text)
    text, usage = sol_client.chat(prompt, max_tokens=3000, timeout=240)
    m = re.search(r"CHỌN\s*[:：]\s*([123])", text)
    chon = int(m.group(1)) if m else 1
    verdict = "PASS" if re.search(r"KẾT QUẢ\s*[:：]\s*PASS", text, re.I) else "FIX"
    print(text)
    print(f"\n[verdict={verdict} chon={chon}] usage={json.dumps(usage)}", file=sys.stderr)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return verdict, chon, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True, help="đường dẫn script.txt")
    ap.add_argument("--title", help="tiêu đề video (chuỗi trực tiếp)")
    ap.add_argument("--title-file", help="file mà DÒNG ĐẦU là tiêu đề (quy ước listting.txt)")
    ap.add_argument("--profile", help="id lane (profiles/profiles/<id>.json) — lấy domain_focus riêng")
    ap.add_argument("--out", help="lưu output thô ra file")
    args = ap.parse_args()

    title = args.title
    if args.title_file:
        lines = Path(args.title_file).read_text(encoding="utf-8").splitlines()
        title = next((l.strip() for l in lines if l.strip()), "")
    if not title:
        title = "(chưa chốt tiêu đề)"

    script_text = Path(args.script).read_text(encoding="utf-8")
    verdict, _ = run(script_text, title, profile_id=args.profile, out=args.out)
    sys.exit(0 if verdict == "PASS" else 2 if verdict == "FIX" else 3)


if __name__ == "__main__":
    main()
