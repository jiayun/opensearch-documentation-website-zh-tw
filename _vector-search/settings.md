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

- `knn.algo_param.index_thread_qty` (動態，整數)：用於原生程式庫與 Lucene 程式庫 (適用於 OpenSearch 2.19 及更新版本) 索引建立的執行緒數量。將此值保持在較低可減少 k-NN 外掛程式對 CPU 的影響，但也會降低編製索引的效能。在 CPU 核心少於 32 個的系統上預設為 `1`，在具有 32 個或更多核心的系統上預設為 `4`。

- `knn.cache.item.expiry.enabled` (動態，布林值)：是否將在指定時間內未被存取的原生程式庫索引從記憶體中移除。預設為 `false`。

- `knn.cache.item.expiry.minutes` (動態，時間單位)：原生程式庫索引從記憶體中移除前的閒置時間。僅在 `knn.cache.item.expiry.enabled` 為 `true` 時生效。預設為 `3h`。

- `knn.circuit_breaker.unset.percentage` (動態，百分比)：斷路器的原生記憶體使用量門檻。記憶體使用量必須低於 `knn.memory.circuit_breaker.limit` 的此百分比，`knn.circuit_breaker.triggered` 才能維持 `false`。預設為 `75`。

- `knn.circuit_breaker.triggered` (動態，布林值)：當記憶體使用量超過 `knn.circuit_breaker.unset.percentage` 值時設為 `true`。預設為 `false`。

- `knn.memory.circuit_breaker.limit` (動態，百分比或位元組單位)：原生程式庫索引的原生記憶體限制。在預設值下，若機器有 100 GB 記憶體且 JVM 使用 32 GB，則 k-NN 外掛程式會使用剩餘 68 GB 的 50% (34 GB)。若記憶體使用量超過此值，外掛程式會移除最近最少使用的原生程式庫索引。若要在節點層級設定此限制，請在 `opensearch.yml` 中加入 `node.attr.knn_cb_tier: "<tier-name>"`，並在叢集設定中設定 `knn.memory.circuit_breaker.limit.<tier-name>`。例如，將節點層級定義為 `node.attr.knn_cb_tier: "integ"` 並設定 `knn.memory.circuit_breaker.limit.integ: "80%"`。若已設定節點層級的斷路器限制，節點會使用該限制；若未設定節點專屬值，則使用叢集範圍的設定。預設為 `50%`。

- `knn.memory.circuit_breaker.enabled` (動態，布林值)：是否啟用 k-NN 記憶體斷路器。預設為 `true`。

- `knn.model.index.number_of_shards` (動態，整數)：模型系統索引所使用的分片數量，該索引是用於儲存近似最近鄰 (ANN) 搜尋所用模型的 OpenSearch 索引。預設為 `1`。

- `knn.model.index.number_of_replicas` (動態，整數)：模型系統索引所使用的副本分片數量。在多節點叢集中，請將此值至少設為 `1` 以提高穩定性。預設為 `1`。

- `knn.model.cache.size.limit` (動態，百分比)：模型快取限制，不得超過 JVM 堆積的 25%。預設為 `10%`。

- `knn.faiss.avx2.disabled` (靜態，布林值)：是否在 x64 架構的機器上，為 Faiss 引擎停用基於 SIMD 的 `libopensearchknn_faiss_avx2.so` 程式庫並載入未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設為 `false`。如需更多資訊，請參閱[單一指令多重資料 (SIMD) 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.faiss.avx512.disabled` (靜態，布林值)：是否在 x64 架構的機器上，為 Faiss 引擎停用基於 SIMD 的 `libopensearchknn_faiss_avx512.so` 程式庫，並載入 `libopensearchknn_faiss_avx2.so` 或未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設為 `false`。如需更多資訊，請參閱 [SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.faiss.avx512_spr.disabled` (靜態，布林值)：是否在 x64 架構的機器上，為 Faiss 引擎停用基於 SIMD 的 `libopensearchknn_faiss_avx512_spr.so` 程式庫，並載入 `libopensearchknn_faiss_avx512.so`、`libopensearchknn_faiss_avx2.so` 或未最佳化的 `libopensearchknn_faiss.so` 程式庫。預設為 `false`。如需更多資訊，請參閱 [SIMD 最佳化]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#simd-optimization)。

- `knn.dynamic_mapping.enabled` (動態，布林值)：是否啟用 `knn_vector` 欄位的[動態對應]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/#dynamic-mapping)，包括推斷未對應的扁平數值陣列，以及將 `knn_vector` 指定為 `match_mapping_type` 的動態範本。預設為 `false`。

### 索引設定

索引設定中定義的多個參數目前正處於淘汰程序中。請在對應中設定這些參數，而非在索引設定中。在對應中設定的參數會覆寫索引設定中的參數，並允許索引擁有多個具有不同參數的 `knn_vector` 欄位。

下列 k-NN 外掛程式設定適用於索引層級。如需更新這些設定的資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)：

- `index.knn` (靜態，布林值)：索引是否為其 `knn_vector` 欄位建立原生程式庫索引。若為 `false`，`knn_vector` 欄位會儲存在 doc values 中，但近似 k-NN 搜尋會停用。預設為 `false`。

- `index.knn.algo_param.ef_search` (動態，整數)：搜尋期間使用的最近鄰動態清單大小 (`ef`，即 `efSearch`)。數值越高，搜尋越精確但越慢。此值不得低於查詢的最近鄰數量 `k`，且可為 `k` 至資料集大小之間的任何值。預設為 `100`。

