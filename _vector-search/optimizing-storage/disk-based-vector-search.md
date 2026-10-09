---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "磁碟式向量搜尋"
nav_order: 20
parent: Optimizing vector storage
has_children: false
redirect_from:
  - /search-plugins/knn/disk-based-vector-search/
---

# 磁碟式向量搜尋
**於 2.17 版推出**
{: .label .label-purple}

針對低記憶體環境，OpenSearch 提供_磁碟式向量搜尋_，可大幅降低向量工作負載的營運成本。磁碟式向量搜尋支援[純量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/)（預設的量化類型）與[二進位量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/binary-quantization/)，可壓縮向量並降低記憶體需求。這項記憶體最佳化可節省大量記憶體，代價是搜尋延遲略微增加，同時仍維持良好的召回率。

若要使用磁碟式向量搜尋，請為您的向量欄位類型將 [`mode`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#vector-workload-modes) 參數設為 `on_disk`。此參數會將您的索引設定為使用次要儲存空間。如需磁碟式搜尋參數的詳細資訊，請參閱[記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)。

## 建立磁碟式向量搜尋的索引

若要建立磁碟式向量搜尋的索引，請傳送下列請求：

```json
PUT my-vector-index
{
  "settings" : {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "innerproduct",
        "data_type": "float",
        "mode": "on_disk"
      }
    }
  }
}
```
{% include copy-curl.html %}

根據預設，`on_disk` 模式會將索引設定為使用 `faiss` 引擎與 `hnsw` 方法。預設的 [`compression_level`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#compression-levels) 為 `32x`，可將向量所需的記憶體量減少 32 倍。為了維持搜尋召回率，重新評分預設為啟用。對磁碟最佳化索引進行的搜尋分兩個階段執行：先搜尋壓縮後的索引，然後使用從磁碟載入的全精度向量重新評分結果。

若要降低壓縮層級，請在建立索引對應時提供 `compression_level` 參數：

```json
PUT my-vector-index
{
  "settings" : {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "innerproduct",
        "data_type": "float",
        "mode": "on_disk",
        "compression_level": "16x"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需 `compression_level` 參數的詳細資訊，請參閱[壓縮層級]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#compression-levels)。請注意，若使用 `4x` 壓縮，將會使用 `lucene` 引擎。
{: .note}

如果您需要更精細的微調，可以在方法定義中覆寫其他 k-NN 參數。例如，若要提升召回率，請增加 `ef_construction` 參數值：

```json
PUT my-vector-index
{
  "settings" : {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "innerproduct",
        "data_type": "float",
        "mode": "on_disk",
        "method": {
          "params": {
            "ef_construction": 512
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`on_disk` 模式僅適用於 `float` 與 `half_float` 資料類型。
{: .note}

## 匯入

您可以像對一般向量索引一樣，對磁碟最佳化向量索引執行文件匯入。若要大量將多份文件編製索引，請傳送下列請求：

```json
POST _bulk
{ "index": { "_index": "my-vector-index", "_id": "1" } }
{ "my_vector_field": [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5], "price": 12.2 }
{ "index": { "_index": "my-vector-index", "_id": "2" } }
{ "my_vector_field": [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], "price": 7.1 }
{ "index": { "_index": "my-vector-index", "_id": "3" } }
{ "my_vector_field": [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5], "price": 12.9 }
{ "index": { "_index": "my-vector-index", "_id": "4" } }
{ "my_vector_field": [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5], "price": 1.2 }
{ "index": { "_index": "my-vector-index", "_id": "5" } }
{ "my_vector_field": [5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5], "price": 3.7 }
{ "index": { "_index": "my-vector-index", "_id": "6" } }
{ "my_vector_field": [6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5], "price": 10.3 }
{ "index": { "_index": "my-vector-index", "_id": "7" } }
{ "my_vector_field": [7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5], "price": 5.5 }
{ "index": { "_index": "my-vector-index", "_id": "8" } }
{ "my_vector_field": [8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5], "price": 4.4 }
{ "index": { "_index": "my-vector-index", "_id": "9" } }
{ "my_vector_field": [9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5], "price": 8.9 }
```
{% include copy-curl.html %}

## 搜尋

搜尋的執行方式也與其他索引組態相同。主要差異在於，根據預設，重新評分參數的 `oversample_factor` 會設為 `2.0`（除非您覆寫 `compression_level`）。如需詳細資訊，請參閱[將量化結果重新評分至全精度]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)。若要在磁碟最佳化索引上執行向量搜尋，請提供搜尋向量：

```json
GET my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5],
        "k": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

與其他索引組態類似，您可以在搜尋請求中覆寫 k-NN 參數：

```json
GET my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5],
        "k": 5,
        "method_parameters": {
            "ef_search": 512
        },
        "rescore": {
            "oversample_factor": 10.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

[徑向搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/radial-search-knn/)不支援磁碟式向量搜尋。
{: .note}

## 以模型為基礎的索引

對於[以模型為基礎的索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/#building-a-vector-index-from-a-model)，您可以在訓練請求中指定 `on_disk` 參數，方式與建立索引時指定該參數相同。根據預設，`on_disk` 模式會使用 [Faiss IVF 方法]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#ivf-parameters)與 `32x` 的壓縮層級。若要執行訓練 API，請傳送下列請求：

```json
POST /_plugins/_knn/models/test-model/_train
{
    "training_index": "train-index-name",
    "training_field": "train-field-name",
    "dimension": 8,
    "max_training_vector_count": 1200,
    "search_size": 100,
    "description": "My model",
    "space_type": "innerproduct",
    "mode": "on_disk"
}
```
{% include copy-curl.html %}

此命令假設訓練資料已匯入 `train-index-name` 索引。如需詳細資訊，請參閱[從模型建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/#building-a-vector-index-from-a-model)。
{: .note}

您可以像對一般向量索引一樣，為磁碟最佳化索引覆寫 `compression_level`。


## 後續步驟

- [二進位量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/binary-quantization/)
- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)