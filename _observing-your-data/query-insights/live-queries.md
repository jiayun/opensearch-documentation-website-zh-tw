---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "即時查詢"
parent: Query insights
nav_order: 20
---

# 即時查詢
**3.0 版新增**
{: .label .label-purple }

使用 Live Queries API 來擷取整個叢集或特定節點上目前正在執行的搜尋查詢。透過 Query Insights 監視即時查詢，可讓您即時掌握 OpenSearch 叢集內目前正在執行的搜尋查詢。這對於識別和除錯執行時間異常過長，或當下消耗大量資源的查詢非常有用。

此 API 會傳回目前正在執行的搜尋查詢清單，依指定的指標（預設為 `latency`）以遞減順序排序。回應包含每個即時查詢的詳細資訊，例如查詢狀態、開始時間、跨協調器任務與分片任務彙總的總資源使用量，以及個別任務層級的明細。

## 端點

```json
GET /_insights/live_queries
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `verbose` | 布林值 | 是否在輸出中包含詳細的查詢資訊。預設為 `true`。 |
| `nodeId` | 字串 | 用於篩選結果的節點 ID 逗號分隔清單。若省略，則傳回所有節點的查詢。 |
| `sort` | 字串 | 用於排序結果的指標。有效值為 `latency`、`cpu` 或 `memory`。預設為 `latency`。 |
| `size` | 整數 | 要傳回的查詢記錄數量。必須為正整數。預設為 `100`。 |
| `wlmGroupId` | 字串 | 篩選結果，僅傳回屬於指定工作負載管理群組的查詢。若省略，則傳回所有群組的查詢。 |
| `use_finished_cache` | 布林值 | 設為 `true` 時，回應會包含 `finished_queries` 陣列，其中含有來自已完成查詢快取的最近完成查詢。預設為 `false`。 |

## 已完成查詢快取

指定 `use_finished_cache=true` 時，API 除了傳回目前正在執行的查詢外，也會一併傳回最近完成的查詢。這有助於將即時查詢與剛完成的查詢建立關聯，提供更全面的近期查詢活動檢視。

### 快取生命週期

已完成查詢快取在節點啟動時保持非作用中狀態，在您啟用它之前不會消耗任何資源。其生命週期運作方式如下：

1. 快取會在第一個包含 `use_finished_cache=true` 的 API 呼叫時啟用。快取一旦進入作用中狀態，節點便會開始將已完成的查詢擷取到快取中。
2. 在作用中狀態下，快取最多儲存 1,000 筆最近完成的查詢。個別記錄會保留 5 分鐘，之後自動清除。每次 API 呼叫最多傳回 50 筆最近的記錄。
3. 若在閒置逾時期間（預設為 5 分鐘）內沒有進行包含 `use_finished_cache=true` 的 API 呼叫，快取會自動停用並清除其資料。
4. 閒置停用後，快取會在下一個包含 `use_finished_cache=true` 的 API 呼叫時自動重新啟用，並再次開始擷取查詢。

由於快取僅在需要時啟用，在第一次 `use_finished_cache=true` 呼叫之前完成的查詢不會被擷取。為確保完整涵蓋，請在執行您要監視的查詢之前，先進行一次包含 `use_finished_cache=true` 的 API 呼叫。
{: .note}

### 快取設定

您可以使用下列動態叢集設定來設定閒置逾時：

```json
PUT _cluster/settings
{
  "persistent": {
    "search.insights.live_queries.cache.idle_timeout": "5m"
  }
}
```
{% include copy-curl.html %}

`search.insights.live_queries.cache.idle_timeout` 設定接受時間值。設為 `0` 可完全停用快取並立即將其停止。非零值必須介於 `2m` 與 `10m` 之間。預設為 `5m`。從 `0` 變更為非零值會重新啟用快取，無需重新啟動節點。

如需更多資訊，請參閱 [動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/#dynamic-settings)。

## 範例請求

下列範例請求會擷取依 CPU 使用量排序的前 10 筆查詢，並停用詳細輸出：

```json
GET /_insights/live_queries?verbose=false&sort=cpu&size=10
```
{% include copy-curl.html %}

下列範例請求會擷取即時查詢以及最近完成的查詢：

```json
GET /_insights/live_queries?use_finished_cache=true
```
{% include copy-curl.html %}

下列範例請求會依工作負載管理群組篩選即時查詢：

```json
GET /_insights/live_queries?wlmGroupId=DEFAULT_WORKLOAD_GROUP
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "live_queries": [
    {
      "id": "troGHNGUShqDj3wK_K5ZIw:512",
      "status": "running",
      "start_time": 1745359226777,
      "total_latency_millis": 13959,
      "total_cpu_nanos": 405000,
      "total_memory_bytes": 3104,
      "coordinator_task": {
        "task_id": "troGHNGUShqDj3wK_K5ZIw:512",
        "node_id": "troGHNGUShqDj3wK_K5ZIw",
        "action": "indices:data/read/search",
        "status": "running",
        "description": "indices[my-index-*], search_type[QUERY_THEN_FETCH], source[{\"size\":20,\"query\":{\"term\":{\"user.id\":{\"value\":\"userId\",\"boost\":1.0}}}}]",
        "start_time": 1745359226777,
        "running_time_nanos": 13959364458,
        "cpu_nanos": 305000,
        "memory_bytes": 2048
      },
      "shard_tasks": [
        {
          "task_id": "Y6eBnbdISPO6XaVfxCBRgg:101",
          "node_id": "Y6eBnbdISPO6XaVfxCBRgg",
          "action": "indices:data/read/search[phase/query]",
          "status": "running",
          "description": "id[0], type[query], indices[my-index-*]",
          "start_time": 1745359226800,
          "running_time_nanos": 13900000000,
          "cpu_nanos": 100000,
          "memory_bytes": 1056
        }
      ]
    }
  ]
}
```

上述回應顯示單一即時查詢：

- 頂層欄位（`id`、`status`、`start_time`、`total_latency_millis`、`total_cpu_nanos`、`total_memory_bytes`）提供整個搜尋請求的摘要。`total_*` 指標是跨協調器任務與所有分片任務彙總而成，讓您以單一檢視掌握查詢的整體資源消耗。
- `coordinator_task` 物件描述接收搜尋請求並跨分片協調查詢的協調節點上的任務。在此範例中，協調節點（`troGHNGUShqDj3wK_K5ZIw`）已執行約 13.9 秒，並消耗了 305,000 奈秒的 CPU 時間與 2,048 位元組的記憶體。`description` 欄位包含目標索引、搜尋類型與完整查詢來源。
- `shard_tasks` 陣列列出由協調節點產生的個別分片層級任務。每個分片任務在特定的資料節點上執行，並執行搜尋的某個階段（例如 `search[phase/query]`）。在此範例中，有一個分片任務正在節點 `Y6eBnbdISPO6XaVfxCBRgg` 上執行，消耗了 100,000 奈秒的 CPU 與 1,056 位元組的記憶體。跨越多個分片或多個資料節點的查詢在此陣列中會有多筆項目。

指定 `use_finished_cache=true` 時，回應也會包含 `finished_queries` 陣列：

```json
{
  "live_queries": [],
  "finished_queries": [
    {
      "timestamp": 1745359230000,
      "id": "troGHNGUShqDj3wK_K5ZIw:512",
      "top_n_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "completed",
      "node_id": "troGHNGUShqDj3wK_K5ZIw",
      "source": {
        "size": 20,
        "query": {
          "term": {
            "user.id": {
              "value": "userId",
              "boost": 1.0
            }
          }
        }
      },
      "indices": ["my-index-*"],
      "search_type": "query_then_fetch",
      "measurements": {
        "latency": {
          "number": 13959364458,
          "count": 1,
          "aggregationType": "NONE"
        },
        "cpu": {
          "number": 405000,
          "count": 1,
          "aggregationType": "NONE"
        },
        "memory": {
          "number": 3104,
          "count": 1,
          "aggregationType": "NONE"
        }
      }
    }
  ]
}
```

已完成查詢記錄中的 `id` 欄位使用與即時查詢 `id` 相同的 `nodeId:taskId` 格式（例如 `troGHNGUShqDj3wK_K5ZIw:512`）。這讓您可以將已完成的查詢與其來源的即時查詢建立關聯。`top_n_id` 是另一個 UUID，用於將已完成的查詢連結到 [前 N 名查詢]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/) 儲存區中對應的記錄。若該查詢不符合前 N 名查詢的資格，`top_n_id` 會是 `null`。

## 回應欄位

下表列出 `live_queries` 陣列中每個物件的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `id` | 字串 | 搜尋請求的唯一識別碼（`nodeId:taskId` 格式的協調節點任務 ID）。 |
| `status` | 字串 | 查詢的目前狀態。有效值為 `running` 或 `cancelled`。 |
| `start_time` | 長整數 | 查詢開始的時間，以自 epoch 起算的毫秒數表示。 |
| `wlm_group_id` | 字串 | 與該查詢相關聯的工作負載管理群組 ID。僅在查詢屬於某個工作負載群組時才會出現。 |
| `total_latency_millis` | 長整數 | 查詢的總經過時間（毫秒），彙總協調與分片任務的結果。 |
| `total_cpu_nanos` | 長整數 | 查詢所耗用的總 CPU 時間（奈秒），彙總協調與分片任務的結果。 |
| `total_memory_bytes` | 長整數 | 查詢所使用的總堆積記憶體（位元組），彙總協調與分片任務的結果。 |
| `coordinator_task` | 物件 | 此查詢之協調任務的詳細資料。請參閱[任務欄位](#task-fields)。 |
| `shard_tasks` | 陣列 | 此查詢的分片層級任務詳細資料清單。每個元素的結構與[任務欄位](#task-fields)相同。 |

### 任務欄位

每個 `coordinator_task` 物件及 `shard_tasks` 陣列的每個成員都包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `task_id` | 字串 | `nodeId:taskId` 格式的任務識別碼。 |
| `node_id` | 字串 | 執行該任務之節點的 ID。 |
| `action` | 字串 | 該任務所執行的動作（例如，協調任務為 `indices:data/read/search`，分片任務為 `indices:data/read/search[phase/query]`）。 |
| `status` | 字串 | 任務的目前狀態。 |
| `description` | 字串 | 任務的說明，包含目標索引、搜尋類型及查詢來源。僅在 `verbose` 為 `true` 時才會包含。 |
| `start_time` | 長整數 | 任務開始的時間，以自 epoch 起算的毫秒數表示。 |
| `running_time_nanos` | 長整數 | 任務的經過時間（奈秒）。 |
| `cpu_nanos` | 長整數 | 任務所耗用的 CPU 時間（奈秒）。 |
| `memory_bytes` | 長整數 | 任務所使用的堆積記憶體量（位元組）。 |

### finished_queries 陣列欄位

指定 `use_finished_cache=true` 時，`finished_queries` 陣列會包含具有下列欄位的查詢物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `timestamp` | 長整數 | 查詢完成的時間，以自 epoch 起算的毫秒數表示。 |
| `id` | 字串 | 即時查詢識別碼（`nodeId:taskId` 格式），用於與即時查詢相互關聯。 |
| `top_n_id` | 字串 | 將此記錄連結至對應前 N 名查詢記錄的 UUID。若該查詢不符合前 N 名查詢的資格，可能為 `null`。 |
| `status` | 字串 | 查詢的完成狀態（例如 `completed`）。 |
| `node_id` | 字串 | 協調節點 ID。 |
| `source` | 物件 | 查詢來源本文。 |
| `indices` | 陣列 | 查詢所鎖定的索引清單。 |
| `search_type` | 字串 | 搜尋執行類型（例如 `query_then_fetch`）。 |
| `phase_latency_map` | 物件 | 依搜尋階段細分的延遲。 |
| `task_resource_usages` | 陣列 | 各項任務的資源使用詳細資料。 |
| `measurements` | 物件 | 包含查詢最終效能指標的物件。每個指標（`latency`、`cpu`、`memory`）都包含 `number`、`count` 及 `aggregationType` 欄位。 |
