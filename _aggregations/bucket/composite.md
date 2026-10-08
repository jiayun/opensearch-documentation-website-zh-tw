---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複合"
parent: Bucket aggregations
nav_order: 17
redirect_from:
  - /query-dsl/aggregations/bucket/composite/
---

# 複合彙總

`composite` 彙總會根據一或多個文件欄位或來源建立桶 (bucket)。`composite` 彙總會為個別來源值的每一種組合各建立一個桶。根據預設，若某個組合在一或多個個別欄位中有缺失值，該組合會從結果中省略。

每個來源都屬於下列四種彙總類型之一：

- `terms` 類型依唯一值（通常為 `String`）分組。
- `histogram` 類型以數值方式分組到指定寬度的桶中。
- `date_histogram` 類型依指定寬度的日期或時間範圍分組。
- `geotile_grid` 類型將地理點分組到具有指定解析度的網格中。

`composite` 彙總的運作方式是將其來源鍵組合成桶。產生的桶在來源之間與來源之內都會排序：

- **來源之間**：桶會依照來源在彙總請求中的排列順序巢狀排列。
- **來源之內**：每個來源中值的順序決定該來源的桶順序。排序方式依來源類型而定，可能是字母、數值、日期時間或地理圖磚順序。

請參考下列馬拉松參賽者索引中的欄位：

```json
{... "city": "Albuquerque", "place": "Bronze" ...}
{... "city": "Boston",  ...}
{... "city": "Chicago", "place": "Bronze" ...}
{... "city": "Albuquerque", "place": "Gold" ...}
{... "city": "Chicago", "place": "Silver" ...}
{... "city": "Boston", "place": "Bronze" ...}
{... "city": "Chicago", "place": "Gold" ...}
```

假設請求如下指定來源：

```json
    ...
    "sources": [
        { "marathon_city": { "terms": { "field": "city" }}},
        { "participant_medal": { "terms": { "field": "place" }}}
    ],
    ...
```

您必須為每個來源指派唯一的鍵名稱。
{: .important}

產生的 `composite` 依序包含下列桶：

```json
{ "city": "Albuquerque", "place": "Bronze" }
{ "city": "Albuquerque", "place": "Gold" }
{ "city": "Boston", "place": "Bronze" }
{ "city": "Boston", "place": "Silver" }
{ "city": "Chicago", "place": "Bronze" }
{ "city": "Chicago", "place": "Gold" }
{ "city": "Chicago", "place": "Silver" }
```

請注意，`city` 和 `place` 欄位都是依字母順序排序。

## 參數

