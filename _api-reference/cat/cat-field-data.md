---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 欄位資料"
parent: CAT APIs
nav_order: 15
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-field-data/
---

# CAT Field Data API
**於 1.0 版推出**
{: .label .label-purple }

CAT Field Data 操作會列出每個節點上各欄位使用的記憶體大小。

<!-- spec_insert_start
api: cat.fielddata
component: endpoints
-->
## 端點
```json
GET /_cat/fielddata
GET /_cat/fielddata/{fields}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.fielddata
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | 字串 | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 和 `p`。 | N/A |
| `fields` | 清單或字串 | 以逗號分隔的欄位清單，用於限制傳回的資訊量。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的欄名稱清單，指定要顯示的欄。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `s` | 清單 | 以逗號分隔的欄名稱或欄別名清單，用於指定排序依據。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示欄標頭。 | `false` |

<!-- spec_insert_end -->

## 請求範例

<!-- spec_insert_start
component: example_code
rest: GET /_cat/fielddata?v
-->
{% capture step1_rest %}
GET /_cat/fielddata?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.fielddata(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要將資訊限制為特定欄位，請在您的查詢後加上欄位名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/fielddata/<field_name>?v
-->
{% capture step1_rest %}
GET /_cat/fielddata/<field_name>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.fielddata(
  fields = "<field_name>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若您想取得多個欄位的資訊，請以逗號分隔欄位名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/fielddata/field_name_1,field_name_2,field_name_3
-->
{% capture step1_rest %}
GET /_cat/fielddata/field_name_1,field_name_2,field_name_3
{% endcapture %}

{% capture step1_python %}


response = client.cat.fielddata(
  fields = "field_name_1,field_name_2,field_name_3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

下列回應顯示所有欄位的記憶體大小為 284 位元組：

```json
id                     host       ip         node       field size
1vo54NuxSxOrbPEYdkSF0w 172.18.0.4 172.18.0.4 odfe-node1 _id   284b
ZaIkkUd4TEiAihqJGkp5CA 172.18.0.3 172.18.0.3 odfe-node2 _id   284b
```
