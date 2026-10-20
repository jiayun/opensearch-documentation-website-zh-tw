---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "滾動升級實驗"
parent: Rolling upgrade
nav_order: 10
redirect_from:
  - /upgrade-opensearch/appendix/rolling-upgrade-lab/
  - /install-and-configure/upgrade-opensearch/appendix/index/
  - /install-and-configure/upgrade-opensearch/appendix/
  - /install-and-configure/upgrade-opensearch/appendix/rolling-upgrade-lab/
  - /migrate-or-upgrade/rolling-upgrade/appendix/
  - /migrate-or-upgrade/rolling-upgrade/appendix/rolling-upgrade-lab/
---

# 滾動升級實驗

您可以在自己的相容主機上依照下列步驟，重建 OpenSearch Project 用於測試[滾動升級]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/)的相同叢集狀態。如果您想在開發環境中測試升級流程，這個練習會很有幫助。

在本實驗中，您會在 Docker 中部署一個四節點的 OpenSearch 2.19.6 叢集和一個 OpenSearch Dashboards 2.19.6 節點，新增資料與安全性設定，備份叢集，然後將每個節點升級至 OpenSearch 3.9.0 與 OpenSearch Dashboards 3.9.0。本實驗中的命令與範例回應皆專屬於這些版本。

本實驗使用的步驟已在 [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/) `m6i.xlarge` 執行個體（4 個 vCPU 與 16 GiB 記憶體）上驗證，使用 [Amazon Linux 2023](https://aws.amazon.com/linux/amazon-linux-2023/) 核心 `6.18.54-121.166.amzn2023.x86_64` 版本與 [Docker](https://www.docker.com/) `25.0.16` 版本。該執行個體已掛載 50 GiB gp3 [Amazon EBS](https://aws.amazon.com/ebs/) 根磁碟區。這些規格僅供參考，並不代表 OpenSearch 或 OpenSearch Dashboards 的硬體需求。

本實驗已考量升級至 OpenSearch 3.x 的下列需求：

- 叢集在升級至 3.x 之前必須執行 OpenSearch 2.19.0 或更新版本。OpenSearch 3.x 無法讀取在 OpenSearch 1.x 中建立的索引，因此本實驗從執行 2.19.6 的叢集開始。如需更多資訊，請參閱[重大變更]({{site.url}}{{site.baseurl}}/breaking-changes/#300)。
- 從 OpenSearch 2.12 開始，`admin` 使用者需要自訂密碼。本實驗的部署指令碼會從 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 環境變數讀取密碼。
- OpenSearch 3.x 不在連接埠 9600 提供 Performance Analyzer API，因此本實驗不會發布連接埠 9600。

本程序中對主機上 `$HOME` 路徑的參照以波狀字元（「~」）表示，以提升指示的可攜性。如果您偏好指定絕對路徑，請修改 `upgrade-demo-cluster-2.19-to-3.sh` 中定義並在本文相關命令中使用的磁碟區路徑，以反映您的環境。

## 設定環境

當您依照本文件中的步驟操作時，您會使用我們提供的指令碼定義數個 Docker 資源，包括容器、磁碟區，以及專用的 Docker 網路。如果您想重新開始整個流程，可以使用下列命令清理您的環境：

```bash
docker container stop $(docker container ls -aqf name=os-); \
	docker container rm $(docker container ls -aqf name=os-); \
	docker volume rm -f $(docker volume ls -q | grep -E 'data-0|repo-0'); \
	docker network rm opensearch-dev-net; \
	rm -rf ~/deploy
```
{% include copy.html %}

此命令會移除名稱符合規則表達式 `os-*` 的容器、符合 `data-0*` 與 `repo-0*` 的資料磁碟區、名為 `opensearch-dev-net` 的 Docker 網路，以及 `~/deploy` 目錄，該目錄包含您在本實驗中建立的 TLS 憑證、組態檔案與備份。如果您的主機上還有其他正在執行的 Docker 資源，您應檢視並修改此命令，以免不慎移除其他資源。此命令不會還原主機組態的變更，例如記憶體置換行為。
{: .warning}

選定主機後，您就可以開始進行本實驗：

1. 為您的 Linux 發行版與系統架構安裝對應版本的 [Docker Engine](https://docs.docker.com/engine/install/)。例如，在 Amazon Linux 2023 上，從發行版儲存庫安裝 Docker、啟動 Docker 服務，並將您的使用者加入 `docker` 群組：
   ```bash
   sudo dnf install -y docker && \
      sudo systemctl enable --now docker && \
      sudo usermod -aG docker $USER
   ```
   {% include copy.html %}

   請登出後再重新登入，讓群組成員資格生效。
1. 在主機上設定[重要的系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)：
   1. 停用主機上的記憶體分頁與置換，以提升效能：
      ```bash
      sudo swapoff -a
      ```
      {% include copy.html %}
   1. 在 `sysctl` 組態檔案中加入 `vm.max_map_count` 設定，以增加 OpenSearch 可用的記憶體映射數量：
      ```bash
      echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf
      ```
      {% include copy.html %}
   1. 套用組態變更：
      ```bash
      sudo sysctl -p
      ```
      {% include copy.html %}

      回應應類似下列內容：

      ```bash
      vm.max_map_count = 262144
      ```
1. 在您的家目錄中建立名為 `deploy` 的新目錄，然後切換至該目錄。您將在部署指令碼、組態檔案與 TLS 憑證的路徑中使用 `~/deploy`：
   ```bash
   mkdir ~/deploy && cd ~/deploy
   ```
   {% include copy.html %}
1. 從 OpenSearch Project 的 [`documentation-website`](https://github.com/opensearch-project/documentation-website) 儲存庫下載 `upgrade-demo-cluster-2.19-to-3.sh`：
   ```bash
   wget https://raw.githubusercontent.com/opensearch-project/documentation-website/main/assets/examples/upgrade-demo-cluster-2.19-to-3.sh
   ```
   {% include copy.html %}
1. 設定 `admin` 使用者的密碼。請將 `<custom-admin-password>` 替換為您自行選擇的強式密碼。單引號可避免 shell 解譯密碼中的特殊字元：
   ```bash
   export OPENSEARCH_INITIAL_ADMIN_PASSWORD='<custom-admin-password>'
   ```
   {% include copy.html %}

   您會在本實驗的各種命令中，搭配使用者名稱 `admin` 使用此密碼。
1. 不需任何修改即可執行此指令碼，以部署四個執行 OpenSearch 2.19.6 的容器，以及一個執行 OpenSearch Dashboards 2.19.6 的容器，並使用自訂的自簽 TLS 憑證與內部使用者 `admin` 和 `kibanaserver`：
   ```bash
   bash upgrade-demo-cluster-2.19-to-3.sh
   ```
   {% include copy.html %}

   此指令碼會將您 `admin` 密碼的 bcrypt 雜湊寫入 `~/deploy/internal_users.yml`，叢集首次啟動時會以此初始化 Security 外掛程式。此指令碼也會為 `kibanaserver` 使用者產生隨機密碼，OpenSearch Dashboards 會使用該密碼連線至 OpenSearch，並將其寫入 `~/deploy/opensearch_dashboards.yml`。由於容器以 UID 1000 執行，此指令碼會讓掛載至容器的檔案可供所有使用者讀取，並將 `~/deploy` 目錄的存取權限限制為您的使用者。此指令碼只會在主機的迴路介面（`127.0.0.1`）上發布容器連接埠，因此無法從其他機器存取該叢集。
1. 確認容器已成功啟動：
   ```bash
   docker container ls
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   CONTAINER ID   IMAGE                                            COMMAND                  CREATED              STATUS              PORTS                                                    NAMES
   2812c2945d33   opensearchproject/opensearch-dashboards:2.19.6   "./opensearch-dashbo…"   12 seconds ago       Up 5 seconds        127.0.0.1:5601->5601/tcp                                 os-dashboards-01
   928957045cc4   opensearchproject/opensearch:2.19.6              "./opensearch-docker…"   About a minute ago   Up About a minute   9300/tcp, 9600/tcp, 9650/tcp, 127.0.0.1:9204->9200/tcp   os-node-04
   16a84b2a314b   opensearchproject/opensearch:2.19.6              "./opensearch-docker…"   About a minute ago   Up About a minute   9300/tcp, 9600/tcp, 9650/tcp, 127.0.0.1:9203->9200/tcp   os-node-03
   aa539a9a4b1b   opensearchproject/opensearch:2.19.6              "./opensearch-docker…"   About a minute ago   Up About a minute   9300/tcp, 9600/tcp, 9650/tcp, 127.0.0.1:9202->9200/tcp   os-node-02
   25a56091a268   opensearchproject/opensearch:2.19.6              "./opensearch-docker…"   About a minute ago   Up About a minute   9300/tcp, 9600/tcp, 9650/tcp, 127.0.0.1:9201->9200/tcp   os-node-01
   ```
1. OpenSearch 初始化叢集所需的時間會因底層主機的效能能力而異。您可以追蹤容器記錄檔，查看 OpenSearch 在啟動程序期間的運作情形：
   1. 在終端機視窗中輸入下列命令，以顯示容器 `os-node-01` 的記錄檔：
      ```bash
      docker logs -f os-node-01
      ```
      {% include copy.html %}
   1. 當節點就緒時，您會看到類似下列範例的記錄檔項目：

      ```bash
      [INFO ][o.o.s.c.ConfigurationRepository] [os-node-01] Node 'os-node-01' initialized
      ```
   1. 按下 `Ctrl+C` 停止追蹤容器記錄檔，並返回命令提示字元。
1. 使用 cURL 查詢 OpenSearch REST API。在下列命令中，會將請求傳送至主機連接埠 `9201`（對應至容器上的連接埠 `9200`）來查詢 `os-node-01`：
   ```bash
   curl -s "https://localhost:9201" -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```json
   {
     "name" : "os-node-01",
     "cluster_name" : "opensearch-dev-cluster",
     "cluster_uuid" : "pJ2t0RKrTw2Xeva40ZAF1Q",
     "version" : {
       "distribution" : "opensearch",
       "number" : "2.19.6",
       "build_type" : "tar",
       "build_hash" : "97d3c13bf22a4a72ac11dc503fe44c97662b9161",
       "build_date" : "2026-07-01T04:27:16.038403104Z",
       "build_snapshot" : false,
       "lucene_version" : "9.12.3",
       "minimum_wire_compatibility_version" : "7.10.0",
       "minimum_index_compatibility_version" : "7.0.0"
     },
     "tagline" : "The OpenSearch Project: https://opensearch.org/"
   }
   ```

   `-s` 選項會隱藏 cURL 進度計與錯誤訊息。`-k` 選項會略過自簽 TLS 憑證的驗證。
   {: .tip}

## 新增資料並設定 OpenSearch Security

現在 OpenSearch 叢集已在執行中，是時候新增資料並設定一些 OpenSearch Security 設定了。您新增的資料與設定的設定，將在版本升級完成後再次進行驗證。

本節可分為兩個部分：
- [使用 REST API 編製資料索引](#indexing-data-with-the-rest-api)
- [使用 OpenSearch Dashboards 新增資料](#adding-data-using-opensearch-dashboards)

### 使用 REST API 編製資料索引

1. 下載範例欄位對應檔案：
   ```bash
   wget https://raw.githubusercontent.com/opensearch-project/documentation-website/main/assets/examples/ecommerce-field_mappings.json
   ```
   {% include copy.html %}
1. 接著，下載您要匯入此索引的大量資料：
   ```bash
   wget https://raw.githubusercontent.com/opensearch-project/documentation-website/main/assets/examples/ecommerce.ndjson
   ```
   {% include copy.html %}
1. 使用 [Create index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/) API，以 `ecommerce-field_mappings.json` 中定義的對應建立索引：
   ```bash
   curl -s -H "Content-Type: application/json" \
      -X PUT "https://localhost:9201/ecommerce?pretty" \
      --data-binary "@ecommerce-field_mappings.json" \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "acknowledged" : true,
     "shards_acknowledged" : true,
     "index" : "ecommerce"
   }
   ```
1. 使用 [Bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) API，將 `ecommerce.ndjson` 的資料新增至新的 ecommerce 索引：
   ```bash
   curl -s -H "Content-Type: application/x-ndjson" \
      -X PUT "https://localhost:9201/ecommerce/_bulk?pretty" \
      --data-binary "@ecommerce.ndjson" \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下（已截斷）：

   ```json
   {
     "took" : 3448,
     "errors" : false,
     "items" : [
       ...
       {
         "index" : {
           "_index" : "ecommerce",
           "_id" : "4674",
           "_version" : 1,
           "result" : "created",
           "_shards" : {
             "total" : 2,
             "successful" : 2,
             "failed" : 0
           },
           "_seq_no" : 4674,
           "_primary_term" : 1,
           "status" : 201
         }
       }
     ]
   }
   ```
1. <p id="validation">您也可以使用搜尋查詢來確認資料已成功編製索引。下列查詢會傳回關鍵字 `customer_first_name` 等於 `Sonya` 的文件數量：</p>
   ```bash
   curl -s -H 'Content-Type: application/json' \
      -X GET "https://localhost:9201/ecommerce/_search?pretty=true&filter_path=hits.total" \
      -d'{"query":{"match":{"customer_first_name":"Sonya"}}}' \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "hits" : {
       "total" : {
         "value" : 106,
         "relation" : "eq"
       }
     }
   }
   ```

### 使用 OpenSearch Dashboards 新增資料

1. 開啟網頁瀏覽器，並在您的 Docker 主機上瀏覽至 `https://localhost:5601`。如果 OpenSearch Dashboards 正在執行，您會被重新導向至登入頁面。
   1. 連接埠 `5601` 只發佈於 Docker 主機的回送介面上。如果您的 Docker 主機是遠端機器，請將該連接埠轉送至您的本機，然後在您本機的瀏覽器中瀏覽至 `https://localhost:5601`。例如，若要使用 SSH 轉送連接埠，請在您的本機上執行下列命令：
      ```bash
      ssh -L 5601:localhost:5601 <user>@<host-address>
      ```
      {% include copy.html %}

      如果您的 Docker 主機是 Amazon EC2 執行個體，您可以改用 AWS Systems Manager Session Manager 連接埠轉送，這種方式不需要開放 SSH 連接埠。將 `<instance-id>` 替換為您的執行個體 ID，並在您的本機上執行下列命令：
      ```bash
      aws ssm start-session --target <instance-id> \
         --document-name AWS-StartPortForwardingSession \
         --parameters '{"portNumber":["5601"],"localPortNumber":["5601"]}'
      ```
      {% include copy.html %}

      如需詳細資訊，請參閱 AWS Systems Manager 使用者指南中的[啟動工作階段（連接埠轉送）](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html#sessions-start-port-forwarding)。如果您的本機上已在使用連接埠 `5601`，請改為將該連接埠轉送至未使用的本機連接埠，並在瀏覽器中瀏覽至該連接埠。
   1. 如果網頁瀏覽器因為 TLS 憑證為自簽憑證而發生錯誤，您可能需要略過瀏覽器中的憑證檢查。如需略過憑證檢查的相關資訊，請參閱瀏覽器的說明文件。
1. 輸入使用者名稱 `admin` 以及您在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼，然後選取 **Log in**。
1. 在 **Welcome to OpenSearch Dashboards** 頁面上，選取 **Add data**。
1. 如果系統提示您選取租用戶，請保持選取 **Private** 租用戶，然後選取 **Confirm**。OpenSearch Dashboards 會重新載入 **Welcome to OpenSearch Dashboards** 頁面。再次選取 **Add data**。
1. 在 **Add sample data** 頁面的 **Sample web logs** 卡片中，選取 **Add data**。
   1. **選用**：選取 **View data** 以檢閱 **[Logs] Web Traffic** 儀表板。
1. 在頂端功能表中，前往 **Management** > **Security**，然後選取 **Internal users**。
1. 選取 **Create internal user**。
1. 輸入 **Username**（例如 `testuser`）、**Password**，並在 **Re-enter password** 中輸入相同的密碼。密碼必須包含至少 8 個字元，其中至少包含一個大寫字母、一個小寫字母、一個數字及一個特殊字元。
1. 在 **Backend role** 欄位中，輸入 `admin`。
1. 選取 **Create**。

## 備份重要檔案

對叢集進行變更前，請務必先建立備份，尤其是叢集在生產環境中執行時。

在本節中，您將：
- [註冊快照儲存庫](#registering-a-snapshot-repository)。
- [建立快照](#creating-a-snapshot)。
- [備份安全性設定](#backing-up-security-settings)。

### 註冊快照儲存庫

1. 使用由 `upgrade-demo-cluster-2.19-to-3.sh` 對應的磁碟區註冊儲存庫：
   ```bash
   curl -s -H 'Content-Type: application/json' \
      -X PUT "https://localhost:9201/_snapshot/snapshot-repo?pretty" \
      -d '{"type":"fs","settings":{"location":"/usr/share/opensearch/snapshots"}}' \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "acknowledged" : true
   }
   ```
1. **選用**：執行額外檢查，以確認儲存庫已成功建立：
   ```bash
   curl -s -X POST "https://localhost:9201/_snapshot/snapshot-repo/_verify?timeout=0s&cluster_manager_timeout=50s&pretty" \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "nodes" : {
       "wTUZqPxRQWuE0HuuumEXVw" : {
         "name" : "os-node-04"
       },
       "acexFqflTHaDN96Gv5qqaw" : {
         "name" : "os-node-03"
       },
       "q_NbbV4jTUyr0XbkzzZRUg" : {
         "name" : "os-node-02"
       },
       "5XXNm56wQYa0ybVNNrodtA" : {
         "name" : "os-node-01"
       }
     }
   }
   ```

### 建立快照

快照是叢集索引與狀態的備份。請參閱[快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/)以了解更多。

1. 建立一個包含所有索引與叢集狀態的快照：
   ```bash
   curl -s -X PUT "https://localhost:9201/_snapshot/snapshot-repo/cluster-snapshot-v2196?wait_for_completion=true&pretty" \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "snapshot" : {
       "snapshot" : "cluster-snapshot-v2196",
       "uuid" : "nNiqZRLkQ0uers3gjyrGBg",
       "version_id" : 136408427,
       "version" : "2.19.6",
       "remote_store_index_shallow_copy" : false,
       "indices" : [
         "top_queries-2026.10.16-59496",
         ".opensearch-sap-log-types-config",
         "opensearch_dashboards_sample_data_logs",
         ".opensearch-observability",
         ".opendistro_security",
         ".ql-datasources",
         ".kibana_92668751_admin_1",
         "ecommerce",
         ".plugins-ml-config",
         "security-auditlog-2026.10.16",
         ".kibana_1"
       ],
       "data_streams" : [ ],
       "include_global_state" : true,
       "state" : "SUCCESS",
       "start_time" : "2026-10-16T15:59:27.839Z",
       "start_time_in_millis" : 1792166367839,
       "end_time" : "2026-10-16T15:59:28.239Z",
       "end_time_in_millis" : 1792166368239,
       "duration_in_millis" : 400,
       "failures" : [ ],
       "shards" : {
         "total" : 11,
         "failed" : 0,
         "successful" : 11
       }
     }
   }
   ```

### 備份安全性設定

叢集管理員可以使用下列任一方法修改 OpenSearch Security 設定：

- 修改 YAML 檔案並執行 `securityadmin.sh`
- 使用管理員憑證發出 REST API 請求
- 透過 OpenSearch Dashboards 進行變更

無論您選擇哪種方法，OpenSearch Security 都會將您的組態寫入名為 `.opendistro_security` 的特殊系統索引。此系統索引在升級過程中會保留，也會儲存在您建立的快照中。不過，還原系統索引需要由 `admin` 憑證授予的提高權限。如需詳細資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)和[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

您也可以在任何 OpenSearch 節點上使用 `-backup` 選項執行 `securityadmin.sh`，將 OpenSearch Security 設定匯出為 YAML 檔案。這些 YAML 檔案可用來以您現有的組態重新初始化 `.opendistro_security` 索引。下列步驟將引導您產生這些備份檔案，並將其複製到您的主機以進行儲存：

1. 在 `os-node-01` 容器中建立名為 `backups` 的目錄：
   ```bash
   docker exec os-node-01 mkdir /usr/share/opensearch/backups
   ```
   {% include copy.html %}
1. 使用 `securityadmin.sh` 在 `/usr/share/opensearch/backups/` 中建立 OpenSearch Security 設定的備份：
   ```bash
   docker exec os-node-01 /usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
      -backup /usr/share/opensearch/backups \
      -icl \
      -nhnv \
      -cacert /usr/share/opensearch/config/root-ca.pem \
      -cert /usr/share/opensearch/config/admin.pem \
      -key /usr/share/opensearch/config/admin-key.pem
   ```
   {% include copy.html %}

   回應應類似於下列內容：

   ```bash
   Security Admin v7
   Will connect to localhost:9200 ... done
   Connected as "CN=A,OU=DOCS,O=OPENSEARCH,L=PORTLAND,ST=OREGON,C=US"
   OpenSearch Version: 2.19.6
   Contacting opensearch cluster 'opensearch' and wait for YELLOW clusterstate ...
   Clustername: opensearch-dev-cluster
   Clusterstate: GREEN
   Number of nodes: 4
   Number of data nodes: 4
   .opendistro_security index already exists, so we do not need to create one.
   Will retrieve '/config' into /usr/share/opensearch/backups/config.yml 
      SUCC: Configuration for 'config' stored in /usr/share/opensearch/backups/config.yml
   Will retrieve '/roles' into /usr/share/opensearch/backups/roles.yml 
      SUCC: Configuration for 'roles' stored in /usr/share/opensearch/backups/roles.yml
   ...
   Will retrieve '/audit' into /usr/share/opensearch/backups/audit.yml 
      SUCC: Configuration for 'audit' stored in /usr/share/opensearch/backups/audit.yml
   ```
1. **選用**：建立 TLS 憑證的備份目錄，並儲存憑證的副本。如果您使用唯一的 TLS 憑證，請對每個節點重複此步驟：
   ```bash
   docker exec os-node-01 bash -c 'mkdir /usr/share/opensearch/backups/certs && cp /usr/share/opensearch/config/*pem /usr/share/opensearch/backups/certs/'
   ```
   {% include copy.html %}
1. 將檔案複製到您的主機：
   ```bash
   docker cp os-node-01:/usr/share/opensearch/backups ~/deploy/
   ```
   {% include copy.html %}

## 執行升級

現在叢集已完成組態，您也已備份重要檔案與設定，是時候開始版本升級了。

本節中的某些步驟，例如停用分片複寫和排清交易記錄檔，不會影響叢集的效能。這些步驟是最佳實務的一部分，在用戶端於整個升級過程中持續與 OpenSearch 叢集互動的情況下（例如查詢現有資料或將文件編製索引），可顯著提升叢集效能。
{: .note}

1. 停用分片複寫，以停止 Lucene 索引分段在叢集內的移動：
   ```bash
   curl -s -H 'Content-type: application/json' \
      -X PUT "https://localhost:9201/_cluster/settings?pretty" \
      -d'{"persistent":{"cluster.routing.allocation.enable":"primaries"}}' \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "acknowledged" : true,
     "persistent" : {
       "cluster" : {
         "routing" : {
           "allocation" : {
             "enable" : "primaries"
           }
         }
       }
     },
     "transient" : { }
   }
   ```
1. 對叢集執行排清作業，將交易記錄檔項目提交至 Lucene 索引：
   ```bash
   curl -s -X POST "https://localhost:9201/_flush?pretty" -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "_shards" : {
       "total" : 27,
       "successful" : 27,
       "failed" : 0
     }
   }
   ```
1. 選擇要升級的節點。您可以依任何順序升級節點，因為此示範叢集中的所有節點都符合叢集管理員的資格。下列命令將停止並移除容器 `os-node-01`，但不會移除已掛載的資料卷：
   ```bash
   docker stop os-node-01 && docker container rm os-node-01
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:3.9.0` 映像啟動名為 `os-node-01` 的新容器，並使用與原始容器相同的對應卷：
   ```bash
   docker run -d \
      -p 127.0.0.1:9201:9200 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      -e "DISABLE_INSTALL_DEMO_CONFIG=true" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-01:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-01.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-01.pem:/usr/share/opensearch/config/os-node-01.pem \
      -v ~/deploy/os-node-01-key.pem:/usr/share/opensearch/config/os-node-01-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.11 \
      --name os-node-01 \
      opensearchproject/opensearch:3.9.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   a9f69e3540d0632eb457f834270a280d41038bc3ce36f4bb1bbb2f112702c88c
   ```
1. 確認 `os-node-01` 已重新加入叢集並執行 3.9.0 版。回應也會顯示哪個節點擔任叢集管理員，因此您可以在過程中的任何時間執行此命令，以查看何時選出新叢集管理員。在升級每個節點後執行此命令，並在升級後的節點出現在回應中之前，不要停止下一個節點：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,cluster_manager" \
      -ku 'admin:<custom-admin-password>' | column -t
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   name        version  node.role  cluster_manager
   os-node-04  2.19.6   dimr       -
   os-node-03  2.19.6   dimr       -
   os-node-02  2.19.6   dimr       *
   os-node-01  3.9.0    dimr       -
   ```
1. **選用**：查詢叢集，以查看節點被移除和替換時分片配置的變化。您可以在過程中的任何時間執行此命令，以查看分片狀態的變化：
   ```bash
   curl -s "https://localhost:9201/_cat/shards" \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下（已截斷）：

   ```bash
   opensearch_dashboards_sample_data_logs 0 p STARTED    14074   9.2mb 172.20.0.13 os-node-03
   opensearch_dashboards_sample_data_logs 0 r STARTED    14074   9.2mb 172.20.0.12 os-node-02
   .kibana_92668751_admin_1               0 p STARTED      146    81kb 172.20.0.14 os-node-04
   .kibana_92668751_admin_1               0 r STARTED      146  81.1kb 172.20.0.13 os-node-03
   ecommerce                              0 p STARTED     4675   3.9mb 172.20.0.13 os-node-03
   ecommerce                              0 r UNASSIGNED                           
   security-auditlog-2026.10.16           0 p STARTED      141 511.9kb 172.20.0.14 os-node-04
   security-auditlog-2026.10.16           0 r STARTED      141 334.7kb 172.20.0.12 os-node-02
   .opendistro_security                   0 r STARTED       10  81.1kb 172.20.0.14 os-node-04
   .opendistro_security                   0 p STARTED       10  81.1kb 172.20.0.13 os-node-03
   .opendistro_security                   0 r STARTED       10  81.1kb 172.20.0.12 os-node-02
   .opendistro_security                   0 r UNASSIGNED                           
   .kibana_1                              0 r STARTED        1   4.3kb 172.20.0.14 os-node-04
   .kibana_1                              0 p STARTED        1   4.3kb 172.20.0.12 os-node-02
   ```

   在停用分片複寫期間，副本分片會保持未指派狀態。OpenSearch 不會將副本分配給執行版本早於主要分片所在節點的節點，因此在所有節點升級完成之前，部分副本會保持未指派狀態。
1. 停止 `os-node-02`：
   ```bash
   docker stop os-node-02 && docker container rm os-node-02
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:3.9.0` 映像啟動名為 `os-node-02` 的新容器，並使用與原始容器相同的對應卷：
   ```bash
   docker run -d \
      -p 127.0.0.1:9202:9200 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      -e "DISABLE_INSTALL_DEMO_CONFIG=true" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-02:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-02.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-02.pem:/usr/share/opensearch/config/os-node-02.pem \
      -v ~/deploy/os-node-02-key.pem:/usr/share/opensearch/config/os-node-02-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.12 \
      --name os-node-02 \
      opensearchproject/opensearch:3.9.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   6fd3fa8e6ba69afb85d582047d2be9b12bea12cb0809aa3a3b7d3252924d3685
   ```
1. 停止 `os-node-03`：
   ```bash
   docker stop os-node-03 && docker container rm os-node-03
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:3.9.0` 映像啟動名為 `os-node-03` 的新容器，並使用與原始容器相同的對應卷：
   ```bash
   docker run -d \
      -p 127.0.0.1:9203:9200 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      -e "DISABLE_INSTALL_DEMO_CONFIG=true" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-03:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-03.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-03.pem:/usr/share/opensearch/config/os-node-03.pem \
      -v ~/deploy/os-node-03-key.pem:/usr/share/opensearch/config/os-node-03-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.13 \
      --name os-node-03 \
      opensearchproject/opensearch:3.9.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   023d7510b4509140507e9b808e3504676a0a946ac7d1f49f0987d7c1a4c78f2b
   ```
1. 停止 `os-node-04`：
   ```bash
   docker stop os-node-04 && docker container rm os-node-04
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:3.9.0` 映像啟動名為 `os-node-04` 的新容器，並使用與原始容器相同的對應卷：
   ```bash
   docker run -d \
      -p 127.0.0.1:9204:9200 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      -e "DISABLE_INSTALL_DEMO_CONFIG=true" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-04:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-04.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-04.pem:/usr/share/opensearch/config/os-node-04.pem \
      -v ~/deploy/os-node-04-key.pem:/usr/share/opensearch/config/os-node-04-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.14 \
      --name os-node-04 \
      opensearchproject/opensearch:3.9.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   6848100ed927663de46489e54facfe781fe3508a857da081ebd6f299dfbf3887
   ```
1. 確認您的叢集正在執行新版本：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,cluster_manager" \
      -ku 'admin:<custom-admin-password>' | column -t
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   name        version  node.role  cluster_manager
   os-node-04  3.9.0    dimr       -
   os-node-03  3.9.0    dimr       -
   os-node-02  3.9.0    dimr       *
   os-node-01  3.9.0    dimr       -
   ```
1. 您最後應升級的元件是 OpenSearch Dashboards 節點。首先，停止並移除舊的容器：
   ```bash
   docker stop os-dashboards-01 && docker rm os-dashboards-01
   ```
   {% include copy.html %}
1. 建立執行目標版本 OpenSearch Dashboards 的新容器：
   ```bash
   docker run -d \
      -p 127.0.0.1:5601:5601 \
      -v ~/deploy/opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch-dashboards/config/root-ca.pem \
      -v ~/deploy/os-dashboards-01.pem:/usr/share/opensearch-dashboards/config/os-dashboards-01.pem \
      -v ~/deploy/os-dashboards-01-key.pem:/usr/share/opensearch-dashboards/config/os-dashboards-01-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.10 \
      --name os-dashboards-01 \
      opensearchproject/opensearch-dashboards:3.9.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   0cea291d8bbcf540187ffe4f0ce55c73a76807c0ba3b26c044da26e83c543e85
   ```
1. 確認 OpenSearch Dashboards 容器已正常啟動。OpenSearch Dashboards 可能需要一分鐘才能啟動。您可以使用類似以下的命令，確認傳送至 `https://localhost:5601` 的請求會重新導向（HTTP 狀態碼 302）至 `/app/login`：
   ```bash
   curl -s https://localhost:5601 -kI
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   HTTP/1.1 302 Found
   location: /app/login
   osd-name: opensearch-dashboards-dev
   cache-control: private, no-cache, no-store, must-revalidate
   set-cookie: security_authentication=; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Secure; HttpOnly; Path=/
   content-length: 0
   Date: Fri, 16 Oct 2026 16:20:51 GMT
   Connection: keep-alive
   Keep-Alive: timeout=120
   ```
1. 重新啟用副本分片的配置：
   ```bash
   curl -s -H 'Content-type: application/json' \
      -X PUT "https://localhost:9201/_cluster/settings?pretty" \
      -d'{"persistent":{"cluster.routing.allocation.enable":"all"}}' \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
     "acknowledged" : true,
     "persistent" : {
       "cluster" : {
         "routing" : {
           "allocation" : {
             "enable" : "all"
           }
         }
       }
     },
     "transient" : { }
   }
   ```

## 驗證升級

您已成功部署安全的 OpenSearch 叢集、為資料編製索引、建立填入範例資料的儀表板、建立新的內部使用者、備份重要檔案，並將叢集從 2.19.6 版升級至 3.9.0 版。在繼續探索與實驗 OpenSearch 和 OpenSearch Dashboards 之前，您應該先驗證升級的結果。

針對此叢集，升級後的驗證步驟可包含確認下列項目：

- [執行中的版本](#verifying-the-new-running-version)
- [健康狀態與分片配置](#verifying-cluster-health-and-shard-allocation)
- [資料一致性](#verifying-data-consistency)

### 驗證新的執行中版本

1. 驗證 OpenSearch 節點目前執行的版本：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,cluster_manager" \
      -ku 'admin:<custom-admin-password>' | column -t
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   name        version  node.role  cluster_manager
   os-node-04  3.9.0    dimr       -
   os-node-03  3.9.0    dimr       -
   os-node-02  3.9.0    dimr       *
   os-node-01  3.9.0    dimr       -
   ```
1. 驗證 OpenSearch Dashboards 目前執行的版本：
   1. **選項 1**：從網頁介面驗證 OpenSearch Dashboards 版本。
      1. 開啟網頁瀏覽器並前往 `https://localhost:5601`。
      1. 使用使用者名稱 `admin` 及您在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼登入。
      1. 若出現 **New! Enhanced Discover experience available** 對話方塊，請選取 **Dismiss**。
      1. 選取右上角的 **Help menu** 按鈕。版本會顯示在彈出式視窗中。
      1. 再次選取 **Help menu** 按鈕以關閉彈出式視窗。
   1. **選項 2**：透過檢查 `manifest.yml` 驗證 OpenSearch Dashboards 版本：
      ```bash
      docker exec os-dashboards-01 head -n 5 manifest.yml
      ```
      {% include copy.html %}

      回應應類似下列內容：

      ```yaml
      ---
      schema-version: '1.1'
      build:
        name: OpenSearch Dashboards
        version: 3.9.0
      ```

### 驗證叢集健康狀態與分片配置

1. 查詢 [Cluster health]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) API 端點，以查看叢集健康狀態的相關資訊。您應該會看到狀態為 `green`，表示所有主要分片與副本分片皆已配置。如果狀態為 `yellow`，請等待 OpenSearch 完成副本分片的配置，然後再次執行該命令：
   ```bash
   curl -s "https://localhost:9201/_cluster/health?pretty" -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應該會類似以下內容：

   ```json
   {
     "cluster_name" : "opensearch-dev-cluster",
     "status" : "green",
     "timed_out" : false,
     "number_of_nodes" : 4,
     "number_of_data_nodes" : 4,
     "discovered_master" : true,
     "discovered_cluster_manager" : true,
     "active_primary_shards" : 13,
     "active_shards" : 35,
     "relocating_shards" : 0,
     "initializing_shards" : 0,
     "unassigned_shards" : 0,
     "delayed_unassigned_shards" : 0,
     "number_of_pending_tasks" : 0,
     "number_of_in_flight_fetch" : 0,
     "task_max_waiting_in_queue_millis" : 0,
     "active_shards_percent_as_number" : 100.0
   }
   ```
1. 查詢 [CAT shards]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-shards/) API 端點，以查看叢集升級後分片的配置方式：
   ```bash
   curl -s "https://localhost:9201/_cat/shards" -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應該會類似以下內容：

   ```bash
   .ql-datasources                        0 r STARTED     0    208b 172.20.0.14 os-node-04
   .ql-datasources                        0 p STARTED     0    208b 172.20.0.12 os-node-02
   .ql-datasources                        0 r STARTED     0    208b 172.20.0.11 os-node-01
   .kibana_92668751_admin_1               0 r STARTED   146  74.4kb 172.20.0.14 os-node-04
   .kibana_92668751_admin_1               0 p STARTED   146  74.4kb 172.20.0.13 os-node-03
   .kibana_92668751_admin_2               0 p STARTED   146  70.9kb 172.20.0.14 os-node-04
   .kibana_92668751_admin_2               0 r STARTED   146    208b 172.20.0.13 os-node-03
   .kibana_2                              0 p STARTED     1   4.8kb 172.20.0.13 os-node-03
   .kibana_2                              0 r STARTED     1      0b 172.20.0.11 os-node-01
   .opendistro_security                   0 p STARTED    10  81.1kb 172.20.0.14 os-node-04
   .opendistro_security                   0 r STARTED    10  81.1kb 172.20.0.13 os-node-03
   .opendistro_security                   0 r STARTED    10  81.1kb 172.20.0.12 os-node-02
   .opendistro_security                   0 r STARTED    10  81.1kb 172.20.0.11 os-node-01
   .kibana_1                              0 r STARTED     1   4.3kb 172.20.0.14 os-node-04
   .kibana_1                              0 p STARTED     1   4.3kb 172.20.0.12 os-node-02
   .opensearch-observability              0 r STARTED     0    208b 172.20.0.13 os-node-03
   .opensearch-observability              0 r STARTED     0    208b 172.20.0.12 os-node-02
   .opensearch-observability              0 p STARTED     0    208b 172.20.0.11 os-node-01
   .plugins-ml-config                     0 r STARTED     1     4kb 172.20.0.14 os-node-04
   .plugins-ml-config                     0 r STARTED     1     4kb 172.20.0.13 os-node-03
   .plugins-ml-config                     0 p STARTED     1     4kb 172.20.0.12 os-node-02
   .plugins-ml-config                     0 r STARTED     1     4kb 172.20.0.11 os-node-01
   top_queries-2026.10.16-59496           0 r STARTED    43   523kb 172.20.0.14 os-node-04
   top_queries-2026.10.16-59496           0 p STARTED    43 184.4kb 172.20.0.12 os-node-02
   top_queries-2026.10.16-59496           0 r STARTED    43   523kb 172.20.0.11 os-node-01
   opensearch_dashboards_sample_data_logs 0 r STARTED 14074   9.2mb 172.20.0.13 os-node-03
   opensearch_dashboards_sample_data_logs 0 p STARTED 14074   9.2mb 172.20.0.12 os-node-02
   .opensearch-sap-log-types-config       0 p STARTED               172.20.0.14 os-node-04
   .opensearch-sap-log-types-config       0 r STARTED               172.20.0.13 os-node-03
   .opensearch-sap-log-types-config       0 r STARTED               172.20.0.12 os-node-02
   .opensearch-sap-log-types-config       0 r STARTED               172.20.0.11 os-node-01
   ecommerce                              0 r STARTED  4675   3.9mb 172.20.0.13 os-node-03
   ecommerce                              0 p STARTED  4675     4mb 172.20.0.11 os-node-01
   security-auditlog-2026.10.16           0 r STARTED   143 315.1kb 172.20.0.14 os-node-04
   security-auditlog-2026.10.16           0 p STARTED   143 548.6kb 172.20.0.12 os-node-02
   ```

### 驗證資料一致性

您需要再次查詢電子商務索引，以確認範例資料仍然存在：

1. 將此查詢的回應與您在[使用 REST API 編製資料索引](#indexing-data-with-the-rest-api)的[最後一個步驟](#validation)中收到的回應進行比較：
   ```bash
   curl -s -H 'Content-Type: application/json' \
      -X GET "https://localhost:9201/ecommerce/_search?pretty=true&filter_path=hits.total" \
      -d'{"query":{"match":{"customer_first_name":"Sonya"}}}' \
      -ku 'admin:<custom-admin-password>'
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```json
   {
     "hits" : {
       "total" : {
         "value" : 106,
         "relation" : "eq"
       }
     }
   }
   ```
1. 開啟網頁瀏覽器並前往 `https://localhost:5601`。
1. 如果系統提示您登入，請輸入使用者名稱 `admin` 以及您在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼。如果出現 **New! Enhanced Discover experience available** 對話方塊，請選取 **Dismiss**。
1. 選取網頁介面左上角的 **Menu** 按鈕，開啟導覽窗格。
1. 前往 **OpenSearch Dashboards** > **Dashboards**。
1. 選取 **[Logs] Web Traffic**，開啟您先前在此流程中新增範例資料時建立的儀表板。如果您在升級前曾檢視此儀表板，OpenSearch Dashboards 可能會直接開啟它。
1. 檢閱完儀表板後，請選取右上角的使用者個人資料按鈕。選取 **Log out**，以便使用其他使用者身分登入。
1. 輸入您在升級前建立的使用者名稱和密碼，然後選取 **Log in**。
1. 若要確認您已使用所建立的使用者身分登入，請選取 **Help menu** 按鈕旁的使用者個人資料按鈕。此按鈕會顯示使用者名稱的第一個字母，例如 `testuser` 會顯示 `t`。如果您能以此使用者身分登入，表示您在升級前建立的內部使用者已保留。

## 後續步驟

檢閱下列資源，以進一步了解 OpenSearch 的運作方式：

- [REST API 參考文件]({{site.url}}{{site.baseurl}}/api-reference/index/)
- [OpenSearch Dashboards 入門]({{site.url}}{{site.baseurl}}/dashboards/getting-started/)
- [OpenSearch 中的安全性簡介]({{site.url}}{{site.baseurl}}/security/index/)