`composite` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型  | 說明 |
| :--       | :--               | :--        | :--         |
| `sources` | 必要          | 陣列      | 來源物件的陣列。有效類型為 [`terms`](#terms)、[`histogram`](#histogram)、[`date_histogram`](#date-histogram) 和 [`geotile_grid`](#geotile-grid)。 |
| `size`    | 選用          | 數值    | 要在結果中傳回的 `composite` 桶數量。預設值為 `10`。請參閱[將複合結果分頁](#paginating-composite-results)。 |
| `after` | 選用 | 字串 | 指定要從何處繼續顯示分頁 `composite` 桶的鍵。請參閱[將複合結果分頁](#paginating-composite-results)。 |
| `order`   | 選用          | 字串     | 針對每個來源，指定要以遞增或遞減順序排列值。有效值為 `asc` 和 `desc`。預設為 `asc`。 |
| `missing_bucket` | 選用    | 布林值   | 針對每個來源，指定是否包含具有缺失值的文件。預設值為 `false`。若設為 `true`，OpenSearch 會包含這些文件，並以 `null` 作為該欄位的鍵。Null 值在遞增順序中排在最前面。 |

如需彙總特定的參數，請參閱對應的彙總文件。
{: .note}

## 詞彙

使用 `terms` 彙總來彙總字串或布林值資料。如需詳細資訊，請參閱[詞彙彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)。

您可以使用 `terms` 來源為任何類型的資料建立複合桶。不過，由於 `terms` 來源會為每個唯一值建立桶，因此對於數值資料，您通常會改用 `histogram` 來源。
{: .note}

下列範例請求會傳回 OpenSearch Dashboards 範例電子商務資料中，依星期幾和客戶性別分組的前 `4` 個複合桶：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "day": { "terms": { "field": "day_of_week" }}},
          { "gender": { "terms": { "field": "customer_gender" }}}
        ],
        "size": 4
      }
    }
  }
}
```
{% include copy-curl.html %}

由於此範例的資料集在每個桶中都包含有效資料，因此彙總會為性別與星期幾的每種組合產生一個桶，總共產生 14 個桶。

由於請求將 `size` 指定為 `4`，因此回應包含前四個複合桶。由於來源為 `terms`，桶在來源之間與來源之內都會依字母遞增順序排序：

```json
{
  "took": 51,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "day": "Monday",
        "gender": "MALE"
      },
      "buckets": [
        {
          "key": {
            "day": "Friday",
            "gender": "FEMALE"
          },
          "doc_count": 399
        },
        {
          "key": {
            "day": "Friday",
            "gender": "MALE"
          },
          "doc_count": 371
        },
        {
          "key": {
            "day": "Monday",
            "gender": "FEMALE"
          },
          "doc_count": 320
        },
        {
          "key": {
            "day": "Monday",
            "gender": "MALE"
          },
          "doc_count": 259
        }
      ]
    }
  }
}
```

您可以使用回應中傳回的 `after_key` 來檢視更多結果。請參閱下一節中的範例。

## 直方圖

使用 `histogram` 來源建立數值資料的複合彙總。如需詳細資訊，請參閱[直方圖彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/)。

對於 `histogram` 來源，每個 `composite` 桶鍵中使用的名稱，是該鍵直方圖間隔中的最小值。每個來源直方圖間隔包含 `[lower_bound, lower_bound + interval)` 範圍內的值。第一個間隔的名稱是來源欄位中的最小值（適用於遞增值來源）。

下列範例請求會根據寬度分別為 `1` 和 `50` 的桶，傳回 OpenSearch Dashboards 範例電子商務資料中數量與基本單價的前 `6` 個複合桶：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "quantity": { "histogram": { "field": "products.quantity", "interval": 1 }}},
          { "unit_price": { "histogram": { "field": "products.base_unit_price", "interval": 50 }}}
        ],
        "size": 6
      }
    }
  }
}
```
{% include copy-curl.html %}

彙總會傳回兩個 `histogram` 來源的前 `6` 個桶鍵和文件計數。與 `terms` 範例相同，桶會在來源欄位之間與之內排序。不過，在此情況下，排序為數值順序，並以每個直方圖寬度的包含下限為依據：

```json
{
  "took": 11,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "quantity": 2,
        "unit_price": 150
      },
      "buckets": [
        {
          "key": {
            "quantity": 1,
            "unit_price": 0
          },
          "doc_count": 17691
        },
        {
          "key": {
            "quantity": 1,
            "unit_price": 50
          },
          "doc_count": 5014
        },
        {
          "key": {
            "quantity": 1,
            "unit_price": 100
          },
          "doc_count": 482
        },
        {
          "key": {
            "quantity": 1,
            "unit_price": 150
          },
          "doc_count": 148
        },
        {
          "key": {
            "quantity": 1,
            "unit_price": 200
          },
          "doc_count": 32
        },
        {
          "key": {
            "quantity": 2,
            "unit_price": 150
          },
          "doc_count": 4
        }
      ]
    }
  }
}
```

每個欄位的桶鍵是該欄位間隔的下限。例如，第一個 `composite` 桶的 `unit_price` 鍵為 `0`。

若要擷取接下來的 `6` 個桶，請如下所示，在 `after` 參數中提供回應中的 `after_key` 物件：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "quantity": { "histogram": { "field": "products.quantity", "interval": 1 }}},
          { "unit_price": { "histogram": { "field": "products.base_unit_price", "interval": 50 }}}
        ],
        "size": 6,
        "after": {
            "quantity": 2,
            "unit_price": 150
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

只剩下兩個桶：

```json
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "quantity": 2,
        "unit_price": 500
      },
      "buckets": [
        {
          "key": {
            "quantity": 2,
            "unit_price": 200
          },
          "doc_count": 8
        },
        {
          "key": {
            "quantity": 2,
            "unit_price": 500
          },
          "doc_count": 4
        }
      ]
    }
  }
}
```

## 日期直方圖

若要建立日期範圍的複合彙總，請使用 `date_histogram` 彙總。如需詳細資訊，請參閱[日期直方圖彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)。

OpenSearch 會將日期（包括 `date_interval` 桶 (bucket) 鍵）表示為 `long` 整數，代表自 [Unix 時間](https://en.wikipedia.org/wiki/Unix_time)紀元起算的毫秒數。您可以使用 `format` 參數格式化日期輸出。這不會變更鍵的順序。

OpenSearch 以 UTC 儲存日期時間。您可以使用 `time_zone` 參數，以不同的時區顯示輸出結果。

以下範例請求會根據分別為 1 年和 1 天的桶寬度，傳回 OpenSearch Dashboards 範例電子商務資料中，每個已售出產品的建立年份及其售出日期的前 `4` 個複合桶：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "product_creation_date": { "date_histogram": { "field": "products.created_on", "calendar_interval": "1y", "format": "yyyy" }}},
          { "order_date": { "date_histogram": { "field": "order_date", "calendar_interval": "1d", "format": "yyyy-MM-dd" }}}
        ],
        "size": 4
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會傳回已格式化的日期型桶鍵及計數。對於 `date_interval` 複合彙總，欄位會依日期排序：

