---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
parent: Improving search performance
title: "搜尋分片路由"
nav_order: 30
---

# 搜尋分片路由

為了確保備援並提升搜尋效能，OpenSearch 會將索引資料分散到多個主要分片，而每個主要分片會有一或多個副本分片。執行搜尋查詢時，OpenSearch 會將請求路由到包含主要或副本索引分片的節點。這項技術稱為_搜尋分片路由_。


## 調適型副本選擇

為了縮短延遲，搜尋請求會使用 _調適型副本選擇_ 進行路由，此機制會根據下列因素選擇節點：

- 特定節點執行先前請求所花費的時間。
- 協調節點與所選節點之間的延遲。
- 節點搜尋執行緒集區的佇列大小。

OpenSearch 僅對未指定 [`preference`](#node-and-shard-selection-during-searches) 值的搜尋使用調適型副本選擇。如果已設定加權分片路由，或已設定分片配置感知屬性且 `cluster.search.ignore_awareness_attributes` 設定為 `false`，也不會使用調適型副本選擇。在這些情況下，OpenSearch 會根據路由權重或感知屬性對搜尋進行路由。如需詳細資訊，請參閱[叢集層級搜尋設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-search-settings)。

如果您具有呼叫 OpenSearch REST API 的權限，就可以關閉搜尋分片路由。如需 REST API 使用者存取權的詳細資訊，請參閱 [REST 管理 API 設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/#rest-management-api-settings)。若要停用搜尋分片路由，請依照下列方式更新叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.use_adaptive_replica_selection": false
  }
}
```
{% include copy-curl.html %}

如果您關閉搜尋分片路由，OpenSearch 將使用循環路由，這可能會對搜尋延遲造成負面影響。
{: .note}

## 搜尋期間的節點與分片選擇

OpenSearch 會使用所有節點，為搜尋請求選擇最佳的路由。不過，在某些情況下，您可能會想手動選擇搜尋請求要傳送至哪些節點或分片，包括下列情況：

- 使用先前搜尋的快取。
- 將特定硬體專門用於搜尋。
- 僅使用本機節點進行搜尋。

將搜尋路由至特定分片副本可能會造成熱點，因為搜尋負載不再平均分散於整個叢集。只有在效益（例如更妥善地使用快取）大於此成本時，才使用 `preference` 參數。

您可以在搜尋查詢中使用 `preference` 參數來指出搜尋目的地。以下是可用選項的完整清單：

1. `_primary`：強制搜尋僅在主要分片上執行。

    ```json
    GET /my-index/_search?preference=_primary
    ```
    {% include copy-curl.html %}

2. `_primary_first`：偏好主要分片，但若主要分片無法使用，則會使用副本分片。

    ```json
    GET /my-index/_search?preference=_primary_first
    ```
    {% include copy-curl.html %}

3. `_replica`：強制搜尋僅在副本分片上執行。

    ```json
    GET /my-index/_search?preference=_replica
    ```
    {% include copy-curl.html %}

4. `_replica_first`：偏好副本分片，但若沒有可用的副本分片，則會使用主要分片。

    ```json
    GET /my-index/_search?preference=_replica_first
    ```
    {% include copy-curl.html %}

5. `_only_nodes:<node-id>,<node-id>`：將搜尋限制為僅在特定節點上執行。您可以使用任何 [節點規格]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters) 來指定節點，例如節點 ID、節點名稱、`data-node-*` 之類的萬用字元模式，或 `zone:us-east-1a` 之類的節點屬性。若指定的節點中沒有任何一個含有分片副本，搜尋就會失敗。

    ```json
    GET /my-index/_search?preference=_only_nodes:node-1,node-2
    ```
    {% include copy-curl.html %}

6. `_prefer_nodes:<node-id>,<node-id>`：偏好於特定節點上執行搜尋，但若偏好的節點無法使用，則會使用其他節點。

    ```json
    GET /my-index/_search?preference=_prefer_nodes:node-1,node-2
    ```
    {% include copy-curl.html %}

7. `_shards:<shard-id>,<shard-id>`：將搜尋限制為特定分片。您可以將 `_shards` 與另一個偏好值結合，並以管道字元（`|`）分隔，例如 `_shards:0,1|_local`。`_shards` 值必須放在最前面。

    ```json
    GET /my-index/_search?preference=_shards:0,1
    ```
    {% include copy-curl.html %}

8. `_local`：若可能，在本機節點上執行搜尋，這可以降低延遲。

    ```json
    GET /my-index/_search?preference=_local
    ```
    {% include copy-curl.html %}

9. `_only_local`：僅在配置給本機節點的分片副本上執行搜尋。

    ```json
    GET /my-index/_search?preference=_only_local
    ```
    {% include copy-curl.html %}

10. `_search_replica`：僅在 [搜尋副本]({{site.url}}{{site.baseurl}}/tuning-your-cluster/separate-index-and-search-workloads/) 上執行搜尋，這些副本託管於具有 `search` 角色的節點上。若索引沒有搜尋副本，搜尋就會失敗。

    ```json
    GET /my-index/_search?preference=_search_replica
    ```
    {% include copy-curl.html %}

11. 自訂字串：您可以使用任何自訂字串作為偏好值。OpenSearch 會將包含相同字串的請求路由至相同的分片副本，這對快取很有用。該字串不得以底線（`_`）開頭。工作階段 ID 或使用者名稱是不錯的選擇，如此一來每位使用者的搜尋都會使用相同的分片副本。只有在叢集狀態不變時，路由才會保持一致：若分片被重新配置或節點故障，相同的字串可能會被路由至不同的分片副本。

    ```json
    GET /my-index/_search?preference=custom_string
    ```
    {% include copy-curl.html %}

`_only_local` 值可保證搜尋僅使用本機節點上的分片副本，因此適合用來對特定節點進行疑難排解。其他 `preference` 值則無法完全保證由哪些分片副本提供搜尋。由於分片副本可能處於不同的重新整理狀態，若搜尋由不同的副本提供，對正在更新的索引重複執行搜尋可能會傳回不同的結果。
{: .note}

## 索引與搜尋期間的自訂路由

您可以在編製索引與搜尋作業期間指定路由。

### 編製索引期間的路由

當您將文件編製索引時，OpenSearch 會計算路由值的雜湊值，並使用此雜湊值決定文件要儲存在哪個分片上。如果您未指定路由值，OpenSearch 會使用文件 ID 來計算雜湊值。

以下是指定路由值的索引操作範例：

```json
POST /index1/_doc/1?routing=user1
{
  "name": "John Doe",
  "age": 20
}
```
{% include copy-curl.html %}

在此範例中，ID 為 `1` 的文件以路由值 `user1` 編製索引。所有具有相同路由值的文件都會儲存在同一個分片上。

### 搜尋期間的路由

當您搜尋文件時，指定相同的路由值可確保搜尋請求會路由到適當的分片。這可透過減少需要查詢的分片數量來大幅提升效能。

以下範例請求會以特定路由值進行搜尋：

```json
GET /index1/_search?routing=user1
{
  "query": {
    "match": {
      "name": "John Doe"
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，搜尋查詢會路由到包含以路由值 `user1` 編製索引之文件的分片。

使用自訂路由時必須謹慎，以避免熱點與資料偏斜：

 - 當數量不成比例的文件被路由到單一分片時，就會發生_熱點_。這可能會導致該分片成為瓶頸，因為相較於其他分片，它必須處理更多的讀取與寫入作業。因此，此分片可能會經歷更高的 CPU、記憶體與 I/O 使用量，導致效能降低。

 - _資料偏斜_是指資料在各分片之間分布不均。如果路由值未平均分布，某些分片最終可能會儲存比其他分片多得多的資料。這可能會導致儲存空間使用量不平衡，其中某些節點的磁碟使用率遠高於其他節點。

## 並行分片請求

搜尋期間同時命中大量分片可能會大幅影響 CPU 與記憶體耗用量。根據預設，OpenSearch 不會拒絕這些請求。不過，您可以使用多種方法來降低此風險。下列各節將說明這些方法。

### 限制可同時查詢的分片數量

您可以在搜尋請求中使用 `max_concurrent_shard_requests` 參數，限制可同時查詢的分片數量。例如，下列請求將並行分片請求數限制為 `12`：

```json
GET /index1/_search?max_concurrent_shard_requests=12
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}


### 定義搜尋分片數量上限

您可以在 `opensearch.yml` 檔案中定義動態 `action.search.shard_count.limit` 設定，或使用 REST API 進行定義。任何超過此上限的搜尋請求都會遭到拒絕並擲回錯誤。這有助於防止單一搜尋請求耗用過多資源，進而導致整個叢集的效能降低。以下範例請求使用 API 更新此叢集設定：

```json
PUT /_cluster/settings
{
  "transient": {
    "action.search.shard_count.limit": 1000
  }
}
```
{% include copy-curl.html %}

### 設定搜尋執行緒集區

OpenSearch 使用執行緒集區來管理各種任務的執行，包括搜尋作業。搜尋執行緒集區專門用於處理搜尋請求。您可以透過在 `opensearch.yml` 中加入以下設定，來調整搜尋執行緒集區的大小與佇列容量：

```yaml
thread_pool.search.size: 100
thread_pool.search.queue_size: 1000
```

此設定為靜態設定。如需動態與靜態設定的組態方式詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

#### 執行緒集區狀態

下列三種狀態說明執行緒集區的運作：

 - _執行緒指派_：如果搜尋執行緒集區中有可用的執行緒，請求會立即被指派給一個執行緒並開始處理。

 - _排隊_：如果搜尋執行緒集區中的所有執行緒都在忙碌中，請求會被放入佇列。

 - _拒絕_：如果佇列已滿（例如，排隊的請求數達到佇列大小上限），後續進來的搜尋請求會被拒絕，直到佇列中有可用空間為止。

您可以執行下列請求來查看搜尋執行緒集區目前的組態：

```json
GET /_cat/thread_pool/search?v&h=id,name,active,rejected,completed,size,queue_size
```
{% include copy-curl.html %}
