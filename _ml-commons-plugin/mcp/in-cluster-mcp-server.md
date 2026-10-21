---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集內 MCP 伺服器"
parent: MCP servers and clients
nav_order: 10
---

# 使用叢集內 MCP 伺服器
**3.3 版新增**
{: .label .label-purple }

叢集內 Model Context Protocol (MCP) 伺服器可讓外部 MCP 用戶端（例如 AI 助理與代理程式框架）探索並呼叫 OpenSearch 叢集中的工具。該伺服器在 OpenSearch 內部執行，因此無需額外安裝。伺服器透過 `/_plugins/_ml/mcp` 端點公開，並使用[可串流 HTTP 傳輸方式](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。用戶端只能呼叫您註冊的工具。

該伺服器是無狀態的：所有通訊都透過個別的 HTTP `POST` 請求進行，伺服器不會開啟 Server-Sent Events (SSE) 串流。如果用戶端傳送 `GET` 請求（通常是為了開啟 SSE 串流），伺服器會傳回 `405 Method Not Allowed` 回應，用戶端則繼續使用 `POST` 請求。

若要比較叢集內 MCP 伺服器與獨立 MCP 伺服器，請參閱[選擇 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/#choosing-an-mcp-server)。

## 步驟 1：啟用 MCP 伺服器

MCP 伺服器預設為停用。若要啟用，請更新 `plugins.ml_commons.mcp_server_enabled` 設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.mcp_server_enabled": "true"
  }
}
```
{% include copy-curl.html %}

## 步驟 2：註冊工具

註冊您希望 MCP 用戶端呼叫的工具。每個工具定義包含下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `type` | 字串 | 必要 | 工具類型，例如 `ListIndexTool`。工具類型清單請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。 |
| `name` | 字串 | 選用 | 用戶端呼叫工具時使用的名稱。預設為 `type` 值。若要註冊多個相同類型的工具，請為每個工具指定不同的名稱。 |
| `description` | 字串 | 選用 | 工具的說明。用戶端中的大型語言模型 (LLM) 會使用此說明來決定何時呼叫該工具。 |
| `parameters` | 物件 | 選用 | 工具參數。某些工具類型需要參數。各工具類型的參數請參閱對應的[工具文件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。 |
| `attributes` | 物件 | 選用 | 工具屬性。使用 `input_schema` 屬性提供 JSON schema，定義工具接受的引數。用戶端會將此 schema 傳送給 LLM，讓 LLM 能提供格式正確的引數。 |

下列請求會註冊 [List Index 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/list-index-tool/)與 [Search Index 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-index-tool/)：

```json
POST /_plugins/_ml/mcp/tools/_register
{
  "tools": [
    {
      "name": "ListIndexTool",
      "type": "ListIndexTool",
      "description": "This tool returns information about indices in the OpenSearch cluster along with the index `health`, `status`, `index`, `uuid`, `pri`, `rep`, `docs.count`, `docs.deleted`, `store.size`, `pri.store. size `, `pri.store.size`, `pri.store`. Optional arguments: 1. `indices`, a comma-delimited list of one or more indices to get information from (default is an empty list meaning all indices). Use only valid index names. 2. `local`, whether to return information from the local node only instead of the cluster manager node (Default is false)",
      "attributes": {
        "input_schema": {
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
    },
    {
      "name": "SearchIndexTool",
      "type": "SearchIndexTool",
      "description": "Searches an index. Provide the index name and a query written in OpenSearch query domain-specific language (DSL).",
      "attributes": {
        "input_schema": {
          "type": "object",
          "properties": {
            "index": {
              "type": "string",
              "description": "The name of the index to search."
            },
            "query": {
              "type": "object",
              "description": "The search request body, for example, {\"query\": {\"match\": {\"field\": \"value\"}}}."
            }
          },
          "required": ["index", "query"],
          "additionalProperties": false
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會包含每個節點的節點 ID 與註冊狀態：

```json
{
  "6It0uQ1AR06IDC4nMstPQw": {
    "created": true
  }
}
```

## 步驟 3：連接 MCP 用戶端

若要連接 MCP 用戶端，請將用戶端設定為使用可串流 HTTP 傳輸方式，並提供 MCP 伺服器 URL：

```
http://<host>:<port>/_plugins/_ml/mcp
```

下列 Python 範例使用 [FastMCP](https://gofastmcp.com/) 用戶端列出已註冊的工具，然後在 `opensearch_dashboards_sample_data_ecommerce` 範例索引上呼叫這兩個工具：

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:9200/_plugins/_ml/mcp") as client:
        for tool in await client.list_tools():
            print(tool.name)

        result = await client.call_tool(
            "ListIndexTool",
            {"indices": ["opensearch_dashboards_sample_data_ecommerce"]},
        )
        print(result.content[0].text)

        result = await client.call_tool(
            "SearchIndexTool",
            {
                "index": "opensearch_dashboards_sample_data_ecommerce",
                "query": {
                    "size": 1,
                    "_source": ["customer_full_name", "products.product_name", "taxful_total_price"],
                    "query": {"match": {"products.product_name": "jacket"}},
                },
            },
        )
        print(result.content[0].text)

asyncio.run(main())
```
{% include copy.html %}

該指令碼會印出工具名稱、索引資訊與搜尋結果：

```
ListIndexTool
SearchIndexTool
row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)
1,green,open,opensearch_dashboards_sample_data_ecommerce,ryn25tMCTDex530BrUVmfw,1,0,4675,0,4mb,4mb

{"_index":"opensearch_dashboards_sample_data_ecommerce","_source":{"customer_full_name":"Sultan Al Mccarthy","products":[{"product_name":"Summer jacket - navy"},{"product_name":"Light jacket - khaki"}],"taxful_total_price":86.98},"_id":"eWBchqABedeO5z2s7srO","_score":1.6412048}
```

### 對使用 Security 外掛程式的叢集進行驗證

如果您的叢集使用 Security 外掛程式，用戶端必須在每個請求中進行驗證。請在請求標頭中傳遞認證資訊。例如，若要搭配 FastMCP 使用基本驗證，請在傳輸方式中設定 `Authorization` 標頭。如果您的叢集使用由您自己的憑證授權單位 (CA) 簽署的憑證，請在 `verify` 參數中提供 CA 憑證的路徑：

```python
import asyncio, base64
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

credentials = base64.b64encode(b"<username>:<password>").decode()
transport = StreamableHttpTransport(
    "https://localhost:9200/_plugins/_ml/mcp",
    headers={"Authorization": f"Basic {credentials}"},
    verify="<path-to-root-ca.pem>",
)

async def main():
    async with Client(transport) as client:
        print([tool.name for tool in await client.list_tools()])

asyncio.run(main())
```
{% include copy.html %}

使用者必須具備[權限](#permissions)中所述的權限。

## 手動傳送 MCP 請求

MCP 用戶端使用 [JSON-RPC](https://www.jsonrpc.org/specification) 訊息與伺服器通訊。若要偵錯用戶端，或不透過用戶端測試伺服器，您可以自行將相同的訊息傳送至 MCP 端點。下列步驟說明一般 MCP 用戶端所傳送的請求順序。

### 步驟 1：初始化連線

傳送包含用戶端資訊與功能的 `initialize` 請求。`protocolVersion` 必須符合支援的 MCP 規格版本：

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

伺服器會回應其功能與伺服器資訊。`tools.listChanged` 功能表示伺服器支援動態工具探索：

```json
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

### 步驟 2：傳送初始化完成通知

傳送通知以表示初始化已完成：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```
{% include copy-curl.html %}

伺服器會傳回 `202 Accepted` 狀態，且回應本文為空。

### 步驟 3：列出可用的工具

使用 `tools/list` 方法探索可用的工具：

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

伺服器會傳回已註冊的工具，包括每個工具的名稱、描述與輸入結構定義（`inputSchema`）：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
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
              "description": "OpenSearch index name list, separated by comma. for example: [\"index1\", \"index2\"], use empty array [] to list all indices in the cluster",
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          "additionalProperties": false
        }
      },
      {
        "name": "SearchIndexTool",
        "description": "Searches an index. Provide the index name and a query written in OpenSearch query domain-specific language (DSL).",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "description": "The search request body, for example, {\"query\": {\"match\": {\"field\": \"value\"}}}.",
              "type": "object"
            },
            "index": {
              "description": "The name of the index to search.",
              "type": "string"
            }
          },
          "required": [
            "index",
            "query"
          ],
          "additionalProperties": false
        }
      }
    ]
  }
}
```
</details>

### 步驟 4：呼叫工具

使用 `tools/call` 方法呼叫工具。提供符合工具輸入結構定義的工具名稱與引數：

```json
POST /_plugins/_ml/mcp
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ListIndexTool",
    "arguments": {
      "indices": ["opensearch_dashboards_sample_data_ecommerce"]
    }
  }
}
```
{% include copy-curl.html %}

伺服器會執行工具，並在 `content` 陣列中傳回結果。`isError` 欄位表示工具是否執行成功：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)\n1,green,open,opensearch_dashboards_sample_data_ecommerce,ryn25tMCTDex530BrUVmfw,1,0,4675,0,4mb,4mb\n"
      }
    ],
    "isError": false,
    "_meta": {}
  }
}
```

## 管理已註冊的工具

若要檢視已註冊的工具，請傳送下列請求：

```json
GET /_plugins/_ml/mcp/tools/_list
```
{% include copy-curl.html %}

若要更新工具，請提供工具名稱與要變更的欄位。您省略的欄位會保留目前的值。例如，下列請求只會更新 `SearchIndexTool` 工具的說明：

```json
POST /_plugins/_ml/mcp/tools/_update
{
  "tools": [
    {
      "name": "SearchIndexTool",
      "description": "Searches an index of ecommerce orders. Provide the index name and a query written in OpenSearch query DSL."
    }
  ]
}
```
{% include copy-curl.html %}

若要移除工具，請提供工具名稱的陣列：

```json
POST /_plugins/_ml/mcp/tools/_remove
["ListIndexTool", "SearchIndexTool"]
```
{% include copy-curl.html %}

如需詳細資訊，請參閱 [MCP 伺服器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/)。

## 權限

如果您的叢集使用 Security 外掛程式，下列權限會控制對 MCP 伺服器的存取。

| 權限 | 允許的動作 |
| :--- | :--- |
| `cluster:admin/opensearch/ml/mcp/server` | 連線至 MCP 伺服器、使用 `tools/list` 方法列出工具，以及呼叫工具 |
| `cluster:admin/opensearch/ml/mcp_tools/list` | 列出已註冊的工具 |
| `cluster:admin/opensearch/ml/mcp_tools/register` | 註冊工具 |
| `cluster:admin/opensearch/ml/mcp_tools/update` | 更新工具 |
| `cluster:admin/opensearch/ml/mcp_tools/remove` | 移除工具 |

`ml_full_access` 預先定義的角色包含所有這些權限。`ml_read_access` 角色則不包含其中任何權限。

工具會以用戶端驗證身分的使用者權限執行。若要呼叫會存取索引資料的工具，使用者還需要對應的索引權限。例如，若要呼叫在[步驟 2](#step-2-register-tools) 中註冊的 `SearchIndexTool` 工具，使用者需要對該工具所搜尋的索引具備 `read` 權限。`ml_full_access` 角色不會授予您索引的權限。

如需詳細資訊，請參閱[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。

## 後續步驟

- [MCP 伺服器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/)。

