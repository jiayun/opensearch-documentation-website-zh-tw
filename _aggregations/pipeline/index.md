---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線彙總"
nav_order: 5
has_children: true
has_toc: false
redirect_from:
  - /opensearch/pipeline-agg/
  - /query-dsl/aggregations/pipeline-agg/
  - /aggregations/pipeline/
  - /aggregations/pipeline-agg/
---

# 管線彙總

管線彙總會將一個彙總的輸出作為另一個彙總的輸入，藉此將多個彙總串連在一起。管線彙總可計算複雜的統計與數學量值，例如導數、移動平均及累計總和。部分管線彙總與指標彙總和桶彙總的功能重複，但在許多情況下使用起來更為直覺。

管線彙總會在所有其他同層級彙總之後執行。這會對效能造成影響。例如，使用 `bucket_selector` 管線彙總來縮減桶清單，並不會減少對被省略的桶所執行的運算次數。
{: .note}

管線彙總無法建立子彙總，但可以串連至其他管線彙總。例如，您可以串連兩個連續的 `derivative` 彙總來計算二階導數。請注意，管線彙總會附加至現有的輸出。例如，透過串連 `derivative` 彙總來計算二階導數時，會同時輸出一階與二階導數。

## 管線彙總類型

管線彙總分為兩種類型：[同層級 (sibling)](#sibling-aggregations) 與 [父層級 (parent)](#parent-aggregations)。

### 同層級彙總

_同層級_管線彙總會取用巢狀彙總的輸出，並在與巢狀桶相同的層級產生新的桶或新的彙總。

同層級彙總必須是多桶彙總 (對特定欄位具有多個分組值)，且指標必須是數值。

### 父層級彙總

_父層級_彙總會取用外層彙總的輸出，並在與現有桶相同的層級產生新的桶或新的彙總。同層級管線彙總會跨所有桶運作並產生單一輸出；與之不同的是，父層級管線彙總會個別處理每個桶，並將結果寫回各個桶中。

父層級彙總所指定的指標必須是數值。

我們強烈建議為父層級彙總將 `min_doc_count` 設定為 `0` (這是 `histogram` 彙總的預設值)。如果 `min_doc_count` 大於 `0`，彙總就會省略部分桶，可能導致結果不正確。
{: .important}

## 支援的管線彙總

OpenSearch 支援下列管線彙總。

| 名稱 | 類型 | 說明 |
|------|------|-------------|
| [`avg_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/avg-bucket/) | 同層級 | 計算前一個彙總中每個桶的指標平均值。 |
| [`bucket_script`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-script/) | 父層級 | 執行指令碼，在一組桶上對每個桶進行數值運算。 |
| [`bucket_selector`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-selector/) | 父層級 | 評估指令碼，以判斷 `histogram` (或 `date_histogram`) 彙總傳回的桶是否應納入最終結果。 |
| [`bucket_sort`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-selector/) | 父層級 | 對其父層級多桶彙總所產生的桶進行排序或截斷。 |
| [`cumulative_sum`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/cumulative-sum/) | 父層級 | 計算前一個彙總各桶的累計總和。 |
| [`derivative`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/derivative/) | 父層級 | 計算彙總中每個桶的一階與二階導數。 |
| [`extended_stats`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/extended-stats/) | 同層級 | `stats_bucket` 彙總的更完整版本，提供額外的指標。 |
| [`max_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/max-bucket/) | 同層級 | 計算前一個彙總中每個桶的指標最大值。 |
| [`min_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/min-bucket/) | 同層級 | 計算前一個彙總中每個桶的指標最小值。 |
| [`moving_avg`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/moving-avg/) *(已淘汰)* | 父層級 | 計算有序資料集的視窗 (相鄰子集) 中所含指標的一系列平均值。 |
| [`moving_fn`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/moving-function/) | 父層級 | 在滑動視窗上執行指令碼。 |
| [`percentiles_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/percentiles-bucket/) | 同層級 | 計算分桶指標的百分位數位置。 |
| [`serial_diff`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/serial-diff/) | 父層級 | 計算目前桶與先前桶之間指標值的差異，並將結果儲存在目前的桶中。 |
| [`stats_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/stats-bucket/) | 同層級 | 針對前一個彙總的桶傳回多種統計資料 (`count`、`min`、`max`、`avg` 和 `sum`)。 |
| [`sum_bucket`]({{site.url}}{{site.baseurl}}/aggregations/pipeline/sum-bucket/) | 同層級 | 計算前一個彙總中每個桶的指標總和。 |


## 桶路徑

管線彙總使用 `buckets_path` 參數來參照其他彙總的輸出。
`buckets_path` 參數的語法如下：

```r
buckets_path = <agg_name>[ > <agg_name> ... ][ .<metric_name> ]
```

此語法使用下列元素。

| 元素 | 說明 |
| :-- | :-- |
| `<agg_name>` | 彙總的名稱。 |
| `>` |  子項選取器，用於從一個彙總 (父項) 導覽至另一個巢狀彙總 (子項)。  |
| `.<metric_name>` |  指定要從多值彙總中擷取的指標。僅在目標彙總產生多個指標時為必要。 |

為了將桶路徑視覺化，假設您有下列彙總結構：

```json
"aggs": {
  "parent_agg": {
    "terms": {
      "field": "category"
    },
    "aggs": {
      "child_agg": {
        "stats": {
          "field": "price"
        }
      }
    }
  }
}
```

若要參照巢狀於 `parent_agg` 中的 `child_agg` 的平均價格，請使用 `parent_agg>child_agg.avg`。

範例：

- `my_sum.sum`：參照 `my_sum` 彙總中的總和指標。

- `popular_tags>my_sum.sum`：參照 `my_sum` 彙總中的 `sum` 指標，該彙總巢狀於 `popular_tags` 彙總之下。

對於 `stats` 或 `percentiles` 等多值指標彙總，您必須在路徑中包含指標名稱 (例如 `.min`)。對於 `sum` 或 `avg` 等單值指標，若不會造成歧義，指標名稱為選用。
{: .tip}


### 桶路徑範例

下列範例以 OpenSearch Dashboards 記錄檔範例資料進行運算。它會建立 `bytes` 欄位值的直方圖，加總每個直方圖桶中的 `phpmemory` 欄位，最後使用 `sum_bucket` 管線彙總加總各桶。`buckets_path` 會依循 `number_of_bytes>sum_total_memory ` 路徑，從 `number_of_bytes` 父層級彙總到 `sum_total_memory` 子彙總：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "number_of_bytes": {
      "histogram": {
        "field": "bytes",
        "interval": 10000
      },
      "aggs": {
        "sum_total_memory": {
          "sum": {
            "field": "phpmemory"
          }
        }
      }
    },
    "sum_copies": {
      "sum_bucket": {
        "buckets_path": "number_of_bytes>sum_total_memory"
      }
    }
  }
}
```
{% include copy-curl.html %}

請注意，`buckets_path` 包含各組成彙總的名稱。路徑具有方向性，也就是說，路徑只會單向串接，由父項向下至子項。

管線彙總會傳回從所有桶加總而得的記憶體總量：

```json
{
  ...
  "aggregations": {
    "number_of_bytes": {
      "buckets": [
        {
          "key": 0,
          "doc_count": 13372,
          "sum_total_memory": {
            "value": 91266400
          }
        },
        {
          "key": 10000,
          "doc_count": 702,
          "sum_total_memory": {
            "value": 0
          }
        }
      ]
    },
    "sum_copies": {
      "value": 91266400
    }
  }
}
```

### 計數路徑

您可以指示 `buckets_path` 使用計數而非值作為輸入。若要這麼做，請使用 `_count` 桶路徑變數。

下列範例針對 OpenSearch Dashboards 記錄檔範例資料中位元組數的直方圖計算基本統計資料。它會建立 `bytes` 欄位值的直方圖，然後計算直方圖桶中計數的統計資料。

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "number_of_bytes": {
      "histogram": {
        "field": "bytes",
        "interval": 10000
      }
    },
    "count_stats": {
      "stats_bucket": {
        "buckets_path": "number_of_bytes>_count"
      }
    }
  }
}
```
{% include copy-curl.html %}

結果顯示各桶*文件計數*的統計資料：

```json
{
...
  "aggregations": {
    "number_of_bytes": {
      "buckets": [
        {
          "key": 0,
          "doc_count": 13372
        },
        {
          "key": 10000,
          "doc_count": 702
        }
      ]
    },
    "count_stats": {
      "count": 2,
      "min": 702,
      "max": 13372,
      "avg": 7037,
      "sum": 14074
    }
  }
}
```

## 資料缺漏

實際資料可能因多種原因而在巢狀彙總中缺漏，包括：

- 文件中缺少值。
- 彙總鏈中任何位置出現空桶。
- 缺少計算桶值所需的資料 (例如，`derivative` 等滾動函式需要一個或多個先前的值才能開始計算)。

您可以使用 `gap_policy` 屬性指定處理缺漏資料的策略：略過缺漏資料，或以零取代缺漏資料。

`gap_policy` 參數適用於所有管線彙總。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的策略。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |

