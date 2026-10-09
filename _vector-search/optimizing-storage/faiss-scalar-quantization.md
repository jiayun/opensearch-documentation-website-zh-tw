---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Faiss 純量量化"
parent: Vector quantization
grand_parent: Optimizing vector storage
nav_order: 20
has_children: false
has_math: true
redirect_from:
  - /vector-search/optimizing-storage/faiss-16-bit-quantization/
---

# Faiss 純量量化

OpenSearch 支援 Faiss 引擎的內建純量量化。Faiss 純量量化器會在匯入期間將 32 位元浮點輸入向量轉換為較低位元的表示形式，並將量化後的向量儲存在向量索引中。OpenSearch 支援 1、2、4 和 16 位元的 Faiss 純量量化。

量化可減少記憶體用量，代價是召回率略有下降。搭配 [SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization) 使用時，Faiss 純量量化也能大幅降低搜尋延遲，並提高編製索引的輸送量。

Windows 不支援 SIMD 最佳化。在 Windows 上使用 Faiss 純量量化可能導致效能大幅下降，包括編製索引的輸送量降低及搜尋延遲增加。
{: .warning}

## 使用 Faiss 純量量化

若要使用 Faiss 純量量化，請在建立向量索引時，將 k-NN 向量欄位的 `method.parameters.encoder.name` 設為 `sq`。您必須在 `method.parameters.encoder.parameters` 物件中指定 `bits` 參數：

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 16
              }
            },
            "ef_construction": 256,
            "m": 8
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

Faiss `sq` 編碼器支援下列參數。

參數名稱 | 必要 | 預設 | 說明
:--- | :--- | :--- | :---
`bits` | 是 | 無 | 用於量化每個向量維度的位元數。有效值為 `1`、`2`、`4` 和 `16`。
`type` | 否 | `fp16` | 要使用的純量量化類型。有效值為 `fp16` 和 `bf16`。對於 `fp16` 編碼器，向量值必須介於 [-65504.0, 65504.0] 範圍內。`bf16` 編碼器接受任何有限的 32 位元浮點值。
`clip` | 否 | `false` | 對於 `fp16`，若 `true`，則會將支援範圍之外的向量值捨入，使其落在範圍內。若 `false`，則只要有任何向量值超出支援範圍，就會拒絕請求。將 `clip` 設為 `true` 可能會降低召回率。對於 `bf16`，將 `clip` 設為 `true` 會遭到拒絕；將其設為 `false` 則沒有作用。

`type` 和 `clip` 參數僅支援 16 位元量化。如果您將 `bits` 設為任何其他值，並指定 `type` 或 `clip`，則會拒絕請求。
{: .warning}

## 1 位元、2 位元和 4 位元量化

若要將記憶體用量降至最低，請將每個向量維度量化為 1、2 或 4 位元。每種位元寬度都對應一個 `compression_level`。

位元數 | `compression_level` | 相較於 32 位元向量的記憶體縮減倍數 | 引入版本
:--- | :--- | :--- | :---
`1` | `32x` | 32x | 3.6
`2` | `16x` | 16x | 3.9
`4` | `8x` | 8x | 3.9

每個維度使用的位元越少，產生的索引就越小，但召回率也會下降。這些位元寬度僅支援 HNSW 方法；IVF 需要 16 位元量化。1 位元量化使用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)。

下列範例在 `knn_vector` 對應中將 `compression_level` 設為 `16x`，以對 `float` 欄位啟用 2 位元量化。若要使用 1 位元或 4 位元量化，請將 `compression_level` 設為 `32x` 或 `8x`：

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "compression_level": "16x"
      }
    }
  }
}
```
{% include copy-curl.html %}

或者，您可以在 `sq` 編碼器中設定 `bits`，以明確指定編碼器：

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 2
              }
            },
            "ef_construction": 256,
            "m": 8
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

1 位元量化也支援 [`half_float` 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#half-float-vectors)。由於 `half_float` 欄位不接受在 `method` 對應中指定 `encoder`，請改將 `compression_level` 設為 `16x`。此等級以 `half_float` 向量的 16 位元基準衡量，因此會將每個維度對應至單一位元。

## 16 位元量化

使用 16 位元量化時，Faiss 純量量化器會將 32 位元浮點向量轉換為 16 位元向量，並將其儲存在向量索引中。搜尋時，儲存的 16 位元值會轉換回 32 位元浮點值，以計算距離。在 Intel Sapphire Rapids 或更新世代的處理器上，OpenSearch 會直接以 16 位元值計算距離，使用 AVX-512 BF16 指令計算 `bf16` 內積，並使用 AVX-512 FP16 指令計算 `fp16` 餘弦相似度。如需詳細資訊，請參閱 [SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

OpenSearch 支援兩種 16 位元編碼器類型，可在 `type` 參數中指定：

- `fp16`（預設）：IEEE 754 半精度格式（FP16），使用 5 個指數位元和 10 個尾數位元。此格式提供最高的 16 位元精度，但數值範圍較窄，為 [-65504.0, 65504.0]。當您所有的向量值都落在該範圍內時，請使用 `fp16`。
- `bf16`：[bfloat16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) 格式（BF16），使用 8 個指數位元和 7 個尾數位元。其數值範圍與 32 位元浮點數相同，但精度較低，因此可能導致召回率的降幅稍大。當您的向量可能包含超出 `fp16` 範圍的值，或您想避免 `fp16` 的範圍驗證與裁剪時，請使用 `bf16`。

這兩種編碼器類型都以 2 位元組儲存每個向量維度，因此都能將記憶體用量減半，且召回率損失極小。

### fp16 編碼器

`fp16` 編碼器會將 32 位元向量轉換為對應的 16 位元向量。對於此編碼器類型，向量值必須介於 [-65504.0, 65504.0] 範圍內。若要定義如何處理超出範圍的值，您可以指定 `clip` 參數。此參數預設為 `false`，任何包含超出範圍值的向量都會遭到拒絕。

當 `clip` 設為 `true` 時，會將超出範圍的向量值向上或向下捨入，使其落在支援範圍內。例如，如果原始的 32 位元向量為 `[65510.82, -65504.1]`，則會以 16 位元向量 `[65504.0, -65504.0]` 編製索引。

我們建議僅在極少數向量維度超出支援範圍時，才將 `clip` 設為 `true`。將數值捨入可能導致召回率下降。
{: .note}

下列範例指定採用 16 位元量化的 Faiss `fp16` 編碼器，此編碼器會拒絕任何包含超出範圍向量值的編製索引請求（因為 `clip` 參數預設為 `false`）：

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 16
              }
            },
            "ef_construction": 256,
            "m": 8
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

為向量編製索引時，請確保每個向量維度都在支援範圍內：

```json
PUT test-index/_doc/1
{
  "my_vector1": [-65504.0, 65503.845, 55.82]
}
```
{% include copy-curl.html %}

查詢向量時，查詢向量沒有範圍限制：

```json
GET test-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector1": {
        "vector": [265436.876, -120906.256, 99.84],
        "k": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