- `index.knn.advanced.approximate_threshold` (動態，整數)：OpenSearch 為 ANN 搜尋建立專用資料結構前，一個分段必須包含的向量數量。設為 `-1` 可停用向量資料結構的建立，設為 `0` 則一律建立。預設為 `0`。

- `index.knn.advanced.filtered_exact_search_threshold` (動態，整數)：在篩選式 ANN 搜尋期間，OpenSearch 切換至精確搜尋的篩選 ID 門檻。若分段中的篩選 ID 數量低於此值，則會對篩選 ID 執行精確搜尋。預設為 `-1`，表示不套用任何門檻。

- `index.knn.faiss.efficient_filter.disable_exact_search` (動態，布林值)：設為 `true` 時，停用當 Faiss 高效篩選式近似最近鄰 (ANN) 搜尋傳回少於 `k` 筆結果時所發生的精確搜尋後備機制。預設為 `false`。如需更多資訊，請參閱[停用精確搜尋後備機制]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/efficient-knn-filtering/#disabling-the-exact-search-fallback)。

- `index.knn.derived_source.enabled` (靜態，布林值)：防止向量儲存在 `_source` 中，以減少向量索引的磁碟用量。對於建立時將 `index.knn` 設為 `true` 的索引，預設為 `true`；對於所有其他索引，預設為 `false`。

- `index.knn.memory_optimized_search` (靜態，布林值)：在索引上啟用[記憶體最佳化搜尋]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/memory-optimized-search/)。預設為 `false`。

在 OpenSearch 2.11 或更早版本中建立的索引，仍會使用先前的 `ef_construction` 與 `ef_search` 值 (`512`)。
{: .note}

當您建立索引並將 `index.knn` 設為 `true` 時，k-NN 外掛程式也會降低兩項[分層合併原則設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#tiered-merge-policy-settings)，以減少合併與搜尋之間的 CPU 競爭：它會將 `index.merge.policy.max_merge_at_once` 設為 `10` 而非預設的 `30`，並將 `index.merge.policy.floor_segment` 設為 `2mb` 而非預設的 `16mb`。這兩項設定都是動態的，因此您可以在建立索引後變更它們。

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

下列 Neural Search 外掛程式設定適用於叢集層級。動態設定可透過 [Cluster Settings API]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#updating-cluster-settings-using-the-api) 更新；靜態設定則必須在每個節點的 `opensearch.yml` 中設定：

- `plugins.neural_search.stats_enabled` (動態，布林值)：啟用 [Neural Search Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#stats)。預設值為 `false`。
- `plugins.neural_search.circuit_breaker.limit` (動態，百分比)：指定[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)斷路器的 JVM 記憶體限制。此限制僅約束 Lucene 引擎使用的 JVM 堆積快取，對依賴作業系統分頁快取的原生引擎沒有影響。預設值為 JVM 堆積的 `10%`。如需更多資訊，請參閱[記憶體與快取設定]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#memory-and-caching-settings)。
- `plugins.neural_search.circuit_breaker.overhead` (動態，浮點數)：用於調整[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)記憶體用量估算值的乘數。數值越高，記憶體估算越保守。與 `plugins.neural_search.circuit_breaker.limit` 一樣，此設定僅適用於 Lucene 引擎。預設值為 `1.0`。
- `plugins.neural_search.sparse.algo_param.index_thread_qty` (動態，整數)：用於為[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)建置索引的執行緒數量。增加此值會為索引建置工作配置更多 CPU，並提升編製索引的效能。有效值範圍為 `1` 至 `1024`。此設定同時適用於 Lucene 引擎與原生引擎。預設值為 `1`。如需更多資訊，請參閱[執行緒集區組態]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#thread-pool-configuration)。
- `plugins.neural_search.sparse.native_engine_feature_enabled` (靜態，布林值)：是否提供適用於神經稀疏 ANN 搜尋的[原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#native-engine)。由於此設定為靜態，請在每個節點的 `opensearch.yml` 中設定；變更此設定需要重新啟動節點。預設值為 `true`。
- `plugins.neural_search.sparse.native_engine_enabled` (動態，布林值)：適用於神經稀疏 ANN 搜尋的[原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#native-engine)是否在執行階段啟用。在欄位可以使用原生引擎之前，此設定與 `plugins.neural_search.sparse.native_engine_feature_enabled` 都必須為 `true`。預設值為 `false`。如需更多資訊，請參閱[啟用原生引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#enabling-the-native-engine)。

沒有任何設定會限制原生引擎索引使用的記憶體量。原生引擎會從記憶體對應檔案讀取其索引，因此若要為原生引擎調整節點大小，請為作業系統分頁快取保留足夠的 RAM，與其他任何記憶體對應的 Lucene 資料相同。
{: .note}

### 索引設定

下列 Neural Search 外掛程式設定適用於索引層級：

- `index.neural_search.semantic_ingest_batch_size` (動態，整數)：指定在匯入期間為 `semantic` 欄位產生嵌入時批次處理的文件數量。預設值為 `10`。

<p id="hybrid-collapse-docs-per-group"></p>

- `index.neural_search.hybrid_collapse_docs_per_group_per_subquery` (_已棄用_)：此設定已棄用，不再有任何影響。傳回的文件數量完全由 `size` 參數控制。