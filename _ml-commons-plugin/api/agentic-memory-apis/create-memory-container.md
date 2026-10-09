---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立記憶容器"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 建立記憶容器 API
**3.3 版新增**
{: .label .label-purple }

使用此 API 建立儲存代理程式記憶的[記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-containers)。容器可以關聯兩種模型類型：

- 文字嵌入模型，用於將訊息向量化以便搜尋。稠密向量嵌入請使用文字嵌入模型，稀疏向量格式請使用稀疏編碼模型。若未指定嵌入模型，訊息會被儲存，但無法用於以向量為基礎的搜尋。
- 大型語言模型 (LLM)，用於對訊息進行推理以產生事實性或經過處理的內容。若未指定 LLM，訊息會直接儲存，不套用推論。長期記憶需要同時設定 LLM 模型與嵌入模型。

如需更多資訊，請參閱[整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

LLM 連接器必須支援 `system_prompt` 與 `user_prompt` 參數，才能進行代理程式記憶處理。預設的 `llm_result_path` 是 Amazon Bedrock Converse API 回應路徑 (`"$.output.message.content[0].text"`)。若使用 OpenAI GPT 模型，請將 `llm_result_path` 設為 `$.choices[0].message.content`。
{: .note}

建立記憶容器後，請將其 `memory_container_id` 提供給其他 API 使用。

## 建立的索引

為記憶容器建立的索引取決於您提供的 `configuration`。下表摘要說明其行為。

組態 | 建立的索引 | 功能
:--- | :--- | :---
無 `configuration` 或無 `strategies` | 工作記憶 + 工作階段 (除非 `disable_session` 為 `true`) | 原始訊息的儲存與擷取。無語意搜尋、無長期記憶、無事實擷取。
有 `strategies` (需要 `llm_id`、`embedding_model_id` 與 `embedding_model_type`) | 工作記憶 + 工作階段 + 長期記憶 + 歷史記錄 (除非 `disable_session` 為 `true`) | 語意搜尋、事實擷取、記憶整合 (ADD/UPDATE/DELETE 決策)，以及所有長期記憶變更的稽核軌跡。

每種索引類型都有特定用途：

- **工作記憶**：在收到訊息時儲存原始訊息。一定會建立。
- **工作階段**：追蹤對話工作階段及其中繼資料。預設會建立。若要停用工作階段追蹤，請將 `disable_session` 設為 `true`。
- **長期記憶**：儲存由策略產生的已擷取事實與持續性知識。僅在設定策略時建立。
- **歷史記錄**：記錄長期記憶上每一次 ADD、UPDATE 與 DELETE 操作的稽核軌跡。僅在設定策略時建立。可透過將 `disable_history` 設為 `true` 選擇不使用。

## 必要條件

若要使用其中一種模型類型來處理記憶，請在 OpenSearch 中註冊模型。

### 嵌入模型

註冊本機或外部託管的嵌入模型。OpenSearch 支援文字嵌入與稀疏編碼模型。

如需在本機使用模型的更多資訊，請參閱[在 OpenSearch 內使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。支援的模型清單請參閱 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#supported-pretrained-models)。


如需使用外部託管模型的更多資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。例如，若要註冊外部託管的 Amazon Titan Embeddings 模型，請傳送以下請求：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Bedrock embedding model",
    "function_name": "remote",
    "description": "test model",
    "connector": {
        "name": "Amazon Bedrock Connector: embedding",
        "description": "The connector to bedrock Titan embedding model",
        "version": 1,
        "protocol": "aws_sigv4",
        "parameters": {
              "region": "us-east-1",
              "service_name": "bedrock",
              "model": "amazon.titan-embed-text-v2:0",
              "dimensions": 1024,
             "normalize": true,
             "embeddingTypes": [
              "float"
            ]
        },
        "credential": {
             "access_key": "...",
             "secret_key": "...",
             "session_token": "..."
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
                "headers": {
                    "content-type": "application/json",
                    "x-amz-content-sha256": "required"
                },
                "request_body": """{ "inputText": "${parameters.inputText}", "dimensions": ${parameters.dimensions}, "normalize": ${parameters.normalize}, "embeddingTypes": ${parameters.embeddingTypes} }""",
                "pre_process_function": "connector.pre_process.bedrock.embedding",
                "post_process_function": "connector.post_process.bedrock.embedding"
            }
        ]
    }
}
```
{% include copy-curl.html %}

### LLM


若要註冊 Anthropic Claude 模型，請傳送以下請求：

```json
POST /_plugins/_ml/models/_register
{
    "name": "Bedrock infer model",
    "function_name": "remote",
    "description": "test model",
    "connector": {
        "name": "Amazon Bedrock Connector: Chat",
        "description": "The connector to bedrock Claude 3.7 sonnet model",
        "version": 1,
        "protocol": "aws_sigv4",
        "parameters": {
            "region": "us-east-1",
            "service_name": "bedrock",
            "max_tokens": 8000,
            "temperature": 1,
            "anthropic_version": "bedrock-2023-05-31",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        },
        "credential": {
            "access_key": "...",
            "secret_key": "...",
            "session_token": "..."
            },
        "actions": [
            {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
            "request_body": "{  \"anthropic_version\": \"${parameters.anthropic_version}\", \"max_tokens\": ${parameters.max_tokens}, \"temperature\": ${parameters.temperature}, \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [ { \"role\": \"user\", \"content\": [ {\"text\": \"${parameters.user_prompt}\" }] }]}"
            }
        ]
    }
}
```
{% include copy-curl.html %}

Claude 模型需要 `system_prompt` 參數。
{: .note}

如需使用外部託管模型的更多資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

## 端點

```json
POST /_plugins/_ml/memory_containers/_create
```

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`name` | 字串 | 必要 | 記憶容器的名稱。
`memory_container_id` | 字串 | 選用 | 記憶容器的唯一識別碼。若省略，OpenSearch 會自動產生。 |
`description` | 字串 | 選用 | 記憶容器的描述。
`configuration` | 物件 | 選用 | 記憶容器的組態。未提供時，會使用僅建立無 AI 功能之工作記憶容器的預設組態。若要取得包括語意搜尋與長期記憶在內的完整功能，請提供包含模型 ID 與策略的組態。請參閱 [`configuration` 物件](#the-configuration-object)。
`backend_roles` | 陣列 | 選用 | 用於存取控制的後端角色清單。每個角色最多 128 個字元，且只能包含英數字元與 `:+=,.@-_/`。

### 組態物件

`configuration` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`embedding_model_type` | 字串 | 選用 | 嵌入模型類型。支援的類型為 `TEXT_EMBEDDING` 和 `SPARSE_ENCODING`。若提供 `embedding_model_id` 則為必要。
`embedding_model_id` | 字串 | 選用 | 嵌入模型 ID。若提供 `embedding_model_type` 則為必要。
`embedding_dimension` | 整數 | 選用 | 嵌入模型的維度。若 `embedding_model_type` 為 `TEXT_EMBEDDING` 則為必要。若 `embedding_model_type` 為 `SPARSE_ENCODING` 則不允許。
`llm_id` | 字串 | 選用 | 用於處理與推論的 LLM 模型 ID。
`index_prefix` | 字串 | 選用 | 記憶索引的自訂前置字元。若未指定，則使用預設前置字元：當 `use_system_index` 為 `true` 時為 `default`，或當 `use_system_index` 為 `false` 時為 8 字元的隨機 UUID。
`use_system_index` | 布林值 | 選用 | 是否使用系統索引 (以 `.plugins-ml-agentic-memory-` 為前置字元的隱藏索引)。預設為 `true`。
`disable_history`  | 布林值 | 選用 | 是否停用歷史稽核軌跡索引。預設為 `false`。此設定僅在已設定策略時生效，因為歷史索引會記錄長期記憶的變更。若未設定策略，則無論此設定為何，都不會建立長期記憶或歷史索引。
`disable_session`  | 布林值 | 選用 | 是否停用工作階段追蹤索引。預設為 `false` (預設會啟用工作階段)。設為 `true` 可停用工作階段追蹤。
`max_infer_size`   | 整數 | 選用 | 在記憶整併期間所擷取之相似現有記憶的最大數量，用於做出 ADD/UPDATE/DELETE 決策。預設為 `5`。最大值為 `10`。
`index_settings`   | 物件 | 選用 | 為此容器將建立之記憶儲存索引的自訂 OpenSearch 索引設定。每種記憶類型 (`sessions`、`working`、`long_term` 和 `history`) 使用各自的索引。請參閱 [`index_settings` 物件](#the-index_settings-object)。
`strategies` | 陣列 | 選用 | [記憶處理策略]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-processing-strategies) 的陣列。提供策略時，`llm_id` 和嵌入模型欄位 (`embedding_model_id`、`embedding_model_type`) 皆為必要。請參閱 [`strategies` 陣列](#the-strategies-array)。
`parameters` | 物件 | 選用 | 記憶容器的全域參數。請參閱 [`parameters` 物件](#the-parameters-object)。

### index_settings 物件

您可以自訂將建立用於儲存記憶資料之儲存索引的 OpenSearch 索引設定。每種記憶類型使用專屬索引，您可以設定分片和副本數量等設定以最佳化效能。

下列範例說明如何在 `configuration` 物件中指定自訂索引設定：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "my-memory-container",
  "configuration": {
    "embedding_model_id": "your-model-id",
    "index_settings": {
      "session_index": {
        "index": {
          "number_of_shards": "2",
          "number_of_replicas": "2"
        }
      },
      "working_memory_index": {
        "index": {
          "number_of_shards": "2",
          "number_of_replicas": "2"
        }
      },
      "long_term_memory_index": {
        "index": {
          "number_of_shards": "2",
          "number_of_replicas": "2"
        }
      },
      "long_term_memory_history_index": {
        "index": {
          "number_of_shards": "2",
          "number_of_replicas": "2"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### strategies 陣列

`strategies` 陣列中的每個策略支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`type` | 字串 | 必要 | 策略類型。有效值為 `SEMANTIC`、`USER_PREFERENCE` 和 `SUMMARY`。
`namespace` | 陣列 | 必要 | 用於組織記憶的[命名空間]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#namespaces)維度陣列 (例如 `["user_id"]` 或 `["agent_id", "session_id"]`)。
`configuration` | 物件 | 選用 | 策略專屬組態。請參閱 [`strategies.configuration` 物件](#the-strategies-configuration-object)。
`enabled`       | 布林值             | 選用 | 是否在記憶容器中啟用該策略。預設為 `true`。

### strategies 組態物件

`strategies.configuration` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`llm_result_path` | 字串 | 選用 | 用於從回應中擷取 LLM 結果的 JSONPath 運算式。預設為 Amazon Bedrock Converse API 回應路徑 (`"$.output.message.content[0].text"`)。
`system_prompt` | 字串 | 選用 | 用於覆寫預設策略提示的自訂系統提示。
`llm_id` | 字串 | 選用 | 此策略的 LLM 模型 ID。會覆寫全域 LLM 設定。

### parameters 物件

`parameters` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`llm_result_path` | 字串 | 選用 | 用於從回應中擷取 LLM 結果的全域 JSONPath 運算式。預設為 Amazon Bedrock Converse API 回應路徑 (`"$.output.message.content[0].text"`)。

## 範例請求：最小記憶容器

下列請求會建立僅含工作記憶 (原始訊息儲存) 的最小記憶容器。未設定任何 AI 模型或策略：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "simple-message-store"
}
```
{% include copy-curl.html %}

