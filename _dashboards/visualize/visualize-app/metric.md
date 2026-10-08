---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 120
redirect_from:
  - /dashboards/visualize/metric/
---

# 指標視覺化

指標視覺化會顯示單一資料欄位。此視覺化可以顯示單一值，或多個分桶後的值。請在儀表板上使用指標視覺化來呈現關鍵指標，尤其是經常更新的值。

## 何時使用指標視覺化

使用指標視覺化可讓人一眼掌握關鍵的業務或營運數值，尤其是需要持續監控的即時或經常更新的值，例如系統健康狀態、業務效能或營運狀態。

## 建立指標視覺化

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立指標視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Metric**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   視覺化會顯示索引模式中的文件數量。對於 `opensearch_dashboards_sample_data_flights` 資料，若日期範圍涵蓋所有文件，此數量為 `13059`。
   {: .note}

2. 在 **Metrics** 下，展開 **Metric Count**。
3. 將 **Aggregation** 設為 **Average**，並將 **Field** 設為 **DistanceKilometers**。
4. 選取 **Update**。

   視覺化會顯示 `7092.142`，即航班資料庫中所有文件的平均距離（以公里為單位）。

   如果您的視覺化顯示不同的值，請確認您的[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)時間範圍夠大，足以涵蓋所有範例航班資料。
   {: .note}

   ![顯示平均航班距離的指標視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/metric-example.png)

## 設定指標視覺化

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
