---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝 OpenSearch Dashboards"
parent: Getting started
nav_order: 10
---

# 安裝 OpenSearch Dashboards

OpenSearch Dashboards 是 OpenSearch 的使用者介面。若要使用您自己的執行個體跟著教學操作，請依照下列步驟安裝 OpenSearch 和 OpenSearch Dashboards。

## 步驟 1：安裝 OpenSearch 和 OpenSearch Dashboards

請選擇下列其中一個選項：

- 若要使用 Docker 試用 OpenSearch 和 OpenSearch Dashboards，請依照[安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/)操作。

- 若要在正式環境中安裝 OpenSearch Dashboards，請先使用[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 中的其中一種方法安裝 OpenSearch，再使用[安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/) 中的其中一種方法安裝 OpenSearch Dashboards。

## 步驟 2（選用）：設定 OpenSearch Dashboards

您可以在 `opensearch_dashboards.yml` 檔案中設定 OpenSearch Dashboards 的設定。此檔案控制伺服器選項、驗證、外掛程式設定，以及[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)等功能。變更組態檔案後，請重新啟動 OpenSearch Dashboards，變更才會生效。

如需完整的設定清單，請參閱[設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-dashboards/)。

部分設定也可以直接在 OpenSearch Dashboards 中變更，而不必編輯 `opensearch_dashboards.yml`。如需詳細資訊，請參閱[進階設定]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)。

## 後續步驟

- 請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/getting-started/access/)，了解如何瀏覽介面。
