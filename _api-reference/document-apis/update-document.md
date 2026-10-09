---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新文件"
parent: Document APIs
nav_order: 10
redirect_from: 
 - /opensearch/rest-api/document-apis/update-document/
---

# Update Document API
**於 1.0 版推出**
{: .label .label-purple }

如果您需要在索引中更新文件的欄位，可以使用 update document API 操作。您可以指定想要放入索引的新資料，或在請求本文中加入指令碼，讓 OpenSearch 執行以更新文件。根據預設，更新操作只會更新索引中已存在的文件。如果文件不存在，API 會傳回錯誤。若要 _upsert_ 文件（更新已存在的文件或將新文件編製索引），請使用 [upsert](#using-the-upsert-operation) 操作。

當您提交更新請求時，OpenSearch 會執行下列操作：

1. 從儲存該文件的分片擷取目前的文件。
2. 使用提供的指令碼，或將部分文件與現有文件合併，以套用更新。
3. 將更新後的文件重新編製索引，並遞增其版本號碼。

雖然文件必須重新編製索引，但與手動使用 `GET` 方法擷取文件、修改文件，再使用 Index API 重新編製索引相比，使用 Update Document API 可減少網路來回次數並將版本衝突降到最低。

若要使用 Update Document API，必須在您的索引中啟用 `_source` 欄位。 
{: .important}

呼叫 Update Document API 時，您無法明確指定資料匯入管線。如果您的索引中定義了 `default_pipeline` 或 `final_pipeline`，則會套用下列行為：

- **Upsert 操作**：將新文件編製索引時，會依指定執行索引中定義的 `default_pipeline` 和 `final_pipeline`。  
- **更新操作**：更新現有文件時，不建議執行資料匯入管線，因為可能會產生錯誤的結果。在更新操作期間執行資料匯入管線的支援已棄用，並將於 3.0.0 版中移除。如果您的索引定義了資料匯入管線，update document 操作會傳回下列棄用警告： 

```
the index [sample-index1] has a default ingest pipeline or a final ingest pipeline, the support of the ingest pipelines for update operation causes unexpected result and will be removed in 3.0.0
```

<!-- spec_insert_start
api: update
component: endpoints
-->
## 端點
```json
POST /{index}/_update/{id}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `id` | **必要** | 字串 | 文件 ID。 |
| `index` | **必要** | 字串 | 索引名稱。根據預設，如果索引不存在，會自動建立。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明 | 必要
:--- | :--- | :--- | :---
`if_seq_no` | 整數 | 僅在文件具有指定的序號時才執行更新操作。 | 否
`if_primary_term` | 整數 | 在文件具有指定的主要分片任期時執行更新操作。 | 否
`lang` | 字串 | 指令碼的語言。預設為 `painless`。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。 | 否
`require_alias` | 布林值 | 指定目的地是否必須是索引別名。預設為 `false`。 | 否
`refresh` | 列舉 | 若為 true，OpenSearch 會重新整理分片，使操作可被搜尋看見。有效選項為 `true`、`false` 和 `wait_for`，後者會告訴 OpenSearch 在執行操作前等待重新整理。預設為 `false`。 | 否
`retry_on_conflict` | 整數 | 如果發生文件衝突，OpenSearch 應重試操作的次數。預設為 0。 | 否
`routing` | 字串 | 將更新操作路由至特定分片的值。 | 否
`_source` | 布林值或清單 | 是否在回應本文中包含 `_source` 欄位。預設為 `false`。此參數也支援以逗號分隔的來源欄位清單，以便在查詢回應中包含多個來源欄位。 | 否
`_source_excludes` | 清單 | 要在查詢回應中排除的來源欄位清單，以逗號分隔。 | 否
`_source_includes` | 清單 | 要在查詢回應中納入的來源欄位清單，以逗號分隔。 | 否
`timeout` | 時間 | 等待叢集回應的時間長度。 | 否
`wait_for_active_shards` | 字串 | 在 OpenSearch 處理更新請求之前必須可用的作用中分片數。預設為 1（僅主要分片）。設為 `all` 或正整數。大於 1 的值需要副本。例如，如果您指定值為 3，則索引必須有兩個副本分散於兩個額外節點上，操作才能成功。 | 否

## 請求本文欄位

您的請求本文必須包含您要用來更新文件的資訊。下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`doc` | 物件 | 包含要合併至現有文件之欄位的部分文件。用於簡單的欄位更新。請參閱[使用 doc 物件更新文件](#updating-a-document-using-a-doc-object)。
`script` | 物件 | 定義如何更新文件的指令碼。用於需要條件式邏輯或計算值的複雜更新。如果同時指定 `doc` 和 `script`，則會忽略 `doc`。請參閱[使用指令碼更新文件](#updating-a-document-using-a-script)。
`upsert` | 物件 | 如果目標文件不存在，則要編製索引的文件。與 `doc` 或 `script` 搭配使用，以進行條件式 upsert 操作。請參閱 [Upsert](#upsert)。
`doc_as_upsert` | 布林值 | 若為 `true`，則更新和插入都使用 `doc` 內容。預設為 `false`。請參閱[以 doc 執行 upsert](#doc-as-upsert)。
`scripted_upsert` | 布林值 | 若為 `true`，則無論文件是否存在都會執行指令碼。預設為 `false`。需要 `script` 和 `upsert` 兩個欄位。請參閱[使用指令碼執行 upsert](#scripted-upsert)。
`detect_noop` | 布林值 | 若為 `true`，OpenSearch 會檢查更新是否變更文件。如果未偵測到變更，則會略過更新。預設為 `true`。請參閱[偵測無操作更新](#detecting-no-op-updates)。

### 指令碼環境與變數

指令碼可透過 `ctx` 對應存取及修改文件，該對應提供下列變數的存取權。

變數 | 說明
:--- | :---
`ctx._source` | 文件來源。您可以讀取及修改此物件以更新文件欄位。
`ctx._index` | 包含該文件之索引的名稱。
`ctx._id` | 文件 ID。
`ctx._version` | 目前的文件版本。
`ctx._routing` | 用於將文件路由至分片的路由值（如果使用了自訂路由）。
`ctx._now` | 目前的時間戳記，以自 epoch 起算的毫秒為單位。
`ctx.op` | 要執行的操作。將此設為 `delete` 可刪除文件，或設為 `none` 以不執行任何操作（no-op）。

您可以在指令碼中使用這些變數，根據文件的目前狀態實作條件式邏輯。

## 範例設定

下列範例使用 `sample-index1` 索引中的測試文件。若要跟著操作，請先建立包含範例文件的索引：

<!-- spec_insert_start
component: example_code
rest: PUT /sample-index1/_doc/1
body: |
{
  "first_name": "Bruce",
  "last_name": "Wayne",
  "age": 35,
  "gadgets": ["batarang"]
}
-->
{% capture step1_rest %}
PUT /sample-index1/_doc/1
{
  "first_name": "Bruce",
  "last_name": "Wayne",
  "age": 35,
  "gadgets": [
    "batarang"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "sample-index1",
  id = "1",
  body =   {
    "first_name": "Bruce",
    "last_name": "Wayne",
    "age": 35,
    "gadgets": [
      "batarang"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求

下列範例示範如何使用不同的請求本文欄位來更新文件。

### 使用 doc 物件更新文件

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "doc": {
    "first_name" : "Bruce",
    "last_name" : "Wayne"
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "doc": {
    "first_name": "Bruce",
    "last_name": "Wayne"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "doc": {
      "first_name": "Bruce",
      "last_name": "Wayne"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用指令碼更新文件

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script" : {
    "source": "ctx._source.secret_identity = \"Batman\""
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": {
    "source": "ctx._source.secret_identity = \"Batman\""
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": {
      "source": "ctx._source.secret_identity = \"Batman\""
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用 upsert 操作

Upsert 是一種依據請求中的資訊，有條件地更新現有文件或插入新文件的操作。當您不確定文件是否已存在，並希望無論如何都確保內容正確時，這個操作非常有用。

#### Upsert

在下列範例中，`upsert` 操作會在文件已存在時更新 `first_name` 與 `last_name` 欄位。如果文件不存在，則會使用 `upsert` 物件中的內容為新文件編製索引。

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "doc": {
    "first_name": "Martha",
    "last_name": "Rivera"
  },
  "upsert": {
    "last_name": "Oliveira",
    "age": "31"
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "doc": {
    "first_name": "Martha",
    "last_name": "Rivera"
  },
  "upsert": {
    "last_name": "Oliveira",
    "age": "31"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "doc": {
      "first_name": "Martha",
      "last_name": "Rivera"
    },
    "upsert": {
      "last_name": "Oliveira",
      "age": "31"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

假設某個索引包含下列文件：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_score": 1,
  "_source": {
    "first_name": "Bruce",
    "last_name": "Wayne"
  }
}
```
{% include copy-curl.html %}

執行 upsert 操作後，文件的 `first_name` 與 `last_name` 欄位會被更新：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_score": 1,
  "_source": {
    "first_name": "Martha",
    "last_name": "Rivera"
  }
}
```
{% include copy-curl.html %}

如果索引中不存在該文件，則會使用 `upsert` 物件中指定的欄位為新文件編製索引：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_score": 1,
  "_source": {
    "last_name": "Oliveira",
    "age": "31"
  }
}
```
{% include copy-curl.html %}

