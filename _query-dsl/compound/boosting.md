---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "加權"
parent: Compound queries
nav_order: 30
redirect_from:
  - /query-dsl/query-dsl/compound/boosting/
---

# Boosting 查詢

如果您要搜尋「pitcher」這個詞，您的結果可能與棒球投手或盛裝液體的容器有關。若是在棒球的脈絡下搜尋，您可能會想使用 `must_not` 子句，完全排除包含「glass」或「water」等詞的結果。不過，如果您想保留這些結果，但降低它們的相關性，則可以使用 `boosting` 查詢來達成。

`boosting` 查詢會傳回符合 `positive` 查詢的文件。在這些文件中，同時符合 `negative` 查詢的文件，其相關性分數會較低（其相關性分數會乘以負向加權係數）。

## 範例

假設有一個索引包含兩份文件，您將它們編製索引如下：

```json
PUT testindex/_doc/1
{
  "article_name": "The greatest pitcher in baseball history"
}
```

```json
PUT testindex/_doc/2
{
  "article_name": "The making of a glass pitcher"
}
```

使用下列 match 查詢來搜尋包含「pitcher」這個詞的文件：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "article_name": "pitcher"
    }
  }
}
```

傳回的兩份文件具有相同的相關性分數：

```json
{
  "took": 5,
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
    "max_score": 0.18232156,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.18232156,
        "_source": {
          "article_name": "The greatest pitcher in baseball history"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.18232156,
        "_source": {
          "article_name": "The making of a glass pitcher"
        }
      }
    ]
  }
}
```

現在使用下列 `boosting` 查詢來搜尋包含「pitcher」這個詞的文件，但降低包含「glass」、「crystal」或「water」等詞之文件的相關性：

```json
GET testindex/_search
{
  "query": {
    "boosting": {
      "positive": {
        "match": {
          "article_name": "pitcher"
        }
      },
      "negative": {
        "match": {
          "article_name": "glass crystal water"
        }
      },
      "negative_boost": 0.1
    }
  }
}
```
{% include copy-curl.html %}

兩份文件仍會傳回，但包含「glass」這個詞的文件，其相關性分數比前一個情況低 10 倍：

```json
{
  "took": 13,
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
    "max_score": 0.18232156,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.18232156,
        "_source": {
          "article_name": "The greatest pitcher in baseball history"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.018232157,
        "_source": {
          "article_name": "The making of a glass pitcher"
        }
      }
    ]
  }
}
```

## 參數

下表列出 `boosting` 查詢支援的所有最上層參數。

參數 | 說明
:--- | :---
`positive` | 文件必須符合此查詢，才會出現在結果中。必要。
`negative` | 如果結果中的文件符合此查詢，其相關性分數會降低，方式是將其原始相關性分數（由 `positive` 查詢產生）乘以 `negative_boost` 參數。必要。
`negative_boost` | 介於 0 與 1.0 之間的浮點數因數，用來乘以原始相關性分數，以降低符合 `negative` 查詢之文件的相關性。必要。
