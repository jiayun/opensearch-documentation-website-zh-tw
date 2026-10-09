---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得任務"
parent: Tasks APIs
nav_order: 20
---

# Get Task API
**於 1.0 版推出**
{: .label .label-purple }

Get Task API 會回傳單一一般 OpenSearch 任務（例如搜尋、重新編製索引或大量操作）的詳細資訊。

此 API 與 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 不同，後者追蹤機器學習任務，並具有不同的回應格式。
{: .important }

<!-- spec_insert_start
api: tasks.get
component: endpoints
-->
## 端點
```json
GET /_tasks/{task_id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.get
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `task_id` | **必要** | 字串 | 任務 ID。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.get
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `timeout` | 字串 | 等待回應的時間長度。 | `30s` |
| `wait_for_completion` | 布林值 | 等待符合條件的任務完成。當設為 `true` 時，請求會被阻擋，直到任務完成為止。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列請求會回傳進行中搜尋任務的詳細資訊：

```bash
curl -XGET "localhost:9200/_tasks?actions=*search&detailed
```
{% include copy.html %}

## 範例回應

下列回應會回傳 `transport` 任務的詳細資訊：

```json
{
  "nodes": {
    "JzrCxdtFTCO_RaINw8ckNA": {
      "name": "node-1",
      "transport_address": "127.0.0.1:9300",
      "host": "127.0.0.1",
      "ip": "127.0.0.1:9300",
      "roles": [
        "data",
        "ingest",
        "cluster_manager",
        "remote_cluster_client"
      ],
      "tasks": {
        "JzrCxdtFTCO_RaINw8ckNA:54321": {
          "node": "JzrCxdtFTCO_RaINw8ckNA",
          "id": 54321,
          "type": "transport",
          "action": "indices:data/read/search",
          "status": {
            "total": 1000,
            "created": 0,
            "updated": 0,
            "deleted": 0,
            "batches": 1,
            "version_conflicts": 0,
            "noops": 0,
            "retries": {
              "bulk": 0,
              "search": 0
            },
            "throttled_millis": 0,
            "requests_per_second": -1.0,
            "throttled_until_millis": 0
          },
          "description": "indices[test_index], types[_doc], search_type[QUERY_THEN_FETCH], source[{\"query\":{\"match_all\":{}}}]",
          "start_time_in_millis": 1625145678901,
          "running_time_in_nanos": 2345678,
          "cancellable": true
        }
      }
    }
  }
}
```

### `resource_stats` 物件

`resource_stats` 物件僅會針對支援資源追蹤的任務進行更新。這些統計數據是根據已排程的執行緒執行計算而得，包括已完成該任務工作的執行緒，以及目前正在處理該任務的執行緒。由於同一個執行緒可能被排程多次處理同一個任務，因此每個執行緒被排程處理某個任務的執行個體，都視為單次執行緒執行。

下表列出 `resource_stats` 物件中的所有回應欄位。

回應欄位 | 說明 |
:--- | :--- |
`average` | 所有已排程執行緒執行的平均資源使用量。 |
`total` | 所有已排程執行緒執行的總資源使用量。 |
`min` | 所有已排程執行緒執行的最小資源使用量。 |
`max` | 所有已排程執行緒執行的最大資源使用量。 |
`thread_info` | 與執行緒數量相關的統計數據。|
`thread_info.active_threads` | 目前正在處理該任務的執行緒數量。 |
`thread_info.thread_executions` | 執行緒被排程處理該任務的執行次數。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/tasks/get`。
