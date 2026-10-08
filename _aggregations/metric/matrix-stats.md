---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "矩陣統計資料"
parent: Metric aggregations
nav_order: 50
redirect_from:
  - /query-dsl/aggregations/metric/matrix-stats/
---

# 矩陣統計資料彙總

`matrix_stats` 彙總是一種多值指標彙總，會以矩陣形式為兩個或更多欄位產生共變異數統計資料。

`matrix_stats` 彙總不支援指令碼。
{: .note}

## 參數

`matrix_stats` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--       | :--               | :--            | :--         |
| `fields`  | 必要          | 字串         | 要計算矩陣統計資料的欄位陣列。 |
| `missing`    | 選用          | 物件         | 用來取代缺失值的值。預設會忽略缺失值。請參閱[缺失值](#missing-values)。 |
| `mode`    | 選用          | 字串         | 從多值欄位或陣列欄位中作為樣本使用的值。允許的值為 `avg`、`min`、`max`、`sum` 和 `median`。預設為 `avg`。 |

## 範例

下列範例會傳回 OpenSearch Dashboards 電子商務範例資料中 `taxful_total_price` 和 `products.base_price` 欄位的統計資料：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "matrix_stats_taxful_total_price": {
      "matrix_stats": {
        "fields": ["taxful_total_price", "products.base_price"]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含彙總結果：

```json
{
  "took": 250,
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
    "matrix_stats_taxful_total_price": {
      "doc_count": 4675,
      "fields": [
        {
          "name": "products.base_price",
          "count": 4675,
          "mean": 34.99423943014724,
          "variance": 360.5035285833702,
          "skewness": 5.530161335032689,
          "kurtosis": 131.1630632404217,
          "covariance": {
            "products.base_price": 360.5035285833702,
            "taxful_total_price": 846.6489362233169
          },
          "correlation": {
            "products.base_price": 1,
            "taxful_total_price": 0.8444765264325269
          }
        },
        {
          "name": "taxful_total_price",
          "count": 4675,
          "mean": 75.05542864304839,
          "variance": 2788.1879749835425,
          "skewness": 15.812149139923994,
          "kurtosis": 619.1235507385886,
          "covariance": {
            "products.base_price": 846.6489362233169,
            "taxful_total_price": 2788.1879749835425
          },
          "correlation": {
            "products.base_price": 0.8444765264325269,
            "taxful_total_price": 1
          }
        }
      ]
    }
  }
}
```

下表說明回應欄位。

| 統計量    | 說明 |
| :---         | :---        |
| `count`      | 為彙總取樣的文件數。 |
| `mean`       | 從樣本計算出的欄位平均值。 |
| `variance`   | 與平均值偏差的平方，用於衡量資料的分散程度。 |
| `skewness`   | 衡量分布相對於平均值的不對稱性。請參閱[偏態](https://en.wikipedia.org/wiki/Skewness)。 |
| `kurtosis` | 衡量分布尾部的厚重程度。尾部越輕，峰度就越低。透過評估峰度和偏態來判斷母體是否可能呈[常態分布](https://en.wikipedia.org/wiki/Normal_distribution)。請參閱[峰度](https://en.wikipedia.org/wiki/Kurtosis)。|
| `covariance`  | 衡量兩個欄位之間的共同變異程度。正值表示兩者的值朝相同方向變動。 |
| `correlation` | 標準化的共變異數，用於衡量兩個欄位之間關係的強度。可能的值介於 -1 到 1 之間（含兩端），代表從完全負線性相關到完全正線性相關。值為 0 表示變數之間沒有可辨識的關係。 |

## 缺失值

若要定義缺失值的處理方式，請使用 `missing` 參數。預設會忽略缺失值。

例如，建立一個索引，其中文件 1 缺少 `gpa` 和 `class_grades` 欄位：

```json
POST _bulk
{ "create": { "_index": "students", "_id": "1" } }
{ "name": "John Doe" } 
{ "create": { "_index": "students", "_id": "2" } }
{ "name": "Jonathan Powers", "gpa": 3.85, "class_grades": [3.0, 3.9, 4.0] } 
{ "create": { "_index": "students", "_id": "3" } }
{ "name": "Jane Doe", "gpa": 3.52, "class_grades": [3.2, 2.1, 3.8] }
```
{% include copy-curl.html %}

首先，在不提供 `missing` 參數的情況下執行 `matrix_stats` 彙總：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "matrix_stats_taxful_total_price": {
      "matrix_stats": {
        "fields": [
          "gpa",
          "class_grades"
        ],
        "mode": "avg"
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 在計算矩陣統計資料時會忽略缺失值：

```json
{
  "took": 5,
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
    "matrix_stats_taxful_total_price": {
      "doc_count": 2,
      "fields": [
        {
          "name": "gpa",
          "count": 2,
          "mean": 3.684999942779541,
          "variance": 0.05444997482300096,
          "skewness": 0,
          "kurtosis": 1,
          "covariance": {
            "gpa": 0.05444997482300096,
            "class_grades": 0.09899998760223136
          },
          "correlation": {
            "gpa": 1,
            "class_grades": 0.9999999999999991
          }
        },
        {
          "name": "class_grades",
          "count": 2,
          "mean": 3.333333333333333,
          "variance": 0.1800000381469746,
          "skewness": 0,
          "kurtosis": 1,
          "covariance": {
            "gpa": 0.09899998760223136,
            "class_grades": 0.1800000381469746
          },
          "correlation": {
            "gpa": 0.9999999999999991,
            "class_grades": 1
          }
        }
      ]
    }
  }
}
```

若要將缺失的欄位設為 `0`，請以鍵值對應的形式提供 `missing` 參數。雖然 `class_grades` 是陣列欄位，但 `matrix_stats` 彙總會將多值數值欄位扁平化為每份文件的平均值，因此您必須提供單一數字作為缺失值：

```json
GET students/_search
{
  "size": 0,
  "aggs": {
    "matrix_stats_taxful_total_price": {
      "matrix_stats": {
        "fields": ["gpa", "class_grades"],
        "mode": "avg",
        "missing": {
          "gpa": 0,
          "class_grades": 0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 在計算矩陣統計資料時，會以 `0` 取代任何缺失的 `gpa` 或 `class_grades` 值：

```json
{
  "took": 23,
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
    "matrix_stats_taxful_total_price": {
      "doc_count": 3,
      "fields": [
        {
          "name": "gpa",
          "count": 3,
          "mean": 2.456666628519694,
          "variance": 4.55363318017324,
          "skewness": -0.688130006360758,
          "kurtosis": 1.5,
          "covariance": {
            "gpa": 4.55363318017324,
            "class_grades": 4.143944374667273
          },
          "correlation": {
            "gpa": 1,
            "class_grades": 0.9970184390038257
          }
        },
        {
          "name": "class_grades",
          "count": 3,
          "mean": 2.2222222222222223,
          "variance": 3.793703722777191,
          "skewness": -0.6323693521730989,
          "kurtosis": 1.5000000000000002,
          "covariance": {
            "gpa": 4.143944374667273,
            "class_grades": 3.793703722777191
          },
          "correlation": {
            "gpa": 0.9970184390038257,
            "class_grades": 1
          }
        }
      ]
    }
  }
}
```
