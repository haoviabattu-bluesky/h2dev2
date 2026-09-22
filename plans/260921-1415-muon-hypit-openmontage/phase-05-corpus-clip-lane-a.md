---
phase: 5
title: "M2 — corpus CLIP cho lane clip stock (Lane A)"
status: blocked
priority: P3
effort: "1.5d"
dependencies: [3]
smoke_test: ""
---

## Điều kiện mở phase
Lane A (`toshi-densetsu-jp`) sản xuất ≥ 1 tập/tuần — lúc đó kho dùng chung mới trả công embed.

## Overview
Port `OpenMontage/lib/corpus.py` (index.jsonl + embeddings.npy 512-d, append-only) +
`lib/clip_embedder.py` (CLIP ViT-B/32 qua transformers, CPU được, model 350 MB) +
`tools/video/clip_search.py` (rank_for_slot / find_similar_set MMR / diversify). Kho embed 1 lần
(`assets/toshi-densetsu-jp/_kho_stock/`), mỗi tập: câu script → embed text → knn thay cho
query từng câu rồi tải mới ở B5 (`make_video.py:1520`). `diversify` chặn 2 clip giống nhau đứng cạnh —
lỗi hiện `qc_canh.py` chỉ bắt "lạc lời", không bắt "trùng hình".

## Việc cụ thể khi mở
1. Cài `torch` CPU + `transformers`; đo thời gian embed 1 kho ~300 clip (lấy 1 khung giữa mỗi clip + tag text).
2. `pipeline/corpus_clip.py` (build/add/knn/diversify) ≤ 200 dòng, đọc `manifest.jsonl` hiện có.
3. Cắm vào `stock_cut.chon_nguon()` như một nguồn xếp hạng thay cho `manifest["query"]`.
4. Smoke: 1 tập cũ đã giao → so tỉ lệ cảnh lạc (qc_canh) trước/sau, mục tiêu giảm ≥ 50%.
