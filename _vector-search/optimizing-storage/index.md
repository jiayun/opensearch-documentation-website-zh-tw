---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最佳化向量儲存"
nav_order: 60
has_children: true
has_toc: false
redirect_from:
  - /vector-search/optimizing-storage/
storage_cards:
- heading: 向量量化
  description: 透過向量的量化減少向量儲存空間
  link: /vector-search/optimizing-storage/knn-vector-quantization/
- heading: 以磁碟為基礎的向量搜尋
  description: 使用二元量化降低向量工作負載的營運成本
  link: /vector-search/optimizing-storage/disk-based-vector-search/
---

# 最佳化向量儲存

向量搜尋作業可能相當耗用資源，尤其是在處理大規模向量資料集時。OpenSearch 提供多種最佳化技術來降低記憶體使用量。

{% include cards.html cards=page.storage_cards %}

## 使用 opensearch-jvector 外掛程式進行磁碟友善的量化

`jvector` 引擎由 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/) 提供，實作 DiskANN 風格的索引：它將向量儲存在磁碟上而非記憶體中，並直接從量化後的向量建立索引。這可降低記憶體使用量，且無需另外設定量化。

與內建引擎相比，`jvector` 引擎提供下列儲存優勢：

- 它從量化後的向量建立索引，減少編製索引時所需的記憶體。
- 它在合併期間以漸進方式微調量化碼簿 (codebook)，無需完整重建。
