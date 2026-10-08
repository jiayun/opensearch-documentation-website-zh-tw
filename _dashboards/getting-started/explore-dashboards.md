---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索 Dashboards 應用程式"
parent: Getting started
nav_order: 40
---

# 探索 Dashboards 應用程式

**Dashboards** 應用程式可讓您將多個視覺化組合到單一頁面中，以進行監控與分析。

使用 **Dashboards**，您可以：

- 在單一檢視中顯示多個資料視覺化。
- 建置動態儀表板。
- 建立並分享報告。
- 嵌入分析功能，讓您的應用程式更具特色。

## 先決條件

本頁的範例使用 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中已安裝的 [**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您使用的是本機安裝的 OpenSearch Dashboards，且尚未新增範例資料，請參閱[準備您的資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 動手試試：探索預先建置的儀表板

1. 從導覽面板中，選取 **OpenSearch Dashboards** > **Dashboards**。面板會顯示現有儀表板的清單。

1. 在搜尋工具列中，搜尋並選取 **[Flights] Global Flight Dashboard**。

    面板會顯示一個預先載入視覺化的儀表板，包括圖表、地圖和資料表。

1. 若要將其他面板新增至儀表板，請選取 **Edit** 按鈕，然後從工具列中選擇 **Add**。

1. 在 **Add panels** 視窗的搜尋工具列中，輸入 `flights`。

1. 從篩選後的清單中，選取 **[Flights] Delay Buckets**。

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）以關閉確認對話方塊。

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）以關閉 **Add panels** 視窗。

1. 向下捲動，確認新增的面板現在顯示為儀表板上的最後一個面板。

    產生的檢視如下圖所示。

    ![新增面板檢視]({{site.url}}{{site.baseurl}}/images/dashboards/add-dash-panel.png)

### 新增您自己的視覺化

如果您使用的是本機安裝，且已在[探索 Visualize 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-visualize/)中儲存 `Flight count over time` 視覺化，即可將其新增至此儀表板。由於 OpenSearch Playground 為唯讀，因此無法在其中儲存視覺化。

若要新增視覺化，請依照下列步驟操作：

1. 從工具列中選取 **Add**。
1. 在搜尋工具列中，輸入 `Flight count over time`。
1. 從清單中選取該視覺化。

    該視覺化會新增為儀表板上的最後一個面板，如下圖所示。

    ![新增至儀表板末端的 Flight count over time 面板]({{site.url}}{{site.baseurl}}/images/dashboards/add-flight-count-panel.png)

## 在 Dashboards 應用程式中篩選資料

您可以與視覺化互動以篩選資料。

使用 **[Flights] Global Flight Dashboard** 儀表板，依照下列步驟篩選範例航班資料：

1. 在 **[Flights] Airline Carrier** 面板上，選取左下角的 **Toggle legend** 圖示。接著選取 **OpenSearch-Air**，然後選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/plus-icon.png" class="inline-icon" alt="plus icon"/>{:/}（加號）圖示。

    儀表板會自動更新，並將篩選條件 `Carrier: OpenSearch-Air` 新增至左上方的篩選列，如下圖所示。

    ![依 OpenSearch-Air 航空公司篩選的儀表板]({{site.url}}{{site.baseurl}}/images/dashboards/airline-carrier-filter.png)

1. 選取 **Save** 以儲存儀表板。

或者，您也可以使用儀表板工具列來套用篩選條件：

1. 如果您已依照前述說明新增篩選條件，請先在篩選列的 `Carrier: OpenSearch-Air` 篩選條件中選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）以移除該篩選條件。

1. 在儀表板工具列中，選取 **+ Add filter**。

1. 從 **Field**、**Operator** 和 **Value** 下拉式清單中，分別選取 **Carrier**、**is** 和 **OpenSearch-Air**。

1. 選取 **Save**。

## 延伸閱讀

- 如需完整的 Dashboards 參考資料，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。

## 後續步驟

- 在[在 Dev Tools 主控台中執行查詢]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dev-tools/)中，了解如何執行 API 查詢。
