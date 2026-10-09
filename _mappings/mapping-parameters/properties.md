---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "屬性"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/properties/
nav_order: 230
has_children: false
has_toc: false
---

# Properties 對應參數

`properties` 對應參數用於定義物件內或文件根層級之欄位的結構與資料類型。它是任何對應定義的核心，可讓您明確指定欄位名稱、類型（例如 `text`、`keyword`、`date` 或 `float`），以及每個欄位的其他設定或對應參數。

使用 `properties` 後，您就能完全掌控資料的編製索引與儲存方式，實現精確的搜尋行為、彙總支援與資料驗證。

## 使用 properties 定義欄位

下列請求會建立名為 `products` 的索引，並使用 `properties` 參數建立結構化對應。其中包含一個名為 `dimensions` 的巢狀物件欄位，並帶有下列子欄位：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "sku": {
        "type": "keyword"
      },
      "price": {
        "type": "float"
      },
      "available": {
        "type": "boolean"
      },
      "created_at": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "dimensions": {
        "type": "object",
        "properties": {
          "width": { "type": "float" },
          "height": { "type": "float" },
          "depth": { "type": "float" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 將文件編製索引

使用下列命令，將含有[巢狀欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)的文件編製索引：

```json
PUT /products/_doc/1
{
  "name": "Wireless Mouse",
  "sku": "WM-1001",
  "price": 24.99,
  "available": true,
  "created_at": "2024-12-01",
  "dimensions": {
    "width": 6.5,
    "height": 3.2,
    "depth": 1.5
  }
}
```
{% include copy-curl.html %}

## 使用點記法查詢與彙總

您可以使用點記法查詢或彙總物件的子欄位。使用下列命令執行查詢，該查詢會：

- 依 `dimensions.width` 欄位篩選文件，傳回 `width` 介於 `5` 與 `10` 之間的文件。
- 在 `dimensions.depth` 欄位上建立[直方圖彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/)，以 `0.5` 的 `depth` 間隔為產品建立桶 (bucket)。

```json
POST /products/_search
{
  "query": {
    "range": {
      "dimensions.width": {
        "gte": 5,
        "lte": 10
      }
    }
  },
  "aggs": {
    "Depth Distribution": {
      "histogram": {
        "field": "dimensions.depth",
        "interval": 0.5
      }
    }
  }
}
```
{% include copy-curl.html %}

下列回應顯示一筆符合的文件，其中 `dimensions.width` 欄位落在指定的範圍內。它也包含 `dimensions.depth` 的直方圖彙總結果：

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
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Wireless Mouse",
          "sku": "WM-1001",
          "price": 24.99,
          "available": true,
          "created_at": "2024-12-01",
          "dimensions": {
            "width": 6.5,
            "height": 3.2,
            "depth": 1.5
          }
        }
      }
    ]
  },
  "aggregations": {
    "Depth Distribution": {
      "buckets": [
        {
          "key": 1.5,
          "doc_count": 1
        }
      ]
    }
  }
}
```
