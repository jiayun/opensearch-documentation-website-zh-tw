---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "百分位數"
parent: Metric aggregations
nav_order: 90
redirect_from:
  - /query-dsl/aggregations/metric/percentile/
---

# 百分位數彙總

`percentiles` 彙總會估算數值欄位在指定百分位數上的值。這對於瞭解分佈邊界非常有用。

例如，第 95 百分位數為 `load_time` = `120ms`，表示 95% 的值小於或等於 120 ms。

請在下列情境中使用 `percentiles` 彙總：

- 尋找離群值，例如最慢的 1% 請求。
- 透過比較多個百分位數，判斷資料是否偏斜或具有多個峰值。
- 比平均值或最大值更可靠地描述典型值。例如，單一個非常慢的請求可能會將最大載入時間拉高到遠超過大多數使用者實際體驗的程度。

與 [`cardinality`]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/) 指標類似，`percentiles` 彙總是近似值。如需更多資訊，請參閱 [百分位數精確度](#percentile-accuracy)。

## 參數

`percentiles` 彙總接受下列參數。

| 參數                                | 必要/選用 | 資料類型        | 說明                                                                                                                 |
| ---------------------------------------- | -------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `field`                                  | 必要      | 字串           | 用於計算百分位數的數值欄位。                                                                                    |
| `percents`                               | 選用       | 雙精度浮點數陣列 | 回應中傳回的百分位數清單。每個值必須介於 `0` 與 `100` 之間（含端點）。預設為 `[1, 5, 25, 50, 75, 95, 99]`。                                                 |
| `keyed`                                  | 選用       | 布林值          | 若設為 `false`，則以陣列形式傳回結果；否則以 JSON 物件形式傳回結果。預設為 `true`。 |
| `tdigest.compression`                    | 選用       | 雙精度浮點數           | 控制 `tdigest` 演算法的精確度與記憶體用量。預設為 `100`。請參閱 [使用 `tdigest` 進行精確度調校](#precision-tuning-with-tdigest)。                                      |
| `hdr.number_of_significant_value_digits` | 選用       | 整數          | HDR 直方圖的精確度設定。有效值為 0--5。預設為 `3`。請參閱 [HDR 直方圖](#hdr-histogram)。                                   |
| `missing`                                | 選用       | 數值           | 當文件中缺少目標欄位時所使用的預設值。                                                                              |
| `script`                                 | 選用       | 物件           | 用於計算自訂值（而非使用欄位）的指令碼。支援內嵌與已儲存的指令碼。                                |

您可以在請求中指定 `tdigest` 或 `hdr`，但不可同時指定兩者。
{: .note}

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

加入範例數值以說明百分位數的計算：

```json
POST /latency_data/_bulk?refresh
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

下列範例計算 `load_time` 欄位的預設百分位數集合：

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

預設會傳回第 1、5、25、50、75、95 與 99 百分位數：

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

回應只包含所要求的三個百分位數：

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

## 鍵值型回應

您可以將 `keyed` 參數設為 `false`，將傳回的彙總格式從 JSON 物件改為鍵值對清單：

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

回應會以值陣列的形式提供百分位數：

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

## 選擇演算法

OpenSearch 提供兩種計算百分位數的演算法：`tdigest`（預設）與 HDR 直方圖。`tdigest` 演算法使用的記憶體較少，而 HDR 直方圖速度較快，但使用較多記憶體。

<!-- vale off -->

### 使用 tdigest 進行精確度調校

<!-- vale on -->

`tdigest` 演算法是計算百分位數的預設方法。它提供一種節省記憶體的方式來估算百分位數，尤其是在處理回應時間或延遲等浮點數資料時。

與精確的百分位數計算不同，`tdigest` 採用機率方法，將值分組為 _質心_（centroid）---也就是概括分佈的小型叢集。這種方法無需將所有原始資料儲存在記憶體中，即可對大多數百分位數提供準確的估算。

此演算法的設計在分佈的尾部附近---低百分位數（例如第 1 百分位數）與高百分位數（例如第 99 百分位數）---具有極高的準確度，而這些尾部通常對效能分析最為重要。您可以使用 `compression` 參數控制結果的精確度。

較高的 `compression` 值表示使用更多質心，這會提高準確度（尤其是在尾部），但需要更多記憶體與 CPU。較低的 `compression` 值可減少記憶體用量並加快執行速度，但結果可能較不準確。摘要所使用的記憶體會隨 `compression` 值增加，而與被彙總的值數量無關。

在下列情況使用 `tdigest`：

* 您的資料包含浮點數值，例如回應時間、延遲或持續時間。
* 您需要在極端百分位數（例如第 1 或第 99 百分位數）取得準確的結果。

在下列情況避免使用 `tdigest`：

* 速度比記憶體用量更重要時（請考慮改用 [`hdr`](#hdr-histogram)）。

下列範例將 `tdigest.compression` 設為 `200`：

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

高動態範圍 (HDR) 直方圖是計算百分位數時 [`tdigest`](#precision-tuning-with-tdigest) 的替代方案。在處理大型資料集與延遲測量時特別實用。它的設計著重於速度，並支援廣泛的動態數值範圍，同時維持固定且可設定的精確度等級。

與 [`tdigest`](#precision-tuning-with-tdigest) 不同，後者在分布的尾部（極端百分位數）提供更高的準確度，HDR 則優先考量速度以及整個範圍內一致的精確度。當桶的數量很大，且不需要對罕見數值提供極高精確度時，HDR 的表現最佳。

舉例來說，如果您測量的回應時間範圍從 1 微秒到 1 小時，並將 HDR 設定為 3 位有效數字，則對於最高 1 毫秒的數值，它會以 ±1 微秒的精確度記錄；對於接近 1 小時的數值，則以 ±3.6 秒的精確度記錄。

這樣的取捨讓 HDR 比 [`tdigest`](#precision-tuning-with-tdigest) 快得多，但也更耗用記憶體。

下表呈現 HDR 有效數字的細分。

| 有效數字 | 相對精確度（最大誤差） |
| ------------------ | ------------------------------ |
| 1                  | 10 分之 1       = 10%       |
| 2                  | 100 分之 1      = 1%        |
| 3                  | 1,000 分之 1    = 0.1%      |
| 4                  | 10,000 分之 1   = 0.01%     |
| 5                  | 100,000 分之 1  = 0.001%    |

如果您符合下列情況，應使用 HDR：

* 要跨多個桶進行彙總。
* 有足夠的可用記憶體。

如果您的資料包含負值，或數值範圍未知，則應避免使用 HDR。如需更多資訊，請參閱本範例之後的注意事項。

下列範例將 `hdr.number_of_significant_value_digits` 設定為 `3`：

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

與 `tdigest` 不同，後者會為這個小型資料集傳回精確值，HDR 則會將每個數值四捨五入至設定的精確度：

```json
{
  ...
  "aggregations": {
    "load_time_percentiles": {
      "values": {
        "1.0": 20.0,
        "5.0": 20.0,
        "25.0": 40.015625,
        "50.0": 80.046875,
        "75.0": 120.046875,
        "95.0": 140.109375,
        "99.0": 140.109375
      }
    }
  }
}
```

HDR 直方圖僅支援非負值。當數值範圍未知時，請避免使用 HDR，因為範圍過大可能需要大量記憶體。
{: .note}

## 百分位數準確度

計算精確的百分位數需要排序所有數值，這會依資料大小成比例地使用記憶體。若要在大型資料集中計算百分位數，OpenSearch 會使用近似演算法。請留意下列考量：

- 準確度與 q(1 − q) 成正比，其中 q 是所要求的百分位數，以分數表示（例如，第 99 百分位數為 0.99）。因此，極端百分位數（例如第 1 或第 99 百分位數）的準確度最高，而接近中位數的百分位數準確度最低。
- 對於小型資料集，結果為精確值或非常接近精確值。例如，本頁七個 `load_time` 值的百分位數即為精確值。
- 隨著數值數量增加，演算法會近似百分位數以限制記憶體用量。誤差大小取決於資料的分布與數量。
- 對於呈均勻分布的大型資料集，誤差通常會隨著數值數量增加而降低，因為摘要能更平均地概述分布。偏態分布則無法以相同方式受益。
- 對相同資料的不同請求，結果可能略有差異。

`tdigest` 演算法在論文 [Computing Extremely Accurate Quantiles Using t-Digests](https://arxiv.org/abs/1902.04023) 中有詳細說明。

若要平衡準確度與記憶體用量，請使用 `tdigest.compression` 或 `hdr.number_of_significant_value_digits` 參數。

## 指令碼

您可以不指定欄位，改用指令碼動態計算數值。當您需要套用轉換（例如轉換貨幣或套用權重）時，這會很實用。 

### 內嵌指令碼

使用指令碼計算衍生值：

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

若要將數值傳遞至指令碼，請使用 `params`。下列範例會為每個載入時間加上預估的 15 毫秒網路額外負荷：

```json
GET /latency_data/_search
{
  "size": 0,
  "aggs": {
    "load_time_with_overhead": {
      "percentiles": {
        "script": {
          "lang": "painless",
          "source": "doc['load_time'].value + params.network_overhead_ms",
          "params": {
            "network_overhead_ms": 15
          }
        },
        "percents": [
          50,
          95
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

每個百分位數都會增加 15 毫秒：

```json
{
  ...
  "aggregations": {
    "load_time_with_overhead": {
      "values": {
        "50.0": 95.0,
        "95.0": 155.0
      }
    }
  }
}
```

### 已儲存的指令碼

首先，使用下列請求建立範例指令碼：

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

接著在 `percentiles` 彙總中使用已儲存的指令碼，並提供已儲存指令碼所需的 `params`：

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

## 缺少值

根據預設，不包含目標欄位的文件會被忽略。使用 `missing` 設定可為這些文件設定備援值。

若要試用 `missing` 設定，請將不包含 `load_time` 值的文件編製索引：

```json
PUT /latency_data/_doc/health-check?refresh
{
  "endpoint": "/health"
}
```
{% include copy-curl.html %}

下列請求會將沒有 `load_time` 值的文件計為 `0`：

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

沒有 `load_time` 值的文件會計為 `0`，因此第 1 與第 5 百分位數會從 `20` 降至 `0`：

```json
{
  ...
  "aggregations": {
    "load_time_percentiles": {
      "values": {
        "1.0": 0.0,
        "5.0": 0.0,
        "25.0": 40.0,
        "50.0": 80.0,
        "75.0": 120.0,
        "95.0": 140.0,
        "99.0": 140.0
      }
    }
  }
}
```

讀取 `doc['load_time'].value` 的指令碼（例如 [指令碼](#script) 一節中的指令碼）在沒有 `load_time` 值的文件上會失敗。若要在指令碼中處理這些文件，請先檢查 `doc['load_time'].size() == 0`。
{: .note}
