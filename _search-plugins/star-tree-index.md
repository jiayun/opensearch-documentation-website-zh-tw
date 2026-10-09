---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Star-tree index
parent: Improving search performance
nav_order: 50
---

# Star-tree index

_star-tree index_（星狀樹索引）是一種專門設計的索引結構，透過在不同粒度層級預先計算並儲存彙總值來提升彙總效能。這種索引技術能加快彙總的執行速度，尤其是多欄位彙總。

啟用 star-tree 索引後，如果篩選欄位符合 star-tree 對應組態中定義的維度，且彙總欄位符合定義的指標，OpenSearch 會自動建立並使用 star-tree 索引來最佳化支援的彙總。您不需要變更查詢語法或請求參數。

當您想加速彙總時，可以使用 star-tree 索引：

- Star-tree 索引原生支援多欄位彙總。
- Star-tree 索引會在編製索引程序中即時建立，因此 star-tree 中的資料永遠是最新的。
- Star-tree 索引會彙總資料，以提升分頁效率並減少搜尋查詢時的磁碟 I/O。

## Star-tree 索引結構

Star-tree 索引會跨維度欄位組合來組織與彙總資料，並在匯入期間每次分段被排清或重新整理時，為所有維度組合預先計算指標值。這種結構讓 OpenSearch 能快速處理彙總查詢，而不需要掃描每份文件。

以下是 star-tree 組態範例：

```json
"ordered_dimensions": [
  {
    "name": "status"
  },
  {
    "name": "port"
  }
],
"metrics": [
  {
    "name": "size",
    "stats": [
      "sum"
    ]
  },
  {
    "name": "latency",
    "stats": [
      "avg"
    ]
  }
]
```

此組態定義了以下內容：

* 兩個維度欄位：`status` 與 `port`。`ordered_dimension` 欄位指定資料的排序方式（先依 `status`，再依 `port`）。
* 兩個指標欄位：`size` 與 `latency`，以及對應的彙總（`sum` 與 `avg`）。對於每個不重複的維度組合，指標值（`Sum(size)` 與 `Avg(latency)`）會預先彙總並儲存在 star-tree 結構中。

OpenSearch 會根據此組態建立 star-tree 索引結構。樹中的每個節點對應某個維度的一個值（或萬用字元 `*`）。查詢時，OpenSearch 會根據查詢中提供的維度值走訪這棵樹。

### 葉節點

葉節點包含針對特定維度組合預先計算的指標彙總。這些值以 doc values 形式儲存，並由 star-tree 節點參照。

`max_leaf_docs` 設定控制每個葉節點可參照的文件數量，透過限制任一節點掃描的文件數，有助於讓查詢延遲保持可預測。

### Star 節點

_star node_（星狀節點，在下圖中標記為 `*`）會彙總特定維度的所有值。如果查詢未指定該維度的篩選條件，OpenSearch 會從 star 節點擷取預先計算的彙總，而不是逐一迭代多個葉節點。例如，如果查詢篩選 `port` 但未篩選 `status`，OpenSearch 可以使用彙總所有狀態值資料的 star 節點。

### 查詢如何使用 star-tree

下圖顯示為此範例建立的 star-tree 索引以及三個範例查詢路徑。請注意，圖中每個分支對應一個維度（`status` 與 `port`）。有些節點包含預先計算的彙總值（例如 `Sum(size)`），讓 OpenSearch 能在查詢時略過不必要的計算。

![包含兩個維度與兩個指標的 star-tree 索引]({{site.url}}{{site.baseurl}}/images/star-tree-index.png)

彩色箭頭顯示三個查詢範例：

* **藍色箭頭**：多 term 查詢搭配指標彙總
  該查詢同時篩選 `status = 200` 與 `port = 5600`，並計算請求大小的總和。

  * OpenSearch 走訪此路徑：`Root → 200 → 5600`
  * 它從 Doc ID 1 擷取指標，其中 `Sum(size) = 988`

* **綠色箭頭**：單一 term 查詢搭配指標彙總
  該查詢僅篩選 `status = 200`，並計算請求延遲的平均值。

  * OpenSearch 走訪此路徑：`Root → 200 → *`
  * 它從 Doc ID 5 擷取指標，其中 `Avg(latency) = 70`

* **紅色箭頭**：單一 term 查詢搭配指標彙總
  該查詢僅篩選 `port = 8443`，並計算請求大小的總和。

  * OpenSearch 走訪此路徑：`Root → * → 8443`
  * 它從 Doc ID 7 擷取指標，其中 `Sum(size) = 1111`

