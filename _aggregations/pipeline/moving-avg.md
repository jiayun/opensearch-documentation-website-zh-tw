---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移動平均"
parent: Pipeline aggregations
nav_order: 120
---

# 移動平均彙總
**已棄用**
{: .label .label-red }

`moving_avg` 彙總已棄用，請改用 `moving_fn` 彙總。
{: .important}

`moving_avg` 彙總是一種父管線彙總，會針對有序資料集的各個視窗（相鄰子集）計算其中所含指標的一系列平均值。

若要建立 `moving_avg` 彙總，請先建立 `histogram` 或 `date_histogram` 彙總。接著，您可以選擇在直方圖彙總中嵌入指標彙總。最後，將 `moving_avg` 彙總嵌入直方圖中，並將 `buckets_path` 參數設定為您要追蹤的嵌入指標。

視窗大小是指視窗中連續資料值的數量。每次迭代時，演算法會計算視窗中所有資料點的平均值，然後向前滑動一個資料值，排除前一個視窗的第一個值，並納入下一個視窗的第一個值。

例如，給定資料 `[1, 5, 8, 23, 34, 28, 7, 23, 20, 19]`，視窗大小為 5 的移動平均如下：

```
(1 + 5 + 8 + 23 + 34) / 5 = 14.2
(5 + 8 + 23 + 34 + 28) / 5 = 19.6
(8 + 23 + 34 + 28 + 7) / 5 = 20
and so on ...
```

`moving_avg` 彙總通常套用於時間序列資料，以平滑雜訊或短期波動並找出趨勢。
指定較小的視窗大小可平滑小規模波動。指定較大的視窗大小可平滑高頻波動或隨機雜訊，使低頻趨勢更加明顯。

