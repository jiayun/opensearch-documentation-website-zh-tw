---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "k-NN 查詢說明"
parent: k-NN
grand_parent: AI and vector search queries
nav_order: 10
---

# k-NN 查詢說明
**3.0 版新增**
{: .label .label-purple }

您可以提供 `explain` 參數，以了解 `knn` 查詢中分數的計算、正規化與合併方式。啟用後，它會提供每個搜尋結果評分程序的詳細資訊，包括所使用的分數正規化技術、不同分數的合併方式，以及各個子查詢分數的計算過程。這種全面的洞察讓您更容易理解並最佳化 `knn` 查詢結果。如需 `explain` 的更多資訊，請參閱 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/explain/)。

`explain` 在資源與時間方面都是昂貴的操作。對於正式環境叢集，我們建議僅在疑難排解時少量使用。
{: .warning }

使用下列語法執行 Faiss 引擎的完整 `knn` 查詢時，您可以在 URL 中提供 `explain` 參數：

```json
GET {index}/_search?explain=true
POST {index}/_search?explain=true
```

`explain`：使用 Lucene 引擎的所有類型 k-NN 搜尋，不會像 Faiss 引擎那樣回傳詳細說明。
{: .note }

`explain` 參數適用於使用 Faiss 引擎的下列 k-NN 搜尋類型：

- [近似 k-NN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/approximate-knn/)
- 搭配 [精確搜尋]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/knn-score-script/) 的近似 k-NN 搜尋
- [磁碟型搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)
- [搭配高效篩選的 k-NN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/efficient-knn-filtering/)
- [放射狀搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/radial-search-knn/)
- 搭配 `term` 查詢的 k-NN 搜尋

`explain`：使用巢狀欄位的 k-NN 搜尋，不會像其他搜尋那樣回傳詳細說明。
{: .note }

您可以將 `explain` 參數作為查詢參數提供：

```json
GET my-knn-index/_search?explain=true
{
  "query": {
    "knn": {
      "my_vector": {
      "vector": [2, 3, 5, 7],
      "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，您可以在請求本文中提供 `explain` 參數：

```json
GET my-knn-index/_search
{
  "query": {
    "knn": {
      "my_vector": {
      "vector": [2, 3, 5, 7],
      "k": 2
      }
    }
  },
  "explain": true
}
```
{% include copy-curl.html %}

## 範例：近似 k-NN 搜尋

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took": 216038,
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
    "max_score": 88.4,
    "hits": [
      {
        "_shard": "[my-knn-index-1][0]",
        "_node": "VHcyav6OTsmXdpsttX2Yug",
        "_index": "my-knn-index-1",
        "_id": "5",
        "_score": 88.4,
        "_source": {
          "my_vector1": [
            2.5,
            3.5,
            5.5,
            7.4
          ],
          "price": 8.9
        },
        "_explanation": {
          "value": 88.4,
          "description": "the type of knn search executed was Approximate-NN",
          "details": [
            {
              "value": 88.4,
              "description": "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = innerproduct where score is computed as `-rawScore + 1` from:",
              "details": [
                {
                  "value": -87.4,
                  "description": "rawScore, returned from FAISS library",
                  "details": []
                }
              ]
            }
          ]
        }
      },
      {
        "_shard": "[my-knn-index-1][0]",
        "_node": "VHcyav6OTsmXdpsttX2Yug",
        "_index": "my-knn-index-1",
        "_id": "2",
        "_score": 84.7,
        "_source": {
          "my_vector1": [
            2.5,
            3.5,
            5.6,
            6.7
          ],
          "price": 5.5
        },
        "_explanation": {
          "value": 84.7,
          "description": "the type of knn search executed was Approximate-NN",
          "details": [
            {
              "value": 84.7,
              "description": "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = innerproduct where score is computed as `-rawScore + 1` from:",
              "details": [
                {
                  "value": -83.7,
                  "description": "rawScore, returned from FAISS library",
                  "details": []
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```
</details>

