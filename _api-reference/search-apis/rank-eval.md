---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排名評估"
parent: Search APIs
nav_order: 60
redirect_from:
  - /api-reference/rank-eval/
---

# Ranking Evaluation API
**於 1.0 版導入**
{: .label .label-purple }

Rank Evaluation API 用於評估排名搜尋結果的品質。

## 端點

```json
GET {index_name}/_rank_eval 
POST {index_name}/_rank_eval
```

## 查詢參數

查詢參數為選用。

參數 | 資料類型 | 說明
:--- | :---  | :---
`ignore_unavailable` | 布林值 | 預設為 `false`。設為 `false` 時，若索引已關閉或不存在，回應本文會傳回錯誤。
`allow_no_indices` | 布林值 | 預設為 `true`。設為 `false` 時，若萬用字元運算式指向已關閉或不存在的索引，回應本文會傳回錯誤。
`expand_wildcards` | 字串 | 針對狀態為 `open`、`closed`、`hidden`、`none` 或 `all` 的索引展開萬用字元運算式。
`search_type` | 字串 | 將搜尋類型設為 `query_then_fetch` 或 `dfs_query_then_fetch`。

## 請求本文欄位

請求本文必須包含至少一個參數。

欄位類型 | 說明
:--- | :---  
`id` | 文件或範本 ID。
`requests` | 在 request 欄位區段中設定多個搜尋請求。
`ratings` | 文件相關性分數。
k | 每個查詢傳回的文件數量。預設為 10。
`relevant_rating_threshold` | 判定文件為相關的門檻值。預設為 1。
`normalize` | 設為 `true` 時，將計算折扣累計增益。
`maximum_relevance` | 使用預期倒數排名指標時，設定相關性分數的最大值。
`ignore_unlabeled` | 預設為 `false`。設為 `true` 時，將忽略未標示的文件。
`template_id` | 範本 ID。
`params` | 範本中使用的參數。

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_rank_eval
body: |
{
  "requests": [
    {
      "id": "books_query",
      "request": {
          "query": { "match": { "text": "thou" } }
      },
      "ratings": [
        { "_index": "shakespeare", "_id": "80", "rating": 0 },
        { "_index": "shakespeare", "_id": "115", "rating": 1 },
        { "_index": "shakespeare", "_id": "117", "rating": 2 }
      ]
    },
    {
      "id": "words_query",
      "request": {
        "query": { "match": { "text": "art" } }
      },
      "ratings": [
        { "_index": "shakespeare", "_id": "115", "rating": 2 }
      ]
    }
  ]
}
-->
{% capture step1_rest %}
GET /shakespeare/_rank_eval
{
  "requests": [
    {
      "id": "books_query",
      "request": {
        "query": {
          "match": {
            "text": "thou"
          }
        }
      },
      "ratings": [
        {
          "_index": "shakespeare",
          "_id": "80",
          "rating": 0
        },
        {
          "_index": "shakespeare",
          "_id": "115",
          "rating": 1
        },
        {
          "_index": "shakespeare",
          "_id": "117",
          "rating": 2
        }
      ]
    },
    {
      "id": "words_query",
      "request": {
        "query": {
          "match": {
            "text": "art"
          }
        }
      },
      "ratings": [
        {
          "_index": "shakespeare",
          "_id": "115",
          "rating": 2
        }
      ]
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.rank_eval(
  index = "shakespeare",
  body =   {
    "requests": [
      {
        "id": "books_query",
        "request": {
          "query": {
            "match": {
              "text": "thou"
            }
          }
        },
        "ratings": [
          {
            "_index": "shakespeare",
            "_id": "80",
            "rating": 0
          },
          {
            "_index": "shakespeare",
            "_id": "115",
            "rating": 1
          },
          {
            "_index": "shakespeare",
            "_id": "117",
            "rating": 2
          }
        ]
      },
      {
        "id": "words_query",
        "request": {
          "query": {
            "match": {
              "text": "art"
            }
          }
        },
        "ratings": [
          {
            "_index": "shakespeare",
            "_id": "115",
            "rating": 2
          }
        ]
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

````json
{
  "rank_eval": {
    "metric_score": 0.7,
      "details": {
      "query_1": {                           
        "metric_score": 0.9,                      
        "unrated_docs": [                         
          {
            "_index": "shakespeare",
            "_id": "1234567"
          }, ...
        ],
        "hits": [
          {
            "hit": {                              
              "_index": "shakespeare",
              "_type": "page",
              "_id": "1234567",
              "_score": 5.123456789
            },
            "rating": 1
          }, ...
        ],
        "metric_details": {                       
          "precision": {
            "relevant_docs_retrieved": 3,
            "docs_retrieved": 6
          }
        }
      },
      "query_2": { [... ] }
    },
    "failures": { [... ] }
  }
}
````