---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "百分位數排名"
parent: Metric aggregations
nav_order: 80
redirect_from:
  - /query-dsl/aggregations/metric/percentile-ranks/
---

# 百分位數排名彙總

`percentile_ranks` 彙總會估算觀測值中小於或等於指定閾值的百分比。這有助於了解特定值在值分布中的相對位置。

例如，您可以使用百分位數排名彙總來了解 `45` 的交易金額與資料集中其他交易值相比的情況。百分位數排名彙總會傳回像 `82.3` 這樣的值，這表示 82.3% 的交易小於或等於 `45`。

## 參數

`percentile_ranks` 彙總接受下列參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| ---------------------------------------- | ---------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `field` | 字串 | 必要 | 用於計算百分位數排名的數值欄位。 |
| `values` | double 陣列 | 必要 | 用於計算百分位數排名的值。 |
| `keyed` | 布林值 | 選用 | 如果設定為 `false`，則以陣列傳回結果。否則以 JSON 物件傳回結果。預設值為 `true`。 |
| `tdigest.compression` | Double | 選用 | 控制 `tdigest` 演算法的準確度和記憶體使用量。請參閱[使用 `tdigest` 進行精確度調整](#precision-tuning-with-tdigest)。 |
| `hdr.number_of_significant_value_digits` | 整數 | 選用 | HDR 直方圖的精確度設定。請參閱 [HDR 直方圖](#hdr-histogram)。 |
| `missing` | 數字 | 選用 | 當文件中缺少目標欄位時使用的預設值。 |
| `script` | 物件 | 選用 | 用於計算自訂值（而非使用欄位）的指令碼。支援內嵌指令碼和預存指令碼。 |


## 範例



首先，建立範例索引：

```json
PUT /transaction_data
{
  "mappings": {
    "properties": {
      "amount": {
        "type": "double"
      }
    }
  }
}
```
{% include copy-curl.html %}

新增範例數值，以說明百分位數排名的計算方式：

```json
POST /transaction_data/_bulk
{ "index": {} }
{ "amount": 10 }
{ "index": {} }
{ "amount": 20 }
{ "index": {} }
{ "amount": 30 }
{ "index": {} }
{ "amount": 40 }
{ "index": {} }
{ "amount": 50 }
{ "index": {} }
{ "amount": 60 }
{ "index": {} }
{ "amount": 70 }
```
{% include copy-curl.html %}


執行 `percentile_ranks` 彙總，計算特定值與整體分布相比的情況：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "field": "amount",
        "values": [25, 55]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示 28.6% 的值小於或等於 `25`，而 71.4% 的值小於或等於 `55`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rank_check": {
      "values": {
        "25.0": 28.57142857142857,
        "55.0": 71.42857142857143
      }
    }
  }
}
```

## 鍵值回應

您可以將 `keyed` 參數設定為 `false`，將傳回的彙總格式從 JSON 物件變更為鍵值對清單：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "field": "amount",
        "values": [25, 55],
        "keyed": false
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含陣列而非物件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rank_check": {
      "values": [
        {
          "key": 25,
          "value": 28.57142857142857
        },
        {
          "key": 55,
          "value": 71.42857142857143
        }
      ]
    }
  }
}
```

<!-- vale off -->

## 使用 tdigest 進行精確度調整

<!-- vale on -->

根據預設，百分位數排名是使用 `tdigest` 演算法計算。您可以指定 `tdigest.compression` 參數，以控制準確度與記憶體使用量之間的取捨。值越高，準確度越好，但需要更多記憶體。如需 `tdigest` 運作方式的詳細資訊，請參閱[使用 `tdigest` 進行精確度調整]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/#precision-tuning-with-tdigest)。

以下範例將 `tdigest.compression` 設定為 `200`：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "field": "amount",
        "values": [25, 55],
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

除了 `tdigest` 之外，您也可以使用高動態範圍（HDR）直方圖演算法，此演算法較適合大量的桶 (bucket) 及快速處理。如需 HDR 直方圖運作方式的詳細資訊，請參閱 [HDR 直方圖]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/#hdr-histogram)。

在下列情況下，您應該使用 HDR：

* 您要跨多個桶進行彙總。
* 您不需要尾端百分位數具有極高的精確度。
* 您有足夠的可用記憶體。

在下列情況下，您應該避免使用 HDR：

* 尾端準確度很重要。
* 您要分析偏斜或稀疏的資料分布。

以下範例將 `hdr.number_of_significant_value_digits` 設定為 `3`：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "field": "amount",
        "values": [25, 55],
        "hdr": {
          "number_of_significant_value_digits": 3
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 遺漏值

如果某些文件缺少目標欄位，您可以設定 `missing` 參數，指示查詢使用備用值。以下範例確保沒有 `amount` 欄位的文件被視為其值為 `0`，並納入百分位數排名的計算中：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "field": "amount",
        "values": [25, 55],
        "missing": 0
      }
    }
  }
}
```
{% include copy-curl.html %}

### 指令碼

您可以使用指令碼動態計算值，而不是指定欄位。當您需要套用轉換（例如轉換貨幣或套用權重）時，這非常有用。

#### 內嵌指令碼

以下範例使用內嵌指令碼，計算轉換後的值 `30` 和 `60` 相對於 `amount` 欄位值（增加 10% 後）的百分位數排名：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "values": [30, 60],
        "script": {
          "source": "doc['amount'].value * 1.1"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 預存指令碼


若要使用預存指令碼，請先使用以下請求建立它：

```json
POST _scripts/percentile_script
{
  "script": {
    "lang": "painless",
    "source": "doc[params.field].value * params.multiplier"
  }
}
```
{% include copy-curl.html %}

然後在 `percentile_ranks` 彙總中使用該預存指令碼：

```json
GET /transaction_data/_search
{
  "size": 0,
  "aggs": {
    "rank_check": {
      "percentile_ranks": {
        "values": [30, 60],
        "script": {
          "id": "percentile_script",
          "params": {
            "field": "amount",
            "multiplier": 1.1
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
