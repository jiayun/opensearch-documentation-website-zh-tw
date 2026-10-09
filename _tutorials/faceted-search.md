---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分面搜尋"
nav_order: 60
---

# 在 OpenSearch 中實作分面搜尋

_分面_ 是使用者可選取以縮小搜尋結果範圍的可篩選欄位。在電子商務情境中，您可能會在搜尋結果左側看到品牌、顏色、尺寸和價格範圍等分面。例如，「冬季外套」這類查詢可能會傳回許多商品。分面讓使用者依特定顏色或價格範圍篩選商品。

分面搜尋會顯示每個分面各個值或範圍的計數，協助使用者瞭解結果的分布並快速套用篩選條件。這種方式特別適用於電子商務和以位置為基礎的搜尋。您可以使用 [`terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/) 彙總來實作精確值（例如顏色或尺寸）的分面，並使用 [`range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/) 彙總來實作連續值（例如價格、日期或距離）的分面。

本教學以電子商務網站的商品目錄為例，說明如何在 OpenSearch 中實作分面搜尋。

## 步驟 1：定義您的索引對應

首先定義您將用於分面篩選的欄位。[對應]({{site.url}}{{site.baseurl}}/mappings/)組態對有效的分面搜尋至關重要。若要對字串欄位進行分面篩選，請將欄位對應為 `keyword`，而非 `text`，因為 `text` 欄位並未針對彙總最佳化。

雖然您可以藉由設定 `"fielddata": true`，在 `text` 欄位上啟用彙總，但應避免在正式環境中採用這種方式，因為它會將所有欄位值載入堆積記憶體，大幅增加記憶體用量，並可能導致效能問題和記憶體不足錯誤。
{: .tip}

分面搜尋的常見挑戰之一，是處理資料中不一致的大小寫。例如，顏色可能儲存為「red」、「RED」或「Red」，這會建立不同的分面桶，使您的結果分散。

若要解決此問題，請建立資料匯入管線，在編製索引時將值統一轉為小寫：

```json
PUT _ingest/pipeline/normalize-color-pipeline
{
  "description": "Normalize color field to lowercase",
  "processors": [
    {
      "lowercase": {
        "field": "color"
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著將所有欄位對應為 `keyword` 以進行彙總，並將管線套用至索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "description": {
        "type": "text"
      },
      "color": {
        "type": "keyword"
      },
      "size": {
        "type": "keyword"
      },
      "price": {
        "type": "float"
      }
    }
  },
  "settings": {
    "default_pipeline": "normalize-color-pipeline"
  }
}
```
{% include copy-curl.html %}

## 步驟 2：將商品資料編製索引

接著，將範例資料編製索引至您的索引中：

```json
POST /products/_bulk
{ "index": {"_id": 1} }
{ "name": "Cotton T-shirt", "description": "Comfortable t-shirt for everyday wear", "color": "red", "size": "M", "price": 19.99 }
{ "index": {"_id": 2} }
{ "name": "T-shirt", "description": "Soft cotton t-shirt perfect for casual outings", "color": "Blue", "size": "L", "price": 19.99 }
{ "index": {"_id": 3} }
{ "name": "Jeans", "description": "Classic denim jeans with a modern fit", "color": "blue", "size": "M", "price": 49.99 }
{ "index": {"_id": 4} }
{ "name": "Sweater", "description": "Warm wool sweater for cold weather", "color": "RED", "size": "L", "price": 39.99 }
```
{% include copy-curl.html %}

## 步驟 3：執行分面搜尋

使用 `terms` 彙總，傳回所需欄位（在此範例中為 `color` 和 `size`）的分面桶：

