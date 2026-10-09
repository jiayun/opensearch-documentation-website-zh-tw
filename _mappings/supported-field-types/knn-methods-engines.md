---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "方法與引擎"
parent: k-NN vector
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/knn-methods-engines/
nav_order: 20
---

# 方法與引擎

_方法_ 定義在編製索引時組織向量資料，以及在搜尋時搜尋這些資料所使用的演算法，適用於[近似 k-NN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/approximate-knn/)。

OpenSearch 支援下列方法：

- **Hierarchical Navigable Small World (HNSW)** 會建立向量之間連結的階層式圖形結構。如需此演算法的更多資訊，請參閱[使用階層式可導覽小世界圖進行高效且穩健的近似最近鄰搜尋](https://arxiv.org/abs/1603.09320)。
- **Inverted File Index (IVF)** 會根據分群將向量組織成桶，並在搜尋時僅搜尋其中一部分的桶。

_引擎_ 是實作這些方法的程式庫。不同的引擎可以實作相同的方法，有時會有不同的最佳化方式或特性。例如，HNSW 由所有支援的引擎實作，各自有其優勢。

OpenSearch 支援下列引擎：
- [**Lucene**](#lucene-engine)：原生搜尋程式庫，提供具備高效篩選功能的 HNSW 實作
- [**Faiss**](#faiss-engine) (Facebook AI Similarity Search)：一個功能完整的程式庫，同時實作 HNSW 與 IVF 方法，並提供額外的向量壓縮選項
- [**NMSLIB**](#nmslib-engine-deprecated) (Non-Metric Space Library)：HNSW 的舊版實作（現已棄用）
- [**JVector**](#jvector-engine)：使用 `disk_ann` 方法的 DiskANN 風格搜尋純 Java 實作，支援並行插入、增量合併與原生乘積量化 (PQ)，可透過 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)取得

## 方法定義範例

方法定義包含下列元件：

- 方法名稱 `name`（例如 `hnsw` 或 `ivf`）
- 方法所建構的 `space_type`（例如 `l2` 或 `cosinesimil`）
- 將實作該方法的 `engine`（例如 `faiss` 或 `lucene`）
- 該實作專屬的 `parameters` 對應表

下列範例設定了一個 `hnsw` 方法，使用 `l2` 空間類型、`faiss` 引擎以及方法專屬參數：

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
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": {
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

並非每個方法/引擎組合都支援所有空間。如需支援的空間清單，請參閱特定引擎的章節。
{: .note}

## 共同參數

下列參數為所有方法定義所共用。

對應參數 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`name` | 是 | N/A | 否 | 最近鄰方法。有效值為 `hnsw`、`ivf`、`flat` 與 `disk_ann`。並非每個引擎組合都支援所有方法。如需支援的方法清單，請參閱特定引擎的章節。
`space_type` | 否 | `l2` | 否 | 用於計算向量之間距離的向量空間。有效值為 `l1`、`l2`、`linf`、`cosinesimil`、`innerproduct`、`hamming` 與 `hammingbit`。並非每個方法/引擎組合都支援所有空間。如需支援的空間清單，請參閱特定引擎的章節。注意：此值也可以在對應的最上層指定。如需更多資訊，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。
`engine` | 否 | `faiss`  | 否 | 用於編製索引與搜尋的近似 k-NN 程式庫。有效值為 `faiss`、`lucene`、`nmslib`（已棄用）與 `jvector`（需要 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)）。
`parameters` | 否 | `null` | 否 | 用於最近鄰方法的參數。如需更多資訊，請參閱特定引擎的章節。

## Lucene 引擎

Lucene 引擎直接在 Lucene 內提供向量搜尋的原生實作。它具備高效篩選功能，非常適合較小規模的部署。

### 支援的方法

Lucene 引擎支援下列方法。

方法名稱 | 需要訓練 | 支援的空間 
:--- | :--- |:---
[`hnsw`](#hnsw-parameters) | 否 | `l2`、`cosinesimil`、`innerproduct`（OpenSearch 2.13 及之後版本支援） 
[`flat`](#flat-parameters) | 否 | `l2`、`cosinesimil`、`innerproduct`（OpenSearch 3.6 及之後版本支援） 

#### HNSW 參數

HNSW 方法支援下列參數。

參數名稱 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`ef_construction` | 否 | 100 | 否 | 建立 k-NN 圖形時使用的動態清單大小。數值越高，圖形越精確，但索引速度越慢。<br>注意：Lucene 內部使用 `beam_width` 一詞，但 OpenSearch 文件為求一致使用 `ef_construction`。
`m` | 否 | 16 | 否 | 為每個新元素建立的雙向連結數量。對記憶體消耗影響顯著。請保持在 `2` 與 `100` 之間。<br>注意：Lucene 內部使用 `max_connections` 一詞，但 OpenSearch 文件為求一致使用 `m`。

Lucene 的 HNSW 實作會忽略 `ef_search`，並在搜尋請求中動態將其設定為 "k" 的值。因此使用 Lucene 引擎時，無需為 `ef_search` 設定組態。
{: .note}

在 OpenSearch 2.11 或更早版本建立的索引仍會使用先前的 `ef_construction` 值（`512`）。
{: .note}

### 組態範例

```json
"method": {
    "name": "hnsw",
    "engine": "lucene",
    "parameters": {
        "m": 2048,
        "ef_construction": 245
    }
}
```

#### Flat 參數

`flat` 方法不支援任何方法層級的參數。若要選取套用至向量的純量量化，請在 `knn_vector` 對應上設定 `compression_level` 欄位。`flat` 方法支援 `32x`、`16x` 與 `8x` 壓縮層級，分別對應 1-bit、2-bit 與 4-bit 純量量化。若未指定 `compression_level`，`flat` 預設為 `32x`。

`flat` 方法與引擎無關，不接受 `engine` 參數。在方法層級或 `flat` 方法的欄位層級指定 `engine` 會導致建立索引失敗。在 OpenSearch 3.8 或更早版本建立的索引不受影響。
{: .important}

如需更多資訊，請參閱[使用純量量化進行精確搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/exact-search-scalar-quantization/)。

### 組態範例

```json
"method": {
    "name": "flat"
}
```

## Faiss 引擎

Faiss 引擎提供進階的向量索引功能，支援多種方法與編碼選項，以最佳化記憶體使用量與搜尋效能。

### 支援的方法

Faiss 引擎支援下列方法。

方法名稱 | 需要訓練 | 支援的空間
:--- | :--- |:---
[`hnsw`](#hnsw-parameters-1) | 否 | `l2`、`innerproduct` (使用 [PQ](#pq-parameters) 時無法使用)、`hamming`，以及 `cosinesimil` (支援於 OpenSearch 2.19 及更新版本)。
[`ivf`](#ivf-parameters) | 是 | `l2`、`innerproduct`、`hamming` (支援於 OpenSearch 2.16 版及更新版本的二進位向量。如需更多資訊，請參閱[二進位 k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized#binary-vectors))、`cosinesimil` (支援於 OpenSearch 2.19 及更新版本)。

在 Faiss 引擎中使用 `cosinesimil` 時，向量會在編製索引期間自動正規化為單位長度，因為 Faiss 在內部會對正規化向量使用內積。因此，儲存的向量值會與輸入值不同。
{: .important}

#### HNSW 參數

`hnsw` 方法支援下列參數。

參數名稱 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`ef_search` | 否 | 100 | 否 | k-NN 搜尋期間使用的動態清單大小。較高的值可獲得更準確但較慢的搜尋。對於[二進位索引]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/binary-quantization/)，預設值為 `256`。
`ef_construction` | 否 | 100 | 否 | 建立 k-NN 圖形期間使用的動態清單大小。較高的值可獲得更準確的圖形，但會降低編製索引速度。對於[二進位索引]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/binary-quantization/)，預設值為 `256`。
`m` | 否 | 16 | 否 | 此外掛程式為每個新元素建立的雙向連結數目。增加及減少此值可能會對記憶體耗用量造成很大的影響。請將此值保持在 `2` 與 `100` 之間。
`encoder` | 否 | flat | 否 | 用於編碼向量的編碼器定義。編碼器可減少索引的記憶體佔用量，但會犧牲搜尋準確度。

在 OpenSearch 2.11 版或更早版本中建立的索引仍會使用先前的 `ef_construction` 值 (`512`)。
{: .note}

#### IVF 參數

IVF 方法支援下列參數。

參數名稱 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`nlist` | 否 | 4 | 否 | 要將向量分割成的桶數。較高的值可能會提高準確度，但也會增加記憶體和訓練延遲。
`nprobes` | 否 | 1 | 否 | 查詢期間要搜尋的桶數。較高的值可獲得更準確但較慢的搜尋。
`encoder` | 否 | flat | 否 | 用於編碼向量的編碼器定義。

如需這些參數的詳細資訊，請參閱 [Faiss 文件](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)。

### IVF 訓練需求

IVF 演算法需要訓練步驟。若要建立使用 IVF 的索引，您需要使用 [Train API]({{site.url}}{{site.baseurl}}/vector-search/api/knn#train-a-model) 訓練模型，並傳入 IVF 方法定義。IVF 至少需要 `nlist` 個訓練資料點，但我們建議[使用更多資料點](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index#how-big-is-the-dataset)。訓練資料可以與您計劃編製索引的資料相同，也可以來自個別的資料集。

### 支援的編碼器

您可以使用編碼器來減少向量索引的記憶體佔用量，但會犧牲搜尋準確度。

OpenSearch 在 Faiss 程式庫中支援下列編碼器。

編碼器名稱 | 需要訓練 | 說明
:--- | :--- | :---
`flat` (預設) | 否 | 將向量編碼為浮點數陣列。此編碼方式不會減少記憶體佔用量。
[`pq`](#pq-parameters) | 是 | _product quantization_ (乘積量化) 的縮寫，PQ 是一種有損壓縮技術，使用叢集將向量編碼為固定的位元組大小，目標是將 k-NN 搜尋準確度的下降降到最低。概括而言，向量會分割成 `m` 個子向量，然後每個子向量會以從訓練期間產生的編碼簿取得的 `code_size` 碼來表示。如需乘積量化的詳細資訊，請參閱[這篇部落格文章](https://medium.com/dotstar/understanding-faiss-part-2-79d90b1e5388)。
[`sq`](#sq-parameters) | 否 | _scalar quantization_ (純量量化) 的縮寫。使用 `sq` 編碼器將 32 位元浮點數向量量化為較低位元的表示法。對於 16 位元量化，`fp16` 類型會使用 SQFP16 Faiss 編碼器將向量量化為 16 位元浮點數，而 `bf16` 類型則會將其量化為 bfloat16 值。此編碼器可減少記憶體佔用量，並將精確度損失降到最低，同時使用 SIMD 最佳化 (在 x86 架構上使用 AVX2，或在 ARM64 架構上使用 Neon) 來提升效能。如需更多資訊，請參閱 [Faiss 純量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/)。

#### PQ 參數

`pq` 編碼器支援下列參數。

參數名稱 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`m` | 否 | `1` | 否 |  決定要將向量分割成的子向量數目。子向量會彼此獨立編碼。此向量維度必須可被 `m` 整除。最大值為 1,024。
`code_size` | 否 | `8` | 否 | 決定要將子向量編碼成的位元數。最大值為 `8`。對於 `ivf`，此值必須小於或等於 `8`。對於 `hnsw`，此值必須為 `8`。

`hnsw` 方法支援 OpenSearch 2.10 版及更新版本的 `pq` 編碼器。使用 `hnsw` 方法的 `pq` 編碼器，其 `code_size` 參數必須為 **8**。
{: .important}

#### SQ 參數

`sq` 編碼器支援下列參數。

參數名稱 | 必要 | 預設 | 建立索引後可更新 | 說明
:--- |:---------|:--------| :--- | :---
`type` | 否       | `fp16`  | 否 |  要用來將 32 位元浮點數向量編碼為對應類型的純量量化類型。有效值為 `fp16` 和 `bf16`。對於 `fp16` 編碼器，向量值必須在 [-65504.0, 65504.0] 範圍內。`bf16` 編碼器接受任何有限的 32 位元浮點數值。僅支援 16 位元量化。
`clip` | 否       | `false` | 否 | 對於 `fp16` 編碼器類型，若 `true`，超出支援範圍的向量值會調整至該範圍內。若 `false`，則只要有任何向量值超出支援範圍，請求就會遭到拒絕。將 `clip` 設為 `true` 可能會降低召回率。對於 `bf16`，將 `clip` 設為 `true` 會遭到拒絕；設為 `false` 則沒有任何作用。僅支援 16 位元量化。
`bits` | 是      | 無    | 否 | 用來量化每個 32 位元浮點數向量維度的位元數。有效值為 `1`、`2`、`4` 和 `16`。

如需更多資訊和範例，請參閱[使用 Faiss 純量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/)。

### SIMD 最佳化

如果基礎硬體支援 SIMD 指令，OpenSearch 支援[單指令多重資料 (SIMD)](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) 處理。在 Linux 機器上，只有 Faiss 引擎預設支援 SIMD。SIMD 架構可改善編製索引輸送量並縮短搜尋延遲，有助於提升整體效能。OpenSearch 使用下列指令集：

- ARM64 架構上的 Neon。
- x64 架構上的 AVX2 和 AVX-512。
- Intel Sapphire Rapids 或更新世代處理器上的進階 AVX-512 指令，可改善漢明距離計算的效能。在這些處理器上，OpenSearch 也會使用 AVX-512 BF16 指令來加速使用 [`bf16` 編碼器類型]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/#the-bf16-encoder) 量化之向量的內積計算，並使用 AVX-512 FP16 指令來加速使用 [`fp16` 編碼器類型]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/#the-fp16-encoder) 量化之向量的餘弦相似度計算。

只有在向量維度為 8 的倍數時，才適用 SIMD 最佳化。
{: .note}

<!-- vale off -->
#### x64 架構
<!-- vale on -->

針對 x64 架構，下列版本的 Faiss 程式庫會建置並隨成品一併提供：

- `libopensearchknn_faiss_avx512_spr.so`：包含適用於新一代處理器之進階 AVX-512 SIMD 指令的 Faiss 程式庫，可在 AWS 等公有雲的 c/m/r 7i 或更新的執行個體上使用。 
- `libopensearchknn_faiss_avx512.so`：包含 AVX-512 SIMD 指令的 Faiss 程式庫。 
- `libopensearchknn_faiss_avx2.so`：包含 AVX2 SIMD 指令的 Faiss 程式庫。
- `libopensearchknn_faiss.so`：不含 SIMD 指令且未經最佳化的 Faiss 程式庫。

使用 Faiss 程式庫時，效能排序如下：進階 AVX-512 > AVX-512 > AVX2 > 未經最佳化。
{: .note }

如果您的硬體支援進階 AVX-512(spr)，OpenSearch 會在執行階段載入 `libopensearchknn_faiss_avx512_spr.so` 程式庫。

如果您的硬體支援 AVX-512，OpenSearch 會在執行階段載入 `libopensearchknn_faiss_avx512.so` 程式庫。

如果您的硬體支援 AVX2，但不支援 AVX-512，OpenSearch 會在執行階段載入 `libopensearchknn_faiss_avx2.so` 程式庫。

若要停用進階 AVX-512（適用於 Sapphire Rapids 或更新一代的處理器）、AVX-512 和 AVX2 SIMD 指令，並載入未經最佳化的 Faiss 程式庫（`libopensearchknn_faiss.so`），請在 `opensearch.yml` 中將 `knn.faiss.avx512_spr.disabled`、`knn.faiss.avx512.disabled` 和 `knn.faiss.avx2.disabled` 靜態設定指定為 `true`（這些設定預設皆為 `false`）。

請注意，若要更新靜態設定，您必須停止叢集、變更設定，然後重新啟動叢集。如需詳細資訊，請參閱[靜態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#static-settings)。

#### ARM64 架構

針對 ARM64 架構，只會建置並提供一個可提升效能的 Faiss 程式庫（`libopensearchknn_faiss.so`）。此程式庫包含 Neon SIMD 指令，且無法停用。 

### 組態範例

下列範例使用 `ivf` 方法，且未指定編碼器（OpenSearch 預設使用 `flat` 編碼器）：

```json
"method": {
  "name":"ivf",
  "engine":"faiss",
  "parameters":{
    "nlist": 4,
    "nprobes": 2
  }
}
```

下列範例使用 `ivf` 方法搭配 `pq` 編碼器：

```json
"method": {
  "name":"ivf",
  "engine":"faiss",
  "parameters":{
    "encoder":{
      "name":"pq",
      "parameters":{
        "code_size": 8,
        "m": 8
      }
    }
  }
}
```

下列範例使用 `hnsw` 方法，且未指定編碼器（OpenSearch 預設使用 `flat` 編碼器）：

```json
"method": {
  "name":"hnsw",
  "engine":"faiss",
  "parameters":{
    "ef_construction": 256,
    "m": 8
  }
}
```

下列範例示範如何設定 `ivf` 方法，搭配使用 16 位元量化且停用裁切的 `sq` 編碼器：

```json
"method": {
  "name":"ivf",
  "engine":"faiss",
  "parameters":{
    "encoder": {
      "name": "sq",
      "parameters": {
        "bits": 16,
        "clip": false
      }
    },
    "nprobes": 2
  }
}
```

下列範例示範如何設定 `hnsw` 方法，搭配使用 1 位元量化的 `sq` 編碼器：

```json
"method": {
  "name":"hnsw",
  "engine":"faiss",
  "parameters":{
    "encoder": {
      "name": "sq",
      "parameters": {
        "bits": 1
      }
    },
    "ef_construction": 512,
    "m": 16
  }
}
```

下列範例示範如何設定 `hnsw` 方法，搭配使用 16 位元量化且啟用裁切的 `sq` 編碼器：

```json
"method": {
  "name":"hnsw",
  "engine":"faiss",
  "parameters":{
    "encoder": {
      "name": "sq",
      "parameters": {
        "bits": 16,
        "clip": true
      }  
    },    
    "ef_construction": 256,
    "m": 8
  }
}
```

## NMSLIB 引擎（已棄用）

Non-Metric Space Library（NMSLIB）引擎是 OpenSearch 最早的向量搜尋實作之一。雖然仍受支援，但此引擎已棄用，建議改用 Faiss 和 Lucene 引擎。

### 支援的方法

NMSLIB 引擎支援下列方法。

方法名稱 | 需要訓練 | 支援的空間 
:--- | :--- | :--- 
[`hnsw`](#hnsw-parameters-2) | 否 | `l2`、`innerproduct`、`cosinesimil`、`l1`、`linf` 

#### HNSW 參數

HNSW 方法支援下列參數。

參數名稱 | 必要 | 預設 | 索引建立後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`ef_construction` | 否 | 100 | 否 | 建立 k-NN 圖時使用的動態清單大小。較高的值可產生更精確的圖，但編製索引的速度較慢。
`m` | 否 | 16 | 否 | 為每個新元素建立的雙向連結數量。會顯著影響記憶體用量。請維持在 `2` 到 `100` 之間。

對於 NMSLIB（已棄用），*ef_search* 在[索引設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#index-settings)中設定。
{: .note}

在 OpenSearch 2.11 版或更早版本中建立的索引，仍會使用先前的 `ef_construction` 值（`512`）。
{: .note}

### 組態範例

```json
"method": {
    "name": "hnsw",
    "engine": "nmslib",
    "space_type": "l2",
    "parameters": {
        "ef_construction": 100,
        "m": 16
    }
}
```

## JVector 引擎

`jvector` 引擎以純 Java 實作 DiskANN 風格的近似最近鄰搜尋，不依賴 Java Native Interface（JNI）。此引擎未包含在任何 OpenSearch 發行版中；它由 `opensearch-jvector` 外掛程式提供，而該外掛程式無法與 `opensearch-knn` 安裝在同一個叢集中。如需安裝指示，請參閱 [OpenSearch JVector 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/#installation)。

### 支援的方法

`jvector` 引擎支援下列方法。

方法名稱 | 需要訓練 | 支援的空間
:--- | :--- | :---
[`disk_ann`](#diskann-parameters) | 否 | `l2`、`cosinesimil`、`innerproduct`

#### DiskANN 參數

`disk_ann` 方法支援下列參數。

參數名稱 | 必要 | 預設 | 索引建立後可更新 | 說明
:--- | :--- | :--- | :--- | :---
`m` | 否 | `16` | 否 | 每個節點的雙向連結數量。較高的值可提高召回率，但會增加索引大小。
`ef_construction` | 否 | `100` | 否 | 建構圖時使用的候選清單大小。較高的值可提高召回率，但會減慢匯入速度。
`advanced.alpha` | 否 | `1.2` | 否 | 選取鄰居的多樣性因子。
`advanced.neighbor_overflow` | 否 | `1.2` | 否 | 鄰居清單的溢位因子。
`advanced.hierarchy_enabled` | 否 | `false` | 否 | 是否啟用階層式圖結構。
`advanced.num_pq_subspaces` | 否 | 依據向量維度（請參閱[下表](#num-pq-subspaces)） | 否 | PQ 子空間的數量。不得超過向量維度數量，且為維度數的因數時效果最佳。較高的值會降低壓縮程度，但可提高召回率。
`advanced.min_batch_size_for_quantization` | 否 | `1024` | 否 | 訓練量化前所需的文件數量。
`advanced.leading_segment_merge_disabled` | 否 | `false` | 是 | 是否防止在強制合併期間重建首要分段。

<p id="num-pq-subspaces"> </p>

下表列出各向量維度的 `advanced.num_pq_subspaces` 預設值。

向量維度 | 預設 PQ 子空間數量
:--- | :---
`384` | `96`
`768` | `192`
`1536` | `192`
`3072` | `384`

### 空間類型

`space_type` 參數決定用來比較向量的距離度量。下表列出 `jvector` 引擎支援的空間類型。如需更多資訊，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

空間類型 | 距離度量 | 使用情境
:--- | :--- | :---
`l2` (預設) | 歐幾里得距離 (L2 範數) | 對原始座標進行一般用途搜尋
`cosinesimil` | 餘弦相似度 | 文字嵌入，方向比大小更重要的情境
`innerproduct` | 點積 (內積) | 大小具有意義的嵌入，例如由 bi-encoder 模型產生的嵌入

### 組態範例

```json
"method": {
  "name": "disk_ann",
  "engine": "jvector",
  "space_type": "l2",
  "parameters": {
    "m": 16,
    "ef_construction": 100
  }
}
```

## 選擇正確的方法與引擎

建立 `knn_vector` 欄位時有多種選項可選。若要選擇正確的方法與參數，您應先了解工作負載的需求，以及您願意做出哪些取捨。需要考慮的因素包括：(1) 查詢延遲、(2) 查詢品質、(3) 記憶體限制，以及 (4) 編製索引延遲。

如果記憶體不是問題，HNSW 在查詢延遲與查詢品質之間提供了良好的取捨。

如果您想在使用較少記憶體並提高編製索引速度的同時，維持與 HNSW 相近的查詢品質，您應該評估 IVF。

如果記憶體是問題，請考慮在您的 HNSW 或 IVF 索引中加入 PQ 編碼器。由於 PQ 是有損編碼，查詢品質會下降。

如果您的資料集持續成長或超出可用記憶體，請考慮 [JVector 引擎](#jvector-engine)，它由 [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)提供。它支援並行插入、無需完整重建圖形的增量合併，以及在更高壓縮比下具有更佳召回率的原生 PQ。

您可以使用 [`fp_16` 編碼器]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/#16-bit-quantization)，以最小的搜尋品質損失將記憶體佔用量減少為 1/2。如果您的向量維度在 [-128, 127] 位元組範圍內，我們建議使用[位元組量化器]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#byte-vectors)將記憶體佔用量減少為 1/4。若要進一步了解向量量化選項，請參閱 [k-NN 向量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/)。

## 引擎建議

一般而言，大規模使用情境請選擇 Faiss。Lucene 適合較小型的部署，並提供智慧篩選等優點，可依情況自動套用最佳篩選策略——預先篩選、事後篩選或精確 k-NN。若是高更新工作負載或記憶體受限的大規模部署，請考慮 JVector。下表摘要各選項之間的差異。

| |   Faiss/HNSW |  Faiss/IVF |  Lucene/HNSW | JVector/DiskANN |
|:---|:---|:---|:---|:---|
|  最大維度 |    16,000 |  16,000 |  16,000 | 16,000 |
|  篩選 |    事後篩選 |  事後篩選 |  搜尋期間篩選 | 搜尋期間篩選 <br><br> 事後篩選 |
|  需要訓練 |    否 (PQ 則為是) |  是 |  否 | 否 |
|  相似度度量 | `l2`, `innerproduct`, `cosinesimil` |  `l2`, `innerproduct`, `cosinesimil` |  `l2`, `cosinesimil` | `l2`, `cosinesimil`, `innerproduct` |
|  向量數量   |    數百億 |  數百億 |  少於 1,000 萬 | 數十億 |
|  編製索引延遲 |   低  |  最低  |  低  | 低 (並行插入) |
|  查詢延遲與品質  |    低延遲與高品質  |  低延遲與低品質  |  高延遲與高品質  | 低延遲與高品質 |
|  向量壓縮  |   Flat <br><br>PQ |  Flat <br><br>PQ |  Flat  | Flat <br><br> PQ (原生、無需訓練) |
|  記憶體消耗 |   高 <br><br> 使用 PQ 則為低 |  中 <br><br> 使用 PQ 則為低 |  高  | 低 (DiskANN) <br><br> 使用 PQ 則為極低 |
|  需要外掛程式 | 否 | 否 | 否 | 是 ([`opensearch-jvector`]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)) |

## 記憶體估算

在典型的 OpenSearch 叢集中，RAM 的一部分會保留給 JVM 堆積。OpenSearch 會將原生程式庫索引分配到剩餘 RAM 的一部分。這部分的大小由 `circuit_breaker_limit` 叢集設定決定。預設情況下，此限制設為 50%。

使用副本會使向量總數加倍。
{: .note }

如需搭配向量量化使用記憶體估算的資訊，請參閱 [向量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/)。
{: .note }

### HNSW 記憶體估算

HNSW 所需的記憶體估算為 `1.1 * (4 * dimension + 8 * m)` 位元組/向量。

舉例來說，假設您有 100 萬個向量，`dimension` 為 256，`m` 為 16。記憶體需求可估算如下：

```r
1.1 * (4 * 256 + 8 * 16) * 1,000,000 ~= 1.267 GB
```

### IVF 記憶體估算

IVF 所需的記憶體估算為 `1.1 * (((4 * dimension) * num_vectors) + (4 * nlist * d))` 位元組。

舉例來說，假設您有 100 萬個向量，`dimension` 為 `256`，`nlist` 為 `128`。記憶體需求可估算如下：

```r
1.1 * (((4 * 256) * 1,000,000) + (4 * 128 * 256))  ~= 1.126 GB
```

## 後續步驟

- [效能調校]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning/)
- [最佳化向量儲存]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/)
- [向量量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/)
