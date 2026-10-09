---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經稀疏 ANN 搜尋"
parent: Neural sparse search
grand_parent: AI search
nav_order: 60
has_children: false
---

# 神經稀疏 ANN 搜尋
**於 3.3 版推出**
{: .label .label-purple }

神經稀疏近似最近鄰 (ANN) 搜尋透過在準確度與延遲之間取得平衡，來提升查詢效率。傳統的神經稀疏搜尋會在 `rank_features` 欄位上執行精確搜尋，神經稀疏 ANN 搜尋則不同，它會在 `sparse_vector` 欄位上使用 Spilled Clustering of Inverted Lists with Summaries for Maximum Inner Product Search (SEISMIC) 演算法，運用近似搜尋技術提供最佳化的查詢效能。

相較於傳統的神經稀疏搜尋，神經稀疏 ANN 搜尋提供下列優點：

- **查詢效能提升**：在召回率 ≥90% 的條件下，相較於兩階段查詢可大幅提升查詢速度，且隨著資料集規模成長，效能擴展優於線性。
- **可擴展性**：當資料集在單一節點上擴展至 5,000 萬個向量時，仍能維持一致的查詢效能。
- **記憶體效率**：使用位元組量化來縮減索引大小。視引擎而定，記憶體由具備斷路器的 JVM 堆積快取管理，或由堆積外的記憶體對應檔案管理，可避免資源耗盡。
- **混合式做法**：根據分段大小自動選取最佳的索引策略，對索引效能影響極小。
- **搜尋彈性**：使用查詢參數，在高召回率與低延遲之間提供可調整的取捨。
- **引擎選擇**：可使用 Lucene 引擎或原生引擎，後者會在堆積外記憶體中建立及搜尋索引。如需更多資訊，請參閱[引擎](#engines)。

當您需要稀疏擷取的效率，但同時需要比傳統神經稀疏搜尋方法在大規模下所能提供的更好效能時，請考慮使用神經稀疏 ANN 搜尋：

- **大規模應用**：包含數百萬至數十億份文件，且查詢效能至關重要的資料集。
- **高輸送量情境**：需要在大量查詢負載下快速回應的應用。

## 神經稀疏 ANN 搜尋的運作方式

神經稀疏 ANN 搜尋實作了多項技術，以同時最佳化神經稀疏向量的索引編製與查詢。

### 索引編製

在索引編製階段，神經稀疏 ANN 搜尋實作了幾項關鍵最佳化：

1. **張貼清單分群**：對於倒排索引中的每個詞彙，演算法會執行下列動作：
   - 依詞元權重由高至低排序文件。
   - 僅保留權重最高的前 `n_postings` 份文件。
   - 套用分群演算法，將相似的文件歸為同一叢集。原生引擎使用 `clustering_batch_size` 將每個張貼清單分割成批次，並分別對每個批次分群，如此可減少建立索引所需的記憶體，但代價是建置時間較長。
   - 為每個叢集產生摘要稀疏向量，僅保留權重最高的詞元。

2. **正向索引維護**：神經稀疏 ANN 搜尋同時維護分群的倒排索引，以及一份正向索引，後者依文件 ID 儲存完整的稀疏向量，以便在查詢處理期間有效率地存取。 

### 查詢處理

在查詢執行期間，神經稀疏 ANN 搜尋採用高效率的擷取流程：

1. **詞元層級剪枝**：對於指定的查詢，所有詞元會依其權重排序。僅保留權重最高的 `top_n` 個詞元，以減少造訪的張貼清單數量。

2. **叢集層級剪枝**：演算法會先計算查詢向量與叢集摘要向量之間的內積分數。僅選取分數高於動態閾值的叢集進行詳細檢查。

3. **文件層級評分**：對於選取的叢集，神經稀疏 ANN 搜尋會檢查這些叢集中的個別文件，計算查詢與從正向索引擷取之文件向量之間的精確內積分數。

此做法可大幅減少需要評分的文件數量，在維持高準確度的同時帶來顯著的效能提升。

### 混合式索引編製

神經稀疏 ANN 搜尋是一種混合式索引編製做法，會依據每個分段中的文件數量來平衡索引編製與查詢效能：

- 文件數少於 `approximate_threshold` 的分段：不進行分群即編製索引，因此對這些分段的查詢會為每份相符的文件評分。Lucene 引擎會將這些分段編製為一般的神經稀疏 (`rank_features`) 分段，並使用標準神經稀疏查詢來查詢。原生引擎則會將它們編製為以其原生格式建立的等效倒排索引。

- 文件數多於 `approximate_threshold` 的分段：編製為神經稀疏 ANN 分段，並使用稀疏 ANN 查詢來查詢。

此混合式做法可平衡索引編製效能與查詢速度。小型分段可避免分群的額外負擔，大型分段則可受益於近似搜尋最佳化。系統支援傳統神經稀疏查詢與神經稀疏 ANN 查詢並存於同一索引中，以維持回溯相容性。

如需 SEISMIC 演算法的更多資訊，請參閱 [Efficient Inverted Indexes for Approximate Retrieval over Learned Sparse Representations](https://arxiv.org/abs/2404.18812)。

## 引擎
**於 3.9 版推出**
{: .label .label-purple }

_引擎_ 是負責建立神經稀疏 ANN 索引並對其執行查詢的實作。兩種引擎都實作 SEISMIC 演算法，並接受相同的演算法與查詢參數；它們的差異在於索引的位置以及管理其記憶體的方式。

OpenSearch 支援下列引擎：

- [Lucene](#lucene-engine)：在 JVM 堆積中建立分群的張貼清單與正向索引，並由外掛程式管理的快取提供查詢服務。此為預設值。
- [原生](#native-engine)：將索引建立到磁碟上的記憶體對應檔案，並由堆積外記憶體提供查詢服務。

使用欄位之 `method` 物件中的 `engine` 參數來選取引擎：

```json
PUT /my-sparse-ann-index
{
  "settings": {
    "index": {
      "sparse": true
    }
  },
  "mappings": {
    "properties": {
      "sparse_embedding": {
        "type": "sparse_vector",
        "method": {
          "name": "seismic",
          "engine": "native",
          "parameters": {
            "n_postings": 4000,
            "cluster_ratio": 0.1,
            "forward_index": "per_block",
            "clustering_batch_size": 1
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

欄位建立後即無法更新 `method` 物件。若要變更引擎，請以所需的對應建立新索引，並重新將資料編製索引。
{: .important}

### 比較引擎

下表比較這兩種引擎。

| 特性 | Lucene 引擎 | 原生引擎 |
|:--- |:--- |:--- |
| `engine` 值 | `lucene` | `native` |
| 預設啟用 | 是 | 否。請參閱[啟用原生引擎](#enabling-the-native-engine)。 |
| 查詢效能 | 基準 | 更高的搜尋輸送量與更低的查詢延遲 |
| 索引建置效能 | 基準 | 更快的分段與強制合併建置 |
| 索引的存放位置 | JVM 堆積，位於外掛程式管理的快取中 | 磁碟上的記憶體對應檔案，從堆積外記憶體讀取 |
| 記憶體上限受何者限制 | `plugins.neural_search.circuit_breaker.limit` 設定，並採用最近最少使用快取逐出 | 作業系統分頁快取，沒有可設定的上限，且 OpenSearch 不會逐出 |
| 所需的 JVM 堆積 | 與節點所服務之稀疏分段的工作集成正比 | 極少，因為索引不存放在堆積中 |
| 磁碟配置 | 由 Lucene 管理 | 專用的引擎檔案，於查詢時進行記憶體對應，其大小取決於[正向索引配置](#choosing-a-forward-index-layout) |
| 篩選 | 後置篩選 | 前置篩選。請參閱[篩選支援](#filtering-support)。 |
| 文件數少於 `approximate_threshold` 之分段的格式 | `rank_features`，使用標準神經稀疏查詢來查詢 | 等效於 `rank_features` 的倒排索引，以引擎的原生格式建立 |
| Warm Up 與 Clear Cache API | 支援 | 不適用 |
| 稀疏記憶體統計資料 | 會回報 | 不會回報 |

如需在兩種引擎之間選擇的指引，請參閱[選擇引擎]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-sparse/#choosing-an-engine)。

### Lucene 引擎

Lucene 引擎是預設引擎，不需要額外組態。它將分群的張貼清單和正向索引資料儲存在 JVM 堆積中。記憶體用量受斷路器限制，達到上限時，資料會從快取中逐出。如需更多資訊，請參閱[記憶體與快取設定](#memory-and-caching-settings)。

由於索引保存在堆積中，大規模執行 Lucene 引擎的節點需要足夠大的 JVM 堆積，以容納其提供服務的每個稀疏分段的工作集。

### 原生引擎

原生引擎將 SEISMIC 索引寫入檔案，OpenSearch 會在查詢時將該檔案對應至記憶體，並直接讀取。磁碟上的配置就是執行階段的配置，因此載入索引時不會重建任何內容。這會產生下列影響：

- 索引不會耗用 JVM 堆積，也不會增加垃圾回收壓力，因此節點可以使用相對較小的堆積，為大型稀疏索引提供服務。
- 索引記憶體屬於可回收的作業系統分頁快取，因此作業系統會在記憶體壓力下回收它。此過程不涉及斷路器或逐出原則。
- 首次對分段進行查詢時，會產生建立記憶體對應的一次性成本。後續查詢會重複使用該對應。此成本會隨分段大小增加。

原生引擎依賴作業系統分頁快取，且沒有任何設定會限制其索引使用的記憶體量。規劃原生引擎節點的容量時，請為分頁快取保留足夠的 RAM，就如同處理其他任何對應至記憶體的 Lucene 資料一樣。

#### 啟用原生引擎

原生引擎預設為停用。欄位要使用原生引擎，下列兩個叢集設定都必須為 `true`：

| 設定 | 靜態／動態 | 預設 | 說明 |
|:--- |:--- |:--- |:--- |
| `plugins.neural_search.sparse.native_engine_feature_enabled` | 靜態 | `true` | 原生引擎是否可用。由於此設定是靜態設定，請在每個節點的 `opensearch.yml` 中設定；變更此設定需要重新啟動節點。 |
| `plugins.neural_search.sparse.native_engine_enabled` | 動態 | `false` | 是否在執行階段啟用原生引擎。 |

若要啟用原生引擎，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.neural_search.sparse.native_engine_enabled": true
  }
}
```
{% include copy-curl.html %}

如果任一設定為 `false`，OpenSearch 會拒絕建立將 `engine` 設為 `native` 的欄位、將文件編製索引至現有的原生引擎欄位，以及查詢此類欄位的嘗試。OpenSearch 不會退回使用 Lucene 引擎，因為欄位的對應指定了原生引擎。

原生引擎停用期間，OpenSearch 會在分段排清與合併時略過建立原生索引。原始向量仍會寫入磁碟，因此重新啟用引擎，再對受影響的索引執行強制合併，就會重建原生索引。
{: .note}

#### 選擇正向索引配置

`forward_index` 演算法參數控制原生引擎儲存正向索引的方式。請在欄位的 `method.parameters` 物件中指定此參數。下表說明可用的配置。

| 值 | 說明 | 取捨 |
|:--- |:--- |:--- |
| `shared`（預設） | 欄位使用單一連續的正向索引。 | 磁碟用量較低。 |
| `per_block` | 每個區塊的向量都與該區塊一起以內嵌方式儲存，因此查詢只會讀取所選的區塊。 | 查詢延遲較低，磁碟用量較高。 |

兩種配置都會對應至記憶體，並套用相同的量化方式。`forward_index` 參數選擇正向索引資料的放置位置；兩種配置儲存資料的精確度相同。

如果您將 `engine` 設為 `lucene`，並指定 `shared` 以外的 `forward_index` 值，請求就會遭到拒絕。
{: .warning}

#### 原生引擎的注意事項

選擇原生引擎之前，請注意下列事項：

- [Warm Up]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#warm-up) 和 [Clear Cache]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#clear-cache) API 操作的是 Lucene 引擎的快取，不適用於原生引擎。
- [Neural Search Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#stats) 傳回的稀疏記憶體統計資料只會回報 Lucene 引擎的快取用量，不包含原生引擎索引的記憶體用量。
- `plugins.neural_search.circuit_breaker.limit` 設定對原生引擎沒有影響。
- 原生引擎要求索引的資料儲存在本機檔案系統上。

## 步驟 1：建立索引

若要使用神經稀疏 ANN 搜尋，您必須在索引層級啟用 `sparse` 設定，並使用 `sparse_vector` 作為欄位類型。

### 索引設定

設定 `index.sparse: true` 以啟用神經稀疏 ANN 搜尋功能：

```json
PUT /my-sparse-ann-index
{
  "settings": {
    "index": {
      "sparse": true,
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "sparse_embedding": {
        "type": "sparse_vector",
        "method": {
          "name": "seismic",
          "parameters": {
            "n_postings": 4000,
            "cluster_ratio": 0.1,
            "summary_prune_ratio": 0.4,
            "approximate_threshold": 1000000
          }
        }
      },
      "text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

此範例省略了 `engine` 參數，因此欄位會使用預設的 Lucene 引擎。若要改用原生引擎，請參閱[引擎](#engines)。

如需參數資訊，請參閱[稀疏向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/sparse-vector/)。

## 步驟 2：匯入資料

匯入含有稀疏嵌入的文件，其中詞元以整數表示，並具有對應的權重：

```json
POST _bulk
{ "create": { "_index": "my-sparse-ann-index", "_id": "1" } }
{ "sparse_embedding": {"10": 0.85, "23": 1.92, "24": 0.67, "78": 2.54, "156": 0.73}, "text": "OpenSearch neural sparse search" }
{ "create": { "_index": "my-sparse-ann-index", "_id": "2" } }
{ "sparse_embedding": {"3": 1.22, "19": 0.11, "21": 0.35, "300": 1.74, "985": 0.96}, "text": "Machine learning algorithms" }
```
{% include copy-curl.html %}

您也可以使用[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，自動將詞元格式化為整數。

## 步驟 3：查詢索引

使用 `neural_sparse` 查詢執行神經稀疏 ANN 搜尋，並透過 `method_parameters` 調整效能。

請勿將神經稀疏 ANN 搜尋與[兩階段]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-sparse-query-two-phase-processor/)管線搭配使用。
{: .important}

### 使用自然語言查詢

使用自然語言文字進行查詢，需要已部署的稀疏編碼模型將文字轉換為稀疏向量：

```json
GET /my-sparse-ann-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_text": "machine learning algorithms",
        "model_id": "your_sparse_model_id",
        "method_parameters": {
          "k": 10,
          "top_n": 10,
          "heap_factor": 1.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 使用原始向量查詢

使用預先計算的稀疏向量進行查詢，其中詞元以整數及其對應權重指定：

```json
GET /my-sparse-ann-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "1055": 1.7,
          "2931": 2.3
        },
        "method_parameters": {
          "k": 10,
          "top_n": 6,
          "heap_factor": 1.2
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 查詢參數

| 參數 | 說明 |
|:--- |:--- |
| `k` | 要傳回的最相近前幾筆結果數量 |
| `top_n` | 要保留的最高權重查詢詞元數量 |
| `heap_factor` | 控制召回率與效能之間的取捨 |
| `filter` | 用於預先篩選或事後篩選的選用布林值篩選器 |

兩種引擎的查詢語法與這些參數皆相同。您會在欄位對應中選取引擎。如需更多資訊，請參閱[引擎](#engines)。
{: .note}

## 篩選支援

神經稀疏 ANN 搜尋支援篩選。如果篩選器符合的文件數少於 `k`，兩種引擎都會對篩選後的文件執行精確搜尋。否則，兩種引擎會在不同的階段套用篩選器：

- Lucene 引擎在近似擷取之後套用篩選器（事後篩選）。結果是前幾筆相符項目與篩選器的交集，因此選擇性篩選器可能傳回少於 `k` 筆結果。
- 原生引擎在擷取之前將篩選器下推為候選集合（預先篩選）。擷取會在篩選後的集合內進行，因此查詢可以傳回完整的 `k` 筆結果。

如需更多資訊，請參閱[神經稀疏 ANN 搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)。

## 叢集設定

神經稀疏 ANN 搜尋支援下列叢集設定。

### 執行緒集區組態

建立叢集化倒排索引結構需要大量運算。預設情況下，演算法使用單執行緒的執行緒集區來建立叢集。您可以增加執行緒集區大小以平行方式建立叢集，使用更多 CPU 核心並縮短索引建立時間。此設定適用於兩種引擎。

若要設定執行緒集區大小，請更新 `plugins.neural_search.sparse.algo_param.index_thread_qty` 設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.neural_search.sparse.algo_param.index_thread_qty": 4
  }
}
```
{% include copy-curl.html %}

### 記憶體與快取設定

Lucene 引擎提供斷路器，可防止演算法使用過多記憶體，並確保其他 OpenSearch 作業不受影響。`circuit_breaker.limit` 的預設值為 `10%`。您可以調整此設定來控制配置給演算法的總記憶體。當記憶體使用量達到定義的限制時，會發生快取逐出，移除最近最少使用的資料。

較高的斷路器限制允許更多記憶體使用量並降低快取逐出的頻率，但可能影響其他 OpenSearch 作業。較低的限制提供更高的安全性，但可能導致更頻繁的快取逐出。

若要設定斷路器限制，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.neural_search.circuit_breaker.limit": "30%"
  }
}
```
{% include copy-curl.html %}

斷路器限制 Lucene 引擎的 JVM 堆積快取。它對原生引擎沒有效果，原生引擎將其索引保存在由作業系統管理的記憶體對應檔案中。如需更多資訊，請參閱[原生引擎](#native-engine)。
{: .note}

如需更多資訊，請參閱[Neural Search 外掛程式設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#neural-search-plugin-settings)。

### 監控

使用 [Neural Search Stats API]({{site.url}}{{site.baseurl}}/vector-search/api/neural/#stats) 監控記憶體使用量與查詢統計資料。

稀疏記憶體統計資料僅報告 Lucene 引擎的快取使用量。原生引擎的索引記憶體保存在作業系統的分頁快取中，不會反映在這些統計資料中。
{: .note}

## 效能調校

神經稀疏 ANN 搜尋提供多個參數，用於平衡搜尋精確度與查詢速度。如需完整的調校指引，請參閱[神經稀疏 ANN 搜尋效能調校]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-sparse/)。

## 後續步驟

- 如需查詢語法，請參閱[神經稀疏查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/)。
- 如需欄位類型資訊，請參閱[稀疏向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/sparse-vector/)。
- 如需效能最佳化，請參閱[神經稀疏 ANN 搜尋效能調校]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-sparse/)。
- 如需篩選選項，請參閱[神經稀疏 ANN 搜尋中的篩選]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/filtering-in-sparse-search/)。