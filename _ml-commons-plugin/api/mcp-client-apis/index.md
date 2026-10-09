---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "MCP 用戶端 API"
parent: ML Commons APIs
has_children: true
has_toc: false
nav_order: 41
redirect_from:
  - /ml-commons-plugin/api/mcp-client-apis/
---

# MCP 用戶端 API
**於 3.8 版推出**
{: .label .label-purple }

當 OpenSearch 透過 MCP 連接器連線至外部 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 伺服器時，它會扮演 MCP 用戶端的角色。這些 API 可讓您在設定代理程式之前，探索並檢視外部 MCP 伺服器所公開的工具。

這與 [MCP 伺服器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/) 不同，後者是 OpenSearch 將自己的工具公開給外部 MCP 用戶端。如需將外部 MCP 伺服器與代理程式搭配使用的概念性資訊，請參閱[連線至外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/)。

ML Commons 支援下列 MCP 用戶端 API：

- [列出連接器 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-client-apis/list-connector-mcp-tools/)
