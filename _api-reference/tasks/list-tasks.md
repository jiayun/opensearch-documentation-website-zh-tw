---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出工作"
parent: Tasks APIs
nav_order: 10
---

# 列出工作 API
**於 1.0 版推出**
{: .label .label-purple }

列出工作 API 會傳回叢集中正在執行的工作清單。 

<!-- spec_insert_start
api: tasks.list
component: endpoints
-->
## 端點
```json
GET /_tasks
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.list
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `actions` | 清單或字串 | 要傳回的動作清單，以逗號分隔。保留空白可傳回所有動作。 | N/A |
| `detailed` | 布林值 | 當值為 `true` 時，回應會包含分片復原的詳細資訊。 | `false` |
| `group_by` | 字串 | 依父子關係或節點將工作分組。<br> 有效值為：`nodes`、`none` 和 `parents`。 | `nodes` |
| `nodes` | 清單 | 以逗號分隔的節點 ID 或名稱清單，用於限制傳回的資訊。使用 `_local` 可傳回您正在連線的節點資訊；指定節點名稱可取得特定節點的資訊；將參數保留空白可取得所有節點的資訊。 | N/A |
| `parent_task_id` | 字串 | 傳回具有指定父工作 ID（`node_id:task_number`）的工作。保留空白或設為 -1 可傳回所有工作。 | N/A |
| `timeout` | 字串 | 等待回應的時間長度。 | N/A |
| `wait_for_completion` | 布林值 | 等待符合條件的工作完成。當值為 `true` 時，請求會持續等待，直到工作完成。 | `false` |

<!-- spec_insert_end -->

## 請求範例

下列請求會傳回目前在名為 `opensearch-node1` 的節點上執行的工作：

<!-- spec_insert_start
component: example_code
rest: GET /_tasks?nodes=opensearch-node1
-->
{% capture step1_rest %}
GET /_tasks?nodes=opensearch-node1
{% endcapture %}

{% capture step1_python %}


response = client.tasks.list(
  params = { "nodes": "opensearch-node1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

下列回應提供正在執行的工作資訊：

```json
{
  "nodes": {
    "Mgqdm0r9SEGClWxp_RbnaQ": {
      "name": "opensearch-node1",
      "transport_address": "sample_address",
      "host": "sample_host",
      "ip": "sample_ip",
      "roles": [
        "data",
        "ingest",
        "master",
        "remote_cluster_client"
      ],
      "tasks": {
        "Mgqdm0r9SEGClWxp_RbnaQ:24578": {
          "node": "Mgqdm0r9SEGClWxp_RbnaQ",
          "id": 24578,
          "type": "transport",
          "action": "cluster:monitor/tasks/lists",
          "start_time_in_millis": 1611612517044,
          "running_time_in_nanos": 638700,
          "cancellable": false,
          "headers": {}
        },
        "Mgqdm0r9SEGClWxp_RbnaQ:24579": {
          "node": "Mgqdm0r9SEGClWxp_RbnaQ",
          "id": 24579,
          "type": "direct",
          "action": "cluster:monitor/tasks/lists[n]",
          "start_time_in_millis": 1611612517044,
          "running_time_in_nanos": 222200,
          "cancellable": false,
          "parent_task_id": "Mgqdm0r9SEGClWxp_RbnaQ:24578",
          "headers": {}
        }
      }
    }
  }
}
```

### `resource_stats` 物件

`resource_stats` 物件僅會針對支援資源追蹤的工作更新。這些統計資料根據排程的執行緒執行次數計算，涵蓋已完成工作及目前正在處理工作的執行緒。由於同一執行緒可能多次被排程處理同一工作，因此特定執行緒每次被排程處理特定工作，都視為一次執行緒執行。

下表列出 `resource_stats` 物件中的所有回應欄位。 

回應欄位 | 說明 |
:--- | :--- |
`average` | 所有排程的執行緒執行所使用的平均資源量。 |
`total` | 所有排程的執行緒執行所使用的資源總量。 |
`min` | 所有排程的執行緒執行所使用的最小資源量。 |
`max` | 所有排程的執行緒執行所使用的最大資源量。 |
`thread_info` | 與執行緒數量相關的統計資料。|
`thread_info.active_threads` | 目前正在處理工作的執行緒數量。 |
`thread_info.thread_executions` | 已被排程處理工作的執行緒數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/tasks/list`。
