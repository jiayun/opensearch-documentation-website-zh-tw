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

`terms` 彙總會為欄位中的每個不重複詞彙動態建立一個桶。

## 參數

`terms` 彙總接受下列參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 選用 | 字串 | 要進行彙總的欄位。必須是 `keyword`、`numeric`、`ip`、`boolean` 或 `date` 欄位。`field` 或 `script` 其中之一為必要參數。 |
| `script` | 選用 | 物件 | 產生用於彙總之值的指令碼。`field` 或 `script` 其中之一為必要參數。與 `field` 搭配使用時，此指令碼會作為值指令碼，並透過 `_value` 接收欄位值。 |
| `size` | 選用 | 整數 | 要傳回的桶數。預設為 `10`。 |
| `shard_size` | 選用 | 整數 | 從每個分片收集的候選詞彙數。較高的值可提高準確度。預設為 `size * 1.5 + 10`。 |
| `min_doc_count` | 選用 | 整數 | 桶要納入回應所需的最小文件數。預設為 `1`。 |
| `shard_min_doc_count` | 選用 | 整數 | 詞彙要成為候選詞彙，在分片層級所需的最小文件數。預設為 `0`。 |
| `show_term_doc_count_error` | 選用 | 布林值 | 設為 `true` 時，會包含每個桶的誤差估計值。預設為 `false`。 |
| `order` | 選用 | 物件 | 控制桶的排序順序。接受 `_count`、`_key` 或子彙總指標的名稱，每個項目都搭配 `asc` 或 `desc`。預設為 `{"_count": "desc"}`。 |
| `include` | 選用 | 字串、陣列或物件 | 篩選哪些詞彙值可以建立桶。接受正規表示式字串、精確值的陣列或 `partition` 物件。 |
| `exclude` | 選用 | 字串或陣列 | 篩選哪些詞彙值不能建立桶。接受正規表示式字串或精確值的陣列。 |
| `missing` | 選用 | 字串或數字 | 缺少目標欄位的文件所使用的值，讓這些文件歸入對應的桶。預設會忽略缺少欄位的文件。 |
| `execution_hint` | 選用 | 字串 | 控制詞彙的收集方式。有效值為 `map`（直接將值保留在記憶體中）和 `global_ordinals`（使用序數對應，對高基數欄位而言更節省記憶體）。OpenSearch 會自動選取最佳選項。 |
| `collect_mode` | 選用 | 字串 | 控制巢狀彙總的計算方式。有效值為：<br> - `depth_first`：先展開所有分支，再進行剪枝。<br> - `breadth_first`：在每個層級先進行剪枝，再展開，以減少深層巢狀彙總的記憶體用量。<br><br>預設為 `depth_first`。 |

## 範例

下列範例使用 `terms` 彙總，找出網頁記錄資料中每個回應碼的文件數：

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

#### 回應範例

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

這些值會以 `key` 索引鍵傳回。
`doc_count` 指定每個桶中的文件數。預設會依 `doc-count` 遞減排序桶。

您可以使用 `terms`，依計數遞增排序傳回的值（`"order": {"count": "asc"}`），以搜尋低頻值。不過，我們強烈不建議採用這種做法，因為涉及多個分片時，可能會產生不準確的結果。整體而言出現頻率低的詞彙，在每個個別分片上不一定都屬於低頻詞彙，也可能完全未出現在某些分片傳回的最低頻結果中。反之，在某個分片上出現頻率低的詞彙，在另一個分片上可能很常見。在這兩種情況下，分片層級的彙總都可能遺漏罕見詞彙，導致整體結果不正確。我們建議使用 `rare_terms` 彙總來取代 `terms` 彙總，前者專為更準確地處理這些情況而設計。
{: .warning}


## size 和 shard_size 參數

`terms` 彙總傳回的桶數由 `size` 參數控制，其預設值為 10。

此外，負責彙總的協調節點會向每個分片請求排名最前面的不重複詞彙。每個分片傳回的桶數由 `shard_size` 參數控制。此參數與 `size` 參數不同，其用途是提高桶內文件計數的準確度。

例如，假設 `size` 和 `shard_size` 參數的值都是 3。`terms` 彙總會向每個分片請求排名前三的不重複詞彙。協調節點會彙總這些結果，以計算最終結果。如果分片包含未列入前三名的物件，該物件就不會出現在回應中。不過，提高此請求的 `shard_size` 值，可讓每個分片傳回更多不重複詞彙，提高協調節點收到所有相關結果的機率。

