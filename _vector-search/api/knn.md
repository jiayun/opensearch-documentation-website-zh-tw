---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: k-NN API
parent: Vector search API
nav_order: 10
has_children: false
redirect_from:
  - /search-plugins/knn/jni-libraries/
---

# k-NN API

OpenSearch 提供數個 k 近鄰（k-NN）API，用於管理、監控及最佳化您的向量工作負載。

## 統計資料

k-NN `stats` API 提供 k-NN 外掛程式的目前狀態相關資訊，該外掛程式實作向量搜尋功能。這包括叢集層級與節點層級的統計資料。叢集層級統計資料對整個叢集只有單一值。節點層級統計資料對叢集中的每個節點各有一個值。您可以依 `nodeId` 與 `statName` 篩選查詢，如下列範例所示：

```json
GET /_plugins/_knn/nodeId1,nodeId2/stats/statName1,statName2
```
{% include copy-curl.html %}

### 回應本文欄位

下表列出可用的回應本文欄位。

欄位 | 說明
:--- | :---
`circuit_breaker_triggered` | 指出是否觸發斷路器。此統計資料僅與近似 k-NN 搜尋相關。
`total_load_time` | k-NN 將原生程式庫索引載入快取所花費的時間，以奈秒為單位。此統計資料僅與近似 k-NN 搜尋相關。
`eviction_count` | 因記憶體限制或閒置時間而從快取中移出的原生程式庫索引數量。此統計資料僅與近似 k-NN 搜尋相關。<br /> **注意**：因刪除索引而發生的明確移出不會計入。
`hit_count` | 快取命中次數。當使用者查詢已載入記憶體的原生程式庫索引時，就會發生快取命中。此統計資料僅與近似 k-NN 搜尋相關。
`miss_count` | 快取未命中次數。當使用者查詢尚未載入記憶體的原生程式庫索引時，就會發生快取未命中。此統計資料僅與近似 k-NN 搜尋相關。
`graph_memory_usage` | 原生程式庫索引在節點上使用的原生記憶體量，以 KB 為單位。
`graph_memory_usage_percentage` | 原生程式庫索引在節點上使用的原生記憶體量，佔最大快取容量的百分比。
`graph_index_requests` | 將文件的 `knn_vector` 欄位新增至原生程式庫索引的請求次數。
`graph_index_errors` | 將文件的 `knn_vector` 欄位新增至原生程式庫索引而產生錯誤的請求次數。
`graph_query_requests` | 已進行的原生程式庫索引查詢次數。
`graph_query_errors` | 已產生錯誤的原生程式庫索引查詢次數。
`knn_query_requests` | 收到的 k-NN 查詢請求次數。
`knn_query_with_filter_requests` | 收到且包含篩選條件的 k-NN 查詢請求次數。
`min_score_query_requests` | 收到且使用 `min_score` 的徑向搜尋請求次數。
`min_score_query_with_filter_requests` | 收到且使用 `min_score` 並包含篩選條件的徑向搜尋請求次數。
`max_distance_query_requests` | 收到且使用 `max_distance` 的徑向搜尋請求次數。
`max_distance_query_with_filter_requests` | 收到且使用 `max_distance` 並包含篩選條件的徑向搜尋請求次數。
`cache_capacity_reached` | 是否已達到 `knn.memory.circuit_breaker.limit`。此統計資料僅與近似 k-NN 搜尋相關。
`load_success_count` | k-NN 成功將原生程式庫索引載入快取的次數。此統計資料僅與近似 k-NN 搜尋相關。
`load_exception_count` | 嘗試將原生程式庫索引載入快取時發生例外狀況的次數。此統計資料僅與近似 k-NN 搜尋相關。
`indices_in_cache` | 對於每個具有 `knn_vector` 欄位且已啟用近似 k-NN 的 OpenSearch 索引，此統計資料會提供該 OpenSearch 索引擁有的原生程式庫索引數量，以及該 OpenSearch 索引正在使用的 `graph_memory_usage` 總量，以 KB 為單位。
`script_compilations` | k-NN 指令碼已編譯的次數。此值通常應為 1 或 0，但如果包含已編譯指令碼的快取已滿，k-NN 指令碼可能會重新編譯。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_compilation_errors` | 指令碼編譯期間的錯誤次數。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_query_requests` | 指令碼查詢的總次數。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_query_errors` | 指令碼查詢期間的錯誤次數。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`nmslib_initialized` | 布林值，指出 `nmslib` JNI 程式庫是否已在節點上載入並初始化。
`faiss_initialized` | 布林值，指出 `faiss` JNI 程式庫是否已在節點上載入並初始化。
`lucene_initialized` | 布林值，指出 `lucene` 引擎是否已在節點上初始化。
`model_index_status` | 模型系統索引的狀態。有效值為 `red`、`yellow` 和 `green`。如果索引不存在，此值為 `null`。
`indexing_from_model_degraded` | 布林值，指出從模型編製索引是否已降級。如果沒有足夠的 JVM 記憶體可快取模型，就會發生此情況。
`training_requests` | 對節點提出的訓練請求次數。
`training_errors` | 節點上已發生的訓練錯誤次數。
`training_memory_usage` | 訓練在節點上使用的原生記憶體量，以 KB 為單位。
`training_memory_usage_percentage` | 訓練在節點上使用的原生記憶體量，佔最大快取容量的百分比。
`graph_stats` | 在節點上建置原生程式庫索引的相關統計資料。`refresh` 物件包含重新整理作業的總次數（`total`）及其總時間（`total_time_in_millis`）。`merge` 物件包含目前與總合併作業次數（`current`、`total`）、其總時間（`total_time_in_millis`），以及目前與總合併中的文件數量和大小（`current_docs`、`total_docs`、`current_size_in_bytes`、`total_size_in_bytes`）。
`remote_vector_index_build_stats` | 遠端索引建置統計資料。如需詳細資訊，請參閱[遠端索引建置統計資料](#remote-index-build-stats)。

部分統計資料的名稱包含 *graph*。在這些情況下，*graph* 與*原生程式庫索引*同義。*graph* 一詞反映了此外掛程式僅支援 HNSW 演算法（由階層式圖形組成）的時期。
{: .note}

#### 遠端索引建置統計資料
於 3.0 版推出 
{: .label .label-purple }

`remote_vector_index_build_stats` 物件包含[遠端索引建置]({{site.url}}{{site.baseurl}}/vector-search/remote-index-build/)的統計資料。下表列出 `remote_vector_index_build_stats` 物件中的欄位。

| 欄位 | 說明 |
|:---|:---|
| `repository_stats.read_success_count` | 從儲存庫成功執行讀取作業的次數。 |
| `repository_stats.read_failure_count` | 從儲存庫讀取作業失敗的次數。 |
| `repository_stats.successful_read_time_in_millis` | 成功讀取作業所花費的總時間（毫秒）。 |
| `repository_stats.write_success_count` | 成功執行寫入儲存庫作業的次數。 |
| `repository_stats.write_failure_count` | 寫入儲存庫作業失敗的次數。 |
| `repository_stats.successful_write_time_in_millis` | 成功寫入作業所花費的總時間（毫秒）。 |
| `client_stats.build_request_success_count` | 成功執行建置請求作業的次數。 |
| `client_stats.build_request_failure_count` | 建置請求作業失敗的次數。 |
| `client_stats.status_request_failure_count` | 狀態請求作業失敗的次數。 |
| `client_stats.status_request_success_count` | 成功執行狀態請求作業的次數。 |
| `client_stats.index_build_success_count` | 成功執行索引建置作業的次數。 |
| `client_stats.index_build_failure_count` | 索引建置作業失敗的次數。 |
| `client_stats.index_build_merge_abort_exception` | 因合併作業中止而停止的遠端索引建置次數。這些建置不會計入 `index_build_failure_count`。 |
| `client_stats.index_build_terminal_exception` | 因終止性 I/O 例外而停止的遠端索引建置次數。這些建置不會計入 `index_build_failure_count`。 |
| `client_stats.waiting_time_in_ms` | 用戶端等待遠端建置完成所花費的總時間（毫秒）。 |
| `build_stats.remote_index_build_flush_time_in_millis` | 遠端排清作業所花費的總時間（毫秒）。 |
| `build_stats.remote_index_build_merge_time_in_millis` | 遠端合併作業所花費的總時間（毫秒）。 |
| `build_stats.remote_index_build_current_merge_operations` | 目前進行中的遠端合併作業數量。 |
| `build_stats.remote_index_build_current_flush_operations` | 目前進行中的遠端排清作業數量。 |
| `build_stats.remote_index_build_current_merge_size` | 目前遠端合併作業的大小。 |
| `build_stats.remote_index_build_current_flush_size` | 目前遠端排清作業的大小。 |

#### 範例請求

下列範例示範如何擷取與 k-NN 外掛程式相關的統計資料。

下列範例會擷取叢集中所有節點上 k-NN 外掛程式的完整統計資料：

```json
GET /_plugins/_knn/stats?pretty
```
{% include copy-curl.html %}

回應包含叢集層級的統計資料，以及每個節點的統計資料：

```json
{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "my-cluster",
  "circuit_breaker_triggered" : false,
  "model_index_status" : "YELLOW",
  "nodes" : {
    "JdfxIkOS1-43UxqNz98nw" : {
      "remote_vector_index_build_stats" : {
        "repository_stats" : {
          "read_success_count" : 0,
          "read_failure_count" : 0,
          "successful_read_time_in_millis" : 0,
          "write_success_count" : 0,
          "write_failure_count" : 0,
          "successful_write_time_in_millis" : 0
        },
        "client_stats" : {
          "status_request_failure_count" : 0,
          "index_build_terminal_exception" : 0,
          "status_request_success_count" : 0,
          "index_build_success_count" : 0,
          "index_build_failure_count" : 0,
          "build_request_failure_count" : 0,
          "index_build_merge_abort_exception" : 0,
          "build_request_success_count" : 0,
          "waiting_time_in_ms" : 0
        },
        "build_stats" : {
          "remote_index_build_flush_time_in_millis" : 0,
          "remote_index_build_current_merge_operations" : 0,
          "remote_index_build_current_flush_operations" : 0,
          "remote_index_build_current_merge_size" : 0,
          "remote_index_build_current_flush_size" : 0,
          "remote_index_build_merge_time_in_millis" : 0
        }
      },
      "max_distance_query_with_filter_requests" : 0,
      "graph_memory_usage_percentage" : 3.68,
      "graph_query_requests" : 1420920,
      "graph_memory_usage" : 2,
      "cache_capacity_reached" : false,
      "load_success_count" : 179,
      "training_memory_usage" : 0,
      "indices_in_cache" : {
        "myindex" : {
          "graph_memory_usage_percentage" : 3.68,
          "graph_memory_usage" : 2,
          "graph_count" : 2
        }
      },
      "script_query_errors" : 0,
      "hit_count" : 1420775,
      "knn_query_requests" : 147092,
      "total_load_time" : 2436679306,
      "miss_count" : 179,
      "min_score_query_requests" : 0,
      "knn_query_with_filter_requests" : 5,
      "training_memory_usage_percentage" : 0.0,
      "max_distance_query_requests" : 0,
      "lucene_initialized" : true,
      "graph_index_requests" : 656,
      "faiss_initialized" : true,
      "load_exception_count" : 0,
      "training_errors" : 0,
      "min_score_query_with_filter_requests" : 0,
      "eviction_count" : 0,
      "nmslib_initialized" : false,
      "script_compilations" : 0,
      "script_query_requests" : 0,
      "graph_stats" : {
        "merge" : {
          "current" : 0,
          "total" : 0,
          "total_time_in_millis" : 0,
          "current_docs" : 0,
          "total_docs" : 0,
          "total_size_in_bytes" : 0,
          "current_size_in_bytes" : 0
        },
        "refresh" : {
          "total" : 4,
          "total_time_in_millis" : 19
        }
      },
      "graph_query_errors" : 0,
      "indexing_from_model_degraded" : false,
      "graph_index_errors" : 0,
      "training_requests" : 17,
      "script_compilation_errors" : 0
    }
  }
}
```

下列範例會擷取單一節點的特定指標（斷路器狀態與圖形記憶體使用量）：

```json
GET /_plugins/_knn/HYMrXXsBSamUkcAjhjeN0w/stats/circuit_breaker_triggered,graph_memory_usage?pretty
```
{% include copy-curl.html %}

回應只包含所請求的統計資料：

```json
{
    "_nodes" : {
        "total" : 1,
        "successful" : 1,
        "failed" : 0
    },
    "cluster_name" : "my-cluster",
    "circuit_breaker_triggered" : false,
    "nodes" : {
        "HYMrXXsBSamUkcAjhjeN0w" : {
            "graph_memory_usage" : 1
        }
    }
}
```

## 預熱作業

用於執行近似 k-NN 搜尋的原生程式庫索引，會以特殊檔案的形式與其他 Apache Lucene 分段檔案一併儲存。若要使用 k-NN 外掛程式對這些索引執行搜尋，外掛程式必須將這些檔案載入原生記憶體。

如果外掛程式尚未將檔案載入原生記憶體，則會在收到搜尋請求時載入。載入時間可能會在初始查詢時造成高延遲。為避免此問題，使用者通常會在預熱期間執行隨機查詢。預熱期間結束後，檔案已載入原生記憶體，即可啟動生產工作負載。此載入過程是間接的，需要額外的工夫。

或者，您可以對想要搜尋的索引執行 k-NN 外掛程式預熱 API 作業，以避免此延遲問題。此作業會將請求中指定之所有索引的所有分片（主要與副本）的原生程式庫檔案載入原生記憶體。

程序完成後，您即可搜尋這些索引，而不會產生初始延遲。預熱 API 作業具有冪等性，因此如果某個分段的原生程式庫檔案已載入記憶體，此作業不會產生任何效果。它只會載入目前未儲存在記憶體中的檔案。

#### 範例請求

以下請求會對三個索引執行暖機：

```json
GET /_plugins/_knn/warmup/index1,index2,index3?pretty
```
{% include copy-curl.html %}

回應包含此作業的分片數量：

```json
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```

`total` 值表示 k-NN 外掛程式嘗試暖機的分片數量。回應也包含外掛程式成功暖機及暖機失敗的分片數量。

在暖機作業完成或請求逾時之前，此呼叫不會傳回結果。如果請求逾時，作業會在叢集上繼續進行。若要監控暖機作業，請使用 OpenSearch `_tasks` API：

```json
GET /_tasks
```
{% include copy-curl.html %}

作業完成後，請使用 [k-NN `_stats` API 操作](#stats)查看 k-NN 外掛程式已將哪些內容載入圖形中。

### 最佳做法

若要讓預熱作業正常運作，請遵循下列最佳做法：

* 不要對想要預熱的索引執行合併作業。在合併作業期間，k-NN 外掛程式會建立新的分段，有時會刪除舊的分段。例如，您可能會遇到以下情況：預熱 API 作業將原生程式庫索引 A 與 B 載入原生記憶體，但分段 C 是由分段 A 與 B 合併而成。原生程式庫索引 A 與 B 將不再存在於記憶體中，而原生程式庫索引 C 也尚未載入記憶體。在這種情況下，載入原生程式庫索引 C 的初始延遲仍然存在。

* 確認所有想要預熱的原生程式庫索引都能容納於原生記憶體中。如需原生記憶體限制的詳細資訊，請參閱 [knn.memory.circuit_breaker.limit 統計資料]({{site.url}}{{site.baseurl}}/search-plugins/knn/settings#cluster-settings)。圖形記憶體使用量過高會導致快取頻繁置換，可能使作業不斷失敗並嘗試重新執行。

* 不要對想要載入快取的文件編製索引。將新資訊寫入分段會使預熱 API 作業無法載入原生程式庫索引，直到它們可供搜尋為止。這表示您必須在編製索引後再次執行預熱作業。

## k-NN 清除快取
於 2.14 版導入
{: .label .label-purple }

在近似 k-NN 搜尋或預熱作業期間，原生程式庫索引（`faiss` 與 `nmslib` [已淘汰] 引擎）會載入原生記憶體。目前，您可以透過刪除索引，或設定 k-NN 叢集設定 `knn.cache.item.expiry.enabled` 與 `knn.cache.item.expiry.minutes`（若索引閒置一段時間即將其從快取中移除）來將索引從快取或原生記憶體中逐出。然而，您無法在不刪除索引的情況下將索引從快取中逐出。為解決此問題，您可以使用 k-NN 清除快取 API 作業，將指定的索引集合從快取中清除。

k-NN 清除快取 API 會逐出請求中指定之所有索引的所有分片（主要與副本）的所有原生程式庫檔案。與[預熱作業](#warmup-operation)的行為類似，k-NN 清除快取 API 具有冪等性，也就是說，如果您嘗試清除已從快取中逐出之索引的快取，不會產生任何額外效果。

此 API 作業僅適用於使用 `faiss` 與 `nmslib`（已淘汰）引擎建立的索引。對使用 `lucene` 引擎建立的索引沒有任何效果。
{: .note}

#### 範例請求

下列請求會從快取中清除三個索引的原生程式庫索引：

```json
POST /_plugins/_knn/clear_cache/index1,index2,index3?pretty
```
{% include copy-curl.html %}

回應包含此作業的分片計數：

```json
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```

`total` 參數表示此 API 嘗試從快取中清除的分片數量。回應同時包含已清除的分片數量，以及此外掛程式未能清除的分片數量。

k-NN 清除快取 API 可搭配索引模式使用，以從快取中清除一或多個符合指定模式的索引，如下列範例所示：

```json
POST /_plugins/_knn/clear_cache/index*?pretty
```
{% include copy-curl.html %}

回應包含此作業的分片計數：

```json
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```

在作業完成或請求逾時之前，此 API 呼叫不會傳回結果。如果請求逾時，作業仍會在叢集上繼續執行。若要監視請求，請使用 `_tasks` API，如下列範例所示：

```json
GET /_tasks
```
{% include copy-curl.html %}

作業完成後，請使用 [k-NN `_stats` API 操作](#stats) 查看哪些索引已從快取中清除。

## 取得模型

GET 模型操作會擷取叢集中現有模型的相關資訊。部分原生函式庫索引組態需要先進行訓練步驟，才能開始編製索引和查詢。訓練的輸出是一個模型，可用於在編製索引期間初始化原生函式庫索引檔案。模型會序列化並儲存在 k-NN 模型系統索引中。

#### 範例請求

```json
GET /_plugins/_knn/models/{model_id}
```
{% include copy-curl.html %}

### 回應本文欄位

下表列出可用的回應本文欄位。

回應欄位 |  說明
:--- | :---
`model_id` | 所取得模型的唯一識別碼。
`model_blob` | 序列化模型的 Base64 編碼字串。
`state` | 模型目前的狀態，可以是 `created`、`failed` 或 `training`。
`timestamp` | 模型建立的日期與時間。
`description` | 使用者提供的模型描述。
`error` | 說明模型為何處於失敗狀態的錯誤訊息。
`space_type` | 模型訓練時使用的空間類型，例如歐幾里得或餘弦。注意：此值可以在請求的最上層設定。
`dimension` | 此模型所設計之向量空間的維度。
`engine` | 用來建立模型的原生程式庫，即 `faiss` 或 `nmslib`（已淘汰）。 
`training_node_assignment` | 訓練模型所在的節點。
`model_definition` | 用來訓練模型的方法組態，包括方法 `name` 及其 `parameters`。
`data_type` | 用來訓練模型之向量的資料類型。
`model_version` | 建立模型時的 OpenSearch 版本。

#### 範例請求

下列範例示範如何使用 k-NN 外掛程式 API 擷取特定模型的相關資訊。

下列範例會傳回該模型所有可用的資訊：

```json
GET /_plugins/_knn/models/test-model?pretty
```
{% include copy-curl.html %}

回應包含模型資訊：

```json
{
  "model_id" : "test-model",
  "model_blob" : "SXdGbIAAAAAAAAAAAA...",
  "state" : "created",
  "timestamp" : "2021-11-15T18:45:07.505369036Z",
  "description" : "Default",
  "error" : "",
  "space_type" : "l2",
  "dimension" : 128,
  "engine" : "faiss",
  "training_node_assignment" : "1P2BbY_5Snq0CRMzKuWm_Q",
  "model_definition" : {
    "name" : "ivf",
    "parameters" : {
      "nprobes" : 1,
      "nlist" : 128,
      "encoder" : {
        "name" : "pq",
        "parameters" : {
          "code_size" : 8
        }
      }
    }
  },
  "data_type" : "float",
  "model_version" : "3.9.0"
}
```

下列範例示範如何選擇性擷取欄位：

```json
GET /_plugins/_knn/models/test-model?pretty&filter_path=model_id,state
```
{% include copy-curl.html %}

回應只包含所請求的欄位：

```json
{
  "model_id" : "test-model",
  "state" : "created"
}
```

## 搜尋模型

您可以使用 OpenSearch 查詢來搜尋索引中的模型。將 `GET` 或 `POST` 請求傳送至 `_plugins/_knn/models/_search` 端點。`size` 查詢參數必須介於 1 到 1,000 之間。

#### 範例請求

下列範例示範如何在 OpenSearch 叢集中搜尋 k-NN 模型，以及如何擷取這些模型的中繼資料，但排除可能非常龐大的 `model_blob` 欄位：

```json
GET /_plugins/_knn/models/_search?pretty&_source_excludes=model_blob
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應包含模型資訊：

