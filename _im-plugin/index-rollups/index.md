---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引彙整"
nav_order: 50
has_children: true
has_toc: false
redirect_from: 
  - /im-plugin/index-rollups/
---

# 索引彙整

未壓縮的時間序列資料最終會增加儲存成本、拖累叢集健康狀態，並減慢彙總速度。_索引彙整_ (index rollup) 透過定期將舊資料壓縮為粒度較低的摘要索引，來緩解這些影響。

您可以挑選感興趣的欄位，並使用索引彙整建立一個僅包含這些欄位的新索引，將資料彙總到較粗的時間桶中。您可以用極低的成本儲存數月或數年的歷史資料，同時維持相同的查詢效能。

例如，假設您每五秒收集一次 CPU 消耗資料，並儲存在熱節點上。與其將較舊的資料移至唯讀的溫節點，您可以逐步壓縮這些資料，每週將其間隔縮減 10%。或者，您也可以只儲存每天的 CPU 平均消耗量。

您可以透過三種方式使用索引彙整：

1. 使用 Index Rollup API 執行隨選索引彙整作業，作用於未主動匯入資料的索引，例如已輪替的索引。例如，您可以執行索引彙整作業，將以 5 分鐘間隔收集的資料彙總為每週平均值，以進行趨勢分析。
2. 使用 OpenSearch Dashboards UI 建立依定義排程執行的索引彙整作業。您也可以設定該作業，在索引匯入資料時即進行彙整。例如，您可以持續將 Logstash 索引從五秒間隔彙整為一小時間隔。
3. 將索引彙整作業指定為 ISM 動作，作為完整索引管理的一部分。這可讓您在事件發生後觸發彙整，例如輪替、索引達到一定時間、索引變為唯讀等。您也可以讓輪替與索引彙整作業依序執行：輪替先將目前索引移至溫節點，然後索引彙整作業在熱節點上建立一個包含精簡資料的新索引。

## 設定彙整作業

彙整作業會從來源索引讀取資料，並將摘要文件寫入目標索引。來源索引不會變更，且作業建立後無法變更任一索引的選擇。

作業會依時間戳記欄位彙總來源文件，使用固定間隔 (每個桶長度相同) 或日曆間隔 (遵循日曆單位，例如月份，長度可能不相等)。您可以依其他欄位分組---任何欄位類型可用 terms 彙總，數值欄位可用 histogram 彙總---並為數值欄位儲存 `avg`、`sum`、`max`、`min`、`value_count` 和 `cardinality` 指標。

請謹慎選擇分組欄位。粒度過高的欄位所產生的彙整文件數量幾乎與來源文件一樣多，節省的空間有限。欄位的順序也很重要：先依桶數最少的欄位分組。例如，對於依城市劃分的人口統計資料集，應先依城市分組，並將人口統計資料儲存為指標。

作業會依固定間隔或您以 [cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions) 定義的排程執行，每次執行會處理一定數量的頁面，以在執行時間與記憶體之間取得平衡。請加入執行延遲，讓匯入作業有時間完成：延遲 10 分鐘時，彙整下午 1 點至 2 點這一小時的執行會在下午 2:10 開始。將作業標記為連續，即可在資料匯入時即進行彙整，而非一次性處理。

