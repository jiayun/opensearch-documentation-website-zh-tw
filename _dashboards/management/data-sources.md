---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連接資料來源"
nav_order: 30
has_children: true
---

# 資料來源

OpenSearch 資料來源是 OpenSearch 可以連接並從中匯入資料的應用程式。連接資料來源並匯入資料後，即可使用 [REST API]({{site.url}}{{site.baseurl}}/api-reference/index/) 或 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/) 將資料編製索引、搜尋及分析。

本文件著重說明如何使用 OpenSearch Dashboards 網頁介面來連接及管理您的資料來源。如需使用 API 連接資料來源的相關資訊，請參閱[後續步驟](#next-steps)中所連結的開發人員資源。

## 先決條件

將資料來源連接至 OpenSearch 的第一步，是在您的系統上安裝 OpenSearch 和 OpenSearch Dashboards。如需相關資訊，請參閱[安裝說明]({{site.url}}{{site.baseurl}}/install-and-configure/index/)。

安裝 OpenSearch 和 OpenSearch Dashboards 後，您可以使用 Dashboards 將資料來源連接至 OpenSearch，接著使用 Dashboards 管理資料來源、根據這些資料來源建立索引模式、對特定資料來源執行查詢，以及將多個視覺化組合在同一個儀表板中。

您必須設定 [YAML 檔案]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/#configuration-file)，並安裝 `dashboards-observability` 和 `opensearch-sql` 外掛程式。如需詳細資訊，請參閱 [OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

若要在 OpenSearch 中安全地儲存並加密資料來源連線，您必須在所有節點的 `opensearch.yml` 檔案中加入下列組態：

`plugins.query.datasources.encryption.masterkey: "YOUR_GENERATED_MASTER_KEY_HERE"`

金鑰長度必須為 16、24 或 32 個字元。您可以使用下列命令產生 24 個字元的金鑰：

`openssl rand -hex 12`

產生 12 個位元組會得到長度為 12 * 2 = 24 個字元的十六進位字串。
{: .note}

## 權限

若要在 OpenSearch Dashboards 中使用資料來源，您必須獲指派正確的叢集層級[資料來源權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions#data-source-permissions)。

## 資料串流類型

若要透過 OpenSearch Dashboards 設定資料來源，請前往 **Management** > **Dashboards Management** > **Data sources**。此流程可用於 OpenSearch 資料串流連線。請參閱[設定及使用多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)。

或者，如果您執行的是 OpenSearch Dashboards 2.16 或更新版本，請前往 **Management** > **Data sources**。此流程可用於連接 Amazon Simple Storage Service (Amazon S3) 和 Prometheus。如需詳細資訊，請參閱[將 Amazon S3 連接至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/S3-data-source/) 和[將 Prometheus 連接至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)。

## 後續步驟

- 了解如何透過 OpenSearch Dashboards [管理索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。
- 了解如何透過 OpenSearch Dashboards [使用 Index Management 將資料編製索引]({{site.url}}{{site.baseurl}}/dashboards/im-dashboards/index/)。
- 了解如何連接[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)。
- 了解如何使用 OpenSearch Dashboards 介面連接 [OpenSearch 與 Amazon S3]({{site.url}}{{site.baseurl}}/dashboards/management/S3-data-source/) 以及 [OpenSearch 與 Prometheus]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)。
- 了解 [Integrations]({{site.url}}{{site.baseurl}}/integrations/index/) 外掛程式，此外掛程式可讓您彈性運用各種資料匯入方法，並將資料連接至 OpenSearch Dashboards。
