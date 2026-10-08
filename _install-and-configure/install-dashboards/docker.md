---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Docker
parent: Installing OpenSearch Dashboards
nav_order: 5
redirect_from: 
  - /dashboards/install/docker/
  - /opensearch/install/docker-security/
---

# 使用 Docker 安裝 OpenSearch Dashboards

您可以使用 Docker 或 Docker Compose 來執行 OpenSearch Dashboards。使用 Docker Compose 的方法較簡單，因為範例 Compose 檔案會同時啟動 OpenSearch 和 OpenSearch Dashboards。

## 前置條件

使用 Docker 安裝 OpenSearch。如需更多資訊，請參閱 [使用 Docker 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/)。

## 使用 Docker 安裝 OpenSearch Dashboards

如果您已使用 `docker network create os-net` 定義網路，並使用以下命令啟動 OpenSearch：

```bash
docker run -d --name opensearch-node -p 9200:9200 -p 9600:9600 --network os-net -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<admin_password>" opensearchproject/opensearch:latest
```
{% include copy.html %}

接著您可以透過以下步驟啟動 OpenSearch Dashboards：

1. 啟動 OpenSearch Dashboards，並在 `OPENSEARCH_HOSTS` 環境變數中指定 OpenSearch 容器名稱：

    ```bash
    docker run -d --name osd \
      --network os-net \
      -p 5601:5601 \
      -e 'OPENSEARCH_HOSTS=["https://opensearch-node:9200"]' \
      opensearchproject/opensearch-dashboards:latest
    ```
    {% include copy.html %}

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## 使用 Docker Compose 安裝 OpenSearch Dashboards

[範例 `docker-compose.yml`]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#sample-docker-composeyml) 檔案包含一個 `opensearch-dashboards` 服務，因此 OpenSearch Dashboards 會與 OpenSearch 同時啟動。當您 [使用 Docker Compose 部署叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#deploy-an-opensearch-cluster-using-docker-compose) 時，不需要額外步驟來安裝 OpenSearch Dashboards。

在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## 自訂 OpenSearch Dashboards 組態

OpenSearch Dashboards 映像包含一個預設的 `opensearch_dashboards.yml` 檔案，可與示範安全性組態配合使用，因此大多數部署不需要變更它。若要變更設定，請將其作為環境變數傳遞。變數名稱為設定名稱的大寫形式，且將點號替換為底線。例如，`OPENSEARCH_HOSTS` 可設定 `opensearch.hosts`，而 `OPENSEARCH_REQUESTTIMEOUT` 可設定 `opensearch.requestTimeout`。

使用 `docker run` 時，請使用 `-e` 選項傳遞變數。使用 Docker Compose 時，請將變數新增至 `opensearch-dashboards` 服務的 `environment` 區段：

```yaml
opensearch-dashboards:
  environment:
    OPENSEARCH_HOSTS: '["https://opensearch-node1:9200","https://opensearch-node2:9200"]'
    OPENSEARCH_REQUESTTIMEOUT: 60000
```

並非所有設定都能以環境變數傳遞。若要使用不支援環境變數的設定，請建立您自己的 `opensearch_dashboards.yml` 檔案並將其掛載到容器中，以替換預設檔案。由於掛載的檔案會完全替換預設檔案，因此它必須包含 OpenSearch Dashboards 所需的所有設定，包括 `opensearch.hosts` 和連線憑證。範例請參閱 [包含自訂組態的完整 Docker Compose 範例]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#complete-docker-compose-example-with-custom-configuration)。

## 相關文件

- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
