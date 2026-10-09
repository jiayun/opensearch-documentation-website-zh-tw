---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記憶體最佳化向量"
parent: k-NN vector
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/knn-memory-optimized/
nav_order: 30
---

# 記憶體最佳化向量

向量搜尋作業可能相當耗用記憶體，尤其是在處理大規模部署時。OpenSearch 提供多種策略，可在維持搜尋效能的同時最佳化記憶體使用量。您可以選擇以低延遲或低成本為優先的不同工作負載模式、套用各種壓縮層級以減少記憶體佔用量，或使用位元組向量或二進位向量等替代向量表示法。這些最佳化技術可讓您根據特定使用案例需求，在記憶體耗用量、搜尋效能與成本之間取得平衡。

## 向量工作負載模式

向量搜尋需要在搜尋效能與營運成本之間取得平衡。記憶體內搜尋可提供最低延遲，而[磁碟式搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)則透過減少記憶體使用量提供更具成本效益的方法，但會導致搜尋延遲略微提高。若要在這些方法之間選擇，請在您的 `knn_vector` 欄位組態中使用 `mode` 對應參數。此參數會根據您的優先順序 (低延遲或低成本)，為 k-NN 參數設定適當的預設值。如需進一步最佳化，您可以在 k-NN 欄位對應中覆寫這些預設參數值。

OpenSearch 支援下列向量工作負載模式。

| 模式    | 預設引擎 | 說明                                                                                                                                                                                                                                             |
|:---|:---|:---|
| `in_memory` (預設) | `faiss`        | 以低延遲搜尋為優先。此模式使用 `faiss` 引擎，且不套用任何量化。其設定為 OpenSearch 中向量搜尋的預設參數值。                                                                 |
| `on_disk`             | `faiss`        | 以低成本向量搜尋為優先，同時維持良好的召回率。根據預設，`on_disk` 模式會使用量化與重新評分來執行兩階段方法，以擷取最相近的鄰居。`on_disk` 模式僅支援 `float` 與 `half_float` 向量類型。 |

若要建立使用 `on_disk` 模式進行低成本搜尋的向量索引，請傳送下列請求：

```json
PUT test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "mode": "on_disk"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 壓縮層級

`compression_level` 對應參數會選取量化編碼器，以指定的倍數減少向量記憶體耗用量。壓縮倍數是相對於向量資料類型的儲存大小來衡量：`float` 向量為每維度 32 位元，`half_float` 向量為每維度 16 位元。因此，相同的 `compression_level` 值會對每種資料類型套用不同的量化。下表列出可用的 `compression_level` 值、支援這些值的引擎與資料類型，以及各自套用的量化。

| 壓縮層級 | 支援的引擎                            | `float` 向量的量化 | `half_float` 向量的量化 |
|:------------------|:---------------------------------------------|:---------------------------------|:--------------------------------------|
| `1x`              | `faiss`、`lucene` 及 `nmslib` (已棄用) | 無 (32 位元儲存)            | 無 (16 位元 FP16 儲存)；僅限 `faiss` 與 `lucene` |
| `2x`              | `faiss`                                      | 16 位元                           | 不支援                         |
| `4x`              | `lucene`                                     | 7 位元                            | 不支援                         |
| `8x`              | `faiss` 與 `lucene`                         | 4 位元                            | 不支援                         |
| `16x`             | `faiss` 與 `lucene`                         | 2 位元                            | 1 位元                                 |
| `32x`             | `faiss` 與 `lucene`                         | 1 位元                            | 不支援                         |

例如，若為 768 維向量的 `float32` 索引傳入 `32x` 的 `compression_level`，則每個向量的記憶體會從 `4 * 768 = 3072` 位元組減少為 `3072 / 32 = 96` 位元組。在內部，可能會使用二進位量化 (將 `float` 對應至 `bit`) 來達成此壓縮。

如果您設定了 `compression_level` 參數，就無法在 `method` 對應中指定 `encoder`。`compression_level` 參數僅支援 `float` 與 [`half_float`](#half-float-vectors) 向量。對於 `half_float` 向量，壓縮層級是相對於其 16 位元基準來衡量。
{: .note}

啟用 `on_disk` 模式並搭配 `1x` 壓縮層級，即會啟用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)。在此模式中，引擎會在搜尋期間視需要載入資料，而不是一次將所有資料載入記憶體。
{: .important}

下表列出可用工作負載模式的預設 `compression_level` 值。對於這兩種資料類型，`on_disk` 預設會套用 1 位元量化；層級不同是因為壓縮倍數是相對於資料類型的儲存大小來衡量。

| 模式 | `float` 的預設壓縮層級 | `half_float` 的預設壓縮層級 |
|:------------------|:-------------------------------|:-------------------------------|
| `in_memory`       | `1x` | `1x` |
| `on_disk`         | `32x` | `16x` |


若要建立具有 `16x` 的 `compression_level` 的向量欄位，請在對應中指定 `compression_level` 參數。此參數會將 `on_disk` 模式的預設壓縮層級從 `32x` 覆寫為 `16x`，以更大的記憶體佔用量換取更高的召回率與準確度：

```json
PUT test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "mode": "on_disk",
        "compression_level": "16x"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 將量化結果重新評分至完整精確度