#### 以 doc 執行 upsert

您也可以在請求中加入 `doc_as_upsert` 並將其設為 `true`，以使用 `doc` 欄位中的資訊執行 upsert 操作：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "doc": {
    "first_name": "Martha",
    "last_name": "Oliveira",
    "age": "31"
  },
  "doc_as_upsert": true
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "doc": {
    "first_name": "Martha",
    "last_name": "Oliveira",
    "age": "31"
  },
  "doc_as_upsert": true
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "doc": {
      "first_name": "Martha",
      "last_name": "Oliveira",
      "age": "31"
    },
    "doc_as_upsert": true
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

假設某個索引包含下列文件：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_score": 1,
  "_source": {
    "first_name": "Bruce",
    "last_name": "Wayne"
  }
}
```
{% include copy-curl.html %}

執行 upsert 操作後，文件的 `first_name` 與 `last_name` 欄位會被更新，並新增一個 `age` 欄位。如果索引中不存在該文件，則會使用 `doc` 物件中的欄位建立新文件：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_score": 1,
  "_source": {
    "first_name": "Martha",
    "last_name": "Oliveira",
    "age": "31"
  }
}
```
{% include copy-curl.html %}

#### 使用指令碼執行 upsert

您也可以使用指令碼來控制文件的更新方式。將 `scripted_upsert` 參數設為 `true`，即可指示 OpenSearch 即使文件尚不存在也使用該指令碼。這讓您能夠在指令碼中定義整個 upsert 邏輯。