```json
{
    "took" : 0,
    "timed_out" : false,
    "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
    },
    "hits" : {
      "total" : {
          "value" : 1,
          "relation" : "eq"
      },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : ".opensearch-knn-models",
        "_id" : "test-model",
        "_score" : 1.0,
        "_source" : {
          "model_version" : "3.9.0",
          "model_definition" : "{\"name\":\"ivf\",\"parameters\":{\"nprobes\":1,\"nlist\":128,\"encoder\":{\"name\":\"pq\",\"parameters\":{\"code_size\":8}}}}",
          "engine" : "faiss",
          "space_type" : "l2",
          "data_type" : "FLOAT",
          "description" : "Default",
          "model_id" : "test-model",
          "state" : "created",
          "error" : "",
          "training_node_assignment" : "1P2BbY_5Snq0CRMzKuWm_Q",
          "dimension" : 128,
          "timestamp" : "2021-11-15T18:45:07.505369036Z"
        }
      }
    ]
  }
}
```

## 刪除模型

您可以使用 DELETE 操作來刪除叢集中的模型。請參閱下列使用範例。

#### 範例請求

以下範例說明如何刪除 k-NN 模型：

```json
DELETE /_plugins/_knn/models/{model_id}
```
{% include copy-curl.html %}

回應確認模型已刪除：

