---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得資料串流"
parent: Data stream APIs
nav_order: 20
---

# Get Data Stream API
**於 1.0 版導入**
{: .label .label-purple }

Get Data Stream API 會傳回一或多個資料串流的資訊，包括其後備索引、世代與狀態。

<!-- spec_insert_start
api: indices.get_data_stream
component: endpoints
-->
## 端點
```json
GET /_data_stream
GET /_data_stream/{name}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: indices.get_data_stream
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | List 或 String | 以逗號分隔的資料串流名稱清單，用於限制請求範圍。支援萬用字元 (`*`) 運算式。若省略，則傳回所有資料串流。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `error_trace` | Boolean | 是否在傳回的錯誤中包含堆疊追蹤。 | `false` |
| `filter_path` | List 或 String | 用於縮減回應內容。此參數接受以逗號分隔的篩選條件清單，並支援使用萬用字元比對任何欄位名稱或其部分。您也可以使用 `-` 排除欄位。 | N/A |
| `human` | Boolean | 是否以人類可讀的格式傳回統計數值。 | `false` |
| `pretty` | Boolean | 是否將傳回的 JSON 回應格式化為易讀樣式。 | `false` |
| `source` | String | 經 URL 編碼的請求定義。對於不接受非 POST 請求本文的程式庫很有用。 | N/A |


## 範例請求

下列範例請求會傳回叢集中所有資料串流的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_data_stream
-->
{% capture step1_rest %}
GET /_data_stream
{% endcapture %}

{% capture step1_python %}

response = client.indices.get_data_stream()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要傳回特定資料串流的資訊，請將其名稱作為 `name` 路徑參數提供：

<!-- spec_insert_start
component: example_code
rest: GET /_data_stream/logs-app
-->
{% capture step1_rest %}
GET /_data_stream/logs-app
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_data_stream(
  name = "logs-app"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "data_streams": [
    {
      "name": "logs-app",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-logs-app-000001",
          "index_uuid": "23dD0HE5Sg2kSLLAP_YtNA"
        }
      ],
      "generation": 1,
      "status": "YELLOW",
      "template": "template-logs-app"
    }
  ]
}
```

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `data_streams` | Array | 物件清單，每個資料串流一個物件。物件欄位請參閱[資料串流物件](#the-data-stream-objects)。 |

### 資料串流物件

每個資料串流物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | String | 資料串流的名稱。 |
| `timestamp_field` | Object | 資料串流的時間戳記欄位組態。 |
| `timestamp_field.name` | String | 時間戳記欄位的名稱，通常為 `@timestamp`。 |
| `indices` | Array | 資料串流後備索引的清單。陣列中的最後一個項目是目前用於寫入的索引。物件欄位請參閱[後備索引物件](#the-backing-index-objects)。 |
| `generation` | Integer | 資料串流目前的世代。此數字每次輪替 (rollover) 時會加一。 |
| `status` | String | 資料串流的健康狀態，依據其後備索引的健康狀態而定。有效值為 `GREEN`、`YELLOW` 與 `RED`。 |
| `template` | String | 用於建立此資料串流的索引範本名稱。 |
| `hidden` | Boolean | 資料串流是否為隱藏。 |
| `system` | Boolean | 資料串流是否由 OpenSearch 內部管理，且無法透過一般使用者操作修改。 |
| `ilm_policy` | String | 相關聯的 Index State Management (ISM) 政策名稱（若有設定）。 |
| `allow_custom_routing` | Boolean | 資料串流是否允許在寫入請求中使用自訂路由。 |
| `_meta` | Object | 附加至資料串流的自訂中繼資料。 |

### 後備索引物件

每個後備索引物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index_name` | String | 後備索引的名稱。 |
| `index_uuid` | String | 後備索引的 UUID。 |

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/data_stream/get`。

## 相關文件

- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [取得資料串流統計]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-stats/)
