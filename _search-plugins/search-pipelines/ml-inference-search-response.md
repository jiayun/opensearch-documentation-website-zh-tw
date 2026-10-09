---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML 推論 (回應)"
nav_order: 40
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# ML 推論搜尋回應處理器
於 2.16 版導入
{: .label .label-purple }

`ml_inference` 搜尋回應處理器用於呼叫已註冊的機器學習 (ML) 模型，將其輸出納入搜尋結果文件中的新欄位。

**必要條件**<br>
使用 `ml_inference` 搜尋回應處理器之前，您必須擁有託管在 OpenSearch 叢集上的本機 ML 模型，或透過 ML Commons 外掛程式連線至 OpenSearch 叢集的外部託管模型。如需本機模型的詳細資訊，請參閱 [在 OpenSearch 內使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。如需外部託管模型的詳細資訊，請參閱 [連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
{: .note}

## 語法

以下是 `ml-inference` 搜尋回應處理器的語法：

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
    "override": "<override>",
    "one_to_one": false
  }
}
```
{% include copy-curl.html %}

## 請求本文欄位

下表列出 `ml-inference` 搜尋回應處理器的必要與選用參數。

| 參數 | 資料類型 | 必要/選用 | 說明  |
|:--| :--- | :--- |:---|
| `model_id` | 字串 | 必要 | 處理器所使用的 ML 模型 ID。 |
| `function_name`        | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 處理器中設定的 ML 模型函式名稱。對於本機模型，有效值為 `sparse_encoding`、`sparse_tokenize`、`text_embedding` 和 `text_similarity`。對於外部託管模型，有效值為 `remote`。預設為 `remote`。 |
| `model_config`         | 物件    | 選用   | ML 模型的自訂組態選項。對於外部託管模型，若設定此項，此組態會覆寫預設的連接器參數。對於本機模型，您可以在 `model_input` 中加入 `model_config`，以覆寫註冊時設定的模型組態。如需詳細資訊，請參閱 [`model_config` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-model_config-object)。 |
| `model_input`          | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 定義模型所預期輸入欄位格式的範本。每種本機模型類型可能使用不同的輸入集合。對於外部託管模型，預設為 `"{ \"parameters\": ${ml_inference.parameters} }`。 |
| `input_map`            | 陣列 | 外部託管模型為選用<br/><br/>本機模型為必要 | 一個陣列，指定如何將搜尋回應中的文件欄位對應到模型輸入欄位。陣列的每個元素都是 `"<model_input_field>": "<document_field>"` 格式的對應，並對應至一個文件欄位的一次模型呼叫。若外部託管模型未指定輸入對應，則所有文件欄位會直接作為輸入傳遞給模型。`input_map` 的大小表示模型被呼叫的次數 (Predict API 請求的次數)。 |
| `<model_input_field>`  | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要  | 模型輸入欄位名稱。 |
| `<document_field>`     | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 搜尋回應中用作模型輸入的文件欄位名稱或 JSON 路徑。  |
| `output_map`           | 陣列 | 外部託管模型為選用<br/><br/>本機模型為必要 | 一個陣列，指定如何將模型輸出欄位對應到搜尋回應文件中的新欄位。陣列的每個元素都是 `"<new_document_field>": "<model_output_field>"` 格式的對應。 |
| `<new_document_field>` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 文件中新欄位的名稱，模型的輸出 (由 `model_output` 指定) 會儲存在此欄位。若外部託管模型未指定輸出對應，則模型輸出的所有欄位都會加入新的文件欄位。  |
| `<model_output_field>` | 字串    | 外部託管模型為選用<br/><br/>本機模型為必要 | 模型輸出中要儲存至 `new_document_field` 的欄位名稱或 JSON 路徑。  |
| `full_response_path`   | 布林值   | 選用   | 若 `model_output_field` 包含欄位的完整 JSON 路徑而非欄位名稱，請將此參數設為 `true`。屆時模型輸出將被完整解析以取得該欄位的值。本機模型預設為 `true`，外部託管模型預設為 `false`。  |
| `ignore_missing`       | 布林值   | 選用  | 若為 `true`，且 `input_map` 或 `output_map` 中定義的任何輸入欄位遺漏，則會忽略此處理器。否則，欄位遺漏會導致失敗。預設為 `false`。 |
| `ignore_failure`       | 布林值   | 選用  | 指定處理器即使遇到錯誤仍繼續執行。若為 `true`，則會忽略此處理器並繼續搜尋。若為 `false`，則任何失敗都會導致搜尋被取消。預設為 `false`。 |
| `override`             | 布林值   | 選用   | 當回應中的文件已包含名稱為 `<new_document_field>` 所指定名稱的欄位時，此參數才有作用。若 `override` 為 `false`，則會略過輸入欄位。若為 `true`，則現有的欄位值會被新的模型輸出覆寫。預設為 `false`。  |
| `max_prediction_tasks` | 整數   | 選用  | 文件搜尋期間可執行的並行模型呼叫數目上限。預設為 `10`。  |
| `one_to_one`           | 布林值    | 選用  | 將此參數設為 `true`，可為每個文件呼叫模型一次 (發出一個 Predict API 請求)。預設值 (`false`) 指定以搜尋回應中的所有文件呼叫模型，發出一個 Predict API 請求。 |
| `description`          | 字串    | 選用  | 處理器的簡要說明。 |
| `tag`                  | 字串    | 選用 | 處理器的識別標籤。在偵錯時可用於區分相同類型的處理器。 |

