---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理 OpenSearch Dashboards 外掛程式"
nav_order: 100
redirect_from: 
  - /dashboards/install/plugins/
---

# 管理 OpenSearch Dashboards 外掛程式

OpenSearch Dashboards 提供了一個名為 `opensearch-dashboards-plugin` 的命令列工具用於管理外掛程式。

## 前置條件

- 相容的 OpenSearch 叢集
- [安裝在該叢集上]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)的對應 OpenSearch 外掛程式
- 對應版本的 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/) (例如，OpenSearch Dashboards 2.3.0 可與 OpenSearch 2.3.0 搭配使用)

## 使用 `opensearch-dashboards-plugin` 工具

使用 `opensearch-dashboards-plugin` 工具來執行以下操作：

- [列出](#listing-installed-plugins)已安裝的外掛程式。
- [安裝](#installing-plugins)外掛程式。
- [移除](#removing-plugins)已安裝的外掛程式。

### 列出已安裝的外掛程式

若要從命令列查看已安裝外掛程式的清單，請使用以下命令：

```bash
sudo bin/opensearch-dashboards-plugin list
```
{% include copy.html %}

該命令會回傳已安裝外掛程式及其版本的清單：

```bash
alertingDashboards@3.1.0.0
anomalyDetectionDashboards@3.1.0.0
assistantDashboards@3.1.0.0
customImportMapDashboards@3.1.0.0
flowFrameworkDashboards@3.1.0.0
indexManagementDashboards@3.1.0.0
mlCommonsDashboards@3.1.0.0
notificationsDashboards@3.1.0.0
observabilityDashboards@3.1.0.0
queryInsightsDashboards@3.1.0.0
queryWorkbenchDashboards@3.1.0.0
reportsDashboards@3.1.0.0
searchRelevanceDashboards@3.1.0.0
securityAnalyticsDashboards@3.1.0.0
```

### 安裝外掛程式

若要安裝外掛程式，請提供外掛程式 zip 檔案的 URL：

```bash
sudo bin/opensearch-dashboards-plugin install <plugin-zip-url>
```
{% include copy.html %}

若要從主機上的 zip 檔案安裝外掛程式，請使用 `file://` 方案提供檔案路徑：

```bash
sudo bin/opensearch-dashboards-plugin install file:///<path-to-plugin-zip>
```
{% include copy.html %}

外掛程式版本必須與您的 OpenSearch Dashboards 版本相符。如需更多資訊，請參閱 [外掛程式相容性](#plugin-compatibility)。安裝外掛程式後，請重新啟動 OpenSearch Dashboards。

### 移除外掛程式

若要移除外掛程式，請使用以下命令：

```bash
sudo bin/opensearch-dashboards-plugin remove alertingDashboards
```
{% include copy.html %}

接著從 `opensearch_dashboards.yml` 中移除所有相關項目，並重新啟動 OpenSearch Dashboards。

### 更新外掛程式

`opensearch-dashboards-plugin` 工具不支援更新外掛程式。若要更新外掛程式，請[移除舊版本](#removing-plugins)、[安裝新版本](#installing-plugins)並重新啟動 OpenSearch Dashboards。

## 可用的外掛程式

下表列出了可用的 OpenSearch Dashboards 外掛程式。所有列出的外掛程式均包含在預設的 OpenSearch 發行版中。

| 外掛程式名稱 | 儲存庫 | 最早可用版本 |
| :--- | :--- | :--- |
| `alertingDashboards` | [alerting-dashboards-plugin](https://github.com/opensearch-project/alerting-dashboards-plugin) | 1.0.0 |
| `anomalyDetectionDashboards` | [anomaly-detection-dashboards-plugin](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin) | 1.0.0 |
| `assistantDashboards` | [dashboards-assistant](https://github.com/opensearch-project/dashboards-assistant) | 2.13.0 |
| `customImportMapDashboards` | [dashboards-maps](https://github.com/opensearch-project/dashboards-maps) | 2.2.0 |
| `flowFrameworkDashboards` | [dashboards-flow-framework](https://github.com/opensearch-project/dashboards-flow-framework) | 2.19.0 |
| `indexManagementDashboards` | [index-management-dashboards-plugin](https://github.com/opensearch-project/index-management-dashboards-plugin) | 1.0.0 |
| `mlCommonsDashboards` | [ml-commons-dashboards](https://github.com/opensearch-project/ml-commons-dashboards) | 2.6.0 |
| `notificationsDashboards` | [dashboards-notifications](https://github.com/opensearch-project/dashboards-notifications) | 2.0.0 |
| `observabilityDashboards` | [dashboards-observability](https://github.com/opensearch-project/dashboards-observability) | 2.0.0 |
| `queryInsightsDashboards` | [query-insights-dashboards](https://github.com/opensearch-project/query-insights-dashboards) | 2.19.0 |
| `queryWorkbenchDashboards` | [query-workbench](https://github.com/opensearch-project/dashboards-query-workbench) | 1.0.0 |
| `reportsDashboards` | [dashboards-reporting](https://github.com/opensearch-project/dashboards-reporting) | 1.0.0 |
| `searchRelevanceDashboards` | [dashboards-search-relevance](https://github.com/opensearch-project/dashboards-search-relevance) | 2.4.0 |
| `securityAnalyticsDashboards` | [security-analytics-dashboards-plugin](https://github.com/opensearch-project/security-analytics-dashboards-plugin)| 2.4.0 |
| `securityDashboards` | [security-dashboards-plugin](https://github.com/opensearch-project/security-dashboards-plugin) | 1.0.0 |

_<sup>*</sup>`dashboardNotebooks` 已在 OpenSearch 1.2.0 版本中合併至 Observability 外掛程式。_<br>

## 外掛程式相容性

外掛程式的主版本、次版本和修補版本必須與 OpenSearch 的主版本、次版本和修補版本相符才能相容。例如，外掛程式版本 2.3.0.x 僅能與 OpenSearch 2.3.0 搭配使用。
{: .warning}

## 外掛程式相依性

某些外掛程式會擴展其他外掛程式的功能。如果某個外掛程式相依於另一個外掛程式，您必須在安裝相依外掛程式之前先安裝所需的相依項目。關於外掛程式相依性，請參閱 [manifest 檔案](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}.yml)。在此檔案中，每個外掛程式的相依項目都列在 `depends_on` 參數中。

## 相關文件

- [安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
