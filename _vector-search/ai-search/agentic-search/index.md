---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式搜尋"
parent: AI search
nav_order: 75
has_children: true
has_toc: false
redirect_from:
  - /vector-search/ai-search/agentic-search/
---

# 代理程式搜尋
**於 3.2 版導入**
{: .label .label-purple }

代理程式搜尋 (agentic search) 讓您能以自然語言提問，並由 OpenSearch 自動規劃與執行擷取作業。預先設定的代理程式會讀取問題、規劃搜尋，並傳回相關結果。

您可以透過 API 或 OpenSearch Dashboards 設定代理程式搜尋。本指南說明如何使用 API 設定代理程式搜尋。若要了解如何在 OpenSearch Dashboards 中設定，請參閱 [建立代理程式搜尋流程]({{site.url}}{{site.baseurl}}/vector-search/ai-search/building-agentic-search-flows/)。

## 代理程式類型

代理程式搜尋支援兩種代理程式類型，各自針對不同的使用情境最佳化。

### 對話式代理程式

對話式代理程式提供最靈活且強大的代理程式搜尋體驗。它們支援多種工具、對話記憶，以及詳細的推理軌跡。當您需要以下功能時，請使用對話式代理程式：

- **多工具工作流程**：自動探索索引、分析綱要，以及整合外部資料。
- **對話記憶**：能夠使用記憶 ID 在多個查詢之間延續對話。
- **複雜推理**：詳細的逐步推理軌跡與工具協調。
- **最高查詢品質**：處理複雜或模糊查詢時的最大靈活性。

### 流程代理程式

流程代理程式 (flow agent) 提供精簡的替代方案，僅專注於查詢規劃。它們只使用 `QueryPlanningTool`，因此回應時間更快且成本更低。當您需要以下功能時，請使用流程代理程式：

- **低延遲**：減少大型語言模型 (LLM) 呼叫次數，加快查詢處理速度。
- **成本效益**：降低運算負擔與 API 成本。
- **簡單查詢**：無需複雜推理的直接搜尋需求。
- **已知索引**：當您可以直接在請求中指定目標索引時。

下列教學使用對話式代理程式。若要了解流程代理程式，請參閱 [使用流程代理程式進行代理程式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/flow-agent/)。

## 必要條件

使用代理程式搜尋之前，您必須先使用 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/) 設定代理程式。

## 步驟 1：建立用於匯入的索引

建立用於匯入的索引：

