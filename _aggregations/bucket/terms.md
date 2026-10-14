---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙"
parent: Bucket aggregations
nav_order: 200
redirect_from:
  - /query-dsl/aggregations/bucket/terms/
---

# 詞彙彙總

`terms` 彙總會為欄位的每個唯一詞彙動態建立一個桶 (bucket)。

## 參數

`terms` 彙總採用下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 選用 | 字串 | 要彙總的欄位。必須是 `keyword`、`numeric`、`ip`、`boolean` 或 `date` 欄位。只有在為該欄位啟用 [`fielddata`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 時，才能使用 `text` 欄位，這可能會耗用大量記憶體。必須提供 `field` 或 `script`。 |
| `script` | 選用 | 物件 | 產生要彙總之值的指令碼。必須提供 `field` 或 `script`。與 `field` 搭配使用時，指令碼會做為值指令碼，並以 `_value` 接收欄位值。 |
| `size` | 選用 | 整數 | 要傳回的桶數。預設為 `10`。 |
| `shard_size` | 選用 | 整數 | 從每個分片收集的候選詞彙數。較高的值可提升準確度。預設為 `size * 1.5 + 10`。 |
| `min_doc_count` | 選用 | 整數 | 桶要納入回應所需的最低文件數。預設為 `1`。 |
| `shard_min_doc_count` | 選用 | 整數 | 詞彙要成為候選所需的分片層級最低文件數。預設為 `0`。 |
| `show_term_doc_count_error` | 選用 | 布林值 | 設為 `true` 時，會包含每個桶的誤差估計。預設為 `false`。 |
| `order` | 選用 | 物件 | 控制桶的排序順序。接受 `_count`、`_key` 或子彙總指標的名稱，各搭配 `asc` 或 `desc`。預設為 `{"_count": "desc"}`。 |
| `include` | 選用 | 字串、陣列或物件 | 篩選哪些詞彙值可以建立桶。接受規則運算式字串、確切值的陣列或 `partition` 物件。 |
| `exclude` | 選用 | 字串或陣列 | 篩選哪些詞彙值不能建立桶。接受規則運算式字串或確切值的陣列。 |
| `missing` | 選用 | 字串或數字 | 用於缺少目標欄位之文件的值，會將這些文件放入對應的桶。預設會忽略缺少的文件。 |
| `execution_hint` | 選用 | 字串 | 控制詞彙的收集方式。有效值為 `map` (直接彙總欄位值) 與 `global_ordinals` (使用欄位的全域序數進行彙總)。OpenSearch 會自動選擇最佳選項。如需更多資訊，請參閱[執行提示](#execution-hint)。 |
| `collect_mode` | 選用 | 字串 | 控制巢狀彙總的計算方式。有效值為：<br> - `depth_first`：先展開所有分支再修剪。<br> - `breadth_first`：在每一層先修剪再展開，可減少深度巢狀彙總的記憶體用量。<br><br>根據預設，OpenSearch 會自動選擇模式。如需更多資訊，請參閱[收集模式](#collect-mode)。 |

## 範例

下列範例使用 `terms` 彙總，從網站記錄資料中找出每個回應程式碼的文件數：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response.keyword",
        "size": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
...
"aggregations" : {
  "response_codes" : {
    "doc_count_error_upper_bound" : 0,
    "sum_other_doc_count" : 0,
    "buckets" : [
      {
        "key" : "200",
        "doc_count" : 12832
      },
      {
        "key" : "404",
        "doc_count" : 801
      },
      {
        "key" : "503",
        "doc_count" : 441
      }
    ]
  }
 }
}
```

每個桶都包含 `key` 欄位中的詞彙，以及 `doc_count` 欄位中包含該詞彙的文件數。根據預設，桶會依 `doc_count` 遞減排序。

您可以使用 `terms`，將傳回的值依計數遞增排序 (`"order": {"_count": "asc"}`)，以搜尋不常出現的值。不過，我們強烈不建議這麼做，因為涉及多個分片時，可能會導致結果不準確。全域不常出現的詞彙，在每個個別分片上未必都不常出現，也可能完全不會出現在某些分片所傳回的最不常出現結果中。反之，在某個分片上不常出現的詞彙，在另一個分片上可能很常見。在這兩種情況下，分片層級彙總期間都可能遺漏罕見詞彙，導致整體結果不正確。我們建議改用 `rare_terms` 彙總，而非 `terms` 彙總，因為前者是專為更準確地處理這些情況而設計。
{: .warning}


## size 與 shard_size 參數

`terms` 彙總傳回的桶數由 `size` 參數控制，預設為 10。

此外，負責彙總的協調節點會向每個分片要求其最常出現的唯一詞彙。每個分片傳回的桶數由 `shard_size` 參數控制。此參數與 `size` 參數不同，其存在是為了提高桶文件計數的準確度。

例如，假設 `size` 與 `shard_size` 參數的值都是 3。`terms` 彙總會向每個分片要求其最常出現的三個唯一詞彙。協調節點會彙總這些結果以計算最終結果。如果某個分片包含的詞彙不在其前三個詞彙中，該詞彙就不會出現在回應中。不過，提高此請求的 `shard_size` 值，可讓每個分片傳回更多唯一詞彙，提高協調節點收到所有相關結果的可能性。

根據預設，`shard_size` 參數設為 `size * 1.5 + 10`。如果您將 `shard_size` 設為小於 `size` 的值，OpenSearch 會改用 `size` 值。

使用並行分段搜尋時，`shard_size` 參數也會套用至每個分段切片。

`shard_size` 參數可用來平衡 `terms` 彙總的效能與文件計數準確度。較高的 `shard_size` 值可確保較高的文件計數準確度，但會導致更高的記憶體與運算用量。較低的 `shard_size` 值效能較佳，但會導致較低的文件計數準確度。

## 文件計數誤差

回應中也包含兩個名為 `doc_count_error_upper_bound` 與 `sum_other_doc_count` 的索引鍵。

`terms` 彙總會傳回最常出現的唯一詞彙。因此，如果資料包含許多唯一詞彙，其中有些可能不會出現在結果中。`sum_other_doc_count` 欄位代表從回應中排除的文件總和。在此情況下，數字為 0，因為所有唯一值都出現在回應中。

`doc_count_error_upper_bound` 欄位代表從最終結果中排除之唯一值的可能最大計數。請使用此欄位來估計計數的誤差範圍。

`doc_count_error_upper_bound` 值與準確度的概念僅適用於使用預設排序順序 (依文件計數遞減) 的彙總。這是因為當您依文件計數遞減排序時，任何未傳回的詞彙，其文件數必定等於或少於已傳回的詞彙。根據這點，您可以計算 `doc_count_error_upper_bound`。

OpenSearch 會將每個分片所傳回最後一個詞彙的文件計數加總，以計算整體 `doc_count_error_upper_bound`。任何未傳回的詞彙，其文件數最多就是這麼多。

如果 `show_term_doc_count_error` 參數設為 `true`，則 `terms` 彙總除了顯示整體值之外，還會顯示為每個唯一桶計算的 `doc_count_error_upper_bound`。每個桶的誤差，是未傳回該桶詞彙之每個分片所傳回最後一個詞彙的文件計數總和。它代表該桶計數可能遺漏的最多文件數，可協助您選擇 `shard_size` 值。

當桶依索引鍵排序時，誤差一律為 `0`，因為未傳回某詞彙的分片並不包含該詞彙。當桶依文件計數遞增或依子彙總排序時，無法計算誤差，且 `doc_count_error_upper_bound` 為 `-1`，表示誤差沒有上限。

## min_doc_count 與 shard_min_doc_count 參數

您可以使用 `min_doc_count` 參數來篩選掉結果數少於 `min_doc_count` 的任何唯一詞彙。`min_doc_count` 門檻只會在合併所有分片擷取的結果之後套用。每個分片並不知道特定詞彙的全域文件數。如果全域高頻詞彙的前 `shard_size` 名與某個分片本機的前幾名詞彙之間有顯著差異，使用 `min_doc_count` 參數時可能會得到非預期的結果。例如，如果每個分片的候選清單都填入了全域上不常見的詞彙，全域高頻詞彙可能會從結果中消失。為了減少這種影響，可以增加 `shard_size`，讓每個分片傳回更多候選詞彙，但代價是更多的記憶體與網路流量。

另外，`shard_min_doc_count` 參數用來篩選掉分片傳回給協調器時結果數少於 `shard_min_doc_count` 的唯一詞彙。您可以用它來捨棄不太可能達到 `min_doc_count` 的詞彙，例如拼字錯誤，即使在合併分片計數之後也一樣。請將 `shard_min_doc_count` 設定為遠低於 `min_doc_count` 除以分片數的值。否則，全域上能達到 `min_doc_count` 的詞彙可能會在個別分片上被篩選掉。

使用這些參數時，請記住以下注意事項：

- 將 `min_doc_count` 設為 `0` 也會為未比對到任何文件的詞彙傳回桶。其中某些詞彙可能只存在於已刪除的文件中，因此 `match_all` 查詢不保證能為它們找到任何文件。
- 如果您沒有依文件數遞減排序桶，較高的 `min_doc_count` 值可能會傳回少於 `size` 個桶，因為分片沒有傳回足夠的候選詞彙。若要擷取遺漏的桶，請增加 `shard_size`。

使用並行分段搜尋時，`shard_min_doc_count` 參數不會套用至每個分段切片。如需更多資訊，請參閱[相關的 GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/11847)。

## 將值篩選為子集

您可以使用 `include` 與 `exclude` 參數來篩選出現在彙總桶中的詞彙值。當同時指定這兩個參數時，會先評估 `include`，然後再將 `exclude` 套用至結果。

### 正規表示式篩選

`include` 與 `exclude` 參數都接受採用 Lucene [正規表示式語法]({{site.url}}{{site.baseurl}}/query-dsl/regex-syntax/) 的正規表示式字串：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "success_codes": {
      "terms": {
        "field": "response.keyword",
        "include": "2.*",
        "exclude": "204"
      }
    }
  }
}
```
{% include copy-curl.html %}

預設情況下，正規表示式字串的最大長度為 1000 個字元。您可以使用 `index.max_regex_length` 索引設定來變更此限制。如需更多資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

### 精確值篩選

`include` 與 `exclude` 參數都接受精確值的陣列：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "specific_codes": {
      "terms": {
        "field": "response.keyword",
        "include": ["200", "404", "503"]
      }
    }
  }
}
```
{% include copy-curl.html %}

`include` 與 `exclude` 參數必須使用相同的格式：正規表示式字串或精確值陣列。

## 逐頁檢視所有詞彙

當某個欄位包含過多的唯一詞彙而無法在單一請求中擷取時，您可以使用以分割區為基礎的篩選，透過傳送多個請求來擷取所有詞彙。詞彙會使用雜湊函式指派到分割區，因此分佈大致平均。

若要擷取所有唯一詞彙，請傳送等於 `num_partitions` 的請求數。在 `include` 參數中指定 `partition` 與 `num_partitions`。對於每個請求，保持 `num_partitions` 不變，並將 `partition` 從 `0` 遞增到 `num_partitions - 1`。以下範例擷取範例資料中用戶端 IP 位址五個分割區中的第一個，該資料包含約 1,000 個唯一值：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "partitioned_terms": {
      "terms": {
        "field": "clientip",
        "size": 250,
        "include": {
          "partition": 0,
          "num_partitions": 5
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含指派給分割區 0 的 206 個用戶端 IP 位址，且 `sum_other_doc_count` 為 `0`，表示該分割區已完整傳回。如果欄位只包含少數唯一詞彙，某些分割區可能會是空的。例如，當 `num_partitions` 為 `5` 時，`response.keyword` 的三個值全部落在分割區 1 與 3。

若要選擇分割區設定，請使用以下程序：

1. 使用 [`cardinality`]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/) 彙總估計唯一詞彙的數量。
1. 選擇一個 `num_partitions` 值與一個夠大的 `size` 值，讓每個分割區都能傳回其所有詞彙。例如，1,000 個唯一詞彙分成 5 個分割區，平均每個分割區 200 個詞彙。由於雜湊分佈不均，某些分割區包含的詞彙會多於平均值，因此請加入餘裕，使用例如 `250` 這樣的 `size`。
1. 對一個分割區執行測試請求。如果請求因斷路器而失敗，表示分割區太大：請增加 `num_partitions`。如果請求成功但 `sum_other_doc_count` 大於 `0`，表示有些詞彙未能納入：請增加 `size` 或 `num_partitions`。

若要依排序順序逐頁檢視每個唯一詞彙或詞彙組合，請考慮使用 [`composite`]({{site.url}}{{site.baseurl}}/aggregations/bucket/composite/) 彙總，它會傳回一個 `after_key`，您可以將其傳遞給下一個請求。

`include` 參數在每個請求中只能使用一種格式：正規表示式字串、值陣列，或 `partition` 物件。因此，您無法將篩選（以正規表示式或陣列為基礎）與以分割區為基礎的擷取結合使用。使用以分割區為基礎的擷取時，不支援 `exclude` 參數。
{: .note}


## 收集模式

有兩種收集模式可用：`depth_first` 與 `breadth_first`。`depth_first` 收集模式會以深度優先的方式展開彙總樹的所有分支，並且只在展開完成後才執行修剪。

然而，使用巢狀 `terms` 彙總時，傳回桶的基數會乘以每一層巢狀中欄位的基數，因此隨著彙總的巢狀加深，桶數很容易出現組合爆炸。

您可以使用 `breadth_first` 收集模式來解決這個問題。在這種情況下，會在彙總樹的第一層展開到下一層之前先進行修剪，可能大幅減少計算的桶數。

在 `breadth_first` 模式下，`order` 參數仍然可以參考子彙總。OpenSearch 會先計算該子彙總，以便在修剪桶之前先排序。

需要相關性分數的子彙總（例如 `top_hits`）在 `breadth_first` 模式下受支援。為了計算它們，OpenSearch 會重新執行查詢，但只針對篩選後保留的前幾個桶中的文件。

如果您沒有指定 `collect_mode`，OpenSearch 會自動選擇。當 `terms` 彙總有子彙總，且欄位包含的唯一詞彙多於 `shard_size`（或唯一詞彙數未知）時，它會使用 `breadth_first`。否則，它會使用 `depth_first`。

此外，執行 `breadth_first` 收集會產生與比對文件數呈線性關係的記憶體負擔。這是因為 `breadth_first` 收集的運作方式是快取並重新執行父層修剪後的桶集合。


## 排序順序

根據預設，桶會依 `_count` 遞減排序（文件數最多的在前）。您可以使用 `order` 參數變更排序順序。下列範例依字母順序排序回應碼：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response.keyword",
        "order": { "_key": "asc" }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回依鍵值遞增排序的桶：

```json
{
  ...
  "aggregations" : {
    "response_codes" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "200",
          "doc_count" : 12832
        },
        {
          "key" : "404",
          "doc_count" : 801
        },
        {
          "key" : "503",
          "doc_count" : 441
        }
      ]
    }
  }
}
```

您也可以依子彙總指標排序。下列範例依平均位元組數遞減排序回應碼：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response.keyword",
        "order": { "avg_bytes": "desc" }
      },
      "aggs": {
        "avg_bytes": {
          "avg": { "field": "bytes" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

依子彙總排序時，文件計數可能包含無界限的誤差。只有在單一分片上執行彙總，或在編製索引時將彙總的欄位用作[路由]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/routing/)鍵，使每個詞彙只儲存在一個分片上時，結果才會準確。依 [`max`]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/) 子彙總遞減排序，或依 [`min`]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/) 子彙總遞增排序，也會選出正確的前幾個桶，儘管其文件計數可能不精確。
{: .warning}

若要依巢狀於彙總樹更深處的指標排序，請使用 `>` 分隔符號指定路徑。排序路徑可以包含任意數量的單桶彙總，例如 `filter`，並以 `>` 分隔。路徑中的最後一個彙總必須是單桶彙總或指標彙總：

- 如果最後一個彙總是單桶彙總，桶會依其 `doc_count` 排序。
- 如果最後一個彙總是單值指標彙總，例如 `avg`，桶會依其值排序。
- 如果最後一個彙總是多值指標彙總，例如 `stats`，請使用 `.` 分隔符號附加指標名稱。

多桶彙總（例如 `terms`）不能出現在排序路徑中。

下列範例僅依成功 (200) 回應的平均位元組數排序作業系統：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os": {
      "terms": {
        "field": "machine.os.keyword",
        "size": 3,
        "order": { "successful>avg_bytes": "desc" }
      },
      "aggs": {
        "successful": {
          "filter": { "term": { "response.keyword": "200" } },
          "aggs": {
            "avg_bytes": {
              "avg": { "field": "bytes" }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會依巢狀的 `avg_bytes` 指標排序 OS 桶：

```json
{
  ...
  "aggregations" : {
    "os" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 5639,
      "buckets" : [
        {
          "key" : "win xp",
          "doc_count" : 2885,
          "successful" : {
            "doc_count" : 2549,
            "avg_bytes" : {
              "value" : 6083.602196939976
            }
          }
        },
        {
          "key" : "ios",
          "doc_count" : 2737,
          "successful" : {
            "doc_count" : 2512,
            "avg_bytes" : {
              "value" : 5954.860270700637
            }
          }
        },
        {
          "key" : "win 8",
          "doc_count" : 2813,
          "successful" : {
            "doc_count" : 2585,
            "avg_bytes" : {
              "value" : 5910.602321083172
            }
          }
        }
      ]
    }
  }
}
```

管線彙總不能用於排序，因為它們會在縮減階段執行，此時桶已排序完成。
{: .note}

若要依多值指標彙總的其中一個指標排序，請使用 `.` 分隔符號。下列範例使用 `stats` 子彙總的 `max` 指標，依每個桶中最大的 `bytes` 值排序作業系統：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os": {
      "terms": {
        "field": "machine.os.keyword",
        "size": 3,
        "order": { "bytes_stats.max": "desc" }
      },
      "aggs": {
        "bytes_stats": {
          "stats": { "field": "bytes" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以在 `order` 參數中提供陣列，以依多個準則排序。OpenSearch 會依序套用這些準則，並使用後續的每個準則來打破平手。下列範例先依成功回應的平均位元組數排序作業系統，再依文件計數排序：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os": {
      "terms": {
        "field": "machine.os.keyword",
        "order": [
          { "successful>avg_bytes": "desc" },
          { "_count": "desc" }
        ]
      },
      "aggs": {
        "successful": {
          "filter": { "term": { "response.keyword": "200" } },
          "aggs": {
            "avg_bytes": {
              "avg": { "field": "bytes" }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如果兩個桶在所有排序準則上的值都相同，OpenSearch 會依鍵值遞增排序它們。

## 多欄位詞彙彙總

`terms` 彙總原生不支援多個欄位，因為它依賴全域序數，而全域序數只存在於單一欄位內。若要依欄位組合分組，請使用 [`multi_terms` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/) 或結合欄位值的 `script`：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os_and_response": {
      "terms": {
        "script": {
          "source": "doc['machine.os.keyword'].value + ' - ' + doc['response.keyword'].value"
        },
        "size": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

結合欄位的指令碼無法使用全域序數，因此比在單一欄位上彙總更慢。為獲得更好的效能，請考慮使用 [`multi_terms` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/)，或在編製索引時使用 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 建立合併欄位。

## 跨索引混合欄位類型

當相同欄位名稱在不同索引中具有不同的數值類型時（例如，一個索引中為 `long`，另一個索引中為 `double`），`terms` 彙總會將值提升為更廣泛的類型。非小數值會轉型為 `double`，這可能導致超過 2^53 的值失去精確度。
{: .warning}

## 執行提示

OpenSearch 可透過下列兩種方式之一收集詞彙：

- `global_ordinals`：使用欄位的全域序數進行彙總，為每個序數指派一個桶。這是 `keyword` 欄位的預設值。
- `map`：直接在對應表中彙總欄位值。僅在符合查詢的文件非常少時，才考慮使用此選項。否則，`global_ordinals` 通常較快。

OpenSearch 會自動選取模式，因此您很少需要設定 `execution_hint`。下列範例會請求 `map` 模式：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response.keyword",
        "execution_hint": "map"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含的桶與未使用 `execution_hint` 的請求相同，只有收集方式不同。若要確認 OpenSearch 使用的方式，請在搜尋請求中將 `profile` 設為 `true`，並檢查回應中的彙總器類型。

當請求的模式不適用時，OpenSearch 會忽略 `execution_hint`。例如，數值欄位和指令碼沒有序數，因此一律不使用全域序數進行彙總。
{: .note}

## 遺漏值

`missing` 參數會為不含目標欄位的文件指派一個值，並將這些文件放入對應的桶中。根據預設，不含該欄位的文件會從彙總中排除。在範例資料中，大部分文件都不含 `memory` 欄位。下列範例會將值 `-1` 指派給這些文件：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "memory": {
      "terms": {
        "field": "memory",
        "size": 3,
        "missing": -1
      }
    }
  }
}
```
{% include copy-curl.html %}

