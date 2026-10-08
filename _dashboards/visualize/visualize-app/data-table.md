---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料表格"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 60
redirect_from:
  - /dashboards/visualize/data-table/
---

# 資料表格

資料表格以列與欄的形式顯示選取的欄位。您可以將一或多個指標顯示為欄，並分桶為列，再將桶資料細分為不同的表格。

## 何時使用資料表格

當您需要檢查個別文件、驗證資料品質，或調查彙總視覺化背後的細節時，請使用資料表格。您可以排序、篩選，並檢查欄位之間在較抽象的視覺化中可能不明顯的關聯性。您也可以將資料表格做為向下鑽研的目標，從高階的視覺化摘要深入到特定記錄層級的細節。

## 建立資料表格

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立資料表格，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Data Table**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   根據預設，此視覺化會選取 `Count` 做為唯一要顯示的指標。由於資料未分桶，因此會顯示文件總數。

   若未篩除任何資料，此資料集的計數為 `13,059`。如果您的視覺化顯示不同的值，請確認您的時間篩選範圍夠大，足以涵蓋所有範例航班資料。請參閱[時間篩選]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。
   {: .note}

2. 在 **Metrics** 面板中，展開 **Metric Count**。
3. 將 **Aggregation** 設為 **Average**，並將 **Field** 設為 **FlightDelayMin**。
4. （選用）輸入 **Custom label**，例如 `Flight delay in minutes`。
5. 選取 **Update**。

   表格會顯示所有資料的單一值，`47.335`。這是航班資料庫中每份文件的平均航班延誤時間，包含零分鐘的延誤。

6. 在 **Buckets** 面板中，選取 **Add** > **Split rows**。
7. 將 **Aggregation** 設為 **Terms**，並將 **Field** 設為 **FlightDelay**。
8. 選取 **Update**。

   表格顯示未延誤的航班平均延誤時間為零分鐘。非零航班延誤桶的值遠高於整體值，因為零延誤已不再計入該平均值。
   {: .note}

9. 從 **Aggregation** 下拉式清單中選擇 **Range**，並從 **Field** 下拉式清單中選擇 **DistanceMiles**，以變更列桶。
10. 設定下列範圍（第三列請選取 **Add range**）：

    | From | To |
    | :--- | :--- |
    | 0 | 4000 |
    | 4000 | 8000 |
    | 8000 | Infinity |

11. 在 **Metrics** 面板中，選取 **Add** > **Metric**，並將 **Aggregation** 設為 **Count**。

    請在 **Metrics** 面板中選取 **Add**，而非 **Buckets** 面板。
    {: .tip}

12. 選取 **Update**。

    表格會顯示每個距離範圍的平均航班延誤時間與計數，如下圖所示。

    ![顯示依距離範圍區分之航班延誤的資料表格]({{site.url}}{{site.baseurl}}/images/dashboards/example-table-flightdelay.png)

## 顯示多個欄

資料表格一律至少包含一個指標。當 **Metrics** 面板只含有一個指標時，面板不提供移除或停用該指標的選項，因此沒有指標欄就無法建立以彙總為基礎的資料表格。若要顯示多個欄，請為每個欄位新增一個桶或一個 **Top Hit** 指標。

### 為每個分組依據的欄位新增一個欄

每個 **Split rows** 桶都會為表格新增一個欄。

本範例從使用預設 **Count** 指標的新資料表格開始。如果您從先前的程序繼續操作，表格會保留 **DistanceMiles** 桶與兩個指標，因此會顯示額外的欄。
{: .note}

若要依航空公司與目的地國家將航班分組，請依照下列步驟操作：

1. 在 **Buckets** 面板中，選取 **Add** > **Split rows**。
1. 將 **Aggregation** 設為 **Terms**，並將 **Field** 設為 **Carrier**。
1. 再次選取 **Add** > **Split rows**。
1. 將 **Aggregation** 設為 **Terms**，並將 **Field** 設為 **DestCountry**。
1. 選取 **Update**。

表格會顯示三個欄：**Carrier: Descending**、**DestCountry: Descending** 以及指標欄。桶欄會以欄位名稱與桶的排序順序做為標籤。桶為巢狀結構，因此每一列會將一家航空公司與其文件中出現的其中一個目的地國家配對。

### 新增一個欄位值欄

**Top Hit** 指標會傳回直接取自文件的值，且在資料表格中除了數值欄位外，也接受字串欄位。每個 **Top Hit** 指標都會成為一個欄位值欄。若要新增各群組最近一班航班的目的地城市，請依照下列步驟操作：

1. 在 **Metrics** 面板中，選取 **Add** > **Metric**。
1. 從 **Aggregation** 下拉式清單中，選取 **Top Hit**。
1. 從 **Field** 下拉式清單中，選取 **DestCityName**。
1. 確認 **Size** 設為 `1`、**Sort on** 設為 **timestamp**，且 **Order** 設為 **Descending**。
1. 選取 **Update**。

表格現在會顯示四個欄：**Carrier: Descending**、**DestCountry: Descending**、**Count** 以及 **Last DestCityName**。每一列會回報該航空公司飛往該國家的航班數，以及其最近一班航班降落的城市，例如 `Rome` 或 `San Antonio`。若要為每個額外欄位新增一個欄，請重複這些步驟並選取不同的欄位。

**Top Hit** 會從每一列桶中的文件傳回值，因此表格仍會將文件分組。提高 **Size** 會在單一儲存格中傳回那麼多個值，但桶中的文件經常重複相同的值，因此該儲存格會列出同一個城市許多次。若要讓每份文件各自佔一列，請參閱[列出個別文件](#listing-individual-documents)。
{: .note}

## 列出個別文件

若要建立每一列為單一文件、每一欄為一個欄位的表格，請改在 **Discover** 應用程式中儲存搜尋，而非建立資料表格。Discover 會傳回文件而不進行彙總，且儲存的搜尋可與視覺化一樣，在相同的 **Add panels** 對話方塊中新增至儀表板。

若要選擇哪些欄位顯示為欄，請參閱[使用欄位選取工具]({{site.url}}{{site.baseurl}}/dashboards/discover/field-select/)。若要將儲存的搜尋放到儀表板上，請參閱[將視覺化新增至儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/adding-a-viz/#adding-a-panel-to-a-dashboard)。

## 設定資料表格

如需一般視覺化設定的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

## 後續步驟

- 若要選擇不同的視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
