---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋分片"
parent: Search APIs
nav_order: 85
---

# 搜尋分片 API
**於 1.0 版導入**
{: .label .label-purple }

`_search_shards` API 提供相關資訊，說明如果執行請求，OpenSearch 會將搜尋請求路由到哪些分片。這可協助您了解 OpenSearch 計畫如何將查詢分配到各分片，而無需實際執行搜尋。此 API 不會執行搜尋，但可讓您檢視路由決策、分片分佈，以及將處理該請求的節點。

## 端點

```json
GET /_search_shards
GET /{index}/_search_shards
POST /_search_shards
POST /{index}/_search_shards
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| --------- | ------ | ------------------------------------------------------ |
| `<index>` | 字串 | 以逗號分隔的目標索引名稱清單。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| `allow_no_indices` | 布林值 | 若為 `true`，當萬用字元運算式或索引別名未解析到任何具體索引時，請求不會失敗。預設為 `true`。 |
| `expand_wildcards` | 字串 | 控制萬用字元運算式的展開方式。選項為：`open`（預設）、`closed`、`hidden`、`none` 或 `all`。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，將忽略遺失或已關閉的索引。預設為 `false`。 |
| `local` | 布林值 | 若為 `true`，此操作僅在本機節點上執行，不會從叢集管理員節點擷取狀態。預設為 `false`。 |
| `preference` | 字串 | 指定選取目標分片或節點時的偏好設定。如需更多資訊，請參閱 [`preference` 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter)。 |
| `routing` | 字串 | 以逗號分隔的特定路由值清單，用於分片選取。 |


## 請求本文欄位

請求本文可包含完整的搜尋查詢，以模擬請求的路由方式：

```json
{
  "query": {
    "term": {
      "user": "alice"
    }
  }
}
```

## 範例

建立索引：

```json
PUT /logs-demo
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "user": { "type": "keyword" },
      "message": { "type": "text" },
      "@timestamp": { "type": "date" }
    }
  }
}
```
{% include copy-curl.html %}

使用 `routing=user1` 為第一份文件編製索引：

<!-- spec_insert_start
component: example_code
rest: POST /logs-demo/_doc?routing=user1
body: |
{
  "@timestamp": "2025-05-23T10:00:00Z",
  "user": "user1",
  "message": "User login successful"
}
-->
{% capture step1_rest %}
POST /logs-demo/_doc?routing=user1
{
  "@timestamp": "2025-05-23T10:00:00Z",
  "user": "user1",
  "message": "User login successful"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "logs-demo",
  params = { "routing": "user1" },
  body =   {
    "@timestamp": "2025-05-23T10:00:00Z",
    "user": "user1",
    "message": "User login successful"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

使用 `routing=user2` 為第二份文件編製索引：

<!-- spec_insert_start
component: example_code
rest: POST /logs-demo/_doc?routing=user2
body: |
{
  "@timestamp": "2025-05-23T10:01:00Z",
  "user": "user2",
  "message": "User login failed"
}
-->
{% capture step1_rest %}
POST /logs-demo/_doc?routing=user2
{
  "@timestamp": "2025-05-23T10:01:00Z",
  "user": "user2",
  "message": "User login failed"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "logs-demo",
  params = { "routing": "user2" },
  body =   {
    "@timestamp": "2025-05-23T10:01:00Z",
    "user": "user2",
    "message": "User login failed"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例請求

使用 `_search_shards` 模擬路由：

<!-- spec_insert_start
component: example_code
rest: POST /logs-demo/_search_shards?routing=user1
body: |
{
  "query": {
    "term": {
      "user": "user1"
    }
  }
}
-->
{% capture step1_rest %}
POST /logs-demo/_search_shards?routing=user1
{
  "query": {
    "term": {
      "user": "user1"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_shards(
  index = "logs-demo",
  params = { "routing": "user1" },
  body =   {
    "query": {
      "term": {
        "user": "user1"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


### 範例回應

回應會顯示如果執行搜尋，將被搜尋的節點與分片：

```json
{
  "nodes": {
    "12ljrWLsQyiWHLzhFZgL9Q": {
      "name": "opensearch-node3",
      "ephemeral_id": "-JPvYKPMSGubd0VmSEzlbw",
      "transport_address": "172.18.0.4:9300",
      "attributes": {
        "shard_indexing_pressure_enabled": "true"
      }
    }
  },
  "indices": {
    "logs-demo": {}
  },
  "shards": [
    [
      {
        "state": "STARTED",
        "primary": true,
        "node": "12ljrWLsQyiWHLzhFZgL9Q",
        "relocating_node": null,
        "shard": 1,
        "index": "logs-demo",
        "allocation_id": {
          "id": "HwEjTdYQQJuULdQn10FRBw"
        }
      }
    ]
  ]
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| `nodes` | 物件 | 包含節點 ID 對應至節點中繼資料（例如名稱與傳輸位址）的對應表。 |
| `indices` | 物件 | 包含請求中所含索引名稱的對應表。 |
| `shards` | 陣列的陣列 | 代表此請求之分片副本（主要分片／副本分片）的巢狀陣列。 |
| `shards.index` | 字串 | 索引名稱。 |
| `shards.shard` | 整數 | 分片編號。 |
| `shards.node` | 字串 | 包含此分片之節點的節點 ID。 |
| `shards.primary` | 布林值 | 是否為主要分片。 |
| `shards.state` | 字串 | 目前的分片狀態。 |
| `shards.allocation_id.id` | 字串 | 此分片分配的唯一 ID。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/shards/search_shards`。
