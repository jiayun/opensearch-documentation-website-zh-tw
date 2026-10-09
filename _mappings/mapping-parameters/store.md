---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儲存"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/store/
nav_order: 260
has_children: false
has_toc: false
---

# Store 對應參數

`store` 對應參數決定是否將欄位值與 `_source` 分開儲存，並讓您可使用搜尋請求中的 `stored_fields` 選項直接擷取該值。

預設情況下，`store` 設為 `false`，表示欄位值不會個別儲存，只能作為文件 `_source` 的一部分存取。如果將 `store` 設為 `true`，您可以停用 `_source` 以節省磁碟空間，同時仍可[擷取特定欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/)。

## 範例：在欄位上啟用 `store`

下列請求會建立名為 `products` 的索引，其中 `model` 欄位會與 `_source` 分開儲存：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "model": {
        "type": "keyword",
        "store": true
      },
      "name": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將文件匯入索引：

```json
PUT /products/_doc/1
{
  "model": "WM-1001",
  "name": "Wireless Mouse"
}
```
{% include copy-curl.html %}

僅擷取已儲存的欄位：

```json
POST /products/_search
{
  "query": {
    "match": {
      "name": "Mouse"
    }
  },
  "stored_fields": ["model"]
}
```
{% include copy-curl.html %}

此查詢會傳回分開儲存的 `model` 欄位，即使 `_source` 仍可存取。

---

## 範例：在停用 `_source` 的情況下儲存欄位

如果您想節省磁碟空間，且之後不需要存取完整的原始文件（例如，用於重新編製索引或更新），可以停用 `_source`，只儲存必要的欄位：

```json
PUT /products_no_source
{
  "mappings": {
    "_source": {
      "enabled": false
    },
    "properties": {
      "model": {
        "type": "keyword",
        "store": true
      },
      "name": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將文件匯入索引：

```json
PUT /products_no_source/_doc/1
{
  "model": "KB-2002",
  "name": "Mechanical Keyboard"
}
```
{% include copy-curl.html %}

擷取已儲存的欄位：

```json
POST /products_no_source/_search
{
  "query": {
    "match": {
      "name": "Keyboard"
    }
  },
  "stored_fields": ["model"]
}
```
{% include copy-curl.html %}

此查詢會傳回從 `stored_fields` 擷取的 `model` 欄位，且不會存取 `_source`。

如果您嘗試以下列方式擷取 `_source`：

```json
GET /products_no_source/_doc/1
```

則回應中的 `_source` 會是 `null`。這表示完整文件已無法存取，且由於 `_source` 已停用，因此只能擷取已儲存的欄位：

```json
{
  "_index": "products_no_source",
  "_id": "1",
  "found": true,
  "_source": null
}
```
