---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 叢集管理員"
parent: CAT APIs
redirect_from:
 - /opensearch/rest-api/cat/cat-master/
nav_order: 30
has_children: false
---

# CAT Cluster Manager API
**於 1.0 版推出**
{: .label .label-purple }

CAT 叢集管理員操作會列出有助於識別已選出的叢集管理員節點的資訊。


<!-- spec_insert_start
api: cat.cluster_manager
component: endpoints
-->
## 端點
```json
GET /_cat/cluster_manager
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.cluster_manager
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 連線至叢集管理員節點的逾時時間。 | N/A |
| `format` | 字串 | HTTP `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的要顯示的欄名稱清單。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `s` | 清單 | 以逗號分隔的排序依據欄名稱或欄別名清單。 | N/A |
| `v` | 布林值 | 啟用詳細模式，此模式會顯示欄標頭。 | `false` |

<!-- spec_insert_end -->


## 請求範例

<!-- spec_insert_start
component: example_code
rest: GET /_cat/cluster_manager?v
-->
{% capture step1_rest %}
GET /_cat/cluster_manager?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.cluster_manager(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
id                     |   host     |     ip     |   node
ZaIkkUd4TEiAihqJGkp5CA | 172.18.0.3 | 172.18.0.3 | opensearch-node2
```

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/state`。
