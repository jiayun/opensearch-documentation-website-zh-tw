---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "統計桶"
parent: Pipeline aggregations
nav_order: 190
---

# 統計桶彙總

`stats_bucket` 彙總是一種同層級彙總，會針對前一個彙總的桶 (bucket) 傳回多種統計資料（`count`、`min`、`max`、`avg` 和 `sum`）。

指定的指標必須是數值，且同層級彙總必須是多桶彙總。

## 參數

`stats_bucket` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總之彙總桶的路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設值為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `<stat>_as_string` 屬性中傳回格式化後的輸出。 |

## 範例

下列範例使用 OpenSearch Dashboards 電子商務範例資料，建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`stats_bucket` 彙總會根據這些總和傳回 `count`、`avg`、`sum`、`min` 和 `max` 統計資料：

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
      "stats_bucket": {
        "buckets_path": "visits_per_month>sum_of_bytes"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

此彙總會針對這些桶傳回全部五項基本統計資料：

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
      "sum": 79725689
    }
  }
}
```
