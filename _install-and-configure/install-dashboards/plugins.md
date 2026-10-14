---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理 OpenSearch Dashboards 外掛程式"
nav_order: 100
redirect_from: 
  - /dashboards/install/plugins/
---

# 管理 OpenSearch Dashboards 外掛程式

OpenSearch Dashboards 提供一個名為 `opensearch-dashboards-plugin` 的命令列工具，用於管理外掛程式。

## 必要條件

- 一個相容的 OpenSearch 叢集
- 該叢集上已[安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)對應的 OpenSearch 外掛程式
- 對應版本的 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/)（例如 OpenSearch Dashboards 2.3.0 可與 OpenSearch 2.3.0 搭配使用）

## 使用 `opensearch-dashboards-plugin` 工具

請從 OpenSearch Dashboards 安裝目錄執行 `opensearch-dashboards-plugin`，例如 RPM 與 Debian 安裝的 `/usr/share/opensearch-dashboards`。該工具拒絕以 `root` 使用者身分執行，並會傳回 `OpenSearch Dashboards should not be run as root` 錯誤。RPM 與 Debian 套件會以 `root` 擁有權安裝 `plugins` 目錄，因此在這類安裝中，請以 `sudo` 執行該工具並加上 `--allow-root` 選項，如本頁範例所示。對於 tarball 與 Windows 安裝，請以擁有安裝目錄的使用者身分執行該工具，且不使用 `sudo` 或 `--allow-root`。

使用 `opensearch-dashboards-plugin` 工具可以執行下列動作：

