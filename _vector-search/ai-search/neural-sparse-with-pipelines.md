---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動產生稀疏向量嵌入"
parent: Neural sparse search
grand_parent: AI search
nav_order: 10
has_children: false
redirect_from:
  - /search-plugins/neural-sparse-with-pipelines/
---

# 自動產生稀疏向量嵌入

自動產生稀疏向量嵌入可讓神經稀疏搜尋像詞彙搜尋一樣運作。若要利用此封裝，請設定資料匯入管線，在匯入期間從文件文字建立並儲存稀疏向量嵌入。查詢時，輸入純文字，系統會自動將其轉換為向量嵌入以供搜尋。

神經稀疏搜尋的運作方式如下：

- 匯入時，神經稀疏搜尋會使用稀疏編碼模型，從文字欄位產生稀疏向量嵌入。

- 查詢時，神經稀疏搜尋會以下列兩種搜尋模式之一運作：

    - **僅文件模式 (預設)**：稀疏編碼模型會在匯入時從文件產生稀疏向量嵌入。查詢時，神經稀疏搜尋會將查詢文字斷詞，並從查閱表中取得詞元權重。此方法可提供更快的擷取速度，但會稍微降低搜尋相關性。查詢時的斷詞可由下列元件執行：
      - **DL 模型分析器 (預設)**：[DL 模型分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/dl-model-analyzers/) 使用內建的 ML 模型。此方法可提供更快的擷取速度，但會稍微降低搜尋相關性。
      - **自訂斷詞器**：您可以使用 [Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/) 部署自訂斷詞器，為查詢文字斷詞。此方法提供更大的彈性，同時在您的神經稀疏搜尋實作中維持一致的斷詞方式。

    - **雙編碼器模式**：稀疏編碼模型會同時從文件和查詢文字產生稀疏向量嵌入。此方法可提供更好的搜尋相關性，但會增加延遲。

我們建議使用搭配 DL 分析器的預設僅文件模式，因為對大多數使用案例而言，它能在效能與相關性之間取得最佳平衡。
{: tip}

搭配分析器的預設僅文件模式運作方式如下：

1. 匯入時：
   - 您註冊的稀疏編碼模型會產生稀疏向量嵌入。
   - 這些嵌入會以詞元權重配對的形式儲存在您的索引中。

2. 搜尋時：
   - 查詢文字會使用內建的 DL 模型分析器進行分析 (該分析器使用對應的內建 ML 模型斷詞器)。
   - 詞元權重會從 OpenSearch 內建的預先計算查閱表中取得。
   - 斷詞結果會與稀疏編碼模型的預期相符，因為兩者使用相同的斷詞配置。

因此，您必須在匯入時選擇並套用 ML 模型，但在搜尋時只需指定分析器 (而非模型)。

## 稀疏編碼模型/分析器相容性

下表列出所有可用於僅文件模式的模型。每個模型都搭配其相容的分析器，應在搜尋時使用。請根據您的語言需求（英文或多語言）和效能需求來選擇。

| 模型                                                                    | 分析器        | BEIR 相關性 | MIRACL 相關性 | 模型參數 |
| ------------------------------------------------------------------------ | --------------- | -------------- | ---------------- | ---------------- |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v1`          | `bert-uncased`  | 0.490          | N/A              | 133M             |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-distill`  | `bert-uncased`  | 0.504          | N/A              | 67M              |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-mini`     | `bert-uncased`  | 0.497          | N/A              | 23M              |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill`  | `bert-uncased`  | 0.517          | N/A              | 67M              |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte`       | `bert-uncased`  | 0.546          | N/A              | 133M             |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-multilingual-v1` | `mbert-uncased` | 0.500          | 0.629            | 168M             |

## 範例：使用搭配分析器的預設僅文件模式

此範例使用建議的 **僅文件** 模式搭配 **DL 模型分析器**。在此模式中，OpenSearch 會在匯入時套用稀疏編碼模型，並在搜尋時套用相容的 DL 模型分析器。如需其他模式的範例，請參閱[使用自訂組態進行神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-custom/)。

在此範例中，您將使用神經稀疏搜尋，並搭配 OpenSearch 內建的機器學習 (ML) 模型代管與資料匯入管線。由於文字轉換為嵌入的作業是在 OpenSearch 內執行，因此您在匯入及搜尋文件時將使用文字。

### 先決條件

開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/#prerequisites)。

### 步驟 1：設定用於匯入的稀疏編碼模型

