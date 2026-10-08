---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可變寬度直方圖"
parent: Bucket aggregations
nav_order: 210
---

# 可變寬度直方圖彙總

`variable_width_histogram` 彙總將數值欄位的值劃分為目標數量的桶，其寬度會根據資料自動調整。桶的邊界是透過對值進行分群 (clustering) 來衍生的，因此值範圍中較密集的部分會被劃分為窄桶，而稀疏的部分則由寬桶覆蓋。請將此彙總用於分佈不均的資料，對於這類資料，在 [`histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/) 彙總中使用固定的 `interval` 會導致產生許多幾乎為空的桶，或者只有少數幾個桶包含幾乎所有文件。

每個分片會緩衝其收集到的前 `initial_buffer` 個值，對其進行排序，並將其劃分為數量等於 `shard_size` 四分之三的初始分群。它將每個剩餘的值分配給最近的分群，除非該值與所有分群中心點 (centroids) 之間的距離都超過相鄰分群中心點平均距離的兩倍，且該分片擁有的分群數量少於 `shard_size`，在這種情況下，分片會啟動一個新分群。協調節點會收集所有分片的分群，並重複合併中心點最近的兩個分群，直到剩下 `buckets` 個為止。

## 參數

`variable_width_histogram` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要進行彙總的數值欄位。請提供 `field` 或 `script`。 |
| `buckets` | 選用 | 整數 | 目標桶數量。必須大於 `0` 且不能超過 `search.max_buckets` 設定。當值無法分開成這麼多個分群時，回應中包含的桶數量可能會少於請求的數量。預設值為 `10`。 |
| `shard_size` | 選用 | 整數 | 每個分片在將結果發送到協調節點之前建立的分群數量。必須大於 `1`。較大的值會在每個分片上產生較小的分群，這能減少最終桶之間的重疊，並更準確地定位其邊界，但會增加分片上使用的記憶體以及傳輸到協調節點的資料量。預設值為 `buckets` 乘以 `50`。 |
| `initial_buffer` | 選用 | 整數 | 每個分片在計算初始分群邊界之前緩衝的值數量。必須大於或等於 `buckets`。較大的緩衝區能從更具代表性的資料樣本中衍生出初始邊界，但會使用更多記憶體。預設值為 `shard_size` 乘以 `10` 與 `50000` 兩者中的較小值。 |
| `script` | 選用 | 物件 | 用於產生要彙總之數值的指令碼。請提供 `field` 或 `script`。 |
| `missing` | 選用 | 數字 | 分配給缺失目標欄位之文件的值。預設情況下，會忽略缺失此欄位的文件。 |
| `format` | 選用 | 字串 | 應用於 `min`、`key` 和 `max` 的 [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式化字串。在額外的 `min_as_string`、`key_as_string` 和 `max_as_string` 回應欄位中返回格式化後的輸出。 |

## 範例

以下範例將電子商務訂單總額分組為五個可變寬度的桶：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_buckets": {
      "variable_width_histogram": {
        "field": "taxful_total_price",
        "buckets": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 17,
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
    "price_buckets": {
      "buckets": [
        {
          "min": 6.98828125,
          "key": 59.14907207464146,
          "max": 105.46875,
          "doc_count": 3835
        },
        {
          "min": 105.46875,
          "key": 139.096796875,
          "max": 229.5,
          "doc_count": 800
        },
        {
          "min": 229.5,
          "key": 247.11111111111111,
          "max": 304.0,
          "doc_count": 27
        },
        {
          "min": 304.0,
          "key": 318.4,
          "max": 308.0,
          "doc_count": 5
        },
        {
          "min": 308.0,
          "key": 563.25,
          "max": 2250.0,
          "doc_count": 8
        }
      ]
    }
  }
}
```

覆蓋價格範圍低端密集區域的桶寬度僅為數十美元，而最後一個桶則跨越近 2,000 美元，以覆蓋少數最高金額的訂單。

## 範例：巢狀子彙總

與其他桶彙總一樣，`variable_width_histogram` 接受子彙總。以下範例計算每個價格桶中訂購項目的平均數量：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "price_buckets": {
      "variable_width_histogram": {
        "field": "taxful_total_price",
        "buckets": 3
      },
      "aggs": {
        "avg_quantity": {
          "avg": {
            "field": "total_quantity"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含每個桶的子彙總結果：

```json
{
  "aggregations": {
    "price_buckets": {
      "buckets": [
        {
          "min": 6.98828125,
          "key": 73.45130757286513,
          "max": 246.0,
          "doc_count": 4649,
          "avg_quantity": {
            "value": 2.1559475155947516
          }
        },
        {
          "min": 246.0,
          "key": 281.9166666666667,
          "max": 370.0,
          "doc_count": 24,
          "avg_quantity": {
            "value": 2.7083333333333335
          }
        },
        {
          "min": 393.0,
          "key": 1321.5,
          "max": 2250.0,
          "doc_count": 2,
          "avg_quantity": {
            "value": 1.5
          }
        }
      ]
    }
  }
}
```

## 回應本文欄位

下表列出了回應本文的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列 | 可變寬度的桶，按 `key` 升序排序。 |
| `buckets.min` | 雙精度浮點數 | 桶的下限。 |
| `buckets.key` | 雙精度浮點數 | 桶中值的平均值。 |
| `buckets.max` | 雙精度浮點數 | 桶的上限。 |
| `buckets.doc_count` | 整數 | 桶中的文件數量。 |
| `buckets.min_as_string` | 字串 | 根據 `format` 格式化後的桶下限。僅在設定 `format` 時返回。 |
| `buckets.key_as_string` | 字串 | 根據 `format` 格式化後的桶中值平均值。僅在設定 `format` 時返回。 |
| `buckets.max_as_string` | 字串 | 根據 `format` 格式化後的桶上限。僅在設定 `format` 時返回。 |

## 限制

`variable_width_histogram` 彙總有以下限制：

- 該彙總不能巢狀在收集多個桶的父彙總內部。使用 [`terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)、[`histogram`]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/)、[`range`]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/) 或 [`filters`]({{site.url}}{{site.baseurl}}/aggregations/bucket/filters/) 作為父彙總會返回以下錯誤：

  ```
  [variable_width_histogram] cannot be nested inside an aggregation that collects more than a single bucket.
  ```

  支援單桶父彙總，例如 [`filter`]({{site.url}}{{site.baseurl}}/aggregations/bucket/filter/)、[`global`]({{site.url}}{{site.baseurl}}/aggregations/bucket/global/) 和 [`nested`]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/)。
- 當該彙總具有需要文件分數的子彙總（例如 [`top_hits`]({{site.url}}{{site.baseurl}}/aggregations/metric/top-hits/)）時，不能作為 [`nested`]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/) 彙總的子彙總執行。這種組合會返回錯誤。
- 不支援 `keyed` 參數，因此桶始終以陣列形式返回。
- `min` 和 `max` 邊界是近似值。在合併分群時，如果兩個分群的中心點相距較遠，OpenSearch 可能會將邊界重疊的兩個分群保留為獨立的桶。接著它會將兩個桶之間的邊界設定為重疊部分的中點，因此邊界不一定是資料中存在的值，且較低的桶包含的值比其邊界所示的更多，而較高的桶包含的值較少。以這種方式降低桶的 `max` 可能會使其低於桶自身的 `key`（即桶中值的平均值）。第一個範例回應中的第四個桶由於這個原因，報告的 `key` 為 `318.4`，而 `max` 為 `308.0`。此合併步驟在單分片索引和多分片索引上都會執行。
- 桶是不連續的。每個桶的邊界是其包含的最小值和最大值，因此資料中的間隙會表現為相鄰桶之間的間隙。在子彙總範例回應中，一個桶在 `370.0` 結束，而下一個桶在 `393.0` 開始。
- 桶邊界對離群值很敏感。少數極端值會使桶跨越寬廣的資料範圍：第一個範例回應中的最後一個桶跨越 `308.0` 到 `2250.0` 以包含 8 筆訂單。
- 桶邊界取決於每個分片收集值的順序，因此即使值分佈保持不變，邊界也可能隨著分段 (segments) 合併或文件新增而改變。
