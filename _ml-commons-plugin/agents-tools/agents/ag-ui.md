---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AG-UI 代理程式"
has_children: false
has_toc: false
nav_order: 50
parent: Agents
grand_parent: Agents and tools
---

# AG-UI 代理程式
**於 3.5 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需功能進展的最新消息，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。    
{: .warning}

Agent-User Interaction (AG-UI) 代理程式遵循 [AG-UI 通訊協定](https://docs.ag-ui.com/introduction)，將 AI 代理程式與前端應用程式整合。此實作透過標準化的串流互動與精密的工具執行，將即時 AI 代理程式功能直接帶入使用者介面。

與[對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)類似，AG-UI 代理程式會以大語言模型 (LLM) 及選用工具進行設定。處理使用者輸入時，代理程式會使用 LLM 對請求進行推理，同時考量對話歷程與可用的前端情境。接著，代理程式會判斷要使用哪些工具並執行這些工具，以提供適當的回應。

AG-UI 代理程式可使用兩種類型的工具：
- **後端工具**：向代理程式註冊 (例如 `ListIndexTool` 或 `SearchIndexTool`)，用於查詢 OpenSearch 資料並執行伺服器端作業。
- **前端工具**：在每個請求中提供，讓代理程式能與 UI 互動，例如重新整理儀表板、套用篩選條件，或在頁面之間瀏覽。

## 先決條件

使用 AG-UI 代理程式之前，您必須更新叢集設定以啟用此功能。`ag_ui_enabled` 與 `stream_enabled` 設定為必要，而 `mcp_connector_enabled` (用於連線至 Model Context Protocol [MCP] 伺服器) 與 `unified_agent_api_enabled` 則為選用但建議設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.ag_ui_enabled": true,
    "plugins.ml_commons.stream_enabled": true,
    "plugins.ml_commons.mcp_connector_enabled": true,
    "plugins.ml_commons.unified_agent_api_enabled": true
  }
}
```
{% include copy-curl.html %}

## 建立 AG-UI 代理程式

AG-UI 代理程式使用統一註冊方法，將代理程式建立流程簡化為單一 API 呼叫。若要註冊 AG-UI 代理程式，請將 `type` 欄位設為 `AG_UI`，並使用 Unified Agent API 設定您的模型。

如需所有支援之模型供應商 (Amazon Bedrock、Google Gemini、OpenAI) 的完整註冊指示、欄位定義與範例，請參閱[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#unified-agent-registration)。

<!-- vale off -->
### 範例請求：Amazon Bedrock Converse
<!-- vale on -->

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
    "max_iteration": 5,
    "mcp_connectors": [{
        "mcp_connector_id": "<MCP CONNECTOR ID>" 
    }]
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

<!-- vale off -->
### 範例請求：OpenAI Chat Completion
<!-- vale on -->

```json
POST /_plugins/_ml/agents/_register
{
  "name": "AG-UI Agent",
  "type": "AG_UI",
  "description": "An AI agent designed for UI interactions with streaming support",
  "model": {
    "model_id": "<MODEL ID>",
    "model_provider": "openai/v1/chat/completions",
    "credential": {
      "openai_api_key": "<OPENAI API KEY>"
    },
    "model_parameters": {
      "system_prompt": "You are a helpful assistant and an expert in OpenSearch."
    }
  },
  "parameters": {
    "max_iteration": 50,
    "mcp_connectors": [{
        "mcp_connector_id": "<MCP CONNECTOR ID>"  
    }]
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

## 執行代理程式串流

AG-UI 代理程式使用專為前端應用程式設計的特殊執行通訊協定。與使用 `input` 欄位的一般代理程式執行 ([Execute Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/)) 不同，AG-UI 代理程式使用 AG-UI 通訊協定格式，並搭配前端情境、工具與串流回應。

### AG-UI 通訊協定格式

AG-UI 執行遵循 [AG-UI 通訊協定](https://docs.ag-ui.com/introduction)規格，在前端應用程式與 AI 代理程式之間提供結構化通訊。此通訊協定包含對話執行緒、前端工具整合與即時串流回應。

如需輸入格式規格的詳細資訊，請參閱 AG-UI 文件中的 [RunAgentInput](https://docs.ag-ui.com/sdk/js/core/types#runagentinput)。

### 請求欄位

下表列出請求欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `threadId` | 字串 | 必要 | 對話執行緒的唯一識別碼，由前端產生。用於在多個請求之間維持對話連續性，並啟用對話記憶。 |
| `runId` | 字串 | 必要 | 此執行緒中此次特定執行的唯一識別碼，由前端產生。每個新請求都應有新的 `runId`。 |
| `state` | 物件 | 必要 | 代理程式工作階段的目前內部狀態。可儲存工作流程狀態、使用者偏好設定，或在同一次執行中跨工具呼叫持續存在的特定工作階段資料。 |
| `messages` | 陣列 | 必要 | 對話訊息的陣列，包含使用者輸入與先前的助理回應。每則訊息都有 `id`、`role` (user/assistant) 與 `content`。 |
| `tools` | 陣列 | 必要 | 前端專屬工具的陣列，代理程式可呼叫這些工具與 UI 互動。每個工具都包含 `name`、`description` 與 `parameters` 結構定義，說明代理程式如何叫用 UI 動作。 |
| `context` | 陣列 | 必要 | 情境物件的陣列，向代理程式提供目前的應用程式狀態。包含作用中的儀表板、已套用的篩選條件、時間範圍，或任何可協助代理程式瞭解使用者目前情況的相關 UI 情境等資訊。 |
| `forwardedProps` | 物件 | 必要 | 從前端應用程式轉送的其他屬性，例如使用者驗證詳細資料、權限、應用程式組態，或代理程式作業所需的其他中繼資料。 |

#### 範例請求

下列範例顯示如何使用 AG-UI 通訊協定格式，搭配前端工具、對話情境與應用程式狀態來執行 AG-UI 代理程式：

```json
POST /_plugins/_ml/agents/{{agent_id}}/_execute/stream
{
    "threadId": "thread-xxxxx",
    "runId": "run-xxxxx",
    "messages": [
        {
            "id": "msg-xxxxx",
            "role": "user",
            "content": "hello"
        }
    ],
    "tools": [
        {
            "name": "frontend_tool_example",
            "description": "This is a frontend tool",
            "parameters": {
                ...
            }
        }
    ],
    "context": [
        {
            "description": "Page context example",
            "value": "{\"appId\":\"example\",\"timeRange\":{\"from\":\"now-15m\",\"to\":\"now\"},\"query\":{\"query\":\"example\",\"language\":\"PPL\"}}"
        }
    ],
    "state": {},
    "forwardedProps": {}
}
```
{% include copy-curl.html %}

### 範例回應

AG-UI 代理程式會回傳 Server-Sent Events (SSE)，讓前端能在代理程式處理請求時提供即時回饋：

```json
data: {"type":"RUN_STARTED","timestamp":1234567890,"threadId":"thread-xxxxx","runId":"run-xxxxx"}

data: {"type":"TEXT_MESSAGE_START","timestamp":1234567890,"messageId":"msg-xxxxx","role":"assistant"}

data: {"type":"TEXT_MESSAGE_CONTENT","timestamp":1234567890,"messageId":"msg-xxxxx","delta":"Response text here"}

data: {"type":"TEXT_MESSAGE_END","timestamp":1234567890,"messageId":"msg-xxxxx"}

data: {"type":"TOOL_CALL_START","timestamp":1234567890,"toolCallId":"tool-xxxxx","toolCallName":"frontend_tool_example"}

data: {"type":"TOOL_CALL_ARGS","timestamp":1234567890,"toolCallId":"tool-xxxxx","delta":"{\"param\":\"value\"}"}

data: {"type":"TOOL_CALL_END","timestamp":1234567890,"toolCallId":"tool-xxxxx"}

data: {"type":"RUN_FINISHED","timestamp":1234567890,"threadId":"thread-xxxxx","runId":"run-xxxxx"}
```

### 回應欄位

每個 SSE 包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `type` | 字串 | 事件類型。 |
| `timestamp` | Long | 事件產生時的 Unix 時間戳記，單位為毫秒。 |
| `threadId` | 字串 | 來自請求的對話執行緒 ID。 |
| `runId` | 字串 | 來自請求的執行 ID。 |
| `messageId` | 字串 | 訊息的唯一識別碼 (出現在訊息事件中)。 |
| `role` | 字串 | 訊息傳送者的角色，通常為 "assistant" (出現在訊息開始事件中)。 |
| `delta` | 字串 | 串流文字或工具引數的增量內容 (出現在 content/args 事件中)。 |
| `toolCallId` | 字串 | 工具呼叫的唯一識別碼 (出現在工具呼叫事件中)。 |
| `toolCallName` | 字串 | 被呼叫工具的名稱 (出現在工具呼叫開始事件中)。 |

### 事件類型

AG-UI 代理程式會在 `type` 欄位中回傳下列事件類型的 SSE。

| 事件類型 | 說明 |
| :--- | :--- |
| `RUN_STARTED` | 表示一次執行的開始 |
| `TEXT_MESSAGE_START` | 標記助理訊息的開始 |
| `TEXT_MESSAGE_CONTENT` | 包含增量文字內容 (串流) |
| `TEXT_MESSAGE_END` | 標記助理訊息的結束 |
| `TOOL_CALL_START` | 表示一次工具呼叫的開始 |
| `TOOL_CALL_ARGS` | 包含增量工具呼叫引數 |
| `TOOL_CALL_END` | 標記工具呼叫的結束 |
| `RUN_FINISHED` | 表示一次執行的完成 |

## 追蹤詞元用量
**3.6 版新增**
{: .label .label-purple }

AG-UI 代理程式支援詞元用量追蹤，可提供代理程式執行期間每次 LLM 呼叫的詳細詞元消耗指標。詞元用量會作為串流事件序列的一部分傳送。

對於 AG-UI 代理程式，詞元用量追蹤是在代理程式註冊時，透過在 `parameters` 欄位中設定 `"include_token_usage": true` 來啟用。這同時適用於統一註冊方法 (新介面) 與一般註冊方法 (舊介面)。代理程式註冊後，此設定在代理程式執行期間無法變更，必須在註冊時設定。

### 在註冊時啟用詞元用量追蹤 (統一方法)

若要使用統一註冊方法為 AG-UI 代理程式啟用詞元用量追蹤，請在註冊時於 `parameters` 欄位中加入 `include_token_usage` 參數：

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
    "max_iteration": 5,
    "include_token_usage": true
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

### 在註冊時啟用詞元用量追蹤 (一般方法)

或者，您可以使用一般註冊方法啟用詞元用量追蹤，方法是在代理程式的 `parameters` 中加入 `include_token_usage`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "AG-UI Agent",
  "type": "AG_UI",
  "llm": {
    "model_id": "<MODEL_ID>",
    "parameters": {
      "max_iteration": 5
    }
  },
  "tools": [{
    "type": "ListIndexTool"
  }],
  "parameters": {
    "include_token_usage": true
  },
  "memory": {
    "type": "conversation_index"
  }
}
```
{% include copy-curl.html %}

### 串流回應中的詞元用量

啟用詞元用量追蹤後，串流回應會在 `RUN_FINISHED` 事件之後包含一個帶有詞元用量指標的 `Custom` 事件。這些指標包含每輪與每個模型的詞元消耗：

```json
data: {"type":"RUN_STARTED","timestamp":1775501029508,"threadId":"thread-agui-new-agmem-postman","runId":"run-postman-agui-new-am"}

data: {"type":"TOOL_CALL_START","timestamp":1775501031547,"toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w","toolCallName":"ListIndexTool"}

data: {"type":"TOOL_CALL_ARGS","timestamp":1775501031549,"toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w","delta":""}

data: {"type":"TOOL_CALL_ARGS","timestamp":1775501031814,"toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w","delta":"{\"indi"}

data: {"type":"TOOL_CALL_ARGS","timestamp":1775501031814,"toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w","delta":"ces\": []}"}

data: {"type":"TOOL_CALL_END","timestamp":1775501031893,"toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w"}

data: {"type":"TOOL_CALL_RESULT","timestamp":1775501031911,"messageId":"msg_66642762007875","toolCallId":"tooluse_Z8ov0YNqeAW8B2h1qNH49w","content":"..."}

data: {"type":"TEXT_MESSAGE_START","timestamp":1775501033817,"messageId":"msg_66644668213500","role":"assistant"}

data: {"type":"TEXT_MESSAGE_CONTENT","timestamp":1775501033818,"messageId":"msg_66644668213500","delta":"Here are all the indices..."}

data: {"type":"TEXT_MESSAGE_END","timestamp":1775501041102,"messageId":"msg_66644668213500"}

data: {"type":"Custom","timestamp":1775501041115,"name":"token_usage","value":{"per_turn_usage":[{"model_name":"Auto-generated model for us.anthropic.claude-sonnet-4-5-20250929-v1:0","model_url":"https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-5-20250929-v1:0/converse","total_tokens":4806.0,"output_tokens":54.0,"turn":1.0,"model_id":"9RIbZJ0B1Feno22Ak-7G","input_tokens":4752.0},{"model_name":"Auto-generated model for us.anthropic.claude-sonnet-4-5-20250929-v1:0","model_url":"https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-5-20250929-v1:0/converse","total_tokens":6262.0,"output_tokens":898.0,"turn":2.0,"model_id":"9RIbZJ0B1Feno22Ak-7G","input_tokens":5364.0}],"per_model_usage":[{"model_name":"Auto-generated model for us.anthropic.claude-sonnet-4-5-20250929-v1:0","model_url":"https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-5-20250929-v1:0/converse","call_count":2.0,"total_tokens":11068.0,"output_tokens":952.0,"model_id":"9RIbZJ0B1Feno22Ak-7G","input_tokens":10116.0}]}}

data: {"type":"RUN_FINISHED","timestamp":1775501041116,"threadId":"thread-agui-new-agmem-postman","runId":"run-postman-agui-new-am"}
```

`token_usage` 事件包含：
- **`per_turn_usage`**：代理程式執行期間每一輪的詞元指標，包括 `turn` 數量、`model_id`、`model_name`、`model_url`、`input_tokens`、`output_tokens` 與 `total_tokens`。
- **`per_model_usage`**：依模型分組的彙總詞元指標，包括 `model_id`、`model_name`、`model_url`、`call_count`、`input_tokens`、`output_tokens` 與 `total_tokens`。

如需有關詞元用量欄位以及不同模型供應商如何計算詞元的詳細資訊，請參閱 Execute Agent API 文件中的 [追蹤詞元用量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#tracking-token-usage)。

## 後續步驟

- 如需 AG-UI 代理程式註冊，請參閱[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)。
- 如需統一代理程式執行，請參閱[統一代理程式執行]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#unified-agent-execution)。
- 了解 [AG-UI 通訊協定規格](https://docs.ag-ui.com/introduction)。
- 探索代理程式可用的後端[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 檢閱[代理程式 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/) 以了解其他功能。
