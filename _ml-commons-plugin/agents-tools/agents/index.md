---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式"
parent: Agents and tools
has_children: true
has_toc: false
nav_order: 10
redirect_from: 
  - /ml-commons-plugin/agents-tools/agents/
---

# 代理程式
**於 2.13 版推出**
{: .label .label-purple }

_代理程式_ 是一種協調器，會使用大型語言模型 (LLM) 來解決問題。在 LLM 進行推理並決定要採取的行動之後，代理程式會協調行動的執行。OpenSearch 支援下列代理程式類型：

- [_流程代理程式_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/)：依其組態中指定的順序，循序執行工具。流程代理程式的工作流程是固定的。適用於檢索增強生成 (RAG)。
- [_對話流程代理程式_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational-flow/)：依其組態中指定的順序，循序執行工具。對話流程代理程式的工作流程是固定的。會儲存對話歷程記錄，讓使用者可以提出後續問題。適用於建立聊天機器人。
- [_對話代理程式_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)：進行推理，以根據可用的知識提供回應，包括 LLM 知識庫以及提供給 LLM 的一組工具。LLM 會反覆進行推理，以決定要採取的行動，直到取得最終答案或達到反覆運算次數上限為止。會儲存對話歷程記錄，讓使用者可以提出後續問題。對話代理程式的工作流程會依後續問題而有所不同。針對特定問題，會使用思維鏈 (CoT) 程序，從已設定的工具中選出最適合用來提供問題回應的工具。適用於建立採用 RAG 的聊天機器人。
- [_對話代理程式 V2_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/#the-conversational_v2-agent-with-full-multimodal-support)：對話代理程式的增強版本，內建多模態支援且開箱即用，只需最少的組態。使用標準化介面接受文字、影像、文件和多重回合訊息歷程記錄作為輸入，不需要自訂連接器設定。會傳回標準化的輸出格式以及詞元用量指標。需要[統一註冊方法](#unified-registration-method)和 [Agentic Memory]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。
- [_規劃-執行-反思代理程式_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)：動態規劃、執行及調整多步驟工作流程，以解決複雜的工作。在內部，規劃-執行-反思代理程式會使用對話代理程式來執行計畫中的每個個別步驟。代理程式會根據工具描述和內容，自動為每個步驟選出最適合的工具。非常適合可受益於反覆推理和調適性執行的長時間執行、探索性流程。適用於進行研究或執行根本原因分析 (RCA)。
- [_AG-UI 代理程式_]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/ag-ui/)：遵循 AG-UI 通訊協定，將 AI 代理程式與前端應用程式整合。透過接受前端內容和工具，讓 OpenSearch 與 UI 之間能夠順暢通訊，使代理程式可以直接與 UI 元件和應用程式狀態互動。適用於互動式儀表板。

## 建立代理程式

您可以使用兩種註冊方法建立代理程式：一般註冊方法或統一註冊方法。

### 一般註冊方法

一般註冊方法使用 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)，且需要多個步驟才能建立代理程式：

1. **註冊連接器**：建立具有複雜 JSON 組態的連接器，包括 `request_body` 和 `url` 參數。
2. **註冊模型**：建立模型，手動參照步驟 1 中的 `connector_id`。
3. **註冊代理程式**：提供 `model_id`、設定 `_llm_interface` 參數，並將 `question` 對應至 `prompt`，以建立代理程式。
4. **執行代理程式**：僅使用有限的文字型 `question` 參數來執行代理程式。

### 統一註冊方法
**於 3.5 版推出**
{: .label .label-purple }

Unified Agent API 會自動設定連接器和模型，大幅降低在 OpenSearch 中使用代理程式的複雜度，進而簡化代理程式的建立和執行。Unified Agent API 會根據 `model` 區塊組態自動處理模型群組建立、連接器設定和模型註冊，只需一次 API 呼叫即可註冊代理程式：

1. **註冊代理程式** (會自動建立連接器和模型)。
2. 使用 `input` 欄位**執行代理程式**。

統一註冊方法和一般註冊方法有下列不同之處。

