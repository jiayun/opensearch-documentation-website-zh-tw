---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Bulk
parent: Document APIs
nav_order: 20
redirect_from:
 - /opensearch/rest-api/document-apis/bulk/
---

# Bulk API
**於 1.0 版導入**
{: .label .label-purple }

Bulk API 可在單一請求中執行多個編製索引、更新或刪除操作。這能大幅降低額外負擔，並透過減少所需的網路往返次數與處理週期，顯著提升索引速度。

Bulk API 的請求本文採用以換行符分隔的 JSON (NDJSON) 結構。每個動作佔一行，若該動作需要來源資料（例如 `index`、`create` 或 `update` 操作），則來源資料會提供於下一行。此格式讓 OpenSearch 能快速剖析並處理動作，而無需將整個請求本文讀入記憶體。

使用 bulk 操作編製文件索引時，文件 `_id` 的大小必須為 512 位元組或更小。
{: .note}

Bulk API 可用於下列用途：

- 將多個文件操作合併為單一請求，以有效率地對大型資料集編製索引。
- 同時對多個文件執行混合操作（index、create、update 與 delete）。
- 在執行大量文件操作時，將網路額外負擔降至最低。
- 使用用戶端 bulk 輔助工具，將資料從一個索引重新編製索引至另一個索引。

Bulk API 會獨立處理各個動作。若某個動作失敗，OpenSearch 會繼續處理後續動作。回應會指出每個個別動作成功或失敗。

<!-- spec_insert_start
api: bulk
component: endpoints
-->
## 端點
```json
POST /_bulk
PUT  /_bulk
POST /{index}/_bulk
PUT  /{index}/_bulk
```
<!-- spec_insert_end -->

