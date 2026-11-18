---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移至以遠端儲存空間為後端的儲存架構"
nav_order: 5
parent: Remote-backed storage
grand_parent: Availability and recovery
canonical_url: https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/remote-store/migrating-to-remote/
---

# 遷移至遠端後端儲存空間

於 2.15 版引入
{: .label .label-purple }

遠端後端儲存空間提供一種防止資料遺失的新方法：自動為所有索引交易建立備份，並將其傳送至遠端儲存空間。若要使用此功能，必須啟用[分段複寫]({{site.url}}{{site.baseurl}}/opensearch/segment-replication/)。

您可以透過滾動升級機制，將以文件複寫為基礎的叢集遷移至遠端後端儲存空間。

滾動升級有時也稱為*節點替換升級*，可在執行中的叢集上進行。節點會逐一停止並就地遷移。或者，也可以一次一個地停止節點，並以遠端後端主機取代。在此過程中，您可以繼續在叢集中將資料編製索引及查詢資料。

當叢集同時包含遠端後端節點與非遠端節點時，OpenSearch 會限制各個分片可配置的位置。只有在副本的主要分片位於遠端後端節點上時，該副本才能配置到遠端後端節點；而儲存在遠端後端索引中的分片只能配置到遠端後端節點。因此，在遷移期間，部分副本分片會維持未指派狀態，且部分分片可能只剩一份作用中的分片。為了讓每個分片都保持可用，請在停止每個節點之前，先將分片移出該節點。

## 準備遷移

在對 OpenSearch 叢集進行任何變更之前，請先檢閱[升級 OpenSearch]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/index/)，以了解有關備份組態檔以及建立叢集狀態與索引快照的建議。

在遷移至遠端後端儲存空間之前，請先升級至 OpenSearch 2.15 或更新版本。

在升級至 OpenSearch 2.15 之前，請先建立叢集快照並將其儲存在遠端。OpenSearch 2.15 節點無法還原為文件複寫。如果需要復原遷移，請執行全新的 OpenSearch 安裝，並從遠端快照還原。將快照儲存在遠端，可在遷移過程中發生問題時供您擷取並還原。
{: .important}

## 執行升級

1. 開始之前，請先使用 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) 確認 OpenSearch 叢集的健康狀態。請在升級前解決所有索引或分片配置問題，以確保您的資料得以保留。狀態為 **green** 表示所有主要分片和副本分片都已配置。您可以使用類似下列的命令查詢 `_cluster/health` API 端點：

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

1. 將 `cluster.remote_store.compatibility_mode` 設定設為 `mixed`，以允許遠端後端儲存空間節點加入叢集：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.remote_store.compatibility_mode": "mixed"
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
           "compatibility_mode" : "mixed"
         }
       }
     },
     "transient" : { }
   }
   ```

1. 檢查您的叢集，並找出第一個要遷移的節點。

1. 將該節點排除在分片配置之外，讓 OpenSearch 將其分片移至其他節點。請將 `<node-name>` 替換為節點名稱：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.routing.allocation.exclude._name": "<node-name>"
       }
   }
   ```

1. 等待分片重新配置完成：

   ```json
   GET "/_cluster/health?wait_for_no_relocating_shards=true&wait_for_no_initializing_shards=true&pretty"
   ```

   確認回應中包含 `"timed_out" : false`。如果回應中包含 `"timed_out" : true`，表示分片仍在重新配置中。請重複傳送請求，直到重新配置完成為止。

1. 列出叢集中的分片，並檢查仍留在該節點上的分片：

   ```json
   GET "/_cat/shards?v&h=index,shard,prirep,state,node&s=index,shard"
   ```

   有些分片可能會留在該節點上，因為沒有其他節點符合存放這些分片的條件。例如，當副本的主要分片位於非遠端節點上，且其他每個非遠端節點都已持有該分片的一份時，該副本就會留在此節點上。停止節點之前，請確認留在該節點上的每個分片，在另一個節點上都有狀態為 `STARTED` 的另一份。若停止持有某分片唯一一份的節點，該分片將無法使用，直到該節點重新加入叢集為止。若要了解分片無法移動的原因，請使用 [Cluster Allocation Explain API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-allocation/)。

