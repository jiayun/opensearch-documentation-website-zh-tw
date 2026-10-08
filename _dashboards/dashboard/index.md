---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立儀表板"
nav_order: 70
has_children: true
redirect_from:
  - /dashboards/dashboard/
---

# 建立儀表板

您可以使用 OpenSearch Dashboards 中的 **Dashboards** 應用程式來建立儀表板，儀表板是一個包含多個面板的頁面，可用於顯示資料的不同檢視。

如果您是第一次使用 Dashboards 應用程式，請參閱 [探索 Dashboards 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dashboards/)，透過範例資料進行實作入門。
{: .tip}

>本文件使用以下術語：
>- _OpenSearch Dashboards_：OpenSearch 的網頁使用者介面 (UI)。
>- **Dashboards** 應用程式：OpenSearch Dashboards 中用於建立儀表板的應用程式。
>- _儀表板 (dashboard)_（小寫）：在 **Dashboards** 應用程式中建立的單一資料視覺化集合。
{: .note}

儀表板通常包含視覺化，但也可以包含搜尋。

儀表板顯示一個或多個面板，通常排列以支援業務目標，例如營運、決策支援或可觀測性。儀表板可以包含任意數量的面板，僅受限於顯示與可讀性的限制。

## 前置條件

本頁面的教學使用已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中的 [**Sample eCommerce data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您安裝了本機的 OpenSearch Dashboards 執行個體，請按照以下步驟新增範例資料：

1. 在 OpenSearch Dashboards 首頁上，選取 **Add sample data**。
2. 在 **Sample eCommerce data** 面板中，選取 **Add data**。

如需更多資訊，請參閱 [新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data).

## 導覽 Dashboards 應用程式 UI

下圖顯示了 **Dashboards** 應用程式的主要元件。

![Dashboards app default page]({{site.url}}{{site.baseurl}}/images/dashboards/dashboard-UI-blank-callouts.png)

- _應用程式選單_ (A) 包含應用程式選項。此選單具有情境感知能力，且在不同應用程式中有所不同。
- _搜尋_ 欄 (B) 可使用查詢語言搜尋來選取資料。
- _時間篩選器_ (C) 可根據時間和日期範圍選取資料。
- _篩選器_ (D) 提供圖形介面以選取資料值和範圍。
- _應用程式面板_ (E) 顯示儀表板，其中包含視覺化和搜尋面板。

## 建立儀表板並新增現有的視覺化

建立儀表板的程序如下：

1. 開啟儀表板。您可以從新的（空白）儀表板開始、修改現有的儀表板，或複製現有的儀表板作為建立類似儀表板的起點。請參閱 [開啟儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/opening-a-dashboard/)。

1. 確認資料篩選器包含您要處理的資料。這通常（但並非總是）表示要將時間篩選器設定為包含某個時間戳記範圍。請參閱 [選取時間範圍]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/#selecting-a-time-range)。

   OpenSearch 應用程式（包括 Dashboards、Visualize 和 Discover）會將篩選器套用至應用程式中的所有資料。篩選器會套用至儀表板中使用的所有索引模式。例如，套用至記錄檔監控儀表板的時間篩選器，會從該儀表板上的所有記錄檔視覺化中選取文件，即使這些文件來自不同的索引模式也是如此。請參閱 [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。
   {: .note}

1. 將面板新增至儀表板。您可以選取已儲存的面板，或在 **Dashboards** 應用程式中建立新的視覺化。請參閱 [將視覺化新增至儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/adding-a-viz/)。

1. 在儀表板上排列面板並調整其大小。請參閱 [自訂儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/customizing-a-dash/)。

1. 儲存已完成（或仍在進行中）的儀表板。請參閱 [儲存儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/managing-a-dash/#saving-a-dashboard)。


## 後續步驟

- 如需快速了解如何檢視和篩選儀表板，請參閱 [探索 Dashboards 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dashboards/)。 

- 如需完整的端到端教學，請參閱 [教學：建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/dash-tutorial/)。
