---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引"
parent: Metadata fields
nav_order: 40
redirect_from:
  - /field-types/metadata-fields/index-metadata/
---

# 索引中繼資料欄位

在跨多個索引進行查詢時，您可能需要根據文件被編製索引的索引來篩選結果。`index` 欄位會依據文件所在的索引來比對文件。

下列範例請求會建立兩個索引 `products` 和 `customers`，並分別在每個索引中新增一份文件。

第一個請求會在 `products` 索引中新增一份文件：

```json
PUT products/_doc/1
{
  "name": "Widget X"
}
```
{% include copy-curl.html %}

第二個請求會在 `customers` 索引中新增一份文件：

```json
PUT customers/_doc/2
{
  "name": "John Doe"
}
```
{% include copy-curl.html %}

接著您可以使用 `_index` 欄位查詢這兩個索引並篩選結果，如下列範例請求所示：

```json
GET products,customers/_search
{
  "query": {
    "terms": {
      "_index": ["products", "customers"]
    }
  },
  "aggs": {
    "index_groups": {
      "terms": {
        "field": "_index",
        "size": 10
      }
    }
  },
  "sort": [
    {
      "_index": {
        "order": "desc"
      }
    }
  ],
  "script_fields": {
    "index_name": {
      "script": {
        "lang": "painless",
        "source": "doc['_index'].value"
      }
    }
  }
}
```
{% include copy-curl.html %}

在此範例中：

- `query` 區段使用 `terms` 查詢來比對來自 `products` 和 `customers` 索引的文件。
- `aggs` 區段對 `_index` 欄位執行 `terms` 彙總，並依索引將結果分組。
- `sort` 區段依 `_index` 欄位以遞增順序排序結果。
- `script_fields` 區段在搜尋結果中新增名為 `index_name` 的新欄位，其中包含每份文件的 `_index` 欄位值。

## 在 `_index` 欄位上進行查詢

`_index` 欄位代表文件被編製索引的索引。您可以在查詢中使用此欄位，以篩選、彙總、排序或擷取搜尋結果的索引資訊。

由於 `_index` 欄位會自動新增至每份文件，您可以像使用其他欄位一樣在查詢中使用它。例如，您可以使用 `terms` 查詢來比對來自多個索引的文件。下列範例查詢會傳回 `products` 和 `customers` 索引中的所有文件：

```json
 {
  "query": {
    "terms": {
      "_index": ["products", "customers"]
    }
  }
}
```
{% include copy-curl.html %}
