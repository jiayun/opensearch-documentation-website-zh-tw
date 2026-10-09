---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分層快取"
parent: Caching
grand_parent: Improving search performance
nav_order: 10
---

# 分層快取

分層快取是一種多層級快取，其中每一層都有各自的特性與效能等級。透過組合不同的層級，您可以在快取效能與大小之間取得平衡。

## 分層快取的類型

OpenSearch 提供一種分層溢出快取的實作，稱為 `tiered_spillover`，其實作儲存在 `cache-common` 模組中。它有兩層：上層與下層。雖然每一層都可以使用任何可插拔的快取實作，但通常上層會是較小且較快的堆上層，例如 `opensearch_onheap`，而下層則是較大且較慢的磁碟層，例如 `ehcache_disk`。此下層可以透過設定 `indices.requests.cache.tiered_spillover.disk.store.enabled` 動態啟用與停用。

進入快取的項目會先進入上層的堆上層。當上層滿了之後，它會驅逐項目（通常依 LRU 順序，但快取實作可以以任何順序驅逐項目）。這些被驅逐的項目會進入下層的磁碟層。當磁碟層滿了之後，它所驅逐的項目會從快取中完全移除。如果下層已停用，從上層驅逐的項目將會離開快取。

請注意，同一個鍵一次只能存在於一個層級中；上層並不包含下層的子集。在取得鍵時，會依序檢查每一層。

您可以使用 `tiered_spillover` 讓磁碟層非常大---比在記憶體中可能達到的大小還大。這讓您可以在不使用額外堆積空間的情況下快取更多項目。

## 安裝必要的外掛程式

