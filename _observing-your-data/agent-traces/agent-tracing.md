---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檢視代理程式追蹤"
parent: Agent traces
nav_order: 20
---

# 檢視代理程式追蹤
**於 3.6 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 **Agent Traces** 頁面可讓您探索、偵錯及監視大型語言模型（LLM）代理程式的執行追蹤。您可以透過多個同步的視覺化檢視來查看追蹤、檢查跨度詳細資訊，以及分析代理式 AI 應用程式的指標。

## 啟用代理程式追蹤

預設的 OpenSearch 發行版本包含代理程式追蹤功能。若要啟用代理程式追蹤，請將下列功能旗標新增至您的 `opensearch_dashboards.yml` 組態檔案：

```yaml
workspace.enabled: true
data_source.enabled: true
explore.enabled: true
explore.agentTraces.enabled: true
```
{% include copy.html %}

更新組態後，請重新啟動 OpenSearch Dashboards，讓變更生效。

預設的 OpenSearch 發行版本預設會啟用 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢支援。如果您執行的是 OpenSearch 精簡發行版本，請先[安裝 SQL 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)，再使用代理程式追蹤。
{: .note}

## 瞭解追蹤與跨度

在代理程式追蹤中，**追蹤**代表完整的執行流程（例如單次代理程式呼叫），而**跨度**代表該追蹤中的個別操作（例如 LLM 呼叫、工具執行或擷取操作）。每個追蹤都由一或多個跨度組成，並依父子階層組織。

### 跨度類別

代理程式追蹤會根據 `gen_ai.operation.name` 屬性將跨度分類。每個類別在 **Agent Traces** 頁面中都有不同的顏色與圖示。

| 類別 | 操作名稱 | 說明 |
| :--- | :--- | :--- |
| Agent | `invoke_agent`, `create_agent` | 代理程式呼叫與初始化。 |
| LLM | `chat`, `text_completion`, `generate_content` | LLM 聊天補全、文字補全與內容生成請求。 |
| Tool | `execute_tool` | 工具與函式呼叫。 |
| Embeddings | `embeddings` | 嵌入生成請求。 |
| Retrieval | `retrieval` | 文件或資料擷取操作。 |
| Other | 未對應的操作 | 不符合任何已知類別的操作。 |

### 跨度屬性

當您使用 [`opensearch-genai-observability-sdk-py` SDK]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/instrument/) 為應用程式加入檢測功能時，系統會自動建立具有必要屬性的跨度。下列表格列出核心 OpenTelemetry 屬性與生成式 AI 語意慣例屬性。

#### 核心屬性

下表列出核心 OpenTelemetry 屬性。

| 屬性 | 必要 | 說明 |
| :--- | :--- | :--- |
| `traceId` | 是 | 追蹤的唯一識別碼。 |
| `spanId` | 是 | 跨度的唯一識別碼。 |
| `parentSpanId` | 否 | 父跨度的識別碼。根跨度的此值為空。 |
| `startTime` | 是 | 跨度的開始時間戳記。 |
| `endTime` | 是 | 跨度的結束時間戳記。 |
| `durationInNanos` | 是 | 跨度的持續時間，以奈秒為單位。 |
| `status.code` | 是 | 跨度的狀態碼。有效值為 `OK`（成功）、`ERROR`（失敗）或 `UNSET`（未明確設定時的預設狀態）。 |

#### 生成式 AI 屬性

下表列出生成式 AI 語意慣例屬性。

| 屬性 | 必要 | 說明 |
| :--- | :--- | :--- |
| `gen_ai.operation.name` | 是 | 操作類型。有效值為 `chat`、`invoke_agent`、`execute_tool`、`create_agent`、`text_completion`、`embeddings` 或 `retrieval`。用於跨度分類、篩選及分頁查詢。 |
| `gen_ai.provider.name` | 是 | 生成式 AI 提供者名稱（例如 `openai`、`anthropic`）。 |
| `gen_ai.agent.name` | 選用 | 便於人員閱讀的 GenAI 代理程式名稱。 |
| `gen_ai.request.model` | 選用 | 接收請求的模型名稱。 |
| `gen_ai.usage.input_tokens` | 選用 | 消耗的輸入詞元數量。 |
| `gen_ai.usage.output_tokens` | 選用 | 生成的輸出詞元數量。 |
| `gen_ai.input.messages` | 選用 | 作為模型輸入的聊天歷程記錄或提示。 |
| `gen_ai.output.messages` | 選用 | 模型傳回的訊息或補全內容。 |
| `gen_ai.tool.name` | 選用 | 代理程式使用的工具名稱。僅適用於 `execute_tool` 操作跨度。 |
| `gen_ai.tool.call.id` | 選用 | 工具呼叫識別碼。僅適用於 `execute_tool` 操作跨度。 |

