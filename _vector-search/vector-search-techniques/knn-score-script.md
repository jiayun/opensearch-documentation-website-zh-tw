---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用評分指令碼進行精確 k-NN 搜尋"
nav_order: 20
parent: Vector search techniques
has_children: true
has_math: true
redirect_from:
  - /search-plugins/knn/knn-score-script/ 
---

# 使用評分指令碼進行精確 k-NN 搜尋

您可以使用評分指令碼進行精確 k-nearest neighbors (k-NN) 搜尋，以找出與給定查詢點最接近的精確 k 個最近鄰。使用 k-NN 評分指令碼，您可以在執行最近鄰搜尋之前，先對索引套用篩選條件。這對於動態搜尋使用案例很有用，因為這類案例的索引本文可能會依其他條件而有所不同。

由於評分指令碼方法會執行暴力搜尋，其擴展效率不如[近似方法]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/)。在某些情況下，您最好考慮重構工作流程或索引結構，改用近似方法，而非評分指令碼方法。

## 開始使用向量評分指令碼

與近似最近鄰 (ANN) 搜尋類似，若要在向量本文上使用評分指令碼，您必須先建立一個含有一或多個 `knn_vector` 欄位的索引。

如果您打算只使用評分指令碼方法（而不使用近似方法），可以將 `index.knn` 設為 `false`，並不要設定 `index.knn.space_type`。您可以在搜尋時選擇空間類型。關於 k-NN 評分指令碼支援的空間，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

此範例建立一個含有兩個 `knn_vector` 欄位的索引：

```json
PUT my-knn-index-1
{
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 2
      },
      "my_vector2": {
        "type": "knn_vector",
        "dimension": 4
      }
    }
  }
}
```
{% include copy-curl.html %}

如果您想*只*使用評分指令碼，可以省略 `"index.knn": true`。此方法可加快編製索引速度並降低記憶體用量，但您將無法在該索引上執行標準 k-NN 查詢。
{: .tip}

建立索引之後，您可以新增一些資料到索引中：

```json
POST _bulk
{ "index": { "_index": "my-knn-index-1", "_id": "1" } }
{ "my_vector1": [1.5, 2.5], "price": 12.2 }
{ "index": { "_index": "my-knn-index-1", "_id": "2" } }
{ "my_vector1": [2.5, 3.5], "price": 7.1 }
{ "index": { "_index": "my-knn-index-1", "_id": "3" } }
{ "my_vector1": [3.5, 4.5], "price": 12.9 }
{ "index": { "_index": "my-knn-index-1", "_id": "4" } }
{ "my_vector1": [5.5, 6.5], "price": 1.2 }
{ "index": { "_index": "my-knn-index-1", "_id": "5" } }
{ "my_vector1": [4.5, 5.5], "price": 3.7 }
{ "index": { "_index": "my-knn-index-1", "_id": "6" } }
{ "my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 10.3 }
{ "index": { "_index": "my-knn-index-1", "_id": "7" } }
{ "my_vector2": [2.5, 3.5, 5.6, 6.7], "price": 5.5 }
{ "index": { "_index": "my-knn-index-1", "_id": "8" } }
{ "my_vector2": [4.5, 5.5, 6.7, 3.7], "price": 4.4 }
{ "index": { "_index": "my-knn-index-1", "_id": "9" } }
{ "my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 8.9 }
```
{% include copy-curl.html %}

最後，您可以使用 `knn` 指令碼對資料執行精確最近鄰搜尋：

```json
GET my-knn-index-1/_search
{
 "size": 4,
 "query": {
   "script_score": {
     "query": {
       "match_all": {}
     },
     "script": {
       "source": "knn_score",
       "lang": "knn",
       "params": {
         "field": "my_vector2",
         "query_value": [2.0, 3.0, 5.0, 6.0],
         "space_type": "cosinesimil"
       }
     }
   }
 }
}
```
{% include copy-curl.html %}

所有參數都是必要。

- `lang` 是指令碼類型。此值通常是 `painless`，但在此您必須指定 `knn`。
- `source` 是指令碼名稱，即 `knn_score`。

  此指令碼是 k-NN 外掛程式的一部分，無法在標準 `_scripts` 路徑取得。對 `_cluster/state/metadata` 發出 GET 請求也不會傳回它。

