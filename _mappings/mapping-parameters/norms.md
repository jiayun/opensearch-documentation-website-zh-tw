---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Norms
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/norms/
nav_order: 200
has_children: false
has_toc: false
---

# Norms 對應參數

`norms` 對應參數控制是否為欄位計算並儲存正規化因子。這些因子會在查詢評分時用於調整搜尋結果的相關性。然而，儲存 `norms` 會增加索引大小並消耗額外的記憶體。

預設情況下，`norms` 在 `text` 欄位上是啟用的，因為這類欄位的相關性評分非常重要。不需要這些評分功能的欄位，例如僅用於篩選的 `keyword` 欄位，則設定為停用 `norms`。

## 在欄位上停用 `norms`

下列請求會建立一個名為 `products` 的索引，其中 `description` 欄位為 `text` 欄位並停用 `norms`：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "norms": false
      }
    }
  }
}
```
{% include copy-curl.html %}

若要在現有索引的欄位上停用 `norms`，請使用下列請求：

```json
PUT /products/_mapping
{
  "properties": {
    "review": {
      "type": "text",
      "norms": false
    }
  }
}
```
{% include copy-curl.html %}

在已停用 `norms` 的欄位上啟用 `norms` 是不可能的，並會導致下列錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Mapper for [description] conflicts with existing mapper:\n\tCannot update parameter [norms] from [false] to [true]"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "Mapper for [description] conflicts with existing mapper:\n\tCannot update parameter [norms] from [false] to [true]"
  },
  "status": 400
}
```