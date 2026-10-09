---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語意"
nav_order: 15
has_children: false
parent: Specialized search field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/semantic/
---

# Semantic 欄位類型
**於 3.1 版推出**
{: .label .label-purple }

`semantic` 欄位類型是一種高階抽象，可簡化 OpenSearch 中的神經搜尋設定。它能包裝多種欄位類型，包括所有字串和二進位欄位。`semantic` 欄位類型會根據所設定的機器學習 (ML) 模型自動啟用語意索引和查詢。

**先決條件**<br>
使用 `semantic` 欄位類型之前，您必須設定裝載於 OpenSearch 叢集上的本機 ML 模型，或連線至 OpenSearch 叢集的外部裝載模型。如需本機模型的詳細資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。如需外部裝載模型的詳細資訊，請參閱[連線至外部裝載模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
{: .note}

## 範例：稠密嵌入模型

`semantic` 欄位類型同時支援對稱與非對稱嵌入模型。對稱模型對文件和查詢使用相同的嵌入表示法。非對稱模型（例如 E5）在匯入期間將文件內容編碼為段落，並在搜尋時將查詢文字編碼為查詢。
{: .note}

設定模型後，您可以使用它建立含有 `semantic` 欄位的索引。此範例假設您已在叢集中設定 ID 為 `n17yX5cBsaYnPfyOzmQU` 的稠密嵌入模型：

```json
PUT /my-nlp-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "n17yX5cBsaYnPfyOzmQU"
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引後，您可以擷取其對應，以確認已自動建立 `passage_semantic_info` 欄位。`passage_semantic_info` 欄位包含用於儲存稠密嵌入的 `knn_vector` 子欄位，以及用於擷取模型 ID、模型名稱和模型類型等資訊的其他中繼資料欄位：

```json
GET /my-nlp-index/_mapping
{
  "my-nlp-index": {
    "mappings": {
      "properties": {
        "passage": {
          "type": "semantic",
          "model_id": "n17yX5cBsaYnPfyOzmQU",
          "raw_field_type": "text"
        },
        "passage_semantic_info": {
          "properties": {
            "embedding": {
              "type": "knn_vector",
              "dimension": 384,
              "method": {
                "engine": "faiss",
                "space_type": "l2",
                "name": "hnsw",
                "parameters": {}
              }
            },
            "model": {
              "properties": {
                "id": {
                  "type": "text",
                  "index": false
                },
                "name": {
                  "type": "text",
                  "index": false
                },
                "type": {
                  "type": "text",
                  "index": false
                }
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

`knn_vector` 欄位的 `dimension` 和 `space_type` 取決於 ML 模型組態。對於[預先訓練的稠密模型](ml-commons-plugin/pretrained-models/#sentence-transformers)，此資訊包含在預設模型組態中。對於外部裝載的稠密嵌入模型，您必須在模型組態中明確定義 `dimension` 和 `space_type`，才能將模型與 `semantic` 欄位搭配使用。

自動產生的 `knn_vector` 子欄位支援其他設定，但目前無法在 `semantic` 欄位中設定。如需詳細資訊，請參閱[限制](#limitations)。
{: .note}

## 範例：稀疏編碼模型

設定模型後，您可以使用它建立含有 `semantic` 欄位的索引。此範例假設您已在叢集中設定 ID 為 `n17yX5cBsaYnPfyOzmQU` 的稀疏編碼模型：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG"
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引後，您可以擷取其對應，以確認已自動建立 `rank_features` 欄位：

```json
GET /my-nlp-index/_mapping
{
  "my-nlp-index": {
    "mappings": {
      "properties": {
        "passage": {
          "type": "semantic",
          "model_id": "nF7yX5cBsaYnPfyOq2SG",
          "raw_field_type": "text"
        },
        "passage_semantic_info": {
          "properties": {
            "embedding": {
              "type": "rank_features"
            },
            "model": {
              "properties": {
                "id": {
                  "type": "text",
                  "index": false
                },
                "name": {
                  "type": "text",
                  "index": false
                },
                "type": {
                  "type": "text",
                  "index": false
                }
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

## 參數

`semantic` 欄位類型支援下列參數。

| 參數                             | 資料類型                  | 可更新      | 必要/選用          | 說明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|----------------------------------|--------------------------|-----------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`                           | 字串                   | 否        | 必要          | 必須設定為 `semantic`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `raw_field_type`                 | 字串                   | 否        | 選用          | `semantic` 欄位所封裝的底層欄位類型。原始輸入會以此類型儲存在 `semantic` 欄位的路徑下，使其行為如同該類型的標準欄位。有效值為 `text`、`keyword`、`match_only_text`、`wildcard`、`token_count` 與 `binary`。預設值為 `text`。您可以使用底層欄位類型支援的任何參數；這些參數會如預期運作。                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `model_id`                       | 字串                   | 是       | 必要          | 在編製索引時用於從欄位值產生嵌入、以及在搜尋時從查詢輸入產生嵌入的 ML 模型 ID。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `search_model_id`                | 字串                   | 是       | 選用          | 專門用於查詢時產生嵌入的 ML 模型 ID。若未指定，則使用 `model_id`。不可與 `semantic_field_search_analyzer` 同時指定。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `semantic_info_field_name`       | 字串                   | 否        | 選用          | 儲存嵌入與模型資訊的內部中繼資料欄位的自訂名稱。預設情況下，此欄位名稱是在 `semantic` 欄位名稱後附加 `_semantic_info` 而得。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `chunking`                       | 布林值或對應表陣列 | 否        | 選用          | 在匯入時啟用長篇文字的分塊處理。設定為 `Yes` 可使用預設的固定詞元長度策略，或指定策略物件清單以依序套用多種分塊演算法。請參閱 [文字分塊](#text-chunking)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `semantic_field_search_analyzer` | 字串                   | 是       | 選用          | 指定在使用稀疏模型時用於斷詞查詢輸入的分析器。有效值為 `standard`、`bert-uncased` 與 `mbert-uncased`。不可與 `search_model_id` 同時使用。如需更多資訊，請參閱 [分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/)。                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `dense_embedding_config`         | 對應表                      | 否        | 選用          | 當 `semantic` 欄位由稠密嵌入模型支援時，為其所使用的底層 `knn_vector` 欄位定義自訂設定。這可對向量索引行為、相似度函式與引擎參數進行細緻控制。若省略，OpenSearch 會依據模型的嵌入維度與引擎預設值套用預設設定。如需支援的參數，請參閱 [稠密嵌入組態](#dense-embedding-configuration)。                                                                                                                                                                                                                                                                                                                                                                                                     |
| `sparse_encoding_config`         | 對應表                      | 否        | 選用          | 設定在使用稀疏模型時，`semantic` 欄位的稀疏向量編碼方式。支援 [`sparse_encoding` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/#pruning-sparse-vectors) 中所有可用的修剪策略。若省略，則使用 `max_ratio` 套用預設修剪策略，修剪比例為 `0.1`。這有助於降低雜訊與索引大小，同時保留稀疏向量中資訊量最高的維度。如需支援的參數，請參閱 [稀疏編碼組態](#sparse-encoding-configuration)。 |
| `skip_existing_embedding`        | 布林值                  | 是       | 選用          | 決定是否略過 `semantic` 欄位的嵌入產生。啟用時，OpenSearch 會檢查現有文件，確認 `semantic` 欄位是否已有嵌入，以及 `semantic` 欄位的值與用於產生嵌入的 ML 模型 ID 是否皆未變更。若兩項條件皆成立，OpenSearch 會重複使用現有的嵌入並略過產生。預設值為 `false`。                                                                                                                                                                                                                                                                                                                                                                                                                                 |


## 文字分塊

預設情況下，`semantic` 欄位的文字分塊功能為停用狀態。這是因為啟用分塊需要將每個區塊的嵌入儲存在巢狀物件中，這可能增加搜尋延遲。搜尋巢狀物件需要將子文件與其父文件聯結，並執行額外的評分與彙總邏輯。符合條件的子文件越多，潛在的延遲就越高。

如果您正在處理長篇文字，且想要改善搜尋相關性，可以透過 `semantic` 欄位的 `chunking` 參數啟用分塊。

### 基本分塊組態

若要啟用預設分塊行為（使用所有預設值的固定詞元長度），請將 `chunking` 設為 `true`：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG",
        "chunking": true
      }
    }
  }
}
```
{% include copy-curl.html %}

這相當於將 `algorithm` 設為 `fixed_token_length`：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG",
        "chunking": [
          {
            "algorithm": "fixed_token_length"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

分塊使用[固定詞元長度演算法]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-chunking/#the-fixed-token-length-algorithm)執行。 

### 進階分塊組態

若要設定進階分塊組態，您可以將 `chunking` 指定為分塊策略清單，其中每個策略會依序套用至 `semantic` 欄位。清單中的每個項目都必須指定 `algorithm` 及其參數。

例如，若要先套用 `delimiter` 演算法，再進行固定詞元分塊，請使用下列請求。文字會先在段落分隔處（`\n\n`）分割，再將產生的每個分段切分為固定大小的詞元區塊：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG",
        "chunking": [
          {
            "algorithm": "delimiter",
            "parameters": {
              "delimiter": "\n\n"
            }
          },
          {
            "algorithm": "fixed_token_length",
            "parameters": {
              "token_limit": 128,
              "overlap_rate": 0.2
            }
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

這讓您更能控制輸入文字的分割方式，並確保嵌入更能反映自然語言的邊界。

### 支援的演算法

`chunking` 參數支援[文字分塊匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-chunking/)支援的所有演算法。


## 稠密嵌入組態

當 `semantic` 欄位使用稠密模型時，OpenSearch 會自動產生伴隨的 `knn_vector` 欄位來儲存嵌入。您可以使用 `dense_embedding_config` 參數，自訂建立索引時此向量欄位的組態。

`dense_embedding_config` 的結構與標準 `knn_vector` 欄位的組態非常相似。您可以使用此參數來設定 k-NN 引擎和編製索引行為等設定。

如需 `dense_embedding_config` 支援的所有參數，請參閱 [k-NN 向量參數]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/#parameters)。雖然 `dense_embedding_config` 支援與 `knn_vector` 大致相同的選項，但不支援下列參數：

- `dimension`：嵌入維度必須與機器學習模型的輸出維度相符，且會自動從 `model_id` 推斷。您應在模型組態中設定正確的維度，而非在欄位對應中設定。

- `space_type`：相似度空間（例如 `cosinesimil`、`l2` 或 `innerproduct`）必須與模型一致，並由模型組態解析得出。

下列範例包含 `dense_embedding_config`：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG",
        "dense_embedding_config": {
          "method": {
            "name": "hnsw",
            "engine": "lucene",
            "parameters": {
              "ef_construction": 128,
              "m": 32
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 稀疏編碼組態

當 `semantic` 欄位使用稀疏模型時，OpenSearch 會自動產生伴隨欄位來儲存稀疏向量表示。預設情況下，會對此向量進行剪枝，以降低維度並提高效率。

`sparse_encoding_config` 參數可讓您透過指定策略及其參數，控制編碼期間套用剪枝的方式。這可讓您精細控制稀疏向量的編製索引方式，在準確度與儲存空間／效能之間取得平衡。

`sparse_encoding_config` 物件支援[稀疏編碼匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/#pruning-sparse-vectors)中所有可用的剪枝策略。

下列範例包含 `sparse_encoding_config`。它只保留稀疏向量中分數最高的 64 個詞彙：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "passage": {
        "type": "semantic",
        "model_id": "nF7yX5cBsaYnPfyOq2SG",
        "sparse_encoding_config": {
          "prune_type": "top_k",
          "prune_ratio": 64
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 語意欄位的匯入批次大小

當文件匯入包含 `semantic` 欄位的索引時，OpenSearch 會使用系統產生的資料匯入管線來呼叫底層機器學習模型並產生嵌入。為了最佳化效能，這些作業會以批次執行。 

您可以使用索引層級的動態 `index.neural_search.semantic_ingest_batch_size` 設定，控制此步驟中一起處理的文件數量。此設定指定匯入期間為 `semantic` 欄位產生嵌入時，一起批次處理的文件數量（預設為 `10`）。 

批次處理可減少模型推論的額外負擔，進而提高輸送量。然而，增加批次大小也可能增加記憶體用量。您應根據模型的效能特性與預期匯入量調整此設定。

此設定控制一個批次中一起處理的文件數量，但不會直接決定傳送至模型的輸入大小。
{: .note}

如果單一文件包含多個語意欄位，則會為每個欄位產生嵌入。
{: .note}

如果 `semantic` 欄位啟用了文字分塊，內容可能會分割成多個區塊，且會為每個區塊產生嵌入。因此，每個批次的實際模型推論呼叫次數與嵌入輸入總數，可能遠高於批次大小的值。
{: .note}

下列範例將 `my-index` 索引的匯入批次大小更新為 32。此變更會立即生效，並套用至後續匯入且包含 `semantic` 欄位的所有文件。

```json
PUT /my-index/_settings
{
  "index": {
    "neural_search.semantic_ingest_batch_size": 32
  }
}
```
{% include copy-curl.html %}

如需更新動態設定的詳細資訊，請參閱[更新動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#updating-a-dynamic-index-setting)。

## 限制

請注意 `semantic` 欄位的下列限制：

- 遠端叢集支援：跨叢集搜尋不支援對 `semantic` 欄位執行 `neural` 查詢。雖然您可以從遠端索引擷取文件，但語意查詢需要存取本機模型組態與索引對應。因此，您必須使用傳統查詢方法，直接對嵌入欄位執行查詢。

- 對應限制：`semantic` 欄位不支援動態對應，必須在索引對應中明確定義。此外，您無法在其他欄位的 `fields` 區段中使用 `semantic` 欄位，因此不支援多欄位組態。

## 後續步驟

- [將 `semantic` 欄位與文字嵌入模型搭配使用以進行語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/#using-a-semantic-field)
- [將 `semantic` 欄位與稀疏編碼模型搭配使用以進行神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/#using-a-semantic-field)