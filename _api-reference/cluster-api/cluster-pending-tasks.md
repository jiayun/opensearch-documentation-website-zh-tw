---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集擱置中任務"
nav_order: 46
parent: Cluster APIs
has_children: false
---

# Cluster Pending Tasks API
**於 1.0 版導入**
{: .label .label-purple }

`/_cluster/pending_tasks` API 會回傳尚未執行的叢集層級變更清單。這些擱置中的任務通常是排入佇列的操作，例如建立索引、更新範本、變更分片配置，以及其他叢集狀態更新。

此 API 可用於監控叢集狀態，並診斷叢集狀態更新延遲的問題，尤其是在任務積壓或卡住時。

## 端點

```json
GET /_cluster/pending_tasks
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數        | 資料類型 | 說明                                                                                                             |
| ---------------- | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| `local` | 布林值 | 是否僅從本機節點回傳資訊，而非從選出的叢集管理員節點回傳。預設為 `false`。 |
| `cluster_manager_timeout` | Time | 指定連線至叢集管理員節點的逾時時間。預設為 `30s`。                                     |

## 範例請求

下列請求會回傳目前擱置中的叢集狀態更新任務清單：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/pending_tasks
-->
{% capture step1_rest %}
GET /_cluster/pending_tasks
{% endcapture %}

{% capture step1_python %}

response = client.cluster.pending_tasks()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例回應

```json
{
  "tasks": [
    {
      "insert_order": 1234,
      "priority": "HIGH",
      "source": "create-index [logs-2025.07.15]",
      "executing": false,
      "time_in_queue_millis": 28,
      "time_in_queue": "28ms"
    },
    {
      "insert_order": 1235,
      "priority": "URGENT",
      "source": "shard-started shard id [logs-2025.07.15][0]",
      "executing": true,
      "time_in_queue_millis": 3,
      "time_in_queue": "3ms"
    }
  ]
}
```

`_cluster/pending_tasks` API 通常會回傳空陣列，因為任務通常處理得太快，而不會出現在回應中。
{: .note}  

## 回應欄位

下表列出所有回應欄位。

| 欄位                           | 資料類型 | 說明                                                        |
| ------------------------------- | --------- | ------------------------------------------------------------------ |
| `tasks` | 陣列 | 擱置中的叢集狀態更新任務清單。                        |
| `tasks[n].insert_order` | 整數 | 任務加入佇列的順序。                    |
| `tasks[n].priority` | 字串 | 任務的優先順序層級 (例如 `HIGH`、`URGENT`)。               |
| `tasks[n].source` | 字串 | 提交該任務之操作的說明。              |
| `tasks[n].executing` | 布林值 | 確認任務目前是否正在執行。                      |
| `tasks[n].time_in_queue_millis` | 整數 | 任務在佇列中等待的時間 (以毫秒為單位)。 |
| `tasks[n].time_in_queue` | 字串 | `time_in_queue_millis` 的易讀版本。                  |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/task`。
