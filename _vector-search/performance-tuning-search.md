---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋效能調校"
nav_order: 20
parent: Performance tuning
---

# 向量搜尋查詢效能調校

請依照下列步驟改善搜尋效能。

## 減少分段數量

若要改善搜尋效能，您必須將分段數量控制在合理範圍內。Lucene 的 IndexSearcher 會搜尋分片中的所有分段，以找出 'size' 筆最佳結果。

每個分片只有一個分段時，搜尋延遲可達最佳效能。您可以設定索引使用多個分片，以避免分片過大並達到更高的平行度。

您可以選擇較長的重新整理間隔來控制分段數量，或在編製索引時停用重新整理間隔，要求 OpenSearch 減緩分段建立速度。

## 預熱索引

原生程式庫索引會在編製索引時建構，但在第一次搜尋時才載入記憶體。在 Lucene 中，每個分段會依序搜尋（因此對 k-NN 而言，每個分段會傳回最多 k 個查詢點的最近鄰居）。最終的 `size` 筆結果會依分數排序，從分片內所有分段層級的結果中傳回（分數越高代表結果越好）。

原生程式庫索引一旦載入（原生程式庫索引是在 OpenSearch JVM 之外載入），OpenSearch 會將它們快取在記憶體中。初始查詢成本高昂，需要數秒才能完成，而後續查詢則較快，可在數毫秒內完成（假設 k-NN 熔斷器未被觸發）。

您可以使用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)，讓引擎在搜尋時只載入必要的位元組，而不是在 JVM 之外載入整個索引。啟用此模式後，Warm-up API 只會將所需的資料載入記憶體，並開啟底層索引的讀取串流。因此，即使啟用了記憶體最佳化搜尋，Warm-up API 也有助於確保預熱後的搜尋執行得更快。

若要避免第一次查詢時的延遲，您可以對想要搜尋的索引使用 warmup API 操作：

```json
GET /_plugins/_knn/warmup/index1,index2,index3?pretty
{
    "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
    }
}
```
{% include copy-curl.html %}

warmup API 操作會將指定索引的所有分片（主要分片與副本分片）的所有原生程式庫索引載入快取，因此初始搜尋時不會有載入原生程式庫索引的負擔。

此 API 操作只會將作用中索引的分段載入快取。如果合併或重新整理操作在此 API 執行後才完成，或者您新增了新文件，則需要重新執行此 API，將那些原生程式庫索引載入記憶體。
{: .warning}


## 避免讀取儲存欄位

如果您的使用情境只需要讀取最近鄰居的 ID 與分數，您可以停用儲存欄位的讀取，以節省原本用於從儲存欄位擷取向量的時間。若要完全停用儲存欄位，請將 `_source` 設為 `false`：

```json
GET /my-index/_search
{
  "_source": false,
  "query": {
    "knn": {
      "vector_field": {
        "vector": [ 0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢只會傳回文件 ID 與分數，因此當您不需要實際文件內容時，這是最快的選項。如需詳細資訊，請參閱[停用 `_source`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#disabling-_source)。

## 從搜尋結果中排除向量

如果您需要文件內容但想最佳化效能，您可以只在搜尋結果中排除向量欄位。這種做法可減少網路傳輸量，同時仍能存取其他文件欄位。若要從搜尋結果中排除向量，請在 `_source.excludes` 中提供向量欄位名稱：

```json
GET /my-index/_search
{
  "_source": {
    "excludes": [
      "vector_field"
    ]
  },
  "query": {
    "knn": {
      "vector_field": {
        "vector": [ 0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

如需詳細資訊，請參閱[擷取特定欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/)。

## 自動從搜尋結果中排除向量
**3.8 版新增**
{: .label .label-purple }

OpenSearch 可以自動從搜尋回應中排除向量欄位，因此您不必在每次請求的 `_source.excludes` 中逐一列出。啟用後，`knn_default_excludes` [系統產生的搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/system-generated-search-processors/)會檢查每個搜尋請求的索引對應，識別所有 `knn_vector` 欄位（包括巢狀於物件或 nested 欄位中的欄位），並在請求執行前將它們加入 `_source.excludes`。這可減少搜尋回應的承載大小。

自動排除只會改變回應中傳回的欄位，不會影響評分：在查詢執行期間透過 `doc['vector_field']` 或 `params._source['vector_field']` 存取向量的指令碼仍會讀取完整向量，因為排除是在擷取階段而非查詢階段套用。向量也會完整儲存，並透過[衍生來源]({{site.url}}{{site.baseurl}}/vector-search/settings/)重建，因此從回應中排除向量並不會將它們從索引中移除。

此處理器預設為停用。若要啟用，請將其工廠 `knn_default_excludes_factory` 加入 `cluster.search.enabled_system_generated_factories` 叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.search.enabled_system_generated_factories": [
      "knn_default_excludes_factory"
    ]
  }
}
```
{% include copy-curl.html %}

啟用處理器後，搜尋回應中的 `_source` 預設會省略向量欄位：

```json
GET /my-index/_search
{
  "query": {
    "knn": {
      "vector_field": {
        "vector": [ 0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

### 覆寫自動排除

處理器不會排除您在請求中指定的任何欄位。請使用下列其中一種選項來控制回應中的 `_source`：

- 若要傳回所有欄位（包括向量欄位），請將 `_source` 設為 `true`。
- 若要傳回特定向量欄位，請將它列在 `_source.includes` 中。
- 若要完全省略來源文件內容，請將 `_source` 設為 `false`。

例如，下列請求明確包含 `vector_field`，因此即使處理器已啟用，回應仍會傳回該欄位：

```json
GET /my-index/_search
{
  "_source": {
    "includes": [
      "vector_field"
    ]
  },
  "query": {
    "knn": {
      "vector_field": {
        "vector": [ 0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

處理器也會略過已列在索引對應的 `_source.excludes` 或請求的 `_source.includes` 或 `_source.excludes` 中的任何欄位。

## 使用 doc values 擷取向量
**3.7 版新增**
{: .label .label-purple }

使用 `docvalue_fields` 可直接從磁碟上的欄式儲存擷取向量欄位，避免讀取與解析完整的 `_source` 文件。在單一搜尋請求中擷取大量向量時，這種做法明顯更快。

為獲得最佳效能，請使用 `_source.excludes` 或將 `_source` 設為 `false`，從 `_source` 中排除向量欄位。這可確保 OpenSearch 只從 `doc_values` 讀取向量，而不會從儲存的 `_source` 重複解壓縮。
{: .tip}

如需支援的格式與範例，請參閱[使用 `docvalue_fields` 擷取向量欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#retrieving-vector-fields-using-docvalue_fields)。
