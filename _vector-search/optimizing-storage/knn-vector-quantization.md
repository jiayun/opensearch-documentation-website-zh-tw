---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量量化"
parent: Optimizing vector storage
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /search-plugins/knn/knn-vector-quantization/
outside_cards:
- heading: 半精度浮點向量
  description: 以 16 位元浮點格式原生儲存向量
  link: /mappings/supported-field-types/knn-memory-optimized/#half-float-vectors
- heading: 位元組向量
  description: 將向量量化為位元組向量
  link: /mappings/supported-field-types/knn-memory-optimized/#byte-vectors
- heading: 二進位向量
  description: 將向量量化為二進位向量
  link: /mappings/supported-field-types/knn-memory-optimized/#binary-vectors
inside_cards:
- heading: Lucene 純量量化
  description: 為 Lucene 引擎使用內建的純量量化
  link: /vector-search/optimizing-storage/lucene-scalar-quantization/
- heading: Faiss 純量量化
  description: 為 Faiss 引擎使用內建的純量量化
  link: /vector-search/optimizing-storage/faiss-scalar-quantization/
- heading: 使用純量量化的精確搜尋
  description: 搭配 flat 方法使用純量量化進行精確搜尋
  link: /vector-search/optimizing-storage/exact-search-scalar-quantization/
- heading: Faiss 乘積量化
  description: 為 Faiss 引擎使用內建的乘積量化
  link: /vector-search/optimizing-storage/faiss-product-quantization/
- heading: 二進位量化
  description: 為 Faiss 引擎使用內建的二進位量化
  link: /vector-search/optimizing-storage/binary-quantization/
---

# 向量量化

根據預設，OpenSearch 支援 `float` 類型向量的編製索引與查詢，其中向量的每個維度佔用 4 位元組的記憶體。對於需要大規模匯入的使用案例，保留 `float` 向量的成本可能會很高，因為 OpenSearch 需要建構、載入、儲存及搜尋圖（針對原生 `faiss` 與 `nmslib` [已棄用] 引擎）。若要減少記憶體使用量，您可以使用向量量化。

OpenSearch 支援多種量化方式。一般而言，量化程度會在最近鄰搜尋的準確性與向量搜尋所耗用的記憶體使用量之間形成取捨。

## 在 OpenSearch 外部量化向量

將向量匯入 OpenSearch 索引之前，先在 OpenSearch 外部進行量化。

{% include cards.html cards=page.outside_cards %}

## 在 OpenSearch 內量化向量

使用 OpenSearch 內建的量化功能來量化向量。

{% include cards.html cards=page.inside_cards %}