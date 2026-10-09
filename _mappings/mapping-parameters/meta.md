---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Meta
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/meta/
nav_order: 180
has_children: false
has_toc: false
---

# Meta 對應參數

`_meta` 對應參數可讓您將中繼資料附加至對應定義。此中繼資料會與對應一併儲存，並在擷取對應時一併回傳，僅作為資訊性內容，不會影響編製索引或搜尋作業。

您可以使用 `_meta` 對應參數提供重要細節，例如版本資訊、描述或作者資訊。中繼資料也可以透過提交會覆寫現有中繼資料的對應更新來更新。


## 在對應上啟用 meta

下列請求會建立名為 `products` 的索引，其中包含含有版本與描述資訊的 `_meta` 對應參數：

```json
PUT /products
{
  "mappings": {
    "_meta": {
      "version": "1.0",
      "description": "Mapping for the products index."
    },
    "properties": {
      "name": {
        "type": "text"
      },
      "price": {
        "type": "float"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 更新索引上的中繼資料

使用下列請求來更新索引上的 `_meta` 對應參數：

```json
PUT /products/_mapping
{
  "_meta": {
    "version": "1.1",
    "description": "Updated mapping for the products index.",
    "author": "Team B"
  }
}
```
{% include copy-curl.html %}

### 編製文件索引

建立索引後，您可以照常將文件編製索引。`_meta` 資訊會保留在對應中，且不會影響文件編製索引的程序：

```json
PUT /products/_doc/1
{
  "name": "Widget",
  "price": 19.99
}
```
{% include copy-curl.html %}

### 擷取 meta 資訊

若要驗證 `_meta` 資訊是否已儲存，您可以擷取該索引的對應：

```json
GET /products/_mapping
```
{% include copy-curl.html %}
