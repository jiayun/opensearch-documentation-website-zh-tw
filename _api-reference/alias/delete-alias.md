---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除別名"
parent: Alias APIs
grand_parent: Index APIs
nav_order: 30
---

# Delete Index Alias API
**於 1.0 版推出**
{: .label .label-purple }

刪除現有的別名。

## 端點

```json
DELETE /{index}/_alias/{alias}
DELETE /{index}/_aliases/{alias}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為必要參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<index>` | 字串 | 用於限制請求範圍的索引名稱清單（以逗號分隔）或萬用字元運算式。若要包含叢集中的所有索引，請使用 `_all` 或 `*`。 |
| `<alias>` | 字串 | 要刪除的別名名稱清單（以逗號分隔）或萬用字元運算式。若要刪除所有別名，請使用 `_all` 或 `*`。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | 時間 | 等待叢集管理員節點回應的時間。預設為 `30s`。 |
| `timeout` | 時間 | 等待叢集回應的時間。預設為 `30s`。 |

## 請求範例

下列請求會從 `logs_20302801` 索引中刪除 `alias1` 別名：

<!-- spec_insert_start
component: example_code
rest: DELETE /logs_20302801/_alias/alias1
-->
{% capture step1_rest %}
DELETE /logs_20302801/_alias/alias1
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete_alias(
  index = "logs_20302801",
  name = "alias1"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
    "acknowledged": true
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `acknowledged` | 布林值 | 是否已收到請求。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具有適當的權限：`indices:admin/aliases`。

## 相關文件

如需索引別名的詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。