---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引分片儲存"
parent: Index operations
grand_parent: Index APIs
nav_order: 95
redirect_from:
  - /api-reference/cluster-api/shard-stores/
---

# 索引分片儲存 API
**於 1.0 版導入**
{: .label .label-purple }

`_shard_stores` API 提供一或多個索引之分片副本的資訊。此 API 會指出分片為何未指派，並提供其目前狀態，協助診斷未配置分片的問題。

## 端點
```json
GET /_shard_stores
GET /{index}/_shard_stores
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 清單或字串 | 用於限制請求範圍的資料串流、索引與別名清單。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值僅指向遺失或已關閉的索引時，請求會傳回錯誤。即使請求同時指向其他開啟的索引，此行為仍然適用。 | `false` |
| `expand_wildcards` | 清單或字串 | 萬用字元模式可比對的索引類型。若請求可指向資料串流，此引數會決定萬用字元運算式是否比對隱藏的資料串流。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏的索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須與 open、closed 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且非隱藏的索引。 | `open`  |
| `ignore_unavailable` | 布林值 | 若為 `true`，遺失或已關閉的索引不會包含在回應中。 | `false` |
| `status` | 清單或字串 | 用於限制請求範圍的分片健康狀態清單。<br> 有效值為：<br> - `all`：傳回所有分片，不論健康狀態為何。<br> - `green`：主要分片與所有副本分片皆已指派。<br> - `red`：主要分片未指派。<br> - `yellow`：一或多個副本分片未指派。 | `yellow,red` |

## 範例請求

在單一節點叢集上建立具有多個主要分片的索引：

```json
PUT /logs-shardstore
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "message": { "type": "text" }
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引：

<!-- spec_insert_start
component: example_code
rest: POST /logs-shardstore/_doc
body: |
{
  "timestamp": "2025-06-20T12:00:00Z",
  "message": "Log message 1"
}
-->
{% capture step1_rest %}
POST /logs-shardstore/_doc
{
  "timestamp": "2025-06-20T12:00:00Z",
  "message": "Log message 1"
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "logs-shardstore",
  body =   {
    "timestamp": "2025-06-20T12:00:00Z",
    "message": "Log message 1"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

取得 `logs-shardstore` 索引的分片儲存狀態：

<!-- spec_insert_start
component: example_code
rest: GET /logs-shardstore/_shard_stores?status=all
-->
{% capture step1_rest %}
GET /logs-shardstore/_shard_stores?status=all
{% endcapture %}

{% capture step1_python %}


response = client.indices.shard_stores(
  index = "logs-shardstore",
  params = { "status": "all" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

回應會列出指派給每個分片的儲存。若分片沒有已指派的儲存，則會標記為 `unassigned`：

```json
{
  "indices": {
    "logs-shardstore": {
      "shards": {
        "0": {
          "stores": [
            {
              "UFyVYVMCSDOObiRwPxSW5w": {
                "name": "opensearch-node1",
                "ephemeral_id": "vkSB_-M7QVyFXvgda6oRZg",
                "transport_address": "172.19.0.2:9300",
                "attributes": {
                  "shard_indexing_pressure_enabled": "true"
                }
              },
              "allocation_id": "PEM5YjEWSz-jJEj-Not6Aw",
              "allocation": "primary"
            }
          ]
        },
        "1": {
          "stores": []
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明|
| `indices` | 物件 | 包含每個索引的分片儲存資訊。 |
| `indices.<index>.shards` | 物件 | 包含索引中每個分片的儲存資料。 |
| `shards.<shard_id>.stores` | 陣列 | 該分片的儲存項目清單。|
| `stores[n].<node_id>` | 物件 | 節點中繼資料，包括名稱、傳輸位址與屬性。 |
| `stores[n].allocation` | 字串 | 此分片在該節點上的角色（`primary` 或 `replica`）。 |
| `stores[n].allocation_id` | 字串 | 此分片副本的唯一配置 ID。|
| `stores[n].store_exception` | 物件（選用） | 儲存讀取分片儲存時遇到的例外狀況。 |
| `stores[n].store_exception.type` | 字串 | 例外狀況的類型。|
| `stores[n].store_exception.reason` | 字串 | 例外狀況的原因訊息。|

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/shard_stores`。
