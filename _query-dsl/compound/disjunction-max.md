---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "析取最大值"
parent: Compound queries
nav_order: 50
redirect_from:
  - /query-dsl/query-dsl/compound/disjunction-max/
---

# 析取最大值查詢

析取最大值（`dis_max`）查詢會傳回符合一或多個查詢子句的任何文件。對於符合多個查詢子句的文件，其相關性分數會設為所有符合的查詢子句中最高的相關性分數。

當傳回文件的相關性分數相同時，您可以使用 `tie_breaker` 參數，讓符合多個查詢子句的文件獲得更高的權重。

## 範例

假設有一個包含兩份文件的索引，您依下列方式將文件編製索引：

```json
PUT testindex1/_doc/1
{
  "title": "The Top 10 Shakespeare Poems",
  "body": "Top 10 sonnets of England's national poet and the Bard of Avon"
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "title": "Sonnets of the 16th Century",
  "body": "The poems written by various 16th-century poets"
}
```
{% include copy-curl.html %}

使用 `dis_max` 查詢，在 `title` 與 `body` 欄位中搜尋「Shakespeare poems」這兩個詞：

```json
GET testindex1/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "Shakespeare poems" }},
        { "match": { "body":  "Shakespeare poems" }}
      ]
    }
  }            
}
```
{% include copy-curl.html %}

回應包含這兩份文件。文件 1 獲得較高的相關性分數，因為其 `title` 欄位同時符合兩個詞，而文件 2 只符合「poems」這個詞：

```json
{
  "took": 1,
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
    "max_score": 0.63013375,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 0.63013375,
        "_source": {
          "title": "The Top 10 Shakespeare Poems",
          "body": "Top 10 sonnets of England's national poet and the Bard of Avon"
        }
      },
      {
        "_index": "testindex1",
        "_id": "2",
        "_score": 0.34314215,
        "_source": {
          "title": "Sonnets of the 16th Century",
          "body": "The poems written by various 16th-century poets"
        }
      }
    ]
  }
}
```

## 參數

下表列出 `dis_max` 查詢支援的所有頂層參數。

參數 | 說明
:--- | :---
`queries` | 由一或多個查詢子句組成的陣列，用於比對文件。文件必須至少符合一個查詢子句，才會出現在結果中。如果文件符合多個查詢子句，其相關性分數會設為所有符合的查詢子句中最高的相關性分數。必要。
`tie_breaker` | 介於 0 與 1.0 之間的浮點數係數，用於讓符合多個查詢子句的文件獲得更高的權重。在此情況下，文件的相關性分數會使用下列演算法計算：取所有符合的查詢子句中最高的相關性分數，將其他所有符合子句的分數乘以 `tie_breaker` 值，再將相關性分數相加並進行正規化。選用。預設為 0（表示只有最高分數會被計入）。