這些範例顯示 OpenSearch 如何在 star-tree 中選擇最短路徑，並使用預先彙總的值來有效率地處理查詢。

## 限制

請注意 star-tree 索引的以下限制：

- Star-tree 索引不支援更新或刪除。若要使用 star-tree 索引，資料應僅限附加。請參閱[啟用 star-tree 索引](#enabling-a-star-tree-index)。
- Star-tree 索引僅適用於以索引 star-tree 組態中定義的維度欄位進行篩選、並彙總所定義指標欄位的彙總查詢。
- 對 star-tree 組態的任何變更都需要重新編製索引。
- 不支援[陣列值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/index/#arrays)。
- 僅支援[特定查詢與彙總](#supported-queries-and-aggregations)。
- 避免使用 `_id` 這類高基數欄位作為維度，因為它們會大幅增加儲存空間使用量與查詢延遲。

## 啟用 star-tree 索引

Star-tree 索引行為由下列叢集層級與索引層級設定控制。索引層級設定的優先順序高於叢集設定。

| 設定                                     | 範圍   | 預設值 | 用途                                                                                                                              |
| ------------------------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `indices.composite_index.star_tree.enabled` | 叢集 | `true`  | 在整個叢集中啟用或停用 star-tree 搜尋最佳化。  |
| `index.composite_index`                     | 索引   | 無       | 為特定索引啟用 star-tree 索引。必須在建立索引時設定。                                                |
| `index.append_only.enabled`                 | 索引   | 無      | Star-tree 索引的必要設定。防止更新與刪除。必須設為 `true`。                                                      |
| `index.search.star_tree_index.enabled`      | 索引   | `true`  | 啟用或停用對該索引的搜尋查詢使用 star-tree 索引。                                                 |

將 `indices.composite_index.star_tree.enabled` 設為 `false` 會防止 OpenSearch 在搜尋時使用 star-tree 最佳化，但仍會建立 star-tree 索引結構。若要完全移除 star-tree 結構，您必須在不含 star-tree 對應的情況下重新編製資料索引。
{: .note}

## 進階 star-tree 索引設定

下列索引層級設定可對 star-tree 索引行為提供細緻的控制。這些設定是靜態的，表示必須在建立索引時設定，之後無法變更。

| 設定                                                    | 預設值 | 範圍      | 用途                                                                                                                              |
| ---------------------------------------------------------- | ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `index.composite_index.star_tree.default.max_leaf_docs`   | `10000` | 最小值：`1`   | 設定葉節點允許的最大文件數。較低的值可改善查詢延遲，但會增加儲存需求。  |
| `index.composite_index.star_tree.field.default.metrics`   | `["value_count", "sum"]` | 不適用 | 定義為 star-tree 彙總計算的預設指標。這些指標會預先計算，以加速彙總查詢。 |
| `index.composite_index.star_tree.field.max_base_metrics`  | `100`   | `4` 至 `100` | 控制可為 star-tree 欄位設定的基礎指標數量上限。指標越多，可用的彙總選項越多，但會增加索引大小。 |
| `index.composite_index.star_tree.field.max_dimensions`    | `10`    | `2` 至 `10`  | 設定可作為 star-tree 索引欄位的維度數量上限。會影響 star-tree 索引大小與查詢效能。 |
| `index.composite_index.star_tree.field.max_date_intervals` | `3`     | `1` 至 `3`   | 指定可為 star-tree 日期欄位設定的日期區間數量上限。控制時間粒度選項。 |
| `index.composite_index.star_tree.max_fields`              | `1`     | `1` 至 `1`   | 控制每個索引的 star-tree 欄位數量上限。每個索引僅支援一個 star-tree 欄位。            |


若要建立使用 star-tree 索引的索引，請傳送以下請求：

```json
PUT /logs
{
  "settings": {
    "index.composite_index": true,
    "index.append_only.enabled": true
  }
}
```
{% include copy-curl.html %}

請確保 star-tree 對應中使用的維度與指標欄位已啟用 `doc_values` 參數。大多數欄位類型預設已啟用此參數。如需更多資訊，請參閱 [Doc values]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)。

### 停用 star-tree 使用

根據預設，`indices.composite_index.star_tree.enabled` 叢集設定和 `index.search.star_tree_index.enabled` 索引設定都會設為 `true`。若要停用使用 star-tree 索引的搜尋，請將這兩個設定都設為 `false`。請注意，索引設定的優先順序高於叢集設定。

## 對應範例

以下範例顯示如何建立一個 star-tree 索引，在 `logs` 索引中預先計算彙總。`sum` 和 `average` 彙總分別針對 `size` 和 `latency` 欄位計算，涵蓋維度欄位中所有值的組合。維度的排序依序為 `status`、`port`，最後是 `method`，這決定了資料在樹狀結構中的組織方式：

```json
PUT /logs
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 0,
    "index.composite_index": true,
    "index.append_only.enabled": true
  },
  "mappings": {
    "composite": {
      "request_aggs": {
        "type": "star_tree",
        "config": {
          "date_dimension" : {
            "name": "@timestamp",
            "calendar_intervals": [
              "month",
              "day"
            ]
          },
          "ordered_dimensions": [
            {
              "name": "status"
            },
            {
              "name": "port"
            },
            {
              "name": "method"
            }
          ],
          "metrics": [
            {
              "name": "size",
              "stats": [
                "sum"
              ]
            },
            {
              "name": "latency",
              "stats": [
                "avg"
              ]
            }
          ]
        }
      }
    },
    "properties": {
      "status": {
        "type": "integer"
      },
      "port": {
        "type": "integer"
      },
      "size": {
        "type": "integer"
      },
      "method" : {
        "type": "keyword"
      },
      "latency": {
        "type": "scaled_float",
        "scaling_factor": 10
      }
    }
  }
}
```
{% include copy.html %}

如需 star-tree 索引對應和參數的詳細資訊，請參閱 [Star-tree 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/star-tree/)。

## 支援的查詢和彙總

Star-tree 索引會最佳化彙總。每個查詢都必須包含至少一個支援的彙總，才能使用 star-tree 最佳化。

### 支援的查詢

沒有彙總的查詢無法使用 star-tree 最佳化。查詢的欄位必須存在於 star-tree 組態的 `ordered_dimensions` 區段中。支援下列查詢：

- [Term 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/term/)
- [Terms 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/terms/)
- [Match all docs 查詢]({{site.url}}{{site.baseurl}}/query-dsl/match-all/)
- [Range 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)
- [Boolean 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)

#### Boolean 查詢限制

star-tree 索引中的 Boolean 查詢會針對每種子句類型遵循特定規則：

* `must` 和 `filter` 子句：
  - 兩者都支援，且處理方式相同，因為 `filter` 不會影響評分。
  - 可以跨不同維度運作。
  - 在所有 `must`/`filter` 子句中，每個維度只允許一個條件，包括巢狀子句。
  - 支援 term、terms 和 range 查詢。

* `should` 子句：
  - 必須在同一維度上運作，且不能跨不同維度運作
  - 只能使用 term、terms 和 range 查詢。

* `should` 子句內的 `must` 子句：
  - 做為必要條件。
  - 與外層 `must` 在同一維度上運作時：`should` 條件的聯集會與外層 `must` 條件取交集。
  - 在不同維度上運作時：會正常處理為必要條件。

* 不支援 `must_not` 子句。
* 不支援帶有 `minimum_should_match` 參數的查詢。

下列 Boolean 查詢**支援**，因為它遵循這些限制：

```json
{
  "bool": {
    "must": [
      {"term": {"method": "GET"}}
    ],
    "filter": [
      {"range": {"status": {"gte": 200, "lt": 300}}}
    ],
    "should": [
      {"term": {"port": 443}},
      {"term": {"port": 8443}}
    ]
  }
}
```
{% include copy.html %}

下列 Boolean 查詢**不**支援，因為它們違反這些限制：

```json
{
  "bool": {
    "should": [
      {"term": {"status": 200}},
      {"term": {"method": "GET"}}  // SHOULD across different dimensions
    ]
  }
}
```

```json
{
  "bool": {
    "must": [
      {"term": {"status": 200}}
    ],
    "must_not": [  // MUST_NOT not supported
      {"term": {"method": "DELETE"}}
    ]
  }
}
```

### 支援的彙總

star-tree 索引支援下列彙總。

#### 指標彙總
 
支援下列指標彙總：

- [Sum]({{site.url}}{{site.baseurl}}/aggregations/metric/sum/)
- [Minimum]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/)
- [Maximum]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/)
- [Value count]({{site.url}}{{site.baseurl}}/aggregations/metric/value-count/)
- [Average]({{site.url}}{{site.baseurl}}/aggregations/metric/average/)

