---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "具名查詢"
nav_order: 77
---

# 具名查詢

任何查詢子句都可以包含 `_name` 參數，為該子句指派標籤。當文件相符時，回應會包含 `matched_queries` 陣列，列出所有對該次相符有貢獻的查詢子句名稱。這對於辨識複雜查詢中符合特定文件的部分很有用。

## 範例

下列查詢在 `bool` 查詢內使用兩個具名的 `match` 子句。每個子句都有一個用於識別它的 `_name`：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 2,
  "_source": ["products.product_name", "customer_full_name"],
  "query": {
    "bool": {
      "should": [
        {"match": {"products.product_name": {"query": "shirt", "_name": "shirt_query"}}},
        {"match": {"products.product_name": {"query": "dress", "_name": "dress_query"}}}
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

每個命中項目中的 `matched_queries` 陣列會顯示哪些具名子句符合該文件：

```json
{
  "took": 16,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1746,
      "relation": "eq"
    },
    "max_score": 1.8150847,
    "hits": [
      {
        "_index": "opensearch_dashboards_sample_data_ecommerce",
        "_id": "aoN5u50BpPQaFxRehbyq",
        "_score": 1.8150847,
        "_source": {
          "customer_full_name": "Stephanie Reyes",
          "products": [
            {
              "product_name": "Shirt - black/white"
            },
            {
              "product_name": "Cocktail dress / Party dress - navy"
            }
          ]
        },
        "matched_queries": [
          "shirt_query",
          "dress_query"
        ]
      },
      {
        "_index": "opensearch_dashboards_sample_data_ecommerce",
        "_id": "fYN5u50BpPQaFxRehLqd",
        "_score": 1.6545942,
        "_source": {
          "customer_full_name": "Clarice Daniels",
          "products": [
            {
              "product_name": "Summer dress - grey"
            },
            {
              "product_name": "Shirt - black/white"
            }
          ]
        },
        "matched_queries": [
          "shirt_query",
          "dress_query"
        ]
      }
    ]
  }
}
```

## 回應本文欄位

下表列出具名查詢專屬的回應欄位。

| 欄位 | 說明 |
| :--- | :--- |
| `matched_queries` | 字串陣列，列出所有符合此文件的查詢子句的 `_name` 值。只有在至少一個具名子句相符時才會出現。 |