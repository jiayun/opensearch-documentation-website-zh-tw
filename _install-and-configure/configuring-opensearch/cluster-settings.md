---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集管理設定"
parent: Configuring OpenSearch
nav_order: 50
---

# 叢集管理設定

下列設定可控制分片配置、協調、故障偵測及其他叢集層級的作業。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 叢集層級的路由與配置設定

OpenSearch 支援下列叢集層級的路由與分片配置設定：

- `cluster.routing.allocation.enable`（動態，字串）：啟用或停用特定類型分片的配置。
    
    有效值如下：
     - `all`：允許所有類型的分片進行分片配置。
     - `primaries`：僅允許主要分片進行分片配置。
     - `new_primaries`：僅允許新索引的主要分片進行分片配置。
     - `none`：不允許任何索引進行分片配置。
     
     預設值為 `all`。

- `cluster.routing.allocation.node_concurrent_incoming_recoveries`（動態，整數）：設定一個節點上允許同時進行的傳入分片復原數量。預設值為 `2`。

- `cluster.routing.allocation.node_concurrent_outgoing_recoveries`（動態，整數）：設定一個節點上允許同時進行的傳出分片復原數量。預設值為 `2`。

- `cluster.routing.allocation.node_concurrent_recoveries`（動態，字串）：用於將 `cluster.routing.allocation.node_concurrent_incoming_recoveries` 和 `cluster.routing.allocation.node_concurrent_outgoing_recoveries` 設為相同的值。

- `cluster.routing.allocation.node_initial_primaries_recoveries`（動態，整數）：設定節點重新啟動後，未指派主要分片的復原數量。預設值為 `4`。

- `cluster.routing.allocation.unassigned.node_left.delayed_timeout`（動態，時間單位）：設定當節點離開叢集而導致副本分片變為未指派狀態時，OpenSearch 在配置該副本分片之前預設等待的時間。延遲配置有助於在滾動升級、節點重新啟動及暫時性網路故障期間，避免不必要的分片復原。此設定僅適用於未設定索引層級 `index.unassigned.node_left.delayed_timeout` 設定的索引。設為 `0` 可針對使用叢集預設值的索引停用延遲配置。預設值為 `1m`。

- `cluster.routing.allocation.same_shard.host`（動態，布林值）：設為 `true` 時，會防止同一分片的多個複本被配置到同一主機上的不同節點。預設值為 `false`。

- `cluster.routing.rebalance.enable`（動態，字串）：啟用或停用特定類型分片的重新平衡。
    
    有效值如下：
     - `all`：允許所有類型的分片進行分片平衡。
     - `primaries`：僅允許主要分片進行分片平衡。
     - `replicas`：僅允許副本分片進行分片平衡。
     - `none`：不允許任何索引進行分片平衡。

     預設值為 `all`。

-  `cluster.routing.allocation.allow_rebalance`（動態，字串）：指定何時允許分片重新平衡。
    
    有效值如下：
    -  `always`：一律允許重新平衡。
    - `indices_primaries_active`：僅在叢集中所有主要分片都已配置時，才允許重新平衡。
    - `indices_all_active`：僅在叢集中所有分片都已配置時，才允許重新平衡。

    預設值為 `indices_all_active`。

- `cluster.routing.allocation.cluster_concurrent_rebalance`（動態，整數）：可讓您控制整個叢集中允許同時進行的分片重新平衡數量。預設值為 `2`。

- `cluster.routing.allocation.balance.shard`（動態，浮點數）：定義每個節點所配置分片總數的權重因子。預設值為 `0.45`。

- `cluster.routing.allocation.balance.index`（動態，浮點數）：定義節點上每個索引所配置分片數量的權重因子。預設值為 `0.55`。

- `cluster.routing.allocation.balance.threshold`（動態，浮點數）：應執行之作業的最低最佳化值。預設值為 `1.0`。

- `cluster.routing.allocation.balance.prefer_primary`（動態，布林值）：設為 `true` 時，OpenSearch 會嘗試在叢集節點之間平均分配主要分片。啟用此設定並不一定能保證每個節點上的主要分片數量相等，特別是在發生容錯移轉時。將此設定從 `true` 變更為 `false` 不會觸發主要分片的重新分配。預設值為 `false`。

- `cluster.routing.allocation.rebalance.primary.enable`（動態，布林值）：設為 `true` 時，OpenSearch 會嘗試在叢集節點之間重新平衡主要分片。啟用後，叢集會嘗試維持每個節點上的主要分片數量，最大緩衝由 `cluster.routing.allocation.rebalance.primary.buffer` 設定定義。將此設定從 `true` 變更為 `false` 不會觸發主要分片的重新分配。預設值為 `false`。

- `cluster.routing.allocation.rebalance.primary.buffer`（動態，浮點數）：定義啟用 `cluster.routing.allocation.rebalance.primary.enable` 時，節點之間主要分片允許的最大緩衝。預設值為 `0.1`。

