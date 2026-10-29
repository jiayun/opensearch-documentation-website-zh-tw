---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML 推論"
parent: Ingest processors
nav_order: 215
redirect_from:
- /api-reference/ingest-apis/processors/ml-inference/
---

# ML 推論處理器

`ml_inference` 處理器會呼叫已在 OpenSearch 中註冊的[機器學習（ML）模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)。模型輸出會作為新欄位新增至匯入的文件中。

**先決條件**<br>
使用 `ml_inference` 處理器之前，您必須具備託管於 OpenSearch 叢集上的本機 ML 模型，或已連線至 OpenSearch 叢集的外部託管模型。如需本機模型的詳細資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。如需外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。 
{: .note}

## 語法

以下是 `ml_inference` 處理器的語法：

```json
{
  "ml_inference": {
    "model_id": "<model_id>",
    "function_name": "<function_name>",
    "full_response_path": "<full_response_path>",
    "model_config":{
      "<model_config_field>": "<config_value>"
    },
    "model_input": "<model_input>",
    "input_map": [
      {
        "<model_input_field>": "<document_field>"
      }
    ],
    "output_map": [
      {
        "<new_document_field>": "<model_output_field>"
      }
    ],
    "override": "<override>"
  }
}
```
{% include copy.html %}

## 參數

下表列出 `ml_inference` 處理器的必要與選用參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
|:--- | :--- | :--- | :--- |
| `model_id` | 字串 | 必要 | 處理器所使用的 ML 模型 ID。 |
| `function_name` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 處理器中設定的 ML 模型函式名稱。對於本機模型，有效值為 `sparse_encoding`、`sparse_tokenize`、`text_embedding` 與 `text_similarity`。對於外部託管模型，有效值為 `remote`。預設為 `remote`。 |
| `model_config` | 物件    | 選用   | ML 模型的自訂組態選項。對於外部託管模型，若設定此項，此組態會覆寫預設的連接器參數。對於本機模型，您可以新增 `model_config` 至 `model_input` 來覆寫註冊時設定的模型組態。如需更多資訊，請參閱 [`model_config` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-model_config-object)。 |
| `model_input`  | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 定義模型預期輸入欄位格式的範本。每種本機模型類型可能使用不同的輸入集合。對於外部託管模型，預設為 `"{ \"parameters\": ${ml_inference.parameters} }`。|
| `input_map` | 陣列 | 外部託管模型為選用<br/><br/>本機模型為必要 | 指定如何將匯入文件欄位對應到模型輸入欄位的陣列。陣列的每個元素都是 `"<model_input_field>": "<document_field>"` 格式的對應，並對應到一個文件欄位的一次模型呼叫。若未為外部託管模型指定輸入對應，則文件的所有欄位會直接作為輸入傳遞給模型。`input_map` 的大小表示模型被呼叫的次數（Predict API 請求的數量）。 |
| `<model_input_field>` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要  | 模型輸入欄位名稱。 |
| `<document_field>`   | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 作為模型輸入的匯入文件欄位名稱或 JSON 路徑。 |
| `output_map` | 陣列 | 外部託管模型為選用<br/><br/>本機模型為必要 | 指定如何將模型輸出欄位對應到匯入文件中新欄位的陣列。陣列的每個元素都是 `"<new_document_field>": "<model_output_field>"` 格式的對應。|
| `<new_document_field>`   | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 匯入文件中新欄位的名稱，模型的輸出（由 `model_output` 指定）會儲存在此欄位。若未為外部託管模型指定輸出對應，則模型輸出的所有欄位都會新增到新的文件欄位。 |
| `<model_output_field>` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 模型輸出中要儲存到 `new_document_field` 的欄位名稱或 JSON 路徑。 |
| `full_response_path` | 布林值   | 選用   | 若 `model_output_field` 包含欄位的完整 JSON 路徑而非欄位名稱，請將此參數設為 `true`。屆時模型輸出會被完整解析以取得該欄位的值。本機模型預設為 `true`，外部託管模型預設為 `false`。 |
| `ignore_missing` | 布林值   | 選用  | 若設為 `true`，且 `input_map` 或 `output_map` 中定義的任何輸入欄位遺漏，則會忽略遺漏的欄位。否則，欄位遺漏會導致失敗。預設為 `false`。 |
| `ignore_failure` | 布林值   | 選用  | 指定即使遇到錯誤，處理器是否仍繼續執行。若為 `true`，則任何失敗都會被忽略，匯入繼續進行。若為 `false`，則任何失敗都會導致匯入取消。預設為 `false`。 |
| `override` | 布林值   | 選用   | 當匯入文件已包含 `<new_document_field>` 中指定名稱的欄位時適用。若 `override` 為 `false`，則略過輸入欄位。若為 `true`，則現有欄位值會被新的模型輸出覆寫。預設為 `false`。 |
| `max_prediction_tasks`  | 整數   | 選用  | 文件匯入期間可同時執行的模型呼叫數量上限。預設為 `10`。 |
| `description` | 字串    | 選用  | 處理器的簡短說明。 |
| `if` | 包含布林運算式的字串 | 選用 | 執行處理器的條件。 |
| `on_failure` | 清單 | 選用 | 處理器失敗時要執行的處理器清單。 |
| `tag` | 字串    | 選用 | 處理器的識別標籤。可用於除錯，以區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |

