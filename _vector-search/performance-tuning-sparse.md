---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經稀疏 ANN 搜尋效能調校"
parent: Performance tuning
nav_order: 30
has_math: true
---

# 神經稀疏 ANN 搜尋效能調校

[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/) 提供數個參數，讓您能在查詢召回率（準確度）與查詢效率（延遲）之間取得平衡。查詢參數是在查詢的 `method_parameters` 物件中提供，會立即生效。對應參數是在 `sparse_vector` 欄位的 `method` 物件中提供，會在建立欄位時固定。若要變更 `engine` 或 `method.parameters` 中的任何值，請以所需的對應建立新索引，並將資料重新編製索引。

## 選擇引擎
**自 3.9 版推出**
{: .label .label-purple }

神經稀疏 ANN 搜尋會使用兩種引擎之一來執行 SEISMIC 演算法，您可以透過 `method.engine` 對應參數為每個 `sparse_vector` 欄位選取要使用的引擎。有效值為 `lucene`（預設）與 `native`。兩種引擎接受相同的查詢參數，且除了僅適用於原生引擎的 `clustering_batch_size` 與 `forward_index` 之外，它們也接受相同的 `method.parameters` 值。因此，本頁其餘的調校指引適用於兩種引擎。如需引擎的完整比較以及啟用原生引擎的說明，請參閱 [引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。

兩種引擎的差異在於演算法所讀取之資料結構的位置，這會影響節點大小規劃：

- Lucene 引擎會將叢集化的張貼清單與正向索引保存在受 `plugins.neural_search.circuit_breaker.limit` 限制的 JVM 堆積快取中。請將節點的堆積大小設定為足以容納其服務之每個稀疏分段的工作集。
- 原生引擎會從磁碟上的記憶體對應檔案讀取其索引，因此索引不會耗用 JVM 堆積，也不會增加垃圾回收壓力。請將節點大小設定為為作業系統頁面快取保留足夠的 RAM。

當您想要更好的查詢與索引建置效能、當您的稀疏索引大到將其保存在 JVM 堆積中會對節點造成限制，或當您想以相對較小的堆積服務大型稀疏索引時，請考慮使用原生引擎。當您想要預設組態，或當您依賴 [Warm Up]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#warm-up) 與 [Clear Cache]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#clear-cache) API，或依賴 [Neural Search Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#stats) 所回報的稀疏記憶體統計資料時，請考慮使用 Lucene 引擎。

在選擇引擎之前，請先針對您自己的資料與查詢組合對兩種引擎進行基準測試。相對輸送量、延遲與記憶體使用量取決於您的語料庫、您的參數設定，以及節點上可用的資源。
{: .note}

## 索引效能調校

這些參數控制索引建構與記憶體使用量：

- `n_postings`：每個張貼清單中要保留的文件數上限。

    `n_postings` 值越小，會套用越積極的剪除，表示每個張貼清單中保留的文件識別碼越少。較低的值可加快索引建置與查詢執行速度，但會降低召回率與記憶體耗用量。若未指定，演算法會在分段層級將該值計算為 $$0.0005 \times \text{document count}$$。

- `cluster_ratio`：每個張貼清單中用來決定叢集數的文件比例。

    剪除之後，每個張貼清單會包含 `cluster_ratio × posting_document_count`。增加 `cluster_ratio` 會產生更多叢集，可改善召回率，但會增加索引建置時間、查詢延遲與記憶體使用量。

- `summary_prune_ratio`：叢集摘要向量中要保留以供近似比對的詞元比例。

    此參數控制每個叢集的 `summary` 中保留多少詞元。`summary` 有助於判斷查詢期間是否要檢查某個叢集。若嵌入的詞元數差異很大，請據此調整此參數。較高的值會在 `summary` 中保留更多詞元。

- `approximate_threshold`：分段中要啟用神經稀疏 ANN 搜尋所需的文件數下限。

    此參數控制當分段的文件數達到指定閾值時，是否要在該分段中啟用神經稀疏 ANN 演算法。隨著文件總數增加，個別分段會包含更多文件。在此情況下，您可以將 `approximate_threshold` 設為較高的值，以避免在文件數較少的分段合併時反覆重建叢集。如果您不使用 force merge 作業將所有分段合併成一個，此參數尤其重要，因為文件數少於閾值的分段會退回 `rank_features`（一般神經稀疏搜尋）模式。請注意，若將此值設得太高，神經稀疏 ANN 搜尋可能永遠不會啟用。

- `clustering_batch_size`：每個倒排清單在進行叢集化時要分割成的批次數。僅原生引擎支援。

    依預設，此參數為 `1`，叢集化會對整個語料庫執行。將其設為較高的值（最高為 `10000`）會將每個倒排清單分割成該數量的批次，並分別對每個批次進行叢集化，這可減少建置索引所需的記憶體，但會延長建置時間。若索引建置受記憶體限制，請增加此值。

- `forward_index`：正向索引在磁碟上的儲存方式。僅原生引擎支援。

    預設的 `shared` 配置會為欄位儲存一個連續的正向索引，使用的磁碟空間較少。`per_block` 配置會將每個區塊的向量內嵌儲存在該區塊旁，因此查詢只會讀取其選取的區塊，可降低查詢延遲，但會使用更多磁碟空間。如需詳細資訊，請參閱 [選擇正向索引配置]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#choosing-a-forward-index-layout)。

## 查詢效能調校

這些參數會影響搜尋效能與召回率：

- `top_n`：近似稀疏查詢要保留之權重最高的查詢詞元數。

    在神經稀疏 ANN 搜尋演算法中，查詢中只會依權重保留前 `top_n` 個詞元。此參數控制搜尋效率（延遲）與準確度（召回率）之間的平衡。較高的值可改善準確度，但會增加延遲；較低的值可降低延遲，但會犧牲準確度。

- `heap_factor`：控制召回率與效能之間的取捨。

    在神經稀疏 ANN 搜尋期間，演算法會將叢集的分數與結果佇列中的最高分數除以 `heap_factor` 後的結果進行比較，以決定是否要檢查某個叢集。`heap_factor` 越大，叢集必須達到的閾值越低，使演算法檢查更多叢集，進而改善準確度，但會降低查詢速度。反之，`heap_factor` 越小，閾值越高，使演算法對要檢查哪些叢集更具選擇性。此參數提供比 `top_n` 更精細的控制，讓您能微調準確度與延遲之間的取捨。


## 其他最佳化策略

除了調校上述參數之外，您還可以採用下列最佳化策略。

### 建置叢集

索引建置可受益於使用多個執行緒。您可以指定 `plugins.neural_search.sparse.algo_param.index_thread_qty` 設定（預設為 `1`）來調整用於叢集建置的執行緒數。如需更新此設定的相關資訊，請參閱 [向量搜尋設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#cluster-settings-2)。在啟用神經稀疏 ANN 搜尋時，使用較高的 `plugins.neural_search.sparse.algo_param.index_thread_qty` 可縮短 force merge 時間，不過也會耗用更多系統資源。此設定同時適用於 Lucene 引擎與原生引擎。

### 冷啟動後查詢

重新啟動 OpenSearch 後，Lucene 引擎的快取是空的，因此前幾百次查詢可能會遇到高延遲。為了解決這個「冷啟動」問題，您可以使用 [Warm Up API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#warm-up)。此 API 會將資料從磁碟載入快取，確保後續查詢有最佳效能。您也可以在需要時使用 [Clear Cache API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#clear-cache) 來釋放記憶體。

原生引擎不使用此快取，因此 Warm Up 與 Clear Cache API 不適用於它。對於原生引擎，對某個分段的第一個查詢會支付一次性的成本，將該分段的索引檔案進行記憶體對應，之後的查詢則會重複使用既有的對應。

### 強制合併分段

一旦分段的文件數超過 `approximate_threshold`，神經稀疏 ANN 搜尋就會自動建置叢集化的張貼清單。不過，將所有分段合併成單一分段通常可達到更低的查詢延遲：

```json
POST /sparse-ann-documents/_forcemerge?max_num_segments=1
```
{% include copy-curl.html %}

您也可以將 `approximate_threshold` 設為較高的值，讓個別分段不會觸發叢集化，但合併後的分段會觸發。此做法有助於避免在編製索引期間反覆建置叢集。

原生引擎建置稀疏索引的速度較快，因此 force merge 會較早完成。如需詳細資訊，請參閱 [選擇引擎](#choosing-an-engine)。

## 最佳做法

- 從預設參數開始，並根據您的特定資料集進行調校。
- 對於 Lucene 引擎，請監控記憶體使用量並據此調整快取設定。
- 請考量索引時間與查詢效能之間的取捨。
- 在建立欄位之前先選擇引擎。`method` 無法更新，因此之後若要切換引擎，必須將資料重新編製索引至新索引。
- 如果您受記憶體限制或 JVM 堆積承受壓力，我們建議使用原生引擎，它會將其索引保存在磁碟上的記憶體對應檔案中。
- 為原生引擎規劃節點大小時，請為作業系統頁面快取保留足夠的 RAM，而不是增加 JVM 堆積。
- 當查詢延遲比磁碟使用量更重要時，請將 `forward_index` 設為 `per_block`；當您想盡量減少磁碟使用量時，請保留預設的 `shared` 配置。
- 對於原生引擎，若索引建置受記憶體限制，請增加 `clustering_batch_size` 以降低建置尖峰記憶體，但會延長建置時間。
- 請勿將神經稀疏 ANN 搜尋欄位與包含[兩階段處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-sparse-query-two-phase-processor/)的管線結合使用。

## 後續步驟

- [神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)