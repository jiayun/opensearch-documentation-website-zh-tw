---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Multi-get 文件"
parent: Document APIs
nav_order: 30
redirect_from:
 - /opensearch/rest-api/document-apis/multi-get/
---

# Multi-get Documents API
**於 1.0 版導入**
{: .label .label-purple }

Multi-get Documents API 可在單一請求中從一或多個索引擷取多份文件。此操作比執行多個個別的 GET 請求更有效率，因為它可減少網路負擔，並將多個操作合併為對叢集的單次往返。

當您需要依 ID 擷取特定文件，且已知要取得哪些文件時，可使用此 API。常見情境包括：

- 根據已知的 ID 清單擷取一批使用者設定檔、產品詳細資料或其他實體。
- 在單一操作中從不同索引取得相關文件，例如同時取得訂單記錄及其關聯的客戶資訊。
- 實作高效的資料存取模式，在擷取多份文件的同時控制每份文件要傳回哪些欄位。

## 部分回應

Multi-get Documents API 以快速回應為優先，若在操作期間有一或多個分片失敗，將會傳回部分結果。若因分片失敗而無法擷取特定文件，或該文件不存在，回應會包含該文件的錯誤詳細資訊，同時仍傳回成功擷取的文件。這可確保暫時性失敗或文件遺失不會阻礙整個操作。

