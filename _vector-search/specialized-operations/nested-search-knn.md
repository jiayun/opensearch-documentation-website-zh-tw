---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巢狀欄位搜尋"
nav_order: 40
parent: Specialized vector search
has_children: false
has_math: true
redirect_from:
  - /search-plugins/knn/nested-search-knn/ 
---

# 巢狀欄位搜尋

在向量索引中使用[巢狀欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)，您可以將多個向量儲存在單一文件中。例如，如果您的文件由多個元件組成，您可以為每個元件產生向量值，並將每個向量儲存在巢狀欄位中。

向量搜尋是在欄位層級運作。對於包含巢狀欄位的文件，OpenSearch 只會檢查最接近查詢向量的向量，以決定是否將該文件納入結果中。例如，考慮一個包含文件 `A` 和 `B` 的索引。文件 `A` 由向量 `A1` 和 `A2` 表示，文件 `B` 由向量 `B1` 表示。此外，查詢 Q 的相似度順序為 `A1`、`A2`、`B1`。如果您使用 k 值為 2 的查詢 Q 進行搜尋，搜尋將會同時傳回文件 `A` 和 `B`，而不只是文件 `A`。

請注意，在近似搜尋的情況下，結果是近似值，並非完全相符。

Lucene 和 Faiss 引擎的 HNSW 演算法支援搭配巢狀欄位的向量搜尋。


## 巢狀欄位的索引編製與搜尋

若要搭配巢狀欄位使用向量搜尋，您必須將 `index.knn` 設定為 `true` 來建立向量索引。將巢狀欄位的 `type` 設定為 `nested` 來建立巢狀欄位，並在該巢狀欄位內指定一或多個 `knn_vector` 資料類型的欄位。在此範例中，`knn_vector` 欄位 `my_vector` 巢狀於 `nested_field` 欄位內：

