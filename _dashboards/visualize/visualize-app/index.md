---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Visualize 應用程式中建立視覺化"
nav_order: 40
parent: Building data visualizations
grand_parent: OpenSearch Dashboards
has_children: true
has_toc: false
redirect_from:
  - /dashboards/visualize/visualize-app/
  - /dashboards/visualize/viz-index/
---

# 在 Visualize 應用程式中建立視覺化

**Visualize** 應用程式使用點選式介面，從彙總建立資料視覺化。您可以選取視覺化類型、設定指標與桶，並調整顯示設定，以建立圖表、表格、地圖及其他資料視覺呈現方式。

如果您是初次使用 Visualize 應用程式，請參閱[探索 Visualize 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-visualize/)，透過範例資料進行實作導覽。
{: .tip}

## 必要條件

本頁的範例使用已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中的 [**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您已安裝本機 OpenSearch Dashboards 執行個體，請依照下列步驟新增範例資料：

1. 在 OpenSearch Dashboards 首頁，選取 **Add sample data**。
2. 在 **Sample flight data** 面板中，選取 **Add data**。

如需更多資訊，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

若要使用您自己的資料，您需要一個索引樣式。請參閱[設定您的資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/)。

## 導覽 Visualize 應用程式 UI

下圖顯示 **Visualize** 應用程式的主要元件。

![Visualize 應用程式介面]({{site.url}}{{site.baseurl}}/images/dashboards/viz-app-panel-callouts.png)

- _搜尋列_ (A) 可使用查詢語言搜尋來選取資料。請參閱[使用搜尋列]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/)。
- _時間篩選器_ (B) 提供圖形化介面，用於選取資料值與範圍。請參閱[使用時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。
- _篩選工具_ (C) 包含常用的命令與捷徑。請參閱[使用篩選工具]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/)。
- _視覺化面板_ (D) 顯示視覺化。
- _組態面板_ (E) 包含選取與設定視覺化的所有控制項。其內容取決於視覺化類型。請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

## 建立視覺化

若要建立視覺化，請依照下列步驟：

1. 在左側導覽選單中，選取 **OpenSearch Dashboards** > **Visualize**。

   應用程式會顯示 **Visualizations** 清單，即已儲存視覺化的表格。

1. 在右上角選取 **Create visualization**。

   應用程式會顯示 **New Visualization** 對話方塊，如下圖所示。

   ![新增視覺化對話方塊]({{site.url}}{{site.baseurl}}/images/dashboards/new-viz-dialog.png){: width=500 }

1. 選取圖示以選擇視覺化類型。如需選擇類型的協助，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。

1. 若系統提示，請在 **Choose a source** 對話方塊中選取索引樣式。並非所有視覺化類型都會顯示此對話方塊。如需建立各種視覺化類型的範例，請參閱各視覺化類型頁面。
   
   預設視覺化會顯示目前資料集的單一數值，即文件數。

   如果視覺化未顯示任何資料，或數量與預期不同，請確認[搜尋列]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/)、[篩選工具]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/)，尤其是[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)並未將未顯示的文件篩選掉。
   {: .tip}

1. 設定視覺化。如需更多資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)或各視覺化類型頁面。如需完整範例，請參閱[探索 Visualize 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-visualize/)。

## 其他開始建立視覺化的方式

除了 **Visualize** 應用程式之外，您也可以從下列位置開始建立新的視覺化：

- 若要從[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)建立視覺化 (若已啟用工作區)，請依照下列步驟：

    1. 在首頁上，選取或建立[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)。
    1. 在左側導覽選單中，展開 **Visualize and report** 並選取 **Visualizations**。
    1. 選取 **Create new visualization**。

- 若要從儀表板建立視覺化，請依照下列步驟：

    1. 在左側導覽選單中，選取 **OpenSearch Dashboards** > **Dashboards**。
    1. 開啟現有的儀表板或建立新的儀表板。
    1. 選取 **Edit**。
    1. 在工具列中選取 **Create new**，或選取 **Add** (或加號圖示)，然後在 **Add panels** 對話方塊中選取 **Create new**。

    當您從儀表板建立視覺化時，儲存時該視覺化會自動新增至該儀表板。
    {: .note}

## 儲存視覺化

即使您離開 **Visualize** 應用程式，視覺化仍會保留在應用程式中。但是，如果您在未儲存視覺化的情況下再次選取 **Visualize** 應用程式，對視覺化的變更將會遺失。我們建議您在離開 **Visualize** 應用程式前，務必先儲存視覺化。
{: .warning}

### 儲存新的視覺化

若要儲存新的視覺化，請依照下列步驟：

1. 在 **Create** 面板右上方選取 **Save**。

   應用程式會顯示 **Save visualization** 對話方塊。

1. 在 **Title** 方塊中輸入視覺化的標題。

1. (選用) 輸入 **Description**。

1. 選取 **Save**。

### 儲存現有的視覺化

您可以隨時儲存視覺化，次數不限。

若要儲存現有的視覺化，請依照下列步驟：

1. 在 **Create** 面板右上方選取 **Save**。

   如果您先前已儲存過該視覺化，**Save visualization** 的 **Title** 方塊會顯示該視覺化的標題。

1. (選用) 若要變更視覺化名稱，請在 **Title** 方塊中輸入新的視覺化標題。

1. (選用) 更新 **Description**。

1. (選用) 若要讓已儲存的視覺化保持目前狀態，並將變更儲存為新的視覺化，請選取 **Save as new visualization**。

   儲存現有的視覺化時，若未選取 **Save as new visualization**，將會覆寫視覺化先前的狀態，即使您已重新命名視覺化也一樣。
   {: .warning}

1. 若要儲存目前的變更，請選取 **Save** 按鈕。

## 將視覺化新增至儀表板

若要將已儲存的視覺化新增至儀表板，請依照下列步驟：

1. 開啟[儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
1. 選取 **Edit**。
1. 在工具列中選取 **Add** 或加號圖示。若系統提示，請選取 **From library**。
1. 從清單中選取已儲存的視覺化。

視覺化會以面板形式顯示在儀表板上。您可以調整其大小、重新定位，並與其他面板一起設定。

## 動手試試

如需使用範例資料建立折線圖的實作逐步解說，請參閱[探索 Visualize 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-visualize/)。

## 後續步驟

- 若要了解如何使用範例資料建立各種視覺化，請參閱[建立以彙總為基礎的視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/aggregation-based-viz/)。
- 如需選擇視覺化類型的協助，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要了解如何將視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
