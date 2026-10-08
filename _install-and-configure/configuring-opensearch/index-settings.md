---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引設定"
parent: Configuring OpenSearch
nav_order: 170
redirect_from:
  - /im-plugin/index-settings/
---

# 索引設定

索引設定套用於個別索引，其名稱以 `index.` 開頭。若要了解套用於叢集中所有索引的叢集設定，請參閱[索引的叢集設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/)。

您可以在建立索引時指定索引設定。索引設定可以是靜態或動態的。下表說明您可以在何時以及如何更新各類型的設定。

| 設定類型 | 可更新的時機 | 更新方式 |
|:---|:---|:---|
| [靜態](#static-index-settings) | 索引關閉時 | 關閉索引，使用 Update Index Settings API 更新設定，然後重新開啟索引。如需詳細資訊，請參閱[更新靜態索引設定](#updating-a-static-index-setting)。 |
| [動態](#dynamic-index-settings) | 任何時候 | 使用 Update Index Settings API。如需詳細資訊，請參閱[更新動態索引設定](#updating-a-dynamic-index-setting)。 |

## 在建立索引時指定設定

建立索引時，您可以依下列方式指定其靜態或動態設定：

```json
PUT /testindex
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 2
  }
}
```
{% include copy-curl.html %}

## 更新靜態索引設定

您只能在已關閉的索引上更新靜態索引設定。下列範例示範如何更新索引編解碼器 (codec) 設定。

首先，關閉索引：

```json
POST /testindex/_close
```
{% include copy-curl.html %}

接著，向 `_settings` 端點傳送請求以更新設定：

```json
PUT /testindex/_settings
{
  "index": {
    "codec": "zstd_no_dict",
    "codec.compression_level": 3
  }
}
```
{% include copy-curl.html %}

最後，重新開啟索引以啟用讀取和寫入操作：

```json
POST /testindex/_open
```
{% include copy-curl.html %}

如需更新設定的詳細資訊（包括支援的查詢參數），請參閱[更新設定]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)。

## 更新動態索引設定

您可以隨時透過 API 更新動態索引設定。例如，若要更新重新整理間隔，請使用下列請求：

```json
PUT /testindex/_settings
{
  "index": {
    "refresh_interval": "2s"
  }
}
```
{% include copy-curl.html %}

如需更新設定的詳細資訊（包括支援的查詢參數），請參閱[更新設定]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)。

## 靜態索引設定

靜態索引設定是只能在已關閉的索引上更新的設定。部分靜態索引設定為 _最終_ 設定。您只能在建立索引時指定最終設定，之後即使在已關閉的索引上也無法更新。

OpenSearch 支援下列靜態索引設定：

- `index.number_of_shards`（最終，整數）：索引中的主要分片數量。預設為 1。

- `index.number_of_routing_shards`（靜態，整數）：用於分割索引的路由分片數量。

- `index.shard.check_on_startup`（靜態，布林值）：是否應檢查索引的分片是否損毀。可用選項為 `false`（不檢查損毀）、`checksum`（檢查實體損毀）以及 `true`（同時檢查實體和邏輯損毀）。預設為 `false`。

- `index.codec`（靜態，字串）：決定索引的儲存欄位 (stored fields) 如何壓縮並儲存於磁碟。此設定會影響索引分片的大小以及索引操作的效能。

    有效值為：

    - `default`
    - `best_compression`
    - `zstd`（OpenSearch 2.9 及更新版本）
    - `zstd_no_dict`（OpenSearch 2.9 及更新版本）
    - `qat_lz4`（OpenSearch 2.14 及更新版本，於支援的系統上）
    - `qat_deflate`（OpenSearch 2.14 及更新版本，於支援的系統上）
    - `qat_zstd`（OpenSearch 2.19.3 及更新版本，於支援的系統上）

對於 `zstd`、`zstd_no_dict`、`qat_lz4`、`qat_deflate` 和 `qat_zstd`，您可以在 `index.codec.compression_level` 設定中指定壓縮等級。如需詳細資訊，請參閱[索引編解碼器設定]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/)。選用。預設為 `default`。

- `index.codec.compression_level`（靜態，整數）：壓縮等級設定可在壓縮比與速度之間取得平衡。壓縮等級越高，壓縮比就越高（儲存空間越小），但壓縮和解壓縮速度較慢，會導致較高的索引編製和搜尋延遲。只有在下列情況下才能指定此設定：在 OpenSearch 2.9 及更新版本中，`index.codec` 設為 `zstd` 或 `zstd_no_dict`；在 OpenSearch 2.14 及更新版本中，設為 `qat_lz4` 或 `qat_deflate`；或在 OpenSearch 2.19.3 及更新版本中，設為 `qat_zstd`。有效值為 `[1, 6]` 範圍內的整數。如需詳細資訊，請參閱[索引編解碼器設定]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/)。選用。預設為 `3`。

