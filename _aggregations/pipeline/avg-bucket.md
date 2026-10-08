---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "平均桶"
parent: Pipeline aggregations
nav_order: 10
---

# 平均桶彙總

`avg_bucket` 彙總是一種同層級彙總，會計算先前彙總中每個桶 (bucket) 內某項指標的平均值。

指定的指標必須是數值，且同層級彙總必須是多桶彙總。

## 參數

`avg_bucket` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設值為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#data-gaps)。|
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。會在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |

## 範例

下列範例會從 OpenSearch Dashboards 電子商務範例資料建立以一個月為間隔的日期長條圖。`sum` 子彙總會計算每個月的位元組總和。最後，`avg_bucket` 彙總會根據這些總和計算每月平均位元組數：

```json
POST opensearch_dashboards_sample_data_logs/_search
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
    "avg_monthly_bytes": {
      "avg_bucket": {
        "buckets_path": "visits_per_month>sum_of_bytes"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

此彙總會傳回每月桶的平均位元組數：

```json
{
  "took": 43,
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
    "avg_monthly_bytes": {
      "value": 26575229.666666668
    }
  }
}
```