- `cluster.routing.allocation.disk.threshold_enabled`（動態，布林值）：設為 `false` 時，會停用磁碟配置決策器。停用時也會移除任何現有的 `index.blocks.read_only_allow_delete index blocks`。預設值為 `true`。

- `cluster.routing.allocation.disk.watermark.low`（動態，字串）：控制磁碟使用量的低水位線。設為百分比時，OpenSearch 不會將分片配置到磁碟使用量達到該百分比的節點。此值也可以輸入為比率值，例如 `0.85`。此外，也可以設為位元組值，例如 `400mb`。此設定不會影響新建立索引的主要分片，但會阻止其副本被配置。預設值為 `85%`。

- `cluster.routing.allocation.disk.watermark.high`（動態，字串）：控制高水位線。OpenSearch 會嘗試將分片從磁碟使用量超過所定義百分比的節點移出。此值也可以輸入為比率值，例如 `0.85`。此外，也可以設為位元組值，例如 `400mb`。此設定會影響所有分片的配置。預設值為 `90%`。

- `cluster.routing.allocation.disk.watermark.flood_stage`（動態，字串）：控制洪水階段水位線。這是防止節點耗盡磁碟空間的最後手段。對於在該節點上配置了一個或多個分片，且至少有一個磁碟超過洪水階段的每個索引，OpenSearch 都會強制套用唯讀索引封鎖（`index.blocks.read_only_allow_delete`）。當磁碟使用率降至高水位線以下時，即會解除索引封鎖。此值也可以輸入為比率值，例如 `0.85`。此外，也可以設為位元組值，例如 `400mb`。預設值為 `95%`。

- `cluster.info.update.interval`（動態，時間單位）：設定 OpenSearch 檢查叢集中每個節點磁碟使用量的頻率。預設值為 `30s`。

- `cluster.blocks.create_index`（動態，布林值）：控制是否在叢集層級封鎖索引建立。設為 `true` 時，會防止建立新索引。預設值為 `false`。

- `cluster.blocks.create_index.auto_release`（動態，布林值）：控制當磁碟使用量回到閾值以下時，是否自動移除（因磁碟使用量過高而觸發的）自動索引建立封鎖。預設值為 `true`。

- `cluster.ignore_dot_indexes`（動態，布林值）：設為 `true` 時，會在分片限制驗證檢查中忽略以點號開頭的索引（例如 `.opensearch-*`）。預設值為 `false`。

- `cluster.routing.allocation.awareness.balance`（動態，布林值）：啟用跨感知屬性的感知式副本平衡。僅在同時指定 `cluster.routing.allocation.awareness.attributes` 和 `cluster.routing.allocation.awareness.force.zone.values` 時才會生效。預設值為 `false`。

- `cluster.routing.allocation.primary_constraint.threshold`（動態，long）：配置決策中主要分片限制檢查的閾值。預設值為 `10`。強制的最小值為 `0`。

- `cluster.routing.allocation.remote_primary.ignore_throttle`（動態，布林值）：是否忽略遠端主要分片還原作業的節流限制。預設值為 `true`。

- `cluster.routing.ignore_weighted_routing`（動態，布林值）：設為 `true` 時，會忽略加權路由組態並使用預設的路由行為。預設值為 `false`。

- `cluster.routing.weighted.default_weight`（動態，double）：當啟用加權路由但未設定特定權重時，指派給節點的預設權重。預設值為 `1.0`。強制的最小值為 `1.0`。

- `cluster.routing.weighted.fail_open`（動態，布林值）：啟用加權路由時，決定在所有加權節點都無法使用時是否採取失敗開放（允許請求傳送至任何節點）。預設值為 `true`。

- `cluster.routing.weighted.strict`（動態，布林值）：啟用時，會強制執行嚴格的加權路由，請求只會路由至具有適當權重的節點。預設值為 `true`。

