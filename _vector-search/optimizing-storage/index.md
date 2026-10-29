---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最佳化向量儲存空間"
nav_order: 60
has_children: true
has_toc: false
redirect_from:
  - /vector-search/optimizing-storage/
storage_cards:
- heading: 向量量化
  description: 透過量化向量來減少向量儲存空間
  link: /vector-search/optimizing-storage/knn-vector-quantization/
- heading: 以磁碟為基礎的向量搜尋
  description: 使用量化來降低向量工作負載的營運成本
  link: /vector-search/optimizing-storage/disk-based-vector-search/
---

# 最佳化向量儲存空間

向量搜尋作業可能相當耗費資源，尤其是在處理大規模向量資料集時。OpenSearch 提供數種最佳化技術來減少記憶體用量。

{% include cards.html cards=page.storage_cards %}

## 使用 opensearch-jvector 外掛程式的磁碟友善量化

由 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/) 提供的 `jvector` 引擎採用 DiskANN 風格的索引方式：它將向量儲存在磁碟上而非記憶體中，並直接從量化後的向量建立索引。如此一來便能減少記憶體用量，且不需要另外設定量化。

與內建引擎相比，`jvector` 引擎提供下列儲存空間優勢：

- 它從量化後的向量建立索引，減少建立索引期間所需的記憶體。
- 它在合併期間以增量方式精進量化編碼簿，不需要完整重建。
