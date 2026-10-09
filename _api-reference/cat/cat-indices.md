---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 索引"
parent: CAT APIs
nav_order: 25
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-indices/
---

# CAT Indices API
**1.0 版引入**
{: .label .label-purple }

CAT indices 操作會列出與索引相關的資訊，例如它們使用了多少磁碟空間、有多少分片、健康狀態等等。

回應中的文件計數直接來自 Lucene，因此包含隱藏的[巢狀]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)文件。舉例來說，包含兩個巢狀物件的文件會計為三份文件。若只要計算最上層的文件，請使用 [CAT count]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-count/) 或 [Count]({{site.url}}{{site.baseurl}}/api-reference/search-apis/count/) API。


<!-- spec_insert_start
api: cat.indices
component: endpoints
-->
## 端點
```json
GET /_cat/indices
GET /_cat/indices/{index}
```
<!-- spec_insert_end -->


## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `bytes` | 字串 | 用來顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 及 `p`。 | N/A |
| `cluster_manager_timeout` | 字串 | 允許建立與叢集管理員節點連線的時間長度。 | N/A |
| `expand_wildcards` | 清單或字串 | 指定萬用字元運算式可符合的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：符合任何索引，包括隱藏索引。<br> - `closed`：符合已關閉且非隱藏的索引。<br> - `hidden`：符合隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：符合已開啟且非隱藏的索引。 | 若 `system` 為 `false` 或省略則為 `open,closed`，若 `system` 為 `true` 則為 `open,closed,hidden`。 |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 要顯示的欄位名稱清單，以逗號分隔。 | N/A |
| `health` | 字串 | 依據索引的健康狀態加以限制。支援的值為 `green`、`yellow` 及 `red`。<br> 有效值為：`green`、`GREEN`、`yellow`、`YELLOW`、`red` 及 `RED`。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `include_unloaded_segments` | 布林值 | 是否包含未載入記憶體之分段的資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `pri` | 布林值 | 當 `true` 時，僅從主要分片傳回資訊。 | `false` |
| `s` | 清單 | 要排序的欄位名稱或欄位別名清單，以逗號分隔。 | N/A |
| `system` | 布林值 | 依據索引的系統索引分類來篩選索引。當 `true` 時，僅傳回系統索引。當 `false` 時，僅傳回非系統索引。如需更多資訊，請參閱[系統索引](#system-indexes)。 | N/A |
| `time` | 字串 | 指定時間單位。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 及 `d`。 | N/A |
| `v` | 布林值 | 啟用詳細模式，此模式會顯示欄位標頭。 | `false` |

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cat/indices?v
-->
{% capture step1_rest %}
GET /_cat/indices?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.indices(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要將資訊限制在特定索引，請在查詢後加上索引名稱。

<!-- spec_insert_start
component: example_code
rest: GET /_cat/indices/<index>?v
-->
{% capture step1_rest %}
GET /_cat/indices/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.indices(
  index = "<index>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想取得多個索引的資訊，請以逗號分隔索引：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/indices/index1,index2,index3
-->
{% capture step1_rest %}
GET /_cat/indices/index1,index2,index3
{% endcapture %}

{% capture step1_python %}


response = client.cat.indices(
  index = "index1,index2,index3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

```json
health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size
green  | open | movies | UZbpfERBQ1-3GSH2bnM3sg | 1 | 1 | 1 | 0 | 7.7kb | 3.8kb
```

## 回應欄位

根據預設，回應會包含 `health`、`status`、`index`、`uuid`、`pri`、`rep`、`docs.count`、`docs.deleted`、`store.size` 及 `pri.store.size` 欄位。若要選擇要顯示的欄位，請在 `h` 查詢參數中提供以逗號分隔的欄位名稱或別名清單。`h` 參數也接受萬用字元，例如 `h=index,search.*`。若要列出所有可用的欄位，請傳送 `GET /_cat/indices?help`。

舉例來說，下列請求會傳回 `opensearch_dashboards_sample_data_ecommerce` 索引的名稱、健康狀態、文件計數及儲存大小：

```json
GET /_cat/indices/opensearch_dashboards_sample_data_ecommerce?v&h=index,health,docs.count,store.size
```
{% include copy-curl.html %}

回應僅包含所請求的欄位：

```json
index                                       health docs.count store.size
opensearch_dashboards_sample_data_ecommerce green        4675        4mb
```

下表列出一般索引資訊欄位。

| 欄位 | 別名 | 說明 |
| :--- | :--- | :--- |
| `health` | `h` | 索引目前的健康狀態。 |
| `status` | `s` | 索引是開啟還是關閉。 |
| `index` | `i`、`idx` | 索引名稱。 |
| `uuid` | `id` | 索引 UUID。 |
| `pri` | `p`、`shards.primary`、`shardsPrimary` | 主要分片的數量。 |
| `rep` | `r`、`shards.replica`、`shardsReplica` | 副本分片的數量。 |
| `docs.count` | `dc`、`docsCount` | 可用文件的數量。 |
| `docs.deleted` | `dd`、`docsDeleted` | 已刪除文件的數量。 |
| `creation.date` | `cd` | 索引建立日期，以自 epoch 起算的毫秒數表示。 |
| `creation.date.string` | `cds` | 索引建立日期，以字串表示。 |
| `store.size` | `ss`、`storeSize` | 主要分片與副本分片的儲存大小。 |
| `pri.store.size` | N/A | 主要分片的儲存大小。 |
| `search.throttled` | `sth` | 是否對索引的搜尋進行節流。 |
| `last_index_request_timestamp` | `last_index_ts`、`lastIndexRequestTimestamp` | 上次處理索引請求的時間戳記，以自 epoch 起算的毫秒數表示。 |
| `last_index_request_timestamp_string` | `last_index_ts_string`、`lastIndexRequestTimestampString` | 上次處理索引請求的時間戳記，以 ISO 8601 字串表示。 |
| `system` | `sys` | 索引是否在叢集中繼資料中標示為系統索引。當您指定 `system` 查詢參數時會傳回。如需更多資訊，請參閱[系統索引](#system-indexes)。 |
| `system.description` | `sysdesc` | 相符系統索引描述項中的說明（若有）。當您指定 `system` 查詢參數時會傳回。如需更多資訊，請參閱[系統索引](#system-indexes)。 |

下表列出索引統計資料欄位。這些欄位會同時報告主要分片與副本分片的值。每個欄位都有一個加上 `pri.` 前置字元的對應欄位，僅報告主要分片的值，例如 `pri.completion.size` 或 `pri.search.query_total`。`pri.` 欄位沒有別名。`search.startree_query_current`、`search.startree_query_time` 及 `search.startree_query_total` 的主要分片對應欄位分別命名為 `pri.search.startree.query_current`、`pri.search.startree.query_time` 及 `pri.search.startree.query_total`。

| 欄位 | 別名 | 說明 |
| :--- | :--- | :--- |
| `completion.size` | `cs`, `completionSize` | 自動完成資料的大小。 |
| `fielddata.evictions` | `fe`, `fielddataEvictions` | 欄位資料快取的逐出次數。 |
| `fielddata.memory_size` | `fm`, `fielddataMemory` | 欄位資料快取所使用的記憶體。 |
| `flush.total` | `ft`, `flushTotal` | 排清作業的次數。 |
| `flush.total_time` | `ftt`, `flushTotalTime` | 排清作業所花費的時間。 |
| `get.current` | `gc`, `getCurrent` | 目前 get 作業的次數。 |
| `get.exists_time` | `geti`, `getExistsTime` | 成功 get 作業所花費的時間。 |
| `get.exists_total` | `geto`, `getExistsTotal` | 成功 get 作業的次數。 |
| `get.missing_time` | `gmti`, `getMissingTime` | 失敗 get 作業所花費的時間。 |
| `get.missing_total` | `gmto`, `getMissingTotal` | 失敗 get 作業的次數。 |
| `get.time` | `gti`, `getTime` | get 作業所花費的時間。 |
| `get.total` | `gto`, `getTotal` | get 作業的次數。 |
| `indexing.delete_current` | `idc`, `indexingDeleteCurrent` | 目前 delete 作業的次數。 |
| `indexing.delete_time` | `idti`, `indexingDeleteTime` | delete 作業所花費的時間。 |
| `indexing.delete_total` | `idto`, `indexingDeleteTotal` | delete 作業的次數。 |
| `indexing.index_current` | `iic`, `indexingIndexCurrent` | 目前編製索引作業的次數。 |
| `indexing.index_failed` | `iif`, `indexingIndexFailed` | 失敗編製索引作業的次數。 |
| `indexing.index_time` | `iiti`, `indexingIndexTime` | 編製索引作業所花費的時間。 |
| `indexing.index_total` | `iito`, `indexingIndexTotal` | 編製索引作業的次數。 |
| `memory.total` | `tm`, `memoryTotal` | 使用的記憶體總量。 |
| `merges.current` | `mc`, `mergesCurrent` | 目前合併作業的次數。 |
| `merges.current_docs` | `mcd`, `mergesCurrentDocs` | 目前合併作業中的文件數。 |
| `merges.current_size` | `mcs`, `mergesCurrentSize` | 目前合併作業的大小。 |
| `merges.total` | `mt`, `mergesTotal` | 已完成合併作業的次數。 |
| `merges.total_docs` | `mtd`, `mergesTotalDocs` | 已合併文件的數量。 |
| `merges.total_size` | `mts`, `mergesTotalSize` | 已合併資料的總大小。 |
| `merges.total_time` | `mtt`, `mergesTotalTime` | 合併作業所花費的時間。 |
| `merges.warmer.ongoing_count` | `mswoc`, `mergedSegmentWarmerOngoingCount` | 目前進行中的已合併分段預熱作業數。 |
| `merges.warmer.total_bytes_received` | `mswtbr`, `mergedSegmentWarmerTotalBytesReceived` | 已合併分段預熱期間，副本分片接收的位元組總數。 |
| `merges.warmer.total_bytes_sent` | `mswtbs`, `mergedSegmentWarmerTotalBytesSent` | 已合併分段預熱期間，主要分片傳送的位元組總數。 |
| `merges.warmer.total_failure_count` | `mswtfc`, `mergedSegmentWarmerTotalFailureCount` | 已合併分段預熱器的失敗總數。 |
| `merges.warmer.total_invocations` | `mswti`, `mergedSegmentWarmerTotalInvocations` | 已合併分段預熱器的叫用總數。 |
| `merges.warmer.total_receive_time` | `mswtrt`, `mergedSegmentWarmerTotalReceiveTime` | 副本分片接收已合併分段所花費的實際時間總量。 |
| `merges.warmer.total_send_time` | `mswtst`, `mergedSegmentWarmerTotalSendTime` | 主要分片傳送已合併分段所花費的實際時間總量。 |
| `merges.warmer.total_time` | `mswtt`, `mergedSegmentWarmerTotalTime` | 已合併分段預熱作業所花費的實際時間總量。 |
| `query_cache.evictions` | `qce`, `queryCacheEvictions` | 查詢快取的逐出次數。 |
| `query_cache.memory_size` | `qcm`, `queryCacheMemory` | 查詢快取所使用的記憶體。 |
| `refresh.external_time` | `rti`, `refreshTime` | 外部重新整理作業所花費的時間。 |
| `refresh.external_total` | `rto`, `refreshTotal` | 外部重新整理作業的總數。 |
| `refresh.listeners` | `rli`, `refreshListeners` | 待處理的重新整理接聽程式數。 |
| `refresh.time` | N/A | 重新整理作業所花費的時間。說明輸出會列出此欄位的 `rti` 與 `refreshTime` 別名，但它們會選取 `refresh.external_time`。 |
| `refresh.total` | N/A | 重新整理作業的總數。說明輸出會列出此欄位的 `rto` 與 `refreshTotal` 別名，但它們會選取 `refresh.external_total`。 |
| `request_cache.evictions` | `rce`, `requestCacheEvictions` | 請求快取的逐出次數。 |
| `request_cache.hit_count` | `rchc`, `requestCacheHitCount` | 請求快取命中次數。 |
| `request_cache.memory_size` | `rcm`, `requestCacheMemory` | 請求快取所使用的記憶體。 |
| `request_cache.miss_count` | `rcmc`, `requestCacheMissCount` | 請求快取未命中次數。 |
| `search.concurrent_avg_slice_count` | `casc`, `searchConcurrentAvgSliceCount` | 並行分段搜尋的平均配量計數。 |
| `search.concurrent_query_current` | `scqc`, `searchConcurrentQueryCurrent` | 目前並行查詢階段作業的次數。 |
| `search.concurrent_query_time` | `scqti`, `searchConcurrentQueryTime` | 並行查詢階段所花費的時間。 |
| `search.concurrent_query_total` | `scqto`, `searchConcurrentQueryTotal` | 並行查詢階段作業的次數。 |
| `search.fetch_current` | `sfc`, `searchFetchCurrent` | 目前擷取階段作業的次數。 |
| `search.fetch_time` | `sfti`, `searchFetchTime` | 擷取階段所花費的時間。 |
| `search.fetch_total` | `sfto`, `searchFetchTotal` | 擷取階段作業的次數。 |
| `search.open_contexts` | `so`, `searchOpenContexts` | 開啟的搜尋上下文數。 |
| `search.point_in_time_current` | `scc`, `searchPointInTimeCurrent` | 開啟的時間點上下文數。 |
| `search.point_in_time_time` | `scti`, `searchPointInTimeTime` | 時間點上下文保持開啟的時間。 |
| `search.point_in_time_total` | `scto`, `searchPointInTimeTotal` | 已完成的時間點上下文數。 |
| `search.query_current` | `sqc`, `searchQueryCurrent` | 目前查詢階段作業的次數。 |
| `search.query_failed` | `sqf`, `searchQueryFailed` | 失敗查詢階段作業的次數。 |
| `search.query_time` | `sqti`, `searchQueryTime` | 查詢階段所花費的時間。 |
| `search.query_total` | `sqto`, `searchQueryTotal` | 查詢階段作業的次數。 |
| `search.scroll_current` | `searchScrollCurrent` | 開啟的捲動上下文數。 |
| `search.scroll_time` | `searchScrollTime` | 捲動上下文保持開啟的時間。 |
| `search.scroll_total` | `searchScrollTotal` | 已完成的捲動上下文數。 |
| `search.startree_query_current` | `stqc` | 目前 star-tree 查詢作業的次數。 |
| `search.startree_query_failed` | `stqf`, `startreeQueryFailed` | 失敗 star-tree 查詢作業的次數。 |
| `search.startree_query_time` | `stqti`, `startreeQueryTime` | star-tree 查詢所花費的時間。 |
| `search.startree_query_total` | `stqto`, `startreeQueryCurrent` | 使用 star-tree 索引解析的查詢數。 |
| `segments.count` | `sc`, `segmentsCount` | 分段數。 |
| `segments.fixed_bitset_memory` | `sfbm`, `fixedBitsetMemory` | 巢狀物件欄位類型與類型篩選器所使用的固定位元集記憶體。 |
| `segments.index_writer_memory` | `siwm`, `segmentsIndexWriterMemory` | 索引寫入器所使用的記憶體。 |
| `segments.memory` | `sm`, `segmentsMemory` | 分段所使用的記憶體。 |
| `segments.version_map_memory` | `svmm`, `segmentsVersionMapMemory` | 版本對應所使用的記憶體。 |
| `suggest.current` | `suc`, `suggestCurrent` | 目前建議作業的次數。 |
| `suggest.time` | `suti`, `suggestTime` | 建議作業所花費的時間。 |
| `suggest.total` | `suto`, `suggestTotal` | 建議作業的次數。 |
| `warmer.current` | `wc`, `warmerCurrent` | 目前預熱作業的次數。 |
| `warmer.total` | `wto`, `warmerTotal` | 預熱作業的次數。 |
| `warmer.total_time` | `wtt`, `warmerTotalTime` | 預熱作業所花費的時間。 |

## 系統索引
**3.9 版引入**
{: .label .label-purple }

`system` 查詢參數會依據系統索引分類篩選索引：

- `system=true` 僅傳回系統索引。
- `system=false` 僅傳回非系統索引。

若省略 `system`，則會依據請求的索引選取與萬用字元展開結果，同時傳回系統索引與非系統索引。

當指定 `system=true` 且省略 `expand_wildcards` 時，萬用字元展開預設會包含隱藏索引。當指定 `system=false` 或省略 `system` 時，萬用字元展開預設不會包含隱藏索引。明確指定的 `expand_wildcards` 值會覆寫這些預設行為。例如，`system=true&expand_wildcards=open` 會排除隱藏索引，而 `system=true&expand_wildcards=all` 則會包含開啟、關閉及隱藏的索引。

索引的系統分類與該索引是否為隱藏索引無關。`system` 篩選條件不會識別所有隱藏索引，也不會識別所有受 Security 外掛程式保護的索引。此篩選條件不會授予索引的存取權；您現有的權限仍然適用。如需 Security 外掛程式如何保護系統索引的相關資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。

只要您指定 `system`（包括 `system=false`），回應中就會包含 `system` 與 `system.description` 欄。當省略 `system` 時，預設欄位保持不變。請使用 `h` 明確選取欄位。使用 `h` 選取其中任一欄，不會改變索引選取結果，也不會在萬用字元展開中包含隱藏索引。

描述的提供與 `system` 旗標無關。沒有相符描述元的索引不會有描述。若描述元登錄檔與索引中繼資料暫時不同步，具有 `system=false` 的索引仍可能會有描述。

例如，若要列出系統索引及其描述（預設包含隱藏索引），請使用下列請求：

```json
GET /_cat/indices?system=true&h=index,system,system.description&format=json
```
{% include copy-curl.html %}

以下範例回應適用於包含任務結果索引的叢集：

```json
[
  {
    "index": ".tasks",
    "system": "true",
    "system.description": "Task Result Index"
  }
]
```

若要同時顯示系統索引與非系統索引（包括開啟、關閉及隱藏的索引），請使用下列請求：

```json
GET /_cat/indices?expand_wildcards=all&h=index,system,system.description&format=json
```
{% include copy-curl.html %}

## 限制回應大小

若要限制傳回的索引數量，請設定 `cat.indices.response.limit.number_of_indices` 設定。如需詳細資訊，請參閱[叢集層級 CAT 回應限制設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-cat-response-limit-settings)。

當指定 `system` 時，此限制僅計算符合所請求系統分類的索引。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:monitor/stats` 與 `cluster:monitor/state`。