```json
{
  "took": 21,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "product_creation_date": "2016",
        "order_date": "2025-02-23"
      },
      "buckets": [
        {
          "key": {
            "product_creation_date": "2016",
            "order_date": "2025-02-20"
          },
          "doc_count": 146
        },
        {
          "key": {
            "product_creation_date": "2016",
            "order_date": "2025-02-21"
          },
          "doc_count": 153
        },
        {
          "key": {
            "product_creation_date": "2016",
            "order_date": "2025-02-22"
          },
          "doc_count": 143
        },
        {
          "key": {
            "product_creation_date": "2016",
            "order_date": "2025-02-23"
          },
          "doc_count": 140
        }
      ]
    }
  }
}
```

## Geotile 網格

使用 `geotile_grid` 來源，將 `geo_point` 值彙總至代表地圖圖磚的桶中。與其他複合彙總來源一樣，結果預設只包含含有資料的桶。如需詳細資訊，請參閱 [Geotile 網格彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/geotile-grid/)。

每個儲存格對應一個[地圖圖磚](https://en.wikipedia.org/wiki/Tiled_web_map)。儲存格標籤使用 `{zoom}/{x}/{y}` 格式。

以下範例請求會以 `8` 的精確度，傳回包含 `geoip.location` 欄位中位置的前 `6` 個圖磚：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "tile": { "geotile_grid": { "field": "geoip.location", "precision": 8 } } }
        ],
        "size": 6
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會傳回指定的 `geo_tiles` 及點計數：

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "tile": "8/122/104"
      },
      "buckets": [
        {
          "key": {
            "tile": "8/43/102"
          },
          "doc_count": 310
        },
        {
          "key": {
            "tile": "8/75/96"
          },
          "doc_count": 896
        },
        {
          "key": {
            "tile": "8/75/124"
          },
          "doc_count": 178
        },
        {
          "key": {
            "tile": "8/122/104"
          },
          "doc_count": 408
        }
      ]
    }
  }
}
```

## 結合來源

您可以結合兩個或多個任意不同類型的來源。

以下範例請求會傳回由三種不同來源類型組成的桶：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "order_date": { "date_histogram": { "field": "order_date", "calendar_interval": "1M", "format": "yyyy-MM" }}},
          { "gender": { "terms": { "field": "customer_gender" }}},          
          { "unit_price": { "histogram": { "field": "products.base_unit_price", "interval": 200 }}}
        ],
        "size": 10
      }
    }
  }
}
```

此彙總會傳回混合類型的 `composite` 桶及文件計數：

```json
{
  "took": 11,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "order_date": "2025-03",
        "gender": "MALE",
        "unit_price": 200
      },
      "buckets": [
        {
          "key": {
            "order_date": "2025-02",
            "gender": "FEMALE",
            "unit_price": 0
          },
          "doc_count": 1517
        },
        {
          "key": {
            "order_date": "2025-02",
            "gender": "MALE",
            "unit_price": 0
          },
          "doc_count": 1369
        },
        {
          "key": {
            "order_date": "2025-02",
            "gender": "MALE",
            "unit_price": 200
          },
          "doc_count": 6
        },
        {
          "key": {
            "order_date": "2025-02",
            "gender": "MALE",
            "unit_price": 400
          },
          "doc_count": 1
        },
        {
          "key": {
            "order_date": "2025-03",
            "gender": "FEMALE",
            "unit_price": 0
          },
          "doc_count": 3656
        },
        {
          "key": {
            "order_date": "2025-03",
            "gender": "FEMALE",
            "unit_price": 200
          },
          "doc_count": 1
        },
        {
          "key": {
            "order_date": "2025-03",
            "gender": "MALE",
            "unit_price": 0
          },
          "doc_count": 3530
        },
        {
          "key": {
            "order_date": "2025-03",
            "gender": "MALE",
            "unit_price": 200
          },
          "doc_count": 7
        }
      ]
    }
  }
}
```

