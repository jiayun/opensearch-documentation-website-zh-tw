---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: k-NN
parent: AI and vector search queries
has_children: true
nav_order: 15
redirect_from:
  - /query-dsl/specialized/k-nn/
---

# k-NN 查詢

使用 `knn` 查詢在向量欄位上執行最近鄰搜尋。

## 傳輸通訊協定

k-NN 查詢可使用兩種傳輸通訊協定執行：

- **HTTP/REST API**：本節所記載的標準做法。
- **gRPC API**（自 3.2 起正式推出）：高效能二進位通訊協定，搭配 [k-NN (gRPC) API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/knn/)。

對於高輸送量的向量搜尋應用程式，請考慮使用 gRPC k-NN API，相較於以 HTTP 為基礎的查詢，它能提供更低的延遲與更高的輸送量。

## 請求本文欄位

在 `knn` 查詢中提供向量欄位，並在向量欄位物件中指定其他請求欄位：

```json
"knn": {
  "<vector_field>": {
    "vector": [<vector_values>],
    "k": <k_value>,
    ...
  }
}
```

最上層的 `vector_field` 會指定要對其執行搜尋查詢的向量欄位。下表列出所有支援的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`vector` | 浮點數或位元組陣列 | 必要 | 用於向量搜尋的查詢向量。向量元素的資料類型必須與所搜尋之 [`knn_vector` 欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/) 中編製索引的向量資料類型相符。
`k` | 整數 | 選用 | 要傳回的最近鄰數目。有效值範圍為 [1, 10,000]。若未指定 `max_distance` 或 `min_score`，則此欄位為必要。
`max_distance` | 浮點數 | 選用 | 搜尋結果的最大距離臨界值。`k`、`max_distance` 或 `min_score` 僅能指定其中一個。如需詳細資訊，請參閱[徑向搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/radial-search-knn/)。
`min_score` | 浮點數 | 選用 | 搜尋結果的最低分數臨界值。`k`、`max_distance` 或 `min_score` 僅能指定其中一個。如需詳細資訊，請參閱[徑向搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/radial-search-knn/)。
`filter` | 物件 | 選用 | 套用至 k-NN 搜尋的篩選條件。如需詳細資訊，請參閱[使用篩選條件的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/)。**重要**：篩選條件僅能與 `faiss` 或 `lucene` 引擎搭配使用。
`method_parameters` | 物件 | 選用 | 用於微調搜尋的其他參數：<br>- `ef_search` (整數)：要檢查的向量數目 (適用於 `hnsw` 方法)<br>- `nprobes` (整數)：要檢查的桶數 (適用於 `ivf` 方法)。如需詳細資訊，請參閱[在查詢中指定方法參數](#specifying-method-parameters-in-the-query)。
`rescore` | 物件或布林值 | 選用 | 用於設定重新評分功能的參數：<br>- `oversample_factor` (浮點數)：控制在重新評分前要擷取多少候選向量。有效值範圍為 `[1.0, 100.0]`。對於 `in_memory` 模式的欄位，預設值為 `false` (不重新評分)；對於 `on_disk` 模式的欄位，則為啟用 (含動態值)。在 `on_disk` 模式下，預設的 `oversample_factor` 由 `compression_level` 決定。如需詳細資訊，請參閱[壓縮層級表]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)。若要使用預設的 `1.0` 之 `oversample_factor` 明確啟用重新評分，請將 `rescore` 設為 `true`。如需詳細資訊，請參閱[重新評分結果](#rescoring-results)。
`expand_nested_docs` | 布林值 | 選用 | 當設為 `true` 時，會擷取每個父文件內所有巢狀欄位文件的分數。用於巢狀查詢。如需詳細資訊，請參閱[使用巢狀欄位的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/nested-search-knn/)。

## 範例請求

```json
GET /my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [1.5, 2.5],
        "k": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例請求：巢狀欄位

```json
GET /my-vector-index/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "nested_field",
      "query": {
        "knn": {
          "nested_field.my_vector": {
            "vector": [1,1,1],
            "k": 2,
            "expand_nested_docs": true
          }
        }
      },
      "inner_hits": {
        "_source": false,
        "fields":["nested_field.color"]
      },
      "score_mode": "max"
    }
  }
}
```
{% include copy-curl.html %}

## 範例請求：使用 max_distance 的徑向搜尋

下列範例顯示使用 `max_distance` 執行的徑向搜尋：

```json
GET /my-vector-index/_search
{
    "query": {
        "knn": {
            "my_vector": {
                "vector": [
                    7.1,
                    8.3
                ],
                "max_distance": 2
            }
        }
    }
}
```
{% include copy-curl.html %}


## 範例請求：使用 min_score 的徑向搜尋

下列範例顯示使用 `min_score` 執行的徑向搜尋：

```json
GET /my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [7.1, 8.3],
        "min_score": 0.95
      }
    }
  }
}
```
{% include copy-curl.html %}

## 在查詢中指定方法參數

您可以在搜尋請求中提供 `method_parameters`：

```json
GET /my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "target-field": {
        "vector": [2, 3, 5, 6],
        "k": 2,
        "method_parameters" : {
          "ef_search": 100
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

這些參數取決於建立索引時所使用的引擎與方法組合。下列各節提供支援的 `method_parameters` 相關資訊。

### ef_search

搜尋使用 `hnsw` 方法建立的索引時，您可以提供 `ef_search` 參數。`ef_search` 參數會指定為了找出前 k 個最近鄰而要檢查的向量數目。較高的 `ef_search` 值可提升召回率，但會增加搜尋延遲。此值必須為正數。

下表提供支援的引擎其 `ef_search` 參數相關資訊。

引擎 | 徑向查詢支援 | 備註
:--- | :--- | :---
`nmslib` (已棄用) | 否 | 若查詢中包含 `ef_search`，它會覆寫 `index.knn.algo_param.ef_search` 索引設定。
`faiss` | 是 | 若查詢中包含 `ef_search`，它會覆寫 `index.knn.algo_param.ef_search` 索引設定。
`lucene` | 否 | 建立搜尋查詢時，您必須指定 `k`。若同時提供 `k` 與 `ef_search`，則會將較大的值傳遞給引擎。若 `ef_search` 大於 `k`，您可以提供 `size` 參數，將最終結果數目限制為 `k`。

<!-- vale off -->
### nprobes
<!-- vale on -->

搜尋使用 `ivf` 方法建立的索引時，您可以提供 `nprobes` 參數。`nprobes` 參數會指定為了找出前 k 個最近鄰而要檢查的桶數。較高的 `nprobes` 值可提升召回率，但會增加搜尋延遲。此值必須為正數。

下表提供支援的引擎其 `nprobes` 參數相關資訊。

引擎 | 備註
:--- | :---
`faiss` | 若查詢中包含 `nprobes`，它會覆寫建立索引時所提供的值。

## 重新評分結果

您可以提供 `ef_search` 與 `oversample_factor` 參數來微調搜尋。

`oversample_factor` 參數會控制搜尋在為候選向量排名前過度取樣的倍數。使用較高的過度取樣倍數表示在排名前會考量更多候選向量，可提升準確度，但也會增加搜尋時間。選擇 `oversample_factor` 值時，請考量準確度與效率之間的取捨。例如，將 `oversample_factor` 設為 `2.0` 會使排名階段考量的候選向量數目加倍，這可能有助於獲得更佳的結果。

下列請求指定了 `ef_search` 與 `oversample_factor` 參數：

```json
GET /my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 5.5, 1.5, 5.5, 1.5, 5.5, 1.5, 5.5],
        "k": 10,
        "method_parameters": {
            "ef_search": 10
        },
        "rescore": {
            "oversample_factor": 10.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)
- [將量化結果重新評分至完整精確度]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)
