---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝快速入門"
nav_order: 3
description: "使用 Docker 快速設定本機 OpenSearch 和 OpenSearch Dashboards 叢集，然後新增並搜尋範例資料以開始使用。"
redirect_from: 
  - /about/quickstart/
  - /opensearch/install/quickstart/
  - /quickstart/
---

# 安裝快速入門

OpenSearch 支援多種安裝方式：Docker、Debian、Helm、RPM、tarball 和 Windows。

本指南使用 [Docker](https://www.docker.com/) 進行快速的本機設定。如需其他安裝選項，請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 和[安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)。

本頁面上的組態僅供本機測試使用。這些組態會停用安全性或使用示範憑證，並透過 HTTP 提供 OpenSearch Dashboards。若要為正式環境設定 OpenSearch，請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 和[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。
{: .note }

開始使用的方式有兩種：

* [使用單一命令試用 OpenSearch](#option-1-try-opensearch-in-one-command) -- 非常適合快速示範。
* [設定自訂 Docker 叢集](#option-2-set-up-a-custom-docker-cluster) -- 適合需要更多控制權的情況。

## 先決條件

開始之前，請在您的電腦上安裝 [Docker](https://docs.docker.com/get-docker/)。

## 選項 1：使用一個命令試用 OpenSearch

使用此方法，只需最少的設定，即可在本機電腦上快速啟動 OpenSearch 和 OpenSearch Dashboards。此組態會停用安全性。

啟動 OpenSearch：

```bash
docker pull opensearchproject/opensearch:latest && docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "DISABLE_SECURITY_PLUGIN=true" --name opensearch opensearchproject/opensearch:latest
```
{% include copy.html %}

啟動 OpenSearch Dashboards：

```bash
docker pull opensearchproject/opensearch-dashboards:latest && docker run -d -p 5601:5601 --add-host=host.docker.internal:host-gateway -e "OPENSEARCH_HOSTS=http://host.docker.internal:9200" -e "DISABLE_SECURITY_DASHBOARDS_PLUGIN=true" --name opensearch-dashboards opensearchproject/opensearch-dashboards:latest
```
{% include copy.html %}

此過程可能需要一些時間。完成後，OpenSearch 會在連接埠 `9200` 上執行，OpenSearch Dashboards 則在連接埠 `5601` 上執行。若要確認 OpenSearch 正在執行，請傳送下列請求：

```bash
curl http://localhost:9200
```
{% include copy.html %}

您應該會收到類似下列內容的回應：

```json
{
  "name" : "a937e018cee5",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "GLAjAG6bTeWErFUy_d-CLw",
  "version" : {
    "distribution" : "opensearch",
    "number" : <version>,
    "build_type" : <build-type>,
    "build_hash" : <build-hash>,
    "build_date" : <build-date>,
    "build_snapshot" : false,
    "lucene_version" : <lucene-version>,
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

若要確認 OpenSearch Dashboards 已啟動，請在瀏覽器中前往 `http://localhost:5601/`。

## 選項 2：設定自訂 Docker 叢集

使用 [Docker Compose](https://docs.docker.com/compose/) 執行本機多節點 OpenSearch 和 OpenSearch Dashboards 叢集：

- [設定不含安全性的叢集](#set-up-a-cluster-without-security) -- 最適合本機開發。
- [設定含安全性的叢集](#set-up-a-cluster-with-security) -- 使用預設憑證安裝 OpenSearch，以試用含安全性的 OpenSearch。

### 設定不含安全性的叢集

此設定使用停用安全性的開發用 Docker Compose 檔案。

1. 為您的 OpenSearch 叢集建立目錄（例如 `opensearch-cluster`）。在此目錄中建立 `docker-compose.yml` 檔案，並將[開發用 Docker Compose 檔案]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#sample-docker-compose-file-for-development)的內容複製到此檔案中。

1. 執行下列命令以啟動叢集：

    ```bash
    docker compose up -d
    ```
    {% include copy.html %}

1. 檢查容器是否正在執行：

    ```bash
    docker compose ps
    ```
    {% include copy.html %}

    您應該會看到類似下列的輸出：

    ```bash
    NAME                    IMAGE                                            COMMAND                  SERVICE                 CREATED          STATUS          PORTS
    opensearch-dashboards   opensearchproject/opensearch-dashboards:latest   "./opensearch-dashbo…"   opensearch-dashboards   30 seconds ago   Up 30 seconds   0.0.0.0:5601->5601/tcp, [::]:5601->5601/tcp
    opensearch-node1        opensearchproject/opensearch:latest              "./opensearch-docker…"   opensearch-node1        30 seconds ago   Up 30 seconds   0.0.0.0:9200->9200/tcp, [::]:9200->9200/tcp, 9300/tcp, 0.0.0.0:9600->9600/tcp, [::]:9600->9600/tcp, 9650/tcp
    opensearch-node2        opensearchproject/opensearch:latest              "./opensearch-docker…"   opensearch-node2        30 seconds ago   Up 30 seconds   9200/tcp, 9300/tcp, 9600/tcp, 9650/tcp
    ```

1. 若要確認 OpenSearch 正在執行，請傳送下列請求：

    ```bash
    curl http://localhost:9200
    ```
    {% include copy.html %}

    您應該會收到類似[選項 1](#option-1-try-opensearch-in-one-command) 中的回應。

您現在可以開啟 `http://localhost:5601/` 來探索 OpenSearch Dashboards。

### 設定含安全性的叢集

此組態使用示範憑證啟用安全性，並需要額外的系統設定。

1. 在您的電腦上執行 OpenSearch 之前，應在主機上停用記憶體分頁和置換，以提升效能，並增加 OpenSearch 可用的記憶體對應數量。
    
    停用記憶體分頁和置換：
    
    ```bash
    sudo swapoff -a
    ```
    {% include copy.html %}

    編輯定義主機最大對應數量的 sysctl 組態檔案：

    ```bash
    sudo vi /etc/sysctl.conf
    ```
    {% include copy.html %}

    將最大對應數量設定為建議值 `262144`：
    
    ```bash
    vm.max_map_count=262144
    ```
    {% include copy.html %}

    重新載入核心參數：

    ```bash
    sudo sysctl -p
    ```  
    {% include copy.html %}

    如需詳細資訊，請參閱[重要的系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。

1. 將範例 Compose 檔案下載到您的主機。您可以使用 `curl` 和 `wget` 等命令列公用程式下載檔案，也可以使用網頁瀏覽器，從 OpenSearch Project documentation-website 儲存庫手動複製 [`docker-compose.yml`](https://github.com/opensearch-project/documentation-website/blob/{{site.opensearch_major_minor_version}}/assets/examples/docker-compose.yml)。

    若要使用 cURL，請傳送下列請求：

    ```bash
    curl -O https://raw.githubusercontent.com/opensearch-project/documentation-website/{{site.opensearch_major_minor_version}}/assets/examples/docker-compose.yml
    ```
    {% include copy.html %}

    若要使用 wget，請傳送下列請求：

    ```bash
    wget https://raw.githubusercontent.com/opensearch-project/documentation-website/{{site.opensearch_major_minor_version}}/assets/examples/docker-compose.yml
    ```
    {% include copy.html %}

1. 首先，建立自訂管理員密碼。在 `docker-compose.yml` 檔案所在的相同目錄中建立（或編輯）`.env` 檔案。此檔案會儲存 Docker Compose 在啟動容器時自動讀取的環境變數。新增下列這一行以定義管理員密碼：

    ```bash
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
    ```
    {% include copy.html %}

1. 在您的終端機應用程式中，前往包含您所下載之 `docker-compose.yml` 檔案的目錄，然後執行下列命令，以背景處理序的形式建立並啟動叢集：
    
    ```bash
    docker compose up -d
    ```
    {% include copy.html %}

1. 使用下列命令確認容器正在執行：

    ```bash
    docker compose ps
    ```
    {% include copy.html %}

    您應該會看到類似下列的輸出：

    ```bash
    NAME                    IMAGE                                            COMMAND                  SERVICE                 CREATED          STATUS          PORTS
    opensearch-dashboards   opensearchproject/opensearch-dashboards:latest   "./opensearch-dashbo…"   opensearch-dashboards   30 seconds ago   Up 30 seconds   0.0.0.0:5601->5601/tcp, [::]:5601->5601/tcp
    opensearch-node1        opensearchproject/opensearch:latest              "./opensearch-docker…"   opensearch-node1        30 seconds ago   Up 30 seconds   0.0.0.0:9200->9200/tcp, [::]:9200->9200/tcp, 9300/tcp, 0.0.0.0:9600->9600/tcp, [::]:9600->9600/tcp, 9650/tcp
    opensearch-node2        opensearchproject/opensearch:latest              "./opensearch-docker…"   opensearch-node2        30 seconds ago   Up 30 seconds   9200/tcp, 9300/tcp, 9600/tcp, 9650/tcp
    ```

1. 確認 OpenSearch 正在執行。由於預設的安全性組態使用示範憑證，您應該使用 `-k`（也可寫作 `--insecure`）來停用主機名稱檢查。使用 `-u` 傳遞預設的使用者名稱和密碼（`admin:<custom-admin-password>`）：

    ```bash
    curl https://localhost:9200 -ku admin:<custom-admin-password>
    ```
    {% include copy.html %}

    您應該會收到類似[選項 1](#option-1-try-opensearch-in-one-command) 中的回應。

您現在可以在執行 OpenSearch 叢集的同一部主機上，使用網頁瀏覽器開啟 `http://localhost:5601/` 來探索 OpenSearch Dashboards。請使用您在 `.env` 檔案中設定的自訂管理員密碼，以 `admin` 使用者身分登入。

## 常見問題

如果您的容器無法啟動或意外結束，請參閱 Docker 安裝指南中的[常見問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#common-issues)。

## 停止叢集

若要停止您在[選項 1](#option-1-try-opensearch-in-one-command) 中啟動的容器，請執行下列命令：

```bash
docker stop opensearch opensearch-dashboards
```
{% include copy.html %}

選項 1 不會掛載磁碟區，因此容器會在內部儲存您的資料。若要再次啟動容器並保留您的資料，請使用 `docker start` 取代 `docker stop`。使用 `docker rm` 移除容器會刪除其資料，包括您在後續教學中建立的所有索引。

若要停止您在[選項 2](#option-2-set-up-a-custom-docker-cluster) 中啟動的叢集，請在包含 `docker-compose.yml` 檔案的目錄中執行下列命令：

```bash
docker compose down
```
{% include copy.html %}

此命令會移除容器和網路，但會保留叢集用來儲存您資料的具名磁碟區，因此再次執行 `docker compose up -d` 即可還原叢集並保留您的資料。將 `-v` 加入 `docker compose down` 會刪除磁碟區及其中的資料。

## 其他安裝類型

除了 Docker 之外，您也可以在各種 Linux 發行版和 Windows 上安裝 OpenSearch 和 OpenSearch Dashboards。如需所有可用的安裝指南，請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 和[安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)。

## 延伸閱讀

您已成功部署自己的 OpenSearch 叢集與 OpenSearch Dashboards。若要更詳細地了解組態和功能，請參閱下列頁面：
- [關於 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/index/)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)

## 後續步驟

- 若要了解如何傳送請求至 OpenSearch，請參閱[與 OpenSearch 通訊]({{site.url}}{{site.baseurl}}/getting-started/communicate/)。
