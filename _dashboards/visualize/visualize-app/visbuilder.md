---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: VisBuilder
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 190
redirect_from:
  - /dashboards/visualize/visbuilder/
  - /dashboards/drag-drop-wizard/
---

# VisBuilder

VisBuilder 讓您在 OpenSearch Dashboards 中以拖放方式建立視覺化。使用 VisBuilder，您可以：

* 立即檢視資料，不需要預先選取視覺化輸出。
* 靈活且快速地變更視覺化類型與索引模式。
* 輕鬆在多個畫面之間切換。

## 何時使用 VisBuilder

VisBuilder 透過直覺的拖放介面，讓您快速探索資料之間的關係。您不需要具備查詢語言知識，就能縮短驗證假設與探索資料模式所需的時間。

## 使用 VisBuilder 建立視覺化

本頁範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要使用 VisBuilder 建立視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **VisBuilder**，如下圖所示。

   ![VisBuilder 新視覺化起始頁面]({{site.url}}{{site.baseurl}}/images/dashboards/vis-builder-2.png)
2. 從 **Data Source** 下拉式選單中，選取 **opensearch_dashboards_sample_data_flights**。
3. 在 **Configuration** 面板中，將欄位從左側的欄位清單拖曳到圖表上，或選取各區段中的 **+** 圖示，將欄位新增至圖表：
   - **Y-axis**：選取 **+** 圖示，將 **Aggregation** 設為 **Average**，並將 **Field** 設為 **AvgTicketPrice**。
   - **X-axis**：選取 **+** 圖示，將 **Aggregation** 設為 **Terms**，將 **Field** 設為 **Carrier**，並將 **Order** 設為 **Descending**。
   - **Split series**：選取 **+** 圖示，將 **Aggregation** 設為 **Terms**，並將 **Field** 設為 **FlightDelay**。

圖表會在您新增欄位時自動更新。**Split series** 欄位會將每個長條分成以顏色區分的子群組。在此範例中，`FlightDelay` 有兩個值（`true` 與 `false`），因此每家航空公司會以不同顏色顯示兩個長條：一個代表延誤的航班，另一個代表未延誤的航班，如下圖所示。

![VisBuilder 長條圖，顯示各航空公司的平均票價，並依航班延誤狀態分組]({{site.url}}{{site.baseurl}}/images/dashboards/visbuilder-example.png)

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
