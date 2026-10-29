---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合搜尋說明"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 70
---

# 混合搜尋說明
**2.19 版新增**
{: .label .label-purple }

您可以提供 `explain` 參數，以了解混合查詢中分數的計算、正規化與合併方式。啟用後，它會提供每個搜尋結果評分程序的詳細資訊，包括所使用的分數正規化技術、不同分數的合併方式，以及各個子查詢分數的計算過程。這些完整的深入資訊能讓您更輕鬆地了解並最佳化混合查詢結果。如需 `explain` 的更多資訊，請參閱 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/)。

`explain` 無論在資源或時間上都是昂貴的操作。對於正式環境叢集，我們建議僅在疑難排解時少量使用。
{: .warning }

您可以在執行完整混合查詢時，使用下列語法在 URL 中提供 `explain` 參數：

```json
GET {index}/_search?search_pipeline={search_pipeline}&explain=true
POST {index}/_search?search_pipeline={search_pipeline}&explain=true
```

若要使用 `explain` 參數，您必須在搜尋管線中設定 `hybrid_score_explanation` 回應處理器。如需更多資訊，請參閱[混合分數說明處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/explanation-processor/)。

### 依文件 ID 說明

您可以將 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/) 與混合查詢搭配使用，以取得單一文件的評分詳細資訊：

```json
GET {index}/_explain/{id}
POST {index}/_explain/{id}
```

在此情況下，結果只包含原始的 Lucene 層級評分資訊，例如 `term` 或 `match` 等以文字為基礎的子查詢的 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 分數。回應範例請參閱 [Explain API 範例回應]({{site.url}}{{site.baseurl}}/api-reference/explain/#example-response)。

Explain API 與混合查詢搭配使用時有下列限制：

- `_explain` 端點不支援在請求本文或 URL 中使用 `search_pipeline` 參數，並會拒絕包含此參數的請求。此限制適用於所有查詢類型，不僅限於混合查詢。
- 分數正規化技術（例如 `min_max`、`l2` 或 `z_score`）與組合技術（例如 `arithmetic_mean`）需要所有相符文件的分數才能計算統計資料。由於 Explain API 只針對單一文件運作，因此無法提供正規化脈絡。`hybrid_score_explanation` 回應處理器不會被叫用，也不會傳回任何正規化後的評分詳細資訊。

若要取得特定文件的完整混合查詢說明（包含正規化與組合詳細資訊），請使用 Search API 搭配 `explain=true`，並在查詢中篩選所需的文件 ID：

```json
GET {index}/_search?search_pipeline={search_pipeline}&explain=true
{
  "query": {
    "hybrid": {
      "filter": {
        "term": {
          "_id": "<doc-id>"
        }
      },
      "queries": [...]
    }
  }
}
```
{% include copy-curl.html %}

若要查看所有結果的 `explain` 輸出，請在 URL 或請求本文中將該參數設為 `true`。下列範例使用[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/tutorials/vector-search/neural-search-tutorial/)中的索引與模型，以及名為 `my_pipeline` 的搜尋管線，其中包含 `normalization-processor` 與 `hybrid_score_explanation` 處理器：

```json
POST my-nlp-index/_search?search_pipeline=my_pipeline&explain=true
{
  "_source": {
    "exclude": [
      "passage_embedding"
    ]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "text": {
              "query": "horse"
            }
          }
        },
        {
          "neural": {
            "passage_embedding": {
              "query_text": "wild west",
              "model_id": "aVeif4oB5Vm0Tdw8zYO2",
              "k": 5
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含評分資訊：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
    "took": 54,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 5,
            "relation": "eq"
        },
        "max_score": 0.92510754,
        "hits": [
            {
                "_shard": "[my-nlp-index][0]",
                "_node": "IsuzeVYdSqKUfy0qfqil2w",
                "_index": "my-nlp-index",
                "_id": "5",
                "_score": 0.92510754,
                "_source": {
                    "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
                    "id": "2691147709.jpg"
                },
                "_explanation": {
                    "value": 0.92510754,
                    "description": "arithmetic_mean combination of:",
                    "details": [
                        {
                            "value": 1.0,
                            "description": "min_max normalization of:",
                            "details": [
                                {
                                    "value": 0.40775257,
                                    "description": "weight(text:horse in 0) [PerFieldSimilarity], result of:",
                                    "details": [
                                        {
                                            "value": 0.40775257,
                                            "description": "score(freq=1.0), computed as boost * idf * tf from:",
                                            "details": [
                                                {
                                                    "value": 0.87546873,
                                                    "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
                                                    "details": [
                                                        {
                                                            "value": 2,
                                                            "description": "n, number of documents containing term",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 5,
                                                            "description": "N, total number of documents with field",
                                                            "details": []
                                                        }
                                                    ]
                                                },
                                                {
                                                    "value": 0.46575344,
                                                    "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                                                    "details": [
                                                        {
                                                            "value": 1.0,
                                                            "description": "freq, occurrences of term within document",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 1.2,
                                                            "description": "k1, term saturation parameter",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 0.75,
                                                            "description": "b, length normalization parameter",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 16.0,
                                                            "description": "dl, length of field",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 17.0,
                                                            "description": "avgdl, average length of field",
                                                            "details": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "value": 0.85036486,
                            "description": "min_max normalization of:",
                            "details": [
                                {
                                    "value": 0.015177963,
                                    "description": "the type of knn search executed was Approximate-NN",
                                    "details": [
                                        {
                                            "value": 0.015177963,
                                            "description": "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = l2 where score is computed as `1 / (1 + rawScore)` from:",
                                            "details": [
                                                {
                                                    "value": 64.884995,
                                                    "description": "rawScore, returned from FAISS library",
                                                    "details": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
...
```
</details>

## 回應本文欄位

欄位 | 說明
:--- | :---
`explanation` | `explanation` 物件有三個屬性：`value`、`description` 與 `details`。`value` 屬性顯示計算結果，`description` 說明所執行的計算類型，`details` 則顯示任何已執行的子計算。對於分數正規化，`description` 屬性中的資訊包含用於正規化或合併的技術，以及對應的分數。

## 後續步驟

- 若要了解如何將 `explain` 與 inner hits 搭配使用，請參閱[在混合查詢中使用 inner hits]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/inner-hits/)。