- `index.routing_partition_size`（靜態，整數）：自訂路由值可對應到的分片數量。路由會將值重新配置到一部分分片，而非單一分片，藉此協助改善不平衡的叢集。若要啟用路由，請將此值設為大於 1 但小於 `index.number_of_shards`。預設為 1。

<p id="index-sort-settings"></p>

- `index.sort.field`（最終，字串）：指定在索引時用於排序文件的欄位。預設排序順序為 `asc`（遞增）。若要變更順序，請設定 `index.sort.order` 參數。

- `index.sort.order`（最終，字串）：指定在索引時的文件排序順序。有效值為 `asc`（遞增）和 `desc`（遞減）。預設為 `asc`。此設定需要同時設定 `index.sort.field`。

- `index.sort.mode`（最終，字串）：控制排序時如何處理多值欄位。有效值為 `min`（使用最小值）和 `max`（使用最大值）。

- `index.sort.missing`（最終，字串）：決定如何處理缺少排序欄位的文件。有效值為 `_last`（將沒有該欄位的文件放在最後）和 `_first`（將沒有該欄位的文件放在開頭）。

- `index.load_fixed_bitset_filters_eagerly`（靜態，布林值）：OpenSearch 是否應預先載入快取的篩選條件。可用選項為 `true` 和 `false`。預設為 `true`。

- `index.queries.cache.enabled`（靜態，布林值）：為索引啟用或停用查詢快取。查詢快取會在每個資料節點上儲存常用篩選條件的結果。若要設定查詢快取的大小，請使用節點層級的 [`indices.queries.cache.size`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/) 設定。預設為 `true`。

- `index.query.parse.allow_unmapped_fields`（靜態，布林值）：允許在查詢剖析中使用未對應的欄位。預設為 `true`。

- `index.query_string.lenient`（靜態，布林值）：為查詢字串啟用寬鬆剖析。預設為 `false`。

- `index.store.type`（靜態，字串）：OpenSearch 用來在磁碟上儲存和讀取索引分片資料的檔案系統實作。有效值為：

    - `fs`：OpenSearch 會依作業環境選取實作。在允許記憶體映射的 64 位元系統上會使用 `hybridfs`，否則使用 `niofs`。
    - `hybridfs`：使用記憶體映射讀取大多數索引檔案，並使用 Java NIO 讀取 [`index.store.hybrid.nio.extensions`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/) 設定中列出的檔案類型。
    - `mmapfs`：使用記憶體映射讀取所有索引檔案。記憶體映射使用的虛擬位址空間與檔案大小成正比，因此請確認作業系統允許足夠的記憶體映射區域。
    - `niofs`：使用 Java NIO 讀取所有索引檔案，不使用記憶體映射。

    如果已使用 [`node.store.allow_mmap`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/configuration-system/) 設定停用記憶體映射，OpenSearch 會拒絕 `hybridfs` 和 `mmapfs` 值。預設為 `fs`。

- `index.store.stats_refresh_interval`（靜態，時間單位）：索引儲存統計資料的重新整理間隔。預設為 `10s`。

- `index.check_pending_flush.enabled`（靜態，布林值）：此設定控制 Apache Lucene 的 `checkPendingFlushOnUpdate` 索引寫入器設定，該設定指定索引執行緒是否應在更新時檢查待處理的排清 (flush)，以便將索引緩衝區排清至磁碟。預設為 `true`。

- `index.use_compound_file`（靜態，布林值）：此設定控制 Apache Lucene 的 `useCompoundFile` 索引寫入器設定，該設定指定新寫入的區段檔案是否會封裝成複合檔案。預設為 `true`。

- `index.append_only.enabled`（最終，布林值）：設為 `true` 可防止對索引中的文件進行任何更新。預設為 `false`。

- `index.derived_source.enabled`（最終，布林值）：設為 `true` 可在不明確儲存 `_source` 欄位的情況下動態產生來源，進而最佳化儲存空間。預設為 `false`。如需詳細資訊，請參閱[衍生來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source)。

- `index.mapping.ignore_malformed`（靜態，布林值）：控制在文件剖析期間是否忽略格式錯誤的欄位。啟用時，含有格式錯誤欄位值的文件會成功編製索引，格式錯誤的欄位會依欄位類型被忽略或設為 null。停用時，含有格式錯誤欄位的文件會被拒絕。此設定提供可在欄位層級覆寫的預設行為。預設為 `false`。

- `index.soft_deletes.enabled`（最終，布林值）：為索引啟用軟刪除。啟用時，已刪除的文件會被標記為已刪除，而非立即移除，進而提升復原和複寫效能。此設定對 OpenSearch 2.0+ 索引而言是必要的，且對舊版索引預設為啟用。一旦設定，就無法在建立索引後變更此設定。預設為 `true`。