若要使用分層快取，請安裝 `cache-ehcache` 外掛程式。此外掛程式提供磁碟快取實作 `ehcache_disk`，可作為分層快取中的磁碟層。如需安裝非隨附外掛程式的更多資訊，請參閱 [其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#additional-plugins)。

如果未安裝 `cache-ehcache` 外掛程式，或未設定磁碟快取屬性，分層快取將無法初始化。
{: .warning}

## 分層快取設定

在 OpenSearch 2.14 及更新版本中，請求快取可以使用 `tiered_spillover` 快取或任何其他可插拔的快取實作。首先，請在 `opensearch.yml` 檔案中設定以下設定。

### 快取儲存區名稱

若要使用 OpenSearch 提供的分層溢出快取實作，請將快取儲存區名稱設為 `tiered_spillover`，如下列範例所示：

```yaml
indices.requests.cache.store.name: tiered_spillover
```
{% include copy.html %}

### 設定堆上與磁碟儲存層

將堆上與磁碟儲存層設為 `opensearch_onheap` 與 `ehcache_disk`，如下列範例所示：

```yaml
indices.requests.cache.tiered_spillover.onheap.store.name: opensearch_onheap
indices.requests.cache.tiered_spillover.disk.store.name: ehcache_disk
```
`opensearch_onheap` 設定使用 OpenSearch 內建的堆上快取。

`ehcache_disk` 設定是基於 [Ehcache](https://www.ehcache.org/) 的磁碟快取實作，需要安裝 `cache-ehcache` 外掛程式。

{% include copy.html %}

### 設定堆上與磁碟儲存區

下表列出 `opensearch_onheap` 儲存區的快取儲存區設定。

設定 | 資料類型 | 預設值 | 說明
:--- | :--- | :--- | :---
`indices.requests.cache.opensearch_onheap.size` | 百分比 | 堆積記憶體大小的 1% | 堆上快取的大小。選用。
`indices.requests.cache.opensearch_onheap.expire` | 時間單位 | `MAX_VALUE`（停用） | 指定快取結果的存活時間（TTL）。選用。

下表列出 `ehcache_disk` 儲存區的磁碟快取儲存區設定。

設定 | 資料類型 | 預設值 | 說明
:--- | :--- | :--- | :---
`indices.requests.cache.ehcache_disk.max_size_in_bytes` | 長整數 | `1073741824`（1 GB）  | 定義磁碟快取的大小。選用。
`indices.requests.cache.ehcache_disk.storage.path` | 字串 | `{data.paths}/nodes/{node.id}/request_cache` | 定義磁碟快取的儲存路徑。選用。
`indices.requests.cache.ehcache_disk.expire_after_access` | 時間單位 | `MAX_VALUE`（停用） | 指定快取結果的 TTL。選用。
`indices.requests.cache.ehcache_disk.alias` | 字串 | `ehcacheDiskCache#INDICES_REQUEST_CACHE` | 指定磁碟快取的別名。選用。
`indices.requests.cache.ehcache_disk.segments` | 整數 | `16` | 定義磁碟快取所分割的分段數量。用於並行處理。選用。
`indices.requests.cache.ehcache_disk.concurrency` | 整數 | `1` | 定義為磁碟儲存區建立的不同寫入佇列數量，其中一組分段共用一個寫入佇列。選用。
`indices.requests.cache.ehcache_disk.min_threads` | 整數 | `2`  | 定義集區中 Ehcache 磁碟執行緒的最小數量。選用。
`indices.requests.cache.ehcache_disk.max_threads` | 整數 | CPU 核心數  | 定義集區中 Ehcache 磁碟執行緒的最大數量。允許的最大值為 `10 * num_cpu_cores`。磁碟作業通常受限於 I/O 而非 CPU，因此您可以將此值設為大於 CPU 核心數的數字。選用。

### `tiered_spillover` 儲存區的其他設定

下表列出 `tiered_spillover` 儲存區設定的其他設定。

設定 | 資料類型 | 預設值 | 說明
:--- | :--- | :--- | :---
`indices.requests.cache.tiered_spillover.policies.took_time.threshold` | 時間單位 | `0ms` | 根據查詢階段的執行時間，決定是否將查詢快取至快取中的原則。這是動態設定。選用。
`indices.requests.cache.tiered_spillover.disk.store.policies.took_time.threshold` | 時間單位 | `10ms` | 根據查詢階段的執行時間，決定是否將查詢快取至快取磁碟層的原則。這是動態設定。選用。
`indices.requests.cache.tiered_spillover.disk.store.enabled` | 布林值 | `True` | 在分層溢出快取中動態啟用或停用磁碟快取。注意：停用磁碟快取後，項目不會自動移除，需要手動清除快取。選用。
`indices.requests.cache.tiered_spillover.onheap.store.size` | 百分比 | 堆積記憶體大小的 1% | 定義分層快取中堆上快取的大小。此設定會覆寫堆上快取實作本身的任何大小設定，例如 `indices.requests.cache.opensearch_onheap.size`。選用。
`indices.requests.cache.tiered_spillover.disk.store.size` | 長整數 | `1073741824`（1 GB） | 定義分層快取中磁碟快取的大小。此設定會覆寫磁碟快取實作本身的任何大小設定，例如 `indices.requests.cache.ehcache_disk.max_size_in_bytes`。選用。
`indices.requests.cache.tiered_spillover.segments` | 整數 | `2 ^ (ceil(log2(CPU_CORES * 1.5)))` | 這決定分層快取中的分段數量，每個分段都由一個可重入的讀取/寫入鎖保護。這些鎖可讓多個讀取者並行作業而不產生競爭，而分段則允許多個寫入者同時作業，從而提高寫入吞吐量。選用。

### 刪除失效項目的設定

下表列出與從快取刪除失效項目相關的設定。

設定 | 資料類型 | 預設值 | 說明
:--- | :--- |:--------| :---
`indices.requests.cache.cleanup.staleness_threshold` | 字串 | `0%`    | 定義快取中失效鍵的百分比。識別之後，所有失效的快取項目都會被刪除。選用。
`indices.requests.cache.cleanup.interval` | 時間單位 | `1m`  | 定義刪除請求快取失效項目的頻率。選用。

## 取得 `tiered_spillover` 儲存區的統計資料 

若要評估使用分層溢出快取的影響，請使用 [Node Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/#caches)，如下列範例所示：

```json
GET /_nodes/stats/caches/request_cache?level=tier
```

`tier` 層級只有在使用 `tiered_spillover` 快取時才有效，它會依上層與下層快取層級彙總統計資料。 

