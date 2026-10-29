---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
nav_order: 90
redirect_from:
  - /search-plugins/knn/settings/
---

# 向量搜尋設定

OpenSearch 支援下列向量搜尋設定。動態設定可透過 [Cluster Settings API]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#updating-cluster-settings-using-the-api) 更新；靜態設定則必須在每個節點的 `opensearch.yml` 中設定。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## k-NN 外掛程式設定

k-NN 外掛程式支援下列設定。

### 叢集設定

下列 k-NN 外掛程式設定適用於叢集層級：

- `knn.algo_param.index_thread_qty`（動態，整數）：用於建立原生程式庫與 Lucene 程式庫（OpenSearch 2.19 版及更新版本）索引的執行緒數。將此值保持較低可降低 k-NN 外掛程式對 CPU 的影響，但也會降低編製索引的效能。有效值為 1--32。對於 CPU 核心數少於 32 的系統，預設值為 `1`；對於 32 個或更多核心的系統，預設值為 `4`。

- `knn.vector_streaming_memory.limit`（動態，百分比或位元組單位）：建立原生程式庫索引時，每批次從 JVM 堆積傳輸至原生記憶體的向量可使用的記憶體上限。每批次的向量數為此上限除以單一向量的大小，最少為一個向量。預設值為 JVM 堆積的 `1%`。

- `knn.cache.item.expiry.enabled`（動態，布林值）：是否從記憶體中移除在指定期間內未被存取的原生程式庫索引。預設值為 `false`。

- `knn.cache.item.expiry.minutes`（動態，時間單位）：原生程式庫索引從記憶體中移除前的閒置時間。僅在 `knn.cache.item.expiry.enabled` 為 `true` 時生效。預設值為 `3h`。

- `knn.circuit_breaker.unset.percentage`（動態，百分比）：斷路器的原生記憶體使用量閾值。記憶體使用量必須低於 `knn.memory.circuit_breaker.limit` 的此百分比，`knn.circuit_breaker.triggered` 才能保持為 `false`。預設值為 `75`。

- `knn.circuit_breaker.triggered`（動態，布林值）：當記憶體使用量超過 `knn.circuit_breaker.unset.percentage` 值時，設為 `true`。預設值為 `false`。

- `knn.memory.circuit_breaker.limit`（動態，百分比或位元組單位）：原生程式庫索引的原生記憶體上限。在預設值下，若機器有 100 GB 記憶體且 JVM 使用 32 GB，則 k-NN 外掛程式會使用剩餘 68 GB 中的 50%（34 GB）。若記憶體使用量超過此值，外掛程式會移除最近最少使用的原生程式庫索引。若要在節點層級設定此上限，請在 `opensearch.yml` 中新增 `node.attr.knn_cb_tier: "<tier-name>"`，並在叢集設定中設定 `knn.memory.circuit_breaker.limit.<tier-name>`。例如，將節點層級定義為 `node.attr.knn_cb_tier: "integ"` 並設定 `knn.memory.circuit_breaker.limit.integ: "80%"`。若已設定節點層級的斷路器上限，節點會使用該上限；若未設定節點專屬值，則使用叢集範圍的設定。預設值為 `50%`。

- `knn.memory.circuit_breaker.enabled`（動態，布林值）：是否啟用 k-NN 記憶體斷路器。預設值為 `true`。

- `knn.model.index.number_of_shards`（動態，整數）：模型系統索引要使用的分片數，該索引是 OpenSearch 中用來儲存近似最近鄰（ANN）搜尋所用模型的索引。預設值為 `1`。

- `knn.model.index.number_of_replicas`（動態，整數）：模型系統索引要使用的副本分片數。在多節點叢集中，請將此值設為至少 `1` 以提升穩定性。預設值為 `1`。

- `knn.model.cache.size.limit`（動態，百分比）：模型快取上限，不得超過 JVM 堆積的 25%。預設值為 `10%`。

- `knn.quantization.cache.size.limit`（動態，百分比或位元組單位）：用於保存[二進位量化]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/binary-quantization/)欄位量化狀態的快取大小上限，OpenSearch 會從每個分段讀取該狀態以量化查詢向量。快取已滿時，會移除最近最少使用的項目。不得超過 JVM 堆積的 10%。變更此設定會清除快取。預設值為 `5%`。

