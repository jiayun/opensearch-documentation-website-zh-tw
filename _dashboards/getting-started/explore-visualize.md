---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索 Visualize 應用程式"
parent: Getting started
nav_order: 35
---

# 探索 Visualize 應用程式

**Visualize** 應用程式讓您可以使用點擊介面來建立圖表、地圖、表格以及資料的其他視覺化表示方式。

## 前置條件

本頁面的範例使用了已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中的 [**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您使用的是本機安裝的 OpenSearch Dashboards 且尚未加入範例資料，請參閱 [準備您的資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 動手試試：使用範例資料建立折線圖

請依照下列步驟，使用 **Visualize** 應用程式建立顯示航班數量隨時間變化的折線圖：

1. 在左側導覽選單中，選取 **OpenSearch Dashboards** > **Visualize**。
2. 選取 **Create visualization**。
3. 在 **New Visualization** 對話方塊中，選取 **Line**。
4. 在 **Choose a source** 對話方塊中，選取 **opensearch_dashboards_sample_data_flights**。
5. 將時間篩選條件設為 **Last 7 days**。
6. 在 **Buckets** 下，選取 **Add** > **X-axis**。
7. 將 **Aggregation** 設為 **Date Histogram**，並將 **Field** 設為 **timestamp**。
8. 選取 **Update**。圖表會顯示每個時間間隔的航班數量，如下圖所示。

   ![顯示航班數量隨時間變化的折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualize-app-line-chart-example.png)

9. 在工具列中，選取 **Save**（磁碟圖示）。

   由於 OpenSearch Playground 為唯讀，因此無法在其中儲存。
   {: .note}
10. 在 **Save visualization** 對話方塊中，輸入 `Flight count over time` 作為標題。
11. 選取 **Save**。


視覺化已儲存，並會顯示在 **Visualizations** 清單中。

## 進一步閱讀

- 如需完整的 Visualize 參考指南，請參閱 [在 Visualize 應用程式中建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)。
- 如需實作教學，請參閱 [建立以彙總為基礎的視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/aggregation-based-viz/)。

## 後續步驟

- 使用 [探索 Dashboards 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dashboards/) 將視覺化元件組合至儀表板中。