在下列範例中，無論文件先前是否存在，指令碼都會將文件設定為包含特定欄位：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/2
body: |
{
  "scripted_upsert": true,
  "script": {
    "source": "ctx._source.first_name = params.first_name; ctx._source.last_name = params.last_name; ctx._source.age = params.age;",
    "params": {
      "first_name": "Selina",
      "last_name": "Kyle",
      "age": 28
    }
  },
  "upsert": {}
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/2
{
  "scripted_upsert": true,
  "script": {
    "source": "ctx._source.first_name = params.first_name; ctx._source.last_name = params.last_name; ctx._source.age = params.age;",
    "params": {
      "first_name": "Selina",
      "last_name": "Kyle",
      "age": 28
    }
  },
  "upsert": {}
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "2",
  index = "sample-index1",
  body =   {
    "scripted_upsert": true,
    "script": {
      "source": "ctx._source.first_name = params.first_name; ctx._source.last_name = params.last_name; ctx._source.age = params.age;",
      "params": {
        "first_name": "Selina",
        "last_name": "Kyle",
        "age": 28
      }
    },
    "upsert": {}
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果 ID 為 `2` 的文件尚不存在，此操作會使用該指令碼建立文件。如果文件已存在，指令碼則會更新指定的欄位。在這兩種情況下，結果都是：

```json
{
  "_index": "sample-index1",
  "_id": "2",
  "_score": 1,
  "_source": {
    "first_name": "Selina",
    "last_name": "Kyle",
    "age": 28
  }
}
```
{% include copy-curl.html %}

當標準的 `doc` 型操作不夠靈活時，使用 `scripted_upsert` 可讓您完全掌控文件的建立與更新。

### 偵測無操作更新

依預設，OpenSearch 會偵測更新操作是否確實變更文件。如果更新未做出任何變更，OpenSearch 會略過該操作並傳回 `"result": "noop"`，表示未執行任何操作。當文件已包含您嘗試設定的值時，這項最佳化可避免不必要的重新編製索引。

下列範例嘗試以文件 `1` 已包含的值更新該文件：

```json
POST /sample-index1/_update/1
{
  "doc": {
    "first_name": "Bruce",
    "last_name": "Wayne",
    "age": 35
  }
}
```
{% include copy-curl.html %}

由於文件已有完全相同的值，OpenSearch 偵測到沒有變更，並傳回無操作回應：

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_version": 2,
  "result": "noop",
  "_shards": {
    "total": 0,
    "successful": 0,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```
{% include copy-curl.html %}

請注意，偵測到無操作時，`_shards.total` 為 `0`，表示未執行任何分片操作。

您可以將 `detect_noop` 設為 `false`，以停用無操作偵測。這會強制 OpenSearch 重新編製文件索引，即使值未變更：

```json
POST /sample-index1/_update/1
{
  "doc": {
    "first_name": "Bruce",
    "last_name": "Wayne",
    "age": 35
  },
  "detect_noop": false
}
```
{% include copy-curl.html %}

停用 `noop` 偵測後，即使內容完全相同，OpenSearch 仍會重新編製文件索引，並遞增其版本號碼。


## 回應範例

```json
{
  "_index": "sample-index1",
  "_id": "1",
  "_version": 3,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 4,
  "_primary_term": 17
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 說明
:--- | :---
`_index` | 索引的名稱。
`_id` | 文件的 ID。
`_version` | 文件的版本。每次更新文件時都會遞增。
`result` | 更新操作的結果。文件成功更新時傳回 `updated`，upsert 操作建立新文件時傳回 `created`，未做出任何變更時則傳回 `noop`。
`_shards` | 叢集分片的詳細資訊。
`_shards.total` | 分片總數（主要分片和副本分片）。
`_shards.successful` | 成功處理更新操作的分片數量。
`_shards.failed` | 處理更新操作失敗的分片數量。
`_seq_no` | 更新文件時指派的序號。用於樂觀並行控制。
`_primary_term` | 更新文件時指派的主要分片任期。與 `_seq_no` 搭配用於樂觀並行控制。

## 進階指令碼範例

下列範例示範用於文件更新的進階指令碼功能。

#### 在陣列中新增項目

您可以使用指令碼在陣列欄位中新增項目。下列範例在 `gadgets` 陣列中新增一個小工具（即使該小工具已存在於清單中，仍會新增）：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script": {
    "source": "ctx._source.gadgets.add(params.gadget)",
    "lang": "painless",
    "params": {
      "gadget": "grappling hook"
    }
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": {
    "source": "ctx._source.gadgets.add(params.gadget)",
    "lang": "painless",
    "params": {
      "gadget": "grappling hook"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": {
      "source": "ctx._source.gadgets.add(params.gadget)",
      "lang": "painless",
      "params": {
        "gadget": "grappling hook"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 從陣列中移除項目

您可以使用指令碼從陣列中移除項目。Painless 的 `remove` 函式接受您要移除之元素的陣列索引值。為避免執行階段錯誤，請先確認該項目存在。如果清單包含重複項目，此指令碼只會移除其中一個：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script": {
    "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx._source.gadgets.remove(ctx._source.gadgets.indexOf(params.gadget)) }",
    "lang": "painless",
    "params": {
      "gadget": "grappling hook"
    }
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": {
    "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx._source.gadgets.remove(ctx._source.gadgets.indexOf(params.gadget)) }",
    "lang": "painless",
    "params": {
      "gadget": "grappling hook"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": {
      "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx._source.gadgets.remove(ctx._source.gadgets.indexOf(params.gadget)) }",
      "lang": "painless",
      "params": {
        "gadget": "grappling hook"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 新增和移除欄位

您可以使用指令碼在文件中新增或移除欄位。下列範例新增一個欄位：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script": "ctx._source.bat_signal_location = 'Gotham City Hall'"
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": "ctx._source.bat_signal_location = 'Gotham City Hall'"
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": "ctx._source.bat_signal_location = 'Gotham City Hall'"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例移除一個欄位：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script": "ctx._source.remove('bat_signal_location')"
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": "ctx._source.remove('bat_signal_location')"
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": "ctx._source.remove('bat_signal_location')"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 變更操作類型

您可以使用指令碼，根據文件內容變更要執行的操作。在下列範例中，如果 `gadgets` 欄位包含 `kryptonite`，就會刪除文件；否則不會執行任何操作（`noop`）：

<!-- spec_insert_start
component: example_code
rest: POST /sample-index1/_update/1
body: |
{
  "script": {
    "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx.op = 'delete' } else { ctx.op = 'none' }",
    "lang": "painless",
    "params": {
      "gadget": "kryptonite"
    }
  }
}
-->
{% capture step1_rest %}
POST /sample-index1/_update/1
{
  "script": {
    "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx.op = 'delete' } else { ctx.op = 'none' }",
    "lang": "painless",
    "params": {
      "gadget": "kryptonite"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update(
  id = "1",
  index = "sample-index1",
  body =   {
    "script": {
      "source": "if (ctx._source.gadgets.contains(params.gadget)) { ctx.op = 'delete' } else { ctx.op = 'none' }",
      "lang": "painless",
      "params": {
        "gadget": "kryptonite"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 錯誤回應

以下範例顯示使用 Update Document API 時可能遇到的常見錯誤回應。

### 找不到文件

如果您嘗試更新索引中不存在的文件，且未使用 upsert 操作，OpenSearch 會傳回 404 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "document_missing_exception",
        "reason": "[1]: document missing",
        "index": "sample-index1",
        "shard": "0",
        "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA"
      }
    ],
    "type": "document_missing_exception",
    "reason": "[1]: document missing",
    "index": "sample-index1",
    "shard": "0",
    "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA"
  },
  "status": 404
}
```

若要避免此錯誤，請使用 [upsert 操作](#using-the-upsert-operation) 在文件不存在時建立該文件。

### 版本衝突

如果您使用 `if_seq_no` 與 `if_primary_term` 參數進行樂觀並行控制，而文件在您上次讀取後已被修改，OpenSearch 會傳回 409 衝突錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "version_conflict_engine_exception",
        "reason": "[1]: version conflict, required seqNo [3], primary term [1]. current document has seqNo [4] and primary term [1]",
        "index": "sample-index1",
        "shard": "0",
        "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA"
      }
    ],
    "type": "version_conflict_engine_exception",
    "reason": "[1]: version conflict, required seqNo [3], primary term [1]. current document has seqNo [4] and primary term [1]",
    "index": "sample-index1",
    "shard": "0",
    "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA"
  },
  "status": 409
}
```

若要處理此錯誤，請擷取文件的最新版本，並使用正確的 `if_seq_no` 與 `if_primary_term` 值重試更新，或使用 `retry_on_conflict` 參數自動重試該操作。

### 指令碼編譯錯誤

如果您的 Painless 指令碼有錯誤，OpenSearch 會傳回 400 錯誤，並附上編譯失敗的詳細資訊：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "failed to execute script"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "failed to execute script",
    "caused_by": {
      "type": "script_exception",
      "reason": "compile error",
      "script_stack": [
        "ctx._source.value = params.newValue",
        "                         ^---- HERE"
      ],
      "script": "ctx._source.value = params.newValue",
      "lang": "painless",
      "position": {
        "offset": 25,
        "start": 0,
        "end": 34
      },
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "cannot resolve symbol [params.newValue]"
      }
    }
  },
  "status": 400
}
```

請檢查錯誤回應中的 `script_stack` 與 `caused_by` 欄位，以找出並修正指令碼錯誤。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:data/write/update`。
