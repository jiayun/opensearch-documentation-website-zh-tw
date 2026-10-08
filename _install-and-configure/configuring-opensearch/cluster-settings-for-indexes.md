---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引的叢集設定"
parent: Configuring OpenSearch
nav_order: 60
---

# 索引的叢集設定

下列叢集設定適用於叢集中的所有索引。如需適用於個別索引的設定，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 靜態設定

OpenSearch 支援下列索引的靜態叢集設定：

- `indices.cache.cleanup_interval`（靜態，時間單位）：排程一個週期性的背景工作，依指定的間隔清除快取中已過期的項目。預設為 `1m`（1 分鐘）。如需詳細資訊，請參閱[索引請求快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)。

- `indices.requests.cache.size`（靜態，字串）：快取大小，以堆積大小的百分比表示（例如，若要使用 1% 的堆積，請指定 `1%`）。預設為 `1%`。如需詳細資訊，請參閱[索引請求快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)。

- `indices.analysis.hunspell.dictionary.ignore_case`（靜態，布林值）：控制 Hunspell 字典比對是否針對所有地區設定全域忽略大小寫。啟用時，字典比對將不區分大小寫。此設定可在多個層級進行設定：節點層級（即此設定）、使用 `indices.analysis.hunspell.dictionary.<locale>.ignore_case` 針對個別地區設定（例如 `indices.analysis.hunspell.dictionary.en_US.ignore_case`），或在各字典目錄中的字典專屬 `settings.yml` 檔案中設定。個別地區設定與字典專屬的設定會覆寫全域設定。預設為 `false`。

- `indices.analysis.hunspell.dictionary.lazy`（靜態，布林值）：控制 Hunspell 字典的載入時機。若為 `true`，字典會延遲到實際使用時才載入，可縮短啟動時間，但首次使用時的延遲可能會增加。若為 `false`，節點啟動時會檢查字典目錄並自動載入所有字典。預設為 `false`。

- `indices.analysis.hunspell.dictionary.<locale>.strict_affix_parsing`（靜態，布林值）：控制讀取 Hunspell 詞綴規則檔案時遇到的錯誤是否會引發例外狀況，或是靜默忽略。設為 `true` 時，詞綴檔案中的剖析錯誤會擲回例外狀況並阻止字典載入。設為 `false` 時，會忽略剖析錯誤，字典將繼續載入。您可以將 `<locale>` 取代為特定的地區設定識別碼（例如 `indices.analysis.hunspell.dictionary.en_US.strict_affix_parsing`），針對個別地區設定此設定。預設為 `true`。

- `indices.memory.index_buffer_size`（靜態，字串）：控制節點上所有分片的索引作業所配置的堆積記憶體量。可接受百分比（如 `10%`）或位元組大小值（如 `512mb`）。此緩衝區由所有分片共用，用於在寫入磁碟前批次處理索引作業。預設為總堆積的 `10%`。

- `indices.memory.min_index_buffer_size`（靜態，位元組單位）：當 `indices.memory.index_buffer_size` 以百分比指定時，設定索引緩衝區的絕對最小大小。這可確保在堆積記憶體有限的節點上，索引緩衝區不會變得過小。預設為 `48mb`。

- `indices.memory.max_index_buffer_size`（靜態，位元組單位）：當 `indices.memory.index_buffer_size` 以百分比指定時，設定索引緩衝區的絕對最大大小。這可防止索引緩衝區在大型堆積的節點上耗用過多記憶體。預設為無上限（無限制）。

- `indices.queries.cache.size`（靜態，字串）：控制每個資料節點上查詢快取（篩選器快取）所配置的記憶體大小。查詢快取會儲存常用篩選器的結果，以提升搜尋效能。可接受百分比值（如 `5%`）或確切的位元組值（如 `512mb`）。預設為堆積記憶體的 `10%`。

- `indices.queries.cache.all_segments`（靜態，布林值）：是否在所有區段中快取查詢，或僅在經常存取的區段中快取。

- `indices.queries.cache.count`（靜態，整數）：要快取的查詢數量上限。

- `index.store.hybrid.nio.extensions`（靜態，清單）：**專家設定。**要以 NIO 而非記憶體對應方式載入的 Lucene 副檔名。預設包含常見的副檔名，例如 `segments_N`、`write.lock`、`si` 和 `cfe`。

