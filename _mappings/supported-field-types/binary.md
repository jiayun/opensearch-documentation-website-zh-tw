---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "二進位"
nav_order: 20
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/binary/
  - /opensearch/supported-field-types/binary/
  - /field-types/binary/
---

# 二進位欄位類型
**於 1.0 版導入**
{: .label .label-purple }

二進位欄位類型包含以 [Base64](https://en.wikipedia.org/wiki/Base64) 編碼的二進位值，且無法進行搜尋。

## 範例

建立包含 binary 欄位的對應：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "binary_value" : {
        "type" : "binary"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有二進位值的文件編製索引：

```json
PUT testindex/_doc/1 
{
  "binary_value" : "bGlkaHQtd29rfx4="
}
```
{% include copy-curl.html %}

使用 `=` 作為填充字元。不允許內嵌換行字元。
{: .note }

## 參數

下表列出 binary 欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`doc_values` | 布林值，指定是否應將此欄位儲存在磁碟上，以便用於彙總、排序或指令碼。選用。預設為 `false`。
`store` | 布林值，指定是否應儲存欄位值，並可從 `_source` 欄位個別擷取。選用。預設為 `false`。
