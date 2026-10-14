---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "顯著詞彙"
parent: Bucket aggregations
nav_order: 180
redirect_from:
  - /query-dsl/aggregations/bucket/significant-terms/
---

# 顯著詞彙彙總

`significant_terms` 彙總會找出在文件子集（前景集）中，相較於較廣泛的參考集（背景集），出現頻率異常高的詞彙。根據預設，背景集涵蓋目標索引中的所有文件。您可以使用 `background_filter` 縮小背景集的範圍。當您需要擷取*代表性過高*的值，而僅顯示*最常見*值的一般 `terms` 彙總無法滿足需求時，請使用此彙總。

每個結果桶 (bucket) 包含：

- `key`：詞彙值。
- `doc_count`：包含該詞彙的前景文件數量。
- `bg_count`：包含該詞彙的背景文件數量。
- `score`：表示該詞彙在前景中相對於背景的突出程度。如需詳細資訊，請參閱[啟發式方法與評分](#heuristics-and-scoring)。

如果彙總未傳回任何桶，通常表示前景未經篩選（例如，您使用了 `match_all` 查詢），或前景中的詞彙分布與背景相同。
{: .note}

## 參數

`significant_terms` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要分析的欄位。請使用已編製索引的 `keyword`、整數或其他精確值欄位。只有在 `text` 欄位已啟用 `fielddata` 時才能使用該欄位，但不建議這麼做。不支援浮點數欄位。如需詳細資訊，請參閱[欄位類型考量](#field-type-considerations)和[限制](#limitations)。 |
| `size` | 選用 | 整數 | 要傳回的桶數量。預設值為 `10`。 |
| `shard_size` | 選用 | 整數 | 每個分片傳回的候選詞彙數量。根據預設，每個分片會傳回 `2 * (size * 1.5 + 10)` 個詞彙。如需詳細資訊，請參閱[大小與分片大小](#size-and-shard-size)。 |
| `min_doc_count` | 選用 | 整數 | 詞彙必須出現在至少多少個前景文件中才會被傳回。預設值為 `3`。 |
| `shard_min_doc_count` | 選用 | 整數 | 分片上必須有至少多少個前景文件包含某詞彙，該分片才會將其作為候選詞彙傳回。預設值為 `0`。 |
| `include` | 選用 | 字串或陣列 | 限制可建立桶的詞彙。接受規則運算式或精確值陣列。 |
| `exclude` | 選用 | 字串或陣列 | 防止詞彙建立桶。接受規則運算式或精確值陣列。 |
| `background_filter` | 選用 | 物件 | 用於限制背景集的查詢。預設為目標索引中的所有文件。如需詳細資訊，請參閱[使用背景篩選器縮小背景集範圍](#using-a-background-filter-to-narrow-the-background-set)。 |
| `execution_hint` | 選用 | 字串 | 控制詞彙的收集方式。有效值為 `map` 和 `global_ordinals`。OpenSearch 會自動選取最佳選項。如需詳細資訊，請參閱[執行提示](#execution-hint)。 |
| `jlh`、`mutual_information`、`chi_square`、`gnd`、`percentage` 或 `script_heuristic` | 選用 | 物件 | 用於為詞彙評分的顯著性啟發式方法。每個彙總只能指定一種啟發式方法。預設值為 `jlh`。如需詳細資訊，請參閱[啟發式方法與評分](#heuristics-and-scoring)。 |

## 基本範例：找出電子商務應用程式中高價退貨的特徵詞彙

建立包含客戶訂單的索引：

```json
PUT /retail_orders
{
  "mappings": {
    "properties": {
      "status":        { "type": "keyword" },
      "order_total":   { "type": "double" },
      "payment_method": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件匯入索引：

```json
POST _bulk?refresh
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 950, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 720, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 540, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 820, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 500, "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 130, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 75,  "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 260, "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 45,  "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 310, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 220, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 410, "payment_method":"paypal" }
```
{% include copy-curl.html %}

執行下列查詢，找出在已退貨且金額超過 $500 的訂單中，相較於整個索引異常常見的 `payment_method` 值：

```json
GET /retail_orders/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        { "term": { "status": "RETURNED" } },
        { "range": { "order_total": { "gte": 500 } } }
      ]
    }
  },
  "aggs": {
    "payment_signals": {
      "significant_terms": {
        "field": "payment_method"
      }
    }
  }
}
```
{% include copy-curl.html %}

傳回的彙總顯示，在五筆高價退貨中，`gift_card` 出現 3 次（60%），而在整個索引中則為 12 次中出現 3 次（25%）。因此，它被標記為代表性最高的付款方式：

```json
{
  ...
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "payment_signals": {
      "doc_count": 5,
      "bg_count": 12,
      "buckets": [
        {
          "key": "gift_card",
          "doc_count": 3,
          "score": 0.84,
          "bg_count": 3
        }
      ]
    }
  }
}
```

## 多集合分析

您可以先將文件分組到桶中，再於每個桶內執行 `significant_terms` 彙總，藉此找出每個類別的異常值。

### 範例：各區域的異常取消原因

下列範例使用包含已取消叫車請求的 `rides` 索引。建立索引：

```json
PUT rides
{
  "mappings": {
    "properties": {
      "region": {
        "type": "keyword"
      },
      "cancel_reason": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引，其中包含市中心 7 筆、機場 6 筆及郊區 4 筆已取消的行程：

```json
POST _bulk?refresh
{ "index": { "_index": "rides", "_id": "1" } }
{ "region": "airport", "cancel_reason": "could_not_find_rider" }
{ "index": { "_index": "rides", "_id": "2" } }
{ "region": "airport", "cancel_reason": "could_not_find_rider" }
{ "index": { "_index": "rides", "_id": "3" } }
{ "region": "airport", "cancel_reason": "could_not_find_rider" }
{ "index": { "_index": "rides", "_id": "4" } }
{ "region": "airport", "cancel_reason": "changed_plans" }
{ "index": { "_index": "rides", "_id": "5" } }
{ "region": "airport", "cancel_reason": "changed_plans" }
{ "index": { "_index": "rides", "_id": "6" } }
{ "region": "airport", "cancel_reason": "long_wait" }
{ "index": { "_index": "rides", "_id": "7" } }
{ "region": "downtown", "cancel_reason": "long_wait" }
{ "index": { "_index": "rides", "_id": "8" } }
{ "region": "downtown", "cancel_reason": "long_wait" }
{ "index": { "_index": "rides", "_id": "9" } }
{ "region": "downtown", "cancel_reason": "long_wait" }
{ "index": { "_index": "rides", "_id": "10" } }
{ "region": "downtown", "cancel_reason": "long_wait" }
{ "index": { "_index": "rides", "_id": "11" } }
{ "region": "downtown", "cancel_reason": "changed_plans" }
{ "index": { "_index": "rides", "_id": "12" } }
{ "region": "downtown", "cancel_reason": "changed_plans" }
{ "index": { "_index": "rides", "_id": "13" } }
{ "region": "downtown", "cancel_reason": "could_not_find_rider" }
{ "index": { "_index": "rides", "_id": "14" } }
{ "region": "suburbs", "cancel_reason": "driver_cancelled" }
{ "index": { "_index": "rides", "_id": "15" } }
{ "region": "suburbs", "cancel_reason": "driver_cancelled" }
{ "index": { "_index": "rides", "_id": "16" } }
{ "region": "suburbs", "cancel_reason": "driver_cancelled" }
{ "index": { "_index": "rides", "_id": "17" } }
{ "region": "suburbs", "cancel_reason": "changed_plans" }
```
{% include copy-curl.html %}

下列請求使用 `terms` 彙總依區域將行程分組，並在每個區域內執行 `significant_terms`，以找出在該區域中比例特別高的取消原因：

```json
GET rides/_search
{
  "size": 0,
  "aggs": {
    "by_region": {
      "terms": {
        "field": "region"
      },
      "aggs": {
        "odd_cancellations": {
          "significant_terms": {
            "field": "cancel_reason"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

每個區域都有各自代表性過高的原因：市中心的乘客等候時間過長、機場的乘客無法被司機找到，而郊區的司機則較常取消行程。郊區的行程數最少，但分數最高，因為其原因的代表性最高：`driver_cancelled` 占郊區 4 筆取消中的 3 筆，卻只占全部 17 筆取消中的 3 筆。在某區域中出現次數少於三筆的原因（例如市中心的 `could_not_find_rider`）不會被傳回，因為預設的 `min_doc_count` 為 `3`：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "aggregations": {
    "by_region": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "downtown",
          "doc_count": 7,
          "odd_cancellations": {
            "doc_count": 7,
            "bg_count": 17,
            "buckets": [
              {
                "key": "long_wait",
                "doc_count": 4,
                "score": 0.5387755102040814,
                "bg_count": 5
              }
            ]
          }
        },
        {
          "key": "airport",
          "doc_count": 6,
          "odd_cancellations": {
            "doc_count": 6,
            "bg_count": 17,
            "buckets": [
              {
                "key": "could_not_find_rider",
                "doc_count": 3,
                "score": 0.5625,
                "bg_count": 4
              }
            ]
          }
        },
        {
          "key": "suburbs",
          "doc_count": 4,
          "odd_cancellations": {
            "doc_count": 4,
            "bg_count": 17,
            "buckets": [
              {
                "key": "driver_cancelled",
                "doc_count": 3,
                "score": 2.4375,
                "bg_count": 3
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

### 範例：地圖上的熱點

您可以使用 `geotile_grid` 彙總將地圖劃分為縮放層級的圖磚，然後在每個圖磚內執行 `significant_terms` 彙總，以識別區域性的離群值。較高的 `precision` 會產生較小的圖磚，例如街道或城市街區；較低的 `precision` 則會產生較大的圖磚，例如城市或區域。

下列範例使用 `field_ops` 索引，其中包含三個城市各據點回報的現場事件。請建立該索引，並將 `site.location` 對應為 `geo_point`：

```json
PUT field_ops
{
  "mappings": {
    "properties": {
      "site": {
        "properties": {
          "name": {
            "type": "text"
          },
          "location": {
            "type": "geo_point"
          }
        }
      },
      "issue": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將下列事件編製索引。每個城市都會發生停電：

```json
POST _bulk?refresh
{ "index": { "_index": "field_ops", "_id": "1" } }
{ "site": { "name": "Seattle site 1", "location": { "lat": 47.61, "lon": -122.33 } }, "issue": "FIBER_CUT" }
{ "index": { "_index": "field_ops", "_id": "2" } }
{ "site": { "name": "Seattle site 2", "location": { "lat": 47.62, "lon": -122.34 } }, "issue": "FIBER_CUT" }
{ "index": { "_index": "field_ops", "_id": "3" } }
{ "site": { "name": "Seattle site 3", "location": { "lat": 47.63, "lon": -122.35 } }, "issue": "FIBER_CUT" }
{ "index": { "_index": "field_ops", "_id": "4" } }
{ "site": { "name": "Seattle site 4", "location": { "lat": 47.64, "lon": -122.36 } }, "issue": "POWER_OUTAGE" }
{ "index": { "_index": "field_ops", "_id": "5" } }
{ "site": { "name": "Seattle site 5", "location": { "lat": 47.65, "lon": -122.37 } }, "issue": "POWER_OUTAGE" }
{ "index": { "_index": "field_ops", "_id": "6" } }
{ "site": { "name": "Seattle site 6", "location": { "lat": 47.66, "lon": -122.38 } }, "issue": "VANDALISM" }
{ "index": { "_index": "field_ops", "_id": "7" } }
{ "site": { "name": "Denver site 1", "location": { "lat": 39.74, "lon": -104.99 } }, "issue": "VANDALISM" }
{ "index": { "_index": "field_ops", "_id": "8" } }
{ "site": { "name": "Denver site 2", "location": { "lat": 39.75, "lon": -105.0 } }, "issue": "VANDALISM" }
{ "index": { "_index": "field_ops", "_id": "9" } }
{ "site": { "name": "Denver site 3", "location": { "lat": 39.76, "lon": -105.01 } }, "issue": "VANDALISM" }
{ "index": { "_index": "field_ops", "_id": "10" } }
{ "site": { "name": "Denver site 4", "location": { "lat": 39.77, "lon": -105.02 } }, "issue": "POWER_OUTAGE" }
{ "index": { "_index": "field_ops", "_id": "11" } }
{ "site": { "name": "Denver site 5", "location": { "lat": 39.78, "lon": -105.03 } }, "issue": "EQUIPMENT_FAILURE" }
{ "index": { "_index": "field_ops", "_id": "12" } }
{ "site": { "name": "Phoenix site 1", "location": { "lat": 33.45, "lon": -112.07 } }, "issue": "EQUIPMENT_FAILURE" }
{ "index": { "_index": "field_ops", "_id": "13" } }
{ "site": { "name": "Phoenix site 2", "location": { "lat": 33.46, "lon": -112.08 } }, "issue": "EQUIPMENT_FAILURE" }
{ "index": { "_index": "field_ops", "_id": "14" } }
{ "site": { "name": "Phoenix site 3", "location": { "lat": 33.47, "lon": -112.09 } }, "issue": "EQUIPMENT_FAILURE" }
{ "index": { "_index": "field_ops", "_id": "15" } }
{ "site": { "name": "Phoenix site 4", "location": { "lat": 33.48, "lon": -112.1 } }, "issue": "POWER_OUTAGE" }
{ "index": { "_index": "field_ops", "_id": "16" } }
{ "site": { "name": "Phoenix site 5", "location": { "lat": 33.49, "lon": -112.11 } }, "issue": "POWER_OUTAGE" }
```
{% include copy-curl.html %}

下列請求將地點劃分為圖磚，並找出在每個圖磚中出現頻率異常高的 `issue` 值：

```json
GET field_ops/_search
{
  "size": 0,
  "aggs": {
    "tiles": {
      "geotile_grid": {
        "field": "site.location",
        "precision": 6
      },
      "aggs": {
        "odd_issues": {
          "significant_terms": {
            "field": "issue"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

每個城市都落在各自的圖磚中，且每個圖磚都有各自過度代表的問題：丹佛的破壞公物（圖磚 `6/13/24`）、鳳凰城的設備故障（圖磚 `6/12/25`），以及西雅圖的光纖中斷（圖磚 `6/10/22`）。停電在各地都很常見，因此不會被傳回：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "tiles": {
      "buckets": [
        {
          "key": "6/10/22",
          "doc_count": 6,
          "odd_issues": {
            "doc_count": 6,
            "bg_count": 16,
            "buckets": [
              {
                "key": "FIBER_CUT",
                "doc_count": 3,
                "score": 0.8333333333333333,
                "bg_count": 3
              }
            ]
          }
        },
        {
          "key": "6/13/24",
          "doc_count": 5,
          "odd_issues": {
            "doc_count": 5,
            "bg_count": 16,
            "buckets": [
              {
                "key": "VANDALISM",
                "doc_count": 3,
                "score": 0.84,
                "bg_count": 4
              }
            ]
          }
        },
        {
          "key": "6/12/25",
          "doc_count": 5,
          "odd_issues": {
            "doc_count": 5,
            "bg_count": 16,
            "buckets": [
              {
                "key": "EQUIPMENT_FAILURE",
                "doc_count": 3,
                "score": 0.84,
                "bg_count": 4
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

### 範例：顯著詞彙隨時間的變化

若要了解顯著詞彙如何隨時間變化，請使用 `date_histogram` 彙總作為父層。本範例與[背景篩選範例](#example-compare-toronto-to-the-rest-of-canada)使用 `news` 索引，其中包含 2025 年 10 月發布於加拿大與美國城市的文章主題。請建立該索引：

```json
PUT news
{
  "mappings": {
    "properties": {
      "city": {
        "type": "keyword"
      },
      "country": {
        "type": "keyword"
      },
      "topic": {
        "type": "keyword"
      },
      "publish_date": {
        "type": "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引。冰球是加拿大各地的常見主題，但不會出現在美國的文章中：

```json
POST _bulk?refresh
{ "index": { "_index": "news", "_id": "1" } }
{ "city": "Toronto", "country": "Canada", "topic": "transit", "publish_date": "2025-10-06" }
{ "index": { "_index": "news", "_id": "2" } }
{ "city": "Toronto", "country": "Canada", "topic": "transit", "publish_date": "2025-10-07" }
{ "index": { "_index": "news", "_id": "3" } }
{ "city": "Toronto", "country": "Canada", "topic": "transit", "publish_date": "2025-10-13" }
{ "index": { "_index": "news", "_id": "4" } }
{ "city": "Toronto", "country": "Canada", "topic": "transit", "publish_date": "2025-10-14" }
{ "index": { "_index": "news", "_id": "5" } }
{ "city": "Toronto", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-15" }
{ "index": { "_index": "news", "_id": "6" } }
{ "city": "Toronto", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-16" }
{ "index": { "_index": "news", "_id": "7" } }
{ "city": "Toronto", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-17" }
{ "index": { "_index": "news", "_id": "8" } }
{ "city": "Toronto", "country": "Canada", "topic": "weather", "publish_date": "2025-10-08" }
{ "index": { "_index": "news", "_id": "9" } }
{ "city": "Vancouver", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-13" }
{ "index": { "_index": "news", "_id": "10" } }
{ "city": "Montreal", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-14" }
{ "index": { "_index": "news", "_id": "11" } }
{ "city": "Calgary", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-15" }
{ "index": { "_index": "news", "_id": "12" } }
{ "city": "Vancouver", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-16" }
{ "index": { "_index": "news", "_id": "13" } }
{ "city": "Montreal", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-17" }
{ "index": { "_index": "news", "_id": "14" } }
{ "city": "Calgary", "country": "Canada", "topic": "hockey", "publish_date": "2025-10-13" }
{ "index": { "_index": "news", "_id": "15" } }
{ "city": "Vancouver", "country": "Canada", "topic": "weather", "publish_date": "2025-10-09" }
{ "index": { "_index": "news", "_id": "16" } }
{ "city": "Montreal", "country": "Canada", "topic": "weather", "publish_date": "2025-10-10" }
{ "index": { "_index": "news", "_id": "17" } }
{ "city": "Calgary", "country": "Canada", "topic": "weather", "publish_date": "2025-10-14" }
{ "index": { "_index": "news", "_id": "18" } }
{ "city": "Vancouver", "country": "Canada", "topic": "weather", "publish_date": "2025-10-15" }
{ "index": { "_index": "news", "_id": "19" } }
{ "city": "Montreal", "country": "Canada", "topic": "transit", "publish_date": "2025-10-20" }
{ "index": { "_index": "news", "_id": "20" } }
{ "city": "Calgary", "country": "Canada", "topic": "elections", "publish_date": "2025-10-06" }
{ "index": { "_index": "news", "_id": "21" } }
{ "city": "Chicago", "country": "United States", "topic": "elections", "publish_date": "2025-10-07" }
{ "index": { "_index": "news", "_id": "22" } }
{ "city": "Boston", "country": "United States", "topic": "elections", "publish_date": "2025-10-08" }
{ "index": { "_index": "news", "_id": "23" } }
{ "city": "Denver", "country": "United States", "topic": "elections", "publish_date": "2025-10-09" }
{ "index": { "_index": "news", "_id": "24" } }
{ "city": "Denver", "country": "United States", "topic": "baseball", "publish_date": "2025-10-24" }
{ "index": { "_index": "news", "_id": "25" } }
{ "city": "Chicago", "country": "United States", "topic": "baseball", "publish_date": "2025-10-20" }
{ "index": { "_index": "news", "_id": "26" } }
{ "city": "Boston", "country": "United States", "topic": "baseball", "publish_date": "2025-10-21" }
```
{% include copy-curl.html %}

下列請求將文章依週分組，並找出與整個月相比，在每週中異常常見的主題：

```json
GET news/_search
{
  "size": 0,
  "aggs": {
    "weeks": {
      "date_histogram": {
        "field": "publish_date",
        "calendar_interval": "week"
      },
      "aggs": {
        "trending_topics": {
          "significant_terms": {
            "field": "topic"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

每週都有自己的熱門主題：第一週是選舉，第二週是冰球，第三週是棒球。在第一週，`weather` 也會以較低的分數被傳回，因為它在該週比整個月稍微更常見：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "weeks": {
      "buckets": [
        {
          "key_as_string": "2025-10-06T00:00:00.000Z",
          "key": 1759708800000,
          "doc_count": 9,
          "trending_topics": {
            "doc_count": 9,
            "bg_count": 26,
            "buckets": [
              {
                "key": "elections",
                "doc_count": 4,
                "score": 0.8395061728395059,
                "bg_count": 4
              },
              {
                "key": "weather",
                "doc_count": 3,
                "score": 0.24444444444444438,
                "bg_count": 5
              }
            ]
          }
        },
        {
          "key_as_string": "2025-10-13T00:00:00.000Z",
          "key": 1760313600000,
          "doc_count": 13,
          "trending_topics": {
            "doc_count": 13,
            "bg_count": 26,
            "buckets": [
              {
                "key": "hockey",
                "doc_count": 9,
                "score": 0.6923076923076923,
                "bg_count": 9
              }
            ]
          }
        },
        {
          "key_as_string": "2025-10-20T00:00:00.000Z",
          "key": 1760918400000,
          "doc_count": 4,
          "trending_topics": {
            "doc_count": 4,
            "bg_count": 26,
            "buckets": [
              {
                "key": "baseball",
                "doc_count": 3,
                "score": 4.125,
                "bg_count": 3
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

## 使用背景篩選器縮小背景集合

根據預設，背景包含整個索引。使用 `background_filter` 限制背景文件，以獲得更精確的結果。

### 範例：比較多倫多與加拿大其他地區

下列範例使用[前一個範例](#example-significant-terms-over-time)中建立的 `news` 索引。

下列範例將前景篩選為來自多倫多的文章，並設定僅包含加拿大文章的 `background_filter`。`significant_terms` 彙總會突顯出相較於加拿大其他地區，在多倫多異常頻繁出現的主題：

```json
GET news/_search
{
  "size": 0,
  "query": {
    "term": {
      "city": "Toronto"
    }
  },
  "aggs": {
    "unusual_topics": {
      "significant_terms": {
        "field": "topic",
        "background_filter": {
          "term": {
            "country": "Canada"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

僅會傳回 `transit`。若沒有 `background_filter`，背景也會包含美國文章，而冰球從未出現在其中，因此 `hockey` 也會被傳回為對多倫多而言顯著。若使用加拿大背景，冰球在多倫多的常見程度不會高於加拿大其他地區：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "unusual_topics": {
      "doc_count": 8,
      "bg_count": 20,
      "buckets": [
        {
          "key": "transit",
          "doc_count": 4,
          "score": 0.5,
          "bg_count": 5
        }
      ]
    }
  }
}
```
</details>

使用自訂背景需要額外處理，因為每個候選詞元的背景頻率都必須套用篩選器來計算。這可能比使用預設的整個索引計數更慢。
{: .warning}

## 欄位類型考量

`significant_terms` 彙總最適合用於確切值欄位（例如 `keyword` 或 `numeric`）。不建議在 `text` 欄位上執行 `significant_terms` 彙總：這需要在該欄位上啟用 `fielddata`，並將每個唯一詞元載入記憶體，可能會使用大量記憶體。對於經過分析的文字，請使用[`significant_text` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-text/)，其專為全文欄位設計，並支援相同的顯著性啟發式方法。

## 啟發式方法與評分

`score` 會根據詞元的前景頻率與背景頻率的差異程度來排序詞元。它沒有單位，只有在相同請求和啟發式方法內進行比較時才有意義。

您可以透過在 `significant_terms` 下指定啟發式方法，為每個請求選取一種啟發式方法。支援下列啟發式方法。

### JLH

JLH 啟發式方法是預設值，適合大多數一般用途情境。它同時平衡詞元的絕對頻率及其相對於背景集合的過度呈現程度，偏好同時在*絕對*和*相對*上增加的詞元。

```json
"significant_terms": {
  "field": "payment_method",
  "jlh": {}
}
```

#### JLH 評分

JLH 分數的計算方式如下：

`fg_pct = doc_count / foreground_total` 和 `bg_pct = bg_count / background_total`。JLH ≈ `(fg_pct − bg_pct) * (fg_pct / bg_pct)`。

由於絕對變化會乘以前景與背景百分比的比率，因此相同的絕對增加量，對於背景占比小的詞元會產生比背景占比大的詞元更高的分數。例如，從文件占比 1% 增加到 2% 的分數會高於從 50% 增加到 51%。

如果詞元的前景百分比小於或等於其背景百分比，其 JLH 分數為 `0`，因此不會傳回該詞元。

#### 使用 JLH 的分數範例計算

假設您的前景集合（高價值退貨）包含 `2,000` 筆訂單，而背景集合（所有訂單）包含 `120,000` 筆訂單。考慮 `significant_terms` 彙總中的單一詞元，其計數如下：

- `doc_count = 160`
- `bg_count = 3,200`

包含該詞元的文件百分比計算如下：

- `fg_pct = 160 / 2000 = 0.08`
- `bg_pct = 3200 / 120000 ≈ 0.026666…`

JLH ≈ `(0.08 − 0.026666…) * (0.08 / 0.026666…) ≈ 0.053333… * 3 ≈ 0.16`

這個正分數表示搜尋的詞元在高價值退貨中比整體更為普遍。分數是相對的：請用它們來排序詞元，而不是當作絕對機率。

### 相互資訊

相互資訊（MI）偏好頻繁的詞元，並找出熱門但仍具區別性的詞元。設定 `include_negatives: false` 以忽略在前景中比在背景中更不常見的詞元。如果您的背景不是前景的超集，請設定 `background_is_superset: false`：

```json
"significant_terms": {
  "field": "product.keyword",
  "mutual_information": {
    "include_negatives": false,
    "background_is_superset": true
  }
}
```

### 卡方

卡方是一種統計檢定，用於衡量詞元在子集（前景）中觀察到的頻率與根據參考集合（背景）得出的預期頻率之間的偏差程度。與 [MI](#mutual-information) 類似，卡方支援 `include_negatives` 和 `background_is_superset`：

```json
"significant_terms": {
  "field": "error.keyword",
  "chi_square": { "include_negatives": false }
}
```

### Google 正規化距離

Google 正規化距離（GND）偏好強烈的共現。它適用於同義詞探索或傾向於一起出現的項目。GND 支援 `background_is_superset` 參數：

```json
"significant_terms": {
  "field": "tag.keyword",
  "gnd": { "background_is_superset": true }
}
```

### 百分比

Percentage 依 `doc_count`/`bg_count` 的比例對詞彙排序，並識別某個詞彙在前景集合中的命中次數相對於其背景集合命中次數的數量。它不會考量兩個集合的整體大小，因此非常罕見的詞彙可能會佔據主導地位。例如，某個只出現在一個文件中、且該文件也在前景集合中的詞彙，其分數為 `1`，這是可能的最高分。為了避免只出現一次的詞彙主導結果，請提高 `min_doc_count` 與 `shard_min_doc_count`，例如設為 `10`：

```json
"significant_terms": {
  "field": "sku.keyword",
  "min_doc_count": 10,
  "shard_min_doc_count": 10,
  "percentage": {}
}
```

### 指令碼啟發式方法

若要提供自訂的啟發式公式，可以使用下列變數：

- `_subset_freq`：前景集合中包含該詞彙的文件數量。
- `_superset_freq`：背景集合中包含該詞彙的文件數量。
- `_subset_size`：前景集合中的文件總數。
- `_superset_size`：背景集合中的文件總數。

下列請求在 `field.keyword` 上執行 `significant_terms` 彙總，使用自訂的指令碼啟發式，根據詞彙在前景相對於背景的出現頻率來評分：

```json
"significant_terms": {
  "field": "field.keyword",
  "script_heuristic": {
    "script": {
      "lang": "painless",
      "source": "params._subset_freq / (params._superset_freq - params._subset_freq + 1)"
    }
  }
}
```

### 選擇啟發式方法

各種啟發式方法偏好不同類型的詞彙：

- Mutual information 偏好高頻詞彙，即使它們在背景集合中也很常見。在自然語言文字中，它可能會選出停用詞，但很少選出非常罕見的詞彙，例如拼錯的字。
- GND 偏好經常與前景集合共同出現的詞彙，並避免停用詞。不過，它傾向於選出非常罕見的詞彙，例如拼錯的字。
- Chi-square 與 JLH 則介於這兩者之間。

沒有任何啟發式方法適用於所有資料集。請在您的資料上嘗試多種啟發式方法並比較結果。

## 大小與分片大小

`size` 參數控制彙總傳回的桶數。每個分片會先使用本機統計資料選出自己的候選詞彙，然後協調節點將所有分片的候選詞彙合併為最終清單。由於分片無法得知詞彙的全域頻率，屬於最終結果的詞彙可能會遺漏，或其計數可能略有不準確。

為了減少這些錯誤，每個分片傳回的候選詞彙數量會多於所要求的 `size`。預設情況下，它會傳回 `2 * (size * 1.5 + 10)` 個詞彙，是 `terms` 彙總傳回數量的兩倍。需要更多候選詞彙，是因為整體而言顯著的詞彙可能在每個分片上只出現一兩次，在該分片上看起來與不顯著的詞彙相同。

若要控制候選詞彙的數量，請設定 `shard_size`。`shard_size` 值若遠大於 `size`，可以改善結果品質，但也會增加記憶體使用量與網路流量。

## 最小文件數量

`min_doc_count` 參數會排除在前景文件中出現次數少於指定數量的詞彙。`3` 的預設值要求必須有一些證據顯示詞彙具有意義：只出現在一個文件中的詞彙通常是打錯字或其他一次性出現，因此一般不建議將 `min_doc_count` 設為 `1`。

`min_doc_count` 門檻只在協調節點合併分片結果之後套用。每個分片會根據本機分數選取候選詞彙，因此本機分數高的低頻詞彙可能會取代原本在全域範圍內符合 `min_doc_count` 的詞彙。若要傳回這些詞彙，請提高 `shard_size`。

`shard_min_doc_count` 參數會在候選詞彙傳送至協調節點之前，於每個分片上進行篩選。您可以用它來捨棄即使在合併分片計數之後也不太可能達到 `min_doc_count` 的詞彙，例如拼錯的字。請將 `shard_min_doc_count` 設為遠低於 `min_doc_count` 除以分片數的值。否則，顯著的詞彙可能會在個別分片上被篩除。

## 篩選值

您可以使用 `include` 與 `exclude` 參數來限制要建立桶的詞彙。這些參數接受規則運算式或精確值的陣列，其運作方式與 `terms` 彙總中相同。如需更多資訊，請參閱[將值篩選為子集]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/#filtering-values-to-a-subset)。

## 收集模式

為了限制記憶體使用量，`significant_terms` 彙總一律以 `breadth_first` 模式計算子彙總。如需收集模式的更多資訊，請參閱[收集模式]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/#collect-mode)。

## 執行提示

`execution_hint` 參數接受 `map` 與 `global_ordinals`，其運作方式與 `terms` 彙總中相同。OpenSearch 會自動選取模式，因此您很少需要設定它。如需更多資訊，請參閱[執行提示]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/#execution-hint)。

## 限制

`significant_terms` 彙總有下列限制：

- 詞彙必須是已編製索引的值。您無法使用指令碼產生詞彙，因為為指令碼產生的詞彙計算背景頻率，將需要在索引中的每個文件上執行該指令碼。
- 不支援浮點數欄位。整數欄位（例如帳號或類別編號）可能適合分析，但浮點數欄位通常包含數量，其個別值並不是有意義的詞彙。
- 當查詢符合所有文件時，請勿使用 `significant_terms` 作為頂層彙總。在這種情況下，前景與背景集合完全相同，因此不會有任何詞彙特別突出。
- 避免在 `significant_terms` 之下放置大型子彙總。每個分片會產生許多候選詞彙，而其中大多數在合併分片結果後會被捨棄，因此為所有候選詞彙計算子彙總的成本很高。建議改為執行一次搜尋以取得顯著詞彙，再執行第二次搜尋，只對這些詞彙執行子彙總。
- 文件計數是近似值。`doc_count` 值可能過低，因為某些分片未在其候選詞彙中傳回該詞彙；`bg_count` 值可能過高，因為背景計數可能包含已刪除的文件。若要改善準確性，請提高 `shard_size`。
