---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "編製文件索引"
parent: Document APIs
nav_order: 1
redirect_from: 
 - /opensearch/rest-api/document-apis/index-document/
---

# Index Document API
**於 1.0 版推出**
{: .label .label-purple}

Index Document API 會將 JSON 文件新增至指定的索引，並使其可供搜尋。如果已存在具有相同 ID 的文件，此 API 會更新該文件並遞增其版本號碼。


## 端點

```json
PUT {index}/_doc/{id}
POST {index}/_doc

PUT {index}/_create/{id}
POST {index}/_create/{id}
```

使用下列端點組合來控制文件的索引編製方式：

- `PUT {index}/_doc/{id}`：新增具有指定 ID 的文件，或更新具有相同 ID 的現有文件。
- `POST {index}/_doc`：新增文件，並自動產生唯一的 ID。
- `PUT {index}/_create/{id}` 或 `POST {index}/_create/{id}`：僅在尚未存在具有該 ID 的文件時，才新增具有指定 ID 的文件。如果文件已存在，操作就會失敗。


## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 索引的名稱。如果索引不存在，OpenSearch 會自動建立索引，除非已停用自動建立索引功能。必要。 |
| `id` | 字串 | 唯一的文件 ID。使用 PUT 時為必要參數。使用 POST 時，省略此參數可讓 OpenSearch 自動產生唯一的 ID。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `if_seq_no` | 整數 | 僅在文件目前的序號符合指定值時執行操作。用於樂觀並行控制。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |
| `if_primary_term` | 整數 | 僅在文件目前的主要任期符合指定值時執行操作。用於樂觀並行控制。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |
| `op_type` | 列舉 | 操作類型。有效值為 `create`（僅在文件尚不存在時編製其索引）和 `index`（建立新文件或更新現有文件）。如果指定了文件 ID，預設值為 `index`。否則，預設值為 `create`。 |
| `pipeline` | 字串 | 用於在編製索引前預先處理文件的資料匯入管線 ID。 |
| `routing` | 字串 | 用於將操作路由至特定分片的自訂路由值。請參閱[路由](#routing)。 |
| `refresh` | 列舉 | 是否在操作後重新整理受影響的分片。有效值為 `true`（立即重新整理）、`false`（不重新整理）和 `wait_for`（等待重新整理發生後再回應）。預設值為 `false`。請參閱[重新整理](#refresh)。 |
| `timeout` | 時間 | 主要分片無法使用時，等待其恢復可用的時間。預設值為 `1m`。請參閱[逾時](#timeout)。 |
| `version` | 整數 | 用於並行控制的明確版本號碼。僅在文件目前的版本符合此值時，才會編製其索引。請參閱[版本控制](#versioning)。 |
| `version_type` | 列舉 | 用於外部版本控制的版本類型。有效值為 `external`（僅在指定版本大於儲存的版本時編製索引）和 `external_gte`（僅在指定版本大於或等於儲存的版本時編製索引）。預設值為 `internal`。請參閱[版本控制](#versioning)。 |
| `wait_for_active_shards` | 字串 | 繼續執行操作前所需的作用中分片複本數量。有效值為 `all`，或不超過分片總數的正整數。預設值為 `1`（僅主要分片）。請參閱[等待作用中的分片](#wait-for-active-shards)。 |
| `require_alias` | 布林值 | 目標索引名稱是否必須為索引別名。如果為 `true` 且目標不是別名，請求就會失敗。預設值為 `false`。 |

## 請求範例

下列請求範例會為名為 `sample_index` 的索引建立範例索引文件。


### PUT 請求範例

<!-- spec_insert_start
component: example_code
rest: PUT /sample_index/_doc/1
body: |
{
  "name": "Example",
  "price": 29.99,
  "description": "To be or not to be, that is the question"
}
-->
{% capture step1_rest %}
PUT /sample_index/_doc/1
{
  "name": "Example",
  "price": 29.99,
  "description": "To be or not to be, that is the question"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "sample_index",
  id = "1",
  body =   {
    "name": "Example",
    "price": 29.99,
    "description": "To be or not to be, that is the question"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### POST 請求範例

<!-- spec_insert_start
component: example_code
rest: POST /sample_index/_doc
body: |
{
  "name": "Another Example",
  "price": 19.99,
  "description": "We are such stuff as dreams are made on"
}
-->
{% capture step1_rest %}
POST /sample_index/_doc
{
  "name": "Another Example",
  "price": 19.99,
  "description": "We are such stuff as dreams are made on"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "sample_index",
  body =   {
    "name": "Another Example",
    "price": 19.99,
    "description": "We are such stuff as dreams are made on"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "_index": "sample-index",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_index` | 字串 | 文件新增至的索引名稱。 |
| `_id` | 字串 | 文件的唯一識別碼。 |
| `_version` | 整數 | 文件的版本號碼。每次更新文件時都會遞增。 |
| `result` | 字串 | 索引編製操作的結果。可能的值為 `created`（已建立新文件）和 `updated`（已更新現有文件）。 |
| `_shards` | 物件 | 複寫程序的資訊。 |
| `_shards.total` | 整數 | 應執行操作的分片複本（主要分片和副本）數量。 |
| `_shards.successful` | 整數 | 操作成功的分片複本數量。操作成功時，此值至少為 1（主要分片）。 |
| `_shards.failed` | 整數 | 操作失敗的分片複本數量。如果操作成功，此值為 0。 |
| `_seq_no` | 整數 | 此次索引編製操作指派給文件的序號。序號用於確保文件的舊版本不會覆寫新版本。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |
| `_primary_term` | 整數 | 此次索引編製操作指派給文件的主要任期。請參閱[樂觀並行控制](#optimistic-concurrency-control)。 |


## 自動建立索引

預設情況下，如果指定的索引不存在，Index Document API 會自動建立索引，並套用任何已設定的索引範本。如果沒有明確的對應，API 也會為新欄位建立動態對應。

自動建立索引由 `action.auto_create_index` 設定控制。此設定的預設值為 `true`，允許自動建立任何索引。您可以修改此設定，根據特定模式允許或阻擋索引建立，或完全停用自動建立索引。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。

## 樂觀並行控制

您可以使用 `if_seq_no` 和 `if_primary_term` 參數，根據文件目前的序號和主要任期進行條件式索引。這可確保只有在文件自您上次擷取後未經修改時，操作才會成功。

例如，若要僅在文件的序號為 3 且主要任期為 1 時更新文件，請在請求中包含這些參數：

```json
PUT sample-index/_doc/1?if_seq_no=3&if_primary_term=1
{
  "name": "Updated Example",
  "price": 39.99
}
```

如果序號或主要任期與目前的值不符，OpenSearch 會傳回版本衝突錯誤（HTTP 409），讓您能擷取最新版本並重試操作。

## 自動產生 ID

當您使用 POST 方法而未指定文件 ID 時，OpenSearch 會自動為文件產生唯一的 ID。`op_type` 會自動設為 `create`，確保一律建立新文件。

下列範例在未指定 ID 的情況下將文件編製索引，讓 OpenSearch 自動產生 ID：

```json
POST sample-index/_doc
{
  "user": "john_doe",
  "post_date": "2024-01-15T10:30:00",
  "message": "Hello, OpenSearch!"
}
```

回應包含自動產生的 ID：

```json
{
  "_index": "sample-index",
  "_id": "W0tpsmIBdwcYyG50zbta",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

產生的 ID 是以 Base64 編碼的 UUID，可確保在整個叢集中具有唯一性。

## 路由

預設情況下，OpenSearch 會計算文件 ID 的雜湊值，以決定由哪個分片儲存文件。您可以提供自訂的 `routing` 參數值來覆寫此行為。

下列範例根據路由值 `user123` 將文件路由至分片：

```json
POST sample-index/_doc?routing=user123
{
  "user": "john_doe",
  "message": "Hello, world!"
}
```

當您在編製索引時使用自訂路由，擷取、更新或刪除文件時，必須提供相同的路由值。否則，OpenSearch 無法找到文件。

## 分散式模型

索引操作會根據文件的路由值（文件 ID 或自訂路由值）導向主要分片。主要分片完成操作後，OpenSearch 會將更新分發至複寫群組中所有適用的副本分片。

此分散式方法可確保所有分片複本維持同步。主要分片會協調複寫程序，並等待所需數量的作用中分片確認後，才向用戶端確認操作成功。

## 等待作用中分片

為了提高寫入操作的韌性，您可以設定 Index Document API，使其在繼續執行前，先等待一定數量的分片複本進入作用中狀態。預設情況下，操作只會等待主要分片進入作用中狀態（`wait_for_active_shards=1`）。

您可以將 `wait_for_active_shards` 設為 `all`，或不超過分片複本總數（`number_of_replicas + 1`）的任何正整數。如果所需數量的作用中分片無法使用，操作會等待並重試，直到分片可用或發生逾時。

例如，假設叢集有三個節點（A、B 和 C），且某個索引的 `number_of_replicas` 設為 3，因此共有 4 個分片複本（一個主要分片和三個副本分片）。預設情況下，只要主要分片可用，索引操作就會繼續執行，即使節點 B 和 C 停機，而節點 A 託管主要分片複本，也是如此。

如果您在請求中設定 `wait_for_active_shards=3`，索引操作就需要 3 個作用中的分片複本才能繼續執行。當全部 3 個節點都在執行，且每個節點都包含一個分片複本時，就能滿足此要求。不過，如果您設定 `wait_for_active_shards=all`（或 `4`），索引操作就不會繼續執行，因為您需要全部 4 個複本都處於作用中狀態，但只有 3 個節點。除非有新節點加入叢集以託管第四個分片複本，否則操作會逾時。

下列範例要求至少有 2 個作用中的分片複本（主要分片和一個副本分片）才能繼續執行：

```json
PUT sample-index/_doc/1?wait_for_active_shards=2
{
  "name": "Example",
  "price": 29.99
}
```

此設定可降低寫入至數量不足的分片複本的風險，但無法完全消除此風險。檢查會在寫入操作開始前進行。操作開始後，即使主要分片上的操作成功，部分副本上的複寫仍可能失敗。回應中的 `_shards` 區段會指出成功或失敗的分片複本數量。

## 重新整理

`refresh` 參數控制已編製索引的文件何時可供搜尋操作查得。對於大多數使用案例，請使用預設值（`false`）以獲得最佳效能。

有效選項如下：

- `false`（預設）：文件會依照索引的重新整理間隔（預設為 1 秒）變為可供搜尋查得。
- `true`：編製索引後強制立即重新整理，使文件立即可供搜尋。請謹慎使用，因為頻繁重新整理可能對效能造成顯著影響。
- `wait_for`：等待下一次排定的重新整理後才回應。對於批次操作，比 `true` 更有效率。

## 逾時

如果您提交索引請求時主要分片無法使用（例如，在復原或重新配置期間），操作預設最多會等待 1 分鐘才失敗。您可以使用 `timeout` 參數調整此行為：

```json
PUT sample-index/_doc/1?timeout=5m
{
  "name": "Example",
  "price": 29.99
}
```

## 版本控制

每個已編製索引的文件都有版本號碼。預設情況下，OpenSearch 使用內部版本控制，從 1 開始，並隨著每次更新或刪除操作遞增。

若要使用外部版本控制（例如，在另一個資料庫中維護版本號碼），請設定 `version_type` 參數，以控制 OpenSearch 處理版本衝突的方式。下表列出可用的版本類型。

| 版本類型 | 說明 |
| :--- | :--- |
| `internal` | 只有在指定版本與已儲存文件的版本相同時，才會將文件編製索引。這是預設的版本類型。 |
| `external` 或 `external_gt` | 只有在指定版本嚴格大於已儲存文件的版本，或沒有現有文件時，才會將文件編製索引。指定版本會用作新版本，並與文件一起儲存。提供的版本必須是非負長整數。 |
| `external_gte` | 只有在指定版本大於或等於已儲存文件的版本時，才會將文件編製索引。如果沒有現有文件，操作就會成功。指定版本會用作新版本，並與文件一起儲存。提供的版本必須是非負長整數。 |

`external_gte` 版本類型適用於特殊使用案例，應謹慎使用。使用不當可能導致資料遺失。

例如，若要使用外部版本控制將文件編製索引：

```json
PUT sample-index/_doc/1?version=5&version_type=external
{
  "name": "Example",
  "price": 29.99,
  "description": "Updated from external system"
}
```

如果提供的版本不符合指定版本類型的要求，OpenSearch 會傳回版本衝突錯誤。版本控制完全即時，不受搜尋操作近乎即時的特性影響。

## 無操作更新

當您使用 Index Document API 更新文件時，OpenSearch 一律會建立文件的新版本，即使文件內容並未變更也一樣。如果您經常重新編製索引內容相同的文件，這種行為可能會沒有效率。

如果您需要避免建立不必要的文件版本，請使用 [Update Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)，並將 `detect_noop` 參數設為 `true`。Update API 會擷取現有文件、將其與新內容比較，並僅在內容已變更時建立新版本。

Index Document API 不支援無操作偵測，因為它不會擷取舊的來源進行比較。無操作更新是否有問題取決於多項因素，包括您的資料來源傳送未變更文件之更新的頻率，以及接收更新的分片上的查詢負載。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:data/write/index`。
