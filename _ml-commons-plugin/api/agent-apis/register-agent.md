---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "註冊代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 註冊代理程式 API
**於 2.13 版引入**
{: .label .label-purple }

使用此 API 註冊代理程式。

代理程式可能為下列類型：

- _流程_代理程式
- _對話式流程_代理程式
- _對話式代理程式_
- _規劃、執行與反思_代理程式
- _AG-UI_ 代理程式

如需代理程式的詳細資訊，請參閱[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。

您可以使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)來註冊代理程式，並自動建立連接器和模型。此方法支援 Amazon Bedrock Converse、Google Gemini 和 OpenAI 模型，且需要啟用 `plugins.ml_commons.unified_agent_api_enabled` 叢集設定。
{: .note}

## 端點

```json
POST /_plugins/_ml/agents/_register
```

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 代理程式類型 | 說明
:---  | :--- | :--- | :--- | :---
`name`| 字串 | 必要 | 全部 | 代理程式名稱。 |
`type` | 字串 | 必要 | 全部 | 代理程式類型。有效值為 [`flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/)、[`conversational_flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational-flow/)、[`conversational`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/#the-conversational-agent-v1)、[`conversational_v2`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/#the-conversational_v2-agent-with-full-multimodal-support)、[`plan_execute_and_reflect`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/) 及 [`ag_ui`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/ag-ui/)。如需詳細資訊，請參閱[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。 |
`agent_id` | 字串 | 選用 | 全部 | 代理程式的唯一識別碼。若省略，OpenSearch 會自動產生一個。 |
`description` | 字串 | 選用| 全部 | 代理程式的描述。 |
`tools` | 陣列 | 選用 | 全部 | 代理程式可執行的一組工具。
`app_type` | 字串 | 選用 | 全部 | 指定選用的代理程式類別。您接著可以對該類別中的所有代理程式執行操作。例如，您可以刪除 RAG 代理程式的所有訊息。
`memory.type` | 字串 | 選用 | `conversational_flow`, `conversational`, `plan_execute_and_reflect` | 指定對話記憶的儲存位置。支援的值為 `conversation_index`（將記憶儲存在對話索引中）及 `agentic_memory`（將記憶儲存在記憶容器中）。
`memory.memory_container_id` | 字串 | 選用 | `conversational_flow`, `conversational`, `plan_execute_and_reflect` | `agentic_memory` 的預設記憶容器 ID。若省略，您在執行代理程式時必須提供 `parameters.memory_container_id`。若兩者皆未提供，請求會失敗。
`llm.model_id` | 字串 | 必要 | `conversational` | 要傳送問題的 LLM 模型 ID。
`llm.parameters.response_filter` | 字串 | 必要 | `conversational` | 用於解析 LLM 回應的模式。對於每個 LLM，您需要提供回應所在的欄位。例如，對於 Anthropic Claude 模型，回應位於 `completion` 欄位，因此模式為 `$.completion`。對於 OpenAI 模型，模式為 `$.choices[0].message.content`。
`llm.parameters.max_iteration` | 整數 | 選用 | `conversational` | 傳送給 LLM 的訊息數量上限。預設為 `10`。
`parameters` | 物件 | 選用 | 全部 | 代理程式參數，可用於控制代理程式執行的 `max_steps`、修改預設提示等。
`parameters.executor_agent_id`| 整數 | 選用 | `plan_execute_and_reflect` | `plan_execute_and_reflect` 代理程式內部會使用 `conversational` 代理程式來執行每個步驟。根據預設，此執行程式代理程式會使用與 `llm` 組態中指定的規劃模型相同的模型。若要使用不同的模型來執行步驟，請使用另一個模型建立 `conversational` 代理程式，並在此欄位中傳入該代理程式 ID。若您想針對規劃和執行使用不同的模型，這會很有用。
`parameters.max_steps` | 整數 | 選用 | `plan_execute_and_reflect` | LLM 執行的步驟數量上限。預設為 `20`。
`parameters.executor_max_iterations` | 整數 | 選用 | `plan_execute_and_reflect` | 執行程式代理程式傳送給 LLM 的訊息數量上限。預設為 `20`。
`parameters.message_history_limit` | 整數 | 選用 | `plan_execute_and_reflect` | 要從對話記憶納入作為規劃程式內容的近期訊息數量。預設為 `10`。
`parameters.executor_message_history_limit` | 整數 | 選用 | `plan_execute_and_reflect` | 要從對話記憶納入作為執行程式內容的近期訊息數量。預設為 `10`。
`parameters._llm_interface` | 字串 | 必要 | `plan_execute_and_reflect`, `conversational` | 指定使用函式呼叫時如何解析 LLM 輸出。有效值為：<br> - `bedrock/converse/claude`：託管於 Amazon Bedrock 的 Anthropic Claude 對話模型 <br> - `bedrock/converse/deepseek_r1`：託管於 Amazon Bedrock 的 DeepSeek-R1 模型 <br> - `openai/v1/chat/completions`：託管於 OpenAI 的 OpenAI 聊天完成模型。每個介面都會定義預設的回應結構描述和函式呼叫解析器。
`inject_datetime` | 布林值 | 選用 | `conversational`, `plan_execute_and_reflect` | 是否自動將目前日期注入系統提示。預設為 `false`。
`datetime_format` | 字串 | 選用 | `conversational`, `plan_execute_and_reflect` | 啟用 `inject_datetime` 時所使用的日期格式字串。預設為 `"yyyy-MM-dd'T'HH:mm:ss'Z'"`（ISO 格式）。
`model` | 物件 | 選用 | `conversational`, `plan_execute_and_reflect` | **僅限統一註冊方法（3.5 以上版本）**：自動建立連接器和模型的模型組態。請參閱[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)。
`model.model_id` | 字串 | 必要（若使用 `model`） | `conversational`, `plan_execute_and_reflect` | 模型識別碼（例如，Amazon Bedrock 為 `us.anthropic.claude-3-7-sonnet-20250219-v1:0`，Google Gemini 為 `gemini-2.5-pro`）。
`model.model_provider` | 字串 | 必要（若使用 `model`） | `conversational`, `plan_execute_and_reflect` | 模型供應商。支援的值：`bedrock/converse`、`gemini/v1beta/generatecontent`、`openai/v1/chat/completions`。
`model.credential` | 物件 | 必要（若使用 `model`） | `conversational`, `plan_execute_and_reflect` | 存取模型的憑證。接受連接器支援的任何憑證格式。如需詳細資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints#request-body-fields)。
`model.model_parameters` | 物件 | 選用（若使用 `model`） | `conversational`, `plan_execute_and_reflect` | 模型特定參數，例如系統提示和其他組態選項。
`provisioned_by` | 字串 | 選用 | 全部 | 選用的歸屬標籤，用於識別註冊代理程式的外掛程式或用戶端（例如 `flow-framework`）。包含在 ML 統計指標中。

### 使用代理式記憶

若要使用代理式記憶，請使用 [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/) 建立記憶容器，並依下列方式設定記憶組態：

```json
"memory": {
  "type": "agentic_memory",
  "memory_container_id": "<memory_container_id>"
}
```
{% include copy.html %}

對於設定了 `agentic_memory` 的代理程式，請參閱[檢視記憶資料]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#inspecting-memory-data-opensearch-agents)，以瞭解如何在代理程式執行後檢視工作階段與追蹤資料。

### 工具組態

`tools` 陣列包含代理程式的工具清單。每個工具包含下列欄位。

欄位 | 資料類型 | 必要／選用 | 說明
:---  | :--- | :---
`type` | 字串 | 必要 | 工具類型。如需支援的工具清單，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
`name`| 字串 | 選用 | 工具名稱。工具名稱預設為 `type` 參數值。若您需要在代理程式中包含多個相同類型的工具，請為這些工具指定不同的名稱。 |
`description`| 字串 | 選用 | 工具說明。預設為指定類型的內建說明。 | 
`parameters` | 物件 | 選用 | 此工具的參數。參數高度取決於工具類型。您可以在[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)中找到特定工具類型的資訊。
`parameters.output_processors` | 陣列 | 選用 | 用於轉換工具輸出的處理器清單。如需詳細資訊，請參閱[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)。
`attributes.input_schema` | 物件 | 選用 | 以 [JSON 結構描述](https://json-schema.org/)定義的此工具預期輸入格式。用於定義 LLM 呼叫工具時應遵循的結構。
`attributes.strict` | 布林值 | 選用 | 函式呼叫是否確實遵循輸入結構描述。

## 請求範例：流程代理程式

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_RAG",
  "type": "flow",
  "description": "this is a test agent",
  "tools": [
    {
      "name": "vector_tool",
      "type": "VectorDBTool",
      "parameters": {
        "model_id": "zBRyYIsBls05QaITo5ex",
        "index": "my_test_data",
        "embedding_field": "embedding",
        "source_field": [
          "text"
        ],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "MLModelTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "NWR9YIsBUysqmzBdifVJ",
        "prompt": "\n\nHuman:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.vector_tool.output}\n\nHuman:${parameters.question}\n\nAssistant:"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 請求範例：對話式流程代理程式

```json
POST /_plugins/_ml/agents/_register
{
  "name": "population data analysis agent",
  "type": "conversational_flow",
  "description": "This is a demo agent for population data analysis",
  "app_type": "rag",
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "VectorDBTool",
      "name": "population_knowledge_base",
      "parameters": {
        "model_id": "your_text_embedding_model_id",
        "index": "test_population_data",
        "embedding_field": "population_description_embedding",
        "source_field": [
          "population_description"
        ],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "MLModelTool",
      "name": "bedrock_claude_model",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "your_LLM_model_id",
        "prompt": """

Human:You are a professional data analysist. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. 

Context:
${parameters.population_knowledge_base.output:-}

${parameters.chat_history:-}

Human:${parameters.question}

Assistant:"""
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 請求範例：對話式代理程式

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_ReAct_ClaudeV2",
  "type": "conversational",
  "description": "this is a test agent",
  "app_type": "my chatbot",
  "llm": {
    "model_id": "<llm_model_id>",
    "parameters": {
      "max_iteration": 5,
      "stop_when_no_tool_found": true,
      "response_filter": "$.completion"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "VectorDBTool",
      "name": "VectorDBTool",
      "description": "A tool to search opensearch index with natural language question. If you don't know answer for some question, you should always try to search data with this tool. Action Input: <natural language question>",
      "parameters": {
        "model_id": "<embedding_model_id>",
        "index": "<your_knn_index>",
        "embedding_field": "<embedding_filed_name>",
        "source_field": [
          "<source_filed>"
        ],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "ListIndexTool",
      "name": "RetrieveIndexMetaTool",
      "description": "Use this tool to get OpenSearch index information: (health, status, index, uuid, primary count, replica count, docs.count, docs.deleted, store.size, primary.store.size)."
    }
  ]
}
```
{% include copy-curl.html %}

## 請求範例：規劃、執行與反思代理程式
**於 3.0 版引入**
{: .label .label-purple }

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My plan execute and reflect agent",
  "type": "plan_execute_and_reflect",
  "description": "this is a test agent",
  "llm": {
    "model_id": "<llm_model_id>",
    "parameters": {
      "prompt": "${parameters.question}"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "<llm_interface>"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

## 請求範例：AG-UI 代理程式
**於 3.5 版引入**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。若要取得此功能的進度更新，或您想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。
{: .warning}

AG-UI 代理程式使用統一的註冊方法，將 AI 代理程式與前端應用程式整合。下列範例顯示基本結構：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "AG-UI Agent",
  "type": "AG_UI",
  "description": "An AI agent designed for UI interactions with streaming support",
  "model": {
    "model_id": "<MODEL ID>",
    "model_provider": "bedrock/converse",
    "credential": {
      "access_key": "<AWS ACCESS KEY>",
      "secret_key": "<AWS SECRET KEY>",
      "session_token": "<AWS SESSION TOKEN>"
    },
    "model_parameters": {
      "system_prompt": "You are a helpful assistant and an expert in OpenSearch."
    }
  },
  "parameters": {
    "max_iteration": 5
  },
  "tools": [{
    "type": "ListIndexTool"
  }],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

如需完整的 AG-UI 代理程式文件，包括欄位定義、先決條件、執行範例與 AG-UI 通訊協定格式，請參閱 [AG-UI 代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/ag-ui/)。

## 回應範例

OpenSearch 會回應一個代理程式 ID，您可以使用它來參照該代理程式：

```json
{
  "agent_id": "bpV_Zo0BRhAwb9PZqGja"
}
```

## 統一代理程式註冊
**3.5 版新增**
{: .label .label-purple }

統一註冊方法透過在單一 API 呼叫中自動處理連接器與模型的設定，簡化了代理程式的建立。此方法支援搭配 Anthropic Claude 模型的 Amazon Bedrock Converse API、Google Gemini 模型，以及 OpenAI 模型。

使用統一代理程式之前，請參閱[必要條件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#prerequisites)以了解所需的叢集設定。如需更多資訊與支援的代理程式類型，請參閱[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)。

### 統一註冊請求欄位

下表列出統一代理程式註冊可用的請求欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `name` | 字串 | 必要 | 代理程式名稱。 |
| `type` | 字串 | 必要 | 代理程式類型。支援的值：`conversational`、`conversational_v2`、`plan_execute_and_reflect` 與 `AG_UI`。 |
| `agent_id` | 字串 | 選用 | 代理程式的唯一識別碼。若省略，OpenSearch 會自動產生。 |
| `description` | 字串 | 選用 | 代理程式的描述。 |
| `model` | 物件 | 必要 | 使用統一註冊方法之 LLM 模型的組態。取代一般的 `llm` 物件，並自動建立模型資源。 |
| `model.model_id` | 字串 | 必要 | 供應商的模型識別碼。對於 Amazon Bedrock，請使用完整的模型 ID（例如 `us.anthropic.claude-3-7-sonnet-20250219-v1:0`）。對於 Google Gemini，請使用模型名稱（例如 `gemini-2.5-pro`）。對於 OpenAI，請使用 `gpt-4o-mini` 之類的模型名稱。 |
| `model.model_provider` | 字串 | 必要 | 模型供應商類型。有效值：`bedrock/converse`、`gemini/v1beta/generatecontent`、`openai/v1/chat/completions`。 |
| `model.credential` | 物件 | 必要 | 模型供應商的憑證。結構取決於供應商。 |
| `model.credential.access_key` | 字串 | 必要 (Amazon Bedrock) | Amazon Bedrock 模型的 AWS 存取金鑰。 |
| `model.credential.secret_key` | 字串 | 必要 (Amazon Bedrock) | Amazon Bedrock 模型的 AWS 私密金鑰。 |
| `model.credential.session_token` | 字串 | 選用 (Amazon Bedrock) | 使用暫時性憑證時，Amazon Bedrock 模型的 AWS 工作階段權杖。 |
| `model.credential.openai_api_key` | 字串 | 必要 (OpenAI) | OpenAI 模型的 API 金鑰。 |
| `model.credential.gemini_api_key` | 字串 | 必要 (Google Gemini) | Google Gemini 模型的 API 金鑰。 |
| `model.model_parameters` | 物件 | 選用 | 模型專屬的參數與組態。 |
| `model.model_parameters.system_prompt` | 字串 | 選用 | 定義代理程式角色與行為的系統提示。 |
| `model.model_parameters.temperature` | 浮點數 | 選用 | 控制模型回應的隨機性 (0.0 至 1.0)。預設值依模型而異。 |
| `model.model_parameters.max_tokens` | 整數 | 選用 | 模型回應中的詞元數上限。預設值依模型而異。 |
| `parameters` | 物件 | 選用 | 用於控制行為的其他代理程式參數。 |
| `parameters.max_iteration` | 整數 | 選用 | 代理程式可執行的推理迭代次數上限。預設為 10。 |
| `parameters.mcp_connectors` | 陣列 | 選用 | 用於擴充代理程式能力的 Model Context Protocol (MCP) 連接器組態陣列。對於 `conversational` 與 `plan_execute_and_reflect` 代理程式，MCP 工具會自動探索。對於 `flow` 與 `conversational_flow` 代理程式，請在 `tools` 陣列中明確列出 MCP 工具。請參閱[連接至外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/#step-3-register-an-agent-for-accessing-mcp-tools)。 |
| `parameters.mcp_connectors[].mcp_connector_id` | 字串 | 必要 | 已註冊 MCP 連接器的 ID。 |
| `parameters.mcp_connectors[].tool_filters` | 陣列 | 選用 | 指定代理程式可用 MCP 工具的 Java 規則運算式。 |
| `parameters.mcp_connectors[].tool_descriptions` | 陣列 | 選用 | 覆寫呈現給 LLM 之 MCP 工具描述的物件。 |
| `tools` | 陣列 | 選用 | 代理程式可用工具的陣列。如需支援的工具，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。 |
| `memory` | 物件 | 選用 | 對話記憶儲存空間的組態。 |
| `memory.type` | 字串 | 選用 | 記憶的儲存類型。支援的值：`conversation_index`、`agentic_memory`。 |

`tools` 陣列中的每個工具包含下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `type` | 字串 | 必要 | 工具類型（例如 `ListIndexTool`、`SearchIndexTool`、`McpStreamableHttpTool`、`McpSseTool`）。對於 `flow` 與 `conversational_flow` 代理程式中的 MCP 工具，請搭配 `mcp_streamable_http` 連接器使用 `McpStreamableHttpTool`，或搭配 `mcp_sse` 連接器使用 `McpSseTool`。 |
| `name` | 字串 | 選用 | 工具的自訂名稱。預設為 `type` 值。使用多個相同類型的工具時為必要。對於流程代理程式中的 MCP 工具，請將 `name` 設定為 MCP 伺服器工具名稱。 |
| `description` | 字串 | 選用 | 工具描述，協助 LLM 了解何時以及如何使用該工具。 |
| `parameters` | 物件 | 選用 | 工具專屬的參數。結構依工具類型而異。 |

<!-- vale off -->
### 範例請求：Amazon Bedrock Claude
<!-- vale on -->

此範例使用託管於 Amazon Bedrock 上的 Anthropic Claude 模型建立代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Claude Research Agent",
  "type": "conversational",
  "description": "An agent using Claude for research tasks",
  "model": {
    "model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "model_provider": "bedrock/converse",
    "credential": {
      "access_key": "YOUR_AWS_ACCESS_KEY",
      "secret_key": "YOUR_AWS_SECRET_KEY",
      "session_token": "YOUR_AWS_SESSION_TOKEN"
    },
    "model_parameters": {
      "system_prompt": "You are a helpful research assistant with access to OpenSearch data.",
      "temperature": 0.7,
      "max_tokens": 1000
    }
  },
  "parameters": {
    "max_iteration": 5
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

<!-- vale off -->
### 範例請求：Google Gemini
<!-- vale on -->

此範例使用 Google Gemini 模型建立代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Gemini Analysis Agent",
  "type": "conversational",
  "description": "An agent using Gemini for data analysis",
  "model": {
    "model_id": "gemini-2.5-pro",
    "model_provider": "gemini/v1beta/generatecontent",
    "credential": {
      "gemini_api_key": "YOUR_GEMINI_API_KEY"
    },
    "model_parameters": {
      "system_prompt": "You are an expert data analyst with access to OpenSearch indices."
    }
  },
  "tools": [
    {
      "type": "SearchIndexTool"
    }
  ],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

<!-- vale off -->
### 範例請求：OpenAI Chat Completion
<!-- vale on -->

此範例使用 OpenAI 的 GPT 模型建立代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT Customer Service Agent",
  "type": "conversational",
  "description": "An agent using GPT for customer service tasks",
  "model": {
    "model_id": "gpt-4o-mini",
    "model_provider": "openai/v1/chat/completions",
    "credential": {
      "openai_api_key": "YOUR_OPENAI_API_KEY"
    },
    "model_parameters": {
      "system_prompt": "You are a helpful customer service agent with access to customer data.",
      "temperature": 0.3,
      "max_tokens": 800
    }
  },
  "parameters": {
    "max_iteration": 10
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    }
  ],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

### 範例請求：規劃、執行與反思代理程式

此範例建立用於複雜多步驟工作的規劃、執行與反思代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Research Planning Agent",
  "type": "plan_execute_and_reflect",
  "description": "An agent that can plan and execute complex research tasks",
  "model": {
    "model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "model_provider": "bedrock/converse",
    "credential": {
      "access_key": "YOUR_AWS_ACCESS_KEY",
      "secret_key": "YOUR_AWS_SECRET_KEY",
      "session_token": "YOUR_AWS_SESSION_TOKEN"
    },
    "model_parameters": {
      "system_prompt": "You are an expert researcher who can plan and execute multi-step research tasks."
    }
  },
  "parameters": {
    "max_steps": 15,
    "max_iteration": 20
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ],
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

## 相關文件

- 對於設定了 `agentic_memory` 的代理程式，請參閱[檢視記憶資料]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。
