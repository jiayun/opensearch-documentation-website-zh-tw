---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Discover 探索資料"
parent: Exploring data
nav_order: 10
has_children: true
has_toc: false
---

# 使用 Discover 探索資料

您可以使用 **OpenSearch Dashboards** 中的 **Discover** 應用程式，探索 OpenSearch 中的資料並將其視覺化。

如果您剛開始使用 Discover 應用程式，請參閱[探索 Discover 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-discover/)，透過範例資料進行實作入門。
{: .tip}

## 先決條件

本頁的範例使用已安裝於 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 的 [**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您已安裝本機 OpenSearch Dashboards 執行個體，請依照下列步驟新增範例資料：

1. 在 OpenSearch Dashboards 首頁上，選取 **Add sample data**。
2. 在 **Sample flight data** 面板中，選取 **Add data**。

如需詳細資訊，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 瀏覽 Discover 應用程式使用者介面

下圖顯示 **Discover** 應用程式的主要元件。

![Discover 應用程式預設頁面]({{site.url}}{{site.baseurl}}/images/dashboards/discover-app-panel-callouts.png)

- _應用程式選單_（A）提供建立和儲存 Discover 篩選器設定的選項。
- _欄位選取_工具（B）決定哪些欄位會顯示在 **Discover** 應用程式面板中。請參閱[使用欄位選取工具]({{site.url}}{{site.baseurl}}/dashboards/discover/field-select/)。
- _時間篩選器_（C）提供圖形介面，可用來選取資料值和範圍。請參閱[使用時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。
- _搜尋_列（D）可讓您透過查詢語言搜尋來選取資料。請參閱[使用搜尋列]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/)。
- _篩選器_工具（E）包含常用命令和捷徑。請參閱[使用篩選器工具]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/)。
- **Discover** _應用程式面板_顯示下列元素：
  - _日期範圍顯示區_（F）可用來指定和選取日期時間範圍，並決定時間軸視覺化的刻度。
  - _時間戳記直方圖_（G）顯示每個時間間隔的文件數量。
  - **Results** 表格（H）顯示所選文件的摘要。您可以展開每份文件，並以表格或 JSON 格式檢視。

  如果未選取任何資料，應用程式面板會顯示 **</> No Results** 訊息。這種情況經常發生，尤其是在使用 OpenSearch Dashboards 範例資料時，因為所有資料都落在時間篩選器的時間間隔之外。
  {: .note}

  時間篩選器的時間間隔預設為 **Last 15 minutes**。若要變更時間篩選器的時間間隔，請[擴大時間範圍]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/#selecting-a-time-range)以納入資料。
  {: .note}

## 檢視 Results 表格

**Results** 表格顯示所選資料。每一列代表一份文件，每一欄則包含文件屬性。

依預設，表格會顯示所有所選文件的全部屬性。

若要在 **Discover** 應用程式中顯示文件，請依照下列步驟操作：

1. 在導覽面板中，選取 **OpenSearch Dashboards** > **Discover**。

1. 從欄位選取工具的 **Index patterns** 下拉式選單中，選擇您要處理的資料。請參閱[選取索引模式]({{site.url}}{{site.baseurl}}/dashboards/discover/field-select/#selecting-an-index-pattern)。

   在下列範例中，請選擇 `opensearch_dashboards_sample_data_flights`。

1. 使用時間篩選器選取您感興趣的時間間隔。請參閱[選取時間範圍]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/#selecting-a-time-range)。

   在此範例中，請選取 **Last 12 months**。

   下圖顯示 Discover 應用程式中產生的畫面。

   ![Discover 介面顯示最近 90 天航班範例資料的搜尋結果]({{site.url}}{{site.baseurl}}/images/dashboards/discover-display-flight-data-3-mo.png){: width="95%" }

1. 如下圖所示，在時間戳記直方圖中拖曳選取狹窄的資料區段。

   ![Discover 介面顯示拖曳選取操作]({{site.url}}{{site.baseurl}}/images/dashboards/discover-drag-select.png){: width="95%" }

   資料會調整為橫跨資料顯示區的寬度，刻度也會自動調整。

   以互動方式選取日期範圍會產生絕對時間間隔。
   {: .note}

1. 從日期範圍顯示區的下拉式選單中選取 **Auto**。

   產生的檢視畫面應如下圖所示。

   ![Discover 介面顯示縮放至顯示區寬度的航班範例資料]({{site.url}}{{site.baseurl}}/images/dashboards/discover-display-flight-data-adjusted.png){: width="95%" }


## 篩選文件

您可以透過幾種方式，從所選索引模式中篩除文件：

- 進一步縮小時間間隔
- 輸入查詢語言查詢
- 在以選單操作的篩選器工具中選取屬性值

您可以儲存這些篩選器的任意組合，之後再將其套用至相同或不同的索引模式。請參閱[儲存查詢]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/#saving-a-query)。


### 縮小時間間隔

**Discover** 應用程式只會顯示時間篩選器的時間間隔內所包含的文件。時間間隔可以是_相對_時間間隔（相對於_現在_的固定時間範圍），或_絕對_時間間隔（兩個固定時間之間）。

前面的範例示範了部分用來變更時間間隔的工具。若要瞭解其他工具，請參閱[使用時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。


### 輸入查詢

您可以使用兩種查詢語言之一，在搜尋列中輸入查詢字串來篩選文件。

- [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/discover/dql/) 是搜尋列中的預設查詢語言，僅在 **Dashboards** 中提供。
- [查詢字串查詢語言（Lucene）]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) 以 [Apache Lucene](https://lucene.apache.org/core/{{site.lucene_version}}/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package.description) 查詢語言為基礎。

若要使用搜尋列篩選文件，請參閱[使用搜尋列]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/)。

例如，使用 _flights_ 範例資料時，請輸入下列 DQL 搜尋：

```
Carrier: "OpenSearch-Air"
```

### 選取屬性值

您可以使用篩選器工具，根據屬性值新增任意數量的個別篩選器。

您可以逐一或一次啟用或停用所有篩選器；反轉任一篩選器的納入或排除狀態；並將篩選器整組釘選，使其套用至 **Dashboards** 和  **Visualization** 應用程式。

若要使用篩選器工具，請參閱[使用篩選器工具]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/)。

