---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分離索引與搜尋工作負載"
nav_order: 20
parent: Performance tuning
has_children: false
redirect_from: 
   - /tuning-your-cluster/seperate-index-and-search-workloads/
   - /tuning-your-cluster/separate-index-and-search-workloads/
---

# 分離索引與搜尋工作負載

在啟用遠端儲存空間的叢集中，若索引啟用了分段複製，您可以使用專用的 `search` 節點角色，並在索引中佈建對應的搜尋副本，將索引與搜尋工作負載分配到不同的硬體上。

OpenSearch 使用兩種類型的副本：

- **寫入副本**：作為主要分片的備援複本。如果主要分片失敗（例如因節點掉線或硬體問題），寫入副本可以升級為新的主要分片，以確保寫入作業的高可用性。
- **搜尋副本**：專門處理搜尋查詢。搜尋副本無法升級為主要分片。

## 分離工作負載的優點

分離索引與搜尋工作負載可提供下列優點：

1. **平行且隔離的處理**：平行處理索引與搜尋工作負載，並將兩者彼此隔離，以提升整體系統輸送量並確保效能可預測。
2. **獨立擴展**：透過新增更多資料節點（用於寫入副本）或搜尋節點（用於搜尋副本），獨立擴展索引與搜尋的規模。
3. **故障韌性**：防止索引或搜尋的故障互相影響，以提升整體系統可用性。
4. **成本效益與效能**：使用專用硬體（例如索引使用運算最佳化執行個體、搜尋使用記憶體最佳化執行個體），以降低成本並提升效能。
5. **調校彈性**：針對索引與搜尋工作負載，分別最佳化緩衝區與快取等效能設定。

## 設定工作負載分離

若要分離索引與搜尋工作負載，您需要設定搜尋節點、啟用遠端儲存空間，並為索引新增搜尋副本。請依照下列步驟在叢集中設定工作負載分離。

### 步驟 1：設定搜尋節點

在分離工作負載之前，您需要指定特定節點來處理搜尋作業。搜尋節點專門用於服務搜尋請求，有助於最佳化叢集的搜尋效能。

下列請求會在 `opensearch.yml` 中將節點設定為僅處理搜尋工作負載：

```yaml
node.name: searcher-node1
node.roles: [ search ]
```

### 步驟 2：啟用遠端儲存空間

遠端儲存空間為索引資料提供集中式的儲存位置。此組態對分段複製至關重要，可確保所有節點無論其角色為何，都能存取相同的資料。遠端儲存空間在雲端環境中特別有用，因為您可能希望將儲存空間與運算資源分離。

下列請求會在 `opensearch.yml` 中設定遠端儲存空間的儲存庫組態（例如 Amazon Simple Storage Service [Amazon S3]）：

```yaml
node.attr.remote_store.segment.repository: "my-repository"
node.attr.remote_store.translog.repository: "my-repository"
node.attr.remote_store.state.repository: "my-repository"
node.attr.remote_store.repository.my-repository.type: s3
node.attr.remote_store.repository.my-repository.settings.bucket: <Bucket Name 1>
node.attr.remote_store.repository.my-repository.settings.base_path: <Bucket Base Path 1>
node.attr.remote_store.repository.my-repository.settings.region: <Region>
```

如需更多資訊，請參閱 [Remote-backed storage]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)。

分離索引與搜尋工作負載時，請在初始設定期間將 `cluster.remote_store.state.enabled` 設為 `true`。此設定可確保 OpenSearch 將索引中繼資料儲存在遠端儲存空間中，讓搜尋副本能在[僅搜尋模式](#turn-off-write-workloads-with-search-only-mode)下順利復原。如需更多資訊，請參閱[搜尋副本復原情境](#search-replica-recovery-scenarios)。
{: .note}


### 步驟 3：為索引新增搜尋副本

設定好節點與遠端儲存空間後，您需要為索引設定搜尋副本。搜尋副本是專門處理搜尋請求的索引複本，讓您可以獨立於索引容量之外擴展搜尋容量。

預設情況下，在啟用遠端儲存空間的叢集中建立的索引會使用分段複製。如需更多資訊，請參閱 [Segment replication]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/index/)。

您可以使用 `number_of_search_replicas` 設定（預設值為 0），以下列其中一種方式為索引新增搜尋副本。

#### 選項 1：建立含搜尋副本的索引

當您要建立新索引，並希望在流程一開始就設定搜尋副本時，請使用此選項。這種方式適合在編製索引資料之前規劃工作負載分離策略。

