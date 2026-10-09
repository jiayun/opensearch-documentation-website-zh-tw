---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 OpenSearch Dashboards 中建立 AI 搜尋工作流程"
parent: AI search
has_children: true
has_toc: false
nav_order: 80
redirect_from:
  - /automating-configurations/workflow-builder/
  - /tutorials/ai-search-flows/building-flows/
  - /tutorials/gen-ai/ai-search-flows/building-flows/
---

# 在 OpenSearch Dashboards 中建立 AI 搜尋工作流程

在 OpenSearch Dashboards 中，您可以使用 AI Search Flows 反覆建立並測試包含資料匯入管線與搜尋管線的工作流程。使用 UI 編輯器建立工作流程，可簡化包含 ML 推論處理器的人工智慧與機器學習 (AI/ML) 使用案例的建立，例如向量搜尋與檢索增強生成 (RAG)。

如需各種可用 AI 搜尋類型（包括語意搜尋、混合搜尋、RAG 與多模態搜尋）的範例組態，請參閱[設定 AI 搜尋類型]({{site.url}}{{site.baseurl}}/vector-search/ai-search/building-flows/)。

如需設定代理式搜尋流程的範例，請參閱[設定代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/building-agentic-search-flows/)。

工作流程完成後，您可以將其匯出為[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)，以便在多個叢集之間重建相同的資源。

## 必備知識

[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)與[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)可在 OpenSearch 匯入與搜尋作業的不同階段轉換資料。_資料匯入管線_由一連串的[_資料匯入處理器_]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)組成，而_搜尋管線_則由[_搜尋請求處理器_]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors#search-request-processors)及/或[_搜尋回應處理器_]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors#search-response-processors)組成。您可以組合這些處理器，建立符合您資料處理需求的自訂管線。

這些管線在三個關鍵階段修改資料：

1. **匯入**：在文件匯入索引之前轉換文件。
2. **搜尋請求**：在執行搜尋之前轉換搜尋請求。
3. **搜尋回應**：在執行搜尋之後、傳回回應之前，轉換搜尋回應（包括結果中的文件）。

在 OpenSearch 中，您可以[整合託管於第三方平台的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)，並直接在 OpenSearch 中使用其推論功能。資料匯入管線與搜尋管線都提供 [ML 推論處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)，讓您在匯入與搜尋期間於管線中使用外部託管的模型進行推論。

<!-- vale off -->

## 存取 AI Search Flows

<!-- vale on -->

若要存取 AI Search Flows，請前往 **OpenSearch Dashboards**，並從頂端選單選取 **OpenSearch Plugins** > **AI Search Flows**。

## 預設範本

在首頁上，選取 **New workflow** 標籤，或選取右側的 **Create workflow** 按鈕。這會開啟一系列為不同使用案例設計的預設範本，每個範本都有一組獨特的預先設定的資料匯入與搜尋處理器。這些範本有兩個主要用途：

- **快速測試 AI/ML 解決方案**：如果您部署的模型具有已定義的介面，只需幾次點擊即可在叢集中設定基本解決方案。如需更多資訊，請參閱[範例：使用 RAG 的語意搜尋](#example-semantic-search-with-rag)。
- **自訂/進階解決方案的起點**：每個範本都為建立自訂解決方案提供結構化的起點。您可以修改並擴充這些範本，以符合您的特定需求。

## 工作流程編輯器

您可以在工作流程編輯器中建立並測試您的資料匯入與搜尋工作流程，如下圖所示。

![工作流程編輯器]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/details-page.png)

工作流程編輯器的組織方式類似整合式開發環境 (IDE)，包含三個主要元件：

- **Flow overview**：可摺疊的導覽面板，用於選取資料匯入與搜尋流程中的不同元件。在此面板中，您可以新增、移除或重新排序處理器。如果您已有已填入資料的索引，且只需要搜尋流程，可以停用 **Ingest flow**。
- **Component details**：用於設定個別元件詳細資訊的中央面板。從 **Flow overview** 選取元件後，此面板會填入相關的詳細資訊。
- **Inspect**：用於與工作流程互動的一組標籤。
  - **Test flow**：讓您執行搜尋流程（可含或不含搜尋管線），並以表格或原始 JSON 格式檢視結果。
  - **Ingest response**：顯示更新資料匯入流程後的 API 回應。
  - **Errors**：顯示更新、匯入作業或搜尋的最新錯誤。發生新錯誤時，此標籤會自動開啟。
  - **Resources**：列出與工作流程相關聯的 OpenSearch 資源，包括最多一個資料匯入管線、一個索引與一個搜尋管線。若要檢視資源詳細資訊，請選取 **Inspect**。
  - **Preview**：資料如何在您的資料匯入與搜尋流程中流動的唯讀視覺化。當您對流程進行變更時，此檢視會自動更新。您也可以切換至 **JSON** 標籤，檢視底層的範本組態。

