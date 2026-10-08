---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Bucket script
parent: Pipeline aggregations
nav_order: 20
---

# Bucket script 彙總

`bucket_script` 彙總是一種父管線彙總，會執行指令碼，對一組桶 (bucket) 逐桶進行數值計算。使用 `bucket_script` 彙總可對分桶彙總中的多個指標執行自訂數值計算。例如，您可以：

- 計算衍生指標與複合指標。
- 使用 if/else 陳述式套用條件邏輯。
- 計算特定業務的 KPI，例如自訂評分指標。

## 參數

`bucket_script` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 物件          | 變數名稱與分桶指標之間的對應，用於識別指令碼中要使用的指標。指標必須為數值。請參閱[指令碼變數](#script-variables)。 |
| `script`              | 必要          | 字串或物件 | 要執行的指令碼。可以是內嵌指令碼、已儲存的指令碼或指令碼檔案。指令碼可存取 `buckets_path` 參數中定義的變數名稱。必須傳回數值。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 參數中傳回格式化後的輸出。 |

## 指令碼變數

`buckets_path` 參數會將指令碼變數名稱對應至父彙總中的指標。之後即可在指令碼中使用這些變數。

對於 `bucket_script` 和 `bucket_selector` 彙總，`buckets_path` 參數是物件而非字串，因為它必須參照多個桶指標。如需 `buckets_path` 字串版本的說明，請參閱[管線彙總]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)頁面。
{: .note}

下列 `buckets_path` 會將 `sales_sum` 指標對應至 `total_sales` 指令碼變數，並將 `item_count` 指標對應至 `item_count` 指令碼變數：

```json
"buckets_path": {
  "total_sales": "sales_sum",
  "item_count": "item_count"
}
```

對應的變數可從 `params` 內容中存取。例如：

- `params.total_sales`
- `params.item_count`

## 啟用內嵌指令碼

使用 `script` 參數新增您的指令碼。指令碼可以是內嵌的、位於檔案中，或位於索引中。若要啟用內嵌指令碼，`config` 資料夾中的 `opensearch.yml` 檔案必須包含下列內容：

```yml
script.inline: on
```

## 範例

下列範例會從 OpenSearch Dashboards 電子商務範例資料建立間隔為一個月的日期長條圖。`total_sales` 子彙總會加總每個月所售出所有商品的含稅價格。`vendor_count` 彙總會計算每個月不重複供應商的總數。最後，`avg_vendor_spend` 彙總會使用內嵌指令碼，計算每個月每位供應商的平均支出金額：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "sales_per_month": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "month"
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "taxful_total_price"
          }
        },
        "vendor_count": {
          "cardinality": {
            "field": "products.manufacturer.keyword"
          }
        },
        "avg_vendor_spend": {
          "bucket_script": {
            "buckets_path": {
              "sales": "total_sales",
              "vendors": "vendor_count"
            },
            "script": "params.sales / params.vendors",
            "format": "$#,###.00"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

此彙總會傳回格式化後的每月供應商平均支出：

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
      "value": 4675,
      "relation": "eq"
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
          "doc_count": 721,
          "vendor_count": {
            "value": 21
          },
          "total_sales": {
            "value": 53468.1484375
          },
          "avg_vendor_spend": {
            "value": 2546.1023065476193,
            "value_as_string": "$2,546.10"
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 3954,
          "vendor_count": {
            "value": 21
          },
          "total_sales": {
            "value": 297415.98046875
          },
          "avg_vendor_spend": {
            "value": 14162.665736607143,
            "value_as_string": "$14,162.67"
          }
        }
      ]
    }
  }
}
```




