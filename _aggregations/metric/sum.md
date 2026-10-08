---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "總和"
parent: Metric aggregations
nav_order: 120
redirect_from:
  - /query-dsl/aggregations/metric/sum/
---

# 總和彙總

`sum` 彙總是一種單值指標彙總，會計算所有相符文件中從某個欄位擷取的數值總和。此彙總常用於計算營收、數量或持續時間等指標的總計。

## 參數

`sum` 彙總接受下列參數。

| 參數 | 資料類型 | 說明                                                                                |
| --------- | --------- | ------------------------------------------------------------------------------------------ |
| `field`   | 字串    | 要進行彙總的欄位。必須是數值欄位。                                            |
| `script`  | 物件    | 用於計算彙總自訂值的指令碼。可取代 `field` 使用，或與其搭配使用。 |
| `missing` | 數字    | 用於缺少目標欄位之文件的預設值。 |

## 範例

下列範例示範如何計算物流索引中所記錄配送的總重量。 

建立索引：

```json
PUT /deliveries
{
  "mappings": {
    "properties": {
      "shipment_id": { "type": "keyword" },
      "weight_kg": { "type": "double" }
    }
  }
}
```
{% include copy-curl.html %}

新增範例文件：

```json
POST /deliveries/_bulk?refresh=true
{"index": {}}
{"shipment_id": "S001", "weight_kg": 12.5}
{"index": {}}
{"shipment_id": "S002", "weight_kg": 7.8}
{"index": {}}
{"shipment_id": "S003", "weight_kg": 15.0}
{"index": {}}
{"shipment_id": "S004", "weight_kg": 10.3}
```
{% include copy-curl.html %}


下列請求會計算 `deliveries` 索引中所有文件的總重量，透過將 `size` 設為 `0` 省略文件命中結果，並傳回 `weight_kg` 的總和：

```json
GET /deliveries/_search
{
  "size": 0,
  "aggs": {
    "total_weight": {
      "sum": {
        "field": "weight_kg"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含值 `45.6`，對應 `12.5` + `7.8` + `15.0` + `10.3` 的總和：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "total_weight": {
      "value": 45.6
    }
  }
}
```

### 使用指令碼計算值

您可以提供指令碼來計算彙總的值，而不直接指定欄位。當值必須經過推導或調整時，此方法相當實用。

在下列範例中，會先使用指令碼將每個重量從公斤轉換為公克，再進行加總：

```json
GET /deliveries/_search
{
  "size": 0,
  "aggs": {
    "total_weight_grams": {
      "sum": {
        "script": {
          "source": "doc['weight_kg'].value * 1000"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含 `45600` 的 `total_weight_grams`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "total_weight_grams": {
      "value": 45600
    }
  }
}
```

### 結合欄位與值指令碼

您也可以同時指定 `field` 和 `script`，並使用特殊變數 `_value` 參照該欄位的值。當您要對現有欄位值套用轉換時，此方法相當實用。

下列範例會在加總前將所有重量增加 10%：

```json
GET /deliveries/_search
{
  "size": 0,
  "aggs": {
    "adjusted_weight": {
      "sum": {
        "field": "weight_kg",
        "script": {
          "source": "Math.round(_value * 110) / 100.0"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應反映出原始總重量增加了 10%：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "adjusted_weight": {
      "value": 50.16
    }
  }
}
```

### 缺少的值

根據預設，缺少目標欄位的文件會被忽略。若要使用預設值將這些文件納入計算，請使用 `missing` 參數。 

下列範例會為缺少的 `weight_kg` 欄位指定預設值 `0`。這可確保沒有此欄位的文件會被視為 `weight_kg` 設為 `0`，並納入彙總中。

```json
GET /deliveries/_search
{
  "size": 0,
  "aggs": {
    "total_weight_with_missing": {
      "sum": {
        "field": "weight_kg",
        "missing": 0
      }
    }
  }
}
```
{% include copy-curl.html %}
