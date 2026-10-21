---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新 MCP 工具"
parent: MCP server APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 更新 MCP 工具 API
**於 3.0 推出**
{: .label .label-purple }

使用此 API 更新一或多個以 Model Context Protocol（MCP）為基礎的工具。如需支援工具的詳細資訊，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。

## 端點

```json
POST /_plugins/_ml/mcp/tools/_update
```

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :--- 
`tools` | 陣列 | 必要 | 工具清單。 


`tools` 陣列包含工具清單。每個工具包含下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`name`| 字串 | 必要 | 要更新的工具名稱。 |
`type` | 字串 | 選用 | 工具類型。由於已註冊工具的類型無法變更，因此會忽略此欄位。
`description` | 字串 | 選用 | 工具的說明。
`parameters` | 物件 | 選用 | 工具的參數。參數取決於工具類型。如需特定工具類型的相關資訊，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
`attributes` | 物件 | 選用 | 工具的組態屬性（attributes）。此欄位中最重要的屬性是工具的 `input_schema`，它定義了工具預期的參數格式。此結構描述（schema）會傳送給大型語言模型（LLM），使其在執行工具時能正確格式化參數。


## 請求範例

下列各節提供更新工具的請求範例。如需工具專屬參數的資訊，請參閱對應的[工具文件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。

### WebSearchTool

```json
POST /_plugins/_ml/mcp/tools/_update
{
  "tools": [
    {
      "type": "WebSearchTool",
      "name": "GoogleSearchTool",
      "description": "This tool can be used to perform search via google engine and parse the content of the searched results",
      "attributes": {
        "input_schema": {
          "type": "object",
          "properties": {
            "engine": {
              "type": "string",
              "description": "The search engine that will be used by the tool."
            },
            "query": {
              "type": "string",
              "description": "The search query parameter that will be used by the engine to perform the search."
            },
            "next_page": {
              "type": "string",
              "description": "The search result's next page link. If this is provided, the WebSearchTool will fetch the next page results using this link and crawl the links on the page."
            }
          },
          "required": [
            "engine",
            "query"
          ]
        },
        "strict": false
      }
    }
  ]
}
```
{% include copy-curl.html %}

<!-- vale off -->
### PPLTool
<!-- vale on -->

```json
POST /_plugins/_ml/mcp/tools/_update
{
  "tools": [
    {
      "type": "PPLTool",
      "name": "TransferQuestionToPPLAndExecuteTool",
      "description": "Use this tool to convert natural language into PPL queries and execute them. Use this tool after you know the index name; otherwise, call IndexRoutingTool first. The input parameters are: {index: IndexName, question: UserQuestion}",
      "parameters": {
        "model_id": "${your_model_id}",
        "model_type": "FINETUNE"
      },
      "attributes": {
        "input_schema": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string",
              "description": "The user's natural language question that needs to be converted to PPL."
            },
            "index": {
              "type": "string",
              "description": "The index on which the generated PPL query will be executed."
            }
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例回應

針對每個節點，OpenSearch 會回應節點 ID，以及所有工具的更新作業狀態：

```json
{
    "_ZNV5BrNTVm6ilcM7Jn1pw": {
        "updated": true
    },
    "NZ9aiUCrSp2b5KBqdJGJKw": {
        "updated": true
    }
}
```

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/opensearch/ml/mcp_tools/update`。
