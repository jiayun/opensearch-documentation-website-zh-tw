---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "別名是否存在"
parent: Alias APIs
grand_parent: Index APIs
nav_order: 40
---

# Index Alias Exists API
**1.0 版推出**
{: .label .label-purple }

檢查別名是否存在。

## 端點

```json
HEAD /_alias/{alias}
HEAD /{index}/_alias/{alias}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<alias>` | 字串 | 要檢查的別名名稱，以逗號分隔的清單或萬用字元運算式表示。 |
| `<index>` | 字串 | 用於限制請求範圍的索引名稱，以逗號分隔的清單或萬用字元運算式表示。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `expand_wildcards` | 字串 | 萬用字元運算式可比對的索引類型。支援以逗號分隔的值。有效值為 `all`、`open`、`closed`、`hidden` 和 `none`。預設為 `all`。 |
| `ignore_unavailable` | 布林值 | 是否忽略無法使用的索引。預設為 `false`。 |
| `local` | 布林值 | 是否僅從本機節點傳回資訊，而非從叢集管理員節點傳回。預設為 `false`。 |

## 回應碼

API 會傳回下列其中一個回應碼。

| 回應碼 | 說明 |
| :--- | :--- |
| `200` | 表示所有指定的別名皆存在。 |
| `404` | 表示一個或多個指定的別名不存在。 |

## 請求範例

<!-- spec_insert_start
component: example_code
rest: HEAD /_alias/2030
-->
{% capture step1_rest %}
HEAD /_alias/2030
{% endcapture %}

{% capture step1_python %}


response = client.indices.exists_alias(
  name = "2030"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/aliases/get`。

## 相關文件

如需索引別名的詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。