1. 停用分片複寫，以避免在節點離線期間建立分片副本：

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

1. 對叢集執行下列排清作業，將交易記錄檔項目提交至 Lucene 索引：

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

1. 在 `opensearch.yml` 中以節點屬性的形式提供遠端後端儲存空間儲存庫的詳細資訊，如下列範例所示：

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

1. 停止您要遷移的節點。刪除容器時，請勿刪除與該容器相關聯的磁碟區。新的 OpenSearch 容器將使用現有的磁碟區。**刪除磁碟區將導致資料遺失**。

1. 部署一個新容器，其執行相同版本的 OpenSearch，並對應至您所刪除容器的同一個磁碟區。

1. OpenSearch 在新節點上執行後，查詢 `_cat/nodes` 端點以確認該節點已加入叢集：

   ```json
   GET "/_cat/nodes?v&h=name,node.role,master"
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

1. 等待分片復原完成：

   ```json
   GET "/_cluster/health?wait_for_no_initializing_shards=true&wait_for_no_relocating_shards=true&pretty"
   ```

   確認回應中包含 `"timed_out" : false`。如果回應中包含 `"timed_out" : true`，請重複傳送請求，直到復原完成為止。在所有節點遷移完成之前，叢集狀態可能會維持 yellow，因為遷移期間無法配置的副本會維持未指派狀態。

1. 第一個節點以遠端後端節點身分加入叢集後，將 `cluster.migration.direction` 設為 `remote_store`。此設定會將新索引配置到遠端後端資料節點，並允許主要分片從非遠端節點重新配置到遠端後端節點。請務必在遠端後端節點已加入叢集後，才設定此設定。如果沒有可用的遠端後端節點，新索引的主要分片將無法配置，且叢集狀態會變成 red：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.migration.direction": "remote_store"
       }
   }
   ```

   您應該會收到類似下列的回應：

   ```json
   {
     "acknowledged" : true,
     "persistent" : {
       "cluster" : {
         "migration" : {
           "direction" : "remote_store"
         }
       }
     },
     "transient" : { }
   }
   ```

1. 針對叢集中其餘的每個節點重複步驟 4 至 14。在步驟 4 中，請指定下一個節點的名稱。對於最後一個非遠端節點，OpenSearch 會將其所有分片移至遠端後端節點，因此當您停止該節點時，它不會存放任何分片。

1. 移除節點排除設定：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.routing.allocation.exclude._name": null
       }
   }
   ```

1. 使用 Cluster Health API 確認叢集處於健康狀態，如下列命令所示：

   ```json
   GET "/_cluster/health?wait_for_status=green&pretty"
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

1. 使用下列命令清除 `remote_store.compatibility_mode` 和 `migration.direction` 設定，使非遠端節點無法加入叢集：

   ```json
   PUT "/_cluster/settings?pretty"
   {
       "persistent": {
           "cluster.remote_store.compatibility_mode": null,
           "cluster.migration.direction": null
       }
   }
   ```

   您應該會收到類似下列的回應：

   ```json
   {
     "acknowledged" : true,
     "persistent" : { },
     "transient" : { }
   }
   ```

遷移至遠端後端儲存空間的作業現已完成。

## 相關叢集設定

使用下列叢集設定，以啟用遷移至遠端後端叢集的功能。

| 欄位                                     | 資料類型 | 說明 |
|:------------------------------------------|:--- |:---|
| `cluster.remote_store.compatibility_mode` | 字串  | 設定為 `strict` 時，會依初始叢集類型，只允許建立非遠端節點或遠端節點其中一種。設定為 `mixed` 時，允許遠端節點與非遠端節點同時加入叢集。預設值為 `strict`。 |  
| `cluster.migration.direction`             | 字串 |  設定為 `remote_store` 時，只會在遠端後端儲存空間節點上建立新分片，並允許主要分片從非遠端節點重新配置至遠端後端節點。預設值為 `None`。 |                                                                                                                                                                                            