預設情況下，`shard_size` 參數設為 `size * 1.5 + 10`。

使用並行區段搜尋時，`shard_size` 參數也會套用至每個區段切片。 

`shard_size` 參數可用於平衡 `terms` 彙總的效能與文件計數準確度。較高的 `shard_size` 值可確保較高的文件計數準確度，但會增加記憶體與運算資源用量。較低的 `shard_size` 值可提供較佳效能，但會降低文件計數準確度。

## 文件計數誤差

回應也包含兩個名為 `doc_count_error_upper_bound` 和 `sum_other_doc_count` 的索引鍵。

`terms` 彙總會傳回排名最前面的不重複詞彙。因此，如果資料包含許多不重複詞彙，其中一些可能不會出現在結果中。`sum_other_doc_count` 欄位代表未納入回應的文件總數。在此範例中，這個數字為 0，因為所有不重複值都出現在回應中。 

`doc_count_error_upper_bound` 欄位代表未納入最終結果之不重複值的最大可能計數。使用此欄位可估計計數的誤差範圍。 

`doc_count_error_upper_bound` 值與準確度的概念僅適用於使用預設排序順序的彙總，也就是依文件數遞減排序。這是因為依文件數遞減排序時，可以確保任何未傳回詞彙所包含的文件數，都等於或少於已傳回詞彙所包含的文件數。根據這一點，您可以計算 `doc_count_error_upper_bound`。

如果將 `show_term_doc_count_error` 參數設為 `true`，`terms` 彙總除了顯示整體值，也會顯示為每個不重複桶計算的 `doc_count_error_upper_bound`。

## `min_doc_count` 和 `shard_min_doc_count` 參數

您可以使用 `min_doc_count` 參數篩選掉結果少於 `min_doc_count` 筆的任何唯一詞彙。`min_doc_count` 門檻值只會在合併從所有分片擷取的結果之後才套用。每個分片都不知道特定詞彙的全域文件計數。如果全域前 `shard_size` 個最常出現的詞彙與分片本機的前幾個詞彙之間有顯著差異，使用 `min_doc_count` 參數時，您可能會收到非預期的結果。

另外，`shard_min_doc_count` 參數用於篩選掉分片傳回給協調節點、結果少於 `shard_min_doc_count` 筆的唯一詞彙。

