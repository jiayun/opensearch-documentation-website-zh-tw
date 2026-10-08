---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 節點屬性"
parent: CAT APIs
nav_order: 35
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-nodeattrs/
---

# CAT 節點屬性 API
**於 1.0 版推出**
{: .label .label-purple }

CAT 節點屬性操作會列出自訂節點的屬性。


<!-- spec_insert_start
api: cat.nodeattrs
component: endpoints
-->
## 端點
```json
GET /_cat/nodeattrs
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.nodeattrs
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 允許與叢集管理員節點建立連線的時間長度。 | 不適用 |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | 不適用 |
| `h` | 清單 | 要顯示的欄名稱清單，以逗號分隔。 | 不適用 |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `s` | 清單 | 用於排序的欄名稱或欄別名清單，以逗號分隔。 | 不適用 |
| `v` | 布林值 | 啟用詳細模式，會顯示欄標頭。 | `false` |

<!-- spec_insert_end -->

## 請求範例

下列範例請求會傳回自訂節點的屬性：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/nodeattrs?v
body: 
-->
{% capture step1_rest %}
GET /_cat/nodeattrs?v

{% endcapture %}

{% capture step1_python %}


response = client.cat.nodeattrs(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例

```json
node | host | ip | attr | value
odfe-node2 | 172.18.0.3 | 172.18.0.3 | testattr | test
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/nodes/info`。
