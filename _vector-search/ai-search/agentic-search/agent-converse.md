---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用對話式代理程式"
parent: Agentic search
grand_parent: AI search
nav_order: 70
has_children: false
---

# 將對話式代理程式用於代理程式搜尋

對話式代理程式提供進階的代理程式搜尋功能，包含詳細的推理追蹤與對話記憶。不同於依序執行工具、且只傳回產生的查詢領域特定語言 (DSL) 查詢的流程代理程式，對話式代理程式會透過 `agentic_context` 回應處理器提供額外的內容，包括逐步推理摘要，以及用於跨多個查詢延續對話的記憶 ID。

本指南示範如何設定具備多個工具的對話式代理程式，並在複雜的搜尋情境中使用其進階功能。

使用對話式代理程式設定代理程式搜尋有兩種方式：

- [**自動化工作流程**](#automated-workflow) (建議用於快速設定)：透過單一 API 呼叫自動建立除索引以外的所有代理程式搜尋資源。
- [**手動設定**](#manual-setup) (建議用於自訂組態)：手動設定每個元件，以獲得更大的彈性與控制。

## 自動化工作流程

OpenSearch 提供一個[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates#agentic-search-with-a-conversational-agent)，會自動建立 Amazon Bedrock 連接器、遠端聊天模型、`QueryPlanningTool`、`ListIndexTool`、`IndexMappingTool`、具備對話記憶的對話式代理程式，以及搜尋管線。請檢視工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/agentic-search-with-conversational-agent-defaults.json)，以判斷是否需要更新任何參數。若要建立使用對話式代理程式的預設代理程式搜尋工作流程，請傳送以下請求：

```json
POST /_plugins/_flow_framework/workflow?use_case=agentic_search_with_conversational_agent&provision=true
{
  "create_connector.credential.access_key": "<your-aws-access-key>",
  "create_connector.credential.secret_key": "<your-aws-secret-key>",
  "create_connector.credential.session_token": "<your-aws-session-token>"
}
```
{% include copy-curl.html %}

OpenSearch 會以所建立工作流程的工作流程 ID 回應：

```json
{
  "workflow_id" : "abc123"
}
```

若要檢查工作流程狀態，請傳送以下請求：

```json
GET /_plugins/_flow_framework/workflow/abc123/_status
```
{% include copy-curl.html %}

工作流程完成後，`state` 會變更為 `COMPLETED`。此工作流程會建立代理程式搜尋資源，但不會建立索引。您可以使用已佈建的搜尋管線查詢任何現有的索引。查詢範例請參閱[步驟 6](#step-6-run-an-agentic-search)。

## 手動設定

請依照下列步驟手動設定代理程式對話流程。

## 步驟 1：建立產品索引

建立一個包含產品資料的範例索引，其中包含名稱、價格、顏色與類別等各種屬性：

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

將範例產品文件加入索引：

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

## 步驟 3：建立模型

請檢視[模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)並選擇要使用的模型。

以下範例註冊一個 GPT 模型，該模型將同時供對話式代理程式與 `QueryPlanningTool` 使用：

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
            "openAI_key": "your-openai-api-key"
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

## 步驟 4：註冊代理程式

註冊一個具備多個工具的對話式代理程式---`ListIndexTool` 用於探索可用的索引、`IndexMappingTool` 用於了解索引結構、`WebSearchTool` 用於存取外部資料，以及產生 OpenSearch DSL 所需的 `QueryPlanningTool`。

基本組態請參閱[設定代理程式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/)。代理程式必須包含一個 `QueryPlanningTool`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "E-commerce Search Agent",
  "type": "conversational",
  "description": "Intelligent e-commerce search with product discovery",
  "llm": {
    "model_id": "your-model-id",
    "parameters": {
      "max_iteration": 20
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
      "type": "ListIndexTool",
      "name": "ListIndexTool"
    },
    {
      "type": "IndexMappingTool",
      "name": "IndexMappingTool"
    },
    {
      "type": "WebSearchTool",
      "parameters": {
        "engine": "duckduckgo"
      }
    },
    {
      "type": "QueryPlanningTool"
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

## 步驟 5：設定搜尋管線

建立同時包含請求與回應處理器的搜尋管線。[`agentic_query_translator` 請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) 會將自然語言查詢轉譯為 OpenSearch DSL，而 [`agentic_context` 回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/) 則會加入代理程式執行情境資訊，以供監控及對話延續使用：

```json
PUT _search/pipeline/agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-ecommerce-agent-id"
      }
    }
  ],
  "response_processors": [
    {
      "agentic_context": {
        "agent_steps_summary": true,
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 6：執行代理式搜尋

若要執行搜尋，請傳送自然語言搜尋查詢。代理程式會分析請求、探索適當的索引，並產生最佳化的 DSL 查詢：

```json
GET /_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find me white shoes under 150 dollars"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的產品；`ext` 物件則包含詳細的代理程式資訊，顯示代理程式的推理過程及所產生的 DSL 查詢：

```json
{
  "took": 12146,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "products-index",
        "_id": "3",
        "_score": 0.0,
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
          65.0,
          0.0
        ]
      },
      {
        "_index": "products-index",
        "_id": "1",
        "_score": 0.0,
        "_source": {
          "product_name": "Nike Air Max 270",
          "description": "Comfortable running shoes with Air Max technology",
          "price": 150.0,
          "currency": "USD",
          "rating": 4.5,
          "review_count": 1200,
          "in_stock": true,
          "color": "white",
          "size": "10",
          "category": "shoes",
          "brand": "Nike",
          "tags": [
            "running",
            "athletic",
            "comfortable"
          ]
        },
        "sort": [
          150.0,
          0.0
        ]
      }
    ]
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: ListIndexTool — input: \"[]\"; context gained: \"Found indices; 'products-index' appears most relevant for product queries\"\nSecond I used: query_planner_tool — qpt.question: \"Find white shoes under 150 dollars.\"; index_name_provided: \"products-index\"\nThird I used: query_planner_tool — qpt.question: \"Find white shoes priced under 150 dollars.\"; index_name_provided: \"products-index\"\nValidation: qpt output is valid JSON and aligns with the request for white shoes under 150 dollars in the products-index.",
    "memory_id": "XRzFl5kB-5P992SCeeqO",
    "dsl_query": "{\"size\":10.0,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category\":\"shoes\"}},{\"term\":{\"color\":\"white\"}},{\"range\":{\"price\":{\"lte\":150.0}}}]}},\"sort\":[{\"price\":{\"order\":\"asc\"}},{\"_score\":{\"order\":\"desc\"}}]}"
  }
}
```

## 步驟 7：使用記憶 ID 執行代理程式搜尋

使用前一個回應中的 `memory_id` 傳送後續查詢：

```json
GET /_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Actually, show black ones instead",
      "memory_id": "<memory_id from previous response>"
    }
  }
}
```
{% include copy-curl.html %}

代理程式會記住情境並將其套用至新的請求。它會成功解讀「改成黑色的」，並維持先前情境中的 $150 預算：

```json
{
  "took": 8942,
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
        "_id": "4",
        "_score": 0.0,
        "_source": {
          "product_name": "Puma RS-X",
          "description": "Retro-inspired running shoes with modern comfort",
          "price": 120.0,
          "currency": "USD",
          "rating": 4.3,
          "review_count": 750,
          "in_stock": true,
          "color": "black",
          "size": "9",
          "category": "shoes",
          "brand": "Puma",
          "tags": [
            "retro",
            "running",
            "comfortable"
          ]
        },
        "sort": [
          120.0,
          0.0
        ]
      }
    ]
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: query_planner_tool — qpt.question: \"Find black shoes priced under 150 dollars.\"; index_name_provided: \"products-index\"\nValidation: qpt output is valid JSON and aligns with the request for black shoes under 150 dollars in the products-index.",
    "memory_id": "XRzFl5kB-5P992SCeeqO",
    "dsl_query": "{\"size\":10.0,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category\":\"shoes\"}},{\"term\":{\"color\":\"black\"}},{\"range\":{\"price\":{\"lte\":150.0}}}]}},\"sort\":[{\"price\":{\"order\":\"asc\"}},{\"_score\":{\"order\":\"desc\"}}]}"
  }
}
```

## 使用提示引導 LLM

您可以在 `query_text` 中提供提示，引導大型語言模型 (LLM) 產生您偏好的 DSL 查詢。代理程式在規劃搜尋時會考量這些提示。

下列查詢提供關於排序與彙總的特定提示，以引導代理程式產生 DSL：

```json
GET /_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find expensive running shoes, sort by rating descending, and use aggregations to show average price by brand"
    }
  }
}
```
{% include copy-curl.html %}

相較之下，下列查詢使用簡單的語言，未提供特定的 DSL 提示：

```json
GET /_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Show me running shoes"
    }
  }
}
```
{% include copy-curl.html %}

第一個查詢可能會產生包含排序與彙總的較複雜 DSL，而第二個查詢則較為簡單。請使用「sort by」、「aggregate」、「filter by」及「group by」等特定詞彙，引導代理程式產生查詢。

## 後續步驟

- [代理程式查詢轉譯器處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) -- 進一步了解可將自然語言查詢轉換為 OpenSearch DSL 的請求處理器。
- [代理程式情境處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/) -- 進一步了解可新增代理程式執行情境資訊以供監控與對話延續使用的回應處理器。
- [設定代理程式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/) -- 使用不同的模型、工具與提示來設定代理程式行為。