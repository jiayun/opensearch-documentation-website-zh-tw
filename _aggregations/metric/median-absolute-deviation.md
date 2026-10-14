---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "中位數絕對偏差"
parent: Metric aggregations
nav_order: 65
redirect_from:
  - /query-dsl/aggregations/metric/median-absolute-deviation/
---

# 中位數絕對偏差彙總

`median_absolute_deviation` 彙總是一種單一數值指標彙總。中位數絕對偏差是一種變異性指標，用來衡量資料偏離中位數的離散程度。

標準差依賴誤差平方項，而中位數絕對偏差比標準差更不容易受到離群值影響，適合用來描述非常態分布的資料。

中位數絕對偏差的計算方式如下：

```
median_absolute_deviation = median( | x<sub>i</sub> - median(x<sub>i</sub>) | )
```


由於記憶體限制，OpenSearch 會估計 `median_absolute_deviation`，而非直接計算。此估計的運算成本很高。您可以調整估計準確度與效能之間的取捨。如需更多資訊，請參閱[調整估計準確度](https://github.com/opensearch-project/documentation-website/pull/9453/files#adjusting-estimation-accuracy)。

## 參數

`median_absolute_deviation` 彙總採用下列參數。

| 參數 | 必要/選用 | 資料類型      | 說明 |
| :--       | :--               | :--            | :--         |
| `field`   | 必要          | 字串         | 要計算中位數絕對偏差的數值欄位名稱。 |
| `missing` | 選用          | 數值        | 欄位值缺失時要使用的值。若未提供，估計時會略過缺少該欄位值的文件。 |
| `compression` | 選用          | 數值        | 用來[調整估計準確度與效能之間平衡](#adjusting-estimation-accuracy)的參數。`compression` 的值必須大於 `0`。預設值為 `1000`。 |

## 範例

下列範例會計算 `opensearch_dashboards_sample_data_flights` 資料集中 `DistanceMiles` 欄位的中位數絕對偏差：

```json
GET opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "median_absolute_deviation_DistanceMiles": {
      "median_absolute_deviation": {
        "field": "DistanceMiles"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

如下列範例回應所示，該彙總會在 `median_absolute_deviation_DistanceMiles` 變數中傳回中位數絕對偏差的估計值：

```json
{
  "took": 490,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "median_absolute_deviation_DistanceMiles": {
      "value": 1830.917892238693
    }
  }
}
```

## 缺少值

OpenSearch 在計算 `median_absolute_deviation` 時會忽略缺少值和 null 值。

您可以為缺少彙總欄位值的文件指定一個值。如需更多資訊，請參閱[缺少值彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)。

## 調整估計準確度

中位數絕對偏差是使用 [t-digest](https://github.com/tdunning/t-digest/tree/main) 資料結構計算，該結構採用 `compression` 參數來平衡效能與估計準確度。較低的 `compression` 值可提升效能，但可能降低估計準確度，如下列請求所示：

```json
GET opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "median_absolute_deviation_DistanceMiles": {
      "median_absolute_deviation": {
        "field": "DistanceMiles",
        "compression": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

估計誤差取決於資料集，但通常低於 5%，即使 `compression` 值低至 `100` 亦然。（此處使用偏低的範例值 `10` 是為了說明取捨效果，並不建議使用。）

請注意下列回應中減少的運算時間（`took` 時間），以及估計參數值略微降低的準確度。

供參考，OpenSearch 對 `DistanceMiles` 中位數絕對偏差的最佳估計值（將 `compression` 任意設高）為 `1831.076904296875`：


```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "median_absolute_deviation_DistanceMiles": {
      "value": 1836.265614211182
    }
  }
}
```