若要在 star-tree 索引中使用可搜尋的彙總，請確定您符合下列先決條件：

- 欄位必須存在於 star-tree 組態的 `metrics` 區段中。
- 指標彙總類型必須是 `stats` 參數的一部分。

下列範例使用[對應範例](#example-mapping)，取得所有具有 `status=500` 的錯誤記錄中 `size` 欄位所有值的總和：

```json
POST /logs/_search
{
  "query": {
    "term": {
      "status": "500"
    }
  },
  "aggs": {
    "sum_size": {
      "sum": {
        "field": "size"
      }
    }
  }
}
```
{% include copy.html %}

使用 star-tree 索引時，結果會在走訪 `status=500` 節點時從單一彙總文件擷取，而不是掃描所有符合的文件。這可降低查詢延遲。

#### 搭配指標彙總的日期直方圖

您可以在日曆間隔上使用[日期直方圖]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)搭配指標子彙總。

若要在 star-tree 索引中使用日期直方圖彙總並使其可搜尋，請記住下列需求：

- star-tree 對應組態中的日曆間隔可以使用請求的日曆欄位，或使用比請求欄位粒度更低的欄位。例如，如果彙總使用 `month` 欄位，star-tree 搜尋仍可使用 `day` 等較低粒度的欄位。
- 指標子彙總必須是彙總請求的一部分。

