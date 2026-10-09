---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用代理程式記憶"
parent: Agentic search
grand_parent: AI search
nav_order: 80
has_children: false
---

# 使用代理程式記憶進行代理程式搜尋

[代理程式記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/) 透過專用的記憶容器，提供在代理程式搜尋中管理對話內容的結構化方法。與對話代理程式使用的預設 `conversation_index` 記憶類型不同，代理程式記憶使用個別建立並設定的記憶容器，讓您更能掌控對話歷史的儲存與管理方式。這適用於您想要獨立於代理程式管理記憶生命週期、設定記憶行為，或在不同工作流程之間共用記憶容器的情境。

下列範例示範如何建立記憶容器、設定使用代理程式記憶的代理程式，以及跨多個搜尋查詢使用記憶連續性。

## 步驟 1：建立產品索引

建立包含產品資料的範例索引，其中包含各種產品屬性，例如 `product_name`、`price`、`color` 及 `category`：

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

## 步驟 3：建立模型

檢閱[模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)並選擇要使用的模型。

下列範例註冊一個 GPT 模型，供 `conversational` 代理程式與 `QueryPlanningTool` 兩者使用：

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

## 步驟 4：建立記憶容器

建立記憶容器以儲存代理程式的對話內容：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "agent-memory-container",
  "configuration": {
    "disable_history": true
  }
}
```
{% include copy-curl.html %}

記憶容器會個別建立，並可使用各種選項進行設定。如需詳細資訊，請參閱[組態物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/#the-configuration-object)。

回應包含記憶容器 ID：

```json
{
  "memory_container_id": "your-memory-container-id"
}
```

## 步驟 5：註冊使用代理程式記憶的代理程式

註冊使用 `agentic_memory` 作為記憶類型的對話代理程式。在 `memory_container_id` 欄位中指定前一步驟建立的記憶容器。代理程式包含產生 Query DSL 所需的 `QueryPlanningTool`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "GPT 5 Agent for Agentic Search",
  "type": "conversational",
  "description": "Use this for Agentic Search",
  "llm": {
    "model_id": "your-model-id",
    "parameters": {
      "max_iteration": 15
    }
  },
  "memory": {
    "type": "agentic_memory",
    "memory_container_id": "your-memory-container-id"
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

如需更多組態選項，請參閱[設定代理程式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/)。

## 步驟 6：設定搜尋管線

建立同時包含請求與回應處理器的搜尋管線。[`agentic_query_translator` 請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/)會將自然語言查詢轉譯為 Query DSL。[`agentic_context` 回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/)會新增代理程式執行脈絡資訊，以供監控及維持對話連續性：

```json
PUT _search/pipeline/agentic_search_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id"
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

## 步驟 7：執行代理程式搜尋

若要執行代理程式搜尋，請傳送自然語言搜尋查詢：

```json
GET /_search?search_pipeline=agentic_search_pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find me white shoes under 150 dollars"
    }
  }
}
```
{% include copy-curl.html %}

代理程式會分析請求、探索適當的索引，並產生最佳化的 Query DSL 查詢。回應會在 `hits` 陣列中包含相符的產品。`ext` 物件包含 `memory_id`（用於繼續對話）及產生的 `dsl_query`：

```json
{
  "took": 32240,
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
    "max_score": 0.0,
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
        }
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
        }
      }
    ]
  },
  "ext": {
    "memory_id": "BrLLHJ0BMk3oS6TPFO_2",
    "dsl_query": "{\"size\":10,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category.keyword\":\"shoes\"}},{\"term\":{\"color.keyword\":\"white\"}},{\"range\":{\"price\":{\"lte\":150}}}]}}}"
  }
}
```

## 步驟 8：執行後續的代理程式搜尋

使用上一個回應中的 `memory_id` 傳送後續查詢：

```json
GET /_search?search_pipeline=agentic_search_pipeline
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

透過代理程式記憶容器，代理程式會記住先前的對話並將其套用到新的請求。代理程式成功解讀「改為黑色」，同時維持 150 美元以下的價格限制。在回應中，`memory_id` 保持不變，產生的 Query DSL 查詢僅將顏色篩選條件從白色改為黑色，並保留所有其他限制條件：

```json
{
  "took": 19311,
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
    "max_score": 0.0,
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
        }
      },
      {
        "_index": "products-index",
        "_id": "2",
        "_score": 0.0,
        "_source": {
          "product_name": "Adidas Ultraboost 22",
          "description": "Premium running shoes with Boost midsole",
          "price": 180.0,
          "currency": "USD",
          "rating": 4.7,
          "review_count": 850,
          "in_stock": true,
          "color": "black",
          "size": "9",
          "category": "shoes",
          "brand": "Adidas",
          "tags": [
            "running",
            "premium",
            "boost"
          ]
        }
      }
    ]
  },
  "ext": {
    "memory_id": "BrLLHJ0BMk3oS6TPFO_2",
    "dsl_query": "{\"size\":10,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category.keyword\":\"shoes\"}},{\"term\":{\"color.keyword\":\"black\"}},{\"range\":{\"price\":{\"lte\":150}}}]}}}"
  }
}
```

## 後續步驟

- [使用對話式代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/) -- 了解具備推理軌跡與對話索引記憶的對話式代理程式。
- [代理程式查詢轉譯處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) -- 進一步了解將自然語言查詢轉換為 Query DSL 的請求處理器。
- [代理程式脈絡處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/) -- 進一步了解為監控與對話連續性新增代理程式執行脈絡資訊的回應處理器。
- [設定代理程式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/) -- 使用不同的模型、工具與提示詞設定代理程式行為。