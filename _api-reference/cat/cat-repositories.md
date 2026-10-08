---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 儲存庫"
parent: CAT APIs
nav_order: 52
has_children: false
redirect_from:
 - /opensearch/rest-api/cat/cat-repositories/
---

# CAT Repositories API
**於 1.0 版引入**
{: .label .label-purple }

CAT repositories 操作會列出叢集的所有快照儲存庫。

<!-- spec_insert_start
api: cat.repositories
component: endpoints
-->
## 端點
```json
GET /_cat/repositories
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.repositories
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 允許用於建立與叢集管理員節點連線的時間長度。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 要顯示的欄名稱清單，以逗號分隔。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不從叢集管理員節點擷取狀態。 | `false` |
| `s` | 清單 | 用於排序的欄名稱或欄別名清單，以逗號分隔。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示欄標題。 | `false` |

<!-- spec_insert_end -->

## 請求範例

下列請求範例會列出叢集中的所有快照儲存庫：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/repositories?v
-->
{% capture step1_rest %}
GET /_cat/repositories?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.repositories(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例

```json
id    type
repo1   fs
repo2   s3
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/repository/get`。
