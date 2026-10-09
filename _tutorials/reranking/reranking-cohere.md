---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Cohere Rerank 重新排序"
parent: Reranking search results
nav_order: 90
redirect_from:
  - /ml-commons-plugin/tutorials/reranking-cohere/
  - /vector-search/tutorials/reranking/reranking-cohere/
---

# 使用 Cohere Rerank 重新排序搜尋結果

[重新排序管線]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)可以重新排序搜尋結果，為搜尋結果中的每份文件提供相對於搜尋查詢的相關性分數。相關性分數由交叉編碼器模型計算。

本教學說明如何在重新排序管線中使用 [Cohere Rerank](https://docs.cohere.com/reference/rerank-1) 模型。

請將開頭為前置字元 `your_` 的預留位置替換為您自己的值。
{: .note}

## 步驟 1：註冊 Cohere Rerank 模型

為 Cohere Rerank 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "cohere-rerank",
    "description": "The connector to Cohere reanker model",
    "version": "1",
    "protocol": "http",
    "credential": {
        "cohere_key": "your_cohere_api_key"
    },
    "parameters": {
        "model": "rerank-english-v2.0"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://api.cohere.ai/v1/rerank",
            "headers": {
                "Authorization": "Bearer ${credential.cohere_key}"
            },
            "request_body": "{ \"documents\": ${parameters.documents}, \"query\": \"${parameters.query}\", \"model\": \"${parameters.model}\", \"top_n\": ${parameters.top_n} }",
            "pre_process_function": "connector.pre_process.cohere.rerank",
            "post_process_function": "connector.post_process.cohere.rerank"
        }
    ]
}
```
{% include copy-curl.html %}

使用回應中的連接器 ID 註冊 Cohere Rerank 模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "cohere rerank model",
    "function_name": "remote",
    "description": "test rerank model",
    "connector_id": "your_connector_id"
}
```
{% include copy-curl.html %}

請記下回應中的模型 ID；您將在後續步驟中使用它。

呼叫 Predict API 來測試模型：

```json
POST _plugins/_ml/models/your_model_id/_predict
{
  "parameters": {
    "query": "What is the capital of the United States?",
    "documents": [
      "Carson City is the capital city of the American state of Nevada.",
      "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
      "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
      "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
    ],
    "top_n": 4
  }
}
```

為確保與重新排序管線相容，`top_n` 值必須與 `documents` 清單的長度相同。
{: .important}

您可以提供 `size` 參數，自訂回應中傳回的頂端文件數量。如需詳細資訊，請參閱[步驟 2.3](#step-23-test-the-reranking)。

OpenSearch 會回應推論結果：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.10194652
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.0721122
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.98005307
          ]
        },
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            0.27904198
          ]
        }
      ],
      "status_code": 200
    }
  ]
}
```

回應包含四個 `similarity` 物件。對於每個 `similarity` 物件，`data` 陣列包含每份文件相對於查詢的相關性分數。`similarity` 物件會依輸入文件的順序提供；第一個物件對應第一份文件。這與 Cohere Rerank 模型的預設輸出不同，後者會依相關性分數排序文件。文件順序會在 `connector.post_process.cohere.rerank` 後處理函式中變更，以使輸出與重新排序管線相容。

## 步驟 2：設定重新排序管線

請依照下列步驟設定重新排序管線。

### 步驟 2.1：匯入測試資料

傳送大量請求以匯入測試資料：

```json
POST _bulk
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Carson City is the capital city of the American state of Nevada." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district." }
{ "index": { "_index": "my-test-data" } }
{ "passage_text" : "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states." }
```
{% include copy-curl.html %}

### 步驟 2.2：建立重新排序管線

使用 Cohere Rerank 模型建立重新排序管線：

```json
PUT /_search/pipeline/rerank_pipeline_cohere
{
    "description": "Pipeline for reranking with Cohere Rerank model",
    "response_processors": [
        {
            "rerank": {
                "ml_opensearch": {
                    "model_id": "your_model_id_created_in_step1"
                },
                "context": {
                    "document_fields": ["passage_text"]
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

### 步驟 2.3：測試重新排序

若要限制傳回的結果數量，您可以指定 `size` 參數。例如，將 `"size": 2` 設為傳回前兩份文件：

```json
GET my-test-data/_search?search_pipeline=rerank_pipeline_cohere
{
  "query": {
    "match_all": {}
  },
  "size": 4,
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "What is the capital of the United States?"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩份最相關的文件：

```json
{
  "took": 0,
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
    "max_score": 0.98005307,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "zbUOw40B8vrNLhb9vBif",
        "_score": 0.98005307,
        "_source": {
          "passage_text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "zrUOw40B8vrNLhb9vBif",
        "_score": 0.27904198,
        "_source": {
          "passage_text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "y7UOw40B8vrNLhb9vBif",
        "_score": 0.10194652,
        "_source": {
          "passage_text": "Carson City is the capital city of the American state of Nevada."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "zLUOw40B8vrNLhb9vBif",
        "_score": 0.0721122,
        "_source": {
          "passage_text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

若要將這些結果與未重新排序的結果進行比較，請在沒有重新排序管線的情況下執行搜尋：

```json
GET my-test-data/_search
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "rerank": {
      "query_context": {
         "query_text": "What is the capital of the United States?"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中的第一份文件對應 Carson City，而 Carson City 並非美國首都：

```json
{
  "took": 0,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my-test-data",
        "_id": "y7UOw40B8vrNLhb9vBif",
        "_score": 1,
        "_source": {
          "passage_text": "Carson City is the capital city of the American state of Nevada."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "zLUOw40B8vrNLhb9vBif",
        "_score": 1,
        "_source": {
          "passage_text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "zbUOw40B8vrNLhb9vBif",
        "_score": 1,
        "_source": {
          "passage_text": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district."
        }
      },
      {
        "_index": "my-test-data",
        "_id": "zrUOw40B8vrNLhb9vBif",
        "_score": 1,
        "_source": {
          "passage_text": "Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states."
        }
      }
    ]
  }
}
```