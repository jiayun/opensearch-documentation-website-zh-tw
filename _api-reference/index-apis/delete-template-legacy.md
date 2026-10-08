---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.

layout: default
title: "刪除範本（已淘汰）"
parent: Index templates
grand_parent: Index APIs
nav_order: 110
---

# 刪除範本
**於 1.0 版導入**
{: .label .label-purple }

Delete Template API 已被淘汰。請改用新的 [Delete Index Template]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index-template/) API。
{: .warning}

刪除範本 API 操作會刪除使用舊版 `/_template` 端點建立的索引範本。


## 端點

```json
DELETE /_template/{template-name}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數    | 類型   | 說明                                                 |
| :----------- | :----- | :---------------------------------------------------------- |
| `index-name` | String | 要刪除的索引名稱。支援萬用字元運算式。 |

## 查詢參數

下表列出可用的查詢參數。所有參數皆為選用。

| 參數       | 類型 | 說明                                                                                  |
| :-------------- | :--- | :------------------------------------------------------------------------------------------- |
| `cluster_manager_timeout` | Time | 指定等待連線至叢集管理員節點的時間長度。預設為 `30s`。 |
| `timeout` | Time | 指定等待操作完成的時間長度。預設為 `30s`。 |

## 範例請求

<!-- spec_insert_start
component: example_code
rest: DELETE /_template/logging_template
-->
{% capture step1_rest %}
DELETE /_template/logging_template
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete_template(
  name = "logging_template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "acknowledged": true
}
```

