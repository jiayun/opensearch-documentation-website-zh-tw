---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋背壓"
nav_order: 60
has_children: false
parent: Availability and recovery
redirect_from: 
  - /opensearch/search-backpressure/
---

# 搜尋背壓

搜尋背壓是一種機制，用於識別耗用大量資源的搜尋請求，並在節點承受壓力時取消這些請求。如果節點或分片上的搜尋請求已超出資源限制，且未能在特定臨界值內恢復，該請求就會遭到拒絕。這些臨界值是動態的，可透過 [叢集設定](#search-backpressure-settings) 並使用 `/_cluster/settings` API 端點來設定。

## 衡量資源耗用量

為了決定是否套用搜尋背壓，OpenSearch 會定期衡量每個搜尋請求的下列資源耗用量統計資料：

- CPU 使用量
- 堆積使用量
- 經過時間

觀察執行緒會定期衡量節點的資源使用量。如果 OpenSearch 判斷節點承受壓力，就會檢查每個搜尋工作和搜尋分片工作的資源使用量，並與可設定的臨界值進行比較。OpenSearch 會考量 CPU 使用量、堆積使用量和經過時間，為每個工作指派取消分數，再據以取消耗用最多資源的工作。

OpenSearch 會將取消次數限制為成功完成工作數的一小部分。此外，也會限制每單位時間的取消次數。OpenSearch 會持續監視並取消工作，直到節點不再承受壓力為止。

## 已取消的查詢

如果查詢遭到取消，且部分分片失敗，OpenSearch 可能會傳回部分結果。如果所有分片都失敗，OpenSearch 會從伺服器傳回類似下列的錯誤：

```json
{
  "error": {
    "root_cause": [
      {
          "type": "task_cancelled_exception",
          "reason": "cancelled task with reason: cpu usage exceeded [17.9ms >= 15ms], elapsed time exceeded [1.1s >= 300ms]"
      },
      {
          "type": "task_cancelled_exception",
          "reason": "cancelled task with reason: elapsed time exceeded [1.1s >= 300ms]"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "foobar",
        "node": "7yIqOeMfRyWW1rHs2S4byw",
        "reason": {
            "type": "task_cancelled_exception",
            "reason": "cancelled task with reason: cpu usage exceeded [17.9ms >= 15ms], elapsed time exceeded [1.1s >= 300ms]"
        }
      },
      {
        "shard": 1,
        "index": "foobar",
        "node": "7yIqOeMfRyWW1rHs2S4byw",
        "reason": {
            "type": "task_cancelled_exception",
            "reason": "cancelled task with reason: elapsed time exceeded [1.1s >= 300ms]"
        }
      }
    ]
  },
  "status": 500
}
```

## 搜尋背壓模式

搜尋背壓會以 `monitor_only` (預設)、`enforced` 或 `disabled` 模式執行。在 `enforced` 模式中，伺服器會拒絕搜尋請求。在 `monitor_only` 模式中，伺服器實際上不會取消搜尋請求，但會追蹤這些請求的統計資料。您可以在 [`search_backpressure.mode`](#search-backpressure-settings) 參數中指定模式。

## 搜尋背壓設定

搜尋背壓會在標準 OpenSearch 叢集設定中新增數個設定。這些設定是動態的，因此您不需要重新啟動叢集，就能變更此功能的預設行為。

若要設定這些設定，請將 PUT 請求傳送至 `/_cluster/settings`：

```json
PUT /_cluster/settings
{
  "persistent": {
    "search_backpressure": {
      "mode": "monitor_only"
    }
  }
}
```
{% include copy-curl.html %}

設定 | 預設 | 說明
:--- | :--- | :---
`search_backpressure.mode` | `monitor_only` | 搜尋背壓[模式](#search-backpressure-modes)。有效值為 `monitor_only`、`enforced` 或 `disabled`。
search_backpressure.cancellation_ratio<br> *已於 2.6 版棄用。由 search_backpressure.search_shard_task.cancellation_ratio 取代* | 10% | 要取消的工作數上限，以成功完成工作數的百分比表示。
search_backpressure.cancellation_rate<br> *已於 2.6 版棄用。由 search_backpressure.search_shard_task.cancellation_rate 取代* | 0.003 | 每毫秒經過時間要取消的工作數上限。
search_backpressure.cancellation_burst<br> *已於 2.6 版棄用。由 search_backpressure.search_shard_task.cancellation_burst 取代* | 10 | 觀察執行緒單次迭代中要取消的搜尋分片工作數上限。
`search_backpressure.node_duress.num_successive_breaches` | 3 | 節點被視為承受壓力前，連續超出限制的次數。
`search_backpressure.node_duress.cpu_threshold` | 90% | 節點被視為承受壓力所需的 CPU 使用量臨界值 (以百分比表示)。
`search_backpressure.node_duress.heap_threshold` | 70% | 節點被視為承受壓力所需的堆積使用量臨界值 (以百分比表示)。
`search_backpressure.search_task.elapsed_time_millis_threshold` | 45,000 | 個別父工作被納入取消考量前所需的經過時間臨界值 (以毫秒為單位)。
`search_backpressure.search_task.cancellation_ratio` | 0.1 | 要取消的搜尋工作數上限，以成功完成搜尋工作數的百分比表示。值範圍為 (0, 1]。
`search_backpressure.search_task.cancellation_rate`| 0.003 | 每毫秒經過時間要取消的搜尋工作數上限。值必須大於 0。
`search_backpressure.search_task.cancellation_burst` | 5 | 觀察執行緒單次迭代中要取消的搜尋工作數上限。值必須大於或等於 1。
`search_backpressure.search_task.heap_percent_threshold` | 2% | 個別父工作被納入取消考量前所需的堆積使用量臨界值 (以百分比表示)。值範圍為 [0%, 100%]。
`search_backpressure.search_task.total_heap_percent_threshold` | 5% | 套用取消前，所有搜尋工作堆積使用量總和所需的堆積使用量臨界值 (以百分比表示)。值範圍為 [0%, 100%]。
`search_backpressure.search_task.heap_variance` | 2.0 | 個別父工作被納入取消考量前所需的堆積使用量變異數。當 `taskHeapUsage` 大於或等於 `heapUsageMovingAverage` * `variance` 時，該工作會被納入取消考量。值必須大於或等於 0。
`search_backpressure.search_task.heap_moving_average_window_size` | 10 | 用於計算已完成父工作堆積使用量移動平均值的視窗大小。值必須大於或等於 0。
`search_backpressure.search_task.cpu_time_millis_threshold` | 30,000 | 個別父工作被納入取消考量前所需的 CPU 使用量臨界值 (以毫秒為單位)。值必須大於或等於 0。
`search_backpressure.search_shard_task.elapsed_time_millis_threshold` | 30,000 | 單一搜尋分片工作被納入取消考量前所需的經過時間臨界值 (以毫秒為單位)。值必須大於或等於 0。
`search_backpressure.search_shard_task.cancellation_ratio` | 0.1 | 要取消的搜尋分片工作數上限，以成功完成搜尋分片工作數的百分比表示。值範圍為 (0, 1]。
`search_backpressure.search_shard_task.cancellation_rate` | 0.003 | 每毫秒經過時間要取消的搜尋分片工作數上限。值必須大於 0。
`search_backpressure.search_shard_task.cancellation_burst` | 10 | 觀察執行緒單次迭代中要取消的搜尋分片工作數上限。值必須大於或等於 1。
`search_backpressure.search_shard_task.heap_percent_threshold` | 0.5% | 單一搜尋分片工作被納入取消考量前所需的堆積使用量臨界值 (以百分比表示)。值範圍為 [0%, 100%]。
`search_backpressure.search_shard_task.total_heap_percent_threshold` | 5% | 套用取消前，所有搜尋分片工作堆積使用量總和所需的堆積使用量臨界值 (以百分比表示)。值範圍為 [0%, 100%]。
`search_backpressure.search_shard_task.heap_variance` | 2.0 | 單一搜尋分片工作的堆積使用量與先前已完成工作移動平均值相比，被納入取消考量前所需的最小變異數。值必須大於或等於 0。
`search_backpressure.search_shard_task.heap_moving_average_window_size` | 100 | 計算堆積使用量移動平均值時，要納入考量的先前已完成搜尋分片工作數。值必須大於或等於 0。
`search_backpressure.search_shard_task.cpu_time_millis_threshold` | 15,000 | 單一搜尋分片工作被納入取消考量前所需的 CPU 使用量臨界值 (以毫秒為單位)。值必須大於或等於 0。

## Search Backpressure Stats API
於 2.4 版導入
{: .label .label-purple }

您可以使用 [nodes stats API 操作]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)來監控伺服器端的請求取消情況。

#### 範例請求

若要取得統計資料，請使用下列請求：

```json
GET _nodes/stats/search_backpressure
```

#### 範例回應

回應包含伺服器端的請求取消統計資料：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "runTask",
  "nodes": {
    "T7aqO6zaQX-lt8XBWBYLsA": {
      "timestamp": 1667409521070,
      "name": "runTask-0",
      "transport_address": "127.0.0.1:9300",
      "host": "127.0.0.1",
      "ip": "127.0.0.1:9300",
      "roles": [
         
      ],
      "attributes": {
        "testattr": "test",
        "shard_indexing_pressure_enabled": "true"
      },
      "search_backpressure": {
        "search_task": {
          "resource_tracker_stats": {
            "heap_usage_tracker": {
              "cancellation_count": 57,
              "current_max_bytes": 5739204,
              "current_avg_bytes": 962465,
              "rolling_avg_bytes": 4009239
            },
            "elapsed_time_tracker": {
              "cancellation_count": 97,
              "current_max_millis": 15902,
              "current_avg_millis": 9705
            },
            "cpu_usage_tracker": {
              "cancellation_count": 64,
              "current_max_millis": 8483,
              "current_avg_millis": 7843
            }
          },
          "cancellation_stats": {
            "cancellation_count": 102,
            "cancellation_limit_reached_count": 25
          }
        },
        "search_shard_task": {
          "resource_tracker_stats": {
            "heap_usage_tracker": {
              "cancellation_count": 34,
              "current_max_bytes": 1203272,
              "current_avg_bytes": 700267,
              "rolling_avg_bytes": 1156270
            },
            "cpu_usage_tracker": {
              "cancellation_count": 318,
              "current_max_millis": 731,
              "current_avg_millis": 303
            },
            "elapsed_time_tracker": {
              "cancellation_count": 310,
              "current_max_millis": 1305,
              "current_avg_millis": 649
            }
          },
          "cancellation_stats": {
            "cancellation_count": 318,
            "cancellation_limit_reached_count": 97
          }
        },
        "mode": "enforced"
      }
    }
  }
}
```

### 回應本文欄位

回應包含下列欄位。

欄位名稱 | 資料類型 | 說明
:--- | :--- | :---
`search_backpressure` | 物件 | 搜尋背壓的統計資料。
`search_backpressure.search_task` | 物件 | 搜尋任務的統計資料。包含各取消條件 (heap、CPU、經過時間) 的資源追蹤器統計資料，以及這些追蹤器所有取消活動的摘要。
search_backpressure.search_task.[resource_tracker_stats](#resource_tracker_stats) | 物件 | 各追蹤器的統計資料，顯示每種資源類型 (heap 使用量、CPU 使用量、經過時間) 的取消次數，以及目前的資源消耗指標。
search_backpressure.search_task.[cancellation_stats](#cancellation_stats) | 物件 | 彙總所有資源追蹤器的取消統計資料。`cancellation_count` 與 `cancellation_limit_reached_count` 的總和等於所有資源追蹤器取消次數的總計。
`search_backpressure.search_shard_task` | 物件 | 搜尋分片任務的統計資料。包含各取消條件 (heap、CPU、經過時間) 的資源追蹤器統計資料，以及這些追蹤器所有取消活動的摘要。
search_backpressure.search_shard_task.[resource_tracker_stats](#resource_tracker_stats) | 物件 | 各追蹤器的統計資料，顯示每種資源類型 (heap 使用量、CPU 使用量、經過時間) 的取消次數，以及目前的資源消耗指標。
search_backpressure.search_shard_task.[cancellation_stats](#cancellation_stats) | 物件 | 彙總所有資源追蹤器的取消統計資料。`cancellation_count` 與 `cancellation_limit_reached_count` 的總和等於所有資源追蹤器取消次數的總計。
`search_backpressure.mode` | 字串 | 搜尋背壓的[模式](#search-backpressure-modes)。

### `resource_tracker_stats`

`resource_tracker_stats` 物件包含每個資源追蹤器的統計資料：[`elapsed_time_tracker`](#elapsed_time_tracker)、[`heap_usage_tracker`](#heap_usage_tracker) 與 [`cpu_usage_tracker`](#cpu_usage_tracker)。

#### `elapsed_time_tracker`

`elapsed_time_tracker` 物件包含下列與經過時間相關的統計資料。

欄位名稱 | 資料類型 | 說明
:--- | :--- | :---
`cancellation_count` | 整數 | 自節點上次重新啟動以來，因經過時間過長而被標記為取消的任務數量。
`current_max_millis` | 整數 | 節點上目前執行的所有任務的最大經過時間，單位為毫秒。
`current_avg_millis` | 整數 | 節點上目前執行的所有任務的平均經過時間，單位為毫秒。

#### `heap_usage_tracker`

`heap_usage_tracker` 物件包含下列與 heap 使用量相關的統計資料。

欄位名稱 | 資料類型 | 說明
:--- | :--- | :---
`cancellation_count` | 整數 | 自節點上次重新啟動以來，因 heap 使用量過高而被標記為取消的任務數量。
`current_max_bytes` | 整數 | 節點上目前執行的所有任務的最大 heap 使用量，單位為位元組。
`current_avg_bytes` | 整數 | 節點上目前執行的所有任務的平均 heap 使用量，單位為位元組。
`rolling_avg_bytes` | 整數 | 最近 `n` 個任務的滾動平均 heap 使用量，單位為位元組。`n` 可透過 `search_backpressure.search_shard_task.heap_moving_average_window_size` 設定來組態。此設定的預設值為 100。

#### `cpu_usage_tracker`

`cpu_usage_tracker` 物件包含下列與 CPU 使用量相關的統計資料。

欄位名稱 | 資料類型 | 說明
:--- | :--- | :---
`cancellation_count` | 整數 | 自節點上次重新啟動以來，因 CPU 使用量過高而被標記為取消的任務數量。
`current_max_millis` | 整數 | 節點上目前執行的所有任務的最大 CPU 時間，單位為毫秒。
`current_avg_millis` | 整數 | 節點上目前執行的所有任務的平均 CPU 時間，單位為毫秒。

### `cancellation_stats`

`cancellation_stats` 物件包含被標記為取消之任務的下列統計資料。

欄位名稱 | 資料類型 | 說明
:--- | :--- | :---
`cancellation_count` | 整數 | 自節點上次重新啟動以來，被標記為取消的任務總數。
`cancellation_limit_reached_count` | 整數 | 符合取消條件的任務數量超過所設定取消閾值的次數。

每個資源追蹤器 (heap、CPU、經過時間) 會獨立識別超出其閾值的任務，並遞增自己的 `cancellation_count`。由於單一任務可能同時超出多個資源閾值，因此資源追蹤器 `cancellation_count` 值的總和可能高於頂層 `cancellation_count`，後者代表實際被取消的不重複任務數量。`cancellation_limit_reached_count` 會在觀察器迭代期間達到取消速率限制時遞增，以防止該次迭代中進行額外的取消。
{: .note}
