---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT allocation
parent: CAT APIs
redirect_from:
- /opensearch/rest-api/cat/cat-allocation/
nav_order: 5
has_children: false
---

# CAT Allocation API
**Introduced 1.0**
{: .label .label-purple }

CAT allocation 作業會列出索引的磁碟空間配置，以及每個節點上的分片數量。



<!-- spec_insert_start
api: cat.allocation
component: endpoints
-->
## 端點
```json
GET /_cat/allocation
GET /_cat/allocation/{node_id}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.allocation
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | String | 用來顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 及 `p`。 | N/A |
| `cluster_manager_timeout` | String | 連線至叢集管理員節點的逾時時間。 | N/A |
| `format` | String | HTTP `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `local` | Boolean | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `s` | List | 以逗號分隔的欄位名稱或欄位別名清單，用於指定排序依據。 | N/A |
| `v` | Boolean | 啟用詳細模式，會顯示欄位標頭。 | `false` |

<!-- spec_insert_end -->

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cat/allocation?v
-->
{% capture step1_rest %}
GET /_cat/allocation?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.allocation(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要將資訊限制在特定節點，請在查詢後加上節點名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/allocation/<node_name>
-->
{% capture step1_rest %}
GET /_cat/allocation/<node_name>
{% endcapture %}

{% capture step1_python %}


response = client.cat.allocation(
  node_id = "<node_name>"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想取得多個節點的資訊，請以逗號分隔節點名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/allocation/node_name_1,node_name_2,node_name_3
-->
{% capture step1_rest %}
GET /_cat/allocation/node_name_1,node_name_2,node_name_3
{% endcapture %}

{% capture step1_python %}


response = client.cat.allocation(
  node_id = "node_name_1,node_name_2,node_name_3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列回應顯示兩個可用節點各配置了八個分片：

```json
shards | disk.indices | disk.used | disk.avail | disk.total | disk.percent | host         | ip          | node
  8    |   989.4kb    |   25.9gb  |   32.4gb   |   58.4gb   |   44         | 172.18.0.4   | 172.18.0.4  | odfe-node1
  8    |   962.4kb    |   25.9gb  |   32.4gb   |   58.4gb   |   44         | 172.18.0.3   | 172.18.0.3  | odfe-node2
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:monitor/allocation/explain`。
