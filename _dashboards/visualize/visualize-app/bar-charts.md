---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "長條圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 40
redirect_from:
  - /dashboards/visualize/bar-charts/
---

# 長條圖

長條圖以成比例的長條長度來表示數值，藉此比較各類別之間的數值。時間序列資料或類別比較請使用垂直長條；當類別標籤較長或需要比較許多類別時，請使用水平長條。

## 何時使用長條圖

使用長條圖可以呈現隨某個自變數而產生的變化、各類別之間的效能比較，以及隨時間變化的趨勢。長條圖可以顯示各類別之間的效能差距、離群值、季節性模式及比較優勢。您可以選取長條，以篩選同一儀表板上的其他視覺化。

## 建立長條圖

本頁範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立長條圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Vertical Bar**（或 **Horizontal Bar**），然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。
2. 在 **Metrics** 下，展開 **Y-axis Count**。
3. 將 **Aggregation** 設為 **Average**，並將 **Field** 設為 **FlightDelayMin**。
4. （選用）輸入 **Custom label**，例如 `Flight delay in minutes`。
5. 選取 **Update**。

   圖表會顯示單一長條，高度約為 `47`，即航班資料庫中所有文件的平均航班延誤時間。

   如果您的視覺化顯示不同的數值，請確認您的時間篩選範圍夠大，足以涵蓋所有範例航班資料。
   {: .note}

6. 在 **Buckets** 下，選取 **Add** > **X-axis**。
7. 將 **Aggregation** 設為 **Terms**，並將 **Field** 設為 **OriginWeather**。
8. 將 **Order by** 設為 `Metric: FlightDelayMin`，將 **Order** 設為 **Descending**，並將 **Size** 設為 `8`。

   任何大於或等於 8 的數字都會顯示所有可用的 `OriginWeather` 詞彙。
   {: .note}

9. 選取 **Update**。

   圖表會顯示航班出發地每種天氣類型的平均延誤時間。平均延誤時間最長的是 `Damaging Wind`，如下圖所示。

   ![依出發地天氣顯示平均航班延誤時間的長條圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-bar-chart-flight-delay.png)

## 設定長條圖

長條圖與其他以彙總為基礎的視覺化共用相同的組態索引標籤。如需各索引標籤的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Data 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Metrics** | 定義 Y 軸數值。支援所有標準彙總（Count、Average、Sum、Min、Max、Unique Count、Median、Percentiles 等）。 |
| **Buckets > X-axis** | 沿水平軸將長條分組。類別資料請使用 **Terms**，時間型資料請使用 **Date Histogram**，數值範圍請使用 **Histogram**。 |
| **Buckets > Split series** | 依欄位的值，將每個長條分割為分組或堆疊的子長條。 |
| **Buckets > Split chart** | 為每個桶 (bucket) 值建立個別的圖表面板（小型多圖）。 |

### Metrics & axes 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Chart type** | 依序列覆寫圖表類型。支援 **Line**、**Area**、**Bar**。 |
| **Mode** | **Stacked** 會將長條上下堆疊。**Normal** 會將長條並排分組。 |
| **Y-axis position** | **Left** 或 **Right**。 |
| **Y-axis scale** | **Linear**、**Log** 或 **Square root**。 |

### Panel settings 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Legend position** | **Top**、**Left**、**Right**、**Bottom**。 |
| **Show tooltip** | 滑鼠游標停留時顯示數值。 |
| **Order buckets by sum** | 依總值排序分割序列。 |
| **Show threshold line** | 在指定的數值處繪製一條水平參考線。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
