---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Profile
parent: Search APIs
nav_order: 55
redirect_from:
  - /api-reference/profile/
---

# Profile API
**於 1.0 版導入**
{: .label .label-purple }

Profile API 提供搜尋請求中各個元件執行時間的資訊。使用 Profile API，您可以對緩慢的請求進行除錯，並了解如何改善其效能。Profile API 不會測量以下項目：

- 網路延遲
- 請求在佇列中等待的時間
- 在協調節點上合併分片回應時的閒置時間

Profile API 是一種消耗資源的操作，會為搜尋作業增加額外負擔。
{: .warning}

## 端點

```json
GET /testindex/_search
{
  "profile": true,
  "query" : {
    "match" : { "title" : "wind" }
  }
}
```

## 並行分段搜尋

[並行分段搜尋]({{site.url}}{{site.baseurl}}/search-plugins/concurrent-segment-search/)允許每個分片層級的請求在查詢階段以平行方式搜尋分段。Profile API 回應包含數個額外欄位，提供有關 _工作切片（slice）_ 的統計資訊。

工作切片是可由執行緒執行的工作單位。每個查詢可以分割成多個工作切片，每個工作切片包含一或多個分段。所有工作切片可以平行執行，或依集區中可用的執行緒以某種順序執行。

一般而言，最大/最小/平均工作切片時間會針對某種計時類型彙整所有工作切片的統計資料。例如，在剖析彙總時，`aggregations` 區段中的 `max_slice_time_in_nanos` 欄位會顯示彙總操作及其子項在所有工作切片中消耗的最長時間。

## 範例請求：非並行搜尋

若要使用 Profile API，請在傳送至 `_search` 端點的搜尋請求中加入設為 `true` 的 `profile` 參數：

