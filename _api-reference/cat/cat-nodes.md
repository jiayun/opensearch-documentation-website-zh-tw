---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT nodes
parent: CAT APIs
nav_order: 40
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-nodes/
---

# CAT Nodes API
**於 1.0 版導入**
{: .label .label-purple }

CAT nodes 操作會列出節點層級的資訊，包括節點角色與負載指標。

幾個重要的節點指標包括 `pid`、`name`、`cluster_manager`、`ip`、`port`、`version`、`build`、`jdk`，以及 `disk`、`heap`、`ram` 和 `file_desc`。


<!-- spec_insert_start
api: cat.nodes
component: endpoints
-->
## 端點
```json
GET /_cat/nodes
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.nodes
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | 字串 | 顯示位元組值時使用的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 和 `p`。 | N/A |
| `cluster_manager_timeout` | 字串 | 建立與叢集管理員節點之連線所允許的時間。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `full_id` | 布林值或字串 | 當設為 `true` 時，傳回完整的節點 ID；當設為 `false` 時，傳回縮短的節點 ID。 | `false` |
| `h` | 清單 | 以逗號分隔的欄位名稱清單，指定要顯示的欄位。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `s` | 清單 | 以逗號分隔的欄位名稱或欄位別名清單，用於排序。 | N/A |
| `time` | 字串 | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 和 `d`。 | N/A |
| `v` | 布林值 | 啟用詳細模式，顯示欄位標頭。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會列出節點層級的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/nodes?v
-->
{% capture step1_rest %}
GET /_cat/nodes?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.nodes(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

```json
ip       |   heap.percent | ram.percent | cpu load_1m | load_5m | load_15m | node.role | node.roles |     cluster_manager |  name
10.11.1.225  |         31   |    32  | 0  |  0.00  |  0.00   | di  | data,ingest,ml  | - |  data-e5b89ad7
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/nodes/info` 和 `cluster:monitor/nodes/stats`。