- [列出](#listing-installed-plugins)已安裝的外掛程式。
- [安裝](#installing-plugins)外掛程式。
- [移除](#removing-plugins)已安裝的外掛程式。

### 列出已安裝的外掛程式

若要從命令列檢視已安裝外掛程式的清單，請使用下列命令：

```bash
sudo bin/opensearch-dashboards-plugin list --allow-root
```
{% include copy.html %}

該命令會傳回已安裝外掛程式及其版本的清單：

```text
alertingDashboards@{{site.opensearch_dashboards_version}}.0
anomalyDetectionDashboards@{{site.opensearch_dashboards_version}}.0
assistantDashboards@{{site.opensearch_dashboards_version}}.0
customImportMapDashboards@{{site.opensearch_dashboards_version}}.0
flowFrameworkDashboards@{{site.opensearch_dashboards_version}}.0
indexManagementDashboards@{{site.opensearch_dashboards_version}}.0
investigationDashboards@{{site.opensearch_dashboards_version}}.0
mlCommonsDashboards@{{site.opensearch_dashboards_version}}.0
notificationsDashboards@{{site.opensearch_dashboards_version}}.0
observabilityDashboards@{{site.opensearch_dashboards_version}}.0
queryInsightsDashboards@{{site.opensearch_dashboards_version}}.0
queryWorkbenchDashboards@{{site.opensearch_dashboards_version}}.0
reportsDashboards@{{site.opensearch_dashboards_version}}.0
searchRelevanceDashboards@{{site.opensearch_dashboards_version}}.0
securityAnalyticsDashboards@{{site.opensearch_dashboards_version}}.0
securityDashboards@{{site.opensearch_dashboards_version}}.0
```

### 安裝外掛程式

若要安裝外掛程式，請提供該外掛程式 zip 檔案的 URL：

```bash
sudo bin/opensearch-dashboards-plugin install <plugin-zip-url> --allow-root
```
{% include copy.html %}

若要從主機上的 zip 檔案安裝外掛程式，請使用 `file://` 配置提供檔案路徑：

```bash
sudo bin/opensearch-dashboards-plugin install file:///<path-to-plugin-zip> --allow-root
```
{% include copy.html %}

外掛程式版本必須與您的 OpenSearch Dashboards 版本相符。如需更多資訊，請參閱[外掛程式相容性](#plugin-compatibility)。安裝外掛程式後，請重新啟動 OpenSearch Dashboards。

隨附外掛程式的下載 URL 列於 OpenSearch Dashboards 安裝目錄根目錄下的 `manifest.yml` 檔案中。如需更多資訊，請參閱[下載隨附外掛程式以進行離線安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#downloading-bundled-plugins-for-offline-installation)。

### 移除外掛程式

若要移除外掛程式，請使用下列命令：

```bash
sudo bin/opensearch-dashboards-plugin remove alertingDashboards --allow-root
```
{% include copy.html %}

然後從 `opensearch_dashboards.yml` 移除所有相關項目，並重新啟動 OpenSearch Dashboards。

### 更新外掛程式

`opensearch-dashboards-plugin` 工具不會更新外掛程式。若要更新外掛程式，請[移除舊版本](#removing-plugins)、[安裝新版本](#installing-plugins)，然後重新啟動 OpenSearch Dashboards。

## 可用的外掛程式

下表列出可用的 OpenSearch Dashboards 外掛程式。所有列出的外掛程式都包含在預設的 OpenSearch 發行版中。

| 外掛程式名稱 | 儲存庫 | 導入版本 |
| :--- | :--- | :--- |
| `alertingDashboards` | [alerting-dashboards-plugin](https://github.com/opensearch-project/alerting-dashboards-plugin) | 1.0.0 |
| `anomalyDetectionDashboards` | [anomaly-detection-dashboards-plugin](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin) | 1.0.0 |
| `assistantDashboards` | [dashboards-assistant](https://github.com/opensearch-project/dashboards-assistant) | 2.13.0 |
| `customImportMapDashboards` | [dashboards-maps](https://github.com/opensearch-project/dashboards-maps) | 2.2.0 |
| `flowFrameworkDashboards` | [dashboards-flow-framework](https://github.com/opensearch-project/dashboards-flow-framework) | 2.19.0 |
| `indexManagementDashboards` | [index-management-dashboards-plugin](https://github.com/opensearch-project/index-management-dashboards-plugin) | 1.0.0 |
| `investigationDashboards` | [dashboards-investigation](https://github.com/opensearch-project/dashboards-investigation) | 3.8.0 |
| `mlCommonsDashboards` | [ml-commons-dashboards](https://github.com/opensearch-project/ml-commons-dashboards) | 2.6.0 |
| `notificationsDashboards` | [dashboards-notifications](https://github.com/opensearch-project/dashboards-notifications) | 2.0.0 |
| `observabilityDashboards` | [dashboards-observability](https://github.com/opensearch-project/dashboards-observability) | 2.0.0 |
| `queryInsightsDashboards` | [query-insights-dashboards](https://github.com/opensearch-project/query-insights-dashboards) | 2.19.0 |
| `queryWorkbenchDashboards` | [query-workbench](https://github.com/opensearch-project/dashboards-query-workbench) | 1.0.0 |
| `reportsDashboards` | [dashboards-reporting](https://github.com/opensearch-project/dashboards-reporting) | 1.0.0 |
| `searchRelevanceDashboards` | [dashboards-search-relevance](https://github.com/opensearch-project/dashboards-search-relevance) | 2.4.0 |
| `securityAnalyticsDashboards` | [security-analytics-dashboards-plugin](https://github.com/opensearch-project/security-analytics-dashboards-plugin)| 2.4.0 |
| `securityDashboards` | [security-dashboards-plugin](https://github.com/opensearch-project/security-dashboards-plugin) | 1.0.0 |

_<sup>*</sup>`dashboardNotebooks` 已在 OpenSearch 1.2.0 發行時合併至 Observability 外掛程式。_<br>

## 外掛程式相容性

外掛程式的主要、次要與修補版本必須與 OpenSearch 的主要、次要與修補版本相符才能相容。例如，外掛程式版本 2.3.0.x 僅適用於 OpenSearch 2.3.0。
{: .warning}

## 外掛程式相依性

有些外掛程式會擴充其他外掛程式的功能。如果某個外掛程式相依於另一個外掛程式，您必須在安裝相依外掛程式之前先安裝所需的相依項。外掛程式的相依性請參閱[資訊清單檔案](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}.yml)。在該檔案中，每個外掛程式的相依性都列於 `depends_on` 參數中。

## 相關文件

- [安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