下列請求會建立一個含有一個主要分片、一個副本和兩個搜尋副本的索引：

```json
PUT /my-index
{
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "number_of_search_replicas": 2,
        }
  }
}
```
{% include copy-curl.html %}

#### 選項 2：更新現有索引的搜尋副本數量

當您已有現有索引，並想新增或修改搜尋副本時，請使用此選項。當您需要根據不斷變化的工作負載需求調整搜尋容量時，這個方式非常實用。

下列請求會更新搜尋副本數量：

```json
PUT /my-index/_settings
{
  "settings": {
    "index": {
      "number_of_search_replicas": 1
    }
  }
}
```
{% include copy-curl.html %}

#### 選項 3：從快照還原含搜尋副本的索引

當您要從快照還原索引，並希望在還原過程中設定搜尋副本時，請使用此選項。這對災難復原情境或在叢集之間遷移索引時特別有用。

下列請求會從快照還原含搜尋副本的索引：

```json
POST /_snapshot/my-repository/my-snapshot/_restore
{ 
    "indices": "my-index", 
    "index_settings": { 
        "index.number_of_search_replicas": 2,
        "index.replication.type": "SEGMENT"
     } 
}'
```
{% include copy-curl.html %}

## 其他組態

設定好基本的工作負載分離後，您可以微調組態，以最佳化效能與資源使用率。下列設定可讓您控制搜尋路由、自動擴展副本，並根據特定需求管理寫入工作負載。

### 強制叢集層級的搜尋請求路由

啟用搜尋副本後，預設情況下所有搜尋流量都會路由至搜尋副本。下列請求可強制或放寬此路由行為：

```json
PUT /_cluster/settings
{ 
    "persistent": {
        "cluster.routing.search_replica.strict": "true"
    }
}
```
{% include copy-curl.html %}

`cluster.routing.search_replica.strict` 設定支援下列選項：

- `true`（預設）：僅路由至搜尋副本。
- `false`：必要時允許回退至主要分片／寫入副本。

### 自動擴展搜尋副本

使用 `auto_expand_search_replicas` 索引設定，可根據叢集中可用的搜尋節點數量自動擴展搜尋副本。如需更多資訊，請參閱 [Index settings]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。

### 使用僅搜尋模式關閉寫入工作負載

當您不需要寫入索引時，可以使用 `_scale` API 關閉該索引的主要分片與寫入副本。這種方式非常適合寫入一次、讀取多次的情境，例如記錄分析，您可以只保留搜尋副本運作，以降低資源使用量。

下列請求會透過停用寫入副本來開啟僅搜尋模式：

```json
POST my_index/_scale 
{
   "search_only": true
}
```
{% include copy-curl.html %}

下列請求會透過啟用寫入副本來關閉僅搜尋模式：

```json
POST my_index/_scale 
{
   "search_only": false
}
```
{% include copy-curl.html %}

#### 搜尋副本復原情境

OpenSearch 會根據組態，以不同方式處理僅搜尋模式下搜尋副本的復原。

##### 情境 1：使用持續性資料目錄且停用遠端儲存空間狀態

當您使用持續性資料目錄並將 `cluster.remote_store.state.enabled` 設為 `false` 時，搜尋副本會在節點重新啟動後自動復原。

##### 情境 2：啟用遠端儲存空間狀態但沒有持續性資料目錄

當 `cluster.remote_store.state.enabled` 設為 `true` 且沒有持續性資料目錄時，OpenSearch 會在不需要主要分片或寫入副本的情況下復原搜尋副本。由於已啟用遠端儲存空間狀態，OpenSearch 會在重新啟動後保留索引中繼資料。配置邏輯會跳過搜尋副本的作用中主要分片檢查，讓搜尋副本得以配置，使搜尋查詢持續運作。

##### 情境 3：啟用遠端儲存空間狀態且使用持續性資料目錄

此組態可提供順暢的復原。在僅搜尋模式下，同時具備持續性資料目錄並將 `cluster.remote_store.state.enabled` 設為 `true` 時，OpenSearch 只會啟動搜尋副本（排除主要分片與寫入副本），確保索引在重新啟動後仍可查詢。

##### 情境 4：沒有持續性資料目錄且停用遠端儲存空間狀態

當持續性資料目錄不存在且 `cluster.remote_store.state.enabled` 設為 `false` 時，所有本機狀態都會在重新啟動時遺失。OpenSearch 沒有中繼資料參考，因此索引將無法復原。

