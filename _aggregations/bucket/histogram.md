---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "直方圖"
parent: Bucket aggregations
nav_order: 100
redirect_from:
  - /query-dsl/aggregations/bucket/histogram/
---

# 直方圖彙總

`histogram` 彙總會將數值欄位的值範圍劃分為固定寬度的區間，並計算每個區間中的文件數量。每個桶 (bucket) 的 `key` 代表該區間的下限，計算方式為 `Math.floor((value - offset) / interval) * interval + offset`。

## 參數

`histogram` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要進行彙總的數值欄位。 |
| `interval` | 必要 | 數字 | 每個桶的寬度。必須為正值。 |
| `min_doc_count` | 選用 | 整數 | 桶出現在回應中所需的最少文件數量。設定為 `1` 可省略空的桶。預設為 `0`（包含空的桶）。 |
| `extended_bounds` | 選用 | 物件 | 確保從 `min` 到 `max` 都存在桶，即使該範圍內沒有任何文件。不會篩除超出邊界的桶——若要排除範圍以外的桶，請使用 `hard_bounds` 或範圍查詢。接受 `min` 和 `max` 值。僅在 `min_doc_count` 為 `0` 時才有意義。 |
| `hard_bounds` | 選用 | 物件 | 限制回應中桶的範圍。接受 `min` 和 `max` 值。超出這些邊界的桶會被排除。 |
| `offset` | 選用 | 數字 | 依指定的量位移桶的邊界。必須介於 [0, `interval`) 範圍內。預設為 `0`。 |
| `keyed` | 選用 | 布林值 | 為 `true` 時，會將桶以物件形式傳回，並以桶值作為索引鍵，而非以陣列形式傳回。預設為 `false`。 |
| `order` | 選用 | 物件 | 控制桶的排序順序。接受 `_key` 或 `_count`，並各自搭配 `asc` 或 `desc`。預設為 `{"_key": "asc"}`。 |
| `missing` | 選用 | 數字 | 要指派給缺少目標欄位之文件的值，會將這些文件放入對應的桶中。預設會忽略缺少該欄位的文件。 |

對[數值範圍欄位]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/range/)而非單一值數值欄位進行彙總時，一份文件可能會出現在多個桶中——其下限與上限之間的每個區間各一個。
{: .note}

## 範例：基本直方圖

下列範例會將電子商務訂單總額分組為 $50 的區間，並僅顯示至少包含一份文件的桶：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_histogram": {
      "histogram": {
        "field": "taxful_total_price",
        "interval": 50,
        "min_doc_count": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用 offset 位移桶的邊界

`offset` 參數會位移桶邊界的起始位置。下列範例使用 `10` 的位移量，因此桶的起始點為 10、60、110 等，而非 0、50、100：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_histogram": {
      "histogram": {
        "field": "taxful_total_price",
        "interval": 50,
        "offset": 10,
        "min_doc_count": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

下列回應對應基本直方圖範例：

```json
{
  "took": 2,
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
    "price_histogram": {
      "buckets": [
        {
          "key": 0.0,
          "doc_count": 1633
        },
        {
          "key": 50.0,
          "doc_count": 2036
        },
        {
          "key": 100.0,
          "doc_count": 724
        },
        {
          "key": 150.0,
          "doc_count": 205
        },
        {
          "key": 200.0,
          "doc_count": 53
        },
        {
          "key": 250.0,
          "doc_count": 14
        },
        {
          "key": 300.0,
          "doc_count": 7
        },
        {
          "key": 350.0,
          "doc_count": 2
        },
        {
          "key": 2250.0,
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列或物件 | 直方圖的桶。預設以陣列形式傳回；當 `keyed` 為 `true` 時，則以物件形式傳回。 |
| `buckets.key` | 雙精度浮點數 | 桶區間的下限。 |
| `buckets.doc_count` | 整數 | 桶中的文件數量。 |
