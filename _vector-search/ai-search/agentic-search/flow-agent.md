---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用流程代理程式"
parent: Agentic search
grand_parent: AI search
nav_order: 20
has_children: false
---

# 使用流程代理程式進行代理式搜尋

流程代理程式提供了一種比對話式代理程式更精簡的替代方案。對話式代理程式使用多種工具進行靈活、具情境感知的搜尋，而流程代理程式則僅專注於查詢規劃。這可減少大型語言模型 (LLM) 呼叫次數、縮短回應時間並降低成本。

流程代理程式已足以因應大多數使用案例。當低延遲與成本效益是優先考量、查詢很簡單，且不需要對話記憶時，請使用流程代理程式。若需要複雜搜尋、多工具工作流程、持續性情境或最高查詢品質，請使用對話式代理程式。

流程代理程式與對話式代理程式的差異如下：

- 流程代理程式只使用一種工具---`QueryPlanningTool`。
- 您必須在搜尋請求中明確指定目標索引名稱。
- 流程代理程式不提供代理程式步驟摘要或推理追蹤 (使用 `agentic_context` 回應處理器時，只會提供產生的查詢領域特定語言 [DSL] 查詢)。
- 流程代理程式沒有對話記憶，無法在多次互動之間維持情境。

使用流程代理程式設定代理式搜尋有兩種方式：