使用並行區段搜尋時，`shard_min_doc_count` 參數不會套用至每個區段切片。如需詳細資訊，請參閱[相關的 GitHub 問題](https://github.com/opensearch-project/OpenSearch/issues/11847)。

## 將值篩選為子集

您可以使用 `include` 和 `exclude` 參數篩選出現在彙總桶中的詞彙值。同時指定這兩個參數時，會先評估 `include`，再將 `exclude` 套用至結果。

### 規則運算式篩選

`include` 和 `exclude` 參數都接受採用 Lucene [規則運算式語法]({{site.url}}{{site.baseurl}}/query-dsl/regex-syntax/)的規則運算式字串：

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

根據預設，規則運算式字串的長度上限為 1000 個字元。您可以使用 `index.max_regex_length` 索引設定變更此限制。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

### 精確值篩選

`include` 和 `exclude` 參數都接受精確值陣列：

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

`include` 和 `exclude` 參數必須使用相同的格式：規則運算式字串或精確值陣列。

## 分頁瀏覽所有詞彙

當欄位包含太多唯一詞彙，無法在單一請求中擷取時，您可以使用以分割區為基礎的篩選，透過傳送多個請求來擷取所有詞彙。詞彙會使用雜湊函式指派給分割區，因此分布大致平均。

若要擷取所有唯一詞彙，請傳送與 `num_partitions` 數量相同的請求。在 `include` 參數中指定 `partition` 和 `num_partitions`。每個請求都保持 `num_partitions` 不變，並將 `partition` 從 `0` 遞增至 `num_partitions - 1`：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "partitioned_terms": {
      "terms": {
        "field": "response.keyword",
        "size": 10000,
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

`include` 參數在每個請求中只能使用一種格式：規則運算式字串、值陣列或 `partition` 物件。因此，您無法將篩選（以規則運算式或陣列為基礎）與以分割區為基礎的擷取結合使用。使用以分割區為基礎的擷取時，不支援 `exclude` 參數。
{: .note}


## 收集模式

可用的收集模式有兩種：`depth_first` 和 `breadth_first`。`depth_first` 收集模式會以深度優先的方式展開彙總樹狀結構的所有分支，並且只會在展開完成後才執行修剪。

然而，使用巢狀 `terms` 彙總時，傳回的桶數量基數會乘以每一層巢狀欄位的基數，因此當您將彙總巢狀化時，很容易出現桶數量的組合爆炸。

您可以使用 `breadth_first` 收集模式來解決此問題。在此情況下，會先對彙總樹狀結構的第一層套用修剪，再展開至下一層，這可能會大幅減少計算的桶數量。

此外，執行 `breadth_first` 收集會產生記憶體額外負荷，且與相符文件的數量呈線性關係。這是因為 `breadth_first` 收集的運作方式是快取並重播來自上層的已修剪桶集合。


## 排序順序

根據預設，桶會依 `_count` 遞減排序（文件最多者排在最前面）。您可以使用 `order` 參數變更排序順序。下列範例依字母順序排序回應碼：

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

回應會傳回依索引鍵遞增排序的桶：

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

若要依彙總樹狀結構中更深層的巢狀指標排序，請使用 `>` 分隔符號指定路徑。下列範例僅依作業系統成功（200）回應的平均位元組數來排序作業系統：

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

回應會依巢狀的 `avg_bytes` 指標排序作業系統桶：

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

管線彙總無法用於排序。
{: .note}

## 多欄位 terms 彙總

`terms` 彙總並未原生支援多個欄位。若要依欄位組合分組，請使用 [`multi_terms` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/)，或使用結合欄位值的 `script`：

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

為了提升效能，請考慮使用 [`multi_terms` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/)，或在編製索引時使用 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 建立組合欄位。

## 跨索引混用欄位類型

當相同欄位名稱在不同索引中具有不同的數值類型（例如，在一個索引中為 `long`，在另一個索引中為 `double`）時，`terms` 彙總會將值提升為範圍較大的類型。非小數值會轉型為 `double`，這可能導致超過 2^53 的值失去精確度。
{: .warning}

## 缺少的值

`missing` 參數會為沒有目標欄位的文件指定一個值，將這些文件放入對應的桶中。預設情況下，沒有該欄位的文件會排除在彙總之外。下列範例會將 `"unknown"` 指定給任何缺少 `machine.os.keyword` 欄位的文件：

```json
GET /opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "os": {
      "terms": {
        "field": "machine.os.keyword",
        "missing": "unknown"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 指令碼

您可以使用 `script` 取代 `field`，以動態計算詞項值。下列範例會根據 `bytes` 欄位，將記錄項目分類到不同的大小類別：

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

回應會將文件分組到計算出的類別中：

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

### 值指令碼

同時指定 `field` 和 `script` 時，指令碼會作為值指令碼運作，並以 `_value` 接收欄位值。下列範例會在每個回應碼前加上「HTTP 」：

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

## 將預先彙總的資料納入計算

雖然 `doc_count` 欄位表示桶中彙總的個別文件數量，但 `doc_count` 本身無法正確累加儲存預先彙總資料的文件所代表的文件數量。若要將預先彙總的資料納入計算，並準確計算桶中的文件數量，您可以使用 `_doc_count` 欄位，在單一摘要欄位中加入文件數量。當文件包含 `_doc_count` 欄位時，所有桶彙總都會辨識其值，並累加桶的 `doc_count`。使用 `_doc_count` 欄位時，請注意下列事項：

* 此欄位不支援巢狀陣列；只能使用正整數。
* 如果文件不包含 `_doc_count` 欄位，彙總會使用該文件將計數增加 1。

依賴準確文件計數的 OpenSearch 功能說明了使用 `_doc_count` 欄位的重要性。若要瞭解如何使用此欄位來支援其他搜尋工具，請參閱[索引彙整]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/)。這是 Index Management（IM）外掛程式的 OpenSearch 功能，可將含有預先彙總資料的文件儲存在彙整索引中。
{: .tip}

#### 範例請求

```json
PUT /my_index/_doc/1
{
  "response_code": 404,
  "date":"2022-08-05",
  "_doc_count": 20
}

PUT /my_index/_doc/2
{
  "response_code": 404,
  "date":"2022-08-06",
  "_doc_count": 10
}

PUT /my_index/_doc/3
{
  "response_code": 200,
  "date":"2022-08-06",
  "_doc_count": 300
}

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

#### 範例回應

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