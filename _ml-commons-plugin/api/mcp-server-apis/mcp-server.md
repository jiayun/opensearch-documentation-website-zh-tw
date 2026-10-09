---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "MCP Streamable HTTP 伺服器"
parent: MCP server APIs
grand_parent: ML Commons APIs
nav_order: 50
---

# MCP Streamable HTTP 伺服器 API
**3.3 版新增**
{: .label .label-purple }

MCP 伺服器透過 `/_plugins/_ml/mcp` 端點公開，並實作 Model Context Protocol (MCP) 定義的 Streamable HTTP 傳輸方式。它允許代理程式或用戶端連線至 OpenSearch，並探索或呼叫可用的工具。

此伺服器不會與用戶端建立持續性的 SSE 連線；所有通訊皆透過無狀態的 HTTP 呼叫進行。
如果用戶端傳送 `GET` 請求（通常是為了建立 SSE 連線），伺服器會回傳 `405 Method Not Allowed` 回應，讓用戶端繼續使用 `POST` 通訊。


若要進一步了解此傳輸方式，請參閱 [MCP 官方文件](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。
{: .note }

## 必要條件

在連線至 MCP 伺服器端點之前，您必須先在叢集中啟用 MCP 伺服器功能：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.mcp_server_enabled": "true"
  }
}
```
{% include copy-curl.html %}

您也可以選擇性地註冊工具，讓用戶端能夠探索並呼叫它們。請參閱[註冊 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/register-mcp-tools/)。

## 連線至 MCP 伺服器

您可以使用任何支援 Streamable HTTP 傳輸方式的用戶端連線至 MCP 伺服器。

### 使用 MCP 用戶端連線

下列範例使用 `fastmcp` 來初始化連線、列出工具並呼叫工具：

```python
import asyncio, logging
from fastmcp import Client


async def main():
    async with Client("http://localhost:9200/_plugins/_ml/mcp") as client:
        for t in await client.list_tools():
            print(t.name)
        r = await client.call_tool("ListIndexTool", {})
        print("result: ", r)

asyncio.run(main())
```
{% include copy.html %}

### 手動呼叫 MCP 伺服器（用於除錯）

雖然一般使用時不需要這麼做，但您可以透過 HTTP 使用 JSON-RPC 呼叫手動叫用 MCP 伺服器。下列範例展示典型的 MCP 用戶端行為。

#### 步驟 1（選用）：註冊自訂工具

在連線至 MCP 伺服器之前，您可以使用 [Register MCP Tools API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/register-mcp-tools/) 註冊自訂工具。例如，若要註冊 [List Index 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/list-index-tool/)，請傳送下列請求：

```json
POST /_plugins/_ml/mcp/tools/_register
{
    "tools": [
        {
            "name": "ListIndexTool",
            "type": "ListIndexTool",
            "description": "This tool returns information about indices in the OpenSearch cluster along with the index `health`, `status`, `index`, `uuid`, `pri`, `rep`, `docs.count`, `docs.deleted`, `store.size`, `pri.store. size `, `pri.store.size`, `pri.store`. Optional arguments: 1. `indices`, a comma-delimited list of one or more indices to get information from (default is an empty list meaning all indices). Use only valid index names. 2. `local`, whether to return information from the local node only instead of the cluster manager node (Default is false)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "indices": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "OpenSearch index name list, separated by comma. for example: [\"index1\", \"index2\"], use empty array [] to list all indices in the cluster"
                    }
                },
                "additionalProperties": false
            }
        }
    ]
}
```
{% include copy-curl.html %}

伺服器會回應確認工具已註冊：

```json
200 OK
{
  "message": "Tool 'ListIndexTool' registered successfully"
}
```

#### 步驟 2：初始化連線

傳送 `initialize` 方法，並附上您的用戶端資訊與功能。請注意，`protocolVersion` 必須符合 MCP 規格版本：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "test-client",
      "version": "1.0.0"
    }
  }
}
```
{% include copy-curl.html %}

伺服器會回應其功能與伺服器資訊。`tools.listChanged` 表示伺服器支援動態工具探索：

```json
200 OK
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "logging": {},
      "prompts": {
        "listChanged": false
      },
      "resources": {
        "subscribe": false,
        "listChanged": false
      },
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "OpenSearch-MCP-Stateless-Server",
      "version": "0.1.0"
    },
    "instructions": "OpenSearch MCP Stateless Server - provides access to ML tools without sessions"
  }
}
```

#### 步驟 3：傳送初始化完成通知

傳送通知以表示初始化已完成。此通知不會預期收到回應內容：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```
{% include copy-curl.html %}

伺服器會以 `202 Accepted` 狀態確認收到通知：

```json
202 Accepted
```

#### 步驟 4：列出可用工具

使用 `tools/list` 方法來探索可用的工具：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```
{% include copy-curl.html %}

若要使用專屬 API，請參閱[列出 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/list-mcp-tools/)。

伺服器會回傳可用工具的陣列，包含其名稱、描述與輸入結構描述。請注意，每個工具都包含詳細的 `inputSchema`，用以描述預期的參數：

```json
200 OK
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "ListIndexTool",
        "description": "This tool returns information about indices in the OpenSearch cluster along with the index `health`, `status`, `index`, `uuid`, `pri`, `rep`, `docs.count`, `docs.deleted`, `store.size`, `pri.store. size `, `pri.store.size`, `pri.store`. Optional arguments: 1. `indices`, a comma-delimited list of one or more indices to get information from (default is an empty list meaning all indices). Use only valid index names. 2. `local`, whether to return information from the local node only instead of the cluster manager node (Default is false)",
        "inputSchema": {
          "type": "object",
          "properties": {
            "indices": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "OpenSearch index name list, separated by comma. for example: [\"index1\", \"index2\"], use empty array [] to list all indices in the cluster"
            }
          },
          "additionalProperties": false
        }
      }
    ]
  }
}
```

#### 步驟 5：呼叫工具

使用 `tools/call` 方法來叫用特定工具。請提供工具名稱，以及符合該工具輸入結構描述的引數：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ListIndexTool",
    "arguments": {
      "indices": []
    }
  }
}
```
{% include copy-curl.html %}

伺服器會執行該工具，並在 `content` 陣列中回傳結果。`isError` 欄位表示工具執行是否成功：

```json
200 OK
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)\n1,green,open,.plugins-ml-config,nKyzDAupTGCwuybs9S_iBA,1,0,1,0,3.9kb,3.9kb\n2,green,open,.plugins-ml-mcp-tools,k1QwQKmXSeqRexmB2JDJiw,1,0,1,0,5kb,5kb\n"
      }
    ],
    "isError": false
  }
}
```
