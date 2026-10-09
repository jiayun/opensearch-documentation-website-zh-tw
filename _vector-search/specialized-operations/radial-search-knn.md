---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "徑向搜尋"
nav_order: 50
parent: Specialized vector search
has_children: false
has_math: true
redirect_from:
  - /search-plugins/knn/radial-search-knn/
---

# 徑向搜尋

徑向搜尋強化了向量搜尋能力，超越近似 top-k 搜尋。透過徑向搜尋，您可以搜尋向量空間中所有與查詢點距離在指定最大距離內，或分數達到指定最低分數門檻的點。這為搜尋作業提供了更高的彈性與實用性。

您可以使用 Lucene 或 Faiss 引擎執行徑向搜尋。兩種引擎都支援巢狀欄位的徑向搜尋。

## 參數

徑向搜尋支援下列參數：

- `max_distance`：指定向量空間中的實際距離，找出所有與查詢點距離在此範圍內的點。此方法特別適用於需要空間鄰近性或絕對距離測量的應用。

`min_score`：指定相似度分數，便於擷取與查詢點相比達到或超過此分數的點。當相對於特定指標的相似性比實際鄰近性更為關鍵時，此方法最為理想。

在徑向搜尋期間，只需要指定一個查詢變數，即 `k`、`max_distance` 或 `min_score`。

## 空間

如需支援的空間，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

## 範例

下列範例可協助您開始使用徑向搜尋。

### 先決條件

若要將向量索引與徑向搜尋搭配使用，請將 `index.knn` 設定為 `true` 來建立向量索引。指定一或多個 `knn_vector` 資料類型的欄位，如下列範例所示：

```json
PUT knn-index-test
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 2,
        "space_type": "l2",
        "method": {
            "name": "hnsw",
            "engine": "faiss",
            "parameters": {
              "ef_construction": 100,
              "m": 16,
              "ef_search": 100
            }
          }
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引之後，新增一些類似下列內容的資料：

```json
PUT _bulk?refresh=true
{"index": {"_index": "knn-index-test", "_id": "1"}}
{"my_vector": [7.0, 8.2], "price": 4.4}
{"index": {"_index": "knn-index-test", "_id": "2"}}
{"my_vector": [7.1, 7.4], "price": 14.2}
{"index": {"_index": "knn-index-test", "_id": "3"}}
{"my_vector": [7.3, 8.3], "price": 19.1}
{"index": {"_index": "knn-index-test", "_id": "4"}}
{"my_vector": [6.5, 8.8], "price": 1.2}
{"index": {"_index": "knn-index-test", "_id": "5"}}
{"my_vector": [5.7, 7.9], "price": 16.5}

```
{% include copy-curl.html %}

### 範例：使用 `max_distance` 的徑向搜尋

下列範例顯示使用 `max_distance` 執行的徑向搜尋：

```json
GET knn-index-test/_search
{
    "query": {
        "knn": {
            "my_vector": {
                "vector": [
                    7.1,
                    8.3
                ],
                "max_distance": 2
            }
        }
    }
}
```
{% include copy-curl.html %}

所有落在歐幾里得距離平方（`l2^2`）為 2 以內的文件都會被傳回，如下列回應所示：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
    "took": 6,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 4,
            "relation": "eq"
        },
        "max_score": 0.98039204,
        "hits": [
            {
                "_index": "knn-index-test",
                "_id": "1",
                "_score": 0.98039204,
                "_source": {
                    "my_vector": [
                        7.0,
                        8.2
                    ],
                    "price": 4.4
                }
            },
            {
                "_index": "knn-index-test",
                "_id": "3",
                "_score": 0.9615384,
                "_source": {
                    "my_vector": [
                        7.3,
                        8.3
                    ],
                    "price": 19.1
                }
            },
            {
                "_index": "knn-index-test",
                "_id": "4",
                "_score": 0.62111807,
                "_source": {
                    "my_vector": [
                        6.5,
                        8.8
                    ],
                    "price": 1.2
                }
            },
            {
                "_index": "knn-index-test",
                "_id": "2",
                "_score": 0.5524861,
                "_source": {
                    "my_vector": [
                        7.1,
                        7.4
                    ],
                    "price": 14.2
                }
            }
        ]
    }
}
```
</details>

### 範例：使用 `max_distance` 與篩選條件的徑向搜尋

下列範例顯示使用 `max_distance` 與回應篩選條件執行的徑向搜尋：

