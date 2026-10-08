---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Stats
parent: Metric aggregations
nav_order: 110
redirect_from:
  - /query-dsl/aggregations/metric/stats/
---

# Stats 彙總

`stats` 彙總是一種多值指標彙總，用於計算數值資料的摘要。此彙總有助於快速了解數值欄位的分布情況。它可以直接對欄位執行運算、套用指令碼來衍生值，或處理缺少欄位的文件。`stats` 彙總會傳回五個值：

* `count`：收集到的值的數量
* `min`：最小值
* `max`：最大值
* `sum`：所有值的總和
* `avg`：值的平均數（總和除以數量）

## 參數

`stats` 彙總接受下列選用參數。

| 參數 | 資料類型 | 說明                                                                                |
| --------- | --------- | ------------------------------------------------------------------------------------------ |
| `field`   | 字串    | 要進行彙總的欄位。必須是數值欄位。                                            |
| `script`  | 物件    | 用於計算彙總自訂值的指令碼。可取代 `field` 或與其搭配使用。 |
| `missing` | 數字    | 用於缺少目標欄位之文件的預設值。 

## 範例

下列範例會計算用電量的 `stats` 彙總。

建立名為 `power_usage` 的索引，並新增包含特定小時內所消耗千瓦時 (kWh) 數的文件：

```json
PUT /power_usage/_bulk?refresh=true
{"index": {}}
{"device_id": "A1", "kwh": 1.2}
{"index": {}}
{"device_id": "A2", "kwh": 0.7}
{"index": {}}
{"device_id": "A3", "kwh": 1.5}
```
{% include copy-curl.html %}

若要計算所有文件中 `kwh` 欄位的統計資料，請對 `kwh` 欄位使用名為 `consumption_stats` 的 `stats` 彙總。將 `size` 設為 `0` 表示不傳回文件命中結果：

```json
GET /power_usage/_search
{
  "size": 0,
  "aggs": {
    "consumption_stats": {
      "stats": {
        "field": "kwh"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含索引中三份文件的 `count`、`min`、`max`、`avg` 和 `sum` 值：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "consumption_stats": {
      "count": 3,
      "min": 0.699999988079071,
      "max": 1.5,
      "avg": 1.1333333452542622,
      "sum": 3.400000035762787
    }
  }
}
```

### 針對每個桶執行 stats 彙總

您可以將 `stats` 彙總巢狀置於 `device_id` 欄位上的 `terms` 彙總中，藉此為每個裝置分別計算統計資料。`terms` 彙總會根據不重複的 `device_id` 值將文件分組到桶 (bucket) 中，而 `stats` 彙總則會在每個桶內計算摘要統計資料：

```json
GET /power_usage/_search
{
  "size": 0,
  "aggs": {
    "per_device": {
      "terms": {
        "field": "device_id.keyword"
      },
      "aggs": {
        "device_usage_stats": {
          "stats": {
            "field": "kwh"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會為每個 `device_id` 傳回一個桶，每個桶內都包含計算出的 `count`、`min`、`max`、`avg` 和 `sum` 欄位：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "per_device": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "A1",
          "doc_count": 1,
          "device_usage_stats": {
            "count": 1,
            "min": 1.2000000476837158,
            "max": 1.2000000476837158,
            "avg": 1.2000000476837158,
            "sum": 1.2000000476837158
          }
        },
        {
          "key": "A2",
          "doc_count": 1,
          "device_usage_stats": {
            "count": 1,
            "min": 0.699999988079071,
            "max": 0.699999988079071,
            "avg": 0.699999988079071,
            "sum": 0.699999988079071
          }
        },
        {
          "key": "A3",
          "doc_count": 1,
          "device_usage_stats": {
            "count": 1,
            "min": 1.5,
            "max": 1.5,
            "avg": 1.5,
            "sum": 1.5
          }
        }
      ]
    }
  }
}
```

這讓您只需一個查詢即可比較各裝置的使用量統計資料。

### 使用指令碼計算衍生值

您也可以使用指令碼來計算 `stats` 彙總中使用的值。當指標是從文件欄位衍生而來或需要轉換時，這項功能就很實用。

例如，由於 `1 kWh` 等於 `1,000 Wh`，若要在執行 `stats` 彙總前將千瓦時 (kWh) 轉換為瓦時 (Wh)，您可以使用將每個值乘以 `1,000` 的指令碼。下列指令碼 `doc['kwh'].value * 1000` 用於衍生每份文件的輸入值：

```json
GET /power_usage/_search
{
  "size": 0,
  "aggs": {
    "usage_wh_stats": {
      "stats": {
        "script": {
          "source": "doc['kwh'].value * 1000"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中傳回的 `stats` 彙總反映了 `1200`、`700` 和 `1500` Wh 的值：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "usage_wh_stats": {
      "count": 3,
      "min": 699.999988079071,
      "max": 1500,
      "avg": 1133.3333452542622,
      "sum": 3400.000035762787
    }
  }
}
```

### 搭配欄位使用值指令碼

將欄位與轉換結合時，您可以同時指定 `field` 和 `script`。如此即可使用 `_value` 變數，在指令碼中參照該欄位的值。

下列範例會在計算 `stats` 彙總前，將每筆能源讀數增加 5%：

```json
GET /power_usage/_search
{
  "size": 0,
  "aggs": {
    "adjusted_usage": {
      "stats": {
        "field": "kwh",
        "script": {
          "source": "_value * 1.05"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 缺少的值

如果部分文件不包含目標欄位，預設會將其排除在彙總之外。若要使用預設值將這些文件納入，您可以指定 `missing` 參數。

下列請求會將缺少的 `kwh` 值視為 `0.0`：

```json
GET /power_usage/_search
{
  "size": 0,
  "aggs": {
    "consumption_with_default": {
      "stats": {
        "field": "kwh",
        "missing": 0.0
      }
    }
  }
}
```
{% include copy-curl.html %}
