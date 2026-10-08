---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "熱度圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 90
redirect_from:
  - /dashboards/visualize/heat-map/
---

# 熱度圖

熱度圖會在二維網格上以顏色或飽和度漸層來呈現數值，實際上形成三維的資料顯示。X 與 Y 維度可以相同（例如空間熱度圖），也可以不同。例如，在某地點的平均氣溫紀錄中，以月份對應年份，藉此區分該地點的週期性資料與趨勢資料。

## 何時使用熱度圖

使用熱度圖可以揭示多維度資料集中的叢集、相關性強度與異常。它們能讓在表格格式或多個二維圖表中難以察覺的模式變得清晰可見。

## 建立熱度圖

本頁範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立熱度圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Heat Map**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。
2. 在 **Metrics** 下，展開 **Value Count**，並將 **Aggregation** 設為 **Count**。
3. 在 **Buckets** 下，選取 **Add** > **X-axis**。
4. 將 **Aggregation** 設為 **Terms**、**Field** 設為 **OriginWeather**，並將 **Size** 設為 `8`。
5. 選取 **Update**。
6. 在 **Buckets** 下，選取 **Add** > **Y-axis**。
7. 將 **Sub aggregation** 設為 **Terms**、**Field** 設為 **DestWeather**，並將 **Size** 設為 `8`。
8. 選取 **Update**。

### 自訂顯示

1. 選取 **Options** 索引標籤。
2. 在 **Heatmap settings** 中，將 **Color schema** 設為 **Greys**，並將 **Number of colors** 設為 `8`。
3. 在 **Labels** 中，啟用 **Show labels**。
4. 選取 **Update**。

   熱度圖會顯示對應至起飛與目的地天氣組合的平均航班延誤，如下圖所示。

   ![依天氣狀況顯示航班延誤的熱度圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-heatmap-flight-delay.png)

   請注意以下幾點：
   - 熱度圖資料分為四個象限，對應目的地與起飛地「良好」（Cloudy、Rain、Clear、Sunny）與「惡劣」（Hail、Heavy Fog、Damaging Wind、Thunder & Lightning）天氣狀況的四種組合。
   - 當起飛地與目的地天氣皆良好時，延誤時間最長；當兩地天氣皆惡劣時，延誤時間最短。

### 使用分割圖表進行篩選

您可以使用[篩選工具]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/)篩選資料，但如果視覺化位於儀表板中，此操作也會篩選其他視覺化的資料。下列程序只會限制此視覺化的資料。
{: .note}

若要將熱度圖限制為特定條件（例如僅限已取消的航班）：

1. 在 **Buckets** 下，選取 **Add** > **Split chart** > **Rows**。
2. 將 **Sub aggregation** 設為 **Filters**。
3. 在 **Filter 1** 方塊中，輸入 `Cancelled: true`。

   篩選詞彙會區分大小寫。
   {: .tip}

4. 選取 **Update**。

   熱度圖現在僅顯示已取消的航班。結果顯示，當航班兩端的天氣皆良好時，未發生任何取消情況，如下圖所示。

   ![依天氣狀況顯示已取消航班的熱度圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-heatmap-cancellation.png)

## 設定熱度圖

如需一般視覺化組態的資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Color schema** | 熱度圖的色盤（例如 **Greens**、**Blues**、**Greys**、**Yellow to Orange**）。 |
| **Reverse schema** | 反轉顏色對應。 |
| **Number of colors** | 離散顏色區間的數量。 |
| **Show labels** | 在每個儲存格內顯示數值。 |
| **Percentage mode** | 將數值正規化為 0 到 1 之間。 |

## 後續步驟

- 若要選擇不同的視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