您可以在路徑中指定目標索引，或將其包含在[請求本文](#request-body)中。

OpenSearch 接受傳送至 `_bulk` 端點的 `PUT` 請求，但強烈建議使用 `POST`。`PUT` 的典型語意（在特定路徑建立或取代單一資源）與 bulk 操作的行為不符。
{: .note }

<!-- spec_insert_start
api: bulk
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 要對其執行 bulk 動作的資料串流、索引或索引別名名稱。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: bulk
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_source` | 布林值、清單或字串 | `true` 或 `false` 以決定是否傳回 `_source` 欄位，或是要傳回的欄位清單。 |
| `_source_excludes` | 清單或字串 | 要從回應中排除的來源欄位清單，以逗號分隔。 |
| `_source_includes` | 清單或字串 | 要包含在回應中的來源欄位清單，以逗號分隔。 |
| `index` | 字串 | 要對其執行 bulk 動作的資料串流、索引或索引別名名稱。 |
| `pipeline` | 字串 | 用於前置處理傳入文件的管線 ID。若索引指定了預設資料匯入管線，則將此值設為 `_none` 會停用此請求的預設資料匯入管線。若設定了最終管線，則無論此參數的值為何，最終管線一律會執行。 |
| `refresh` | 布林值或字串 | 若為 `true`，OpenSearch 會重新整理受影響的分片，使此操作可被搜尋看見；若為 `wait_for`，則等待重新整理，使此操作可被搜尋看見；若為 `false`，則不進行任何重新整理。有效值：`true`、`false`、`wait_for`。<br> 有效值為：<br> - `false`：不要重新整理受影響的分片。<br> - `true`：立即重新整理受影響的分片。<br> - `wait_for`：等待變更變為可見後再回覆。 |
| `require_alias` | 布林值 | 若為 `true`，請求的動作必須以索引別名為目標。_(預設：`false`)_ |
| `routing` | 字串 | 用於將操作路由至特定分片的自訂值。 |
| `timeout` | 字串 | 每個動作等待下列操作的期間：自動建立索引、動態對應更新、等待作用中的分片。 |
| `type` | 字串 | 未提供類型的項目所使用的預設文件類型。 |
| `wait_for_active_shards` | 整數、字串、NULL 或字串 | 在繼續進行操作之前必須處於作用中狀態的分片副本數。可設為 all 或任何不大於索引中分片總數的正整數（`number_of_replicas+1`）。<br> 有效值為：<br> - `all`：等待所有分片變為作用中。 |

<!-- spec_insert_end -->

## 使用 cURL 提交 bulk 請求

使用 cURL 命令從檔案提交 bulk 請求時，請使用 `--data-binary` 旗標而非 `-d`，以保留換行字元。`-d` 旗標會移除換行符，進而破壞 Bulk API 所需的 NDJSON 格式。

下列範例示範正確的做法。首先，建立一個包含 bulk 操作的檔案：

```bash
cat > bulk-operations.ndjson << 'EOF'
{ "index": { "_index": "movies", "_id": "curl-test1" } }
{ "title": "Curl Test Movie 1", "year": 2025 }
{ "index": { "_index": "movies", "_id": "curl-test2" } }
{ "title": "Curl Test Movie 2", "year": 2025 }
EOF
```

然後使用 `--data-binary` 提交該檔案：

```bash
curl -H "Content-Type: application/x-ndjson" -X POST "localhost:9200/_bulk?pretty" --data-binary "@bulk-operations.ndjson"
```

使用 cURL 傳送內嵌 bulk 請求時，請確保在 shell 中正確逸出換行符。使用單引號與實體換行通常比使用 `\n` 逸出序列更清晰。

## 樂觀並行控制

當多個處理程序同時嘗試修改同一份文件時，OpenSearch 會使用樂觀並行控制來防止衝突。Bulk API 支援兩種並行控制方式：以序號為基礎與以版本為基礎。

### 以序號為基礎的並行控制

序號提供最可靠的並行控制形式。每個文件操作都會遞增 `_seq_no` 欄位，而 `_primary_term` 會追蹤主要分片的選舉。在 bulk 操作中同時指定這兩個值，即可確保只有在文件自您上次讀取後未曾變更時，操作才會成功。

下列範例示範以序號為基礎的並行控制：

```json
{ "index": { "_index": "movies", "_id": "version-test", "if_seq_no": 13, "if_primary_term": 1 } }
{ "title": "Updated with OCC", "year": 2025 }
```

若另一個處理程序在您的讀取與更新操作之間修改了文件，`_seq_no` 或 `_primary_term` 將會改變，OpenSearch 會傳回 `version_conflict_engine_exception` 錯誤。您的應用程式接著可以擷取文件的最新版本並重試該操作。

這種方式無需明確鎖定即可防止遺失更新，讓多個處理程序能夠並行運作，同時維持資料一致性。

### 以版本為基礎的並行控制

OpenSearch 也支援使用明確版本號碼進行並行控制。每份文件都有一個 `_version` 欄位，會隨每次修改遞增。您可以在 bulk 操作中指定必要的版本：

```json
{ "index": { "_index": "movies", "_id": "doc1", "version": 5, "version_type": "internal" } }
{ "title": "Version-controlled update", "year": 2025 }
```

只有當文件目前的版本為 5 時，此操作才會成功。`version_type` 參數支援下列值：

- `internal`（預設）：使用 OpenSearch 的內部版本編號。
- `external`：允許您維護來自外部系統的版本號碼。版本必須大於目前的版本。
- `external_gte`：類似於 `external`，但允許版本大於或等於目前的版本。

## 版本控制

OpenSearch 的文件版本控制會追蹤文件隨時間的變更。每次透過索引、更新或刪除操作修改文件時，`_version` 欄位都會自動遞增。

### 內部版本控制

預設情況下，OpenSearch 使用內部版本控制，新文件從 1 開始，並隨每次修改遞增。內部版本會自動管理，即使文件被刪除後以相同 ID 重新建立，版本仍會保留。

以下範例建立一個帶有外部版本號的文件：

```json
{ "index": { "_index": "movies", "_id": "external-version-test", "version": 100, "version_type": "external" } }
{ "title": "External Version Movie", "year": 2025 }
```

### 外部版本控制

當您要將 OpenSearch 與維護自身版本號的外部資料來源同步時，外部版本控制非常實用。使用 `version_type: external` 時，OpenSearch 會接受您提供的版本號，並且只有在提供的版本大於已儲存的版本時才編製索引。這可確保亂序的更新不會以較舊的版本覆寫較新的資料。

### 版本衝突

當操作指定的版本與目前文件版本不符時，就會發生版本衝突。發生這種情況時，OpenSearch 會在該特定操作的回應中傳回 `version_conflict_engine_exception` 錯誤。大量請求會繼續處理其他操作，因此即使某些操作因版本衝突而失敗，仍可部分成功。

## 路由

路由決定哪個分片儲存特定文件。預設情況下，OpenSearch 使用文件 ID 的雜湊值來路由文件，將文件平均分散到各個分片。自訂路由可讓您覆寫此行為並控制文件的存放位置。

您可以透過兩種方式指定路由：在查詢參數層級，或在個別動作的中繼資料中。

### 查詢參數路由

在查詢參數層級套用路由會影響大量請求中的所有操作：

```json
POST /_bulk?routing=user123
{ "index": { "_index": "movies", "_id": "routed-doc" } }
{ "title": "Routed Movie", "user_id": "user123" }
```

### 動作層級路由

在動作中繼資料中指定路由可提供更精細的控制，讓同一個大量請求中的不同操作使用不同的路由值：

```json
POST /_bulk
{ "index": { "_index": "movies", "_id": "routed-action", "routing": "user456" } }
{ "title": "Action Routed Movie", "user_id": "user456" }
```

自訂路由對多租用戶應用程式特別實用，因為您可能希望將特定租用戶的所有文件儲存在同一個分片上。這可改善在單一租用戶內搜尋時的查詢效能，因為 OpenSearch 只需要查詢一個分片，而不是索引中的所有分片。

使用自訂路由時，您必須為文件的所有操作（索引、取得、更新、刪除）提供相同的路由值。否則，OpenSearch 可能會因為搜尋了錯誤的分片而找不到文件。

## 重新整理

`refresh` 參數控制大量操作所做的變更何時對搜尋查詢可見。OpenSearch 使用近即時搜尋模型，文件在編製索引後不會立即可供搜尋。

`refresh` 參數接受三個值：

- `false`（預設）：文件不會立即重新整理。它們會依據索引的重新整理間隔（通常為 1 秒）變成可供搜尋。
- `true`：強制立即重新整理所有受影響的分片，讓文件立即可供搜尋，但會付出效能成本。
- `wait_for`：在傳回之前等待下一次排定的重新整理，在可見性與效能之間取得平衡。

以下範例使用 `refresh=wait_for`：

```json
POST /_bulk?refresh=wait_for
{ "index": { "_index": "movies", "_id": "refresh-test" } }
{ "title": "Refresh Test Movie", "year": 2025 }
```

只有從大量請求接收文件的分片會被重新整理。如果一個大量請求包含路由到具有五個分片之索引中三個分片的文件，則只有那三個分片會被重新整理，其餘兩個分片不受影響。

使用 `refresh=true` 可能會顯著影響叢集效能，尤其是在頻繁發出大量請求時。對於正式環境的工作負載，請考慮使用預設行為或 `refresh=wait_for`，後者可提供較佳的效能特性，同時確保文件在有限的時間內可供搜尋。

## 等待作用中分片

`wait_for_active_shards` 參數控制在 OpenSearch 處理大量請求之前，必須有多少分片複本處於作用中狀態。此設定可防止在過多分片複本無法使用時繼續執行操作，有助於確保資料耐久性。

預設情況下，`wait_for_active_shards` 設定為 `1`，表示只有主要分片必須處於作用中狀態。您可以將它設定為：

- 正整數：操作會等待直到該數量的分片複本（包括主要分片）處於作用中狀態。
- `all`：操作會等待直到所有分片複本（主要分片與所有副本）都處於作用中狀態。

以下範例等待主要分片與一個副本分片處於作用中狀態：

```json
POST /_bulk?wait_for_active_shards=2
{ "index": { "_index": "movies", "_id": "active-shards-test" } }
{ "title": "Active Shards Test", "year": 2025 }
```

對於設定為一個主要分片與兩個副本（`number_of_replicas=2`）的索引，設定 `wait_for_active_shards=2` 會要求主要分片與至少一個副本處於作用中狀態。這在可用性與耐久性之間提供了平衡。

如果在逾時期間內（由 `timeout` 參數控制）無法達到所需的作用中分片數量，大量操作會失敗並出現逾時錯誤。已變成作用中狀態的分片可能仍包含成功編製索引的文件。

## 效能考量

使用 Bulk API 時，有幾項因素會影響效能與輸送量。了解這些考量有助於您針對特定工作負載最佳化大量操作。

### 最佳批次大小

單一大量請求中應包含多少操作並沒有通用的「正確」數量。最佳批次大小取決於幾項因素：

- **文件大小**：較大的文件需要較少的每請求操作數才能達到理想的請求大小。
- **索引複雜度**：具有許多欄位或複雜對應的文件需要較長的處理時間。
- **硬體資源**：叢集節點上可用的記憶體與 CPU 容量。
- **網路頻寬**：用戶端與 OpenSearch 叢集之間的連線速度。

從 1,000 到 5,000 個操作的批次開始，並嘗試不同的大小。監控叢集的效能指標（CPU 使用率、記憶體消耗、索引延遲），以找出適合您工作負載的最佳批次大小。良好的大量請求大小通常介於 5 MB 到 15 MB 之間。

### HTTP 分塊

使用 HTTP API 時，請確保您的用戶端不會傳送 HTTP 分塊（`Transfer-Encoding: chunked`）。HTTP 分塊會妨礙 OpenSearch 有效剖析請求本文，因為它必須在分塊抵達時以漸進方式處理資料，而不是一次讀取整個請求。

大多數 HTTP 用戶端預設會停用分塊，但如果您遇到大量操作緩慢的情況，請確認您的用戶端組態沒有啟用分塊傳輸編碼。

### 用戶端緩衝

Bulk API 所使用的 NDJSON 格式是為了將緩衝降到最低而設計。每個動作及其選用的來源資料會分別出現在不同行，讓 OpenSearch 能在剖析後立即處理操作，而不必將整個請求載入記憶體。

在應用程式中實作大量操作時：

- 避免在傳送前將所有操作累積在記憶體中。請在產生操作時，就將其串流至 Bulk API。
- 逐步處理回應，而不是等待所有操作完成。
- 使用支援高效率大量輔助工具的用戶端程式庫，這些工具會自動處理批次處理與錯誤重試。

### 請求剖析

OpenSearch 僅在接收節點上剖析動作中繼資料，以最佳化大量請求的處理。動作中繼資料包含路由資訊，可決定應由哪個分片處理該操作。一旦決定路由後，OpenSearch 會將完整操作 (中繼資料與來源資料) 轉送至適當的分片。

此設計可將協調節點上的處理降到最低，讓 OpenSearch 能有效率地將大量操作分散到整個叢集，而不會在進入點造成瓶頸。

## 請求本文

大量請求本文使用以換行符號分隔的 JSON (NDJSON) 格式。每個動作都必須指定在單一行中，並以換行字元 (`\n`) 結尾；而來源資料 (若有需要) 必須放在下一行，並以換行字元結尾。

```
Action and metadata\n
Optional document\n
Action and metadata\n
Optional document\n
```

每個 JSON 文件可以包含空格以便閱讀，但必須位於單一行中。OpenSearch 使用換行字元來剖析大量請求，並要求請求本文必須以換行字元結尾。將請求傳送至 Bulk API 時，請將 `Content-Type` 標頭設為 `application/x-ndjson`。

### 動作中繼資料欄位

所有動作皆支援在動作行中使用下列中繼資料欄位。除非您在請求路徑中指定索引，否則 `_index` 欄位為必要欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_index` | 字串 | 索引的名稱。若未在請求路徑中指定，則為必要。
`_id` | 字串 | 文件 ID。選用。若未提供，OpenSearch 會自動產生 ID。
`_require_alias` | 布林值 | 若為 `true`，則目的地必須是索引別名。預設為 `false`。
`routing` | 字串 | 文件操作的自訂路由值。
`version` | 整數 | 文件的明確版本號碼。用於樂觀並行控制。
`version_type` | 字串 | 版本類型：`internal`、`external`、`external_gte`。預設為 `internal`。
`if_seq_no` | 整數 | 僅在文件具有此序號時才執行操作。用於樂觀並行控制。
`if_primary_term` | 整數 | 僅在文件具有此主要任期時才執行操作。用於樂觀並行控制。

### 動作

Bulk API 支援下列動作。

### Create

若文件尚不存在則建立文件，否則傳回錯誤。下一行必須包含 JSON 文件：

```json
{ "create": { "_index": "movies", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
```

### Delete

此動作會刪除文件 (若存在)。若文件不存在，OpenSearch 不會傳回錯誤，而是在 `result` 下傳回 `not_found`。Delete 動作不需要下一行的文件：

```json
{ "delete": { "_index": "movies", "_id": "tt2229499" } }
```

### Index

Index 動作會建立文件 (若尚不存在)，並取代文件 (若已存在)。下一行必須包含 JSON 文件：

```json
{ "index": { "_index": "movies", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013}
```

### Update

根據預設，此動作會更新現有文件，並在文件不存在時傳回錯誤。下一行必須包含完整或部分的 JSON 文件，取決於您要更新文件的多寡：

```json
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }
```

`update` 動作支援動作中繼資料中的 `retry_on_conflict` 欄位。這會指定發生版本衝突時應重試更新的次數：

```json
{ "update": { "_index": "movies", "_id": "tt0816711", "retry_on_conflict": 3 } }
{ "doc" : { "title": "World War Z" } }
```

更新操作不會執行使用者定義的資料匯入管線。如果您需要透過資料匯入管線處理文件，請改用 [upsert](#upsert) 操作。
{: .note}

### Upsert

若要 upsert 文件，請使用下列其中一個選項：

1. 在 `doc` 欄位中指定文件，並設定 `doc_as_upsert=true`。若文件存在，會以 `doc` 欄位的內容更新。若文件不存在，則會以 `doc` 欄位中指定的參數，將新文件編製索引：

    ```json
    { "update": { "_index": "movies", "_id": "tt0816711" } }
    { "doc" : { "title": "World War Z" }, "doc_as_upsert": true }
    ```
1. 在 `doc` 欄位中指定要更新的文件 (當文件存在時)，在 `upsert` 欄位中指定要插入的文件 (當文件不存在時)，並將 `doc_as_upsert` 保持設為 `false`：

    ```json
    { "update": { "_index": "products", "_id": "widget-123" } }
    { "doc": { "stock": 75, "updated_at": "2025-01-15T10:30:00Z" }, "upsert": { "name": "Widget", "price": 39.99, "stock": 100, "created_at": "2025-01-15T10:30:00Z" }}
    ```
    
當您只想在文件存在時更新特定欄位，但在文件不存在時插入完整文件，請使用此選項。

Upsert 操作會觸發資料匯入管線，讓您能在文件編製索引或更新前先行處理。
{: .note}

### Script

您可以透過使用 `source` 或文件中的 `id` 定義指令碼，為更複雜的文件更新指定指令碼：

```json
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "script" : { "source": "ctx._source.title = \"World War Z\"" } }
```

### 指令碼式 upsert

您可以使用指令碼以下列方式更新或 upsert 文件：

1. 指令碼 + upsert (`scripted_upsert=false`，預設)：若文件存在，會使用 `script` 更新文件。若文件不存在，則會插入 `upsert` 欄位中的文件，而不執行指令碼：

    ```json
    POST _bulk
    { "update": { "_index": "movies", "_id": "tt0816711" } }
    { "script": { "source": "ctx._source.title = params.title; ctx._source.genre = params.genre;", "params": { "title": "World War Z", "genre": "Action" } }, "upsert": { "title": "World War Z", "genre": "Action", "author": "Tom Smith" } }
    ```
    {% include copy-curl.html %}

1. 指令碼 + upsert + `scripted_upsert=true`。若文件存在，會使用 `script` 更新文件。若文件不存在，指令碼會在 `upsert` 欄位上執行，並插入產生的文件：

    ```json
    POST _bulk
    { "update": { "_index": "movies", "_id": "tt0816711" } }
    { "script": { "source": "ctx._source.title = params.title; ctx._source.genre = params.genre;", "params": { "title": "World War Z", "genre": "Action" } }, "scripted_upsert": true }
    ```
    {% include copy-curl.html %}

## 範例：執行多個動作

以下範例請求會在單一請求中執行多個文件操作，包括刪除、編製索引、建立及更新操作：

<!-- spec_insert_start
component: example_code
rest: POST /_bulk
body: |
{ "delete": { "_index": "movies", "_id": "tt2229499" } }
{ "index": { "_index": "movies", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013 }
{ "create": { "_index": "movies", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }
-->
{% capture step1_rest %}
POST /_bulk
{ "delete": { "_index": "movies", "_id": "tt2229499" } }
{ "index": { "_index": "movies", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013 }
{ "create": { "_index": "movies", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  body = '''
{ "delete": { "_index": "movies", "_id": "tt2229499" } }
{ "index": { "_index": "movies", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013 }
{ "create": { "_index": "movies", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：在路徑中指定索引

以下範例請求會在請求路徑中指定索引，因此不需要在每個動作行中包含 `_index`：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_bulk
body: |
{ "index": { "_id": "tt0468569" } }
{ "title": "The Dark Knight", "year": 2008, "director": "Christopher Nolan" }
{ "index": { "_id": "tt0137523" } }
{ "title": "Fight Club", "year": 1999, "director": "David Fincher" }
-->
{% capture step1_rest %}
POST /movies/_bulk
{ "index": { "_id": "tt0468569" } }
{ "title": "The Dark Knight", "year": 2008, "director": "Christopher Nolan" }
{ "index": { "_id": "tt0137523" } }
{ "title": "Fight Club", "year": 1999, "director": "David Fincher" }
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  index = "movies",
  body = '''
{ "index": { "_id": "tt0468569" } }
{ "title": "The Dark Knight", "year": 2008, "director": "Christopher Nolan" }
{ "index": { "_id": "tt0137523" } }
{ "title": "Fight Club", "year": 1999, "director": "David Fincher" }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 upsert 操作

以下範例請求使用 `doc_as_upsert`，在文件存在時更新文件，若不存在則建立文件：

<!-- spec_insert_start
component: example_code
rest: POST /_bulk
body: |
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "rating": 9.0 }, "doc_as_upsert": true }
{ "update": { "_index": "movies", "_id": "tt9999999" } }
{ "doc": { "title": "New Movie", "year": 2024 }, "doc_as_upsert": true }
-->
{% capture step1_rest %}
POST /_bulk
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "rating": 9.0 }, "doc_as_upsert": true }
{ "update": { "_index": "movies", "_id": "tt9999999" } }
{ "doc": { "title": "New Movie", "year": 2024 }, "doc_as_upsert": true }
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  body = '''
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "rating": 9.0 }, "doc_as_upsert": true }
{ "update": { "_index": "movies", "_id": "tt9999999" } }
{ "doc": { "title": "New Movie", "year": 2024 }, "doc_as_upsert": true }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 retry_on_conflict 處理版本衝突

以下範例請求使用 `retry_on_conflict`，在發生版本衝突時自動重試更新：

<!-- spec_insert_start
component: example_code
rest: POST /_bulk
body: |
{ "update": { "_index": "movies", "_id": "tt0468569", "retry_on_conflict": 3 } }
{ "doc": { "rating": 9.5 } }
-->
{% capture step1_rest %}
POST /_bulk
{ "update": { "_index": "movies", "_id": "tt0468569", "retry_on_conflict": 3 } }
{ "doc": { "rating": 9.5 } }
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  body = '''
{ "update": { "_index": "movies", "_id": "tt0468569", "retry_on_conflict": 3 } }
{ "doc": { "rating": 9.5 } }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：篩選回應以僅顯示錯誤

以下範例請求使用 `filter_path` 查詢參數，僅傳回失敗的操作：

<!-- spec_insert_start
component: example_code
rest: POST /_bulk?filter_path=items.*.error
body: |
{ "update": { "_index": "movies", "_id": "missing1" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "missing2" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "title": "Success" } }
-->
{% capture step1_rest %}
POST /_bulk?filter_path=items.*.error
{ "update": { "_index": "movies", "_id": "missing1" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "missing2" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "title": "Success" } }
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  params = { "filter_path": "items.*.error" },
  body = '''
{ "update": { "_index": "movies", "_id": "missing1" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "missing2" } }
{ "doc": { "title": "Error" } }
{ "update": { "_index": "movies", "_id": "tt0468569" } }
{ "doc": { "title": "Success" } }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

Bulk API 會依照提交順序，傳回請求中每個操作的資訊。請特別注意最上層的 `errors` 布林值。若 `true`，表示一個或多個操作失敗，您可以檢查個別項目以取得詳細資訊。

即使部分操作因分片失敗或其他錯誤而失敗，Bulk API 仍會一律傳回完整回應。這種部分回應行為可確保您收到所有成功處理的操作結果，而不必無限期等待失敗的操作完成。

以下範例回應對應到第一個包含多個動作的範例請求：

```json
{
  "took": 35,
  "errors": false,
  "items": [
    {
      "delete": {
        "_index": "movies",
        "_id": "tt2229499",
        "_version": 1,
        "result": "not_found",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1,
        "status": 404
      }
    },
    {
      "index": {
        "_index": "movies",
        "_id": "tt1979320",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 2,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": "movies",
        "_id": "tt1392214",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 3,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "update": {
        "_index": "movies",
        "_id": "tt0816711",
        "_version": 2,
        "result": "updated",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 4,
        "_primary_term": 1,
        "status": 200
      }
    }
  ]
}
```

當操作失敗時，回應會包含一個 `error` 物件，其中提供失敗的詳細資訊：

```json
{
  "took": 9,
  "errors": true,
  "items": [
    {
      "update": {
        "_index": "movies",
        "_id": "nonexistent1",
        "status": 404,
        "error": {
          "type": "document_missing_exception",
          "reason": "[nonexistent1]: document missing",
          "index": "movies",
          "shard": "0",
          "index_uuid": "UZdzhOjDQvGihxfS-m_UFA"
        }
      }
    }
  ]
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`took` | 整數 | 處理大量請求所花費的時間（毫秒）。
`errors` | 布林值 | 指出大量請求中是否有任何操作失敗。若為 `true`，請檢查個別項目以取得錯誤詳細資訊。
`items` | 物件陣列 | 按照提交順序包含大量請求中每個操作的結果。

### items 陣列

`items` 陣列中的每個物件都對應一個操作，並包含一個符合動作類型的鍵（`index`、`create`、`update` 或 `delete`）。其值為一個包含下列欄位的物件。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_index` | 字串 | 與該操作相關聯的索引名稱。
`_id` | 字串 | 與該操作相關聯的文件 ID。
`_version` | 整數 | 操作後的文件版本。每次更新文件時遞增。僅在操作成功時傳回。
`result` | 字串 | 操作的結果：`created`、`updated`、`deleted` 或 `not_found`。僅在操作成功時傳回。
`_shards` | 物件 | 包含該操作的分片資訊。僅在操作成功時傳回。
`_shards.total` | 整數 | 嘗試執行該操作的分片數。
`_shards.successful` | 整數 | 成功執行該操作的分片數。
`_shards.failed` | 整數 | 執行該操作失敗的分片數。
`_seq_no` | 整數 | 為該操作的文件指派的序號。用於樂觀並行控制。僅在操作成功時傳回。
`_primary_term` | 整數 | 為該操作的文件指派的主要任期。用於樂觀並行控制。僅在操作成功時傳回。
`status` | 整數 | 該操作的 HTTP 狀態碼：`200`（已更新）、`201`（已建立）、`404`（找不到）或 `409`（版本衝突）。
`error` | 物件 | 包含失敗操作的相關資訊。僅在操作失敗時傳回。
`error.type` | 字串 | 失敗操作的錯誤類型，例如 `document_missing_exception` 或 `version_conflict_engine_exception`。
`error.reason` | 字串 | 操作失敗原因的人類可讀說明。
`error.index` | 字串 | 與失敗操作相關聯的索引名稱。
`error.shard` | 字串 | 與失敗操作相關聯的分片 ID。
`error.index_uuid` | 字串 | 與失敗操作相關聯之索引的通用唯一識別碼 (UUID)。

## 部分回應與分片失敗

為確保快速回應，Bulk API 即使某些分片操作失敗仍會傳回結果。大量請求中的每個操作都是獨立處理的，無論其他操作成功或失敗，OpenSearch 都會在回應中包含每個操作的結果。

當一或多個分片無法處理某個操作時，OpenSearch 會繼續處理其餘操作，並在回應中包含失敗操作的錯誤資訊。頂層 `errors` 欄位指出是否有任何操作發生錯誤，讓您能快速判斷是否需要檢查個別操作的結果。

分片失敗可能由多種原因造成：

- **資源不足**：託管分片的節點記憶體或磁碟空間耗盡。
- **網路分割**：分片因網路問題而暫時無法連線。
- **版本衝突**：樂觀並行控制導致操作無法完成。
- **對應錯誤**：文件不符合索引的對應要求。

您的應用程式應一律檢查回應中的 `errors` 欄位，並適當處理失敗的操作。視您的使用情境而定，您可以重試失敗的操作、將其記錄以供日後檢視，或發出警示通知維運人員調查根本原因。

## 必要權限

如果您使用 Security 外掛程式，請確保您具備執行大量操作的適當權限。所需權限取決於大量請求中的操作：

- `indices:data/write/bulk`：所有大量操作皆需要。
- `indices:data/write/index`：索引與建立操作需要。
- `indices:data/write/update`：更新操作需要。
- `indices:data/write/delete`：刪除操作需要。

您還需要對大量請求中指定之目標索引的權限。使用索引模式或別名時，請確保您的安全性角色授予對該模式或別名可能符合之所有索引的存取權。