若要建立作業，請使用 [Index rollups API]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/rollup-api/) 或[建立彙整作業](#creating-a-rollup-job)中的步驟。

## 搜尋目標索引

使用 `_search` API 搜尋目標索引。查詢必須符合目標索引的限制。對未分組欄位執行 terms 彙總，或對未儲存的指標執行彙總，都會被拒絕並傳回 `400`。

在彙整索引上，巢狀於 `date_histogram` 之下的 `avg` 子彙總會傳回帶有 `script_exception` 的 `400`。請改用 `sum` 和 `value_count` 並將兩者相除，或將 `avg` 巢狀於 `terms` 彙總之下。
{: .note}

您無法存取目標索引中文件的內部結構。OpenSearch 會改寫查詢以符合目標索引，讓您可以對來源索引與目標索引使用相同的查詢。

若要查詢目標索引，請將 `size` 設為 0：

```json
GET {target_index}/_search
{
  "size": 0,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "avg_cpu": {
      "avg": {
        "field": "cpu_usage"
      }
    }
  }
}
```

請考慮以下情境：您以每小時間隔收集下午 1 點至 9 點的彙整資料，並以每分鐘間隔收集下午 7 點至 11 點的即時資料。如果您在同一個查詢中對這些資料執行彙總，則下午 7 點至 9 點會同時出現彙整資料與即時資料的重疊，因為它們在彙總中被重複計算。

## Cardinality 指標
**3.5 版新增**
{: .label .label-purple }

cardinality 指標使用 HyperLogLog++ (HLL++) 演算法，以節省記憶體的方式追蹤彙整資料中的唯一值計數。這非常適合使用者 ID、IP 位址或工作階段 ID 等高基數欄位，因為儲存所有唯一值的成本會高得驚人。

### 組態

在彙整作業中定義 cardinality 指標時，您可以指定以下參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `precision_threshold` | 整數 | 控制精確度與記憶體用量之間的取捨。數值越高精確度越高，但使用更多記憶體。請使用 100 到 40,000 之間的值；超出該範圍的值會被接受而不會報錯，但不受支援。預設值為 3,000。|

您可以在 `cardinality` 物件中指定 `precision_threshold` 參數，如下所示：

```json
{
  "metrics": [
    {
      "source_field": "user_id",
      "metrics": [
        {
          "cardinality": {
            "precision_threshold": 10000
          }
        }
      ]
    }
  ]
}
```

### 查詢 cardinality 指標

您可以用與來源索引相同的方式查詢彙整索引上的 cardinality 指標：

```json
GET {rollup_index}/_search
{
  "size": 0,
  "aggs": {
    "unique_users": {
      "cardinality": {
        "field": "user_id"
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢彙整索引時，查詢中指定的任何 `precision_threshold` 都會被忽略。系統一律使用建立彙整作業時設定的精確度門檻，以確保與已儲存的 HLL 概略資料一致。
{: .important }

### 範例：追蹤不重複訪客

此範例建立一個彙整作業，追蹤每小時的不重複訪客數量。首先建立來源索引：

```json
PUT web_logs
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "visitor_id": { "type": "keyword" },
      "page_views": { "type": "integer" }
    }
  }
}
```
{% include copy-curl.html %}

接著建立彙整作業：

```json
PUT _plugins/_rollup/jobs/visitor_rollup
{
  "rollup": {
    "description": "Unique visitors per hour",
    "enabled": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Hours"
      }
    },
    "source_index": "web_logs",
    "target_index": "web_logs_hourly",
    "page_size": 1000,
    "dimensions": [
      {
        "date_histogram": {
          "source_field": "timestamp",
          "fixed_interval": "1h"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "visitor_id",
        "metrics": [
          {
            "cardinality": {
              "precision_threshold": 10000
            }
          }
        ]
      },
      {
        "source_field": "page_views",
        "metrics": [
          {
            "sum": {}
          }
        ]
      }
    ]
  }
}
```
{% include copy-curl.html %}

彙整作業會在第一次執行時建立其目標索引，這會在設定的間隔經過後發生。在此之前，搜尋目標索引會傳回 `index_not_found_exception`。若要檢查作業是否已執行，請傳送 `GET _plugins/_rollup/jobs/visitor_rollup/_explain`：若 `rollup_metadata` 為 `null`，表示作業尚未執行。
{: .note}

查詢彙整索引：

```json
GET web_logs_hourly/_search
{
  "size": 0,
  "aggs": {
    "hourly_stats": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h"
      },
      "aggs": {
        "unique_visitors": {
          "cardinality": {
            "field": "visitor_id"
          }
        },
        "total_page_views": {
          "sum": {
            "field": "page_views"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 多層級彙整
**於 3.5 版推出**
{: .label .label-purple }

多層級彙整可讓您建立彙整的彙整 (rollup-of-rollup) 作業，隨著時間逐步降低資料精細度。這對於長期資料保留策略很有用，您可以保留近期期間的細粒度資料，並為較舊期間保留越來越粗略的資料。

使用多層級彙整，您可以建立彙整作業的階層：

```
Raw Data (5-second intervals)
    ↓ Tier 1 Rollup
Hourly Rollup (1-hour intervals)
    ↓ Tier 2 Rollup
Daily Rollup (1-day intervals)
    ↓ Tier 3 Rollup
Weekly Rollup (1-week intervals)
```

每個層級都使用前一層級的彙整索引作為其來源，逐步降低儲存空間需求，同時維持查詢資料的能力。

### 先決條件

若要讓多層級彙整正確運作，您必須符合下列先決條件：

1. 所有層級都必須使用相同的維度欄位，且欄位名稱與類型必須相符。
2. 每個層級的間隔必須是前一層級間隔的倍數，例如 `5m` → `1h` → `1d`。
3. 如果使用[基數指標](#cardinality-metric)，所有層級都必須使用相同的 `precision_threshold` 值。
4. 第二個及後續層級的來源索引必須是前一層級所建立的彙整索引。
5. 來源層級必須至少完成一次彙整執行，您才能建立下一個層級。從空的彙整索引建立彙整作業會成功，但會產生非預期的結果。

### 範例：兩層級彙整策略

此範例示範物聯網 (IoT) 感應器資料的兩層級彙整。它由第 1 層級與第 2 層級組成：
- 兩個層級都使用相同的維度欄位：`timestamp`、`sensor_id`、`location`。
- 兩個層級都使用相同的指標欄位：`temperature` (`avg`/`max`/`min`)、`device_id` (`cardinality`)。
- 兩個層級的 cardinality `precision_threshold` 相同 (`10000`)。
- 第 2 層級使用 `sensor_data_hourly` (第 1 層級的輸出) 作為其來源。

建立來源索引並在其中新增一些文件：

```json
PUT sensor_data
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "sensor_id": { "type": "keyword" },
      "location": { "type": "keyword" },
      "device_id": { "type": "keyword" },
      "temperature": { "type": "double" }
    }
  }
}
```
{% include copy-curl.html %}

```json
POST _bulk?refresh=true
{ "index": { "_index": "sensor_data" } }
{ "timestamp": "2026-01-05T08:15:00", "sensor_id": "s1", "location": "warehouse", "device_id": "d1", "temperature": 21.4 }
{ "index": { "_index": "sensor_data" } }
{ "timestamp": "2026-01-05T08:45:00", "sensor_id": "s1", "location": "warehouse", "device_id": "d1", "temperature": 22.1 }
{ "index": { "_index": "sensor_data" } }
{ "timestamp": "2026-01-05T09:10:00", "sensor_id": "s2", "location": "cold-store", "device_id": "d2", "temperature": 4.8 }
{ "index": { "_index": "sensor_data" } }
{ "timestamp": "2026-01-05T10:05:00", "sensor_id": "s2", "location": "cold-store", "device_id": "d2", "temperature": 5.2 }
```
{% include copy-curl.html %}

**第 1 層級：原始資料 → 每小時彙整**

```json
PUT _plugins/_rollup/jobs/sensors_hourly
{
  "rollup": {
    "description": "Hourly rollup of raw sensor data",
    "enabled": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Hours"
      }
    },
    "source_index": "sensor_data",
    "target_index": "sensor_data_hourly",
    "page_size": 1000,
    "dimensions": [
      {
        "date_histogram": {
          "source_field": "timestamp",
          "fixed_interval": "1h"
        }
      },
      {
        "terms": {
          "source_field": "sensor_id"
        }
      },
      {
        "terms": {
          "source_field": "location"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "temperature",
        "metrics": [
          {"avg": {}},
          {"max": {}},
          {"min": {}}
        ]
      },
      {
        "source_field": "device_id",
        "metrics": [
          {
            "cardinality": {
              "precision_threshold": 10000
            }
          }
        ]
      }
    ]
  }
}
```
{% include copy-curl.html %}

**第 2 層級：每小時彙整 → 每日彙整**

```json
PUT _plugins/_rollup/jobs/sensors_daily
{
  "rollup": {
    "description": "Daily rollup of hourly sensor data",
    "enabled": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Days"
      }
    },
    "source_index": "sensor_data_hourly",
    "target_index": "sensor_data_daily",
    "page_size": 1000,
    "dimensions": [
      {
        "date_histogram": {
          "source_field": "timestamp",
          "fixed_interval": "1d"
        }
      },
      {
        "terms": {
          "source_field": "sensor_id"
        }
      },
      {
        "terms": {
          "source_field": "location"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "temperature",
        "metrics": [
          {"avg": {}},
          {"max": {}},
          {"min": {}}
        ]
      },
      {
        "source_field": "device_id",
        "metrics": [
          {
            "cardinality": {
              "precision_threshold": 10000
            }
          }
        ]
      }
    ]
  }
}
```
{% include copy-curl.html %}

每個層級都依自己的間隔執行，因此 `sensor_data_hourly` 會在第一次每小時執行後出現，而 `sensor_data_daily` 會在第一次每日執行後出現。
{: .note}

### 查詢多層級彙整

您可以個別查詢任一層級，或跨多個層級搜尋。

**查詢特定層級**：

```json
GET sensor_data_daily/_search
{
  "size": 0,
  "aggs": {
    "daily_avg_temp": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1d"
      },
      "aggs": {
        "max_temperature": {
          "max": {
            "field": "temperature"
          }
        },
        "unique_devices": {
          "cardinality": {
            "field": "device_id"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

**跨多個層級查詢** (使用索引模式)：

```json
GET sensor_data_hourly,sensor_data_daily/_search
{
  "size": 0,
  "aggs": {
    "temperature_stats": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1d"
      },
      "aggs": {
        "max_temp": {
          "max": {
            "field": "temperature"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例逐步解說

此逐步解說使用 OpenSearch Dashboards 的範例電子商務資料。若要新增，請前往 OpenSearch Dashboards 首頁，選取 **Try our sample data**，然後在 **Sample eCommerce orders** 中選取 **Add data**。

然後執行搜尋：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
```

#### 範例回應

```json
{
  "took": 23,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "opensearch_dashboards_sample_data_ecommerce",
        "_id": "jlMlwXcBQVLeQPrkC_kQ",
        "_score": 1,
        "_source": {
          "category": [
            "Women's Clothing",
            "Women's Accessories"
          ],
          "currency": "EUR",
          "customer_first_name": "Selena",
          "customer_full_name": "Selena Mullins",
          "customer_gender": "FEMALE",
          "customer_id": 42,
          "customer_last_name": "Mullins",
          "customer_phone": "",
          "day_of_week": "Saturday",
          "day_of_week_i": 5,
          "email": "selena@mullins-family.zzz",
          "manufacturer": [
            "Tigress Enterprises"
          ],
          "order_date": "2021-02-27T03:56:10+00:00",
          "order_id": 581553,
          "products": [
            {
              "base_price": 24.99,
              "discount_percentage": 0,
              "quantity": 1,
              "manufacturer": "Tigress Enterprises",
              "tax_amount": 0,
              "product_id": 19240,
              "category": "Women's Clothing",
              "sku": "ZO0064500645",
              "taxless_price": 24.99,
              "unit_discount_amount": 0,
              "min_price": 12.99,
              "_id": "sold_product_581553_19240",
              "discount_amount": 0,
              "created_on": "2016-12-24T03:56:10+00:00",
              "product_name": "Blouse - port royal",
              "price": 24.99,
              "taxful_price": 24.99,
              "base_unit_price": 24.99
            },
            {
              "base_price": 10.99,
              "discount_percentage": 0,
              "quantity": 1,
              "manufacturer": "Tigress Enterprises",
              "tax_amount": 0,
              "product_id": 17221,
              "category": "Women's Accessories",
              "sku": "ZO0085200852",
              "taxless_price": 10.99,
              "unit_discount_amount": 0,
              "min_price": 5.06,
              "_id": "sold_product_581553_17221",
              "discount_amount": 0,
              "created_on": "2016-12-24T03:56:10+00:00",
              "product_name": "Snood - rose",
              "price": 10.99,
              "taxful_price": 10.99,
              "base_unit_price": 10.99
            }
          ],
          "sku": [
            "ZO0064500645",
            "ZO0085200852"
          ],
          "taxful_total_price": 35.98,
          "taxless_total_price": 35.98,
          "total_quantity": 2,
          "total_unique_products": 2,
          "type": "order",
          "user": "selena",
          "geoip": {
            "country_iso_code": "MA",
            "location": {
              "lon": -8,
              "lat": 31.6
            },
            "region_name": "Marrakech-Tensift-Al Haouz",
            "continent_name": "Africa",
            "city_name": "Marrakesh"
          },
          "event": {
            "dataset": "sample_ecommerce"
          }
        }
      }
    ]
  }
}
...
```

建立索引彙整作業。
此範例挑選 `order_date`、`customer_gender`、`geoip.city_name`、`geoip.region_name` 及 `day_of_week` 欄位，並將它們彙整至 `example_rollup` 目標索引：

```json
PUT _plugins/_rollup/jobs/example
{
  "rollup": {
    "enabled": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Minutes",
        "start_time": 1602100553
      }
    },
    "last_updated_time": 1602100553,
    "description": "An example policy that rolls up the sample ecommerce data",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "target_index": "example_rollup",
    "page_size": 1000,
    "delay": 0,
    "continuous": false,
    "dimensions": [
      {
        "date_histogram": {
          "source_field": "order_date",
          "fixed_interval": "60m",
          "timezone": "America/Los_Angeles"
        }
      },
      {
        "terms": {
          "source_field": "customer_gender"
        }
      },
      {
        "terms": {
          "source_field": "geoip.city_name"
        }
      },
      {
        "terms": {
          "source_field": "geoip.region_name"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "taxless_total_price",
        "metrics": [
          {
            "avg": {}
          },
          {
            "sum": {}
          },
          {
            "max": {}
          },
          {
            "min": {}
          },
          {
            "value_count": {}
          }
        ]
      },
      {
        "source_field": "total_quantity",
        "metrics": [
          {
            "avg": {}
          },
          {
            "max": {}
          }
        ]
      }
    ]
  }
}
```

您可以查詢 `example_rollup` 索引，取得彙整作業中所設定欄位的詞彙彙總。
您會得到與查詢原始 `opensearch_dashboards_sample_data_ecommerce` 來源索引相同的回應：

```json
POST example_rollup/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": {"term": { "geoip.region_name": "California" } }
    }
  },
  "aggregations": {
    "daily_numbers": {
      "terms": {
        "field": "day_of_week"
      },
      "aggs": {
        "per_city": {
          "terms": {
            "field": "geoip.city_name"
          },
          "aggregations": {
            "average quantity": {
               "avg": {
                  "field": "total_quantity"
                }
              }
            }
          },
          "total_revenue": {
            "sum": {
              "field": "taxless_total_price"
          }
        }
      }
    }
  }
}
```

#### 回應範例

```json
{
  "took" : 14,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 281,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "daily_numbers" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "Friday",
          "doc_count" : 59,
          "total_revenue" : {
            "value" : 4858.84375
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 59,
                "average quantity" : {
                  "value" : 2.305084745762712
                }
              }
            ]
          }
        },
        {
          "key" : "Saturday",
          "doc_count" : 46,
          "total_revenue" : {
            "value" : 3547.203125
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 46,
                "average quantity" : {
                  "value" : 2.260869565217391
                }
              }
            ]
          }
        },
        {
          "key" : "Tuesday",
          "doc_count" : 45,
          "total_revenue" : {
            "value" : 3983.28125
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 45,
                "average quantity" : {
                  "value" : 2.2888888888888888
                }
              }
            ]
          }
        },
        {
          "key" : "Sunday",
          "doc_count" : 44,
          "total_revenue" : {
            "value" : 3308.1640625
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 44,
                "average quantity" : {
                  "value" : 2.090909090909091
                }
              }
            ]
          }
        },
        {
          "key" : "Thursday",
          "doc_count" : 40,
          "total_revenue" : {
            "value" : 2876.125
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 40,
                "average quantity" : {
                  "value" : 2.3
                }
              }
            ]
          }
        },
        {
          "key" : "Monday",
          "doc_count" : 38,
          "total_revenue" : {
            "value" : 2673.453125
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 38,
                "average quantity" : {
                  "value" : 2.1578947368421053
                }
              }
            ]
          }
        },
        {
          "key" : "Wednesday",
          "doc_count" : 38,
          "total_revenue" : {
            "value" : 3202.453125
          },
          "per_city" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Los Angeles",
                "doc_count" : 38,
                "average quantity" : {
                  "value" : 2.236842105263158
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

## doc_count 欄位

桶彙總中的 `doc_count` 欄位包含每個桶中收集的文件數量。在計算桶的 `doc_count` 時，文件數量會加上每份摘要文件中預先彙總的文件數量。從彙整搜尋傳回的 `doc_count` 代表來源索引中符合條件的文件總數。無論您搜尋來源索引還是彙整目標索引，每個桶的文件計數都相同。

## 查詢字串查詢

若要利用 Query DSL 中較短且更容易撰寫的字串，您可以使用[查詢字串]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/query-string/)來簡化彙整索引中的搜尋查詢。若要使用查詢字串，請在彙整搜尋請求中加入以下欄位：

```json
"query": {
  "query_string": {
    "query": "field_name:field_value"
  }
}
```
{% include copy.html %}

您只能查詢彙整作業已編製索引為維度的欄位。以下範例使用帶有 `*` 萬用字元運算子的查詢字串，在 `sensor_data_hourly` 彙整索引中搜尋其中兩個 `location` 維度值：

```json
GET sensor_data_hourly/_search
{
  "size": 0,
  "query": {
    "query_string": {
      "query": "warehouse OR cold*",
      "default_field": "location"
    }
  },
  "aggs": {
    "by_location": {
      "terms": {
        "field": "location"
      },
      "aggs": {
        "by_sensor": {
          "terms": {
            "field": "sensor_id"
          },
          "aggs": {
            "average temperature": {
              "avg": {
                "field": "temperature"
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中每個符合條件的位置各有一個桶：

```json
{
  "took": 52,
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
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "by_location": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "cold-store",
          "doc_count": 2,
          "by_sensor": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
              {
                "key": "s2",
                "doc_count": 2,
                "average temperature": {
                  "value": 5.0
                }
              }
            ]
          }
        },
        {
          "key": "warehouse",
          "doc_count": 2,
          "by_sensor": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
              {
                "key": "s1",
                "doc_count": 2,
                "average temperature": {
                  "value": 21.75
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

如需查詢字串查詢參數的詳細資訊，請參閱[查詢字串查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/query-string/#parameters)。

## 動態目標索引

<style>
.nobr { white-space: nowrap }
</style>

在 ISM 彙整中，`target_index` 欄位可以包含一個範本，該範本會在每次彙整編製索引時編譯。例如，如果您將 `target_index` 欄位指定為 <span style="white-space: nowrap">`{% raw %}rollup_ndx-{{ctx.source_index}}{% endraw %}`,</span>，則來源索引 `log-000001` 會彙整至目標索引 `rollup_ndx-log-000001`。這可讓您將資料彙整至多個以時間為基礎的索引，並為每個來源索引建立一個彙整作業。

{% raw %}`{{ctx.source_index}}`{% endraw %} 中的 `source_index` 參數不能包含萬用字元。
{: .note}

## 搜尋多個彙整索引

當資料彙整至多個目標索引時，您可以對所有彙整索引執行一次搜尋。若要搜尋具有相同彙整的多個目標索引，請將索引名稱指定為以逗號分隔的清單或萬用字元模式。例如，若 `target_index` 為 <span style="white-space: nowrap">`{% raw %}rollup_ndx-{{ctx.source_index}}{% endraw %}`</span>，且來源索引開頭為 `log`，請指定 `rollup_ndx-log*` 模式。或者，若要搜尋已彙整的 log-000001 和 log-000002 索引，請指定 `rollup_ndx-log-000001,rollup_ndx-log-000002` 清單。

請勿使用相同的查詢同時搜尋彙整與非彙整索引的混合。請求會傳回 `200`，但彙整索引會失敗並產生分片失敗，因此結果只會包含非彙整資料。
{: .warning}

## 範例

下列範例示範 `doc_count` 欄位、動態索引名稱，以及使用相同彙整搜尋多個彙整索引。

**步驟 1：** 新增一個 ISM 索引範本，以管理別名為 `log` 之索引的輪替：

```json
PUT _index_template/ism_rollover
{
  "index_patterns": ["log*"],
  "template": {
   "settings": {
    "plugins.index_state_management.rollover_alias": "log"
   }
 }
}
```

**步驟 2：** 設定 ISM 輪替原則，以在將一份文件上傳至任何名稱開頭為 `log*` 的索引後輪替該索引，然後彙整個別的後端索引。目標索引名稱會透過在來源索引名稱前面加上字串 `rollup_ndx-`，從來源索引名稱動態產生。

```json
PUT _plugins/_ism/policies/rollover_policy 
{ 
  "policy": { 
    "description": "Example rollover policy.", 
    "default_state": "rollover", 
    "states": [ 
      { 
        "name": "rollover", 
        "actions": [ 
          { 
            "rollover": { 
              "min_doc_count": 1 
            } 
          } 
        ], 
        "transitions": [ 
          { 
            "state_name": "rp" 
          } 
        ] 
      }, 
      { 
        "name": "rp", 
        "actions": [
          { 
            "rollup": { 
              "ism_rollup": { 
                "target_index": {% raw %}"rollup_ndx-{{ctx.source_index}}"{% endraw %}, 
                "description": "Example rollup job", 
                "page_size": 200, 
                "dimensions": [ 
                  { 
                    "date_histogram": { 
                      "source_field": "ts", 
                      "fixed_interval": "60m", 
                      "timezone": "America/Los_Angeles" 
                    } 
                  }, 
                  { 
                    "terms": { 
                      "source_field": "message.keyword" 
                    } 
                  } 
                ], 
                "metrics": [ 
                  { 
                    "source_field": "msg_size", 
                    "metrics": [ 
                      { 
                        "sum": {} 
                      } 
                    ]
                  } 
                ]
              } 
            } 
          } 
        ], 
        "transitions": [] 
      } 
    ], 
    "ism_template": { 
      "index_patterns": ["log*"], 
      "priority": 100 
    } 
  } 
}
```

**步驟 3：** 建立名為 `log-000001` 的索引，並為其設定別名 `log`。

```json
PUT log-000001
{
  "aliases": {
    "log": {
      "is_write_index": true
    }
  }
}
```

**步驟 4：** 將四份文件編製索引至先前建立的索引。其中兩份文件的訊息為「Success」，另外兩份的訊息為「Error」。

```json
POST log/_doc?refresh=true 
{ 
  "ts" : "2022-08-26T09:28:48-04:00", 
  "message": "Success", 
  "msg_size": 10 
}
```

```json
POST log/_doc?refresh=true 
{ 
  "ts" : "2022-08-26T10:06:25-04:00", 
  "message": "Error", 
  "msg_size": 20 
}
```

```json
POST log/_doc?refresh=true 
{ 
  "ts" : "2022-08-26T10:23:54-04:00", 
  "message": "Error", 
  "msg_size": 30 
}
```

```json
POST log/_doc?refresh=true 
{ 
  "ts" : "2022-08-26T10:53:41-04:00", 
  "message": "Success", 
  "msg_size": 40 
}
```

在您將第一份文件編製索引後，輪替動作會執行並建立索引 `log-000002`，且將 `rollover_policy` 附加至該索引。接著彙整動作會執行並建立彙整索引 `rollup_ndx-log-000001`。

每個步驟都會等待下一次 ISM 作業執行，因此完整順序需要數個 ISM 週期才能完成——在預設 `job_interval` 為 5 分鐘的情況下約需 20 分鐘。若要追蹤其進度，請執行 `GET _plugins/_ism/explain` 並觀察狀態變化。
{: .tip}

**步驟 5：** 搜尋彙整索引。

```json
GET rollup_ndx-log-*/_search
{
  "size": 0,
  "query": {
    "match_all": {}
  },
  "aggregations": {
    "message_numbers": {
      "terms": {
        "field": "message.keyword"
      },
      "aggs": {
        "per_message": {
          "terms": {
            "field": "message.keyword"
          },
          "aggregations": {
            "sum_message": {
              "sum": {
                "field": "msg_size"
              }
            }
          }
        }
      }
    }
  }
}
```

回應包含兩個桶 (bucket)：「Error」和「Success」，且每個桶的文件計數為 2：

```json
{
  "took" : 30,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "message_numbers" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "Success",
          "doc_count" : 2,
          "per_message" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Success",
                "doc_count" : 2,
                "sum_message" : {
                  "value" : 50.0
                }
              }
            ]
          }
        },
        {
          "key" : "Error",
          "doc_count" : 2,
          "per_message" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets" : [
              {
                "key" : "Error",
                "doc_count" : 2,
                "sum_message" : {
                  "value" : 50.0
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

## 索引轉碼器注意事項

關於索引轉碼器注意事項，請參閱[索引轉碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#index-rollups-and-transforms)。

## OpenSearch Dashboards 中的索引彙整

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。選取 **Rollup jobs**，即可列出您叢集中的彙整作業及其狀態和下次執行時間。選取作業即可檢視其組態和執行結果。若要對作業執行動作，請選取作業旁的核取方塊，然後選取 **Enable**、**Disable** 或 **Actions > Delete**。

下圖顯示 **Rollup jobs** 頁面。

![Rollup jobs 頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/rollup-jobs-list.png)

彙整作業需要包含時間戳記欄位的來源索引。如果您的叢集沒有可供彙整的時間序列資料，請從 OpenSearch Dashboards 首頁新增電子商務範例資料，並依照[範例逐步操作](#sample-walkthrough)中的說明，彙整其 `order_date` 欄位。

### 建立彙整作業

1. 在 **Index Management** 中，選取 **Rollup jobs**，然後選取 **Create rollup job**。
1. 在 **Name** 中輸入作業名稱，並視需要輸入說明。
1. 在 **Source index** 中，選取要彙整的索引或索引模式。
1. 在 **Target index** 中，選取現有索引，或輸入新索引的名稱。名稱可以包含[嵌入變數](#dynamic-target-index)。
1. 選取 **Next**。
1. 在 **Time aggregation** 中，執行下列操作：

   1. 選取要用於彙總的 **Timestamp field**。
   1. 選取 **Interval type**。固定間隔的長度皆相同。日曆間隔依照月份等日曆單位劃分，長度可能不相等。
   1. 在 **Interval** 中，選取間隔長度。
   1. 在 **Timezone** 中，選取時間戳記的時區。

1. 視需要在 **Additional aggregation** 中，新增用於分組的欄位：

   1. 選取 **Add fields**，選取欄位名稱，然後選取 **Add**。
   1. 為每個欄位選取 **Aggregation method**。關鍵字欄位只能依詞彙彙總。
   1. 對於每個直方圖彙總，在 **Interval** 中輸入每個桶包含的時間戳記間隔數。
   1. 視需要重新排列欄位，將桶數最少的欄位排在前面。

1. 視需要在 **Additional metrics** 中，新增要儲存的指標：

   1. 選取 **Add fields**，選取數值欄位名稱，然後選取 **Add**。
   1. 為每個欄位選取要儲存的指標：**Min**、**Max**、**Sum**、**Avg**、**Value count** 或 **All**。若要儲存表格中每個欄位的所有指標，請選取 **Enable all**；若要清除這些選取項目，請選取 **Disable all**。

1. 選取 **Next**。
1. 在 **Schedule** 中，執行下列操作：

   1. 若要依排程執行作業，而非僅在原則呼叫時執行，請保持選取 **Enable job by default**。
   1. 若要在匯入資料時進行彙整，請在 **Continuous** 中選取 **Yes**。
   1. 在 **Rollup execution frequency** 中，選取 **Define by fixed interval** 並輸入 **Rollup interval**，或選取 **Define by cron expression** 並輸入 cron 運算式及時區。如需運算式語法，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。
   1. 在 **Page per execution** 中，輸入每次執行要處理的頁數。數值越大，執行速度越快，使用的記憶體也越多。
   1. 視需要在 **Execution delay** 中，輸入作業執行前等待匯入完成的時間。

1. 選取 **Next**，檢閱組態，然後選取 **Create**。

## 相關文件

- [索引彙整 API]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/rollup-api/)
- [索引彙整設定]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/settings/)
- [索引轉換]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/index/)
- [索引狀態管理]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
