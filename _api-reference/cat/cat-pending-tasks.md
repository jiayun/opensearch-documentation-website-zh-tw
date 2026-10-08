---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 擱置中任務"
parent: CAT APIs
nav_order: 45
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-pending-tasks/
---

# CAT Pending Tasks API
**於 1.0 版導入**
{: .label .label-purple }

CAT pending tasks 作業會列出所有擱置中任務的進度，包括任務優先順序以及在佇列中的時間。


<!-- spec_insert_start
api: cat.pending_tasks
component: endpoints
-->
## 端點
```json
GET /_cat/pending_tasks
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.pending_tasks
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | String | 允許建立與叢集管理員節點連線的時間。 | N/A |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔、要顯示的欄位名稱清單。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `local` | Boolean | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `s` | List | 以逗號分隔、用於排序的欄位名稱或欄位別名清單。 | N/A |
| `time` | String | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱 [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。 <br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 與 `d`。 | N/A |
| `v` | Boolean | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會列出所有擱置中節點任務的進度：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/pending_tasks?v
-->
{% capture step1_rest %}
GET /_cat/pending_tasks?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.pending_tasks(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
insertOrder | timeInQueue | priority | source
  1786      |    1.8s     |  URGENT  | shard-started
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/task`。
