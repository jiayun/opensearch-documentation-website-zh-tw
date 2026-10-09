---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "二元量化"
parent: Vector quantization
grand_parent: Optimizing vector storage
nav_order: 40
has_children: false
has_math: true
---

# 二元量化

OpenSearch 透過 Faiss 引擎的二進位向量支援，提供二元量化 (BQ) 功能。BQ 將向量壓縮成二進位格式 (0 與 1)，因此在記憶體使用上非常有效率。您可以依據所需的精確度，選擇以 1、2 或 4 位元表示每個向量維度。使用 BQ 的優點之一是訓練程序會在編製索引時自動處理。這表示不需要另外執行訓練步驟，與 PQ 等其他量化技術不同。

## 使用 BQ

若要為 Faiss 引擎設定 BQ，請定義 `knn_vector` 欄位，並在 method 參數中指定 `binary` 編碼器。`bits` 參數控制量化所使用的位元數，可設定為 `1`、`2` 或 `4`：

- `1` 位元量化：32 倍壓縮
- `2` 位元量化：16 倍壓縮
- `4` 位元量化：8 倍壓縮

下列範例建立一個使用 1 位元二元量化的索引：

```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "m": 16,
            "ef_construction": 512,
            "encoder": {
              "name": "binary",
              "parameters": {
                "bits": 1
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

## 使用 ADC 與 RR 提升搜尋品質
**3.2 版新增**
{: .label .label-purple }

如果您的搜尋結果召回率偏低，可以在索引對應中指定非對稱距離計算 (ADC) 或隨機旋轉 (RR) 來提升搜尋品質。

ADC 會保留全精確度的查詢向量，同時重新調整其比例，以便對二元量化的文件向量進行有意義的距離計算。這種非對稱做法保留了更多查詢向量的資訊，在不顯著增加記憶體負擔的情況下提升搜尋品質。ADC 僅支援 1 位元量化。

RR 解決了二元量化在量化過程中對每個向量維度給予相同權重的問題。透過旋轉分布，RR 可以將變異數 (資訊) 從高變異數維度重新分配到低變異數維度，在 32 倍壓縮過程中保留更多資訊。RR 支援 1 位元、2 位元與 4 位元量化。

若要獲得最佳效能與召回率提升，請同時使用 ADC 與 RR：

```json
PUT vector-index
{
  "settings" : {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "vector_field": {
        "type": "knn_vector",
        "dimension": 8,
        "space_type": "l2",
        "method": {
            "name": "hnsw",
            "engine": "faiss",
            "parameters": {
              "encoder": {
                "name": "binary",
                "parameters": {
                  "bits": 1,
                  "random_rotation": true,
                  "enable_adc": true
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

ADC 與 RR 會影響搜尋與索引效能，因此預設為停用。ADC 因為需要進行全精確度距離計算，可能會適度增加延遲；而 RR 主要影響索引延遲，因為向量在此過程中必須旋轉。
{: .note}

## 使用二元量化向量進行搜尋

您可以提供向量並指定要傳回的最近鄰居數量 (k)，對索引執行向量搜尋：

```json
GET my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 5.5, 1.5, 5.5, 1.5, 5.5, 1.5, 5.5],
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

您也可以提供 `ef_search` 與 `oversample_factor` 參數來微調搜尋。
`oversample_factor` 參數控制搜尋在排名前對候選向量進行超取樣的倍數。使用較高的超取樣倍數表示在排名前會考慮更多候選向量，可提升準確度，但也會增加搜尋時間。選擇 `oversample_factor` 值時，請考量準確度與效率之間的取捨。例如，將 `oversample_factor` 設為 `2.0` 會使排名階段考慮的候選向量數量加倍，可能有助於取得更好的結果。

下列請求指定了 `ef_search` 與 `oversample_factor` 參數：

```json
GET my-vector-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 5.5, 1.5, 5.5, 1.5, 5.5, 1.5, 5.5],
        "k": 10,
        "method_parameters": {
            "ef_search": 10
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


## HNSW 記憶體估算

階層式可導航小世界 (HNSW) 圖形所需的記憶體可估算為 `1.1 * (dimension * bits / 8 + 8 * m)` 位元組/向量，其中 `m` 是建構圖形時為每個元素建立的最大雙向連結數。

舉例來說，假設您有 100 萬個向量，維度為 256，`m` 為 16。以下各節提供各種壓縮值的記憶體需求估算。

### 1 位元量化 (32 倍壓縮)

在 1 位元量化中，每個維度以 1 位元表示，相當於 32 倍壓縮。記憶體需求可估算如下：

```r
Memory = 1.1 * ((256 * 1 / 8) + 8 * 16) * 1,000,000
       ~= 0.176 GB
```

### 2 位元量化 (16 倍壓縮)

在 2 位元量化中，每個維度以 2 位元表示，相當於 16 倍壓縮。記憶體需求可估算如下：

```r
Memory = 1.1 * ((256 * 2 / 8) + 8 * 16) * 1,000,000
       ~= 0.211 GB
```

### 4 位元量化 (8 倍壓縮)

在 4 位元量化中，每個維度以 4 位元表示，相當於 8 倍壓縮。記憶體需求可估算如下：

```r
Memory = 1.1 * ((256 * 4 / 8) + 8 * 16) * 1,000,000
       ~= 0.282 GB
```

## 後續步驟

- [磁碟型向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)
- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
