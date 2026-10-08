---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "延伸統計桶"
parent: Pipeline aggregations
nav_order: 80
---

# 延伸統計桶彙總

`extended_stats_bucket` 彙總是 [`stats_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/stats-bucket/) 同層級彙總的更完整版本。除了 `stats_bucket` 提供的基本統計量之外，`extended_stats_bucket` 還會計算下列指標：

- 平方和
- 變異數
- 母體變異數
- 樣本變異數
- 標準差
- 母體標準差
- 樣本標準差
- 標準差界限：
  - 上限
  - 下限
  - 母體上限
  - 母體下限
  - 樣本上限
  - 樣本下限

標準差與變異數屬於母體統計量；兩者分別一律等於母體標準差與母體變異數。

`std_deviation_bounds` 物件定義一個範圍，涵蓋平均值上下指定數量的標準差（預設為兩個標準差）。此物件一律會包含在輸出中，但僅對常態分布的資料有意義。在解讀這些值之前，請先確認您的資料集符合常態分布。

指定的指標必須為數值，且同層級彙總必須是多桶（bucket）彙總。

## 參數

`extended_stats_bucket` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總之彙總桶的路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺失資料的原則。有效值為 `skip` 與 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。|
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `<stat>_as_string` 屬性中傳回格式化後的輸出。 |
| `sigma`   | 選用          | Double（非負數） | 用於計算 `std_deviation_bounds` 區間的平均值上下標準差數量。預設為 `2`。請參閱 `extended_stats` 中的[定義界限]({{site.url}}{{site.baseurl}}/aggregations/metric/extended-stats#defining-bounds)。 |

## 範例

下列範例使用 OpenSearch Dashboards 電子商務範例資料，建立一個以一個月為間隔的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`extended_stats_bucket` 彙總會傳回這些總和的延伸統計：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "visits_per_month": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "month"
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        }
      }
    },
    "stats_monthly_bytes": {
      "extended_stats_bucket": {
        "buckets_path": "visits_per_month>sum_of_bytes",
        "sigma": 3,
        "format": "0.##E0"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

回應包含所選桶的延伸統計。請注意，標準差界限是針對三個標準差（three-sigma）的範圍；變更 `sigma`（或讓其使用預設值 `2`）會傳回不同的結果：

<details open markdown="block">
  <summary>
    回應
  </summary>

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
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "visits_per_month": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "sum_of_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "sum_of_bytes": {
            "value": 39103067
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "sum_of_bytes": {
            "value": 37818519
          }
        }
      ]
    },
    "stats_monthly_bytes": {
      "count": 3,
      "min": 2804103,
      "max": 39103067,
      "avg": 26575229.666666668,
      "sum": 79725689,
      "min_as_string": "2.8E6",
      "max_as_string": "3.91E7",
      "avg_as_string": "2.66E7",
      "sum_as_string": "7.97E7",
      "sum_of_squares": 2967153221794459,
      "variance": 282808242095406.25,
      "variance_population": 282808242095406.25,
      "variance_sampling": 424212363143109.4,
      "std_deviation": 16816903.46334325,
      "std_deviation_population": 16816903.46334325,
      "std_deviation_sampling": 20596416.2694171,
      "std_deviation_bounds": {
        "upper": 77025940.05669643,
        "lower": -23875480.72336309,
        "upper_population": 77025940.05669643,
        "lower_population": -23875480.72336309,
        "upper_sampling": 88364478.47491796,
        "lower_sampling": -35214019.141584635
      },
      "sum_of_squares_as_string": "2.97E15",
      "variance_as_string": "2.83E14",
      "variance_population_as_string": "2.83E14",
      "variance_sampling_as_string": "4.24E14",
      "std_deviation_as_string": "1.68E7",
      "std_deviation_population_as_string": "1.68E7",
      "std_deviation_sampling_as_string": "2.06E7",
      "std_deviation_bounds_as_string": {
        "upper": "7.7E7",
        "lower": "-2.39E7",
        "upper_population": "7.7E7",
        "lower_population": "-2.39E7",
        "upper_sampling": "8.84E7",
        "lower_sampling": "-3.52E7"
      }
    }
  }
}
```

</details>