## 範例：搭配精確搜尋的近似 k-NN 搜尋

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took": 87,
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
    "max_score": 84.7,
    "hits": [
      {
        "_shard": "[my-knn-index-1][0]",
        "_node": "MQVux8dZRWeznuEYKhMq0Q",
        "_index": "my-knn-index-1",
        "_id": "7",
        "_score": 84.7,
        "_source": {
          "my_vector2": [
            2.5,
            3.5,
            5.6,
            6.7
          ],
          "price": 5.5
        },
        "_explanation": {
          "value": 84.7,
          "description": "the type of knn search executed was Approximate-NN",
          "details": [
            {
              "value": 84.7,
              "description": "the type of knn search executed at leaf was Exact with spaceType = INNER_PRODUCT, vectorDataType = FLOAT, queryVector = [2.0, 3.0, 5.0, 6.0]",
              "details": []
            }
          ]
        }
      },
      {
        "_shard": "[my-knn-index-1][0]",
        "_node": "MQVux8dZRWeznuEYKhMq0Q",
        "_index": "my-knn-index-1",
        "_id": "8",
        "_score": 82.2,
        "_source": {
          "my_vector2": [
            4.5,
            5.5,
            6.7,
            3.7
          ],
          "price": 4.4
        },
        "_explanation": {
          "value": 82.2,
          "description": "the type of knn search executed was Approximate-NN",
          "details": [
            {
              "value": 82.2,
              "description": "the type of knn search executed at leaf was Exact with spaceType = INNER_PRODUCT, vectorDataType = FLOAT, queryVector = [2.0, 3.0, 5.0, 6.0]",
              "details": []
            }
          ]
        }
      }
    ]
  }
```
</details>

## 範例：磁碟型搜尋

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 381.0,
    "hits" : [
      {
        "_shard" : "[my-vector-index][0]",
        "_node" : "pLaiqZftTX-MVSKdQSu7ow",
        "_index" : "my-vector-index",
        "_id" : "9",
        "_score" : 381.0,
        "_source" : {
          "my_vector_field" : [
            9.5,
            9.5,
            9.5,
            9.5,
            9.5,
            9.5,
            9.5,
            9.5
          ],
          "price" : 8.9
        },
        "_explanation" : {
          "value" : 381.0,
          "description" : "the type of knn search executed was Disk-based and the first pass k was 100 with vector dimension of 8, over sampling factor of 5.0, shard level rescoring enabled",
          "details" : [
            {
              "value" : 381.0,
              "description" : "the type of knn search executed at leaf was Approximate-NN with spaceType = HAMMING, vectorDataType = FLOAT, queryVector = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]",
              "details" : [ ]
            }
          ]
        }
      }
    ]
  }
}
```
</details>

