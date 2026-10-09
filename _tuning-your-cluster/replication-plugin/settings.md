---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複製設定"
nav_order: 40
parent: Cross-cluster replication
redirect_from:
  - /replication-plugin/settings/
---

# 複製設定

複製外掛程式為標準的 OpenSearch 叢集與索引設定新增了數項設定。
這些設定是動態的，因此您無需重新啟動叢集即可變更外掛程式的預設行為。若要進一步了解靜態與動態設定，請參閱 [設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

您可以將設定標記為 `persistent` 或 `transient`。

例如，若要更新追隨者叢集向領導者叢集輪詢更新的頻率：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.replication.follower.metadata_sync_interval": "30s"
  }
}
```

這些設定可管理遠端復原所消耗的資源。我們不建議變更這些設定；預設值應能適用於大多數使用情境。

## 叢集層級設定

您可以在叢集層級指定這些設定，以控制叢集中所有索引的預設複製行為。除非被索引層級設定覆寫，否則這些設定會全域套用。

設定 | 預設值 | 說明
:--- | :--- | :---
`plugins.replication.follower.concurrent_readers_per_shard` | 2 | 複製同步階段期間，追隨者叢集每個分片的並行請求數量。
`plugins.replication.autofollow.fetch_poll_interval` | 30s | 自動跟隨任務向領導者叢集輪詢新符合索引的頻率。
`plugins.replication.follower.metadata_sync_interval` | 60s | 追隨者叢集向領導者叢集輪詢更新索引中繼資料的頻率。
`plugins.replication.translog.retention_lease.pruning.enabled` | true | 若啟用，會根據領導者索引上的保留租約修剪 translog。
`plugins.replication.translog.retention_size` | 512 MB | 控制領導者索引上 translog 的大小。
`plugins.replication.replicate.delete_index` | false | 若啟用，每當對應的領導者索引被刪除時，追隨者索引會自動刪除。
`plugins.replication.follower.index.ops_batch_size` | 50000 | 複製同步階段期間，一次可擷取的操作數量。

## 索引層級設定

您可以在建立追隨者索引時指定這些設定，或為現有的追隨者索引更新它們。這些設定可控制複製期間個別索引的行為。

設定 | 預設值 | 說明
:--- |:------| :---
`index.plugins.replication.follower.ops_batch_size` | 50000 | 複製同步階段期間，該特定索引一次可擷取的操作數量。此設定會覆寫叢集層級設定。

## 大量複製設定

下列設定可控制 [Bulk Replication API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/bulk-api/) 的行為。

設定 | 預設值 | 說明
:--- | :--- | :---
`plugins.replication.follower.bulk_batch_size` | 10 | 大量複製任務期間，每個批次中同時處理的索引數量。最小值為 `1`，最大值為 `100`。
`plugins.replication.follower.bulk_poll_timeout` | 15 | 啟動與恢復任務在將索引判定為逾時前，等待複製確認的時間（以分鐘為單位）。最小值為 `1`，最大值為 `30`。
