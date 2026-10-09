---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移動函式"
parent: Pipeline aggregations
nav_order: 130
---

# 移動函式彙總

`moving_fn` 彙總是一種父管線彙總，會在滑動視窗上執行指令碼。滑動視窗會在從父 `histogram` 或 `date histogram` 彙總擷取的一連串數值上移動。視窗每次由左向右移動一個桶 (bucket)；每次視窗移動時，`moving_fn` 都會執行指令碼。

使用 `moving_fn` 彙總，即可透過指令碼對滑動視窗內的資料進行任何數值計算。您可以將 `moving_fn` 用於下列用途：

- 趨勢分析
- 離群值偵測
- 自訂時間序列分析
- 自訂平滑演算法
- 數位訊號處理 (DSP)


## 參數

`moving_fn` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 包含要處理之指標值的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `script`              | 必要          | 字串或物件 | 為每個資料視窗計算數值的指令碼。可以是內嵌指令碼、已儲存的指令碼或指令碼檔案。指令碼可以存取 `buckets_path` 參數中定義的變數名稱。 |
| `window`              | 必要          | 整數         | 滑動視窗中的桶數。必須是正整數。 |
| `gap_policy`          | 選用          | 字串          | 套用至缺漏資料的政策。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |
| `shift`               | 選用          | 整數         | 視窗要移動的桶數。可以是正數（向右移往未來的桶）或負數（移往過去的桶）。預設為 `0`，會將視窗置於目前桶的緊鄰左側。請參閱[移動視窗](#shifting-the-window)。 |


## 移動函式的運作方式

`moving_fn` 彙總會在有序桶序列上的滑動視窗中運作。從父彙總的第一個桶開始，`moving_fn` 會執行下列動作：

1. 從 `window` 和 `shift` 參數指定的桶中，收集數值的子序列（視窗）。
2. 將這些數值以陣列形式傳遞給 `script` 指定的函式。
3. 使用 `script` 從陣列計算出單一數值。
4. 將此數值傳回，作為目前桶的結果。
5. 向前移動一個桶，並重複此程序。

「過去」與「未來」數值意指時間序列資料，這是移動視窗函式最常見的使用案例。更廣義地說，它們分別指任何有序資料序列中先前與後續的數值。
{: .note}

`moving_fn` 套用的指令碼可以是[預先定義的函式](#predefined-functions)或[自訂指令碼](#custom-scripts)。桶值會以 `values` 陣列提供給指令碼。指令碼會傳回 double 值作為結果。結果值允許為 `NaN` 和 `+/- Inf`，但不允許為 `null`。


### 視窗大小

`window` 參數指定定義視窗大小的桶數。

傳遞給 `script` 函式的陣列索引從零開始。在指令碼中，以 `values[0]` 到 `values[n]` 存取其值，其中 `n = values.length - 1`。


### 移動視窗

`shift` 參數控制移動視窗相對於目前桶的位置。請根據您的分析需要歷史脈絡、目前資料或未來預測來設定 `shift`。預設為 `0`，只會顯示過去的值（不包括目前的桶）。

`shift` 的一些常用值如下：

| `shift` | 視窗說明                            |                     |
| :--           | :--                                           | :--                 |
| `0`           | 僅過去的值。不包括目前的值。 | `--[-----]x----`    |
| `1`           | 過去的值，包括目前的值。     | `--[----x]-----`    |
| `window/2`    | 以目前數值為中心放置視窗。  | `--[--x--]-----`    |
| `window`      | 未來的值，包括目前的值。   | `--[x----]-----`    |

當視窗在序列開頭或結尾超出可用資料範圍時，`window` 會自動縮小，只使用可用的資料點：

```
[x----]--
-[x----]-
--[x----]
---[x---]
----[x--]
-----[x-]
------[x]
```


## 預先定義的函式

`moving_fn` 彙總支援多個預先定義的函式，可用來取代自訂指令碼。這些函式可從 `MovingFunctions` 內容存取。例如，您可以用 `MovingFunctions.max(values)` 存取 `max` 函式。

下表說明預先定義的函式。

| 函式                              | 模型關鍵字        | 說明                      |
|:--                                    | :--                  |:--                               |
| 最大值                                   | `max`                | 視窗中的最大值。 |
| 最小值                                   | `min`                | 視窗中的最小值。 |
| 總和                                   | `sum`                | 視窗中數值的總和。 |
| 未加權平均值                    | `unweightedAvg`      | 視窗中所有數值的未加權平均數，等於 `sum` / `window`。 |
| 線性加權平均值               | `linearWeightedAvg`  | 使用線性遞減權重的加權平均值，賦予較近期的數值較高的重要性。 |
| 指數加權移動平均值 | `ewma`               | 使用指數遞減權重的加權平均值，賦予較近期的數值較高的重要性。 |
| Holt                                  | `holt`               | 使用第二個指數項來平滑長期趨勢的加權平均值。 |
| Holt-Winters                          | `holt_wimnters`      | 使用第三個指數項來平滑週期性（季節性）效應的加權平均值。 |
| 標準差                    | `stdDev`             | 視窗中數值的總和。 |

所有預先定義的函式都以 `values` 陣列作為第一個參數。對於接受額外參數的函式，請在 `values` 之後依序傳遞這些參數。例如，將 `script` 值設為 `MovingFunctions.stdDev(values, MovingFunctions.unweightedAvg(values))` 來呼叫 `stdDev` 函式。

下表顯示每個模型所需的設定。

| 函式            | 額外參數   | 允許值  | 預設 | 說明 |
| :--                 | :--                | :--             | :--     | :--         |
| `max`               | 無               |   數值陣列   |   無   |  視窗的最大值。 |
| `min`               | 無               |    數值陣列   |   無   | 視窗的最小值。 |
| `sum`               | 無               |    數值陣列 |   無    | 視窗中所有數值的總和。 |
| `unweightedAvg`     | 無               |    數值陣列  |   無   | 視窗中所有數值的算術平均數。 |
| `linearWeightedAvg` | 無               |    數值陣列  |   無    | 視窗中所有數值的加權平均值，較近期的數值權重較高。|
| `ewma`              | `alpha`            | [0, 1] | 0.3     | 衰減參數。值越高，越近期的資料點權重越高。 |
| `holt`              | `alpha`            | [0, 1] | 0.3     | 水準成分的衰減參數。 |
|              | `beta`             | [0, 1] | 0.1     | 趨勢成分的衰減參數。|
| `holt_winters`      | `alpha`            | [0, 1] | 0.3     | 水準成分的衰減參數。  |
|       | `beta`             | [0, 1] | 0.3     | 趨勢成分的衰減參數。 |
|       | `gamma`            | [0, 1] | 0.3     | 季節性成分的衰減參數。  |
|       | `type`             | `add`, `mult`   | `add`   | 定義季節性的建模方式：加法或乘法。 |
|       | `period`           | 整數         | 1       | 構成週期的桶數。 |
|      | `pad`              | 布林值         | true    | 是否為 `mult` 類型模型的 `0` 值加上少量偏移，以避免除以零錯誤。 |
| `stdDev`            | `avg`              | 任意 double 值      | 無    | 視窗的標準差。若要計算有意義的標準差，請使用滑動視窗陣列的平均值，通常為 `MovingFunctions.unweightedAvg(values)`。 |

預先定義的函式不支援缺少參數的函式簽章。因此，即使使用預設值，您也必須提供額外參數。
{: .important}  


### 範例：預先定義的函式

下列範例從 OpenSearch Dashboards 記錄檔範例資料建立以一週為間隔的日期直方圖。`sum` 子彙總會計算每週記錄的所有位元組總和。最後，`moving_fn` 彙總使用 `window` 大小 `5`、預設的 `shift` 值 `0` 以及未加權平均值，計算位元組總和的標準差：

```json
POST /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "my_date_histo": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "week"
      },
      "aggs": {
        "the_sum": {
          "sum": { "field": "bytes" }
        },
        "the_movavg": {
          "moving_fn": {
            "buckets_path": "the_sum",
            "window": 5,
            "script": "MovingFunctions.stdDev(values, MovingFunctions.unweightedAvg(values))"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應顯示移動視窗的標準差，從第二個桶 (bucket) 的零值開始。對於空的視窗或僅包含無效值 (`null` 或 `NaN`) 的視窗，`stdDev` 函式會傳回 `0`：

<details open markdown="block">
  <summary>
    回應
  </summary>

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
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "my_date_histo": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 249,
          "the_sum": {
            "value": 1531493
          },
          "the_movavg": {
            "value": null
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1617,
          "the_sum": {
            "value": 9213161
          },
          "the_movavg": {
            "value": 0
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9188671
          },
          "the_movavg": {
            "value": 3840834
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9244851
          },
          "the_movavg": {
            "value": 3615414.498228507
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 1609,
          "the_sum": {
            "value": 9061045
          },
          "the_movavg": {
            "value": 3327358.65618917
          }
        },
        {
          "key_as_string": "2025-04-28T00:00:00.000Z",
          "key": 1745798400000,
          "doc_count": 1554,
          "the_sum": {
            "value": 8713507
          },
          "the_movavg": {
            "value": 3058812.9440705855
          }
        },
        {
          "key_as_string": "2025-05-05T00:00:00.000Z",
          "key": 1746403200000,
          "doc_count": 1710,
          "the_sum": {
            "value": 9544718
          },
          "the_movavg": {
            "value": 195603.33146038183
          }
        },
        {
          "key_as_string": "2025-05-12T00:00:00.000Z",
          "key": 1747008000000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9155820
          },
          "the_movavg": {
            "value": 270085.92336040025
          }
        },
        {
          "key_as_string": "2025-05-19T00:00:00.000Z",
          "key": 1747612800000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9025078
          },
          "the_movavg": {
            "value": 269477.75659701484
          }
        },
        {
          "key_as_string": "2025-05-26T00:00:00.000Z",
          "key": 1748217600000,
          "doc_count": 895,
          "the_sum": {
            "value": 5047345
          },
          "the_movavg": {
            "value": 267356.5422566652
          }
        }
      ]
    }
  }
}
```
</details>


## 自訂指令碼

您可以提供任意的自訂指令碼來計算 `moving_fn` 結果。自訂指令碼使用 Painless 指令碼語言。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

### 範例：自訂指令碼

下列範例從 OpenSearch Dashboards 電子商務範例資料建立以一週為間隔的日期直方圖。`sum` 子彙總會計算每週所有含稅營收的總和。接著，`moving_fn` 指令碼會傳回目前值之前兩個值中較大的一個；如果沒有兩個可用的值，則傳回 `NaN`：

```json
POST /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "my_date_histo": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "week"
      },
      "aggs": {
        "the_sum": {
          "sum": { "field": "taxful_total_price" }
        },
        "the_movavg": {
          "moving_fn": {
            "buckets_path": "the_sum",
            "window": 2,
            "script": "return (values.length < 2 ? Double.NaN : (values[0]>values[1] ? values[0] : values[1]))"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此範例從第三個桶開始傳回計算結果，因為從該處起才有足夠的先前資料可執行計算：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
  "took": 7,
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
    "my_date_histo": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 582,
          "the_sum": {
            "value": 41455.5390625
          },
          "the_movavg": {
            "value": null
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1048,
          "the_sum": {
            "value": 79448.60546875
          },
          "the_movavg": {
            "value": null
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1048,
          "the_sum": {
            "value": 78208.4296875
          },
          "the_movavg": {
            "value": 79448.60546875
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1073,
          "the_sum": {
            "value": 81277.296875
          },
          "the_movavg": {
            "value": 79448.60546875
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 924,
          "the_sum": {
            "value": 70494.2578125
          },
          "the_movavg": {
            "value": 81277.296875
          }
        }
      ]
    }
  }
}
```
</details>


## 範例：移動平均

`moving_fn` 彙總取代了已棄用的 `moving_avg` 彙總。`moving_fn` 彙總與 `moving_avg` 彙總類似，但用途更廣泛，因為它可以計算任意函式，而不僅限於平均值。所有預先定義的 `moving_avg` 函式也都在 `moving_fn` 中實作。 

`holt` 模型是一種移動平均，使用由 `alpha` 和 `beta` 參數控制的指數衰減權重。以下範例使用 OpenSearch Dashboards 記錄檔範例資料，建立間隔為一週的日期直方圖。`sum` 子彙總會計算每週所有位元組的總和。最後，`moving_fn` 彙總使用 Holt 模型計算位元組總和的加權平均值，其中 `window` 大小為 `6`，`shift` 採用預設值 `0`，`alpha` 值為 `0.3`，而 `beta` 值為 `0.1`：

```json
POST /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "my_date_histogram": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "week"
      },
      "aggs": {
        "the_sum": {
          "sum": { "field": "bytes" }
        },
        "the_movavg": {
          "moving_fn": {
            "buckets_path": "the_sum",
            "window": 6,
            "script": "MovingFunctions.holt(values, 0.3, 0.1)"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會從第二個桶開始傳回 `holt` 移動平均值：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
  "took": 16,
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
    "my_date_histogram": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 249,
          "the_sum": {
            "value": 1531493
          },
          "the_movavg": {
            "value": null
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1617,
          "the_sum": {
            "value": 9213161
          },
          "the_movavg": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9188671
          },
          "the_movavg": {
            "value": 3835993.3999999994
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9244851
          },
          "the_movavg": {
            "value": 5603111.707999999
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 1609,
          "the_sum": {
            "value": 9061045
          },
          "the_movavg": {
            "value": 6964515.302359998
          }
        },
        {
          "key_as_string": "2025-04-28T00:00:00.000Z",
          "key": 1745798400000,
          "doc_count": 1554,
          "the_sum": {
            "value": 8713507
          },
          "the_movavg": {
            "value": 7930766.089341199
          }
        },
        {
          "key_as_string": "2025-05-05T00:00:00.000Z",
          "key": 1746403200000,
          "doc_count": 1710,
          "the_sum": {
            "value": 9544718
          },
          "the_movavg": {
            "value": 8536788.607547803
          }
        },
        {
          "key_as_string": "2025-05-12T00:00:00.000Z",
          "key": 1747008000000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9155820
          },
          "the_movavg": {
            "value": 9172269.837272028
          }
        },
        {
          "key_as_string": "2025-05-19T00:00:00.000Z",
          "key": 1747612800000,
          "doc_count": 1610,
          "the_sum": {
            "value": 9025078
          },
          "the_movavg": {
            "value": 9166173.88436614
          }
        },
        {
          "key_as_string": "2025-05-26T00:00:00.000Z",
          "key": 1748217600000,
          "doc_count": 895,
          "the_sum": {
            "value": 5047345
          },
          "the_movavg": {
            "value": 9123157.830417283
          }
        }
      ]
    }
  }
}
```
</details>

