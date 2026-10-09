---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "效能調校"
nav_order: 70
has_children: true
redirect_from:
  - /search-plugins/knn/performance-tuning/
---

# 向量搜尋效能調校

本主題提供效能調校建議，以改善近似 k-NN（ANN）搜尋的索引編製與搜尋效能。概括而言，k-NN 依照下列原則運作：
* 每個 `knn_vector` 欄位與 Lucene 分段的配對都會建立向量索引。
* 查詢會依序在分片中的分段上執行（與其他 OpenSearch 查詢相同）。
* 協調節點會從各分片傳回的鄰近向量中，選出最終的 `size` 個鄰近向量。

以下各節提供比較 ANN 與使用評分指令碼的精確 k-NN 的相關建議。

## 引擎與叢集節點規模的建議

用於 ANN 搜尋的三種引擎各有其特性，使其在特定情境下比其他引擎更適合使用。請使用下列資訊，協助判斷哪種引擎最能滿足您的需求。

若要最佳化索引編製的輸送量，Faiss 是不錯的選擇。對於相對較小的資料集（最多數百萬個向量），Lucene 引擎的延遲與召回率表現較佳。同時，其索引大小也是各引擎中最小的，因此資料節點可以使用較小的 AWS 執行個體。如需其他考量事項，請參閱[選擇合適的方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#choosing-the-right-method-and-engine)及[記憶體估算]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#memory-estimation)。

考量叢集節點規模時，一般做法是先讓索引均勻分布於整個叢集。不過，還有其他考量事項。為協助您做出這些選擇，您可以參閱[決定網域規模](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html)一節中的 OpenSearch 受管服務指引。

## 改善召回率

召回率取決於多種因素，例如向量數量、維度、分段等。搜尋大量小型分段並彙總結果，比搜尋少量大型分段並彙總結果能獲得更好的召回率。如果您使用較小的演算法參數，較大的原生程式庫索引更容易降低召回率。為演算法參數選擇較大的值應有助於解決此問題，但會犧牲搜尋延遲與索引編製時間。務必瞭解系統對延遲與準確度的需求，再根據實驗結果選擇分段數量。

預設參數適用於較廣泛的使用案例，但請務必針對您的資料集自行進行實驗，並選擇適當的值。如需索引層級的設定，請參閱[索引設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#index-settings)。

## ANN 與評分指令碼的比較

標準 k-NN 查詢與自訂評分選項的效能表現不同。請使用具代表性的文件集進行測試，確認搜尋結果與延遲是否符合您的預期。

當初始篩選器將文件數量減少至不超過 20,000 份時，自訂評分的效果最佳。增加分片數量可以改善延遲，但請務必將分片大小維持在[建議指引]({{site.url}}{{site.baseurl}}/intro/#primary-and-replica-shards)的範圍內。