---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Neural sparse ANN 說明"
parent: Neural sparse
grand_parent: AI and vector search queries
nav_order: 10
---

# Neural sparse ANN 查詢說明
**3.5 版推出**
{: .label .label-purple }

您可以提供 `explain` 參數，以瞭解 neural sparse 近似最近鄰 (ANN) 查詢的分數計算方式。啟用後，它會提供每個搜尋結果評分程序的詳細資訊，包括查詢詞元修剪、量化點積計算、量化重新縮放，以及篩選器的套用。這種全面的洞察讓您更容易理解並最佳化 neural sparse ANN 查詢結果。如需 `explain` 的更多資訊，請參閱 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/)。

`explain` 在資源與時間方面都是昂貴的操作。對於生產環境叢集，我們建議僅在疑難排解時少量使用。
{: .warning }

本頁的範例與欄位說明描述的是 Lucene 引擎的說明輸出，該引擎是 `sparse_vector` 欄位的預設引擎。原生引擎的說明會報告查詢詞元修剪與精確點積分數，但不包含量化重新縮放元件。兩種引擎都會使用 `quantization_ceiling_ingest` 與 `quantization_ceiling_search` 對應參數將詞元權重量化為 8 位元，因此這兩個參數對任一引擎都有意義。兩種引擎的差異僅在於說明的細項。如需引擎的更多資訊，請參閱 [引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

只有當分段至少包含 `approximate_threshold` 份文件 (預設為 `1000000`) 時，說明才會包含本頁所述的 neural sparse ANN 元件。對較小分段的查詢會回傳標準的 `rank_features` 說明。如需更多資訊，請參閱 [混合索引編製]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#hybrid-indexing)。
{: .note}

您可以在執行 neural sparse ANN 查詢時，使用下列語法在 URL 中提供 `explain` 參數：

```json
GET {index}/_search?explain=true
POST {index}/_search?explain=true
```

`explain` 參數適用於下列類型的 neural sparse ANN 搜尋：

- 基本 neural sparse ANN 搜尋
- 含篩選器的 neural sparse ANN 搜尋

您可以將 `explain` 參數作為查詢參數提供：

```json
GET my-sparse-index/_search?explain=true
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "7001": 6.25,
          "3509": 5.57
        },
        "method_parameters": {
          "k": 5,
          "top_n": 6
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，您也可以在請求本文中提供 `explain` 參數：

```json
GET my-sparse-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "7001": 6.25,
          "3509": 5.57
        },
        "method_parameters": {
          "k": 5,
          "top_n": 3
        }
      }
    }
  },
  "explain": true
}
```
{% include copy-curl.html %}

## 範例：基本 neural sparse ANN 搜尋

```json
GET my-sparse-index/_search?explain=true
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "13723": 0.75,
          "9266": 0.61,
          "2078": 0.35,
          "2365": 0.41
        },
        "method_parameters": {
          "k": 10,
          "top_n": 6
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took": 15,
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
    "max_score": 16.059792,
    "hits": [
      {
        "_shard": "[my-sparse-index][0]",
        "_node": "iId6ipt-SCWA-7vHLh981Q",
        "_index": "my-sparse-index",
        "_id": "1",
        "_score": 16.059792,
        "_source": {
          "sparse_embedding": {
            "13723": 3.16,
            "9266": 2.85,
            "2078": 1.09,
            "2365": 0.22
          }
        },
        "_explanation": {
          "value": 16.059792,
          "description": "sparse_ann score for doc 94830 in field 'sparse_embedding'",
          "details": [
            {
              "value": 6,
              "description": "query token pruning: kept top 6 of 33 tokens",
              "details": []
            },
            {
              "value": 21756,
              "description": "raw dot product score (quantized): 21756",
              "details": [
                {
                  "value": 9494,
                  "description": "token '13723' contribution: query_weight=47 * doc_weight=202",
                  "details": []
                },
                {
                  "value": 7098,
                  "description": "token '9266' contribution: query_weight=39 * doc_weight=182",
                  "details": []
                },
                {
                  "value": 1540,
                  "description": "token '2078' contribution: query_weight=22 * doc_weight=70",
                  "details": []
                },
                {
                  "value": 364,
                  "description": "token '2365' contribution: query_weight=26 * doc_weight=14",
                  "details": []
                }
              ]
            },
            {
              "value": 0.0007381776,
              "description": "quantization rescaling: 1.0000 * 3.00 * 16.00 / 255 / 255 = 0.000738",
              "details": [
                {
                  "value": 1,
                  "description": "original boost: 1.0000",
                  "details": []
                },
                {
                  "value": 3,
                  "description": "ceiling_ingest (quantization parameter): 3.00",
                  "details": []
                },
                {
                  "value": 16,
                  "description": "ceiling_search (quantization parameter): 16.00",
                  "details": []
                },
                {
                  "value": 255,
                  "description": "MAX_UNSIGNED_BYTE_VALUE: 255",
                  "details": []
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```
</details>

## 範例：含篩選器的 neural sparse ANN 搜尋

```json
GET hotels-index/_search?explain=true
{
  "query": {
    "neural_sparse": {
      "name_embedding": {
        "query_tokens": {
          "7001": 6.25,
          "3509": 5.57
        },
        "method_parameters": {
          "k": 5,
          "filter": {
            "range": {
              "rating": {
                "gte": 8,
                "lte": 10
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 70.55404,
    "hits": [
      {
        "_shard": "[hotels-index][0]",
        "_node": "iId6ipt-SCWA-7vHLh981Q",
        "_index": "hotels-index",
        "_id": "8",
        "_score": 70.55404,
        "_source": {
          "parking": true,
          "name": "Crystal Beach Resort",
          "rating": 9,
          "name_embedding": {
            "3509": 5.5722017,
            "6121": 6.5081306,
            "7001": 6.25483
          }
        },
        "_explanation": {
          "value": 70.55404,
          "description": "sparse_ann score for doc 7 in field 'name_embedding'",
          "details": [
            {
              "value": 2,
              "description": "query token pruning: kept all 2 tokens (no pruning occurred)",
              "details": []
            },
            {
              "value": 17921,
              "description": "raw dot product score (quantized): 17921",
              "details": [
                {
                  "value": 10000,
                  "description": "token '7001' contribution: query_weight=100 * doc_weight=100",
                  "details": []
                },
                {
                  "value": 7921,
                  "description": "token '3509' contribution: query_weight=89 * doc_weight=89",
                  "details": []
                }
              ]
            },
            {
              "value": 0.003936948,
              "description": "quantization rescaling: 1.0000 * 16.00 * 16.00 / 255 / 255 = 0.003937",
              "details": [
                {
                  "value": 1,
                  "description": "original boost: 1.0000",
                  "details": []
                },
                {
                  "value": 16,
                  "description": "ceiling_ingest (quantization parameter): 16.00",
                  "details": []
                },
                {
                  "value": 16,
                  "description": "ceiling_search (quantization parameter): 16.00",
                  "details": []
                },
                {
                  "value": 255,
                  "description": "MAX_UNSIGNED_BYTE_VALUE: 255",
                  "details": []
                }
              ]
            },
            {
              "value": 1,
              "description": "document passed filter with exact search mode (filter matched 4 documents <= k=5, all filtered documents scored exactly)",
              "details": [
                {
                  "value": 1,
                  "description": "filter criteria: +ApproximateScoreQuery(originalQuery=IndexOrDocValuesQuery(indexQuery=rating:[8 TO 10], dvQuery=rating:[8 TO 10]), approximationQuery=Approximate(rating:[8 TO 10]))",
                  "details": []
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```
</details>

## 回應本文欄位

下表說明解釋回應中的欄位。

欄位 | 說明
:--- | :---
`explanation` | `explanation` 物件包含下列欄位：<br> - `value`：包含計算結果。<br> - `description`：說明執行了何種計算。<br> - `details`：顯示執行的任何子計算。

### 解釋元件

解釋中的 `details` 陣列會根據 neural sparse ANN 評分流程包含下列元件。

元件 | 說明
:--- | :---
查詢詞元剪除 | 顯示根據 `top_n` 參數剪除後保留的查詢詞元數量。若未進行剪除，表示所有詞元皆保留。
原始內積分數 | 重新縮放前的量化內積分數。包含巢狀詳細資料，顯示每個詞元的貢獻為 `query_weight * doc_weight`。
量化重新縮放 | （僅限 Lucene 引擎）說明如何使用下列公式將原始量化分數轉換為最終浮點分數：`boost * ceiling_ingest * ceiling_search / 255 / 255`。包含計算中使用之每個參數的詳細資料。
篩選解釋 | （套用篩選時）顯示篩選條件與搜尋模式。指出當篩選後的文件數小於或等於 `k` 時，是否使用精確搜尋模式。

### 量化參數

Neural sparse ANN 搜尋使用無正負號位元組量化來減少記憶體用量並改善搜尋效能。Lucene 引擎的量化重新縮放區段包含下列參數。原生引擎會套用相同的量化，但會回報精確的內積分數，因此其解釋中不會出現此區段。

參數 | 說明
:--- | :---
`original boost` | 套用至查詢的提升值。預設為 1.0。
`ceiling_ingest` | 文件匯入期間使用的量化上限參數。
`ceiling_search` | 搜尋期間使用的量化上限參數。
`MAX_UNSIGNED_BYTE_VALUE` | 無正負號位元組量化的最大值 (255)。

匯入期間，浮點詞元權重會除以 `ceiling_ingest` 並縮放至位元組範圍，藉此轉換為無正負號位元組 (0--255)。同樣地，搜尋期間會使用 `ceiling_search` 將查詢詞元權重量化。原始內積會使用這些量化後的位元組值計算。為了還原近似的原始分數，會使用公式 `final_score = raw_quantized_score * boost * ceiling_ingest * ceiling_search / 255 / 255` 重新縮放結果。上限參數決定可表示而不裁切的最大權重值——超過上限的權重會以 255 為上限。

## 後續步驟

- 如需 neural sparse ANN 搜尋的詳細資訊，請參閱 [Neural sparse ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。
- 如需 Explain API 的詳細資訊，請參閱 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/)。
- 如需 neural sparse ANN 搜尋中篩選的相關資訊，請參閱 [Neural sparse ANN 搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)。
