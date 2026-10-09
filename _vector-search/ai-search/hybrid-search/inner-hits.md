---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在混合查詢中使用內部命中"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 60
---

# 在混合查詢中使用內部命中
**於 3.0 版導入**
{: .label .label-purple }

執行混合搜尋時，您可以在搜尋請求中加入 `inner_hits` 子句，以擷取相符的巢狀物件或子文件。這項資訊可讓您探索文件中與查詢相符的特定部分。

若要進一步了解 `inner_hits` 的運作方式，請參閱[擷取內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。


混合查詢執行時，文件的評分與擷取方式如下：

1. 每個子查詢會根據內部命中的相關性選取父文件。
1. 來自所有子查詢的已選取父文件會被合併，其分數會經過標準化以產生混合分數。
1. 針對每個父文件，相關的 `inner_hits` 會從分片中擷取，並包含在最終回應中。

混合查詢在決定最終搜尋結果時，處理內部命中的方式與傳統查詢不同：

- 在**傳統查詢**中，父文件的最終排名直接由 `inner_hits` 分數決定。
- 在**混合查詢**中，最終排名由**混合分數**（所有子查詢分數經標準化後的組合）決定。不過，父文件仍會根據其 `inner_hits` 的相關性從分片中擷取。

回應中的 `inner_hits` 區段會顯示標準化之前的原始分數。父文件則顯示最終的混合分數。
{: .note}

## 範例

下列範例示範如何在混合查詢中使用 `inner_hits`。

### 步驟 1：建立索引

建立一個包含兩個巢狀欄位（`user` 與 `location`）的索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "user": {
        "type": "nested",
        "properties": {
          "name": {
            "type": "text"
          },
          "age": {
            "type": "integer"
          }
        }
      },
      "location": {
        "type": "nested",
        "properties": {
          "city": {
            "type": "text"
          },
          "state": {
            "type": "text"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：建立搜尋管線

使用 `min_max` 標準化技術與 `arithmetic_mean` 組合技術，設定一個包含 `normalization-processor` 的搜尋管線：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {}
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：將文件匯入索引

若要將文件匯入上一個步驟建立的索引，請傳送下列請求：

```json
POST /my-nlp-index/_bulk
{"index": {"_index": "my-nlp-index"}}
{"user":[{"name":"John Alder","age":35},{"name":"Sammy","age":34},{"name":"Mike","age":32},{"name":"Maples","age":30}],"location":[{"city":"Amsterdam","state":"Netherlands"},{"city":"Udaipur","state":"Rajasthan"},{"city":"Naples","state":"Italy"}]}
{"index": {"_index": "my-nlp-index"}}
{"user":[{"name":"John Wick","age":46},{"name":"John Snow","age":40},{"name":"Sansa Stark","age":22},{"name":"Arya Stark","age":20}],"location":[{"city":"Tromso","state":"Norway"},{"city":"Los Angeles","state":"California"},{"city":"London","state":"UK"}]}
```
{% include copy-curl.html %}

### 步驟 4：使用混合搜尋搜尋索引並擷取內部命中

下列請求會執行混合查詢，在兩個巢狀欄位 `user` 與 `location` 中搜尋相符項目。它會將每個欄位的結果合併為單一排名的父文件清單，同時使用 `inner_hits` 擷取相符的巢狀物件：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "nested": {
            "path": "user",
            "query": {
              "match": {
                "user.name": "John"
              }
            },
            "score_mode": "sum",
            "inner_hits": {}
          }
        },
        {
          "nested": {
            "path": "location",
            "query": {
              "match": {
                "location.city": "Udaipur"
              }
            },
            "inner_hits": {}
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的父文件，以及 `user` 與 `location` 兩個巢狀欄位的相關巢狀 `inner_hits`。每個內部命中會顯示哪個巢狀物件相符，以及它對整體混合分數的貢獻程度：

```json
...
{
  "hits": [
    {
      "_index": "my-nlp-index",
      "_id": "1",
      "_score": 1.0,
      "inner_hits": {
        "location": {
          "hits": {
            "max_score": 0.44583148,
            "hits": [
              {
                "_nested": {
                  "field": "location",
                  "offset": 1
                },
                "_score": 0.44583148,
                "_source": {
                  "city": "Udaipur",
                  "state": "Rajasthan"
                }
              }
            ]
          }
        },
        "user": {
          "hits": {
            "max_score": 0.4394061,
            "hits": [
              {
                "_nested": {
                  "field": "user",
                  "offset": 0
                },
                "_score": 0.4394061,
                "_source": {
                  "name": "John Alder",
                  "age": 35
                }
              }
            ]
          }
        }
      }
      // Additional details omitted for brevity
    },
    {
      "_index": "my-nlp-index",
      "_id": "2",
      "_score": 5.0E-4,
      "inner_hits": {
        "user": {
          "hits": {
            "max_score": 0.31506687,
            "hits": [
              {
                "_nested": {
                  "field": "user",
                  "offset": 0
                },
                "_score": 0.31506687,
                "_source": {
                  "name": "John Wick",
                  "age": 46
                }
              },
              {
                "_nested": {
                  "field": "user",
                  "offset": 1
                },
                "_score": 0.31506687,
                "_source": {
                  "name": "John Snow",
                  "age": 40
                }
              }
            ]
          }
        }
        // Additional details omitted for brevity
      }
    }
  ]
  // Additional details omitted for brevity
}
...
```

## 使用 explain 參數

若要了解內部命中如何影響混合分數，您可以啟用說明功能。回應將包含詳細的評分資訊。如需在混合查詢中使用 `explain` 的更多資訊，請參閱[混合搜尋說明]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/explain/)。

`explain` 在資源與時間方面都是昂貴的操作。對於正式環境叢集，我們建議僅在疑難排解時少量使用。
{: .warning}

首先，將 `hybrid_score_explanation` 處理器加入您在步驟 2 建立的搜尋管線：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean"
        }
      }
    }
  ],
  "response_processors": [
    {
      "hybrid_score_explanation": {}
    }
  ]
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[混合分數說明處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/explanation-processor/)與[混合搜尋說明]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/explain/)。