### bf16 編碼器
**3.9 版新增**
{: .label .label-purple }

`bf16` 編碼器會將 32 位元向量轉換為 bfloat16 向量。由於 bfloat16 使用的指數位元數與 32 位元浮點數相同，因此涵蓋相同的數值範圍。任何有限的 32 位元浮點值都可以編製索引，不會因範圍限制而被拒絕或裁剪。在量化過程中，每個值會四捨五入至最接近的可表示 bfloat16 值，將尾數從 23 位元縮減為 7 位元。因此，與 `fp16` 相比，`bf16` 以精確度換取範圍。

以下範例指定使用 16 位元量化的 Faiss `bf16` 編碼器：

```json
PUT /test-index-bf16
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 16,
                "type": "bf16"
              }
            },
            "ef_construction": 256,
            "m": 8
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

向量值不受範圍限制，因此不會有任何維度被拒絕：

```json
PUT test-index-bf16/_doc/1
{
  "my_vector1": [-150000.5, 123456.75, 55.82]
}
```
{% include copy-curl.html %}

僅接受有限值。包含 `NaN` 或無限值的編製索引請求會被拒絕。
{: .note}

請注意 `bf16` 編碼器的以下限制：

- 不支援將 `clip` 設定為 `true`，否則請求會被拒絕。因為 `bf16` 涵蓋完整的 32 位元浮點值範圍，裁剪不會產生任何效果。
- 不支援[遠端索引建置]({{site.url}}{{site.baseurl}}/vector-search/remote-index-build/)。使用 `bf16` 編碼器的索引一律在本機建置。

## 記憶體估算

在最佳情況下，量化向量所需的記憶體為 32 位元向量所需記憶體的以下百分比。

位元 | 佔 32 位元向量記憶體的百分比 | 縮減幅度
:--- | :--- | :---
`1` | 3.125% | 32 倍
`2` | 6.25% | 16 倍
`4` | 12.5% | 8 倍
`16` | 50% | 2 倍

### HNSW 記憶體估算

Hierarchical Navigable Small Worlds (HNSW) 所需的記憶體估算為每個向量 `1.1 * (dimension * bits_per_dimension / 8 + 8 * m)` 位元組，其中 `m` 是在建構圖形時為每個元素建立的最大雙向連結數。

例如，假設您有 100 萬個向量，維度為 256，`m` 為 16。每個位元寬度的記憶體需求可估算如下。

位元 | 估算 | 結果
:--- | :--- | :---
`1` | `1.1 * (256 * 1 / 8 + 8 * 16) * 1,000,000` | ~0.176 GB
`2` | `1.1 * (256 * 2 / 8 + 8 * 16) * 1,000,000` | ~0.211 GB
`4` | `1.1 * (256 * 4 / 8 + 8 * 16) * 1,000,000` | ~0.282 GB
`16` | `1.1 * (256 * 16 / 8 + 8 * 16) * 1,000,000` | ~0.656 GB

### IVF 記憶體估算

IVF 所需的記憶體估算為 `1.1 * (((bytes_per_dimension * dimension) * num_vectors) + (4 * nlist * dimension))` 位元組，其中 `nlist` 是向量分割成的桶數。

例如，假設您有 100 萬個向量，維度為 256，`nlist` 為 128。

IVF 僅支援 16 位元 Faiss 純量量化。1 位元、2 位元與 4 位元量化僅支援 HNSW 方法。
{: .note}

對於 16 位元量化，記憶體需求可估算如下：

```r
1.1 * (((2 * 256) * 1,000,000) + (4 * 128 * 256))  ~= 0.525 GB
```

## 後續步驟

- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
