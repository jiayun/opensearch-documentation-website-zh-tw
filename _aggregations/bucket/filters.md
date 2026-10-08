---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Filters
parent: Bucket aggregations
nav_order: 60
redirect_from:
  - /query-dsl/aggregations/bucket/filters/
---

# Filters 彙總

`filters` 彙總會建立多個桶 (bucket)，每個桶都與一個具名或匿名的篩選查詢相關聯。每份文件都會依據所有篩選條件進行評估；如果文件符合多個篩選條件，就可能歸入多個桶。這與單數形式的 [`filter` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/filter/)不同，後者只會產生一個桶。

## 參數

`filters` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `filters` | 必要 | 物件或陣列 | 篩選條件定義。若要建立帶有標籤的桶，請提供具有具名鍵的物件；若要建立匿名（依位置排列）的桶，請提供陣列。 |
| `other_bucket` | 選用 | 布林值 | 設為 `true` 時，會新增一個桶，其中包含所有不符合任何篩選條件的文件。預設為 `false`。 |
| `other_bucket_key` | 選用 | 字串 | 其他桶的鍵名稱。設定此參數會隱含啟用 `other_bucket`。預設為 `_other_`。 |

## 範例：具名篩選條件

當您以物件形式提供篩選條件時，每個鍵都會成為回應中的桶名稱。下列範例將電子商務訂單分為三個價格層級：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "filters": {
        "filters": {
          "budget": { "range": { "taxful_total_price": { "lte": 50 } } },
          "mid_range": { "range": { "taxful_total_price": { "gt": 50, "lte": 100 } } },
          "premium": { "range": { "taxful_total_price": { "gt": 100 } } }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：匿名篩選條件

當您以陣列形式提供篩選條件時，桶會依照陣列中的相同順序傳回。下列範例使用匿名篩選條件：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "filters": {
        "filters": [
          { "range": { "taxful_total_price": { "lte": 50 } } },
          { "range": { "taxful_total_price": { "gt": 50, "lte": 100 } } }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：其他桶

`other_bucket` 參數會擷取所有不符合任何已定義篩選條件的文件。下列範例使用 `other_bucket_key` 為這個涵蓋其餘文件的桶指定自訂名稱：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "filters": {
        "other_bucket": true,
        "other_bucket_key": "all_others",
        "filters": {
          "budget": { "range": { "taxful_total_price": { "lte": 50 } } },
          "premium": { "range": { "taxful_total_price": { "gt": 100 } } }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

下列回應對應於其他桶範例：

```json
{
  "took": 3,
  "timed_out": false,
  "terminated_early": true,
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
    "price_ranges": {
      "buckets": {
        "budget": {
          "doc_count": 1633
        },
        "premium": {
          "doc_count": 950
        },
        "all_others": {
          "doc_count": 2092
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 物件或陣列 | 使用具名篩選條件時為具有具名鍵的物件；使用匿名篩選條件時為物件陣列。 |
| `buckets.<key>.doc_count` | 整數 | 此桶中符合篩選條件的文件數量。 |
