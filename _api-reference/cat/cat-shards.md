---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT shards
parent: CAT APIs
nav_order: 60
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-shards/
---

# CAT Shards API
**於 1.0 版導入**
{: .label .label-purple }

CAT shards 作業會列出所有主要分片與副本分片的狀態，以及它們的分佈方式。


<!-- spec_insert_start
api: cat.shards
component: endpoints
-->
## 端點
```json
GET /_cat/shards
GET /_cat/shards/{index}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.shards
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | String | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 與 `p`。 | N/A |
| `cluster_manager_timeout` | String | 建立與叢集管理員節點連線所允許的時間。 | N/A |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔、要顯示的欄位名稱清單。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `local` | Boolean | 傳回本機資訊，但不從叢集管理員節點擷取狀態。 | `false` |
| `s` | List | 以逗號分隔、用於排序的欄位名稱或欄位別名清單。 | N/A |
| `time` | String | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱 [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 與 `d`。 | N/A |
| `v` | Boolean | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會傳回分片的相關資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/shards?v
-->
{% capture step1_rest %}
GET /_cat/shards?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.shards(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若只要查看特定索引之分片的資訊，請在查詢後面加上索引名稱。

<!-- spec_insert_start
component: example_code
rest: GET /_cat/shards/<index>?v
-->
{% capture step1_rest %}
GET /_cat/shards/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.shards(
  index = "<index>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得多個索引的資訊，請以逗號分隔各索引：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/shards/index1,index2,index3
-->
{% capture step1_rest %}
GET /_cat/shards/index1,index2,index3
{% endcapture %}

{% capture step1_python %}


response = client.cat.shards(
  index = "index1,index2,index3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
index | shard | prirep | state   | docs | store | ip |       | node
plugins | 0   |   p    | STARTED |   0  |  208b | 172.18.0.4 | odfe-node1
plugins | 0   |   r    | STARTED |   0  |  208b | 172.18.0.3 |  odfe-node2          
```

## 限制回應大小

若要限制傳回的分片數量，請設定 `cat.shards.response.limit.number_of_shards` 設定。如需更多資訊，請參閱 [叢集層級 CAT 回應限制設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-cat-response-limit-settings)。

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/stats` 與 `cluster:monitor/state`。
