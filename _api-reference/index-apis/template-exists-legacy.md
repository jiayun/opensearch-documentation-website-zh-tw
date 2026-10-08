---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "範本是否存在（已棄用）"
parent: Index templates
grand_parent: Index APIs
nav_order: 100
---

# 範本是否存在
**於 1.0 版引入**
{: .label .label-purple }

Template Exists API 已棄用。請使用新的 [Index Template Exists]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-template-exists/) API。
{: .warning}

範本是否存在 API 作業用於確認使用舊版 `/_template` 端點建立的一或多個索引範本是否存在。

## 端點

```json
HEAD /_template/{template-name}
```

## 路徑參數

下表列出可用的路徑參數。所有參數皆為必要參數。

| 參數       | 類型   | 說明                                                                      |
| :-------------- | :----- | :------------------------------------------------------------------------------- |
| `template-name` | 字串 | 要檢查的索引範本名稱。接受萬用字元運算式。               |

## 查詢參數

下表列出可用的查詢參數。所有參數皆為選用參數。

| 參數                  | 類型    | 說明                                                                                          |
| :------------------------- | :------ | :--------------------------------------------------------------------------------------------------- |
| `flat_settings` | 布林值 | 若為 `true`，則以扁平格式傳回設定。預設為 `false`。                                       |
| `local` | 布林值 | 若為 `true`，則請求不會從叢集管理員節點擷取狀態。預設為 `false`。 |
| `cluster_manager_timeout` | 時間 | 指定等待連線至叢集管理員節點的時間長度。預設為 `30s`。           |

## 請求範例

<!-- spec_insert_start
component: example_code
rest: HEAD /_template/logging_template
-->
{% capture step1_rest %}
HEAD /_template/logging_template
{% endcapture %}

{% capture step1_python %}


response = client.indices.exists_template(
  name = "logging_template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

若範本存在，則傳回 `200 OK` 狀態，且不含回應本文。若範本不存在，則傳回 `404 Not Found`。

