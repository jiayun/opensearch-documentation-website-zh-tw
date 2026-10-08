---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 快照"
parent: CAT APIs
nav_order: 65
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-snapshots/
---

# CAT Snapshots API
**1.0 版推出**
{: .label .label-purple }

CAT snapshots 操作會列出儲存庫的所有快照。


<!-- spec_insert_start
api: cat.snapshots
component: endpoints
-->
## 端點
```json
GET /_cat/snapshots
GET /_cat/snapshots/{repository}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.snapshots
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `repository` | 清單或字串 | **（必要）** 以逗號分隔的快照儲存庫清單，用於限制請求。接受萬用字元運算式。`_all` 會傳回所有儲存庫。若請求期間有任何儲存庫失敗，OpenSearch 會傳回錯誤。 | N/A |
| `cluster_manager_timeout` | 字串 | 允許建立與叢集管理員節點連線的時間長度。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `ignore_unavailable` | 布林值 | 當設為 `true` 時，回應不會包含來自無法使用之快照的資訊。 | `false` |
| `s` | 清單 | 以逗號分隔的欄位名稱或欄位別名清單，用於指定排序依據。 | N/A |
| `time` | 字串 | 指定時間單位，例如 `5d` 或 `7h`。如需詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 及 `d`。 | N/A |
| `v` | 布林值 | 啟用詳細模式，會顯示欄位標頭。 | `false` |

<!-- spec_insert_end -->

## 請求範例

以下請求範例會列出所有快照：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/snapshots?v
-->
{% capture step1_rest %}
GET /_cat/snapshots?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.snapshots(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例

```json
index | shard | prirep | state   | docs | store | ip |       | node
plugins | 0   |   p    | STARTED |   0  |  208b | 172.18.0.4 | odfe-node1
plugins | 0   |   r    | STARTED |   0  |  208b | 172.18.0.3 |  odfe-node2          
```

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/snapshot/get`。
