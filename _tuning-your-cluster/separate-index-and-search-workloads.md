---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分離索引與搜尋工作負載"
nav_order: 42
has_children: false
redirect_from: 
   - /tuning-your-cluster/seperate-index-and-search-workloads/
---

# 分離索引與搜尋工作負載

在啟用遠端儲存且索引已啟用分段複寫的叢集中，您可以使用專門的 `search` 節點角色，並在索引中佈建對應的搜尋副本，將索引編製與搜尋工作負載分散到不同的硬體上。

OpenSearch 使用兩種類型的副本：

- **寫入副本**：做為主要分片的備援複本。如果主要分片失敗（例如因為節點離線或硬體問題），寫入副本可以提升為新的主要分片，以確保寫入作業的高可用性。
- **搜尋副本**：專門處理搜尋查詢。搜尋副本無法提升為主要分片。

## 分離工作負載的優點

分離索引與搜尋工作負載可提供下列優點：

1. **平行且隔離的處理**：平行處理索引編製與搜尋工作負載，並將兩者彼此隔離，以提升整體系統輸送量並確保可預測的效能。
2. **獨立擴充**：透過新增更多資料節點（用於寫入副本）或搜尋節點（用於搜尋副本），獨立擴充索引編製與搜尋。
3. **容錯能力**：避免索引編製或搜尋的失敗互相影響，以提升整體系統可用性。
4. **成本效益與效能**：使用專門的硬體（例如用於索引編製的運算最佳化執行個體，以及用於搜尋的記憶體最佳化執行個體）來降低成本並提升效能。
5. **調校彈性**：分別針對索引編製與搜尋工作負載最佳化效能設定，例如緩衝區與快取。

## 設定工作負載分離

若要分離索引編製與搜尋工作負載，您需要設定搜尋節點、啟用遠端儲存，並將搜尋副本新增至索引。請依照下列步驟在叢集中設定工作負載分離。

### 步驟 1：設定搜尋節點

在分離工作負載之前，您需要指定特定節點來處理搜尋作業。搜尋節點專門用來處理搜尋請求，可協助最佳化叢集的搜尋效能。

下列請求會在 `opensearch.yml` 中將節點設定為僅處理搜尋工作負載：

```yaml
node.name: searcher-node1
node.roles: [ search ]
```

### 步驟 2：啟用遠端儲存

遠端儲存為您的索引資料提供集中式儲存位置。此組態對分段複寫至關重要，可確保所有節點都能存取相同的資料，無論其角色為何。遠端儲存在您想要將儲存空間與運算資源分離的雲端環境中特別實用。

下列請求會在 `opensearch.yml` 中設定遠端儲存（例如 Amazon Simple Storage Service [Amazon S3]）的儲存庫組態：

```yaml
node.attr.remote_store.segment.repository: "my-repository"
node.attr.remote_store.translog.repository: "my-repository"
node.attr.remote_store.state.repository: "my-repository"
node.attr.remote_store.repository.my-repository.type: s3
node.attr.remote_store.repository.my-repository.settings.bucket: <Bucket Name 1>
node.attr.remote_store.repository.my-repository.settings.base_path: <Bucket Base Path 1>
node.attr.remote_store.repository.my-repository.settings.region: <Region>
```

如需更多資訊，請參閱[遠端後端儲存]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)。