- `indexing_pressure.memory.limit`（靜態，位元組大小）：控制索引作業的記憶體限制，以防止在大量索引工作負載期間耗盡記憶體。當索引作業超過此閾值時，可能會遭到拒絕或節流，以保護叢集穩定性。可接受百分比值（如堆積的 `10%`）或位元組大小值（如 `512mb`）。預設為總堆積記憶體的 `10%`。

- `indices.query.query_string.allowLeadingWildcard`（靜態，布林值）：控制查詢字串查詢中是否允許前置萬用字元。啟用時，允許 `*term` 或 `?term` 之類的查詢，但由於需要掃描索引中的所有詞彙，可能會影響效能。停用時，會拒絕前置萬用字元查詢，以提升查詢效能。預設為 `true`。

- `indices.query.query_string.analyze_wildcard`（靜態，布林值）：控制查詢字串查詢中的萬用字元詞彙是否使用已設定的分析器進行分析。啟用時，萬用字元查詢會經過分析（斷詞、篩選），可改善比對結果，但可能影響效能。停用時，萬用字元詞彙會維持原樣使用，不經分析。預設為 `false`。

- `indices.time_series_index.default_index_merge_policy`（靜態，字串）：設定整個叢集中時間序列索引的預設合併原則。此設定控制時間序列資料的 Lucene 區段如何合併，可能會大幅影響索引效能與儲存效率。有效值包括 `default`、`tiered` 和 `log_byte_size`。預設為 `default`。

- `cluster.remote_store.translog.path.prefix`（靜態，字串）：控制已啟用遠端儲存的叢集上 translog 資料的固定路徑前置詞。此設定僅在 `cluster.remote_store.index.path.type` 設定為 `HASHED_PREFIX` 或 `HASHED_INFIX` 時適用。預設為空字串 `""`。

- `cluster.remote_store.segments.path.prefix`（靜態，字串）：控制已啟用遠端儲存的叢集上區段資料的固定路徑前置詞。此設定僅在 `cluster.remote_store.index.path.type` 設定為 `HASHED_PREFIX` 或 `HASHED_INFIX` 時適用。預設為空字串 `""`。

- `cluster.snapshot.shard.path.prefix`（靜態，字串）：控制快照分片層級 blob 的固定路徑前置詞。此設定僅在儲存庫的 `shard_path_type` 設定為 `HASHED_PREFIX` 或 `HASHED_INFIX` 時適用。預設為空字串 `""`。

## 動態設定

OpenSearch 支援下列索引的動態叢集設定：

- `action.auto_create_index`（動態，布林值）：若索引尚不存在，則自動建立索引，同時套用所有已設定的索引範本。預設為 `true`。

- `action.destructive_requires_name`（動態，布林值）：若為 `true`，您必須指定索引名稱才能刪除索引。您無法刪除所有索引或使用萬用字元。預設為 `false`。

- `cluster.default.index.refresh_interval`（動態，時間單位）：在未提供 `index.refresh_interval` 設定時，設定重新整理間隔。若您想為叢集中的所有索引設定預設的重新整理間隔，並支援 `searchIdle` 設定，此設定會很有用。您無法將間隔設定為低於 `cluster.minimum.index.refresh_interval` 設定的值。

- `cluster.minimum.index.refresh_interval`（動態，時間單位）：設定最小重新整理間隔，並套用至叢集中的所有索引。`cluster.default.index.refresh_interval` 設定應高於此設定的值。若在建立索引時，`index.refresh_interval` 設定低於所設定的最小值，索引建立將會失敗。

- `cluster.indices.close.enable`（動態，布林值）：允許關閉 OpenSearch 中已開啟的索引。預設為 `true`。

- `indices.recovery.max_bytes_per_sec`（動態，字串）：限制每個節點的輸入與輸出復原流量總和。此設定適用於對等復原與快照復原。預設為 `40mb`。若您將復原流量值設定為小於或等於 `0mb`，將停用速率限制，使復原資料以最高可能速率傳輸。

- `indices.recovery.max_concurrent_file_chunks`（動態，整數）：每次復原作業平行傳送的檔案區塊數量。預設為 `2`。

- `indices.recovery.max_concurrent_operations`（動態，整數）：每次復原平行傳送的作業數量。預設為 `1`。

