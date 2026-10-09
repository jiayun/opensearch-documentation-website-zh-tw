---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除 MCP 工具"
parent: MCP server APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 移除 MCP 工具 API
**於 3.0 版推出**
{: .label .label-purple }

使用此 API 依名稱刪除一或多個以 Model Context Protocol (MCP) 為基礎的工具。

## 端點

```json
POST /_plugins/_ml/mcp/tools/_remove
```

## 範例請求

```json
POST /_plugins/_ml/mcp/tools/_remove
[
 "WebSearchTool", "ListIndexTool"
]
```
{% include copy-curl.html %}

## 範例回應

OpenSearch 會回應節點 ID 以及每個節點的工具刪除狀態：

```json
{
    "_ZNV5BrNTVm6ilcM7Jn1pw": {
        "removed": true
    },
    "NZ9aiUCrSp2b5KBqdJGJKw": {
        "removed": true
    }
}
```