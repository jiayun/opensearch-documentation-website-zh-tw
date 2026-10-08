---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立以彙總為基礎的視覺化"
parent: Creating visualizations in the Visualize application
grand_parent: Building data visualizations
nav_order: 10
---

# 建立以彙總為基礎的視覺化

[彙總]({{site.url}}{{site.baseurl}}/aggregations/)是 OpenSearch Dashboards 中大多數視覺化背後的分析引擎。彙總會計算統計值（指標），並將資料分組為類別（桶），讓結果能以圖表、表格和地圖呈現。當您在 **Visualize** 應用程式中設定視覺化時，OpenSearch Dashboards 會自動將您的選擇轉換為彙總查詢。

下列視覺化類型使用彙總：**Area**、**Horizontal Bar**、**Vertical Bar**、**Coordinate Map**、**Data Table**、**Gauge**、**Goal**、**Heat Map**、**Line**、**Metric**、**Pie**、**Region Map** 和 **Tag Cloud**。

如需可用指標和桶的完整清單，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/#data-tab)。

在本教學中，您將使用範例航班資料建立 Vertical Bar 視覺化，並學習如何使用指標彙總、桶彙總、分割序列、百分位數、管線彙總和 top hits。

## 先決條件

本頁的範例使用 **Sample flight data** 資料集。如果您尚未新增範例資料，請參閱[準備您的資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 範例 1：一段時間內的航班數

此範例使用預設的 **Count** 指標搭配 **Date Histogram** 桶，以顯示每個時間間隔的航班數。

若要建立航班數視覺化，請依照下列步驟操作：

1. 在左側導覽選單中，選取 **OpenSearch Dashboards** > **Visualize**。
1. 選取 **Create visualization**。
1. 選取 **Vertical Bar**，然後選取 **opensearch_dashboards_sample_data_flights** 作為來源。
1. 將時間篩選器設為 **Last 7 days**。
1. 在 **Buckets** 面板中，選取 **Add** > **X-axis**。
1. 從 **Aggregation** 下拉式清單中，選取 **Date Histogram**。
1. 確認 **Field** 已設為 **timestamp**。
1. 選取 **Update**。

圖表會顯示每 3 小時間隔的航班數。Y 軸顯示 **Count**，也就是每個時間桶中的文件（航班）數量。由於 **Count** 是預設指標，因此不需要選取欄位。

![使用 Count 指標和 Date Histogram 桶的一段時間內航班數]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-count-date-histogram.png)

## 範例 2：一段時間內的平均票價

此範例將 Count 替換為 **Average** 指標，以顯示票價隨時間的變化。

若要將指標變更為 **Average**，請依照下列步驟操作：

1. 在 **Metrics** 面板中，選取 **Y-axis** 區段。
1. 從 **Aggregation** 下拉式清單中，選取 **Average**。
1. 從 **Field** 下拉式清單中，選取 **AvgTicketPrice**。
1. 選取 **Update**。

Y 軸現在顯示金額，而非文件數。每個長條代表該時間間隔內所有航班的平均票價。

![一段時間內的平均票價]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-avg-ticket-price.png)

## 範例 3：依航空公司區分的航班數

此範例新增 **Split series** 桶，以依航空公司細分 **Count** 指標。

若要依航空公司分割序列，請依照下列步驟操作：

1. 在 **Metrics** 面板中，將 **Aggregation** 改回 **Count**。
1. 在 **Buckets** 面板中，選取 **Add** > **Split series**。
1. 從 **Aggregation** 下拉式清單中，選取 **Terms**。
1. 從 **Field** 下拉式清單中，選取 **Carrier**。
1. 選取 **Update**。

圖表現在會顯示堆疊長條，每種顏色代表不同的航空公司。圖例會標示每家航空公司。此組態會建立巢狀彙總：**Date Histogram** 將航班分組到時間桶中，而 **Terms** 彙總則依航空公司細分每個桶。

![依航空公司分割的航班數]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-split-series-carrier.png)

## 範例 4：一段時間內的票價百分位數

