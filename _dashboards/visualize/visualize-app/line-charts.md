---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "折線圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 100
redirect_from:
  - /dashboards/visualize/line-charts/
---

# 折線圖

折線圖將 Y 軸上的一個或多個數值資料點序列，對照 X 軸上的數值欄位繪製出來。資料點可以用線連接。X 軸的值可以是時間軸，或任何其他連續或離散的數值序列。

## 何時使用折線圖

使用折線圖呈現隨時間或任何連續數值量變化的趨勢、週期性行為、變化率資訊及轉折點。使用多條線呈現指標之間的相關性。

## 建立折線圖

本頁範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立折線圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Line**，然後選取您的索引模式（例如，**opensearch_dashboards_sample_data_flights**）。
2. 在 **Metrics** 下，展開 **Y-axis Count**。
3. 將 **Aggregation** 設為 **Average**，並將 **Field** 設為 **AvgTicketPrice**。
4. （選用）輸入 **Custom label**，例如 `Average Ticket Price`。
5. 選取 **Update**。

   圖表會顯示一個高度略高於 `$600` 的長條，代表航班資料庫中所有文件的平均票價。

   如果您的視覺化顯示不同的值，請確認您的時間篩選範圍夠大，足以涵蓋所有航班範例資料。
   {: .note}

6. 在 **Buckets** 下，選取 **Add** > **X-axis**。
7. 將 **Aggregation** 設為 **Histogram**，並將 **Field** 設為 **DistanceKilometers**。
8. 選取 **Update**。

   圖表會顯示平均票價隨分桶後的飛行距離變化的情形。

### 新增分割序列

1. 在 **Buckets** 下，選取 **Add** > **Split series**。
2. 將 **Sub aggregation** 設為 **Terms**、**Field** 設為 **dayOfWeek**、**Order by** 設為 **Alphabetical**，並將 **Size** 設為 `7`。
3. 選取 **Update**。

   平均票價會依星期值，以七條不同的線顯示，如下圖所示。在大多數飛行距離中，星期值鍵為 5 和 6 的平均票價明顯較高。

   ![顯示依星期區分的平均票價與距離比較的折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-line-cost-vs-distance.png)

## 設定折線圖

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Metrics & axes 分頁

| 設定 | 說明 |
| :--- | :--- |
| **Chart type** | 可針對各序列覆寫。支援 **Line**、**Area**、**Bar**。 |
| **Mode** | **Normal** 會讓線條重疊。與區域圖／長條圖類型結合時，可使用 **Stacked**。 |
| **Line mode** | **Straight**、**Smoothed** 或 **Stepped**。 |
| **Y-axis scale** | **Linear**、**Log** 或 **Square root**。 |

## 後續步驟

- 若要選擇不同的視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
