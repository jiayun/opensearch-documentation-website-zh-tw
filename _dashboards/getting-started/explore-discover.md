---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索 Discover 應用程式"
parent: Getting started
nav_order: 30
---

# 探索 Discover 應用程式

**Discover** 應用程式可讓您以互動方式搜尋、篩選及檢視資料。您可以使用它來了解有哪些欄位可用、資料隨時間的分布情形，以及存在哪些模式。

使用 **Discover**，您可以：

- 選擇要分析的資料、設定該資料的時間範圍、搜尋資料，並篩選結果。
- 分析資料：查詢及篩選資料、在表格中檢視結果，以及檢視文件。
- 建立直方圖以顯示資料的分布情形。

在 Discover 和 Dashboards 應用程式的搜尋列中，您可以使用 [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/dql/) 撰寫查詢——這是一種簡單的文字型語言，可使用欄位名稱和值來篩選資料。您也可以切換為 [查詢字串 (Lucene) 語法]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。

## 前置條件

本頁面的範例使用已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中的 [**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集。

如果您使用的是本機安裝的 OpenSearch Dashboards 且尚未加入範例資料，請參閱 [Prepare your data]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 動手試試：搜尋及篩選航班資料

請依照下列步驟使用 **Discover** 應用程式：

1. 從導覽面板中，選取 **OpenSearch Dashboards** > **Discover**。

1. 在 **Discover** 頁面上，從左上方的下拉式選單中選取索引模式 `opensearch_dashboards_sample_data_flights`。

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/}（日曆）圖示，將 [時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/) 從預設的 **Last 15 minutes** 變更為 **Last 7 days**。

1. 在 DQL 搜尋列中，輸入下列查詢： 

    ```sql
    FlightDelay:true AND DestCountry: US AND FlightDelayMin >= 60
    ```
    {% include copy.html %}

1. 選取 **Update**。

    結果會顯示飛往美國且延誤 60 分鐘以上的航班。

1. 若要篩選資料，請從 DQL **搜尋列**選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/plus-icon.png" class="inline-icon" alt="plus icon"/>{:/}（加號）**Add filter**，然後在 **Edit Filter** 快顯視窗的下拉式清單中選取 **Field**、**Operator** 和 **Value**。例如，選取 `FlightDelayType`、**is** 和 **Weather Delay**。

1. 選取 **Save**。

    產生的檢視畫面如下圖所示。

    ![顯示已篩選航班資料的 Discover 輸出]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-dashboards-discover.png)

## 進一步閱讀

- 如需完整的 Discover 參考指南，請參閱 [Exploring data with Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。
- 如需 DQL 參考指南，請參閱 [Dashboards Query Language]({{site.url}}{{site.baseurl}}/dashboards/dql/)。

## 後續步驟

- 使用 [Explore the Visualize application]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-visualize/) 從您的資料建立視覺化。