---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取消任務"
parent: Tasks APIs
nav_order: 40
---

# Cancel Tasks API
**於 1.0 版推出**
{: .label .label-purple }

Cancel Tasks API 會取消任務，使其停止在叢集中執行。並非所有任務都可以取消。若要判斷任務是否可取消，請檢查 Cancel Tasks API 回應中的 `cancellable` 欄位。


<!-- spec_insert_start
api: tasks.cancel
component: endpoints
-->
## 端點
```json
POST /_tasks/_cancel
POST /_tasks/{task_id}/_cancel
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.cancel
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `task_id` | String | 任務 ID。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.cancel
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `actions` | List 或 String | 以逗號分隔的動作清單，指定應傳回的動作。保留空白即可傳回全部。 |
| `nodes` | List | 以逗號分隔的節點 ID 或名稱清單，用於限制傳回的資訊。使用 `_local` 可傳回您所連線節點的資訊；指定節點名稱可取得特定節點的資訊；保留此參數空白則可取得所有節點的資訊。 |
| `parent_task_id` | String | 傳回具有指定父任務 ID（`node_id:task_number`）的任務。保留空白或設為 -1 即可傳回全部。 |
| `wait_for_completion` | Boolean | 等待相符的任務完成。設為 `true` 時，請求會持續等待，直到任務完成為止。_（預設值：`false`）_ |

<!-- spec_insert_end -->

## 範例請求

下列請求會取消目前在 `opensearch-node1` 和 `opensearch-node2` 上執行的所有任務：

<!-- spec_insert_start
component: example_code
rest: POST /_tasks/_cancel?nodes=opensearch-node1,opensearch-node2
-->
{% capture step1_rest %}
POST /_tasks/_cancel?nodes=opensearch-node1,opensearch-node2
{% endcapture %}

{% capture step1_python %}


response = client.tasks.cancel(
  params = { "nodes": "opensearch-node1,opensearch-node2" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列回應顯示，一個批次寫入任務和一個更新任務已在沒有節點失敗的情況下取消，並提供已取消任務的其他資訊：

```json
{
  "node_failures": [],
  "nodes": {
    "JzrCxdtFTCO_RaINw8ckNA": {
      "name": "opensearch-node1",
      "transport_address": "127.0.0.1:9300",
      "host": "127.0.0.1",
      "ip": "127.0.0.1:9300",
      "roles": [
        "data",
        "ingest",
        "cluster_manager",
        "remote_cluster_client"
      ],
      "attributes": {},
      "tasks": {
        "JzrCxdtFTCO_RaINw8ckNA:54": {
          "node": "JzrCxdtFTCO_RaINw8ckNA",
          "id": 54,
          "type": "transport",
          "action": "indices:data/write/bulk",
          "status": "cancelled",
          "description": "bulk request to [test_index]",
          "start_time_in_millis": 1625145678901,
          "running_time_in_nanos": 2345678,
          "cancellable": true,
          "cancelled": true
        }
      }
    },
    "K8iyDdtGQCO_SbJNw9dkMB": {
      "name": "opensearch-node2",
      "transport_address": "127.0.0.1:9301",
      "host": "127.0.0.1",
      "ip": "127.0.0.1:9301",
      "roles": [
        "data",
        "ingest",
        "master",
        "remote_cluster_client"
      ],
      "attributes": {},
      "tasks": {
        "K8iyDdtGQCO_SbJNw9dkMB:78": {
          "node": "K8iyDdtGQCO_SbJNw9dkMB",
          "id": 78,
          "type": "transport",
          "action": "indices:data/write/update",
          "status": "cancelled",
          "description": "updating document in [another_index]",
          "start_time_in_millis": 1625145679012,
          "running_time_in_nanos": 1234567,
          "cancellable": true,
          "cancelled": true
        }
      }
    }
  }
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/tasks/cancel`。
