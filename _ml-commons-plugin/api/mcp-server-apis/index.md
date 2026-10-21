---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "MCP 伺服器 API"
parent: ML Commons APIs
has_children: true
has_toc: false
nav_order: 40
redirect_from: 
  - /ml-commons-plugin/api/mcp-server-apis/
  - /ml-commons-plugin/api/mcp-server-apis/sse-message/
  - /ml-commons-plugin/api/mcp-server-apis/sse-session/
---

# MCP 伺服器 API
**3.0 版新增**
{: .label .label-purple }

使用這些 API 來管理叢集內的 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 伺服器，讓外部 MCP 用戶端能夠探索並呼叫您叢集中註冊的[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/)。

叢集內的 MCP 伺服器使用 Streamable HTTP 傳輸協定與用戶端通訊。關於此傳輸方式的詳細資訊，請參閱[官方 MCP 文件](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。
{: .note }

關於設定 MCP 伺服器與連接用戶端的說明，請參閱[使用叢集內 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/in-cluster-mcp-server/)。

叢集內的 MCP 伺服器支援下列 API：

- [註冊 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/register-mcp-tools/)
- [更新 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/update-mcp-tools/)
- [列出 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/list-mcp-tools/)
- [移除 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/remove-mcp-tools/)
- [MCP Streamable HTTP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/mcp-server/)

## 已移除的 API

下列實驗性 API 已於 OpenSearch 3.3 中移除，改採用 Streamable HTTP 傳輸：

- MCP SSE Message API
- MCP SSE Session API