此範例使用 **Percentiles** 指標，顯示各時間間隔的票價分布。與 **Average**（傳回單一值）不同，**Percentiles** 會傳回多個值，每個您設定的百分位數各一個。

若要建立 **Percentiles** 視覺化，請依照下列步驟操作：

1. 在 **Metrics** 面板中，選取 **Y-axis** 區段。
1. 從 **Aggregation** 下拉式清單中，選取 **Percentiles**。
1. 從 **Field** 下拉式清單中，選取 **AvgTicketPrice**。
1. 在 **Percents** 區段中，移除預設值並輸入 `25`、`50` 和 `75`（四分位距）。使用每個值旁的刪除圖示將其移除，並選取 **Add percent** 新增值。
1. 在 **Buckets** 面板中，確認 **X-axis** 已設為使用 **timestamp** 欄位的 **Date Histogram**。
1. 選取 **Update**。

圖表會顯示三個堆疊序列，每個百分位數各一個。第 50 百分位數（中位數）顯示中間值，而第 25 與第 75 百分位數之間的差距則顯示每個時間桶中票價的分散程度。

![一段時間內的票價百分位數]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-percentiles.png)

## 範例 5：累計航班數

此範例使用 **Cumulative Sum** 管線彙總來顯示航班的累計總數。管線彙總是對另一個指標的輸出進行運算，而不是直接對文件欄位運算。

若要在視覺化中新增累計總和，請依照下列步驟操作：

1. 在 **Metrics** 面板中，確認第一個 Y 軸已設為 **Count**。
1. 選取 **Add** 以建立第二個指標。
1. 在 **Aggregation** 下拉式清單中，向下捲動至 **Parent Pipeline Aggregations** 並選取 **Cumulative Sum**。
1. 在 **Metric** 下拉式清單中，選取 **Custom metric**。
1. 在出現的巢狀 **Aggregation** 下拉式清單中，選取 **Count**。
1. 在 **Buckets** 面板中，確認 **X-axis** 已設為使用 **timestamp** 欄位的 **Date Histogram**。
1. 選取 **Update**。

圖表會以底部的長條顯示每個間隔的 **Count**，並以上升的折線顯示 **Cumulative Sum**。折線顯示隨時間累積的航班總數。

![累計航班數]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-cumulative-sum.png)

## 範例 6：一段時間內的最新票價

此範例使用 **Top Hit** 指標，顯示每個時間桶中的最新票價。**Top Hit** 是所有指標中組態選項最多的一個：它可讓您控制要傳回哪些文件值、傳回多少個，以及以何種順序傳回。

若要建立 **Top Hit** 視覺化，請依照下列步驟操作：

1. 在 **Metrics** 面板中，選取 **Y-axis** 區段。
1. 從 **Aggregation** 下拉式清單中，選取 **Top Hit**。
1. 從 **Field** 下拉式清單中，選取 **AvgTicketPrice**。
1. 從 **Aggregate with** 下拉式清單中，選取 **Max**（這會決定如何合併同一個桶內的多個值）。
1. 將 **Size** 設為 `1`（每個桶傳回一個值）。
1. 從 **Sort on** 下拉式清單中，選取 **timestamp**。
1. 從 **Order** 下拉式清單中，選取 **Descending**（最新的優先）。
1. 在 **Buckets** 面板中，確認 **X-axis** 已設為使用 **timestamp** 欄位的 **Date Histogram**。
1. 選取 **Update**。

圖表會顯示每個 3 小時間隔中最新（時間戳記最大）的票價。與將所有值平滑化的 **Average** 不同，**Top Hit** 會顯示單一文件的實際值，有助於追蹤每個時間範圍內的最新狀態。

![使用 Top Hit 的一段時間內最新票價]({{site.url}}{{site.baseurl}}/images/dashboards/aggregation-viz-top-hit.png)

## 後續步驟

- 若要了解所有可用的指標彙總和桶彙總，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/#data-tab)。
- 若要了解彙總在 API 中的運作方式，請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。
