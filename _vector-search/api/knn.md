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

OpenSearch 提供數個 k-nearest neighbors (k-NN) API，用於管理、監控及最佳化您的向量工作負載。

## Stats

k-NN `stats` API 提供 k-NN 外掛程式的目前狀態相關資訊，該外掛程式實作向量搜尋功能。這包括叢集層級與節點層級的統計資料。叢集層級統計資料對整個叢集只有單一值。節點層級統計資料對叢集中的每個節點各有一個值。您可以依 `nodeId` 與 `statName` 篩選查詢，如下列範例所示：

```json
GET /_plugins/_knn/nodeId1,nodeId2/stats/statName1,statName2
```
{% include copy-curl.html %}

### 回應本文欄位

下表列出可用的回應本文欄位。

欄位 |  說明
:--- | :---
`circuit_breaker_triggered` | 指出是否觸發斷路器。此統計資料僅與近似 k-NN 搜尋相關。
`total_load_time` | k-NN 將原生程式庫索引載入快取所花費的時間，以奈秒為單位。此統計資料僅與近似 k-NN 搜尋相關。
`eviction_count` | 因記憶體限制或閒置時間而從快取中逐出的原生程式庫索引數目。此統計資料僅與近似 k-NN 搜尋相關。<br /> **注意**：因刪除索引而發生的明確逐出不會計入。
`hit_count` | 快取命中次數。當使用者查詢已載入記憶體的原生程式庫索引時，即發生快取命中。此統計資料僅與近似 k-NN 搜尋相關。
`miss_count` | 快取未命中次數。當使用者查詢尚未載入記憶體的原生程式庫索引時，即發生快取未命中。此統計資料僅與近似 k-NN 搜尋相關。
`graph_memory_usage` | 原生程式庫索引在節點上使用的原生記憶體量，以 KB 為單位。
`graph_memory_usage_percentage` | 原生程式庫索引在節點上使用的原生記憶體量，以最大快取容量的百分比表示。
`graph_index_requests` | 將文件的 `knn_vector` 欄位新增至原生程式庫索引的請求數目。
`graph_index_errors` | 將文件的 `knn_vector` 欄位新增至原生程式庫索引而產生錯誤的請求數目。
`graph_query_requests` | 已進行的原生程式庫索引查詢數目。
`graph_query_errors` | 已產生錯誤的原生程式庫索引查詢數目。
`knn_query_requests` | 收到的 k-NN 查詢請求數目。
`cache_capacity_reached` | 是否已達到 `knn.memory.circuit_breaker.limit`。此統計資料僅與近似 k-NN 搜尋相關。
`load_success_count` | k-NN 成功將原生程式庫索引載入快取的次數。此統計資料僅與近似 k-NN 搜尋相關。
`load_exception_count` | 嘗試將原生程式庫索引載入快取時發生例外狀況的次數。此統計資料僅與近似 k-NN 搜尋相關。
`indices_in_cache` | 對於每個已開啟 `knn_vector` 欄位與近似 k-NN 的 OpenSearch 索引，此統計資料提供該 OpenSearch 索引擁有的原生程式庫索引數目，以及該 OpenSearch 索引正在使用的總 `graph_memory_usage`，以 KB 為單位。
`script_compilations` | k-NN 指令碼已編譯的次數。此值通常應為 1 或 0，但如果包含已編譯指令碼的快取已滿，k-NN 指令碼可能會重新編譯。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_compilation_errors` | 指令碼編譯期間的錯誤數目。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_query_requests` | 指令碼查詢的總數。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`script_query_errors` | 指令碼查詢期間的錯誤數目。此統計資料僅與 k-NN 評分指令碼搜尋相關。
`nmslib_initialized` | 布林值，指出節點上是否已載入並初始化 `nmslib` JNI 程式庫。
`faiss_initialized` | 布林值，指出節點上是否已載入並初始化 `faiss` JNI 程式庫。
`model_index_status` | 模型系統索引的狀態。有效值為 `red`、`yellow` 及 `green`。如果索引不存在，此值為 `null`。
`indexing_from_model_degraded` | 布林值，指出從模型編製索引是否已降級。若沒有足夠的 JVM 記憶體可快取模型，就會發生此情況。
`ing_requests` | 對節點進行的訓練請求數目。
`training_errors` | 節點上已發生的訓練錯誤數目。
`training_memory_usage` | 訓練在節點上使用的原生記憶體量，以 KB 為單位。
`training_memory_usage_percentage` | 訓練在節點上使用的原生記憶體量，以最大快取容量的百分比表示。

