---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "桶選取器"
parent: Pipeline aggregations
nav_order: 30
---

# 桶選取器彙總

`bucket_selector` 彙總是一種父管線彙總，會評估指令碼，以判斷 `histogram`（或 `date_histogram`）彙總所傳回的桶 (bucket) 是否應包含在最終結果中。 

與建立新值的管線彙總不同，`bucket_selector` 彙總的作用是篩選器，會根據指定的條件保留或移除整個桶。您可以使用此彙總，根據桶的計算指標來篩選桶。 

## 參數

`bucket_selector` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 物件          | 變數名稱與桶指標的對應，用來識別要在指令碼中使用的指標。指標必須為數值。請參閱[指令碼變數]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-script#script-variables)。 |
| `script`              | 必要          | 字串或物件 | 要執行的指令碼。可以是內嵌指令碼、已儲存的指令碼或指令碼檔案。指令碼可以存取 `buckets_path` 參數中定義的變數名稱。必須傳回布林值。傳回 `false` 的桶會從最終輸出中移除。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。  |


## 範例

下列範例會從 OpenSearch Dashboards 電子商務範例資料建立間隔為一週的日期直方圖。`sum` 子彙總會計算每週所有銷售額的總和。最後，`bucket_selector` 彙總會篩選產生的每週桶，移除所有總和未超過 $75,000 的桶：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "sales_per_week": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "week"
      },
      "aggs": {
        "weekly_sales": {
          "sum": {
            "field": "taxful_total_price",
            "format": "$#,###.00"
          }
        },
        "avg_vendor_spend": {
          "bucket_selector": {
            "buckets_path": {
              "weekly_sales": "weekly_sales"
            },
            "script": "params.weekly_sales > 75000"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

此彙總會傳回符合指令碼條件的 `sales_per_week` 桶：

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
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "sales_per_week": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1048,
          "weekly_sales": {
            "value": 79448.60546875,
            "value_as_string": "$79,448.61"
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1048,
          "weekly_sales": {
            "value": 78208.4296875,
            "value_as_string": "$78,208.43"
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1073,
          "weekly_sales": {
            "value": 81277.296875,
            "value_as_string": "$81,277.30"
          }
        }
      ]
    }
  }
}
```

由於 `buckets_selector` 彙總傳回的是布林值而非數值，因此不接受 `format` 參數。在此範例中，格式化後的指標是由 `sum` 子彙總在 `value_as_string` 結果中傳回。請與 [`bucket_script` 彙總中的範例]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-script/#example)進行對照。
{: .note}