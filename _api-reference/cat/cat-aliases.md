---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 別名"
parent: CAT APIs
redirect_from:
- /opensearch/rest-api/cat/cat-aliases/

nav_order: 1
has_children: false
---

# CAT 別名 API
**於 1.0 版推出**
{: .label .label-purple }

CAT 別名操作會列出別名與索引之間的對應，以及路由與篩選資訊。



<!-- spec_insert_start
api: cat.aliases
component: endpoints
-->
## 端點
```json
GET /_cat/aliases
GET /_cat/aliases/{name}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.aliases
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `expand_wildcards` | 清單或字串 | 指定萬用字元運算式可比對的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏的索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且非隱藏的索引。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔、要顯示的欄名稱清單。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 是否僅從本機節點而非叢集管理員節點傳回資訊。 | `false` |
| `s` | 清單 | 以逗號分隔、用於排序的欄名稱或欄別名清單。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示欄標題。 | `false` |

<!-- spec_insert_end -->


## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?v
-->
{% capture step1_rest %}
GET /_cat/aliases?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要將資訊限定為特定別名，請在查詢後方加上別名名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases/<alias>?v
-->
{% capture step1_rest %}
GET /_cat/aliases/<alias>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  name = "<alias>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得多個別名的資訊，請以逗號分隔各個別名名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases/alias1,alias2,alias3
body: 
-->
{% capture step1_rest %}
GET /_cat/aliases/alias1,alias2,alias3

{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  name = "alias1,alias2,alias3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列回應顯示不同類型的別名組態：

```json
alias            | index          | filter | routing.index | routing.search | is_write_index
current-logs     | app-logs-2024  | -      | -             | -              | -
filtered-data    | customer-data  | *      | -             | -              | -
regional-orders  | orders-2024    | -      | west          | west           | -
multi-route      | products       | -      | 1             | 1,2            | -
```

此回應顯示：
- `current-logs`：沒有篩選器或路由的簡單別名
- `filtered-data`：設定了篩選器的別名（以 `*` 表示）
- `regional-orders`：為編製索引與搜尋都設定了路由的別名
- `multi-route`：編製索引 (1) 與搜尋 (1,2) 使用不同路由的別名

若要進一步了解索引別名，請參閱[索引別名]({{site.url}}{{site.baseurl}}/opensearch/index-alias/)。有關別名管理 API，請參閱[別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/aliases/get`。
