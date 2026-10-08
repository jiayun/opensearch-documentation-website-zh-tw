---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT health
parent: CAT APIs
nav_order: 20
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-health/
---

# CAT Health API
**1.0 版新增**
{: .label .label-purple }

CAT health 操作會列出叢集的狀態、叢集已執行的時間、節點數量，以及其他有助於您分析叢集健康狀態的實用資訊。


<!-- spec_insert_start
api: cat.health
component: endpoints
-->
## Endpoints
```json
GET /_cat/health
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.health
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## Query parameters

下表列出可用的查詢參數。所有查詢參數皆為選用。

| Parameter | Data type | Description | Default |
| :--- | :--- | :--- | :--- |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `s` | List | 以逗號分隔的欄位名稱或欄位別名清單，用於排序。 | N/A |
| `time` | String | 用於顯示時間值的單位。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 與 `d`。 | N/A |
| `ts` | Boolean | 設為 `true` 時，傳回 `HH:MM:SS` 與 Unix 紀元時間戳記。 | `true` |
| `v` | Boolean | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## Example request

下列範例請求會提供過去 5 天的叢集健康狀態資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/health?v&time=5d
-->
{% capture step1_rest %}
GET /_cat/health?v&time=5d
{% endcapture %}

{% capture step1_python %}


response = client.cat.health(
  params = { "v": "true", "time": "5d" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## Example response

```json
GET _cat/health?v&time=5d

epoch | timestamp | cluster | status | node.total | node.data | shards | pri | relo | init | unassign | pending_tasks | max_task_wait_time | active_shards_percent
1624248112 | 04:01:52 | odfe-cluster | green | 2 | 2 | 16 | 8 | 0 | 0 | 0 | 0 | - | 100.0%
```

## Required permissions

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/health`。
