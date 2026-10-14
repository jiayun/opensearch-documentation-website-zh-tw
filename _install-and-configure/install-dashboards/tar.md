---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "TAR 封存檔"
parent: Installing OpenSearch Dashboards
nav_order: 30
redirect_from: 
  - /dashboards/install/tar/
---

# 從 tarball 安裝 OpenSearch Dashboards

## 必要條件

安裝 OpenSearch。如需更多資訊，請參閱[從 tarball 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/)。

## 從 tarball 安裝 OpenSearch Dashboards

若要從 tarball 安裝 OpenSearch Dashboards，請依照下列步驟操作：

1. 從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載 tarball，或使用命令列下載，例如使用 `curl`。

   若為 x64 主機，請使用下列命令：

   ```bash
   curl -fsSLO https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.tar.gz
   ```
   {% include copy.html %}

   若為 ARM64 主機，請使用下列命令：

   ```bash
   curl -fsSLO https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.tar.gz
   ```
   {% include copy.html %}

1. 將 TAR 檔案解壓縮至某個目錄。

   若為 x64 主機，請使用下列命令：

   ```bash
   tar -zxf opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.tar.gz
   ```
   {% include copy.html %}

   若為 ARM64 主機，請使用下列命令：

   ```bash
   tar -zxf opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.tar.gz
   ```
   {% include copy.html %}

   然後切換至解壓縮後的目錄：

   ```bash
   cd opensearch-dashboards-{{site.opensearch_dashboards_version}}
   ```
   {% include copy.html %}

1. 啟動 OpenSearch Dashboards：

   ```bash
   ./bin/opensearch-dashboards
   ```
   {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`，並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行於遠端主機，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。OpenSearch Dashboards 可能需要約 1 分鐘才會啟動。如需更多資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

預設情況下，OpenSearch Dashboards 會以 `kibanaserver` 使用者身分連線至位於 `https://localhost:9200` 的 OpenSearch，並且僅接受來自其執行所在主機的連線。若要變更這些設定，請編輯 `config/opensearch_dashboards.yml`。如需更多資訊，請參閱[設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-dashboards/)。
{: .note}

## 相關文件

- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
