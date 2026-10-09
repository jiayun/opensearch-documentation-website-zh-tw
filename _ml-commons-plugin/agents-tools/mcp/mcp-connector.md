---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連線至外部 MCP 伺服器"
parent: Using MCP tools
grand_parent: Agents and tools
nav_order: 10
---

# 連線至外部 MCP 伺服器 
**於 3.0 版推出**
{: .label .label-purple }

OpenSearch 支援使用 [代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/) 的代理式工作流程。雖然 OpenSearch 提供內建工具來執行複雜查詢，但 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 可與外部工具和資料來源整合。MCP 是一項開放通訊協定標準，為 AI 模型提供標準化的方式來連線至外部資料來源和工具，做為遠端 MCP 伺服器工具的「通用轉接器」。

OpenSearch 支援使用 Server-Sent Events (SSE) 通訊協定或 Streamable HTTP 通訊協定的 MCP 伺服器。不支援 Standard Input/Output (`stdio`) 通訊協定。
{: .note}

下列範例示範如何在代理式工作流程中使用 MCP 工具。

## 先決條件

使用 MCP 工具之前，您必須完成下列先決條件。

### 啟用 MCP 並設定受信任的連接器端點

- 透過設定 `plugins.ml_commons.mcp_connector_enabled` 設定來啟用 MCP 通訊協定。
- 在 `plugins.ml_commons.trusted_connector_endpoints_regex` 設定中設定受信任的連接器端點。基於安全性考量，此設定使用 regex 模式來定義允許哪些 MCP 伺服器 URL。

若要設定這兩個設定，請傳送下列請求：

```json
PUT /_cluster/settings/
{
  "persistent": {
    "plugins.ml_commons.trusted_connector_endpoints_regex": [
      "<mcp server url>"
    ],
    "plugins.ml_commons.mcp_connector_enabled": "true"
  }
}
```
{% include copy-curl.html %}

### 設定 MCP 伺服器

請確認您有一個執行中且可從 OpenSearch 叢集存取的 MCP 伺服器。

## 步驟 1：建立 MCP 連接器

MCP 連接器會儲存 MCP 伺服器的連線詳細資料和認證。您可以使用 SSE 或 Streamable HTTP 進行連線。

若要使用 SSE 建立 MCP 連接器，請傳送下列請求：

```json
POST /_plugins/_ml/connectors/_create
{
  "name":        "My MCP Connector",
  "description": "Connects to the external MCP server for weather tools",
  "version":     1,
  "protocol":    "mcp_sse",
  "url":         "https://my-mcp-server.domain.com",
  "credential": {
    "mcp_server_key": "THE_MCP_SERVER_API_KEY"
  },
  "parameters":{
    "sse_endpoint": "/sse" 
  },
  "headers": {
    "Authorization": "Bearer ${credential.mcp_server_key}"
  }
}
```
{% include copy-curl.html %}

若要使用 Streamable HTTP 建立 MCP 連接器，請將 `protocol` 設為 `mcp_streamable_http`。您也可以選擇將 `parameters.endpoint` 設為覆寫預設端點 (`/_plugins/_ml/mcp`)。不需要 SSE 專用的端點：

```json
POST /_plugins/_ml/connectors/_create
{
  "name":        "My MCP Connector (Streamable HTTP)",
  "description": "Connects to the external MCP server using Streamable HTTP",
  "version":     1,
  "protocol":    "mcp_streamable_http",
  "url":         "https://my-mcp-server.domain.com",
  "credential": {
    "mcp_server_key": "THE_MCP_SERVER_API_KEY"
  },
  "parameters": {
    "endpoint": "/_plugins/_ml/mcp"
  },
  "headers": {
    "Authorization": "Bearer ${credential.mcp_server_key}"
  }
}
```
{% include copy-curl.html %}