## 範例：使用 RAG 的語意搜尋

下列範例使用已部署的 [Titan Text Embedding](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) 模型與[託管於 Amazon Bedrock 的 Anthropic Claude 模型](https://aws.amazon.com/bedrock/claude/)，建立用於執行向量搜尋與 RAG 的[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)、[索引]({{site.url}}{{site.baseurl}}/getting-started/intro/#index)與[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。

我們強烈建議使用具有完整模型介面的模型。如需範例組態清單，請參閱[模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md)。
{: .note}

1. 在 **Workflows** 頁面上，選取 **New workflow** 標籤，如下圖所示。
   ![新增工作流程頁面]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/new-workflow-page.png)
2. 在 **RAG with Vector Retrieval** 範本中，選取 **Create**。
3. 提供一些基本詳細資訊，如下圖所示：

   - 唯一的工作流程名稱與描述
   - 用於產生向量嵌入的嵌入模型
   - 用於執行 RAG 的大型語言模型 (LLM)
     ![快速設定強制回應視窗]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/quick-configure-modal.png)

   如需其他選項（例如將保存在索引中的文字欄位與向量欄位名稱），請選取 **Optional configuration**。您可以隨時更新這些設定。

4. 選取 **Create** 以預先填入組態，並自動導覽至 **Workflow Details** 頁面，您可以在該頁面設定資料匯入流程。
5. 若要提供範例資料，請從 **Flow overview** 選取 **Sample data**，然後選取 **Import data**。您可以手動輸入資料、上傳本機 `.jsonl` 檔案，或從現有索引擷取範例文件，如下圖所示。
   ![匯入資料強制回應視窗]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/import-data-modal.png)

   此表單預期資料採用 [JSON Lines 格式](https://jsonlines.org/)，每一行代表一個獨立的[文件]({{site.url}}{{site.baseurl}}/getting-started/intro/#document)。此程序類似於[大量匯入作業]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/#bulk-indexing)。完成後，選取 **Confirm**。

6. 在 **Flow overview** 面板中，選取最上層的 **ML Inference Processor**。此處理器已預先填入用於將資料對應_至_預期模型輸入以及_從_預期模型輸出對應的組態。**Inputs** 區段將目標文件欄位對應至模型輸入欄位，為該欄位產生向量嵌入。**Outputs** 區段將模型輸出欄位對應至儲存在索引中的新欄位，如下圖所示。
   ![轉換資料]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/transform-data.png)

   如需可處理複雜資料結構描述與模型介面的轉換類型的更多資訊，請參閱[進階資料轉換](#advanced-data-transformations)。

7. 在 **Flow overview** 面板中，選取 **Index**。索引已預先填入所選使用案例所需的索引組態。例如，對於向量搜尋，`my_embedding` 欄位會對應為 `knn_vector`，且索引會指定為向量索引 (`index.knn: true`)，如下圖所示。您可以視需要修改此組態。
   ![匯入資料]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/ingest-data.png)
8. 選取 **Flow overview** 底部的 **Update ingest flow**，以建立已設定的資料匯入管線與索引，並匯入提供的範例資料。然後前往 **Inspect** 下的 **Test flow**，搜尋新建立的索引，並確認轉換後的文件如預期顯示。在此範例中，請確認每個匯入的文件都已產生向量嵌入，如下圖所示。
   ![測試資料匯入流程]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/ingest-test-flow.png)
