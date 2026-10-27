---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "MCP Streamable HTTP 伺服器"
parent: MCP server APIs
grand_parent: ML APIs
nav_order: 50
---

# MCP Streamable HTTP 伺服器 API
**於 3.3 版推出**
{: .label .label-purple }

叢集內的 Model Context Protocol (MCP) 伺服器會透過 `/_plugins/_ml/mcp` 端點對外提供，並實作 [Streamable HTTP 傳輸](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。MCP 用戶端會使用此端點來探索並呼叫您叢集中註冊的工具。

此伺服器為無狀態：所有通訊都透過個別的 HTTP `POST` 請求進行，且伺服器不會開啟 Server-Sent Events (SSE) 串流。若用戶端傳送 `GET` 請求，伺服器會傳回 `405 Method Not Allowed` 回應。

若要使用此端點，請啟用 `plugins.ml_commons.mcp_server_enabled` 設定。如需設定說明與範例請求，請參閱[使用叢集內的 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/in-cluster-mcp-server/)。

## 端點

```json
POST /_plugins/_ml/mcp
```

## 請求本文欄位

請求本文是一則 [JSON-RPC 2.0](https://www.jsonrpc.org/specification) 訊息。下表列出請求本文的欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `jsonrpc` | 字串 | 必要 | JSON-RPC 版本。必須為 `2.0`。 |
| `id` | 整數或字串 | 選用 | 請求 ID，伺服器會在回應中傳回此 ID。通知訊息應省略 ID。 |
| `method` | 字串 | 必要 | MCP 方法。用戶端使用 `initialize` 與 `notifications/initialized` 建立連線、使用 `tools/list` 探索工具，並使用 `tools/call` 呼叫工具。伺服器也會回應 `ping`，並對 `prompts/list` 與 `resources/list` 傳回空清單，因為它僅提供工具。 |
| `params` | 物件 | 選用 | 方法參數。例如，`tools/call` 請求會提供工具的 `name` 與 `arguments`。 |

## 範例請求

下列請求會呼叫 `ListIndexTool` 工具：

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

## 範例回應

伺服器會在 `content` 陣列中回傳工具輸出：

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

如需 MCP 用戶端傳送的完整請求序列，請參閱 [手動傳送 MCP 請求]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/in-cluster-mcp-server/#sending-mcp-requests-manually)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/opensearch/ml/mcp/server`。工具會以呼叫使用者的權限執行，因此呼叫會存取索引資料的工具時，也需要對應的索引權限。如需詳細資訊，請參閱[權限]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/in-cluster-mcp-server/#permissions)。