`input_map` 與 `output_map` 對應支援標準的 [JSON 路徑](https://github.com/json-path/JsonPath)標記法，用於指定複雜的資料結構。 
{: .note}

## 使用處理器

請依照下列步驟在管線中使用處理器。建立處理器時，您必須提供模型 ID。使用處理器測試管線或匯入文件之前，請確定模型已成功部署。您可以使用 [Get Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/get-model/) 檢查模型狀態。

若為本機模型，您必須提供指定模型輸入格式的 `model_input` 欄位。將 `model_config` 中的所有輸入欄位新增至 `model_input`。

若為遠端模型，`model_input` 欄位為選用，其預設值為 `"{ \"parameters\": ${ml_inference.parameters} }`。

### 範例：外部託管的模型

下列範例會使用外部託管的模型來設定 `ml_inference` 處理器。

#### 步驟 1：建立管線

下列範例會為外部託管的文字嵌入模型建立資料匯入管線。此模型需要 `input` 欄位，並在 `data` 欄位中產生結果。它會將 `passage_text` 欄位中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_embedding` 欄位中。處理器組態未明確指定 `function_name`，因此其預設值為 `remote`，表示使用外部託管的模型：

```json
PUT /_ingest/pipeline/ml_inference_pipeline
{
  "description": "Generate passage_embedding for ingested documents",
  "processors": [
    {
      "ml_inference": {
        "model_id": "<your model id>",
        "input_map": [
          {
            "input": "passage_text"
          }
        ],
        "output_map": [
          {
            "passage_embedding": "data"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

對於傳送至外部託管模型的 Predict API 請求，所有欄位通常都巢狀置於 `parameters` 物件內：

```json
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_predict
{
  "parameters": {
    "input": [
      {
        ...
      }
    ]
  }
}
```

為外部託管模型指定 `input_map` 時，您可以直接參照 `input` 欄位，而無須提供其點分隔路徑 `parameters.input`：

```json
"input_map": [
  {
    "input": "passage_text"
  }
]
```

#### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/ml_inference_pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "passage_text": "hello world"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會確認處理器已在 `passage_embedding` 欄位中產生文字嵌入。該文件現在同時包含 `passage_text` 與 `passage_embedding` 欄位：

```json
{
  "docs" : [
    {
      "doc" : {
        "_index" : "testindex1",
        "_id" : "1",
        "_source" : {
          "passage_embedding" : [
            0.017304314,
            -0.021530833,
            0.050184276,
            0.08962978,
            ...
          ],
          "passage_text" : "hello world"
        },
        "_ingest" : {
          "timestamp" : "2023-10-11T22:35:53.654650086Z"
        }
      }
    }
  ]
}
```

建立資料匯入管線之後，您需要建立一個索引來進行匯入，並將文件匯入該索引。
{: .note}

### 範例：本機模型

下列範例會使用本機模型設定 `ml_inference` 處理器。

#### 步驟 1：建立管線

下列範例會為 `huggingface/sentence-transformers/all-distilroberta-v1` 本機模型建立資料匯入管線。此模型是託管於您 OpenSearch 叢集中的句子轉換器[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sentence-transformers)。

如果您使用 Predict API 叫用模型，請求看起來如下：

```json
POST /_plugins/_ml/_predict/text_embedding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```

使用此結構描述，依下列方式指定 `model_input`：

```json
 "model_input": "{ \"text_docs\": ${input_map.text_docs}, \"return_number\": ${model_config.return_number}, \"target_response\": ${model_config.target_response} }"
```

在 `input_map` 中，將 `book.*.chunk.text.*.context` 文件欄位對應至模型預期的 `text_docs` 欄位：

```json
"input_map": [
  {
    "text_docs": "book.*.chunk.text.*.context"
  }
]
```

由於您將要轉換為嵌入的欄位指定為 JSON 路徑，因此需要將 `full_response_path` 設為 `true`，以便剖析完整的 JSON 文件來取得輸入欄位：

```json
"full_response_path": true
```

您編製索引的文件會如下所示。`context` 欄位中的文字將用於產生嵌入：

```json
"book": [
  {
    "chunk": {
      "text": [
        {
          "chapter": "first chapter",
          "context": "this is the first part"
        }
      ]
    }
  }
]
```

Predict API 請求會傳回下列回應：

```json
{
  "inference_results" : [
    {
      "output" : [
        {
          "name" : "sentence_embedding",
          "data_type" : "FLOAT32",
          "shape" : [
            768
          ],
          "data" : [
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

模型會在 `$.inference_results.*.output.*.data` 欄位中產生嵌入。`output_map` 會將此欄位對應至匯入文件中新建立的 `book.*.chunk.text.*.context_embedding` 欄位：

```json
"output_map": [
  {
    "book.*.chunk.text.*.context_embedding": "$.inference_results.*.output.*.data"
  }
]
```

若要使用本機模型設定 `ml_inference` 處理器，請明確指定 `function_name`。在此範例中，`function_name` 為 `text_embedding`。如需有效 `function_name` 值的相關資訊，請參閱[參數](#parameters)。

在此範例中，使用本機模型的 `ml_inference` 處理器最終組態如下：

```json
PUT /_ingest/pipeline/ml_inference_pipeline_local
{
  "description": "ingests reviews and generates embeddings",
  "processors": [
    {
      "ml_inference": {
        "function_name": "text_embedding",
        "full_response_path": true,
        "model_id": "<your model id>",
        "model_config": {
          "return_number": true,
          "target_response": ["sentence_embedding"]
        },
        "model_input": "{ \"text_docs\": ${input_map.text_docs}, \"return_number\": ${model_config.return_number}, \"target_response\": ${model_config.target_response} }",
        "input_map": [
          {
            "text_docs": "book.*.chunk.text.*.context"
          }
        ],
        "output_map": [
          {
            "book.*.chunk.text.*.context_embedding": "$.inference_results.*.output.*.data"
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

#### 步驟 2（選用）：測試管線

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/ml_inference_pipeline/_simulate
{
  "docs": [
    {
      "_index": "my_books",
      "_id": "1",
      "_source": {
        "book": [
          {
            "chunk": {
              "text": [
                {
                  "chapter": "first chapter",
                  "context": "this is the first part"
                },
                {
                  "chapter": "first chapter",
                  "context": "this is the second part"
                }
              ]
            }
          },
          {
            "chunk": {
              "text": [
                {
                  "chapter": "second chapter",
                  "context": "this is the third part"
                },
                {
                  "chapter": "second chapter",
                  "context": "this is the fourth part"
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會確認處理器已在 `context_embedding` 欄位中產生文字嵌入。該文件現在在相同路徑下同時包含 `context` 與 `context_embedding` 欄位：

```json
{
  "docs" : [
    {
      "doc" : {
        "_index": "my_books",
        "_id": "1",
        "_source": {
          "book": [
            {
              "chunk": {
                "text": [
                  {
                    "chapter": "first chapter",
                    "context": "this is the first part",
                    "context_embedding": [
                      0.15756914,
                      0.05150984,
                      0.25225413,
                      0.4941875,
                      ...
                    ]
                  },
                  {
                    "chapter": "first chapter",
                    "context": "this is the second part",
                    "context_embedding": [
                      0.10526893,
                      0.026559234,
                      0.28763372,
                      0.4653795,
                      ...
                    ]
                  }
                ]
              }
            },
            {
              "chunk": {
                "text": [
                  {
                    "chapter": "second chapter",
                    "context": "this is the third part",
                    "context_embedding": [
                      0.017304314,
                      -0.021530833,
                      0.050184276,
                      0.08962978,
                      ...
                    ]
                  },
                  {
                    "chapter": "second chapter",
                    "context": "this is the fourth part",
                    "context_embedding": [
                      0.37742054,
                      0.046911318,
                      1.2053889,
                      0.04663613,
                      ...
                    ]
                  }
                ]
              }
            }
          ]
        }
      }
    }
  ]
}
```

建立資料匯入管線之後，您需要建立一個索引來進行匯入，並將文件匯入該索引。
{: .note}

## 後續步驟

- 如需在匯入期間產生文字與影像嵌入的完整範例，請參閱[使用 ML 推論處理器進行多模態搜尋]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-search/multimodal-search-ml-inference/)。
- 如需在匯入期間偵測文件語言的完整範例，請參閱[為多語言搜尋識別文件語言]({{site.url}}{{site.baseurl}}/tutorials/language-identification/)。
- 如需為文字區塊產生嵌入的完整範例，請參閱[使用文字區塊化進行語意搜尋]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-search/long-document/)。