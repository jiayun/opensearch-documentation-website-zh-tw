---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "滾動升級"
nav_order: 20
has_children: true
has_toc: false
permalink: /migrate-or-upgrade/rolling-upgrade/
nav_exclude: false
redirect_from:
 - /upgrade-opensearch/
 - /rolling-upgrade/index/
 - /install-and-configure/upgrade-opensearch/rolling-upgrade/
---

# 滾動升級

滾動升級（有時稱為「節點替換升級」）幾乎可以在不停機的情況下於執行中的叢集上進行。節點會逐一停止並就地升級。或者，也可以一次一個地停止節點，並以執行新版本的主機取代。在此過程中，您仍可繼續在叢集中編製索引及查詢資料。

本文件提供滾動升級程序的高階、平台無關概覽。如需指令、指令碼與組態檔的具體範例，請參閱 [滾動升級實驗室]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/rolling-upgrade-lab/)。

## 準備升級
在對您的 OpenSearch 叢集進行任何變更之前，強烈建議先備份您的組態檔，並為叢集狀態與索引建立[快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)。

**重要**：OpenSearch 節點**無法降級**。如果您需要復原升級，就必須重新安裝 OpenSearch，並從快照還原叢集。請在開始升級程序之前建立快照，並將其儲存在遠端儲存庫中。滾動升級**僅支援相鄰的主要版本之間**，例如從 OpenSearch 1.x 升級到 2.x，但不支援從 1.x 升級到 3.x。
{: .important}

**重要**：升級至 3.x.x 所需的最低叢集版本為 2.19.0。
{: .important}

### 跨叢集複寫

如果您的叢集使用[跨叢集複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/)，升級時請遵循以下準則：

- **單向複寫**：先升級追隨者叢集，再升級領導者叢集。
- **雙向複寫**：先停止其中一個方向的複寫，然後升級兩個叢集。對於仍在運作的複寫，先升級追隨者叢集，再升級領導者叢集。兩個叢集都升級完成後，再恢復已停止的複寫。

## 執行升級

1. 開始之前，請先確認 OpenSearch 叢集的健康狀態。您應在升級前解決任何索引或分片分配問題，以確保資料不會遺失。**green** 狀態表示所有主要分片與副本分片皆已分配。如需更多資訊，請參閱 [Cluster health]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)。下列指令查詢 `_cluster/health` API 端點：
   ```json
   GET "/_cluster/health?pretty"
   ```
   回應應類似於下列範例：
   ```json
   {
       "cluster_name":"opensearch-dev-cluster",
       "status":"green",
       "timed_out":false,
       "number_of_nodes":4,
       "number_of_data_nodes":4,
       "active_primary_shards":1,
       "active_shards":4,
       "relocating_shards":0,
       "initializing_shards":0,
       "unassigned_shards":0,
       "delayed_unassigned_shards":0,
       "number_of_pending_tasks":0,
       "number_of_in_flight_fetch":0,
       "task_max_waiting_in_queue_millis":0,
       "active_shards_percent_as_number":100.0
   }
   ```
