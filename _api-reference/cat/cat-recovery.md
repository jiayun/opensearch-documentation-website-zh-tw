---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT recovery
parent: CAT APIs
nav_order: 50
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-recovery/
---

# CAT Recovery API
**1.0 版導入**
{: .label .label-purple }

CAT recovery 操作會列出所有已完成與進行中的索引與分片復原。


<!-- spec_insert_start
api: cat.recovery
component: endpoints
-->
## 端點
```json
GET /_cat/recovery
GET /_cat/recovery/{index}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.recovery
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `active_only` | 布林值 | 若為 `true`，回應僅包含進行中的分片復原。 | `false` |
| `bytes` | 字串 | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 與 `p`。 | N/A |
| `detailed` | 布林值 | 當為 `true` 時，包含分片復原的詳細資訊。 | `false` |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `index` | 清單 | 以逗號分隔的資料串流、索引與別名清單，用於限制請求範圍。支援萬用字元 (`*`)。若要指定所有資料串流與索引，請省略此參數或使用 `*` 或 `_all`。 | N/A |
| `s` | 清單 | 以逗號分隔的欄位名稱或欄位別名清單，用於排序。 | N/A |
| `time` | 字串 | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 與 `d`。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cat/recovery?v
-->
{% capture step1_rest %}
GET /_cat/recovery?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.recovery(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若只要查看特定索引的復原情形，請在查詢後加上索引名稱。

<!-- spec_insert_start
component: example_code
rest: GET /_cat/recovery/<index>?v
-->
{% capture step1_rest %}
GET /_cat/recovery/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.recovery(
  index = "<index>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得多個索引的資訊，請以逗號分隔索引：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/recovery/index1,index2,index3
-->
{% capture step1_rest %}
GET /_cat/recovery/index1,index2,index3
{% endcapture %}

{% capture step1_python %}


response = client.cat.recovery(
  index = "index1,index2,index3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
index | shard | time | type | stage | source_host | source_node | target_host | target_node | repository | snapshot | files | files_recovered | files_percent | files_total | bytes | bytes_recovered | bytes_percent | bytes_total | translog_ops | translog_ops_recovered | translog_ops_percent
movies | 0 | 117ms | empty_store | done | n/a | n/a | 172.18.0.4 | odfe-node1 | n/a | n/a | 0 | 0 | 0.0% | 0 | 0 | 0 | 0.0% | 0 | 0 | 0 | 100.0%
movies | 0 | 382ms | peer | done | 172.18.0.4 | odfe-node1 | 172.18.0.3 | odfe-node2 | n/a | n/a | 1 | 1 |  100.0% | 1 | 208 | 208 | 100.0% | 208 | 1 | 1 | 100.0%
```

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/recovery`。
