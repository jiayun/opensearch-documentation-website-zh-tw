---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位名稱"
parent: Metadata fields
nav_order: 10
redirect_from:
  - /field-types/metadata-fields/field-names/
---

# 欄位名稱中繼資料欄位

`_field_names` 欄位會將包含非 null 值的欄位名稱編製索引。這讓您能夠使用 `exists` 查詢，該查詢可識別指定欄位具有或不具有非 null 值的文件。

然而，只有在 `doc_values` 與 `norms` 皆停用時，`_field_names` 才會將欄位名稱編製索引。若啟用了 `doc_values` 或 `norms`，則 `exists` 查詢仍可運作，但不會依賴 `_field_names` 欄位。

## 對應範例

```json
{
    "mappings": {
       "_field_names": {
        "enabled": "true"
      },
    "properties": {
      },
      "title": {
        "type": "text",
        "doc_values": false,
        "norms": false
      },
      "description": {
        "type": "text",
        "doc_values": true,
        "norms": false
      },
      "price": {
        "type": "float",
        "doc_values": false,
        "norms": true
      }
    }
  }
}
```
{% include copy-curl.html %}
