---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Docker
parent: Installing OpenSearch
nav_order: 5
redirect_from: 
  - /opensearch/install/docker/
---

# 使用 Docker 安裝 OpenSearch

[Docker](https://www.docker.com/) 大幅簡化了設定與管理 OpenSearch 叢集的程序。您可以從 [Docker Hub](https://hub.docker.com/u/opensearchproject) 或 [Amazon Elastic Container Registry (Amazon ECR)](https://gallery.ecr.aws/opensearchproject/) 拉取官方映像檔，並使用 [Docker Compose](https://github.com/docker/compose) 以及本指南中提供的任一範例 Docker Compose 檔案快速部署叢集。有經驗的 OpenSearch 使用者可以透過建立自訂的 Docker Compose 檔案進一步自訂部署。

Docker 容器具有可攜性，可在任何支援 Docker 的相容主機上執行（例如 Linux、macOS 或 Windows）。與其他安裝方式（例如 [RPM]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/) 或手動安裝 [tar 封存檔]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/)，兩者在下載與解壓縮後都需要額外設定）相比，Docker 容器的可攜性提供了更大的彈性。

本指南假設您熟悉 Linux 命令列介面 (CLI) 的操作。您應該了解如何輸入命令、在目錄之間切換，以及編輯文字檔。如需 [Docker](https://www.docker.com/) 或 [Docker Compose](https://github.com/docker/compose) 的協助，請參閱其官方網站上的文件。
{:.note}

## 安裝 Docker 與 Docker Compose

請造訪[取得 Docker](https://docs.docker.com/get-docker/)，以取得為您的環境安裝與設定 Docker 的指引。如果您是使用 CLI 安裝 Docker Engine，Docker 預設不會對主機可用資源施加任何限制。視您的環境而定，您可能會希望在 Docker 中設定資源限制。相關資訊請參閱[記憶體、CPU 與 GPU 的執行階段選項](https://docs.docker.com/config/containers/resource_constraints/)。

Docker Desktop 使用者應開啟 Docker Desktop，選取 **Settings** → **Resources**，並將可用的主機記憶體設定為至少 4 GB。
{: .tip}

Docker Compose 是一種公用程式，可讓使用者以單一命令啟動多個容器。您在叫用 Docker Compose 時會傳遞一個檔案給它。Docker Compose 會讀取這些設定並啟動所要求的容器。Docker Compose 會隨 Docker Desktop 自動安裝，但在命令列環境中操作的使用者必須手動安裝 Docker Compose。您可以在官方的 [Docker Compose GitHub 頁面](https://github.com/docker/compose)上找到有關安裝 Docker Compose 的資訊。

在 Linux 上，您可以將 Docker Compose 作為 Docker 外掛程式安裝。如需更多資訊，請參閱[安裝 Docker Compose 外掛程式](https://docs.docker.com/compose/install/linux/)。本指南中的範例使用該外掛程式提供的 `docker compose` 命令。
{: .tip}

## 設定重要的主機設定
在使用 Docker 安裝 OpenSearch 之前，請先設定以下設定。這些是可能影響服務效能的最重要設定，如需更多資訊，請參閱[重要系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings){:target='\_blank'}。

### Linux 設定
在 Linux 環境中，請執行以下命令：

1. 停用主機上的記憶體分頁與交換，以提升效能：

   ```bash
   sudo swapoff -a
   ```
   {% include copy.html %}

1. 增加 OpenSearch 可用的記憶體對應數量。開啟 `sysctl` 組態檔：

   ```bash
   sudo vi /etc/sysctl.conf
   ```
   {% include copy.html %}

   新增以下一行，若該設定已存在則變更其值，然後儲存變更：

   ```bash
   vm.max_map_count=262144
   ```
   {% include copy.html %}

   重新載入核心參數：

   ```bash
   sudo sysctl -p
   ```
   {% include copy.html %}

   檢查該值以確認變更已套用：

   ```bash
   cat /proc/sys/vm/max_map_count
   ```
   {% include copy.html %}

### Windows 設定
對於透過 Docker Desktop 使用 WSL 的 Windows 工作負載，請在 Docker Desktop 的 WSL 發行版中設定 `vm.max_map_count`。首先，在該發行版中開啟一個 shell：

```bash
wsl -d docker-desktop
```
{% include copy.html %}

然後設定該值：

```bash
sysctl -w vm.max_map_count=262144
```
{% include copy.html %}

## 在 Docker 容器中執行 OpenSearch

官方 OpenSearch 映像檔託管於 [Docker Hub](https://hub.docker.com/u/opensearchproject/) 與 [Amazon ECR](https://gallery.ecr.aws/opensearchproject/)。如果您想檢視這些映像檔，可以使用 `docker pull` 個別拉取，如下列範例所示。

[Docker Hub](https://hub.docker.com/u/opensearchproject/)：
```bash
docker pull opensearchproject/opensearch:{{ site.opensearch_version | split: "." | first }}
```
{% include copy.html %}

```bash
docker pull opensearchproject/opensearch-dashboards:{{ site.opensearch_version | split: "." | first }}
```
{% include copy.html %}

[Amazon ECR](https://gallery.ecr.aws/opensearchproject/)：
```bash
docker pull public.ecr.aws/opensearchproject/opensearch:{{ site.opensearch_version | split: "." | first }}
```
{% include copy.html %}

```bash
docker pull public.ecr.aws/opensearchproject/opensearch-dashboards:{{ site.opensearch_version | split: "." | first }}
```
{% include copy.html %}

若要下載最新可用版本以外的特定 OpenSearch 或 OpenSearch Dashboards 版本，請在其被參照的位置修改映像檔標籤（在命令列或 Docker Compose 檔案中）。例如，`opensearchproject/opensearch:{{site.opensearch_version}}` 會拉取 OpenSearch {{site.opensearch_version}} 版。若要拉取最新版本，請使用 `opensearchproject/opensearch:latest`。可用的版本請參閱官方映像檔儲存庫。
{: .tip}

在繼續之前，您應該透過在單一容器中部署 OpenSearch，來驗證 Docker 是否正常運作。

1. 在 Docker 中啟動 OpenSearch。
    OpenSearch 2.12 或更新版本要求您在啟動時設定自訂管理員密碼。如需更多資訊，請參閱[設定自訂管理員密碼](#setting-a-custom-admin-password)。如果密碼強度不足，記錄檔中會回報錯誤，且 OpenSearch 會結束：
    ```bash
    docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>" opensearchproject/opensearch:latest
    ```
    舊版本在啟動時不包含密碼：
    ```bash
    # This command maps ports 9200 and 9600, sets the discovery type to "single-node" and requests the newest image of OpenSearch
    docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
    ```
1. 等待幾分鐘讓 OpenSearch 啟動後，向連接埠 `9200` 傳送請求。對於 2.12 之前的版本，預設的使用者名稱與密碼為 `admin`。
    ```bash
    curl https://localhost:9200 -ku admin:"<custom-admin-password>"
    ```
    {% include copy.html %}

    - 您應該會收到類似以下的回應：
      ```bash
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
1. 在停止執行中的容器之前，顯示所有執行中容器的清單，並複製您正在測試的 OpenSearch 節點的容器 ID。在以下範例中，容器 ID 為 `a937e018cee5`：
    ```bash
    docker container ls
    ```
    {% include copy.html %}

    回應會列出執行中的容器：

    ```bash
    CONTAINER ID   IMAGE                                 COMMAND                  CREATED          STATUS          PORTS                                                                NAMES
    a937e018cee5   opensearchproject/opensearch:latest   "./opensearch-docker…"   19 minutes ago   Up 19 minutes   0.0.0.0:9200->9200/tcp, 9300/tcp, 0.0.0.0:9600->9600/tcp, 9650/tcp   wonderful_boyd
    ```
1. 透過將容器 ID 傳遞給 `docker stop` 來停止執行中的容器。
    ```bash
    docker stop <containerId>
    ```
    {% include copy.html %}

請記住，`docker container ls` 不會列出已停止的容器。如果您想檢視已停止的容器，請使用 `docker container ls -a`。您可以使用 `docker container rm <containerId_1> <containerId_2> <containerId_3> [...]` 手動移除不需要的容器（傳遞所有要停止的容器 ID，以空格分隔），或者如果您想移除所有已停止的容器，可以使用較短的命令 `docker container prune`。
{: .tip}

## 使用 Docker Compose 部署 OpenSearch 叢集

雖然技術上可以透過一次建立一個容器的指令來建置 OpenSearch 叢集，但在 YAML 檔案中定義您的環境並讓 Docker Compose 管理叢集會容易得多。以下小節包含範例 YAML 檔案，您可以使用這些檔案來啟動包含 OpenSearch 與 OpenSearch Dashboards 的預先定義叢集。這些範例適合用於測試與開發，但不適合用於正式環境。如果您先前沒有使用 Docker Compose 的經驗，建議您先參閱 Docker [Compose 規格](https://docs.docker.com/compose/compose-file/)，以了解語法與格式的指引，再對範例中的字典結構進行任何變更。

定義環境的 YAML 檔案稱為 Docker Compose 檔案。根據預設，`docker-compose` 指令會先檢查您目前的目錄中是否有符合下列任何名稱的檔案：
- `docker-compose.yml`
- `docker-compose.yaml`
- `compose.yml`
- `compose.yaml`

如果目前的目錄中沒有這些檔案，`docker-compose` 指令就會失敗。

您可以在呼叫 `docker-compose` 時使用 `-f` 旗標來指定自訂的檔案位置與名稱：
```bash
# Use a relative or absolute path to the file.
docker compose -f /path/to/your-file.yml up
```

如果這是您第一次使用 Docker Compose 啟動 OpenSearch 叢集，請使用[範例 `docker-compose.yml` 檔案](#sample-docker-composeyml)。此檔案會建立一個包含三個容器的叢集：兩個執行 OpenSearch 服務的容器，以及一個執行 OpenSearch Dashboards 的容器。這些容器會透過名為 `opensearch-net` 的橋接網路進行通訊，並使用兩個磁碟區，每個 OpenSearch 節點各一個。由於此檔案並未明確停用示範安全性組態，因此會安裝自簽 TLS 憑證，並建立具有預設名稱與密碼的內部使用者。

### 設定自訂管理員密碼

從 OpenSearch 2.12 開始，設定示範安全性組態時必須提供自訂管理員密碼。請執行下列其中一項操作：

- 在執行 `docker-compose.yml` 之前，使用下列指令設定新的自訂管理員密碼：
  ```
  export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
  ```
  {% include copy.html %}
  
- 在與您的 `docker-compose.yml` 檔案相同的資料夾中建立 `.env` 檔案，並在其中設定 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 與高強度的密碼值。

### 密碼需求

您在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼必須符合長度下限、包含多種字元類別，並通過以熵為基礎的強度檢查。如需完整清單，請參閱[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。

### 範例 `docker-compose.yml`

將範例 Docker Compose 檔案下載到您主機的家目錄。您可以使用 `curl` 和 `wget` 等命令列工具下載該檔案，也可以使用網頁瀏覽器從 OpenSearch Project `documentation-website` 儲存庫手動複製 [`docker-compose.yml`](https://github.com/opensearch-project/documentation-website/blob/{{site.opensearch_major_minor_version}}/assets/examples/docker-compose.yml)。

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

此檔案是以 [`opensearch-build` 儲存庫](https://github.com/opensearch-project/opensearch-build/tree/main/docker/release/dockercomposefiles)中維護的 Docker Compose 檔案為基礎。

如果您在 compose 檔案中使用環境變數來覆寫 `opensearch_dashboards.yml` 設定，請使用全大寫字母並將句點取代為底線（例如，對於 `opensearch.hosts`，請使用 `OPENSEARCH_HOSTS`）。此行為與覆寫 `opensearch.yml` 設定不一致，後者的轉換只是變更賦值運算子（例如，`opensearch.yml` 中的 `discovery.type: single-node` 在 `docker-compose.yml` 中定義為 `discovery.type=single-node`）。
{: .note}

從您主機的家目錄（包含 `docker-compose.yml`）建立並以分離模式啟動容器：
```bash
docker compose up -d
```
{% include copy.html %}

確認服務容器已正確啟動：
```bash
docker compose ps
```
{% include copy.html %}

如果容器啟動失敗，您可以檢閱服務記錄檔：
```bash
# If you don't pass a service name, docker compose will show you logs from all of the nodes
docker compose logs <serviceName>
```
{% include copy.html %}

如需常見啟動錯誤的解決方法，請參閱[常見問題](#common-issues)。

從瀏覽器連線至 http://localhost:5601，以確認可存取 OpenSearch Dashboards。針對 OpenSearch 2.12 及更新版本，您必須使用已設定的使用者名稱與密碼。針對較早版本，預設的使用者名稱與密碼為 `admin`。在您自訂部署的安全性組態之前，我們不建議在可從公開網際網路存取的的主機上使用此組態。

請記住，`localhost` 無法從遠端存取。如果您要將這些容器部署到遠端主機，則需要建立網路連線，並將 `localhost` 取代為對應至該主機的 IP 或 DNS 記錄。
{: .note}

停止叢集中正在執行的容器：
```bash
docker compose down
```
{% include copy.html %}

`docker compose down` 會停止正在執行的容器，但不會移除主機上現有的 Docker 磁碟區。如果您不在意這些磁碟區的內容，請使用 `-v` 選項來刪除所有磁碟區，例如 `docker compose down -v`。
{: .tip}

## 設定 OpenSearch

OpenSearch 的 RPM 發行版需要大量的安裝後組態，而使用 Docker 執行 OpenSearch 叢集則可讓您在容器建立之前就先定義環境。無論您使用 Docker 或 Docker Compose 都可以這麼做。

例如，請看下列指令：
```bash
docker run \
  -p 9200:9200 -p 9600:9600 \
  -e "discovery.type=single-node" \
  -v /path/to/custom-opensearch.yml:/usr/share/opensearch/config/opensearch.yml \
  opensearchproject/opensearch:latest
```
{% include copy.html %}

檢閱此指令的每個部分，您可以看到它：
- 對應連接埠 `9200` 與 `9600`（`HOST_PORT`:`CONTAINER_PORT`）。
- 將 `discovery.type` 設為 `single-node`，讓此單一節點部署的啟動檢查不會失敗。
- 使用 [-v 旗標](https://docs.docker.com/engine/reference/commandline/run#mount-volume--v---read-only)將名為 `custom-opensearch.yml` 的本機檔案傳遞至容器，取代映像檔隨附的 `opensearch.yml` 檔案。
- 從 Docker Hub 請求 `opensearchproject/opensearch:latest` 映像檔。
- 執行容器。

如果您將此指令與[範例 `docker-compose.yml`](#sample-docker-composeyml)檔案相比較，可能會注意到一些常見設定，例如連接埠對應與映像檔參照。不過，此指令只會部署一個執行 OpenSearch 的容器，並不會為 OpenSearch Dashboards 建立容器。此外，如果您想使用自訂 TLS 憑證、使用者或角色，或定義其他磁碟區與網路，那麼這個「一行」指令很快就會變得過於龐大而不實用。這正是 Docker Compose 發揮效用之處。

當您使用 Docker Compose 建置 OpenSearch 叢集時，您可能會發現從主機將自訂組態檔案傳遞至容器，比在 `docker-compose.yml` 中逐一列舉每個設定更容易。類似於範例 `docker run` 指令使用 `-v` 旗標將主機的磁碟區掛載至容器，compose 檔案可以將要掛載的磁碟區指定為對應服務的子選項。下列截斷的 YAML 檔案示範如何將檔案或目錄掛載至容器。如需磁碟區用法與語法的完整資訊，請參閱 Docker 官方關於[磁碟區](https://docs.docker.com/storage/volumes/)的文件。

```yml
services:
  opensearch-node1:
    volumes:
      - opensearch-data1:/usr/share/opensearch/data
      - ./custom-opensearch.yml:/usr/share/opensearch/config/opensearch.yml
  opensearch-node2:
    volumes:
      - opensearch-data2:/usr/share/opensearch/data
      - ./custom-opensearch.yml:/usr/share/opensearch/config/opensearch.yml
  opensearch-dashboards:
    volumes:
      - ./custom-opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml
```
{% include copy.html %}

### 開發用的 Docker Compose 範例檔案

如果您想以範例為基礎建立自己的 compose 檔案，請檢視下列 `docker-compose.yml` 範例檔案。此範例檔案會建立兩個 OpenSearch 節點和一個 OpenSearch Dashboards 節點，並停用 Security 外掛程式。您可以在檢視[設定基本安全性設定](#configuring-basic-security-settings)時，將此範例檔案作為起點。
```yml
services:
  opensearch-node1:
    image: opensearchproject/opensearch:latest
    container_name: opensearch-node1
    environment:
      - cluster.name=opensearch-cluster # Name the cluster
      - node.name=opensearch-node1 # Name the node that will run in this container
      - discovery.seed_hosts=opensearch-node1,opensearch-node2 # Nodes to look for when discovering the cluster
      - cluster.initial_cluster_manager_nodes=opensearch-node1,opensearch-node2 # Nodes eligibile to serve as cluster manager
      - bootstrap.memory_lock=true # Disable JVM heap memory swapping
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" # Set min and max JVM heap sizes to at least 50% of system RAM
      - "DISABLE_INSTALL_DEMO_CONFIG=true" # Prevents execution of bundled demo script which installs demo certificates and security configurations to OpenSearch
      - "DISABLE_SECURITY_PLUGIN=true" # Disables Security plugin
    ulimits:
      memlock:
        soft: -1 # Set memlock to unlimited (no soft or hard limit)
        hard: -1
      nofile:
        soft: 65536 # Maximum number of open files for the opensearch user - set to at least 65536
        hard: 65536
    volumes:
      - opensearch-data1:/usr/share/opensearch/data # Creates volume called opensearch-data1 and mounts it to the container
    ports:
      - 9200:9200 # REST API
      - 9600:9600 # Performance Analyzer
    networks:
      - opensearch-net # All of the containers will join the same Docker bridge network
  opensearch-node2:
    image: opensearchproject/opensearch:latest
    container_name: opensearch-node2
    environment:
      - cluster.name=opensearch-cluster # Name the cluster
      - node.name=opensearch-node2 # Name the node that will run in this container
      - discovery.seed_hosts=opensearch-node1,opensearch-node2 # Nodes to look for when discovering the cluster
      - cluster.initial_cluster_manager_nodes=opensearch-node1,opensearch-node2 # Nodes eligibile to serve as cluster manager
      - bootstrap.memory_lock=true # Disable JVM heap memory swapping
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" # Set min and max JVM heap sizes to at least 50% of system RAM
      - "DISABLE_INSTALL_DEMO_CONFIG=true" # Prevents execution of bundled demo script which installs demo certificates and security configurations to OpenSearch
      - "DISABLE_SECURITY_PLUGIN=true" # Disables Security plugin
    ulimits:
      memlock:
        soft: -1 # Set memlock to unlimited (no soft or hard limit)
        hard: -1
      nofile:
        soft: 65536 # Maximum number of open files for the opensearch user - set to at least 65536
        hard: 65536
    volumes:
      - opensearch-data2:/usr/share/opensearch/data # Creates volume called opensearch-data2 and mounts it to the container
    networks:
      - opensearch-net # All of the containers will join the same Docker bridge network
  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    container_name: opensearch-dashboards
    ports:
      - 5601:5601 # Map host port 5601 to container port 5601
    expose:
      - "5601" # Expose port 5601 for web access to OpenSearch Dashboards
    environment:
      - 'OPENSEARCH_HOSTS=["http://opensearch-node1:9200","http://opensearch-node2:9200"]'
      - "DISABLE_SECURITY_DASHBOARDS_PLUGIN=true" # disables security dashboards plugin in OpenSearch Dashboards
    networks:
      - opensearch-net

volumes:
  opensearch-data1:
  opensearch-data2:

networks:
  opensearch-net:
```
{% include copy.html %}

### 設定基本安全性設定

在將 OpenSearch 叢集開放給外部主機之前，建議先檢視部署的安全性組態。您可能記得第一個[`docker-compose.yml` 範例](#sample-docker-composeyml)檔案中，除非透過設定 `DISABLE_SECURITY_PLUGIN=true` 停用，否則隨附的指令碼會將預設的示範安全性組態套用至叢集中的節點。由於此組態僅供示範用途，預設的使用者名稱和密碼是公開已知的。因此，我們建議您建立自己的安全性組態檔案，並使用 `volumes` 將這些檔案傳遞至容器。有關 OpenSearch 安全性設定的具體指引，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。

若要在組態中使用自己的憑證，請將所有必要的憑證加入 compose 檔案的 volumes 區段：
```yml
volumes:
  - ./root-ca.pem:/usr/share/opensearch/config/root-ca.pem
  - ./admin.pem:/usr/share/opensearch/config/admin.pem
  - ./admin-key.pem:/usr/share/opensearch/config/admin-key.pem
  - ./node1.pem:/usr/share/opensearch/config/node1.pem
  - ./node1-key.pem:/usr/share/opensearch/config/node1-key.pem
```
{% include copy.html %}

當您使用 Docker Compose volumes 將 TLS 憑證加入 OpenSearch 節點時，也應包含一個定義這些憑證的自訂 `opensearch.yml` 檔案。例如：
```yml
volumes:
  - ./root-ca.pem:/usr/share/opensearch/config/root-ca.pem
  - ./admin.pem:/usr/share/opensearch/config/admin.pem
  - ./admin-key.pem:/usr/share/opensearch/config/admin-key.pem
  - ./node1.pem:/usr/share/opensearch/config/node1.pem
  - ./node1-key.pem:/usr/share/opensearch/config/node1-key.pem
  - ./custom-opensearch.yml:/usr/share/opensearch/config/opensearch.yml
```
{% include copy.html %}

請記住，您在 compose 檔案中指定的憑證必須與自訂 `opensearch.yml` 檔案中定義的憑證相同。您應將根憑證、管理員憑證和節點憑證替換為自己的憑證。如需更多資訊，請參閱[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。
```yml
plugins.security.ssl.transport.pemcert_filepath: node1.pem
plugins.security.ssl.transport.pemkey_filepath: node1-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
plugins.security.ssl.http.pemcert_filepath: node1.pem
plugins.security.ssl.http.pemkey_filepath: node1-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem
plugins.security.authcz.admin_dn:
  - CN=admin,OU=SSL,O=Test,L=Test,C=DE
```
{% include copy.html %}

設定安全性設定之後，您的自訂 `opensearch.yml` 檔案可能類似於下列範例，其中加入了 TLS 憑證與管理員憑證的辨別名稱 (DN)、定義了幾項權限，並啟用了詳細的稽核記錄：
```yml
plugins.security.ssl.transport.pemcert_filepath: node1.pem
plugins.security.ssl.transport.pemkey_filepath: node1-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
transport.ssl.enforce_hostname_verification: false
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: node1.pem
plugins.security.ssl.http.pemkey_filepath: node1-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem
plugins.security.allow_default_init_securityindex: true
plugins.security.authcz.admin_dn:
  - CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA
plugins.security.nodes_dn:
  - 'CN=N,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
plugins.security.audit.type: internal_opensearch
plugins.security.enable_snapshot_restore_privilege: true
plugins.security.check_snapshot_restore_write_privileges: true
plugins.security.restapi.roles_enabled: ["all_access", "security_rest_api_access"]
cluster.routing.allocation.disk.threshold_enabled: false
opendistro_security.audit.config.disabled_rest_categories: NONE
opendistro_security.audit.config.disabled_transport_categories: NONE
```
{% include copy.html %}

完整的設定清單請參閱[安全性]({{site.url}}{{site.baseurl}}/security/configuration/index/)。

您可以使用相同的程序，在 `/usr/share/opensearch/config/opensearch-security/config.yml` 中指定[後端組態]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)，並在其各自的 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)中定義新的內部使用者、角色、對應、動作群組和租用戶。

#### 使用自訂組態的完整 Docker Compose 範例

此範例使用 `${OS_VER}` 與 `${OSD_VER}` 環境變數來指定 OpenSearch 與 OpenSearch Dashboards 的版本。若任一變數未設定，Docker Compose 會失敗並出現 `invalid reference format` 錯誤。使用此範例之前，請先匯出變數以設定版本：

```bash
export OS_VER={{ site.opensearch_version }}
export OSD_VER={{ site.opensearch_dashboards_version }}
```
{% include copy.html %}

或者，在與 `docker-compose.yml` 相同的目錄中建立 `.env` 檔案：

```bash
OS_VER={{ site.opensearch_version }}
OSD_VER={{ site.opensearch_dashboards_version }}
```
{% include copy.html %}

建議在正式環境部署中使用環境變數或明確的版本標籤（例如 `{{ site.opensearch_version }}`），以確保叢集中各節點版本一致，並避免非預期的更新。
{: .tip}

在建立您自己的憑證、`internal_users.yml`、`roles.yml`、`roles_mapping.yml` 以及其餘安全性組態檔案之後，您的 `docker-compose.yaml` 檔案應類似如下：

```yaml
services:
  opensearch-node1:
    image: opensearchproject/opensearch:${OS_VER}
    container_name: opensearch-node1_${OS_VER}
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node1
      - discovery.seed_hosts=opensearch-node1,opensearch-node2,opensearch-node3
      - cluster.initial_master_nodes=opensearch-node1,opensearch-node2,opensearch-node3
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - ./opensearch.yml:/usr/share/opensearch/config/opensearch.yml
      - ./esnode.pem:/usr/share/opensearch/config/esnode.pem
      - ./esnode-key.pem:/usr/share/opensearch/config/esnode-key.pem
      - ./root-ca.pem:/usr/share/opensearch/config/root-ca.pem
      - ./kirk-key.pem:/usr/share/opensearch/config/kirk-key.pem
      - ./kirk.pem:/usr/share/opensearch/config/kirk.pem
      - ./config.yml:/usr/share/opensearch/config/opensearch-security/config.yml
      - ./roles_mapping.yml:/usr/share/opensearch/config/opensearch-security/roles_mapping.yml
      - ./roles.yml:/usr/share/opensearch/config/opensearch-security/roles.yml
      - ./action_groups.yml:/usr/share/opensearch/config/opensearch-security/action_groups.yml
      - ./allowlist.yml:/usr/share/opensearch/config/opensearch-security/allowlist.yml
      - ./audit.yml:/usr/share/opensearch/config/opensearch-security/audit.yml
      - ./internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml
      - ./nodes_dn.yml:/usr/share/opensearch/config/opensearch-security/nodes_dn.yml
      - ./tenants.yml:/usr/share/opensearch/config/opensearch-security/tenants.yml
    ports:
      - 9201:9200
      - 9600:9600
    networks:
      - opensearch-net

  opensearch-node2:
    image: opensearchproject/opensearch:${OS_VER}
    container_name: opensearch-node2_${OS_VER}
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node2
      - discovery.seed_hosts=opensearch-node1,opensearch-node2,opensearch-node3
      - cluster.initial_master_nodes=opensearch-node1,opensearch-node2,opensearch-node3
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - ./opensearch.yml:/usr/share/opensearch/config/opensearch.yml
      - ./esnode.pem:/usr/share/opensearch/config/esnode.pem
      - ./esnode-key.pem:/usr/share/opensearch/config/esnode-key.pem
      - ./root-ca.pem:/usr/share/opensearch/config/root-ca.pem
      - ./kirk-key.pem:/usr/share/opensearch/config/kirk-key.pem
      - ./kirk.pem:/usr/share/opensearch/config/kirk.pem
      - ./config.yml:/usr/share/opensearch/config/opensearch-security/config.yml
      - ./roles_mapping.yml:/usr/share/opensearch/config/opensearch-security/roles_mapping.yml
      - ./roles.yml:/usr/share/opensearch/config/opensearch-security/roles.yml
      - ./action_groups.yml:/usr/share/opensearch/config/opensearch-security/action_groups.yml
      - ./allowlist.yml:/usr/share/opensearch/config/opensearch-security/allowlist.yml
      - ./audit.yml:/usr/share/opensearch/config/opensearch-security/audit.yml
      - ./internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml
      - ./nodes_dn.yml:/usr/share/opensearch/config/opensearch-security/nodes_dn.yml
      - ./tenants.yml:/usr/share/opensearch/config/opensearch-security/tenants.yml
    ports:
      - 9200:9200
    networks:
      - opensearch-net

  opensearch-node3:
    image: opensearchproject/opensearch:${OS_VER}
    container_name: opensearch-node3_${OS_VER}
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node3
      - discovery.seed_hosts=opensearch-node1,opensearch-node2,opensearch-node3
      - cluster.initial_master_nodes=opensearch-node1,opensearch-node2,opensearch-node3
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - ./opensearch.yml:/usr/share/opensearch/config/opensearch.yml
      - ./esnode.pem:/usr/share/opensearch/config/esnode.pem
      - ./esnode-key.pem:/usr/share/opensearch/config/esnode-key.pem
      - ./root-ca.pem:/usr/share/opensearch/config/root-ca.pem
      - ./kirk-key.pem:/usr/share/opensearch/config/kirk-key.pem
      - ./kirk.pem:/usr/share/opensearch/config/kirk.pem
      - ./config.yml:/usr/share/opensearch/config/opensearch-security/config.yml
      - ./roles_mapping.yml:/usr/share/opensearch/config/opensearch-security/roles_mapping.yml
      - ./roles.yml:/usr/share/opensearch/config/opensearch-security/roles.yml
      - ./action_groups.yml:/usr/share/opensearch/config/opensearch-security/action_groups.yml
      - ./allowlist.yml:/usr/share/opensearch/config/opensearch-security/allowlist.yml
      - ./audit.yml:/usr/share/opensearch/config/opensearch-security/audit.yml
      - ./internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml
      - ./nodes_dn.yml:/usr/share/opensearch/config/opensearch-security/nodes_dn.yml
      - ./tenants.yml:/usr/share/opensearch/config/opensearch-security/tenants.yml
    ports:
      - 9202:9200
    networks:
      - opensearch-net

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:${OSD_VER}
    container_name: opensearch-dashboards_${OSD_VER}
    volumes:
      - ./opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml
      - ./opensearch_dashboards.crt:/usr/share/opensearch-dashboards/config/opensearch_dashboards.crt
      - ./opensearch_dashboards.key:/usr/share/opensearch-dashboards/config/opensearch_dashboards.key
    ports:
      - 5601:5601
    expose:
      - "5601"
    environment:
      OPENSEARCH_HOSTS: '["https://opensearch-node1:9200", "https://opensearch-node2:9200", "https://opensearch-node3:9200" ]'
    networks:
      - opensearch-net
    depends_on:
      - opensearch-node1
      - opensearch-node2
      - opensearch-node3

networks:
  opensearch-net:

```
{% include copy.html %}

使用 Docker Compose 啟動叢集：
```bash
docker compose up -d
```
{% include copy.html %}

`.env` 檔案中提供的 `admin` 使用者密碼，會被 `internal_users.yml` 檔案中提供的密碼覆寫。
{: .note}

### 使用外掛程式

若要使用帶有自訂外掛程式的 OpenSearch 映像，您必須先建立 [`Dockerfile`](https://docs.docker.com/engine/reference/builder/)。請參閱官方 Docker 文件以取得建立 Dockerfile 的相關資訊。
```
FROM opensearchproject/opensearch:latest
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch <pluginId>
```

然後執行下列命令：
```bash
# Build an image from a Dockerfile
docker build --tag=opensearch-custom-plugin .
# Start the container from the custom image
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>" -v /usr/share/opensearch/data opensearch-custom-plugin
```

或者，您可能想在部署映像之前從中移除外掛程式。此範例 Dockerfile 會移除 Security 外掛程式：
```
FROM opensearchproject/opensearch:latest
RUN /usr/share/opensearch/bin/opensearch-plugin remove opensearch-security
```
{% include copy.html %}

您也可以使用 Dockerfile 傳入自己的憑證，以供 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security/)使用：
```
FROM opensearchproject/opensearch:latest
COPY --chown=opensearch:opensearch opensearch.yml /usr/share/opensearch/config/
COPY --chown=opensearch:opensearch my-key-file.pem /usr/share/opensearch/config/
COPY --chown=opensearch:opensearch my-certificate-chain.pem /usr/share/opensearch/config/
COPY --chown=opensearch:opensearch my-root-cas.pem /usr/share/opensearch/config/
```
{% include copy.html %}

## 常見問題

如果您的容器無法啟動或意外結束，請參閱這些常見問題與建議的解決方案。

若問題可能發生於任何安裝方式，例如對 HTTPS 端點發出 HTTP 請求，或管理員密碼遭拒，請參閱[常見問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)。

### Docker 命令需要較高的權限

將您的使用者加入 `docker` 使用者群組，即可免除使用 `sudo` 執行 Docker 命令的需求。如需詳細資訊，請參閱 Docker 的 [Linux 安裝後步驟](https://docs.docker.com/engine/install/linux-postinstall/)。

```bash
sudo usermod -aG docker $USER
```
{% include copy.html %}

### 錯誤訊息：「max virtual memory areas vm.max_map_count [65530] is too low」

如果主機的 `vm.max_map_count` 設定太低，OpenSearch 將無法啟動。請在主機機器上設定 `vm.max_map_count`，而非在容器中設定，如 [Linux 設定](#linux-settings)所述。如需詳細資訊，請參閱[常見問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#error-message-max-virtual-memory-areas-vmmax_map_count-65530-is-too-low)。

### 錯誤訊息：「local node does not have quorum in voting configuration」

[範例 `docker-compose.yml`](#sample-docker-composeyml) 檔案中的資料磁碟區會儲存雙節點叢集的狀態。如果您變更該檔案以使用 `discovery.type: single-node` 執行單一節點，但保留現有的磁碟區，OpenSearch 將無法啟動，並記錄類似下列的錯誤：

```
cannot start with [discovery.type] set to [single-node] when local node does not have quorum in voting configuration
```

若要修正此錯誤，請移除現有的磁碟區：

```bash
docker compose down -v
```
{% include copy.html %}

`docker compose down -v` 命令會刪除儲存在磁碟區中的所有資料。
{: .warning}

然後再次啟動叢集：

```bash
docker compose up -d
```
{% include copy.html %}

## 相關文件

- [準備正式環境的叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [Performance Analyzer]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/index/)
- [安裝與設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [關於 OpenSearch 中的安全性]({{site.url}}{{site.baseurl}}/security/index/)
