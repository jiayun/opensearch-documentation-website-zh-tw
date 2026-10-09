---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分段複寫背壓"
nav_order: 75
parent: Segment replication
has_children: false
grand_parent: Availability and recovery
---

# 分段複寫背壓

分段複寫背壓是一種分片層級的拒絕機制，當您叢集中的副本分片落後主要分片時，會動態拒絕索引請求。使用分段複寫背壓時，當複寫群組中過期分片的百分比超過 `segrep.pressure.replica.stale.limit`（預設為 50%）時，索引請求就會被拒絕。若副本落後主要分片的檢查點數量超過 `segrep.pressure.checkpoint.limit` 設定，且其目前的複寫延遲大於定義的 `segrep.pressure.time.limit` 欄位，則該副本會被視為過期。

系統也會監視副本分片，以判斷這些分片是否卡住或延遲過長。當副本分片卡住或延遲的時間超過 `segrep.pressure.time.limit` 欄位所定義時間的兩倍時，這些分片會被移除，並以新的副本分片取代。

## 請求本文欄位

分段複寫背壓預設為停用。若要啟用，請將 `segrep.pressure.enabled` 設為 `true`。您可以使用 [叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) API 端點更新下列動態叢集設定。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`segrep.pressure.enabled `| 布林值 | 啟用分段複寫背壓機制。預設為 `false`。
`segrep.pressure.time.limit` | 時間單位 | 副本分片從主要分片複製所能花費的時間上限。一旦 `segrep.pressure.time.limit` 與 `segrep.pressure.checkpoint.limit` 同時超過，就會啟動分段複寫背壓機制。預設為 `5 minutes`。
`segrep.pressure.checkpoint.limit` | 整數 | 副本分片從主要分片複製時，所能落後的索引檢查點數量上限。一旦 `segrep.pressure.checkpoint.limit` 與 `segrep.pressure.time.limit` 同時超過，就會啟動分段複寫背壓機制。預設為 `4` 個檢查點。
`segrep.pressure.replica.stale.limit `| 浮點數 | 複寫群組中可存在的過期副本分片數量上限。一旦超過 `segrep.pressure.replica.stale.limit`，就會啟動分段複寫背壓機制。預設為 `.5`，即複寫群組的 50%。

## 端點

您可以使用分段複寫 API 端點擷取分段複寫背壓指標，如下所示：

```bash
GET _cat/segment_replication
```
{% include copy-curl.html %}

#### 範例回應

```json
shardId       target_node    target_host   checkpoints_behind bytes_behind   current_lag   last_completed_lag   rejected_requests
[index-1][0]     runTask-1    127.0.0.1              0              0b           0s              7ms                    0
```

啟動分段複寫背壓時，會將 `checkpoints_behind` 與 `current_lag` 指標納入考量。系統會分別將它們與 `segrep.pressure.checkpoint.limit` 和 `segrep.pressure.time.limit` 進行比對。
