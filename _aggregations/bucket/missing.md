---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Missing
parent: Bucket aggregations
nav_order: 120
redirect_from:
  - /query-dsl/aggregations/bucket/missing/
---

# Missing 彙總

`missing` 彙總會建立單一桶 (bucket)，其中包含指定欄位沒有值的所有文件。若欄位完全不存在，或包含已設定的 `NULL` 值，該文件即視為缺少該欄位。此彙總通常會與其他桶彙總搭配使用，以納入因缺少必要欄位而無法歸入任何其他桶的文件。

## 參數

`missing` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要檢查缺少值的欄位。 |

## 範例

下列範例使用 `products` 索引（建立於[加權平均範例]({{site.url}}{{site.baseurl}}/aggregations/metric/weighted-avg/#example)中），其中包含一份沒有 `rating` 欄位的文件。此彙總會計算有多少產品缺少評分，並包含 `terms` 子彙總以找出這些產品：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "without_rating": {
      "missing": {
        "field": "rating"
      },
      "aggs": {
        "names": {
          "terms": {
            "field": "name.keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應顯示有一項產品 (Product C) 缺少 `rating` 欄位：

```json
{
  "took": 9,
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
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "without_rating": {
      "doc_count": 1,
      "names": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "Product C",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 缺少指定欄位的文件數量。 |
