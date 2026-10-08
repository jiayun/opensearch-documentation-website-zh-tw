---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "外掛程式設定"
parent: Configuring OpenSearch
nav_order: 140
---

# 外掛程式設定

以下設定與 OpenSearch 外掛程式相關。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## Alerting 外掛程式設定

如需警示設定的相關資訊，請參閱[警示設定]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/settings/#alerting-settings)。

## Anomaly Detection 外掛程式設定

如需異常偵測設定的相關資訊，請參閱[異常偵測設定]({{site.url}}{{site.baseurl}}/observing-your-data/ad/settings/)。

## Asynchronous Search 外掛程式設定

如需非同步搜尋設定的相關資訊，請參閱[非同步搜尋設定]({{site.url}}{{site.baseurl}}/search-plugins/async/settings/)。

## Cross-Cluster Replication 外掛程式設定

如需跨叢集複寫設定的相關資訊，請參閱[複寫設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/settings/)。

## Flow Framework 外掛程式設定

如需自動化工作流程設定的相關資訊，請參閱[工作流程設定]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-settings/)。

## Geospatial 外掛程式設定

如需 Geospatial 外掛程式的 IP2Geo 處理器設定的相關資訊，請參閱[叢集設定]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ip2geo/#cluster-settings)。

如需 Geospatial 外掛程式的 GeoJSON 複雜度設定的相關資訊，請參閱[設定 GeoJSON 複雜度]({{site.url}}{{site.baseurl}}/dashboards/visualize/geojson-regionmaps/#configuring-geojson-complexity)。

## Index Management 外掛程式設定

如需索引狀態管理 (ISM) 設定的相關資訊，請參閱 [ISM 設定]({{site.url}}{{site.baseurl}}/im-plugin/ism/settings/)。

### 索引彙整設定

如需索引彙整 (rollup) 設定的相關資訊，請參閱[索引彙整設定]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/settings/)。

## Job Scheduler 外掛程式設定

如需 Job Scheduler 外掛程式設定的相關資訊，請參閱 [Job Scheduler 叢集設定]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/job-scheduler/index/#job-scheduler-cluster-settings)。

## k-NN 外掛程式設定

如需 k-NN 設定的相關資訊，請參閱 [k-NN 設定]({{site.url}}{{site.baseurl}}/search-plugins/knn/settings/)。

## ML Commons 外掛程式設定

如需機器學習設定的相關資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

## Neural Search 外掛程式設定

如需 Neural Search 外掛程式設定的相關資訊，請參閱 [Neural Search 外掛程式設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#neural-search-plugin-settings)。

## Notifications 外掛程式設定

Notifications 外掛程式支援下列設定。此清單中的所有設定皆為動態設定：

- `opensearch.notifications.core.allowed_config_types` (清單)：Notifications 外掛程式允許的組態類型。請使用 `GET /_plugins/_notifications/features` API 擷取此設定的值。組態類型包括 `slack`、`chime`、`microsoft_teams`、`webhook`、`email`、`sns`、`ses_account`、`smtp_account` 和 `email_group`。

- `opensearch.notifications.core.email.minimum_header_length` (整數)：電子郵件標頭的最小長度。用於驗證電子郵件訊息的總長度。預設值為 `160`。

- `opensearch.notifications.core.email.size_limit` (整數)：電子郵件大小上限。用於驗證電子郵件訊息的總長度。預設值為 `10000000`。

- `opensearch.notifications.core.http.connection_timeout` (整數)：內部 HTTP 用戶端的連線逾時。此用戶端用於以 webhook 為基礎的通知管道。預設值為 `5000`。

- `opensearch.notifications.core.http.host_deny_list` (清單)：遭拒主機的清單。HTTP 用戶端不會將通知傳送至此清單中的 webhook URL。

- `opensearch.notifications.core.http.max_connection_per_route` (整數)：內部 HTTP 用戶端每個路由的 HTTP 連線數上限。此用戶端用於以 webhook 為基礎的通知管道。預設值為 `20`。

- `opensearch.notifications.core.http.max_connections` (整數)：內部 HTTP 用戶端的 HTTP 連線數上限。此用戶端用於以 webhook 為基礎的通知管道。預設值為 `60`。

- `opensearch.notifications.core.http.socket_timeout` (整數)：內部 HTTP 用戶端的通訊端逾時組態。此用戶端用於以 webhook 為基礎的通知管道。預設值為 `50000`。

- `opensearch.notifications.core.tooltip_support` (布林值)：為 Notifications 外掛程式啟用工具提示支援。請使用 `GET /_plugins/_notifications/features` API 擷取此設定的值。預設值為 `true`。

- `opensearch.notifications.general.filter_by_backend_roles` (布林值)：啟用依後端角色篩選 (通知管道的角色型存取控制)。預設值為 `false`。

- `opensearch.notifications.general.filter_by_backend_roles_access_strategy` (字串)：控制依後端角色篩選的方式 (通知管道的角色型存取控制)。有效值如下：
  - `intersect` (預設) -- 若使用者與建立物件的使用者至少共用一個後端角色，即可存取通知物件。
  - `exact` -- 若使用者的後端角色與建立物件的使用者完全相同 (沒有額外角色)，即可存取通知物件。
  - `all` -- 若使用者的後端角色包含建立物件的使用者的所有後端角色，即可存取通知物件。

## Query Insights 外掛程式設定

如需 Query Insights 外掛程式設定的相關資訊，請參閱 [Query Insights 功能與設定]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/index#query-insights-features-and-settings)。

## Security 外掛程式設定

如需 Security 外掛程式設定的相關資訊，請參閱[安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)。

## Security Analytics 外掛程式設定

如需 Security Analytics 外掛程式設定的相關資訊，請參閱 [Security Analytics 設定]({{site.url}}{{site.baseurl}}/security-analytics/settings/)。

## SQL 外掛程式設定

如需 SQL 和 PPL 相關設定的資訊，請參閱 [SQL 設定]({{site.url}}{{site.baseurl}}/search-plugins/sql/settings/)。

## Workload Management 外掛程式設定

如需工作負載管理設定的相關資訊，請參閱[工作負載管理設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/#workload-management-settings)。

## 一般外掛程式設定

OpenSearch 支援下列一般外掛程式組態設定：

- `plugin.mandatory` (靜態，清單)：指定節點成功啟動所必需的外掛程式。若列出的任何外掛程式無法使用或載入失敗，節點將不會啟動。對於依賴自訂處理器或其他關鍵外掛程式功能的叢集而言，此設定特別重要，可確保所有節點的行為一致。您可以使用逗號分隔清單指定多個外掛程式。預設值為 `[]` (空白清單)。