```json
POST /products/_search
{
  "query": {
    "match": {
      "name": "T-shirt"
    }
  },
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    },
    "sizes": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含依顏色和尺寸彙總的所有 T 恤：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 68,
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
    "max_score": 0.59534115,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.59534115,
        "_source": {
          "color": "blue",
          "size": "L",
          "price": 19.99,
          "name": "T-shirt",
          "description": "Soft cotton t-shirt perfect for casual outings"
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.48764127,
        "_source": {
          "color": "red",
          "size": "M",
          "price": 19.99,
          "name": "Cotton T-shirt",
          "description": "Comfortable t-shirt for everyday wear"
        }
      }
    ]
  },
  "aggregations": {
    "sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "L",
          "doc_count": 1
        },
        {
          "key": "M",
          "doc_count": 1
        }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 1
        },
        {
          "key": "red",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

### 搜尋多個欄位

若要同時搜尋 `name` 和 `description` 欄位，請使用 `multi_match` 查詢。請注意，雖然查詢會搜尋多個文字欄位（`name` 和 `description`），但彙總使用的是關鍵字欄位（`color`、`size`），以確保分面值一致：

```json
POST /products/_search
{
  "query": {
    "multi_match": {
      "query": "cotton t-shirt",
      "fields": ["name", "description"],
      "operator": "and",
      "type": "best_fields"
    }
  },
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    },
    "sizes": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩件 T 恤：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 33,
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
    "max_score": 1.0944791,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1.0944791,
        "_source": {
          "color": "blue",
          "size": "L",
          "price": 19.99,
          "name": "T-shirt",
          "description": "Soft cotton t-shirt perfect for casual outings"
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.9111493,
        "_source": {
          "color": "red",
          "size": "M",
          "price": 19.99,
          "name": "Cotton T-shirt",
          "description": "Comfortable t-shirt for everyday wear"
        }
      }
    ]
  },
  "aggregations": {
    "sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "L",
          "doc_count": 1
        },
        {
          "key": "M",
          "doc_count": 1
        }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 1
        },
        {
          "key": "red",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

如需 `multi_match` 查詢參數的詳細資訊，請參閱[多重比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/)。

### 只回傳分面資料

如果您只需要分面計數而不需要實際的搜尋結果，可以設定 `"size": 0` 以提升效能：

```json
POST /products/_search
{
  "size": 0,
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 指定結果數量

預設情況下，`terms` 彙總會回傳出現次數最多的前 10 個詞彙。如果您需要更多或更少的結果，可以設定 `size` 參數：

```json
POST /products/_search
{
  "aggs": {
    "colors": {
      "terms": {
        "field": "color",
        "size": 20
      }
    }
  }
}
```
{% include copy-curl.html %}


## 步驟 4：依分面值篩選

若要縮小結果範圍（例如，搜尋藍色且尺寸為 L 的 T 恤），請新增 `filter` 子句：

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "T-shirt" } }
      ],
      "filter": [
        { "term": { "color": "blue" } },
        { "term": { "size": "L" } }
      ]
    }
  },
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    },
    "sizes": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含符合條件的產品：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 66,
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
    "max_score": 0.59534115,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.59534115,
        "_source": {
          "color": "blue",
          "size": "L",
          "price": 19.99,
          "name": "T-shirt",
          "description": "Soft cotton t-shirt perfect for casual outings"
        }
      }
    ]
  },
  "aggregations": {
    "sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "L",
          "doc_count": 1
        }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

結果顯示如下。

![分面搜尋結果]({{site.url}}{{site.baseurl}}/images/faceted-search/faceted-search-filter.png)

### 篩選時保留分面選項

當使用者選取分面篩選器時，通常仍會期望看到其他可用的篩選選項。例如，如果使用者篩選紅色 T 恤，顏色分面仍應顯示原始搜尋結果中所有可用的顏色（紅色、藍色及其他），而不只是「紅色」。這有助於使用者了解完整的選項範圍，並輕鬆地在篩選器之間切換。

您可以使用 `post_filter` 來達成此行為。`post_filter` 會在彙總計算完成後篩選搜尋結果，因此分面會反映未篩選的資料集：

```json
POST /products/_search
{
  "query": {
    "match": {
      "name": "t-shirt"
    }
  },
  "post_filter": {
    "term": { "color": "red" }
  },
  "aggs": {
    "all_colors": {
      "terms": {
        "field": "color"
      }
    },
    "sizes_for_red": {
      "filter": {
        "term": { "color": "red" }
      },
      "aggs": {
        "sizes": {
          "terms": {
            "field": "size"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含符合條件的 T 恤，以及所有 T 恤的顏色桶：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 17,
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
    "max_score": 0.48764127,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.48764127,
        "_source": {
          "color": "red",
          "size": "M",
          "price": 19.99,
          "name": "Cotton T-shirt",
          "description": "Comfortable t-shirt for everyday wear"
        }
      }
    ]
  },
  "aggregations": {
    "sizes_for_red": {
      "doc_count": 1,
      "sizes": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "M",
            "doc_count": 1
          }
        ]
      }
    },
    "all_colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 1
        },
        {
          "key": "red",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

結果顯示如下。

![篩選時保留分面的分面搜尋結果]({{site.url}}{{site.baseurl}}/images/faceted-search/faceted-search-maintain.png)

或者，您可以使用[全域彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/global/)來確保分面一律反映完整的資料集，而不受已套用篩選器的影響：

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "t-shirt" } }
      ],
      "filter": [
        { "term": { "color": "red" } }
      ]
    }
  },
  "aggs": {
    "all_facets": {
      "global": {},
      "aggs": {
        "all_colors": {
          "filter": {
            "match": { "name": "t-shirt" }
          },
          "aggs": {
            "colors": {
              "terms": {
                "field": "color"
              }
            }
          }
        }
      }
    },
    "filtered_sizes": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}

