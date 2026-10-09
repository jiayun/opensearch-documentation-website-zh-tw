---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "後置篩選"
parent: Filtering data
nav_order: 20
---

# 對向量搜尋結果進行後置篩選

您可以透過 [布林篩選](#boolean-filter-with-ann-search) 或提供 [`post_filter` 參數](#the-post_filter-parameter) 來實現後置篩選。

### 搭配 ANN 搜尋的布林篩選

布林篩選由一個包含 k-NN 查詢與篩選條件的布林查詢組成。例如，下列查詢會搜尋距離指定 `location` 最近的飯店，然後篩選結果，只回傳評分介於 8 到 10（含）且提供停車位的飯店：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "bool": {
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "rating": {
                  "gte": 8,
                  "lte": 10
                }
              }
            },
            {
              "term": {
                "parking": "true"
              }
            }
          ]
        }
      },
      "must": [
        {
          "knn": {
            "location": {
              "vector": [
                5,
                4
              ],
              "k": 20
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應會包含內含符合飯店的文件：

```json
{
  "took" : 95,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 5,
      "relation" : "eq"
    },
    "max_score" : 0.72992706,
    "hits" : [
      {
        "_index" : "hotels-index",
        "_id" : "3",
        "_score" : 0.72992706,
        "_source" : {
          "location" : [
            4.9,
            3.4
          ],
          "parking" : "true",
          "rating" : 9
        }
      },
      {
        "_index" : "hotels-index",
        "_id" : "6",
        "_score" : 0.3012048,
        "_source" : {
          "location" : [
            6.4,
            3.4
          ],
          "parking" : "true",
          "rating" : 9
        }
      },
      {
        "_index" : "hotels-index",
        "_id" : "5",
        "_score" : 0.24154587,
        "_source" : {
          "location" : [
            3.3,
            4.5
          ],
          "parking" : "true",
          "rating" : 8
        }
      }
    ]
  }
}
```

### post_filter 參數

如果您將 `knn` 查詢與篩選條件或其他子句（例如 `bool`、`must`、`match`）一起使用，可能會收到少於 `k` 筆的結果。在此範例中，`post_filter` 會將結果數量從 2 筆減少為 1 筆：

```json
GET my-knn-index-1/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector2": {
        "vector": [2, 3, 5, 6],
        "k": 2
      }
    }
  },
  "post_filter": {
    "range": {
      "price": {
        "gte": 5,
        "lte": 10
      }
    }
  }
}
```
{% include copy-curl.html %}