- [**自動化工作流程**](#automated-workflow) (建議用於快速設定)：使用單一 API 呼叫自動建立索引以外的所有代理式搜尋資源。
- [**手動設定**](#manual-setup) (建議用於自訂組態)：手動設定每個元件，以獲得更大的靈活性與控制權。

## 自動化工作流程

OpenSearch 提供一個[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates#agentic-search-with-a-flow-agent)，會自動建立 Amazon Bedrock 連接器、遠端聊天模型、`QueryPlanningTool`、流程代理程式及搜尋管線。請檢閱工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/agentic-search-with-flow-agent-defaults.json)，以判斷您是否需要更新任何參數。若要使用流程代理程式建立預設的代理式搜尋工作流程，請傳送下列請求：

```json
POST /_plugins/_flow_framework/workflow?use_case=agentic_search_with_flow_agent&provision=true
{
  "create_connector.credential.access_key": "<your-aws-access-key>",
  "create_connector.credential.secret_key": "<your-aws-secret-key>",
  "create_connector.credential.session_token": "<your-aws-session-token>"
}
```
{% include copy-curl.html %}

OpenSearch 會回應所建立工作流程的工作流程 ID：

```json
{
  "workflow_id" : "abc123"
}
```

若要檢查工作流程狀態，請傳送下列請求：

```json
GET /_plugins/_flow_framework/workflow/abc123/_status
```
{% include copy-curl.html %}

工作流程完成後，`state` 會變更為 `COMPLETED`。工作流程會建立代理式搜尋資源，但不會建立索引。您可以使用佈建的搜尋管線查詢任何現有索引。如需查詢範例，請參閱[步驟 6](#step-6-run-an-agentic-search)。

## 手動設定

請使用下列步驟手動設定代理式搜尋流程。

## 步驟 1：建立產品索引

建立包含產品資料的範例索引，其中包含名稱、價格、顏色及類別等各種屬性：

```json
PUT /products-index
{
  "settings": {
    "number_of_shards": "4",
    "number_of_replicas": "2"
  },
  "mappings": {
    "properties": {
      "product_name": { "type": "text" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "currency": { "type": "keyword" },
      "rating": { "type": "float" },
      "review_count": { "type": "integer" },
      "in_stock": { "type": "boolean" },
      "color": { "type": "keyword" },
      "size": { "type": "keyword" },
      "category": { "type": "keyword" },
      "brand": { "type": "keyword" },
      "tags": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 2：匯入範例資料

將範例產品文件新增至索引：

```json
POST _bulk
{ "index": { "_index": "products-index", "_id": "1" } }
{ "product_name": "Nike Air Max 270", "description": "Comfortable running shoes with Air Max technology", "price": 150.0, "currency": "USD", "rating": 4.5, "review_count": 1200, "in_stock": true, "color": "white", "size": "10", "category": "shoes", "brand": "Nike", "tags": ["running", "athletic", "comfortable"] }
{ "index": { "_index": "products-index", "_id": "2" } }
{ "product_name": "Adidas Ultraboost 22", "description": "Premium running shoes with Boost midsole", "price": 180.0, "currency": "USD", "rating": 4.7, "review_count": 850, "in_stock": true, "color": "black", "size": "9", "category": "shoes", "brand": "Adidas", "tags": ["running", "premium", "boost"] }
{ "index": { "_index": "products-index", "_id": "3" } }
{ "product_name": "Converse Chuck Taylor", "description": "Classic canvas sneakers", "price": 65.0, "currency": "USD", "rating": 4.2, "review_count": 2100, "in_stock": true, "color": "white", "size": "8", "category": "shoes", "brand": "Converse", "tags": ["casual", "classic", "canvas"] }
{ "index": { "_index": "products-index", "_id": "4" } }
{ "product_name": "Puma RS-X", "description": "Retro-inspired running shoes with modern comfort", "price": 120.0, "currency": "USD", "rating": 4.3, "review_count": 750, "in_stock": true, "color": "black", "size": "9", "category": "shoes", "brand": "Puma", "tags": ["retro", "running", "comfortable"] }
```
{% include copy-curl.html %}

## 步驟 3：為代理程式與 QueryPlanningTool 建立模型

註冊一個同時供對話式代理程式與 `QueryPlanningTool` 使用的模型。此模型會分析自然語言問題、協調工具使用情形，並產生 OpenSearch DSL。如需可用的模型選項，請參閱[模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)：

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

## 步驟 4：註冊流程代理程式

接著，註冊流程代理程式。您必須在 `QueryPlanningTool` 參數中包含 `response_filter`，代理程式才能從您的模型供應商回應中正確擷取產生的 DSL：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Flow Agent for Agentic Search",
  "type": "flow",
  "description": "Flow agent for agentic search",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your_model_id_from_step_3",
        "response_filter": "<response-filter-based-on-model-type>"
      }
    }
  ]
}
```
{% include copy-curl.html %}

請根據您的模型供應商使用下列回應篩選條件：

- **OpenAI**：`"response_filter": "$.choices[0].message.content"`
- **Anthropic Claude (Amazon Bedrock Converse API)**：`"response_filter": "$.output.message.content[0].text"`

## 步驟 5：使用流程代理程式建立代理式管線

建立使用您流程代理程式將自然語言查詢轉譯為 DSL 的搜尋管線。您可以選擇性加入回應處理器，以檢視產生的 DSL 查詢：

```json
PUT _search/pipeline/agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your_flow_agentId_from_step_4"
      }
    }
  ],
  "response_processors": [
    {
      "agentic_context": {
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 6：執行代理式搜尋

若要執行代理式搜尋，請使用 `agentic` 查詢子句。流程代理程式*要求索引名稱*，因此您必須在搜尋請求中包含該名稱。流程代理程式不支援對話記憶，因此您不能包含 `memory_id` 參數：

```json
GET products-index/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find me white shoes under 150 dollars"
    }
  }
}
```
{% include copy-curl.html %}

流程代理程式會處理自然語言查詢，並在回應中傳回相符的產品以及產生的 DSL 查詢：

```json
{
  "took": 3965,
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
    "max_score": null,
    "hits": [
      {
        "_index": "products-index",
        "_id": "3",
        "_score": null,
        "_source": {
          "product_name": "Converse Chuck Taylor",
          "description": "Classic canvas sneakers",
          "price": 65.0,
          "currency": "USD",
          "rating": 4.2,
          "review_count": 2100,
          "in_stock": true,
          "color": "white",
          "size": "8",
          "category": "shoes",
          "brand": "Converse",
          "tags": [
            "casual",
            "classic",
            "canvas"
          ]
        },
        "sort": [
          4.2,
          2100
        ]
      }
    ]
  },
  "ext": {
    "dsl_query": "{\"size\":10.0,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category\":\"shoes\"}},{\"term\":{\"color\":\"white\"}},{\"range\":{\"price\":{\"lt\":150.0}}}]}},\"sort\":[{\"rating\":{\"order\":\"desc\"}},{\"review_count\":{\"order\":\"desc\"}}]}"
  }
}
```

