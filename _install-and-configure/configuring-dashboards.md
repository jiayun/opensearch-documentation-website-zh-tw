---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 OpenSearch Dashboards"
nav_order: 15
---

# 設定 OpenSearch Dashboards

OpenSearch Dashboards 會在您啟動叢集時，從 `opensearch_dashboards.yml` 組態檔案讀取設定。您可以在每個節點的 `/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml`（Docker）或 `/etc/opensearch-dashboards/opensearch_dashboards.yml`（大多數 Linux 發行版）中找到 `opensearch_dashboards.yml`。

如需 OpenSearch Dashboards 設定的相關資訊，請參閱範例 [`opensearch_dashboards.yml`](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml) 檔案。

部分 OpenSearch Dashboards 設定也可以在 UI 中變更，無須編輯 `opensearch_dashboards.yml`。如需詳細資訊，請參閱[進階設定]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)。