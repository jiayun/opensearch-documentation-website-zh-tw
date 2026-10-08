---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最大值"
parent: Metric aggregations
nav_order: 60
redirect_from:
  - /query-dsl/aggregations/metric/maximum/
---

# 最大值彙總

`max` 指標是一種單值指標，會回傳某個欄位的最大值。

`max` 彙總使用 `double`（雙精度）表示法來比較數值欄位。對於包含大於 2<sup>53</sup> 的 `long` 或 `unsigned_long` 整數值的欄位，結果應被視為近似值，因為 `double` 尾數的有效位元數為 53。
{: .note}

## 參數

`max` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :-- | :-- | :-- | :-- |
| `field` | 必要 | String | 要計算最大值的欄位名稱。 |
| `missing` | 選用 | Numeric | 指派給遺漏該欄位之實例的值。如果未提供，則包含遺漏值的文件將從彙總中省略。 |

## 範例

以下範例請求在 OpenSearch Dashboards 的電子商務範例資料中，尋找最昂貴的項目——即 `base_unit_price` 具有最大值的項目：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "max_base_unit_price": {
      "max": {
        "field": "products.base_unit_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

如下方範例回應所示，該彙總回傳了 `products.base_unit_price` 的最大值：

```json
{
  "took": 24,
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
    "max_base_unit_price": {
      "value": 540
    }
  }
}
```

您可以使用彙總名稱（`max_base_unit_price`）作為鍵，從回應中檢索該彙總。

## 遺漏值

您可以為彙總欄位遺漏的實例指派一個值。請參閱 [遺漏值彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/) 以取得更多資訊。

遺漏值通常會被 `max` 忽略。如果您使用 `missing` 指派一個大於任何現有值的數值，則 `max` 會將此替換值作為最大值回傳。
