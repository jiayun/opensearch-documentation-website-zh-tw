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

布林（`bool`）查詢可以將多個查詢子句合併為一個進階查詢。這些子句以布林邏輯合併，用來找出結果中傳回的相符文件。

您可以在 `bool` 查詢中使用下列查詢子句：

子句 | 行為
:--- | :---
`must` | 邏輯 `and` 運算子。結果必須符合此子句中的所有查詢。
`must_not` | 邏輯 `not` 運算子。所有相符項目都會從結果中排除。如果 `must_not` 包含多個子句，則只會傳回不符合任何這些子句的文件。例如，`"must_not":[{clause_A}, {clause_B}]` 等同於 `NOT(A OR B)`。
`should` | 邏輯 `or` 運算子。符合越多 `should` 子句，文件的相關性分數就越高。您可以使用 [`minimum_should_match`]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/) 參數設定必須符合的最低查詢數量。如果查詢包含 `must` 或 `filter` 子句，`minimum_should_match` 的預設值為 0，因此文件不需要符合任何 `should` 子句。否則，`minimum_should_match` 的預設值為 1，因此結果必須至少符合其中一個查詢。
`filter` | 不影響相關性分數的邏輯 `and` 運算子。篩選子句中的查詢是「是或否」的選項。如果文件符合該查詢，就會傳回在結果中；否則不會傳回。篩選查詢的結果通常會被快取，以加快傳回速度。請使用篩選查詢，根據完全符合、範圍、日期或數字來篩選結果。

`must` 與 `should` 子句在[查詢情境]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)中執行，因此所有相符的 `must` 與 `should` 子句的分數會加總，產生文件的相關性分數。因此，符合越多子句的文件排名越高。`filter` 與 `must_not` 子句在篩選情境中執行：它們判斷文件是否符合，但不會影響其分數，而且 OpenSearch 可以快取其結果。

布林查詢具有以下結構：

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

## 參數

`bool` 查詢接受下列參數。所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`must` | 物件或物件陣列 | 文件必須符合的查詢。相符的查詢會計入相關性分數。
`should` | 物件或物件陣列 | 文件應該符合的查詢。每個相符的查詢都會增加相關性分數。文件是否必須符合這些查詢中的任何一個，取決於 `minimum_should_match`。
`filter` | 物件或物件陣列 | 文件必須符合的查詢。這些查詢在篩選情境中執行，不會計入相關性分數。
`must_not` | 物件或物件陣列 | 文件不得符合的查詢。這些查詢在篩選情境中執行，不會計入相關性分數。
`minimum_should_match` | 整數或字串 | 文件必須符合的 `should` 子句數量或百分比。如果查詢包含 `must` 或 `filter` 子句，預設為 `0`，否則為 `1`。有效值請參閱[最低應符合數量]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`boost` | 浮點數 | 套用至整個 `bool` 查詢相關性分數的乘數。介於 0 與 1 之間的值會降低相關性，大於 1 的值會提高相關性。由於 `filter` 與 `must_not` 子句不會計入分數，`boost` 對僅包含這些子句的查詢沒有作用。預設為 `1.0`。

## 範例

例如，假設您已將莎士比亞全集編製索引到 OpenSearch 叢集中。您想建立一個符合下列需求的單一查詢：

1. `text_entry` 欄位必須包含 `love` 一詞，並且應該包含 `life` 或 `grace`。
2. `speaker` 欄位不得包含 `ROMEO`。
3. 將這些結果篩選到劇作 `Romeo and Juliet`，且不影響相關性分數。

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
{% include copy-curl.html %}

回應包含相符的文件：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 5.1232996,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "88020",
        "_score": 5.1232996,
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

如果您想找出究竟是哪些子句造成了相符結果，可以使用 `_name` 參數為每個查詢命名。如需更多資訊，請參閱[具名查詢]({{site.url}}{{site.baseurl}}/query-dsl/named-queries/)。
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
{% include copy-curl.html %}

OpenSearch 會傳回一個 `matched_queries` 陣列，列出符合這些結果的查詢：

```json
"matched_queries": [
  "love-must",
  "life-should"
]
```

如果您移除不在此清單中的查詢，仍會看到完全相同的結果。
透過檢視哪個 `should` 子句相符，您可以更了解結果的相關性分數。

您也可以透過巢狀 `bool` 查詢來建立複雜的布林運算式。
例如，使用下列查詢，在劇作 `Romeo and Juliet` 中找出符合 (`love` OR `hate`) AND (`life` OR `grace`) 的 `text_entry` 欄位：

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
                  "text_entry": "hate"
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
                  "text_entry": "grace"
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
{% include copy-curl.html %}

回應包含三行相符的內容：

```json
{
  "took": 6,
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
    "max_score": 5.557603,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "86436",
        "_score": 5.557603,
        "_source": {
          "type": "line",
          "line_id": 86437,
          "play_name": "Romeo and Juliet",
          "speech_number": 16,
          "line_number": "2.3.88",
          "speaker": "ROMEO",
          "text_entry": "Doth grace for grace and love for love allow;"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "88020",
        "_score": 5.1232996,
        "_source": {
          "type": "line",
          "line_id": 88021,
          "play_name": "Romeo and Juliet",
          "speech_number": 19,
          "line_number": "4.5.61",
          "speaker": "PARIS",
          "text_entry": "O love! O life! not life, but love in death!"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "86214",
        "_score": 5.0415897,
        "_source": {
          "type": "line",
          "line_id": 86215,
          "play_name": "Romeo and Juliet",
          "speech_number": 17,
          "line_number": "2.2.81",
          "speaker": "ROMEO",
          "text_entry": "My life were better ended by their hate,"
        }
      }
    ]
  }
}
```

## 使用 filter 子句計分

`filter` 子句中的查詢會決定哪些文件相符，但不會增加相關性分數。分數只取決於查詢中的計分子句（`must` 和 `should`）。下列範例使用 `support_tickets` 索引。建立索引並將 `status` 欄位對應為 `keyword` 欄位，讓 `term` 查詢能與其完全相符：

```json
PUT support_tickets
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "status": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引：

```json
POST support_tickets/_bulk?refresh
{ "index": { "_id": "1" } }
{ "title": "Login page times out", "status": "open" }
{ "index": { "_id": "2" } }
{ "title": "Password reset email not received", "status": "open" }
{ "index": { "_id": "3" } }
{ "title": "Dashboard loads slowly", "status": "closed" }
```
{% include copy-curl.html %}

下列三個查詢都會傳回這兩張開啟的票證。它們的差異只在於所指定的分數。

下列查詢只包含 `filter` 子句。因為沒有計分子句，每個相符的文件都會獲得 `0` 的分數：

```json
GET support_tickets/_search
{
  "query": {
    "bool": {
      "filter": {
        "term": {
          "status": "open"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

下列查詢在 `must` 子句中新增了 `match_all` 查詢。`match_all` 查詢會為每個文件指定 `1` 的分數，因此兩張開啟的票證都會獲得 `1` 的分數：

```json
GET support_tickets/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "term": {
          "status": "open"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

下列 [`constant_score`]({{site.url}}{{site.baseurl}}/query-dsl/compound/constant-score/) 查詢傳回的結果與前一個查詢相同。它會為每個符合其篩選條件的文件指定 `1` 的分數：

```json
GET support_tickets/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "status": "open"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

當 `must` 子句包含全文查詢時，篩選條件仍然不會改變分數。例如，在 `title` 欄位中對 `login` 進行 `match` 查詢，會為票證 1 指定 `0.44583148` 的分數，無論查詢是否也包含 `status` 篩選條件。