如需移動平均的詳細資訊，請參閱 [Wikipedia](https://en.wikipedia.org/wiki/Moving_average)。

## 參數

`moving_avg` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的桶 (bucket) 路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。會在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |
| `window`              | 選用          | 數值       | 視窗中包含的資料點數量。預設為 `5`。 |
| `model`               | 選用          | 字串          | 要使用的加權移動平均模型。選項為 `ewma`、`holt`、`holt_winters`、`linear` 和 `simple`。預設為 `simple`。請參閱[模型](#models)。 |
| `settings`            | 選用          | 物件          |  用於調整視窗的參數。請參閱[模型](#models)。 |
| `predict`             | 選用          | 數值        | 要附加在結果末尾的預測值數量。預設為 `0`。 |


## 範例

下列範例會從 OpenSearch Dashboards 記錄檔範例資料建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`moving_avg` 彙總會根據這些總和計算每月位元組的移動平均：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "my_date_histogram": {                                
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "month"
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": { "field": "bytes" }                 
        },
        "moving_avg_of_sum_of_bytes": {
          "moving_avg": {
            "buckets_path": "sum_of_bytes" 
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

此彙總會從第二個桶開始傳回 `moving_avg` 值。第一個桶沒有移動平均值，因為先前的資料點不足以進行計算：

```json
{
  "took": 5,
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
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "sum_of_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "sum_of_bytes": {
            "value": 39103067
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "sum_of_bytes": {
            "value": 37818519
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 20953585
          }
        }
      ]
    }
  }
}
```


## 範例：預測

您可以使用 `moving_avg` 彙總來預測未來的桶。

下列範例將前一個範例的間隔縮短為一週，並在回應末尾附加五個預測的一週桶：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "my_date_histogram": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "week"
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "moving_avg_of_sum_of_bytes": {
          "moving_avg": {
            "buckets_path": "sum_of_bytes",
            "predict": 5
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含這五個預測。請注意，預測桶的 `doc_count` 為 `0`：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
  "took": 5,
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
          "sum_of_bytes": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1617,
          "sum_of_bytes": {
            "value": 9213161
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9188671
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 5372327
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9244851
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 6644441.666666667
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 1609,
          "sum_of_bytes": {
            "value": 9061045
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 7294544
          }
        },
        {
          "key_as_string": "2025-04-28T00:00:00.000Z",
          "key": 1745798400000,
          "doc_count": 1554,
          "sum_of_bytes": {
            "value": 8713507
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 7647844.2
          }
        },
        {
          "key_as_string": "2025-05-05T00:00:00.000Z",
          "key": 1746403200000,
          "doc_count": 1710,
          "sum_of_bytes": {
            "value": 9544718
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9084247
          }
        },
        {
          "key_as_string": "2025-05-12T00:00:00.000Z",
          "key": 1747008000000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9155820
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9150558.4
          }
        },
        {
          "key_as_string": "2025-05-19T00:00:00.000Z",
          "key": 1747612800000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9025078
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9143988.2
          }
        },
        {
          "key_as_string": "2025-05-26T00:00:00.000Z",
          "key": 1748217600000,
          "doc_count": 895,
          "sum_of_bytes": {
            "value": 5047345
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9100033.6
          }
        },
        {
          "key_as_string": "2025-06-02T00:00:00.000Z",
          "key": 1748822400000,
          "doc_count": 0,
          "moving_avg_of_sum_of_bytes": {
            "value": 8297293.6
          }
        },
        {
          "key_as_string": "2025-06-09T00:00:00.000Z",
          "key": 1749427200000,
          "doc_count": 0,
          "moving_avg_of_sum_of_bytes": {
            "value": 8297293.6
          }
        },
        {
          "key_as_string": "2025-06-16T00:00:00.000Z",
          "key": 1750032000000,
          "doc_count": 0,
          "moving_avg_of_sum_of_bytes": {
            "value": 8297293.6
          }
        },
        {
          "key_as_string": "2025-06-23T00:00:00.000Z",
          "key": 1750636800000,
          "doc_count": 0,
          "moving_avg_of_sum_of_bytes": {
            "value": 8297293.6
          }
        },
        {
          "key_as_string": "2025-06-30T00:00:00.000Z",
          "key": 1751241600000,
          "doc_count": 0,
          "moving_avg_of_sum_of_bytes": {
            "value": 8297293.6
          }
        }
      ]
    }
  }
}
```
</details>

## 模型

`moving_avg` 彙總支援五種模型，差別在於它們如何為移動視窗中的值加權。

使用 `model` 參數指定要使用的模型。

| 模型 | 模型關鍵字 | 加權方式   |
|-------|---------------|-------------|
| 簡單 | `simple` | 視窗中所有值的未加權平均值。 |
| 線性 | `linear` | 使用線性遞減的權重，讓較新的值更具重要性。 |
| 指數加權移動平均 | `ewma` | 使用指數遞減的權重，讓較新的值更具重要性。 |
| Holt | `holt` | 使用第二個指數項來平滑長期趨勢。 |
| Holt-Winters | `holt_winters` | 使用第三個指數項來平滑週期性（季節性）效應。 |

使用 `settings` 物件設定模型的屬性。下表列出每個模型可用的設定。

| 模型            | 參數   | 允許的值  | 預設 | 說明 |
| :--              | :--         | :--             | :--     | :--         |
| `simple`     | 無               |    數值陣列  |   無   | 視窗中所有值的算術平均值。 |
| `linear` | 無               |    數值陣列  |   無    | 視窗中所有值的加權平均值，較新的值權重較高。|
| `ewma`              | `alpha`            | [0, 1] | 0.3     | 衰減參數。值越高，較新的資料點權重越大。 |
| `holt`              | `alpha`            | [0, 1] | 0.3     | 水準成分的衰減參數。 |
|              | `beta`             | [0, 1] | 0.1     | 趨勢成分的衰減參數。|
| `holt_winters`      | `alpha`            | [0, 1] | 0.3     | 水準成分的衰減參數。  |
|       | `beta`             | [0, 1] | 0.3     | 趨勢成分的衰減參數。 |
|       | `gamma`            | [0, 1] | 0.3     | 季節性成分的衰減參數。  |
|       | `type`             | `add`, `mult`   | `add`   | 定義季節性的建模方式：加法或乘法。 |
|       | `period`           | 整數         | 1       | 構成一個週期的桶 (bucket) 數量。 |
|      | `pad`              | 布林值         | `true`    | 是否為 `mult` 類型模型的 `0` 值加上一個小的偏移量，以避免除以零的錯誤。 |


如需這些模型及其參數的相關說明，請參閱 [Wikipedia](https://en.wikipedia.org/wiki/Moving_average)。


### 範例：Holt 模型

`holt` 模型以指數衰減計算權重，衰減程度由 `alpha` 和 `beta` 參數控制。

下列請求使用 Holt 模型計算每週位元組資料總量的移動平均，其中 `window` 大小為 `6`、`alpha` 值為 `0.4`，且 `beta` 值為 `0.2`：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "my_date_histogram": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "week"
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
        "moving_avg_of_sum_of_bytes": {
          "moving_avg": {
            "buckets_path": "sum_of_bytes",
            "window": 6,
            "model": "holt",
            "settings": { "alpha": 0.4, "beta": 0.2 }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

移動平均從第二個桶開始：

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
          "sum_of_bytes": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1617,
          "sum_of_bytes": {
            "value": 9213161
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9188671
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 4604160.2
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9244851
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 6806684.584000001
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 1609,
          "sum_of_bytes": {
            "value": 9061045
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 8341230.127680001
          }
        },
        {
          "key_as_string": "2025-04-28T00:00:00.000Z",
          "key": 1745798400000,
          "doc_count": 1554,
          "sum_of_bytes": {
            "value": 8713507
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9260724.7236736
          }
        },
        {
          "key_as_string": "2025-05-05T00:00:00.000Z",
          "key": 1746403200000,
          "doc_count": 1710,
          "sum_of_bytes": {
            "value": 9544718
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9657431.903375873
          }
        },
        {
          "key_as_string": "2025-05-12T00:00:00.000Z",
          "key": 1747008000000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9155820
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9173999.55240704
          }
        },
        {
          "key_as_string": "2025-05-19T00:00:00.000Z",
          "key": 1747612800000,
          "doc_count": 1610,
          "sum_of_bytes": {
            "value": 9025078
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9172040.511275519
          }
        },
        {
          "key_as_string": "2025-05-26T00:00:00.000Z",
          "key": 1748217600000,
          "doc_count": 895,
          "sum_of_bytes": {
            "value": 5047345
          },
          "moving_avg_of_sum_of_bytes": {
            "value": 9108804.964619776
          }
        }
      ]
    }
  }
}
```
</details>
