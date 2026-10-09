---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "高效的 k-NN 篩選"
parent: Filtering data
nav_order: 10
---

# 高效的 k-NN 篩選

您可以使用 `lucene`、`faiss` 或 `jvector` 引擎來執行高效的 k-NN 篩選。

## Lucene k-NN 篩選實作

Lucene 引擎支援使用 HNSW 圖形的 k-NN 搜尋的 Lucene 篩選器。

當您為 k-NN 搜尋指定 Lucene 篩選器時，Lucene 演算法會決定要執行搭配預先篩選的精確 k-NN 搜尋，還是執行搭配經修改的後置篩選的近似搜尋。此演算法使用下列變數：

- N：索引中的文件數。
- P：套用篩選器後文件子集中的文件數 (P <= N)。
- k：回應中要傳回的向量數上限。

下列流程圖概述 Lucene 演算法。

![用於篩選的 Lucene 演算法]({{site.url}}{{site.baseurl}}/images/lucene-algorithm.png)

如需 Lucene 篩選實作及基礎 `KnnFloatVectorQuery` 的詳細資訊，請參閱 [Apache Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/KnnFloatVectorQuery.html)。

## 使用 Lucene k-NN 篩選器

請考慮一個包含 12 份飯店資訊文件的資料集。下圖依位置顯示 xy 座標平面上的所有飯店。此外，評分介於 8 到 10 (含) 之間的飯店以橘色圓點表示，提供停車位的飯店則以綠色圓圈表示。搜尋點以紅色標示：

![含篩選條件的文件圖形]({{site.url}}{{site.baseurl}}/images/knn-doc-set-for-filtering.png)

在此範例中，您將建立索引，並搜尋最接近搜尋位置、評分高且提供停車位的前三家飯店。

### 步驟 1：建立新索引

您必須先建立含有 `knn_vector` 欄位的索引，才能執行帶有篩選器的 k-NN 搜尋。針對此欄位，您需要在對應中指定 `lucene` 作為引擎，並指定 `hnsw` 作為 `method`。

下列請求會建立名為 `hotels-index` 的新索引，其中含有名為 `location` 的 `knn-filter` 欄位：

```json
PUT /hotels-index
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100,
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "location": {
        "type": "knn_vector",
        "dimension": 2,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
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
```
{% include copy-curl.html %}

### 步驟 2：將資料新增至您的索引

接著，將資料新增至您的索引。

下列請求會新增 12 份包含飯店位置、評分及停車資訊的文件：

```json
POST /_bulk
{ "index": { "_index": "hotels-index", "_id": "1" } }
{ "location": [5.2, 4.4], "parking" : "true", "rating" : 5 }
{ "index": { "_index": "hotels-index", "_id": "2" } }
{ "location": [5.2, 3.9], "parking" : "false", "rating" : 4 }
{ "index": { "_index": "hotels-index", "_id": "3" } }
{ "location": [4.9, 3.4], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-index", "_id": "4" } }
{ "location": [4.2, 4.6], "parking" : "false", "rating" : 6}
{ "index": { "_index": "hotels-index", "_id": "5" } }
{ "location": [3.3, 4.5], "parking" : "true", "rating" : 8 }
{ "index": { "_index": "hotels-index", "_id": "6" } }
{ "location": [6.4, 3.4], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-index", "_id": "7" } }
{ "location": [4.2, 6.2], "parking" : "true", "rating" : 5 }
{ "index": { "_index": "hotels-index", "_id": "8" } }
{ "location": [2.4, 4.0], "parking" : "true", "rating" : 8 }
{ "index": { "_index": "hotels-index", "_id": "9" } }
{ "location": [1.4, 3.2], "parking" : "false", "rating" : 5 }
{ "index": { "_index": "hotels-index", "_id": "10" } }
{ "location": [7.0, 9.9], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-index", "_id": "11" } }
{ "location": [3.0, 2.3], "parking" : "false", "rating" : 6 }
{ "index": { "_index": "hotels-index", "_id": "12" } }
{ "location": [5.0, 1.0], "parking" : "true", "rating" : 3 }
```
{% include copy-curl.html %}

### 步驟 3：使用篩選器搜尋您的資料

現在您可以建立帶有篩選器的 k-NN 搜尋。在 k-NN 查詢子句中，加入用來搜尋最近鄰的目標點、要傳回的最近鄰數目 (`k`)，以及含有限制條件的篩選器。視您希望篩選器的限制程度而定，您可以在單一請求中新增多個查詢子句。