`input_map` 與 `output_map` 對應支援標準 [JSON path](https://github.com/json-path/JsonPath) 標記法，以指定複雜的資料結構。
{: .note}

### 設定

建立一個名為 `my_index` 的索引，並將一份文件編製索引以說明對應：

```json
POST /my_index/_doc/1
{
  "passage_text": "hello world"
}
```
{% include copy-curl.html %}

## 使用處理器

依照下列步驟在管線中使用處理器。建立處理器時必須提供模型 ID。在使用處理器測試管線之前，請確認模型已成功部署。您可以使用 [Get Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/get-model/) 檢查模型狀態。

對於本機模型，您必須提供 `model_input` 欄位，以指定模型輸入格式。請在 `model_input` 中加入 `model_config` 的任何輸入欄位。

對於遠端模型，`model_input` 欄位為選用，其預設值為 `"{ \"parameters\": ${ml_inference.parameters} }`。

### 範例：本機模型

下列範例示範如何使用本機模型設定 `ml_inference` 搜尋回應處理器。

**步驟 1：建立管線**

下列範例示範如何為 `huggingface/sentence-transformers/all-distilroberta-v1` 本機模型建立搜尋管線。該模型是託管在您的 OpenSearch 叢集中的[預先訓練句子轉換器模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sentence-transformers)。

如果您使用 Predict API 叫用該模型，則請求如下所示：

```json
POST /_plugins/_ml/_predict/text_embedding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```

使用此結構描述，請依照下列方式指定 `model_input`：

```json
 "model_input": "{ \"text_docs\": ${input_map.text_docs}, \"return_number\": ${model_config.return_number}, \"target_response\": ${model_config.target_response} }"
```

在 `input_map` 中，將 `passage_text` 文件欄位對應到模型預期的 `text_docs` 欄位：

```json
"input_map": [
  {
    "text_docs": "passage_text"
  }
]
```

由於您將要轉換為嵌入的欄位指定為 JSON 路徑，因此需要將 `full_response_path` 設定為 `true`。這樣系統會剖析完整的 JSON 文件以取得輸入欄位：

```json
"full_response_path": true
```

`passage_text` 欄位中的文字將用於產生嵌入：

```json
{
  "passage_text": "hello world"
}
```

Predict API 請求會傳回以下回應：

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

模型會在 `$.inference_results.*.output.*.data` 欄位中產生嵌入。`output_map` 會將此欄位對應到搜尋回應文件中新建立的 `passage_embedding` 欄位：

```json
"output_map": [
  {
    "passage_embedding": "$.inference_results.*.output.*.data"
  }
]
```

若要使用本機模型設定 `ml_inference` 搜尋回應處理器，請明確指定 `function_name`。在此範例中，`function_name` 為 `text_embedding`。有關有效 `function_name` 值的資訊，請參閱 [請求本文欄位](#request-body-fields)。

以下是最終的 `ml_inference` 搜尋回應處理器搭配本機模型的組態：

```json
PUT /_search/pipeline/ml_inference_pipeline_local
{
  "description": "search passage and generates embeddings",
  "response_processors": [
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
            "text_docs": "passage_text"
          }
        ],
        "output_map": [
          {
            "passage_embedding": "$.inference_results.*.output.*.data"
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

執行以下查詢，並在請求中提供管線名稱：

```json
GET /my_index/_search?search_pipeline=ml_inference_pipeline_local
{
"query": {
  "term": {
    "passage_text": {
      "value": "hello"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 回應

回應確認處理器已在 `passage_embedding` 欄位中產生文字嵌入：

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
        "_id": "1",
        "_score": 0.00009405752,
        "_source": {
          "passage_text": "hello world",
          "passage_embedding": [
            0.017304314,
            -0.021530833,
            0.050184276,
            0.08962978,
            ...]
        }
      }
    ]
  }
}
```

### 範例：外部託管的文字嵌入模型

下列範例示範如何使用外部託管的模型設定 `ml_inference` 搜尋回應處理器。

**步驟 1：建立管線**

下列範例示範如何為外部託管的文字嵌入模型建立搜尋管線。該模型需要一個 `input` 欄位，並在 `data` 欄位中產生結果。它會將 `passage_text` 欄位中的文字轉換為文字嵌入，並將嵌入儲存在 `passage_embedding` 欄位中。`function_name` 未在處理器組態中明確指定，因此預設為 `remote`，表示外部託管的模型：

```json
PUT /_search/pipeline/ml_inference_pipeline
{
  "description": "Generate passage_embedding when search documents",
  "response_processors": [
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

向外部託管的模型發出 Predict API 請求時，所有必要的欄位和參數通常都包含在 `parameters` 物件中：

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

為外部託管的模型指定 `input_map` 時，您可以直接參照 `input` 欄位，而不用提供其點路徑 `parameters.input`：

```json
"input_map": [
  {
    "input": "passage_text"
  }
]
```

**步驟 2：執行管線**

執行以下查詢，並在請求中提供管線名稱：

```json
GET /my_index/_search?search_pipeline=ml_inference_pipeline_local
{
  "query": {
    "match_all": {
    }
  }
}
```
{% include copy-curl.html %}

回應確認處理器已在 `passage_embedding` 欄位中產生文字嵌入。`_source` 內的文件現在同時包含 `passage_text` 和 `passage_embedding` 欄位：

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
        "_id": "1",
        "_score": 0.00009405752,
        "_source": {
          "passage_text": "hello world",
          "passage_embedding": [
            0.017304314,
            -0.021530833,
            0.050184276,
            0.08962978,
            ...]
        }
      }
      }
    ]
  }
}
```

### 範例：外部託管的大型語言模型

此範例示範如何設定 `ml_inference` 搜尋回應處理器，以搭配外部託管的大型語言模型 (LLM) 使用，並將模型回應對應至搜尋擴充物件。使用 `ml_inference` 處理器，您可以讓 LLM 直接在回應中摘要搜尋結果。摘要會包含在搜尋回應的 `ext` 欄位中，讓您能在原始搜尋結果旁無縫存取 AI 產生的洞察。

**先決條件**

您必須為此使用案例設定外部託管的 LLM。如需外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。註冊 LLM 後，您可以使用下列請求進行測試。此請求需要提供 `prompt` 和 `context` 欄位：

```json
POST /_plugins/_ml/models/KKne6JIBAs32TwoK-FFR/_predict
{
  "parameters": {
    "prompt":"\n\nHuman: You are a professional data analysist. You will always answer question: Which month had the lowest customer acquisition cost per new customer? based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say I don't know. Context: ${parameters.context.toString()}. \n\n Assistant:",
    "context":"Customer acquisition cost: January: $50, February: $45, March: $40. New customers: January: 500, February: 600, March: 750"
  }
}
```
{% include copy-curl.html %}

回應會在 `inference_results` 欄位中包含模型輸出：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": """ Based on the data provided:

                        - Customer acquisition cost in January was $50 and new customers were 500. So cost per new customer was $50/500 = $0.10
                        - Customer acquisition cost in February was $45 and new customers were 600. So cost per new customer was $45/600 = $0.075
                        - Customer acquisition cost in March was $40 and new customers were 750. So cost per new customer was $40/750 = $0.053
            
                        Therefore, the month with the lowest customer acquisition cost per new customer was March, at $0.053."""
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

**步驟 1：建立管線**

為已註冊的模型建立搜尋管線。此模型需要 `context` 欄位作為輸入。模型回應會摘要 `review` 欄位中的文字，並將摘要儲存在搜尋回應的 `ext.ml_inference.llm_response` 欄位中：

```json
PUT /_search/pipeline/my_pipeline_request_review_llm
{
  "response_processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "description": "This processor is going to run llm",
        "model_id": "EOF6wJIBtDGAJRTD4kNg",
        "function_name": "REMOTE",
        "input_map": [
          {
            "context": "review"
          }
        ],
        "output_map": [
          {
            "ext.ml_inference.llm_response": "response"
          }
        ],
        "model_config": {
          "prompt": "\n\nHuman: You are a professional data analysist. You will always answer question: Which month had the lowest customer acquisition cost per new customer? based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say I don't know. Context: ${parameters.context.toString()}. \n\n Assistant:"
        },
        "ignore_missing": false,
        "ignore_failure": false
      }
    }
  ]
}
```
{% include copy-curl.html %}

在此組態中，您提供了下列參數：

- `model_id` 參數指定生成式 AI 模型的 ID。
- `function_name` 參數設為 `REMOTE`，表示此模型為外部託管。
- `input_map` 參數會將文件中的 review 欄位對應至模型預期的 context 欄位。
- `output_map` 參數指定模型回應應儲存在搜尋回應中的 `ext.ml_inference.llm_response`。
- `model_config` 參數包含提示，告知模型如何處理輸入並產生摘要。

**步驟 2：將範例文件編製索引**

將一些範例文件編製索引，以測試管線：

```json
POST /_bulk
{"index":{"_index":"review_string_index","_id":"1"}}
{"review":"Customer acquisition cost: January: $50, New customers: January: 500."}
{"index":{"_index":"review_string_index","_id":"2"}}
{"review":"Customer acquisition cost: February: $45, New customers: February: 600."}
{"index":{"_index":"review_string_index","_id":"3"}}
{"review":"Customer acquisition cost: March: $40, New customers: March: 750."}
```
{% include copy-curl.html %}

**步驟 3：執行管線**

使用管線執行搜尋查詢：

```json
GET /review_string_index/_search?search_pipeline=my_pipeline_request_review_llm
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應包含原始文件，並在 `ext.ml_inference.llm_response` 欄位中包含產生的摘要：

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "review_string_index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "review": "Customer acquisition cost: January: $50, New customers: January: 500."
        }
      },
      {
        "_index": "review_string_index",
        "_id": "2",
        "_score": 1,
        "_source": {
          "review": "Customer acquisition cost: February: $45, New customers: February: 600."
        }
      },
      {
        "_index": "review_string_index",
        "_id": "3",
        "_score": 1,
        "_source": {
          "review": "Customer acquisition cost: March: $40, New customers: March: 750."
        }
      }
    ]
  },
  "ext": {
    "ml_inference": {
      "llm_response": """ Based on the context provided:

      - Customer acquisition cost in January was $50 and new customers were 500. So the cost per new customer was $50/500 = $0.10

      - Customer acquisition cost in February was $45 and new customers were 600. So the cost per new customer was $45/600 = $0.075

      - Customer acquisition cost in March was $40 and new customers were 750. So the cost per new customer was $40/750 = $0.053

      Therefore, the month with the lowest customer acquisition cost per new customer was March, as it had the lowest cost per customer of $0.053."""
    }
  }
}
```

### 範例：使用文字相似度模型重新排序搜尋結果

下列範例示範如何設定 `ml_inference` 搜尋回應處理器以搭配文字相似度模型。

**先決條件**

您必須為此使用案例設定外部託管的文字相似度模型。如需外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。註冊文字相似度模型後，您可以使用下列請求進行測試。此請求需要您在 `inputs` 欄位中提供 `text` 和 `text_pair` 欄位：

```json
POST /_plugins/_ml/models/Ialx65IBAs32TwoK1lXf/_predict
{
  "parameters": {
    "inputs":
    {
      "text": "I like you",
      "text_pair": "I hate you"
    }
  }
}
```
{% include copy-curl.html %}

模型會為每份輸入文件傳回相似度分數：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "label": "LABEL_0",
            "score": 0.022704314440488815
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 1：將範例文件編製索引**

建立索引並新增一些範例文件：

```json
POST _bulk
{"index":{"_index":"demo-index-0","_id":"1"}}
{"diary":"I hate you"}
{"index":{"_index":"demo-index-0","_id":"2"}}
{"diary":"I love you"}
{"index":{"_index":"demo-index-0","_id":"3"}}
{"diary":"I dislike you"}
```
{% include copy-curl.html %}

**步驟 2：建立搜尋管線**

在此範例中，您將建立一個搜尋管線，在 `one-to-one` 推論模式中使用文字相似度模型，逐一處理搜尋結果中的每份文件。此設定可讓模型為每份文件發出一次預測請求，為每個搜尋命中提供特定的相關性洞察。使用 `input_map` 將搜尋請求對應至查詢文字時，JSON 路徑必須以 `$._request` 或 `_request` 開頭：

```json
PUT /_search/pipeline/my_rerank_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "description": "This processor runs ml inference during search response",
        "model_id": "Ialx65IBAs32TwoK1lXf",
        "model_input":"""{"parameters":{"inputs":{"text":"${input_map.text}","text_pair":"${input_map.text_pair}"}}}""",
        "function_name": "REMOTE",
        "input_map": [
          {
            "text": "diary",
            "text_pair":"$._request.query.term.diary.value"
          }
        ],
        "output_map": [
          {
            "rank_score": "$.score"
          }
        ],
        "full_response_path": false,
        "model_config": {},
        "ignore_missing": false,
        "ignore_failure": false,
        "one_to_one": true
        },
        "rerank": {
          "by_field": {
            "target_field": "rank_score",
            "remove_target_field": true
          }
        }
    }
  ]
}
```
{% include copy-curl.html %}

在此組態中，您提供了下列參數：

- `model_id` 參數指定文字相似度模型的唯一識別碼。
- `function_name` 參數設為 `REMOTE`，表示此模型為外部託管。
- `input_map` 參數會將每份文件中的 `diary` 欄位對應至模型的 `text` 輸入，並將搜尋查詢詞彙對應至 `text_pair` 輸入。
- `output_map` 參數會將模型的分數對應至每份文件中名為 `rank_score` 的欄位。
- `model_input` 參數會格式化模型的輸入，確保其符合 Predict API 預期的結構。
- `one_to_one` 參數設為 `true`，確保模型逐一處理每份文件，而非將多份文件批次處理。
- `ignore_missing` 參數設為 `false`，若文件中缺少對應的欄位，會導致處理器失敗。
- `ignore_failure` 參數設為 `false`，若 ML 推論處理器發生錯誤，會導致整個管線失敗。

`rerank` 處理器會在 ML 推論之後套用。它會根據 ML 模型產生的 `rank_score` 欄位重新排序文件，然後從最終結果中移除此欄位。

**步驟 3：執行管線**

現在使用建立的管線執行搜尋：

```json
GET /demo-index-0/_search?search_pipeline=my_rerank_pipeline
{
  "query": {
    "term": {
      "dairy": {
        "value": "today"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含原始文件及其重新排序後的分數：

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.040183373,
    "hits": [
      {
        "_index": "demo-index-0",
        "_id": "1",
        "_score": 0.040183373,
        "_source": {
          "diary": "I hate you"
        }
      },
      {
        "_index": "demo-index-0",
        "_id": "2",
        "_score": 0.022628736,
        "_source": {
          "diary": "I love you"
        }
      },
      {
        "_index": "demo-index-0",
        "_id": "3",
        "_score": 0.0073115323,
        "_source": {
          "diary": "I dislike you"
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```

## 後續步驟

- 請參閱[使用外部託管的交叉編碼器模型依欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-cross-encoder/)的完整範例。