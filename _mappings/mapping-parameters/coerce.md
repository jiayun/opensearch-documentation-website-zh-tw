---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Coerce
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/coerce/
nav_order: 15
has_children: false
has_toc: false
---

# Coerce 對應參數

`coerce` 對應參數可控制 OpenSearch 在編製索引期間是否嘗試將值正規化並轉換，以符合欄位的資料類型。

資料不一定總是一致。視產生方式而定，數字可能呈現為真正的 JSON 數字，例如 10，但也可能呈現為字串，例如 "10"。同樣地，應該是整數的數字可能呈現為浮點數，例如 10.0，甚至呈現為字串，例如 "10.0"。

強制轉型會嘗試轉換這些不一致之處，以符合欄位的資料類型：

- **字串會強制轉型為數字**：`"10"` 會變成 `10`。
- **浮點數會以截斷方式強制轉型為整數**：`10.0` 會變成 `10`。

`coerce` 參數可使用 Update Mapping API 在現有欄位上更新。
{: .tip}

## 範例

下列範例示範如何使用 `coerce` 對應參數。

### 欄位層級的強制轉型

建立具有不同強制轉型設定的索引以進行比較。強制轉型預設為啟用：

```json
PUT /data_quality_demo
{
  "mappings": {
    "properties": {
      "price_with_coercion": {
        "type": "integer"
      },
      "price_without_coercion": {
        "type": "integer",
        "coerce": false
      }
    }
  }
}
```
{% include copy-curl.html %}

在啟用強制轉型的情況下將文件編製索引：

```json
PUT /data_quality_demo/_doc/1
{
  "price_with_coercion": "10"
}
```
{% include copy-curl.html %}

為了符合整數欄位類型，字串 `"10"` 已成功轉換為整數 `10`。

嘗試在停用強制轉型的情況下將文件編製索引：

```json
PUT /data_quality_demo/_doc/2
{
  "price_without_coercion": "10"
}
```
{% include copy-curl.html %}

此文件遭到拒絕，因為強制轉型已停用，且字串 `"10"` 不符合預期的整數類型。

### 索引層級的強制轉型設定

您可以為整個索引設定預設的強制轉型原則，如下所示：

```json
PUT /strict_data_index
{
  "settings": {
    "index.mapping.coerce": false
  },
  "mappings": {
    "properties": {
      "flexible_field": {
        "type": "integer",
        "coerce": true
      },
      "strict_field": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含 `flexible_field` 的文件編製索引：

```json
PUT /strict_data_index/_doc/1
{
  "flexible_field": "10"
}
```
{% include copy-curl.html %}

`flexible_field` 會覆寫索引層級的設定並啟用強制轉型，因此字串 `"10"` 會成功轉換為整數 `10`。

將另一個包含 `strict_field` 的文件編製索引：

```json
PUT /strict_data_index/_doc/2
{
  "strict_field": "10"
}
```
{% include copy-curl.html %}

此文件遭到拒絕，因為 `strict_field` 會繼承索引層級的強制轉型設定 (`false`)，且字串 `"10"` 在沒有強制轉型的情況下無法儲存於整數欄位中。