接著，執行您在步驟 4 執行過的相同查詢，並在搜尋請求中加入 `explain` 參數：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline&explain=true
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "nested": {
            "path": "user",
            "query": {
              "match": {
                "user.name": "John"
              }
            },
            "score_mode": "sum",
            "inner_hits": {}
          }
        },
        {
          "nested": {
            "path": "location",
            "query": {
              "match": {
                "location.city": "Udaipur"
              }
            },
            "inner_hits": {}
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含一個 `_explanation` 物件，其中含有詳細的評分資訊。巢狀的 `details` 陣列提供下列相關資訊：所使用的分數模式、對父文件分數有貢獻的子文件數量，以及分數如何被標準化與組合：

```json
{
  ...
  "_explanation": {
    "value": 1.0,
    "description": "arithmetic_mean combination of:",
    "details": [
      {
        "value": 1.0,
        "description": "min_max normalization of:",
        "details": [
          {
            "value": 0.4458314776420593,
            "description": "combined score of:",
            "details": [
              {
                "value": 0.4394061,
                "description": "Score based on 1 child docs in range from 0 to 6, using score mode Avg",
                "details": [
                  {
                    "value": 0.4394061,
                    "description": "weight(user.name:john in 0) [PerFieldSimilarity], result of:"
                    // Additional details omitted for brevity
                  }
                ]
              },
              {
                "value": 0.44583148,
                "description": "Score based on 1 child docs in range from 0 to 6, using score mode Avg",
                "details": [
                  {
                    "value": 0.44583148,
                    "description": "weight(location.city:udaipur in 5) [PerFieldSimilarity], result of:"
                    // Additional details omitted for brevity
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
...
```

## 使用內部命中進行排序

若要套用排序，請在 `inner_hits` 子句中新增 `sort` 子句。例如，若要依 `user.age` 排序，請在 `inner_hits` 子句中指定此排序條件：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "nested": {
            "path": "user",
            "query": {
              "match": {
                "user.name": "John"
              }
            },
            "score_mode": "sum",
            "inner_hits": {
              "sort": [
                {
                  "user.age": {
                    "order": "desc"
                  }
                }
              ]
            }
          }
        },
        {
          "nested": {
            "path": "location",
            "query": {
              "match": {
                "location.city": "Udaipur"
              }
            },
            "inner_hits": {}
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

在回應中，`user` 內部命中會依 age 遞減排序，而非依相關性排序，這就是為什麼 `_score` 欄位為 `null`（套用自訂排序時不會計算分數）：

```json
...
"user": {
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_nested": {
          "field": "user",
          "offset": 0
        },
        "_score": null,
        "_source": {
          "name": "John Wick",
          "age": 46
        },
        "sort": [
          46
        ]
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_nested": {
          "field": "user",
          "offset": 1
        },
        "_score": null,
        "_source": {
          "name": "John Snow",
          "age": 40
        },
        "sort": [
          40
        ]
      }
    ]
  }
}
...
```

## 使用內部命中進行分頁

若要對內部命中結果進行分頁，請在 `inner_hits` 子句中指定 `from` 參數（起始位置）與 `size` 參數（結果數量）。下列範例請求僅從 `user` 欄位擷取第三個與第四個巢狀物件，其方式是將 `from` 設為 `2`（略過前兩個），並將 `size` 設為 `2`（傳回兩個結果）：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "nested": {
            "path": "user",
            "query": {
              "match_all": {}
            },
            "inner_hits": {
              "from": 2,
              "size": 2
            }
          }
        },
        {
          "nested": {
            "path": "location",
            "query": {
              "match": {
                "location.city": "Udaipur"
              }
            },
            "inner_hits": {}
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含從位移 `2` 開始的 `user` 欄位內部命中：

```json
...
"user": {
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_nested": {
          "field": "user",
          "offset": 2
        },
        "_score": 1.0,
        "_source": {
          "name": "Mike",
          "age": 32
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_nested": {
          "field": "user",
          "offset": 3
        },
        "_score": 1.0,
        "_source": {
          "name": "Maples",
          "age": 30
        }
      }
    ]
  }
}
...
```

## 為 inner_hits 欄位定義自訂名稱

若要區分單一查詢中的多個內部命中，您可以為搜尋回應中的內部命中定義自訂名稱。例如，您可以為 `location` 欄位的內部命中提供自訂名稱 `coordinates`，如下所示：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "nested": {
            "path": "user",
            "query": {
              "match_all": {}
            },
            "inner_hits": {
              "name": "coordinates"
            }
          }
        },
        {
          "nested": {
            "path": "location",
            "query": {
              "match": {
                "location.city": "Udaipur"
              }
            },
            "inner_hits": {}
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

在回應中，`user` 欄位的內部命中會以自訂名稱 `coordinates` 顯示：

```json
...
"inner_hits": {
  "coordinates": {
    "hits": {
      "total": {
        "value": 4,
        "relation": "eq"
      },
      "max_score": 1.0,
      "hits": [
        {
          "_index": "my-nlp-index",
          "_id": "1",
          "_nested": {
            "field": "user",
            "offset": 0
          },
          "_score": 1.0,
          "_source": {
            "name": "John Alder",
            "age": 35
          }
        }
      ]
    }
  },
  "location": {
    "hits": {
      "total": {
        "value": 1,
        "relation": "eq"
      },
      "max_score": 0.44583148,
      "hits": [
        {
          "_index": "my-nlp-index",
          "_id": "1",
          "_nested": {
            "field": "location",
            "offset": 1
          },
          "_score": 0.44583148,
          "_source": {
            "city": "Udaipur",
            "state": "Rajasthan"
          }
        }
      ]
    }
  }
}
...
```
