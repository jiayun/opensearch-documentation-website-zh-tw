---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新節流任務"
parent: Tasks APIs
nav_order: 50
---

# 重新節流任務 API
**於 1.0 版推出**
{: .label .label-purple }

您可以使用下列 API，動態變更已在執行的 [`_reindex`]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)、[`_update_by_query`]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) 或 [`_delete_by_query`]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-by-query/) 作業的 `requests_per_second`。

## 端點

```json
POST /_delete_by_query/{task_id}/_rethrottle
POST /_reindex/{task_id}/_rethrottle
POST /_update_by_query/{task_id}/_rethrottle
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`task_id` | 字串 | 您要重新節流的執行中任務的唯一識別碼。

## 查詢參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`requests_per_second` | 浮點數 | 要套用至任務的新節流值。使用 `-1` 可停用節流。選用。

### 請求範例：重新節流執行中的依查詢刪除任務

<!-- spec_insert_start
component: example_code
rest: POST /_delete_by_query/<YOUR_TASK_ID>/_rethrottle?requests_per_second=10
-->
{% capture step1_rest %}
POST /_delete_by_query/<YOUR_TASK_ID>/_rethrottle?requests_per_second=10
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query_rethrottle(
  task_id = "<YOUR_TASK_ID>",
  params = { "requests_per_second": "10" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


### 請求範例：重新節流執行中的重新編製索引任務

<!-- spec_insert_start
component: example_code
rest: POST /_reindex/<YOUR_TASK_ID>/_rethrottle?requests_per_second=20
-->
{% capture step1_rest %}
POST /_reindex/<YOUR_TASK_ID>/_rethrottle?requests_per_second=20
{% endcapture %}

{% capture step1_python %}


response = client.reindex_rethrottle(
  task_id = "<YOUR_TASK_ID>",
  params = { "requests_per_second": "20" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 請求範例：重新節流執行中的依查詢更新任務

<!-- spec_insert_start
component: example_code
rest: POST /_update_by_query/<YOUR_TASK_ID>/_rethrottle?requests_per_second=5
-->
{% capture step1_rest %}
POST /_update_by_query/<YOUR_TASK_ID>/_rethrottle?requests_per_second=5
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query_rethrottle(
  task_id = "<YOUR_TASK_ID>",
  params = { "requests_per_second": "5" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

下列回應提供執行中的 `update_by_query` 任務的詳細資訊：

```
{
  "nodes": {
    "bvv8SKpiRhOhF9_Bu8gZ7w": {
      "name": "opensearch-node1",
      "transport_address": "172.18.0.4:9300",
      "host": "172.18.0.4",
      "ip": "172.18.0.4:9300",
      "roles": [
        "cluster_manager",
        "data",
        "ingest",
        "remote_cluster_client"
      ],
      "attributes": {
        "shard_indexing_pressure_enabled": "true"
      },
      "tasks": {
        "bvv8SKpiRhOhF9_Bu8gZ7w:640": {
          "node": "bvv8SKpiRhOhF9_Bu8gZ7w",
          "id": 640,
          "type": "transport",
          "action": "indices:data/write/update/byquery",
          "status": {
            "total": 4785,
            "updated": 1000,
            "created": 0,
            "deleted": 0,
            "batches": 1,
            "version_conflicts": 0,
            "noops": 0,
            "retries": {
              "bulk": 0,
              "search": 0
            },
            "throttled_millis": 0,
            "requests_per_second": 50,
            "throttled_until_millis": 2146
          },
          "description": "update-by-query [test-rethrottle] updated with Script{type=inline, lang='painless', idOrCode='ctx._source.new_field = 'updated'', options={}, params={}}",
          "start_time_in_millis": 1751310547697,
          "running_time_in_nanos": 9567425129,
          "cancellable": true,
          "cancelled": false,
          "headers": {
            "X-Opaque-Id": "1b911516-44cd-4920-8c1e-79368ea7cdfd"
          },
          "resource_stats": {
            "average": {
              "cpu_time_in_nanos": 0,
              "memory_in_bytes": 0
            },
            "total": {
              "cpu_time_in_nanos": 0,
              "memory_in_bytes": 0
            },
            "min": {
              "cpu_time_in_nanos": 0,
              "memory_in_bytes": 0
            },
            "max": {
              "cpu_time_in_nanos": 0,
              "memory_in_bytes": 0
            },
            "thread_info": {
              "thread_executions": 0,
              "active_threads": 0
            }
          }
        }
      }
    }
  }
}
```

## 回應本文欄位

回應提供重新節流作業在任務層級與節點層級的詳細資訊。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `nodes` | 物件 | 節點 ID 與各節點上任務詳細資訊的對應表。 |
| `nodes.<node_id>.name` | 字串 | 執行任務的節點名稱。 |
| `nodes.<node_id>.transport_address` | 字串 | 節點的傳輸位址。 |
| `nodes.<node_id>.host` | 字串 | 主機的 IP 位址。 |
| `nodes.<node_id>.ip` | 字串 | IP 位址與連接埠。 |
| `nodes.<node_id>.roles` | 陣列 | 指派給節點的角色。 |
| `nodes.<node_id>.attributes` | 物件 | 節點層級的屬性。 |
| `nodes.<node_id>.tasks` | 物件 | 任務 ID 與各任務詳細資訊的對應表。 |
| `nodes.<node_id>.tasks.<task_id>.type` | 字串 | 任務類型，例如 `transport`。 |
| `nodes.<node_id>.tasks.<task_id>.action` | 字串 | 正在執行的特定動作（例如 `reindex`）。 |
| `nodes.<node_id>.tasks.<task_id>.status` | 物件 | 任務目前的狀態。 |
| `nodes.<node_id>.tasks.<task_id>.status.total` | 整數 | 要處理的文件總數。 |
| `nodes.<node_id>.tasks.<task_id>.status.created` | 整數 | 已建立的文件數量。 |
| `nodes.<node_id>.tasks.<task_id>.status.updated` | 整數 | 已更新的文件數量。 |
| `nodes.<node_id>.tasks.<task_id>.status.deleted` | 整數 | 已刪除的文件數量。 |
| `nodes.<node_id>.tasks.<task_id>.status.batches` | 整數 | 已處理的批次數量。 |
| `nodes.<node_id>.tasks.<task_id>.status.version_conflicts` | 整數 | 版本衝突的次數。 |
| `nodes.<node_id>.tasks.<task_id>.status.noops` | 整數 | 無變更更新的次數。 |
| `nodes.<node_id>.tasks.<task_id>.status.retries` | 物件 | 大量作業與搜尋作業的重試統計資料。 |
| `nodes.<node_id>.tasks.<task_id>.status.requests_per_second` | 浮點數 | 目前的節流速率，以每秒請求數表示。 |
| `nodes.<node_id>.tasks.<task_id>.status.throttled_millis` | 整數 | 任務受到節流的時間，以毫秒為單位。 |
| `nodes.<node_id>.tasks.<task_id>.status.throttled_until_millis` | 整數 | 預期任務仍會受到節流的時間，以毫秒為單位。 |
| `nodes.<node_id>.tasks.<task_id>.description` | 字串 | 便於人員閱讀的任務說明。 |
| `nodes.<node_id>.tasks.<task_id>.start_time_in_millis` | 整數 | 任務開始時間，以自 Unix 紀元起算的毫秒數表示。 |
| `nodes.<node_id>.tasks.<task_id>.running_time_in_nanos` | 整數 | 任務執行時間，以奈秒為單位。 |
| `nodes.<node_id>.tasks.<task_id>.cancellable` | 布林值 | 是否可以取消任務。 |
| `nodes.<node_id>.tasks.<task_id>.cancelled` | 布林值 | 任務是否已取消。 |
| `nodes.<node_id>.tasks.<task_id>.headers` | 物件 | 與任務相關聯的選用 HTTP 標頭。 |
| `nodes.<node_id>.tasks.<task_id>.resource_stats` | 物件 | 資源使用量的統計資料。 |
