---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用外部 MCP 伺服器"
parent: Agentic search
grand_parent: AI search
nav_order: 110
has_children: false
---

# 使用外部 MCP 伺服器

外部 Model Context Protocol (MCP) 伺服器透過提供外部工具與資料來源的存取權，擴展代理式搜尋的能力。透過連線至 MCP 伺服器，您的代理程式可以使用外部 API、資料庫與服務，以即時資訊與特殊功能強化搜尋結果。

本指南示範如何建立外部 MCP 伺服器、將其連線至代理式搜尋代理程式，並使用外部工具回答需要外部資料的複雜查詢。

## 先決條件

在搭配代理式搜尋使用外部 MCP 伺服器之前，請確認您已具備：

- 建立與部署 MCP 伺服器的存取權。
- 了解 [MCP 連接器組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/)。

## 步驟 1：建立範例產品索引

首先，建立產品索引以示範外部 MCP 工具整合：

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

新增範例產品文件以示範外部 MCP 工具的使用方式：

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

## 步驟 3：建立外部 MCP 伺服器

建立範例 MCP 伺服器。此 MCP 伺服器提供一個 `brand_collection_tool`，可根據使用者偏好將品牌分類為不同層級（`favorites`、`budget` 與 `luxury`）。代理程式在處理自然語言查詢時，可使用此工具了解哪些品牌屬於特定類別：

```python
from fastmcp import FastMCP

mcp = FastMCP("brands_server")

@mcp.tool
def brand_collection_tool(category: str) -> list[str]:
    """This is the collection of brands for a given category. There are 3 categories: 1. favorites, 2. budget, 3. luxury. If the category is not one of these, return all the brands."""
    favorites = ["Nike", "Adidas", "Reebok"]
    budget = ["Puma", "New Balance", "Under Armour"]
    luxury = ["Phoenix Motors", "Crystal Palace", "Royal Oak"]
    if category == "favorites":
        return favorites
    elif category == "budget":
        return budget
    elif category == "luxury":
        return luxury
    else:
        return favorites + budget + luxury

if __name__ == "__main__":
    # Streamable HTTP transport; no session/state persisted between requests
    mcp.run(transport="streamable-http")
```
{% include copy.html %}

## 步驟 4：建立 MCP 連接器

註冊 MCP 連接器，將您的代理式搜尋代理程式連線至外部 MCP 伺服器。MCP 連接器使用 `mcp_streamable_http` 通訊協定與您的外部 MCP 伺服器通訊。請將 `<Your MCP Server URL>` 取代為您的 MCP 伺服器實際執行的 URL，並將 `<Your API Key>` 取代為適當的驗證金鑰：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Brands MCP Connector",
  "description": "The connector to external brands MCP server",
  "version": 1,
  "protocol": "mcp_streamable_http",
  "parameters": {
    "endpoint": "/mcp"
  },
  "credential": {
    "access_key": "<Your API Key>"
  },
  "url": "<Your MCP Server URL>",
  "headers": {
    "Authorization": "Bearer ${credential.access_key}",
    "Content-Type": "application/json"
  }
}
```
{% include copy-curl.html %}

## 步驟 5：為代理程式建立模型

註冊一個將由對話代理程式與 `QueryPlanningTool` 共同使用的模型：

```json
POST /_plugins/_ml/models/_register
{
  "name": "My OpenAI model: gpt-5",
  "function_name": "remote",
  "description": "Model for agentic search with external MCP tools",
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
        "request_body": """{ "model": "${parameters.model}", "messages": [{"role":"developer","content":"${parameters.system_prompt}"},${parameters._chat_history:-}{"role":"user","content":"${parameters.user_prompt}"}${parameters._interactions:-}], "reasoning_effort":"low"${parameters.tool_configs:-}}"""
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 步驟 6：建立含 MCP 連接器的代理程式

註冊一個包含 MCP 連接器以存取外部工具的對話代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "E-commerce Agent with External Tools",
  "type": "conversational",
  "description": "Agentic search agent with external MCP tools for brand categorization",
  "llm": {
    "model_id": "<Model ID from Step 5>",
    "parameters": {
      "max_iteration": 15
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions",
    "mcp_connectors": [
      {
        "mcp_connector_id": "<MCP Connector ID from Step 4>"
      }
    ]
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
      "type": "QueryPlanningTool"
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

代理程式組態包含：
- **MCP 連接器**：連結至提供其他工具的外部 MCP 伺服器。
- **標準工具**：`ListIndexTool`、`IndexMappingTool` 與 `QueryPlanningTool`，用於核心代理式搜尋功能。
- **外部工具**：透過 MCP 連接器自動提供（例如 `brand_collection_tool`）。

## 步驟 7：建立代理式搜尋管線

建立一個使用您的代理程式搭配外部 MCP 工具的搜尋管線：

```json
PUT _search/pipeline/mcp-agentic-pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "<Agent ID from Step 6>"
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

## 步驟 8：使用外部工具執行代理式搜尋

傳送需要使用外部 MCP 工具的自然語言查詢：

```json
POST products-index/_search?search_pipeline=mcp-agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find red shoes under 200 USD from my favorite brands"
    }
  }
}
```
{% include copy-curl.html %}

代理程式透過以下方式處理此查詢：

1. **使用外部 MCP 工具**：呼叫 `brand_collection_tool` 並使用 `favorites` 類別，以取得喜愛品牌的清單。
2. **探索索引**：使用 `ListIndexTool` 尋找相關的索引。
3. **分析結構描述**：使用 `IndexMappingTool` 了解索引結構。
4. **規劃查詢**：使用 `QueryPlanningTool` 產生最終的查詢領域特定語言（DSL）查詢。

回應包含相符的產品以及詳細的代理程式執行資訊。`agent_steps_summary` 顯示代理程式如何協調多個工具，包括外部 MCP 工具（`brand_collection_tool`），以了解使用者的請求並產生適當的搜尋查詢：

```json
{
  "took": 29942,
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
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool, brand_collection_tool]\nFirst I used: brand_collection_tool — input: \"favorites\"; context gained: \"User favourite brands are [\"Nike\",\"Adidas\",\"Reebok\"]\"\nSecond I used: ListIndexTool — input: \"[]\"; context gained: \"Found indices; products-index appears relevant\"\nThird I used: IndexMappingTool — input: \"products-index\"; context gained: \"Index contains product-related fields\"\nFourth I used: query_planner_tool — qpt.question: \"Find shoes priced under 200 USD from brands Nike, Adidas, and Reebok.\"; index_name_provided: \"products-index\"\nValidation: qpt output is valid and matches the user's request.",
    "memory_id": "XRzFl5kB-5P992SCeeqO",
    "dsl_query": "{\"size\":10.0,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category\":\"shoes\"}},{\"term\":{\"currency\":\"USD\"}},{\"range\":{\"price\":{\"lte\":200.0}}},{\"terms\":{\"brand\":[\"Nike\",\"Adidas\",\"Reebok\"]}}]}}}"
  }
}
```

## 後續步驟

- [MCP 連接器組態]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/) -- 進一步了解如何設定 MCP 連接器以整合外部工具。
- [設定代理式搜尋代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/) -- 使用不同的模型和工具設定代理程式行為。
- [使用對話代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/) -- 進一步了解對話代理程式及其進階功能。