下列範例會篩選記錄，只包含狀態碼介於 `200` 和 `400` 之間的記錄，並將回應的 `size` 設為 `0`，以便只傳回彙總結果。接著，它會依日曆月份彙總篩選後的記錄，並計算每個月請求的 `size` 總計：

```json
POST /logs/_search
{
    "size": 0,
    "query": {
        "range": {
            "status": {
                "gte": "200",
                "lte": "400"
            }
        }
    },
    "aggs": {
        "by_month": {
            "date_histogram": {
                "field": "@timestamp",
                "calendar_interval": "month"
            },
            "aggs": {
                "sum_size": {
                    "sum": {
                        "field": "size"
                    }
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

#### 關鍵字與數值詞彙彙總

您可以在關鍵字和數值欄位上，搭配 star-tree 索引搜尋使用[詞彙彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)。

若要讓 star-tree 搜尋與詞彙彙總相容，請記住下列行為：

- 詞彙彙總中使用的欄位，應該是 star-tree 索引中所定義維度的一部分。
- 只要相關指標是 star-tree 組態的一部分，指標子彙總即為選用。

下列範例依 `user_id` 欄位彙總記錄檔，並傳回每個不重複使用者的計數：

```json
POST /logs/_search
{
    "size": 0,
    "aggs": {
        "users": {
            "terms": {
                "field": "user_id"
            }
        }
    }
}
```
{% include copy-curl.html %}

下列範例依 `order_quantity` 彙總訂單，並計算每個數量的平均 `total_price`：

```json
POST /orders/_search
{
    "size": 0,
    "aggs": {
        "quantities": {
            "terms": {
                "field": "order_quantity"
            },
            "aggs": {
                "avg_total_price": {
                    "avg": {
                        "field": "total_price"
                    }
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

#### 範圍彙總

您可以在數值欄位上，搭配 star-tree 索引搜尋使用[範圍彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/)。

若要讓範圍彙總與 star-tree 索引有效搭配運作，請記住下列行為：

- 範圍彙總中使用的欄位，應該是 star-tree 索引中所定義維度的一部分。
- 只要相關指標是 star-tree 組態的一部分，您就可以加入指標子彙總，以在每個定義的範圍內計算指標。

下列範例根據 `temperature` 欄位的預先定義範圍彙總文件：

```json
POST /sensors/_search
{
    "size": 0,
    "aggs": {
        "temperature_ranges": {
            "range": {
                "field": "temperature",
                "ranges": [
                    { "to": 20 },
                    { "from": 20, "to": 30 },
                    { "from": 30 }
                ]
            }
        }
    }
}
```
{% include copy-curl.html %}

下列範例依價格範圍彙總銷售資料，並計算每個範圍內售出的 `quantity` 總數：

```json
POST /sales/_search
{
    "size": 0,
    "aggs": {
        "price_ranges": {
            "range": {
                "field": "price",
                "ranges": [
                    { "to": 100 },
                    { "from": 100, "to": 500 },
                    { "from": 500 }
                ]
            },
            "aggs": {
                "total_quantity": {
                    "sum": {
                        "field": "quantity"
                    }
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

#### 巢狀彙總

您可以在巢狀結構中合併多個支援的桶彙總 (例如 `terms` 和 `range`)，star-tree 索引將會最佳化這些巢狀彙總。如需巢狀彙總的詳細資訊，請參閱[巢狀彙總]({{site.url}}{{site.baseurl}}/aggregations/#nested-aggregations)。

#### 多重詞彙彙總

當彙總欄位在 star-tree 組態中定義為維度時，star-tree 索引會最佳化 `multi_terms` 彙總。如需多重詞彙彙總的詳細資訊，請參閱[多重詞彙彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/)。

## 後續步驟

- [Star-tree 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/star-tree/)