<!-- spec_insert_start
component: example_code
rest: GET /testindex/_search
body: |
{
  "profile": true,
  "query" : {
    "match" : { "title" : "wind" }
  }
}
-->
{% capture step1_rest %}
GET /testindex/_search
{
  "profile": true,
  "query": {
    "match": {
      "title": "wind"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "testindex",
  body =   {
    "profile": true,
    "query": {
      "match": {
        "title": "wind"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要啟用人類可讀的格式，請在請求中加入 `?human=true` 查詢參數：

<!-- spec_insert_start
component: example_code
rest: GET /testindex/_search?human=true
body: |
{
  "profile": true,
  "query" : {
    "match" : { "title" : "wind" }
  }
}
-->
{% capture step1_rest %}
GET /testindex/_search?human=true
{
  "profile": true,
  "query": {
    "match": {
      "title": "wind"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "testindex",
  params = { "human": "true" },
  body =   {
    "profile": true,
    "query": {
      "match": {
        "title": "wind"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應會包含一個額外的 `time` 欄位，並附上人類可讀的單位，例如：

```json
"collector": [
    {
        "name": "SimpleTopScoreDocCollector",
        "reason": "search_top_hits",
        "time": "113.7micros",
        "time_in_nanos": 113711
    }
]
```

Profile API 的回應十分冗長，因此如果您是透過 `curl` 命令執行請求，請加入 `?pretty` 查詢參數，讓回應更容易理解。
{: .tip}

## 範例請求：彙總

若要剖析彙總，請傳送彙總請求，並提供設為 `true` 的 `profile` 參數。

### 全域彙總

<!-- spec_insert_start
component: example_code
rest: GET /opensearch_dashboards_sample_data_ecommerce/_search
body: |
{
  "profile": "true",
  "size": 0,
  "query": {
    "match": { "manufacturer": "Elitelligence" }
  },
  "aggs": {
    "all_products": {
      "global": {},
      "aggs": {
      "avg_price": { "avg": { "field": "taxful_total_price" } }
      }
    },
    "elitelligence_products": { "avg": { "field": "taxful_total_price" } }
  }
}
-->
{% capture step1_rest %}
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "profile": "true",
  "size": 0,
  "query": {
    "match": {
      "manufacturer": "Elitelligence"
    }
  },
  "aggs": {
    "all_products": {
      "global": {},
      "aggs": {
        "avg_price": {
          "avg": {
            "field": "taxful_total_price"
          }
        }
      }
    },
    "elitelligence_products": {
      "avg": {
        "field": "taxful_total_price"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "opensearch_dashboards_sample_data_ecommerce",
  body =   {
    "profile": "true",
    "size": 0,
    "query": {
      "match": {
        "manufacturer": "Elitelligence"
      }
    },
    "aggs": {
      "all_products": {
        "global": {},
        "aggs": {
          "avg_price": {
            "avg": {
              "field": "taxful_total_price"
            }
          }
        }
      },
      "elitelligence_products": {
        "avg": {
          "field": "taxful_total_price"
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 非全域彙總

<!-- spec_insert_start
component: example_code
rest: GET /opensearch_dashboards_sample_data_ecommerce/_search
body: |
{
  "size": 0,
  "aggs": {
    "avg_taxful_total_price": {
      "avg": {
        "field": "taxful_total_price"
      }
    }
  }
}
-->
{% capture step1_rest %}
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "avg_taxful_total_price": {
      "avg": {
        "field": "taxful_total_price"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "opensearch_dashboards_sample_data_ecommerce",
  body =   {
    "size": 0,
    "aggs": {
      "avg_taxful_total_price": {
        "avg": {
          "field": "taxful_total_price"
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應：非並行搜尋

回應包含剖析資訊：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 21,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.19363807,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.19363807,
        "_source": {
          "title": "The wind rises"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.17225474,
        "_source": {
          "title": "Gone with the wind",
          "description": "A 1939 American epic historical film"
        }
      }
    ]
  },
  "profile": {
    "shards": [
      {
        "id": "[LidyZ1HVS-u93-73Z49dQg][testindex][0]",
        "inbound_network_time_in_millis": 0,
        "outbound_network_time_in_millis": 0,
        "searches": [
          {
            "query": [
              {
                "type": "BooleanQuery",
                "description": "title:wind title:rise",
                "time_in_nanos": 2473919,
                "breakdown": {
                  "set_min_competitive_score_count": 0,
                  "match_count": 0,
                  "shallow_advance_count": 0,
                  "set_min_competitive_score": 0,
                  "next_doc": 5209,
                  "match": 0,
                  "next_doc_count": 2,
                  "score_count": 2,
                  "compute_max_score_count": 0,
                  "compute_max_score": 0,
                  "advance": 9209,
                  "advance_count": 2,
                  "score": 20751,
                  "build_scorer_count": 4,
                  "create_weight": 1404458,
                  "shallow_advance": 0,
                  "create_weight_count": 1,
                  "build_scorer": 1034292
                },
                "children": [
                  {
                    "type": "TermQuery",
                    "description": "title:wind",
                    "time_in_nanos": 813581,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 3291,
                      "match": 0,
                      "next_doc_count": 2,
                      "score_count": 2,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 7208,
                      "advance_count": 2,
                      "score": 18666,
                      "build_scorer_count": 6,
                      "create_weight": 616375,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 168041
                    }
                  },
                  {
                    "type": "TermQuery",
                    "description": "title:rise",
                    "time_in_nanos": 191083,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 0,
                      "match": 0,
                      "next_doc_count": 0,
                      "score_count": 0,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 0,
                      "advance_count": 0,
                      "score": 0,
                      "build_scorer_count": 2,
                      "create_weight": 188625,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 2458
                    }
                  }
                ]
              }
            ],
            "rewrite_time": 192417,
            "collector": [
              {
                "name": "SimpleTopScoreDocCollector",
                "reason": "search_top_hits",
                "time_in_nanos": 77291
              }
            ]
          }
        ],
        "aggregations": []
      }
    ]
  }
}
```
</details>

### 並行分段搜尋

以下是具有三個分段工作切片的並行分段搜尋範例回應：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      ...
    ]
  },
  "aggregations": {
    ...
  },
  "profile": {
    "shards": [
      {
        "id": "[9Y7lbpaWRhyr5Y-41Zl48g][idx][0]",
        "inbound_network_time_in_millis": 0,
        "outbound_network_time_in_millis": 0,
        "searches": [
          {
            "query": [
              {
                "type": "MatchAllDocsQuery",
                "description": "*:*",
                "time_in_nanos": 868000,
                "max_slice_time_in_nanos": 19376,
                "min_slice_time_in_nanos": 12250,
                "avg_slice_time_in_nanos": 16847,
                "breakdown": {
                  "max_match": 0,
                  "set_min_competitive_score_count": 0,
                  "match_count": 0,
                  "avg_score_count": 1,
                  "shallow_advance_count": 0,
                  "next_doc": 29708,
                  "min_build_scorer": 3125,
                  "score_count": 5,
                  "compute_max_score_count": 0,
                  "advance": 0,
                  "min_set_min_competitive_score": 0,
                  "min_advance": 0,
                  "score": 29250,
                  "avg_set_min_competitive_score_count": 0,
                  "min_match_count": 0,
                  "avg_score": 333,
                  "max_next_doc_count": 3,
                  "max_compute_max_score_count": 0,
                  "avg_shallow_advance": 0,
                  "max_shallow_advance_count": 0,
                  "set_min_competitive_score": 0,
                  "min_build_scorer_count": 2,
                  "next_doc_count": 8,
                  "min_match": 0,
                  "avg_next_doc": 888,
                  "compute_max_score": 0,
                  "min_set_min_competitive_score_count": 0,
                  "max_build_scorer": 5791,
                  "avg_match_count": 0,
                  "avg_advance": 0,
                  "build_scorer_count": 6,
                  "avg_build_scorer_count": 2,
                  "min_next_doc_count": 2,
                  "min_shallow_advance_count": 0,
                  "max_score_count": 2,
                  "avg_match": 0,
                  "avg_compute_max_score": 0,
                  "max_advance": 0,
                  "avg_shallow_advance_count": 0,
                  "avg_set_min_competitive_score": 0,
                  "avg_compute_max_score_count": 0,
                  "avg_build_scorer": 4027,
                  "max_set_min_competitive_score_count": 0,
                  "advance_count": 0,
                  "max_build_scorer_count": 2,
                  "shallow_advance": 0,
                  "min_compute_max_score": 0,
                  "max_match_count": 0,
                  "create_weight_count": 1,
                  "build_scorer": 32459,
                  "max_set_min_competitive_score": 0,
                  "max_compute_max_score": 0,
                  "min_shallow_advance": 0,
                  "match": 0,
                  "max_shallow_advance": 0,
                  "avg_advance_count": 0,
                  "min_next_doc": 708,
                  "max_advance_count": 0,
                  "min_score": 291,
                  "max_next_doc": 999,
                  "create_weight": 1834,
                  "avg_next_doc_count": 2,
                  "max_score": 376,
                  "min_compute_max_score_count": 0,
                  "min_score_count": 1,
                  "min_advance_count": 0
                }
              }
            ],
            "rewrite_time": 8126,
            "collector": [
              {
                "name": "QueryCollectorManager",
                "reason": "search_multi",
                "time_in_nanos": 564708,
                "reduce_time_in_nanos": 1251042,
                "max_slice_time_in_nanos": 121959,
                "min_slice_time_in_nanos": 28958,
                "avg_slice_time_in_nanos": 83208,
                "slice_count": 3,
                "children": [
                  {
                    "name": "SimpleTopDocsCollectorManager",
                    "reason": "search_top_hits",
                    "time_in_nanos": 500459,
                    "reduce_time_in_nanos": 840125,
                    "max_slice_time_in_nanos": 22168,
                    "min_slice_time_in_nanos": 5792,
                    "avg_slice_time_in_nanos": 12084,
                    "slice_count": 3
                  },
                  {
                    "name": "NonGlobalAggCollectorManager: [histo]",
                    "reason": "aggregation",
                    "time_in_nanos": 552167,
                    "reduce_time_in_nanos": 311292,
                    "max_slice_time_in_nanos": 95333,
                    "min_slice_time_in_nanos": 18416,
                    "avg_slice_time_in_nanos": 66249,
                    "slice_count": 3
                  }
                ]
              }
            ]
          }
        ],
        "aggregations": [
          {
            "type": "NumericHistogramAggregator",
            "description": "histo",
            "time_in_nanos": 2847834,
            "max_slice_time_in_nanos": 117374,
            "min_slice_time_in_nanos": 20624,
            "avg_slice_time_in_nanos": 75597,
            "breakdown": {
              "min_build_leaf_collector": 9500,
              "build_aggregation_count": 3,
              "post_collection": 3209,
              "max_collect_count": 2,
              "initialize_count": 3,
              "reduce_count": 0,
              "avg_collect": 17055,
              "max_build_aggregation": 26000,
              "avg_collect_count": 1,
              "max_build_leaf_collector": 64833,
              "min_build_leaf_collector_count": 1,
              "build_aggregation": 41125,
              "min_initialize": 583,
              "max_reduce": 0,
              "build_leaf_collector_count": 3,
              "avg_reduce": 0,
              "min_collect_count": 1,
              "avg_build_leaf_collector_count": 1,
              "avg_build_leaf_collector": 45000,
              "max_collect": 24625,
              "reduce": 0,
              "avg_build_aggregation": 12013,
              "min_post_collection": 292,
              "max_initialize": 1333,
              "max_post_collection": 750,
              "collect_count": 5,
              "avg_post_collection": 541,
              "avg_initialize": 986,
              "post_collection_count": 3,
              "build_leaf_collector": 86833,
              "min_collect": 6250,
              "min_build_aggregation": 3541,
              "initialize": 2786791,
              "max_build_leaf_collector_count": 1,
              "min_reduce": 0,
              "collect": 29834
            },
            "debug": {
              "total_buckets": 1
            }
          }
        ]
      }
    ]
  }
}
```
</details>

## 回應本文欄位

回應包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`profile` | 物件 | 包含剖析資訊。
`profile.shards` | 物件陣列 | 一個搜尋請求可以對索引中的一或多個分片執行，而一次搜尋可能涉及一或多個索引。因此，`profile.shards` 陣列包含搜尋所涉及之每個分片的剖析資訊。
`profile.shards.id` | 字串 | `[node-ID][index-name][shard-ID]` 格式的分片 ID。
`profile.shards.searches` | 物件陣列 | 一次搜尋代表對底層 Lucene 索引執行的一個查詢。大多數搜尋請求會對 Lucene 索引執行單一搜尋，但某些搜尋請求可以執行多個搜尋。例如，包含全域彙總會在全域情境中產生次要的 `match_all` 查詢。`profile.shards` 陣列包含每次搜尋執行的剖析資訊。
[`profile.shards.searches.query`](#the-query-array) | 物件陣列 | 關於查詢執行的剖析資訊。
`profile.shards.searches.rewrite_time` | 整數 | 所有 Lucene 查詢都會被改寫。查詢及其子查詢可能被改寫多次，直到查詢不再變化為止。改寫過程涉及執行最佳化，例如移除冗餘子句或以更有效率的路徑取代查詢路徑。改寫過程之後，原始查詢可能會有顯著變化。`rewrite_time` 欄位包含該查詢及其所有子查詢的累計改寫時間總和，單位為奈秒。
[`profile.shards.searches.collector`](#the-collector-array) | 物件陣列 | 關於執行搜尋之 Lucene 收集器的剖析資訊。
[`profile.shards.aggregations`](#aggregation-responses) | 物件陣列 | 關於彙總執行的剖析資訊。

### `query` 陣列

`query` 陣列包含具有下列欄位的物件。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 搜尋查詢被改寫成的 Lucene 查詢類型。對應至 Lucene 類別名稱（在 OpenSearch 中通常同名）。
`description` | 字串 | 包含查詢的 Lucene 說明。有助於區分類型相同的查詢。
`time_in_nanos`	| 長整數 | 此查詢的總經過時間，單位為奈秒。對於並行分段搜尋，`time_in_nanos` 是所有工作切片花費的總時間（最後完成之工作切片執行結束時間與第一個工作切片執行開始時間之間的差值）。
`max_slice_time_in_nanos`	| 長整數 | 任何工作切片執行查詢所花費的最長時間，單位為奈秒。僅在您啟用並行分段搜尋時才會包含此欄位。	
`min_slice_time_in_nanos`	| 長整數 | 任何工作切片執行查詢所花費的最短時間，單位為奈秒。僅在您啟用並行分段搜尋時才會包含此欄位。
`avg_slice_time_in_nanos`	| 長整數 | 任何工作切片執行查詢所花費的平均時間，單位為奈秒。僅在您啟用並行分段搜尋時才會包含此欄位。
[`breakdown`](#the-breakdown-object) | 物件 | 包含底層 Lucene 執行的計時統計資訊。
`children` | 物件陣列 | 如果查詢有子查詢（子項），此欄位包含子查詢的相關資訊。

### `breakdown` 物件

`breakdown` 物件代表底層 Lucene 執行的計時統計資訊，依方法細分。計時以實際經過的奈秒列出，且未經正規化。`breakdown` 計時包含所有子項的時間。`breakdown` 物件由下列欄位組成。所有欄位皆包含整數值。

欄位 | 說明
:--- | :--- 
`create_weight` | Lucene 中的 `Query` 物件是不可變的。然而，Lucene 應能將 `Query` 物件重複用於多個 `IndexSearcher` 物件。因此，`Query` 物件需要保留與執行查詢之索引相關的暫時狀態與統計資訊。為達成重複使用，每個 `Query` 物件都會產生一個 `Weight` 物件，該物件保留與 `<IndexSearcher, Query>` 元組相關的暫時情境（狀態）。`create_weight` 欄位包含建立 `Weight` 物件所花費的時間。
`build_scorer` | `Scorer` 會迭代比對的文件並為每份文件產生分數。`build_scorer` 欄位包含產生 `Scorer` 物件所花費的時間。這不包括為文件評分所花費的時間。`Scorer` 初始化時間取決於特定查詢的最佳化與複雜度。若查詢適用快取且已啟用快取，`build_scorer` 參數也包含與快取相關的時間。
`next_doc` | `next_doc` Lucene 方法會傳回下一個符合查詢之文件的文件 ID。此方法是 `advance` 方法的一種特殊類型，等同於 `advance(docId() + 1)`。`next_doc` 方法對許多 Lucene 查詢而言更為方便。`next_doc` 欄位包含判定下一個符合文件所需的時間，時間長短視查詢類型而定。  
`advance` | `advance` 方法是 Lucene 中 `next_doc` 方法的較低階版本。它同樣會找出下一個符合的文件，但需要呼叫的查詢執行額外工作，例如識別跳躍。某些查詢（例如布林查詢中的連詞（`must` 子句））無法使用 `next_doc`。對於這些查詢，會計時 `advance`。
`match` | 對於某些查詢，文件比對分兩步驟執行。首先，大致比對文件。其次，透過更全面的程序檢查大致比對到的文件。例如，片語查詢會先檢查文件是否包含片語中的所有詞彙，接著驗證這些詞彙是否依序排列（這是成本更高的程序）。`match` 欄位僅在使用兩步驟驗證程序的查詢中才為非零值。 
`score` | 包含 `Scorer` 為特定文件評分所花費的時間。
`shallow_advance` | 包含執行 `advanceShallow` Lucene 方法所需的時間。
`compute_max_score` | 包含執行 `getMaxScore` Lucene 方法所需的時間。
`set_min_competitive_score` | 包含執行 `setMinCompetitiveScore` Lucene 方法所需的時間。
`<method>_count` | 包含 `<method>` 的叫用次數。例如，`advance_count` 包含 `advance` 方法的叫用次數。同一方法會有不同的叫用，是因為該方法在不同的文件上被呼叫。您可以透過比較不同查詢元件中的計數來判斷查詢的選擇性。
`max_<method>`	| 任何工作切片執行查詢方法所花費的最長時間。`create_weight` 方法的細項統計不包含剖析的 `max` 時間，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。
`min_<method>`	| 任何工作切片執行查詢方法所花費的最短時間。`create_weight` 方法的細項統計不包含剖析的 `min` 時間，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。
`avg_<method>`	| 任何工作切片執行查詢方法所花費的平均時間。`create_weight` 方法的細項統計不包含剖析的 `avg` 時間，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。
`max_<method>_count`	| 任何工作切片上 `<method>` 的最大叫用次數。`create_weight` 方法的細項統計不包含剖析的 `max` 計數，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。
`min_<method>_count`	| 任何工作切片上 `<method>` 的最小叫用次數。`create_weight` 方法的細項統計不包含剖析的 `min` 計數，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。
`avg_<method>_count`	| 任何工作切片上 `<method>` 的平均叫用次數。`create_weight` 方法的細項統計不包含剖析的 `avg` 計數，因為該方法是在查詢層級而非工作切片層級執行。僅在您啟用並行分段搜尋時才會包含此欄位。

### `collector` 陣列

`collector` 陣列包含 Lucene 收集器的相關資訊。收集器負責協調文件遍歷與評分，並收集相符的文件。使用收集器時，個別查詢可以記錄彙總結果，並執行全域查詢或查詢後篩選器。

欄位 | 說明
:--- | :--- 
`name` | 收集器名稱。在[範例回應](#example-response-non-concurrent-search)中，`collector` 是單一 `SimpleTopScoreDocCollector`——預設的評分與排序收集器。
`reason` | 包含收集器的說明。如需可能的欄位值，請參閱[收集器原因](#collector-reasons)。
`time_in_nanos` | 此收集器的總經過時間，以奈秒為單位。若為並行分段搜尋，`time_in_nanos` 是所有工作切片的總時間（最後完成的工作切片執行結束時間與第一個工作切片執行開始時間之間的差異）。
`children` | 如果收集器有子收集器（子項），此欄位會包含子收集器的相關資訊。
`max_slice_time_in_nanos`	|任何工作切片所花費的最長時間，以奈秒為單位。	唯有啟用並行分段搜尋時，才會包含此欄位。
`min_slice_time_in_nanos`	|任何工作切片所花費的最短時間，以奈秒為單位。	唯有啟用並行分段搜尋時，才會包含此欄位。
`avg_slice_time_in_nanos`	|任何工作切片所花費的平均時間，以奈秒為單位。	唯有啟用並行分段搜尋時，才會包含此欄位。
`slice_count`	|此查詢的工作切片總數。唯有啟用並行分段搜尋時，才會包含此欄位。
`reduce_time_in_nanos`	|為所有工作切片收集器縮減結果所花費的時間，以奈秒為單位。	唯有啟用並行分段搜尋時，才會包含此欄位。

收集器時間會個別計算、合併及正規化，因此與查詢時間無關。
{: .note}

#### 收集器原因

下表說明所有可用的收集器原因。

原因 | 說明
:--- | :--- 
`search_sorted` | 為文件評分並排序的收集器。存在於大多數簡單搜尋中。
`search_count` | 計算相符文件數但不會擷取來源的收集器。指定 `size: 0` 時會出現。
`search_terminate_after_count` | 搜尋相符文件，並在找到指定數量的文件時終止搜尋的收集器。指定 `terminate_after_count` 查詢參數時會出現。
`search_min_score` | 傳回分數高於最低分數之相符文件的收集器。指定 `min_score` 參數時會出現。
`search_multi` | 其他收集器的包裝收集器。當搜尋、彙總、全域彙總及查詢後篩選器合併在單一搜尋中時會出現。
`search_timeout` | 在指定時間過後停止執行的收集器。指定 `timeout` 參數時會出現。
`aggregation` | 針對指定查詢範圍執行之彙總的收集器。OpenSearch 使用單一 `aggregation` 收集器來收集所有彙總的文件。
`global_aggregation` | 針對全域查詢範圍執行的收集器。全域範圍與指定的查詢範圍不同，因此為了收集整個資料集，必須執行 `match_all` 查詢。

### 彙總回應

下列範例顯示不同彙總類型的效能分析回應。

#### 回應：全域彙總

回應包含剖析資訊：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1370,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "all_products": {
      "doc_count": 4675,
      "avg_price": {
        "value": 75.05542864304813
      }
    },
    "elitelligence_products": {
      "value": 68.4430200729927
    }
  },
  "profile": {
    "shards": [
      {
        "id": "[LidyZ1HVS-u93-73Z49dQg][opensearch_dashboards_sample_data_ecommerce][0]",
        "inbound_network_time_in_millis": 0,
        "outbound_network_time_in_millis": 0,
        "searches": [
          {
            "query": [
              {
                "type": "ConstantScoreQuery",
                "description": "ConstantScore(manufacturer:elitelligence)",
                "time_in_nanos": 1367487,
                "breakdown": {
                  "set_min_competitive_score_count": 0,
                  "match_count": 0,
                  "shallow_advance_count": 0,
                  "set_min_competitive_score": 0,
                  "next_doc": 634321,
                  "match": 0,
                  "next_doc_count": 1370,
                  "score_count": 0,
                  "compute_max_score_count": 0,
                  "compute_max_score": 0,
                  "advance": 173250,
                  "advance_count": 2,
                  "score": 0,
                  "build_scorer_count": 4,
                  "create_weight": 132458,
                  "shallow_advance": 0,
                  "create_weight_count": 1,
                  "build_scorer": 427458
                },
                "children": [
                  {
                    "type": "TermQuery",
                    "description": "manufacturer:elitelligence",
                    "time_in_nanos": 1174794,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 470918,
                      "match": 0,
                      "next_doc_count": 1370,
                      "score_count": 0,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 172084,
                      "advance_count": 2,
                      "score": 0,
                      "build_scorer_count": 4,
                      "create_weight": 114041,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 417751
                    }
                  }
                ]
              }
            ],
            "rewrite_time": 42542,
            "collector": [
              {
                "name": "MultiCollector",
                "reason": "search_multi",
                "time_in_nanos": 778406,
                "children": [
                  {
                    "name": "EarlyTerminatingCollector",
                    "reason": "search_count",
                    "time_in_nanos": 70290
                  },
                  {
                    "name": "ProfilingAggregator: [elitelligence_products]",
                    "reason": "aggregation",
                    "time_in_nanos": 502780
                  }
                ]
              }
            ]
          },
          {
            "query": [
              {
                "type": "ConstantScoreQuery",
                "description": "ConstantScore(*:*)",
                "time_in_nanos": 995345,
                "breakdown": {
                  "set_min_competitive_score_count": 0,
                  "match_count": 0,
                  "shallow_advance_count": 0,
                  "set_min_competitive_score": 0,
                  "next_doc": 930803,
                  "match": 0,
                  "next_doc_count": 4675,
                  "score_count": 0,
                  "compute_max_score_count": 0,
                  "compute_max_score": 0,
                  "advance": 2209,
                  "advance_count": 2,
                  "score": 0,
                  "build_scorer_count": 4,
                  "create_weight": 23875,
                  "shallow_advance": 0,
                  "create_weight_count": 1,
                  "build_scorer": 38458
                },
                "children": [
                  {
                    "type": "MatchAllDocsQuery",
                    "description": "*:*",
                    "time_in_nanos": 431375,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 389875,
                      "match": 0,
                      "next_doc_count": 4675,
                      "score_count": 0,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 1167,
                      "advance_count": 2,
                      "score": 0,
                      "build_scorer_count": 4,
                      "create_weight": 9458,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 30875
                    }
                  }
                ]
              }
            ],
            "rewrite_time": 8792,
            "collector": [
              {
                "name": "ProfilingAggregator: [all_products]",
                "reason": "aggregation_global",
                "time_in_nanos": 1310536
              }
            ]
          }
        ],
        "aggregations": [
          {
            "type": "AvgAggregator",
            "description": "elitelligence_products",
            "time_in_nanos": 319918,
            "breakdown": {
              "reduce": 0,
              "post_collection_count": 1,
              "build_leaf_collector": 130709,
              "build_aggregation": 2709,
              "build_aggregation_count": 1,
              "build_leaf_collector_count": 2,
              "post_collection": 584,
              "initialize": 4750,
              "initialize_count": 1,
              "reduce_count": 0,
              "collect": 181166,
              "collect_count": 1370
            }
          },
          {
            "type": "GlobalAggregator",
            "description": "all_products",
            "time_in_nanos": 1519340,
            "breakdown": {
              "reduce": 0,
              "post_collection_count": 1,
              "build_leaf_collector": 134625,
              "build_aggregation": 59291,
              "build_aggregation_count": 1,
              "build_leaf_collector_count": 2,
              "post_collection": 5041,
              "initialize": 24500,
              "initialize_count": 1,
              "reduce_count": 0,
              "collect": 1295883,
              "collect_count": 4675
            },
            "children": [
              {
                "type": "AvgAggregator",
                "description": "avg_price",
                "time_in_nanos": 775967,
                "breakdown": {
                  "reduce": 0,
                  "post_collection_count": 1,
                  "build_leaf_collector": 98999,
                  "build_aggregation": 33083,
                  "build_aggregation_count": 1,
                  "build_leaf_collector_count": 2,
                  "post_collection": 2209,
                  "initialize": 1708,
                  "initialize_count": 1,
                  "reduce_count": 0,
                  "collect": 639968,
                  "collect_count": 4675
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```
</details>

#### 回應：非全域彙總

回應包含剖析資訊：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 13,
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
    "avg_taxful_total_price": {
      "value": 75.05542864304813
    }
  },
  "profile": {
    "shards": [
      {
        "id": "[LidyZ1HVS-u93-73Z49dQg][opensearch_dashboards_sample_data_ecommerce][0]",
        "inbound_network_time_in_millis": 0,
        "outbound_network_time_in_millis": 0,
        "searches": [
          {
            "query": [
              {
                "type": "ConstantScoreQuery",
                "description": "ConstantScore(*:*)",
                "time_in_nanos": 1690820,
                "breakdown": {
                  "set_min_competitive_score_count": 0,
                  "match_count": 0,
                  "shallow_advance_count": 0,
                  "set_min_competitive_score": 0,
                  "next_doc": 1614112,
                  "match": 0,
                  "next_doc_count": 4675,
                  "score_count": 0,
                  "compute_max_score_count": 0,
                  "compute_max_score": 0,
                  "advance": 2708,
                  "advance_count": 2,
                  "score": 0,
                  "build_scorer_count": 4,
                  "create_weight": 20250,
                  "shallow_advance": 0,
                  "create_weight_count": 1,
                  "build_scorer": 53750
                },
                "children": [
                  {
                    "type": "MatchAllDocsQuery",
                    "description": "*:*",
                    "time_in_nanos": 770902,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 721943,
                      "match": 0,
                      "next_doc_count": 4675,
                      "score_count": 0,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 1042,
                      "advance_count": 2,
                      "score": 0,
                      "build_scorer_count": 4,
                      "create_weight": 5041,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 42876
                    }
                  }
                ]
              }
            ],
            "rewrite_time": 22000,
            "collector": [
              {
                "name": "MultiCollector",
                "reason": "search_multi",
                "time_in_nanos": 3672676,
                "children": [
                  {
                    "name": "EarlyTerminatingCollector",
                    "reason": "search_count",
                    "time_in_nanos": 78626
                  },
                  {
                    "name": "ProfilingAggregator: [avg_taxful_total_price]",
                    "reason": "aggregation",
                    "time_in_nanos": 2834566
                  }
                ]
              }
            ]
          }
        ],
        "aggregations": [
          {
            "type": "AvgAggregator",
            "description": "avg_taxful_total_price",
            "time_in_nanos": 1973702,
            "breakdown": {
              "reduce": 0,
              "post_collection_count": 1,
              "build_leaf_collector": 199292,
              "build_aggregation": 13584,
              "build_aggregation_count": 1,
              "build_leaf_collector_count": 2,
              "post_collection": 6125,
              "initialize": 6916,
              "initialize_count": 1,
              "reduce_count": 0,
              "collect": 1747785,
              "collect_count": 4675
            }
          }
        ]
      }
    ]
  }
}
```
</details>

#### 回應本文欄位

`aggregations` 陣列包含具有下列欄位的彙總物件。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 彙總器類型。在[非全域彙總範例回應](#response-non-global-aggregation)中，彙總器類型為 `AvgAggregator`。[全域彙總範例回應](#response-global-aggregation)包含一個 `GlobalAggregator`，其下有一個 `AvgAggregator` 子項目。
`description` | 字串 | 包含彙總的 Lucene 說明。有助於區分相同類型的彙總。
`time_in_nanos` | 長整數 | 此彙總經過的總時間，以奈秒為單位。對於並行分段搜尋，`time_in_nanos` 是所有工作切片的總時間（最後一個完成的工作切片執行結束時間與第一個工作切片執行開始時間之間的差值）。	
[`breakdown`](#the-breakdown-object-1) | 物件 | 包含低階 Lucene 執行的計時統計資料。
`children` | 物件陣列 | 如果彙總具有子彙總（子項目），此欄位會包含子彙總的相關資訊。
`debug` | 物件 | 部分彙總會傳回描述底層執行詳細資訊的 `debug` 物件。
`max_slice_time_in_nanos`	|長整數 | 任一工作切片執行彙總所花費的最長時間，以奈秒為單位。只有在您啟用並行分段搜尋時，才會包含此欄位。
`min_slice_time_in_nanos`	|長整數 |任一工作切片執行彙總所花費的最短時間，以奈秒為單位。只有在您啟用並行分段搜尋時，才會包含此欄位。
`avg_slice_time_in_nanos`	|長整數 |任一工作切片執行彙總所花費的平均時間，以奈秒為單位。只有在您啟用並行分段搜尋時，才會包含此欄位。

#### `breakdown` 物件

`breakdown` 物件代表低階 Lucene 執行的計時統計資料，並依方法細分。`breakdown` 物件中的每個欄位都代表在彙總中執行的一個 Lucene 內部方法。計時以實際經過的奈秒數列出，且未經正規化。`breakdown` 計時包含所有子項目的時間。`breakdown` 物件由下列欄位組成。所有欄位皆包含整數值。

欄位 | 說明
:--- | :--- 
`initialize` | 包含在建立 `AggregationCollectorManager` 期間執行 `preCollection()` 回呼方法所花費的時間。對於並行分段搜尋，`initialize` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`build_leaf_collector`| 包含執行彙總的 `getLeafCollector()` 方法所花費的時間，此方法會建立新的收集器，以收集指定上下文中的文件。對於並行分段搜尋，`build_leaf_collector` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`collect`| 包含將文件收集到桶 (bucket) 中所花費的時間。對於並行分段搜尋，`collect` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`post_collection`| 包含執行彙總的 `postCollection()` 回呼方法所花費的時間。對於並行分段搜尋，`post_collection` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`build_aggregation`| 包含執行彙總的 `buildAggregations()` 方法所花費的時間，此方法會建置此彙總的結果。對於並行分段搜尋，`build_aggregation` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`reduce`| 包含在 `reduce` 階段所花費的時間。對於並行分段搜尋，`reduce` 方法包含所有切片的總經過時間 (最後一個完成的切片執行結束時間與第一個切片執行開始時間之間的差值)。
`<method>_count` | 包含 `<method>` 的呼叫次數。例如，`build_leaf_collector_count` 包含 `build_leaf_collector` 方法的呼叫次數。 
`max_<method>`	|任一切片執行彙總方法所花費的最長時間。只有在您啟用並行分段搜尋時，才會包含此欄位。
`min_<method>`|任一切片執行彙總方法所花費的最短時間。只有在您啟用並行分段搜尋時，才會包含此欄位。
`avg_<method>`	|任一切片執行彙總方法所花費的平均時間。只有在您啟用並行分段搜尋時，才會包含此欄位。
`<method>_count`	|所有切片的方法總計數。例如，對於 `collect` 方法，此值是在所有切片中將文件收集到桶中所需的此方法總呼叫次數。 
`max_<method>_count`	|任一切片上 `<method>` 的最大呼叫次數。只有在您啟用並行分段搜尋時，才會包含此欄位。
`min_<method>_count`	|任一切片上 `<method>` 的最小呼叫次數。只有在您啟用並行分段搜尋時，才會包含此欄位。
`avg_<method>_count`	|任一切片上 `<method>` 的平均呼叫次數。只有在您啟用並行分段搜尋時，才會包含此欄位。
