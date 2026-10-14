---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "缺失彙總"
parent: Bucket aggregations
nav_order: 120
redirect_from:
  - /query-dsl/aggregations/bucket/missing/
---

# Missing 彙總

`missing` 彙總會建立一個單一桶 (bucket)，其中包含指定欄位沒有值的所有文件。如果欄位不存在、為 `null` 或空陣列，則該文件視為缺失。如果欄位對應定義了 [`null_value`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/null-value/)，明確的 `null` 值會以該值編製索引，因此不會被視為缺失。此彙總通常與其他桶彙總搭配使用，以涵蓋因缺少必要欄位而無法歸入任何其他桶的文件。

## 參數

`missing` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要檢查是否有缺失值的欄位。 |

如果指定的欄位未在索引中建立對應，則每份文件都會被計為缺失，且不會回傳錯誤。因此，拼錯的欄位名稱會產生一個包含所有文件的桶。如果 `doc_count` 等於文件總數，請確認欄位名稱。
{: .note}

## 範例

下列請求將三個產品編製索引到 `product_ratings` 索引中。產品 C 沒有 `rating` 欄位：

```json
POST product_ratings/_bulk?refresh
{ "index": { "_id": "1" } }
{ "name": "Product A", "rating": 4.5, "num_reviews": 100 }
{ "index": { "_id": "2" } }
{ "name": "Product B", "rating": 3.8, "num_reviews": 50 }
{ "index": { "_id": "3" } }
{ "name": "Product C" }
```
{% include copy-curl.html %}

下列彙總會計算有多少產品缺少評分，並包含一個 `terms` 子彙總來識別它們：

```json
GET /product_ratings/_search
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

## 回應範例

回應顯示有一個產品（產品 C）缺少 `rating` 欄位：

```json
{
  ...
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

下表列出回應本文的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 缺少指定欄位的文件數量。 |
