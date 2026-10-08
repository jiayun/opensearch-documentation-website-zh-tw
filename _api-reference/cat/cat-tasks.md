---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 任務"
parent: CAT APIs
nav_order: 70
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-tasks/
---

# CAT Tasks API
**於 1.0 版引入**
{: .label .label-purple }

CAT tasks 作業會列出目前在您叢集中執行的所有任務的進度。

<!-- spec_insert_start
api: cat.tasks
component: endpoints
-->
## 端點
```json
GET /_cat/tasks
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.tasks
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `actions` | 清單 | 用於限制回應的任務動作名稱。 | N/A |
| `detailed` | 布林值 | 若為 `true`，回應會包含關於分片復原的詳細資訊。 | `false` |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔、要顯示的欄位名稱清單。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `nodes` | 清單 | 以逗號分隔的節點 ID 或名稱清單，用於限制傳回的資訊。  使用 `_local` 傳回您所連線節點的資訊、指定要取得資訊的特定節點，或將此參數留空以取得所有節點的資訊。 | N/A |
| `parent_task_id` | 字串 | 用於限制回應的父任務識別碼。 | N/A |
| `s` | 清單 | 以逗號分隔、用於排序的欄位名稱或欄位別名清單。 | N/A |
| `time` | 字串 | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。 <br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 和 `d`。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 請求範例

下列請求範例會列出所有進行中的任務：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/tasks?v
-->
{% capture step1_rest %}
GET /_cat/tasks?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.tasks(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例

```json
action | task_id | parent_task_id | type | start_time | timestamp | running_time | ip | node
cluster:monitor/tasks/lists | 1vo54NuxSxOrbPEYdkSF0w:168062 | - | transport | 1624337809471 | 04:56:49 | 489.5ms | 172.18.0.4 | odfe-node1     
```

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/tasks/list`。
