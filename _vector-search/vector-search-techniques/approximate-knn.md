---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "近似 k-NN 搜尋"
nav_order: 15
parent: Vector search techniques
has_children: false
has_math: true
redirect_from:
  - /search-plugins/knn/approximate-knn/ 
---

# 近似 k-NN 搜尋

標準的 k 最近鄰 (k-NN) 搜尋方法使用暴力法計算相似度，衡量查詢與多個點之間的最近距離，產生精確的結果。這在許多應用中運作良好。然而，在具有高維度的極大型資料集情況下，這會產生擴展性問題，降低搜尋效率。近似 k-NN 搜尋方法可透過採用能更有效率地重建索引結構並降低可搜尋向量維度的工具來克服此問題。使用此方法需要犧牲準確度，但能明顯提升搜尋處理速度。

OpenSearch 中的近似 k-NN 搜尋方法使用來自 [NMSLIB](https://github.com/nmslib/nmslib)、[Faiss](https://github.com/facebookresearch/faiss) 和 [Lucene](https://lucene.apache.org/) 函式庫的近似最近鄰 (ANN) 演算法來支援 k-NN 搜尋。這些搜尋方法採用 ANN 來改善大型資料集的搜尋延遲。在 OpenSearch 提供的三種搜尋方法中，此方法為大型資料集提供最佳的搜尋擴展性。當資料集達到數十萬個向量時，此方法為首選方法。

[`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/) 為近似 k-NN 搜尋提供額外的 `jvector` 引擎，以純 Java 實作 DiskANN 風格的索引編製。此引擎支援執行緒安全的並行匯入、無需完整重建圖形的增量索引更新，以及原生乘積量化 (PQ)。當您的資料集持續成長，或資料集大於可用記憶體且您需要在高壓縮率下達到高召回率時，請考慮使用 `jvector`。

如需 OpenSearch 支援的演算法相關資訊，請參閱[方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。
{: .note}

OpenSearch 在索引編製期間為每個 `knn-vector` 欄位/Lucene 分段配對建立向量的原生函式庫索引，可用於在搜尋期間有效率地找出查詢向量的 k 個最近鄰。如需進一步了解 Lucene 分段，請參閱 [Apache Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/codecs/lucene104/package-summary.html#package.description)。這些原生函式庫索引會在搜尋期間載入原生記憶體，並由快取管理。如需進一步了解如何將原生函式庫索引預先載入記憶體，請參閱 [Warmup API]({{site.url}}{{site.baseurl}}/vector-search/api/knn#warmup-operation)。此外，您可以使用 [Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/knn#stats) 查看哪些原生函式庫索引已載入記憶體。

由於原生函式庫索引是在索引編製期間建構，因此無法在索引上套用篩選器後再使用此搜尋方法。所有篩選器都會套用至 ANN 搜尋產生的結果。

## 開始使用近似 k-NN

若要使用近似搜尋功能，您必須先建立向量索引，並將 `index.knn` 設為 `true`。此設定會告訴 OpenSearch 為該索引建立原生函式庫索引。

接著，您必須新增一或多個 `knn_vector` 資料類型的欄位。下列範例使用 `faiss` 引擎建立具有兩個 `knn_vector` 欄位的索引：

```json
PUT my-knn-index-1
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
        "my_vector1": {
          "type": "knn_vector",
          "dimension": 2,
          "space_type": "l2",
          "method": {
            "name": "hnsw",
            "engine": "faiss",
            "parameters": {
              "ef_construction": 128,
              "m": 24
            }
          }
        },
        "my_vector2": {
          "type": "knn_vector",
          "dimension": 4,
          "space_type": "innerproduct",
          "method": {
            "name": "hnsw",
            "engine": "faiss",
            "parameters": {
              "ef_construction": 256,
              "m": 48
            }
          }
        }
    }
  }
}
```
{% include copy-curl.html %}

在上述範例中，兩個 `knn_vector` 欄位都是使用方法定義進行設定。此外，`knn_vector` 欄位也可以使用模型進行設定。如需更多資訊，請參閱 [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)。

`knn_vector` 資料類型支援浮點數向量，對於 NMSLIB、Faiss 和 Lucene 引擎，其維度計數最高可達 16,000，由 `dimension` 對應參數設定。

在 OpenSearch 中，編解碼器負責處理索引的儲存與擷取。OpenSearch 使用自訂編解碼器將向量資料寫入原生函式庫索引，以便基礎的 k-NN 搜尋函式庫能夠讀取。
{: .tip }

建立索引後，您可以新增一些資料至其中：

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

接著您可以使用 `knn` 查詢類型對資料執行 ANN 搜尋：

```json
GET my-knn-index-1/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector2": {
        "vector": [2, 3, 5, 6],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

## 傳回的結果數量

在上述查詢中，`k` 代表每個圖形搜尋所傳回的鄰居數量。您也必須包含 `size` 參數，指出您希望查詢傳回的最終結果數量。  