<!-- spec_insert_start
api: mget
component: endpoints
-->
## 端點
```json
GET  /_mget
POST /_mget
GET  /{index}/_mget
POST /{index}/_mget
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: mget
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 當指定 `ids`，或 `docs` 陣列中的文件未指定索引時，用來擷取文件的索引名稱。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: mget
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `_source` | 布林值或清單或字串 | 設為 `true` 或 `false` 以決定是否傳回 `_source` 欄位，或提供要傳回的欄位清單。 | N/A |
| `_source_excludes` | 清單或字串 | 以逗號分隔的來源欄位清單，用於從回應中排除。您也可以使用此參數，從 `_source_includes` 查詢參數所指定的子集中排除欄位。 | N/A |
| `_source_includes` | 清單或字串 | 以逗號分隔的來源欄位清單，用於包含在回應中。若有指定此參數，則只會傳回這些來源欄位。您可以使用 `_source_excludes` 查詢參數從此子集中排除欄位。若 `_source` 參數為 `false`，則會忽略此參數。 | N/A |
| `preference` | 字串 | 指定應在其上執行操作的節點或分片。預設為隨機。 | `random` |
| `realtime` | 布林值 | 若為 `true`，則請求為即時，而非近乎即時。 | N/A |
| `refresh` | 布林值或字串 | 若為 `true`，則請求會在擷取文件前重新整理相關分片。<br> 有效值為：<br> - `false`：不重新整理受影響的分片。<br> - `true`：立即重新整理受影響的分片。<br> - `wait_for`：等待變更可見後再回覆。 | N/A |
| `routing` | 清單或字串 | 用於將操作路由至特定分片的自訂值。 | N/A |
| `stored_fields` | 清單或字串 | 若為 `true`，則擷取儲存在索引中的文件欄位，而非文件 `_source`。 | N/A |

<!-- spec_insert_end -->

## 請求本文欄位

請求本文指定要擷取哪些文件。若您未在請求路徑中指定索引，則必須在請求本文中為每份文件包含索引名稱。下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`docs` | 物件陣列 | 要擷取的文件。若未指定 `ids` 欄位，則為必要。每個物件可包含下列欄位：`_index`、`_id`、`routing`、`_source` 與 `stored_fields`。
`docs._index` | 字串 | 包含該文件的索引名稱。若未在請求路徑中指定索引，則為必要。
`docs._id` | 字串 | 文件 ID。必要。
`docs.routing` | 字串 | 用於將操作路由至特定分片的路由值。若在為文件編製索引時使用了自訂路由值，則為必要。
`docs._source` | 布林值、陣列或物件 | 控制要傳回哪些來源欄位。若為 `false`，則 `_source` 欄位會從回應中排除。若為陣列，則指定要包含的欄位。若為物件，可包含 `includes` 與 `excludes` 陣列，以控制欄位的包含與排除。預設為 `true`。
`docs._source.includes` | 字串陣列 | 要包含在回應中的來源欄位。例如 `["title", "author"]` 只會傳回 `title` 與 `author` 欄位。
`docs._source.excludes` | 字串陣列 | 要從回應中排除的來源欄位。例如 `["internal_notes"]` 會排除 `internal_notes` 欄位。
`docs.stored_fields` | 字串陣列 | 要擷取的儲存欄位，用於取代 `_source` 欄位。只能擷取在索引對應中明確儲存的欄位。若有指定，則不會傳回 `_source` 欄位，除非明確要求。
`ids` | 字串陣列 | 當所有文件都在同一索引時，用來指定文件 ID 的簡化方式。只能在請求路徑中指定索引時使用。若有提供，則不需要 `docs` 欄位。

## 範例：從多個索引擷取文件

下列範例從 `books` 索引擷取一份文件，並從 `articles` 索引擷取一份文件：

<!-- spec_insert_start
component: example_code
rest: GET /_mget
body: |
{
  "docs": [
    {
      "_index": "books",
      "_id": "1"
    },
    {
      "_index": "articles",
      "_id": "1"
    }
  ]
}
-->
{% capture step1_rest %}
GET /_mget
{
  "docs": [
    {
      "_index": "books",
      "_id": "1"
    },
    {
      "_index": "articles",
      "_id": "1"
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mget(
  body =   {
    "docs": [
      {
        "_index": "books",
        "_id": "1"
      },
      {
        "_index": "articles",
        "_id": "1"
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 IDs 陣列

當要從同一索引擷取多份文件時，您可以在路徑中指定索引並使用 `ids` 陣列，以簡化請求。下列範例從 `books` 索引擷取三份文件：

<!-- spec_insert_start
component: example_code
rest: GET /books/_mget
body: |
{
  "ids": ["1", "2", "3"]
}
-->
{% capture step1_rest %}
GET /books/_mget
{
  "ids": [
    "1",
    "2",
    "3"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mget(
  index = "books",
  body =   {
    "ids": [
      "1",
      "2",
      "3"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：篩選來源欄位

您可以使用 `_source` 參數控制每份文件要傳回哪些欄位。下列範例示範不同的來源篩選選項：第一份文件完全排除來源、第二份文件傳回特定欄位，第三份文件使用 includes 傳回選取的欄位：

<!-- spec_insert_start
component: example_code
rest: GET /_mget
body: |
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_source": false
    },
    {
      "_index": "books",
      "_id": "2",
      "_source": ["title", "author"]
    },
    {
      "_index": "books",
      "_id": "3",
      "_source": {
        "includes": ["title", "year"]
      }
    }
  ]
}
-->
{% capture step1_rest %}
GET /_mget
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_source": false
    },
    {
      "_index": "books",
      "_id": "2",
      "_source": [
        "title",
        "author"
      ]
    },
    {
      "_index": "books",
      "_id": "3",
      "_source": {
        "includes": [
          "title",
          "year"
        ]
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mget(
  body =   {
    "docs": [
      {
        "_index": "books",
        "_id": "1",
        "_source": false
      },
      {
        "_index": "books",
        "_id": "2",
        "_source": [
          "title",
          "author"
        ]
      },
      {
        "_index": "books",
        "_id": "3",
        "_source": {
          "includes": [
            "title",
            "year"
          ]
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：擷取儲存的欄位

如果您的索引對應包含儲存的欄位，您可以擷取這些欄位而非文件來源。下列範例從兩份使用者文件中擷取不同的儲存欄位：

<!-- spec_insert_start
component: example_code
rest: GET /_mget
body: |
{
  "docs": [
    {
      "_index": "users",
      "_id": "1",
      "stored_fields": ["name", "location"]
    },
    {
      "_index": "users",
      "_id": "2",
      "stored_fields": ["email", "joined_date"]
    }
  ]
}
-->
{% capture step1_rest %}
GET /_mget
{
  "docs": [
    {
      "_index": "users",
      "_id": "1",
      "stored_fields": [
        "name",
        "location"
      ]
    },
    {
      "_index": "users",
      "_id": "2",
      "stored_fields": [
        "email",
        "joined_date"
      ]
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mget(
  body =   {
    "docs": [
      {
        "_index": "users",
        "_id": "1",
        "stored_fields": [
          "name",
          "location"
        ]
      },
      {
        "_index": "users",
        "_id": "2",
        "stored_fields": [
          "email",
          "joined_date"
        ]
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：指定路由值

如果您在將文件編製索引時使用了自訂路由，則必須在擷取這些文件時提供路由值。下列範例使用路由值擷取兩份訂單文件：第一份文件使用查詢參數中的路由值，第二份文件指定自己的路由值：

<!-- spec_insert_start
component: example_code
rest: GET /_mget?routing=user123
body: |
{
  "docs": [
    {
      "_index": "orders",
      "_id": "1"
    },
    {
      "_index": "orders",
      "_id": "2",
      "routing": "user456"
    }
  ]
}
-->
{% capture step1_rest %}
GET /_mget?routing=user123
{
  "docs": [
    {
      "_index": "orders",
      "_id": "1"
    },
    {
      "_index": "orders",
      "_id": "2",
      "routing": "user456"
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mget(
  params = { "routing": "user123" },
  body =   {
    "docs": [
      {
        "_index": "orders",
        "_id": "1"
      },
      {
        "_index": "orders",
        "_id": "2",
        "routing": "user456"
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

Multi-get Documents API 會傳回一個 `docs` 陣列，其中包含依請求順序排列的已擷取文件。每份文件都包含其中繼資料與來源資料，若文件無法擷取，則包含錯誤資訊。

<details markdown="block">
  <summary>
    從多個索引擷取文件的回應
  </summary>
  {: .text-delta}

```json
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_version": 2,
      "_seq_no": 2,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Fiction",
        "pages": 180
      }
    },
    {
      "_index": "articles",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
        "title": "Introduction to OpenSearch",
        "author": "Jane Smith",
        "published": "2024-01-15",
        "category": "Technology",
        "views": 1500
      }
    }
  ]
}
```
</details>

<details markdown="block">
  <summary>
    使用 IDs 陣列的回應
  </summary>
  {: .text-delta}

```json
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_version": 2,
      "_seq_no": 2,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Fiction",
        "pages": 180
      }
    },
    {
      "_index": "books",
      "_id": "2",
      "_version": 2,
      "_seq_no": 3,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Fiction",
        "pages": 324
      }
    },
    {
      "_index": "books",
      "_id": "3",
      "_version": 1,
      "_seq_no": 4,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
        "pages": 328
      }
    }
  ]
}
```
</details>

<details markdown="block">
  <summary>
    篩選來源欄位的回應
  </summary>
  {: .text-delta}

```json
{
  "docs": [
    {
      "_index": "books",
      "_id": "1",
      "_version": 2,
      "_seq_no": 2,
      "_primary_term": 3,
      "found": true
    },
    {
      "_index": "books",
      "_id": "2",
      "_version": 2,
      "_seq_no": 3,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "author": "Harper Lee",
        "title": "To Kill a Mockingbird"
      }
    },
    {
      "_index": "books",
      "_id": "3",
      "_version": 1,
      "_seq_no": 4,
      "_primary_term": 3,
      "found": true,
      "_source": {
        "year": 1949,
        "title": "1984"
      }
    }
  ]
}
```
</details>

<details markdown="block">
  <summary>
    擷取儲存欄位的回應
  </summary>
  {: .text-delta}

```json
{
  "docs": [
    {
      "_index": "users",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "fields": {
        "name": [
          "Alice Johnson"
        ],
        "location": [
          "San Francisco"
        ]
      }
    },
    {
      "_index": "users",
      "_id": "2",
      "_version": 1,
      "_seq_no": 1,
      "_primary_term": 1,
      "found": true,
      "fields": {
        "joined_date": [
          "2021-06-20T00:00:00.000Z"
        ],
        "email": [
          "bob@example.com"
        ]
      }
    }
  ]
}
```
</details>

<details markdown="block">
  <summary>
    指定路由值的回應
  </summary>
  {: .text-delta}

```json
{
  "docs": [
    {
      "_index": "orders",
      "_id": "1",
      "_version": 2,
      "_seq_no": 3,
      "_primary_term": 14,
      "_routing": "user123",
      "found": true,
      "_source": {
        "order_id": "ORD-001",
        "user_id": "user123",
        "product": "Laptop",
        "amount": 1299.99
      }
    },
    {
      "_index": "orders",
      "_id": "2",
      "_version": 2,
      "_seq_no": 4,
      "_primary_term": 14,
      "_routing": "user456",
      "found": true,
      "_source": {
        "order_id": "ORD-002",
        "user_id": "user456",
        "product": "Smartphone",
        "amount": 899.99
      }
    }
  ]
}
```
</details>

## 回應本文欄位

回應包含一個 `docs` 陣列，每個請求的文件各有一個元素，並依照請求中的順序傳回。下表列出回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`docs` | 物件陣列 | 擷取的文件。每個物件代表一份文件，並包含此表所述的欄位。
`_index` | 字串 | 包含該文件的索引名稱。
`_id` | 字串 | 文件 ID。
`_version` | 整數 | 文件版本號碼。每次更新文件時，此號碼都會遞增。
`_seq_no` | 整數 | 文件在編製索引時被指派的序號。用於樂觀並行控制。
`_primary_term` | 整數 | 文件在編製索引時被指派的主要分片任期。與 `_seq_no` 搭配用於樂觀並行控制。
`found` | 布林值 | 是否找到該文件。如果為 `false`，表示文件不存在，且不包含 `_source` 欄位。
`_source` | 物件 | 文件的原始 JSON 內容。如果 `found` 為 `false`、請求中的 `_source` 設為 `false`，或已指定 `stored_fields`，則會省略。
`fields` | 物件 | 文件的已儲存欄位。僅在請求中指定 `stored_fields` 且 `found` 為 `true` 時包含。每個欄位值都以陣列形式傳回。
`_routing` | 字串 | 用於將文件導向特定分片的路由值。僅在使用自訂路由值時包含。
`error` | 物件 | 因失敗而無法擷取文件時的錯誤資訊。包含錯誤類型與原因的詳細資訊。

## 必要權限

如果您使用 Security 外掛程式，請確保您具有適當的權限：`indices:data/read/mget` 和 `indices:data/read/mget*`。