```json
PUT /iris-index
{
  "mappings": {
    "properties": {
      "petal_length_in_cm": {
        "type": "float"
      },
      "petal_width_in_cm": {
        "type": "float"
      },
      "sepal_length_in_cm": {
        "type": "float"
      },
      "sepal_width_in_cm": {
        "type": "float"
      },
      "species": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 2：將文件匯入索引

若要將文件匯入上一個步驟建立的索引，請傳送下列請求：

```json
POST _bulk
{ "index": { "_index": "iris-index", "_id": "1" } }
{ "petal_length_in_cm": 1.4, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 5.1, "sepal_width_in_cm": 3.5, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "2" } }
{ "petal_length_in_cm": 4.5, "petal_width_in_cm": 1.5, "sepal_length_in_cm": 6.4, "sepal_width_in_cm": 2.9, "species": "versicolor" }
```
{% include copy-curl.html %}

## 步驟 3：為代理程式與 QueryPlanningTool 建立模型

註冊一個同時供對話式代理程式與 `QueryPlanningTool` 使用的模型。此模型會分析自然語言問題、協調工具使用，並產生 OpenSearch 查詢領域特定語言 (DSL)。如需可用的模型選項，請參閱 [模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)：

```json
POST /_plugins/_ml/models/_register
{
    "name": "My OpenAI model: gpt-5",
    "function_name": "remote",
    "description": "test model",
    "connector": {
        "name": "My openai connector: gpt-5",
        "description": "The connector to openai chat model",
        "version": 1,
        "protocol": "http",
        "parameters": {
            "model": "gpt-5"
        },
        "credential": {
            "openAI_key": "<OPEN AI KEY>"    
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Authorization": "Bearer ${credential.openAI_key}"
                },
                "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_prompt}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.user_prompt}\"}${parameters._interactions:-}], \"reasoning_effort\":\"low\"${parameters.tool_configs:-}}"
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 步驟 4：建立代理程式

建立一個帶有 `QueryPlannerTool` (必要) 的 `conversational` 代理程式。您可以視需要新增其他工具。

### 建立使用對話索引記憶的代理程式

下列範例建立一個使用 `conversation_index` 記憶的 `conversational` 代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT 5 Agent for Agentic Search",
  "type": "conversational",
  "description": "Use this for Agentic Search",
  "llm": {
    "model_id": <Model ID from Step 3>,
    "parameters": {
      "max_iteration": 15,
      "embedding_model_id": "<Provide if you want to do neural search>"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions"
  },
  "tools": [
    {
      "type": "QueryPlanningTool"
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

### 建立使用代理程式記憶的代理程式

若要儲存記憶與互動，您可以設定代理程式使用 [代理程式記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。如需更多資訊，請參閱 [使用代理程式記憶]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agentic-memory/)。下列範例建立一個使用 `agentic_memory` 記憶的 `conversational` 代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT 5 Agent for Agentic Search",
  "type": "conversational",
  "description": "Use this for Agentic Search",
  "llm": {
    "model_id": <Model ID from Step 3>,
    "parameters": {
      "max_iteration": 15,
      "embedding_model_id": "<Provide if you want to do neural search>"
    }
  },
  "memory": {
    "type": "agentic_memory",
    "memory_container_id": <Memory Container ID>
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions"
  },
  "tools": [
    {
      "type": "QueryPlanningTool"
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

## 步驟 5：建立搜尋管線

建立一個包含代理程式查詢轉譯器搜尋請求處理器的搜尋管線，並傳入上一個步驟建立的代理程式 ID：

```json
PUT _search/pipeline/agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "<Agent ID from Step 4>"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 6：搜尋索引

若要執行代理程式搜尋，請使用 `agentic` 查詢。`query_text` 參數包含自然語言問題，`query_fields` 參數則列出代理程式在產生搜尋查詢時應考量的欄位：

```json
GET iris-index/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "List all the flowers present",
      "query_fields": ["species", "petal_length_in_cm"]
    }
  }
}
```
{% include copy-curl.html %}

代理程式搜尋請求會以 `QueryPlanningTool` 執行代理程式，並將自然語言問題連同索引對應與預設提示傳送至 LLM 以產生 DSL 查詢。傳回的 DSL 查詢隨後會在 OpenSearch 中作為搜尋請求執行：

```json
"hits": {
  "total": {
    "value": 2,
    "relation": "eq"
  },
  "max_score": 1.0,
  "hits": [
    {
      "_index": "iris-index",
      "_id": "1",
      "_score": 1.0,
      "_source": {
        "petal_length_in_cm": 1.4,
        "petal_width_in_cm": 0.2,
        "sepal_length_in_cm": 5.1,
        "sepal_width_in_cm": 3.5,
        "species": "setosa"
      }
    },
    {
      "_index": "iris-index",
      "_id": "2",
      "_score": 1.0,
      "_source": {
        "petal_length_in_cm": 4.5,
        "petal_width_in_cm": 1.5,
        "sepal_length_in_cm": 6.4,
        "sepal_width_in_cm": 2.9,
        "species": "versicolor"
      }
    }
  ]
}
```

## 進階組態

設定基本代理程式搜尋之後，您可以使用下列進階功能強化實作：

- [設定代理程式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/) -- 了解如何使用不同的模型、工具與組態來設定您的代理程式搜尋代理程式。

- [使用流程代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/flow-agent/) -- 當您不需要對話記憶或複雜的工具協調時，使用精簡的流程代理程式來進行更快、更具成本效益的查詢規劃。

- [設定語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/neural-search/) -- 設定代理程式根據使用者意圖自動在關鍵字搜尋與語意向量搜尋之間做選擇，為概念性問題提供更相關的結果。

- [新增搜尋範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/search-templates/) -- 新增預先定義的搜尋範本，以處理 LLM 難以穩定產生的複雜查詢模式，確保查詢結構可預測並提升可靠性。

- [連接外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/mcp-server/) -- 透過 Model Context Protocol (MCP) 伺服器擴充代理程式搜尋的外部工具與資料來源，以強化功能並即時存取資訊。

- [建立代理程式搜尋流程]({{site.url}}{{site.baseurl}}/vector-search/ai-search/building-agentic-search-flows/) -- 使用 OpenSearch Dashboards 中的 AI 搜尋流程來設定代理程式並執行代理程式搜尋。

- [重新排序代理程式搜尋結果]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/rerank-agentic-search-results/) -- 在您的代理程式搜尋管線中新增 rerank 搜尋回應處理器，以進一步重新排序搜尋結果。

- [使用代理程式記憶]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agentic-memory/) -- 設定代理程式搜尋使用記憶容器來儲存記憶與互動，讓對話之間能保有持續的上下文。

## 後續步驟

- [檢視代理程式搜尋並延續對話]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/) -- 檢視代理程式行為、查看產生的 DSL，並使用記憶 ID 延續對話。