## 子彙總

複合彙總與子彙總結合使用時最為實用，子彙總可揭示 `composite` 桶中文件的相關資訊。

以下範例請求會比較 OpenSearch Dashboards 範例電子商務資料中，一週內每一天依性別區分的平均消費金額：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "composite_buckets": {
      "composite": {
        "sources": [
          { "weekday": { "terms": { "field": "day_of_week" }}},
          { "gender": { "terms": { "field": "customer_gender" }}}          
        ],
        "size": 6
      },
      "aggs": {
        "avg_spend": {
          "avg": { "field": "taxful_total_price" }
        }
      }
    }
  }
}
```

此彙總會傳回前 `6` 個桶的平均 `taxful_total_price`：

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
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "composite_buckets": {
      "after_key": {
        "weekday": "Saturday",
        "gender": "MALE"
      },
      "buckets": [
        {
          "key": {
            "weekday": "Friday",
            "gender": "FEMALE"
          },
          "doc_count": 399,
          "avg_spend": {
            "value": 71.7733395989975
          }
        },
        {
          "key": {
            "weekday": "Friday",
            "gender": "MALE"
          },
          "doc_count": 371,
          "avg_spend": {
            "value": 79.72514108827494
          }
        },
        {
          "key": {
            "weekday": "Monday",
            "gender": "FEMALE"
          },
          "doc_count": 320,
          "avg_spend": {
            "value": 72.1588623046875
          }
        },
        {
          "key": {
            "weekday": "Monday",
            "gender": "MALE"
          },
          "doc_count": 259,
          "avg_spend": {
            "value": 86.1754946911197
          }
        },
        {
          "key": {
            "weekday": "Saturday",
            "gender": "FEMALE"
          },
          "doc_count": 365,
          "avg_spend": {
            "value": 73.53236301369863
          }
        },
        {
          "key": {
            "weekday": "Saturday",
            "gender": "MALE"
          },
          "doc_count": 371,
          "avg_spend": {
            "value": 72.78092360175202
          }
        }
      ]
    }
  }
}
```

## 將複合結果分頁

如果請求產生超過 `size` 個桶 (bucket)，則會傳回 `size` 個桶。在此情況下，結果會包含一個 `after_key` 物件，其中含有清單中下一個桶的鍵。若要擷取請求的下 `size` 個桶，請再次傳送請求，並在 `after` 參數中提供 `after_key`。如需範例，請參閱[直方圖](#histogram)中的請求。

若要繼續分頁回應，請一律使用 `after_key`，而不要複製最後一個桶。這兩者有時會不同。
{: .important}

## 使用索引排序提升效能

若要加快大型資料集上的複合彙總速度，您可以使用與彙總來源相同的欄位和順序來排序索引。當 `index.sort.field` 和 `index.sort.order` 與複合彙總中使用的來源欄位和順序相符時，OpenSearch 可以更有效率地傳回結果，並使用較少的記憶體。雖然索引排序會在編製索引期間增加少量額外負擔，但複合彙總的查詢效能提升相當顯著。

下列範例請求會為 `my-sorted-index` 索引中的每個欄位設定排序欄位和排序順序：

```json
PUT /my-sorted-index
{
  "settings": {
    "index": {
      "sort.field": ["customer_id", "timestamp"],
      "sort.order": ["asc", "desc"]
    }
  },
  "mappings": {
    "properties": {
      "customer_id": {
        "type": "keyword"
      },
      "timestamp": {
        "type": "date"
      },
      "price": {
        "type": "double"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列請求會在 `my-sorted-index` 索引上建立複合彙總。由於索引依 `customer_id` 遞增排序並依 `timestamp` 遞減排序，且彙總來源與該排序順序相符，因此此查詢的執行速度會更快，記憶體壓力也會降低：

```json
GET /my-sorted-index/_search
{
  "size": 0,
  "aggs": {
    "my_buckets": {
      "composite": {
        "size": 1000,
        "sources": [
          { "customer": { "terms": { "field": "customer_id", "order": "asc" } } },
          { "time": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d", "order": "desc" } } }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}