---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引範本是否存在"
parent: Index templates
grand_parent: Index APIs
nav_order: 40
---

# 索引範本是否存在
**於 1.0 版推出**
{: .label .label-purple }

索引範本是否存在 API 操作用於驗證索引範本是否存在。

## 端點

```json
HEAD /_index_template/{template-name}
```

## 路徑參數

所有路徑參數皆為必要。

| 參數       | 類型   | 說明                                        |
| --------------- | ------ | -------------------------------------------------- |
| `template-name` | 字串 | 要檢查是否存在的索引範本名稱。 |

## 查詢參數

所有參數皆為選用。

| 參數                 | 類型    | 說明                                                                                          |
| ------------------------- | ------- | ---------------------------------------------------------------------------------------------------- |
| `local` | 布林值 | 若為 true，請求不會從叢集管理員節點擷取狀態。預設值為 `false`。 |
| `cluster_manager_timeout` | 時間 | 指定等待連線至叢集管理員節點的時間長度。預設值為 `30s`。           |

## 請求範例

<!-- spec_insert_start
component: example_code
rest: HEAD /_index_template/my-template
-->
{% capture step1_rest %}
HEAD /_index_template/my-template
{% endcapture %}

{% capture step1_python %}


response = client.indices.exists_index_template(
  name = "my-template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

若範本存在，回應會傳回成功碼：

```json
200 OK
```

若範本不存在，回應會傳回失敗碼：

```json
404 Not Found
```