1. 停用分片複寫，以防止在節點離線期間建立分片副本。這會停止叢集中節點上 Lucene 索引分段的移動。您可以透過查詢 `_cluster/settings` API 端點來停用分片複寫：
   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.routing.allocation.enable": "primaries"
       }
   }
   ```
   回應應類似於下列範例：
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

1. 對叢集執行排清作業，將異動記錄項目提交至 Lucene 索引：
   ```json
   POST "/_flush?pretty"
   ```
   回應應類似於下列範例：
   ```json
   {
     "_shards" : {
       "total" : 4,
       "successful" : 4,
       "failed" : 0
     }
   }
   ```
1. 檢查您的叢集並找出第一個要升級的節點。節點應依照下列順序升級：

    1. 資料節點
    1. 資料匯入／機器學習（ML）／協調節點
    1. 叢集管理員節點

    符合資格的叢集管理員節點應最後升級，因為 OpenSearch 節點可以加入執行較舊版本的叢集管理員節點所在的叢集，但無法加入所有叢集管理員節點都執行較新版本的叢集。
    {: .important}

1. 查詢 `_cat/nodes` 端點，以確認哪個節點被提升為叢集管理員。下列指令包含額外的查詢參數，僅請求 name、version、node.role 與 master 標頭。請注意，OpenSearch 1.x 版本使用「master」一詞，該詞已被棄用，並在 OpenSearch 2.x 及之後的版本中由「cluster_manager」取代。
   ```bash
   GET "/_cat/nodes?v&h=name,version,node.role,master" | column -t
   ```
   回應應類似於下列範例：
   ```bash
   name        version  node.role  master
   os-node-01  7.10.2   dimr       -
   os-node-04  7.10.2   dimr       -
   os-node-03  7.10.2   dimr       -
   os-node-02  7.10.2   dimr       *
   ```
1. 停止您要升級的節點。如果在 Docker 中執行，刪除容器時請勿刪除與該容器關聯的儲存區。新的 OpenSearch 容器將使用現有的儲存區。**刪除儲存區將導致資料遺失**。
1. 透過查詢 `_cat/nodes` API 端點，確認相關節點已從叢集中移除：
   ```bash
   GET "/_cat/nodes?v&h=name,version,node.role,master" | column -t
   ```
   回應應類似於下列範例：
   ```bash
   name        version  node.role  master
   os-node-02  7.10.2   dimr       *
   os-node-04  7.10.2   dimr       -
   os-node-03  7.10.2   dimr       -
   ```
   `os-node-01` 已不再列出，因為容器已被停止並刪除。
1. 升級節點：
     - 如果在 Docker 中執行，請部署一個執行所需 OpenSearch 版本的新容器，並對應到與您刪除的容器相同的儲存區。
     - 如果使用 [Debian]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/debian/) 或 [RPM]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/) 套件升級，請使用 `rpm`、`yum` 或 `dpkg` 安裝 OpenSearch，並啟動服務。由於位置與檔案都會保留，因此無需進一步設定。
     - 如果使用 [Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/) 升級，則需要執行下列動作：
        - 備份 `jvm.options`、`opensearch.yml`、憑證以及 `data` 資料夾。
        - 解壓縮新的 tarball。
        - 將先前的 `data` 目錄複製到新的 `data` 目錄，**否則資料將會遺失**。
        - 將先前的 `opensearch.yml` 檔案複製到新的 `config/opensearch.yml` 檔案。
        - 將先前的 `jvm.options` 檔案複製到新的 `config/jvm.options` 檔案。
        - 將 `opensearch.yml` 檔案中列出的 TLS 憑證複製到 `./config/` 目錄。
        - 啟動 OpenSearch。
1. 在新節點上執行 OpenSearch 後，查詢 `_cat/nodes` 端點以確認它已加入叢集：
   ```bash
   GET "/_cat/nodes?v&h=name,version,node.role,master" | column -t
   ```
   回應應類似於下列範例：
   ```bash
   name        version  node.role  master
   os-node-02  7.10.2   dimr       *
   os-node-04  7.10.2   dimr       -
   os-node-01  7.10.2   dimr       -
   os-node-03  7.10.2   dimr       -
   ```
   在範例輸出中，新的 OpenSearch 節點向叢集回報的執行版本為 `7.10.2`。這是 `compatibility.override_main_response_version` 的結果，用於連線至會檢查版本的舊式用戶端所在的叢集。您可以透過呼叫 `/_nodes` API 端點手動確認節點的版本，如下列指令所示。請將 `<nodeName>` 取代為您的節點名稱。如需更多資訊，請參閱 [Nodes API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/)。
   ```bash
   GET "/_nodes/{nodeName}?pretty=true" | jq -r '.nodes | .[] | "\(.name) v\(.version)"'
   ```
   回應應類似於下列範例：
   ```bash
   os-node-01 v1.3.7
   ```
1. 重新啟用分片複寫：
   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.routing.allocation.enable": "all"
       }
   }
   ```
   回應應類似於下列範例：
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
1. 確認叢集健康狀態良好：
   ```bash
   GET "/_cluster/health?pretty"
   ```
   回應應類似於下列範例：
   ```json
   {
     "cluster_name" : "opensearch-dev-cluster",
     "status" : "green",
     "timed_out" : false,
     "number_of_nodes" : 4,
     "number_of_data_nodes" : 4,
     "discovered_master" : true,
     "active_primary_shards" : 1,
     "active_shards" : 4,
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
1. 對叢集中的每個節點重複步驟 2 至 11。請記得最後升級符合資格的叢集管理員節點。取代最後一個節點後，查詢 `_cat/nodes` 端點以確認所有節點都已加入叢集。此時叢集已完成新版本 OpenSearch 的引導。您可以透過查詢 `_cat/nodes` API 端點來驗證叢集版本：
   ```bash
   GET "/_cat/nodes?v&h=name,version,node.role,master" | column -t
   ```
   回應應類似於下列範例：
   ```bash
   name        version  node.role  master
   os-node-04  1.3.7    dimr       -
   os-node-02  1.3.7    dimr       *
   os-node-01  1.3.7    dimr       -
   os-node-03  1.3.7    dimr       -
   ```
1. 升級現已完成，您可以開始使用最新的功能與修正。

## 輪流重新啟動

輪流重新啟動遵循與滾動升級相同的逐步程序，差別在於不升級實際節點。在輪流重新啟動期間，節點會逐一重新啟動——通常是為了套用組態變更、更新憑證或執行系統層級維護——而不會中斷叢集可用性。

若要執行輪流重新啟動，請遵循[執行升級](#performing-the-upgrade)中所述的步驟，但排除涉及升級 OpenSearch 二進位檔或容器映像的步驟：

1. **檢查叢集健康狀態**  
   確保叢集狀態為綠色，且所有分片皆已分配。  
   _（請參閱滾動升級程序中的[步驟 1](#performing-the-upgrade)）_

2. **停用分片分配**  
   防止 OpenSearch 在節點離線時嘗試重新分配分片。  
   _（請參閱滾動升級程序中的[步驟 2](#performing-the-upgrade)）_

3. **排清交易記錄**  
   將最近的作業提交至 Lucene，以縮短復原時間。  
   _（請參閱滾動升級程序中的[步驟 3](#performing-the-upgrade)）_

4. **檢閱並識別下一個要重新啟動的節點**  
   確保最後才重新啟動目前的叢集管理員節點。  
   _（請參閱滾動升級程序中的[步驟 4](#performing-the-upgrade)）_

5. **檢查哪個節點是目前叢集管理員**  
   使用 `_cat/nodes` API 判斷哪個節點是目前作用中的叢集管理員。  
   _（請參閱滾動升級程序中的[步驟 5](#performing-the-upgrade)）_

6. **停止節點**  
   正常關閉節點。請勿刪除相關聯的資料磁碟區。  
   _（請參閱滾動升級程序中的[步驟 6](#performing-the-upgrade)）_

7. **確認節點已離開叢集**  
   使用 `_cat/nodes` 驗證該節點已不再列出。  
   _（請參閱滾動升級程序中的[步驟 7](#performing-the-upgrade)）_

8. **重新啟動節點**  
   啟動相同的節點（相同的二進位檔/版本/組態），並讓它重新加入叢集。  
   _（請參閱滾動升級程序中的[步驟 8](#performing-the-upgrade)——不升級二進位檔）_

9. **驗證重新啟動的節點已重新加入**  
   檢查 `_cat/nodes` 以確認該節點存在且狀況良好。  
   _（請參閱滾動升級程序中的[步驟 9](#performing-the-upgrade)）_

10. **重新啟用分片分配**  
    還原完整的分片移動能力。  
    _（請參閱滾動升級程序中的[步驟 10](#performing-the-upgrade)）_

11. **確認叢集健康狀態為綠色**  
    在重新啟動下一個節點之前驗證穩定性。  
    _（請參閱滾動升級程序中的[步驟 11](#performing-the-upgrade)）_

12. **對所有其他節點重複此程序**  
    逐一重新啟動每個節點。如果某個節點符合叢集管理員角色的資格，請最後再重新啟動它。  
    _（請參閱滾動升級程序中的[步驟 12](#performing-the-upgrade)——同樣地，沒有升級步驟）_

藉由維持法定人數並依序重新啟動節點，輪流重新啟動可確保零停機時間與完整的資料持續性。

## 相關文件

- [滾動升級實驗室]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/rolling-upgrade-lab/) -- 提供逐步指示的實作實驗室，可在測試環境中練習滾動升級。
- [OpenSearch 組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [Performance Analyzer]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/index/)
- [安裝並設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)
- [關於 OpenSearch 中的安全性]({{site.url}}{{site.baseurl}}/security/index/)
