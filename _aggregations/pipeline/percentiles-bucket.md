---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "百分位數桶"
parent: Pipeline aggregations
nav_order: 160
---

# 百分位數桶彙總

`percentiles_bucket` 彙總是一種同層級彙總，用於計算分桶指標的百分位數位置。

`percentiles_bucket` 彙總會精確計算百分位數，不使用近似或內插。每個百分位數都會傳回小於或等於目標百分位數的最接近值。

`percentiles_bucket` 彙總需要將整個值清單暫時保留在記憶體中，即使是大型資料集也是如此。相較之下，[`percentiles` 指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/)使用的記憶體較少，但會以近似方式計算百分比。

指定的指標必須是數值，且同層級彙總必須是多桶 (multi-bucket) 彙總。

## 參數

`avg_bucket` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的策略。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |
| `percents`            | 選用          | 清單            | 包含任意數量數值百分比的清單，這些值會包含在輸出中。有效值介於 0.0 到 100.0 之間（含）。預設為 `[1.0, 5.0, 25.0, 50.0, 75.0, 95.0, 99.0]`。 |
| `keyed`               | 選用          | 布林值         | 是否將輸出格式化為字典，而非鍵值對物件的陣列。預設為 `true`（將輸出格式化為鍵值對）。 |


## 範例

下列範例使用 OpenSearch Dashboards 電子商務範例資料，建立間隔為一週的日期直方圖。`sum` 子彙總會加總每週的 `taxful_total_price`。最後，`percentiles_bucket` 彙總會根據這些總和計算每週的百分位數值：

```json
POST /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "weekly_sales": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "week"
      },
      "aggs": {
        "total_price": {
          "sum": {
            "field": "taxful_total_price"
          }
        }
      }
    },
    "percentiles_monthly_sales": {
      "percentiles_bucket": {
        "buckets_path": "weekly_sales>total_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

此彙總會傳回每週價格總和的預設百分位數值：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
  "took": 4,
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
    "weekly_sales": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 582,
          "total_price": {
            "value": 41455.5390625
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1048,
          "total_price": {
            "value": 79448.60546875
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1048,
          "total_price": {
            "value": 78208.4296875
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1073,
          "total_price": {
            "value": 81277.296875
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 924,
          "total_price": {
            "value": 70494.2578125
          }
        }
      ]
    },
    "percentiles_monthly_sales": {
      "values": {
        "1.0": 41455.5390625,
        "5.0": 41455.5390625,
        "25.0": 70494.2578125,
        "50.0": 78208.4296875,
        "75.0": 79448.60546875,
        "95.0": 81277.296875,
        "99.0": 81277.296875
      }
    }
  }
}
```
</details>

## 範例：選項

下一個範例使用與上一個範例相同的資料計算百分位數，但有下列差異：

- `percents` 參數指定只計算第 25、第 50 和第 75 百分位數。
- 使用 `format` 參數附加字串格式的輸出。
- 將 `keyed` 參數設定為 `false`，以鍵值對物件（附加字串值）的形式顯示結果。

範例如下：

```json
POST /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "weekly_sales": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "week"
      },
      "aggs": {
        "total_price": {
          "sum": {
            "field": "taxful_total_price"
          }
        }
      }
    },
    "percentiles_monthly_sales": {
      "percentiles_bucket": {
        "buckets_path": "weekly_sales>total_price",
        "percents": [25.0, 50.0, 75.0],
        "format": "$#,###.00",
        "keyed": false
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應：選項

這些選項會修改彙總的輸出：


<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
  "took": 5,
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
    "weekly_sales": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 582,
          "total_price": {
            "value": 41455.5390625
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1048,
          "total_price": {
            "value": 79448.60546875
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1048,
          "total_price": {
            "value": 78208.4296875
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1073,
          "total_price": {
            "value": 81277.296875
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 924,
          "total_price": {
            "value": 70494.2578125
          }
        }
      ]
    },
    "percentiles_monthly_sales": {
      "values": [
        {
          "key": 25,
          "value": 70494.2578125,
          "25.0_as_string": "$70,494.26"
        },
        {
          "key": 50,
          "value": 78208.4296875,
          "50.0_as_string": "$78,208.43"
        },
        {
          "key": 75,
          "value": 79448.60546875,
          "75.0_as_string": "$79,448.61"
        }
      ]
    }
  }
}
```
</details>

