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
| `wait_for_completion` | 布林值 | 等待符合條件的任務完成。設為 `true` 時，請求會被封鎖，直到任務完成為止。 | `false` |

<!-- spec_insert_end -->

此 API 會傳回目前正在執行之任務的相關資訊。任務完成後，只有在任務結果已儲存於 `.tasks` 索引中時，API 才會傳回其資訊。OpenSearch 僅會為使用 `wait_for_completion=false` 啟動的操作儲存任務結果。對於已完成但未儲存結果的任務，API 會傳回錯誤。

## 請求範例

若要取得任務 ID，請使用 `wait_for_completion=false` 啟動長時間執行的操作，例如重新索引或依查詢更新。下列請求會啟動經過節流的重新索引操作：

```json
POST /_reindex?wait_for_completion=false&requests_per_second=50
{
  "source": {
    "index": "my-source-index"
  },
  "dest": {
    "index": "my-dest-index"
  }
}
```
{% include copy-curl.html %}

回應包含任務 ID：

```json
{
  "task": "6It0uQ1AR06IDC4nMstPQw:1822891"
}
```

或者，您也可以使用 [List Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/list-tasks/) 找出執行中任務的 ID，例如 `GET /_tasks?actions=*reindex`。

下列請求會傳回該任務的相關資訊：

```json
GET /_tasks/<task_id>
```
{% include copy-curl.html %}

## 回應範例

在任務執行期間，回應會包含 `"completed": false` 以及目前的任務狀態：

```json
{
  "completed": false,
  "task": {
    "node": "6It0uQ1AR06IDC4nMstPQw",
    "id": 1822891,
    "type": "transport",
    "action": "indices:data/write/reindex",
    "status": {
      "total": 2000,
      "updated": 0,
      "created": 1000,
      "deleted": 0,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": 50.0,
      "throttled_until_millis": 16963
    },
    "description": "reindex from [my-source-index] to [my-dest-index]",
    "start_time_in_millis": 1792185761839,
    "running_time_in_nanos": 3241833543,
    "cancellable": true,
    "cancelled": false,
    "headers": {},
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
```

任務完成後，回應會包含 `"completed": true`，並在 `response` 物件中包含已儲存的操作結果：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "completed": true,
  "task": {
    "node": "6It0uQ1AR06IDC4nMstPQw",
    "id": 1822891,
    "type": "transport",
    "action": "indices:data/write/reindex",
    "status": {
      "total": 2000,
      "updated": 0,
      "created": 2000,
      "deleted": 0,
      "batches": 2,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 39999,
      "requests_per_second": 50.0,
      "throttled_until_millis": 0
    },
    "description": "reindex from [my-source-index] to [my-dest-index]",
    "start_time_in_millis": 1792185761839,
    "running_time_in_nanos": 40289441643,
    "cancellable": true,
    "cancelled": false,
    "headers": {}
  },
  "response": {
    "took": 40286,
    "timed_out": false,
    "total": 2000,
    "updated": 0,
    "created": 2000,
    "deleted": 0,
    "batches": 2,
    "version_conflicts": 0,
    "noops": 0,
    "retries": {
      "bulk": 0,
      "search": 0
    },
    "throttled": "39.9s",
    "throttled_millis": 39999,
    "requests_per_second": 50.0,
    "throttled_until": "0s",
    "throttled_until_millis": 0,
    "failures": []
  }
}
```
</details>

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `completed` | 布林值 | 任務是否已完成。 |
| `task` | 物件 | 任務的相關資訊。請參閱 [`task` 物件](#the-task-object)。 |
| `response` | 物件 | 操作的結果。僅在任務已完成或已取消，且其結果已儲存時傳回。物件內容取決於操作。例如，重新編製索引任務會傳回與 [Reindex API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) 回應相同的欄位。對於已取消的任務，此物件還會包含 `canceled` 欄位，用於指定取消的原因。 |
| `error` | 物件 | 導致任務失敗的錯誤。僅在任務失敗且其結果已儲存時傳回。 |

### `task` 物件

`task` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `node` | 字串 | 執行該任務的節點 ID。 |
| `id` | 整數 | 該任務在節點上的 ID。完整的任務 ID 格式為 `<node>:<id>`。 |
| `type` | 字串 | 任務類型，例如 `transport`。 |
| `action` | 字串 | 任務執行的動作，例如 `indices:data/write/reindex`。 |
| `status` | 物件 | 任務目前的狀態。物件內容取決於動作。例如，重新編製索引任務會回報已處理的文件數量與節流資訊。並非所有動作都會傳回此欄位。 |
| `description` | 字串 | 任務的說明，例如重新編製索引作業的來源索引與目的地索引。 |
| `start_time_in_millis` | 長整數 | 任務開始的時間，以自 Epoch 起算的毫秒數表示。 |
| `running_time_in_nanos` | 長整數 | 任務已執行的時間長度，以奈秒表示。 |
| `cancellable` | 布林值 | 是否可以取消該任務。 |
| `cancelled` | 布林值 | 該任務是否已被取消。 |
| `cancellation_time_millis` | 長整數 | 任務被取消的時間，以自 Epoch 起算的毫秒數表示。僅針對已取消的任務傳回。 |
| `parent_task_id` | 字串 | 父任務的 ID。僅針對子任務傳回，例如分割重新編製索引作業的各個切片。 |
| `headers` | 物件 | 啟動該任務之請求中受追蹤的請求標頭，例如 `X-Opaque-Id`。不包含其他請求標頭。 |
| `resource_stats` | 物件 | 任務的資源使用統計資料。僅針對支援資源追蹤且正在執行的任務傳回。請參閱 [`resource_stats` 物件](#the-resource_stats-object)。 |

### `resource_stats` 物件

只有支援資源追蹤的任務才會更新 `resource_stats` 物件。這些統計資料是根據已排程的執行緒執行計算而得，包括已完成處理該任務的執行緒，以及目前正在處理該任務的執行緒。由於同一個執行緒可能會多次排程處理同一個任務，因此特定執行緒每次排程處理特定任務的個別實例，都視為一次執行緒執行。

`resource_stats` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `average` | 物件 | 所有已排程執行緒執行的平均資源使用量。 |
| `total` | 物件 | 所有已排程執行緒執行的資源使用總量。 |
| `min` | 物件 | 所有已排程執行緒執行的最小資源使用量。 |
| `max` | 物件 | 所有已排程執行緒執行的最大資源使用量。 |
| `thread_info` | 物件 | 與執行緒數量相關的統計資料。 |

`average`、`total`、`min` 和 `max` 物件各自包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cpu_time_in_nanos` | 長整數 | 使用的 CPU 時間，以奈秒為單位。 |
| `memory_in_bytes` | 長整數 | 使用的記憶體量，以位元組為單位。 |

`thread_info` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `thread_executions` | 整數 | 已排程處理該任務的執行緒數量。 |
| `active_threads` | 整數 | 目前正在處理該任務的執行緒數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/tasks/get`。
