---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼查詢"
parent: Specialized queries
nav_order: 58
---

# 指令碼查詢

使用 `script` 查詢，根據以 Painless 指令碼語言撰寫的自訂條件來篩選文件。此查詢會傳回指令碼評估結果為 `true` 的文件，從而實現無法以標準查詢表達的進階篩選邏輯。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

`script` 查詢的運算成本高昂，應謹慎使用。僅在必要時使用，並確保已啟用 `search.allow_expensive_queries`（預設為 `true`）。如需更多資訊，請參閱 [高成本查詢]({{site.url}}{{site.baseurl}}/query-dsl/#expensive-queries)。
{: .important }

## 範例

使用下列對應建立名為 `products` 的索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "price": { "type": "float" },
      "rating": { "type": "float" }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求為範例文件編製索引：

```json
POST /products/_bulk
{ "index": { "_id": 1 } }
{ "title": "Wireless Earbuds", "price": 99.99, "rating": 4.5 }
{ "index": { "_id": 2 } }
{ "title": "Bluetooth Speaker", "price": 79.99, "rating": 4.8 }
{ "index": { "_id": 3 } }
{ "title": "Noise Cancelling Headphones", "price": 199.99, "rating": 4.7 }
```
{% include copy-curl.html %}

## 基本指令碼查詢

傳回評等高於 `4.6` 的產品：

```json
POST /products/_search
{
  "query": {
    "script": {
      "script": {
        "source": "doc['rating'].value > 4.6"
      }
    }
  }
}
```
{% include copy-curl.html %}

傳回的命中結果僅包含 `rating` 高於 `4.6` 的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Bluetooth Speaker",
          "price": 79.99,
          "rating": 4.8
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 1,
        "_source": {
          "title": "Noise Cancelling Headphones",
          "price": 199.99,
          "rating": 4.7
        }
      }
    ]
  }
}
```

## 參數

`script` 查詢接受下列頂層參數。

| 參數       | 必要/選用 | 說明                                           |
| --------------- | ----------------- | ----------------------------------------------------- |
| `script.source` | 必要          | 評估結果為 `true` 或 `false` 的指令碼程式碼。  |
| `script.params` | 選用          | 在指令碼內參照的使用者自訂參數。 |

## 使用指令碼參數

您可以使用 `params` 安全地注入值，並利用指令碼編譯快取：

```json
POST /products/_search
{
  "query": {
    "script": {
      "script": {
        "source": "doc['price'].value < params.max_price",
        "params": {
          "max_price": 100
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

傳回的命中結果僅包含 `price` 低於 `100` 的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "title": "Wireless Earbuds",
          "price": 99.99,
          "rating": 4.5
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Bluetooth Speaker",
          "price": 79.99,
          "rating": 4.8
        }
      }
    ]
  }
}
```

## 結合多個條件

使用下列查詢搜尋 `rating` 高於 `4.5` 且 `price` 低於 `100` 的產品：

```json
POST /products/_search
{
  "query": {
    "script": {
      "script": {
        "source": "doc['rating'].value > 4.5 && doc['price'].value < 100"
      }
    }
  }
}
```
{% include copy-curl.html %}

僅會傳回符合條件的文件：

```json
{
  "took": 12,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Bluetooth Speaker",
          "price": 79.99,
          "rating": 4.8
        }
      }
    ]
  }
}
```
