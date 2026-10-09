---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出連接器 MCP 工具"
parent: MCP client APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# List Connector MCP Tools API
**3.8 版新增**
{: .label .label-purple }

使用此 API 可列出透過已註冊的 MCP 連接器，在外部 MCP 伺服器上可用的所有工具。回應包含每個工具的名稱、類型、描述與輸入結構描述。

流程代理程式與對話流程代理程式需要在註冊代理程式時預先定義工具。請使用此 API 在將 MCP 工具加入代理程式組態之前，探索可用的工具及其參數。如需更多資訊，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。

此 API 與 [List MCP Tools API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/list-mcp-tools/) 不同，後者列出的是註冊在 OpenSearch 自身 MCP 伺服器上的工具。
{: .note}

## 必要條件

使用此 API 之前，請完成下列步驟：

1. 將 `plugins.ml_commons.mcp_connector_enabled` 設定為 `true` 以啟用 MCP 連接器。
2. 在 `plugins.ml_commons.trusted_connector_endpoints_regex` 中設定信任的 MCP 伺服器端點。
3. 建立通訊協定為 `mcp_sse` 或 `mcp_streamable_http` 的 MCP 連接器。

如需設定說明，請參閱[連線至外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/)。

## 端點

```json
GET /_plugins/_ml/connectors/{connector_id}/tools
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 描述 |
| :--- | :--- | :--- | :--- |
| `connector_id` | 字串 | 必要 | MCP 連接器的 ID。請從 [Create Connector API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/create-connector/) 的回應取得此 ID。連接器必須使用 `mcp_sse` 或 `mcp_streamable_http` 通訊協定。 |

## 請求範例

下列範例列出 ID 為 `1MlVyZwBBtWLSsWgaB6w` 的 MCP 連接器之工具：

```json
GET /_plugins/_ml/connectors/1MlVyZwBBtWLSsWgaB6w/tools
```
{% include copy-curl.html %}

## 回應範例

OpenSearch 透過指定的連接器連線至外部 MCP 伺服器，並傳回可用的工具：

```json
{
  "tools": [
    {
      "name": "search_documents",
      "type": "McpStreamableHttpTool",
      "description": "Search a document repository for relevant content.",
      "input_schema": "{\"type\":\"object\",\"properties\":{\"query\":{\"type\":\"string\",\"description\":\"The search query.\"},\"limit\":{\"type\":\"integer\",\"description\":\"The maximum number of results to return.\",\"minimum\":1,\"maximum\":100}},\"required\":[\"query\"]}"
    },
    {
      "name": "get_weather",
      "type": "McpStreamableHttpTool",
      "description": "Retrieve current weather conditions for a specified location.",
      "input_schema": "{\"type\":\"object\",\"properties\":{\"location\":{\"type\":\"string\",\"description\":\"The city or geographic location.\"},\"units\":{\"type\":\"string\",\"description\":\"The temperature unit system.\",\"enum\":[\"celsius\",\"fahrenheit\"]}},\"required\":[\"location\"]}"
    }
  ]
}
```

如果 MCP 伺服器未公開任何工具，OpenSearch 會傳回空的 `tools` 陣列：

```json
{
  "tools": []
}
```

## 回應本文欄位

下表列出頂層回應欄位。

| 欄位 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `tools` | 陣列 | 外部 MCP 伺服器上可用工具的清單。如果 MCP 伺服器未公開任何工具，則傳回空陣列。 |

`tools` 陣列中的每個物件包含下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 描述 |
| :--- | :--- | :--- | :--- |
| `name` | 字串 | 必要 | 由外部 MCP 伺服器定義的工具名稱。在代理程式中設定 MCP 工具時，請將此值用作 `name` 欄位。 |
| `type` | 字串 | 必要 | 用於執行 MCP 工具的 OpenSearch 工具類型。有效值為通訊協定為 `mcp_streamable_http` 之連接器的 `McpStreamableHttpTool`，以及通訊協定為 `mcp_sse` 之連接器的 `McpSseTool`。在代理程式中設定 MCP 工具時，請將此值用作 `type` 欄位。 |
| `description` | 字串 | 選用 | 由外部 MCP 伺服器提供、關於工具用途的易讀描述。當 MCP 伺服器未提供描述時，回應中會省略此欄位。 |
| `input_schema` | 字串 | 選用 | 描述工具輸入參數的 JSON Schema 字串。此結構描述遵循 [JSON Schema](https://json-schema.org/) 格式，並定義屬性、類型、描述與必要欄位。當 MCP 伺服器未提供輸入結構描述時，回應中會省略此欄位。 |

## 錯誤回應

下表描述常見的錯誤回應。

| HTTP 狀態 | 條件 | 錯誤訊息範例 |
| :--- | :--- | :--- |
| `400` | 連接器存在但不是 MCP 連接器（例如 HTTP 或 Amazon Bedrock 連接器）。 | `Connector with ID {connector_id} is not of type McpConnector or McpStreamableHttpConnector` |
| `404` | 連接器 ID 不存在。 | `Failed to find connector` |
| `500` | MCP 連接器已停用、外部 MCP 伺服器無法連線，或發生其他內部錯誤。 | `The MCP connector is not enabled. To enable, please update the setting plugins.ml_commons.mcp_connector_enabled` |
