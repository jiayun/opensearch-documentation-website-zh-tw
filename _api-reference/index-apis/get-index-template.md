---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 30
---

# Get Index Template API
**於 1.0 版推出**
{: .label .label-purple }

Get Index Template API 會傳回一或多個索引範本的資訊。

## 端點

```json
GET /_index_template/{template-name}
```

## 查詢參數

支援下列選用的查詢參數。

參數 | 類型 | 說明
:--- | :--- | :---
`create` | 布林值 | 設為 true 時，API 無法取代或更新任何現有的索引範本。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。
`flat_settings` | 布林值 | 是否以扁平形式傳回設定，這可提升可讀性，尤其是對於多層巢狀的設定。例如，"index": { "creation_date": "123456789" } 的扁平形式為 "index.creation_date": "123456789"。

## 範例請求

下列範例請求使用萬用字元運算式取得某個索引範本的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_index_template/h*
-->
{% capture step1_rest %}
GET /_index_template/h*
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_index_template(
  name = "h*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例請求取得所有索引範本的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_index_template
-->
{% capture step1_rest %}
GET /_index_template
{% endcapture %}

{% capture step1_python %}

response = client.indices.get_index_template()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/index_template/get`。
