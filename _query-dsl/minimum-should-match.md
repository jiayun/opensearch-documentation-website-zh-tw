---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最低應符合數量"
nav_order: 80
redirect_from:
- /query-dsl/query-dsl/minimum-should-match/
---

# 最低應符合數量 

`minimum_should_match` 參數可用於全文搜尋，用來指定文件必須符合的最少詞彙數量，才能出現在搜尋結果中。 

以下範例要求文件必須符合三個搜尋詞彙中的至少兩個，才會被傳回為搜尋結果：

```json
GET /shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": {
        "query": "prince king star",
        "minimum_should_match": "2"
      }
    }
  }
}
```

在此範例中，查詢有三個以 `OR` 結合的選用子句，因此文件必須符合 `prince` 與 `king`，或 `prince` 與 `star`，或 `king` 與 `star`。

## 有效值

您可以將 `minimum_should_match` 參數指定為下列其中一種值。

值類型 | 範例 | 說明
:--- | :--- | :---
非負整數 | `2` | 文件必須符合此數量的選用子句。
負整數 | `-1` | 文件必須符合選用子句總數減去此數量。
非負百分比 | `70%` | 文件必須符合選用子句總數的此百分比。要符合的子句數量會以捨去方式取至最接近的整數。
負百分比 | `-30%` | 文件可以有選用子句總數的此百分比不符合。允許文件不符合的子句數量會以捨去方式取至最接近的整數。
組合 | `2<75%` | `n<p%` 格式的運算式。如果選用子句的數量小於或等於 `n`，文件必須符合所有選用子句。如果選用子句的數量大於 `n`，則文件必須符合 `p` 百分比的選用子句。
多重組合 | `3<-1 5<50%` | 以空格分隔的多個組合。每個條件適用於大於 `<` 符號左側數字的選用子句數量。在此範例中，如果選用子句為三個或更少，文件必須符合全部子句。如果選用子句為四個或五個，文件必須符合除了一個以外的所有子句。如果選用子句為六個或更多，文件必須符合其中 50%。

設 `n` 為文件必須符合的選用子句數量。當 `n` 以百分比計算時，如果 `n` 小於 1，則使用 1。如果 `n` 大於選用子句的數量，則使用選用子句的數量。
{: .note}


## 在布林查詢中使用此參數

[布林查詢]({{site.url}}{{site.baseurl}}/) 會在 `should` 子句中列出選用子句，並在 `must` 子句中列出必要子句。此外，它還可以包含 `filter` 子句來篩選結果。

假設有一個包含下列五份文件的索引：

```json
PUT testindex/_doc/1
{
  "text": "one OpenSearch"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "text": "one two OpenSearch"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/3
{
  "text": "one two three OpenSearch"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/4
{
  "text": "one two three four OpenSearch"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/5
{
  "text": "OpenSearch"
}
```
{% include copy-curl.html %}

下列查詢包含四個選用子句：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text": "OpenSearch"
          }
        }
      ], 
      "should": [
        {
          "match": {
            "text": "one"
          }
        },
        {
          "match": {
            "text": "two"
          }
        },
        {
          "match": {
            "text": "three"
          }
        },
        {
          "match": {
            "text": "four"
          }
        }
      ],
      "minimum_should_match": "80%"
    }
  }
}
```
{% include copy-curl.html %}

因為 `minimum_should_match` 指定為 `80%`，所以要符合的選用子句數量計算為 4 &middot; 0.8 = 3.2，然後捨去為 3。因此，結果包含至少符合三個子句的文件：

```json
{
  "took": 40,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 2.494999,
    "hits": [
      {
        "_index": "testindex",
        "_id": "4",
        "_score": 2.494999,
        "_source": {
          "text": "one two three four OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "3",
        "_score": 1.5744598,
        "_source": {
          "text": "one two three OpenSearch"
        }
      }
    ]
  }
}
```

現在將 `minimum_should_match` 指定為 `-20%`：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text": "OpenSearch"
          }
        }
      ], 
      "should": [
        {
          "match": {
            "text": "one"
          }
        },
        {
          "match": {
            "text": "two"
          }
        },
        {
          "match": {
            "text": "three"
          }
        },
        {
          "match": {
            "text": "four"
          }
        }
      ],
      "minimum_should_match": "-20%"
    }
  }
}
```
{% include copy-curl.html %}

允許文件不符合的選用子句數量計算為 4 &middot; 0.2 = 0.8，並捨去為 0。因此，結果只包含一份符合所有選用子句的文件：

```json
{
  "took": 41,
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
    "max_score": 2.494999,
    "hits": [
      {
        "_index": "testindex",
        "_id": "4",
        "_score": 2.494999,
        "_source": {
          "text": "one two three four OpenSearch"
        }
      }
    ]
  }
}
```

請注意，指定正百分比（`80%`）與負百分比（`-20%`）並未產生相同的文件必須符合之選用子句數量，因為在兩種情況下結果都被捨去。如果選用子句的數量例如是 5，則 `80%` 與 `-20%` 都會產生相同的文件必須符合之選用子句數量（4）。

### `minimum_should_match` 的預設值 

如果查詢包含 `must` 或 `filter` 子句，預設的 `minimum_should_match` 值為 0。例如，下列查詢搜尋符合 `OpenSearch` 以及 0 個選用 `should` 子句的文件：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text": "OpenSearch"
          }
        }
      ], 
      "should": [
        {
          "match": {
            "text": "one"
          }
        },
        {
          "match": {
            "text": "two"
          }
        },
        {
          "match": {
            "text": "three"
          }
        },
        {
          "match": {
            "text": "four"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

此查詢會傳回索引中的所有五份文件：

```json
{
  "took": 34,
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
    "max_score": 2.494999,
    "hits": [
      {
        "_index": "testindex",
        "_id": "4",
        "_score": 2.494999,
        "_source": {
          "text": "one two three four OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "3",
        "_score": 1.5744598,
        "_source": {
          "text": "one two three OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.91368985,
        "_source": {
          "text": "one two OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.4338556,
        "_source": {
          "text": "one OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "5",
        "_score": 0.11964063,
        "_source": {
          "text": "OpenSearch"
        }
      }
    ]
  }
}
```

不過，如果您省略 `must` 子句，則查詢會搜尋符合一個選用 `should` 子句的文件：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "text": "one"
          }
        },
        {
          "match": {
            "text": "two"
          }
        },
        {
          "match": {
            "text": "three"
          }
        },
        {
          "match": {
            "text": "four"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

結果只包含至少符合一個選用子句的四份文件：

```json
{
  "took": 19,
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
    "max_score": 2.426633,
    "hits": [
      {
        "_index": "testindex",
        "_id": "4",
        "_score": 2.426633,
        "_source": {
          "text": "one two three four OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "3",
        "_score": 1.4978898,
        "_source": {
          "text": "one two three OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.8266785,
        "_source": {
          "text": "one two OpenSearch"
        }
      },
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.3331056,
        "_source": {
          "text": "one OpenSearch"
        }
      }
    ]
  }
}
```
