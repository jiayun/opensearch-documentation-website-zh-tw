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

下列請求會傳回重新編製索引任務的相關資訊：

```json
GET /_tasks/6It0uQ1AR06IDC4nMstPQw:908779
```
{% include copy-curl.html %}

## 範例回應

此範例中的任務已完成，因此回應在 `response` 物件中包含重新編製索引操作的結果：

```json
{
  "completed": true,
  "task": {
    "node": "6It0uQ1AR06IDC4nMstPQw",
    "id": 908779,
    "type": "transport",
    "action": "indices:data/write/reindex",
    "status": {
      "total": 3,
      "updated": 0,
      "created": 3,
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
    "description": "reindex from [products] to [products-copy]",
    "start_time_in_millis": 1793043339924,
    "running_time_in_nanos": 704592000,
    "cancellable": true,
    "cancelled": false,
    "headers": {}
  },
  "response": {
    "took": 434,
    "timed_out": false,
    "total": 3,
    "updated": 0,
    "created": 3,
    "deleted": 0,
    "batches": 1,
    "version_conflicts": 0,
    "noops": 0,
    "retries": {
      "bulk": 0,
      "search": 0
    },
    "throttled": "0s",
    "throttled_millis": 0,
    "requests_per_second": -1.0,
    "throttled_until": "0s",
    "throttled_until_millis": 0,
    "failures": []
  }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`completed` | 布林值 | 任務是否已完成。
`task` | 物件 | 任務的相關資訊。請參閱 [`task` 物件](#the-task-object)。
`response` | 物件 | 任務所執行操作的結果。僅在任務完成後才會出現。欄位取決於操作。例如，重新編製索引任務傳回的欄位與 [Reindex API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) 相同。

### `task` 物件

下表列出 `task` 物件中的所有回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`node` | 字串 | 執行該任務的節點 ID。
`id` | 整數 | 該任務在節點上的任務 ID。請求中使用的完整任務 ID 格式為 `<node>:<id>`。
`type` | 字串 | 任務類型，例如 `transport`。
`action` | 字串 | 該任務執行的動作，例如 `indices:data/write/reindex`。
`status` | 物件 | 任務的目前狀態。其中的欄位取決於任務類型。例如，重新編製索引任務會回報目前為止已處理的文件數量。
`description` | 字串 | 任務的說明。
`start_time_in_millis` | 長整數 | 任務的開始時間，以自 Epoch 起算的毫秒數表示。
`running_time_in_nanos` | 長整數 | 任務已執行的時間長度，以奈秒為單位。
`cancellable` | 布林值 | 任務是否可以取消。
`cancelled` | 布林值 | 任務是否已被取消。
`headers` | 物件 | 啟動該任務之請求中受追蹤的請求標頭，例如 `X-Opaque-Id`。不包含其他請求標頭。
`resource_stats` | 物件 | 資源使用統計資料。僅在支援資源追蹤的執行中任務才會出現。請參閱 [`resource_stats` 物件](#the-resource_stats-object)。

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
`thread_info.thread_executions` | 已被排程處理該任務的執行緒數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/tasks/get`。
