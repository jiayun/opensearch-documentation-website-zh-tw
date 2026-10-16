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

`store` 對應參數決定是否將欄位值與 `_source` 分開儲存，並讓您能夠使用搜尋請求中的 `stored_fields` 選項直接擷取該值。

預設情況下，`store` 設為 `false`，表示欄位值不會個別儲存，只能作為文件 `_source` 的一部分取得。如果將 `store` 設為 `true`，您可以停用 `_source` 以節省磁碟空間，同時仍可[擷取特定欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/)。

在大多數情況下，您不需要儲存欄位。若要僅傳回文件的部分欄位，請使用[來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)，從 `_source` 擷取所要求的欄位。在下列情況下，儲存欄位很有用：

- 文件包含非常大的欄位，例如文章全文，而搜尋僅傳回幾個小欄位，例如標題和發佈日期。讀取已儲存的欄位可避免為每筆命中結果載入並剖析龐大的 `_source`。
- `_source` 欄位已停用，而您需要擷取某些欄位值。
- 欄位未出現在 `_source` 中，例如由 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 填入的欄位。

OpenSearch 會在每筆命中結果的 `fields` 物件中傳回已儲存的欄位值。即使原始文件只包含單一值，也一律以陣列形式傳回值，因為已儲存的欄位不會記錄原始值是單一值還是陣列。若要取得原始形式的值，請從 `_source` 擷取。

您無法變更現有欄位的 `store` 設定。

## 範例：在欄位上啟用 store

下列請求會建立一個名為 `products` 的索引，其中 `model` 欄位會與 `_source` 分開儲存：

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
PUT /products/_doc/1?refresh=true
{
  "model": "WM-1001",
  "name": "Wireless Mouse"
}
```
{% include copy-curl.html %}

僅擷取已儲存的欄位：

```json
GET /products/_search
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

回應會在 `fields` 物件中包含 `model` 值。當您指定 `stored_fields` 時，除非您也在請求中設定 `"_source": true`，否則 OpenSearch 不會傳回 `_source`。未儲存的欄位（例如 `name`）若您在 `stored_fields` 中請求，也不會被傳回：

```json
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.13076457,
        "fields": {
          "model": [
            "WM-1001"
          ]
        }
      }
    ]
  }
}
```

## 範例：在索引中儲存欄位而不儲存 _source

如果您想節省磁碟空間，且之後不需要存取完整原始文件（例如用於重新編製索引或更新），可以停用 `_source`，只儲存必要的欄位：

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
PUT /products_no_source/_doc/1?refresh=true
{
  "model": "KB-2002",
  "name": "Mechanical Keyboard"
}
```
{% include copy-curl.html %}

擷取已儲存的欄位：

```json
GET /products_no_source/_search
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

回應會包含已儲存的 `model` 值，即使索引並未儲存 `_source`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "products_no_source",
        "_id": "1",
        "_score": 0.13076457,
        "fields": {
          "model": [
            "KB-2002"
          ]
        }
      }
    ]
  }
}
```

使用 Get Document API 擷取文件：

```json
GET /products_no_source/_doc/1
```
{% include copy-curl.html %}

回應不包含 `_source`，因為該索引已停用 `_source`：

```json
{
  "_index": "products_no_source",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true
}
```

## 範例：儲存複製的欄位

由 `copy_to` 填入的欄位會被編製索引，但不會加入 `_source`。若要擷取其值，請儲存這些欄位。下列請求會建立一個索引，將 `first_name` 與 `last_name` 欄位複製到已儲存的 `full_name` 欄位：

```json
PUT /store-copy-to
{
  "mappings": {
    "properties": {
      "first_name": {
        "type": "text",
        "copy_to": "full_name"
      },
      "last_name": {
        "type": "text",
        "copy_to": "full_name"
      },
      "full_name": {
        "type": "text",
        "store": true
      }
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引到該索引：

```json
PUT /store-copy-to/_doc/1?refresh=true
{
  "first_name": "Ana",
  "last_name": "Rivera"
}
```
{% include copy-curl.html %}

擷取已儲存的 `full_name` 欄位：

```json
GET /store-copy-to/_search
{
  "stored_fields": ["full_name"]
}
```
{% include copy-curl.html %}

`full_name` 欄位包含兩個複製的值：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "store-copy-to",
        "_id": "1",
        "_score": 1,
        "fields": {
          "full_name": [
            "Ana",
            "Rivera"
          ]
        }
      }
    ]
  }
}
```
