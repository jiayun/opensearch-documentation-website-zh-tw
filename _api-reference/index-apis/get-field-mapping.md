---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得欄位對應"
parent: Index settings and mappings
grand_parent: Index APIs
nav_order: 25
---

# Get Field Mapping API
**於 1.0 版推出**
{: .label .label-purple }

Get Field Mapping API 可擷取一或多個特定欄位的對應定義。當您需要檢查特定欄位的設定方式，而不擷取完整的索引對應時，此 API 非常實用，尤其適用於包含許多欄位的索引。

## 端點

```json
GET /_mapping/field/{field}
GET /{index}/_mapping/field/{field}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | 選用 | 字串 | 以逗號分隔的索引名稱或萬用字元運算式清單。使用 `_all` 或省略此參數，即可指定所有索引。 |
| `field` | 必要 | 字串 | 以逗號分隔的欄位名稱或萬用字元運算式清單。巢狀欄位請使用點號表示法（例如，`author.name`）。 |

## 查詢參數

下表列出可用的查詢參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `include_defaults` | 選用 | 布林值 | 設為 `true` 時，回應會包含通常省略的預設對應參數值。預設為 `false`。 |
| `allow_no_indices` | 選用 | 布林值 | 設為 `true` 時，若萬用字元運算式或 `_all` 未解析出任何索引，請求不會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 選用 | 字串 | 控制萬用字元運算式展開後涵蓋的索引類型。有效值為 `open`、`closed`、`hidden`、`none`、`all`。預設為 `open`。 |
| `ignore_unavailable` | 選用 | 布林值 | 設為 `true` 時，會忽略不存在或已關閉的索引，而不傳回錯誤。預設為 `false`。 |

## 請求範例

下列請求會擷取 `customer_gender` 欄位的對應：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_mapping/field/customer_gender
```
{% include copy-curl.html %}

## 回應範例

回應包含欄位的完整名稱及其對應組態：

```json
{
  "opensearch_dashboards_sample_data_ecommerce" : {
    "mappings" : {
      "customer_gender" : {
        "full_name" : "customer_gender",
        "mapping" : {
          "customer_gender" : {
            "type" : "keyword"
          }
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `{index}.mappings` | 物件 | 指定索引中，欄位名稱與其對應詳細資訊之間的對照表。 |
| `{field}.full_name` | 字串 | 完整限定的欄位名稱，包含任何父物件路徑。 |
| `{field}.mapping` | 物件 | 欄位的對應組態，包含其類型及任何參數。 |
