---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "布林查詢"
parent: Compound queries
nav_order: 10
redirect_from:
  - /opensearch/query-dsl/compound/bool/
  - /opensearch/query-dsl/bool/
  - /query-dsl/query-dsl/compound/bool/
---

# 布林查詢

布林 (`bool`) 查詢可以將多個查詢子句合併為一個進階查詢。這些子句以布林邏輯組合，用於在結果中找出符合條件的文件。

您可以在 `bool` 查詢中使用下列查詢子句：

子句 | 行為
:--- | :---
`must` | 邏輯 `and` 運算子。結果必須符合此子句中的所有查詢。 
`must_not` | 邏輯 `not` 運算子。所有符合的項目都會從結果中排除。如果 `must_not` 包含多個子句，則只會傳回不符合任何這些子句的文件。例如，`"must_not":[{clause_A}, {clause_B}]` 等同於 `NOT(A OR B)`。 
`should` | 邏輯 `or` 運算子。結果必須至少符合其中一個查詢。符合越多 `should` 子句，文件的相關性分數就越高。您可以使用 [`minimum_should_match`]({{site.url}}{{site.baseurl}}/query-dsl/query-dsl/minimum-should-match/) 參數設定必須符合的查詢數量下限。如果查詢包含 `must` 或 `filter` 子句，`minimum_should_match` 的預設值為 0；否則，`minimum_should_match` 的預設值為 1。
`filter` | 邏輯 `and` 運算子，會先套用此運算子以縮小資料集，然後再套用查詢。篩選子句中的查詢是「是或否」的選項。如果文件符合該查詢，就會傳回在結果中；否則不會傳回。篩選查詢的結果通常會被快取，以加快傳回速度。請使用篩選查詢，根據完全符合的條件、範圍、日期或數字來篩選結果。

布林查詢具有下列結構：

```json
GET _search
{
  "query": {
    "bool": {
      "must": [
        {}
      ],
      "must_not": [
        {}
      ],
      "should": [
        {}
      ],
      "filter": {}
    }
  }
}
```

例如，假設您已將莎士比亞的全部作品編製索引到 OpenSearch 叢集中。您想建立一個符合下列需求的單一查詢：

1. `text_entry` 欄位必須包含 `love` 一詞，並且應包含 `life` 或 `grace`。
2. `speaker` 欄位不得包含 `ROMEO`。
3. 將這些結果篩選為劇作 `Romeo and Juliet`，且不影響相關性分數。

這些需求可以合併在下列查詢中：

```json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text_entry": "love"
          }
        }
      ],
      "should": [
        {
          "match": {
            "text_entry": "life"
          }
        },
        {
          "match": {
            "text_entry": "grace"
          }
        }
      ],
      "minimum_should_match": 1,
      "must_not": [
        {
          "match": {
            "speaker": "ROMEO"
          }
        }
      ],
      "filter": {
        "term": {
          "play_name": "Romeo and Juliet"
        }
      }
    }
  }
}
```

回應包含符合條件的文件：

```json
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 4,
    "successful": 4,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 11.356054,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "88020",
        "_score": 11.356054,
        "_source": {
          "type": "line",
          "line_id": 88021,
          "play_name": "Romeo and Juliet",
          "speech_number": 19,
          "line_number": "4.5.61",
          "speaker": "PARIS",
          "text_entry": "O love! O life! not life, but love in death!"
        }
      }
    ]
  }
}
```

如果您想確認究竟是哪些子句造成了符合的結果，可以使用 `_name` 參數為每個查詢命名。
若要加入 `_name` 參數，請將 `match` 查詢中的欄位名稱改為物件：

```json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text_entry": {
              "query": "love",
              "_name": "love-must"
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "text_entry": {
              "query": "life",
              "_name": "life-should"
            }
          }
        },
        {
          "match": {
            "text_entry": {
              "query": "grace",
              "_name": "grace-should"
            }
          }
        }
      ],
      "minimum_should_match": 1,
      "must_not": [
        {
          "match": {
            "speaker": {
              "query": "ROMEO",
              "_name": "ROMEO-must-not"
            }
          }
        }
      ],
      "filter": {
        "term": {
          "play_name": "Romeo and Juliet"
        }
      }
    }
  }
}
```

OpenSearch 會傳回一個 `matched_queries` 陣列，列出符合這些結果的查詢：

```json
"matched_queries": [
  "love-must",
  "life-should"
]
```

如果您移除不在這份清單中的查詢，仍會看到完全相同的結果。
透過檢視是哪個 `should` 子句符合，您可以更了解結果的相關性分數。

您也可以透過巢狀 `bool` 查詢來建構複雜的布林運算式。
例如，使用下列查詢，在劇作 `Romeo and Juliet` 中找出 `text_entry` 欄位符合 (`love` OR `hate`) AND (`life` OR `grace`) 的文件：

```json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {
                "match": {
                  "text_entry": "love"
                }
              },
              {
                "match": {
                  "text": "hate"
                }
              }
            ]
          }
        },
        {
          "bool": {
            "should": [
              {
                "match": {
                  "text_entry": "life"
                }
              },
              {
                "match": {
                  "text": "grace"
                }
              }
            ]
          }
        }
      ],
      "filter": {
        "term": {
          "play_name": "Romeo and Juliet"
        }
      }
    }
  }
}
```

回應包含符合條件的文件：

```json
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 1,
    "max_score": 11.37006,
    "hits": [
      {
        "_index": "shakespeare",
        "_type": "doc",
        "_id": "88020",
        "_score": 11.37006,
        "_source": {
          "type": "line",
          "line_id": 88021,
          "play_name": "Romeo and Juliet",
          "speech_number": 19,
          "line_number": "4.5.61",
          "speaker": "PARIS",
          "text_entry": "O love! O life! not life, but love in death!"
        }
      }
    ]
  }
}
```
