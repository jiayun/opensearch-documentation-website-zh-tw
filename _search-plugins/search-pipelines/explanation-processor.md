---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合分數說明"
nav_order: 15
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 混合分數說明處理器
2.19 版推出
{: .label .label-purple }

`hybrid_score_explanation` 回應處理器會將正規化與合併結果加入傳回的搜尋回應中。您可以使用它作為偵錯工具，以了解分數正規化的過程。如需更多資訊，請參閱[混合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/)。

若要使用 `explain` 參數，您必須在搜尋管線中設定 `hybrid_score_explanation` 回應處理器。
{: .important}

## 請求本文欄位

下表列出所有請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)並繼續執行搜尋管線中剩餘的處理器。選用。預設為 `false`。

## 範例

下列範例示範使用含有 `hybrid_score_explanation` 處理器的搜尋管線。

如需完整的範例，請依照[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/ml-commons-plugin/semantic-search#tutorial)。

### 建立搜尋管線 

下列請求會建立含有 `normalization-processor` 與 `hybrid_score_explanation` 處理器的搜尋管線：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean"
        }
      }
    }
  ],
  "response_processors": [
    {
        "hybrid_score_explanation": {}
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

若要查看說明資訊，請在搜尋請求中指定 `explain=true`：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline&explain=true
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

#### 範例回應

```json
{
    "took": 54,
    "timed_out": false,
    "_shards": {
        "total": 2,
        "successful": 2,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 5,
            "relation": "eq"
        },
        "max_score": 0.9251075,
        "hits": [
            {
                "_shard": "[my-nlp-index][0]",
                "_node": "IsuzeVYdSqKUfy0qfqil2w",
                "_index": "my-nlp-index",
                "_id": "5",
                "_score": 0.9251075,
                "_source": {
                    "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
                    "id": "2691147709.jpg"
                },
                "_explanation": {
                    "value": 0.9251075,
                    "description": "arithmetic_mean combination of:",
                    "details": [
                        {
                            "value": 1.0,
                            "description": "min_max normalization of:",
                            "details": [
                                {
                                    "value": 1.2336599,
                                    "description": "weight(text:horse in 0) [PerFieldSimilarity], result of:",
                                    "details": [
                                        {
                                            "value": 1.2336599,
                                            "description": "score(freq=1.0), computed as boost * idf * tf from:",
                                            "details": [
                                                {
                                                    "value": 2.2,
                                                    "description": "boost",
                                                    "details": []
                                                },
                                                {
                                                    "value": 1.2039728,
                                                    "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
                                                    "details": [
                                                        {
                                                            "value": 1,
                                                            "description": "n, number of documents containing term",
                                                            "details": []
                                                        },
                                                        {
                                                            "value": 4,
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
                            "value": 0.8503647,
                            "description": "min_max normalization of:",
                            "details": [
                                {
                                    "value": 0.015177966,
                                    "description": "within top 5",
                                    "details": []
                                }
                            ]
                        }
                    ]
...
```

如需設定混合搜尋的更多資訊，請參閱[混合搜尋]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/)。