部分統計資料的名稱包含 *graph*。在這些情況下，*graph* 與 *native library index* 同義。*graph* 一詞反映該外掛程式僅支援 HNSW 演算法時的狀況，該演算法由階層式圖形組成。
{: .note}

#### 遠端索引建置統計資料
於 3.0 版推出 
{: .label .label-purple }

如果您已設定[遠端索引建置]({{site.url}}{{site.baseurl}}/vector-search/remote-index-build/)，回應會包含其他欄位。下表列出可用的遠端索引建置統計資料回應本文欄位。

| 欄位 | 說明 |
|:---|:---|
| `repository_stats.read_success_count` | 從儲存庫成功讀取作業的次數。 |
| `repository_stats.read_failure_count` | 從儲存庫失敗讀取作業的次數。 |
| `repository_stats.successful_read_time_in_millis` | 成功讀取作業所花費的總時間，以毫秒為單位。 |
| `repository_stats.write_success_count` | 對儲存庫成功寫入作業的次數。 |
| `repository_stats.write_failure_count` | 對儲存庫失敗寫入作業的次數。 |
| `repository_stats.successful_write_time_in_millis` | 成功寫入作業所花費的總時間，以毫秒為單位。 |
| `client_stats.build_request_success_count` | 成功建置請求作業的次數。 |
| `client_stats.build_request_failure_count` | 失敗建置請求作業的次數。 |
| `client_stats.status_request_failure_count` | 失敗狀態請求作業的次數。 |
| `client_stats.status_request_success_count` | 成功狀態請求作業的次數。 |
| `client_stats.index_build_success_count` | 成功索引建置作業的次數。 |
| `client_stats.index_build_failure_count` | 失敗索引建置作業的次數。 |
| `client_stats.waiting_time_in_ms` | 用戶端等待遠端建置完成所花費的總時間，以毫秒為單位。 |
| `build_stats.remote_index_build_flush_time_in_millis` | 遠端排清作業所花費的總時間，以毫秒為單位。 |
| `build_stats.remote_index_build_merge_time_in_millis` | 遠端合併作業所花費的總時間，以毫秒為單位。 |
| `build_stats.remote_index_build_current_merge_operations` | 目前進行中的遠端合併作業數目。 |
| `build_stats.remote_index_build_current_flush_operations` | 目前進行中的遠端排清作業數目。 |
| `build_stats.remote_index_build_current_merge_size` | 遠端合併作業的目前大小。 |
| `build_stats.remote_index_build_current_flush_size` | 遠端排清作業的目前大小。 |

#### 範例請求

下列範例示範如何擷取與 k-NN 外掛程式相關的統計資料。

下列範例會擷取叢集中所有節點上 k-NN 外掛程式的完整統計資料：

```json
GET /_plugins/_knn/stats?pretty
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
        "graph_memory_usage_percentage" : 3.68,
        "graph_query_requests" : 1420920,
        "graph_memory_usage" : 2,
        "cache_capacity_reached" : false,
        "load_success_count" : 179,
        "training_memory_usage" : 0,
        "indices_in_cache" : {
            "myindex" : {
                "graph_memory_usage" : 2,
                "graph_memory_usage_percentage" : 3.68,
                "graph_count" : 2
            }
        },
        "script_query_errors" : 0,
        "hit_count" : 1420775,
        "knn_query_requests" : 147092,
        "total_load_time" : 2436679306,
        "miss_count" : 179,
        "training_memory_usage_percentage" : 0.0,
        "graph_index_requests" : 656,
        "faiss_initialized" : true,
        "load_exception_count" : 0,
        "training_errors" : 0,
        "eviction_count" : 0,
        "nmslib_initialized" : false,
        "script_compilations" : 0,
        "script_query_requests" : 0,
        "graph_query_errors" : 0,
        "indexing_from_model_degraded" : false,
        "graph_index_errors" : 0,
        "training_requests" : 17,
        "script_compilation_errors" : 0
    }
  }
}
```
{% include copy-curl.html %}

