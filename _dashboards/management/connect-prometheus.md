---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 Prometheus 連接至 OpenSearch"
parent: Connecting data sources
nav_order: 60
---

# 將 Prometheus 連線至 OpenSearch
於 2.16 版推出
{: .label .label-purple }

您可以將 OpenSearch 連線至 Prometheus 伺服器，並在 OpenSearch Dashboards 中查詢其指標。OpenSearch 不會複製指標。而是由 SQL 外掛程式在您執行查詢時，將每個查詢傳送至 Prometheus，因此 Prometheus URI 必須可從 OpenSearch 節點連線。

## 先決條件

建立連線前，請確認您已完成下列先決條件：

- 在所有 OpenSearch 節點上設定 `plugins.query.datasources.encryption.masterkey` 設定。OpenSearch 使用此金鑰加密儲存的連線認證資訊，若未設定金鑰，則會拒絕建立或更新連線的請求。如需詳細資訊，請參閱[先決條件]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/#prerequisites)。
- 確認您具有必要的[權限]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/#permissions)。

## 建立 Prometheus 連線

若要建立 Prometheus 連線，請依照下列步驟操作：

1. 在主選單中，前往 **Management** > **Dashboards Management** > **Data sources**。
1. 選取 **Create direct query connection** > **Prometheus**。
1. 在 **Data source details** 區段中，輸入 **Data source name**，並可選擇性輸入描述。您會在查詢中使用此名稱來參照該連線，例如 `source = my_prometheus.prometheus_http_requests_total`。
1. 在 **Prometheus data location** 區段中，輸入 **Prometheus URI**，例如 `http://prometheus.example.com:9090`。
1. 在 **Authentication details** 區段中，選取 **Authentication method**：
    - **No authentication**：OpenSearch 不使用認證資訊連線至 Prometheus。
    - **Basic authentication**：輸入 **Username** 與 **Password**。
    - **AWS Signature Version 4**：輸入 **Auth Region**、**Access Key** 與 **Secret Key**。Amazon Managed Service for Prometheus 請使用此方法。
1. 在 **Query permissions** 區段中，選取 **Query access level**：
    - **Admin only**：只有管理員使用者可以查詢該連線。此為預設值。
    - **Restricted**：具有您所選 OpenSearch 角色的使用者可以查詢該連線。此選項僅在已安裝 Security 外掛程式時提供。
1. 選取 **Connect to Prometheus**。

新連線會出現在資料來源清單中。

您也可以使用 `_plugins/_query/_datasources` API 建立連線。如需範例，請參閱[指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/#configuring-a-prometheus-connection-using-the-api)。

## 查詢 Prometheus 指標

若要查詢指標，請在 **Data sources** 頁面選取連線，然後選取 **Query data**。Observability 的 **Metrics** 頁面會開啟，您可以在其中將 Prometheus 指標視覺化。您也可以使用 Piped Processing Language (PPL) 查詢這些指標。如需更多資訊，請參閱[指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/)。

## 變更連線的存取權

若要變更哪些使用者可以查詢連線，請在 **Data sources** 頁面選取該連線。在 **Access control** 索引標籤上，選取 **Edit**、更新 **Query access level**，然後儲存您的變更。

## 更新連線

OpenSearch Dashboards 不支援編輯現有連線的 Prometheus URI 或認證資訊。若要更新這些項目，請向 `_plugins/_query/_datasources` API 傳送請求。下列請求會變更 `my_prometheus` 連線的 Prometheus URI：

```json
PATCH _plugins/_query/_datasources
{
  "name": "my_prometheus",
  "properties": {
    "prometheus.uri": "http://prometheus.example.com:9090"
  }
}
```
{% include copy-curl.html %}

## 刪除連線

如果在 OpenSearch Dashboards 中啟用了[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)，您可以在 **Data sources** 頁面刪除連線。在 **Direct query connections** 索引標籤上，選取該連線，選取 **Delete 1 connection**，然後確認刪除。此索引標籤只會列出在 OpenSearch Dashboards 中建立的連線。

否則，請使用 API 刪除連線：

```json
DELETE _plugins/_query/_datasources/my_prometheus
```
{% include copy-curl.html %}

## 相關文件

- [指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/)