```json
PUT my-knn-index-1
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "nested_field": {
        "type": "nested",
        "properties": {
          "my_vector": {
            "type": "knn_vector",
            "dimension": 3,
            "space_type": "l2",
            "method": {
              "name": "hnsw",
              "engine": "lucene",
              "parameters": {
                "ef_construction": 100,
                "m": 16
              }
            }
          },
          "color": {
            "type": "text",
            "index": false
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引後，請新增一些資料：

```json
PUT _bulk?refresh=true
{ "index": { "_index": "my-knn-index-1", "_id": "1" } }
{"nested_field":[{"my_vector":[1,1,1], "color": "blue"},{"my_vector":[2,2,2], "color": "yellow"},{"my_vector":[3,3,3], "color": "white"}]}
{ "index": { "_index": "my-knn-index-1", "_id": "2" } }
{"nested_field":[{"my_vector":[10,10,10], "color": "red"},{"my_vector":[20,20,20], "color": "green"},{"my_vector":[30,30,30], "color": "black"}]}
```
{% include copy-curl.html %}

然後使用 `knn` 查詢類型對資料執行向量搜尋：

```json
GET my-knn-index-1/_search
{
  "query": {
    "nested": {
      "path": "nested_field",
      "query": {
        "knn": {
          "nested_field.my_vector": {
            "vector": [1,1,1],
            "k": 2
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

即使最接近查詢向量的三個向量都在文件 1 中，由於 k 設定為 2，查詢仍會傳回文件 1 和 2：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my-knn-index-1",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "nested_field": [
            {
              "my_vector": [
                1,
                1,
                1
              ],
              "color": "blue"
            },
            {
              "my_vector": [
                2,
                2,
                2
              ],
              "color": "yellow"
            },
            {
              "my_vector": [
                3,
                3,
                3
              ],
              "color": "white"
            }
          ]
        }
      },
      {
        "_index": "my-knn-index-1",
        "_id": "2",
        "_score": 0.0040983604,
        "_source": {
          "nested_field": [
            {
              "my_vector": [
                10,
                10,
                10
              ],
              "color": "red"
            },
            {
              "my_vector": [
                20,
                20,
                20
              ],
              "color": "green"
            },
            {
              "my_vector": [
                30,
                30,
                30
              ],
              "color": "black"
            }
          ]
        }
      }
    ]
  }
}
```

## 內部命中

當您根據巢狀欄位中的相符項目擷取文件時，預設情況下，回應不會包含哪些內部物件與查詢相符的資訊。因此，無法明確看出文件為何相符。若要在回應中包含相符巢狀欄位的資訊，您可以在查詢中提供 `inner_hits` 物件。若只要傳回 `inner_hits` 中相符文件的特定欄位，請在 `fields` 陣列中指定文件欄位。一般而言，您也應該從結果中排除 `_source`，以避免傳回整份文件。下列範例只傳回 `nested_field` 的 `color` 內部欄位：

```json
GET my-knn-index-1/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "nested_field",
      "query": {
        "knn": {
          "nested_field.my_vector": {
            "vector": [1,1,1],
            "k": 2
          }
        }
      },
      "inner_hits": {
        "_source": false,
        "fields":["nested_field.color"]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件。對於每個相符的文件，`inner_hits` 物件在 `fields` 陣列中只包含相符文件的 `nested_field.color` 欄位：

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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my-knn-index-1",
        "_id": "1",
        "_score": 1.0,
        "inner_hits": {
          "nested_field": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "my-knn-index-1",
                  "_id": "1",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 0
                  },
                  "_score": 1.0,
                  "fields": {
                    "nested_field.color": [
                      "blue"
                    ]
                  }
                }
              ]
            }
          }
        }
      },
      {
        "_index": "my-knn-index-1",
        "_id": "2",
        "_score": 0.0040983604,
        "inner_hits": {
          "nested_field": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 0.0040983604,
              "hits": [
                {
                  "_index": "my-knn-index-1",
                  "_id": "2",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 0
                  },
                  "_score": 0.0040983604,
                  "fields": {
                    "nested_field.color": [
                      "red"
                    ]
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

## 擷取所有巢狀命中

根據預設，當您查詢巢狀欄位時，只會考量分數最高的巢狀文件。若要擷取每個父文件內所有巢狀欄位文件的分數，請在查詢中將 `expand_nested_docs` 設為 `true`。父文件的分數會以其分數的平均值計算。若要使用巢狀欄位文件中分數最高者作為父文件的分數，請將 `score_mode` 設為 `max`：

```json
GET my-knn-index-1/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "nested_field",
      "query": {
        "knn": {
          "nested_field.my_vector": {
            "vector": [1,1,1],
            "k": 2,
            "expand_nested_docs": true
          }
        }
      },
      "inner_hits": {
        "_source": false,
        "fields":["nested_field.color"]
      },
      "score_mode": "max"
    }
  }
}
```
{% include copy-curl.html %}

回應會包含所有相符的文件：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my-knn-index-1",
        "_id": "1",
        "_score": 1.0,
        "inner_hits": {
          "nested_field": {
            "hits": {
              "total": {
                "value": 3,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "my-knn-index-1",
                  "_id": "1",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 0
                  },
                  "_score": 1.0,
                  "fields": {
                    "nested_field.color": [
                      "blue"
                    ]
                  }
                },
                {
                  "_index": "my-knn-index-1",
                  "_id": "1",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 1
                  },
                  "_score": 0.25,
                  "fields": {
                    "nested_field.color": [
                      "blue"
                    ]
                  }
                },
                {
                  "_index": "my-knn-index-1",
                  "_id": "1",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 2
                  },
                  "_score": 0.07692308,
                  "fields": {
                    "nested_field.color": [
                      "white"
                    ]
                  }
                }
              ]
            }
          }
        }
      },
      {
        "_index": "my-knn-index-1",
        "_id": "2",
        "_score": 0.0040983604,
        "inner_hits": {
          "nested_field": {
            "hits": {
              "total": {
                "value": 3,
                "relation": "eq"
              },
              "max_score": 0.0040983604,
              "hits": [
                {
                  "_index": "my-knn-index-1",
                  "_id": "2",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 0
                  },
                  "_score": 0.0040983604,
                  "fields": {
                    "nested_field.color": [
                      "blue"
                    ]
                  }
                },
                {
                  "_index": "my-knn-index-1",
                  "_id": "2",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 1
                  },
                  "_score": 9.2250924E-4,
                  "fields": {
                    "nested_field.color": [
                      "yellow"
                    ]
                  }
                },
                {
                  "_index": "my-knn-index-1",
                  "_id": "2",
                  "_nested": {
                    "field": "nested_field",
                    "offset": 2
                  },
                  "_score": 3.9619653E-4,
                  "fields": {
                    "nested_field.color": [
                      "white"
                    ]
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

## 對巢狀欄位套用篩選的向量搜尋

您可以對具有巢狀欄位的向量搜尋套用篩選條件。篩選條件可套用於最上層欄位或巢狀欄位內的欄位。

下列範例會對最上層欄位套用篩選條件。

首先，建立具有巢狀欄位的向量索引：

```json
PUT my-knn-index-1
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "nested_field": {
        "type": "nested",
        "properties": {
          "my_vector": {
            "type": "knn_vector",
            "dimension": 3,
            "space_type": "l2",
            "method": {
              "name": "hnsw",
              "engine": "lucene",
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

建立索引之後，對其新增一些資料：

```json
PUT _bulk?refresh=true
{ "index": { "_index": "my-knn-index-1", "_id": "1" } }
{"parking": false, "nested_field":[{"my_vector":[1,1,1]},{"my_vector":[2,2,2]},{"my_vector":[3,3,3]}]}
{ "index": { "_index": "my-knn-index-1", "_id": "2" } }
{"parking": true, "nested_field":[{"my_vector":[10,10,10]},{"my_vector":[20,20,20]},{"my_vector":[30,30,30]}]}
{ "index": { "_index": "my-knn-index-1", "_id": "3" } }
{"parking": true, "nested_field":[{"my_vector":[100,100,100]},{"my_vector":[200,200,200]},{"my_vector":[300,300,300]}]}
```
{% include copy-curl.html %}

接著使用 `knn` 查詢類型搭配篩選條件，對資料執行向量搜尋。下列查詢會傳回其 `parking` 欄位設為 `true` 的文件：

```json
GET my-knn-index-1/_search
{
  "query": {
    "nested": {
      "path": "nested_field",
      "query": {
        "knn": {
          "nested_field.my_vector": {
            "vector": [
              1,
              1,
              1
            ],
            "k": 3,
            "filter": {
              "term": {
                "parking": true
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

即使最接近查詢向量的三個向量都位於文件 1 中，查詢仍會傳回文件 2 和 3，因為文件 1 已被篩選掉：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.0040983604,
    "hits": [
      {
        "_index": "my-knn-index-1",
        "_id": "2",
        "_score": 0.0040983604,
        "_source": {
          "parking": true,
          "nested_field": [
            {
              "my_vector": [
                10,
                10,
                10
              ]
            },
            {
              "my_vector": [
                20,
                20,
                20
              ]
            },
            {
              "my_vector": [
                30,
                30,
                30
              ]
            }
          ]
        }
      },
      {
        "_index": "my-knn-index-1",
        "_id": "3",
        "_score": 3.400898E-5,
        "_source": {
          "parking": true,
          "nested_field": [
            {
              "my_vector": [
                100,
                100,
                100
              ]
            },
            {
              "my_vector": [
                200,
                200,
                200
              ]
            },
            {
              "my_vector": [
                300,
                300,
                300
              ]
            }
          ]
        }
      }
    ]
  }
}
```
