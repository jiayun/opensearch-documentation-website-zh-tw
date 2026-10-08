---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "桶排序"
parent: Pipeline aggregations
nav_order: 40
---

# 桶排序彙總

`bucket_sort` 彙總是一種父彙總，會對其父多桶彙總所產生的桶 (bucket) 進行排序或截斷。

在 `bucket_sort` 彙總中，您可以依多個欄位對桶進行排序，每個欄位各有其排序順序。桶可以依其鍵、文件計數或子彙總的值進行排序。您也可以使用 `from` 和 `size` 參數截斷結果，無論是否進行排序皆可。

如需指定排序順序的相關資訊，請參閱[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。

## 參數

`bucket_sort` 彙總接受下列參數。

| 參數        | 必要/選用 | 資料類型       | 說明 |
| :--              | :--               |  :--            | :--         |
| `gap_policy`     | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `sort`           | 選用          | 字串          | 用於排序的欄位清單。請參閱[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。 |
| `from`           | 選用          | 字串          | 要傳回的第一個結果的索引。必須為非負整數。預設為 `0`。請參閱[`from` 和 `size` 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。 |
| `size`           | 選用          | 字串          | 要傳回的結果數量上限。必須為正整數。請參閱[`from` 和 `size` 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。|

您必須至少提供 `sort`、`from` 和 `size` 其中之一。
{: .note}

## 範例

下列範例會根據 OpenSearch Dashboards 電子商務範例資料，建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，此彙總會依位元組數以遞減順序對桶進行排序：

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
        "total_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "bytes_bucket_sort": {
          "bucket_sort": {
            "sort": [
              { "total_bytes": { "order": "desc" } }
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

此彙總會依位元組總數以遞減順序重新排列桶：

```json
{
  "took": 3,
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
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 7072,
          "total_bytes": {
            "value": 40124337
          }
        },
        {
          "key_as_string": "2025-06-01T00:00:00.000Z",
          "key": 1748736000000,
          "doc_count": 6056,
          "total_bytes": {
            "value": 34123131
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 946,
          "total_bytes": {
            "value": 5478221
          }
        }
      ]
    }
  }
}
```

## 範例：截斷結果 

若要截斷結果，請提供 `from` 和/或 `size` 參數。下列範例執行相同的排序，但從第二個桶開始傳回兩個桶：

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
        "total_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "bytes_bucket_sort": {
          "bucket_sort": {
            "sort": [
              { "total_bytes": { "order": "desc" } }
            ],
            "from": 1,
            "size": 2
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會傳回兩個已排序的桶：

```json
{
  "took": 2,
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
          "key_as_string": "2025-06-01T00:00:00.000Z",
          "key": 1748736000000,
          "doc_count": 6056,
          "total_bytes": {
            "value": 34123131
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 946,
          "total_bytes": {
            "value": 5478221
          }
        }
      ]
    }
  }
}
```

若要截斷結果而不進行排序，請省略 `sort` 參數：

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
        "total_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "bytes_bucket_sort": {
          "bucket_sort": {
            "from": 1,
            "size": 2
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}