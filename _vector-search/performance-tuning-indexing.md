---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引效能調校"
nav_order: 10
parent: Performance tuning
---

# 向量搜尋索引效能調校

請採取下列任一做法來改善索引效能，尤其是在您打算一次編製大量向量的索引時。

## 停用重新整理間隔

停用重新整理間隔（預設 = 1 秒），或將重新整理間隔設為較長的期間，以避免建立多個小分段：

```json
PUT /{index_name}/_settings
{
    "index" : {
        "refresh_interval" : "-1"
    }
}
```
{% include copy-curl.html %}

請務必在索引完成後重新啟用 `refresh_interval`。

## 停用副本（沒有 OpenSearch 副本分片）

   將副本設為 `0`，以避免在主要分片與副本分片中重複建構原生程式庫索引。當您在索引完成後啟用副本時，序列化的原生程式庫索引會直接複製。如果您沒有副本，節點遺失可能會導致資料遺失，因此請務必將資料儲存在其他位置，以便在發生問題時能重試此初始載入。

## 增加索引執行緒的數量

如果您的硬體有多個核心，您可以允許原生程式庫索引建構使用多個執行緒，以加速索引程序。請使用 [knn.algo_param.index_thread_qty]({{site.url}}{{site.baseurl}}/search-plugins/knn/settings#cluster-settings) 設定來決定要分配的執行緒數量。

請監控 CPU 使用率並選擇正確的執行緒數量。由於原生程式庫索引建構的成本很高，選擇超過所需的執行緒數量可能會造成額外的 CPU 負載。


## 使用衍生的向量來源功能來降低儲存空間需求

您可以使用衍生的向量來源功能，大幅降低向量欄位的儲存空間需求。這是一項[索引設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#index-settings)，預設為啟用。此功能可避免將向量儲存在 `_source` 欄位中，同時仍維持所有功能，包括使用 `update`、`update_by_query` 和 `reindex` API 的能力。

## （專家級）視需求建構向量資料結構

只有在工作負載涉及單一次初始大量上傳，且在強制合併為單一分段後僅用於搜尋時，才建議採用此做法。

在編製索引期間，向量搜尋會為 `knn_vector` 欄位建構特殊化的資料結構，以實現高效率的近似最近鄰（k-NN）搜尋。不過，這些結構會在向量索引的[強制合併]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/)期間重建。若要最佳化索引速度，請依照下列步驟進行：

1. **停用向量資料結構的建立**：將 [`index.knn.advanced.approximate_threshold`]({{site.url}}{{site.baseurl}}/vector-search/settings/#index-settings) 設為 `-1`，以停用新分段的向量資料結構建立。 

    若要在建立索引時指定此設定，請傳送下列請求：

    ```json
    PUT /test-index/
    {
      "settings": {
        "index.knn.advanced.approximate_threshold": "-1"
      }
    }
    ```
    {% include copy-curl.html %}

    若要在建立索引後指定此設定，請傳送下列請求：

    ```json
    PUT /test-index/_settings
    {
      "index.knn.advanced.approximate_threshold": "-1"
    }
    ```
    {% include copy-curl.html %}

1. **執行大量索引**：在匯入期間不執行任何搜尋，以[大量]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)方式將資料編製索引：

    ```json
    POST _bulk
    { "index": { "_index": "test-index", "_id": "1" } }
    { "my_vector1": [1.5, 2.5], "price": 12.2 }
    { "index": { "_index": "test-index", "_id": "2" } }
    { "my_vector1": [2.5, 3.5], "price": 7.1 }
    ```
    {% include copy-curl.html %}

    如果在停用向量資料結構時執行搜尋，搜尋會使用精確 k-NN 搜尋來執行。

1. **重新啟用向量資料結構的建立**：索引完成後，將 `index.knn.advanced.approximate_threshold` 設為 `0`，以啟用向量資料結構的建立：

    ```json
    PUT /test-index/_settings
    {
      "index.knn.advanced.approximate_threshold": "0"
    }
    ```
    {% include copy-curl.html %}

    如果您在強制合併前未將設定重設為 `0`，您將需要重新編製資料的索引。
    {: .note}

1. **將分段強制合併為一個分段**：執行強制合併並指定 `max_num_segments=1`，以僅建立一次向量資料結構：

    ```json
    POST test-index/_forcemerge?max_num_segments=1
    ```
    {% include copy-curl.html %}

    強制合併後，新的搜尋請求將使用新建立的資料結構來執行近似 k-NN 搜尋。