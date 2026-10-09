---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出 MCP 工具"
parent: MCP server APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# 列出 MCP 工具 API
**於 3.1 版推出**
{: .label .label-purple }

使用此 API 依名稱列出所有以 Model Context Protocol (MCP) 為基礎的工具。

## 端點

```json
GET /_plugins/_ml/mcp/tools/_list
```

## 請求範例

```json
GET /_plugins/_ml/mcp/tools/_list
```
{% include copy-curl.html %}

## 回應範例

OpenSearch 會回應 MCP 工具清單：

```json
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
                        "next_page": {
                            "description": "The search result's next page link. If this is provided, the WebSearchTool will fetch the next page results using this link and crawl the links on the page.",
                            "type": "string"
                        },
                        "engine": {
                            "description": "The search engine that will be used by the tool.",
                            "type": "string"
                        },
                        "query": {
                            "description": "The search query parameter that will be used by the engine to perform the search.",
                            "type": "string"
                        }
                    },
                    "required": [
                        "engine",
                        "query"
                    ]
                },
                "strict": false
            },
            "create_time": 1749864622040
        }
    ]
}
```