## 資料管線

代理程式追蹤遵循下列資料管線：

1. 已加入檢測功能的 LLM 應用程式透過 gRPC 或 HTTP 傳送 OpenTelemetry Protocol（OTLP）資料。
2. OpenTelemetry Collector 處理資料並將其路由至目的地。
3. [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/index/) 使用 `otel_trace_raw` 處理器將資料匯入 OpenSearch。
4. OpenSearch 將追蹤資料儲存在 `otel-v1-apm-span-*` 索引中。
5. OpenSearch Dashboards 在 **Agent Traces** 頁面中顯示追蹤。

## 使用介面

若要在 OpenSearch Dashboards 中存取代理程式追蹤，請從主選單選取 **Observability**，然後選取 **Agent Traces**。

**Agent Traces** 頁面包含下列元件。

### Traces 分頁

Traces 分頁會在分頁式表格中顯示根層級的追蹤。您可以展開資料列，直接在該列中檢視子跨度。

下圖顯示 Traces 分頁。

![顯示根層級代理程式追蹤的 Traces 分頁]({{site.url}}{{site.baseurl}}/images/agent-traces/traces-table.png)

### Spans 分頁

Spans 分頁會顯示所有生成式 AI 跨度，而非僅顯示根追蹤。使用此分頁可檢查多個追蹤中的個別操作。此表格包含與 [Traces 分頁](#traces-tab)相同的欄。

下圖顯示 Spans 分頁。

![顯示所有生成式 AI 跨度的 Spans 分頁]({{site.url}}{{site.baseurl}}/images/agent-traces/spans-table.png)

## 追蹤詳細資訊

在 Traces 或 Spans 分頁中選取一個資料列，即可開啟追蹤詳細資訊。追蹤詳細資訊提供三個同步的視覺化檢視與一個跨度詳細資訊面板。在任一檢視中選取跨度時，該跨度會在所有三個檢視中醒目顯示。

### 代理程式圖形

代理程式圖形使用 Dagre 版面配置演算法，將追蹤呈現為有向非循環圖（DAG）。父跨度向下連接至子跨度，同層跨度則以水平方向排列。

下圖顯示代理程式圖形檢視。

![顯示 DAG 視覺化的 Agent Graph]({{site.url}}{{site.baseurl}}/images/agent-traces/agent-graph.png)

圖形中的每個節點都包含下列元素：

- 以顏色區分的徽章，表示跨度類別（例如 Agent、LLM 或 Tool）。
- 跨度名稱，截斷至 37 個字元。
- 長條，顯示跨度持續時間占追蹤總時間的百分比。
- 紅色徽章，顯示於狀態為 `ERROR` 的跨度。

Agent Graph 提供下列控制功能：

- 將縮放倍率調整為 0.1x 至 2x。
- 重設檢視區域以顯示所有節點。

選取節點可在跨度詳細資訊面板中檢視其詳細資訊。選取背景可取消選取節點。

### 追蹤樹狀檢視

追蹤樹狀檢視會以可展開的階層結構顯示所有跨度。每個資料列會顯示下列資訊：

- 以顏色區分的跨度類別。
- 操作名稱。
- 操作消耗的詞元數量。
- 跨度持續時間。

展開或摺疊節點，以瀏覽父子關係。

下圖顯示追蹤樹狀檢視。

![顯示跨度階層結構的追蹤樹狀檢視]({{site.url}}{{site.baseurl}}/images/agent-traces/trace-tree.png)

### 時間軸檢視

時間軸檢視以甘特圖形式，按時間順序顯示跨度的持續時間。每個跨度都會顯示為水平長條，具有下列特性：

- 長條寬度對應跨度持續時間。
- 長條顏色與跨度類別的顏色相符。
- 縮排反映跨度的階層深度。

重疊的長條表示並行操作。使用此檢視可找出瓶頸，並瞭解代理程式的循序與平行執行模式。

下圖顯示時間軸檢視。

![顯示甘特圖形式跨度圖表的時間軸檢視]({{site.url}}{{site.baseurl}}/images/agent-traces/timeline.png)

### 跨度詳細資訊面板

右側面板會顯示所選跨度的詳細資訊，包括所有 JSON 屬性與執行時間資訊。
