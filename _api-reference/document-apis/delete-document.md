---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除文件"
parent: Document APIs
nav_order: 15
redirect_from:
 - /opensearch/rest-api/document-apis/delete-document/
---

# 刪除文件 API
**於 1.0 版導入**
{: .label .label-purple }

刪除文件 API 會從索引中移除文件。您必須同時指定索引名稱與文件 ID。文件被刪除時，OpenSearch 會遞增其版本號，並在下次區段合併時將其標記為待移除。

<!-- spec_insert_start
api: delete
component: endpoints
-->
## 端點
```json
DELETE /{index}/_doc/{id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: delete
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `id` | **必要** | 字串 | 文件的唯一識別碼。 |
| `index` | **必要** | 字串 | 目標索引的名稱。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `if_seq_no` | 整數 | 僅當文件具有此序號時才執行刪除操作。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |
| `if_primary_term` | 整數 | 僅當文件具有此主要任期 (primary term) 時才執行刪除操作。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |
| `refresh` | 布林值或字串 | 控制刪除操作所做的變更何時對搜尋可見。有效值為 `true`（立即重新整理）、`false`（預設，不重新整理）與 `wait_for`（在回應前等待重新整理）。請參閱[重新整理](#refresh)。 |
| `routing` | 字串 | 用於將操作路由至特定分片的自訂值。若文件在編製索引時使用了路由值，則此參數為必要。請參閱[路由](#routing)。 |
| `timeout` | 時間 | 等待主要分片變成可用的時間長度。預設為 `1m`（1 分鐘）。請參閱[逾時](#timeout)。 |
| `version` | 整數 | 用於並行控制的明確版本號。指定的版本必須與文件目前的版本相符，請求才會成功。請參閱[版本控制](#versioning)。 |
| `version_type` | 列舉 | 指定版本類型：`internal`（預設）、`external` 或 `external_gte`。使用 `external` 時，版本號必須大於目前的版本。使用 `external_gte` 時，則必須大於或等於。請參閱[版本控制](#versioning)。 |
| `wait_for_active_shards` | 字串 | 在繼續進行操作之前必須處於作用中的分片複本數量。預設為 `1`（僅主要分片）。可設為 `all`，或設為最多為索引分片複本總數（`number_of_replicas+1`）的任何正整數。請參閱[等待作用中的分片](#wait-for-active-shards)。 |

## 範例請求

下列範例請求會從 `products` 索引中刪除 ID 為 `1` 的文件：

<!-- spec_insert_start
component: example_code
rest: DELETE /products/_doc/1
-->
{% capture step1_rest %}
DELETE /products/_doc/1
{% endcapture %}

{% capture step1_python %}


response = client.delete(
  id = "1",
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列範例回應顯示成功的刪除操作：

```json
{
  "_index" : "products",
  "_id" : "1",
  "_version" : 9,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 45,
  "_primary_term" : 1
}
```

## 回應本文欄位

回應本文包含刪除操作與受影響文件的相關資訊。

欄位 | 說明
:--- | :---
`_index` | 文件被刪除的索引名稱。
`_id` | 被刪除文件的唯一識別碼。
`_version` | 文件刪除後的新版本號。每次刪除操作都會遞增版本號。
`result` | 刪除操作的結果。若文件成功刪除則傳回 `deleted`，若文件不存在則傳回 `not_found`。
`_shards` | 包含刪除操作所涉及分片的相關資訊。
`_shards.total` | 應已確認刪除操作的分片總數（主要與副本）。
`_shards.successful` | 成功處理刪除操作的分片數量。
`_shards.failed` | 處理刪除操作失敗的分片數量。當此值大於 0 時，`failures` 陣列會包含失敗的詳細資訊。
`_seq_no` | 指派給刪除操作的序號。序號用於樂觀並行控制。
`_primary_term` | 刪除操作當下的主要任期。此值與 `_seq_no` 搭配用於樂觀並行控制。

## 樂觀並行控制

刪除操作透過 `if_seq_no` 與 `if_primary_term` 參數支援樂觀並行控制。當您指定這些參數時，OpenSearch 只有在文件目前的序號與主要任期符合所提供的值時，才會執行刪除操作。若不相符，OpenSearch 會傳回狀態碼為 `409` 的 `version_conflict_engine_exception` 錯誤，表示文件自您上次擷取後已被修改。

下列範例請求僅在文件的序號為 `43` 且主要任期為 `1` 時才刪除該文件：

<!-- spec_insert_start
component: example_code
rest: DELETE /products/_doc/3?if_seq_no=43&if_primary_term=1
-->
{% capture step1_rest %}
DELETE /products/_doc/3?if_seq_no=43&if_primary_term=1
{% endcapture %}

{% capture step1_python %}


response = client.delete(
  id = "3",
  index = "products",
  params = { "if_seq_no": "43", "if_primary_term": "1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若文件目前的序號或主要任期與指定的值不符，OpenSearch 會傳回狀態碼為 `409` 的版本衝突錯誤。

## 版本控制

對文件的每次寫入操作（包括刪除）都會遞增文件的版本號。文件被刪除後，其版本號會在短時間內保持可用，以支援並行操作。此版本資訊的保留時間由 `index.gc_deletes` 索引設定控制，預設為 60 秒。這讓 OpenSearch 能夠正確處理並行的刪除請求，並在所有副本之間維持一致性。

## 自動建立索引

當您使用外部版本控制變體（`version_type=external` 或 `version_type=external_gte`）時，若指定的索引不存在，刪除操作會自動建立該索引。此行為僅發生於外部版本控制類型，不適用於預設的內部版本控制。

下列範例請求會自動建立 `auto-created-index` 索引，因為它使用外部版本控制：

<!-- spec_insert_start
component: example_code
rest: DELETE /auto-created-index/_doc/1?version=5&version_type=external
-->
{% capture step1_rest %}
DELETE /auto-created-index/_doc/1?version=5&version_type=external
{% endcapture %}

{% capture step1_python %}


response = client.delete(
  id = "1",
  index = "auto-created-index",
  params = { "version": "5", "version_type": "external" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

由於文件不存在，此操作會傳回 `not_found` 結果，但索引會作為副作用被建立。若未使用外部版本控制，嘗試從不存在的索引中刪除文件會傳回 `index_not_found_exception` 錯誤。

## 路由

當文件以特定路由值編製索引時，OpenSearch 會使用該值來決定由哪個分片儲存文件。若要刪除已路由的文件，您必須提供與編製索引時相同的路由值。若您的索引具有將 `_routing` 設為 `required` 的對應，而您嘗試在未指定路由值的情況下刪除文件，OpenSearch 會以 `RoutingMissingException` 拒絕該請求。

下列範例請求會刪除以路由值 `electronics` 編製索引的文件：

<!-- spec_insert_start
component: example_code
rest: DELETE /products/_doc/2?routing=electronics
-->
{% capture step1_rest %}
DELETE /products/_doc/2?routing=electronics
{% endcapture %}

{% capture step1_python %}


response = client.delete(
  id = "2",
  index = "products",
  params = { "routing": "electronics" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若沒有正確的路由值，OpenSearch 無法在適當的分片上找到文件，刪除操作將會失敗。

## 分散式執行

當您傳送刪除請求時，OpenSearch 會對文件 ID 進行雜湊運算以決定目標分片。接著請求會被路由至該分片群組中的主要分片。主要分片處理完刪除操作後，變更會複製到同一分片群組中的所有副本分片，以確保叢集之間的一致性。

## 重新整理

預設情況下，被刪除的文件只有在下一次索引重新整理後才會對搜尋操作可見，而索引重新整理預設每秒執行一次。您可以使用 `refresh` 參數控制此行為：

- `false`（預設）：刪除操作立即傳回，變更會在下一次自動重新整理後變為可見。
- `true`：OpenSearch 在刪除操作後立即重新整理所有受影響的分片，使變更立即對搜尋操作可見。此選項會影響效能，應謹慎使用。
- `wait_for`：刪除操作會等待下一次自動重新整理後才傳回回應，確保 API 呼叫完成時變更已可見。

## 等待作用中的分片

`wait_for_active_shards` 參數控制 OpenSearch 在處理刪除請求之前必須有多少分片複本可用。預設值為 `1`，表示僅主要分片必須處於作用中。您可以將其設為 `all` 以要求所有分片複本（主要與副本）都處於作用中，或指定一個正整數以要求特定數量的作用中分片。此設定透過在確認刪除操作之前等待副本可用，有助於確保資料持久性。

## 逾時

若刪除請求送達時主要分片無法使用（例如在復原或遷移期間），OpenSearch 會等待該分片變成可用。`timeout` 參數指定在請求失敗之前要等待多久。預設逾時為 1 分鐘。若主要分片在指定的逾時期間內未變成可用，OpenSearch 會傳回錯誤。

下列範例請求設定 30 秒的自訂逾時：

<!-- spec_insert_start
component: example_code
rest: DELETE /products/_doc/4?timeout=30s
-->
{% capture step1_rest %}
DELETE /products/_doc/4?timeout=30s
{% endcapture %}

{% capture step1_python %}


response = client.delete(
  id = "4",
  index = "products",
  params = { "timeout": "30s" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 必要權限

若您使用 Security 外掛程式，請確保您具備適當的權限：`indices:data/write/delete`。
