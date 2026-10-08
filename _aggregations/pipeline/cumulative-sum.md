---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "累計總和"
parent: Pipeline aggregations
has_children: false
nav_order: 60
---

# 累計總和彙總

`cumulative_sum` 彙總是一種父彙總，用於計算前一個彙總各個桶 (bucket) 的累計總和。

累計總和是指定序列的部分和所組成的序列。例如，序列 `{a,b,c,…}` 的累計總和為 `a`、`a+b`、`a+b+c`，依此類推。您可以使用累計總和將欄位隨時間的變化率視覺化。

## 參數

`cumulative_sum` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總之彙總桶的路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |


## 範例

下列範例從 OpenSearch Dashboards 電子商務範例資料建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`cumulative_sum` 彙總會計算每個月份桶的累計位元組數：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "sales_per_month": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "month"
      },
      "aggs": {
        "no-of-bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "cumulative_bytes": {
          "cumulative_sum": {
            "buckets_path": "no-of-bytes"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 8,
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
    "sales_per_month": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "no-of-bytes": {
            "value": 2804103
          },
          "cumulative_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "no-of-bytes": {
            "value": 39103067
          },
          "cumulative_bytes": {
            "value": 41907170
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "no-of-bytes": {
            "value": 37818519
          },
          "cumulative_bytes": {
            "value": 79725689
          }
        }
      ]
    }
  }
}
```
