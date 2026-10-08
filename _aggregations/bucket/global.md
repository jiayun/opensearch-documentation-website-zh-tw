---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Global
parent: Bucket aggregations
nav_order: 90
redirect_from:
  - /query-dsl/aggregations/bucket/global/
---

# Global 彙總

`global` 彙總會建立單一桶 (bucket)，其中包含索引中的所有文件，不受搜尋查詢影響。巢狀於 `global` 內的子彙總會針對完整的文件集運作，讓您可以在同一個請求中比較篩選後的指標與整體指標。

`global` 彙總只能放置為最上層彙總。將其巢狀於其他桶彙總內不會有任何效果。
{: .note}

## 範例

以下範例會在單一請求中計算兩個平均值：一個限定於查詢範圍 (低於 $50 的訂單)，另一個則使用 `global` 彙總計算所有文件的平均值：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "range": {
      "taxful_total_price": {
        "lte": 50
      }
    }
  },
  "aggs": {
    "total_avg_amount": {
      "global": {},
      "aggs": {
        "avg_price": {
          "avg": {
            "field": "taxful_total_price"
          }
        }
      }
    },
    "filtered_avg": {
      "avg": {
        "field": "taxful_total_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "took": 19,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1633,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "total_avg_amount": {
      "doc_count": 4675,
      "avg_price": {
        "value": 75.05542864304813
      }
    },
    "filtered_avg": {
      "value": 38.363175998928355
    }
  }
}
```

`total_avg_amount` 彙總回報所有 4,675 份文件的平均值 ($75.06)，而 `filtered_avg` 僅回報符合查詢的 1,633 份文件的平均值 ($38.36)。

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 索引中的文件總數，與搜尋查詢無關。 |
