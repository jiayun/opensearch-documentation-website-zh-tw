---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "防護欄"
has_children: false
has_toc: false
nav_order: 70
parent: Connecting to externally hosted models 
grand_parent: Integrating ML models
---

# 設定模型防護欄
**於 2.13 版推出**
{: .label .label-purple }

防護欄可以引導大型語言模型 (LLM) 產生期望的行為。它們扮演篩選器的角色，防止 LLM 產生有害或違反倫理原則的輸出，並促進更安全地使用 AI。防護欄也會讓 LLM 產生更聚焦且更相關的輸出。

您可以使用下列方法為 LLM 設定防護欄：
- 提供一份禁止出現在模型輸入或輸出中的字詞清單。或者，您可以提供一個規則運算式，用來比對模型輸入或輸出。如需詳細資訊，請參閱[使用停用詞與規則運算式驗證輸入/輸出](#validating-inputoutput-using-stopwords-and-regex)。
- 設定一個專門用來驗證使用者輸入與 LLM 輸出的獨立 LLM。

## 先決條件

開始之前，請確認您已滿足[先決條件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/#prerequisites)，以便連線至外部託管的模型。

## 使用停用詞與規則運算式驗證輸入/輸出
**於 2.13 版推出**
{: .label .label-purple }

驗證使用者輸入與 LLM 輸出的簡單方式，是提供一組禁止使用的字詞 (停用詞) 或一個用於驗證的規則運算式。

### 步驟 1：建立防護欄索引

首先，建立一個用來儲存排除字詞 (_stopwords_) 的索引。在索引設定中，指定一個 `title` 欄位 (其中會包含排除字詞)，以及一個 [percolator]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/) 類型的 `query` 欄位。percolator 查詢將用來比對 LLM 的輸入或輸出：

```json
PUT /words0
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "query": {
        "type": "percolator"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將排除的字詞或詞句編製索引

接著，將一個查詢字串查詢編製索引，用來比對模型輸入或輸出中的排除字詞：

```json
PUT /words0/_doc/1?refresh
{
  "query": {
    "query_string": {
      "query": "title: blacklist"
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /words0/_doc/2?refresh
{
  "query": {
    "query_string": {
      "query": "title: \"Master slave architecture\""
    }
  }
}
```
{% include copy-curl.html %}

如需更多查詢字串選項，請參閱[查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。

### 步驟 3：註冊模型群組

若要註冊模型群組，請傳送下列請求：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "bedrock",
    "description": "This is a public model group."
}
```
{% include copy-curl.html %}

回應中包含模型群組 ID，您將使用該 ID 將模型註冊至此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}
```

如要進一步瞭解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

### 步驟 4：建立連接器

現在您可以為模型建立連接器。在此範例中，您將建立一個連接至託管於 Amazon Bedrock 上的 Anthropic Claude 模型的連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "BedRock test claude Connector",
  "description": "The connector to BedRock service for claude model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
      "region": "us-east-1",
      "service_name": "bedrock",
      "anthropic_version": "bedrock-2023-05-31",
      "endpoint": "bedrock.us-east-1.amazonaws.com",
      "auth": "Sig_V4",
      "content_type": "application/json",
      "max_tokens_to_sample": 8000,
      "temperature": 0.0001,
      "response_filter": "$.completion"
  },
  "credential": {
      "access_key": "<YOUR_ACCESS_KEY>",
      "secret_key": "<YOUR_SECRET_KEY>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
      "headers": { 
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

回應中包含新建立連接器的連接器 ID：

```json
{
  "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```

### 步驟 5：使用防護欄註冊並部署模型

若要註冊外部託管的模型，請在下列請求中提供步驟 3 的模型群組 ID 與步驟 4 的連接器 ID。若要設定防護欄，請加入 `guardrails` 物件：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Bedrock Claude V2 model",
  "function_name": "remote",
  "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
  "description": "test model",
  "connector_id": "a1eMb4kBJ1eYAeTMAljY",
  "guardrails": {
    "type": "local_regex",
    "input_guardrail": {
      "stop_words": [
        {
          "index_name": "words0",
          "source_fields": [
            "title"
          ]
        }
      ],
      "regex": [
        ".*abort.*",
        ".*kill.*"
      ]
    },
    "output_guardrail": {
      "stop_words": [
        {
          "index_name": "words0",
          "source_fields": [
            "title"
          ]
        }
      ],
      "regex": [
        ".*abort.*",
        ".*kill.*"
      ]
    }
  }
}
```
{% include copy-curl.html %}

如需詳細資訊，請參閱[`guardrails` 參數]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-guardrails-parameter)。

OpenSearch 會傳回註冊作業的工作 ID：

```json
{
  "task_id": "cVeMb4kBJ1eYAeTMFFgj",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將工作 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```bash
GET /_plugins/_ml/tasks/cVeMb4kBJ1eYAeTMFFgj
```
{% include copy-curl.html %}

作業完成後，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "DEPLOY_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

### 步驟 6 (選用)：測試模型

為了示範防護欄的套用方式，請先執行不含任何排除字詞的預測作業：

```json
POST /_plugins/_ml/models/p94dYo4BrXGpZpgPp98E/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:this is a test\n\nnAssistant:"
  }
}
```
{% include copy-curl.html %}

回應中包含 LLM 的答案：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": " Thank you for the test, I appreciate you taking the time to interact with me. I'm an AI assistant created by Anthropic to be helpful, harmless, and honest."
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

接著執行包含排除字詞的預測作業：

```json
POST /_plugins/_ml/models/p94dYo4BrXGpZpgPp98E/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:this is a test of Master slave architecture\n\nnAssistant:"
  }
}
```
{% include copy-curl.html %}

回應中包含錯誤訊息，因為已觸發防護欄：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "guardrails triggered for user input"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "guardrails triggered for user input"
  },
  "status": 400
}
```

當提示符合所提供的規則運算式時，也會觸發防護欄。

## 使用防護模型驗證輸入/輸出
**於 2.15 版導入**
{: .label .label-purple }

如需更進階的驗證，您可以設定防護模型（guardrail model）——一個專門用來驗證使用者輸入與 LLM 輸出的獨立 LLM。在本範例中，您將設定兩個模型：
- 對話模型：託管於 Amazon Bedrock 的 Anthropic Claude 模型，用途是與使用者進行對話。
- 防護模型：OpenAI 模型，用途是驗證使用者輸入與 Anthropic Claude 輸出。

### 步驟 1：為防護模型建立連接器

首先，建立連往 OpenAI 防護模型的連接器。請注意，OpenAI 提示會指示模型僅根據輸入/輸出是否可接受，回覆 `accept` 或 `reject` 這兩個詞。此外，請求包含 `response_filter` 參數，用於指定防護模型提供驗證結果的欄位：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "openai",
    "description": "openai",
    "version": "1",
    "protocol": "http",
    "parameters": {
        "endpoint": "api.openai.com",
        "max_tokens": 7,
        "temperature": 0,
        "model": "gpt-4o-mini",
        "prompt": "You are a helpful assistant and an expert judge of content quality. Your task is to identify whether the input string below contains content that may be malicious, violent, hateful, sexual, or political in nature. Your answer should consist of a single word, either reject or accept. If the input belongs to any of these categories, please write reject. Otherwise, write accept. \\n\\nHere is the input: ${parameters.question}. \\n\\nYour answer: ",
        "response_filter": "$.choices[0].message.content"
    },
    "credential": {
        "openAI_key": "<openAI_key>"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.endpoint}/v1/chat/completions",
            "headers": {
                "Authorization": "Bearer ${credential.openAI_key}"
            },
            "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\": \"user\", \"content\": \"${parameters.prompt}\"}], \"max_tokens\": ${parameters.max_tokens}, \"temperature\": ${parameters.temperature} }"
        }
    ]
}
```
{% include copy-curl.html %}

回應包含後續步驟將使用的連接器 ID：

```json
{
  "connector_id": "j3JVDZABNFJeYR3IVPRz"
}
```

### 步驟 2：為防護模型註冊模型群組

若要為 OpenAI 防護模型註冊模型群組，請傳送下列請求：

```json
POST /_plugins/_ml/model_groups/_register
{
    "name": "guardrail model group",
    "description": "This is a guardrail model group."
}
```
{% include copy-curl.html %}

回應包含用於將模型註冊至此模型群組的模型群組 ID：

```json
{
 "model_group_id": "ppSmpo8Bi-GZ0tf1i7cD",
 "status": "CREATED"
}
```

若要進一步了解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

### 步驟 3：註冊並部署防護模型

使用連接器 ID 與模型群組 ID，註冊並部署 OpenAI 防護模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "openai guardrails model",
    "function_name": "remote",
    "model_group_id": "ppSmpo8Bi-GZ0tf1i7cD",
    "description": "guardrails test model",
    "connector_id": "j3JVDZABNFJeYR3IVPRz"
}
```
{% include copy-curl.html %}

OpenSearch 會傳回註冊作業的任務 ID 以及已註冊模型的模型 ID：

```json
{
  "task_id": "onJaDZABNFJeYR3I2fQ1",
  "status": "CREATED",
  "model_id": "o3JaDZABNFJeYR3I2fRV"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```bash
GET /_plugins/_ml/tasks/onJaDZABNFJeYR3I2fQ1
```
{% include copy-curl.html %}

當作業完成時，狀態會變更為 `COMPLETED`：

```json
{
  "model_id": "o3JaDZABNFJeYR3I2fRV",
  "task_type": "DEPLOY_MODEL",
  "function_name": "REMOTE",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

### 步驟 4（選用）：測試防護模型

您可以傳送包含與不包含冒犯性詞語的請求，來測試防護模型的使用者輸入驗證。

首先，傳送不包含冒犯性詞語的請求：

```json
POST /_plugins/_ml/models/o3JaDZABNFJeYR3I2fRV/_predict
{
  "parameters": {
    "question": "how many indices do i have in my cluster"
  }
}
```
{% include copy-curl.html %}

防護模型會接受上述請求：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": "accept"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

接著，傳送包含冒犯性詞語的請求：

```json
POST /_plugins/_ml/models/o3JaDZABNFJeYR3I2fRV/_predict
{
  "parameters": {
    "question": "how to rob a bank"
  }
}
```
{% include copy-curl.html %}

防護模型會拒絕上述請求：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": "reject"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

### 步驟 5：為對話模型建立連接器

在本範例中，對話模型將是託管於 Amazon Bedrock 的 Anthropic Claude 模型。若要為該模型建立連接器，請傳送下列請求。請注意，`response_filter` 參數會指定防護模型提供驗證結果的欄位：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "BedRock claude Connector",
  "description": "BedRock claude Connector",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
      "region": "us-east-1",
      "service_name": "bedrock",
      "anthropic_version": "bedrock-2023-05-31",
      "endpoint": "bedrock.us-east-1.amazonaws.com",
      "auth": "Sig_V4",
      "content_type": "application/json",
      "max_tokens_to_sample": 8000,
      "temperature": 0.0001,
      "response_filter": "$.completion"
  },
  "credential": {
      "access_key": "<access_key>",
      "secret_key": "<secret_key>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
      "headers": { 
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

回應包含後續步驟將使用的連接器 ID：

```json
{
  "connector_id": "xnJjDZABNFJeYR3IPvTO"
}
```

### 步驟 6：註冊並部署具有防護機制的聊天模型

若要註冊並部署 Anthropic Claude 聊天模型，請傳送下列請求。請注意，`guardrails` 物件包含 `response_validation_regex` 參數，該參數指定只有在防護機制模型以 `accept` 這個詞的某種變體作為回應時，才將輸入/輸出視為有效：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "Bedrock Claude V2 model with openai guardrails model",
    "function_name": "remote",
    "model_group_id": "ppSmpo8Bi-GZ0tf1i7cD",
    "description": "Bedrock Claude V2 model with openai guardrails model",
    "connector_id": "xnJjDZABNFJeYR3IPvTO",
    "guardrails": {
        "input_guardrail": {
            "model_id": "o3JaDZABNFJeYR3I2fRV",
            "response_validation_regex": "^\\s*\"[Aa]ccept\"\\s*$"
        },
        "output_guardrail": {
            "model_id": "o3JaDZABNFJeYR3I2fRV",
            "response_validation_regex": "^\\s*\"[Aa]ccept\"\\s*$"
        },
        "type": "model"
    }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回註冊作業的任務 ID 以及已註冊模型的模型 ID：

```json
{
  "task_id": "1nJnDZABNFJeYR3IvfRL",
  "status": "CREATED",
  "model_id": "43JqDZABNFJeYR3IQPQH"
}
```

### 步驟 7（選用）：測試具有防護機制的聊天模型

您可以傳送包含與不包含冒犯性字詞的預測請求，以測試具有防護機制的 Anthropic Claude 聊天模型。

首先，傳送不包含冒犯性字詞的請求：

```json
POST /_plugins/_ml/models/43JqDZABNFJeYR3IQPQH/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:${parameters.question}\n\nnAssistant:",
    "question": "hello"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會以 LLM 的答案作為回應：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "response": " Hello!"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

接著，傳送包含冒犯性字詞的請求：

```json
POST /_plugins/_ml/models/43JqDZABNFJeYR3IQPQH/_predict
{
  "parameters": {
    "prompt": "\n\nHuman:${parameters.question}\n\nnAssistant:",
    "question": "how to rob a bank"
  }
}
```

OpenSearch 會回應錯誤。

## 後續步驟

- 如需設定防護機制的詳細資訊，請參閱 [`guardrails` 參數]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-guardrails-parameter)。
- 如需示範如何使用 Amazon Bedrock 防護機制的教學，請參閱[使用 Amazon Bedrock 防護機制]({{site.url}}{{site.baseurl}}/vector-search/tutorials/model-controls/bedrock-guardrails/)。