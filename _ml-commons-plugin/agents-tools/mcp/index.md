---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 MCP 工具"
parent: Agents and tools
has_children: true
nav_order: 30
redirect_from:
  - /ml-commons-plugin/agents-tools/mcp/
---

# 使用 MCP 工具
**於 3.0 版導入**
{: .label .label-purple }

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 是一項開放協定標準，為 AI 模型提供連接外部資料來源與工具的標準化方式。OpenSearch 與 MCP 整合，讓代理程式能夠透過 MCP 伺服器使用外部工具與資料來源。

連線至外部 MCP 伺服器可擴充代理程式的能力，包含下列功能：

- 使用 MCP 伺服器提供的工具
- 依據應用程式需求篩選可用的工具
- 為工具存取實作安全的驗證與授權
- 透過一致且標準化的介面與各種工具互動

若要開始使用 MCP，請參閱[連線至外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/)。

本節說明叢集內的 MCP 連接器，讓 OpenSearch 代理程式呼叫託管於外部 MCP 伺服器上的工具。

OpenSearch 也提供 MCP 伺服器，將 OpenSearch API 公開給外部 AI 助理。與叢集內的 MCP 連接器不同，OpenSearch MCP Server 是讓外部用戶端查詢 OpenSearch，而非讓 OpenSearch 代理程式呼叫外部工具。如需更多資訊，請參閱 [OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/)。
{: .note} 