---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Filter
parent: Bucket aggregations
nav_order: 50
redirect_from:
  - /query-dsl/aggregations/bucket/filter/
---

# Filter 彙總

`filter` 彙總會建立單一桶 (bucket)，其中包含所有符合指定查詢的文件。任何查詢子句（`match`、`term`、`range`、`bool` 等）都可以作為篩選條件。巢狀於 `filter` 彙總內的子彙總只會針對符合條件的文件進行運算，因此很適合用來將耗費資源的計算限縮在相關的子集合上。

若要同時將文件篩選至多個具名桶中，請參閱 [`filters` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/filters/)。

## 範例

下列範例將 `avg` 子彙總包裝在 `range` 篩選條件內，以計算所有金額低於 $50 之訂單的平均訂單總額：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "low_value": {
      "filter": {
        "range": {
          "taxful_total_price": {
            "lte": 50
          }
        }
      },
      "aggs": {
        "avg_amount": {
          "avg": {
            "field": "taxful_total_price"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "took": 43,
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
    "low_value": {
      "doc_count": 1633,
      "avg_amount": {
        "value": 38.363175998928355
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 符合篩選查詢的文件數量。 |
