---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: operations
parent: Anatomy of a workload
nav_order: 30
---

<!-- vale off -->
# operations 元素
<!-- vale on -->

`operations` 元素會列出工作負載所執行的 OpenSearch API 操作，以及這些操作的參數化方式。舉例來說，您可以定義一個名為 `create-index` 的操作，在基準測試叢集中建立索引，讓 OpenSearch Benchmark 可以將文件寫入其中。[`schedule`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/schedule/) 元素接著會依名稱參照這些操作，以指定它們的執行順序。

<!-- vale off -->
## bulk
<!-- vale on -->

`bulk` 操作類型可讓您以工作形式執行 [bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 請求。

### 用法

下列範例顯示一個 `bulk` 操作類型，其 `bulk-size` 為 `5000` 份文件：

```yml
{
  "name": "index-append",
  "operation-type": "bulk",
  "bulk-size": 5000
}
```
{% include copy.html %}

### 在用戶端之間分割文件

當您有多個 `clients` 時，OpenSearch Benchmark 會依據設定的用戶端數量分割每份文件。使用多個 `clients` 可將大量索引操作平行化，但不會保留每份文件的匯入順序。舉例來說，如果 `clients` 設為 `2`，其中一個用戶端會從開頭開始將文件編製索引，而另一個用戶端則會從中段開始將文件編製索引。

如果有多份文件或多個語料庫，OpenSearch Benchmark 會嘗試以下列兩種方式平行地將所有文件編製索引：

1. 每個用戶端會從語料庫中的不同位置開始。舉例來說，在具有 2 個語料庫和 5 個用戶端的工作負載中，用戶端 1、3 和 5 會從第一個語料庫開始，而用戶端 2 和 4 則從第二個語料庫開始。
2. 每個用戶端會獲指派多份文件。用戶端 1 會從第一個語料庫第一份文件的第一個分割開始，接著移至第二個語料庫第一份文件的第一個分割，依此類推。

### 組態選項

使用下列選項來自訂 `bulk` 操作。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bulk-size` | 是 | 數字 | 指定要在大量請求中匯入的文件數量。
`ingest-percentage` | 否 | 範圍 [0, 100] | 定義要編製索引的文件語料庫比例。有效值為 0 到 100 之間的數字。
`corpora` | 否 | 清單 | 定義大量操作應以哪些文件語料庫名稱為目標。只有在 `corpora` 區段包含多個文件語料庫，且您不想在大量請求期間將它們全部編製索引時才需要。
`indices` | 否 | 清單 | 定義大量索引操作中應使用哪些索引。OpenSearch Benchmark 只會選取具有相符 `target-index` 的文件檔案。
`batch-size` | 否 | 數字 | 定義 OpenSearch Benchmark 同時讀取多少份文件。這是專家級設定，僅用於避免非常小的大量大小所造成的意外瓶頸。如果您要以 `1` 的 `bulk-size` 進行基準測試，您應設定較高的 `batch-size`。
`pipeline` | 否 | 字串 | 定義要使用哪個現有的資料匯入管線。
`conflicts` | 否 | 字串 | 定義要模擬的索引 `conflicts` 類型。若未指定，則不會模擬任何類型。有效值為 ‘sequential’，會將文件 ID 取代為依序遞增的文件 ID，以及 ‘random’，會將文件 ID 取代為隨機文件 ID。
`conflict-probability` | 否 | 百分比 | 定義發生衝突時要取代多少份文件。結合 `conflicts=sequential` 和 `conflict-probability=0` 會讓 OpenSearch Benchmark 自行產生索引 ID，而不使用 OpenSearch 的自動 ID 產生功能。有效值為 0 到 100 之間的數字。預設為 `25%`。
`on-conflict` | 否 | 字串 |  決定 OpenSearch 在 ID 衝突時應使用 `index` 或 `update` 索引動作。預設為 `index`，會在 ID 衝突期間建立新索引。
`recency` | 否 | 數字 | 使用 0 到 1 之間的數字來表示新近程度。新近程度越接近 `1`，衝突 ID 就越偏向較新的 ID。新近程度越接近 0，則會將所有 ID 納入 ID 衝突的考量。
`detailed-results` | 否 | 布林值 | 記錄大量請求更詳細的 [中繼資料](#metadata)。由於 OpenSearch Benchmark 會更詳細地分析對應的大量回應，因此可能會產生額外負荷，而導致測量結果偏差。此屬性必須設為 `true`，OpenSearch Benchmark 才會記錄個別大量請求的失敗。
`timeout` | 否 | 持續時間 | 定義 OpenSearch 在完成下列操作的處理之前，每個動作等待的時間量 (以分鐘為單位)：自動建立索引、動態對應更新，以及等待作用中的分片。預設為 `1m`。
`refresh` | 否 | 字串 | 控制使用 `refresh` Bulk API 查詢參數之大量請求的 OpenSearch 重新整理行為。有效值為 `true`，會在背景重新整理目標分片；`wait_for`，會封鎖大量請求直到受影響的分片重新整理完成；以及 `false`，會使用預設的重新整理行為。

### 中繼資料

`bulk` 操作一律會傳回下列中繼資料：

- `index`：受影響索引的名稱。如果無法推導出索引，則會傳回 `null`。
- `weight`：大量大小的操作無關表示法，以 `units` 表示。
- `unit`：用來解讀 `weight` 的單位。
- `success`：布林值，指出 `bulk` 請求是否成功。
- `success-count`：請求中成功處理的大量項目數。此值會在發生錯誤，或已在文件中指定 `bulk-size` 時決定。
- `error-count`：請求中失敗的大量項目數。
- `took`：大量回應中 `took` 屬性的值。

如果 `detailed-results` 為 `true`，則會傳回下列中繼資料：

- `ops`：以操作名稱為索引鍵的巢狀文件，例如 `index`、`update` 或 `delete`，並以各種計數為值。`item-count` 包含此索引鍵的項目總數。此外，OpenSearch Benchmark 會為每個結果傳回個別的計數器，例如已建立項目數或已刪除項目數的結果。
- `shards_histogram`：雜湊的陣列，每個雜湊都有兩個索引鍵。`item-count` 索引鍵包含套用分片分佈的項目數。`shards` 索引鍵包含具有 `total`、`successful` 和 `failed` 分片實際分佈的雜湊。
- `bulk-request-size-bytes`：大量請求本文的總大小，以位元組為單位。
- `total-document-size-bytes`：大量請求本文中所有文件的總大小，以位元組為單位。

<!-- vale off -->
## create-index
<!-- vale on -->

`create-index` 操作會執行 [Create Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。它支援下列兩種索引建立模式：

- 建立工作負載 `indices` 區段中指定的所有索引
- 建立操作本身內定義的一個特定索引

### 用法

下列範例會建立工作負載 `indices` 區段中定義的所有索引。它會使用工作負載中定義的所有索引設定，但覆寫分片數：

```yml
{
  "name": "create-all-indices",
  "operation-type": "create-index",
  "settings": {
    "index.number_of_shards": 1
  },
  "request-params": {
    "wait_for_active_shards": "true"
  }
}
```
{% include copy.html %}

下列範例會建立新索引，並在操作本文中指定所有索引設定：

```yml
{
  "name": "create-an-index",
  "operation-type": "create-index",
  "index": "people",
  "body": {
    "settings": {
      "index.number_of_shards": 0
    },
    "mappings": {
      "docs": {
        "properties": {
          "name": {
            "type": "text"
          }
        }
      }
    }
  }
}
```
{% include copy.html %}

### 組態選項

從工作負載的 `indices` 區段建立所有索引時，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`settings` | 否 | 陣列 |  指定要與工作負載的 `indices` 區段中指定的索引設定合併的額外索引設定。
`request-params` | 否 | 設定清單 | 包含 Create Index API 允許的任何請求參數。OpenSearch Benchmark 不會嘗試將參數序列化，而是以其目前狀態傳遞參數。

在操作中建立單一索引時，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 是 | 字串 | 索引名稱。
`body` | 否 | 請求本文 | Create Index API 的請求本文。如需詳細資訊，請參閱 [Create Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`request-params` | 否 | 設定清單 | 包含 Create Index API 允許的任何請求參數。OpenSearch Benchmark 不會嘗試將參數序列化，而是以其目前狀態傳遞參數。

### 中繼資料

`create-index` 操作會傳回下列中繼資料：

- `weight`：操作建立的索引數量。
- `unit`：一律為 `ops`，表示工作負載內的操作數量。
- `success`：表示操作是否成功的布林值。

<!-- vale off -->
## delete-index
<!-- vale on -->

`delete-index` 操作會執行 [Delete Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index/)。與 [`create-index`](#create-index) 操作相同，您可以刪除工作負載的 `indices` 區段中找到的所有索引，或根據傳入 `index` 設定的字串刪除一或多個索引。

### 用法

下列範例會刪除工作負載的 `indices` 區段中找到的所有索引：

```yml
{
  "name": "delete-all-indices",
  "operation-type": "delete-index"
}
```
{% include copy.html %}

下列範例會刪除所有 `logs_*` 索引：

```yml
{
  "name": "delete-logs",
  "operation-type": "delete-index",
  "index": "logs-*",
  "only-if-exists": false,
  "request-params": {
    "expand_wildcards": "all",
    "allow_no_indices": "true",
    "ignore_unavailable": "true"
  }
}
```
{% include copy.html %}

### 組態選項

刪除工作負載的 `indices` 區段中指定的所有索引時，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`only-if-exists` | 否 | 布林值 | 決定是否應刪除現有索引。預設為 `true`。
`request-params` | 否 | 設定清單 | 包含 Create Index API 允許的任何請求參數。OpenSearch Benchmark 不會嘗試將參數序列化，而是以其目前狀態傳遞參數。

如果您想根據 `index` 選項中指定的模式刪除一或多個索引，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 是 | 字串 | 您想刪除的一或多個索引。
`only-if-exists` | 否 | 布林值 | 決定索引存在時是否應刪除該索引。預設為 `true`。
`request-params` | 否 | 設定清單 | 包含 Create Index API 允許的任何請求參數。OpenSearch Benchmark 不會嘗試將參數序列化，而是以其目前狀態傳遞參數。

### 中繼資料

`delete-index` 操作會傳回下列中繼資料：

- `weight`：操作建立的索引數量。
- `unit`：一律為 `ops`，表示工作負載內的操作數量。
- `success`：表示操作是否成功的布林值。

<!-- vale off -->
## cluster-health
<!-- vale on -->

`cluster-health` 操作會執行 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)，此 API 會檢查叢集健康狀態，並根據為 `request-params` 設定的參數傳回預期狀態。如果傳回非預期的叢集健康狀態，操作就會回報失敗。您可以使用 OpenSearch Benchmark `run` 命令中的 `--on-error` 選項，控制 OpenSearch Benchmark 在健康檢查失敗時的行為。


### 用法

下列範例會建立 `cluster-health` 操作，檢查任何 `log-*` 索引是否處於 `green` 健康狀態：

```yml
{
  "name": "check-cluster-green",
  "operation-type": "cluster-health",
  "index": "logs-*",
  "request-params": {
    "wait_for_status": "green",
    "wait_for_no_relocating_shards": "true"
  },
  "retry-until-success": true
}

```
{% include copy.html %}

### 組態選項

請搭配 `cluster-health` 操作使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 是 | 字串 | 您想評估的一或多個索引。
`request-params` | 否 | 設定清單 | 包含 Cluster Health API 允許的任何請求參數。OpenSearch Benchmark 不會嘗試將參數序列化，而是以其目前狀態傳遞參數。

### 中繼資料

`cluster-health` 操作會傳回下列中繼資料：

- `weight`：`cluster-health` 操作評估的索引數量。一律為 `1`，因為操作會對每個索引執行一次。
- `unit`：一律為 `ops`，表示工作負載內的操作數量。
- `success`：表示操作是否成功的布林值。
- `cluster-status`：目前的叢集狀態。
- `relocating-shards`：目前正在重新配置至其他節點的分片數量。

<!-- vale off -->
## refresh
<!-- vale on -->

`refresh` 操作會執行 Refresh API。`operation` 不會傳回任何中繼資料。

### 用法

下列範例會重新整理所有 `logs-*` 索引：

```yml
{
 "name": "refresh",
 "operation-type": "refresh",
 "index": "logs-*"
}
```
{% include copy.html %}

### 組態選項

`refresh` 操作使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 否 | 字串 | 要重新整理的索引或資料串流名稱。

<!-- vale off -->
## search
<!-- vale on -->

`search` 操作會執行 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search/)，您可以使用此 API 在 OpenSearch Benchmark 索引中執行查詢。

### 用法

下列範例會在 `search` 操作內執行 `match_all` 查詢：

```yml
{
  "name": "default",
  "operation-type": "search",
  "body": {
    "query": {
      "match_all": {}
    }
  },
  "request-params": {
    "_source_include": "some_field",
    "analyze_wildcard": "false"
  }
}
```
{% include copy.html %}

### 組態選項

`search` 操作使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 否 | 字串 | 查詢的目標索引或資料串流。只有在 `indices` 區段包含兩個或更多索引時，才需要此選項。否則，OpenSearch Benchmark 會自動推導要使用的索引或資料串流。指定 `"index": "_all"` 可查詢工作負載中的所有索引。
`cache` | 否 | 布林值 | 指定是否使用查詢請求快取。OpenSearch Benchmark 不會定義任何值。預設值取決於基準測試候選項目的設定和 OpenSearch 版本。
`request-params` | 否 | 設定清單 | 包含 Search API 允許的任何請求參數。
`body` | 是 | 請求本文 | 指示要使用的查詢和查詢參數。
`detailed-results` | 否 | 布林值 | 記錄關於查詢的更詳細中繼資料。設定為 `true` 時，可能會產生額外負擔，導致測量結果偏差。此選項不適用於 `scroll` 查詢。
`results-per-page` | 否 | 整數 | 指定每頁要擷取的文件數量。此選項對應至 Search API 的 `size` 參數，可用於捲動和非捲動搜尋。預設為 `10`。

### 中繼資料

下列中繼資料一律會傳回：

- `weight`：作業的「權重」。一般查詢一律為 `1`，而 scroll 查詢則為擷取的頁數。
- `unit`：用來解讀權重的單位，一般查詢為 `ops`，scroll 查詢為 `pages`。
- `success`：布林值，指出查詢是否成功。

若將 `detailed-results` 設為 `true`，也會傳回下列中繼資料：

- `hits`：查詢的命中總數。
- `hits_relation`：命中數是精確的（`eq`），還是實際命中數的下限（`gte`）。
- `timed_out`：查詢是否逾時。對於 scroll 查詢，若發出的任一查詢此旗標為 `true`，則此旗標為 `true`。
 - `took`：查詢回應中 `took` 屬性的值。對於 scroll 查詢，此值為所有查詢回應中所有 `took` 值的總和。

<!-- vale off -->
## paginated-search
<!-- vale on -->

`paginated-search` 作業會使用 [`search_after`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter) 參數執行一連串的分頁搜尋請求。它接受的選項與 `search` 相同，另加上 `pages`，用來控制要擷取的頁數。

### 組態選項

除了 [`search`](#search) 底下所列的選項之外：

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`pages` | 是 | 整數 | 要擷取的頁數上限。若查詢傳回的相符結果少於要求的頁數，作業會提前終止。

### 中繼資料

除了 `search` 傳回的中繼資料之外：

- `pages`：擷取的頁數總計。

<!-- vale off -->
## scroll-search
<!-- vale on -->

`scroll-search` 作業會執行 [scroll 搜尋]({{site.url}}{{site.baseurl}}/api-reference/scroll/)。它接受的選項與 `search` 相同，另加上 `pages`，用來控制要擷取的 scroll 頁數。

### 組態選項

除了 [`search`](#search) 底下所列的選項之外：

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`pages` | 是 | 整數 | 要擷取的 scroll 頁數上限。若在達到此數量前 scroll 已用盡，作業會提前終止。

### 中繼資料

除了 `search` 傳回的中繼資料之外：

- `pages`：擷取的 scroll 頁數總計。

<!-- vale off -->
## force-merge
<!-- vale on -->

`force-merge` 作業會執行 [Force Merge API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/)。

### 使用方式

```yml
{
  "name": "force-merge",
  "operation-type": "force-merge",
  "index": "_all",
  "request-params": {
    "max_num_segments": 1
  }
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 否 | 字串 | 要強制合併的索引。若省略，呼叫會沿用底層用戶端的預設行為，以所有索引為目標。
`max-num-segments` | 否 | 整數 | 每個分片的目標分段數。以 `max_num_segments` 傳遞至 Force Merge API。
`mode` | 否 | 字串 | 設為 `polling` 可非同步發出強制合併，並輪詢 Tasks API 直到完成。省略時，呼叫會同步等待，在大型索引上可能逾時。
`poll-period` | 有條件 | 數字 | 當 `mode` 為 `polling` 時為必要：狀態輪詢之間的秒數。若設定 `mode: polling` 但未提供此值，作業會引發錯誤。
`request-params` | 否 | 物件 | 傳遞至 Force Merge API 的額外請求參數。

這是管理作業。預設不會回報指標。可將 `include-in-reporting` 設為 `true` 來強制回報。

<!-- vale off -->
## index-stats
<!-- vale on -->

`index-stats` 作業會執行 [Index Stats API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/)。

### 使用方式

```yml
{
  "name": "index-stats",
  "operation-type": "index-stats",
  "index": "_all",
  "condition": {
    "path": "_all.total.merges.current",
    "expected-value": 0
  },
  "retry-until-success": true
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 否 | 字串 | 要擷取統計資料的索引。預設為 `_all`。
`condition` | 否 | 物件 | 要在回應中檢查的條件。包含 `path`（回應中的點記法路徑）與 `expected-value`。
`request-params` | 否 | 物件 | 傳遞至 Stats API 的請求參數。

<!-- vale off -->
## node-stats
<!-- vale on -->

`node-stats` 作業會執行 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)。

### 使用方式

```yml
{
  "name": "node-stats",
  "operation-type": "node-stats"
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`request-timeout` | 否 | 數字 | Nodes Stats 請求的用戶端逾時（秒）。

<!-- vale off -->
## vector-search
<!-- vale on -->

`vector-search` 作業會執行 k-NN 向量搜尋查詢，並可選擇性地將結果與基準真相鄰近項目比較，以計算召回率指標。

### 使用方式

```yml
{
  "name": "knn-search",
  "operation-type": "vector-search",
  "index": "vectors",
  "k": 100,
  "body": {
    "query": {
      "knn": {
        "embedding": {
          "vector": [0.1, 0.2, 0.3],
          "k": 100
        }
      }
    }
  }
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 是 | 字串 | 目標索引。必要：省略會導致底層 `search` 執行器發生錯誤。
`body` | 是 | 物件 | 包含 k-NN 查詢的搜尋請求本文。
`k` | 否 | 整數 | 要擷取的最近鄰數量。用於召回率計算。
`detailed-results` | 否 | 布林值 | 是否記錄詳細中繼資料。
`calculate-recall` | 否 | 布林值 | 是否針對基準真相鄰近項目計算 recall@k 與 recall@1。預設為 `true`。
`neighbors` | 否 | 陣列 | 用於召回率計算的基準真相鄰近項目 ID。通常由工作負載在執行階段提供。

### 中繼資料

- `weight`：一律為 `1`。
- `unit`：一律為 `ops`。
- `success`：搜尋是否成功。
- `recall@k`：k 的召回率（若有提供基準真相鄰近項目）。
- `recall@1`：1 的召回率（若有提供基準真相鄰近項目）。

<!-- vale off -->
## bulk-vector-data-set
<!-- vale on -->

`bulk-vector-data-set` 作業會從 HDF5 或 BigANN 資料集檔案大量編製向量資料的索引。支援在部分失敗時重試個別文件。

### 使用方式

```yml
{
  "name": "bulk-vectors",
  "operation-type": "bulk-vector-data-set",
  "bulk-size": 500,
  "index": "vectors"
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bulk-size` | 否 | 整數 | 每個大量請求的文件數。
`index` | 否 | 字串 | 目標索引。
`retries` | 否 | 整數 | 初始請求失敗後的重試次數。預設為 `0`（不重試）。重試時會重新提交每個失敗的文件；連線逾時也會觸發重試。
`retry-wait-period` | 否 | 數字 | 重試之間的初始等待期間（秒）。預設為 `0.5`。
`retry-max-wait-period` | 否 | 數字 | 重試之間的最長等待期間（秒）（指數退避以此值為上限）。預設為 `60`。
`detailed-results` | 否 | 布林值 | 記錄每份文件的詳細成功／失敗中繼資料。預設為 `true`。
`action-metadata-present` | 否 | 布林值 | 大量本文是否包含動作中繼資料行。預設為 `true`。
`unit` | 否 | 字串 | `weight` 所回報的單位。預設為 `docs`。

<!-- vale off -->
## put-pipeline
<!-- vale on -->

`put-pipeline` 操作會建立或更新[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)。

### 使用方式

```yml
{
  "name": "define-pipeline",
  "operation-type": "put-pipeline",
  "id": "my-pipeline",
  "body": {
    "description": "My ingest pipeline",
    "processors": [
      {
        "set": {
          "field": "ingest_time",
          "value": {% raw %}"{{_ingest.timestamp}}"{% endraw %}
        }
      }
    ]
  }
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`id` | 是 | 字串 | 管線 ID。
`body` | 是 | 物件 | 管線定義。

這是管理操作。預設不會回報指標。

<!-- vale off -->
## delete-pipeline
<!-- vale on -->

`delete-pipeline` 操作會刪除資料匯入管線。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`id` | 是 | 字串 | 要刪除的管線 ID。

這是管理操作。預設不會回報指標。

<!-- vale off -->
## create-search-pipeline
<!-- vale on -->

`create-search-pipeline` 操作會建立[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`id` | 是 | 字串 | 搜尋管線 ID。
`body` | 是 | 物件 | 搜尋管線定義。

這是管理操作。預設不會回報指標。

<!-- vale off -->
## update-concurrent-segment-search-settings
<!-- vale on -->

`update-concurrent-segment-search-settings` 操作會切換[並行分段搜尋]({{site.url}}{{site.baseurl}}/search-plugins/concurrent-segment-search/)叢集設定，並可選擇性地切換最大切片數量。此操作會將 `search.concurrent_segment_search.enabled`（以及提供時的 `search.concurrent.max_slice_count`）更新為永久叢集設定。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`enable` | 否 | 布林值 | 是否啟用並行分段搜尋。預設為 `false`。
`max_slice_count` | 否 | 整數 | 每個分片的最大切片數量。若省略，則此設定維持不變。

<!-- vale off -->
## put-settings
<!-- vale on -->

`put-settings` 操作會更新[叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。

### 使用方式

```yml
{
  "name": "increase-watermarks",
  "operation-type": "put-settings",
  "body": {
    "transient": {
      "cluster.routing.allocation.disk.watermark.low": "95%"
    }
  }
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`body` | 是 | 物件 | 要套用的叢集設定。

這是管理操作。預設不會回報指標。

<!-- vale off -->
## create-data-stream
<!-- vale on -->

`create-data-stream` 操作會建立一個或多個[資料串流]({{site.url}}{{site.baseurl}}/opensearch/data-streams/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`data-streams` | 是 | 清單 | 要建立的資料串流名稱清單。
`request-params` | 是 | 物件 | 轉送至 Create Data Stream API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## delete-data-stream
<!-- vale on -->

`delete-data-stream` 操作會刪除一個或多個資料串流。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`data-streams` | 是 | 清單 | 要刪除的資料串流名稱清單。
`only-if-exists` | 是 | 布林值 | 若為 `true`，則僅刪除已存在的資料串流；若為 `false`，則嘗試刪除每個資料串流，並忽略 HTTP 404 回應。
`request-params` | 是 | 物件 | 轉送至 Delete Data Stream API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## create-composable-template
<!-- vale on -->

`create-composable-template` 操作會建立一個或多個[可組合索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | 要建立的 `[template-name, body]` 配對清單。
`request-params` | 是 | 物件 | 轉送至 API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## delete-composable-template
<!-- vale on -->

`delete-composable-template` 操作會刪除一個或多個可組合索引範本，並可選擇性地刪除其符合的索引。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | `[template-name, delete-matching-indices, index-pattern]` 三元組清單。當 `delete-matching-indices` 為 `true` 且 `index-pattern` 不為空時，符合該模式的索引也會一併刪除。
`only-if-exists` | 是 | 布林值 | 若為 `true`，則僅刪除已存在的範本；若為 `false`，則嘗試刪除每個範本，並忽略 HTTP 404 回應。
`request-params` | 是 | 物件 | 轉送至 API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## create-component-template
<!-- vale on -->

`create-component-template` 操作會建立一個或多個[元件範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/component-template/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | 要建立的 `[template-name, body]` 配對清單。
`request-params` | 是 | 物件 | 轉送至 API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## delete-component-template
<!-- vale on -->

`delete-component-template` 操作會刪除一個或多個元件範本。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | 要刪除的元件範本名稱清單。
`only-if-exists` | 是 | 布林值 | 若為 `true`，則僅刪除已存在的範本；若為 `false`，則嘗試刪除每個範本，並忽略 HTTP 404 回應。
`request-params` | 是 | 物件 | 轉送至 API 的請求參數。若不需要任何參數，請傳入空物件（`{}`）。

<!-- vale off -->
## create-index-template
<!-- vale on -->

`create-index-template` 操作會建立一個或多個舊版索引範本。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | 要建立的 `[template-name, body]` 配對清單。
`request-params` | 否 | 物件 | 其他請求參數。

<!-- vale off -->
## delete-index-template
<!-- vale on -->

`delete-index-template` 操作會刪除一個或多個舊版索引範本，並可選擇性地刪除其符合的索引。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`templates` | 是 | 清單 | `[template-name, delete-matching-indices, index-pattern]` 三元組清單。
`only-if-exists` | 否 | 布林值 | 若為 `true`，則僅刪除已存在的範本。預設為 `false`。
`request-params` | 否 | 物件 | 其他請求參數。

<!-- vale off -->
## shrink-index
<!-- vale on -->

`shrink-index` 操作使用 [Shrink Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shrink-index/) 來減少索引中的主要分片數量。

### 用法

```yml
{
  "name": "shrink-index",
  "operation-type": "shrink-index",
  "source-index": "my-index",
  "target-index": "my-index-shrunk",
  "target-body": {
    "settings": {
      "index.number_of_shards": 1,
      "index.codec": "best_compression"
    }
  }
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source-index` | 是 | 字串 | 要縮減的來源索引 (或萬用字元模式)。
`target-index` | 是 | 字串 | 縮減後索引的名稱。當 `source-index` 符合多個索引時，符合的後綴會附加到此名稱。
`target-body` | 是 | 物件 | 目標索引的設定與對應。
`shrink-node` | 否 | 字串 | 在縮減之前，來源分片要配置到的節點。若省略，則隨機選擇一個資料節點。

<!-- vale off -->
## create-snapshot-repository
<!-- vale on -->

`create-snapshot-repository` 操作會建立[快照儲存庫]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`repository` | 是 | 字串 | 儲存庫名稱。
`body` | 是 | 物件 | 儲存庫定義 (類型、設定)。
`request-params` | 否 | 物件 | 其他請求參數。

<!-- vale off -->
## delete-snapshot-repository
<!-- vale on -->

`delete-snapshot-repository` 操作會刪除快照儲存庫。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`repository` | 是 | 字串 | 要刪除的儲存庫名稱。

<!-- vale off -->
## create-snapshot
<!-- vale on -->

`create-snapshot` 操作會建立[快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`repository` | 是 | 字串 | 儲存庫名稱。
`snapshot` | 是 | 字串 | 快照名稱。
`body` | 是 | 物件 | 快照定義。
`wait-for-completion` | 否 | 布林值 | 是否在返回前等待快照完成。預設為 `false`。若要準確評測快照持續時間，請保持此值為 `false`，並接著使用 `wait-for-snapshot-create`。
`request-params` | 否 | 物件 | 其他請求參數。

<!-- vale off -->
## wait-for-snapshot-create
<!-- vale on -->

`wait-for-snapshot-create` 操作會輪詢快照狀態，直到快照達到 `SUCCESS`。若快照以 `FAILED` 結束，此操作會引發斷言錯誤。回報的指標包含快照大小 (位元組)、輸送量與持續時間。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`repository` | 是 | 字串 | 儲存庫名稱。
`snapshot` | 是 | 字串 | 快照名稱。
`completion-recheck-wait-period` | 否 | 數字 | 狀態輪詢之間的秒數。預設為 `1`。

<!-- vale off -->
## restore-snapshot
<!-- vale on -->

`restore-snapshot` 操作會還原快照。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`repository` | 是 | 字串 | 儲存庫名稱。
`snapshot` | 是 | 字串 | 快照名稱。
`body` | 否 | 物件 | 還原請求本文。
`wait-for-completion` | 否 | 布林值 | 是否在返回前等待還原完成。預設為 `false`。搭配 `wait-for-recovery` 使用可評測還原持續時間。
`request-params` | 否 | 物件 | 其他請求參數。

<!-- vale off -->
## wait-for-recovery
<!-- vale on -->

`wait-for-recovery` 操作會透過輪詢 [Index Recovery API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/recover/) 等待索引復原完成。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | 是 | 字串 | 要監視復原的索引。
`completion-recheck-wait-period` | 否 | 數字 | 復原輪詢之間的秒數。預設為 `1`。

<!-- vale off -->
## submit-async-search
<!-- vale on -->

`submit-async-search` 操作會提交[非同步搜尋]({{site.url}}{{site.baseurl}}/search-plugins/async/)請求，並將傳回的非同步搜尋 ID 儲存在操作 `name` 之下，讓同一複合操作中的後續操作可以擷取或刪除它。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 操作名稱。其他操作會參照此名稱來查詢產生的非同步搜尋 ID。
`body` | 是 | 物件 | 搜尋請求本文。
`index` | 否 | 字串 | 目標索引。
`request-params` | 否 | 物件 | 轉送至 Asynchronous Search API 的其他請求參數。

<!-- vale off -->
## get-async-search
<!-- vale on -->

`get-async-search` 操作會從一或多個先前提交的非同步搜尋擷取結果。只有當所有被參照的搜尋都已完成 (`is_running: false`) 時，此操作才會成功。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`retrieve-results-for` | 是 | 字串或清單 | 要擷取結果的 `submit-async-search` 操作名稱 (或名稱清單)。
`request-params` | 否 | 物件 | 轉送至 Asynchronous Search Get API 的其他請求參數。

<!-- vale off -->
## delete-async-search
<!-- vale on -->

`delete-async-search` 操作會刪除一或多個非同步搜尋結果。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`delete-results-for` | 是 | 字串或清單 | 要刪除結果的 `submit-async-search` 操作名稱 (或名稱清單)。

<!-- vale off -->
## create-point-in-time
<!-- vale on -->

`create-point-in-time` 操作會為索引建立 [Point in Time (PIT)]({{site.url}}{{site.baseurl}}/search-plugins/point-in-time/)。產生的 PIT ID 會儲存在操作 `name` 之下，讓同一複合操作中的後續操作可以參照它。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 操作名稱。其他操作會參照此名稱來重複使用產生的 PIT ID。
`index` | 是 | 字串 | 目標索引。
`keep-alive` | 否 | 字串 | PIT 的存活時間 (例如 `5m`)。預設為 `1m`。
`request-params` | 否 | 物件 | 轉送至 Create PIT API 的其他請求參數。

<!-- vale off -->
## delete-point-in-time
<!-- vale on -->

`delete-point-in-time` 操作會刪除一或多個 PIT。若已設定 `with-point-in-time-from`，則只會刪除由該指定操作建立的 PIT；否則，叢集上的所有 PIT 都會被刪除。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`with-point-in-time-from` | 否 | 字串 | 要刪除其 PIT 的 `create-point-in-time` 操作名稱。若省略，則刪除所有 PIT。
`request-params` | 否 | 物件 | 轉送至 Delete PIT API 的其他請求參數。

<!-- vale off -->
## list-all-point-in-time
<!-- vale on -->

`list-all-point-in-time` 操作會列出叢集上所有作用中的 PIT。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`request-params` | 否 | 物件 | 轉送至 List PIT API 的其他請求參數。

<!-- vale off -->
## create-transform
<!-- vale on -->

`create-transform` 操作會建立[索引轉換]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`transform-id` | 是 | 字串 | 轉換 ID。
`body` | 是 | 物件 | 轉換定義。

<!-- vale off -->
## start-transform
<!-- vale on -->

`start-transform` 操作會啟動先前建立的轉換。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`transform-id` | 是 | 字串 | 要啟動的轉換 ID。
`timeout` | 否 | 數字 | 啟動請求的選用用戶端逾時時間。

<!-- vale off -->
## wait-for-transform
<!-- vale on -->

`wait-for-transform` 操作會輪詢轉換狀態，直到轉換到達下一個檢查點 (或停止，視選項而定)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`transform-id` | 是 | 字串 | 要監視的轉換 ID。
`force` | 否 | 布林值 | 輪詢完成時強制停止轉換。預設為 `false`。
`wait-for-checkpoint` | 否 | 布林值 | 等待所有資料處理至下一個檢查點。預設為 `true`。
`wait-for-completion` | 否 | 布林值 | 封鎖直到轉換完全停止。預設為 `true`。
`transform-timeout` | 否 | 數字 | 整體轉換執行逾時秒數。預設為 `3600`。
`poll-interval` | 否 | 數字 | 輪詢轉換統計資料的頻率 (秒)。預設為 `0.5`。

<!-- vale off -->
## delete-transform
<!-- vale on -->

`delete-transform` 操作會刪除先前建立的轉換。缺少的轉換 (HTTP 404) 會被忽略，因此此操作可安全地做為清理步驟使用。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`transform-id` | 是 | 字串 | 要刪除的轉換 ID。
`force` | 否 | 布林值 | 若為 `true`，即使轉換目前正在執行也會將其刪除。預設為 `false`。

<!-- vale off -->
## train-knn-model
<!-- vale on -->

`train-knn-model` 操作會使用 [Train Model API]({{site.url}}{{site.baseurl}}/vector-search/api/knn/#train-a-model) 訓練 k-NN 模型，並輪詢直到訓練完成。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`body` | 是 | 物件 | 訓練請求本文。請參閱 [Train Model API]({{site.url}}{{site.baseurl}}/vector-search/api/knn/#train-a-model) 以了解本文參數。
`model_id` | 是 | 字串 | 要訓練的模型 ID。
`retries` | 否 | 整數 | 放棄前輪詢重試的次數上限。預設為 `1000`。
`poll_period` | 否 | 數字 | 狀態輪詢之間的秒數。預設為 `0.5`。

<!-- vale off -->
## delete-knn-model
<!-- vale on -->

`delete-knn-model` 操作會刪除已訓練的 k-NN 模型。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`model_id` | 是 | 字串 | 要刪除的模型 ID。
`ignore-if-model-does-not-exist` | 否 | 布林值 | 若為 `true`，將缺少的模型 (HTTP 404) 視為成功。預設為 `false`。

<!-- vale off -->
## register-ml-model
<!-- vale on -->

`register-ml-model` 操作會使用 [ML Commons API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/) 註冊機器學習模型。執行器會先搜尋名稱相符的模型；若已存在，則重複使用現有的模型 ID。否則，它會提交新的註冊請求並輪詢直到完成。產生的模型 ID 會寫入工作目錄中的 `model_id.json`，以便後續操作取用。

您可以用下列兩種方式的其中一種提供請求本文：將 `model-config-file` 設為磁碟上的路徑，或設定 `model-name`、`model-version` 和 `model-format`，讓 OpenSearch Benchmark 為您組合本文。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`model-config-file` | 否 | 字串 | 包含完整註冊本文之 JSON 檔案的路徑。若設定此項，其他本文欄位會被忽略。
`model-name` | 否 | 字串 | 模型名稱。在未設定 `model-config-file` 時用於組合本文。
`model-version` | 否 | 字串 | 模型版本。
`model-format` | 否 | 字串 | 模型格式 (例如 `TORCH_SCRIPT`)。
`timeout` | 否 | 數字 | 等待註冊工作完成的秒數上限。預設為 `120`。

<!-- vale off -->
## deploy-ml-model
<!-- vale on -->

`deploy-ml-model` 操作會部署 (載入) 先前註冊的 ML 模型。模型 ID 會從工作目錄中的 `model_id.json` 讀取 (通常由先前的 `register-ml-model` 操作寫入)，因此此操作沒有必要參數。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`timeout` | 否 | 數字 | 等待部署工作完成的秒數上限。預設為 `120`。

<!-- vale off -->
## create-ml-connector
<!-- vale on -->

`create-ml-connector` 操作會建立 [ML 連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/) 以整合遠端模型。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`body` | 是 | 物件 | 連接器定義。

<!-- vale off -->
## delete-ml-connector
<!-- vale on -->

`delete-ml-connector` 操作會依名稱查詢 ML 連接器並將其刪除。若沒有連接器符合提供的名稱，則此操作不會執行任何動作。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`connector_name` | 是 | 字串 | 要查詢並刪除的連接器名稱。

<!-- vale off -->
## register-remote-ml-model
<!-- vale on -->

`register-remote-ml-model` 操作會註冊由 [ML 連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/) 支援的遠端 ML 模型。它會輪詢註冊工作直到完成，然後將產生的模型 ID 寫入工作目錄中的 `model_id.json`，以便後續操作取用。

若請求本文中未設定 `connector_id`，OpenSearch Benchmark 會從工作目錄中的 `connector_id.json` 讀取 (通常由先前的 `create-ml-connector` 操作寫入)。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`body` | 是 | 物件 | 模型註冊請求本文。若省略 `connector_id`，則會從 `connector_id.json` 載入。

<!-- vale off -->
## delete-ml-model
<!-- vale on -->

`delete-ml-model` 操作會依名稱查詢模型，取消部署目前部署的任何模型，然後將其刪除。多個名稱相同的模型 (例如跨版本) 都會一併刪除。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`model-name` | 是 | 字串 | 要查詢並刪除的模型名稱。
`number-of-hits-to-return` | 否 | 整數 | 從搜尋查詢擷取的相符模型數量上限。預設為 `1000`。
`undeploy-timeout` | 否 | 數字 | 刪除前等待每個模型完全取消部署的秒數。預設為 `10`。

<!-- vale off -->
## raw-request
<!-- vale on -->

`raw-request` 操作會向 OpenSearch 傳送任意的 HTTP 請求。此操作適用於沒有專屬操作類型涵蓋的操作。

### 用法

```yml
{
  "name": "check-shard-count",
  "operation-type": "raw-request",
  "method": "GET",
  "path": "/_cat/shards?v",
  "body": {}
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`method` | 否 | 字串 | HTTP 方法（`GET`、`POST`、`PUT`、`DELETE`）。預設為 `GET`。
`path` | 是 | 字串 | URL 路徑。必須以 `/` 開頭。
`body` | 否 | 物件 | 請求本文。
`request-params` | 否 | 物件 | 查詢字串參數。
`headers` | 否 | 物件 | 要包含的 HTTP 標頭。
`ignore` | 否 | 清單 | 要忽略的 HTTP 狀態碼（例如 `[404]`）。

<!-- vale off -->
## sleep
<!-- vale on -->

`sleep` 操作會暫停執行一段指定的時間。

### 用法

```yml
{
  "name": "wait-before-search",
  "operation-type": "sleep",
  "duration": 30
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`duration` | 是 | 數字 | 暫停時間（秒）。

<!-- vale off -->
## composite
<!-- vale on -->

`composite` 操作會將一組結構化的內部操作作為單一測量單位執行，並可選擇使用平行子串流。當多個請求需要共用狀態（例如建立 PIT、使用它進行搜尋，然後刪除它），或您想測量小型工作流程的端對端耗時時，此操作非常實用。

只有部分操作類型可以出現在 `composite` 中：`create-point-in-time`、`delete-point-in-time`、`list-all-point-in-time`、`search`、`paginated-search`、`raw-request`、`sleep`、`submit-async-search`、`get-async-search` 和 `delete-async-search`。巢狀的 `stream` 區塊會平行執行。

### 用法

```yml
{
  "name": "pit-search-workflow",
  "operation-type": "composite",
  "requests": [
    { "operation-type": "create-point-in-time", "name": "pit", "index": "my-index" },
    { "operation-type": "search", "body": { "query": { "match_all": {} } } },
    { "operation-type": "delete-point-in-time", "with-point-in-time-from": "pit" }
  ]
}
```
{% include copy.html %}

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`requests` | 是 | 清單 | 要執行的內部操作或 `stream` 區塊清單。
`max-connections` | 否 | 整數 | 整個 composite 中並行進行中請求數量的上限。預設為無上限。

<!-- vale off -->
## produce-stream-message
<!-- vale on -->

`produce-stream-message` 操作會將訊息發布至已設定的 `message-producer`（例如 Kafka producer），用於串流匯入基準測試。`body` 會依換行符分割，每個非中繼資料行都會作為個別訊息傳送。Producer 是在工作負載或叢集層級設定---執行器本身只取得 producer 參照和訊息承載。

### 組態選項

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`message-producer` | 是 | Producer | 用於傳送訊息的 producer 執行個體（由工作負載在執行階段解析）。
`body` | 是 | 字串或位元組 | 以換行符分隔的訊息承載。索引中繼資料行（`{"index": {"_index": ...}}`）會被略過。

<!-- vale off -->
## proto-bulk
<!-- vale on -->

`proto-bulk` 操作會使用 gRPC 傳輸（而非 HTTP REST）傳送大量索引請求。目標叢集必須啟用 gRPC。

### 組態選項

與 `bulk` 相同，但使用 gRPC 序列化（Protocol Buffers）而非透過 HTTP 的 JSON。使用 `--grpc-target-hosts` 指定 gRPC 端點。

<!-- vale off -->
## proto-search
<!-- vale on -->

`proto-search` 操作會使用 gRPC 傳輸傳送搜尋請求。

### 組態選項

與 `search` 相同，但使用 gRPC。使用 `--grpc-target-hosts` 指定 gRPC 端點。

<!-- vale off -->
## proto-vector-search
<!-- vale on -->

`proto-vector-search` 操作會使用 gRPC 傳輸傳送向量搜尋請求。

### 組態選項

與 `vector-search` 相同，但使用 gRPC。使用 `--grpc-target-hosts` 指定 gRPC 端點。

<!-- vale off -->
## proto-bulk-vector-data-set
<!-- vale on -->

`proto-bulk-vector-data-set` 操作會使用 gRPC 傳輸大量索引向量資料集。它是 `bulk-vector-data-set` 的 gRPC 對應版本。

### 組態選項

與 `bulk-vector-data-set` 相同，但使用 gRPC 序列化（Protocol Buffers）而非透過 HTTP 的 JSON。使用 `--grpc-target-hosts` 指定 gRPC 端點。