- `field` 是包含您向量資料的欄位。
- `query_value` 是您想找出最近鄰的點。對於 Euclidean 和 cosine similarity 空間，此值必須是符合欄位對應中所設定維度的浮點數陣列。對於 Hamming bit distance，此值可以是 signed long 類型，或是 Base64 編碼字串（分別對應 long 和 binary 欄位類型）。
- `space_type` 對應於距離函式。如需更多資訊，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

[近似方法中的後置篩選範例]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/)顯示了一種傳回結果少於 `k` 筆的搜尋。如果您想避免這種情況，評分指令碼方法可讓您基本上反轉事件順序。換句話說，您可以先篩選要執行 k-NN 搜尋的文件集合。

此範例顯示使用評分指令碼方法進行 k-NN 搜尋的前置篩選方法。首先，建立索引：

```json
PUT my-knn-index-2
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 2
      },
      "color": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

然後新增一些文件：

```json
POST _bulk
{ "index": { "_index": "my-knn-index-2", "_id": "1" } }
{ "my_vector": [1, 1], "color" : "RED" }
{ "index": { "_index": "my-knn-index-2", "_id": "2" } }
{ "my_vector": [2, 2], "color" : "RED" }
{ "index": { "_index": "my-knn-index-2", "_id": "3" } }
{ "my_vector": [3, 3], "color" : "RED" }
{ "index": { "_index": "my-knn-index-2", "_id": "4" } }
{ "my_vector": [10, 10], "color" : "BLUE" }
{ "index": { "_index": "my-knn-index-2", "_id": "5" } }
{ "my_vector": [20, 20], "color" : "BLUE" }
{ "index": { "_index": "my-knn-index-2", "_id": "6" } }
{ "my_vector": [30, 30], "color" : "BLUE" }
```
{% include copy-curl.html %}

最後，使用 `script_score` 查詢先篩選您的文件，再找出最近鄰：

```json
GET my-knn-index-2/_search
{
  "size": 2,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "term": {
              "color": "BLUE"
            }
          }
        }
      },
      "script": {
        "lang": "knn",
        "source": "knn_score",
        "params": {
          "field": "my_vector",
          "query_value": [9.9, 9.9],
          "space_type": "l2"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 開始使用二進位資料評分指令碼

k-NN 評分指令碼也可讓您使用 Hamming distance 空間對二進位資料執行 k-NN 搜尋。
若要使用 Hamming distance，目標欄位的類型必須是 `binary` 或 `long`。如果您使用 `binary` 類型，資料必須是 Base64 編碼字串。

此範例顯示如何搭配 `binary` 欄位類型使用 Hamming distance 空間：

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "my_binary": {
        "type": "binary",
        "doc_values": true
      },
      "color": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

然後新增一些文件：

```json
POST _bulk
{ "index": { "_index": "my-index", "_id": "1" } }
{ "my_binary": "SGVsbG8gV29ybGQh", "color" : "RED" }
{ "index": { "_index": "my-index", "_id": "2" } }
{ "my_binary": "ay1OTiBjdXN0b20gc2NvcmluZyE=", "color" : "RED" }
{ "index": { "_index": "my-index", "_id": "3" } }
{ "my_binary": "V2VsY29tZSB0byBrLU5O", "color" : "RED" }
{ "index": { "_index": "my-index", "_id": "4" } }
{ "my_binary": "SSBob3BlIHRoaXMgaXMgaGVscGZ1bA==", "color" : "BLUE" }
{ "index": { "_index": "my-index", "_id": "5" } }
{ "my_binary": "QSBjb3VwbGUgbW9yZSBkb2NzLi4u", "color" : "BLUE" }
{ "index": { "_index": "my-index", "_id": "6" } }
{ "my_binary":  "TGFzdCBvbmUh", "color" : "BLUE" }
```
{% include copy-curl.html %}

最後，使用 `script_score` 查詢先篩選您的文件，再找出最近鄰：

```json
GET my-index/_search
{
  "size": 2,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "term": {
              "color": "BLUE"
            }
          }
        }
      },
      "script": {
        "lang": "knn",
        "source": "knn_score",
        "params": {
          "field": "my_binary",
          "query_value": "U29tZXRoaW5nIEltIGxvb2tpbmcgZm9y",
          "space_type": "hammingbit"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

同樣地，您可以使用 `long` 欄位編碼資料並執行搜尋：

```json
GET my-long-index/_search
{
  "size": 2,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "term": {
              "color": "BLUE"
            }
          }
        }
      },
      "script": {
        "lang": "knn",
        "source": "knn_score",
        "params": {
          "field": "my_long",
          "query_value": 23,
          "space_type": "hammingbit"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