- `index.store.preload`（靜態，清單）：指定開啟索引時應預先載入檔案系統快取的副檔名。此設定僅適用於 `mmap` 目錄實作，並提供盡力而為的快取。預先載入檔案可減少磁碟 I/O 以提升搜尋效能，但會耗用更多記憶體。常見的副檔名包括 `nvd`（norms）、`dvd`（doc values）和 `tim`（terms index）。預設為 `[]`（空清單）。

- `index.replication.type`（最終，字串）：定義索引使用的複寫策略。有效值為：
  - `DOCUMENT`：傳統的文件型複寫，會複寫個別文件
  - `SEGMENT`：區段型複寫，可提升效能並降低網路負擔
  此設定必須在建立索引時設定，之後無法變更。預設為 `DOCUMENT`。

<p id="merge-policy"></p>

- `index.merge.policy`（靜態，字串）：選取控制 Lucene 區段如何合併的合併原則。有效值為 `tiered`、`log_byte_size` 和 `default`。對於標準索引，`default` 值會解析為 `tiered`。對於時間序列索引（OpenSearch 會依是否存在 `@timestamp` 欄位來識別），`default` 會解析為節點層級 `indices.time_series_index.default_index_merge_policy` 設定所指定的原則。預設為 `default`。對於時間序列資料（例如記錄事件），我們建議使用 `log_byte_size`，它可以提升對 `@timestamp` 欄位進行範圍查詢的查詢效能。若要設定所選的原則，請使用[合併設定](#merge-settings)。

## 動態索引設定

動態索引設定是您可以隨時更新的設定。

OpenSearch 支援下列動態索引設定：

- `index.codec.qatmode`（動態，字串）：用於 `qat_lz4`、`qat_deflate` 和 `qat_zstd` 壓縮編解碼器的硬體加速模式。有效值為 `auto` 和 `hardware`。如需詳細資訊，請參閱[索引編解碼器設定]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/)。選用。預設為 `auto`（建議的設定）。

- `index.hidden`（動態，布林值）：索引是否應隱藏。包含萬用字元的查詢不會傳回隱藏索引。可用選項為 `true` 和 `false`。預設為 `false`。

- `index.soft_deletes.retention_lease.period`（動態，時間單位）：保留分片操作歷程記錄的最長時間。預設為 `12h`。

