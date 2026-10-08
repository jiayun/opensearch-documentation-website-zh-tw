---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Range
parent: Bucket aggregations
nav_order: 150
redirect_from:
  - /query-dsl/aggregations/bucket/range/
---

# Range 彙總

`range` 彙總根據您定義的值範圍將文件分組到桶 (bucket) 中。每個桶會擷取其欄位值落在指定 `from` (包含) 與 `to` (不包含) 邊界內的文件。與自動建立均勻間隔的 [`histogram` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/) 不同，`range` 允許您定義任意的、非均勻的邊界。

## 參數

`range` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 選用 | 字串 | 要進行彙總的數值欄位。必須提供 `field` 或 `script` 其中之一。 |
| `script` | 選用 | 物件 | 用於產生彙總值的指令碼。必須提供 `field` 或 `script` 其中之一。當與 `field` 搭配使用時，該指令碼作為值指令碼運作，並將欄位值作為 `_value` 接收。 |
| `ranges` | 必要 | 陣列 | 範圍邊界的清單。每個項目可以包含 `from`、`to`，以及選用的 `key`。 |
| `keyed` | 選用 | 布林值 | 當 `true` 時，會將桶以範圍名稱作為鍵的物件形式傳回，而非陣列。預設值為 `false`。 |
| `missing` | 選用 | 數字 | 用於缺少目標欄位之文件的值。預設情況下，缺少該欄位的文件會被忽略。 |

## 範例：具有子彙總的自訂名稱價格分級

以下範例將電子商務訂單分為三個價格分級，並計算每個分級內的平均訂單價值：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_tiers": {
      "range": {
        "field": "taxful_total_price",
        "keyed": true,
        "ranges": [
          { "key": "budget", "to": 50 },
          { "key": "mid_range", "from": 50, "to": 100 },
          { "key": "premium", "from": 100 }
        ]
      },
      "aggs": {
        "avg_price": {
          "avg": { "field": "taxful_total_price" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應將訂單分組到標記的分級中，並顯示其平均價格：

```json
{
  ...
  "aggregations": {
    "price_tiers": {
      "buckets": {
        "budget": {
          "to": 50.0,
          "doc_count": 1633,
          "avg_price": {
            "value": 38.363175998928355
          }
        },
        "mid_range": {
          "from": 50.0,
          "to": 100.0,
          "doc_count": 2036,
          "avg_price": {
            "value": 72.34457883104126
          }
        },
        "premium": {
          "from": 100.0,
          "doc_count": 1006,
          "avg_price": {
            "value": 140.10288270377734
          }
        }
      }
    }
  }
}
```

## 範例：使用指令碼

您可以使用指令碼代替欄位來即時計算值。以下範例在分桶之前對價格增加 10% 的加價：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "marked_up_tiers": {
      "range": {
        "script": {
          "source": "doc['taxful_total_price'].value * 1.1"
        },
        "ranges": [
          { "to": 55 },
          { "from": 55, "to": 110 },
          { "from": 110 }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用值指令碼轉換欄位值

當您同時指定 `field` 和 `script` 時，指令碼會將每個欄位值作為 `_value` 變數接收。以下範例在評估值落在哪個範圍之前，將美元價格轉換為歐元（匯率為 0.92）：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_in_euros": {
      "range": {
        "field": "taxful_total_price",
        "script": {
          "source": "_value * 0.92"
        },
        "ranges": [
          { "to": 46 },
          { "from": 46, "to": 92 },
          { "from": 92 }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應本文欄位

下表列出了回應本文的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列或物件 | 範圍桶。預設以陣列形式傳回，當 `keyed` 為 `true` 時則以物件形式傳回。 |
| `buckets.key` | 字串 | 自動產生的範圍標籤（例如 `*-50.0` 或 `50.0-100.0`），或指定的自訂鍵。 |
| `buckets.from` | Double | 範圍的下限（包含）。對於沒有下限的開放式範圍，此欄位會被省略。 |
| `buckets.to` | Double | 範圍的上限（不包含）。對於沒有上限的開放式範圍，此欄位會被省略。 |
| `buckets.doc_count` | 整數 | 落在該範圍內的文件數量。 |
