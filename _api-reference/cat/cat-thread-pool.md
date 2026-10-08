---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 執行緒集區"
parent: CAT APIs
nav_order: 75
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-thread-pool/
---

# CAT 執行緒集區 API
**於 1.0 版引入**
{: .label .label-purple }

CAT 執行緒集區操作會列出每個節點上不同執行緒集區中作用中、佇列中及遭拒絕的執行緒。


<!-- spec_insert_start
api: cat.thread_pool
component: endpoints
-->
## 端點
```json
GET /_cat/thread_pool
GET /_cat/thread_pool/{thread_pool_patterns}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.thread_pool
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 連線至叢集管理員節點的逾時時間。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不會從叢集管理員節點擷取狀態。 | `false` |
| `s` | 清單 | 以逗號分隔的欄位名稱或欄位別名清單，用於指定排序依據。 | N/A |
| `size` | 整數 | 顯示數值時所使用的乘數。 | N/A |
| `v` | 布林值 | 啟用詳細模式，會顯示欄位標頭。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會提供所有節點上執行緒集區的相關資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/thread_pool?v
-->
{% capture step1_rest %}
GET /_cat/thread_pool?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.thread_pool(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想取得多個執行緒集區的資訊，請以逗號分隔執行緒集區名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/thread_pool/thread_pool_name_1,thread_pool_name_2,thread_pool_name_3
-->
{% capture step1_rest %}
GET /_cat/thread_pool/thread_pool_name_1,thread_pool_name_2,thread_pool_name_3
{% endcapture %}

{% capture step1_python %}


response = client.cat.thread_pool(
  thread_pool_patterns = "thread_pool_name_1,thread_pool_name_2,thread_pool_name_3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想將資訊限制在特定的執行緒集區，請在查詢後方加上執行緒集區名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/thread_pool/<thread_pool_name>?v
-->
{% capture step1_rest %}
GET /_cat/thread_pool/<thread_pool_name>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.thread_pool(
  thread_pool_patterns = "<thread_pool_name>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

```json
node_name  name                      active queue rejected
odfe-node2 ad-batch-task-threadpool    0     0        0
odfe-node2 ad-threadpool               0     0        0
odfe-node2 analyze                     0     0        0s
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:monitor/nodes/info`。