9. 若要設定搜尋流程，請在 **Flow overview** > **Transform query** 下選取 **ML Inference Processor**，如下圖所示。此處理器會剖析您要為其產生向量嵌入的搜尋查詢輸入。在此範例中，它會將 `query.match.review.query` 的值傳遞給嵌入模型。<br>
   ![轉換查詢]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/transform-query.png)

   此處理器也會執行查詢改寫，使用模型產生的向量嵌入來產生 `knn` 查詢。選取 **Rewrite query** 以檢視其詳細資訊，如下圖所示。這種做法將複雜的查詢細節抽象化，提供一個使用搜尋管線執行進階查詢產生的簡單查詢介面。

   ![改寫查詢]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/rewrite-query.png)

10. 若要設定搜尋結果轉換，請在 **Flow overview** > **Transform response** 底下選取 **ML Inference Processor**，如下圖所示。Claude LLM 用於處理傳回的結果並產生人類可讀的回應。
    ![轉換回應]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/transform-response.png)<br>
    在 **Inputs** 底下，選取 `prompt` 項目旁的鉛筆圖示。這會開啟一個彈出式視窗，其中包含預先設定的提示範本，用於摘要傳回的文件，如下圖所示。您可以視需要修改此範本；有數個預設集可作為起點。您也可以新增、更新或移除 **Input variables**，其中包含您想以情境資訊形式動態注入 LLM 的傳回文件資料。預設選項會收集所有 `review` 資料並摘要結果。選取 **Save** 以套用您的變更。
    ![設定提示]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/configure-prompt.png)
11. 若要建置搜尋管線，請選取 **Create search flow**。**Inspect** 區段會自動導覽至 **Test flow** 元件，您可以在其中測試不同的查詢並執行搜尋，如下圖所示。您可以使用以 {% raw %}`{{ }}`{% endraw %} 包住的變數，快速測試不同的查詢值，而無須修改基礎查詢。
    ![測試搜尋流程]({{site.url}}{{site.baseurl}}/images/dashboards-flow-framework/search-test-flow.png)
12. 若要檢視搜尋結果，請選取 **Run test**。您可以將結果檢視為格式化後的命中清單，或原始 JSON 搜尋回應。
13. 視您的使用案例而定，您可以透過下列方式修改組態：

- 實驗不同的查詢參數。
- 嘗試不同的查詢。
- 在 **Transform query** 或 **Transform results** 底下修改現有的處理器。
- 在 **Transform query** 或 **Transform results** 底下新增或移除處理器。

14. 若要匯出您的工作流程，請選取頁首中的 **Export**。顯示的資料代表 [工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)，其中包含您所建立 OpenSearch 資源的完整組態，包括資料匯入管線、索引和搜尋管線。您可以選取右側的按鈕，以 JSON 或 YAML 格式下載範本。若要在其他 OpenSearch 叢集中建置相同的資源，請使用 [Provision Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/provision-workflow/)。

## 進階資料轉換

ML 推論處理器提供數種彈性的方式，將輸入資料轉換_為_模型輸入，以及_從_模型輸出轉換。

在 **Inputs** 中，您可以設定傳_至_模型的參數。輸入參數轉換類型有四種：

1. **Data field**：使用現有的資料欄位作為模型輸入。
2. **JSONPath expression**：從 JSON 結構擷取資料，並使用 [JSONPath](https://en.wikipedia.org/wiki/JSONPath) 將擷取的資料對應至模型輸入欄位。
3. **Prompt**：使用可包含動態變數的常數值。這結合了 `Custom string` 轉換以及 `Data field` 和 `JSONPath expression` 轉換的元素，對於為 LLM 建置提示特別實用。
4. **Custom string**：使用常數字串值。

在 **Outputs** 中，您可以設定傳_自_模型的值。輸出參數轉換類型有三種：

1. **Data field**：將模型輸出複製到新的文件欄位。
2. **JSONPath Expression**：從 JSON 結構擷取資料，並使用 [JSONPath](https://en.wikipedia.org/wiki/JSONPath) 將擷取的資料對應至一或多個新的文件欄位。
3. **No transformation**：不轉換模型輸出欄位，保留其名稱和值。

## 後續步驟

- 如需建議搭配 AI Search Flows 使用的模型和模型介面，請參閱 [模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md)。

- 如需不同 AI/ML 使用案例的範例組態，請參閱 [設定 AI 搜尋類型]({{site.url}}{{site.baseurl}}/tutorials/ai-search-flows/building-flows/)。

- 如需設定代理式搜尋流程的範例，請參閱 [設定代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/building-agentic-search-flows/)。