- `indices.recovery.max_concurrent_remote_store_streams`（動態，整數）：復原遠端儲存索引時，可平行開啟至遠端儲存庫的串流數量。預設為 `20`。

- `indices.replication.max_bytes_per_sec`（動態，字串）：限制每個節點的輸入與輸出複寫流量總和。若組態中未指定值，則會使用 `indices.recovery.max_bytes_per_sec` 設定，其預設為 40 Mb。若您將複寫流量值設定為小於或等於 0 Mb，將停用速率限制，使複寫資料以最高可能速率傳輸。

- `indices.fielddata.cache.size`（動態，字串）：欄位資料快取的大小上限。可指定為絕對值（例如 `8GB`）或節點堆積的百分比（例如 `50%`）。此設定為動態設定。若您未指定此設定，大小上限為 `35%`。此值應小於 `indices.breaker.fielddata.limit`。如需詳細資訊，請參閱[欄位資料斷路器]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/circuit-breaker/#field-data-circuit-breaker-settings)。

- `indices.query.bool.max_clause_count`（動態，整數）：定義可同時搜尋的欄位數與詞彙數乘積的上限。在 OpenSearch 2.16 之前，必須重新啟動叢集才能套用此靜態設定。此設定現已改為動態，現有的搜尋執行緒集區一開始可能仍使用舊的靜態值，因而導致 `TooManyClauses` 例外狀況。新的執行緒集區則會使用更新後的值。預設為 `1024`。

- `cluster.remote_store.index.path.type`（動態，字串）：遠端儲存中所儲存資料的路徑策略。此設定僅對已啟用遠端儲存的叢集有效。此設定支援下列值：
  - `fixed`：以路徑結構 `<repository_base_path>/<index_uuid>/<shard_id>/` 儲存資料。
  - `hashed_prefix`：以路徑結構 `hash(<shard-data-idenitifer>)/<repository_base_path>/<index_uuid>/<shard_id>/` 儲存資料。
  - `hashed_infix`：以路徑結構 `<repository_base_path>/hash(<shard-data-idenitifer>)/<index_uuid>/<shard_id>/` 儲存資料。
  `shard-data-idenitifer` 由 index_uuid、shard_id、資料種類（translog、segments）及資料類型（data、metadata、lock_files）所構成。
  預設為 `fixed`。

- `cluster.remote_store.index.path.hash_algorithm`（動態，字串）：當 `cluster.remote_store.index.path.type` 設為 `hashed_prefix` 或 `hashed_infix` 時，用於產生雜湊值的雜湊函式。此設定僅對已啟用遠端儲存的叢集有效。此設定支援下列值：
  - `fnv_1a_base64`：使用 FNV1a 雜湊函式，並產生 URL 安全的 20 位元 Base64 編碼雜湊值。
  - `fnv_1a_composite_1`：使用 FNV1a 雜湊函式，並產生可在大多數遠端儲存選項中良好擴充的自訂編碼雜湊值。FNV1a 函式會產生 64 位元的值。自訂編碼使用最高有效的 6 個位元建立一個 URL 安全的 Base64 字元，並使用接下來的 14 個位元建立二進位字串。預設值為 `fnv_1a_composite_1`。

- `cluster.remote_store.translog.transfer_timeout`（動態，時間單位）：控制同步至遠端儲存時上傳 translog 與檢查點檔案的逾時值。此設定僅適用於已啟用遠端儲存的叢集。預設值為 `30s`。

- `cluster.remote_store.index.segment_metadata.retention.max_count`（動態，整數）：控制在遠端儲存的區段儲存庫中保留的中繼資料檔案最小數量。低於 `1` 的值會停用刪除過時區段中繼資料檔案的功能。預設值為 `10`。

- `cluster.remote_store.segment.transfer_timeout`（動態，時間單位）：控制在重新整理後，等待所有新區段更新至遠端儲存的最長時間。如果上傳未在指定時間內完成，會擲回 `SegmentUploadFailedException` 錯誤。預設值為 `30m`。最小限制為 `10m`。

- `cluster.default_number_of_replicas`（動態，整數）：控制叢集中索引的預設副本數量。若未設定索引層級的 `index.number_of_replicas` 設定，則預設為此值。預設值為 `1`。
