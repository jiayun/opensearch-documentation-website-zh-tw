---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定代理式搜尋"
parent: Building AI search workflows in OpenSearch Dashboards
grand_parent: AI search
nav_order: 20
---

# 設定代理式搜尋
**推出於 3.3**
{: .label .label-purple }

這是實驗性的 UI 功能。如需此功能進度的最新資訊，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。    
{: .warning}

[代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/)可讓您以自然語言提出問題，並由 OpenSearch 代理程式自動規劃及執行擷取。此功能結合大型語言模型 (LLM) 與 OpenSearch 的搜尋能力，提供智慧且具情境感知的搜尋體驗。

OpenSearch Dashboards 提供直覺的介面，可用來設定代理程式、為代理程式配備不同的工具、執行代理式搜尋，以及將代理式搜尋整合至您的應用程式。

下圖顯示代理式搜尋工作流程介面，左側為代理程式組態選項，右側為搜尋執行功能。

![代理式搜尋編輯器]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-editor.png)

## 先決條件

設定代理式搜尋之前，請確認您已符合下列先決條件。

### 佈建 ML 資源

若要設定新的代理程式，請先佈建適當的模型。如需可運作的範例，請參閱[模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)。

### 匯入資料

請確認您的叢集中有足夠的文件數量，以便合理評估您的代理式搜尋。

## 存取外掛程式

若要存取此外掛程式，請前往 **OpenSearch Dashboards**，並從頂端選單選取 **OpenSearch Plugins** > **AI Search Flows**。

## 設定代理程式

代理程式具有高度自訂性，可依您的使用情境以多種方式設定。下圖顯示完整設定的對話式代理程式。

![代理程式組態]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agent-configuration.png)

### 代理程式類型

[流程代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/flow/)針對查詢產生的速度與簡潔性進行最佳化。[對話式代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/conversational/)可設定更多工具與功能，以進行更深入的推理。代理程式類型僅能在建立代理程式時設定**一次**。

設定流程代理程式時，部分模型需要您在 **Query Planning** 工具中手動新增合適的 `response_filter`。如需詳細資訊，請參閱[註冊流程代理程式]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/flow-agent/#step-4-register-a-flow-agent)。支援的提供者為 OpenAI 與 Amazon Bedrock Converse。 
{: .note}

### 模型

在對話式代理程式中，模型負責智慧推理，包括工具協調、連線至外部來源，以及產生適當的查詢領域特定語言 (DSL) 查詢。在流程代理程式中，工具會依序執行，而 **Query Planning** 工具中的模型僅用於產生查詢。不同的模型針對不同情境進行最佳化：兼具成本效益與快速推論，相對於需要大量資源的深度推理方法。

如需與代理式搜尋相容的建議模型清單，請參閱[模型組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#model-configuration)。

### 工具

所有代理程式都需要 **Query Planning** 工具才能執行代理式搜尋。查詢產生可完全由 LLM 產生 (預設)，或由預先定義的搜尋範本引導。搜尋範本可引導模型使用已知、經過測試且效能良好的查詢模式，協助維持對所產生查詢的控制。

下圖顯示 **Query Planning** 工具內的搜尋範本組態介面。

![搜尋範本]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-search-template.png)

對話式代理程式還可使用其他預先建置的工具，包括 **Search Index**、**List Index**、**Index Mapping** 與 **Web Search**。啟用這些工具可擴充代理程式的功能。雖然這些是代理式搜尋中最常用的工具，但還有其他多種 [OpenSearch 工具可供使用]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)，且可在 **JSON** 檢視中手動設定。

### MCP 伺服器

若要讓對話式代理程式存取更多外部工具，請將其與 Model Context Protocol (MCP) 伺服器整合。若要限制代理程式可存取的工具，請在 **Tool filters** 下為每個伺服器設定篩選條件。如需詳細資訊，請參閱[使用外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/mcp-server)。

## 執行代理式搜尋

測試代理程式在不同索引與搜尋查詢下的表現。收合 **Configure agent** 面板，以專注於執行搜尋及分析結果。下圖顯示針對 `demo_amazon_fashion` 索引搜尋 `mens blue shirts`，包含相關的結果圖片。

![代理式搜尋組態]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-configuration.png)

### 索引

試用叢集中的不同索引。若要檢視索引詳細資料，請選取 **Inspect** 按鈕。對於對話式代理程式，您可以選取 **All indexes**，讓代理程式選擇適當的索引。

### 代理程式

試用您建立的不同代理程式。若要檢視代理程式詳細資料，請選取 **Inspect** 按鈕。

### 查詢