## 範例：具備高效篩選的 k-NN 搜尋

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 51,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.8620689,
    "hits" : [
      {
        "_shard" : "[products-shirts][0]",
        "_node" : "9epk8WoFT8yvnUI0tAaJgQ",
        "_index" : "products-shirts",
        "_id" : "8",
        "_score" : 0.8620689,
        "_source" : {
          "item_vector" : [
            2.4,
            4.0,
            3.0
          ],
          "size" : "small",
          "rating" : 8
        },
        "_explanation" : {
          "value" : 0.8620689,
          "description" : "the type of knn search executed was Approximate-NN",
          "details" : [
            {
              "value" : 0.8620689,
              "description" : "the type of knn search executed at leaf was Exact since filteredIds = 2 is less than or equal to K = 10 with spaceType = L2, vectorDataType = FLOAT, queryVector = [2.0, 4.0, 3.0]",
              "details" : [ ]
            }
          ]
        }
      },
      {
        "_shard" : "[products-shirts][0]",
        "_node" : "9epk8WoFT8yvnUI0tAaJgQ",
        "_index" : "products-shirts",
        "_id" : "6",
        "_score" : 0.029691212,
        "_source" : {
          "item_vector" : [
            6.4,
            3.4,
            6.6
          ],
          "size" : "small",
          "rating" : 9
        },
        "_explanation" : {
          "value" : 0.029691212,
          "description" : "the type of knn search executed was Approximate-NN",
          "details" : [
            {
              "value" : 0.029691212,
              "description" : "the type of knn search executed at leaf was Exact since filteredIds = 2 is less than or equal to K = 10 with spaceType = L2, vectorDataType = FLOAT, queryVector = [2.0, 4.0, 3.0]",
              "details" : [ ]
            }
          ]
        }
      }
    ]
  }
}
```
</details>

## 範例：徑向搜尋

```json
GET my-knn-index/_search?explain=true
{
  "query": {
    "knn": {
      "my_vector": {
      "vector": [7.1, 8.3],
      "max_distance": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 376529,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.98039204,
    "hits" : [
      {
        "_shard" : "[knn-index-test][0]",
        "_node" : "c9b4aPe4QGO8eOtb8P5D3g",
        "_index" : "knn-index-test",
        "_id" : "1",
        "_score" : 0.98039204,
        "_source" : {
          "my_vector" : [
            7.0,
            8.2
          ],
          "price" : 4.4
        },
        "_explanation" : {
          "value" : 0.98039204,
          "description" : "the type of knn search executed was Radial with the radius of 2.0",
          "details" : [
            {
              "value" : 0.98039204,
              "description" : "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = l2 where score is computed as `1 / (1 + rawScore)` from:",
              "details" : [
                {
                  "value" : 0.020000057,
                  "description" : "rawScore, returned from FAISS library",
                  "details" : [ ]
                }
              ]
            }
          ]
        }
      },
      {
        "_shard" : "[knn-index-test][0]",
        "_node" : "c9b4aPe4QGO8eOtb8P5D3g",
        "_index" : "knn-index-test",
        "_id" : "3",
        "_score" : 0.9615384,
        "_source" : {
          "my_vector" : [
            7.3,
            8.3
          ],
          "price" : 19.1
        },
        "_explanation" : {
          "value" : 0.9615384,
          "description" : "the type of knn search executed was Radial with the radius of 2.0",
          "details" : [
            {
              "value" : 0.9615384,
              "description" : "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = l2 where score is computed as `1 / (1 + rawScore)` from:",
              "details" : [
                {
                  "value" : 0.040000115,
                  "description" : "rawScore, returned from FAISS library",
                  "details" : [ ]
                }
              ]
            }
          ]
        }
      }
    ]
  }
}

```
</details>

## 範例：使用詞項查詢的 k-NN 搜尋

```json
GET my-knn-index/_search?explain=true
{
  "query": {
    "bool": {
      "should": [
        {
          "knn": {
            "my_vector2": { // vector field name
              "vector": [2, 3, 5, 6],
              "k": 2
            }
          }
        },
      {
        "term": {
            "price": "4.4"
          }
        }
      ]
    }  
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    範例回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 51,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 84.7,
    "hits" : [
      {
        "_shard" : "[my-knn-index-1][0]",
        "_node" : "c9b4aPe4QGO8eOtb8P5D3g",
        "_index" : "my-knn-index-1",
        "_id" : "7",
        "_score" : 84.7,
        "_source" : {
          "my_vector2" : [
            2.5,
            3.5,
            5.6,
            6.7
          ],
          "price" : 5.5
        },
        "_explanation" : {
          "value" : 84.7,
          "description" : "sum of:",
          "details" : [
            {
              "value" : 84.7,
              "description" : "the type of knn search executed was Approximate-NN",
              "details" : [
                {
                  "value" : 84.7,
                  "description" : "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = innerproduct where score is computed as `-rawScore + 1` from:",
                  "details" : [
                    {
                      "value" : -83.7,
                      "description" : "rawScore, returned from FAISS library",
                      "details" : [ ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      },
      {
        "_shard" : "[my-knn-index-1][0]",
        "_node" : "c9b4aPe4QGO8eOtb8P5D3g",
        "_index" : "my-knn-index-1",
        "_id" : "8",
        "_score" : 83.2,
        "_source" : {
          "my_vector2" : [
            4.5,
            5.5,
            6.7,
            3.7
          ],
          "price" : 4.4
        },
        "_explanation" : {
          "value" : 83.2,
          "description" : "sum of:",
          "details" : [
            {
              "value" : 82.2,
              "description" : "the type of knn search executed was Approximate-NN",
              "details" : [
                {
                  "value" : 82.2,
                  "description" : "the type of knn search executed at leaf was Approximate-NN with vectorDataType = FLOAT, spaceType = innerproduct where score is computed as `-rawScore + 1` from:",
                  "details" : [
                    {
                      "value" : -81.2,
                      "description" : "rawScore, returned from FAISS library",
                      "details" : [ ]
                    }
                  ]
                }
              ]
            },
            {
              "value" : 1.0,
              "description" : "price:[1082969293 TO 1082969293]",
              "details" : [ ]
            }
          ]
        }
      }
    ]
  }
}
```

</details>

## 回應本文欄位

欄位 | 說明
:--- | :---
`explanation` | `explanation` 物件包含下列欄位：<br> - `value`：包含計算結果。<br> - `description`：說明執行的計算類型。對於分數正規化，`description` 欄位中的資訊包含用於正規化或組合的技術，以及對應的分數。<br> - `details`：顯示執行的任何子計算。 

