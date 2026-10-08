---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 範本"
parent: CAT APIs
nav_order: 70
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-templates/
---

# CAT Templates API
**於 1.0 版導入**
{: .label .label-purple }

CAT templates 操作會列出索引範本的名稱、模式、順序編號與版本編號。


<!-- spec_insert_start
api: cat.templates
component: endpoints
-->
## 端點
```json
GET /_cat/templates
GET /_cat/templates/{name}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.templates
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | String | 建立與叢集管理員節點連線所允許的時間。 | N/A |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔、要顯示的欄位名稱清單。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `local` | Boolean | 傳回本機資訊，但不從叢集管理員節點擷取狀態。 | `false` |
| `s` | List | 以逗號分隔、用於排序的欄位名稱或欄位別名清單。 | N/A |
| `v` | Boolean | 啟用詳細模式，顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會傳回所有範本的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/templates?v
-->
{% capture step1_rest %}
GET /_cat/templates?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.templates(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得特定範本或模式的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/templates/<template_name_or_pattern>
-->
{% capture step1_rest %}
GET /_cat/templates/<template_name_or_pattern>
{% endcapture %}

{% capture step1_python %}


response = client.cat.templates(
  name = "<template_name_or_pattern>"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

```
name | index_patterns order version composed_of
tenant_template | [opensearch-dashboards*] | 0  |    
```

若要進一步了解索引範本，請參閱[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/template/get`。
