---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Constant keyword
nav_order: 30
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/constant-keyword/
---

# Constant keyword 欄位類型
**自 2.14 版起推出**
{: .label .label-purple }

Constant keyword 欄位對索引中的所有文件使用相同的值。

當搜尋請求橫跨多個索引時，您可以依 constant keyword 欄位進行篩選，以比對來自具有指定常數值之索引的文件，而不比對來自具有不同值之索引的文件。

## 範例

下列查詢會建立含有 constant keyword 欄位的對應：

```json
PUT romcom_movies
{
  "mappings" : {
    "properties" : {
      "genre" : {
        "type": "constant_keyword",
        "value" : "Romantic comedy"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出 constant keyword 欄位類型接受的參數。所有值皆為必要。

參數 | 說明
:--- | :---
`value` | 索引中所有文件的字串欄位值。