若要使用僅文件模式，請先[選擇稀疏編碼模型](#sparse-encoding-modelanalyzer-compatibility) 以供匯入時使用。然後註冊並部署模型。例如，若要註冊並部署 `opensearch-neural-sparse-encoding-doc-v3-distill` 模型，請使用下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊模型是非同步工作。OpenSearch 會為您註冊的每個模型傳回一個工作 ID：

```json
{
  "task_id": "aFeif4oB5Vm0Tdw8yoN7",
  "status": "CREATED"
}
```

您可以呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 來檢查工作狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

工作完成後，工作狀態會變更為 `COMPLETED`，且 ML Tasks API 回應會包含已註冊模型之模型的 ID：

```json
{
  "model_id": "<model ID>",
  "task_type": "REGISTER_MODEL",
  "function_name": "SPARSE_ENCODING",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

請記下您所建立模型的 `model_id`；後續步驟會用到。

### 步驟 2：建立資料匯入管線

若要產生稀疏向量嵌入，您需要建立包含 [`sparse_encoding` 處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/sparse-encoding/) 的[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，該處理器會將文件欄位中的文字轉換為向量嵌入。處理器的 `field_map` 會決定要從哪些輸入欄位產生向量嵌入，以及要在哪些輸出欄位中儲存嵌入。

下列範例請求會建立資料匯入管線，其中 `passage_text` 的文字會轉換為稀疏向量嵌入，並儲存在 `passage_embedding` 中。請在請求中提供已註冊模型的模型 ID：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline-sparse
{
  "description": "An sparse encoding ingest pipeline",
  "processors": [
    {
      "sparse_encoding": {
        "model_id": "<bi-encoder or doc-only model ID>",
        "prune_type": "max_ratio",
        "prune_ratio": 0.1,
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要將長文字分割為段落，請在 `sparse_encoding` 處理器之前使用 `text_chunking` 匯入處理器。如需詳細資訊，請參閱[文字區塊化]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

### 步驟 3：建立用於匯入的索引

若要使用管線中定義的稀疏編碼處理器，請建立 rank features 索引，並將上一步建立的管線新增為預設管線。請確保 `field_map` 中定義的欄位已對應為正確的類型。延續先前的範例，`passage_embedding` 欄位必須對應為 [`rank_features`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/#rank-features)。同樣地，`passage_text` 欄位必須對應為 `text`。

下列範例請求會建立一個設定了預設資料匯入管線的 rank features 索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "default_pipeline": "nlp-ingest-pipeline-sparse"
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要節省磁碟空間，您可以依照下列方式將嵌入向量從來源中排除：

```json
PUT /my-nlp-index
{
  "settings": {
    "default_pipeline": "nlp-ingest-pipeline-sparse"
  },
  "mappings": {
    "_source": {
      "excludes": [
        "passage_embedding"
      ]
    },
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

一旦 `<token, weight>` 配對從來源中排除，就無法復原。在套用此最佳化之前，請確認您的應用程式不需要 `<token, weight>` 配對。
{: .important}

### 步驟 4：將文件匯入索引

若要將文件匯入上一步建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/2
{
  "passage_text": "Hi planet",
  "id": "s2"
}
```
{% include copy-curl.html %}

在文件匯入索引之前，資料匯入管線會對文件執行 `sparse_encoding` 處理器，為 `passage_text` 欄位產生向量嵌入。編製索引後的文件包含 `passage_text` 欄位（其中包含原始文字），以及 `passage_embedding` 欄位（其中包含向量嵌入）。


### 步驟 5：搜尋資料

若要對索引執行神經稀疏搜尋，請在 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/) 查詢中使用 `neural_sparse` 查詢子句。

下列範例請求使用 `neural_sparse` 查詢，以原始文字查詢搜尋相關文件。請指定與您所選模型相容的 `analyzer`（請參閱 [稀疏編碼模型／分析器相容性](#sparse-encoding-modelanalyzer-compatibility)）：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "analyzer": "bert-uncased"
      }
    }
  }
}
```
{% include copy-curl.html %}

如果您未指定分析器，則會使用預設的 `bert-uncased` 分析器。因此，此查詢等同於前一個查詢：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
  "took" : 688,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 30.0029,
    "hits" : [
      {
        "_index" : "my-nlp-index",
        "_id" : "1",
        "_score" : 30.0029,
        "_source" : {
          "passage_text" : "Hello world",
          "passage_embedding" : {
            "!" : 0.8708904,
            "door" : 0.8587369,
            "hi" : 2.3929274,
            "worlds" : 2.7839446,
            "yes" : 0.75845814,
            "##world" : 2.5432441,
            "born" : 0.2682308,
            "nothing" : 0.8625516,
            "goodbye" : 0.17146169,
            "greeting" : 0.96817183,
            "birth" : 1.2788506,
            "come" : 0.1623208,
            "global" : 0.4371151,
            "it" : 0.42951578,
            "life" : 1.5750692,
            "thanks" : 0.26481047,
            "world" : 4.7300377,
            "tiny" : 0.5462298,
            "earth" : 2.6555297,
            "universe" : 2.0308156,
            "worldwide" : 1.3903781,
            "hello" : 6.696973,
            "so" : 0.20279501,
            "?" : 0.67785245
          },
          "id" : "s1"
        }
      },
      {
        "_index" : "my-nlp-index",
        "_id" : "2",
        "_score" : 16.480486,
        "_source" : {
          "passage_text" : "Hi planet",
          "passage_embedding" : {
            "hi" : 4.338913,
            "planets" : 2.7755864,
            "planet" : 5.0969057,
            "mars" : 1.7405145,
            "earth" : 2.6087382,
            "hello" : 3.3210192
          },
          "id" : "s2"
        }
      }
    ]
  }
}
```

若要將與稀疏嵌入來源相關的磁碟與網路 I/O 延遲降到最低，您可以依照下列方式在查詢中排除嵌入向量來源：

```json
GET my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "analyzer": "bert-uncased"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 雙編碼器模式

在雙編碼器模式中，請註冊並部署一個雙編碼器模型，以便在匯入與查詢時使用：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

部署完成後，使用相同的 `model_id` 進行搜尋：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "model_id": "<bi-encoder model_id>"
      }
    }
  }
}
```
{% include copy-curl.html %}

完整範例請參閱 [使用自訂組態進行神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-custom/)。

## 搭配自訂斷詞器的僅文件模式

您可以搭配自訂斷詞器使用僅文件模式。若要部署斷詞器，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1",
  "version": "1.0.1",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

部署完成後，在查詢中使用斷詞器的 `model_id`：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world",
        "model_id": "<tokenizer model_id>"
      }
    }
  }
}
```
{% include copy-curl.html %}

