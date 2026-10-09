---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新排序代理式搜尋結果"
parent: Agentic search
grand_parent: AI search
nav_order: 105
has_children: false
---

# 重新排序代理式搜尋結果

代理式搜尋請求由 [`agentic_query_translator` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) 處理，該處理器會攔截指定的查詢文字，並將其傳遞給已設定的代理程式，以產生並執行 OpenSearch DSL 查詢。若要進一步調整相關性分數，也可以使用 [`rerank` 搜尋回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/) 來重新排序搜尋結果。

## 必要條件

在使用代理式搜尋之前，您必須使用 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/) 設定代理程式。

## 步驟 1：建立用於匯入的索引

建立用於匯入的索引：

```json
PUT /iris-index
{
  "mappings": {
    "properties": {
      "petal_length_in_cm": {
        "type": "float"
      },
      "petal_width_in_cm": {
        "type": "float"
      },
      "sepal_length_in_cm": {
        "type": "float"
      },
      "sepal_width_in_cm": {
        "type": "float"
      },
      "species": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 2：將文件匯入索引

若要將文件匯入上一個步驟建立的索引，請傳送下列請求：

```json
POST _bulk
{ "index": { "_index": "iris-index", "_id": "1" } }
{ "petal_length_in_cm": 1.4, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 5.1, "sepal_width_in_cm": 3.5, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "2" } }
{ "petal_length_in_cm": 1.4, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 4.9, "sepal_width_in_cm": 3.0, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "3" } }
{ "petal_length_in_cm": 1.3, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 4.7, "sepal_width_in_cm": 3.2, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "4" } }
{ "petal_length_in_cm": 1.5, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 4.6, "sepal_width_in_cm": 3.1, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "5" } }
{ "petal_length_in_cm": 1.4, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 5.0, "sepal_width_in_cm": 3.6, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "6" } }
{ "petal_length_in_cm": 6.6, "petal_width_in_cm": 2.1, "sepal_length_in_cm": 7.6, "sepal_width_in_cm": 3.0, "species": "virginica" }
{ "index": { "_index": "iris-index", "_id": "7" } }
{ "petal_length_in_cm": 4.5, "petal_width_in_cm": 1.7, "sepal_length_in_cm": 4.9, "sepal_width_in_cm": 2.5, "species": "virginica" }
{ "index": { "_index": "iris-index", "_id": "8" } }
{ "petal_length_in_cm": 6.3, "petal_width_in_cm": 1.8, "sepal_length_in_cm": 7.3, "sepal_width_in_cm": 2.9, "species": "virginica" }
{ "index": { "_index": "iris-index", "_id": "9" } }
{ "petal_length_in_cm": 5.8, "petal_width_in_cm": 1.8, "sepal_length_in_cm": 6.7, "sepal_width_in_cm": 2.5, "species": "virginica" }
{ "index": { "_index": "iris-index", "_id": "10" } }
{ "petal_length_in_cm": 6.1, "petal_width_in_cm": 2.5, "sepal_length_in_cm": 7.2, "sepal_width_in_cm": 3.6, "species": "virginica" }
```
{% include copy-curl.html %}

## 步驟 3：註冊模型與代理程式

依照下列步驟註冊模型與代理程式：

1. [為代理程式與 QueryPlanningTool 建立模型]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/#step-3-create-a-model-for-the-agent-and-queryplanningtool)。
2. [建立代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/#step-4-create-an-agent)。

## 步驟 4：建立搜尋管線

建立使用您的代理程式與 `rerank` 回應處理器的搜尋管線。此範例使用 `by_field` 重新排序處理器，根據 `petal_length_in_cm` 欄位重新排序文件。

### 步驟 4(a)：設定 by_field 重新排序處理器

建立包含 `by_field` 重新排序處理器的代理式搜尋管線：

```json
PUT _search/pipeline/agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-from-step-3"
      }
    }
  ],
  "response_processors": [
    {
      "rerank": {
        "by_field": {
          "target_field": "petal_length_in_cm",
          "keep_previous_score": true
        }
      }
    },
    {
      "agentic_context": {
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

或者，您也可以使用 `ml_opensearch` 重新排序處理器，套用 OpenSearch 提供的 [cross-encoder 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#cross-encoder-models) 來重新排序結果。

### 步驟 4(b)：設定 ml_opensearch 重新排序處理器

註冊 `ms-marco-MiniLM-L-6-v2` cross-encoder 模型：

```json
POST _plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2",
  "version": "1.0.2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

接著提供回應中傳回的模型 ID，設定 `ml_opensearch` 重新排序處理器。您可以為索引中的任何文字欄位設定重新排序處理器。在此範例中，您將使用 `species` 欄位：

```json
POST _search/pipeline/agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-from-step-3"
      }
    }
  ],
  "response_processors": [
    {
      "rerank": {
        "ml_opensearch": {
          "model_id": "your-cross-encoder-model-id",
          "keep_previous_score": true
        },
        "context": {
          "document_fields": [
            "species"
          ]
        }
      }
    },
    {
      "agentic_context": {
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 5：測試問題

透過提出問題來測試您的重新排序代理式搜尋管線。

### 步驟 5(a)：測試 by_field 重新排序處理器

若要測試 `by_field` 重新排序處理器，請傳送下列請求：

```json
POST /iris-index/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me virginica flowers"
    }
  }
}
```
{% include copy-curl.html %}

產生的 DSL 查詢顯示代理程式選擇在 `iris-index` 的 `species` 欄位上使用基本的 `term` 查詢。該查詢會傳回所有符合指定詞彙的文件。在回應中，每份文件包含兩個分數：`previous_score`（原始相關性分數）與 `_score`（重新排序後的更新分數）。文件依花瓣長度以遞減順序排列：

```json
{
  "took": 3402,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 6.6,
    "hits": [
      {
        "_index": "iris-index",
        "_id": "6",
        "_score": 6.6,
        "_source": {
          "sepal_width_in_cm": 3.0,
          "species": "virginica",
          "previous_score": 1.0,
          "sepal_length_in_cm": 7.6,
          "petal_width_in_cm": 2.1,
          "petal_length_in_cm": 6.6
        }
      },
      {
        "_index": "iris-index",
        "_id": "8",
        "_score": 6.3,
        "_source": {
          "sepal_width_in_cm": 2.9,
          "species": "virginica",
          "previous_score": 1.0,
          "sepal_length_in_cm": 7.3,
          "petal_width_in_cm": 1.8,
          "petal_length_in_cm": 6.3
        }
      },
      {
        "_index": "iris-index",
        "_id": "10",
        "_score": 6.1,
        "_source": {
          "sepal_width_in_cm": 3.6,
          "species": "virginica",
          "previous_score": 1.0,
          "sepal_length_in_cm": 7.2,
          "petal_width_in_cm": 2.5,
          "petal_length_in_cm": 6.1
        }
      },
      {
        "_index": "iris-index",
        "_id": "9",
        "_score": 5.8,
        "_source": {
          "sepal_width_in_cm": 2.5,
          "species": "virginica",
          "previous_score": 1.0,
          "sepal_length_in_cm": 6.7,
          "petal_width_in_cm": 1.8,
          "petal_length_in_cm": 5.8
        }
      },
      {
        "_index": "iris-index",
        "_id": "7",
        "_score": 4.5,
        "_source": {
          "sepal_width_in_cm": 2.5,
          "species": "virginica",
          "previous_score": 1.0,
          "sepal_length_in_cm": 4.9,
          "petal_width_in_cm": 1.7,
          "petal_length_in_cm": 4.5
        }
      }
    ]
  },
  "ext": {
    "dsl_query": "{\"query\":{\"term\":{\"species.keyword\":\"virginica\"}}}"
  }
}
```

### 步驟 5(b)：測試 ml_opensearch 重新排序處理器

若要測試 `ml_opensearch` 重新排序處理器，請傳送下列請求：

```json
POST /iris-index/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me virginica flowers"
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
        "query_text": "Show me virginica flowers"
      }
    }
  }
}
```
{% include copy-curl.html %}

模型會同時接收查詢文字與文件文字，並根據兩者產生新的相關性分數：

```json
{
  "took": 2667,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 0.65176475,
    "hits": [
      {
        "_index": "iris-index",
        "_id": "9",
        "_score": 0.65176475,
        "_source": {
          "petal_length_in_cm": 5.8,
          "petal_width_in_cm": 1.8,
          "sepal_length_in_cm": 6.7,
          "sepal_width_in_cm": 2.5,
          "species": "virginica"
        }
      },
      {
        "_index": "iris-index",
        "_id": "7",
        "_score": 0.65176475,
        "_source": {
          "petal_length_in_cm": 4.5,
          "petal_width_in_cm": 1.7,
          "sepal_length_in_cm": 4.9,
          "sepal_width_in_cm": 2.5,
          "species": "virginica"
        }
      },
      {
        "_index": "iris-index",
        "_id": "8",
        "_score": 0.65176475,
        "_source": {
          "petal_length_in_cm": 6.3,
          "petal_width_in_cm": 1.8,
          "sepal_length_in_cm": 7.3,
          "sepal_width_in_cm": 2.9,
          "species": "virginica"
        }
      },
      {
        "_index": "iris-index",
        "_id": "10",
        "_score": 0.65176475,
        "_source": {
          "petal_length_in_cm": 6.1,
          "petal_width_in_cm": 2.5,
          "sepal_length_in_cm": 7.2,
          "sepal_width_in_cm": 3.6,
          "species": "virginica"
        }
      },
      {
        "_index": "iris-index",
        "_id": "6",
        "_score": 0.65176475,
        "_source": {
          "petal_length_in_cm": 6.6,
          "petal_width_in_cm": 2.1,
          "sepal_length_in_cm": 7.6,
          "sepal_width_in_cm": 3.0,
          "species": "virginica"
        }
      }
    ]
  },
  "ext": {
    "dsl_query": "{\"query\":{\"term\":{\"species.keyword\":\"virginica\"}}}"
  }
}
```

## 相關文件

- [重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)
- [Rerank 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)
