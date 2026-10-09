---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
parent: Improving search performance
title: "搜尋分片路由"
nav_order: 30
---

# 搜尋分片路由

為了確保備援並提升搜尋效能，OpenSearch 會將索引資料分散到多個主要分片，而每個主要分片會有一或多個副本分片。執行搜尋查詢時，OpenSearch 會將請求路由到包含主要或副本索引分片的節點。這項技術稱為_搜尋分片路由_。


## 調適性副本選擇

為了改善延遲，搜尋請求會使用_調適性副本選擇_來路由，其會根據下列因素選擇節點：

- 特定節點執行先前請求所花費的時間量。
- 協調節點與所選節點之間的延遲。
- 節點搜尋執行緒集區的佇列大小。

如果您有權限呼叫 OpenSearch REST API，則可以關閉搜尋分片路由。如需 REST API 使用者存取權的詳細資訊，請參閱 [REST 管理 API 設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/#rest-management-api-settings)。若要停用搜尋分片路由，請更新叢集設定，如下所示：

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.use_adaptive_replica_selection": false
  }
}
```
{% include copy-curl.html %}

如果您關閉搜尋分片路由，OpenSearch 將使用輪詢路由，這可能會對搜尋延遲造成負面影響。
{: .note}

## 搜尋期間的節點與分片選擇

OpenSearch 會使用所有節點來為搜尋請求選擇最佳路由。不過，在某些情況下，您可能會想手動選擇搜尋請求要傳送到的節點或分片，包括下列情況：

- 使用先前搜尋的快取。
- 將特定硬體專門用於搜尋。
- 僅使用本機節點進行搜尋。

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

5. `_only_nodes:<node-id>,<node-id>`：根據節點 ID 將搜尋限制為僅在特定節點上執行。

    ```json
    GET /my-index/_search?preference=_only_nodes:node-1,node-2
    ```
    {% include copy-curl.html %}

6. `_prefer_nodes:<node-id>,<node-id>`：偏好於特定節點上執行搜尋，但若偏好的節點無法使用，則會使用其他節點。

    ```json
    GET /my-index/_search?preference=_prefer_nodes:node-1,node-2
    ```
    {% include copy-curl.html %}

7. `_shards:<shard-id>,<shard-id>`：將搜尋限制為特定分片。

    ```json
    GET /my-index/_search?preference=_shards:0,1
    ```
    {% include copy-curl.html %}

8. `_local`：若可能，會在本機節點上執行搜尋，這可降低延遲。

    ```json
    GET /my-index/_search?preference=_local
    ```
    {% include copy-curl.html %}

9. 自訂字串：您可以使用任何自訂字串作為偏好值。此自訂字串可確保包含相同字串的請求會一致地路由到相同的分片，這對快取很有用。

    ```json
    GET /my-index/_search?preference=custom_string
    ```
    {% include copy-curl.html %}

## 索引與搜尋期間的自訂路由

您可以在編製索引與搜尋作業期間指定路由。

### 編製索引期間的路由
當您將文件編製索引時，OpenSearch 會計算路由值的雜湊，並使用此雜湊來判斷文件將儲存在哪個分片上。如果您未指定路由值，OpenSearch 會使用文件 ID 來計算雜湊。

以下是帶有路由值的索引作業範例：

```json
POST /index1/_doc/1?routing=user1
{
  "name": "John Doe",
  "age": 20
}
```
{% include copy-curl.html %}

在此範例中，ID 為 `1` 的文件會以路由值 `user1` 編製索引。所有具有相同路由值的文件都會儲存在相同的分片上。

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

### 限制可並行查詢的分片數量

您可以在搜尋請求中使用 `max_concurrent_shard_requests` 參數來限制可並行查詢的分片數量。例如，下列請求會將並行分片請求數限制為 `12`：

```json
GET /index1/_search?max_concurrent_shard_requests=12
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}


### 定義搜尋分片數限制

您可以在 `opensearch.yml` 檔案中，或使用 REST API 來定義動態的 `action.search.shard_count.limit` 設定。任何超過此限制的搜尋請求都會遭到拒絕並擲回錯誤。這有助於防止單一搜尋請求耗用過多資源，以免降低整個叢集的效能。下列範例請求會使用 API 更新此叢集設定：

```json
PUT /_cluster/settings
{
  "transient": {
    "action.search.shard_count.limit": 1000
  }
}
```
{% include copy-curl.html %}

### 搜尋執行緒集區

OpenSearch 會使用執行緒集區來管理各種工作的執行，包括搜尋作業。搜尋執行緒集區專門用於搜尋請求。您可以將下列設定新增至 `opensearch.yml`，以調整搜尋執行緒集區的大小與佇列容量：
```
thread_pool.search.size: 100
thread_pool.search.queue_size: 1000
```
此設定為靜態。如需如何設定動態與靜態設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

#### 執行緒集區狀態

下列三種狀態說明執行緒集區的運作：

 - _執行緒指派_：如果搜尋執行緒集區中有可用的執行緒，則請求會立即指派給執行緒並開始處理。

 - _佇列_：如果搜尋執行緒集區中的所有執行緒都在忙碌中，則請求會放入佇列。

 - _拒絕_：如果佇列已滿 (例如，已排入佇列的請求數達到佇列大小限制)，則其他傳入的搜尋請求會遭到拒絕，直到佇列中有可用空間為止。

您可以執行下列請求來檢查搜尋執行緒集區的目前組態：

```json
GET /_cat/thread_pool/search?v&h=id,name,active,rejected,completed,size,queue_size
```
{% include copy-curl.html %}
