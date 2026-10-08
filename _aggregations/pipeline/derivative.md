---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "導數"
parent: Pipeline aggregations
nav_order: 70
---

# 導數彙總

`derivative` 彙總是一種父彙總，用於計算某個彙總中每個桶 (bucket) 的一階導數與二階導數。「一階導數」和「二階導數」在英文中常分別簡稱為「first derivative」和「second derivative」。本頁使用簡稱。

對於一系列有序的桶，`derivative` 會將一階導數近似為目前桶與前一個桶之間指標值的差。

## 參數

`derivative` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |

## 範例：一階導數

下列範例使用 OpenSearch Dashboards 電子商務範例資料，建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`derivative` 彙總會計算 `sum` 子彙總的一階導數。一階導數的估算方式為目前月份與前一個月份位元組數的差：

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
        "number_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "bytes_deriv": {
          "derivative": {
            "buckets_path": "number_of_bytes"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例：一階導數

回應顯示針對第二個和第三個桶計算出的導數：

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
    "sales_per_month": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "number_of_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "number_of_bytes": {
            "value": 39103067
          },
          "bytes_deriv": {
            "value": 36298964
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "number_of_bytes": {
            "value": 37818519
          },
          "bytes_deriv": {
            "value": -1284548
          }
        }
      ]
    }
  }
}
```

第一個桶沒有計算導數，因為該桶沒有前一個桶可用。

## 範例：二階導數

若要計算二階導數，請將一個導數彙總串接到另一個導數彙總：

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
        "number_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "bytes_1st_deriv": {
          "derivative": {
            "buckets_path": "number_of_bytes"
          }
        },
        "bytes_2nd_deriv": {
          "derivative": {
            "buckets_path": "bytes_1st_deriv"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例：二階導數

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
    "sales_per_month": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "number_of_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "number_of_bytes": {
            "value": 39103067
          },
          "bytes_1st_deriv": {
            "value": 36298964
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "number_of_bytes": {
            "value": 37818519
          },
          "bytes_1st_deriv": {
            "value": -1284548
          },
          "bytes_2nd_deriv": {
            "value": -37583512
          }
        }
      ]
    }
  }
}
```

第一個桶沒有計算一階導數，因為該桶沒有前一個桶可用。同樣地，第一個和第二個桶也沒有計算二階導數。
