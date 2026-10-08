---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Percentile
parent: Metric aggregations
nav_order: 90
redirect_from:
  - /query-dsl/aggregations/metric/percentile/
---

# Percentile 彙總

`percentiles` 彙總用於估計數值欄位在給定百分位數的值。這對於理解分佈邊界非常有用。

例如，`load_time` = `120ms` 的第 95 個百分位數意味著 95% 的值小於或等於 120 ms。

與 [`cardinality`]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/) 指標類似，`percentile` 指標是近似值。

## 參數

`percentiles` 彙總使用以下參數。

| 參數                                | 資料類型        | 必要/選用 | 說明                                                                                                                 |
| ---------------------------------------- | ---------------- | -------- | --------------------------------------------------------------------------------------------------------------------------- |
| `field`                                  | 字串           | 必要      | 用於計算百分位數的數值欄位。                                                                                    |
| `percents`                               | Double 陣列 | 選用       | 回應中回傳的百分位數清單。預設為 `[1, 5, 25, 50, 75, 95, 99]`。                                                 |
| `keyed`                                  | 布林值          | 選用       | 如果設定為 `false`，則將結果以陣列形式回傳。否則，將結果以 JSON 物件形式回傳。預設為 `true`。 |
| `tdigest.compression`                    | Double           | 選用       | 控制 `tdigest` 演算法的準確度和記憶體使用量。請參閱 [使用 `tdigest` 調整精確度](#precision-tuning-with-tdigest)。                                      |
| `hdr.number_of_significant_value_digits` | 整數          | 選用       | HDR 直方圖的精確度設定。請參閱 [HDR 直方圖](#hdr-histogram)。                                   |
| `missing`                                | 數字           | 選用       | 當文件中缺少目標欄位時使用的預設值。                                                                              |
| `script`                                 | 物件           | 選用       | 用於計算自訂值而非使用欄位的指令碼。支援內嵌指令碼和儲存指令碼。                                |

## 範例



首先，建立一個索引：

```json
PUT /latency_data
{
  "mappings": {
    "properties": {
      "load_time": {
        "type": "double"
      }
    }
  }
}
```
{% include copy-curl.html %}

新增範例數值以說明百分位數計算：

```json
POST /latency_data/_bulk
{ "index": {} }
{ "load_time": 20 }
{ "index": {} }
{ "load_time": 40 }
{ "index": {} }
{ "load_time": 60 }
{ "index": {} }
{ "load_time": 80 }
{ "index": {} }
{ "load_time": 100 }
{ "index": {} }
{ "load_time": 120 }
{ "index": {} }
{ "load_time": 140 }
```

{% include copy-curl.html %}

### Percentiles 彙總

以下範例計算 `load_time` 欄位的預設百分位數集：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time"
      }
    }
  }
}
```
{% include copy-curl.html %}

預設情況下，會回傳第 1、5、25、50、75、95 和 99 個百分位數：

```json
{
  ...
  "aggregations": {
    "load_time_percentiles": {
      "values": {
        "1.0": 20,
        "5.0": 20,
        "25.0": 40,
        "50.0": 80,
        "75.0": 120,
        "95.0": 140,
        "99.0": 140
      }
    }
  }
}
```

## 自訂百分位數

您可以使用 `percents` 陣列指定確切的百分位數：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time",
        "percents": [50, 90, 99]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應僅包含三個請求的百分位數彙總：

```json
{
  ...
  "aggregations": {
    "load_time_percentiles": {
      "values": {
        "50.0": 80,
        "90.0": 140,
        "99.0": 140
      }
    }
  }
}
```

### 鍵值回應

您可以透過將 `keyed` 參數設定為 `false`，將回傳彙總的格式從 JSON 物件更改為鍵值對清單：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time",
        "keyed": false
      }
    }
  }
}
```
{% include copy-curl.html %}

回應將百分位數以值陣列的形式提供：

```json
{
  ...
  "aggregations": {
    "load_time_percentiles": {
      "values": [
        {
          "key": 1,
          "value": 20
        },
        {
          "key": 5,
          "value": 20
        },
        {
          "key": 25,
          "value": 40
        },
        {
          "key": 50,
          "value": 80
        },
        {
          "key": 75,
          "value": 120
        },
        {
          "key": 95,
          "value": 140
        },
        {
          "key": 99,
          "value": 140
        }
      ]
    }
  }
}
```

<!-- vale off -->

### 使用 tdigest 調整精確度

<!-- vale on -->

`tdigest` 演算法是計算百分位數的預設方法。它提供了一種記憶體效率高的方式來估計百分位數排名，特別是在處理回應時間或延遲等浮點數資料時。

