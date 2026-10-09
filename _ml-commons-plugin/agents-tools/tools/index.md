---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工具"
parent: Agents and tools
has_children: true
has_toc: false
nav_order: 20
redirect_from: 
  - /ml-commons-plugin/agents-tools/tools/
  - /ml-commons-plugin/agents-tools/tools/cat-index-tool/
  - /ml-commons-plugin/agents-tools/tools/dynamic-tool/
---

# 工具
**於 2.13 版推出**
{: .label .label-purple }

_工具_ 會執行一組特定工作。下表列出 OpenSearch 支援的所有工具。

指定工具時，請提供其 `type`、`parameters`，以及選用的 `description`。例如，您可以如下指定 `AgentTool`：

```json
{
  "type": "AgentTool",
  "description": "A general agent to answer any question",
  "parameters": {
    "agent_id": "9X7xWI0Bpc3sThaJdY9i"
  }
}
```

每個工具都會接受一組專屬於該工具的參數。在上述範例中，`AgentTool` 會接受其將執行之代理程式的 `agent_id`。如需參數清單，請參閱各工具的說明文件。

您也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 直接執行工具，而不需建立代理程式，這對於測試個別工具或執行獨立操作很有用。

|工具	| 說明	|
|:---	|:---	|
|[`AgentTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/agent-tool/)	|執行任何代理程式。 |
|[`ConnectorTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/connector-tool/)	| 使用[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)呼叫任何 REST API 函式。 |
|[`CreateAnomalyDetectorTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/create-anomaly-detector/)	| 讓 LLM 建議建立異常偵測器所需的參數。 |
|[`DataDistributionTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/data-distribution-tool/)	| 分析資料集內的資料分布模式，並比較不同時間區間的分布。 |
|[`IndexMappingTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index-mapping-tool/)	|擷取索引的索引對應與設定資訊。 |
|[`ListIndexTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/list-index-tool/)	|擷取 OpenSearch 叢集的索引資訊。於 OpenSearch 3.0 版推出，用以取代 `CatIndexTool`。 |
|[`LogPatternAnalysisTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/log-pattern-analysis-tool/)	|透過比較分析偵測異常的記錄檔模式與序列，執行進階記錄檔分析。 |
|[`LogPatternTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/log-pattern-tool/)	|分析記錄資料，以擷取並識別記錄訊息中重複出現的結構模式。 |
|[`MLModelTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/ml-model-tool/)	|執行機器學習模型。	|
|[`NeuralSparseSearchTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/neural-sparse-tool/)	| 執行稀疏向量擷取。 |
|[`PPLTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/ppl-tool/)	|將自然語言轉譯為 Piped Processing Language (PPL) 查詢。	|
|[`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/)	|根據使用者的自然語言問題建立並執行 OpenSearch DSL 查詢。	|
|[`RAGTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/rag-tool/)	|使用神經搜尋或神經稀疏搜尋擷取文件，並整合大型語言模型來摘要答案。 |
|[`ReadFromScratchPadTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/scratchpad-tools/)	|在執行期間從代理程式的暫存記憶體讀取筆記與資訊。 |
|[`SearchAlertsTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-alerts-tool/)	|搜尋警示。	|
|[`SearchAnomalyDetectorsTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-anomaly-detectors/)	| 搜尋異常偵測器。	|
|[`SearchAnomalyResultsTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-anomaly-results/)	| 搜尋異常偵測器產生的異常偵測結果。	|
|[`SearchIndexTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-index-tool/)	|使用以查詢領域特定語言 (DSL) 撰寫的查詢來搜尋索引。 |
|[`SearchMonitorsTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/search-monitors-tool/)	| 搜尋警示監視器。	|
|[`VectorDBTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/vector-db-tool/)	|執行稠密向量擷取。	|
|[`VisualizationTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/visualization-tool/)	|在 OpenSearch Dashboards 中尋找視覺化。	|
|[`WebSearchTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/web-search-tool/)	|使用網路搜尋回答使用者的問題。	|
|[`WriteToScratchPadTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/scratchpad-tools/)	|在執行期間將筆記與資訊寫入代理程式的暫存記憶體。 |

## 開發人員資訊

代理程式與工具架構提供彈性與擴充性。請參閱[工具程式庫](https://github.com/opensearch-project/skills/tree/main/src/main/java/org/opensearch/agent/tools)以了解 OpenSearch 提供的工具。實作 [**Tool** 介面](https://github.com/opensearch-project/ml-commons/blob/2.x/spi/src/main/java/org/opensearch/ml/common/spi/tools/Tool.java)以針對不同使用案例建置自訂工具。
