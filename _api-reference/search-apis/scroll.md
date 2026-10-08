---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "捲動"
parent: Search APIs
nav_order: 30
redirect_from:
 - /opensearch/rest-api/scroll/
 - /api-reference/scroll/
---

# Scroll API
**於 1.0 版推出**
{: .label .label-purple }

您可以使用 `scroll` 操作擷取大量結果。例如，針對機器學習作業，您可以分批請求不限數量的結果。

若要使用 `scroll` 操作，請在請求標頭中加入 `scroll` 參數，指定搜尋情境，告知 OpenSearch 您需要持續捲動多久。此搜尋情境的持續時間必須足以處理單一批次的結果。

由於搜尋情境會消耗大量記憶體，我們建議您不要將 `scroll` 操作用於頻繁的使用者查詢。請改用 `sort` 參數搭配 `search_after` 參數，捲動擷取使用者查詢的回應。
{: .note }

請注意下列效能考量：

- 若不需要計算相關性分數，請依 `_doc` 排序，以達到最有效率的捲動。這會停用評分，並依文件在索引中的自然順序傳回文件，這是逐一處理索引中所有文件最快的方式。
- 只有初始搜尋回應會包含彙總結果。後續捲動請求只會傳回下一批命中結果。
- 每個開啟的捲動情境都會阻止相關分片上的區段合併，並消耗檔案控制代號和堆積記憶體。一旦不再需要捲動情境，請立即關閉。
- 開啟的捲動情境數量上限由 `search.max_open_scroll_context` 叢集設定控制，預設為 500。

