---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Tarball
parent: Installing OpenSearch Dashboards
nav_order: 30
redirect_from: 
  - /dashboards/install/tar/
---

# 從 tarball 安裝 OpenSearch Dashboards

## 前置條件

安裝 OpenSearch。如需更多資訊，請參閱 [從 tarball 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/)。

## 從 tarball 安裝 OpenSearch Dashboards

若要從 tarball 安裝 OpenSearch Dashboards，請執行以下步驟：

1. 從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載 tarball。

1. 將 TAR 檔案解壓縮到一個目錄並切換到該目錄：

   ```bash
   # x64
   tar -zxf opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.tar.gz
   cd opensearch-dashboards-{{site.opensearch_dashboards_version}}
   # ARM64
   tar -zxf opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.tar.gz
   cd opensearch-dashboards-{{site.opensearch_dashboards_version}}
   ```

1. 如有需要，請修改 `config/opensearch_dashboards.yml`。

1. 啟動 OpenSearch Dashboards：

   ```bash
   ./bin/opensearch-dashboards
   ```

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## 相關文件

- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
