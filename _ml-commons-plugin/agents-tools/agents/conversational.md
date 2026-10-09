---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對話式代理程式"
has_children: false
has_toc: false
nav_order: 30
parent: Agents
grand_parent: Agents and tools
---

# 對話式代理程式
**於 2.13 版推出**
{: .label .label-purple }

對話式代理程式使用大型語言模型 (LLM) 及一組輔助工具，以反覆推理並提供回應。代理程式會使用思維鏈 (Chain-of-Thought, CoT) 流程為每個問題選取最佳工具，並儲存對話歷史記錄，讓使用者能提出後續問題。對話式代理程式使用[函式呼叫]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)來叫用工具。

OpenSearch 提供兩種類型的對話式代理程式：

- **[`conversational_v2` 代理程式](#the-conversational_v2-agent-with-full-multimodal-support)** (OpenSearch 3.6 及更新版本)：透過標準化介面提供內建多模態支援的增強型代理程式。需要[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)及[代理程式記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。

- **[`conversational` 代理程式 (v1)](#the-conversational-agent-v1)** (OpenSearch 2.13 及更新版本)：同時支援[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method) (僅限純文字輸入) 及[一般註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#regular-registration-method) (功能取決於連接器)。同時支援 `conversation_index` 與 `agentic_memory` 記憶體類型。

## 具備完整多模態支援的 `conversational_v2` 代理程式
**於 3.6 版推出**
{: .label .label-purple }

`conversational_v2` 代理程式擴充了 `conversational` 代理程式，透過[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)提供內建多模態支援，不需要自訂連接器組態。`conversational` 代理程式在使用統一註冊方法時僅接受純文字輸入，而 `conversational_v2` 代理程式則支援下列輸入格式：

- **純文字**：簡單的字串輸入。
- **內容區塊**：包含文字、影像及文件的多模態陣列。
- **訊息**：具備角色及多模態內容區塊的完整對話歷史記錄，可用於多輪互動。

代理程式會傳回包含停止原因、助理訊息、記憶體工作階段 ID 及詞元使用指標的回應。`conversational_v2` 代理程式需要 `agentic_memory` 記憶體類型。

### 先決條件

`conversational_v2` 代理程式使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)，且需要啟用統一代理程式 API。如需設定指示，請參閱[先決條件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#prerequisites)。

### 註冊 `conversational_v2` 代理程式

若要註冊 `conversational_v2` 代理程式，請依照下列步驟操作。

**步驟 1：建立記憶體容器**

註冊 `conversational_v2` 代理程式之前，請先使用 [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/) 建立記憶體容器：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "my-agent-memory"
}
```
{% include copy-curl.html %}

這會建立具有預設設定的記憶體容器。視您的使用情境而定，您可能會想設定其他選項，例如 `disable_session`、`embedding_model_id` 或記憶體策略。如需所有可用選項，請參閱 [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)。

回應會傳回 `memory_container_id`，供您在註冊代理程式時使用：

```json
{
  "memory_container_id": "SdjmmpgBOh0h20Y9kWuN",
  "status": "created"
}
```

**步驟 2：註冊代理程式**

若要註冊代理程式，請傳送下列請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My Conversational Agent V2",
  "type": "conversational_v2",
  "description": "A multimodal conversational agent",
  "model": {
    "model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "model_provider": "bedrock/converse",
    "credential": {
      "access_key": "<YOUR_AWS_ACCESS_KEY>",
      "secret_key": "<YOUR_AWS_SECRET_KEY>",
      "session_token": "<YOUR_SESSION_TOKEN>"
    }
  },
  "memory": {
    "type": "agentic_memory",
    "memory_container_id": "<YOUR_MEMORY_CONTAINER_ID>"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    }
  ]
}
```
{% include copy-curl.html %}

### 執行 `conversational_v2` 代理程式

`conversational_v2` 代理程式使用 `input` 欄位，並支援下列輸入格式：

- **純文字輸入**：

    ```json
    POST /_plugins/_ml/agents/{agent_id}/_execute
    {
      "input": "What indexes are in my cluster?"
    }
    ```
    {% include copy-curl.html %}

- **多模態內容區塊輸入**：

    ```json
    POST /_plugins/_ml/agents/{agent_id}/_execute
    {
      "input": [
        {
          "type": "text",
          "text": "What can you see in this image?"
        },
        {
          "type": "image",
          "source": {
            "type": "base64",
            "format": "png",
            "data": "iVBORw0KGgoAAAANSUhEUgAA..."
          }
        }
      ]
    }
    ```
    {% include copy-curl.html %}

- **訊息輸入** (多輪對話歷史記錄)：

    ```json
    POST /_plugins/_ml/agents/{agent_id}/_execute
    {
      "input": [
        {
          "role": "user",
          "content": [{"type": "text", "text": "I like the color red"}]
        },
        {
          "role": "assistant",
          "content": [{"type": "text", "text": "Thanks for sharing that!"}]
        },
        {
          "role": "user",
          "content": [{"type": "text", "text": "What color do I like?"}]
        }
      ]
    }
    ```
    {% include copy-curl.html %}

### `conversational_v2` 代理程式回應格式

`conversational_v2` 代理程式會傳回標準化的回應格式：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "stop_reason": "end_turn",
            "message": {
              "role": "assistant",
              "content": [
                {
                  "text": "Based on your cluster, I found the following indexes..."
                }
              ]
            },
            "memory_id": "test_memory_id",
            "metrics": {
              "total_usage": {
                "inputTokens": 1234,
                "outputTokens": 567,
                "totalTokens": 1801
              }
            }
          }
        }
      ]
    }
  ]
}
```

如需 `conversational_v2` 代理程式回應欄位，請參閱[`conversational_v2` 代理程式回應格式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#the-conversational_v2-agent-response-format)。

### 限制

下列限制適用於 `conversational_v2` 代理程式：

- **記憶體類型**：僅支援 `agentic_memory`。`conversation_index` 記憶體類型與 `conversational_v2` 代理程式不相容。
- **串流**：不支援串流回應。
- **掛鉤與上下文管理**：不支援代理程式執行掛鉤與上下文管理。

## `conversational` 代理程式（v1）

`conversational` 代理程式支援兩種註冊方法，各有不同的功能：

- **[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)**：僅接受純文字輸入。使用 `model` 欄位設定 LLM 組態。
- **[一般註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#regular-registration-method)**：輸入功能取決於連接器組態。使用 `llm` 欄位設定 LLM 組態。如果您將連接器設定為將多模態內容傳遞給 LLM，即可支援多模態輸入。

若要透過標準化介面取得完整的多模態支援，請使用 [`conversational_v2` 代理程式](#the-conversational_v2-agent-with-full-multimodal-support)。
{: .note}

您可以為 `conversational` 代理程式設定大型語言模型（LLM）和一組執行特定工作的輔助工具。例如，您可以設定 LLM 和 `ListIndexTool`。當您向模型提出問題時，代理程式會將 `ListIndexTool` 納入上下文。接著，LLM 會決定是否需要使用工具來回答「我的叢集中有多少個索引？」之類的問題。這讓 LLM 能夠回答其知識庫範圍之外的問題。

### 使用統一註冊方法

下列範例使用統一註冊方法註冊 `conversational` 代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My Conversational Agent",
  "type": "conversational",
  "description": "A conversational agent using unified registration",
  "model": {
    "model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "model_provider": "bedrock/converse",
    "credential": {
      "access_key": "<YOUR_AWS_ACCESS_KEY>",
      "secret_key": "<YOUR_AWS_SECRET_KEY>",
      "session_token": "<YOUR_SESSION_TOKEN>"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    }
  ]
}
```
{% include copy-curl.html %}

