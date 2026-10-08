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

`median_absolute_deviation` 彙總是一種單值指標彙總。中位數絕對偏差是一種變異性指標，用於衡量與中位數的離散程度。

中位數絕對偏差比標準差較少受到離群值的影響，因為標準差依賴於平方誤差項；因此，中位數絕對偏差可用於描述非常態分佈的資料。

中位數絕對偏差的計算方式如下：

```
median_absolute_deviation = median( | x<sub>i</sub> - median(x<sub>i</sub>) | )
```


由於記憶體限制，OpenSearch 會估算 `median_absolute_deviation` 而非直接計算。此估算過程在計算上成本較高。您可以調整估算準確度與效能之間的權衡。如需更多資訊，請參閱 [調整估算準確度](https://github.com/opensearch-project/documentation-website/pull/9453/files#adjusting-estimation-accuracy)。

## 參數

`median_absolute_deviation` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :-- | :-- | :-- | :-- |
| `field` | 必要 | String | 要計算中位數絕對偏差的數值欄位名稱。 |
| `missing` | 選用 | Numeric | 指派給欄位遺漏實例的值。如果未提供，則在估算中會省略具有遺漏值的文件。 |
| `compression` | 選用 | Numeric | 用於 [調整估算準確度與效能之間平衡](#adjusting-estimation-accuracy) 的參數。`compression` 的值必須大於 `0`。預設值為 `1000`。 |

## 範例

以下範例計算 `opensearch_dashboards_sample_data_flights` 資料集中 `DistanceMiles` 欄位的中位數絕對偏差：

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

#### 範例回應

如以下範例回應所示，該彙總在 `median_absolute_deviation_DistanceMiles` 變數中回傳中位數絕對偏差的估計值：

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

## 遺漏值

OpenSearch 在計算 `median_absolute_deviation` 時會忽略遺漏值和 null 值。

您可以為彙總欄位的遺漏實例指派一個值。如需更多資訊，請參閱 [遺漏值彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)。

## 調整估算準確度

中位數絕對偏差是使用 [t-digest](https://github.com/tdunning/t-digest/tree/main) 資料結構計算的，該結構使用 `compression` 參數來平衡效能與估算準確度。較低的 `compression` 值可提高效能，但可能會降低估算準確度，如下方請求所示：

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

估算誤差取決於資料集，但通常低於 5%，即使 `compression` 值低至 `100` 也是如此。（此處使用較低的範例值 `10` 是為了說明權衡效果，並不建議使用。）

請注意以下回應中減少的計算時間（`took` 時間）以及估算參數值準確度的輕微下降。

作為參考，OpenSearch 對於 `DistanceMiles` 中位數絕對偏差的最佳估計值（將 `compression` 設定為極高值）為 `1831.076904296875`：


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
