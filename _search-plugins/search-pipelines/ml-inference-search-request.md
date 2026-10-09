---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML 推論（請求）"
nav_order: 30
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# ML 推論搜尋請求處理器
於 2.16 版推出
{: .label .label-purple }

`ml_inference` 搜尋請求處理器用於呼叫已註冊的機器學習（ML）模型，以使用模型輸出改寫查詢。

**先決條件**<br>
使用 `ml_inference` 搜尋請求處理器之前，您必須具備託管於 OpenSearch 叢集上的本機 ML 模型，或透過 ML Commons 外掛程式連線至 OpenSearch 叢集的外部託管模型。如需本機模型的詳細資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。
如需外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
{: .note}

## 語法

以下是 `ml-inference` 搜尋請求處理器的語法：

```json
{
  "ml_inference": {
    "model_id": "<model_id>",
    "function_name": "<function_name>",
    "full_response_path": "<full_response_path>",
    "query_template": "<query_template>",
    "model_config": {
      "<model_config_field>": "<config_value>"
    },
    "model_input": "<model_input>",
    "input_map": [
      {
        "<model_input_field>": "<query_input_field>"
      }
    ],
    "output_map": [
      {
        "<query_output_field>": "<model_output_field>"
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 組態參數

下表列出 `ml-inference` 搜尋請求處理器的必要與選用參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
|:--| :--- |:---|:---|
| `model_id`| 字串 | 必要 | 處理器使用的 ML 模型 ID。 |
| `query_template` | 字串   | 選用  | 用於建構包含 `new_document_field` 的新查詢的查詢字串範本。常用於將搜尋查詢改寫為新的查詢類型。 |
| `function_name` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 處理器中設定的 ML 模型函式名稱。對於本機模型，有效值為 `sparse_encoding`、`sparse_tokenize`、`text_embedding` 和 `text_similarity`。對於外部託管模型，有效值為 `remote`。預設為 `remote`。   |
| `model_config` | 物件    | 選用   | ML 模型的自訂組態選項。對於外部託管模型，若設定此組態，則會覆寫預設的連接器參數。對於本機模型，您可以將 `model_config` 新增至 `model_input`，以覆寫註冊時設定的模型組態。如需詳細資訊，請參閱[`model_config` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-model_config-object)。  |
| `model_input` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 定義模型預期輸入欄位格式的範本。每種本機模型類型可能使用不同的輸入集合。對於外部託管模型，預設為 `"{ \"parameters\": ${ml_inference.parameters} }`。 |
| `input_map` | 陣列 | 必要  | 指定如何將查詢字串欄位對應至模型輸入欄位的陣列。陣列中的每個元素都是採用 `"<model_input_field>": "<query_input_field>"` 格式的對應，並對應至針對某個文件欄位的一次模型呼叫。如果未為外部託管模型指定輸入對應，則所有文件欄位都會直接傳遞至模型作為輸入。`input_map` 的大小表示模型呼叫次數（Predict API 請求數量）。 |
| `<model_input_field>`  | 字串    | 必要 | 模型輸入欄位名稱。  |
| `<query_input_field>`  | 字串    | 必要 | 用作模型輸入的查詢欄位名稱或 JSON 路徑。 |
| `output_map`  | 陣列 | 必要 | 指定如何將模型輸出欄位對應至查詢字串中新欄位的陣列。陣列中的每個元素都是採用 `"<query_output_field>": "<model_output_field>"` 格式的對應。 |
| `<query_output_field>` | 字串    | 必要 | 儲存模型輸出（由 `model_output` 指定）的查詢欄位名稱。  |
| `<model_output_field>` | 字串    | 必要 | 模型輸出中要儲存至 `query_output_field` 的欄位名稱或 JSON 路徑。  |
| `full_response_path`   | 布林值   | 選用  | 如果 `model_output_field` 包含欄位的完整 JSON 路徑而非欄位名稱，請將此參數設為 `true`。接著會完整剖析模型輸出，以取得該欄位的值。本機模型的預設為 `true`，外部託管模型的預設為 `false`。  |
| `ignore_missing`       | 布林值   | 選用  | 如果為 `true`，且缺少 `input_map` 或 `output_map` 中定義的任何輸入欄位，則會忽略此處理器。否則，缺少欄位會導致失敗。預設為 `false`。  |
| `ignore_failure` | 布林值   | 選用 | 指定處理器是否即使遇到錯誤也繼續執行。如果為 `true`，則會忽略此處理器並繼續搜尋。如果為 `false`，則任何失敗都會導致搜尋取消。預設為 `false`。  |
| `max_prediction_tasks` | 整數   | 選用  | 查詢搜尋期間可同時執行的模型呼叫數量上限。預設為 `10`。  |
| `description`          | 字串    | 選用   | 處理器的簡短說明。  |
| `tag`                  | 字串    | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。  |