完整範例請參閱 [使用自訂組態進行神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-custom/)。

## 使用語意欄位

使用 `semantic` 欄位可簡化神經稀疏搜尋的組態。若要使用 `semantic` 欄位，請依照下列步驟操作。如需更多資訊，請參閱 [語意欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/)。

### 步驟 1：註冊並部署稀疏編碼模型

首先，依照 [步驟 1](#step-1-register-and-deploy-a-sparse-encoding-model) 所述註冊並部署稀疏編碼模型。

## 步驟 2：建立含有語意欄位以供匯入的索引

前一步驟中設定的稀疏編碼模型會在匯入時用於產生稀疏向量嵌入。使用 `semantic` 欄位時，請將 `model_id` 設定為用於匯入的模型 ID。若為僅文件模式，您還可以在 `search_model_id` 欄位中提供其 ID，以指定查詢時要使用的模型。

下列範例示範如何使用稀疏編碼模型，建立一個在僅文件模式下設定 `semantic` 欄位的索引。若要啟用將長文字自動拆分為較小段落的機制，請在語意欄位組態中將 `chunking` 設為 `true`：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_text": {
        "type": "semantic",
         "model_id": "_kPwYJcBmp4cG9LrUQsE",
         "search_model_id": "AUPwYJcBmp4cG9LrmQy8",
         "chunking": true
      }
    }
  }
}
```
{% include copy-curl.html %}

建立索引後，您可以擷取其對應，以驗證嵌入欄位是否已自動建立：

```json
GET /my-nlp-index/_mapping
{
   "my-nlp-index": {
      "mappings": {
         "properties": {
            "id": {
               "type": "text"
            },
            "passage_text": {
               "type": "semantic",
               "model_id": "_kPwYJcBmp4cG9LrUQsE",
               "search_model_id": "AUPwYJcBmp4cG9LrmQy8",
               "raw_field_type": "text",
               "chunking": true
            },
            "passage_text_semantic_info": {
               "properties": {
                  "chunks": {
                     "type": "nested",
                     "properties": {
                        "embedding": {
                           "type": "rank_features"
                        },
                        "text": {
                           "type": "text"
                        }
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

系統會自動建立名為 `passage_text_semantic_info` 的物件欄位。其中包含用於儲存嵌入的 `rank_features` 子欄位，以及用於擷取模型中繼資料的其他文字欄位。

### 步驟 3：將文件匯入索引

若要將文件匯入前一步驟建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/2
{
  "passage_text": "Hi planet",
  "id": "s2"
}
```
{% include copy-curl.html %}

在文件匯入索引之前，OpenSearch 會自動將文字分塊，並為每個區塊產生稀疏向量嵌入。若要驗證嵌入是否正確產生，您可以執行搜尋請求來擷取該文件：

```json
GET /my-nlp-index/_doc/1
{
   "_index": "my-nlp-index",
   "_id": "1",
   "_version": 1,
   "_seq_no": 0,
   "_primary_term": 1,
   "found": true,
   "_source": {
      "passage_text": "Hello world",
      "passage_text_semantic_info": {
         "chunks": [
            {
               "text": "Hello world",
               "embedding": {
                  "hi": 0.5843902,
                  ...
               }
            }
         ],
         "model": {
            "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill",
            "id": "_kPwYJcBmp4cG9LrUQsE",
            "type": "SPARSE_ENCODING"
         }
      },
      "id": "s1"
   }
}
```
{% include copy-curl.html %}

## 步驟 3：搜尋資料

若要搜尋語意欄位的嵌入，請在 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/) 查詢中使用 `neural` 查詢子句。

下列範例使用 `neural` 查詢，以文字輸入搜尋相關文件。您只需指定 `semantic` 欄位名稱---OpenSearch 會自動改寫查詢並套用至底層的嵌入欄位，並適當處理任何巢狀物件。查詢中無需提供 `model_id`，因為 OpenSearch 會從索引對應中 `semantic` 欄位的組態取得該值：

```json
GET my-nlp-index/_search
{
   "_source": {
      "excludes": [
         "passage_text_semantic_info"
      ]
   },
   "query": {
      "neural": {
         "passage_text": {
            "query_text": "Hi world"
         }
      }
   }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
   "took": 19,
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
      "max_score": 6.437132,
      "hits": [
         {
            "_index": "my-nlp-index",
            "_id": "1",
            "_score": 6.437132,
            "_source": {
               "passage_text": "Hello world",
               "id": "s1"
            }
         },
         {
            "_index": "my-nlp-index",
            "_id": "2",
            "_score": 5.063226,
            "_source": {
               "passage_text": "Hi planet",
               "id": "s2"
            }
         }
      ]
   }
}
```

或者，您可以使用內建的分析器來對查詢文字進行斷詞：

```json
GET my-nlp-index/_search
{
   "_source": {
      "excludes": [
         "passage_text_semantic_info"
      ]
   },
   "query": {
      "neural": {
         "passage_text": {
            "query_text": "Hi world",
            "semantic_field_search_analyzer": "bert-uncased"
         }
      }
   }
}
```
{% include copy-curl.html %}

若要進一步簡化查詢，您可以在 `semantic` 欄位組態中定義 `semantic_field_search_analyzer`。如此一來，您就可以在查詢本身省略分析器，因為 OpenSearch 會在搜尋時自動套用設定的分析器。

## 加速神經稀疏搜尋

若要深入了解如何改善神經稀疏搜尋的擷取時間，請參閱 [加速神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/#accelerating-neural-sparse-search)。

如果您將 `semantic` 欄位與 `neural` 查詢搭配使用，則不支援查詢加速。您可以透過直接對底層的 `rank_features` 欄位執行 `neural_sparse` 查詢來達到加速效果。
{: .note}

## 疑難排解

本節包含在執行神經稀疏搜尋時，解決常見問題的相關資訊。

### 遠端連接器節流例外

使用連接器呼叫遠端服務 (例如 Amazon SageMaker) 時，匯入和搜尋呼叫有時會因為遠端連接器節流例外而失敗。

在早於 2.15 的 OpenSearch 版本中，節流例外會以遠端服務的錯誤形式傳回：

```json
{
  "type": "status_exception",
  "reason": "Error from remote service: {\"message\":null}"
}
```

若要減輕節流例外，請降低連接器的 [`client_config`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields) 物件中 `max_connection` 設定所指定的最大連線數。這麼做可避免並行連線數上限超過遠端服務的閾值。您也可以修改重試設定，以避免匯入期間的請求暴增。

## 後續步驟

- 若要了解如何使用自訂神經稀疏搜尋組態，請參閱[使用自訂組態進行神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-custom/)。
- 若要進一步了解如何改善神經稀疏搜尋的擷取時間，請參閱[加速神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/#accelerating-neural-sparse-search)。
- 若要了解如何建置 AI 搜尋應用程式，請探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)。 
