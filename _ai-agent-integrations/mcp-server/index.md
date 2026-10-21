---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch MCP Server
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /ai-agent-integrations/mcp-server/
---

# OpenSearch MCP Server

[OpenSearch MCP Server](https://github.com/opensearch-project/opensearch-mcp-server-py) 是一個開放原始碼的 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 伺服器，可將 OpenSearch 提供給 Claude Desktop、Cursor、Kiro 等 AI 助理，或任何其他相容於 MCP 的用戶端使用。連線後，AI 助理即可透過 MCP 工具呼叫 OpenSearch API，來搜尋索引、讀取對應、檢查叢集健康狀態及執行其他操作，而不必自行產生原始 REST 請求。

OpenSearch 也支援叢集內的 MCP：MCP 連接器可讓 OpenSearch 代理程式呼叫託管於外部 MCP 伺服器的工具，而叢集內的 MCP 伺服器則可讓外部 MCP 用戶端呼叫您叢集中註冊的工具。如需詳細資訊，請參閱 [MCP 伺服器與用戶端]({{site.url}}{{site.baseurl}}/ml-commons-plugin/mcp/)。
{: .note}

當您想要執行下列事項時，請使用 OpenSearch MCP Server：

- 讓 AI 助理以自然語言查詢及探索您的 OpenSearch 叢集。
- 建置內部 AI 工具（聊天機器人、可觀測性副駕駛或資料助理），而不必自行實作 OpenSearch 用戶端層。
- 從單一助理工作階段連線至多個叢集（例如 `dev`、`staging` 或 `production`）。
- 使用標準通訊協定，將 OpenSearch 與 LangChain 或 LangGraph 等代理程式架構整合。

OpenSearch MCP Server 提供下列功能：

- MCP 介面：支援任何相容於 MCP 的用戶端，包括 Claude Desktop、Cursor 和 Kiro。
- 工具：包含列出索引、擷取對應、執行搜尋查詢、檢查叢集健康狀態及計算文件數量等工具。可視需要啟用其他工具類別（搜尋相關性和技能式分析）。
- 傳輸選項：支援供本機桌面用戶端使用的標準輸入/輸出（`stdio`），以及供遠端部署使用的串流傳輸。串流傳輸支援 Streamable HTTP 和舊版 Server-Sent Events (SSE) 傳輸。
- 驗證：支援基本驗證、AWS IAM 角色、AWS 設定檔認證資訊、以標頭為基礎的驗證、雙向 TLS (mTLS) 及匿名存取。
- 叢集組態：支援使用環境變數的單一叢集模式，或使用 YAML 組態檔案的多叢集模式。
- 服務相容性：可搭配自行管理的 OpenSearch、Amazon OpenSearch Service 及 Amazon OpenSearch Serverless 集合使用。

伺服器會接收來自 AI 用戶端的 MCP 工具呼叫，將其轉譯為 OpenSearch REST API 呼叫，並傳回結構化結果，如下圖所示。

![顯示從 AI 用戶端到 OpenSearch MCP Server 再到 OpenSearch 叢集之流程的圖表]({{site.url}}{{site.baseurl}}/images/ai-agent-integrations/mcp-server.png)

## 內建工具

核心工具預設為啟用。您可以使用環境變數或多叢集組態檔案啟用其他工具類別。下表列出各工具類別。

| 類別 | 預設 | 範例工具 |
|----------|---------|---------------|
| 核心 | 已啟用 | `ListIndexTool`, `SearchIndexTool`, `IndexMappingTool`, `ClusterHealthTool`, `CountTool`, `ExplainTool`, `MsearchTool`, `GetShardsTool`, `GenericOpenSearchApiTool` |
| 叢集與索引 | 已停用 | `GetClusterStateTool`, `CatNodesTool`, `GetNodesTool`, `GetIndexInfoTool`, `GetIndexStatsTool`, `GetSegmentsTool`, `GetAllocationTool`, `GetLongRunningTasksTool`, `GetNodesHotThreadsTool`, `GetQueryInsightsTool` |
| `search_relevance` | 已停用 | `CreateSearchConfigurationTool`、`CreateQuerySetTool`、`CreateJudgmentListTool`、`CreateExperimentTool`，以及相關的 `Get`/`Delete`/`Search` 變體 |
| `skills` | 已停用 | `DataDistributionTool`, `LogPatternAnalysisTool` |

如需完整清單及各工具的參數，請參閱 [`opensearch-mcp-server-py` README](https://github.com/opensearch-project/opensearch-mcp-server-py#available-tools)。

## 後續步驟

- 若要安裝伺服器並將其連線至您的 AI 用戶端，請參閱[使用 OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/using/)。

## 相關文件

- [`opensearch-mcp-server-py`](https://github.com/opensearch-project/opensearch-mcp-server-py) -- GitHub 上的原始碼儲存庫。
- [Model Context Protocol 規格](https://modelcontextprotocol.io/introduction) -- MCP 協定規格。