`input_map` 和 `output_map` 對應支援標準 [JSON 路徑](https://github.com/json-path/JsonPath)表示法，用於指定複雜的資料結構。
{: .note}

## 使用處理器

請依照下列步驟在管線中使用處理器。建立處理器時，您必須提供模型 ID、`input_map` 和 `output_map`。測試使用此處理器的管線之前，請確認模型已成功部署。您可以使用 [Get Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/get-model/) 檢查模型狀態。

對於本機模型，您必須提供指定模型輸入格式的 `model_input` 欄位。將 `model_config` 中的任何輸入欄位新增至 `model_input`。

對於外部託管模型，`model_input` 欄位為選用，其預設值
為 `"{ \"parameters\": ${ml_inference.parameters} }`。

### 設定

建立名為 `my_index` 的索引，並將兩份文件編製索引：

```json
POST /my_index/_doc/1
{
  "passage_text": "I am excited",
  "passage_language": "en",
  "label": "POSITIVE",
  "passage_embedding": [
    2.3886719,
    0.032714844,
    -0.22229004
    ...]
}
```
{% include copy-curl.html %}

```json
POST /my_index/_doc/2
{
  "passage_text": "I am sad",
  "passage_language": "en",
  "label": "NEGATIVE",
  "passage_embedding": [
    1.7773438,
    0.4309082,
    1.8857422,
    0.95996094,
    ...]
}
```
{% include copy-curl.html %}

當您在建立的索引上執行詞彙查詢且未使用搜尋管線時，查詢會搜尋包含查詢所指定確切詞彙的文件。以下查詢不會傳回任何結果，因為查詢文字與索引中的任何文件都不相符：

```json
GET /my_index/_search
{
  "query": {
    "term": {
      "passage_text": {
        "value": "happy moments",
        "boost": 1
      }
    }
  }
}
```

透過使用模型，搜尋管線可以動態改寫詞彙值，根據模型推論改善或變更搜尋結果。這表示模型會從搜尋查詢取得初始輸入、處理該輸入，然後更新查詢詞彙以反映模型推論，進而可能提高搜尋結果的相關性。

### 範例：外部託管的模型

下列範例會使用外部託管的模型來設定 `ml_inference` 處理器。

**步驟 1：建立管線**

此範例示範如何為外部託管的情感分析模型建立搜尋管線，該模型會改寫詞彙查詢值。此模型需要 `inputs` 欄位，並在 `label` 欄位中產生結果。由於未指定 `function_name`，其預設為 `remote`，表示為外部託管的模型。

詞彙查詢值會根據模型的輸出進行改寫。搜尋請求中的 `ml_inference` 處理器需要 `input_map` 來擷取模型輸入的查詢欄位值，並需要 `output_map` 將模型輸出指派給查詢字串。

在此範例中，`ml_inference` 搜尋請求處理器用於下列詞彙查詢：

```json
 {
  "query": {
    "term": {
      "label": {
        "value": "happy moments",
        "boost": 1
      }
    }
  }
}
```

下列請求會建立搜尋管線，以改寫上述詞彙查詢：

```json
PUT /_search/pipeline/ml_inference_pipeline
{
  "description": "Generate passage_embedding for searched documents",
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "<your model id>",
        "input_map": [
          {
            "inputs": "query.term.label.value"
          }
        ],
        "output_map": [
          {
            "query.term.label.value": "label"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

對外部託管的模型發出 Predict API 請求時，所有必要的欄位與參數通常都包含在 `parameters` 物件中：

```json
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_predict
{
  "parameters": {
    "inputs": [
      {
        ...
      }
    ]
  }
}
```

因此，若要使用外部託管的情感分析模型，請以下列格式傳送 Predict API 請求：

```json
POST /_plugins/_ml/models/cywgD5EB6KAJXDLxyDp1/_predict
{
  "parameters": {
    "inputs": "happy moments"
  }
}
```
{% include copy-curl.html %}

模型會處理輸入，並根據輸入文字的情感產生預測。在此情況下，情感為正面：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "label": "POSITIVE",
            "score": "0.948"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

為外部託管的模型指定 `input_map` 時，您可以直接參照 `inputs` 欄位，而不必提供其點路徑 `parameters.inputs`：

```json
"input_map": [  
  {
    "inputs": "query.term.label.value"
  }
]
```

**步驟 2：執行管線**

建立搜尋管線後，您可以使用該搜尋管線執行相同的詞彙查詢：

```json
GET /my_index/_search?search_pipeline=my_pipeline_request_review
{
  "query": {
    "term": {
      "label": {
        "value": "happy moments",
        "boost": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢詞彙值會根據模型的輸出進行改寫。模型判定查詢詞彙的情感為正面，因此改寫後的查詢如下所示：

```json
{
  "query": {
    "term": {
      "label": {
        "value": "POSITIVE",
        "boost": 1
      }
    }
  }
}
```

回應包含 `label` 欄位值為 `POSITIVE` 的文件：

```json
{
  "took": 288,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.00009405752,
    "hits": [
      {
        "_index": "my_index",
        "_id": "3",
        "_score": 0.00009405752,
        "_source": {
          "passage_text": "I am excited",
          "passage_language": "en",
          "label": "POSITIVE"
        }
      }
    ]
  }
}
```

### 範例：本機模型

下列範例說明如何使用本機模型設定 `ml_inference` 處理器，將詞彙查詢改寫為 k-NN 查詢。

**步驟 1：建立管線**

下列範例說明如何為 `huggingface/sentence-transformers/all-distilroberta-v1` 本機模型建立搜尋管線。此模型是[預先訓練的句子轉換器模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sentence-transformers)，
託管於您的 OpenSearch 叢集中。

如果您使用 Predict API 叫用模型，則請求如下所示：

```json
POST /_plugins/_ml/_predict/text_embedding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs": [
    "today is sunny"
  ],
  "return_number": true,
  "target_response": [
    "sentence_embedding"
  ]
}
```

使用此結構描述，指定 `model_input` 如下：

```json
 "model_input": "{ \"text_docs\": ${input_map.text_docs}, \"return_number\": ${model_config.return_number}, \"target_response\": ${model_config.target_response} }"
```

在 `input_map` 中，將 `query.term.passage_embedding.value` 查詢欄位對應至模型預期的 `text_docs` 欄位：

```json
"input_map": [
  {
    "text_docs": "query.term.passage_embedding.value"
  } 
]
```

由於您將要轉換為嵌入的欄位指定為 JSON 路徑，因此需要將 `full_response_path` 設為 `true`。接著會剖析完整的 JSON 文件，以取得輸入欄位：

```json
"full_response_path": true
```

`query.term.passage_embedding.value` 欄位中的文字將用於產生嵌入：

```json
{
  "text_docs": "happy passage"
}
```

Predict API 請求會傳回下列回應：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "sentence_embedding",
          "data_type": "FLOAT32",
          "shape": [
            768
          ],
          "data": [
            0.25517133,
            -0.28009856,
            0.48519906,
            ...
          ]
        }
      ]
    }
  ]
}
```

模型會在 `$.inference_results.*.output.*.data` 欄位中產生嵌入。`output_map` 會將此欄位對應至查詢範本中的查詢欄位：

```json
"output_map": [
  {
    "modelPredictionOutcome": "$.inference_results.*.output.*.data"
  }
]
```

若要使用本機模型設定 `ml_inference` 搜尋請求處理器，請明確指定 `function_name`。在此範例中，`function_name` 為 `text_embedding`。如需有效 `function_name` 值的相關資訊，請參閱[組態參數](#configuration-parameters)。

以下是使用本機模型之 `ml_inference` 處理器的最終組態：

```json
PUT /_search/pipeline/ml_inference_pipeline_local
{
  "description": "searchs reviews and generates embeddings",
  "request_processors": [
    {
      "ml_inference": {
        "function_name": "text_embedding",
        "full_response_path": true,
        "model_id": "<your model id>",
        "model_config": {
          "return_number": true,
          "target_response": [
            "sentence_embedding"
          ]
        },
        "model_input": "{ \"text_docs\": ${input_map.text_docs}, \"return_number\": ${model_config.return_number}, \"target_response\": ${model_config.target_response} }",
        "query_template": """{
        "size": 2,
        "query": {
          "knn": {
            "passage_embedding": {
              "vector": ${modelPredictionOutcome},
              "k": 5
              }
            }
           }
          }""",
        "input_map": [
          {
            "text_docs": "query.term.passage_embedding.value"
          }
        ],
        "output_map": [
          {
            "modelPredictionOutcome": "$.inference_results.*.output.*.data"
          }
        ],
        "ignore_missing": true,
        "ignore_failure": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2：執行管線**

執行下列查詢，並在請求中提供管線名稱：

```json
GET /my_index/_search?search_pipeline=ml_inference_pipeline_local
{
"query": {
  "term": {
    "passage_embedding": {
      "value": "happy passage"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應確認處理器執行了 k-NN 查詢，其傳回分數較高的文件 1：

```json
{
  "took": 288,
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
    "max_score": 0.00009405752,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 0.00009405752,
        "_source": {
          "passage_text": "I am excited",
          "passage_language": "en",
          "label": "POSITIVE",
          "passage_embedding": [
            2.3886719,
            0.032714844,
            -0.22229004
            ...]
        }
      },
      {
        "_index": "my_index",
        "_id": "2",
        "_score": 0.00001405052,
        "_source": {
          "passage_text": "I am sad",
          "passage_language": "en",
          "label": "NEGATIVE",
          "passage_embedding": [
            1.7773438,
            0.4309082,
            1.8857422,
            0.95996094,
            ...
          ]
        }
      }
    ]
  }
}
```
