---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得資料串流統計"
parent: Data stream APIs
nav_order: 30
redirect_from:
  - /api-reference/index-apis/data-stream-stats/
---

# Data Stream Stats API
**於 1.0 版導入**
{: .label .label-purple }

Data Stream Stats API 提供一或多個資料串流的統計資訊，包括後備索引 (backing index) 的數量、儲存大小與最大時間戳記。請使用此 API 監控各資料串流的儲存與索引活動。

<!-- spec_insert_start
api: indices.data_streams_stats
component: endpoints
-->
## 端點
```json
GET /_data_stream/_stats
GET /_data_stream/{name}/_stats
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: indices.data_streams_stats
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | List 或 String | 以逗號分隔的資料串流清單，用於限制請求範圍。支援萬用字元運算式 (`*`)。若要指定叢集中的所有資料串流，請省略此參數或使用 `*`。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `error_trace` | Boolean | 是否包含所回傳錯誤的堆疊追蹤。 | `false` |
| `filter_path` | List 或 String | 用於篩減回應。此參數接受以逗號分隔的篩選器清單，支援使用萬用字元比對任何欄位或欄位名稱的一部分。您也可以使用 `-` 排除欄位。 | N/A |
| `human` | Boolean | 是否以人類可讀的格式回傳統計值。 | `false` |
| `pretty` | Boolean | 是否將回傳的 JSON 回應格式化為易讀樣式。 | `false` |
| `source` | String | 經 URL 編碼的請求定義。適用於不支援在非 POST 請求中附帶請求本文的用戶端程式庫。 | N/A |

## 範例請求

建立一個包含相符模式並啟用資料串流的索引範本：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/template-logs-app
body: |
{
  "index_patterns": ["logs-app*"],
  "data_stream": {}
}
-->
{% capture step1_rest %}
PUT /_index_template/template-logs-app
{
  "index_patterns": [
    "logs-app*"
  ],
  "data_stream": {}
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "template-logs-app",
  body =   {
    "index_patterns": [
      "logs-app*"
    ],
    "data_stream": {}
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

建立資料串流：

<!-- spec_insert_start
component: example_code
rest: PUT /_data_stream/logs-app
body: {}
-->
{% capture step1_rest %}
PUT /_data_stream/logs-app
{}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create_data_stream(
  name = "logs-app",
  body =   {}
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

將文件編製索引以產生後備索引：

<!-- spec_insert_start
component: example_code
rest: POST /logs-app/_doc
body: |
{
  "@timestamp": "2025-06-23T10:00:00Z",
  "message": "app started"
}
-->
{% capture step1_rest %}
POST /logs-app/_doc
{
  "@timestamp": "2025-06-23T10:00:00Z",
  "message": "app started"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "logs-app",
  body =   {
    "@timestamp": "2025-06-23T10:00:00Z",
    "message": "app started"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

擷取資料串流的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_data_stream/logs-app/_stats?human=true
-->
{% capture step1_rest %}
GET /_data_stream/logs-app/_stats?human=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.data_streams_stats(
  name = "logs-app",
  params = { "human": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "data_stream_count": 1,
  "backing_indices": 1,
  "total_store_size": "16.8kb",
  "total_store_size_bytes": 17304,
  "data_streams": [
    {
      "data_stream": "logs-app",
      "backing_indices": 1,
      "store_size": "16.8kb",
      "store_size_bytes": 17304,
      "maximum_timestamp": 1750673100000
    }
  ]
}
```

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_shards.total` | Integer | 請求所涉及的分片總數。 |
| `_shards.successful` | Integer | 成功擷取的分片數量。 |
| `_shards.failed` | Integer | 擷取失敗的分片數量。 |
| `data_stream_count` | Integer | 回應中回傳的資料串流總數。 |
| `backing_indices` | Integer | 所有資料串流的後備索引總數。 |
| `total_store_size` | String | 所有資料串流儲存空間的人類可讀總大小。僅在 `human=true` 時顯示。 |
| `total_store_size_bytes` | Integer | 所有資料串流使用的儲存空間總量，單位為位元組。 |
| `data_streams` | Array | 物件清單，每個資料串流一個物件。物件欄位請參閱 [資料串流物件](#the-data-stream-objects)。 |

### 資料串流物件

每個資料串流物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `data_stream` | String | 資料串流的名稱。 |
| `backing_indices` | Integer | 該資料串流的後備索引數量。 |
| `store_size` | String | 該資料串流使用儲存空間的人類可讀大小。僅在 `human=true` 時顯示。 |
| `store_size_bytes` | Integer | 該資料串流使用的儲存空間總量，單位為位元組。 |
| `maximum_timestamp` | Long | 資料串流中所有文件的最大時間戳記。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/data_stream/stats`。

## 相關文件

- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [取得資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-info/)