```json
{
  "model_id": "test-model",
  "result": "deleted"
}
```

## 訓練模型

您可以建立並訓練模型，用於在編製索引期間初始化 k-NN 原生程式庫索引。此 API 會從訓練索引中的 `knn_vector` 欄位提取訓練資料，建立並訓練模型，然後將其序列化至模型系統索引。訓練資料必須符合請求本文中傳入的維度。訓練開始時就會傳回此請求的回應。若要監視模型的狀態，請使用[取得模型 API](#get-a-model)。

### 路徑參數

下表列出可用的路徑參數。

路徑參數 |  說明
:--- | :---
`model_id` | 模型的唯一識別碼。若未指定，則會產生隨機 ID。選用。 

### 查詢參數

下表列出可用的查詢參數。

查詢參數 | 說明
:--- | :---
`preference` | 執行訓練程序時偏好的節點 ID。若提供此參數，且指定的節點具備必要的能力與可用資源，則會使用該節點進行訓練。選用。

### 請求本文欄位

下表列出可用的請求本文欄位。

請求欄位 |  說明
:--- | :---
`training_index` | 擷取訓練資料的來源索引。
`training_field` | `training_index` 中擷取訓練資料的 `knn_vector` 欄位。此欄位的維度必須與此請求中傳入的 `dimension` 相符。  
`dimension` | 所訓練模型的維度。
`max_training_vector_count` | 訓練索引中用於訓練的向量數量上限。預設為索引中的所有向量。選用。
`search_size` | 訓練資料是使用捲動查詢從訓練索引中取得。此參數定義每次捲動查詢傳回的結果數量。有效值範圍為 `1` 到 `10000`。預設為 `10000`。選用。
`description` | 使用者提供的模型描述。選用。
`method` | 用於搜尋作業的近似 k-NN 方法組態。如需可用方法的更多資訊，請參閱[方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。此方法必須經過訓練才有效。若 `mode` 與 `compression_level` 皆未設定，則此為必要。
`space_type` | 此模型訓練所用的空間類型，例如歐幾里得或餘弦。注意：此值也可以在 `method` 參數中設定。
`engine` | 用於訓練模型的引擎。預設為 `faiss`。注意：此值也可以在 `method` 參數中設定。選用。
`mode` | 向量工作負載模式，可為 `on_disk` 或 `in_memory`。如需更多資訊，請參閱[向量工作負載模式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#vector-workload-modes)。選用。
`compression_level` | 向量的壓縮層級。如需更多資訊，請參閱[壓縮層級]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#compression-levels)。選用。
`data_type` | 訓練向量的資料類型。預設為 `float`。選用。
   
#### 範例請求

下列範例示範如何為 k-NN 模型啟動訓練程序：

```json
POST /_plugins/_knn/models/{model_id}/_train?preference={node_id}
{
    "training_index": "train-index-name",
    "training_field": "train-field-name",
    "dimension": 16,
    "max_training_vector_count": 1200,
    "search_size": 100,
    "description": "My model",
    "space_type": "l2",
    "method": {
        "name":"ivf",
        "engine":"faiss",
        "parameters":{
            "nlist":128,
            "encoder":{
                "name":"pq",
                "parameters":{
                    "code_size":8
                }
            }
        }
    }
}
```
{% include copy-curl.html %}


```json
POST /_plugins/_knn/models/_train?preference={node_id}
{
    "training_index": "train-index-name",
    "training_field": "train-field-name",
    "dimension": 16,
    "max_training_vector_count": 1200,
    "search_size": 100,
    "description": "My model",
    "space_type": "l2",
    "method": {
        "name":"ivf",
        "engine":"faiss",
        "parameters":{
            "nlist":128,
            "encoder":{
                "name":"pq",
                "parameters":{
                    "code_size":8
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
    "model_id": "dcdwscddscsad"
}
```
