---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "篩選資料"
nav_order: 50
has_children: true
redirect_from:
  - /search-plugins/knn/filter-search-knn/ 
  - /vector-search/filter-search-knn/
---

# 篩選向量搜尋結果

若要精煉向量搜尋結果，您可以使用下列其中一種方法來篩選向量搜尋：

- [高效 k 最近鄰 (k-NN) 篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/efficient-knn-filtering/)：此方法在向量搜尋_期間_套用篩選，而非在向量搜尋之前或之後，以確保傳回 `k` 個結果（若總計至少有 `k` 個結果）。下列引擎支援此方法：
  - 使用階層式可導航小世界 (HNSW) 演算法的 Lucene 引擎（OpenSearch 2.4 及更新版本）
  - 使用 HNSW 演算法（OpenSearch 2.9 及更新版本）或 IVF 演算法（OpenSearch 2.10 及更新版本）的 Faiss 引擎。在 OpenSearch 3.1 及更新版本中，當使用 Faiss 引擎與 HNSW，且啟用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)時，會在 HNSW 走訪期間套用 [Lucene ACORN 篩選最佳化](https://github.com/apache/lucene/pull/14160)。
  - JVector 引擎，由 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)提供，支援在 `knn` 查詢子句內使用與 Lucene 和 Faiss 高效篩選相同語法的內嵌篩選。

-  [後篩選 (post-filtering)]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/post-filtering/)：由於此方法是在向量搜尋之後執行，對於限制嚴格的篩選條件，傳回的結果可能遠少於 `k` 個。此方法可使用下列兩種篩選策略：
    - [布林後篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/post-filtering/#boolean-filter-with-ann-search)：此方法先執行[近似最近鄰 (ANN)]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/) 搜尋，然後對結果套用篩選。兩個查詢部分獨立執行，然後根據查詢中提供的查詢運算子（`should`、`must` 等）合併結果。
    - [`post_filter` 參數]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/post-filtering/#the-post_filter-parameter)：此方法先對完整資料集執行 [ANN]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/) 搜尋，然後對 k-NN 結果套用篩選。

- [評分指令碼篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/scoring-script-filter/)：此方法先預先篩選文件集合，然後對篩選後的子集執行精確 k-NN 搜尋。延遲可能很高，且在篩選後的子集很大時無法擴充。

- [稀疏向量搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)：此方法對近似稀疏向量搜尋套用篩選。

下表摘要上述篩選使用案例。

篩選 | 篩選套用時機 | 搜尋類型 | 支援的引擎與方法 | `filter` 子句的放置位置
:--- | :--- | :--- | :--- | :---
高效 k-NN 篩選 | 搜尋期間（前篩選與後篩選的混合） | 近似 | - `lucene` (`hnsw`) <br> - `faiss` (`hnsw`, `ivf`) | k-NN 查詢子句內部。
布林篩選 | 搜尋之後（後篩選） | 近似 | - `lucene` <br> - `faiss` <br> - `nmslib` (deprecated) | k-NN 查詢子句外部。必須是葉子子句。
`post_filter` 參數 | 搜尋之後（後篩選） | 近似 | - `lucene`<br> - `faiss` <br> - `nmslib` (deprecated) | k-NN 查詢子句外部。
評分指令碼篩選 | 搜尋之前（前篩選） | 精確 | N/A | script score 查詢子句內部。
神經稀疏向量搜尋中的篩選 | 搜尋之後（後篩選） | 近似 | N/A | `neural_sparse` 查詢的 `method_parameters` 欄位。

## 篩選搜尋最佳化

視您的資料集和使用案例而定，您可能更注重最大化召回率或最小化延遲。下表提供各種 k-NN 搜尋組態的指引，以及用於最佳化以提高召回率或降低延遲的篩選方法。表格的前三欄提供數個 k-NN 搜尋組態範例。搜尋組態包含：

- 索引中的文件數量，其中一份 OpenSearch 文件對應一個 k-NN 向量。
- 篩選後結果中剩餘文件的百分比。此值取決於您在查詢中提供的篩選器限制程度。表格中限制最嚴格的篩選器會傳回索引中 2.5% 的文件，而限制最寬鬆的篩選器會傳回 80% 的文件。
- 希望傳回的結果數量（k）。 

估算索引中的文件數量、篩選器的限制程度，以及所需的最近鄰數量後，請使用下表選擇可最佳化召回率或延遲的篩選方法。

| 索引中的文件數量 | 篩選器傳回的文件百分比 | k | 用於提高召回率的篩選方法 | 用於降低延遲的篩選方法 |
| :-- | :-- | :-- | :-- | :-- |
| 10M | 2.5 | 100 | 高效率 k-NN 篩選/評分指令碼 | 評分指令碼 |
| 10M | 38 | 100 | 高效率 k-NN 篩選 | 高效率 k-NN 篩選 |
| 10M | 80 | 100 | 高效率 k-NN 篩選 | 高效率 k-NN 篩選 |
| 1M | 2.5 | 100 | 高效率 k-NN 篩選/評分指令碼 | 評分指令碼 |
| 1M | 38 | 100 | 高效率 k-NN 篩選 | 高效率 k-NN 篩選 |
| 1M | 80 | 100 | 高效率 k-NN 篩選 | 高效率 k-NN 篩選 |