- `knn.quantization.cache.expiry.minutes`（動態，時間單位）：未存取的項目從量化狀態快取中移除前的時間長度。變更此設定會清除快取。預設值為 `60m`。

- `knn.faiss.avx2.disabled`（靜態，布林值）：是否在 x64 架構的機器上停用以 SIMD 為基礎的 `libopensearchknn_faiss_avx2.so` 程式庫，並為 Faiss 引擎載入未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設值為 `false`。如需詳細資訊，請參閱[單指令多資料 (SIMD) 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.faiss.avx512.disabled`（靜態，布林值）：是否在 x64 架構的機器上停用以 SIMD 為基礎的 `libopensearchknn_faiss_avx512.so` 程式庫，並為 Faiss 引擎載入 `libopensearchknn_faiss_avx2.so` 或未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設值為 `false`。如需詳細資訊，請參閱[SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.faiss.avx512_spr.disabled`（靜態，布林值）：是否在 x64 架構的機器上停用以 SIMD 為基礎的 `libopensearchknn_faiss_avx512_spr.so` 程式庫，並為 Faiss 引擎載入 `libopensearchknn_faiss_avx512.so`、`libopensearchknn_faiss_avx2.so` 或未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設值為 `false`。如需詳細資訊，請參閱[SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.dynamic_mapping.enabled`（動態，布林值）：是否啟用 `knn_vector` 欄位的[動態對應]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/#dynamic-mapping)，包括推斷未對應的扁平數值陣列，以及將 `knn_vector` 參照為 `match_mapping_type` 的動態範本。預設值為 `false`。

### 索引設定

索引設定中定義的多個參數目前正處於淘汰程序中。請將這些參數設定在對應中，而不是索引設定裡。在對應中設定的參數會覆寫索引設定中的參數，並允許索引擁有多個帶有不同參數的 `knn_vector` 欄位。

下列 k-NN 外掛程式設定適用於索引層級。有關更新這些設定的資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)：

- `index.knn`（靜態，布林值）：索引是否為其 `knn_vector` 欄位建立原生程式庫索引。若為 `false`，`knn_vector` 欄位會儲存在 doc values 中，但近似 k-NN 搜尋會停用。預設為 `false`。

- `index.knn.algo_param.ef_search`（動態，整數）：搜尋期間使用的最近鄰居動態清單大小（`ef`，或 `efSearch`）。數值越高，搜尋越準確但越慢。此值不得低於查詢的最近鄰居數量 `k`，且可為 `k` 到資料集大小之間的任何值。預設為 `100`。

- `index.knn.advanced.approximate_threshold`（動態，整數）：分段必須包含的向量數量，達到此數量後 OpenSearch 才會為 ANN 搜尋建立專用的資料結構。設為 `-1` 可停用向量資料結構的建立，設為 `0` 則一律建立。預設為 `0`。

- `index.knn.advanced.filtered_exact_search_threshold`（動態，整數）：篩選 ID 的門檻值，當達到此門檻時，OpenSearch 會在篩選式 ANN 搜尋期間切換為精確搜尋。若分段中的篩選 ID 數量低於此值，則會對篩選 ID 執行精確搜尋。預設為 `-1`，表示不套用任何門檻。

- `index.knn.faiss.efficient_filter.disable_exact_search`（動態，布林值）：設為 `true` 時，停用當 Faiss 高效篩選近似最近鄰居 (ANN) 搜尋傳回的結果少於 `k` 筆時所發生的精確搜尋後備機制。預設為 `false`。如需更多資訊，請參閱[停用精確搜尋後備機制]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/efficient-knn-filtering/#disabling-the-exact-search-fallback)。

- `index.knn.disk.vector.shard_level_rescoring_disabled`（動態，布林值）：適用於[重新評分量化結果]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#rescoring-quantized-results-to-full-precision)的搜尋，例如在[磁碟型向量]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/)索引上的搜尋。預設情況下，OpenSearch 會合併分片中所有分段的第一輪結果，僅保留該分片的前幾筆結果，並對這些結果重新評分。保留的結果數量取決於 `k` 與超取樣係數。設為 `true` 時，OpenSearch 會對每個分段的前幾筆第一輪結果重新評分，而不先在分片層級縮減結果，因此會重新評分更多結果。預設為 `false`。

- `index.knn.derived_source.enabled`（靜態，布林值）：防止向量儲存在 `_source` 中，以減少向量索引的磁碟用量。對於將 `index.knn` 設為 `true` 所建立的索引，預設為 `true`；對所有其他索引則為 `false`。

- `index.knn.memory_optimized_search`（靜態，布林值）：在索引上啟用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)。預設為 `false`。

在 OpenSearch 2.11 或更早版本中建立的索引，仍會使用先前的 `ef_construction` 與 `ef_search` 值（`512`）。
{: .note}

當您以 `index.knn` 設為 `true` 建立索引時，k-NN 外掛程式也會調低兩項[分層合併原則設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#tiered-merge-policy-settings)，以減少合併與搜尋之間的 CPU 競爭：它會將 `index.merge.policy.max_merge_at_once` 設為 `10` 而非預設的 `30`，並將 `index.merge.policy.floor_segment` 設為 `2mb` 而非預設的 `16mb`。這兩項設定都是動態的，因此您可以在建立索引後變更它們。

### 遠端索引建置設定

下列設定用於控制[遠端向量索引建置]({{site.url}}{{site.baseurl}}/vector-search/remote-index-build/)。

#### 叢集設定

下列遠端索引建置設定適用於叢集層級：

- `knn.remote_index_build.enabled` (動態，布林值)：為叢集啟用遠端向量索引建置。預設值為 `false`。

- `knn.remote_index_build.repository` (動態，字串)：遠端索引建置器寫入的已註冊儲存庫名稱。沒有預設值；您必須先設定此設定，才能使用遠端索引建置服務。

- `knn.remote_index_build.service.endpoint` (動態，字串)：遠端建置服務的端點 URL。沒有預設值；您必須先設定此設定，才能使用遠端索引建置服務。

- `knn.remote_index_build.poll.interval` (動態，時間單位)：用戶端向遠端建置服務輪詢工作狀態的頻率。預設值為 `5s`。

- `knn.remote_index_build.client.timeout` (動態，時間單位)：等待遠端建置完成的最長時間。如果建置未在此時間內完成，OpenSearch 會改在本機 CPU 上建置索引。預設值為 `60m`。

- `knn.remote_index_build.size.max` (動態，位元組單位)：遠端索引建置服務接受的最大分段大小。請依據您的遠端建置服務實作的限制來設定此設定。預設值為 `0`，表示分段大小沒有上限。

#### 索引設定

下列遠端索引建置設定適用於索引層級。關於更新這些設定的資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)：

- `index.knn.remote_index_build.enabled` (動態，布林值)：為索引啟用遠端索引建置。僅在 `knn.remote_index_build.enabled` 為 `true` 時生效。預設值為 `true`。

- `index.knn.remote_index_build.size.min` (動態，位元組單位)：OpenSearch 使用遠端索引建置服務的最小分段大小。較小的分段會在本機建置。預設值為 `50mb`。

#### 遠端建置驗證

遠端建置服務的使用者名稱與密碼是安全設定，必須依照下列方式在 [OpenSearch keystore]({{site.url}}{{site.baseurl}}/security/configuration/opensearch-keystore/) 中設定：

```bash
./bin/opensearch-keystore add knn.remote_index_build.service.username
./bin/opensearch-keystore add knn.remote_index_build.service.password
```
{% include copy.html %}

您可以使用 [Nodes Reload Secure Settings API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-reload-secure/) 重新載入安全設定，而無需重新啟動節點。

## Neural Search 外掛程式設定

Neural Search 外掛程式支援下列設定。

### 叢集設定

下列 Neural Search 外掛程式設定適用於叢集層級。動態設定會使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#updating-cluster-settings-using-the-api) 更新；靜態設定必須在每個節點上的 `opensearch.yml` 中設定：

- `plugins.neural_search.stats_enabled`（動態，布林值）：啟用 [Neural Search Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#stats)。預設為 `false`。
- `plugins.neural_search.circuit_breaker.limit`（動態，百分比）：指定[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)斷路器的 JVM 記憶體上限。此上限僅限制 Lucene 引擎使用的 JVM 堆積快取，對依賴作業系統頁面快取的原生引擎沒有影響。預設為 JVM 堆積的 `10%`。如需詳細資訊，請參閱[記憶體與快取設定]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#memory-and-caching-settings)。
- `plugins.neural_search.circuit_breaker.overhead`（動態，浮點數）：用於調整[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)記憶體用量估算值的乘數。數值越高，記憶體估算值越保守。與 `plugins.neural_search.circuit_breaker.limit` 相同，此設定僅適用於 Lucene 引擎。預設為 `1.0`。
- `plugins.neural_search.sparse.algo_param.index_thread_qty`（動態，整數）：用於為[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)建立索引的執行緒數。提高此值會為索引建置工作配置更多 CPU，並提升編製索引的效能。有效值範圍為 `1` 到 `1024`。此設定同時適用於 Lucene 引擎與原生引擎。預設為 `1`。如需詳細資訊，請參閱[執行緒集區組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#thread-pool-configuration)。
- `plugins.neural_search.sparse.native_engine_feature_enabled`（靜態，布林值）：是否可使用神經稀疏 ANN 搜尋的[原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#native-engine)。由於此設定為靜態，請在每個節點上的 `opensearch.yml` 中設定；變更此設定需要重新啟動節點。預設為 `true`。
- `plugins.neural_search.sparse.native_engine_enabled`（動態，布林值）：是否在執行階段啟用神經稀疏 ANN 搜尋的[原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#native-engine)。此設定與 `plugins.neural_search.sparse.native_engine_feature_enabled` 都必須為 `true`，欄位才能使用原生引擎。預設為 `false`。如需詳細資訊，請參閱[啟用原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#enabling-the-native-engine)。
- `plugins.neural_search.reranker_max_document_fields`（靜態，整數）：[`rerank` 處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)的 `context.document_fields` 清單可包含的欄位數上限。若建立搜尋管線的請求中，`rerank` 處理器列出更多欄位，該請求會被拒絕。預設為 `50`。
- `plugins.neural_search.model_selection.model_id.<model_type>.<language_option>`（動態，字串）：已部署模型的 ID，用於在 [`semantic` 欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/#example-selecting-a-model-using-a-cluster-setting)中以 `model_selection` 取代 `model_id`。請將 `<model_type>` 取代為 `sparse` 或 `dense`，並將 `<language_option>` 取代為 `english` 或 `multilingual`（使用小寫），以符合該欄位 `model_selection` 中的 `model_type` 與 `language_option` 值。例如，`plugins.neural_search.model_selection.model_id.sparse.english` 會為使用 `"model_selection": {"model_type": "sparse", "language_option": "english"}` 的欄位設定模型。若省略 `model_type` 或 `language_option`，則分別預設為 `sparse` 或 `english`。OpenSearch 會在您建立或更新對應時讀取此設定，並將產生的 `model_id` 儲存在欄位對應中，因此之後變更此設定不會影響現有欄位。若未為該組合設定模型 ID，或模型的類型與 `model_type` 不符，則會拒絕該對應請求。無預設值。

沒有任何設定會限制原生引擎索引使用的記憶體量。原生引擎會從記憶體對應檔案讀取其索引，因此若要為原生引擎調整節點大小，請為作業系統頁面快取保留足夠的 RAM，與其他任何記憶體對應的 Lucene 資料相同。
{: .note}

### 索引設定

下列 Neural Search 外掛程式設定適用於索引層級：

- `index.neural_search.semantic_ingest_batch_size`（動態，整數）：指定在匯入期間為 `semantic` 欄位產生嵌入時，一次批次處理的文件數量。有效值為 1--100。預設值為 `10`。

<p id="hybrid-collapse-docs-per-group"></p>

- `index.neural_search.hybrid_collapse_docs_per_group_per_subquery`（_已棄用_）：此設定已棄用，不再有任何影響。傳回的文件數量完全由 `size` 參數控制。