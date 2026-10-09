---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Lucene 純量量化"
parent: Vector quantization
grand_parent: Optimizing vector storage
nav_order: 10
has_children: false
has_math: true
---

# Lucene 純量量化

OpenSearch 支援 Lucene 引擎的內建純量量化。與[位元組向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#byte-vectors)不同，位元組向量需要您在匯入文件前先量化向量，而 Lucene 純量量化器會在匯入期間於 OpenSearch 中量化輸入向量。量化器會將 32 位元浮點數輸入向量轉換為每個分段中較低位元的表示法。OpenSearch 支援 1、2、4 及 7 位元量化。

搜尋時，查詢向量會在每個分段中量化，以計算查詢向量與該分段量化後輸入向量之間的距離。量化可減少記憶體用量，但會犧牲部分召回率。此外，量化會略微增加磁碟使用量，因為它需要同時儲存原始輸入向量與量化後的向量。

設定 `sq` 編碼器時，必須提供 `bits` 參數。
{: .important}

## 使用 Lucene 純量量化

若要使用 Lucene 純量量化器，請在建立向量索引時將 k-NN 向量欄位的 `method.parameters.encoder.name` 設為 `sq`。您必須在 `method.parameters.encoder.parameters` 物件中指定 `bits` 參數：

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
        "dimension": 2,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 1
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

Lucene 純量量化僅適用於 `float` 與 `half_float` 向量。[半精度浮點數向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#half-float-vectors)在 `method` 對應中不接受 `encoder`；若要將其量化為每個維度 1 位元，請將 `compression_level` 設為 `16x`。若您在對應 [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)時將 `data_type` 參數變更為 `byte` 或任何其他不受支援的類型，則該請求會被拒絕。
{: .warning}

### SQ 參數

Lucene `sq` 編碼器支援下列參數。

參數名稱 | 必要 | 預設 | 說明
:--- | :--- | :--- | :---
`bits` | 是 | 1 | 用於量化每個向量維度的位元數。有效值為 `1`、`2`、`4` 及 `7`。
`confidence_interval` | 否 | 依向量維度計算 | 用於計算量化最小值與最大值的分位數區間。僅支援 7 位元量化。如需更多資訊，請參閱[信賴區間](#confidence-interval)。

`confidence_interval` 參數僅支援 7 位元量化。若您將 `bits` 設為任何其他值並指定 `confidence_interval`，則該請求會被拒絕。
{: .warning}

## 1 位元、2 位元及 4 位元量化

若要達到最低的記憶體用量，請將每個向量維度量化為 1、2 或 4 位元。這些變體支援下列位元寬度。

位元 | 相較於 32 位元向量的記憶體縮減 | 推出版本
:--- | :--- | :---
`1` | 32x | 3.6
`2` | 16x | 3.9
`4` | 8x | 3.9

每個維度的位元數越少，索引就越小，但會犧牲召回率。這些變體皆不支援 `confidence_interval` 參數；指定它會導致請求被拒絕。

下列範例會建立一個將每個 `float` 向量維度量化為 2 位元的索引。若要使用 1 位元或 4 位元量化，請將 `bits` 設為 `1` 或 `4`：

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
          "engine": "lucene",
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

若要將 [`half_float` 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#half-float-vectors)量化為每個維度 1 位元，請將 `compression_level` 設為 `16x`，而不要指定 `bits`。

## 7 位元量化

使用 7 位元量化時，Lucene 純量量化器會根據 [`confidence_interval`](#confidence-interval) 參數計算出的最小與最大分位數，將每個 32 位元浮點數向量維度轉換為 7 位元整數值。搜尋時，查詢向量會使用該分段的最小與最大分位數，在每個分段中量化。

### 信賴區間

您可以選擇在 `method.parameters.encoder` 物件中指定 `confidence_interval` 參數。
`confidence_interval` 用於計算量化向量所需的最小與最大分位數：
- 若您將 `confidence_interval` 設為 `0.9` 至 `1.0` 範圍內（含端點）的值，則分位數會以靜態方式計算。例如，將 `confidence_interval` 設為 `0.9` 表示 OpenSearch 會根據向量值的中間 90% 計算最小與最大分位數，排除最小值 5% 與最大值 5% 的值。
- 將 `confidence_interval` 設為 `0` 表示 OpenSearch 會動態計算分位數，這涉及過度取樣以及對輸入資料執行額外計算。
- 未設定 `confidence_interval` 時，會根據向量維度 $d$ 使用公式 $max(0.9, 1 - \frac{1}{1 + d})$ 計算。

下列範例方法定義指定使用 7 位元量化的 Lucene `sq` 編碼器，並將 `confidence_interval` 設為 `1.0`。此 `confidence_interval` 指定在計算最小與最大分位數時使用所有輸入向量：

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
        "dimension": 2,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 7,
                "confidence_interval": 1.0
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

## 記憶體估算

在理想情況下，量化向量使用的記憶體佔 32 位元向量所需記憶體的下列百分比。

位元 | 佔 32 位元向量記憶體的百分比 | 縮減
:--- | :--- | :---
`1` | 3.125% | 32x
`2` | 6.25% | 16x
`4` | 12.5% | 8x
`7` | 25% | 4x

### HNSW 記憶體估算

階層式可導覽小世界 (HNSW) 圖形所需的記憶體可估算為每個向量 `1.1 * (dimension * bits_per_dimension / 8 + 8 * m)` 位元組，其中 `m` 是在圖形建構期間為每個元素建立的最大雙向連結數。

例如，假設您有 100 萬個維度為 256 且 `m` 為 16 的向量。每個位元寬度的記憶體需求可估算如下。

位元 | 估算 | 結果
:--- | :--- | :---
`1` | `1.1 * (256 * 1 / 8 + 8 * 16) * 1,000,000` | ~0.176 GB
`2` | `1.1 * (256 * 2 / 8 + 8 * 16) * 1,000,000` | ~0.211 GB
`4` | `1.1 * (256 * 4 / 8 + 8 * 16) * 1,000,000` | ~0.282 GB
`7` | `1.1 * (256 * 7 / 8 + 8 * 16) * 1,000,000` | ~0.387 GB

## 後續步驟

- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
