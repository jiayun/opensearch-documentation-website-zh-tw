---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch Dashboards
nav_order: 1
has_children: false
nav_exclude: true
permalink: /dashboards/
redirect_from:
  - /dashboards/index/
start_cards:
- heading: 安裝 OpenSearch Dashboards
  description: 使用 Docker、Helm、套件管理員、tarball 安裝 OpenSearch Dashboards，或在 Windows 上安裝
  link: /install-and-configure/install-dashboards/index/
- heading: 在 Playground 中試用
  description: 無須安裝任何項目，即可在瀏覽器中探索 OpenSearch Dashboards
  link: https://playground.opensearch.org/app/home#/
getting_started_cards:
- heading: 入門
  description: 使用範例資料，逐步了解主要應用程式
  link: /dashboards/getting-started/
- heading: 瀏覽 OpenSearch Dashboards
  description: 了解首頁與左側導覽面板的版面配置
  link: /dashboards/navigating-ui/
---

# OpenSearch Dashboards

OpenSearch Dashboards 是 OpenSearch 的 Web UI。您可以使用它來搜尋與探索資料、建立視覺化與儀表板，以及管理叢集，而無須撰寫 API 請求。

{% include cards.html cards=page.start_cards %}

## 入門

{% include cards.html cards=page.getting_started_cards %}

## 新增資料

若要在 OpenSearch Dashboards 中使用資料，您可以將資料新增至 OpenSearch，或連線至資料的儲存位置：

- 將[資料匯入]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/) OpenSearch 索引。
- [連接資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)，例如其他 OpenSearch 叢集、Amazon S3 或 Prometheus，即可在不匯入資料的情況下查詢資料。

## 探索與視覺化資料

使用下列應用程式搜尋資料並以視覺方式呈現。下表列出各應用程式所使用的查詢語言。

| 應用程式 | 用途 | 查詢語言 |
| :--- | :--- | :--- |
| [Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/) | 搜尋、篩選與檢視資料。 | [DQL]({{site.url}}{{site.baseurl}}/dashboards/dql/) 或 [查詢字串 (Lucene)]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) |
| [Visualize]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/) | 透過點選式介面建立圖表、地圖、表格及其他視覺化。 | [DQL]({{site.url}}{{site.baseurl}}/dashboards/dql/) 或 [查詢字串 (Lucene)]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) |
| [Dashboards]({{site.url}}{{site.baseurl}}/dashboards/dashboard/) | 將多個視覺化合併至單一頁面，並一次篩選所有視覺化。 | [DQL]({{site.url}}{{site.baseurl}}/dashboards/dql/) 或 [查詢字串 (Lucene)]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) |
| [Query Workbench]({{site.url}}{{site.baseurl}}/dashboards/query-workbench/) | 執行隨選 SQL 與 PPL 查詢。 | [SQL]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql/) 或 [PPL]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/) |
| [Dev Tools]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/index/) | 從瀏覽器傳送 OpenSearch API 請求。 | [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) |

若已啟用[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)，您也可以撰寫 PPL 或 PromQL 查詢來建立視覺化。如需詳細資訊，請參閱[使用查詢建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)。

## 管理索引與快照

使用下列應用程式管理索引與快照。

| 應用程式 | 用途 |
| :--- | :--- |
| [Index Management]({{site.url}}{{site.baseurl}}/dashboards/im-dashboards/index/) | 管理索引、資料串流、別名、範本，以及 Index State Management 政策。 |
| [Snapshot Management]({{site.url}}{{site.baseurl}}/dashboards/sm-dashboards/) | 備份與還原叢集的索引與狀態。 |

## 可觀測性

若要在 OpenSearch Dashboards 中監控記錄檔、追蹤與指標，請參閱[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/index/)。若要為常見資料來源 (例如 NGINX 記錄檔) 設定預先建置的儀表板與視覺化，請參閱[整合]({{site.url}}{{site.baseurl}}/dashboards/integrations/index/)。

## 使用 AI 輔助

[OpenSearch Assistant]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/index/) 為 OpenSearch Dashboards 新增 AI 輔助功能。

## 設定與管理 OpenSearch Dashboards

視您的角色而定，您可以在兩個地方設定 OpenSearch Dashboards。

| 位置 | 使用者 | 可設定的項目 |
| :--- | :--- | :--- |
| [Dashboards Management]({{site.url}}{{site.baseurl}}/dashboards/management/management-index/)，UI 中的應用程式 | 具有必要權限的使用者 | [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)、[資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)、[已儲存物件]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)及[進階設定]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/) |
| `opensearch_dashboards.yml` 組態檔案 | 部署 OpenSearch Dashboards 且具有主機存取權的管理員 | 部署層級的設定，例如[自訂品牌]({{site.url}}{{site.baseurl}}/dashboards/branding/)、[網路壓縮]({{site.url}}{{site.baseurl}}/dashboards/compression/)及[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)。如需詳細資訊，請參閱[設定與管理]({{site.url}}{{site.baseurl}}/dashboards/settings-and-administration/)及[設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-dashboards/)。 |
