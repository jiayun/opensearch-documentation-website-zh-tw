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
**於 3.0 版推出**
{: .label .label-purple }

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 定義了代理程式如何探索及執行工具。OpenSearch 中的 MCP 伺服器可讓代理程式連線並使用可用的[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/)。

ML Commons 中的 MCP 伺服器使用 Streamable HTTP 傳輸通訊協定與用戶端通訊。如需傳輸的詳細資訊，請參閱[官方 MCP 文件](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。
{: .note }

ML Commons 支援下列 MCP API：

- [註冊 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/register-mcp-tools/)
- [更新 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/update-mcp-tools/)
- [列出 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/list-mcp-tools/)
- [移除 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/remove-mcp-tools/)
- [MCP Streamable HTTP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/mcp-server/)

## 已移除的 API

下列實驗性 API 已於 OpenSearch 3.3 中移除，改採用 Streamable HTTP 傳輸：

- MCP SSE Message API
- MCP SSE Session API