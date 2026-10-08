---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最小值"
parent: Metric aggregations
nav_order: 70
redirect_from:
  - /query-dsl/aggregations/metric/minimum/
---

# 最小值彙總

`min` 指標是一種單一值指標，會回傳欄位的最小值。

`min` 彙總會使用 `double`（雙精確度）表示法來比較數值欄位。由於 `double` 尾數的有效位元數為 53，對於包含絕對值大於 2<sup>53</sup> 的 `long` 或 `unsigned_long` 整數的欄位，結果應視為近似值。
{: .note}

## 參數

`min` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型      | 說明 |
| :--       | :--               | :--            | :--         |
| `field`   | 必要          | 字串         | 要計算最小值的欄位名稱。    |
| `missing` | 選用          | 數值        | 指派給欄位缺失實例的值。若未提供，包含缺失值的文件將不納入彙總。 |

## 範例

下列範例請求會在 OpenSearch Dashboards 電子商務範例資料中，找出最便宜的商品，也就是 `base_unit_price` 值最小的商品：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "min_base_unit_price": {
      "min": {
        "field": "products.base_unit_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

如下列範例回應所示，彙總會回傳 `products.base_unit_price` 的最小值：

```json
{
  "took": 15,
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
    "min_base_unit_price": {
      "value": 5.98828125
    }
  }
}
```

您可以使用彙總名稱（`min_base_unit_price`）作為鍵，從回應中取得該彙總。

## 缺失值

您可以為彙總欄位的缺失實例指派一個值。如需更多資訊，請參閱[缺失值彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)。

`min` 通常會忽略缺失值。如果您使用 `missing` 指派一個比任何現有值都低的值，`min` 會將此替代值作為最小值回傳。
