---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "圓餅圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 130
redirect_from:
  - /dashboards/visualize/pie-charts/
---

# 圓餅圖

圓餅圖會顯示每個條件在資料欄位總計數中所佔的百分比。此視覺化可以顯示單一值，或多個依桶 (bucket) 分組的值。

## 何時使用圓餅圖

使用圓餅圖來比較構成某項指標的各個條件所佔的相對比例。您可以選取圓餅區塊，以篩選同一個儀表板上的其他視覺化。

## 建立圓餅圖

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立圓餅圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Pie**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   此視覺化會顯示僅呈現單一值的環狀（圓環）圓餅圖。工具提示會顯示該值，也就是索引模式中的文件數量。對於 `opensearch_dashboards_sample_data_flights` 資料，如果日期範圍涵蓋所有文件，此值為 `13059`。
   {: .note}

   如果您的視覺化顯示不同的值，請確認您的[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)時間範圍夠大，足以涵蓋所有範例航班資料。
   {: .note}

2. 在 **Metrics** 下，展開 **Slice size count**。
3. 將 **Aggregation** 設為 **Unique Count**，並將 **Field** 設為 **FlightNum**。

   對於圓餅圖，指標中各桶的值加總必須為 100%。只會顯示具有此特性的彙總。

4. 選取 **Update**。

   圓餅圖會顯示 `12,932`，並以單一值的環狀圓餅圖呈現。

5. 若要依不同條件將欄位的組成視覺化，請將資料分桶：

   1. 在 **Buckets** 下，選取 **Add** > **Split slices**。
   2. 將 **Aggregation** 設為 **Terms**、**Field** 設為 **OriginCountry**，並將 **Size** 設為 `5`。
   3. 選取 **Group other values in separate bucket**，以準確呈現不重複航班的總數。
   4. 選取 **Update**。

   此視覺化顯示義大利和美國是出發航班最多的國家。前五名國家約佔不重複航班號碼的將近一半。

6. （選用）將視覺化顯示為傳統圓餅圖，而非環狀圓餅圖：

   1. 選取 **Options** 索引標籤。
   2. 在 Pie 設定面板中，取消選取 **Donut**。
   3. 選取 **Update**。

   此視覺化會顯示前五名國家的扇形圓餅圖，其他所有國家則歸為一組，如下圖所示。

   ![依出發國家顯示不重複航班的圓餅圖]({{site.url}}{{site.baseurl}}/images/dashboards/example-pie-unique-flights.png)

## 設定圓餅圖

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Donut** | 啟用時，會將圖表呈現為圓環（甜甜圈），而非實心圓。 |
| **Show labels** | 在每個區塊上顯示類別標籤。 |
| **Show top level only** | 當存在巢狀桶 (bucket) 時，僅顯示最外圈的圓環。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
