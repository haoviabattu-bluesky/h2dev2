---
phase: 3
title: "M1 — adapter nguồn tư liệu mới (NARA; LOC/JAXA/ESA/NOAA đã probe và loại)"
status: blocked
priority: P2
effort: "0.5d"
dependencies: []
smoke_test: "CHƯA — code NARA đã viết, chạy `--dry-run --sources nara` báo đúng 'thiếu NARA_API_KEY'; cần key miễn phí để test thật"
---

## Overview
Probe thật 5 nguồn từ OpenMontage ngày 2026-09-21 trước khi port. Kết quả khác hẳn README của
OpenMontage ("works without API key"): chỉ NARA đáng làm, và cần key.

## Kết quả probe (bằng chứng, đừng probe lại)
| Nguồn | Thực tế đo được | Quyết định |
|---|---|---|
| NARA `catalog.archives.gov/api/v2/records/search` | Không key → trả **HTML web app** (HTTP 200, không phải 401). Cần `x-api-key` — đăng ký miễn phí tại catalog.archives.gov → My Account → API key | **Làm** (đã code `stock_sources.nara`, đợi key) |
| LOC `loc.gov/search/?fo=json` (+ `/pictures/`, `/free-to-use/`) | **403 Cloudflare "Just a moment"** từ IP máy này, cả UA browser. Proxy 1 (proxypanel hao2) SOCKS5 auth fail lúc test | Loại — cần cf_clearance (skill cloudflare_capsolver) hoặc proxy US sống; không đáng cho 1 nguồn |
| JAXA `jda.jaxa.jp/search.php?keyword=` | Scrape được, ảnh trên S3 tải thẳng. Nhưng trang ghi **Copyright: JAXA** — không PD/CC | Loại theo luật dự án "không đoán giấy phép, chỉ PD + CC BY" (`stock_sources._license_ok`) |
| ESA | CC BY-**SA** 3.0 IGO | Loại — SA bị `_BAD_SUFFIX` chặn sẵn |
| NOAA `noaa.gov/search` | 404; trang NCEI không có link .mp4 — code OpenMontage đã cũ | Loại |

## Related Code Files
- Modified: `pipeline/stock_sources.py` (+`nara()`), `pipeline/stockfetch.py` (import + dispatch `nara`)

## Việc còn lại để đóng phase
1. Anh đăng ký key NARA (miễn phí) → ghi `NARA_API_KEY=...` vào `pipeline/.env`.
2. `py -3.13 stockfetch.py --q "iwo jima 1945" --n 3 --sources nara --dry-run` → ≥1 item, license PD, url .jpg/.mp4.
3. Nếu cấu trúc JSON khác giả định (`body.hits.hits[]._source.record.digitalObjects[].objectUrl`) thì sửa parser theo response thật rồi ghi smoke_test.