全域彙總會針對整個索引執行，因此您需要在全域彙總內重新套用基礎查詢（T 恤搜尋），才能取得正確的分面計數。回應與前一種方法產生的結果類似：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 9,
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
    "max_score": 0.48764127,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.48764127,
        "_source": {
          "color": "red",
          "size": "M",
          "price": 19.99,
          "name": "Cotton T-shirt",
          "description": "Comfortable t-shirt for everyday wear"
        }
      }
    ]
  },
  "aggregations": {
    "filtered_sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "M",
          "doc_count": 1
        }
      ]
    },
    "all_facets": {
      "doc_count": 4,
      "all_colors": {
        "doc_count": 2,
        "colors": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "blue",
              "doc_count": 1
            },
            {
              "key": "red",
              "doc_count": 1
            }
          ]
        }
      }
    }
  }
}
```

</details>

### 排除分面值

除了篩選特定的分面值之外，使用者可能也想從結果中排除某些值。例如，使用者可能想查看所有產品，但排除紅色的產品。使用 `must_not` 子句來排除特定的分面值：

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match_all": {} }
      ],
      "must_not": [
        { "term": { "color": "red" } }
      ]
    }
  },
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    },
    "sizes": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含非紅色產品，並帶有 color 和 size 桶：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "color": "blue",
          "size": "L",
          "price": 19.99,
          "name": "T-shirt",
          "description": "Soft cotton t-shirt perfect for casual outings"
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 1,
        "_source": {
          "color": "blue",
          "size": "M",
          "price": 49.99,
          "name": "Jeans",
          "description": "Classic denim jeans with a modern fit"
        }
      }
    ]
  },
  "aggregations": {
    "sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "L",
          "doc_count": 1
        },
        {
          "key": "M",
          "doc_count": 1
        }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "blue",
          "doc_count": 2
        }
      ]
    }
  }
}
```

</details>

結果顯示如下。

![使用排除篩選的分面搜尋結果]({{site.url}}{{site.baseurl}}/images/faceted-search/faceted-search-exlclude.png)

## 步驟 5：範圍分面

您可以為包含數值（例如價格、評分或日期）的欄位建立範圍分面。

### 數值範圍

若要為產品建立價格範圍，請使用 `range` 彙總：

```json
POST /products/_search
{
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 20, "key": "Under $20" },
          { "from": 20, "to": 40, "key": "$20 - $40" },
          { "from": 40, "key": "Over $40" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會依價格將產品分桶：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 76,
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
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "color": "red",
          "size": "M",
          "price": 19.99,
          "name": "Cotton T-shirt",
          "description": "Comfortable t-shirt for everyday wear"
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "color": "blue",
          "size": "L",
          "price": 19.99,
          "name": "T-shirt",
          "description": "Soft cotton t-shirt perfect for casual outings"
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 1,
        "_source": {
          "color": "blue",
          "size": "M",
          "price": 49.99,
          "name": "Jeans",
          "description": "Classic denim jeans with a modern fit"
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 1,
        "_source": {
          "color": "red",
          "size": "L",
          "price": 39.99,
          "name": "Sweater",
          "description": "Warm wool sweater for cold weather"
        }
      }
    ]
  },
  "aggregations": {
    "price_ranges": {
      "buckets": [
        {
          "key": "Under $20",
          "to": 20,
          "doc_count": 2
        },
        {
          "key": "$20 - $40",
          "from": 20,
          "to": 40,
          "doc_count": 1
        },
        {
          "key": "Over $40",
          "from": 40,
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

### 地理範圍

地理範圍適用於以位置為基礎的分面，例如尋找距離使用者位置一定距離內的商店。首先，建立包含 `geo_point` 類型之 `store_location` 欄位的對應：

```json
PUT /stores
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "store_location": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