- `index.bulk.adaptive_shard_selection.enabled`（動態，布林值）：設為 `true` 可為大量操作啟用自適應分片選擇，以便為僅附加 (append-only) 索引選擇單一分片。預設為 `false`。如需詳細資訊，請參閱[大量編製索引的自適應分片選擇]({{site.url}}{{site.baseurl}}/im-plugin/append-only-index/#adaptive-shard-selection-for-bulk-indexing)。

- `index.number_of_replicas`（動態，整數）：每個主要分片應具有的副本分片數量。例如，若您有 4 個主要分片並將 `index.number_of_replicas` 設為 3，則索引有 12 個副本分片。若未設定，預設為 `cluster.default_number_of_replicas`（其預設值為 `1`）。

- `index.number_of_search_replicas`（動態，整數）：每個主要分片應具有的搜尋副本分片數量。例如，若您有 4 個主要分片並將 `index.number_of_search_replicas` 設為 3，則索引有 12 個搜尋副本分片。預設為 `0`。

- `index.auto_expand_replicas`（動態，字串）：叢集是否應根據資料節點數量自動新增副本分片。請指定下限與上限（例如 0--9），或以 `all` 作為上限。例如，若您有 5 個資料節點並將 `index.auto_expand_replicas` 設為 0--3，則叢集不會自動新增另一個副本分片。但若您將此值設為 `0-all` 並再新增 2 個節點，總計 7 個，叢集將擴充為 6 個副本分片。預設為停用。

- `index.auto_expand_search_replicas`（動態，字串）：控制叢集是否根據可用搜尋節點的數量，自動調整搜尋副本分片的數量。請將值指定為具有下限與上限的範圍，例如 `0-3` 或 `0-all`。若您未指定值，則此功能為停用。

   例如，若您有 5 個資料節點並將 `index.auto_expand_search_replicas` 設為 `0-3`，索引最多可有 3 個搜尋副本，且叢集不會自動新增另一個搜尋副本分片。但若您將 `index.auto_expand_search_replicas` 設為 `0-all` 並再新增 2 個節點，總計 7 個，叢集將擴充為 7 個搜尋副本分片。此設定預設為停用。

- `index.blocks.write`（動態，布林值）：指定索引是否為唯讀。設為 `true` 會封鎖所有寫入請求，並使索引成為唯讀。預設為 `false`。

- `index.search.idle.after`（動態，時間單位）：分片在進入閒置狀態前等待搜尋或 get 請求的時間。預設為 `30s`。

- `index.search.default_pipeline`（動態，字串）：搜尋索引時若未明確設定管線，所使用的搜尋管線名稱。若已設定預設管線但該管線不存在，則索引請求會失敗。使用管線名稱 `_none` 可指定不使用預設搜尋管線。如需詳細資訊，請參閱[預設搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/#default-search-pipeline)。

- `index.refresh_interval`（動態，時間單位）：索引重新整理的頻率；重新整理會發布索引最近的變更，使其可供搜尋。可設為 `-1` 以停用重新整理。預設為 `1s`。

   若您未明確設定此設定，在 `index.search.idle.after` 所指定的期間內未收到搜尋請求的分片，會停止在背景重新整理，直到下一個搜尋請求送達為止。這可為未被搜尋的索引最佳化大量編製索引作業。若要不論搜尋流量為何都依固定排程重新整理，請明確將 `index.refresh_interval` 設為 `1s`。如需詳細資訊，請參閱[重新整理間隔]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/#refresh-interval)。

- `index.max_result_window`（動態，整數）：搜尋索引時 `from` + `size` 的最大值。`from` 是開始搜尋的起始索引，`size` 是要傳回的結果數量。預設為 10000。

- `index.max_inner_result_window`（動態，整數）：`from` + `size` 的最大值，用於指定查詢期間傳回的巢狀搜尋命中數，以及彙總的最相關文件數。`from` 是開始搜尋的起始索引，`size` 是要傳回的前幾名命中數。預設為 100。

- `index.max_rescore_window`（動態，整數）：對索引發出之重新評分請求的 `window_size` 最大值。重新評分請求會重新排序索引的文件並傳回新的分數，新分數可能更加精確。預設與 `index.max_inner_result_window` 相同，或預設為 10000。

- `index.max_docvalue_fields_search`（動態，整數）：查詢中允許的 `docvalue_fields` 最大數量。預設為 100。

- `index.max_script_fields`（動態，整數）：查詢中允許的 `script_fields` 最大數量。預設為 32。

- `index.max_ngram_diff`（動態，整數）：`NGramTokenizer` 和 `NGramTokenFilter` 的 `min_gram` 與 `max_gram` 值之間的最大差異。預設為 1。

- `index.max_shingle_diff`（動態，整數）：要輸入 `shingle` 詞元篩選器的 `max_shingle_size` 與 `min_shingle_size` 之間的最大差異。預設為 3。

- `index.max_refresh_listeners`（動態，整數）：每個分片允許擁有的重新整理接聽程式最大數量。

- `index.analyze.max_token_count`（動態，整數）：`_analyze` API 操作可傳回的詞元最大數量。預設為 10000。

- `index.highlight.max_analyzed_offset`（動態，整數）：醒目提示請求可分析的字元數。預設為 1000000。

- `index.max_terms_count`（動態，整數）：terms 查詢可接受的詞彙最大數量。預設為 65536。

- `index.max_regex_length`（動態，整數）：regexp 查詢中規則運算式的最大字元長度。預設為 1000。

- `index.query.default_field`（動態，清單）：當參數中未指定欄位時，OpenSearch 在查詢中使用的欄位或欄位清單。

- `index.query.max_nested_depth`（動態，整數）：`nested` 查詢的最大巢狀層級數。預設為 `20`。最小值為 `1`（單一 `nested` 查詢）。

- `index.requests.cache.enable`（動態，布林值）：啟用或停用索引請求快取。預設為 `true`。如需詳細資訊，請參閱[索引請求快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)。

- `index.routing.allocation.enable`（動態，字串）：指定索引分片配置的選項。可用選項為 `all`（允許配置所有分片）、`primaries`（僅允許配置主要分片）、`new_primaries`（僅允許配置新的主要分片）以及 `none`（不允許配置）。預設為 `all`。

- `index.unassigned.node_left.delayed_timeout`（動態，時間單位）：設定 OpenSearch 在配置因節點離開叢集而變成未指派的副本分片之前，所等待的時間。此設定會覆寫叢集層級的 `cluster.routing.allocation.unassigned.node_left.delayed_timeout` 設定。若兩個設定皆未設定，預設為 `1m`。設為 `0` 可停用索引的延遲配置。

- `index.priority`（動態，整數）：OpenSearch 配置未指派分片時（例如叢集重新啟動後）索引的優先順序。OpenSearch 會先配置系統索引的分片，接著先配置 `index.priority` 較高之索引的分片，再配置較低者的分片。優先順序相同的索引會依建立日期配置（最新者優先），再依索引名稱配置。必須為 `0` 或更大。預設為 `1`。

- `index.routing.rebalance.enable`（動態，字串）：啟用索引的分片重新平衡。可用選項為 `all`（允許重新平衡所有分片）、`primaries`（僅允許重新平衡主要分片）、`replicas`（僅允許重新平衡副本）以及 `none`（不允許重新平衡）。預設為 `all`。

- `index.gc_deletes`（動態，時間單位）：保留已刪除文件版本號碼的時間。預設為 `60s`。

- `index.default_pipeline`（動態，字串）：索引的預設匯入節點管線。若已設定預設管線但該管線不存在，則索引請求會失敗。管線名稱 `_none` 表示索引沒有資料匯入管線。

- `index.final_pipeline`（動態，字串）：索引的最終匯入節點管線。若已設定最終管線但該管線不存在，則索引請求會失敗。管線名稱 `_none` 表示索引沒有資料匯入管線。

- `index.optimize_doc_id_lookup.fuzzy_set.enabled`（動態，布林值）：此設定控制是否應啟用 `fuzzy_set`，以透過額外的資料結構（在此情況下為 Bloom filter 資料結構）最佳化索引或搜尋呼叫中的文件 ID 查詢。啟用此設定會建立新的資料結構 (Bloom filter)，藉此提升依賴文件 ID 的 upsert 與搜尋操作的效能。Bloom filter 可透過更快速的堆積外查詢，處理否定情況（亦即 ID 不存在於現有索引中）。請注意，建立 Bloom filter 需要在編製索引期間使用額外的堆積記憶體。預設為 `false`。

- `index.optimize_doc_id_lookup.fuzzy_set.false_positive_probability`（動態，double）：設定底層 `fuzzy_set`（亦即 Bloom filter）的偽陽性機率。較低的偽陽性機率可確保 upsert 與 get 操作有較高的輸送量，但會增加儲存空間與記憶體用量。允許值範圍介於 `0.01` 與 `0.50` 之間。預設為 `0.20`。

- `index.routing.allocation.total_shards_per_node`（動態，整數）：單一索引中可配置到單一節點的主要分片與副本分片合計總數上限。預設為 `-1`（無限制）。透過限制每個節點的分片數量，有助於控制各索引在節點之間的分片分布。請謹慎使用，因為若節點達到其設定的上限，此索引的分片可能會維持未配置狀態。

- `index.routing.allocation.total_primary_shards_per_node`（動態，整數）：單一索引中可配置到單一節點的主要分片數量上限。此設定僅適用於遠端支援 (remote-backed) 叢集。預設為 `-1`（無限制）。透過限制每個節點的主要分片數量，有助於控制各索引在節點之間的主要分片分布。請謹慎使用，因為若節點達到其設定的上限，此索引的主要分片可能會維持未配置狀態。

- `index.derived_source.translog.enabled`（動態，布林值）：控制對於已啟用衍生來源的索引，如何從 translog 讀取文件。預設為 `index.derived_source.enabled` 的值。如需詳細資訊，請參閱[衍生來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source)。

- `index.flush_after_merge`（動態，位元組單位）：合併作業後觸發排清 (flush) 的大小（以位元組為單位）。預設為 `512MB`。

- `index.max_slices_per_pit`（動態，整數）：每個時間點 (point-in-time) 搜尋的最大切片數。預設為 `1024`。

- `index.unreferenced_file_cleanup.enabled`（動態，布林值）：啟用清除未被參照的索引檔案。預設為 `true`。

- `index.warmer.enabled`（動態，布林值）：啟用索引預熱器 (index warmer) 功能。預設為 `true`。

- `index.allocation.max_retries`（動態，整數）：放棄之前可重試分配分片的最大次數。當分片因資源限制或其他問題而無法分配時，此設定可防止無限的分配重試迴圈。預設為 `5`。範圍為 `0` 至 `Integer.MAX_VALUE`。

- `index.max_adjacency_matrix_filters`（動態，整數）：彙總中允許的鄰接矩陣篩選條件最大數量。鄰接矩陣彙總會分析不同篩選條件之間的關係。較高的值可進行更複雜的關係分析，但會耗用更多記憶體。預設為 `100`。最小值為 `2`。

- `index.max_slices_per_scroll`（動態，整數）：此索引的每個捲動 (scroll) 請求所允許的最大切片數。切片可讓捲動作業在多個切片間平行處理，以提升效能。較高的值可提高平行化程度，但會耗用更多資源。預設為 `1024`。最小值為 `1`。

- `index.optimize_auto_generated_id`（動態，布林值）：啟用針對自動產生 ID 之文件的最佳化。啟用後，對於使用自動產生的文件 ID（而非自訂 ID）的文件，OpenSearch 可最佳化其編製索引效能。此最佳化可能不會立即生效，且取決於引擎狀態。預設為 `true`。

- `index.translog.generation_threshold_size`（動態，位元組單位）：觸發建立新 translog 世代的大小閾值。當目前的 translog 世代達到此大小時，OpenSearch 會建立新的世代檔案。較大的值可減少世代輪替的頻率，從而提升編製索引效能，但可能會增加復原時間。預設為 `64MB`。最小值為 `64KB`。

- `index.translog.durability`（動態，字串）：控制 translog 何時以 fsync 寫入磁碟並提交。有效值為 `request` 和 `async`。設定為 `request` 時，OpenSearch 會在確認索引、刪除、更新或大量 (bulk) 請求之前，於主要分片及每個已分配的副本上對 translog 執行 fsync 並提交，因此每筆已確認的寫入在節點當機後都能保留。設定為 `async` 時，OpenSearch 會依 `index.translog.sync_interval` 設定的間隔在背景執行 fsync 並提交，這可降低編製索引的額外負擔，但若節點故障，自上次提交以來所有已確認的寫入都會遺失。值不區分大小寫。預設為 `request`。

- `index.translog.sync_interval`（動態，時間單位）：translog 以 fsync 寫入磁碟並提交的頻率。較頻繁的同步可提供更好的持久性保證，但可能影響編製索引效能。較不頻繁的同步可提升效能，但會增加故障期間資料遺失的風險。預設為 `5s`。最小值為 `100ms`。

- `index.translog.flush_threshold_size`（動態，位元組單位）：尚未提交至 Lucene 的 translog 作業總大小上限。當 translog 達到此大小時，OpenSearch 會排清索引，藉此建立新的 Lucene 提交點並開始新的 translog 世代。較小的值可縮短復原時間，因為需要重新執行的作業較少，但會更頻繁地觸發排清。預設為 `512mb`。最小值為 `56b`。

- `index.translog.retention.age`（動態，時間單位）：為以作業為基礎的對等復原 (peer recovery) 而保留的 translog 檔案最長存留時間。存留時間超過此設定的 translog 檔案會在 translog 清理期間刪除。此設定僅適用於已停用軟刪除 (soft delete) 的索引。由於在 OpenSearch 2.0 及更新版本中建立的所有索引都必須使用軟刪除，因此此設定對目前的索引沒有作用。預設為 `-1`（停用保留）。

- `index.translog.retention.size`（動態，位元組單位）：為以作業為基礎的對等復原而保留的 translog 檔案總大小上限。當總大小超過此閾值時，較舊的檔案會在清理期間刪除。與 `index.translog.retention.age` 相同，此設定僅適用於已停用軟刪除的索引，因此對 OpenSearch 2.0 及更新版本中建立的索引沒有作用。預設為 `-1`（停用保留）。

- `index.soft_deletes.retention.operations`（動態，long）：索引中保留的軟刪除作業最大數量。軟刪除會將文件標記為已刪除，而非立即移除，藉此實現有效率的複寫和時間點復原。此設定控制在軟刪除作業符合清理條件之前要保留多少筆。預設為 `0`（無限制保留）。

- `index.remote_store.translog.keep_extra_gen`（動態，整數）：在復原所需的最低數量之外，於遠端儲存區額外保留的 translog 世代數。較高的值可提供更多復原選項，但會耗用更多儲存空間。此設定有助於在遠端儲存區組態中平衡儲存成本與復原彈性。預設為 `0`。

- `index.remote_store.translog.buffer_interval`（動態，時間單位）：translog 資料在上傳至遠端儲存區之前的緩衝間隔。較頻繁的上傳可提供更好的持久性，但可能影響效能。此設定會與叢集層級的 `cluster.remote_store.translog.buffer_interval` 設定搭配運作，且以索引層級的設定為優先。預設值繼承自叢集設定。

- `index.blocks.read_only`（動態，布林值）：設定為 `true` 時，會封鎖所有寫入作業（包括編製索引、更新和刪除），使索引成為唯讀。搜尋和取得 (get) 等讀取作業仍可正常運作。此設定適用於在維護或疑難排解期間暫時防止寫入。預設為 `false`。

- `index.routing.allocation.require.temp`（動態，字串）：要求此索引的分片只能分配至具有指定溫度屬性的節點。此設定用於冷熱 (hot-warm) 架構，在此架構中，不同類型的節點處理不同溫度的資料。值應符合節點屬性，例如 `hot`、`warm` 或 `cold`。無預設值；未設定時，分片可分配至任何符合資格的節點。

<p id="periodic-flush-interval"> </p>

- `index.periodic_flush_interval`（動態，時間單位）：依設定的間隔定期觸發排清，將所有記憶體內的作業儲存至磁碟上的區段 (segment)。OpenSearch 會根據交易記錄檔大小等條件，自動在背景執行排清作業。預設為 `-1`，表示停用定期排清。對於拉取式匯入 (pull-based ingestion) 索引，預設為 `10m`。請參閱[拉取式匯入]({{site.url}}{{site.baseurl}}/api-reference/document-apis/pull-based-ingestion/)。如果您的工作負載需要可預測、以時間為基礎的排清間隔，可以設定此設定。

### 合併設定

合併設定控制 Lucene 區段的合併方式。用於選取合併策略的 `index.merge.policy` 設定為靜態設定，其他所有合併設定皆為動態設定。如需選取合併策略的詳細資訊，請參閱 [`index.merge.policy`](#merge-policy)。

#### 分層合併策略設定

使用 `tiered` 合併策略（預設）時，下列設定控制合併行為：

- `index.merge.policy.max_merge_at_once`（動態，整數）：設定一般合併作業期間一次合併的最大區段數。較高的值可以減少合併的總次數，但每次合併作業需要更多記憶體與 I/O 資源。預設值為 `30`。最小值為 `2`。

- `index.merge.policy.segments_per_tier`（動態，double）：控制分層合併策略中每一層允許的區段數。較小的值會產生更多合併但區段數較少，這可以提升搜尋效能，代價是增加編製索引的額外負擔。預設值為 `10.0`。最小值為 `2.0`。

- `index.merge.policy.floor_segment`（動態，位元組單位）：設定合併策略可區分的最小區段大小。小於此值的區段會被向上進位至此值，並在策略選取合併候選項目時視為大小相同，因此最小的區段會被分組並提早合併，而不會累積成一長串的微小區段。較大的值會更積極地合併小區段，從而降低區段總數，但會增加合併工作量。此值必須大於 `0`。預設值為 `16mb`。

- `index.merge.policy.max_merged_segment`（動態，位元組單位）：設定背景合併所產生區段的最大大小。當預估的合併結果會超過此大小時，合併策略會停止合併該組區段，因此大於此值的區段只會由強制合併產生。較小的值可讓個別合併的時間較短，但會在索引中留下更多區段。預設值為 `5gb`。

- `index.merge.policy.deletes_pct_allowed`（動態，double）：設定索引在合併策略開始專門為回收空間而合併區段之前，允許累積的已刪除文件百分比。較低的值可以更快回收磁碟空間，但會增加合併工作量。預設值為 `20.0`。有效值範圍為 `5.0` 至 `50.0`。

- `index.merge.policy.expunge_deletes_allowed`（動態，double）：設定區段必須包含的已刪除文件百分比，達到此百分比後，將 `only_expunge_deletes` 設為 `true` 的強制合併才會重寫該區段。預設值為 `10.0`。有效值範圍為 `0.0` 至 `100.0`。如需詳細資訊，請參閱 [Force Merge API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/)。

- `index.merge.policy.reclaim_deletes_weight`（動態，double）：已淘汰且不再套用。OpenSearch 會接受並儲存此值，但不會將其傳遞給合併策略，因此變更此值不會產生任何作用。請使用 `index.merge.policy.deletes_pct_allowed` 控制何時回收已刪除的文件。預設值為 `2.0`。最小值為 `0.0`。

#### log_byte_size 合併策略設定

使用 `log_byte_size` 合併策略時，下列設定控制合併行為：

- `index.merge.log_byte_size_policy.merge_factor`（動態，整數）：控制一般合併作業期間一次合併的區段數。較高的值會產生數量較少但較大的區段，這可以提升搜尋效能，但合併期間會使用更多資源。預設值為 `10`。最小值為 `2`。

- `index.merge.log_byte_size_policy.min_merge`（動態，位元組單位）：設定區段合併的最小大小門檻。小於此大小的區段會被更積極地合併。較小的值會產生較少的小區段，但合併作業會較多。預設值為 `16mb`。

- `index.merge.log_byte_size_policy.max_merge_segment`（動態，位元組單位）：控制一般合併作業期間所建立區段的最大大小。較大的區段可提升查詢效能，但需要更多記憶體，並可能增加合併時間。預設值為 `5gb`。

- `index.merge.log_byte_size_policy.max_merge_segment_forced_merge`（動態，位元組單位）：設定執行強制合併作業（例如索引最佳化期間）時的最大區段大小。這可讓強制合併建立比一般合併更大的區段。預設值為無限制。

- `index.merge.log_byte_size_policy.max_merged_docs`（動態，整數）：設定單一區段可包含的最大文件數。合併策略會略過任何會產生超過此數量之區段的合併，藉此以文件數而非位元組數限制區段大小。預設值為 `2147483647`，實際上不限制每個區段的文件數。

- `index.merge.log_byte_size_policy.no_cfs_ratio`（動態，double）：設定區段在仍能以 Lucene 複合檔案格式寫入的情況下，可占索引總大小的最大比例。複合檔案格式會將區段的檔案打包成單一檔案，以減少開啟的檔案控制碼數量。超過索引此比例的區段會寫入為個別檔案。將此值設為 `1.0`（或 `true`）可讓所有區段使用複合格式，設為 `0.0`（或 `false`）則停用複合格式。預設值為 `0.1`。有效值範圍為 `0.0` 至 `1.0`。

#### 合併排程器設定

下列設定控制合併排程器，合併排程器決定合併作業的執行方式：

- `index.merge.scheduler.max_thread_count`（動態，整數）：設定單一分片上可同時進行合併的最大執行緒數。此設定控制每個分片內合併作業的並行程度。在配備 SSD 與多個 CPU 核心的系統上，較高的值可以提升合併效能，但可能會增加資源使用量。如果您的索引位於傳統旋轉式磁碟上，請將此值降低為 1。預設值為 `Math.max(1, Math.min(4, node.processors / 2))`，適用於固態硬碟。最小值為 `1`。

- `index.merge.scheduler.auto_throttle`（動態，布林值）：啟用合併作業的自動節流，以防止合併作業使系統負荷過重。啟用時，OpenSearch 會根據傳入的編製索引負載自動調整合併 I/O 速率。預設值為 `true`。

- `index.merge_on_flush.enabled`（動態，布林值）：此設定控制 Apache Lucene 的 merge-on-refresh 功能，該功能旨在透過_於重新整理時_（以 OpenSearch 的用語來說，即_於排清時_）執行合併來減少區段數。預設值為 `true`。

- `index.merge_on_flush.max_full_flush_merge_wait_time`（動態，時間單位）：此設定設定啟用 `index.merge_on_flush.enabled` 時等待合併的時間長度。預設值為 `10s`。

- `index.merge_on_flush.policy`（動態，字串）：此設定控制啟用 `index.merge_on_flush.enabled` 時應使用的合併策略。預設值為 `default`。

### 慢速記錄檔設定

OpenSearch 支援下列動態慢速記錄檔設定，用於監控搜尋與編製索引的效能。

#### 編製索引慢速記錄檔設定

- `index.indexing.slowlog.threshold.index.warn`（動態，時間單位）：設定在 WARN 層級記錄緩慢編製索引作業的時間門檻。耗時超過此門檻的編製索引作業會記錄為警告。預設值為 `-1`（停用）。

- `index.indexing.slowlog.threshold.index.info`（動態，時間單位）：設定在 INFO 層級記錄緩慢編製索引作業的時間門檻。耗時超過此門檻的編製索引作業會被記錄以供參考。預設值為 `-1`（停用）。

- `index.indexing.slowlog.threshold.index.debug`（動態，時間單位）：設定在 DEBUG 層級記錄緩慢編製索引作業的時間門檻。這會提供詳細的偵錯資訊，以供分析編製索引效能。預設值為 `-1`（停用）。

- `index.indexing.slowlog.threshold.index.trace`（動態，時間單位）：設定在 TRACE 層級記錄緩慢編製索引作業的時間門檻。這會提供最詳細的記錄，以供排解編製索引效能問題。預設值為 `-1`（停用）。

#### 搜尋慢速記錄檔設定

- `index.search.slowlog.threshold.query.warn`（動態，時間單位）：設定以 WARN 層級記錄慢速搜尋查詢作業的時間閾值。耗時超過此閾值的查詢作業會記錄為警告。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.query.info`（動態，時間單位）：設定以 INFO 層級記錄慢速搜尋查詢作業的時間閾值。耗時超過此閾值的查詢作業會記錄下來以供參考。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.query.debug`（動態，時間單位）：設定以 DEBUG 層級記錄慢速搜尋查詢作業的時間閾值。這會提供詳細的偵錯資訊，以便分析查詢效能。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.query.trace`（動態，時間單位）：設定以 TRACE 層級記錄慢速搜尋查詢作業的時間閾值。這會提供最詳細的記錄，以便疑難排解查詢效能問題。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.fetch.warn`（動態，時間單位）：設定以 WARN 層級記錄慢速搜尋擷取作業的時間閾值。耗時超過此閾值的擷取作業會記錄為警告。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.fetch.info`（動態，時間單位）：設定以 INFO 層級記錄慢速搜尋擷取作業的時間閾值。耗時超過此閾值的擷取作業會記錄下來以供參考。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.fetch.debug`（動態，時間單位）：設定以 DEBUG 層級記錄慢速搜尋擷取作業的時間閾值。這會提供詳細的偵錯資訊，以便分析擷取效能。預設為 `-1`（停用）。

- `index.search.slowlog.threshold.fetch.trace`（動態，時間單位）：設定以 TRACE 層級記錄慢速搜尋擷取作業的時間閾值。這會提供最詳細的記錄，以便疑難排解擷取效能問題。預設為 `-1`（停用）。

## 相關文件

- [Create Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)
- [Get Index Settings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-settings/)
- [Update Index Settings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)
