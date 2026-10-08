---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "準備您的資料"
parent: Getting started
nav_order: 20
---

# 準備您的資料

在 OpenSearch Dashboards 中探索資料、將資料視覺化或為資料建立儀表板之前，您需要在 OpenSearch 中擁有資料，以及指向該資料的索引模式。

## 步驟 1：將資料新增至 OpenSearch

請選擇下列其中一種方式，將資料新增至 OpenSearch。我們建議您從新增範例資料開始入門。

### 新增範例資料

範例資料集隨附預先建置的索引模式、視覺化和儀表板。[**Sample flight data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中。

如果您已安裝本機 OpenSearch Dashboards 執行個體，請依照下列步驟新增一個或多個範例資料集：

**傳統導覽：**

1. 在 OpenSearch Dashboards 首頁上，選取 **Add sample data**。
1. 在 **Add sample data** 頁面上，選取 **Sample flight data** 圖塊以及您想新增的其他圖塊中的 **Add data** 按鈕。

**工作區導覽：**

1. 在左側導覽面板中，展開 **Manage workspace**，然後選取 **Sample data**。
1. 選取 **Sample flight data** 圖塊以及您想新增的其他圖塊中的 **Add data** 按鈕。

下圖顯示可用的範例資料集。

![新增範例資料視窗]({{site.url}}{{site.baseurl}}/images/dashboards/add-sample.png)

如果您已安裝範例資料，系統會自動建立索引模式，您即可開始[探索 Discover 應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-discover/)。
{: .note}

### 匯入您自己的資料

OpenSearch Dashboards 會從 OpenSearch 讀取資料，因此您需要將自己的資料新增至 OpenSearch。請使用 Bulk API、Data Prepper 或其他匯入工具將資料載入 OpenSearch。如需詳細資訊，請參閱[匯入資料]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)。

若要從 OpenSearch Dashboards 傳送 API 請求（例如 Bulk API 請求），請使用 Dev Tools 主控台。如需詳細資訊，請參閱[在 Dev Tools 主控台中執行查詢]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dev-tools/)。

匯入資料後，請依照[步驟 2](#step-2-create-an-index-pattern) 中的說明為資料建立索引模式。

## 步驟 2：建立索引模式

索引模式會告訴 OpenSearch Dashboards 要查詢哪些索引。您至少需要一個索引模式，才能將 Discover、Visualize 或 Dashboards 用於您自己的資料。

若要建立索引模式，請依照下列步驟操作：

1. 在左側導覽選單中，前往 **Management** > **Index patterns**。
2. 選取 **Create index pattern**。
3. 輸入索引名稱或模式（例如，使用 `my-index-*` 比對多個索引）。
4. 選取 **Next step**。
5. 如果您的索引包含時間戳記欄位，請從 **Time field** 下拉式選單中選取該欄位。在本節的範例中，請選取 `timestamp`。這會在 Discover 和視覺化中啟用以時間為基礎的篩選。
6. 選取 **Create index pattern**。

如需詳細資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

## 延伸閱讀

- 如需索引模式的詳細資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。
- [連接資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。

## 後續步驟

- 在[了解主要應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/learn-dashboards/)中了解各個應用程式。