測試不同的自然語言查詢。若要指定代理程式在您所選索引中應聚焦的欄位，請選取 **Add query fields**。若要直接編輯完整的 `agentic` 搜尋查詢，請切換至 **JSON** 檢視。對於對話式代理程式，請在搜尋後選取 **Continue conversation**，以保留後續搜尋的情境。若要捨棄對話歷程並重新開始，請選取 **Clear conversation**。

### 執行搜尋

若要執行代理式搜尋，請選取 **Search**。代理程式在推理查詢、分析索引對應及執行工具協調時，此程序可能需要數秒。如果搜尋耗時過久，或您想嘗試不同的搜尋，請選取 **Stop**。

搜尋完成後，請在下列區段中檢視結果：

- **Generated query**：代理程式產生並對您的叢集執行的 Query DSL
- **Search results**：搜尋回應，並依結果提供可用的分頁：
  - **Aggregations**：當回應包含彙總時顯示
  - **Visual hits**：當文件命中包含圖片時顯示
  - **Hits**：當回應包含任何命中時顯示
  - **Raw response**：一律可供詳細檢查

對於對話式代理程式，請選取 **View agent summary**，以查看代理程式動作的逐步明細，包括所用工具的順序及每個步驟背後的推理。

下圖顯示搜尋結果介面，包含不同的檢視分頁與代理程式摘要選項。

![代理式搜尋結果]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-search-results.png)

### 在您的應用程式中使用代理式搜尋

選取 **Export**，以檢視在下游應用程式中使用代理式搜尋所需的所有基礎資源，包括代理程式與搜尋管線詳細資料。

下圖顯示匯出對話方塊，內含將代理式搜尋整合至應用程式的程式碼範例。

![代理式搜尋匯出]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-export.png)

## 範例：使用 GPT-5 進行產品搜尋

此範例使用已部署的 OpenAI [GPT-5 模型]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-customization/#gpt-5-recommended)，以及由[時尚產品圖片資料集](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)產生的索引。
{: .note}

1. 前往 **AI Search Flows** 外掛程式。在 **Workflows** 頁面上，選取 **New workflow** 分頁，如下圖所示。在 **Agentic Search** 範本中，選取 **Create**。

   ![新增工作流程頁面]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/new-workflow-page.png)
2. 提供唯一的工作流程 **Name** 及選用的 **Description**，如下圖所示。然後選取 **Create** 以建立您的工作流程。您會自動被導向工作流程編輯器，並可在其中開始設定代理程式。

   ![快速設定對話方塊]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-quick-configure-modal.png)
3. 在 **Configure agent** 下，選取 **Create new agent**。輸入唯一的 **Name**，選擇性提供 **Description**，並在 **Model** 下選取已部署的 **OpenAI GPT-5** 模型。最後，在底部選取 **Create agent**。

   ![代理式搜尋組態]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-configuration.png)
4. 在 **Agentic search** 下，選取您要搜尋的索引，或保留預設的 **All indices**，讓代理程式自行決定。代理程式將已處於選取狀態。
5. 在 **Query** 下，輸入關於您資料的自然語言查詢，如下圖所示。選取 **Search** 以執行代理式搜尋。

   ![代理式搜尋]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-search.png)
6. 檢視代理程式產生的查詢、搜尋命中及代理程式摘要。

   下圖顯示代理程式為此搜尋產生的 Query DSL。

   ![代理式搜尋查詢]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-query.png)

   下圖顯示包含產品圖片與詳細資料的搜尋結果。

   ![代理式搜尋命中]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-hits.png)

   下圖顯示代理程式的逐步推理與工具使用摘要。

   ![代理式搜尋摘要]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/agentic-search-example-summary.png)

7. 您也可以選擇性地調整代理程式，嘗試不同的工具、模型及 MCP 伺服器整合，以了解代理程式針對您資料的不同查詢時的表現。

## 後續步驟

- 在 [ML Playground](https://ml.playground.opensearch.org/app/opensearch-flow#/workflows/WAmxgJoBWVNV3bhKKnGx?configureAgent=false) 上試用代理式搜尋。
- 進一步了解[代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/)。
- 閱讀[這篇關於代理式搜尋的部落格文章](https://opensearch.org/blog/introducing-agentic-search-in-opensearch-transforming-data-interaction-through-natural-language/)。
- 探索 [OpenSearch 代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/index/)。
- 加入 [OpenSearch 論壇](https://forum.opensearch.org/t/use-cases-and-general-feedback-for-agentic-search/27488)的討論。
- 在 [GitHub](https://github.com/opensearch-project/dashboards-flow-framework) 上回報問題。