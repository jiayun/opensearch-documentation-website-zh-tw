---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "目標視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 80
redirect_from:
  - /dashboards/visualize/goal/
---

# 目標視覺化

目標視覺化會以類似速度表的儀表顯示數值。它會將數值顯示為預先定義目標的比例。此視覺化也會顯示指標，可以是絕對值，也可以是目標的百分比。此視覺化可以顯示單一數值或多個分桶的數值。若進行分桶，所有桶 (bucket) 的目標都相同。

## 何時使用目標視覺化

使用目標視覺化，可依據目標值監控關鍵指標。

## 建立目標視覺化

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立目標視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Goal**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   視覺化會顯示一個儀表，將文件計數顯示為預設目標 `10,000` 的百分比。對於 `opensearch_dashboards_sample_data_flights` 資料，若日期範圍包含所有文件，此值為 `130.59%`。
   {: .note}

2. 在 **Metrics** 下，展開 **Metric count**。
3. 將 **Aggregation** 設為 **Sum**，並將 **Field** 設為 **DistanceKilometers**。
4. 若要查看資料集距離記錄總計一億公里還有多遠，請將 100,000,000 設為目標：

   1. 選取 **Options** 索引標籤。
   2. 在 **Ranges** 方塊中，輸入 `1e8` 作為範圍上限。

      數值輸入不可使用千分位分隔符號。對於大數值，請使用指數表示法。
      {: .note}

   3. 取消選取 **Percentage mode**。
   4. 選取 **Update**。

   視覺化會顯示 `92,616,288.34`，即所有航班距離的總和（以公里為單位）。此值約佔儀表最大值的 93%，而儀表最大值已依目標校準，如下圖所示。

   ![顯示總航班距離朝 1 億公里目標進展的目標視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/example-goal-total-km.png)

5. （選用）依照[儀表視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/gauge/)中的說明新增刻度，以結合儀表與目標顯示。

## 設定目標視覺化

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Ranges** | 定義目標範圍。最大值代表目標。 |
| **Percentage mode** | 啟用時，會將數值顯示為目標的百分比。 |
| **Show scale** | 啟用時，會在進度列上顯示刻度標記。 |
| **Color options** | 控制指派給各範圍區段的色彩。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
