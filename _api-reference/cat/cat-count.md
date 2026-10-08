---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT count
parent: CAT APIs
nav_order: 10
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-count/

---

# CAT Count API
**1.0 版引入**
{: .label .label-purple }

CAT count 作業會列出叢集中的文件數量。


<!-- spec_insert_start
api: cat.count
component: endpoints
-->
## 端點
```json
GET /_cat/count
GET /_cat/count/{index}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.count
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `s` | List | 以逗號分隔的欄位名稱或欄位別名清單，用於排序。 | N/A |
| `v` | Boolean | 啟用詳細模式，顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_cat/count?v
-->
{% capture step1_rest %}
GET /_cat/count?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.count(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要查看特定索引或別名中的文件數量，請在查詢後加上索引或別名名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/count/<index_or_alias>?v
-->
{% capture step1_rest %}
GET /_cat/count/<index_or_alias>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.count(
  index = "<index_or_alias>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得多個索引或別名的資訊，請以逗號分隔索引或別名名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/count/index_or_alias_1,index_or_alias_2,index_or_alias_3
-->
{% capture step1_rest %}
GET /_cat/count/index_or_alias_1,index_or_alias_2,index_or_alias_3
{% endcapture %}

{% capture step1_python %}


response = client.cat.count(
  index = "index_or_alias_1,index_or_alias_2,index_or_alias_3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列回應顯示整體文件數量為 1625：

```json
epoch      | timestamp | count
1624237738 | 01:08:58  | 1625
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:data/read/search`。