### 使用一般註冊方法

下列範例使用一般註冊方法註冊 `conversational` 代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_ReAct_ClaudeV2",
  "type": "conversational",
  "description": "This is a test agent",
  "llm": {
    "model_id": "YOUR_LLM_MODEL_ID",
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
      "description": "A tool to search OpenSearch index with natural language question. If you don't know answer for some question, you should always try to search data with this tool. Action Input: <natural language question>",
      "parameters": {
        "model_id": "YOUR_TEXT_EMBEDDING_MODEL_ID",
        "index": "my_test_data",
        "embedding_field": "embedding",
        "source_field": [ "text" ],
        "input": "${parameters.question}"
      }
    },
    {
      "type": "ListIndexTool",
      "name": "ListIndexTool",
      "description": "Use this tool to get OpenSearch index information: (health, status, index, uuid, primary count, replica count, docs.count, docs.deleted, store.size, primary.store.size)."
    }
  ],
  "app_type": "my app"
}
```
{% include copy-curl.html %}

## 追蹤詞元用量
**於 3.6 版推出**
{: .label .label-purple }

對話式代理程式支援追蹤詞元用量，可提供代理程式執行期間每次 LLM 呼叫的詞元耗用詳細指標。這有助於您監控成本、偵錯效能問題，以及比較模型效率。

若要啟用詞元用量追蹤，請在執行代理程式時將 `include_token_usage` 參數設為 `true`。回應將包含 `token_usage` 輸出，其中提供依每個對話回合和每個模型彙總的指標。如需詞元用量欄位及不同模型供應商如何計算詞元的詳細資訊，請參閱 Execute Agent API 文件中的[追蹤詞元用量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#tracking-token-usage)。

## 後續步驟

- 若要進一步瞭解如何註冊代理程式，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。
- 如需支援的工具清單，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 如需逐步教學，請參閱[代理程式與工具教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。
- 如需支援的 API，請參閱[代理程式 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/)。
- 若要在組態自動化中使用代理程式與工具，請參閱[自動化組態]({{site.url}}{{site.baseurl}}/automating-configurations/index/)。
