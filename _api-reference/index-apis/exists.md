---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引是否存在"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 40
redirect_from:
  - /opensearch/rest-api/index-apis/exists/
---

# Index Exists API
**於 1.0 版推出**
{: .label .label-purple }

Index Exists API 操作會傳回索引是否已存在。


## 端點

```json
HEAD /{index-name}
```

## 查詢參數

所有參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 是否忽略未符合任何索引的萬用字元。預設為 `true`。
`expand_wildcards` | 字串 | 將萬用字元運算式展開為不同的索引。使用逗號分隔多個值。可用值為 all（符合所有索引）、open（符合開啟的索引）、closed（符合關閉的索引）、hidden（符合隱藏的索引）及 none（不接受萬用字元運算式）。預設為 `open`。
`flat_settings` | 布林值 | 是否以扁平形式傳回設定，以提升可讀性，尤其適用於多層巢狀設定。例如，"index": { "creation_date": "123456789" } 的扁平形式為 "index.creation_date": "123456789"。
`include_defaults` | 布林值 | 是否在回應中包含預設設定。此參數有助於識別您想更新的設定名稱及目前的值。
`ignore_unavailable` | 布林值 | 若為 true，OpenSearch 不會搜尋不存在或已關閉的索引。預設為 `false`。
`local` | 布林值 | 是否僅從本機節點傳回資訊，而非從叢集管理員節點傳回。預設為 `false`。


## 請求範例

<!-- spec_insert_start
component: example_code
rest: HEAD /sample-index
-->
{% capture step1_rest %}
HEAD /sample-index
{% endcapture %}

{% capture step1_python %}


response = client.indices.exists(
  index = "sample-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

Index Exists API 操作只會傳回兩種可能的回應碼之一：`200` -- 索引存在，以及 `404` -- 索引不存在。

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/exists`。
