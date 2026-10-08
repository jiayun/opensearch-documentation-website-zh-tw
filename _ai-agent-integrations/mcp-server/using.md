---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 OpenSearch MCP Server"
parent: OpenSearch MCP Server
nav_order: 10
---

# 使用 OpenSearch MCP Server

本指南說明如何安裝 [OpenSearch MCP Server](https://github.com/opensearch-project/opensearch-mcp-server-py)、將其連接至 AI 用戶端或代理程式架構，以及對 OpenSearch 叢集進行第一次工具呼叫。

## 先決條件

使用 OpenSearch MCP Server 之前，請確認您已具備下列元件：

- 一個執行中的 OpenSearch 叢集，且可從執行伺服器的機器連線。
- 該叢集的認證資訊（自行管理的叢集可使用基本驗證或雙向 TLS (mTLS) 憑證）。
- Python 3.11 或更新版本。
- 下列其中一項工具：
  - [`uv`](https://docs.astral.sh/uv/getting-started/installation/)（建議）-- 使用 `uvx` 執行伺服器，不需要在本機安裝。
  - `pip` -- 將套件安裝至 Python 環境。

## 步驟 1：設定伺服器

請選擇下列其中一種安裝方式：

### 方式 1：使用 `uvx` 執行（建議）

安裝 `uv`，它提供 `uvx` 命令，讓您不必安裝套件即可執行伺服器：

```bash
pip install uv
```
{% include copy.html %}

使用 `uvx`，您可以直接執行伺服器，而不必將其安裝至 Python 環境。本指南中的所有組態範例皆使用 `uvx`。

### 方式 2：使用 pip 安裝

將 `opensearch-mcp-server-py` 套件直接安裝至您的 Python 環境：

```bash
pip install opensearch-mcp-server-py
```
{% include copy.html %}

若您使用此方式，請在後續的組態範例中將 `"command": "uvx"` 替換為 `"command": "python"`，並將 `"args": ["opensearch-mcp-server-py"]` 替換為 `"args": ["-m", "mcp_server_opensearch"]`。

## 步驟 2：將伺服器連接至程式設計助理

Claude Desktop、Cursor 和 Kiro 等程式設計助理會讀取 `mcp.json` 組態檔案來探索 MCP 伺服器。助理啟動時，伺服器會自動以子處理程序的形式啟動。

### Claude Desktop

若要連接至 Claude Desktop，請開啟 **Settings > Developer > Edit Config**。在 macOS 上，組態檔案通常位於 `~/Library/Application Support/Claude/claude_desktop_config.json`。新增下列項目：
```json
{
  "mcpServers": {
    "opensearch": {
      "command": "uvx",
      "args": ["opensearch-mcp-server-py"],
      "env": {
        "OPENSEARCH_URL": "http://localhost:9200",
        "OPENSEARCH_USERNAME": "admin",
        "OPENSEARCH_PASSWORD": "admin",
        "OPENSEARCH_SSL_VERIFY": "false"
      }
    }
  }
}
```
{% include copy.html %}
儲存組態檔案並重新啟動 Claude Desktop。重新啟動後，OpenSearch 工具會出現在 **Tools** 面板中。

### Cursor

若要連接至 Cursor，請開啟 **Cursor Settings > MCP** 並新增伺服器。您也可以直接編輯位於 `~/.cursor/mcp.json` 的組態檔案：
```json
{
  "mcpServers": {
    "opensearch": {
      "command": "uvx",
      "args": ["opensearch-mcp-server-py"],
      "env": {
        "OPENSEARCH_URL": "http://localhost:9200",
        "OPENSEARCH_USERNAME": "admin",
        "OPENSEARCH_PASSWORD": "admin",
        "OPENSEARCH_SSL_VERIFY": "false"
      }
    }
  }
}
```
{% include copy.html %}

### Kiro

若要連接至 Kiro，請編輯工作區中位於 `.kiro/settings/mcp.json` 的組態檔案，或編輯用於全域組態的 `~/.kiro/settings/mcp.json`，並新增下列項目：

```json
{
  "mcpServers": {
    "opensearch": {
      "command": "uvx",
      "args": ["opensearch-mcp-server-py"],
      "env": {
        "OPENSEARCH_URL": "http://localhost:9200",
        "OPENSEARCH_USERNAME": "admin",
        "OPENSEARCH_PASSWORD": "admin",
        "OPENSEARCH_SSL_VERIFY": "false"
      }
    }
  }
}
```
{% include copy.html %}

### 未啟用安全性的叢集

對於未啟用安全性而啟動的本機開發叢集（例如 `docker run -p 9200:9200 opensearchproject/opensearch:latest -e "discovery.type=single-node" -e "DISABLE_SECURITY_PLUGIN=true"`），請使用 `OPENSEARCH_NO_AUTH` 代替認證資訊：

```json
{
  "mcpServers": {
    "opensearch": {
      "command": "uvx",
      "args": ["opensearch-mcp-server-py"],
      "env": {
        "OPENSEARCH_URL": "http://localhost:9200",
        "OPENSEARCH_NO_AUTH": "true"
      }
    }
  }
}
```
{% include copy.html %}

上述範例使用本機開發用的預設認證資訊。請勿在正式環境中使用預設認證資訊。
{: .warning}

## 步驟 3：測試連線

用戶端連接後，請以自然語言提出問題。例如：

> *我的叢集中有哪些索引？哪一個索引的文件最多？*

AI 會選取 `ListIndexTool`，伺服器會呼叫 `_cat/indices`，並將結果傳回給模型。對於後續問題，例如 *「在 `logs` 索引中搜尋過去一小時內的錯誤」*，模型會選取 `SearchIndexTool` 並自動建立 Query DSL 查詢。

## 代理程式架構整合

若要建置管線、聊天機器人或自動化工作流程，您可以將 MCP 伺服器連接至代理程式架構。下列範例使用 `stdio` 傳輸，讓架構能自動以子處理程序的形式啟動 MCP 伺服器。

### Strands Agents

[Strands Agents](https://strandsagents.com/) 是用於建置 AI 代理程式的開放原始碼 Python SDK。它使用 `MCPClient` 類別連接至 MCP 伺服器。使用 stdio 傳輸時，架構會以子處理程序的形式啟動 MCP 伺服器。

若要連接至 Strands Agents，請依照下列步驟操作：

1. 安裝必要的套件：
    ```bash
    pip install strands-agents strands-agents-tools
    ```
    {% include copy.html %}
1. 使用 `MCPClient` 類別連接至 OpenSearch MCP Server：
    ```python
    from mcp import StdioServerParameters
    from strands import Agent
    from strands.tools.mcp import MCPClient

    # The framework launches the MCP server as a subprocess using stdio.
    # No separate server process needed.
    mcp_client = MCPClient(lambda: StdioServerParameters(
        command="uvx",
        args=["opensearch-mcp-server-py"],
        env={
            "OPENSEARCH_URL": "http://localhost:9200",
            "OPENSEARCH_USERNAME": "admin",
            "OPENSEARCH_PASSWORD": "admin",
            "OPENSEARCH_SSL_VERIFY": "false",
        }
    ))

    with mcp_client:
        # Discover all tools exposed by the MCP server
        tools = mcp_client.list_tools_sync()

        # Create an agent with those tools.
        # By default, Strands uses Amazon Bedrock. To use a different model,
        # pass a model= argument. See https://strandsagents.com/docs for options.
        agent = Agent(tools=tools)

        # Natural-language queries — the agent picks the right tool automatically
        print(agent("List all indexes in the cluster and show their document counts."))
        print(agent("Search the 'products' index for items where category is 'electronics'."))
        print(agent("What is the health status of the cluster?"))
    ```
    {% include copy.html %}

### LangGraph

[LangGraph](https://langchain-ai.github.io/langgraph/) 是用於建置具狀態、多步驟代理程式工作流程的架構。請使用 `langchain-mcp-adapters` 將 MCP 工具連接至 LangGraph。使用 `stdio` 傳輸時，架構會為您管理伺服器處理程序。

若要連接至 LangGraph，請依照下列步驟操作：

1. 安裝必要的套件：
    ```bash
    pip install langgraph langchain-mcp-adapters langchain-openai
    ```
    {% include copy.html %}
1. 使用 `langchain-mcp-adapters` 將 MCP 工具連接至 LangGraph：
    ```python
    import asyncio
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    async def main():
        async with MultiServerMCPClient({
            "opensearch": {
                "transport": "stdio",
                "command": "uvx",
                "args": ["opensearch-mcp-server-py"],
                "env": {
                    "OPENSEARCH_URL": "http://localhost:9200",
                    "OPENSEARCH_USERNAME": "admin",
                    "OPENSEARCH_PASSWORD": "admin",
                    "OPENSEARCH_SSL_VERIFY": "false",
                },
            }
        }) as mcp_client:
            tools = mcp_client.get_tools()

            # Create a ReAct agent with the OpenSearch tools.
            # Replace ChatOpenAI with any LangChain-compatible LLM.
            llm = ChatOpenAI(model="gpt-4o")
            agent = create_react_agent(llm, tools)

            # Single query
            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": "List all indexes and tell me which one is largest."}]
            })
            print(result["messages"][-1].content)

            # Multi-step reasoning
            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": (
                    "Find all indexes that contain 'log' in their name, "
                    "then search the largest one for ERROR level entries from the last 24 hours."
                )}]
            })
            print(result["messages"][-1].content)

    asyncio.run(main())
    ```
    {% include copy.html %}

### LangChain（不使用 LangGraph）

若要連接至 LangChain 以進行不使用圖形抽象層的單一代理程式設定，請使用 LangGraph 一節中的相同套件，並建立工具呼叫代理程式：

```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

async def main():
    async with MultiServerMCPClient({
        "opensearch": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["opensearch-mcp-server-py"],
            "env": {
                "OPENSEARCH_URL": "http://localhost:9200",
                "OPENSEARCH_USERNAME": "admin",
                "OPENSEARCH_PASSWORD": "admin",
                "OPENSEARCH_SSL_VERIFY": "false",
            },
        }
    }) as mcp_client:
        tools = mcp_client.get_tools()

        llm = ChatOpenAI(model="gpt-4o")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant with access to OpenSearch tools."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        await agent_executor.ainvoke({"input": "How many documents are in the 'orders' index?"})

asyncio.run(main())
```
{% include copy.html %}

## 多叢集組態

若要將 MCP 伺服器連接至多個叢集，請在您選擇的位置建立 `config.yml` 檔案：

```yaml
version: "1.0"
description: "OpenSearch cluster configurations"

clusters:
  local-dev:
    opensearch_url: "http://localhost:9200"
    opensearch_username: "admin"
    opensearch_password: "admin"

  staging:
    opensearch_url: "https://staging.example.com:9200"
    opensearch_username: "admin"
    opensearch_password: "staging_password"
    opensearch_ca_cert_path: "/path/to/ca.crt"
```
{% include copy.html %}

以多叢集模式啟動伺服器，並指定組態檔案的完整路徑：

```bash
python -m mcp_server_opensearch --mode multi --config /path/to/config.yml --transport stream
```
{% include copy.html %}

在多叢集模式下，每次工具呼叫都必須包含一個 `opensearch_cluster_name` 參數，且其值須與組態檔案中的某個鍵相符。使用程式設計助理時，請在系統提示中列出可用的叢集名稱。

## 驗證選項

伺服器會依下列順序嘗試驗證方法：

1. **不驗證** -- `OPENSEARCH_NO_AUTH=true`，適用於開放式叢集。
2. **以標頭為基礎的驗證** -- `OPENSEARCH_HEADER_AUTH=true`。伺服器會在每次呼叫時從請求標頭讀取認證資訊，因此在使用串流傳輸時，每個工作階段都可以使用不同的認證資訊。
3. **基本驗證** -- `OPENSEARCH_USERNAME` 和 `OPENSEARCH_PASSWORD`。
4. **雙向 TLS** -- `OPENSEARCH_CA_CERT_PATH`、`OPENSEARCH_CLIENT_CERT_PATH` 和 `OPENSEARCH_CLIENT_KEY_PATH`。可搭配或不搭配基本驗證使用。

如需 IAM 和 AWS 認證資訊選項的相關資訊，請參閱 [`opensearch-mcp-server-py` 儲存庫](https://github.com/opensearch-project/opensearch-mcp-server-py/blob/main/USER_GUIDE.md#authentication)。

## 傳輸方式：Stdio 與串流

伺服器支援下列傳輸選項。

| 傳輸方式 | 使用時機 | 啟動方式 |
|-----------|-------------|--------------|
| `stdio`（預設） | 程式設計助理（Claude Desktop、Cursor、Kiro）。用戶端會將伺服器作為子處理序啟動。 | 在 `mcp.json` 中設定。伺服器會在用戶端啟動時自動啟動。 |
| `stream`（streamable-http） | 代理程式框架（Strands、LangGraph、LangChain）以及遠端／共用部署。 | `python -m mcp_server_opensearch --transport stream` |

串流傳輸預設會繫結至 `0.0.0.0:9900`。若要使用不同的主機或連接埠，請指定 `--host` 和 `--port`。

## 常見問題

下列清單說明常見的連線與組態問題：

- **用戶端中未顯示任何工具**：請檢查用戶端的 MCP 記錄檔，確認伺服器已成功啟動。執行 `curl http://localhost:9200` 以確認可以連線至 OpenSearch 叢集。
- **框架無法連線至串流伺服器**：執行 `curl http://localhost:9900/mcp` 以確認伺服器已啟動。確認框架組態中的 URL 與伺服器 URL 完全相符，包括 `/mcp` 路徑。
- **在多叢集模式下，AI 模型選取了錯誤的叢集**：請在系統提示中提供可用叢集名稱及其用途的清單。

## 後續步驟

- 如需 Kubernetes 部署、結構化記錄、工具篩選和工具自訂的相關資訊，請參閱 [`opensearch-mcp-server-py` 儲存庫](https://github.com/opensearch-project/opensearch-mcp-server-py/blob/main/USER_GUIDE.md)。
- 若要將 MCP 工具整合至 OpenSearch 代理程式（而非將 OpenSearch 公開給外部代理程式），請參閱[使用 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/)。
- 如需引導 AI 助理完成 OpenSearch 任務的結構化工作流程，請參閱[代理程式技能]({{site.url}}{{site.baseurl}}/ai-agent-integrations/agent-skills/)。
