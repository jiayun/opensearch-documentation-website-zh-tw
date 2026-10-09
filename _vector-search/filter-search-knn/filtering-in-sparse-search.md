---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經稀疏 ANN 搜尋中的篩選"
parent: Filtering data
nav_order: 40
---

# 神經稀疏 ANN 搜尋中的篩選

您可以透過下列方式執行帶有篩選的神經稀疏近似最近鄰 (ANN) 搜尋查詢：

- 在 `neural_sparse` 查詢的 `method_parameters` 中提供 `filter`。篩選由為 `sparse_vector` 欄位設定的引擎評估，因此篩選的套用方式取決於該引擎。
- 將 `neural_sparse` 查詢包裝在 [布林值篩選](#using-a-boolean-filter-with-neural-sparse-ann-search) 中。篩選在引擎之外評估，於查詢傳回前 `k` 筆結果之後套用，且兩種引擎的套用方式相同。

## 套用篩選
**於 3.9 版導入**
{: .label .label-purple }

神經稀疏 ANN 搜尋支援兩種引擎，透過 `sparse_vector` 欄位的 `method.engine` 對應參數選取。當篩選具有高度選擇性時，兩種引擎都會退回精確搜尋，但當它們執行近似搜尋時，差異在於篩選是在擷取之前或之後套用。兩種引擎的查詢語法完全相同。如需引擎的更多資訊，請參閱 [引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

該演算法使用下列變數來決定如何套用篩選：

- N：索引中的文件數。
- P：套用篩選後文件子集中的文件數 (P <= N)。
- k：回應中要傳回的最大向量數。

當 P 小於 k 時，兩種引擎都會對 P 筆篩選後的文件執行精確搜尋，否則傳回的結果會遠少於 k 筆。當 P 大於 k 時，引擎會依照下列方式套用篩選。

| 引擎 | 篩選的套用方式 | 結果數量 |
|:--- |:--- |:--- |
| `lucene` (預設) | 後置篩選。演算法在 N 筆文件上執行，篩選套用於結果，因此結果是前幾名相符項目與篩選的交集。 | 具選擇性的篩選可能傳回少於 `k` 筆結果。 |
| `native` | 前置篩選。篩選會以候選集的形式下推至引擎，因此擷取會在篩選後的集合內執行。 | 傳回完整的 `k` 筆結果。 |

### 使用 Lucene 引擎進行後置篩選

當 P 大於 k 時，Lucene 引擎會在 N 筆文件上執行神經稀疏 ANN 搜尋演算法，並將篩選套用於結果。由於篩選套用於近似結果，具選擇性的篩選可能傳回少於 k 筆結果。

### 使用 native 引擎進行前置篩選

當 P 大於 k 時，native 引擎會在擷取開始前將篩選以候選集的形式下推。近似擷取接著會在篩選後的集合內執行，因此具選擇性的篩選不會減少結果數量，查詢會傳回完整的 `k` 筆結果。

若要對欄位使用 native 引擎，請在欄位對應中將 `method.engine` 設定為 `native`。

native 引擎預設為停用，需要額外的節點設定。請在建立使用該引擎的欄位之前啟用引擎。如需更多資訊，請參閱 [啟用 native 引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#enabling-the-native-engine)。
{: .note}

下列請求會建立一個等同於範例中使用的 `hotels-index` 索引的索引，其中 `name_embedding` 欄位使用 native 引擎：

```json
PUT /hotels-index-native
{
  "settings": {
    "index": {
      "sparse": true
    }
  },
  "mappings": {
    "properties": {
      "name":{
        "type": "text"
      },
      "rating": {
        "type": "integer"
      },
      "parking": {
        "type": "boolean"
      },
      "name_embedding":{
        "type": "sparse_vector",
        "method": {
          "name": "seismic",
          "engine": "native",
          "parameters": {
            "quantization_ceiling_ingest": 16,
            "n_postings": 4000,
            "cluster_ratio": 0.1,
            "summary_prune_ratio": 0.4,
            "approximate_threshold": 1000000,
            "forward_index": "per_block"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用神經稀疏 ANN 搜尋篩選

在此範例中，您將建立一個索引，並搜尋評分高、有停車場且名稱符合搜尋條件的三家旅館。索引使用預設的 Lucene 引擎，因此篩選會在近似擷取之後套用。若要使用前置篩選執行相同的查詢，請將欄位對應至 native 引擎，如 [使用 native 引擎進行前置篩選](#pre-filtering-using-the-native-engine) 所述。

### 步驟 1：建立新索引

在執行帶有篩選的神經稀疏 ANN 搜尋之前，您需要建立一個包含 `sparse_vector` 欄位的索引。

下列請求會建立名為 `hotels-index` 的新索引：

```json
PUT /hotels-index
{
  "settings": {
    "index": {
      "sparse": true
    }
  },
  "mappings": {
    "properties": {
      "name":{
        "type": "text"
      },
      "rating": {
        "type": "integer"
      },
      "parking": {
        "type": "boolean"
      },
      "name_embedding":{
        "type": "sparse_vector",
        "method": {
          "name": "seismic",
          "parameters": {
            "quantization_ceiling_ingest": 16,
            "n_postings": 4000,
            "cluster_ratio": 0.1,
            "summary_prune_ratio": 0.4,
            "approximate_threshold": 1000000
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將資料加入索引

接下來，將資料加入您的索引。

下列請求會加入 10 筆包含旅館名稱嵌入、評分與停車場資訊的文件：

```json
POST /_bulk
{ "index": { "_index": "hotels-index", "_id": "1" } }
{"parking":true, "name":"Grand Plaza Hotel", "rating":10, "name_embedding":{"8232":7.7817574, "2882":5.847375, "3309":5.575121}}
{ "index": { "_index": "hotels-index", "_id": "2" } }
{"parking":true, "name":"Azure Beach Hotel", "rating":7, "name_embedding":{"24296":8.380939, "3509":5.5722017, "3309":5.575121}}
{ "index": { "_index": "hotels-index", "_id": "3" } }
{"parking":false, "name":"Mountain Lodge", "rating":9, "name_embedding":{"3137":5.615391, "7410":7.636689}}
{ "index": { "_index": "hotels-index", "_id": "4" } }
{"parking":true, "name":"Tropical Beach Resort", "rating":4, "name_embedding":{"7001":6.25483, "5133":6.2035937, "3509":5.5722017}}
{ "index": { "_index": "hotels-index", "_id": "5" } }
{"parking":false, "name":"Coastal Retreat", "rating":5, "name_embedding":{"5780":6.767954, "7822":7.8309207}}
{ "index": { "_index": "hotels-index", "_id": "6" } }
{"parking":true, "name":"Sunset Resort", "rating":2, "name_embedding":{"7001":6.25483, "10434":7.0848904}}
{ "index": { "_index": "hotels-index", "_id": "7" } }
{"parking":true, "name":"Crystal Beach Resort", "rating":1, "name_embedding":{"6121":6.5081306, "7001":6.25483, "3509":5.5722017}}
{ "index": { "_index": "hotels-index", "_id": "8" } }
{"parking":true, "name":"Crystal Beach Resort", "rating":9, "name_embedding":{"6121":6.5081306, "7001":6.25483, "3509":5.5722017}}
{ "index": { "_index": "hotels-index", "_id": "9" } }
{"parking":true, "name":"Azure Beach Hotel", "rating":6, "name_embedding":{"24296":8.380939, "3509":5.5722017, "3309":5.575121}}
{ "index": { "_index": "hotels-index", "_id": "10" } }
{"parking":true, "name":"Garden Court Hotel", "rating":9, "name_embedding":{"2457":4.862541, "3871":5.785374, "3309":5.575121}}
```
{% include copy-curl.html %}

### 步驟 3：使用篩選條件搜尋您的資料

現在您可以建立帶有篩選條件的神經稀疏 ANN 搜尋。在 `neural_sparse` 查詢子句的 `method_parameters` 欄位中，加入用來搜尋最近鄰的關注點、要傳回的最近鄰數量（`k`），以及帶有限制條件的篩選條件。視您希望篩選條件有多嚴格而定，您可以在單一請求中新增多個查詢子句。

下列請求會建立神經稀疏 ANN 搜尋查詢，搜尋名稱符合文字「beach resort」、評分介於 8 到 10（含）之間，且提供停車位的前三家旅館：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "neural_sparse": {
      "name_embedding": {
        "query_text": "beach resort",
        "method_parameters": {
          "k": 3,
          "filter": {
            "bool": {
              "must": [
                {
                  "range": {
                    "rating": {
                      "gte": 8,
                      "lte": 10
                    }
                  }
                },
                {
                  "term": {
                    "parking": "true"
                  }
                }
              ]
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回最接近搜尋點且符合篩選條件的三家旅館：

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 70.08806,
    "hits": [
      {
        "_index": "hotels-index",
        "_id": "8",
        "_score": 70.08806,
        "_source": {
          "parking": true,
          "name": "Crystal Beach Resort",
          "rating": 9,
          "name_embedding": {
            "3509": 5.5722017,
            "6121": 6.5081306,
            "7001": 6.25483
          }
        }
      },
      {
        "_index": "hotels-index",
        "_id": "1",
        "_score": 0,
        "_source": {
          "parking": true,
          "name": "Grand Plaza Hotel",
          "rating": 10,
          "name_embedding": {
            "2882": 5.847375,
            "3309": 5.575121,
            "8232": 7.7817574
          }
        }
      },
      {
        "_index": "hotels-index",
        "_id": "10",
        "_score": 0,
        "_source": {
          "parking": true,
          "name": "Garden Court Hotel",
          "rating": 9,
          "name_embedding": {
            "2457": 4.862541,
            "3309": 5.575121,
            "3871": 5.785374
          }
        }
      }
    ]
  }
}
```

## 查詢外的後置篩選

您也可以使用 [布林值篩選](#using-a-boolean-filter-with-neural-sparse-ann-search) 套用後置篩選。在這種情況下，篩選條件是在引擎外部評估，因此 Lucene 引擎和 native 引擎會以相同方式套用。由於篩選是在神經稀疏 ANN 搜尋擷取其前 k 個結果之後才進行，最終傳回的結果數量可能會遠小於 k。

### 搭配神經稀疏 ANN 搜尋使用布林值篩選

布林值篩選由包含 `neural_sparse` 查詢和篩選條件的 `bool` 查詢組成。例如，下列查詢會搜尋名稱符合文字「beach resort」的旅館，然後篩選結果以傳回評分介於 8 到 10（含）之間，且提供停車位的旅館：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "bool": {
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "rating": {
                  "gte": 8,
                  "lte": 10
                }
              }
            },
            {
              "term": {
                "parking": "true"
              }
            }
          ]
        }
      },
      "must": [
        {
          "neural_sparse": {
            "name_embedding": {
              "query_text": "beach resort",
              "method_parameters": {
                "top_n": 3,
                "heap_factor": 1.0,
                "k": 20
              }
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的旅館文件：

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 70.08806,
    "hits": [
      {
        "_index": "hotels-index",
        "_id": "8",
        "_score": 70.08806,
        "_source": {
          "parking": true,
          "name": "Crystal Beach Resort",
          "rating": 9,
          "name_embedding": {
            "3509": 5.5722017,
            "6121": 6.5081306,
            "7001": 6.25483
          }
        }
      }
    ]
  }
}
```

## 後續步驟

- 如需神經稀疏 ANN 搜尋的詳細資訊，請參閱 [神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。
- 如需 Lucene 引擎和 native 引擎的詳細資訊，請參閱 [引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。
