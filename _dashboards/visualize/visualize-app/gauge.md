---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儀表視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 70
redirect_from:
  - /dashboards/visualize/gauge/
---

# 儀表視覺化

儀表視覺化會以類似速度表的模擬類比儀器來顯示資料欄位。儀表值可以立即與標示的範圍或閾值進行比較。此視覺化可以顯示單一值，或多個分桶後的值。

## 何時使用儀表視覺化

使用儀表視覺化，可在儀表板中監控關鍵指標是否處於可接受的範圍內。

## 建立儀表視覺化

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立儀表視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Gauge**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   此視覺化會顯示一個儀表，呈現索引模式中的文件數量。對於 `opensearch_dashboards_sample_data_flights` 資料，若日期範圍包含所有文件，此值為 `13059`。
   {: .note}

2. 在 **Metrics** 下，展開 **Metric count**。
3. 將 **Aggregation** 設定為 **Median**，並將 **Field** 設定為 **FlightTimeMin**。
4. 選取 **Update**。

   儀表會顯示 `502.775`，並以儀表的完整範圍呈現。

   如果您的視覺化顯示不同的值，請確認您的[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)時間範圍夠大，足以涵蓋所有範例航班資料。
   {: .note}

5. 現在您已大致了解資料的量級，請變更顯示範圍，讓顯示的值落在範圍內。

   1. 選取 **Options** 索引標籤。
   2. 在 **Ranges** 面板中，依下列方式編輯三個預設範圍：

      | 起始 | 結束 |
      | :--- | :--- |
      | 0 | 250 |
      | 250 | 500 |
      | 500 | 750 |

   3. 選取 **Update**。

6. 若要在單一視覺化中比較兩種不同的情況，請將資料分桶。

   1. 在 **Buckets** 下，選取 **Add** > **Split group**。
   2. 將 **Aggregation** 設定為 **Terms**，並將 **Field** 設定為 **FlightDelay**。
   3. 選取 **Update**。

   此視覺化會顯示兩個儀表，分別呈現延誤與未延誤航班的飛行時間中位數，如下圖所示。

   ![依延誤狀態分割的飛行時間中位數儀表]({{site.url}}{{site.baseurl}}/images/dashboards/example-gauge-flight-time.png)

## 設定儀表視覺化

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Ranges** | 定義儀表弧線上以顏色區分的區段。每個範圍都有起始值和結束值。 |
| **Percentage mode** | 啟用時，會將值顯示為最大範圍值的百分比。 |
| **Show scale** | 啟用時，會在儀表上顯示刻度。 |
| **Color options** | 控制指派給每個範圍區段的顏色。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
