---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經查詢"
parent: AI and vector search queries
nav_order: 50
---

# Neural 查詢

使用 `neural` 查詢，在[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)中依文字或圖片搜尋向量欄位。

## 請求本文欄位

在 `neural` 查詢中包含下列請求欄位：

```json
"neural": {
  "<vector_field>": {
    "query_text": "<query_text>",
    "query_image": "<image_binary>",
    "model_id": "<model_id>",
    "k": 100
  }
}
```

最上層的 `vector_field` 指定要執行搜尋查詢的向量或語意欄位。下表列出其他 neural 查詢欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- 
`query_text` | 字串 | 選用 | 用來產生向量嵌入的查詢文字。您必須至少指定 `query_text` 或 `query_image` 其中之一。
`query_image` | 字串 | 選用 | 對應查詢圖片的 Base64 編碼字串，用來產生向量嵌入。您必須至少指定 `query_text` 或 `query_image` 其中之一。
`model_id` | 字串 | 若目標欄位是語意欄位，則為選用。若目標欄位是 `knn_vector` 欄位，且未設定預設模型 ID，則為必要。如需更多資訊，請參閱[在索引或欄位上設定預設模型]({{site.url}}{{site.baseurl}}/search-plugins/neural-text-search/#setting-a-default-model-on-an-index-or-field)。 | 將用來從查詢文字產生向量嵌入的模型 ID。模型必須先部署到 OpenSearch，才能在 neural 搜尋中使用。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)與[神經搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-search/)。不可與 `semantic_field_search_analyzer` 一併提供。
`k` | 整數 | 選用 | k-NN 搜尋傳回的結果數量。只能指定 `k`、`min_score` 或 `max_distance` 其中一個變數。若未指定變數，預設為 `k`，其值為 `10`。
`min_score` | 浮點數 | 選用 | 搜尋結果的最低分數門檻。只能指定 `k`、`min_score` 或 `max_distance` 其中一個變數。如需更多資訊，請參閱[徑向搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/radial-search-knn/)。
`max_distance` | 浮點數 | 選用 | 搜尋結果的最大距離門檻。只能指定 `k`、`min_score` 或 `max_distance` 其中一個變數。如需更多資訊，請參閱[徑向搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/radial-search-knn/)。
`filter` | 物件 | 選用 | 可用來減少所考量文件數量的查詢。如需篩選器用法的更多資訊，請參閱[使用篩選器的向量搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/filter-search-knn/)。
`method_parameters` | 物件 | 選用 | 用於微調搜尋的其他參數：<br>- `ef_search`（整數）：要檢視的向量數量（適用於 `hnsw` 方法）<br>- `nprobes`（整數）：要檢視的桶數量（適用於 `ivf` 方法）。如需更多資訊，請參閱[在查詢中指定方法參數]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/index/#specifying-method-parameters-in-the-query)。
`rescore` | 物件或布林值 | 選用 | 用於設定重新評分功能的參數：<br>- `oversample_factor`（浮點數）：控制在重新評分之前擷取多少候選向量。有效值在 `[1.0, 100.0]` 範圍內。對於 `in_memory` 模式（不重新評分）的欄位，預設為 `false`；對於 `on_disk` 模式的欄位，預設為 `enabled`（動態值）。在 `on_disk` 模式下，預設的 `oversample_factor` 由 `compression_level` 決定。如需更多資訊，請參閱[壓縮層級表]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)。若要以 `1.0` 的預設 `oversample_factor` 明確啟用重新評分，請將 `rescore` 設為 `true`。如需更多資訊，請參閱[重新評分結果]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/index/#rescoring-results)。
`expand_nested_docs` | 布林值 | 選用 | 當設定為 `true` 時，會擷取每個父文件內所有巢狀欄位文件的分數。與巢狀查詢搭配使用。如需更多資訊，請參閱[使用巢狀欄位的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/nested-search-knn/)。
`semantic_field_search_analyzer` | 字串 | 選用 | 使用稀疏編碼模型時，指定用來斷詞 `query_text` 的分析器。有效值為 `standard`、`bert-uncased` 與 `mbert-uncased`。不可與 `model_id` 一起使用。如需更多資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/)。
`query_tokens` | 詞元（字串）對權重（浮點數）的對應 | 選用 | 以詞元及其權重形式表示的原始稀疏向量。作為 `query_text` 的替代方案，用於直接向量輸入。必須指定 `query_text` 或 `query_tokens` 其中之一。

#### 範例請求

下列範例顯示 `k` 值為 `100`，並包含範圍查詢與詞彙查詢之篩選器的搜尋：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "Hi world",
        "query_image": "iVBORw0KGgoAAAAN...",
        "k": 100,
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
```
{% include copy-curl.html %}

下列搜尋查詢包含 k-NN 徑向搜尋 `min_score` 為 `0.95`，以及包含範圍查詢與詞彙查詢之篩選器：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "Hi world",
        "query_image": "iVBORw0KGgoAAAAN...",
        "min_score": 0.95,
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
```
{% include copy-curl.html %}

下列搜尋查詢包含 k-NN 徑向搜尋 `max_distance` 為 `10`，以及包含範圍查詢與詞彙查詢之篩選器：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "Hi world",
        "query_image": "iVBORw0KGgoAAAAN...",
        "max_distance": 10,
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
```
{% include copy-curl.html %}

下列範例顯示使用稠密模型對 `semantic` 欄位進行搜尋。`semantic` 欄位會在其組態中儲存模型資訊。`neural` 查詢會自動從索引對應中 `semantic` 欄位的組態擷取 `model_id`，並改寫查詢以指向對應的嵌入欄位：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural": {
      "passage": {
        "query_text": "Hi world"
        "k": 100
      }
    }
  }
}
```
{% include copy-curl.html %}

下列範例顯示使用稀疏編碼模型對 `semantic` 欄位進行搜尋。此搜尋使用稀疏嵌入：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural": {
      "passage": {
        "query_tokens": {
          "worlds": 0.57605183
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[語意欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/)。