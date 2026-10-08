---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AI 代理程式整合"
nav_order: 1
nav_exclude: true
permalink: /ai-agent-integrations/
redirect_from:
  - /ai-agent-integrations/index/
---

# AI 代理程式整合

OpenSearch 可與 AI 代理程式整合，讓您將其作為外部 AI 工具的資料來源，或在叢集內執行代理程式。OpenSearch 以兩種方式支援 AI 代理程式：

- **連線至 OpenSearch 的外部代理程式**（本節）-- AI 工具在您的 OpenSearch 叢集之外執行，並將 OpenSearch 作為資料來源。範例包括搭配 MCP Server 的 Claude Desktop，或搭配代理程式技能的 Cursor。請在您的電腦上安裝這些工具並設定您的用戶端。
- **在 OpenSearch 中執行的內部代理程式** -- OpenSearch 代理程式在 OpenSearch 叢集內執行，可同時呼叫內部工具與外部 MCP 伺服器。請透過 ML Commons Agent API 註冊這些代理程式並設定叢集設定。如需詳細資訊，請參閱[代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/)。

下圖說明外部與內部代理程式如何與 OpenSearch 整合。

![說明外部與內部代理程式如何與 OpenSearch 整合的圖表]({{site.url}}{{site.baseurl}}/images/ai-agent-integrations/ai-integrations.png)

## 外部代理程式整合

外部 AI 代理程式與程式設計助理可以使用下列在叢集外執行的開放原始碼專案連線至 OpenSearch：

- [OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/) -- 一個 [Model Context Protocol (MCP) 伺服器](https://modelcontextprotocol.io/introduction)，可將 OpenSearch 提供給與 MCP 相容的用戶端使用，例如 Claude Desktop、Cursor 和 Kiro。AI 用戶端提出自然語言請求，伺服器再將其轉譯為 OpenSearch REST 呼叫。
- [代理程式技能]({{site.url}}{{site.baseurl}}/ai-agent-integrations/agent-skills/) -- 可安裝的技能套件，用於教導 AI 程式設計助理如何建置搜尋應用程式、分析記錄檔與追蹤，以及將 OpenSearch 部署至 AWS。技能在助理內執行，並遵循 [Agent Skills 規格](https://agentskills.io/specification)；不需要伺服器。

## 相關功能

OpenSearch 也提供下列在叢集*內部*設定的代理程式功能：

- 透過 ML Commons Agent API 註冊的[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)（flow、conversational 和 plan-execute-reflect）。
- OpenSearch 代理程式可使用的[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/)，例如 `VectorDBTool`、`ListIndexTool` 和 `PPLTool`。
- [叢集內 MCP 連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/)，可讓 OpenSearch 代理程式呼叫託管於*外部* MCP 伺服器上的工具。

下表說明何時使用各項功能。

| 使用案例 | 功能 |
| :--- | :--- |
| 讓外部 AI 助理查詢 OpenSearch | [OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/) |
| 教導程式設計助理如何使用 OpenSearch | [代理程式技能]({{site.url}}{{site.baseurl}}/ai-agent-integrations/agent-skills/) |
| 在 OpenSearch *內部*執行會呼叫外部工具的代理程式  | [使用 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/) |
| 在叢集內註冊並執行代理程式 | [代理程式與工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/) |
