---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移至以遠端儲存空間為後端的儲存架構"
nav_order: 5
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# 遷移至以遠端儲存空間為後端的儲存架構

於 2.15 版導入
{: .label .label-purple }

以遠端儲存空間為後端的儲存架構提供一種防止資料遺失的新方式，會自動建立所有索引交易的備份，並將其傳送至遠端儲存空間。若要使用此功能，必須啟用[分段複製]({{site.url}}{{site.baseurl}}/opensearch/segment-replication/)。

您可以透過滾動升級機制，將以文件複製為基礎的叢集遷移至以遠端儲存空間為後端的儲存架構。

滾動升級，有時稱為*節點替換升級*，幾乎可以在不停機的情況下於執行中的叢集上進行。節點會個別停止並就地遷移。或者，節點也可以一次一個地停止，並由使用遠端儲存空間的主機取代。在此過程中，您仍可繼續在叢集中編製索引與查詢資料。

## 準備遷移

在對 OpenSearch 叢集進行任何變更之前，請先檢閱[升級 OpenSearch]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/index/)，以了解有關備份組態檔以及建立叢集狀態與索引快照的建議。

在遷移至以遠端儲存空間為後端的儲存架構之前，請先升級至 OpenSearch 2.15 或更新版本。

在升級至 OpenSearch 2.15 之前，請先建立叢集快照並將其儲存在遠端。OpenSearch 2.15 節點無法還原為文件複製。如果需要復原遷移，請執行全新的 OpenSearch 安裝，並從遠端快照還原。將快照儲存在遠端，可在遷移過程中發生問題時供您擷取並還原。
{: .important}

## 執行升級

1. 在開始之前，使用 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) 驗證 OpenSearch 叢集的健康狀態。請在升級前解決任何索引或分片配置問題，以確保資料受到保存。狀態為 **green** 表示所有主要與副本分片皆已配置。您可以使用類似下列的命令查詢 `_cluster/health` API 端點：

   ```json
   GET "/_cluster/health?pretty"
   ```

   您應該會收到類似下列的回應：

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
   
1. 停用分片複製，以防止在節點離線時建立分片副本。這會停止叢集中節點上 Lucene 索引分段的移動。您可以透過查詢 `_cluster/settings` API 端點來停用分片複製，如下列範例所示：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.routing.allocation.enable": "primaries"
       }
   }
   ```
   您應該會收到類似下列的回應：
   
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

1. 在叢集上執行下列排清作業，將交易記錄項目提交至 Lucene 索引：

   ```json
   POST "/_flush?pretty"
   ```

   您應該會收到類似下列的回應：
   
   ```json
   {
     "_shards" : {
       "total" : 4,
       "successful" : 4,
       "failed" : 0
     }
   }
   ```

1. 將 `cluster.remote_store.compatibility_mode` 設定設為 `mixed`，以允許使用遠端儲存空間的節點加入叢集。接著將 `cluster.migration.direction` 設為 `remote_store`，這會將新索引配置至使用遠端儲存空間的資料節點。下列範例使用 Cluster Settings API 更新前述設定：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.remote_store.compatibility_mode": "mixed",
           "cluster.migration.direction" :  "remote_store"
       }
   }
   ```
   您應該會收到類似下列的回應：
   
   ```json
   {
     "acknowledged" : true,
     "persistent" : {
        "cluster" : { 
        "remote_store" : {
          "compatibility_mode" : "mixed",
          "migration.direction" :  "remote_store"
        }
      },
      "transient" : { }
    }
   }
   ```
   
1. 檢查您的叢集，並找出第一個要升級的節點。
1. 在 `opensearch.yml` 中以節點屬性的形式提供遠端儲存庫詳細資訊，如下列範例所示：

   ```yml
   # Repository name
   node.attr.remote_store.segment.repository: my-repo-1
   node.attr.remote_store.translog.repository: my-repo-2
   node.attr.remote_store.state.repository: my-repo-3
   
   # Segment repository settings
   node.attr.remote_store.repository.my-repo-1.type: s3
   node.attr.remote_store.repository.my-repo-1.settings.bucket: <Bucket Name 1>
   node.attr.remote_store.repository.my-repo-1.settings.base_path: <Bucket Base Path 1>
   node.attr.remote_store.repository.my-repo-1.settings.region: us-east-1
   
   # Translog repository settings
   node.attr.remote_store.repository.my-repo-2.type: s3
   node.attr.remote_store.repository.my-repo-2.settings.bucket: <Bucket Name 2>
   node.attr.remote_store.repository.my-repo-2.settings.base_path: <Bucket Base Path 2>
   node.attr.remote_store.repository.my-repo-2.settings.region: us-east-1
   
   # Enable Remote cluster state cluster setting
   cluster.remote_store.state.enabled: true
   
   # Remote cluster state repository settings
   node.attr.remote_store.repository.my-repo-3.type: s3
   node.attr.remote_store.repository.my-repo-3.settings.bucket: <Bucket Name 3>
   node.attr.remote_store.repository.my-repo-3.settings.base_path: <Bucket Base Path 3>
   node.attr.remote_store.repository.my-repo-3.settings.region: <Bucket region>
   
   ```

1. 停止要遷移的節點。刪除容器時，請勿刪除與該容器關聯的磁碟區。新的 OpenSearch 容器將使用現有的磁碟區。**刪除磁碟區將導致資料遺失**。

1. 部署一個執行相同版本 OpenSearch 的新容器，並將其對應至與您刪除的容器相同的磁碟區。

1. 在新節點上執行 OpenSearch 後，查詢 `_cat/nodes` 端點以確認其已加入叢集。等待叢集再次變為 green。

1. 對叢集中的每個節點重複步驟 6 至 9。 

1. 使用類似下列的命令重新啟用分片複製：

   ```json
   PUT _cluster/settings?pretty
   {
       "persistent": {
           "cluster.routing.allocation.enable": "all"
       }
   }
   ```
   
   您應該會收到類似下列的回應：
   
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
   
1. 使用 Cluster Health API 確認叢集健康狀態，如下列命令所示：

   ```bash
   GET _cluster/health?pretty
   ```
   您應該會收到類似下列的回應：
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
   
1. 使用下列命令清除 `remote_store.compatibility_mode` 與 `migration.direction` 設定，以避免非遠端節點加入叢集：
 
   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.remote_store.compatibility_mode": null,
            "cluster.migration.direction" :  null
       }
   }
   ```

   您應該會收到類似下列的回應：
   ```json
   {
     "acknowledged" : true,
     "persistent" : { 
        "cluster.remote_store.compatibility_mode": null,
         "cluster.migration.direction" :  null
      },
      "transient" : { }
   }
   ```
   
遷移至遠端儲存空間的程序現已完成。


## 相關叢集設定

使用下列叢集設定來啟用遷移至以遠端儲存空間為後端的叢集。

| 欄位                                      | 資料類型 | 說明 |
|:------------------------------------------|:--- |:---|
| `cluster.remote_store.compatibility_mode` | 字串  | 設為 `strict` 時，僅允許建立非遠端或遠端節點（依初始叢集類型而定）。設為 `mixed` 時，允許遠端與非遠端節點加入叢集。預設為 `strict`。 |  
| `cluster.migration.direction`             | 字串 |  僅在使用遠端儲存空間的節點上建立新分片。預設為 `None`。 |                                                                                                                                                                                            

