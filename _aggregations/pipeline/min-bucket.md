---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最小值桶"
parent: Pipeline aggregations
nav_order: 110
---

# 最小值桶彙總

`min_bucket` 彙總是一種同層級彙總，會計算前一個彙總中每個桶 (bucket) 內某個指標的最小值。

指定的指標必須是數值，且同層級彙總必須是多桶彙總。

## 參數

`min_bucket` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#data-gaps)。|
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。會在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |

## 範例

下列範例會從 OpenSearch Dashboards 電子商務範例資料建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月的位元組總和。最後，`min_bucket` 彙總會找出最小值，也就是這些桶中最小的值：

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
    "min_monthly_bytes": {
      "min_bucket": {
        "buckets_path": "visits_per_month>sum_of_bytes"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

`max_bucket` 彙總會傳回指定指標在多個桶中的最小值。在此範例中，它會根據 `visits_per_month` 內的 `sum_of_bytes` 指標，計算每月位元組數的最小值。`value` 欄位顯示在所有桶中找到的最小值。`keys` 陣列包含觀察到此最小值的桶鍵。它之所以是陣列，是因為可能有多個桶具有相同的最小值。在這種情況下，所有相符的桶鍵都會包含在內。這可確保即使多個時間區間 (或詞彙) 具有相同的最小值，結果仍然準確：

```json
{
  "took": 7,
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
    "min_monthly_bytes": {
      "value": 2804103,
      "keys": [
        "2025-03-01T00:00:00.000Z"
      ]
    }
  }
}
```