將一些包含不同商店的文件編製索引至索引中：

```json
POST /stores/_bulk
{ "index": { "_id": "1" } }
{ "name": "Downtown Store", "store_location": { "lat": 40.7510, "lon": -73.9900 } }
{ "index": { "_id": "2" } }
{ "name": "Suburban Store", "store_location": { "lat": 40.8300, "lon": -74.2000 } }
{ "index": { "_id": "3" } }
{ "name": "Outskirts Store", "store_location": { "lat": 41.2000, "lon": -74.8000 } }
```
{% include copy-curl.html %}

若要以位置為基礎進行分面（例如尋找附近商店提供的產品），請使用 `geo_distance` 彙總：

```json
POST /stores/_search
{
  "aggs": {
    "store_distance": {
      "geo_distance": {
        "field": "store_location",
        "origin": "40.7507, -73.9895",
        "unit": "mi",
        "ranges": [
          { "to": 5, "key": "Within 5 miles" },
          { "from": 5, "to": 25, "key": "5-25 miles away" },
          { "from": 25, "key": "Over 25 miles away" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含依距離分桶的所有三個商店：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 16,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "stores",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Downtown Store",
          "store_location": {
            "lat": 40.751,
            "lon": -73.99
          }
        }
      },
      {
        "_index": "stores",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Suburban Store",
          "store_location": {
            "lat": 40.83,
            "lon": -74.2
          }
        }
      },
      {
        "_index": "stores",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Outskirts Store",
          "store_location": {
            "lat": 41.2,
            "lon": -74.8
          }
        }
      }
    ]
  },
  "aggregations": {
    "store_distance": {
      "buckets": [
        {
          "key": "Within 5 miles",
          "from": 0,
          "to": 5,
          "doc_count": 1
        },
        {
          "key": "5-25 miles away",
          "from": 5,
          "to": 25,
          "doc_count": 1
        },
        {
          "key": "Over 25 miles away",
          "from": 25,
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

## 階層式分面

階層式分面可讓您在屬性階層中逐層深入檢視，例如類別 > 子類別 > 產品類型。這可以使用以分隔符編碼階層的欄位來實作。

首先，建立一個使用 `path_hierarchy` 斷詞器的資料匯入管線，自動產生所有階層層級：

```json
PUT _ingest/pipeline/category-hierarchy-pipeline
{
  "description": "Split category path into multiple hierarchy fields",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          // Split the category_path on '>'
          def parts = ctx.category_path.splitOnToken('>');
          
          // Create individual-level fields
          if (parts.length >= 1) {
            ctx.category_level1 = parts[0].trim();
          }
          if (parts.length >= 2) {
            ctx.category_level2 = parts[1].trim();
          }
          if (parts.length >= 3) {
            ctx.category_level3 = parts[2].trim();
          }
          
          // Create hierarchy array with cumulative paths
          def hierarchy = [];
          def currentPath = '';
          for (int i = 0; i < parts.length; i++) {
            if (i == 0) {
              currentPath = parts[i].trim();
            } else {
              currentPath = currentPath + '>' + parts[i].trim();
            }
            hierarchy.add(currentPath);
          }
          ctx.category_hierarchy = hierarchy;
        """
      }
    }
  ]
}
```
{% include copy.html %}

如果您是在終端機中執行命令，請使用對應的 cURL 請求：

```bash
curl -XPUT "http://localhost:9200/_ingest/pipeline/category-hierarchy-pipeline" -H 'Content-Type: application/json' -d'
{
  "description": "Split category path into multiple hierarchy fields",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": "\n          // Split the category_path on '\''>'\''\n          def parts = ctx.category_path.splitOnToken('\''>'\'');\n          \n          // Create individual level fields\n          if (parts.length >= 1) {\n            ctx.category_level1 = parts[0].trim();\n          }\n          if (parts.length >= 2) {\n            ctx.category_level2 = parts[1].trim();\n          }\n          if (parts.length >= 3) {\n            ctx.category_level3 = parts[2].trim();\n          }\n          \n          // Create hierarchy array with cumulative paths\n          def hierarchy = [];\n          def currentPath = '\'''\'';\n          for (int i = 0; i < parts.length; i++) {\n            if (i == 0) {\n              currentPath = parts[i].trim();\n            } else {\n              currentPath = currentPath + '\''>'\'' + parts[i].trim();\n            }\n            hierarchy.add(currentPath);\n          }\n          ctx.category_hierarchy = hierarchy;\n        "
      }
    }
  ]
}'
```
{% include copy.html %}

這種做法避免在 `text` 欄位上使用 `fielddata`，而是將每個階層層級明確儲存為獨立的 `keyword` 欄位。雖然這需要更多儲存空間，但可提供更好的查詢效能，並在彙總時更節省記憶體。在正式系統中，您可以在編製索引時使用資料匯入管線或應用程式邏輯自動擷取階層層級。

接下來，定義包含階層式欄位的索引對應，並將該管線設定為索引的預設管線：

```json
PUT /products-advanced
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "color": { "type": "keyword" },
      "category_path": { "type": "keyword" },
      "category_level1": { "type": "keyword" },
      "category_level2": { "type": "keyword" },
      "category_level3": { "type": "keyword" },
      "category_hierarchy": { "type": "keyword" }
    }
  },
  "settings": {
    "default_pipeline": "category-hierarchy-pipeline"
  }
}
```
{% include copy-curl.html %}

使用資料匯入管線為含有階層式資料的產品編製索引，以自動產生階層層級：

```json
POST /products-advanced/_bulk
{ "index": {"_id": 1} }
{ "name": "Cotton T-Shirt", "color": "red", "category_path": "Clothing>Shirts>T-Shirts" }
{ "index": {"_id": 2} }
{ "name": "Wool Sweater", "color": "red", "category_path": "Clothing>Sweaters>Wool" }
{ "index": {"_id": 3} }
{ "name": "Running Shoes", "color": "red", "category_path": "Footwear>Athletic>Running" }
{ "index": {"_id": 4} }
{ "name": "Dress Shirt", "color": "blue", "category_path": "Clothing>Shirts>Dress" }
{ "index": {"_id": 5} }
{ "name": "Hiking Boots", "color": "blue", "category_path": "Footwear>Outdoor>Hiking" }
{ "index": {"_id": 6} }
{ "name": "Casual Sneakers", "color": "blue", "category_path": "Footwear>Casual>Sneakers" }
```
{% include copy-curl.html %}

使用多個彙總查詢階層式分面，以取得類別資料的不同檢視。您可以針對個別階層層級進行彙總，或在單一結果中檢視完整的階層路徑：

```json
POST /products-advanced/_search
{
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category_level1"
      }
    },
    "subcategories": {
      "terms": {
        "field": "category_level2"
      }
    },
    "full_hierarchy": {
      "terms": {
        "field": "category_hierarchy"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含具有個別彙總結果的扁平結構。類別會顯示計數以及跨類別總計。例如，`Athletic` 子類別顯示來自 `Clothing` (1) 與 `Footwear` (1) 的合併計數：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 116,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products-advanced",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>T-Shirts"
          ],
          "category_level2": "Shirts",
          "color": "red",
          "category_path": "Clothing>Shirts>T-Shirts",
          "name": "Cotton T-Shirt",
          "category_level3": "T-Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "2",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Athletic",
            "Clothing>Athletic>Shirts"
          ],
          "category_level2": "Athletic",
          "color": "red",
          "category_path": "Clothing>Athletic>Shirts",
          "name": "Athletic shirt",
          "category_level3": "Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "3",
        "_score": 1,
        "_source": {
          "category_level1": "Footwear",
          "category_hierarchy": [
            "Footwear",
            "Footwear>Athletic",
            "Footwear>Athletic>Running"
          ],
          "category_level2": "Athletic",
          "color": "red",
          "category_path": "Footwear>Athletic>Running",
          "name": "Running Shoes",
          "category_level3": "Running"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "4",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "blue",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "5",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "white",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "6",
        "_score": 1,
        "_source": {
          "category_level1": "Footwear",
          "category_hierarchy": [
            "Footwear",
            "Footwear>Casual",
            "Footwear>Casual>Sneakers"
          ],
          "category_level2": "Casual",
          "color": "blue",
          "category_path": "Footwear>Casual>Sneakers",
          "name": "Casual Sneakers",
          "category_level3": "Sneakers"
        }
      }
    ]
  },
  "aggregations": {
    "full_hierarchy": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Clothing",
          "doc_count": 4
        },
        {
          "key": "Clothing>Shirts",
          "doc_count": 3
        },
        {
          "key": "Clothing>Shirts>Dress",
          "doc_count": 2
        },
        {
          "key": "Footwear",
          "doc_count": 2
        },
        {
          "key": "Clothing>Athletic",
          "doc_count": 1
        },
        {
          "key": "Clothing>Athletic>Shirts",
          "doc_count": 1
        },
        {
          "key": "Clothing>Shirts>T-Shirts",
          "doc_count": 1
        },
        {
          "key": "Footwear>Athletic",
          "doc_count": 1
        },
        {
          "key": "Footwear>Athletic>Running",
          "doc_count": 1
        },
        {
          "key": "Footwear>Casual",
          "doc_count": 1
        },
        {
          "key": "Footwear>Casual>Sneakers",
          "doc_count": 1
        }
      ]
    },
    "top_categories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Clothing",
          "doc_count": 4
        },
        {
          "key": "Footwear",
          "doc_count": 2
        }
      ]
    },
    "subcategories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Shirts",
          "doc_count": 3
        },
        {
          "key": "Athletic",
          "doc_count": 2
        },
        {
          "key": "Casual",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

結果顯示如下。

![具有階層式扁平分類的分面搜尋結果]({{site.url}}{{site.baseurl}}/images/faceted-search/faceted-search-hierarchical-flat.png)

若要進行階層式導覽，請使用巢狀彙總：

```json
POST /products-advanced/_search
{
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category_level1"
      },
      "aggs": {
        "subcategories": {
          "terms": {
            "field": "category_level2"
          }
        }
      }
    },
    "full_hierarchy": {
      "terms": {
        "field": "category_hierarchy"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應具有階層式結構，子類別巢狀於其父類別之下。例如，`Athletic` 同時出現在 `Clothing` (1) 與 `Footwear` (1) 之下。子類別計數的範圍限定於其父類別：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 79,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products-advanced",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>T-Shirts"
          ],
          "category_level2": "Shirts",
          "color": "red",
          "category_path": "Clothing>Shirts>T-Shirts",
          "name": "Cotton T-Shirt",
          "category_level3": "T-Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "2",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Athletic",
            "Clothing>Athletic>Shirts"
          ],
          "category_level2": "Athletic",
          "color": "red",
          "category_path": "Clothing>Athletic>Shirts",
          "name": "Athletic shirt",
          "category_level3": "Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "3",
        "_score": 1,
        "_source": {
          "category_level1": "Footwear",
          "category_hierarchy": [
            "Footwear",
            "Footwear>Athletic",
            "Footwear>Athletic>Running"
          ],
          "category_level2": "Athletic",
          "color": "red",
          "category_path": "Footwear>Athletic>Running",
          "name": "Running Shoes",
          "category_level3": "Running"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "4",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "blue",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "5",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "white",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "6",
        "_score": 1,
        "_source": {
          "category_level1": "Footwear",
          "category_hierarchy": [
            "Footwear",
            "Footwear>Casual",
            "Footwear>Casual>Sneakers"
          ],
          "category_level2": "Casual",
          "color": "blue",
          "category_path": "Footwear>Casual>Sneakers",
          "name": "Casual Sneakers",
          "category_level3": "Sneakers"
        }
      }
    ]
  },
  "aggregations": {
    "full_hierarchy": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Clothing",
          "doc_count": 4
        },
        {
          "key": "Clothing>Shirts",
          "doc_count": 3
        },
        {
          "key": "Clothing>Shirts>Dress",
          "doc_count": 2
        },
        {
          "key": "Footwear",
          "doc_count": 2
        },
        {
          "key": "Clothing>Athletic",
          "doc_count": 1
        },
        {
          "key": "Clothing>Athletic>Shirts",
          "doc_count": 1
        },
        {
          "key": "Clothing>Shirts>T-Shirts",
          "doc_count": 1
        },
        {
          "key": "Footwear>Athletic",
          "doc_count": 1
        },
        {
          "key": "Footwear>Athletic>Running",
          "doc_count": 1
        },
        {
          "key": "Footwear>Casual",
          "doc_count": 1
        },
        {
          "key": "Footwear>Casual>Sneakers",
          "doc_count": 1
        }
      ]
    },
    "top_categories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Clothing",
          "doc_count": 4,
          "subcategories": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
              {
                "key": "Shirts",
                "doc_count": 3
              },
              {
                "key": "Athletic",
                "doc_count": 1
              }
            ]
          }
        },
        {
          "key": "Footwear",
          "doc_count": 2,
          "subcategories": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
              {
                "key": "Athletic",
                "doc_count": 1
              },
              {
                "key": "Casual",
                "doc_count": 1
              }
            ]
          }
        }
      ]
    }
  }
}
```

</details>

結果顯示如下。

![具有階層式巢狀分類的分面搜尋結果]({{site.url}}{{site.baseurl}}/images/faceted-search/faceted-search-hierarchical-nested.png)

前綴查詢可讓您依分類階層的特定分支進行篩選，將結果範圍限定在特定分類層級及其所有子分類。若只要顯示 `Clothing>Shirts` 分類及其子分類中的產品，請使用 `keyword` 欄位進行精確的前綴比對：

```json
POST /products-advanced/_search
{
  "query": {
    "prefix": {
      "category_path": "Clothing>Shirts"
    }
  }
}
```
{% include copy-curl.html %}

回應中包含相符的文件。請注意，運動衫不會被傳回：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 44,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "products-advanced",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>T-Shirts"
          ],
          "category_level2": "Shirts",
          "color": "red",
          "category_path": "Clothing>Shirts>T-Shirts",
          "name": "Cotton T-Shirt",
          "category_level3": "T-Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "4",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "blue",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "5",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "white",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      }
    ]
  }
}
```

</details>

若只要依 `Clothing` 分類的顏色進行彙總，請使用下列請求：

```json
POST /products-advanced/_search
{
  "query": {
    "prefix": {
      "category_path": "Clothing>"
    }
  },
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中只包含 `Clothing` 產品：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 30,
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
        "_index": "products-advanced",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>T-Shirts"
          ],
          "category_level2": "Shirts",
          "color": "red",
          "category_path": "Clothing>Shirts>T-Shirts",
          "name": "Cotton T-Shirt",
          "category_level3": "T-Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "2",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Athletic",
            "Clothing>Athletic>Shirts"
          ],
          "category_level2": "Athletic",
          "color": "red",
          "category_path": "Clothing>Athletic>Shirts",
          "name": "Athletic shirt",
          "category_level3": "Shirts"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "4",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "blue",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      },
      {
        "_index": "products-advanced",
        "_id": "5",
        "_score": 1,
        "_source": {
          "category_level1": "Clothing",
          "category_hierarchy": [
            "Clothing",
            "Clothing>Shirts",
            "Clothing>Shirts>Dress"
          ],
          "category_level2": "Shirts",
          "color": "white",
          "category_path": "Clothing>Shirts>Dress",
          "name": "Dress Shirt",
          "category_level3": "Dress"
        }
      }
    ]
  },
  "aggregations": {
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "red",
          "doc_count": 2
        },
        {
          "key": "blue",
          "doc_count": 1
        },
        {
          "key": "white",
          "doc_count": 1
        }
      ]
    }
  }
}
```

</details>

同樣地，您也可以在 `prefix` 查詢中指定 `"category_path": "Clothing>Shirts"`，以彙總 `Clothing>Shirts` 分類。您的應用程式程式碼接著可移除前綴，以提供更簡潔的顯示內容（例如視需要將 `Clothing>Shirts` 改為 `Shirts`）。OpenSearch 負責繁重的工作（斷詞與彙總），而您的應用程式程式碼則依階層層級移除前綴，處理顯示格式。


## 相關文件

- [對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)
- [支援的欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/)
- [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)
- [查詢與篩選情境]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)
- [彙總]({{site.url}}{{site.baseurl}}/aggregations/)