---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可用性與復原設定"
parent: Configuring OpenSearch
nav_order: 100
---

# 可用性與復原設定

可用性與復原設定包含下列項目的設定：

- [一般復原設定](#general-recovery-settings)
- [快照](#snapshot-settings)
- [叢集管理員任務節流](#cluster-manager-task-throttling-settings)
- [遠端支援儲存空間](#remote-backed-storage-settings)
- [搜尋背壓](#search-backpressure-settings)
- [並行限制](#concurrency-limit-settings)
- [分片索引背壓](#shard-indexing-backpressure-settings)
- [區段複寫](#segment-replication-settings)
- [跨叢集複寫](#cross-cluster-replication-settings)

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 一般復原設定

OpenSearch 支援下列一般復原設定：

- `indices.recovery.chunk_size`（動態，位元組單位）：控制索引復原作業期間傳輸資料時所使用的區塊大小。此設定會影響分片復原期間每個網路請求所傳輸的資料量。較大的區塊大小可以提升復原速度，但可能會增加記憶體使用量。預設值為 `512kb`。

- `indices.recovery.recovery_activity_timeout`（動態，時間單位）：設定分片復原作業期間個別復原活動的逾時時間。若復原活動（例如傳輸檔案區塊）所花費的時間超過此逾時時間，該復原作業即視為失敗並會重試。預設值為 `30m`。

## 快照設定

OpenSearch 支援下列快照設定：

- `snapshot.max_concurrent_operations`（動態，整數）：並行快照作業的數量上限。預設值為 `1000`。

- `snapshot.repository_data.cache.threshold`（靜態，位元組大小值或百分比）：可快取於記憶體中的儲存庫中繼資料大小上限。此設定可減少在複製、還原和狀態檢查作業期間重複下載中繼資料的需求，藉此提升快照作業效能。您可以將此值指定為絕對大小（例如 `2gb` 或 `500mb`），或指定為堆積記憶體的百分比（例如 `3%` 或 `1%`）。超過此閾值的中繼資料不會被快取。由於快取資料是以軟參考 (soft reference) 儲存，因此在堆積記憶體壓力下，快取資料可能會被自動進行垃圾回收。預設值為 500 KB 或堆積記憶體的 1%，以較高者為準。

### 安全性相關快照設定

如需安全性相關快照設定，請參閱[安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)。

### 共用檔案系統

如需使用共用檔案系統的相關資訊，請參閱[共用檔案系統]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#shared-file-system)。

### Amazon S3 設定

如需 Amazon S3 儲存庫設定的相關資訊，請參閱 [Amazon S3]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)。

## 叢集管理員任務節流設定

如需叢集管理員任務節流設定的相關資訊，請參閱[設定節流限制]({{site.url}}{{site.baseurl}}/tuning-your-cluster/cluster-manager-task-throttling/#setting-throttling-limits)。

## 遠端支援儲存空間設定

OpenSearch 支援下列叢集層級的遠端支援儲存空間設定：

- `cluster.remote_store.translog.buffer_interval`（動態，時間單位）：執行定期 translog 更新時所使用的 translog 緩衝區間隔預設值。只有在索引設定 `index.remote_store.translog.buffer_interval` 不存在時，此設定才會生效。

如需更多遠端支援儲存空間設定，請參閱[遠端支援儲存空間]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)和[設定遠端支援儲存空間]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/#configuring-remote-backed-storage)。

如需遠端區段背壓設定，請參閱[遠端區段背壓設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-backpressure/#remote-segment-backpressure-settings)。

如需遠端區段預熱設定，請參閱[遠端區段預熱設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-warmer/#remote-segment-warmer-settings)。

## 搜尋背壓設定

搜尋背壓是一種機制，用於識別耗用大量資源的搜尋請求，並在節點承受壓力時取消這些請求。如需詳細資訊，請參閱[搜尋背壓設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/search-backpressure/#search-backpressure-settings)。

## 並行限制設定

並行限制會以自適應方式限制任何傳輸動作的作用中請求數量。如需詳細資訊，請參閱[並行限制設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/concurrency-limits/#concurrency-limit-settings)。

## 分片索引背壓設定

分片索引背壓是一種以個別分片為層級的智慧拒絕機制，會在叢集負載過重時動態拒絕編製索引請求。如需詳細資訊，請參閱分片索引背壓[設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/shard-indexing-settings/)。

## 區段複寫設定

如需區段複寫設定的相關資訊，請參閱[區段複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/index/)。

如需區段複寫背壓設定的相關資訊，請參閱[區段複寫背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/backpressure/)。

## 跨叢集複寫設定

如需跨叢集複寫設定的相關資訊，請參閱[複寫設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/settings/)。
