---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "提取式資料匯入管理"
parent: Pull-based ingestion
grand_parent: Document APIs
has_children: false
nav_order: 10
---

# 提取式資料匯入管理 API
**於 3.0 版推出**
{: .label .label-purple }

OpenSearch 提供下列 API 來管理提取式資料匯入。

## 暫停資料匯入

暫停一或多個索引的資料匯入。暫停時，OpenSearch 會停止從串流來源取用指定索引中所有分片的資料。

### 端點

```json
POST /{index}/ingestion/_pause
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | String | 必要 | 要暫停的索引。可為以逗號分隔的多個索引名稱清單。 |

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `cluster_manager_timeout` | Time units | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。 |
| `timeout` | Time units | 等待叢集回應的時間長度。預設為 `30s`。 |

### 範例請求

<!-- spec_insert_start
component: example_code
rest: POST /my-index/ingestion/_pause
-->
{% capture step1_rest %}
POST /my-index/ingestion/_pause
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.pause(
  index = "my-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 繼續資料匯入

繼續一或多個索引的資料匯入。繼續時，OpenSearch 會繼續從串流來源取用指定索引中所有分片的資料。

在繼續作業中，您可以選擇性地重設串流消費者，使其從特定的位移量或時間戳記開始讀取。若指定了重設設定，則在對索引套用繼續作業之前，會先重設所選分片的所有消費者。重設消費者也會觸發內部重新整理，以保存變更。

### 端點

```json
POST /{index}/ingestion/_resume
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | String | 必要 | 要繼續資料匯入的索引。可為以逗號分隔的多個索引名稱清單。 |

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 |  說明 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | Time units | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。 |
| `timeout` | Time units | 等待叢集回應的時間長度。預設為 `30s`。 |

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `reset_settings` | Array | 選用 | 每個分片的重設設定清單。若未提供，OpenSearch 會從指定索引中每個分片的目前位置繼續資料匯入。 |
| `reset_settings.shard` | Integer | 必要 | 要重設的分片。 |
| `reset_settings.mode` | String | 必要 | 重設模式。有效值為 `offset` (正整數位移量) 與 `timestamp` (以毫秒為單位的 Unix 時間戳記)。 |
| `reset_settings.value` | String | 必要 | &ensp;&#x2022; `offset`：Apache Kafka 位移量或 Amazon Kinesis 序號<br>&ensp;&#x2022; `timestamp`：以毫秒為單位的 Unix 時間戳記。 |

### 範例請求

若要在不指定重設設定的情況下繼續資料匯入，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/ingestion/_resume
-->
{% capture step1_rest %}
POST /my-index/ingestion/_resume
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.resume(
  index = "my-index",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要在繼續資料匯入時提供重設設定，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/ingestion/_resume
body: |
{
  "reset_settings": [
    {
      "shard": 0,
      "mode": "offset",
      "value": "1"
    }
  ]
}
-->
{% capture step1_rest %}
POST /my-index/ingestion/_resume
{
  "reset_settings": [
    {
      "shard": 0,
      "mode": "offset",
      "value": "1"
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.resume(
  index = "my-index",
  body =   {
    "reset_settings": [
      {
        "shard": 0,
        "mode": "offset",
        "value": "1"
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 取得資料匯入狀態

傳回一或多個索引目前的資料匯入狀態。此 API 支援分頁。

### 端點

```json
GET /{index}/ingestion/_state
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | String | 必要 | 要傳回資料匯入狀態的索引。可為以逗號分隔的多個索引名稱清單。 |

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `timeout` | Time units | 等待叢集回應的時間長度。預設為 `30s`。 |

### 範例請求

以下是使用預設設定的請求：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/ingestion/_state
-->
{% capture step1_rest %}
GET /my-index/ingestion/_state
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.get_state(
  index = "my-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例顯示頁面大小為 20 的請求：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/ingestion/_state?size=20
-->
{% capture step1_rest %}
GET /my-index/ingestion/_state?size=20
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.get_state(
  index = "my-index",
  params = { "size": "20" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例顯示帶有下一頁權杖的請求：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/ingestion/_state?size=20&next_token=<next_page_token>
-->
{% capture step1_rest %}
GET /my-index/ingestion/_state?size=20&next_token=<next_page_token>
{% endcapture %}

{% capture step1_python %}


response = client.ingestion.get_state(
  index = "my-index",
  params = { "size": "20", "next_token": "<next_page_token>" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例回應

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0,
    "failures": [
      {
        "shard": 0,
        "index": "my-index",
        "status": "INTERNAL_SERVER_ERROR",
        "reason": {
          "type": "timeout_exception",
          "reason": "error message"
        }
      }
    ]
  },
  "next_page_token" : "page token if not on last page",
  "ingestion_state": {
    "indexName": [
      {
        "shard": 0,
        "poller_state": "POLLING",
        "error_policy": "DROP",
        "poller_paused": false,
        "write_block_enabled" : false,
        "batch_start_pointer" : "KafkaOffset{offset=2}",
        "is_primary" : true,
        "node" : "node_name"
      }
    ]
  }
}
```