分離索引與搜尋工作負載時，請在初始設定期間將 `cluster.remote_store.state.enabled` 設為 `true`。此設定可確保 OpenSearch 將索引中繼資料儲存在遠端儲存中，讓搜尋副本能在[僅搜尋模式](#turn-off-write-workloads-with-search-only-mode)下順暢復原。如需更多資訊，請參閱[搜尋副本復原情境](#search-replica-recovery-scenarios)。
{: .note}


### 步驟 3：將搜尋副本新增至索引

設定節點與遠端儲存之後，您需要為索引設定搜尋副本。搜尋副本是索引的複本，專門用來處理搜尋請求，讓您能獨立於索引編製容量來擴充搜尋容量。

根據預設，在啟用遠端儲存的叢集中建立的索引會使用分段複寫。如需更多資訊，請參閱[分段複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/index/)。

您可以使用 `number_of_search_replicas` 設定（預設為 0），以下列其中一種方式為索引新增搜尋副本。

#### 選項 1：建立含搜尋副本的索引

當您要建立新索引，並想在一開始就設定搜尋副本時，請使用此選項。如果您想在將資料編製索引之前先規劃工作負載分離策略，此做法最理想。

下列請求會建立一個含一個主要分片、一個副本及兩個搜尋副本的索引：

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

#### 選項 2：更新現有索引的搜尋副本計數

當您已有現有索引，並想新增或修改搜尋副本時，請使用此選項。當您需要根據不斷變化的工作負載需求調整搜尋容量時，這很實用。

下列請求會更新搜尋副本計數：

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

當您要從快照還原索引，並想在還原過程中設定搜尋副本時，請使用此選項。這在災難復原情境或叢集之間遷移索引時特別實用。

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

設定基本的工作負載分離之後，您可以微調組態以最佳化效能與資源使用率。下列設定可讓您根據特定需求控制搜尋路由、自動擴充副本，以及管理寫入工作負載。

### 強制執行叢集層級的搜尋請求路由

啟用搜尋副本時，根據預設，所有搜尋流量都會路由至搜尋副本。下列請求會強制執行或放寬此路由行為：

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
- `false`：如有需要，允許退回至主要分片/寫入副本。

### 自動擴充搜尋副本

使用 `auto_expand_search_replicas` 索引設定，根據叢集中可用的搜尋節點數自動擴充搜尋副本。如需更多資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。

### 使用僅搜尋模式關閉寫入工作負載

當您不需要寫入索引時，可以使用 `_scale` API 關閉索引的主要分片與寫入副本。此做法很適合寫入一次、讀取多次的情境，例如記錄檔分析，您只需保持搜尋副本作用中，即可降低資源使用量。

下列請求會停用寫入副本，以開啟僅搜尋模式：

```json
POST my_index/_scale 
{
   "search_only": true
}
```
{% include copy-curl.html %}

下列請求會啟用寫入副本，以關閉僅搜尋模式：

```json
POST my_index/_scale 
{
   "search_only": false
}
```
{% include copy-curl.html %}

#### 搜尋副本復原情境

OpenSearch 會依組態不同，以不同方式處理僅搜尋模式下搜尋副本的復原。

##### 情境 1：持續性資料目錄且停用遠端儲存狀態

當您使用持續性資料目錄並將 `cluster.remote_store.state.enabled` 設為 `false` 時，搜尋副本會在節點重新啟動後自動復原。

##### 情境 2：啟用遠端儲存狀態但沒有持續性資料目錄

當 `cluster.remote_store.state.enabled` 設為 `true` 且沒有持續性資料目錄時，OpenSearch 會復原搜尋副本，而不需要主要分片或寫入副本。因為已啟用遠端儲存狀態，OpenSearch 會在重新啟動後保留索引中繼資料。配置邏輯會略過搜尋副本的作用中主要分片檢查，允許配置搜尋副本，讓搜尋查詢保持正常運作。

##### 情境 3：啟用遠端儲存狀態且有持續性資料目錄

此組態可提供順暢的復原。在僅搜尋模式下，同時具備持續性資料目錄且 `cluster.remote_store.state.enabled` 設為 `true` 時，OpenSearch 只會啟動搜尋副本（排除主要分片與寫入副本），確保索引在重新啟動後仍可查詢。

##### 情境 4：沒有持續性資料目錄且停用遠端儲存狀態

當持續性資料目錄不存在且 `cluster.remote_store.state.enabled` 設為 `false` 時，所有本機狀態都會在重新啟動時遺失。OpenSearch 沒有中繼資料參考，因此索引會變成無法復原。