`-1` 桶包含 13,522 份沒有 `memory` 值的文件：

```json
{
  ...
  "aggregations" : {
    "memory" : {
      "doc_count_error_upper_bound" : 2,
      "sum_other_doc_count" : 439,
      "buckets" : [
        {
          "key" : -1.0,
          "doc_count" : 13522
        },
        {
          "key" : 73240.0,
          "doc_count" : 101
        },
        {
          "key" : 0.0,
          "doc_count" : 12
        }
      ]
    }
  }
}
```

`missing` 值會與其他任何值一樣處理，因此遺漏欄位的文件會與包含該值的文件合併。例如，在前述請求中將 `missing` 設為 `0`，會產生單一 `0` 桶，其中包含 13,534 份文件：13,522 份不含該欄位的文件，以及 12 份 `memory` 值為 `0` 的文件。若要將遺漏欄位的文件保留在獨立的桶中，請選擇該欄位中不會出現的值。

## 指令碼

您可以使用 `script` 取代 `field`，以動態計算詞彙值。下列範例會根據 `bytes` 欄位，將記錄檔項目分類為不同的大小類別：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "byte_ranges": {
      "terms": {
        "script": {
          "source": "if (doc['bytes'].value < 5000) return 'small'; if (doc['bytes'].value < 10000) return 'medium'; return 'large';"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會將文件分組至計算出的類別中：

```json
{
  ...
  "aggregations" : {
    "byte_ranges" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "medium",
          "doc_count" : 6995
        },
        {
          "key" : "small",
          "doc_count" : 6377
        },
        {
          "key" : "large",
          "doc_count" : 702
        }
      ]
    }
  }
}
```

### 預存指令碼

若要重複使用指令碼，請使用 [Create or Update Stored Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/) 儲存指令碼，並透過 `id` 參照該指令碼。請在 `params` 中傳遞指令碼所需的任何值。下列請求會儲存一個指令碼，該指令碼會在欄位值後方附加後綴：

```json
PUT _scripts/os_label
{
  "script": {
    "lang": "painless",
    "source": "doc[params.field].value + params.suffix"
  }
}
```
{% include copy-curl.html %}

下列彙總會對 `machine.os.keyword` 欄位執行預存指令碼：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os": {
      "terms": {
        "size": 3,
        "script": {
          "id": "os_label",
          "params": {
            "field": "machine.os.keyword",
            "suffix": " (OS)"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含 `win xp (OS)` 和 `osx (OS)` 等鍵。

### 值指令碼

同時指定 `field` 和 `script` 時，指令碼會作為值指令碼，並以 `_value` 接收欄位值。下列範例會在每個回應碼前加上「HTTP 」：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "responses_prefixed": {
      "terms": {
        "field": "response.keyword",
        "script": {
          "source": "'HTTP ' + _value"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會顯示轉換後的鍵：

```json
{
  ...
  "aggregations" : {
    "responses_prefixed" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "HTTP 200",
          "doc_count" : 12832
        },
        {
          "key" : "HTTP 404",
          "doc_count" : 801
        },
        {
          "key" : "HTTP 503",
          "doc_count" : 441
        }
      ]
    }
  }
}
```

## 處理預先彙總的資料

雖然 `doc_count` 欄位可呈現桶中所彙總的個別文件數量，但 `doc_count` 本身無法正確遞增儲存預先彙總資料的文件。若要處理預先彙總的資料並準確計算桶中的文件數量，您可以使用 `_doc_count` 欄位，在單一摘要欄位中加入文件數量。當文件包含 `_doc_count` 欄位時，所有桶彙總都會辨識其值，並累加桶的 `doc_count`。使用 `_doc_count` 欄位時，請注意下列事項：

* 此欄位不支援巢狀陣列，且只能使用正整數。
* 如果文件不含 `_doc_count` 欄位，彙總會使用該文件將計數加 1。

依賴準確文件計數的 OpenSearch 功能，說明了使用 `_doc_count` 欄位的重要性。若要了解如何使用此欄位支援其他搜尋工具，請參閱[索引彙整]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/)，這是 Index Management (IM) 外掛程式的 OpenSearch 功能，會將含有預先彙總資料的文件儲存在彙整索引中。
{: .tip}

下列請求會將三份文件編製索引，每份文件的 `_doc_count` 欄位中都包含預先彙總的資料：

```json
PUT /my_index/_doc/1
{
  "response_code": 404,
  "date":"2022-08-05",
  "_doc_count": 20
}
```
{% include copy-curl.html %}

```json
PUT /my_index/_doc/2
{
  "response_code": 404,
  "date":"2022-08-06",
  "_doc_count": 10
}
```
{% include copy-curl.html %}

```json
PUT /my_index/_doc/3?refresh
{
  "response_code": 200,
  "date":"2022-08-06",
  "_doc_count": 300
}
```
{% include copy-curl.html %}

下列請求會對 `response_code` 欄位執行 `terms` 彙總：

```json
GET /my_index/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field" : "response_code"
      }
    }
  }
}
```
{% include copy-curl.html %}

桶的文件計數是 `_doc_count` 值的總和，而不是已編製索引的文件數量：

```json
{
  "took" : 20,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "response_codes" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : 200,
          "doc_count" : 300
        },
        {
          "key" : 404,
          "doc_count" : 30
        }
      ]
    }
  }
}
```