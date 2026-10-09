---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量搜尋技術"
nav_order: 15
has_children: true
has_toc: false
redirect_from:
  - /search-plugins/knn/
  - /search-plugins/knn/index/ 
  - /vector-search/vector-search-techniques/     
---

# 向量搜尋技術

OpenSearch 以 *k-nearest neighbors*（k 最近鄰，簡稱 *k-NN*）搜尋的方式實作向量搜尋。k-NN 搜尋會在向量索引中找出距離查詢點最近的 k 個鄰居。若要判定鄰居，您可以指定用來測量點之間距離的空間（距離函式）。

OpenSearch 支援三種不同的方法，可從向量索引中取得 k 個最近鄰：

- [近似搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/)（approximate k-NN，或稱 ANN）：傳回查詢向量的近似最近鄰。一般而言，近似搜尋演算法會犧牲編製索引的速度與搜尋準確度，以換取效能上的好處，例如更低的延遲、更小的記憶體佔用量，以及更具擴展性的搜尋。對大多數使用情境而言，近似搜尋是最佳選擇。

- 精確搜尋：對向量欄位進行暴力式、精確的 k-NN 搜尋。OpenSearch 支援下列幾種精確搜尋類型：
  - [使用評分指令碼的精確搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-score-script/)：透過評分指令碼，您可以在執行最近鄰搜尋之前，先對索引套用篩選條件。
  - [Painless 擴充功能]({{site.url}}{{site.baseurl}}/search-plugins/knn/painless-functions/)：將距離函式新增為 Painless 擴充功能，讓您能以更複雜的方式組合使用。您可以使用此方法對索引執行暴力式、精確的向量搜尋，同時也支援預先篩選。


一般而言，較大型的資料集應選擇 ANN 方法，因為它的擴展性明顯較佳。對於較小、且您可能需要套用篩選條件的資料集，則應選擇自訂評分的方式。如果您的使用情境較為複雜，需要將距離函式納入評分方法的一部分，則應使用 Painless 指令碼的方式。

## 近似搜尋

OpenSearch 支援多種後端演算法（_methods_）以及實作這些演算法的程式庫（_engines_）。它會根據所選的模式與可用的記憶體，自動選擇最佳組態。如需更多資訊，請參閱 [方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。

[`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/) 提供了額外的 `jvector` 引擎，並具備 `disk_ann` 方法。此外掛程式並未包含在任何 OpenSearch 發行版本中，也無法與 `opensearch-knn` 一併安裝。

## 使用稀疏向量

_神經稀疏搜尋_（Neural sparse search）透過使用稀疏嵌入模型與反向索引，提供密集向量搜尋以外的高效替代方案，效能與 BM25 相近。不同於需要大量記憶體與 CPU 資源的密集向量方法，稀疏搜尋會建立一份詞元與權重的配對清單，並將其儲存在 rank features 索引中。這種做法結合了傳統搜尋的效率與神經網路的語意理解能力。OpenSearch 同時支援透過資料匯入管線自動產生嵌入，以及直接匯入稀疏向量。如需更多資訊，請參閱 [神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。

## 結合多種搜尋技術

_混合搜尋_（Hybrid search）透過結合 OpenSearch 中的多種搜尋技術來提升搜尋相關性。它將傳統關鍵字搜尋與以向量為基礎的語意搜尋整合在一起。透過可組態的搜尋管線，混合搜尋會將不同搜尋方法的分數進行標準化並加以合併，以提供統一且具相關性的結果。這種做法對於同時重視語意理解與精確比對的複雜查詢特別有效。搜尋管線還可以進一步透過後置篩選運算與彙總進行自訂，以符合特定的搜尋需求。如需更多資訊，請參閱 [混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/)。