| 層面 | 一般註冊方法 | 統一註冊方法 |
| :--- | :--- | :--- |
| **工作流程步驟** | 1. 註冊連接器<br>2. 註冊模型<br>3. 註冊代理程式<br>4. 使用 `question` 參數執行 | 1. 註冊代理程式 (自動建立連接器/模型)<br>2. 使用彈性的 `input` 欄位執行 |
| **組態複雜度** | 手動設定連接器，包含請求本文、URL 和參數對應 | 自動設定，內建驗證和預設值 |
| **模型設定** | 建立代理程式之前需要個別註冊模型 | 在代理程式註冊期間自動建立模型資源 |
| **模型參照** | 使用 `llm.model_id` 參照預先註冊的模型 | 使用 `model` 區塊搭配供應商憑證和組態 |
| **LLM 介面** | 手動設定 `_llm_interface` 參數 | 從 `model_provider` 自動偵測 `_llm_interface` |
| **輸入功能** | 僅限文字型 `question` 參數 | 透過增強的執行 API 支援多模態輸入 (文字、影像、訊息) |

#### 支援的模型

支援下列模型：

- **Amazon Bedrock Converse API** 搭配 Anthropic Claude 模型
- **Google Gemini** 模型
- **OpenAI** 模型

#### 先決條件

Unified Agent API 預設為停用。若要啟用，請更新下列叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.unified_agent_api_enabled": true
  }
}
```
{% include copy-curl.html %}

如果您打算搭配統一代理程式使用 Model Context Protocol (MCP) 連接器，也請啟用 MCP 連接器支援：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.mcp_connector_enabled": true
  }
}
```
{% include copy-curl.html %}

#### 範例

下列範例示範統一註冊方法。

**步驟 1：註冊代理程式**

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My Conversational Agent",
  "type": "conversational",
  "description": "A conversational agent using OpenAI gpt-4o-mini",
  "model": {
    "model_id": "gpt-4o-mini",
    "model_provider": "openai/v1/chat/completions",
    "credential": {
      "openai_api_key": "sk-your-api-key"
    },
    "parameters": {
      "max_tokens": 1000,
      "temperature": 0.7
    }
  }
}
```
{% include copy-curl.html %}

如需所有模型供應商的完整註冊詳細資料、欄位定義和範例，請參閱[統一代理程式註冊]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#unified-agent-registration)。

**步驟 2：執行代理程式**

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "input": "What tools do you have access to?"
}
```
{% include copy-curl.html %}

如需執行詳細資料和輸入格式規格，請參閱[統一代理程式執行]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#unified-agent-execution)。

#### 限制

下列限制適用於統一註冊方法：

- **代理程式類型**：僅支援 `conversational`、`conversational_v2`、`plan_execute_and_reflect` 和 `AG_UI` 代理程式。
- **多模態輸入**：使用統一註冊方法時，內容區塊和訊息型輸入格式需要 `conversational_v2` 代理程式。所有其他統一代理程式類型 (包括使用 `conversation_index` 或 `agentic_memory` 的 `conversational` 代理程式) 僅接受純文字輸入。使用一般註冊方法時，如果連接器設定為將多模態內容傳遞至 LLM，則可支援多模態，輸入格式取決於連接器組態。

Unified Agent API 與現有代理程式完全回溯相容。使用一般註冊方法建立的代理程式會繼續正常運作。您可以在同一個叢集中使用這兩種註冊方法。

使用 Unified Agent API 建立的代理程式無法更新為使用一般註冊方法參數。
{: .note}

## 隱藏代理程式
**於 2.13 版推出**
{: .label .label-purple }

若要對終端使用者 (包括叢集管理員) 隱藏代理程式詳細資料，您可以註冊_隱藏_代理程式。如果代理程式已隱藏，非超級管理員使用者就沒有權限對該代理程式呼叫任何 [Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/index/)，但 [Execute API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/) 除外。

只有超級管理員使用者可以註冊隱藏代理程式。若要註冊隱藏代理程式，您必須先使用[管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)進行驗證：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -XGET 'https://localhost:9200/.opendistro_security/_search'
```
{% include copy.html %}

超級管理員使用者建立的所有代理程式都會自動註冊為隱藏。只有超級管理員使用者可以檢視隱藏代理程式詳細資料和刪除隱藏代理程式。
若要註冊隱藏代理程式，請將請求傳送至 `_register` 端點：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -X POST 'https://localhost:9200/_plugins/_ml/agents/_register' -H 'Content-Type: application/json' -d '
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
}'
```
{% include copy.html %}

## 後續步驟

- 若要進一步了解如何註冊代理程式，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。
- 如需支援的工具清單，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 如需逐步教學，請參閱[代理程式與工具教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents-tools-tutorial/)。
- 如需使用規劃-執行-反思代理程式的逐步教學，請參閱[建立規劃-執行-反思代理程式]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/)。
- 如需支援的 API，請參閱 [Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/)。
- 若要在組態自動化中使用代理程式和工具，請參閱[自動化組態]({{site.url}}{{site.baseurl}}/automating-configurations/index/)。
