---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 Amazon S3 連接至 OpenSearch"
parent: Connecting data sources
nav_order: 30
has_children: true
---

# 將 Amazon S3 連接至 OpenSearch
於 2.11 版推出
{: .label .label-purple }

您可以使用 OpenSearch Dashboards 介面，將 OpenSearch 連接至您的 Amazon Simple Storage Service (Amazon S3) 資料來源，接著查詢該資料、最佳化查詢效能、定義資料表，並整合您的 S3 資料。

## 先決條件

連接資料來源之前，請確認已符合下列需求：

- 您具有 Amazon S3 和 [AWS Glue Data Catalog](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/connectors/s3glue_connector.md) 的存取權。
- 您具有 OpenSearch 和 OpenSearch Dashboards 的存取權。
- 您了解 OpenSearch 資料來源和連接器的概念。如需詳細資訊，請參閱[開發人員文件](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/datasources.md)。

## 連接您的資料來源

若要連接您的資料來源，請依照下列步驟操作：

1. 從 OpenSearch Dashboards 主選單，前往 **Management** > **Dashboards Management** > **Data sources**。
2. 在 **Data sources** 頁面上，選取 **Create data source connection** > **Amazon S3**。
3. 在 **Configure Amazon S3 data source** 頁面上，輸入資料來源、驗證詳細資料和權限。
4. 選取 **Review Configuration** 按鈕以確認連線詳細資料。
5. 選取 **Connect to Amazon S3** 按鈕以建立連線。

## 管理您的資料來源

若要管理您的資料來源，請依照下列步驟操作：

1. 在 **Manage data sources** 索引標籤上，從清單中選擇資料來源。
2. 在該資料來源的頁面上，您可以管理資料來源、選擇使用案例，以及設定存取控制。
3. （選用）探索 Amazon S3 的使用案例，包括查詢您的資料和最佳化查詢效能。若要進一步了解各個使用案例，請參閱[**後續步驟**](#next-steps)一節。

## 限制

此功能目前仍在開發中，包括資料整合功能。如需最新資訊，請參閱 [GitHub 上的開發人員文件](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#limitations)。

## 後續步驟

- 了解如何透過 OpenSearch Dashboards [在 Data Explorer 中查詢您的資料]({{site.url}}{{site.baseurl}}/dashboards/management/query-data-source/)。
- 了解如何透過 Query Workbench [最佳化外部資料來源的查詢效能]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/)，例如 Amazon S3。
- 了解 [Amazon S3 和 AWS Glue Data Catalog](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/connectors/s3glue_connector.md)，以及搭配 Amazon S3 資料來源使用的 API，包括組態設定和查詢範例。
- 了解如何透過 OpenSearch Dashboards [管理您的索引]({{site.url}}{{site.baseurl}}/dashboards/im-dashboards/index/)。