<!-- spec_insert_start
api: scroll
component: endpoints
-->
## 端點
```json
GET  /_search/scroll
POST /_search/scroll
GET  /_search/scroll/{scroll_id}
POST /_search/scroll/{scroll_id}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `scroll_id` | 字串 | 搜尋的捲動 ID。由於捲動 ID 可能很長，我們建議改在請求本文中指定捲動 ID。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `scroll` | 字串 | 延長搜尋情境的時間長度。此值會覆寫原始搜尋請求中 `scroll` 參數設定的持續時間。不得超過 `search.max_keep_alive` 叢集設定。 | 無 |
| `scroll_id` | 字串 | 搜尋的捲動 ID。由於捲動 ID 可能很長，我們建議在請求本文中指定捲動 ID，而非使用查詢參數。 | 無 |
| `rest_total_hits_as_int` | 布林值 | `hits.total` 屬性是以整數（`true`）還是物件（`false`）傳回。 | `false` |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `scroll` | 字串 | 為下一個捲動請求延長搜尋情境的時間長度。如果同時指定查詢參數和請求本文欄位，則查詢參數優先。 |
| `scroll_id` | 字串 | 必要。初始搜尋請求或上一個捲動請求傳回的捲動 ID。 |

## 請求範例

下列範例示範從啟動捲動操作到擷取所有結果的捲動工作流程。

### 步驟 1：啟動捲動操作

若要開始捲動，請傳送包含 `scroll` 參數的初始搜尋查詢，指定搜尋情境的保留時間（例如，`10m` 表示 10 分鐘）。使用 `size` 參數設定每批傳回的結果數量：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search?scroll=10m
body: |
{
  "size": 10000
}
-->
{% capture step1_rest %}
GET /shakespeare/_search?scroll=10m
{
  "size": 10000
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "shakespeare",
  params = { "scroll": "10m" },
  body =   {
    "size": 10000
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

OpenSearch 會快取結果，並傳回捲動 ID，讓您分批存取結果：

```json
"_scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
```

### 步驟 2：擷取後續批次

將此捲動 ID 傳遞給 `scroll` 操作，以取得下一批結果：

<!-- spec_insert_start
component: example_code
rest: GET /_search/scroll
body: |
{
  "scroll": "10m",
  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
}
-->
{% capture step1_rest %}
GET /_search/scroll
{
  "scroll": "10m",
  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
}
{% endcapture %}

{% capture step1_python %}


response = client.scroll(
  body =   {
    "scroll": "10m",
    "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

使用此捲動 ID，只要搜尋情境仍開啟，您就能以每批 10,000 筆的方式取得結果。捲動 ID 通常不會在請求之間變更，但它*可能*變更，因此請務必始終使用最新的捲動 ID。如果您未在設定的搜尋情境持續時間內傳送下一個捲動請求，`scroll` 操作就不會傳回任何結果。

### 偵測結果結尾

當您捲動完所有結果時，最後一批會包含空的 `hits` 陣列：

```json
{
  "_scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ==",
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

當 `hits.hits` 為空陣列時，表示您已擷取所有可用結果，應停止捲動。請務必關閉捲動情境以釋放資源。

### 使用切片捲動

如果您預期會有數十億筆結果，請使用切片捲動。切片可讓您針對同一個請求平行執行多個捲動操作。
設定捲動的 ID 和切片數量上限：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search?scroll=10m
body: |
{
  "slice": {
    "id": 0,
    "max": 10
  },
  "query": {
    "match_all": {}
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search?scroll=10m
{
  "slice": {
    "id": 0,
    "max": 10
  },
  "query": {
    "match_all": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "shakespeare",
  params = { "scroll": "10m" },
  body =   {
    "slice": {
      "id": 0,
      "max": 10
    },
    "query": {
      "match_all": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

每個切片都會產生各自獨立的捲動 ID。使用 `"max": 10` 時，您會啟動 10 個獨立的捲動操作（ID 為 0 到 9），每個操作都會傳回不同的資料子集。接著，您可以獨立捲動每個切片，直到所有切片的結果都已擷取完畢。切片數量受 `index.max_slices_per_scroll` 設定限制，其預設值為 `1024`。

### 步驟 3：關閉捲動情境

完成捲動後，請關閉搜尋情境，因為 `scroll` 操作會持續消耗運算資源，直到逾時：

<!-- spec_insert_start
component: example_code
rest: DELETE /_search/scroll/DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAcWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ==
-->
{% capture step1_rest %}
DELETE /_search/scroll/DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAcWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ==
{% endcapture %}

{% capture step1_python %}


response = client.clear_scroll(
  scroll_id = "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAcWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ==",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要關閉所有開啟的捲動情境：

<!-- spec_insert_start
component: example_code
rest: DELETE /_search/scroll/_all
-->
{% capture step1_rest %}
DELETE /_search/scroll/_all
{% endcapture %}

{% capture step1_python %}


response = client.clear_scroll(
  scroll_id = "_all",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

捲動搜尋的結果反映初始搜尋請求當下的索引狀態。在啟動捲動後才編製索引或修改的文件，即使符合查詢，也不會出現在捲動結果中。
{: .important}

## 回應範例

捲動操作會傳回與搜尋 API 相同的回應結構，包括 `_scroll_id`、`hits`、`_shards` 和時間資訊。

清除捲動操作會傳回下列回應：

```json
{
  "succeeded": true,
  "num_freed": 1
}
```

## 回應本文欄位

下表列出捲動操作的回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_scroll_id` | 字串 | 下一個捲動請求要使用的捲動 ID。此值可能會在請求之間變更，因此請始終使用最近傳回的 ID。 |
| `took` | 整數 | 請求完成所花費的時間，以毫秒為單位。 |
| `timed_out` | 布林值 | 請求是否在完成前逾時。 |
| `_shards` | 物件 | 參與操作的分片資訊，包括 `total`、`successful`、`skipped` 和 `failed` 的數量。 |
| `hits` | 物件 | 搜尋結果，包括 `total` 命中數量和符合條件的文件陣列。捲動完成時，`hits.hits` 為空陣列。 |

下表列出清除捲動操作的回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `succeeded` | 布林值 | 是否已成功釋放捲動情境。 |
| `num_freed` | 整數 | 已釋放的捲動情境數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確定您具備適當的權限：`indices:data/read/scroll` 和 `indices:data/read/scroll/clear`。

## 相關文件

- [分頁顯示結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)
- [Point in Time API]({{site.url}}{{site.baseurl}}/search-plugins/point-in-time-api/)
