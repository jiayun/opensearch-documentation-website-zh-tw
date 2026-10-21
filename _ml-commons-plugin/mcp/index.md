---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "MCP 伺服器與用戶端"
nav_order: 25
has_children: true
has_toc: false
redirect_from:
  - /ml-commons-plugin/mcp/
---

# MCP 伺服器與用戶端

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 是一項開放標準，定義 AI 應用程式如何探索及呼叫工具。OpenSearch 透過下列元件支援 MCP。

| 元件 | 使用情境 | 執行位置 |
| :--- | :--- | :--- |
| [MCP 連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/) | 讓 OpenSearch 代理程式呼叫託管於外部 MCP 伺服器的工具。OpenSearch 扮演 MCP 用戶端。 | 您的叢集內 |
| [叢集內 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/in-cluster-mcp-server/) | 讓外部 MCP 用戶端呼叫註冊於您叢集中的工具。OpenSearch 扮演 MCP 伺服器。 | 您的叢集內 |
| [獨立 MCP 伺服器]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/) | 讓外部 AI 助理使用 OpenSearch 的 REST API 查詢 OpenSearch。 | 您的叢集外 |

獨立 MCP 伺服器是開放原始碼的 [OpenSearch MCP Server](https://github.com/opensearch-project/opensearch-mcp-server-py) 專案。

## 選擇 MCP 伺服器

若要讓外部 AI 應用程式存取 OpenSearch，請依您的需求選擇 MCP 伺服器。

| 需求 | 叢集內 MCP 伺服器 | 獨立 MCP 伺服器 |
| :--- | :--- | :--- |
| 設定 | 啟用 `plugins.ml_commons.mcp_server_enabled` 設定。無需安裝。 | 安裝伺服器並以獨立程序執行。 |
| 公開的工具 | 您在叢集中註冊的工具 | 伺服器提供的工具，會呼叫 OpenSearch REST API |
| 傳輸方式 | Streamable HTTP | 標準輸入/輸出 (`stdio`)、Streamable HTTP，以及舊版 Server-Sent Events (SSE) |
| 叢集 | 執行伺服器的叢集 | 一個或多個叢集，包括 Amazon OpenSearch Service 網域與 Amazon OpenSearch Serverless 集合 |