此請求會建立具有單一工作記憶索引的容器。訊息可依 ID 儲存及擷取，但無法使用語意搜尋和長期記憶功能。

## 範例請求：含策略的基本記憶容器

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "agentic memory test",
  "description": "Store conversations with semantic search and summarization",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "{{embedding_model_id}}",
    "embedding_dimension": 1024,
    "llm_id": "{{llm_id}}",
    "strategies": [
      {
        "type": "SEMANTIC",
        "namespace": ["user_id"]
      }
    ]
  }
}
```
{% include copy-curl.html %}

此請求會建立具有工作記憶、長期記憶和歷史索引的容器。`SEMANTIC` 策略使用 LLM 從訊息中擷取事實，並使用嵌入模型對這些事實啟用向量式語意搜尋。

## 範例請求：含多個策略的進階記憶容器

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "agentic memory test",
  "description": "Store conversations with semantic search and summarization",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "{{embedding_model_id}}",
    "embedding_dimension": 1024,
    "llm_id": "{{llm_id}}",
    "index_prefix": "my_custom_prefix",
    "use_system_index": false,
    "strategies": [
      {
        "type": "SEMANTIC",
        "namespace": ["agent_id"],
        "configuration": {
          "llm_result_path": "$.output.message.content[0].text",
          "system_prompt": "Extract semantic information from user conversations",
          "llm_id": "{{custom_llm_id}}"
        }
      },
      {
        "type": "USER_PREFERENCE",
        "namespace": ["agent_id"],
        "configuration": {
          "llm_result_path": "$.output.message.content[0].text"
        }
      },
      {
        "type": "SUMMARY",
        "namespace": ["agent_id"],
        "configuration": {
          "llm_result_path": "$.output.message.content[0].text"
        }
      }
    ],
    "parameters": {
      "llm_result_path": "$.output.message.content[0].text"
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應包含 `memory_container_id`，您可以使用它來擷取或刪除容器：

```json
{
    "memory_container_id": "SdjmmpgBOh0h20Y9kWuN",
    "status": "created"
}
```