```json
GET knn-index-test/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [7.1, 8.3],
        "max_distance": 2,
        "filter": {
          "range": {
            "price": {
              "gte": 1,
              "lte": 5
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

所有落在歐幾里得距離平方（`l2^2`）為 2 以內，且價格介於 1 到 5 範圍內的文件都會被傳回，如下列回應所示：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
    "took": 4,
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
        "max_score": 0.98039204,
        "hits": [
            {
                "_index": "knn-index-test",
                "_id": "1",
                "_score": 0.98039204,
                "_source": {
                    "my_vector": [
                        7.0,
                        8.2
                    ],
                    "price": 4.4
                }
            },
            {
                "_index": "knn-index-test",
                "_id": "4",
                "_score": 0.62111807,
                "_source": {
                    "my_vector": [
                        6.5,
                        8.8
                    ],
                    "price": 1.2
                }
            }
        ]
    }
}
```
</details>

### 範例：使用 `min_score` 的徑向搜尋

下列範例顯示使用 `min_score` 執行的徑向搜尋：

```json
GET knn-index-test/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [7.1, 8.3],
        "min_score": 0.95
      }
    }
  }
}
```
{% include copy-curl.html %}

所有分數為 0.9 或更高的文件都會被傳回，如下列回應所示：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
    "took": 3,
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
        "max_score": 0.98039204,
        "hits": [
            {
                "_index": "knn-index-test",
                "_id": "1",
                "_score": 0.98039204,
                "_source": {
                    "my_vector": [
                        7.0,
                        8.2
                    ],
                    "price": 4.4
                }
            },
            {
                "_index": "knn-index-test",
                "_id": "3",
                "_score": 0.9615384,
                "_source": {
                    "my_vector": [
                        7.3,
                        8.3
                    ],
                    "price": 19.1
                }
            }
        ]
    }
}
```
</details>

### 範例：使用 `min_score` 和篩選器進行徑向搜尋

下列範例示範使用 `min_score` 和回應篩選器執行徑向搜尋：

```json
GET knn-index-test/_search
{
    "query": {
        "knn": {
            "my_vector": {
                "vector": [
                    7.1,
                    8.3
                ],
                "min_score": 0.95,
                "filter": {
                    "range": {
                        "price": {
                            "gte": 1,
                            "lte": 5
                        }
                    }
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

系統會傳回分數大於或等於 0.9，且價格介於 1 到 5 之間的所有文件，如下列範例所示：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
    "took": 4,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.98039204,
        "hits": [
            {
                "_index": "knn-index-test",
                "_id": "1",
                "_score": 0.98039204,
                "_source": {
                    "my_vector": [
                        7.0,
                        8.2
                    ],
                    "price": 4.4
                }
            }
        ]
    }
}
```
</details>

### 範例：對巢狀欄位進行徑向搜尋

下列範例示範如何對巢狀向量欄位執行徑向搜尋。首先，建立包含巢狀 `knn_vector` 欄位的索引：

```json
PUT nested-knn-index
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "my_embeddings": {
        "type": "nested",
        "properties": {
          "embedding": {
            "type": "knn_vector",
            "dimension": 3,
            "method": {
              "engine": "faiss",
              "space_type": "innerproduct",
              "name": "hnsw",
              "parameters": {
                "ef_construction": 100,
                "m": 16
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例資料新增至索引：

```json
PUT _bulk?refresh=true
{"index": {"_index": "nested-knn-index", "_id": "1"}}
{"my_embeddings": [{"embedding": [0.1, 0.2, 0.3]}]}
{"index": {"_index": "nested-knn-index", "_id": "2"}}
{"my_embeddings": [{"embedding": [0.4, 0.5, 0.6]}]}
{"index": {"_index": "nested-knn-index", "_id": "3"}}
{"my_embeddings": [{"embedding": [0.7, 0.8, 0.9]}]}
```
{% include copy-curl.html %}

對 `my_embeddings.embedding` 巢狀欄位執行徑向搜尋，找出與查詢向量相似且相似度分數至少為 0.7 的所有嵌入：

```json
GET nested-knn-index/_search
{
  "query": {
    "nested": {
      "path": "my_embeddings",
      "query": {
        "knn": {
          "my_embeddings.embedding": {
            "vector": [0.2, 0.3, 0.4],
            "min_score": 0.7
          }
        }
      },
      "score_mode": "max"
    }
  }
}
```
{% include copy-curl.html %}

此查詢可搭配 Lucene 和 Faiss 引擎使用，並傳回巢狀向量嵌入達到最低相似度分數門檻的文件，如下列回應所示：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
  "took": 43,
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
    "max_score": 1.74,
    "hits": [
      {
        "_index": "nested-knn-index",
        "_id": "3",
        "_score": 1.74,
        "_source": {
          "my_embeddings": [
            {
              "embedding": [0.7, 0.8, 0.9]
            }
          ]
        }
      },
      {
        "_index": "nested-knn-index",
        "_id": "2",
        "_score": 1.47,
        "_source": {
          "my_embeddings": [
            {
              "embedding": [0.4, 0.5, 0.6]
            }
          ]
        }
      }
    ]
  }
}
```
</details>
