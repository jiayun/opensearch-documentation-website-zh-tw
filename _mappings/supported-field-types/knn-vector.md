---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "k-NN 向量"
nav_order: 90
has_children: true
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/knn-vector/
  - /mappings/supported-field-types/vector-field-types/
has_math: true
---

# k-NN 向量
**於 1.0 版推出**
{: .label .label-purple }

`knn_vector` 資料類型可讓您將向量匯入 OpenSearch 索引，並執行各種向量搜尋。`knn_vector` 欄位具有高度可設定性，可支援許多不同的向量工作負載。一般而言，`knn_vector` 欄位可透過[提供方法定義](#method-definitions)或[指定模型 ID](#model-ids)來建立。

## 範例

若要將 `my_vector` 對應為 `knn_vector`，請使用下列請求：

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
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 最佳化向量儲存空間

若要最佳化向量儲存空間，您可以將[向量工作負載模式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#vector-workload-modes)指定為 `in_memory` (針對最低延遲進行最佳化) 或 `on_disk` (針對最低成本進行最佳化)。`on_disk` 模式可減少記憶體使用量。您也可以選擇指定[`compression_level`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#compression-levels)來微調向量記憶體耗用量：


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


## 方法定義

當基礎的[近似 k-NN (ANN)]({{site.url}}{{site.baseurl}}/search-plugins/knn/approximate-knn/) 演算法不需要訓練時，會使用[方法定義]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。例如，下列 `knn_vector` 欄位指定 ANN 搜尋應使用 HNSW 的 Faiss 實作。在編製索引期間，Faiss 會建立對應的 HNSW 分段檔案：

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

您也可以在頂層指定 `space_type`：

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
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
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

## 模型 ID

當基礎的 ANN 演算法需要訓練步驟時，會使用模型 ID。先決條件是必須使用 [Train API]({{site.url}}{{site.baseurl}}/vector-search/api/knn#train-a-model) 建立模型。模型包含初始化原生程式庫分段檔案所需的資訊。若要為向量欄位設定模型，請指定 `model_id`：

```json
"my_vector": {
  "type": "knn_vector",
  "model_id": "my-model"
}
```

不過，如果您打算使用 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼或 k-NN 分數指令碼，則只需傳入 `dimension`：

```json
"my_vector": {
   "type": "knn_vector",
   "dimension": 128
 }
```

如需詳細資訊，請參閱[從模型建立向量索引]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/approximate-knn/#building-a-vector-index-from-a-model)。

### 參數

下表列出 k-NN 向量欄位類型接受的參數。

參數 | 資料類型 | 說明 
:--- | :--- 
`type` | 字串 | 向量欄位類型。必須是 `knn_vector`。必要。
`dimension` | 整數 | 所用向量的大小。有效值介於 [1, 16,000] 範圍內。必要。
`data_type` | 字串 | 向量元素的資料類型。有效值為 `binary`、`byte`、`float` 和 `half_float`。選用。預設為 `float`。
`space_type` | 字串 | 用來計算向量之間距離的向量空間。有效值為 `l1`、`l2`、`linf`、`cosinesimil`、`innerproduct`、`hamming` 和 `hammingbit`。並非每種方法/引擎組合都支援每個空間。如需支援的空間清單，請參閱特定引擎的章節。注意：此值也可在 `method` 內指定。選用。如需詳細資訊，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。
`mode` | 字串 | 根據您的優先順序（低延遲或低成本）為 k-NN 參數設定適當的預設值。有效值為 `in_memory` 和 `on_disk`。選用。預設為 `in_memory`。如需詳細資訊，請參閱[記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)。
`compression_level` | 字串 | 選取量化編碼器，依指定倍數減少向量記憶體耗用量。有效值為 `1x`、`2x`、`4x`、`8x`、`16x` 和 `32x`。選用。如需詳細資訊，請參閱[記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)。
`method` | 物件 | 用於在編製索引時組織向量資料，並在搜尋時搜尋該資料的演算法。當 ANN 演算法不需要訓練時使用。選用。如需詳細資訊，請參閱[方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。
`model_id` | 字串 | 已訓練模型的模型 ID。當 ANN 演算法需要訓練時使用。請參閱[模型 ID](#model-ids)。選用。

## 動態對應
**於 3.9 版推出**
{: .label .label-purple }

OpenSearch 可以自動將欄位對應為 `knn_vector`，無需明確對應。動態對應有兩種運作方式：使用 `knn_vector` 作為 `match_mapping_type` 的動態範本，或從第一個編製索引的值自動推斷。

動態對應適用於任何尚未對應的欄位，無論是新索引或現有索引皆然。明確對應一律優先：如果欄位已對應，動態對應就不會套用至該欄位。

`knn_vector` 欄位遵循與所有其他動態對應欄位相同的 [`dynamic`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/dynamic/) 對應參數。如果索引或父物件的 `dynamic` 設為 `strict`，OpenSearch 會拒絕任何包含未對應欄位的文件，因此不會建立任何 `knn_vector` 欄位。

動態對應預設為停用。若要啟用，請設定 [`knn.dynamic_mapping.enabled`]({{site.url}}{{site.baseurl}}/vector-search/settings/#cluster-settings) 叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "knn.dynamic_mapping.enabled": true
  }
}
```
{% include copy-curl.html %}

動態對應只會建立 `knn_vector` 欄位。它不會啟用近似 k-NN (ANN) 搜尋。支援的搜尋類型取決於您建立索引時 [`index.knn`]({{site.url}}{{site.baseurl}}/vector-search/settings/#index-settings) 設定的值：

- 如果 `index.knn` 為 `true`，OpenSearch 會建立該欄位所需的資料結構，並同時支援精確和近似 k-NN 搜尋。
- 如果 `index.knn` 未設定或為 `false`，該欄位仍會對應為 `knn_vector`，但只支援精確 k-NN 搜尋。

如果您打算對動態對應的向量欄位執行 ANN 搜尋，請在建立索引時將 `index.knn` 設為 `true`。您無法在現有索引上啟用 ANN 搜尋。若要使用 ANN 搜尋，請將資料重新編製索引至以 `index.knn: true` 建立的新索引。
{: .warning}

### 動態範本

您可以在[動態範本]({{site.url}}{{site.baseurl}}/mappings/#dynamic-mapping)中將 `knn_vector` 參照為 `match_mapping_type`。當 OpenSearch 首次遇到符合的欄位時，會使用您提供的對應區塊將該欄位對應為 `knn_vector`：

```json
PUT /knn-dyn-template
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "dynamic_templates": [
      {
        "vectors": {
          "match_mapping_type": "knn_vector",
          "mapping": {
            "type": "knn_vector"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

此範本未指定任何比對條件，因此適用於索引中每個未對應的欄位，而不僅限於向量欄位。如果欄位的值不是數字陣列，OpenSearch 無法為其推斷維度，並會以 `Dimension value missing` 錯誤拒絕該文件。若要將範本限制於您的向量欄位，請新增 `match`、`match_pattern` 或 `path_match` 條件，例如 `"match": "*_vector"`。
{: .warning}

在符合的欄位被編製索引之前，對應中僅包含動態範本，而沒有 `properties` 物件。將包含 8 維向量的文件編製索引：

```json
POST /knn-dyn-template/_doc/1?refresh=true
{
  "vec_tmpl": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
}
```
{% include copy-curl.html %}

擷取對應以確認 `vec_tmpl` 已被對應為維度為 8 的 `knn_vector`：

```json
GET /knn-dyn-template/_mapping
```
{% include copy-curl.html %}

回應現在包含 `vec_tmpl` 欄位：

```json
{
  "knn-dyn-template": {
    "mappings": {
      "dynamic_templates": [
        {
          "vectors": {
            "match_mapping_type": "knn_vector",
            "mapping": {
              "type": "knn_vector"
            }
          }
        }
      ],
      "properties": {
        "vec_tmpl": {
          "type": "knn_vector",
          "dimension": 8
        }
      }
    }
  }
}
```

您可以在 `mapping` 區塊中指定任何 `knn_vector` 參數（例如 `dimension`、`space_type`、`method` 或 `model_id`）。如果您指定了 `dimension` 或提供維度的 `model_id`，OpenSearch 會使用該值。如果兩者都省略，OpenSearch 會從第一個被編製索引之向量的長度推斷維度。

由於 `match_mapping_type: "knn_vector"` 已隱含欄位類型，因此在 `mapping` 區塊內 `type: knn_vector` 是選用的，若省略則會自動注入。例如，下列範本等同於先前顯示的 `dynamic_templates` 區塊：

```json
"dynamic_templates": [
  {
    "vectors": {
      "match_mapping_type": "knn_vector",
      "mapping": {}
    }
  }
]
```
{% include copy.html %}

由於範本已確立欄位類型，自動推斷所使用的陣列長度啟發式規則（將於下一節說明）並不適用。任何符合範本的扁平數字陣列都會被對應為 `knn_vector`，無論其長度為何。

### 自動推斷

當沒有動態範本符合時，OpenSearch 仍可從欄位值推斷出 `knn_vector` 對應。當未對應欄位的值是長度為 8 的倍數、且落在 128 至預設 k-NN 引擎所支援最大維度（Faiss 為 16,000）範圍內的扁平數字陣列時，該欄位會被對應為 `knn_vector`。此界限在推斷時套用，無論該欄位最終使用哪個引擎。維度會設為陣列長度。長度超出此範圍或不是 8 的倍數的陣列會被對應為數字陣列。

自動推斷僅指定 `type` 和 `dimension`。其餘所有參數皆採用預設值：`faiss` 引擎、`hnsw` 方法、`l2` 空間類型，以及 `float` 資料類型。

例如，建立一個沒有 `embedding` 對應且沒有動態範本的索引。由於自動推斷不會啟用 ANN 搜尋，如果您打算在推斷的欄位上執行 ANN 搜尋，請將 `index.knn` 設為 `true`：

```json
PUT /knn-auto-infer
{
  "settings": {
    "index": {
      "knn": true
    }
  }
}
```
{% include copy-curl.html %}

將包含 768 維向量的文件編製索引。此範例中的陣列已截斷：

```json
POST /knn-auto-infer/_doc/1?refresh=true
{
  "embedding": [0.1, 0.2, 0.3, ..., 0.9]
}
```

擷取對應以確認 `embedding` 已被對應為維度為 768 的 `knn_vector`：

```json
GET /knn-auto-infer/_mapping
```
{% include copy-curl.html %}

回應包含推斷的欄位：

```json
{
  "knn-auto-infer": {
    "mappings": {
      "properties": {
        "embedding": {
          "type": "knn_vector",
          "dimension": 768
        }
      }
    }
  }
}
```

自動推斷是以形狀為基礎的啟發式規則，因此不是向量的數字陣列（例如大量的 ID 或量測值清單），若其長度恰好符合這些條件，也可能被對應為 `knn_vector`。由於維度在第一份文件之後即固定，後續陣列長度不同的文件會被拒絕。若要防止欄位被自動推斷為 `knn_vector`，請為其宣告明確的對應，或使用將該欄位對應為其他類型的動態範本。

### 限制

自動推斷與動態範本僅適用於個別的 `knn_vector` 欄位；它們絕不會建立 [`nested`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 父層。如果您將物件陣列編製索引到未對應的欄位（例如每個區塊的嵌入），文件會被拒絕，因為在一般 `object` 父層之下，內部向量陣列無法被扁平化為單一 `knn_vector` 值：

```json
{
  "chunks": [
    { "my_vector": [0.1, 0.2, ...], "text": "..." },
    { "my_vector": [0.3, 0.4, ...], "text": "..." }
  ]
}
```

若要搜尋個別巢狀物件中的向量，請在建立索引時將父層欄位明確宣告為 `type: nested`。動態對應仍會在 `nested` 父層之下對應內部的 `knn_vector` 欄位。例如，建立索引時將 `chunks` 宣告為 `nested`：

```json
PUT /knn-nested-dyn
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "chunks": { "type": "nested" }
    }
  }
}
```
{% include copy-curl.html %}

將內部 `embedding` 欄位為符合[自動推斷](#auto-inference)要求的扁平數字陣列的文件編製索引。此範例中的陣列已截斷：

```json
POST /knn-nested-dyn/_doc/1?refresh=true
{
  "chunks": [
    { "embedding": [0.1, 0.1, ..., 0.1] },
    { "embedding": [0.2, 0.2, ..., 0.2] }
  ]
}
```

擷取對應以確認 `chunks.embedding` 的對應方式：

```json
GET /knn-nested-dyn/_mapping
```
{% include copy-curl.html %}

回應確認 `chunks` 仍為 `nested`，且 `chunks.embedding` 已被對應為 `knn_vector`：

```json
{
  "knn-nested-dyn": {
    "mappings": {
      "properties": {
        "chunks": {
          "type": "nested",
          "properties": {
            "embedding": {
              "type": "knn_vector",
              "dimension": 128
            }
          }
        }
      }
    }
  }
}
```

## 後續步驟

- [空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)
- [方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)
- [記憶體最佳化向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/)
- [向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)