與精確的百分位數計算不同，`tdigest` 使用機率方法將值分組為 _centroids_（質心）——即總結分佈的小型叢集。這種方法能夠在不需要將所有原始資料儲存在記憶體中的情況下，對大多數百分位數提供準確的估計。

該演算法的設計旨在使分佈的尾端——低百分位數（例如第 1 個）和高百分位數（例如第 99 個）——具有高度準確性，這對於效能分析通常是最重要的。您可以使用 `compression` 參數控制結果的精確度。

較高的 `compression` 值意味著使用更多的質心，這會增加準確度（尤其是在尾端），但需要更多的記憶體和 CPU。較低的 `compression` 值會減少記憶體使用量並加快執行速度，但結果的準確度可能會降低。


在以下情況下使用 `tdigest`：

* 您的資料包含浮點數值，例如回應時間、延遲或持續時間。
* 您需要在極端百分位數（例如第 1 或第 99 個）獲得準確的結果。

在以下情況下避免使用 `tdigest`：

* 您僅處理整數資料且希望獲得最高速度。
* 您較不在意分佈尾端的準確度，而更偏好更快的彙總（請考慮改用 [`hdr`](#hdr-histogram)）。

 以下範例將 `tdigest.compression` 設定為 `200`：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time",
        "tdigest": {
          "compression": 200
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### HDR 直方圖

高動態範圍 (HDR) 直方圖是計算百分位數的另一種選擇，可用於替代 [`tdigest`](#precision-tuning-with-tdigest)。它在處理大型資料集和延遲測量時特別有用。它旨在提高速度，並在維持固定且可設定的精確度水準的同時，支援寬廣的數值動態範圍。

與 [`tdigest`](#precision-tuning-with-tdigest) 不同（後者在分佈的尾端即極端百分位數提供更高的準確度），HDR 優先考慮速度以及在整個範圍內的統一準確度。當桶 (bucket) 數量較多且不需要對罕見值進行極端精確計算時，其效果最佳。

例如，如果您測量從 1 微秒到 1 小時的回應時間，並將 HDR 設定為 3 位有效數字，則對於最高 1 毫秒的值，其記錄精確度為 ±1 微秒；對於接近 1 小時的值，精確度為 ±3.6 秒。

這種權衡使得 HDR 比 [`tdigest`](#precision-tuning-with-tdigest) 快得多，且更消耗記憶體。

下表顯示了 HDR 有效數字的細分。

| 有效數字 | 相對精確度 (最大誤差) |
| ------------------ | ------------------------------ |
| 1                  | 10 分之 1       = 10%       |
| 2                  | 100 分之 1      = 1%        |
| 3                  | 1,000 分之 1    = 0.1%      |
| 4                  | 10,000 分之 1   = 0.01%     |
| 5                  | 100,000 分之 1  = 0.001%    |

如果您符合以下條件，應使用 HDR：

* 正在對許多桶進行彙總。
* 不需要尾端百分位數的極端精確度。
* 有足夠的可用記憶體。

如果您符合以下條件，應避免使用 HDR：

* 尾端準確度很重要。
* 您正在分析偏斜或稀疏的資料分佈。

以下範例將 `hdr.number_of_significant_value_digits` 設定為 `3`：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time",
        "hdr": {
          "number_of_significant_value_digits": 3
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 缺失值

使用 `missing` 設定來為不包含目標欄位的文件設定後備值：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_percentiles": {
      "percentiles": {
        "field": "load_time",
        "missing": 0
      }
    }
  }
}
```
{% include copy-curl.html %}

## 指令碼

您可以透過指令碼動態計算值，而不是指定欄位。當您需要套用轉換（例如轉換貨幣或套用權重）時，這非常有用。

### 內嵌指令碼

使用指令碼來計算衍生值：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "adjusted_percentiles": {
      "percentiles": {
        "script": {
          "source": "doc['load_time'].value * 1.2"
        },
        "percents": [50, 95]
      }
    }
  }
}
```
{% include copy-curl.html %}

### 儲存指令碼


首先，使用以下請求建立一個範例指令碼：

```json
POST _scripts/load_script
{
  "script": {
    "lang": "painless",
    "source": "doc[params.field].value * params.multiplier"
  }
}
```
{% include copy-curl.html %}
{% include copy-curl.html %}

然後在 `percentiles` 彙總中使用該儲存指令碼，並提供儲存指令碼所需的 `params`：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "adjusted_percentiles": {
      "percentiles": {
        "script": {
          "id": "load_script",
          "params": {
            "field": "load_time",
            "multiplier": 1.2
          }
        },
        "percents": [50, 95]
      }
    }
  }
}
```
{% include copy-curl.html %}
{% include copy-curl.html %}