- `cluster.routing.allocation.awareness.attributes`（動態，清單）：請參閱[分片配置感知]({{site.url}}{{site.baseurl}}/tuning-your-cluster/index#shard-allocation-awareness)。

- `cluster.routing.allocation.include.<attribute>`（動態，列舉）：將分片配置到其 `attribute` 包含至少一個所列逗號分隔值的節點。

- `cluster.routing.allocation.require.<attribute>`（動態，列舉）：僅將分片配置到其 `attribute` 包含所有所列逗號分隔值的節點。

- `cluster.routing.allocation.exclude.<attribute>`（動態，列舉）：不將分片配置到其 `attribute` 包含任何所列逗號分隔值的節點。叢集配置設定支援下列內建屬性。
    
    有效值如下：
    - `_name`：依節點名稱比對節點。
    - `_host_ip`：依主機 IP 位址比對節點。
    - `_publish_ip`：依發布 IP 位址比對節點。
    - `_ip`：比對 `_host_ip` 或 `_publish_ip` 其中之一。
    - `_host`：依主機名稱比對節點。
    - `_id`：依節點 ID 比對節點。
    - `_tier`：依資料層角色比對節點。

- `cluster.routing.allocation.awareness.force.<attribute>.values`（動態，清單）：請參閱[強制感知]({{site.url}}{{site.baseurl}}/tuning-your-cluster/index#forced-awareness)。

- `cluster.routing.allocation.shard_movement_strategy`（動態，列舉）：決定將分片從移出節點重新放置到移入節點的順序。

    此設定支援下列策略：
    - `PRIMARY_FIRST`：先重新放置主要分片，再重新放置副本分片。如果重新放置中的節點在過程中發生故障，此優先順序可能有助於防止叢集的健康狀態變為紅色。
    - `REPLICA_FIRST`：先重新放置副本分片，再重新放置主要分片。在混合版本且啟用區段複寫的 OpenSearch 叢集中執行分片重新放置時，此優先順序可能有助於防止叢集的健康狀態變為紅色。在此情況下，重新放置到較新版本 OpenSearch 節點的主要分片，可能會嘗試將區段檔案複製到較舊版本 OpenSearch 上的副本分片，進而導致分片故障。在多版本叢集中，先重新放置副本分片可能有助於避免此問題。
    - `NO_PREFERENCE`：預設行為，分片重新放置的順序不具重要性。 

- `cluster.routing.search_replica.strict`（動態，布林值）：控制當索引存在搜尋副本分片時（例如 `index.number_of_search_replicas` 大於 `0` 時），搜尋請求的路由方式。此設定僅在索引已設定搜尋副本時適用。設為 `true` 時，這類索引的所有搜尋請求只會路由至搜尋副本分片。若搜尋副本未指派，請求將會失敗。設為 `false` 時，若搜尋副本未指派，請求會改為路由至任何可用的分片。預設為 `true`。

- `cluster.allocator.gateway.batch_size`（動態，整數）：限制在單一批次中傳送至資料節點以擷取未指派分片中繼資料的分片數量。預設為 `2000`。

- `cluster.allocator.existing_shards_allocator.batch_enabled`（靜態，布林值）：啟用對已存在於磁碟上之未指派分片的批次配置，而非一次配置一個分片。這會透過在單一批次呼叫中擷取未指派分片的中繼資料，來降低記憶體與傳輸的負擔。預設為 `false`。

- `cluster.routing.allocation.shards_batch_gateway_allocator.primary_allocator_timeout`（動態，時間值）：設定主要分片批次配置器在重新路由作業期間的逾時時間。達到逾時時，重新路由的迭代會被中斷，讓較高優先順序的工作得以執行，並避免叢集在大規模分片配置期間變得無法管理。這有助於避免 API 逾時，並確保叢集的回應能力。有效值為大於或等於 `20s` 的時間值，或設為 `-1ms` 以停用逾時。預設為 `20s`。

- `cluster.routing.allocation.shards_batch_gateway_allocator.replica_allocator_timeout`（動態，時間值）：設定副本分片批次配置器在重新路由作業期間的逾時時間。達到逾時時，重新路由的迭代會被中斷，讓較高優先順序的工作得以執行，並避免叢集在大規模分片配置期間變得無法管理。這有助於避免 API 逾時，並確保叢集的回應能力。有效值為大於或等於 `20s` 的時間值，或設為 `-1ms` 以停用逾時。預設為 `20s`。

- `cluster.routing.allocation.total_shards_per_node`（動態，整數）：可配置至單一節點的主要分片與副本分片合計的最大數量。預設為 `-1`（無限制）。透過限制每個節點的分片總數，有助於將分片平均分散至各節點。請謹慎使用，因為若節點達到其設定的上限，分片可能會維持未配置狀態。

- `cluster.routing.allocation.total_primary_shards_per_node`（動態，整數）：可配置至單一節點的主要分片最大數量。此設定僅適用於遠端支援的叢集。預設為 `-1`（無限制）。透過限制每個節點的主要分片數量，有助於將主要分片平均分散至各節點。請謹慎使用，因為若節點達到其設定的上限，主要分片可能會維持未配置狀態。

- `cluster.routing.allocation.disk.watermark.enable_for_single_data_node`（靜態，布林值）：為僅有單一資料節點的叢集啟用磁碟水位檢查。啟用後，即使在單一節點叢集中，也會強制執行以磁碟為基礎的分片配置決策。預設為 `false`。

### 進階叢集路由與配置設定

OpenSearch 支援下列進階叢集路由與配置設定：

- `cluster.routing.allocation.balanced_shards_allocator.allocator_timeout`（動態，時間單位）：控制平衡分片配置器作業的逾時時間。設為 `-1` 時，會停用逾時。設為正值時，若無法完成配置，配置器會在指定的時間長度後逾時。預設為 `-1`（無逾時）。啟用逾時時，最小值為 `20s`。

- `cluster.routing.allocation.cluster_concurrent_recoveries`（動態，整數）：控制叢集層級允許的最大並行復原作業數量。此設定會限制整個叢集中同時進行的復原作業（重新定位作業）總數，以避免資源耗盡。設為 `-1` 表示不限制並行復原數量。預設為 `-1`。

### 負載感知配置設定

OpenSearch 支援下列負載感知配置設定，可根據節點資源使用率來分散分片：

- `cluster.routing.allocation.load_awareness.allow_unassigned_primaries`（動態，布林值）：啟用負載感知配置時，此設定控制新建立的主要分片是否可在超出偏斜係數的情況下仍被指派。設為 `true` 時，允許指派新的主要分片，同時避免副本配置超出偏斜係數。設為 `false` 可能導致主要分片維持未指派狀態，且叢集狀態變為紅色。預設為 `true`。

- `cluster.routing.allocation.load_awareness.flat_skew`（動態，整數）：負載感知配置中用於判斷節點間可接受不平衡程度的固定偏斜係數。較高的值允許更多不平衡，但可提供更大的配置彈性。預設為 `2`。最小值為 `2`。

- `cluster.routing.allocation.load_awareness.provisioned_capacity`（動態，整數）：負載感知配置的佈建容量設定。這有助於配置器瞭解節點的預期容量，以達到更好的負載分配。設為 `-1` 以停用。預設為 `-1`。

- `cluster.routing.allocation.load_awareness.skew_factor`（動態，double）：負載感知配置的偏斜係數閾值。此設定控制在配置器採取修正動作之前，節點之間可容許的不平衡程度。較高的值允許更多偏斜。預設為 `50`。設為 `-1` 以停用以偏斜為基礎的配置。

- `cluster.routing.allocation.move.primary_first`（動態，布林值）：重新平衡分片時，此設定控制是否先移動主要分片，再移動副本分片。先移動主要分片有助於更有效地平衡負載，但可能在重新平衡期間影響搜尋效能。預設為 `false`。

- `cluster.routing.allocation.node_initial_replicas_recoveries`（動態，整數）：在叢集啟動期間或節點加入時，單一節點上可同時進行的初始副本復原最大數量。此設定與並行復原上限分開，有助於控制啟動時的負載。預設為 `2`。

## 叢集層級快照設定

OpenSearch 支援下列叢集層級快照設定：

- `cluster.snapshot.info.max_concurrent_fetches`（動態，整數）：允許的最大並行快照資訊擷取作業數量。此設定有助於控制從儲存庫擷取快照中繼資料時的負載。較高的值可在管理大量快照時提升效能，但可能增加資源使用量。預設為 `5`。

## 叢集層級複合索引設定

OpenSearch 支援下列複合索引設定：

- `indices.composite_index.translog.max_flush_threshold_size`（動態，位元組大小）：複合索引在觸發排清 (flush) 之前的最大 translog 大小閾值。此設定有助於控制記憶體使用量，並確保複合索引的 translog 資料會定期保存至磁碟。預設為 `512mb`。最小值為 `128mb`。

## 叢集層級的分片、封鎖與工作設定

OpenSearch 支援下列叢集層級的分片、封鎖與工作設定：

- `action.search.shard_count.limit`（整數）：限制搜尋期間可命中的分片數量上限。超過此限制的請求將遭到拒絕。

- `cluster.blocks.read_only`（布林值）：將整個叢集設為唯讀。預設為 `false`。

- `cluster.blocks.read_only_allow_delete`（布林值）：與 `cluster.blocks.read_only` 類似，但允許您刪除索引。

- `cluster.no_cluster_manager_block`（字串）：設定在沒有作用中的叢集管理員時要拒絕的作業。可接受下列三個選項之一：
    - `all`：封鎖對叢集的所有讀取與寫入請求。
    - `write`：僅封鎖寫入請求。讀取請求仍可處理。
    - `metadata_write`：封鎖與中繼資料相關的寫入（例如對應或路由表的更新），但仍可執行一般的文件編製索引作業。讀取與寫入請求會使用節點最後收到的叢集狀態進行處理。由於該節點可能已與叢集的其他部分中斷連線，因此可能導致提供過時的資訊或僅傳回部分資料。

- `cluster.max_shards_per_node`（整數）：限制叢集的主要分片與副本分片總數。此限制的計算方式如下：`cluster.max_shards_per_node` 乘以非凍結資料節點的數量。已關閉索引的分片不計入此限制。預設為 `1000`。

- `cluster.max_remote_capable_shards_per_node`（整數）：限制叢集中由 warm 角色節點使用的主要分片與副本分片總數。此限制的計算方式為 `cluster.max_remote_capable_shards_per_node` 乘以 warm 資料節點的數量。此設定適用於控制可搜尋快照的分片總數。預設為 `1000`。

- `cluster.persistent_tasks.allocation.enable`（字串）：啟用或停用持續性工作的配置。

    有效值如下：
    - `all` – 允許將持續性工作指派給節點。
    - `none` – 不允許配置持續性工作。這不會影響已在執行中的持續性工作。

    預設為 `all`。

- `cluster.persistent_tasks.allocation.recheck_interval`（時間單位）：當叢集狀態發生重大變更時，叢集管理員會自動檢查是否需要指派持續性工作。還有其他因素（例如記憶體使用量）會影響持續性工作是否指派給節點，但這些因素本身不會導致叢集狀態變更。此設定定義因應這些因素而執行指派檢查的頻率。預設為 `30 seconds`，且最小值必須為 `10 seconds`。

- `task_cancellation.duration_millis`（動態，long）：工作取消監控系統中追蹤已取消工作的持續時間閾值，以毫秒為單位。預設為 `10000`（10 秒）。

- `task_cancellation.enabled`（動態，布林值）：啟用或停用工作取消監控服務。預設為 `true`。

- `task_resource_tracking.enabled`（動態，布林值）：控制是否啟用工作資源追蹤，以監控個別工作的 CPU 與記憶體使用量。預設為 `true`。

## 叢集層級的搜尋設定

OpenSearch 支援下列叢集層級的搜尋設定：

- `cluster.search.ignore_awareness_attributes`（布林值）：控制在分片查詢路由期間是否考量感知屬性。若為 `true`，叢集會忽略感知屬性，並使用自適應副本選擇（Adaptive Replica Selection，ARS）來選擇最佳的分片複本，以降低查詢回應延遲。若要讓路由決策優先考量感知屬性，而非依據效能進行選擇，請將此設定為 `false`。預設為 `true`（Amazon OpenSearch Service 為 `false`）。

## 叢集層級的慢速記錄檔設定

如需詳細資訊，請參閱[搜尋請求慢速記錄檔]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/logs/#search-request-slow-logs)。

- `cluster.search.request.slowlog.threshold.warn`（時間單位）：設定請求層級慢速記錄檔的 `WARN` 閾值。預設為 `-1`。

- `cluster.search.request.slowlog.threshold.info`（時間單位）：設定請求層級慢速記錄檔的 `INFO` 閾值。預設為 `-1`。

- `cluster.search.request.slowlog.threshold.debug`（時間單位）：設定請求層級慢速記錄檔的 `DEBUG` 閾值。預設為 `-1`。

- `cluster.search.request.slowlog.threshold.trace`（時間單位）：設定請求層級慢速記錄檔的 `TRACE` 閾值。預設為 `-1`。

- `cluster.search.request.slowlog.level`（字串）：設定要記錄的最低慢速記錄檔層級：`WARN`、`INFO`、`DEBUG` 和 `TRACE`。預設為 `TRACE`。

## 索引的叢集設定

如需套用至所有索引的叢集設定相關資訊，請參閱[索引的叢集設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/)。

## 叢集層級的協調設定

OpenSearch 支援下列叢集層級的協調設定。此清單中的所有設定皆為動態設定：

- `cluster.fault_detection.leader_check.timeout`（時間單位）：在領導者檢查期間，節點等待選出的叢集管理員回應的時間長度，超過此時間即視為檢查失敗。有效值為 `1ms` 到 `60s`（含）。預設為 `10s`。將此設定變更為預設值以外的值，可能導致叢集不穩定。

- `cluster.fault_detection.follower_check.timeout`（時間單位）：在追隨者檢查期間，選出的叢集管理員等待回應的時間長度，超過此時間即視為檢查失敗。有效值為 `1ms` 到 `60s`（含）。預設為 `10s`。將此設定變更為預設值以外的值，可能導致叢集不穩定。

- `cluster.fault_detection.follower_check.interval`（時間單位）：選出的叢集管理員向叢集中其他節點傳送追隨者檢查之間的等待時間。有效值為 `100ms` 以上。預設為 `1000ms`。將此設定變更為預設值以外的值，可能導致叢集不穩定。

- `cluster.follower_lag.timeout`（時間單位）：選出的叢集管理員等待落後節點確認叢集狀態更新的時間長度。預設為 `90s`。若節點未在此時間內成功套用叢集狀態更新，即視為失敗並從叢集中移除。

- `cluster.publish.timeout`（時間單位）：叢集管理員等待每次叢集狀態更新完整發布至所有節點的時間長度，除非 `discovery.type` 設為 `single-node`。預設為 `30s`。

## 叢集層級的故障偵測設定

OpenSearch 支援下列叢集層級的故障偵測設定，用於控制節點如何偵測及因應故障：

- `cluster.fault_detection.follower_check.retry_count`（靜態，整數）：設定追隨者檢查必須連續失敗幾次，選出的叢集管理員才會將節點視為故障並從叢集中移除。此設定控制追隨者節點的故障偵測靈敏度。預設為 `3`。**警告**：變更此設定的預設值可能導致叢集不穩定。

- `cluster.fault_detection.leader_check.interval`（靜態，時間單位）：設定每個節點檢查選出的叢集管理員之間的等待時間。這會控制追隨者節點執行領導者健康狀態檢查的頻率。預設為 `1s`。**警告**：變更此設定的預設值可能導致叢集不穩定。

- `cluster.fault_detection.leader_check.retry_count`（靜態，整數）：設定領導者檢查必須連續失敗幾次，節點才會將選出的叢集管理員視為故障，並嘗試尋找或選出新的叢集管理員。此設定控制叢集管理員節點的故障偵測靈敏度。預設為 `3`。**警告**：變更此設定的預設值可能導致叢集不穩定。

- `cluster.indices.tombstones.size`（靜態，整數）：設定叢集狀態中要保留的索引刪除墓碑數量上限。索引墓碑可防止在刪除發生時不屬於叢集的節點加入叢集，並重新匯入該索引，彷彿從未發出刪除一樣。為避免叢集狀態變得過大，系統只會保留最近的刪除記錄。預設為 `500`。若您預期節點會離開叢集並錯過超過 500 次的索引刪除，可以增加此值，但這種情況很少見。墓碑佔用的空間極小，但不建議使用非常大的值（例如 50,000）。

## 叢集層級 CAT 回應限制設定

OpenSearch 支援下列叢集層級 CAT API 回應限制設定，這些設定皆為動態設定：

- `cat.indices.response.limit.number_of_indices`（整數）：設定 [CAT Indices API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/) 傳回的索引數量上限。預設值為 `-1`（無限制）。如果回應中的索引數量超過此上限，API 會傳回 `429` 錯誤。為避免發生此情況，您可以在查詢中指定索引模式篩選條件（例如 `_cat/indices/<index-pattern>`）。

- `cat.shards.response.limit.number_of_shards`（整數）：設定 [CAT Shards API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-shards/) 傳回的分片數量上限。預設值為 `-1`（無限制）。如果回應中的分片數量超過此上限，API 會傳回 `429` 錯誤。為避免發生此情況，您可以在查詢中指定索引模式篩選條件（例如 `_cat/shards/<index-pattern>`）。

- `cat.segments.response.limit.number_of_indices`（整數）：設定 [CAT Segments API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-segments/) 傳回的索引數量上限。預設值為 `-1`（無限制）。如果回應中的索引數量超過此上限，API 會傳回 `429` 錯誤。為避免發生此情況，您可以在查詢中指定索引模式篩選條件（例如 `_cat/segments/<index-pattern>`）。

## 叢集層級閘道與索引設定

OpenSearch 支援下列閘道與索引設定：

- `gateway.slow_write_logging_threshold`（動態，時間單位）：在閘道叢集狀態持久化過程中，記錄緩慢寫入作業的門檻值。預設值為 `10s`。強制最小值為 `0`。

- `indices.id_field_data.enabled`（動態，布林值）：控制是否為索引啟用 ID 欄位資料，以便對 `_id` 欄位進行排序與彙總。預設值為 `true`。

- `indices.mapping.max_in_flight_updates`（動態，整數）：允許的並行對應更新請求數量上限。預設值為 `10`。強制最小值為 `1`。允許的最大值為 `1000`。

- `indices.recovery.internal_action_long_timeout`（動態，時間單位）：長時間執行之內部復原動作的逾時時間。預設值為 `indices.recovery.internal_action_timeout` 值的兩倍。強制最小值為 `0`。

- `indices.recovery.internal_remote_upload_timeout`（動態，時間單位）：分片復原期間內部遠端上傳作業的逾時時間。預設值為 `1h`。

- `indices.replication.initial_retry_backoff_bound`（動態，時間單位）：複寫作業失敗時，第一次重試退避時間的上限。預設值為 `50ms`。強制最小值為 `10ms`。

- `indices.replication.retry_timeout`（動態，時間單位）：重試失敗複寫請求的總逾時時間。預設值為 `60s`。

## 叢集層級中繼資料設定

OpenSearch 支援下列叢集層級中繼資料設定：

- `cluster.metadata.<key>`（動態，視情況而定）：以 `"cluster.metadata.key": "value"` 格式新增叢集中繼資料。此設定適合用於保存與叢集相關、任意且不常變動的資訊（例如聯絡資訊或註解），而無須建立專用索引。**重要**：使用者定義的叢集中繼資料並非用於儲存敏感或機密資訊。任何可存取 Get Cluster Settings API 的人都能看到這些值，且這些值會被記錄在記錄檔中。

## 叢集層級遠端叢集設定

OpenSearch 支援下列遠端叢集設定：

- `cluster.remote.initial_connect_timeout`（動態，時間單位）：設定節點啟動時與遠端叢集建立初始連線的逾時時間。這可避免在遠端叢集無法使用時，節點於啟動期間無限期停滯。預設值為 `30s`。

- `cluster.remote.connections_per_cluster`（靜態，整數）：與遠端叢集建立的連線數量上限。如果只有一個種子節點，系統會探索其他節點，直到達到此數量為止。預設值為 `3`。最小值為 `1`。

- `cluster.remote.<cluster_alias>.mode`（動態，字串）：指定特定遠端叢集的連線模式。有效值為 `sniff`（探索並連線至遠端叢集中的多個節點）與 `proxy`（透過單一代理位址連線）。預設值為 `sniff`。

- `node.remote_cluster_client`（靜態，布林值）：控制節點是否可作為跨叢集用戶端並連線至遠端叢集。預設值為 `true`。設為 `false` 可防止節點連線至遠端叢集。遠端叢集請求必須傳送至已啟用此設定的節點。

- `cluster.remote.<cluster_alias>.skip_unavailable`（動態，布林值）：控制當此特定遠端叢集無法使用時，跨叢集作業是否應繼續進行。設為 `true` 時，該叢集會成為選用叢集，若無法連線，作業將略過該叢集。設為 `false` 時，若此叢集無法使用，作業將會失敗。預設值為 `false`。

- `cluster.remote.<cluster_alias>.transport.compress`（動態，布林值）：為與特定遠端叢集之間的傳輸通訊啟用壓縮。啟用後可降低網路頻寬用量，但會增加壓縮作業的 CPU 負擔。若未設定，則會以全域 `transport.compress` 設定作為備援。預設值為 `false`。

- `cluster.remote.<cluster_alias>.transport.ping_schedule`（動態，時間單位）：設定傳送應用程式層級 ping 訊息的間隔，以維持與特定遠端叢集的連線。設為 `-1` 會停用此叢集的 ping。若未設定，則使用全域 `transport.ping_schedule` 設定。預設值為 `-1`（停用）。

- `cluster.remote.<cluster_alias>.seeds`（動態，清單）：僅適用於 `sniff` 模式。指定用來探索遠端叢集拓撲的種子節點清單。系統會先聯繫這些節點，以擷取叢集狀態並識別用於持續連線的閘道節點。

- `cluster.remote.<cluster_alias>.node_connections`（動態，整數）：僅適用於 `sniff` 模式。設定在遠端叢集中要維持作用中連線的閘道節點數量。連線越多可提供越佳的可用性，但會耗用更多資源。預設值為 `3`。

- `cluster.remote.<cluster_alias>.cluster_name`（動態，字串）：僅適用於 `sniff` 模式。指定遠端叢集的預期名稱。設定後，系統會在建立連線時驗證遠端叢集名稱。這有助於在種子節點設定錯誤或過時的情況下，避免意外連線至非預期的叢集。

- `cluster.remote.node.attr`（靜態，字串）：僅適用於 `sniff` 模式。指定節點屬性，用以篩選遠端叢集中符合閘道節點資格的節點。設定後，只有具備指定屬性的遠端叢集節點才會用於連線。例如，若遠端叢集節點具有 `node.attr.gateway: true`，且此設定設為 `gateway`，則跨叢集作業只會連線至這些節點。

- `cluster.remote.<cluster_alias>.proxy_address`（動態，字串）：僅適用於 `proxy` 模式。指定連線至遠端叢集時使用的代理伺服器位址。所有遠端連線都會透過此單一代理端點進行路由。

- `cluster.remote.<cluster_alias>.proxy_socket_connections`（動態，整數）：僅適用於 `proxy` 模式。設定要為此遠端叢集開啟至代理伺服器的通訊端連線數量。連線越多可提升輸送量，但會耗用更多資源。預設值為 `18`。

- `cluster.remote.<cluster_alias>.server_name`（動態，字串）：僅適用於 `proxy` 模式。指定在為遠端叢集連線啟用 TLS 時，於 TLS 伺服器名稱指示（SNI）延伸中傳送的主機名稱。此值必須是符合 TLS SNI 規格的有效主機名稱。

## 叢集管理員任務節流設定

OpenSearch 支援下列動態叢集管理員任務節流設定，用於控制特定叢集管理員作業的待處理任務數量：

- `cluster_manager.throttling.thresholds.<task_name>.value`（動態，整數）：設定特定叢集管理員任務類型的節流上限。達到此上限時，此類型的其他任務會排入佇列，而非立即處理。設定為 `-1` 會停用指定任務類型的節流。預設值依任務類型而異。可用的任務名稱包括：
  - `create-index`：控制索引建立作業
  - `delete-index`：控制索引刪除作業
  - `put-mapping`：控制對應更新作業
  - `index-aliases`：控制索引別名作業
  - `cluster-update-settings`：控制叢集設定更新
  - `put-pipeline`：控制資料匯入管線作業
  - `delete-pipeline`：控制資料匯入管線刪除
  - `put-search-pipeline`：控制搜尋管線作業
  - `delete-search-pipeline`：控制搜尋管線刪除
  - `put-script`：控制已儲存指令碼作業
  - `delete-script`：控制已儲存指令碼刪除
  - `create-snapshot`：控制快照建立作業
  - `delete-snapshot`：控制快照刪除作業
  - 以及其他叢集管理員任務類型


## 叢集層級遠端儲存設定

OpenSearch 支援下列遠端儲存設定：

如需實用範例與逐步組態指南，請參閱[遠端支援儲存空間]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/)。
{: .tip}


- `cluster.remote_store.index.restrict.async-durability`（靜態，布林值）：**受限存取設定。** 啟用時（`true`），會限制建立或修改 `index.translog.durability` 設定為 `async` 的索引。此設定可防止索引在遠端儲存環境中使用 `async` 持久性模式，以強制執行更強的持久性保證。設定為 `false` 時，索引可使用任何持久性模式（`sync` 或 `async`），且可隨時在模式之間切換。設定為 `true` 時，任何以 `index.translog.durability=async` 建立或更新索引的嘗試都會遭到拒絕。此設定專為非同步持久性可能危及資料一致性的遠端儲存部署而設計。預設值為 `false`。

- `cluster.remote_store.compatibility_mode`（動態，字串）：控制叢集遷移期間遠端儲存作業的相容性模式。有效值為：
  - `strict`：只有具備相同遠端儲存組態的節點才能加入叢集
  - `mixed`：在遷移期間允許同時包含已啟用遠端儲存的節點與一般節點的混合叢集
  預設值為 `strict`。

- `cluster.remote_store.state.enabled`（靜態，布林值）：啟用遠端叢集狀態功能。啟用時，除了本機儲存空間之外，叢集狀態中繼資料也會儲存在遠端儲存庫中，以啟用無縫搜尋副本復原與提升叢集復原能力等功能。此設定必須在叢集初始化期間設定，且需要適當的遠端儲存庫組態。預設值為 `false`。

- `cluster.remote_store.publication.enabled`（靜態，布林值）：啟用叢集狀態更新的遠端發布。啟用時，叢集狀態變更會發布至遠端儲存，以實現分散式狀態管理並改善叢集協調。此設定需要將 `cluster.remote_store.state.enabled` 設為 `true`。預設值為 `false`。

- `cluster.remote_store.index_metadata.path_type`（靜態，字串）：定義在遠端儲存中儲存索引中繼資料時所使用的路徑結構。有效值為：
  - `FIXED`：使用固定的路徑結構儲存中繼資料
  - `HASHED_PREFIX`：在路徑結構中使用雜湊前綴，以獲得更好的分布
  - `HASHED_INFIX`：在路徑結構中使用雜湊中綴，以實現負載平衡
  預設值為 `HASHED_PREFIX`。

- `cluster.remote_store.index_metadata.path_hash_algo`（靜態，字串）：當 `cluster.remote_store.index_metadata.path_type` 設定為 `HASHED_PREFIX` 或 `HASHED_INFIX` 時，指定用於建構索引中繼資料路徑中前綴或中綴的雜湊演算法。有效值為：
  - `FNV_1A_BASE64`：使用 FNV-1a 雜湊搭配 Base64 編碼
  - `FNV_1A_COMPOSITE_1`：使用 FNV-1a 雜湊搭配複合編碼，以獲得更好的分布
  預設值為 `FNV_1A_BASE64`。

- `cluster.filecache.remote_data_ratio`（動態，double）：在遠端儲存組態中，控制檔案快取的遠端資料與本機磁碟快取的比例。此設定決定有多少遠端資料會快取在本機以提升效能。值越高，在本機快取的資料越多，但會耗用更多磁碟空間。值應介於 0.0 與 1.0 之間。預設值為 `0.8`。

- `cluster.indices.replication.strategy`（動態，字串）：設定叢集中索引的複寫策略。有效值包括：
  - `DOCUMENT`：傳統的以文件為基礎的複寫
  - `SEGMENT`：以區段為基礎的複寫，可提升效能與效率
  預設值為 `DOCUMENT`。

- `cluster.index.restrict.replication.type`（動態，布林值）：啟用時，會限制建立具有特定複寫類型的索引，以確保整個叢集的一致性。此設定有助於強制執行複寫政策，並防止不相容的複寫組態。預設值為 `false`。
