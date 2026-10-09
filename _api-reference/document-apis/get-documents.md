---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得文件"
parent: Document APIs
nav_order: 5
redirect_from:
 - /opensearch/rest-api/document-apis/get-documents/
---

# Get Document API
**於 1.0 版導入**
{: .label .label-purple }

Get Document API 會依文件 ID 從索引中擷取 JSON 文件及其中繼資料。您也可以使用 HEAD 請求來驗證文件或其來源是否存在，而不需擷取完整內容。

## 端點

若要從索引中擷取文件及其中繼資料，請使用 `GET` 方法：

```json
GET /{index}/_doc/{id}
```

若只要擷取文件來源，請使用下列端點：

```json
GET /{index}/_source/{id}
```

若要驗證文件是否存在，請使用 `HEAD` 方法：

```json
HEAD /{index}/_doc/{id}
HEAD /{index}/_source/{id}
```

<!-- spec_insert_start
api: get
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `id` | **必要** | 字串 | 文件的唯一識別碼。 |
| `index` | **必要** | 字串 | 包含該文件的索引名稱。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 方法 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- | :--- |
| `_source` | `GET` | 布林值或清單或字串 | 是否傳回 `_source` 欄位。設為 `true` 表示包含，設為 `false` 表示排除，或指定以逗號分隔的欄位名稱清單以傳回。請參閱[來源篩選](#source-filtering)。| N/A |
| `_source_excludes` | `GET` | 清單或字串 | 要從回應中排除的來源欄位，以逗號分隔的清單。請參閱[來源篩選](#source-filtering)。 | N/A |
| `_source_includes` | `GET` | 清單或字串 | 要包含在回應中的來源欄位，以逗號分隔的清單。請參閱[來源篩選](#source-filtering)。 | N/A |
| `preference` | `GET`, `HEAD` | 字串 | 指定由哪個節點或分片處理此作業的偏好設定。預設情況下，OpenSearch 會隨機選取一個副本分片。請參閱[偏好設定](#preference)。 | `random` |
| `realtime` | `GET`, `HEAD` | 布林值 | 請求是否為即時。若為 `true`，請求會擷取文件的最新版本。若為 `false`，請求為近似即時，並依據最近一次重新整理擷取文件。請參閱[即時行為](#real-time-behavior)。 | `true` |
| `refresh` | `GET`, `HEAD` | 布林值或字串 | 是否在作業前重新整理受影響的分片，使最近的變更可見。<br> 有效值為：<br> - `false`：不重新整理受影響的分片。<br> - `true`：立即重新整理受影響的分片。<br> - `wait_for`：在回應前等待變更變為可見。請參閱[重新整理](#refresh)。 | `false` |
| `routing` | `GET`, `HEAD` | 清單或字串 | 用於指定特定主要分片的路由值。請參閱[路由](#routing)。| N/A |
| `stored_fields` | `GET` | 清單或字串 | 要傳回的儲存欄位，以逗號分隔的清單。若未指定任何欄位，回應中將不包含任何儲存欄位。若指定此參數，`_source` 參數會預設為 `false`。 | N/A |
| `version` | `GET`, `HEAD` | 整數 | 用於並行控制的明確版本號。指定的版本必須與文件目前的版本相符，請求才會成功。 | N/A |
| `version_type` | `GET`, `HEAD` | 字串 | 用於並行控制的版本類型。<br> 有效值為：<br> - `internal`：版本號由 OpenSearch 內部管理。<br> - `external`：版本號必須大於目前的版本。<br> - `external_gte`：版本號必須大於或等於目前的版本。 | `internal` |

## 範例請求

下列範例依 ID 擷取文件：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/1
-->
{% capture step1_rest %}
GET /products/_doc/1
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "1",
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列範例顯示 `GET` 請求的回應：

```json
{
  "_index": "products",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with optical sensor",
    "price": 29.99,
    "category": "Electronics",
    "in_stock": true,
    "manufacturer": "TechCorp",
    "model": "WM-2000",
    "tags": [
      "wireless",
      "ergonomic",
      "optical"
    ]
  }
}
```

## 回應本文欄位

`GET` 回應包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_index` | 字串 | 包含該文件的索引名稱。
`_id` | 字串 | 文件的唯一識別碼。
`_version` | 整數 | 文件的版本號。每次更新文件時都會遞增。
`_seq_no` | 整數 | 為編製索引作業指派給文件的序號。用於確保較舊的版本不會覆寫較新的版本。
`_primary_term` | 整數 | 為編製索引作業指派給文件的主要分片任期。與 `_seq_no` 搭配使用以進行樂觀並行控制。
`found` | 布林值 | 表示文件是否存在。若找到文件則為 `true`，否則為 `false`。
`_routing` | 字串 | 用於判斷哪個分片儲存該文件的路由值。僅在編製索引時有指定路由值才會包含。
`_source` | 物件 | 編製索引的原始 JSON 文件。若 `_source` 參數設為 `false` 或使用 `stored_fields` 參數，則會排除。
`_fields` | 物件 | 當指定 `stored_fields` 參數時包含儲存欄位的值。僅在設定 `stored_fields` 且 `found` 為 `true` 時才會傳回。欄位值一律以陣列形式傳回。請參閱[擷取已儲存的欄位](#retrieving-stored-fields)。

## 來源篩選

預設情況下，Get Document API 會傳回 `_source` 欄位的完整內容。您可以控制傳回來源的哪些部分，或完全排除。

### 停用來源擷取

若要從回應中排除 `_source` 欄位，請將 `_source` 參數設為 `false`。下列範例擷取文件中繼資料但不包含來源內容：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/1?_source=false
-->
{% capture step1_rest %}
GET /products/_doc/1?_source=false
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "1",
  index = "products",
  params = { "_source": "false" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應會排除 `_source` 欄位：

```json
{
  "_index": "products",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true
}
```

### 來源包含與排除

若要從大型文件中只擷取特定欄位，請使用 `_source_includes` 參數包含特定欄位，或使用 `_source_excludes` 參數排除欄位。這樣只會傳輸所需的資料，從而降低網路負擔。

下列範例只擷取 `name` 與 `price` 欄位：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/1?_source_includes=name,price
-->
{% capture step1_rest %}
GET /products/_doc/1?_source_includes=name,price
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "1",
  index = "products",
  params = { "_source_includes": "name,price" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應的 `_source` 欄位只包含 `price` 與 `name` 欄位：

```json
{
  "_index": "products",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "price": 29.99,
    "name": "Wireless Mouse"
  }
}
```

### 簡短表示法

如果您只需要包含特定欄位，而不排除任何欄位，可直接在 `_source` 參數中指定欄位，使用簡短表示法。以下範例只擷取 `name` 和 `price` 欄位：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/1?_source=name,price
-->
{% capture step1_rest %}
GET /products/_doc/1?_source=name,price
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "1",
  index = "products",
  params = { "_source": "name,price" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 只擷取來源欄位

使用 `_source` 端點只擷取文件來源，而不含中繼資料。以下範例只擷取來源內容：

<!-- spec_insert_start
component: example_code
rest: GET /products/_source/1
-->
{% capture step1_rest %}
GET /products/_source/1
{% endcapture %}

{% capture step1_python %}


response = client.get_source(
  id = "1",
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應只包含 `_source` 欄位：

```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with optical sensor",
  "price": 29.99,
  "category": "Electronics",
  "in_stock": true,
  "manufacturer": "TechCorp",
  "model": "WM-2000",
  "tags": [
    "wireless",
    "ergonomic",
    "optical"
  ]
}
```

您可以將 `_source` 端點與來源篩選參數搭配使用。以下範例只從來源擷取特定欄位：

<!-- spec_insert_start
component: example_code
rest: GET /products/_source/1?_source=name,price
-->
{% capture step1_rest %}
GET /products/_source/1?_source=name,price
{% endcapture %}

{% capture step1_python %}


response = client.get_source(
  id = "1",
  index = "products",
  params = { "_source": "name,price" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應只包含 `price` 和 `name` 欄位：

```json
{
  "price": 29.99,
  "name": "Wireless Mouse"
}
```

您可以搭配使用 HEAD 與 `_source` 端點，檢查文件來源是否存在：

<!-- spec_insert_start
component: example_code
rest: HEAD /products/_source/1
-->
{% capture step1_rest %}
HEAD /products/_source/1
{% endcapture %}

{% capture step1_python %}


response = client.exists_source(
  id = "1",
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應只包含 `200 - true`。

## 路由

以自訂路由值將文件編製索引時，您必須在擷取文件時提供相同的路由值。路由值會決定由哪個分片儲存文件。

以下範例擷取以路由值 `user1` 編製索引的文件：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/2?routing=user1
-->
{% capture step1_rest %}
GET /products/_doc/2?routing=user1
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "2",
  index = "products",
  params = { "routing": "user1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含具有指定路由值的文件：

```json
{
  "_index": "products",
  "_id": "2",
  "_version": 1,
  "_seq_no": 1,
  "_primary_term": 1,
  "_routing": "user1",
  "found": true,
  "_source": {
    "name": "Mechanical Keyboard",
    "description": "RGB mechanical gaming keyboard",
    "price": 149.99,
    "category": "Electronics",
    "in_stock": true,
    "manufacturer": "GameGear",
    "model": "MK-500",
    "tags": [
      "mechanical",
      "rgb",
      "gaming"
    ]
  }
}
```

如果您未指定正確的路由值，OpenSearch 就無法找到文件，並會傳回 `found: false` 回應。

## 擷取已儲存的欄位

使用 `stored_fields` 參數擷取在編製索引時儲存於索引中的特定欄位。只有在對應中具有 `store: true` 的欄位才會傳回。沒有此設定的欄位會被忽略。

以下範例只從文件擷取已儲存的 `category` 和 `manufacturer` 欄位：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/1?stored_fields=category,manufacturer
-->
{% capture step1_rest %}
GET /products/_doc/1?stored_fields=category,manufacturer
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "1",
  index = "products",
  params = { "stored_fields": "category,manufacturer" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

請注意，從已儲存欄位擷取的欄位值一律以陣列形式傳回。即使 `category` 和 `manufacturer` 是單值欄位，也會以陣列形式傳回：

```json
{
  "_index": "products",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "fields": {
    "category": [
      "Electronics"
    ],
    "manufacturer": [
      "TechCorp"
    ]
  }
}
```

從使用路由編製索引的文件擷取已儲存欄位時，您必須提供路由值。以下範例從具有路由值的文件擷取已儲存欄位：

<!-- spec_insert_start
component: example_code
rest: GET /products/_doc/2?routing=user1&stored_fields=category,manufacturer
-->
{% capture step1_rest %}
GET /products/_doc/2?routing=user1&stored_fields=category,manufacturer
{% endcapture %}

{% capture step1_python %}


response = client.get(
  id = "2",
  index = "products",
  params = { "routing": "user1", "stored_fields": "category,manufacturer" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 檢查文件是否存在

您可以使用 HEAD 方法確認文件是否存在，而不擷取其內容。如果文件存在，OpenSearch 會傳回 HTTP 狀態碼 `200`；如果不存在，則會傳回 `404`。

以下範例檢查文件是否存在：

<!-- spec_insert_start
component: example_code
rest: HEAD /products/_doc/1
-->
{% capture step1_rest %}
HEAD /products/_doc/1
{% endcapture %}

{% capture step1_python %}


response = client.exists(
  id = "1",
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應只包含 `200 - true`。

## 偏好設定

`preference` 參數控制由哪個副本分片處理請求。預設情況下，OpenSearch 會將 GET 作業隨機分散到可用的副本分片上。

您可以將 `preference` 參數設為下列其中一個值：

- `_local`：將作業導向配置於本機的副本分片，以減少網路額外負擔。
- 自訂字串值：將具有相同自訂值的請求路由至相同的副本分片。這可確保分片處於不同重新整理狀態時，仍能取得一致的結果。常見的自訂值包括工作階段 ID 或使用者名稱。

## 即時行為

預設情況下，Get Document API 以即時方式運作，無論索引重新整理的頻率為何，都會擷取文件的最新版本。這表示您可以在將文件編製索引後立即擷取該文件，即使索引尚未重新整理使其可供搜尋也一樣。

當您請求已儲存的欄位（使用 `stored_fields` 參數），而文件已更新但尚未重新整理時，OpenSearch 會剖析並分析文件來源，以擷取所請求的已儲存欄位。

若要停用即時行為，並根據索引上次重新整理後的狀態擷取文件，請將 `realtime` 參數設為 `false`。

## 重新整理

`refresh` 參數可設為 `true`，以便在擷取文件前重新整理相關的分片。重新整理可讓最近的變更可供搜尋，但可能會造成顯著的系統負載並減緩索引速度。啟用此參數前，請仔細評估資料新鮮度與效能之間的取捨。

## 版本控制

您可以使用 `version` 參數，僅在文件目前版本符合指定號碼時才擷取該文件。這可確保在處理具有版本控制的文件時的資料一致性。

在內部，當文件更新時，OpenSearch 會將舊文件版本標記為已刪除，並建立全新的文件版本。雖然您無法透過 Get Document API 存取舊版本，但 OpenSearch 會在編製索引時自動於背景清理已刪除的版本。

## 分散式模型

Get Document API 使用文件 ID 計算雜湊值，以識別儲存該文件的分片。接著 OpenSearch 會將請求路由至該分片群組中的其中一個副本（包括主要分片及其副本），並傳回結果。

擁有更多副本分片可提升 GET 作業的可擴展性，因為負載會分散到多個副本，進而提高擷取請求的輸送量。

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:data/read/get`。
