---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢並視覺化 Amazon S3 資料"
parent: Connecting Amazon S3 to OpenSearch
grand_parent: Connecting data sources
nav_order: 10
has_children: false
---

# 查詢並視覺化 Amazon S3 資料
2.11 版推出
{: .label .label-purple }

本教學將引導您使用 **Query data** 使用案例，透過 OpenSearch Dashboards 查詢並視覺化您的 Amazon Simple Storage Service (Amazon S3) 資料。

## 先決條件

您必須使用 `opensearch-security` 外掛程式，並具備適當的角色權限。請聯絡您的 IT 管理員為您指派必要的權限。  

## 開始查詢

若要開始，請依照下列步驟操作：

1. 在 **Manage data sources** 頁面上，從清單中選取您的資料來源。 
2. 在資料來源的詳細資料頁面上，選取 **Query data** 卡片。此選項會將您帶往 **Observability** > **Logs** 頁面。
3. 選取 **Event Explorer** 按鈕。此選項可使用 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 或 [SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/index/) 建立並儲存經常搜尋的查詢與視覺化，並連線至 Spark SQL。
4. 從左上角的下拉式選單中選取 Amazon S3 資料來源。
5. 在 **Enter PPL query** 欄位中輸入查詢。請注意，預設語言為 SQL。若要變更語言，請從下拉式選單中選取 PPL。
6. 選取 **Search** 按鈕。畫面會顯示 **Query Processing** 訊息，確認您的查詢正在處理中。
7. 檢視結果，結果會列於 **Events** 索引標籤上的表格中。在此頁面上，可用欄位、來源與時間等詳細資料會以表格格式顯示。
8. （選用）建立資料視覺化。

## 建立 Amazon S3 資料的視覺化

若要建立視覺化，請依照下列步驟操作：

1. 在 **Explorer** 頁面上，選取 **Visualizations** 索引標籤。 
2. 選取 **Index data to visualize**。此選項只會建立[加速索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/)，讓您能從 **Visualizations** 索引標籤檢視資料視覺化。若要建立 Amazon S3 資料的視覺化，請前往 **Discover**。如需相關資訊與教學，請參閱 [Discover 文件]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。

## 搭配 Amazon S3 資料來源使用 Query Workbench

[Query Workbench]({{site.url}}{{site.baseurl}}/search-plugins/sql/workbench/) 可執行隨選 SQL 查詢、將 SQL 轉譯為對應的 REST 等效內容，並以文字、JSON、JDBC 或 CSV 格式檢視及儲存結果。

若要搭配 Amazon S3 資料使用 Query Workbench，請依照下列步驟操作：

1. 從 OpenSearch Dashboards 主選單中，選取 **OpenSearch Plugins** > **Query Workbench**。
2. 從左上角的 **Data Sources** 下拉式選單中，選擇您的 Amazon S3 資料來源。系統會開始載入屬於您資料來源的資料庫。 
3. 檢視左側導覽選單中列出的資料庫，並選取某個資料庫以檢視其詳細資料。任何有關加速索引的資訊都會列於 **Acceleration index destination** 之下。 
4. 選擇 **Describe Index** 按鈕，深入了解資料在該特定索引中的儲存方式。
5. 選擇 **Drop index** 按鈕，以刪除並清除 OpenSearch 索引以及負責重新整理資料的 Amazon S3 Spark 作業。  
6. 輸入您的 SQL 查詢，然後選取 **Run**。

## 後續步驟

- 了解如何[加速外部資料來源的查詢效能]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/)。