例如，使用 _flights_ 範例資料時，請使用篩選器工具輸入下列篩選器：

![資料篩選器]({{site.url}}{{site.baseurl}}/images/dashboards/filter-cancelled-true.png){: width="100" }


## 選擇資料欄位

預設情況下，**Discover** 應用程式會顯示文件中的所有欄位。您可以選擇在 **Results** 表格中顯示一個、多個或所有欄位。

若要選擇在 **Results** 表格中顯示的欄位，請參閱[使用欄位選取工具]({{site.url}}{{site.baseurl}}/dashboards/discover/field-select/)。

例如，在欄位選取工具中選取 **Dest**、**FlightDelayMin** 和 **FlightDelayType**。**Results** 表格現在只會顯示這些欄位（以及 **Time**）。


## 檢視文件

若要展開單一文件，並在 **Results** 表格中查看詳細內容，請依照下列步驟操作：

1. 在 **Results** 表格左側欄中的某一列，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="expand icon"/>{:/}（展開）圖示。展開的文件會顯示在該列下方的 **Expanded document** 區域中。

1. （選用）若要以 JSON 格式顯示文件，請選取 **JSON** 索引標籤。

1. 若要返回（預設的）表格檢視，請選取 **Table** 索引標籤。

1. （選用）若要檢視目前文件之前或之後的文件，請選取 **View surrounding documents**。

   該文件會顯示在新的瀏覽器索引標籤或視窗中，預設也會一併顯示其前後各五份文件。

   如果緊接在前或後的文件較少，顯示的周邊文件數量也會較少。
   {: .note}

1. （選用）若要單獨檢視展開的文件，請選取 **View single document**。

   展開的文件會顯示在新的瀏覽器索引標籤或視窗中。

1. 若要收合展開的文件，請選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-down-icon.png" class="inline-icon" alt="collapse icon"/>{:/}（向下箭頭）圖示。


## 將資料欄位視覺化

若要將資料欄位視覺化，請依照下列步驟操作：

1. 在欄位選取清單中，將滑鼠游標移至您要視覺化的欄位上。

1. 選取欄位名稱右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/inspect-icon.png" class="inline-icon" alt="inspect icon"/>{:/}（檢查）圖示。

   **Top 5 views popover** 隨即顯示，如下圖所示。
   
   ![前 5 個值的彈出視窗]({{site.url}}{{site.baseurl}}/images/dashboards/top-5-values.png){: width="51%" }

1. 在 **Top 5 values** 彈出視窗中，選取 **Visualize** 按鈕。畫面會切換至 **Visualize** 應用程式，顯示所選欄位的預設視覺化。

   請參閱[建立資料視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)，瞭解如何編輯視覺化的顯示方式。


## 匯出資料

您可以將 **Results** 表格中的資料匯出至 CSV 檔案，或複製代表單一文件的 JSON 物件。若要依排程或透過指令碼匯出相同資料，請將您的查詢儲存為已儲存的搜尋，並從中產生 CSV 報表。這樣就能不經由介面匯出資料。如需詳細資訊，請參閱[報表 API]({{site.url}}{{site.baseurl}}/reporting/api/)。

### 將資料下載至 CSV 檔案

若要將 **Results** 表格中的資料下載為 CSV 格式的檔案：

1. 依照[篩選文件](#filtering-documents)中的說明，篩選出您要匯出的文件。

1. 依照[選擇資料欄位](#choosing-data-fields)中的說明，選擇您要匯出的資料欄位。

1. 選取 **Download as CSV**。

1. 在 **DOWNLOAD AS CSV** 彈出視窗中，選擇僅下載頁面上 **Visible** 的文件，或下載 **Max available**（所有選取的文件，上限為 10,000 份文件）。

1. 選取 **Download CSV** 按鈕。

   資料會寫入檔案系統預設位置中的 CSV 檔案。

   如果所選欄位包含物件或陣列，CSV 文件將以 JSON 物件的形式下載。若要下載為個別的 CSV 值，請只選取單值欄位。
   {: .tip}

### 複製文件的 JSON 表示形式

若要複製文件的 JSON 表示形式，請依照下列步驟操作：

1. 在 **Results** 表格中選取個別文件。請參閱[檢視文件](#examining-a-document)。

1. 選取 JSON 索引標籤，以 JSON 形式檢視文件。

1. 選取 JSON 顯示區域右上角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/copy-icon.png" class="inline-icon" alt="copy icon"/>{:/}（複製）圖示。

## 設定警示

您可以為資料值設定閾值，然後設定警示，在資料超過閾值時通知您。

若要瞭解如何建立及管理警示，請參閱[為儀表板和視覺化設定警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/dashboards-alerting/)。