下表說明連接器參數。如需標準連接器參數的詳細資訊，請參閱 [請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

| 參數 | 資料類型 | 必要 | 描述 |
|:----------|:---------|:---|:------------|
| `protocol` | 字串 | 是 | 針對 SSE 指定 `mcp_sse`，或針對 Streamable HTTP 指定 `mcp_streamable_http`。 |
| `url` | 字串 | 是 | MCP 伺服器的完整基礎 URL，包含通訊協定、主機名稱和連接埠 (若未使用預設連接埠，例如 `https://my-mcp-server.com:8443`)。 |
| `credential` | 物件 | 是 | 包含機密驗證資訊，例如 API 金鑰或權杖。儲存在此物件中的值可使用 `${credential.*}` 語法在 `headers` 區段中安全地參照。 |
| `parameters` | 物件 | 否 | 包含 MCP 連接器的組態參數。 |
| `parameters.sse_endpoint` | 字串 | 否 | 僅適用於 SSE。MCP 伺服器的 SSE 端點路徑。預設為 `/sse`。 |
| `parameters.endpoint` | 字串 | 否 | 僅適用於 Streamable HTTP。MCP 伺服器端點路徑。預設為 `/mcp`。 |
| `headers` | 物件 | 否 | 要包含在對 MCP 伺服器之請求中的 HTTP 標頭。如需驗證標頭，請使用 `${credential.*}` 語法來參照 `credential` 物件中的值 (例如 `"Authorization": "Bearer ${credential.mcp_server_key}"`)。  |

回應包含連接器 ID：

```json
{
  "connector_id": "NZ2W2ZUBZ_3SyqdOvh2n",
}
```

## 步驟 2：註冊模型

使用連接器註冊任何外部託管的大型語言模型 (LLM)。如需支援的模型清單，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。

例如，若要註冊 OpenAI 聊天模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register
{
  "name": "My OpenAI model: gpt-4o-mini",
  "function_name": "remote",
  "description": "Test model registration (this example uses OpenAI, but you can register any model)",
  "connector": {
    "name": "My OpenAI Connector: gpt-4o-mini",
    "description": "Connector for the OpenAI chat model",
    "version": 1,
    "protocol": "http",
    "parameters": {
      "model": "gpt-4o"
    },
    "credential": {
      "openAI_key": "<YOUR_API_KEY>"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "headers": {
          "Authorization": "Bearer ${credential.openAI_key}"
        },
        "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_instruction}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.prompt}\"}${parameters._interactions:-}], \"tools\": [${parameters._tools:-}],\"parallel_tool_calls\":${parameters.parallel_tool_calls},\"tool_choice\": \"${parameters.tool_choice}\" }"
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應包含模型 ID：

```json
{
  "task_id": "K_iQfpYBjoQOEoSHN3wU",
  "status": "CREATED",
  "model_id": "LPiQfpYBjoQOEoSHN3zH"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。註冊完成後，任務 `state` 會變更為 `COMPLETED`。

## 步驟 3：註冊代理程式以存取 MCP 工具

下表列出支援 MCP 工具的代理程式類型。

| 代理程式類型 | MCP 整合 |
|:---|:---|
| [`conversational`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/) | LLM 會在執行階段選取 MCP 工具。 |
| [`plan_execute_and_reflect`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/) | LLM 會在執行階段選取 MCP 工具。 |
| [`flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/) | MCP 工具會依固定管線順序執行。 |
| [`conversational_flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational-flow/) | MCP 工具會依固定管線順序執行，並具備對話記憶。 |

對於所有支援的代理程式類型，請在 `parameters.mcp_connectors` 中包含一或多個 MCP 連接器。您設定 `tools` 陣列的方式取決於代理程式類型。

每個連接器都必須在 `parameters.mcp_connectors` 陣列中指定下列參數。

| 參數 | 資料類型 | 必要 | 描述 | 
|:--- |:--- |:--- |:--- |
| `mcp_connector_id` | 字串 | 是 | MCP 連接器的連接器 ID。 | 
| `tool_filters` | 陣列 | 否 | Java 樣式規則運算式的陣列，用於指定要提供給代理程式的 MCP 伺服器工具。若工具符合陣列中至少一個規則運算式，即會納入。若省略或設為空陣列，則連接器所公開的所有工具皆可使用。請使用 `^` 或 `$` 錨點或常值字串來精確比對工具名稱。例如，`^get_forecast` 會比對任何開頭為 "get_forecast" 的工具，而 `search_indices` 只會比對 "search_indices"。|
| `tool_descriptions` | 陣列 | 否 | 物件的陣列，用於覆寫傳送給 LLM 的工具描述。每個物件會將工具名稱 (索引鍵) 對應至取代描述 (字串值)。只有通過 `tool_filters` 評估的工具才能覆寫。若工具不存在於連接器上、被 `tool_filters` 排除，或具有空白、null 或非字串值，則會忽略這些項目。若相同的工具名稱出現在多個物件中，則以最後一個值為準。 |

對於 `conversational` 和 `plan_execute_and_reflect` 代理程式，MCP 工具會從設定的連接器中探索，並呈現給 LLM。LLM 會決定在執行期間要呼叫哪個 MCP 工具。您不需要在 `tools` 陣列中明確列出 MCP 工具，但您可以將 OpenSearch 內建工具與 MCP 工具一併納入。

下列範例會使用步驟 1 中建立的連接器 ID 註冊對話式代理程式。MCP 伺服器有兩個可用的工具 (`get_alerts` 和 `get_forecasts`)，但代理程式的組態中只包含 `get_alerts` 工具，因為它符合指定的 regex 模式 `^get_alerts$`：

```json
POST /_plugins/_ml/agents/_register
{
  "name":        "Weather & Search Bot",
  "type":        "conversational",
  "description": "Uses MCP to fetch forecasts and OpenSearch indices",
  "llm": {
    "model_id": "<MODEL_ID_FROM_STEP_2>",
    "parameters": {
      "max_iteration": 5,
      "system_instruction": "You are a helpful assistant.",
      "prompt": "${parameters.question}"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions",
    "mcp_connectors": [
      {
        "mcp_connector_id": "<MCP_CONNECTOR_ID_FROM_STEP_1>",
        "tool_filters": [
          "^get_alerts$"
        ]
      }
    ]
  },
  "tools": [
    { "type": "ListIndexTool" },
    { "type": "SearchIndexTool" }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

回應包含代理程式 ID：

```json
{
  "agent_id": "LfiXfpYBjoQOEoSH93w7"
}
```

### 覆寫 MCP 工具描述
**3.8 版新增**
{: .label .label-purple }

每個 MCP 工具都包含一段描述，協助 LLM 決定何時呼叫它。若要在不修改 MCP 伺服器的情況下取代工具的描述，請使用 `tool_descriptions` 參數。當伺服器提供的描述太過籠統、使用內部命名，或不符合您代理程式的領域詞彙時，這項功能特別有用。

`tool_descriptions` 中的每個項目都必須是具有單一鍵值對的 JSON 物件：MCP 工具名稱與覆寫描述字串。您可以在陣列中加入多個物件，以指定多個覆寫。

以下範例註冊一個僅公開 `get_alerts` 工具的代理程式（使用 `tool_filters`），並以代理程式專屬的指引取代其描述：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Weather & Search Bot",
  "type": "conversational",
  "description": "Uses MCP to fetch forecasts and OpenSearch indices",
  "llm": {
    "model_id": "<MODEL_ID_FROM_STEP_2>",
    "parameters": {
      "max_iteration": 5
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions",
    "mcp_connectors": [
      {
        "mcp_connector_id": "<MCP_CONNECTOR_ID_FROM_STEP_1>",
        "tool_filters": [
          "^get_alerts$"
        ],
        "tool_descriptions": [
          {
            "get_alerts": "Fetch active weather alerts for a US state. Use when the user asks about warnings or advisories."
          }
        ]
      }
    ]
  },
  "tools": [
    { "type": "ListIndexTool" }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

若要為多個工具覆寫描述而不套用 `tool_filters`，請省略 `tool_filters` 參數或將其設為空陣列，讓所有連接器工具保持可用：

```json
"mcp_connectors": [
  {
    "mcp_connector_id": "<MCP_CONNECTOR_ID_FROM_STEP_1>",
    "tool_descriptions": [
      { "get_alerts": "Fetch active weather alerts for a US state." },
      { "get_forecast": "Fetch a multi-day weather forecast for a city." }
    ]
  }
]
```

對於連接器未公開或被 `tool_filters` 排除的工具名稱所做的覆寫不會產生任何效果。對於沒有有效覆寫的任何工具，代理程式會繼續使用 MCP 伺服器的原始描述。

### Flow 代理程式與對話式 flow 代理程式
**3.8 版新增**
{: .label .label-purple }

對於 [`flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/) 與 [`conversational_flow`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational-flow/) 代理程式，MCP 工具會依照 `tools` 陣列中定義的固定順序執行。您必須明確宣告每個 MCP 工具，並讓工具 `type` 符合您的連接器協定。

| 連接器協定 | MCP 工具 `type` |
|:---|:---|
| `mcp_streamable_http` | `McpStreamableHttpTool` |
| `mcp_sse` | `McpSseTool` |

`tools` 陣列中的每個 MCP 工具項目支援下列欄位。

| 欄位 | 資料類型 | 必要 | 描述 |
|:---|:---|:---|:---|
| `name` | 字串 | 是 | MCP 伺服器工具名稱。必須符合所設定連接器公開的工具之一。用於輸出鏈結（例如 `${parameters.get_simple_price.output}`）。 |
| `type` | 字串 | 是 | `McpStreamableHttpTool` 或 `McpSseTool`，須符合連接器協定。 |
| `description` | 字串 | 否 | 工具的描述。若省略，OpenSearch 會在可用時使用來自 MCP 伺服器的描述。 |
| `parameters.input` | 字串 | 是 | 工具輸入承載，通常是傳遞給 MCP 伺服器工具的 JSON 字串。 |

您可以在同一個管線中將 MCP 工具與 OpenSearch 工具（例如 `MLModelTool`）混合使用。某個步驟的輸出可以使用 `${parameters.<tool_name>.output}` 傳遞給下一個步驟。

如果 MCP 工具列於 `tools` 中，但無法從所設定的連接器取得，代理程式執行將會失敗，並出現指出該工具無法使用的錯誤。如果多個 MCP 連接器公開同名工具，OpenSearch 會使用 `mcp_connectors` 陣列中第一個符合的連接器所提供的工具。

在註冊 flow 或對話式 flow 代理程式之前，請使用 [List Connector MCP Tools API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-client-apis/list-connector-mcp-tools/) 從您的 MCP 連接器探索工具名稱、類型、描述與輸入結構描述。在代理程式中設定 MCP 工具時，請使用回應中的 `name` 與 `type` 值，並根據每個工具的 `input_schema` 建構 `parameters.input` JSON 字串。

以下範例註冊一個 `flow` 代理程式，依序呼叫 `search_documents` 與 `get_weather`，然後使用 `MLModelTool` 摘要結果：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Research and weather flow agent",
  "type": "flow",
  "description": "Flow agent using MCP tools in a fixed order",
  "parameters": {
    "mcp_connectors": [
      {
        "mcp_connector_id": "<MCP_CONNECTOR_ID_FROM_STEP_1>"
      }
    ]
  },
  "tools": [
    {
      "name": "search_documents",
      "type": "McpStreamableHttpTool",
      "description": "Search a document repository for relevant content.",
      "parameters": {
        "input": "{\"query\":\"OpenSearch agentic search\",\"limit\":5}"
      }
    },
    {
      "name": "get_weather",
      "type": "McpStreamableHttpTool",
      "description": "Retrieve current weather conditions for a specified location.",
      "parameters": {
        "input": "{\"location\":\"Seattle\",\"units\":\"celsius\"}"
      }
    },
    {
      "name": "summarize_results",
      "type": "MLModelTool",
      "description": "Summarize MCP tool outputs",
      "parameters": {
        "model_id": "<MODEL_ID_FROM_STEP_2>",
        "prompt": "You are a research assistant.\n\nDocument search results:\n${parameters.search_documents.output}\n\nWeather:\n${parameters.get_weather.output}\n\nProvide a brief summary of the findings."
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要搭配對話記憶使用相同的 MCP 管線，請將 `type` 設為 `conversational_flow`，並在與 `parameters` 和 `tools` 相同的層級加入 `memory` 區塊：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Research and weather conversational flow agent",
  "type": "conversational_flow",
  "description": "Conversational flow agent using MCP tools in a fixed order",
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "mcp_connectors": [
      {
        "mcp_connector_id": "<MCP_CONNECTOR_ID_FROM_STEP_1>"
      }
    ]
  },
  "tools": [
    {
      "name": "search_documents",
      "type": "McpStreamableHttpTool",
      "description": "Search a document repository for relevant content.",
      "parameters": {
        "input": "{\"query\":\"OpenSearch agentic search\",\"limit\":5}"
      }
    },
    {
      "name": "get_weather",
      "type": "McpStreamableHttpTool",
      "description": "Retrieve current weather conditions for a specified location.",
      "parameters": {
        "input": "{\"location\":\"Seattle\",\"units\":\"celsius\"}"
      }
    },
    {
      "name": "summarize_results",
      "type": "MLModelTool",
      "description": "Summarize MCP tool outputs",
      "parameters": {
        "model_id": "<MODEL_ID_FROM_STEP_2>",
        "prompt": "You are a research assistant.\n\nDocument search results:\n${parameters.search_documents.output}\n\nWeather:\n${parameters.get_weather.output}\n\nProvide a brief summary of the findings."
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 4：執行代理程式

呼叫 Execute Agent API 並提供使用者問題，以叫用已註冊的代理程式：

```json
POST /_plugins/_ml/agents/{Agent_ID}/_execute
{
  "parameters": {
    "question": "Any weather alerts in Washington",
    "verbose": true
  }
}
```
{% include copy-curl.html %}

代理程式會同時使用 `tools` 陣列中指定的 OpenSearch 工具，以及來自 MCP 伺服器的所選工具 (依據您的工具篩選條件)，以傳回答案：

```json
{
    "inference_results": [
        {
            "output": [
                {
                    "name": "memory_id",
                    "result": "MfiZfpYBjoQOEoSH13wj"
                },
                {
                    "name": "parent_interaction_id",
                    "result": "MviZfpYBjoQOEoSH13xC"
                },
                {
                    "name": "response",
                    "result": "{\"id\":\"chatcmpl-BRRcdxVjkrKG7HjkVWZVwueJSEjgd\",\"object\":\"chat.completion\",\"created\":1.745880735E9,\"model\":\"gpt-4o-2024-08-06\",\"choices\":[{\"index\":0.0,\"message\":{\"role\":\"assistant\",\"tool_calls\":[{\"id\":\"call_yWg0wk4mfE2v8ARebupfbJ87\",\"type\":\"function\",\"function\":{\"name\":\"get_alerts\",\"arguments\":\"{\\\"state\\\":\\\"WA\\\"}\"}}],\"annotations\":[]},\"finish_reason\":\"tool_calls\"}],\"usage\":{\"prompt_tokens\":201.0,\"completion_tokens\":16.0,\"total_tokens\":217.0,\"prompt_tokens_details\":{\"cached_tokens\":0.0,\"audio_tokens\":0.0},\"completion_tokens_details\":{\"reasoning_tokens\":0.0,\"audio_tokens\":0.0,\"accepted_prediction_tokens\":0.0,\"rejected_prediction_tokens\":0.0}},\"service_tier\":\"default\",\"system_fingerprint\":\"fp_f5bdcc3276\"}"
                },
                {
                    "name": "response",
                    "result": "[{\"text\":\"\\nEvent: Wind Advisory\\nArea: Kittitas Valley\\nSeverity: Moderate\\nDescription: * WHAT...Northwest winds 25 to 35 mph with gusts up to 45 mph\\nexpected.\\n\\n* WHERE...Kittitas Valley.\\n\\n* WHEN...From 2 PM to 8 PM PDT Tuesday.\\n\\n* IMPACTS...Gusty winds will blow around unsecured objects. Tree\\nlimbs could be blown down and a few power outages may result.\\nInstructions: Winds this strong can make driving difficult, especially for high\\nprofile vehicles. Use extra caution.\\n\"}]"
                },
                {
                    "name": "response",
                    "result": "There is a Wind Advisory for the Kittitas Valley in Washington. Here are the details:\n\n- **Event:** Wind Advisory\n- **Area:** Kittitas Valley\n- **Severity:** Moderate\n- **Description:** Northwest winds 25 to 35 mph with gusts up to 45 mph expected.\n- **When:** From 2 PM to 8 PM PDT Tuesday.\n- **Impacts:** Gusty winds may blow around unsecured objects, potentially causing tree limbs to fall, and resulting in a few power outages.\n\n**Instructions:** These strong winds can make driving difficult, especially for high-profile vehicles. Use extra caution if you are traveling in the area."
                }
            ]
        }
    ]
}
```

## 其他資源

* 如需 MCP 通訊協定的詳細資訊，請參閱 [MCP 通訊協定文件](https://modelcontextprotocol.io/introduction)。
* 如需在 Java 中使用 MCP 的資訊，請參閱 [MCP Java SDK](https://github.com/modelcontextprotocol/java-sdk)。
