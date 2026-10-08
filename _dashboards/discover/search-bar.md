---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋列"
parent: Exploring data with Discover
grand_parent: Exploring data
nav_order: 20
redirect_from: 
  - /dashboards/#discover-and-dashboard-search-bar
---

# 使用搜尋列

相同的搜尋列位於 [Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)、[Dashboard]({{site.url}}{{site.baseurl}}/dashboards/dashboard/index/) 與 [Visualize]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/) 應用程式的頂端。您可以使用它來篩選這些應用程式中顯示的資料。

在搜尋列中，您可以使用兩種語言之一進行文字搜尋：

- [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/discover/dql/)：一種具有巢狀欄位查詢的基本查詢語言。

- [Query string query language (Lucene)]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)：一種基於 [Apache Lucene](https://lucene.apache.org/core/{{site.lucene_version}}/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package.description) 查詢語言的查詢語言。

在文件與 UI 中，_Query string query language_ 與 _Lucene_ 這兩個術語可互換使用。  
{: .note}

Query string query language 與 DQL 支援不同的功能。例如，DQL 具有巢狀運算式；Lucene 則具有模糊搜尋與正規表示式。如需完整比較，請參閱 [DQL and query string query quick reference]({{site.url}}{{site.baseurl}}/dashboards/dql/#dql-and-query-string-query-quick-reference)。


## 瀏覽搜尋列

   ![Search bar interface]({{site.url}}{{site.baseurl}}/images/dashboards/search-bar-callouts.png)

搜尋列由下列元件組成：

- {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示 (A) 可儲存目前的查詢。
- **Search** 方塊 (B) 可接受目前所選查詢語言的查詢。
- 查詢語言選取器 (C) 可開啟 **Syntax options** 彈出視窗以選擇查詢語言。

## 變更查詢語言

目前的查詢語言（OpenSearch Dashboards Query Language (DQL) 或 Query String Query Language (Lucene)）會顯示在 **Search** 方塊的右側。

若要在 DQL 與 query string query language 之間切換，請依照下列步驟操作：

1. 選擇查詢語言選取器（顯示目前的查詢語言）。

1. 在 **Syntax options** 對話方塊中，將 **OpenSearch Dashboards Query Language** 切換為開啟或關閉。

   如果 **OpenSearch Dashboard Query Language** (DQL) 切換為**關閉**，查詢語言會設為 OpenSearch Dashboards Query Language，且查詢語言選取器會顯示 **Lucene**。
   {: .note}

   ![Using query string syntax in OpenSearch Dashboards Discover]({{site.url}}{{site.baseurl}}/images/dashboards/discover-lucene-syntax.png){: width="97%" }


## 根據查詢進行篩選

若要使用 **Search** 方塊進行篩選，請依照下列步驟操作：

1. 在 **Search** 方塊中輸入篩選條件。例如，針對 OpenSearch 電子商務範例資料使用 DQL，請輸入 `category: "Men's Clothing"`。

   如需關於使用 DQL 查詢的資訊，請參閱 [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/discover/dql/)。

   如需關於使用 Lucene 查詢的資訊，請參閱 [Query string query language (Lucene)]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。

1. 選擇 **Refresh**。

   ![Refresh button]({{site.url}}{{site.baseurl}}/images/dashboards/refresh-button.png){: width="100" }

   **Results** 表格將更新以反映根據查詢所進行的篩選。

## 編輯篩選查詢

若要變更查詢，請依照下列步驟操作：

1. 編輯 **Search** 方塊中的篩選條件。例如，若要變更前一個範例中的 DQL 查詢，請將查詢變更為 `sales_by_category is "Women's Clothing"`。

1. 選擇 **Refresh**。

   ![Refresh button]({{site.url}}{{site.baseurl}}/images/dashboards/refresh-button.png){: width="100" }

   **Results** 表格將更新以反映變更後的查詢。

## 儲存查詢

使用此程序來儲存下列項目的任何組合：

- DQL 或 Lucene 查詢。
- 篩選器。
- 時間篩選器。

若要儲存查詢，請依照下列步驟操作：

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示。

**Search** 方塊中不需要有查詢。您可以使用此程序來儲存篩選器和/或時間篩選器，而無需儲存查詢。
{: .note}

1. 從 **Save** 彈出視窗中，選擇 **Save current query** 或 **Save as new**。

1. 在 **Save query** 對話方塊中，為查詢輸入 **Name**。

1. (選用) 在 **Description** 方塊中，輸入查詢的描述。

1. (選用) 啟用 **Include filters** 切換開關，以同時儲存 [篩選清單]({{site.url}}{{site.baseurl}}/dashboards/discover/filter-tool/) 中的篩選器。

1. (選用) 啟用 **Include time filter** 切換開關，以同時儲存目前啟用的 [時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。

1. 選擇 **Save**。


## 載入已儲存的搜尋

若要載入已儲存的搜尋，請依照下列步驟操作：

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示。

1. 選擇您要載入的搜尋。

   篩選器將載入，且 **Discover** 應用程式中顯示的資料將更新。


## 編輯查詢

若要變更現有查詢，請依照下列步驟操作：

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示。

1. 選擇您要編輯的查詢。

1. 使用您想要更新查詢的搜尋查詢、篩選器和時間篩選器來篩選資料。

1. 再次選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示。清單中會勾選目前的已儲存查詢。

1. 選擇 **Save changes**。

1. (選用) 在 **Save query** 對話方塊中，輸入或變更 **Description**。

1. 選擇 **Save**。


## 刪除查詢

若要刪除查詢，請依照下列步驟操作：

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/save-icon.png" class="inline-icon" alt="save icon"/>{:/} (儲存) 圖示。

1. 將滑鼠懸停在您要刪除的查詢上。

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/trash-icon.png" class="inline-icon" alt="trash icon"/>{:/} (垃圾桶) 圖示。

1. 在刪除確認對話方塊中，選擇 **Delete**。

