---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "加權平均"
parent: Metric aggregations
nav_order: 150
has_math: true
---

# 加權平均彙總

`weighted_avg` 彙總會計算從文件中擷取之數值的加權平均。一般平均中每個資料點的貢獻相同，加權平均則依據對應的權重值，為每個資料點指定不同的重要性。

加權平均的計算公式為 $$ \frac{\sum_{i=1}^n \text{value}_i \cdot \text{weight}_i}{\sum_{i=1}^n \text{weight}_i} $$。

在一般平均中，每個資料點的貢獻相同，這等同於為所有值指定 `1` 的權重。

## 參數

`weighted_avg` 彙總接受下列參數。

| 參數     | 必要/選用  | 說明 |
|---------------|----------|-------------|
| `value`       | 必要      | 定義如何取得要計算平均的數值。需要 `field` 或 `script`。 |
| `weight`      | 必要      | 定義如何取得每個值的權重。需要 `field` 或 `script`。 |
| `format`      | 選用       | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |
| `value_type`  | 選用       | 使用指令碼或未對應欄位時，值的類型提示。 |

您可以在 `value` 或 `weight` 中指定下列參數。

| 參數  | 必要/選用 |  說明 |
|------------|----------|-------------|
| `field`    | 選用 | 用作值或權重的文件欄位。 |
| `missing`  | 選用 | 欄位缺失時使用的預設值或權重。請參閱[缺失值](#missing-values)。|
| `script`   | 選用 | 提供值或權重的指令碼。與 `field` 互斥。 |


## 範例

首先，建立索引並新增一些資料。產品 C 缺少 `rating` 和 `num_reviews` 欄位：

```json
POST _bulk
{ "index": { "_index": "products" } }
{ "name": "Product A", "rating": 4.5, "num_reviews": 100 }
{ "index": { "_index": "products" } }
{ "name": "Product B", "rating": 3.8, "num_reviews": 50 }
{ "index": { "_index": "products" } }
{ "name": "Product C"}
```
{% include copy-curl.html %}

下列請求會計算產品評分的加權平均，其中每個產品的評分以其 `num_reviews` 加權。評論數較多的產品對最終平均的影響較大：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "weighted_rating": {
      "weighted_avg": {
        "value": {
          "field": "rating"
        },
        "weight": {
          "field": "num_reviews"
        },
        "format": "#.##"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

回應包含 `weighted_rating`，其計算方式為 `(4.5 * 100 + 3.8 * 50) / (100 + 50) = 4.27`。只有同時包含 `rating` 和 `num_reviews` 值的文件才會納入計算：

```json
{
  "took": 21,
  "timed_out": false,
  "terminated_early": true,
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
    "weighted_rating": {
      "value": 4.266666650772095,
      "value_as_string": "4.27"
    }
  }
}
```

## 多值欄位

`value` 欄位在每份文件中可包含多個值，但 `weight` 欄位必須解析為恰好一個值。具有多個權重的文件會導致錯誤。若要處理多值的權重欄位，請使用可將其縮減為單一數字的 `script`。

當文件包含多個值時，單一權重會分別套用至每個值。下列範例會將一份 `rating` 為多值欄位的文件編製索引，然後執行彙總：

```json
POST /products/_doc?refresh=true
{
  "name": "Product D",
  "rating": [1, 2, 3],
  "num_reviews": 2
}
```
{% include copy-curl.html %}

```json
GET /products/_search
{
  "size": 0,
  "query": {
    "term": { "name.keyword": "Product D" }
  },
  "aggs": {
    "weighted_rating": {
      "weighted_avg": {
        "value": {
          "field": "rating"
        },
        "weight": {
          "field": "num_reviews"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

三個值（`1`、`2` 和 `3`）各自以 `2` 加權，結果為 `((1*2) + (2*2) + (3*2)) / (2+2+2) = 2.0`：

```json
{
  ...
  "aggregations": {
    "weighted_rating": {
      "value": 2.0
    }
  }
}
```

## 使用指令碼

您可以為值、權重或兩者提供指令碼，以即時計算衍生數值。下列範例會在計算加權平均之前，將每個評分和權重加上 `1`：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "weighted_rating": {
      "weighted_avg": {
        "value": {
          "script": "if (doc['rating'].size() == 0) return 0; return doc['rating'].value + 1"
        },
        "weight": {
          "script": "if (doc['num_reviews'].size() == 0) return 0; return doc['num_reviews'].value + 1"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 缺失值

根據預設，缺少 `value` 欄位的文件會從計算中排除。缺少 `weight` 欄位的文件仍會納入計算，並使用隱含權重 `1`。

`missing` 參數會為缺少該欄位的文件指定替代值，藉此覆寫這些預設行為。下列範例會為缺少這些欄位的文件指定預設評分 `3.0` 及預設評論數 `1`：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "weighted_rating": {
      "weighted_avg": {
        "value": {
          "field": "rating",
          "missing": 3.0
        },
        "weight": {
          "field": "num_reviews",
          "missing": 1
        },
        "format": "#.##"
      }
    }
  }
}
```
{% include copy-curl.html %}

套用缺失值後，加權平均的計算方式為 `(4.5 * 100 + 3.8 * 50 + 3.0 * 1) / (100 + 50 + 1) = 4.26`：

```json
{
  ...
  "aggregations": {
    "weighted_rating": {
      "value": 4.258278129906055,
      "value_as_string": "4.26"
    }
  }
}
```
