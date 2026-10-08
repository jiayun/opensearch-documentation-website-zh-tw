---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Nested
parent: Bucket aggregations
nav_order: 140
redirect_from:
  - /query-dsl/aggregations/bucket/nested/
---

# Nested 彙總

`nested` 彙總可讓您對 [nested]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/nested/) 物件內的欄位進行彙總。`nested` 類型是 `object` 資料類型的特殊版本，會將物件陣列中的每個元素編製索引為獨立的隱藏文件。這樣可以保留同一陣列元素內欄位之間的關聯，使這些欄位能一起被查詢及彙總。

## Nested 彙總範例

若要對 nested 陣列內的欄位進行彙總，請指定 nested 欄位的 `path`，並在其下定義子彙總：

```json
GET logs-nested/_search
{
  "query": {
    "match": { "response": "200" }
  },
  "aggs": {
    "pages": {
      "nested": { "path": "pages" },
      "aggs": {
        "min_load_time": { "min": { "field": "pages.load_time" } }
      }
    }
  }
}
```
{% include copy-curl.html %}

傳回的命中結果包含所請求的彙總：

```json
"hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs-nested",
        "_id": "0",
        "_score": 1,
        "_source": {
          "response": "200",
          "pages": [
            {
              "page": "landing",
              "load_time": 200
            },
            {
              "page": "blog",
              "load_time": 500
            }
          ]
        }
      }
    ]
  },
  "aggregations": {
    "pages": {
      "doc_count": 2,
      "min_load_time": {
        "value": 200
      }
    }
  }
```