若要在維持量化所節省的記憶體之餘改善召回率，您可以使用兩階段搜尋方法。在第一階段，會使用量化向量從索引擷取 `oversample_factor * k` 筆結果，並近似計算分數。在第二階段，會從磁碟將這些 `oversample_factor * k` 筆結果的完整精確度向量載入記憶體，並針對完整精確度的查詢向量重新計算分數。接著再將結果縮減為前 k 筆。

預設的重新評分行為取決於後端 k-NN 向量欄位的 `mode` 與 `compression_level`：

- 對於 `in_memory` 模式，預設不會套用重新評分。
- 對於 `on_disk` 模式，預設重新評分會以設定的 `compression_level` 為依據。每個 `compression_level` 都會提供預設的 `oversample_factor`，如下表所示。

| 壓縮層級 | 預設重新評分 `oversample_factor` |
|:------------------|:------------------------------------|
| `32x` (預設)   | 2.0                                 |
| `16x`             | 1.0                                 |
| `8x`              | 1.0                                 |
| `4x`              | 1.0                                 |
| `2x`              | 無預設重新評分                |

若要明確套用重新評分，請在量化索引的查詢中提供 `rescore` 參數，並指定 `oversample_factor`：

```json
GET /my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "target-field": {
        "vector": [2, 3, 5, 6],
        "k": 2,
        "rescore" : {
          "oversample_factor": 1.2
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，將 `rescore` 參數設為 `true`，以使用 `1.0` 的預設 `oversample_factor`：

```json
GET /my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "target-field": {
        "vector": [2, 3, 5, 6],
        "k": 2,
        "rescore" : true
      }
    }
  }
}
```
{% include copy-curl.html %}

`oversample_factor` 是介於 1.0 與 100.0 (含) 之間的浮點數。第一階段傳回的結果數目計算方式為 `oversample_factor * k`，並保證介於 100 與 10,000 (含) 之間。如果計算出的結果數目小於 100，則結果數目會設為 100。如果計算出的結果數目大於 10,000，則結果數目會設為 10,000。

重新評分僅適用於 Faiss 與 Lucene 引擎。
{: .note}

如果未使用量化，則不需要重新評分，因為傳回的分數已經是完整精確度。
{: .note}


## 半浮點數向量
**3.9 版新增**
{: .label .label-purple }

預設情況下，k-NN 向量是 `float` 向量，每個維度佔 4 位元組。如果您想將記憶體與儲存需求減半，可以使用 `half_float` 向量。在 `half_float` 向量中，每個維度是一個 16 位元浮點數 (FP16) 值，範圍為 [-65504.0, 65504.0]。如果任何向量值超出此範圍，請求將被拒絕。

若要使用 `half_float` 向量，請在為索引建立對應時，將 `data_type` 參數設為 `half_float`。`half_float` 向量的匯入與查詢方式與 `float` 向量相同；OpenSearch 會以 FP16 格式原生儲存這些向量。

半浮點數向量支援搭配 `faiss` 或 `lucene` 引擎的 `hnsw` 方法，以及搭配 `flat` 方法的[使用純量量化進行精確搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/exact-search-scalar-quantization/)。上述每種組態都支援 `1x` 與 `16x` 壓縮層級。

半浮點數向量不支援 `nmslib` 引擎、`ivf` 方法或[已訓練模型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/#model-ids)。
{: .note}

由於向量已經是 16 位元，`half_float` 欄位在 `method` 對應中不接受 `encoder`。若要套用量化，請改用 `compression_level` 對應參數。壓縮層級是以 `half_float` 向量的 16 位元基準來衡量：

- `1x` 將向量儲存為未量化的 FP16 值，每個維度使用 2 位元組。
- `16x` 套用 1 位元純量量化，將每個維度對應到單一位元。

### 範例：HNSW

下列範例使用 `faiss` 引擎與 `hnsw` 演算法建立半浮點數向量索引：

```json
PUT test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "data_type": "half_float",
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 記憶體估算

