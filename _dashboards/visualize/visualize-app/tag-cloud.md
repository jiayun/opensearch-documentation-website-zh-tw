---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "標籤雲"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 150
redirect_from:
  - /dashboards/visualize/tag-cloud/
---

# 標籤雲

標籤雲會顯示資料中的一組文字欄位（桶 (bucket) 標籤，在視覺化中稱為_標籤_）。每個標籤的字型大小對應資料中該桶的量值。例如，如果視覺化指定 `Average`，則標籤雲中標籤的字型大小會與分桶欄位的平均值成正比。

您可以將標籤雲視為一種反向顯示方式：它對應分桶後的值，以桶標籤的大小來呈現這些值，而不是以圖表數量（例如長條的長度）來呈現。

## 何時使用標籤雲

使用標籤雲可以醒目地比較不同文字標籤桶的量值。

## 建立標籤雲

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立標籤雲，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Tag Cloud**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。

   由於資料尚未分桶，視覺化窗格會以大字顯示 `all`。預設情況下，標籤大小與文件數量成正比，但沒有其他詞彙可與其大小相比較。
   {: .note}

2. 在 **Metrics** 下，展開 **Tag size count**。
3. 將 **Aggregation** 設定為 **Unique Count**，並將 **Field** 設定為 **DestLocation**。
4. （選用）輸入 **Custom label**，例如 `Destinations Served`。
5. 選取 **Update**。

   視覺化不會改變。標籤雲仍然只有一個項目 `all`，因為資料尚未分桶。

6. 在 **Buckets** 下，選取 **Add** > **Tags**。
7. 將 **Aggregation** 設定為 **Terms**，並將 **Field** 設定為 **Carrier**。
8. 選取 **Update**。

   標籤雲會依不重複目的地的數量決定每個航空公司的大小並加以顯示，如下圖所示。

   ![依不重複目的地數量決定航空公司大小的標籤雲]({{site.url}}{{site.baseurl}}/images/dashboards/example-tagcloud-carrier-destinations.png)

## 設定標籤雲

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