下列範例會擷取單一節點的特定指標（斷路器狀態與圖形記憶體使用量）：

```json
GET /_plugins/_knn/HYMrXXsBSamUkcAjhjeN0w/stats/circuit_breaker_triggered,graph_memory_usage?pretty
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
{% include copy-curl.html %}

## 預熱作業

用於執行近似 k-NN 搜尋的原生程式庫索引，會以特殊檔案的形式與其他 Apache Lucene 分段檔案一併儲存。若要使用 k-NN 外掛程式對這些索引執行搜尋，外掛程式必須將這些檔案載入原生記憶體。

如果外掛程式尚未將檔案載入原生記憶體，則會在收到搜尋請求時載入。載入時間可能會在初始查詢時造成高延遲。為避免此問題，使用者通常會在預熱期間執行隨機查詢。預熱期間結束後，檔案已載入原生記憶體，即可啟動生產工作負載。此載入過程是間接的，需要額外的工夫。

或者，您可以對想要搜尋的索引執行 k-NN 外掛程式預熱 API 作業，以避免此延遲問題。此作業會將請求中指定之所有索引的所有分片（主要與副本）的原生程式庫檔案載入原生記憶體。

程序完成後，您即可搜尋這些索引，而不會產生初始延遲。預熱 API 作業具有冪等性，因此如果某個分段的原生程式庫檔案已載入記憶體，此作業不會產生任何效果。它只會載入目前未儲存在記憶體中的檔案。

#### 範例請求

下列請求會對三個索引執行預熱：

```json
GET /_plugins/_knn/warmup/index1,index2,index3?pretty
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```
{% include copy-curl.html %}

`total` 值表示 k-NN 外掛程式嘗試預熱的分片數量。回應中也包含外掛程式成功預熱與預熱失敗的分片數量。

在預熱作業完成或請求逾時之前，此呼叫不會傳回結果。如果請求逾時，作業會繼續在叢集上執行。若要監視預熱作業，請使用 OpenSearch `_tasks` API：

```json
GET /_tasks
```
{% include copy-curl.html %}

作業完成後，請使用 [k-NN `_stats` API 作業](#stats) 查看 k-NN 外掛程式載入圖形中的內容。

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

下列請求會將三個索引的原生程式庫索引從快取中逐出：

```json
POST /_plugins/_knn/clear_cache/index1,index2,index3?pretty
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```
{% include copy-curl.html %}

`total` 參數表示 API 嘗試從快取中清除的分片數量。回應包含已清除的分片數量，以及外掛程式清除失敗的分片數量。

k-NN 清除快取 API 可搭配索引模式使用，從快取中清除一或多個符合指定模式的索引，如下列範例所示：

```json
POST /_plugins/_knn/clear_cache/index*?pretty
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```
{% include copy-curl.html %}

在作業完成或請求逾時之前，API 呼叫不會傳回結果。如果請求逾時，作業會繼續在叢集上執行。若要監視請求，請使用 `_tasks` API，如下列範例所示：

```json
GET /_tasks
```
{% include copy-curl.html %}

作業完成後，請使用 [k-NN `_stats` API 作業](#stats) 查看哪些索引已從快取中逐出。

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
`model_id` | 所擷取模型的唯一識別碼。
`model_blob` | 序列化模型的 Base64 編碼字串。
`state` | 模型的目前狀態，可為 `created`、`failed` 或 `training`。
`timestamp` | 建立模型的日期和時間。
`description` | 使用者提供的模型說明。
`error` | 說明模型為何處於失敗狀態的錯誤訊息。
`space_type` | 訓練模型所用的空間類型，例如 Euclidean 或 cosine。注意：此值可在請求的最上層設定。
`dimension` | 此模型所設計之向量空間的維度。
`engine` | 用於建立模型的原生函式庫，可為 `faiss` 或 `nmslib` (已棄用)。

#### 範例請求

下列範例示範如何使用 k-NN 外掛程式 API 擷取特定模型的相關資訊。

下列範例會傳回模型的所有可用資訊：

```json
GET /_plugins/_knn/models/test-model?pretty
{
  "model_id" : "test-model",
  "model_blob" : "SXdGbIAAAAAAAAAAAA...",
  "state" : "created",
  "timestamp" : "2021-11-15T18:45:07.505369036Z",
  "description" : "Default",
  "error" : "",
  "space_type" : "l2",
  "dimension" : 128,
  "engine" : "faiss" 
}
```
{% include copy-curl.html %}

下列範例示範如何選擇性地擷取欄位：

```json
GET /_plugins/_knn/models/test-model?pretty&filter_path=model_id,state
{
  "model_id" : "test-model",
  "state" : "created"
}
```
{% include copy-curl.html %}

## 搜尋模型

您可以使用 OpenSearch 查詢來搜尋索引中的模型。請參閱下列使用範例。

#### 範例請求

下列範例示範如何在 OpenSearch 叢集中搜尋 k-NN 模型，以及如何擷取這些模型的中繼資料，並排除可能很大的 `model_blob` 欄位：

```json
GET/POST /_plugins/_knn/models/_search?pretty&_source_excludes=model_blob
{
    "query": {
         ...
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
          "engine" : "faiss",
          "space_type" : "l2",
          "description" : "Default",
          "model_id" : "test-model",
          "state" : "created",
          "error" : "",
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

下列範例示範如何刪除 k-NN 模型：

```json
DELETE /_plugins/_knn/models/{model_id}
{
  "model_id": {model_id},
  "acknowledged": true
}
```
{% include copy-curl.html %}

## 訓練模型

您可以建立並訓練模型，用於在編製索引期間初始化 k-NN 原生函式庫索引。此 API 會從訓練索引中的 `knn_vector` 欄位提取訓練資料，建立並訓練模型，然後將其序列化至模型系統索引。訓練資料必須符合請求本文中傳入的維度。訓練開始時會傳回此請求。若要監視模型的狀態，請使用 [Get model API](#get-a-model)。

### 查詢參數

下表列出可用的查詢參數。

查詢參數 |  說明
:--- | :---
`model_id` | 所擷取模型的唯一識別碼。若未指定，則會產生隨機 ID。選用。
`node_id` | 指定執行訓練程序的偏好節點。若有提供，且指定的節點具備必要的能力和可用資源，則會使用該節點進行訓練。選用。

### 請求本文欄位

下表列出可用的請求本文欄位。

請求欄位 |  說明
:--- | :---
`training_index` | 從中擷取訓練資料的索引。
`training_field` | `training_index` 中從中擷取訓練資料的 `knn_vector` 欄位。此欄位的維度必須符合此請求中傳入的 `dimension`。  
`dimension` | 所訓練模型的維度。
`max_training_vector_count` | 訓練索引中用於訓練的向量數量上限。預設為索引中的所有向量。選用。
`search_size` | 訓練資料是使用 scroll 查詢從訓練索引提取。此參數定義每個 scroll 查詢要傳回的結果數。預設為 `10000`。選用。
`description` | 使用者提供的模型說明。選用。
`method` | 用於搜尋操作的近似 k-NN 方法組態。如需可用方法的詳細資訊，請參閱 [方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。此方法需要訓練才能生效。
`space_type` | 訓練此模型所用的空間類型，例如 Euclidean 或 cosine。注意：此值也可在 `method` 參數中設定。

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