半浮點數向量所需的記憶體是 `float` 向量的一半。HNSW 所需的記憶體可估算為 `1.1 * (2 * dimension + 8 * m)` 位元組/向量，其中 `m` 是圖形建構期間為每個元素建立的最大雙向連結數。

舉例來說，假設您有 100 萬個半浮點數向量，`dimension` 為 `256`，`m` 為 `16`。記憶體需求可估算如下：

```r
1.1 * (2 * 256 + 8 * 16) * 1,000,000 ~= 0.656 GB
```

## 位元組向量

預設情況下，k-NN 向量是 `float` 向量，每個維度佔 4 位元組。如果您想節省儲存空間，可以搭配 `faiss` 或 `lucene` 引擎使用 `byte` 向量。在 `byte` 向量中，每個維度是一個範圍為 [-128, 127] 的帶正負號 8 位元整數。
 
位元組向量僅支援 `lucene` 與 `faiss` 引擎，不支援 `nmslib` 引擎。
{: .note}

在 [k-NN 基準測試](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/vectorsearch)中，使用 `byte` 而非 `float` 向量可大幅降低儲存與記憶體用量，同時提升索引處理吞吐量並降低查詢延遲。此外，召回精確度並未受到太大影響（請注意，召回率可能取決於多種因素，例如所使用的[量化技術](#quantization-techniques)與資料分佈）。

使用 `byte` 向量時，與使用 `float` 向量相比，預期會有一些召回精確度的損失。位元組向量適用於大規模應用程式，以及優先考慮以極小召回損失換取較低記憶體佔用量的使用情境。
{: .important}

搭配 `faiss` 引擎使用 `byte` 向量時，我們建議使用[單指令多資料 (SIMD) 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)，這有助於大幅降低搜尋延遲並提升索引處理吞吐量。
{: .important} 

k-NN 外掛程式 2.9 版新增了選用的 `data_type` 參數，用於定義向量的資料類型。此參數的預設值為 `float`。

若要使用 `byte` 向量，請在為索引建立對應時，將 `data_type` 參數設為 `byte`。

### 範例：HNSW

下列範例使用 `lucene` 引擎與 `hnsw` 演算法建立位元組向量索引：

```json
PUT test-index
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "data_type": "byte",
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
```
{% include copy-curl.html %}

建立索引後，照常匯入文件。請確定向量的每個維度都在支援的 [-128, 127] 範圍內：

```json
PUT test-index/_doc/1
{
  "my_vector": [-126, 28, 127]
}
```
{% include copy-curl.html %}

```json
PUT test-index/_doc/2
{
  "my_vector": [100, -128, 0]
}
```
{% include copy-curl.html %}

查詢時，請務必使用 `byte` 向量：

```json
GET test-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [26, -120, 99],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

### 範例：IVF

`ivf` 方法需要一個訓練步驟，以建立模型並加以訓練，從而在建立分段時初始化原生程式庫索引。如需更多資訊，請參閱[從模型建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/#building-a-vector-index-from-a-model)。

首先，建立一個將包含位元組向量訓練資料的索引。指定 `faiss` 引擎與 `ivf` 演算法，並確保 `dimension` 與您要建立的模型維度相符：

```json
PUT train-index
{
  "mappings": {
    "properties": {
      "train-field": {
        "type": "knn_vector",
        "dimension": 4,
        "data_type": "byte"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將包含位元組向量的訓練資料匯入訓練索引：

```json
PUT _bulk
{ "index": { "_index": "train-index", "_id": "1" } }
{ "train-field": [127, 100, 0, -120] }
{ "index": { "_index": "train-index", "_id": "2" } }
{ "train-field": [2, -128, -10, 50] }
{ "index": { "_index": "train-index", "_id": "3" } }
{ "train-field": [13, -100, 5, 126] }
{ "index": { "_index": "train-index", "_id": "4" } }
{ "train-field": [5, 100, -6, -125] }
```
{% include copy-curl.html %}

然後，建立並訓練名為 `byte-vector-model` 的模型。模型將使用 `train-index` 中 `train-field` 的訓練資料進行訓練。請指定 `byte` 資料類型：

```json
POST _plugins/_knn/models/byte-vector-model/_train
{
  "training_index": "train-index",
  "training_field": "train-field",
  "dimension": 4,
  "description": "model with byte data",
  "data_type": "byte",
  "method": {
    "name": "ivf",
    "engine": "faiss",
    "space_type": "l2",
    "parameters": {
      "nlist": 1,
      "nprobes": 1
    }
  }
}
```
{% include copy-curl.html %}

若要檢查模型訓練狀態，請呼叫 Get Model API：

```json
GET _plugins/_knn/models/byte-vector-model?filter_path=state
```
{% include copy-curl.html %}

訓練完成後，`state` 會變更為 `created`。

接下來，建立一個索引，使用已訓練的模型來初始化其原生程式庫索引：

```json
PUT test-byte-ivf
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "model_id": "byte-vector-model"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含您要搜尋之位元組向量的資料匯入已建立的索引：

```json
PUT _bulk?refresh=true
{"index": {"_index": "test-byte-ivf", "_id": "1"}}
{"my_vector": [7, 10, 15, -120]}
{"index": {"_index": "test-byte-ivf", "_id": "2"}}
{"my_vector": [10, -100, 120, -108]}
{"index": {"_index": "test-byte-ivf", "_id": "3"}}
{"my_vector": [1, -2, 5, -50]}
{"index": {"_index": "test-byte-ivf", "_id": "4"}}
{"my_vector": [9, -7, 45, -78]}
{"index": {"_index": "test-byte-ivf", "_id": "5"}}
{"my_vector": [80, -70, 127, -128]}
```
{% include copy-curl.html %}

最後，搜尋資料。請務必在 k-NN 向量欄位中提供位元組向量：

```json
GET test-byte-ivf/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [100, -120, 50, -45],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

### 記憶體估算

在最佳情況下，位元組向量所需的記憶體為 32 位元向量所需記憶體的 25%。

#### HNSW 記憶體估算

階層式可導覽小世界 (Hierarchical Navigable Small World，HNSW) 所需的記憶體估計為每個向量 `1.1 * (dimension + 8 * m)` 位元組，其中 `m` 是在建構圖形期間為每個元素建立的最大雙向連結數。

舉例來說，假設您有 100 萬個向量，`dimension` 為 `256`，且 `m` 為 `16`。記憶體需求可估算如下：

```r
1.1 * (256 + 8 * 16) * 1,000,000 ~= 0.39 GB
```

#### IVF 記憶體估算

倒排檔案索引 (Inverted File Index，IVF) 所需的記憶體估計為每個向量 `1.1 * ((dimension * num_vectors) + (4 * nlist * dimension))` 位元組，其中 `nlist` 是要將向量分割成的桶數。

舉例來說，假設您有 100 萬個向量，`dimension` 為 `256`，且 `nlist` 為 `128`。記憶體需求可估算如下：

```r
1.1 * ((256 * 1,000,000) + (4 * 128 * 256))  ~= 0.27 GB
```


### 量化技術

如果您的向量類型為 `float`，您必須先將其轉換為 `byte` 類型，再匯入文件。此轉換是透過_量化資料集_來完成——降低其向量的精確度。Faiss 引擎支援多種量化技術，例如純量量化 (SQ) 與乘積量化 (PQ)。量化技術的選擇取決於您使用的資料類型，並可能影響召回值的準確度。下列各節說明用於量化 [k-NN 基準測試](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/vectorsearch)資料 (針對 [L2](#scalar-quantization-for-the-l2-space-type) 與 [餘弦相似度](#scalar-quantization-for-the-cosine-similarity-space-type) 空間類型) 的純量量化演算法。所提供的虛擬碼僅供說明之用。

#### L2 空間類型的純量量化

下列範例虛擬碼說明用於 L2 空間類型歐幾里得資料集基準測試的純量量化技術。歐幾里得距離具有平移不變性。如果您將 $$x$$ 與 $$y$$ 同時平移相同的 $$z$$，則距離保持不變 ($$\lVert x-y\rVert =\lVert (x-z)-(y-z)\rVert$$)。

```python
# Random dataset (Example to create a random dataset)
dataset = np.random.uniform(-300, 300, (100, 10))
# Random query set (Example to create a random queryset)
queryset = np.random.uniform(-350, 350, (100, 10))
# Number of values
B = 256

# INDEXING:
# Get min and max
dataset_min = np.min(dataset)
dataset_max = np.max(dataset)
# Shift coordinates to be non-negative
dataset -= dataset_min
# Normalize into [0, 1]
dataset *= 1. / (dataset_max - dataset_min)
# Bucket into 256 values
dataset = np.floor(dataset * (B - 1)) - int(B / 2)

# QUERYING:
# Clip (if queryset range is out of datset range)
queryset = queryset.clip(dataset_min, dataset_max)
# Shift coordinates to be non-negative
queryset -= dataset_min
# Normalize
queryset *= 1. / (dataset_max - dataset_min)
# Bucket into 256 values
queryset = np.floor(queryset * (B - 1)) - int(B / 2)
```
{% include copy.html %}

#### 餘弦相似度空間類型的純量量化

下列範例虛擬碼說明用於餘弦相似度空間類型角度資料集基準測試的純量量化技術。餘弦相似度不具平移不變性 ($$cos(x, y) \neq cos(x-z, y-z)$$)。

下列虛擬碼適用於正數：

```python
# For Positive Numbers

# INDEXING and QUERYING:

# Get Max of train dataset
max = np.max(dataset)
min = 0
B = 127

# Normalize into [0,1]
val = (val - min) / (max - min)
val = (val * B)

# Get int and fraction values
int_part = floor(val)
frac_part = val - int_part

if 0.5 < frac_part:
 bval = int_part + 1
else:
 bval = int_part

return Byte(bval)
```
{% include copy.html %}

下列虛擬碼適用於負數：

```python
# For Negative Numbers

# INDEXING and QUERYING:

# Get Min of train dataset
min = 0
max = -np.min(dataset)
B = 128

# Normalize into [0,1]
val = (val - min) / (max - min)
val = (val * B)

# Get int and fraction values
int_part = floor(var)
frac_part = val - int_part

if 0.5 < frac_part:
 bval = int_part + 1
else:
 bval = int_part

return Byte(bval)
```
{% include copy.html %}

## 二進位向量

您可以從浮點數向量改用二進位向量，將記憶體成本降低為 32 分之一。使用二進位向量索引可降低營運成本，同時維持高召回效能，讓大規模部署更經濟且有效率。

二進位格式適用於下列 k-NN 搜尋類型：

- [近似 k-NN]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/)：僅支援使用 HNSW 與 IVF 演算法的 Faiss 引擎的二進位向量。
- [指令碼分數 k-NN]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-score-script/)：可在指令碼評分中使用二進位向量。
- [Painless 擴充功能]({{site.url}}{{site.baseurl}}/search-plugins/knn/painless-functions/)：允許搭配 Painless 指令碼擴充功能使用二進位向量。

### 需求

在 OpenSearch k-NN 外掛程式中使用二進位向量有幾項需求：

- 二進位向量索引的 `data_type` 必須為 `binary`。
- 二進位向量索引的 `space_type` 必須為 `hamming`。
- 二進位向量索引的 `dimension` 必須是 8 的倍數。
- 您必須將二進位資料轉換為 [-128, 127] 範圍內的 8 位元帶正負號整數 (`int8`)。例如，8 位元的二進位序列 `0, 1, 1, 0, 0, 0, 1, 1` 必須轉換為其對應的位元組值 `99`，才能做為二進位向量輸入使用。

### 範例：HNSW

若要使用 Faiss 引擎與 HNSW 演算法建立二進位向量索引，請傳送下列請求：

```json
PUT /test-binary-hnsw
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 8,
        "data_type": "binary",
        "space_type": "hamming",
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

接著匯入一些包含二進位向量的文件：

```json
PUT _bulk
{"index": {"_index": "test-binary-hnsw", "_id": "1"}}
{"my_vector": [7], "price": 4.4}
{"index": {"_index": "test-binary-hnsw", "_id": "2"}}
{"my_vector": [10], "price": 14.2}
{"index": {"_index": "test-binary-hnsw", "_id": "3"}}
{"my_vector": [15], "price": 19.1}
{"index": {"_index": "test-binary-hnsw", "_id": "4"}}
{"my_vector": [99], "price": 1.2}
{"index": {"_index": "test-binary-hnsw", "_id": "5"}}
{"my_vector": [80], "price": 16.5}
```
{% include copy-curl.html %}

查詢時，請務必使用二進位向量：

```json
GET /test-binary-hnsw/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [9],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含最接近查詢向量的兩個向量：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 8,
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
    "max_score": 0.5,
    "hits": [
      {
        "_index": "test-binary-hnsw",
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "my_vector": [
            10
          ],
          "price": 14.2
        }
      },
      {
        "_index": "test-binary-hnsw",
        "_id": "5",
        "_score": 0.25,
        "_source": {
          "my_vector": [
            80
          ],
          "price": 16.5
        }
      }
    ]
  }
}
```
</details>

### 範例：IVF

IVF 方法需要一個訓練步驟，以建立模型並訓練模型，以便在建立分段時初始化原生程式庫索引。如需更多資訊，請參閱[從模型建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/#building-a-vector-index-from-a-model)。

首先，建立一個將包含二進位向量訓練資料的索引。指定 Faiss 引擎與 IVF 演算法，並確保 `dimension` 與您要建立的模型維度相符：

```json
PUT train-index
{
  "mappings": {
    "properties": {
      "train-field": {
        "type": "knn_vector",
        "dimension": 8,
        "data_type": "binary"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含二進位向量的訓練資料匯入訓練索引：

<details markdown="block">
<summary>
    批次匯入請求
</summary>
{: .text-delta}

```json
PUT _bulk
{ "index": { "_index": "train-index", "_id": "1" } }
{ "train-field": [1] }
{ "index": { "_index": "train-index", "_id": "2" } }
{ "train-field": [2] }
{ "index": { "_index": "train-index", "_id": "3" } }
{ "train-field": [3] }
{ "index": { "_index": "train-index", "_id": "4" } }
{ "train-field": [4] }
{ "index": { "_index": "train-index", "_id": "5" } }
{ "train-field": [5] }
{ "index": { "_index": "train-index", "_id": "6" } }
{ "train-field": [6] }
{ "index": { "_index": "train-index", "_id": "7" } }
{ "train-field": [7] }
{ "index": { "_index": "train-index", "_id": "8" } }
{ "train-field": [8] }
{ "index": { "_index": "train-index", "_id": "9" } }
{ "train-field": [9] }
{ "index": { "_index": "train-index", "_id": "10" } }
{ "train-field": [10] }
{ "index": { "_index": "train-index", "_id": "11" } }
{ "train-field": [11] }
{ "index": { "_index": "train-index", "_id": "12" } }
{ "train-field": [12] }
{ "index": { "_index": "train-index", "_id": "13" } }
{ "train-field": [13] }
{ "index": { "_index": "train-index", "_id": "14" } }
{ "train-field": [14] }
{ "index": { "_index": "train-index", "_id": "15" } }
{ "train-field": [15] }
{ "index": { "_index": "train-index", "_id": "16" } }
{ "train-field": [16] }
{ "index": { "_index": "train-index", "_id": "17" } }
{ "train-field": [17] }
{ "index": { "_index": "train-index", "_id": "18" } }
{ "train-field": [18] }
{ "index": { "_index": "train-index", "_id": "19" } }
{ "train-field": [19] }
{ "index": { "_index": "train-index", "_id": "20" } }
{ "train-field": [20] }
{ "index": { "_index": "train-index", "_id": "21" } }
{ "train-field": [21] }
{ "index": { "_index": "train-index", "_id": "22" } }
{ "train-field": [22] }
{ "index": { "_index": "train-index", "_id": "23" } }
{ "train-field": [23] }
{ "index": { "_index": "train-index", "_id": "24" } }
{ "train-field": [24] }
{ "index": { "_index": "train-index", "_id": "25" } }
{ "train-field": [25] }
{ "index": { "_index": "train-index", "_id": "26" } }
{ "train-field": [26] }
{ "index": { "_index": "train-index", "_id": "27" } }
{ "train-field": [27] }
{ "index": { "_index": "train-index", "_id": "28" } }
{ "train-field": [28] }
{ "index": { "_index": "train-index", "_id": "29" } }
{ "train-field": [29] }
{ "index": { "_index": "train-index", "_id": "30" } }
{ "train-field": [30] }
{ "index": { "_index": "train-index", "_id": "31" } }
{ "train-field": [31] }
{ "index": { "_index": "train-index", "_id": "32" } }
{ "train-field": [32] }
{ "index": { "_index": "train-index", "_id": "33" } }
{ "train-field": [33] }
{ "index": { "_index": "train-index", "_id": "34" } }
{ "train-field": [34] }
{ "index": { "_index": "train-index", "_id": "35" } }
{ "train-field": [35] }
{ "index": { "_index": "train-index", "_id": "36" } }
{ "train-field": [36] }
{ "index": { "_index": "train-index", "_id": "37" } }
{ "train-field": [37] }
{ "index": { "_index": "train-index", "_id": "38" } }
{ "train-field": [38] }
{ "index": { "_index": "train-index", "_id": "39" } }
{ "train-field": [39] }
{ "index": { "_index": "train-index", "_id": "40" } }
{ "train-field": [40] }
```
{% include copy-curl.html %}
</details>

接著，建立並訓練名為 `test-binary-model` 的模型。模型將使用 `train-index` 中 `train_field` 的訓練資料進行訓練。請指定 `binary` 資料類型與 `hamming` 空間類型：

```json
POST _plugins/_knn/models/test-binary-model/_train
{
  "training_index": "train-index",
  "training_field": "train-field",
  "dimension": 8,
  "description": "model with binary data",
  "data_type": "binary",
  "space_type": "hamming",
  "method": {
    "name": "ivf",
    "engine": "faiss",
    "parameters": {
      "nlist": 16,
      "nprobes": 1
    }
  }
}
```
{% include copy-curl.html %}

若要檢查模型訓練狀態，請呼叫 Get Model API：

```json
GET _plugins/_knn/models/test-binary-model?filter_path=state
```
{% include copy-curl.html %}

訓練完成後，`state` 會變更為 `created`。

接下來，建立一個將使用已訓練模型來初始化其原生程式庫索引的索引：

```json
PUT test-binary-ivf
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "model_id": "test-binary-model"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含您要搜尋之二進位向量的資料匯入已建立的索引：

```json
PUT _bulk?refresh=true
{"index": {"_index": "test-binary-ivf", "_id": "1"}}
{"my_vector": [7], "price": 4.4}
{"index": {"_index": "test-binary-ivf", "_id": "2"}}
{"my_vector": [10], "price": 14.2}
{"index": {"_index": "test-binary-ivf", "_id": "3"}}
{"my_vector": [15], "price": 19.1}
{"index": {"_index": "test-binary-ivf", "_id": "4"}}
{"my_vector": [99], "price": 1.2}
{"index": {"_index": "test-binary-ivf", "_id": "5"}}
{"my_vector": [80], "price": 16.5}
```
{% include copy-curl.html %}

最後，搜尋資料。請務必在 k-NN 向量欄位中提供二進位向量：

```json
GET test-binary-ivf/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [8],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含與查詢向量最接近的兩個向量：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
GET /_plugins/_knn/models/my-model?filter_path=state
{
  "took": 7,
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
    "max_score": 0.5,
    "hits": [
      {
        "_index": "test-binary-ivf",
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "my_vector": [
            10
          ],
          "price": 14.2
        }
      },
      {
        "_index": "test-binary-ivf",
        "_id": "3",
        "_score": 0.25,
        "_source": {
          "my_vector": [
            15
          ],
          "price": 19.1
        }
      }
    ]
  }
}
```
</details>

### 記憶體估算

使用下列公式來估算二進位向量所需的記憶體量。

#### HNSW 記憶體估算

HNSW 所需的記憶體可使用下列公式估算，其中 `m` 是在建構圖形時為每個元素建立的最大雙向連結數：

```r
1.1 * (dimension / 8 + 8 * m) bytes/vector
```

#### IVF 記憶體估算

IVF 所需的記憶體可使用下列公式估算，其中 `nlist` 是要將向量分割成的桶數：

```r
1.1 * (((dimension / 8) * num_vectors) + (nlist * dimension / 8))
```

## 後續步驟

- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
- [磁碟式向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)
- [向量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/)