對於 NMSLIB 和 Faiss 引擎，`k` 代表分片所有分段所傳回的文件數量上限。對於 Lucene 引擎，`k` 代表分片所傳回的文件數量。`k` 的最大值為 10,000。

對於任何引擎，每個分片都會將 `size` 個結果傳回協調節點。因此，協調節點接收的結果總數為 `size * number of shards`。協調節點彙整從所有節點接收的結果後，查詢會傳回前 `size` 個結果。

下表提供各種引擎在幾種情境下所傳回結果數量的範例。在這些範例中，假設分段和分片中所包含的文件數量足以傳回表中指定的結果數量。

`size` 	| `k` | 主要分片數量 | 	每個分片的分段數量 | 傳回的結果數量，Faiss/NMSLIB | 傳回的結果數量，Lucene
:--- | :--- | :--- | :--- | :--- | :---
10 |	1 |	1 |	4 |	4 | 1
10 | 10 |	1 |	4 |	10 | 10
10 |	1 |	2 |	4 |	8 | 2

只有在 `k` 小於 `size` 時，Faiss/NMSLIB 傳回的結果數量才會與 Lucene 傳回的結果數量不同。如果 `k` 和 `size` 相等，所有引擎都會傳回相同數量的結果。 

您可以將 `k`、`min_score` 或 `max_distance` 用於[徑向搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/radial-search-knn/)。

## 從模型建立向量索引

對於 OpenSearch 支援的部分演算法，原生函式庫索引需要先經過訓練才能使用。訓練每個新建立的分段所費不貲，因此，OpenSearch 改以 *模型* 的概念，在建立分段期間初始化原生函式庫索引。您可以呼叫 [Train API]({{site.url}}{{site.baseurl}}/vector-search/api/knn#train-a-model) 並傳入訓練資料的來源和模型的方法定義來建立模型。訓練完成後，模型會序列化至 k-NN 模型系統索引。接著，在索引編製期間，會從該索引提取模型來初始化分段。

若要訓練模型，您首先需要一個包含訓練資料的 OpenSearch 索引。訓練資料可以來自任何 `knn_vector` 欄位，其維度須符合您要建立之模型的維度。訓練資料可以與您打算編製索引的資料相同，或來自個別的資料集。若要建立訓練索引，請傳送下列請求：

```json
PUT /train-index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "train-field": {
        "type": "knn_vector",
        "dimension": 4
      }
    }
  }
}
```
{% include copy-curl.html %}

請注意，索引設定中未設定 `index.knn`。這可確保您不會為此索引建立原生函式庫索引。

您現在可以新增一些資料至索引：

```json
POST _bulk
{ "index": { "_index": "train-index", "_id": "1" } }
{ "train-field": [1.5, 5.5, 4.5, 6.4]}
{ "index": { "_index": "train-index", "_id": "2" } }
{ "train-field": [2.5, 3.5, 5.6, 6.7]}
{ "index": { "_index": "train-index", "_id": "3" } }
{ "train-field": [4.5, 5.5, 6.7, 3.7]}
{ "index": { "_index": "train-index", "_id": "4" } }
{ "train-field": [1.5, 5.5, 4.5, 6.4]}
```
{% include copy-curl.html %}

完成訓練索引的索引編製後，您可以呼叫 Train API：

```json
POST /_plugins/_knn/models/my-model/_train
{
  "training_index": "train-index",
  "training_field": "train-field",
  "dimension": 4,
  "description": "My model description",
  "method": {
    "name": "ivf",
    "engine": "faiss",
    "parameters": {
      "encoder": {
        "name": "pq",
        "parameters": {
          "code_size": 2,
          "m": 2
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如需方法參數的詳細資訊，請參閱 [IVF 訓練需求]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#ivf-training-requirements)。

Train API 會在訓練工作開始後立即傳回。若要檢查工作狀態，請使用 Get Model API：

```json
GET /_plugins/_knn/models/my-model?filter_path=state&pretty
{
  "state": "training"
}
```
{% include copy-curl.html %}

一旦模型進入 `created` 狀態，您就可以建立索引，使用此模型來初始化其原生函式庫索引：

```json
PUT /target-index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "target-field": {
        "type": "knn_vector",
        "model_id": "my-model"
      }
    }
  }
}
```
{% include copy-curl.html %}

最後，您可以將要搜尋的文件新增至索引：

```json
POST _bulk
{ "index": { "_index": "target-index", "_id": "1" } }
{ "target-field": [1.5, 5.5, 4.5, 6.4]}
{ "index": { "_index": "target-index", "_id": "2" } }
{ "target-field": [2.5, 3.5, 5.6, 6.7]}
{ "index": { "_index": "target-index", "_id": "3" } }
{ "target-field": [4.5, 5.5, 6.7, 3.7]}
{ "index": { "_index": "target-index", "_id": "4" } }
{ "target-field": [1.5, 5.5, 4.5, 6.4]}
```
{% include copy-curl.html %}

資料匯入後，即可像任何其他 `knn_vector` 欄位一樣進行搜尋。
