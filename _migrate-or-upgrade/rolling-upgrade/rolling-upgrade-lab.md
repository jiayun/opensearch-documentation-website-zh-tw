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

您可以在自己的相容主機上依照這些步驟操作，重現 OpenSearch 專案用於測試[滾動升級]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/)的相同叢集狀態。如果您想在開發環境中測試升級程序，這項練習會很有幫助。

本實驗的步驟已在任意選用的 [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/) `t2.large` 執行個體上驗證，該執行個體使用 [Amazon Linux 2](https://aws.amazon.com/amazon-linux-2/) 核心版本 `Linux 5.10.162-141.675.amzn2.x86_64` 和 [Docker](https://www.docker.com/) 版本 `20.10.17, build 100c701`。佈建此執行個體時，已連接一個 20 GiB gp2 [Amazon EBS](https://aws.amazon.com/ebs/) 根磁碟區。這些規格僅供參考，並不代表 OpenSearch 或 OpenSearch Dashboards 的硬體需求。

本程序中提及主機上的 `$HOME` 路徑時，皆以波浪號字元（「~」）表示，讓操作指示更易於在不同環境中使用。如果您偏好指定絕對路徑，請修改 `upgrade-demo-cluster.sh` 中定義的磁碟區路徑，以及本文相關命令中使用的磁碟區路徑，以符合您的環境。

## 設定環境

依照本文步驟操作時，您將使用我們提供的指令碼，定義數個 Docker 資源，包括容器、磁碟區和專用的 Docker 網路。如果您想重新開始此程序，可以使用下列命令清理環境：

```bash
docker container stop $(docker container ls -aqf name=os-); \
	docker container rm $(docker container ls -aqf name=os-); \
	docker volume rm -f $(docker volume ls -q | egrep 'data-0|repo-0'); \
	docker network rm opensearch-dev-net
```
{% include copy.html %}

此命令會移除名稱符合規則運算式 `os-*` 的容器、符合 `data-0*` 和 `repo-0*` 的資料磁碟區，以及名為 `opensearch-dev-net` 的 Docker 網路。如果您的主機上有其他 Docker 資源正在執行，您應檢查並修改此命令，以免意外移除其他資源。此命令不會還原主機組態的變更，例如記憶體交換行為。
{: .warning}

選好主機後，您就可以開始實驗：

1. 安裝適合您 Linux 發行版和系統架構的 [Docker Engine](https://docs.docker.com/engine/install/) 版本。 
1. 在主機上設定[重要系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)：
    1. 停用主機上的記憶體分頁和交換，以提升效能：
	   ```bash
	   sudo swapoff -a
	   ```
	   {% include copy.html %}
	1. 增加 OpenSearch 可用的記憶體對應數量。開啟 `sysctl` 組態檔案進行編輯。此範例命令使用 [vim](https://www.vim.org/) 文字編輯器，但您可以使用任何可用的文字編輯器：
	   ```bash
	   sudo vim /etc/sysctl.conf
	   ```
	   {% include copy.html %}
	1. 將下列這一行新增至 `/etc/sysctl.conf`：
	   ```bash
	   vm.max_map_count=262144
	   ```
	   {% include copy.html %}
	1. 儲存並結束。如果您使用 `vi` 或 `vim` 文字編輯器，請切換至命令模式，並輸入 `:wq!` 或 `ZZ`，即可儲存並結束。 
	1. 套用組態變更：
	   ```bash
	   sudo sysctl -p
	   ```
	   {% include copy.html %}
1. 在您的家目錄中建立名為 `deploy` 的新目錄，然後切換至該目錄。您將在部署指令碼、組態檔案和 TLS 憑證的路徑中使用 `~/deploy`：
   ```bash
   mkdir ~/deploy && cd ~/deploy
   ```
   {% include copy.html %}
1. 從 OpenSearch 專案的 [`documentation-website`](https://github.com/opensearch-project/documentation-website) 儲存庫下載 `upgrade-demo-cluster.sh`：
   ```bash
   wget https://raw.githubusercontent.com/opensearch-project/documentation-website/main/assets/examples/upgrade-demo-cluster.sh
   ```
   {% include copy.html %}
1. 不做任何修改，直接執行指令碼，以部署四個執行 OpenSearch 的容器和一個執行 OpenSearch Dashboards 的容器，並使用自訂的自我簽署 TLS 憑證和一組預先定義的內部使用者：
   ```bash
   sh upgrade-demo-cluster.sh
   ```
   {% include copy.html %}
1. 確認容器已成功啟動：
   ```bash
   docker container ls
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   CONTAINER ID   IMAGE                                           COMMAND                  CREATED          STATUS          PORTS                                                                                                      NAMES
   6e5218c8397d   opensearchproject/opensearch-dashboards:1.3.7   "./opensearch-dashbo…"   24 seconds ago   Up 22 seconds   0.0.0.0:5601->5601/tcp, :::5601->5601/tcp                                                                  os-dashboards-01
   cb5188308b21   opensearchproject/opensearch:1.3.7              "./opensearch-docker…"   25 seconds ago   Up 24 seconds   9300/tcp, 9650/tcp, 0.0.0.0:9204->9200/tcp, :::9204->9200/tcp, 0.0.0.0:9604->9600/tcp, :::9604->9600/tcp   os-node-04
   71b682aa6671   opensearchproject/opensearch:1.3.7              "./opensearch-docker…"   26 seconds ago   Up 25 seconds   9300/tcp, 9650/tcp, 0.0.0.0:9203->9200/tcp, :::9203->9200/tcp, 0.0.0.0:9603->9600/tcp, :::9603->9600/tcp   os-node-03
   f894054a9378   opensearchproject/opensearch:1.3.7              "./opensearch-docker…"   27 seconds ago   Up 26 seconds   9300/tcp, 9650/tcp, 0.0.0.0:9202->9200/tcp, :::9202->9200/tcp, 0.0.0.0:9602->9600/tcp, :::9602->9600/tcp   os-node-02
   2e9c91c959cd   opensearchproject/opensearch:1.3.7              "./opensearch-docker…"   28 seconds ago   Up 27 seconds   9300/tcp, 9650/tcp, 0.0.0.0:9201->9200/tcp, :::9201->9200/tcp, 0.0.0.0:9601->9600/tcp, :::9601->9600/tcp   os-node-01
   ```
1. OpenSearch 初始化叢集所需的時間，會因底層主機的效能而異。您可以持續查看容器記錄檔，以了解 OpenSearch 在啟動程序期間執行的作業：
   1. 輸入下列命令，在終端機視窗中顯示容器 `os-node-01` 的記錄檔：
      ```bash
      docker logs -f os-node-01
      ```
      {% include copy.html %}
   1. 節點就緒時，您會看到類似下列範例的記錄項目：

      以下為範例：

      ```bash
      [INFO ][o.o.s.c.ConfigurationRepository] [os-node-01] Node 'os-node-01' initialized
      ```
   1. 按下 `Ctrl+C`，停止持續查看容器記錄檔並返回命令提示字元。
1. 使用 cURL 查詢 OpenSearch REST API。在下列命令中，透過將請求傳送至主機連接埠 `9201` 來查詢 `os-node-01`，此連接埠對應至容器上的連接埠 `9200`：
   ```bash
   curl -s "https://localhost:9201" -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```json
   {
       "name" : "os-node-01",
       "cluster_name" : "opensearch-dev-cluster",
       "cluster_uuid" : "g1MMknuDRuuD9IaaNt56KA",
       "version" : {
           "distribution" : "opensearch",
           "number" : "1.3.7",
           "build_type" : "tar",
           "build_hash" : "db18a0d5a08b669fb900c00d81462e221f4438ee",
           "build_date" : "2022-12-07T22:59:20.186520Z",
           "build_snapshot" : false,
           "lucene_version" : "8.10.1",
           "minimum_wire_compatibility_version" : "6.8.0",
           "minimum_index_compatibility_version" : "6.0.0-beta1"
       },
       "tagline" : "The OpenSearch Project: https://opensearch.org/"
   }
   ```

   **提示**：搭配 `curl` 使用 `-s` 選項，可隱藏進度指示器和錯誤訊息。
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
1. 接著，下載您將匯入此索引的批量資料：
   ```bash
   wget https://raw.githubusercontent.com/opensearch-project/documentation-website/main/assets/examples/ecommerce.ndjson
   ```
   {% include copy.html %}
1. 使用 [Create index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/) API，以 `ecommerce-field_mappings.json` 中定義的對應建立索引：
   ```bash
   curl -H "Content-Type: application/json" \
      -X PUT "https://localhost:9201/ecommerce?pretty" \
      --data-binary "@ecommerce-field_mappings.json" \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

      ```json
      {
         "acknowledged" : true,
         "shards_acknowledged" : true,
         "index" : "ecommerce"
      }
      ```
1. 使用 [Bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) API，將 `ecommerce.ndjson` 中的資料新增至新的 ecommerce 索引：
   ```bash
   curl -H "Content-Type: application/x-ndjson" \
      -X PUT "https://localhost:9201/ecommerce/_bulk?pretty" \
      --data-binary "@ecommerce.ndjson" \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容（已截斷）：

      ```json
      {
         "took" : 3323,
         "errors" : false,
         "items" : [
            ...
            "index" : {
               "_index" : "ecommerce",
               "_type" : "_doc",
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
         ]
      }
      ```
1. <p id="validation">搜尋查詢也可確認資料是否已成功編製索引。下列查詢會傳回關鍵字 `customer_first_name` 等於 `Sonya` 的文件數量：</p>
   ```bash
   curl -H 'Content-Type: application/json' \
      -X GET "https://localhost:9201/ecommerce/_search?pretty=true&filter_path=hits.total" \
      -d'{"query":{"match":{"customer_first_name":"Sonya"}}}' \
      -ku admin:<custom-admin-password>
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

### 使用 OpenSearch Dashboards 新增資料

1. 開啟網頁瀏覽器，並瀏覽至 Docker 主機上的連接埠 `5601`（例如 `https://<HOST_ADDRESS>:5601`）。如果 OpenSearch Dashboards 正在執行，且您的瀏覽器用戶端可透過網路存取該主機，則您會被重新導向至登入頁面。
    1. 如果網頁瀏覽器因為 TLS 憑證為自簽而發生錯誤，您可能需要略過瀏覽器中的憑證檢查。請參閱瀏覽器的說明文件，以取得略過憑證檢查的相關資訊。每個憑證的一般名稱 (CN) 是依據容器與節點名稱產生，以供叢集內通訊使用，因此從瀏覽器連線至主機時，仍會出現「invalid CN」警告。
1. 輸入預設使用者名稱（`admin`）與密碼（`admin`）。
1. 在 OpenSearch Dashboards 的 **Home** 頁面上，選取 **Add sample data**。
1. 在 **Sample web logs** 下，選取 **Add data**。
   1. **選用**：選取 **View data** 以檢閱 **[Logs] Web Traffic** 儀表板。
1. 選取 **Menu button** 以開啟 **Navigation pane**，然後前往 **Security > Internal users**。
1. 選取 **Create internal user**。
1. 提供 **Username** 與 **Password**。
1. 在 **Backend role** 欄位中，輸入 `admin`。
1. 選取 **Create**。

## 備份重要檔案

對叢集進行變更前，請務必先建立備份，尤其是叢集在生產環境中執行時。

在本節中，您將：
- [註冊快照儲存庫](#registering-a-snapshot-repository)。
- [建立快照](#creating-a-snapshot)。
- [備份安全性設定](#backing-up-security-settings)。

### 註冊快照儲存庫

1. 使用由 `upgrade-demo-cluster.sh` 對應的磁碟區來註冊儲存庫：
   ```bash
   curl -H 'Content-Type: application/json' \
      -X PUT "https://localhost:9201/_snapshot/snapshot-repo?pretty" \
      -d '{"type":"fs","settings":{"location":"/usr/share/opensearch/snapshots"}}' \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

      ```json
      {
         "acknowledged" : true
      }
      ```
1. **選用**：執行額外檢查，以確認儲存庫已成功建立：
   ```bash
   curl -H 'Content-Type: application/json' \
      -X POST "https://localhost:9201/_snapshot/snapshot-repo/_verify?timeout=0s&master_timeout=50s&pretty" \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

      ```json
      {
         "nodes" : {
            "UODBXfAlRnueJ67grDxqgw" : {
               "name" : "os-node-03"
            },
            "14I_OyBQQXio8nmk0xsVcQ" : {
               "name" : "os-node-04"
            },
            "tQp3knPRRUqHvFNKpuD2vQ" : {
               "name" : "os-node-02"
            },
            "rPe8D6ssRgO5twIP00wbCQ" : {
               "name" : "os-node-01"
            }
         }
      }
      ```

### 建立快照

快照是叢集索引與狀態的備份。請參閱 [Snapshots]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/) 以深入了解。

1. 建立包含所有索引與叢集狀態的快照：
   ```bash
   curl -H 'Content-Type: application/json' \
      -X PUT "https://localhost:9201/_snapshot/snapshot-repo/cluster-snapshot-v137?wait_for_completion=true&pretty" \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

      ```json
      {
         "snapshot" : {
            "snapshot" : "cluster-snapshot-v137",
            "uuid" : "-IYB8QNPShGOTnTtMjBjNg",
            "version_id" : 135248527,
            "version" : "1.3.7",
            "indices" : [
               "opensearch_dashboards_sample_data_logs",
               ".opendistro_security",
               "security-auditlog-2023.02.27",
               ".kibana_1",
               ".kibana_92668751_admin_1",
               "ecommerce",
               "security-auditlog-2023.03.06",
               "security-auditlog-2023.02.28",
               "security-auditlog-2023.03.07"
            ],
            "data_streams" : [ ],
            "include_global_state" : true,
            "state" : "SUCCESS",
            "start_time" : "2023-03-07T18:33:00.656Z",
            "start_time_in_millis" : 1678213980656,
            "end_time" : "2023-03-07T18:33:01.471Z",
            "end_time_in_millis" : 1678213981471,
            "duration_in_millis" : 815,
            "failures" : [ ],
            "shards" : {
               "total" : 9,
               "failed" : 0,
               "successful" : 9
            }
         }
      }
      ```

### 備份安全性設定

叢集管理員可以使用下列任一方法修改 OpenSearch Security 設定：

- 修改 YAML 檔案並執行 `securityadmin.sh`
- 使用管理員憑證發送 REST API 請求
- 透過 OpenSearch Dashboards 進行變更

無論您選擇哪種方法，OpenSearch Security 都會將您的組態寫入名為 `.opendistro_security` 的特殊系統索引。此系統索引會在升級過程中保留，並且也會儲存在您建立的快照中。不過，還原系統索引需要 `admin` 憑證所授予的進階存取權限。若要了解更多，請參閱 [System indexes]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/) 與 [Configuring TLS certificates]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

您也可以在任何 OpenSearch 節點上執行 `securityadmin.sh` 並搭配 `-backup` 選項，將 OpenSearch Security 設定匯出為 YAML 檔案。這些 YAML 檔案可用來以您現有的組態重新初始化 `.opendistro_security` 索引。下列步驟將引導您產生這些備份檔案並將其複製到主機儲存：

1. 使用 `os-node-01` 開啟互動式偽 TTY 工作階段：
   ```bash
   docker exec -it os-node-01 bash
   ```
   {% include copy.html %}
1. 建立名為 `backups` 的目錄並切換至該目錄：
   ```bash
   mkdir /usr/share/opensearch/backups && cd /usr/share/opensearch/backups
   ```
   {% include copy.html %}
1. 使用 `securityadmin.sh` 在 `/usr/share/opensearch/backups/` 中建立 OpenSearch Security 設定的備份：
   ```bash
   /usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
      -backup /usr/share/opensearch/backups \
      -icl \
      -nhnv \
      -cacert /usr/share/opensearch/config/root-ca.pem \
      -cert /usr/share/opensearch/config/admin.pem \
      -key /usr/share/opensearch/config/admin-key.pem
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   Security Admin v7
   Will connect to localhost:9300 ... done
   Connected as CN=A,OU=DOCS,O=OPENSEARCH,L=PORTLAND,ST=OREGON,C=US
   OpenSearch Version: 1.3.7
   OpenSearch Security Version: 1.3.7.0
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
   Will retrieve '/rolesmapping' into /usr/share/opensearch/backups/roles_mapping.yml 
      SUCC: Configuration for 'rolesmapping' stored in /usr/share/opensearch/backups/roles_mapping.yml
   Will retrieve '/internalusers' into /usr/share/opensearch/backups/internal_users.yml 
      SUCC: Configuration for 'internalusers' stored in /usr/share/opensearch/backups/internal_users.yml
   Will retrieve '/actiongroups' into /usr/share/opensearch/backups/action_groups.yml 
      SUCC: Configuration for 'actiongroups' stored in /usr/share/opensearch/backups/action_groups.yml
   Will retrieve '/tenants' into /usr/share/opensearch/backups/tenants.yml 
      SUCC: Configuration for 'tenants' stored in /usr/share/opensearch/backups/tenants.yml
   Will retrieve '/nodesdn' into /usr/share/opensearch/backups/nodes_dn.yml 
      SUCC: Configuration for 'nodesdn' stored in /usr/share/opensearch/backups/nodes_dn.yml
   Will retrieve '/whitelist' into /usr/share/opensearch/backups/whitelist.yml 
      SUCC: Configuration for 'whitelist' stored in /usr/share/opensearch/backups/whitelist.yml
   Will retrieve '/audit' into /usr/share/opensearch/backups/audit.yml 
      SUCC: Configuration for 'audit' stored in /usr/share/opensearch/backups/audit.yml
   ```
1. **選用**：建立 TLS 憑證的備份目錄並儲存憑證副本。如果您使用不同的 TLS 憑證，請對每個節點重複此步驟：
   ```bash
   mkdir /usr/share/opensearch/backups/certs && cp /usr/share/opensearch/config/*pem /usr/share/opensearch/backups/certs/
   ```
   {% include copy.html %}
1. 結束偽 TTY 工作階段：
   ```bash
   exit
   ```
   {% include copy.html %}
1. 將檔案複製到您的主機：
   ```bash
   docker cp os-node-01:/usr/share/opensearch/backups ~/deploy/
   ```
   {% include copy.html %}

## 執行升級

現在叢集已完成設定，您也已備份重要檔案與設定，是時候開始版本升級了。

本節中的某些步驟，例如停用分片複寫與排清交易記錄，不會影響叢集的效能。這些步驟是作為最佳實務而納入，在用戶端於整個升級過程中持續與 OpenSearch 叢集互動的情況下（例如查詢現有資料或將文件編製索引），可顯著提升叢集效能。
{: .note}

1. 停用分片複寫，以停止 Lucene 索引分段在叢集內的移動：
   ```bash
   curl -H 'Content-type: application/json' \
      -X PUT "https://localhost:9201/_cluster/settings?pretty" \
      -d'{"persistent":{"cluster.routing.allocation.enable":"primaries"}}' \
      -ku admin:<custom-admin-password>
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
1. 對叢集執行排清作業，將交易記錄項目提交至 Lucene 索引：
   ```bash
   curl -X POST "https://localhost:9201/_flush?pretty" -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
      "_shards" : {
         "total" : 20,
         "successful" : 20,
         "failed" : 0
      }
   }
   ```
1. 選取要升級的節點。您可以以任何順序升級節點，因為此示範叢集中的所有節點都是合格的叢集管理員節點。下列命令將會停止並移除容器 `os-node-01`，但不會移除已掛載的資料儲存空間：
   ```bash
   docker stop os-node-01 && docker container rm os-node-01
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:2.5.0` 映像啟動名為 `os-node-01` 的新容器，並使用與原始容器相同的掛載儲存空間：
   ```bash
   docker run -d \
      -p 9201:9200 -p 9601:9600 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-01:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-01.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-01.pem:/usr/share/opensearch/config/os-node-01.pem \
      -v ~/deploy/os-node-01-key.pem:/usr/share/opensearch/config/os-node-01-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.11 \
      --name os-node-01 \
      opensearchproject/opensearch:2.5.0
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   d26d0cb2e1e93e9c01bb00f19307525ef89c3c3e306d75913860e6542f729ea4
   ```
1. **選用**：查詢叢集以判斷哪個節點正擔任叢集管理員。您可以在過程中的任何時間執行此命令，以查看何時選出新的叢集管理員：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,master" \
      -ku admin:<custom-admin-password> | column -t
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   name        version  node.role  master
   os-node-01  2.5.0    dimr       -
   os-node-04  1.3.7    dimr       *
   os-node-02  1.3.7    dimr       -
   os-node-03  1.3.7    dimr       -
   ```
1. **選用**：查詢叢集以查看節點移除與替換時分片分配的變化。您可以在過程中的任何時間執行此命令，以查看分片狀態的變化：
   ```bash
   curl -s "https://localhost:9201/_cat/shards" \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   security-auditlog-2023.03.06           0 p STARTED       53 214.5kb 172.20.0.13 os-node-03
   security-auditlog-2023.03.06           0 r UNASSIGNED                           
   .kibana_1                              0 p STARTED        3  14.5kb 172.20.0.12 os-node-02
   .kibana_1                              0 r STARTED        3  14.5kb 172.20.0.13 os-node-03
   ecommerce                              0 p STARTED     4675   3.9mb 172.20.0.12 os-node-02
   ecommerce                              0 r STARTED     4675   3.9mb 172.20.0.14 os-node-04
   security-auditlog-2023.03.07           0 p STARTED       37 175.7kb 172.20.0.14 os-node-04
   security-auditlog-2023.03.07           0 r UNASSIGNED                           
   .opendistro_security                   0 p STARTED       10  67.9kb 172.20.0.12 os-node-02
   .opendistro_security                   0 r STARTED       10  67.9kb 172.20.0.13 os-node-03
   .opendistro_security                   0 r STARTED       10  64.5kb 172.20.0.14 os-node-04
   .opendistro_security                   0 r UNASSIGNED                           
   security-auditlog-2023.02.27           0 p STARTED        4  80.5kb 172.20.0.12 os-node-02
   security-auditlog-2023.02.27           0 r UNASSIGNED                           
   security-auditlog-2023.02.28           0 p STARTED        6 104.1kb 172.20.0.14 os-node-04
   security-auditlog-2023.02.28           0 r UNASSIGNED                           
   opensearch_dashboards_sample_data_logs 0 p STARTED    14074   9.1mb 172.20.0.12 os-node-02
   opensearch_dashboards_sample_data_logs 0 r STARTED    14074   8.9mb 172.20.0.13 os-node-03
   .kibana_92668751_admin_1               0 r STARTED       33  37.3kb 172.20.0.13 os-node-03
   .kibana_92668751_admin_1               0 p STARTED       33  37.3kb 172.20.0.14 os-node-04
   ```
1. 停止 `os-node-02`：
   ```bash
   docker stop os-node-02 && docker container rm os-node-02
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:2.5.0` 映像啟動名為 `os-node-02` 的新容器，並使用與原始容器相同的對應磁碟區：
   ```bash
   docker run -d \
      -p 9202:9200 -p 9602:9600 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-02:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-02.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-02.pem:/usr/share/opensearch/config/os-node-02.pem \
      -v ~/deploy/os-node-02-key.pem:/usr/share/opensearch/config/os-node-02-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.12 \
      --name os-node-02 \
      opensearchproject/opensearch:2.5.0
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   7b802865bd6eb420a106406a54fc388ed8e5e04f6cbd908c2a214ea5ce72ac00
   ```
1. 停止 `os-node-03`：
   ```bash
   docker stop os-node-03 && docker container rm os-node-03
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:2.5.0` 映像啟動名為 `os-node-03` 的新容器，並使用與原始容器相同的對應磁碟區：
   ```bash
   docker run -d \
      -p 9203:9200 -p 9603:9600 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-03:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-03.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-03.pem:/usr/share/opensearch/config/os-node-03.pem \
      -v ~/deploy/os-node-03-key.pem:/usr/share/opensearch/config/os-node-03-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.13 \
      --name os-node-03 \
      opensearchproject/opensearch:2.5.0
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   d7f11726841a89eb88ff57a8cbecab392399f661a5205f0c81b60a995fc6c99d
   ```
1. 停止 `os-node-04`：
   ```bash
   docker stop os-node-04 && docker container rm os-node-04
   ```
   {% include copy.html %}
1. 使用 `opensearchproject/opensearch:2.5.0` 映像啟動名為 `os-node-04` 的新容器，並使用與原始容器相同的對應磁碟區：
   ```bash
   docker run -d \
      -p 9204:9200 -p 9604:9600 \
      -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \
      --ulimit nofile=65536:65536 --ulimit memlock=-1:-1 \
      -v data-04:/usr/share/opensearch/data \
      -v repo-01:/usr/share/opensearch/snapshots \
      -v ~/deploy/opensearch-04.yml:/usr/share/opensearch/config/opensearch.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch/config/root-ca.pem \
      -v ~/deploy/admin.pem:/usr/share/opensearch/config/admin.pem \
      -v ~/deploy/admin-key.pem:/usr/share/opensearch/config/admin-key.pem \
      -v ~/deploy/os-node-04.pem:/usr/share/opensearch/config/os-node-04.pem \
      -v ~/deploy/os-node-04-key.pem:/usr/share/opensearch/config/os-node-04-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.14 \
      --name os-node-04 \
      opensearchproject/opensearch:2.5.0
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   26f8286ab11e6f8dcdf6a83c95f265172f9557578a1b292af84c6f5ef8738e1d
   ```
1. 確認您的叢集執行的是新版本：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,master" \
      -ku admin:<custom-admin-password> | column -t
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   name        version  node.role  master
   os-node-01  2.5.0    dimr       *
   os-node-02  2.5.0    dimr       -
   os-node-04  2.5.0    dimr       -
   os-node-03  2.5.0    dimr       -
   ```
1. 您應升級的最後一個元件是 OpenSearch Dashboards 節點。首先，停止並移除舊容器：
   ```bash
   docker stop os-dashboards-01 && docker rm os-dashboards-01
   ```
   {% include copy.html %}
1. 建立執行目標版本 OpenSearch Dashboards 的新容器：
   ```bash
   docker run -d \
      -p 5601:5601 --expose 5601 \
      -v ~/deploy/opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml \
      -v ~/deploy/root-ca.pem:/usr/share/opensearch-dashboards/config/root-ca.pem \
      -v ~/deploy/os-dashboards-01.pem:/usr/share/opensearch-dashboards/config/os-dashboards-01.pem \
      -v ~/deploy/os-dashboards-01-key.pem:/usr/share/opensearch-dashboards/config/os-dashboards-01-key.pem \
      --network opensearch-dev-net \
      --ip 172.20.0.10 \
      --name os-dashboards-01 \
      opensearchproject/opensearch-dashboards:2.5.0
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   310de7a24cf599ca0b39b241db07fa8865592ebe15b6f5fda26ad19d8e1c1e09
   ```
1. 確認 OpenSearch Dashboards 容器已正確啟動。可使用類似下列的命令來確認對 `https://<HOST_ADDRESS>:5601` 的請求會重新導向 (HTTP 狀態碼 302) 至 `/app/login?`：
   ```bash
   curl https://localhost:5601 -kI
   ```
   {% include copy.html %}

   回應應類似下列內容：

   ```bash
   HTTP/1.1 302 Found
   location: /app/login?
   osd-name: opensearch-dashboards-dev
   cache-control: private, no-cache, no-store, must-revalidate
   set-cookie: security_authentication=; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Secure; HttpOnly; Path=/
   content-length: 0
   Date: Wed, 08 Mar 2023 15:36:53 GMT
   Connection: keep-alive
   Keep-Alive: timeout=120
   ```
1. 重新啟用副本分片的配置：
   ```bash
   curl -H 'Content-type: application/json' \
      -X PUT "https://localhost:9201/_cluster/settings?pretty" \
      -d'{"persistent":{"cluster.routing.allocation.enable":"all"}}' \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似下列內容：

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

您已成功部署安全的 OpenSearch 叢集、將資料編製索引、建立填入範例資料的儀表板、建立新的內部使用者、備份重要檔案，並將叢集從 1.3.7 版升級至 2.5.0 版。在繼續探索與實驗 OpenSearch 和 OpenSearch Dashboards 之前，您應該先驗證升級的結果。

針對此叢集，升級後的驗證步驟可以包括確認以下項目：

- [執行版本](#verifying-the-new-running-version)
- [健康狀態與分片配置](#verifying-cluster-health-and-shard-allocation)
- [資料一致性](#verifying-data-consistency)

### 確認新的執行版本

1. 確認 OpenSearch 節點目前的執行版本：
   ```bash
   curl -s "https://localhost:9201/_cat/nodes?v&h=name,version,node.role,master" \
      -ku admin:<custom-admin-password> | column -t
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   name        version  node.role  master
   os-node-01  2.5.0    dimr       *
   os-node-02  2.5.0    dimr       -
   os-node-04  2.5.0    dimr       -
   os-node-03  2.5.0    dimr       -
   ```
1. 確認 OpenSearch Dashboards 目前的執行版本：
   1. **選項 1**：從網頁介面確認 OpenSearch Dashboards 版本。
      1. 開啟網頁瀏覽器並前往 Docker 主機上的連接埠 `5601` (例如 `https://<HOST_ADDRESS>:5601`)。
      1. 使用預設使用者名稱 (`admin`) 和預設密碼 (`admin`) 登入。
      1. 選取右上角的 **Help button**。版本會顯示在快顯視窗中。
      1. 再次選取 **Help button** 以關閉快顯視窗。
   1. **選項 2**：透過檢查 `manifest.yml` 來確認 OpenSearch Dashboards 版本。
      1. 從命令列開啟與 OpenSearch Dashboards 容器的互動式偽 TTY 工作階段：
         ```bash
         docker exec -it os-dashboards-01 bash
         ```
         {% include copy.html %}
      1. 檢查 `manifest.yml` 中的版本：
         ```bash
         head -n 5 manifest.yml 
         ```
         {% include copy.html %}

         回應應類似如下：

         ```bash
         ---
         schema-version: '1.1'
         build:
            name: OpenSearch Dashboards
            version: 2.5.0
         ```
      1. 結束偽 TTY 工作階段：
         ```bash
         exit
         ```
         {% include copy.html %}

### 確認叢集健康狀態與分片配置

1. 查詢 [Cluster health]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) API 端點以查看叢集健康狀態的資訊。您應該會看到 `green` 狀態，表示所有主要分片與副本分片皆已配置：
   ```bash
   curl -s "https://localhost:9201/_cluster/health?pretty" -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似如下：

   ```json
   {
      "cluster_name" : "opensearch-dev-cluster",
      "status" : "green",
      "timed_out" : false,
      "number_of_nodes" : 4,
      "number_of_data_nodes" : 4,
      "discovered_master" : true,
      "discovered_cluster_manager" : true,
      "active_primary_shards" : 16,
      "active_shards" : 36,
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
   curl -s "https://localhost:9201/_cat/shards" -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應類似如下：

   ```bash
   security-auditlog-2023.02.27           0 r STARTED     4  80.5kb 172.20.0.13 os-node-03
   security-auditlog-2023.02.27           0 p STARTED     4  80.5kb 172.20.0.11 os-node-01
   security-auditlog-2023.03.08           0 p STARTED    30  95.2kb 172.20.0.13 os-node-03
   security-auditlog-2023.03.08           0 r STARTED    30 123.8kb 172.20.0.11 os-node-01
   ecommerce                              0 p STARTED  4675   3.9mb 172.20.0.12 os-node-02
   ecommerce                              0 r STARTED  4675   3.9mb 172.20.0.13 os-node-03
   .kibana_1                              0 p STARTED     3   5.9kb 172.20.0.12 os-node-02
   .kibana_1                              0 r STARTED     3   5.9kb 172.20.0.11 os-node-01
   .kibana_92668751_admin_1               0 p STARTED    33  37.3kb 172.20.0.13 os-node-03
   .kibana_92668751_admin_1               0 r STARTED    33  37.3kb 172.20.0.11 os-node-01
   opensearch_dashboards_sample_data_logs 0 p STARTED 14074   9.1mb 172.20.0.12 os-node-02
   opensearch_dashboards_sample_data_logs 0 r STARTED 14074   9.1mb 172.20.0.14 os-node-04
   security-auditlog-2023.02.28           0 p STARTED     6  26.2kb 172.20.0.11 os-node-01
   security-auditlog-2023.02.28           0 r STARTED     6  26.2kb 172.20.0.14 os-node-04
   .opendistro-reports-definitions        0 p STARTED     0    208b 172.20.0.12 os-node-02
   .opendistro-reports-definitions        0 r STARTED     0    208b 172.20.0.13 os-node-03
   .opendistro-reports-definitions        0 r STARTED     0    208b 172.20.0.14 os-node-04
   security-auditlog-2023.03.06           0 r STARTED    53 174.6kb 172.20.0.12 os-node-02
   security-auditlog-2023.03.06           0 p STARTED    53 174.6kb 172.20.0.14 os-node-04
   .kibana_101107607_newuser_1            0 r STARTED     1   5.1kb 172.20.0.13 os-node-03
   .kibana_101107607_newuser_1            0 p STARTED     1   5.1kb 172.20.0.11 os-node-01
   .opendistro_security                   0 r STARTED    10  64.5kb 172.20.0.12 os-node-02
   .opendistro_security                   0 r STARTED    10  64.5kb 172.20.0.13 os-node-03
   .opendistro_security                   0 r STARTED    10  64.5kb 172.20.0.11 os-node-01
   .opendistro_security                   0 p STARTED    10  64.5kb 172.20.0.14 os-node-04
   .kibana_-152937574_admintenant_1       0 r STARTED     1   5.1kb 172.20.0.12 os-node-02
   .kibana_-152937574_admintenant_1       0 p STARTED     1   5.1kb 172.20.0.14 os-node-04
   security-auditlog-2023.03.07           0 r STARTED    37 175.7kb 172.20.0.12 os-node-02
   security-auditlog-2023.03.07           0 p STARTED    37 175.7kb 172.20.0.14 os-node-04
   .kibana_92668751_admin_2               0 p STARTED    34  38.6kb 172.20.0.13 os-node-03
   .kibana_92668751_admin_2               0 r STARTED    34  38.6kb 172.20.0.11 os-node-01
   .kibana_2                              0 p STARTED     3     6kb 172.20.0.13 os-node-03
   .kibana_2                              0 r STARTED     3     6kb 172.20.0.14 os-node-04
   .opendistro-reports-instances          0 r STARTED     0    208b 172.20.0.12 os-node-02
   .opendistro-reports-instances          0 r STARTED     0    208b 172.20.0.11 os-node-01
   .opendistro-reports-instances          0 p STARTED     0    208b 172.20.0.14 os-node-04
   ```

### 驗證資料一致性

您需要再次查詢電子商務索引，以確認範例資料仍然存在：

1. 將此查詢的回應與您在 [Indexing data with the REST API](#indexing-data-with-the-rest-api) 的[最後一個步驟](#validation)中收到的回應進行比較：
   ```bash
   curl -H 'Content-Type: application/json' \
      -X GET "https://localhost:9201/ecommerce/_search?pretty=true&filter_path=hits.total" \
      -d'{"query":{"match":{"customer_first_name":"Sonya"}}}' \
      -ku admin:<custom-admin-password>
   ```
   {% include copy.html %}

   回應應該會類似以下內容：

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
1. 開啟網頁瀏覽器並前往 Docker 主機上的連接埠 `5601` (例如 `https://<HOST_ADDRESS>:5601`)。
1. 輸入預設的使用者名稱 (`admin`) 與密碼 (`admin`)。
1. 在 OpenSearch Dashboards 的 **Home** 頁面上，選取網頁介面左上角的 **Menu button** 以開啟 **Navigation pane**。
1. 選取 **Dashboard**。
1. 選擇 **[Logs] Web Traffic** 以開啟您先前在此程序中新增範例資料時所建立的儀表板。
1. 檢視完儀表板後，選取 **Profile** 按鈕。選擇 **Log out**，以便以其他使用者身分登入。
1. 輸入您在升級前建立的使用者名稱與密碼，然後選取 **Log in**。

## 後續步驟

檢閱下列資源，以進一步了解 OpenSearch 的運作方式：

- [REST API reference]({{site.url}}{{site.baseurl}}/api-reference/index/)
- [Getting started with OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/getting-started/)
- [About Security in OpenSearch]({{site.url}}{{site.baseurl}}/security/index/)