下列請求會建立 k-NN 查詢，搜尋座標為 `[5, 4]` 的位置附近、評分介於 8 到 10 (含) 之間且提供停車位的前三家飯店：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "knn": {
      "location": {
        "vector": [
          5,
          4
        ],
        "k": 3,
        "filter": {
          "bool": {
            "must": [
              {
                "range": {
                  "rating": {
                    "gte": 8,
                    "lte": 10
                  }
                }
              },
              {
                "term": {
                  "parking": "true"
                }
              }
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回最接近搜尋點且符合篩選條件的前三家飯店：

```json
{
  "took": 47,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.72992706,
    "hits": [
      {
        "_index": "hotels-index",
        "_id": "3",
        "_score": 0.72992706,
        "_source": {
          "location": [4.9, 3.4],
          "parking": "true",
          "rating": 9
        }
      },
      {
        "_index": "hotels-index",
        "_id": "6",
        "_score": 0.3012048,
        "_source": {
          "location": [6.4, 3.4],
          "parking": "true",
          "rating": 9
        }
      },
      {
        "_index": "hotels-index",
        "_id": "5",
        "_score": 0.24154587,
        "_source": {
          "location": [3.3, 4.5],
          "parking": "true",
          "rating": 8
        }
      }
    ]
  }
}
```

如需更多建構篩選器的方式，請參閱[建構篩選器](#constructing-a-filter)。

## Faiss k-NN 篩選實作

針對 k-NN 搜尋，您可以搭配 HNSW 演算法 (OpenSearch 2.9 版及更新版本) 或 IVF 演算法 (OpenSearch 2.10 版及更新版本) 使用 `faiss` 篩選器。

當您為 k-NN 搜尋指定 Faiss 篩選器時，Faiss 演算法會決定要執行搭配預先篩選的精確 k-NN 搜尋，還是執行搭配經修改的後置篩選的近似搜尋。此演算法使用下列變數：

- N：索引中的文件數。
- P：套用篩選器後文件子集中的文件數 (P <= N)。
- k：回應中要傳回的向量數上限。
- R：執行經過篩選的近似最近鄰搜尋後所傳回的結果數。
- FT (篩選閾值)：定義於 [`knn.advanced.filtered_exact_search_threshold` 設定]({{site.url}}{{site.baseurl}}/search-plugins/knn/settings/) 中的索引層級閾值，指定切換為精確搜尋。
- MDC (最大距離計算次數)：若未設定 `FT` (篩選閾值)，精確搜尋中允許的最大距離計算次數。此值無法變更。

下列流程圖概述 Faiss 演算法。

![用於篩選的 Faiss 演算法]({{site.url}}{{site.baseurl}}/images/faiss-algorithm.jpg)

### 停用精確搜尋後備機制

**3.5 版新增**
{: .label .label-purple }

當 Faiss 高效篩選 ANN 搜尋傳回的結果少於 `k` 筆 (R < k)，即使有超過 `k` 份文件符合篩選條件 (P ≥ k)，演算法會退回對已篩選文件 ID 執行精確搜尋，以確保傳回 `k` 筆結果。

對於可接受少於 `k` 筆結果的延遲敏感工作負載，您可以將 `index.knn.faiss.efficient_filter.disable_exact_search` 索引設定設為 `true` 來停用此後備機制。啟用此設定後，搜尋只會傳回近似結果，並略過額外的精確搜尋。
如需此設定的更多資訊，請參閱 [向量搜尋設定]({{site.url}}{{site.baseurl}}/vector-search/settings/)。

## 使用 Faiss 高效篩選器

假設有一個為電子商務應用程式儲存各種襯衫資訊的索引。您想找出與您現有襯衫相似的評分最高襯衫，但希望依襯衫尺寸限制結果。

在此範例中，您將建立一個索引，並搜尋與您提供的襯衫相似的襯衫。

### 步驟 1：建立新索引

在執行帶篩選器的 k-NN 搜尋之前，您需要建立一個含有 `knn_vector` 欄位的索引。對於此欄位，您需要在對應中將 `faiss` 和 `hnsw` 指定為 `method`。

下列請求會建立一個包含襯衫向量表示的索引：

```json
PUT /products-shirts
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "item_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將資料加入索引

接下來，將資料加入您的索引。

下列請求會加入 12 份包含襯衫資訊的文件，包括其向量表示、尺寸與評分：

```json
POST /_bulk?refresh
{ "index": { "_index": "products-shirts", "_id": "1" } }
{ "item_vector": [5.2, 4.4, 8.4], "size" : "large", "rating" : 5 }
{ "index": { "_index": "products-shirts", "_id": "2" } }
{ "item_vector": [5.2, 3.9, 2.9], "size" : "small", "rating" : 4 }
{ "index": { "_index": "products-shirts", "_id": "3" } }
{ "item_vector": [4.9, 3.4, 2.2], "size" : "xlarge", "rating" : 9 }
{ "index": { "_index": "products-shirts", "_id": "4" } }
{ "item_vector": [4.2, 4.6, 5.5], "size" : "large", "rating" : 6}
{ "index": { "_index": "products-shirts", "_id": "5" } }
{ "item_vector": [3.3, 4.5, 8.8], "size" : "medium", "rating" : 8 }
{ "index": { "_index": "products-shirts", "_id": "6" } }
{ "item_vector": [6.4, 3.4, 6.6], "size" : "small", "rating" : 9 }
{ "index": { "_index": "products-shirts", "_id": "7" } }
{ "item_vector": [4.2, 6.2, 4.6], "size" : "small", "rating" : 5 }
{ "index": { "_index": "products-shirts", "_id": "8" } }
{ "item_vector": [2.4, 4.0, 3.0], "size" : "small", "rating" : 8 }
{ "index": { "_index": "products-shirts", "_id": "9" } }
{ "item_vector": [1.4, 3.2, 9.0], "size" : "small", "rating" : 5 }
{ "index": { "_index": "products-shirts", "_id": "10" } }
{ "item_vector": [7.0, 9.9, 9.0], "size" : "xlarge", "rating" : 9 }
{ "index": { "_index": "products-shirts", "_id": "11" } }
{ "item_vector": [3.0, 2.3, 2.0], "size" : "large", "rating" : 6 }
{ "index": { "_index": "products-shirts", "_id": "12" } }
{ "item_vector": [5.0, 1.0, 4.0], "size" : "large", "rating" : 3 }

```
{% include copy-curl.html %}

### 步驟 3：使用篩選器搜尋資料

現在您可以建立帶篩選器的 k-NN 搜尋。在 k-NN 查詢子句中，加入用於搜尋相似襯衫的襯衫向量表示、要傳回的最近鄰居數量 (`k`)，以及依尺寸與評分的篩選器。

下列請求會搜尋評分介於 7 到 10 (含) 之間的小尺寸襯衫：

```json
POST /products-shirts/_search
{
  "size": 2,
  "query": {
    "knn": {
      "item_vector": {
        "vector": [
          2, 4, 3
        ],
        "k": 10,
        "filter": {
          "bool": {
            "must": [
              {
                "range": {
                  "rating": {
                    "gte": 7,
                    "lte": 10
                  }
                }
              },
              {
                "term": {
                  "size": "small"
                }
              }
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回兩份符合的文件：

```json
{
  "took": 2,
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
    "max_score": 0.8620689,
    "hits": [
      {
        "_index": "products-shirts",
        "_id": "8",
        "_score": 0.8620689,
        "_source": {
          "item_vector": [2.4, 4, 3],
          "size": "small",
          "rating": 8
        }
      },
      {
        "_index": "products-shirts",
        "_id": "6",
        "_score": 0.029691212,
        "_source": {
          "item_vector": [6.4, 3.4, 6.6],
          "size": "small",
          "rating": 9
        }
      }
    ]
  }
}
```

如需更多建構篩選器的方式，請參閱 [建構篩選器](#constructing-a-filter)。

### ACORN 篩選最佳化

3.1 版新增
{: .label .label-purple }
ACORN 篩選最佳化會修改基準演算法，僅對符合篩選條件的向量進行評分與探索。當篩選導致圖形稀疏度增加時，搜尋會擴展以包含鄰居的鄰居。此額外探索的程度取決於被篩選掉的鄰居百分比，篩選條件越嚴格，搜尋範圍越廣。

當篩選程度極小時，演算法會完全略過這些最佳化。預設情況下，此門檻為 60%。只有當目前鄰居中符合篩選條件者少於 90% 時，才會進行擴展的鄰居探索。

啟用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)時，高效篩選器架構會繼續在 HNSW 內套用篩選。只有當被篩選的文件數量為 HNSW 演算法目前考慮的搜尋空間中文件總數的 60% 或更少時，才會套用 ACORN 篩選最佳化。

## 使用 JVector 高效篩選器

[`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)支援使用 `jvector` 引擎搭配 `disk_ann` 方法的篩選。`knn` 查詢子句中的內嵌 `filter` 會在圖形遍歷期間限制候選項目。也支援使用 `post_filter` 參數的事後篩選，但當篩選條件嚴格時，可能傳回少於 `k` 筆結果。

在此範例中，您將使用 `jvector` 引擎建立索引，並搜尋評分高且提供停車場的三家最近飯店。

### 步驟 1：建立新索引

建立一個含有 `knn_vector` 欄位的索引，將 `jvector` 指定為引擎，`disk_ann` 指定為方法：

```json
PUT /hotels-jvector-index
{
  "settings": {
    "index": {
      "knn": true,
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "location": {
        "type": "knn_vector",
        "dimension": 2,
        "method": {
          "name": "disk_ann",
          "space_type": "l2",
          "engine": "jvector",
          "parameters": {
            "ef_construction": 100,
            "m": 16
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將資料新增至您的索引

新增 12 份包含飯店位置、評分和停車資訊的文件：

```json
POST /_bulk
{ "index": { "_index": "hotels-jvector-index", "_id": "1" } }
{ "location": [5.2, 4.4], "parking" : "true", "rating" : 5 }
{ "index": { "_index": "hotels-jvector-index", "_id": "2" } }
{ "location": [5.2, 3.9], "parking" : "false", "rating" : 4 }
{ "index": { "_index": "hotels-jvector-index", "_id": "3" } }
{ "location": [4.9, 3.4], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-jvector-index", "_id": "4" } }
{ "location": [4.2, 4.6], "parking" : "false", "rating" : 6}
{ "index": { "_index": "hotels-jvector-index", "_id": "5" } }
{ "location": [3.3, 4.5], "parking" : "true", "rating" : 8 }
{ "index": { "_index": "hotels-jvector-index", "_id": "6" } }
{ "location": [6.4, 3.4], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-jvector-index", "_id": "7" } }
{ "location": [4.2, 6.2], "parking" : "true", "rating" : 5 }
{ "index": { "_index": "hotels-jvector-index", "_id": "8" } }
{ "location": [2.4, 4.0], "parking" : "true", "rating" : 8 }
{ "index": { "_index": "hotels-jvector-index", "_id": "9" } }
{ "location": [1.4, 3.2], "parking" : "false", "rating" : 5 }
{ "index": { "_index": "hotels-jvector-index", "_id": "10" } }
{ "location": [7.0, 9.9], "parking" : "true", "rating" : 9 }
{ "index": { "_index": "hotels-jvector-index", "_id": "11" } }
{ "location": [3.0, 2.3], "parking" : "false", "rating" : 6 }
{ "index": { "_index": "hotels-jvector-index", "_id": "12" } }
{ "location": [5.0, 1.0], "parking" : "true", "rating" : 3 }
```
{% include copy-curl.html %}

### 步驟 3：使用篩選條件搜尋您的資料

將 `filter` 放在 `knn` 查詢子句中，以在圖形遍歷期間限制候選項目。以下請求會搜尋 `[5, 4]` 附近評分介於 8 到 10 之間且提供停車位的前三家飯店：

```json
POST /hotels-jvector-index/_search
{
  "size": 3,
  "query": {
    "knn": {
      "location": {
        "vector": [5, 4],
        "k": 3,
        "filter": {
          "bool": {
            "must": [
              {
                "range": {
                  "rating": {
                    "gte": 8,
                    "lte": 10
                  }
                }
              },
              {
                "term": {
                  "parking": "true"
                }
              }
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 4：使用後置篩選搜尋您的資料

您也可以在 ANN 搜尋之後使用 `post_filter` 套用篩選。由於 `post_filter` 是在 ANN 擷取之後執行，當篩選條件較嚴格時，最終結果數量可能會少於 `k`。為了補償，請將 `k` 設定為大於您所需結果數量的值。

以下請求會擷取最接近的 20 家飯店，然後將結果限制為評分 8 以上且提供停車位的飯店：

```json
POST /hotels-jvector-index/_search
{
  "size": 3,
  "query": {
    "knn": {
      "location": {
        "vector": [5, 4],
        "k": 20
      }
    }
  },
  "post_filter": {
    "bool": {
      "must": [
        {
          "range": {
            "rating": {
              "gte": 8,
              "lte": 10
            }
          }
        },
        {
          "term": {
            "parking": "true"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 建構篩選器

針對相同條件，有多種方式可以建構篩選器。例如，您可以使用下列結構來建立篩選器，以傳回提供停車位的飯店：

- 在 `should` 子句中使用 `term` 查詢子句
- 在 `should` 子句中使用 `wildcard` 查詢子句
- 在 `should` 子句中使用 `regexp` 查詢子句
- 使用 `must_not` 子句來排除 `parking` 設為 `false` 的飯店。

以下請求示範了這四種搜尋提供停車位飯店的不同方式：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "knn": {
      "location": {
        "vector": [ 5.0, 4.0 ],
        "k": 3,
        "filter": {
          "bool": {
            "must": {
              "range": {
                "rating": {
                  "gte": 1,
                  "lte": 6
                }
              }
            },
            "should": [
            {
              "term": {
                "parking": "true"
              }
            },
            {
              "wildcard": {
                "parking": {
                  "value": "t*e"
                }
              }
            },
            {
              "regexp": {
                "parking": "[a-zA-Z]rue"
              }
            }
            ],
            "must_not": [
            {
              "term": {
                  "parking": "false"
              }
            }
            ],
            "minimum_should_match": 1
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
