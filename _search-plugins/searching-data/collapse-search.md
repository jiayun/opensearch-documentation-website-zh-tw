---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "收合搜尋結果"
parent: Customizing search results
nav_order: 40
redirect_from:
  - /search-plugins/collapse-search/
---

# 收合搜尋結果

`collapse` 參數會依特定欄位值將搜尋結果分組。這只會傳回每個群組中最頂端的文件，藉由移除重複項目來協助減少冗餘。

`collapse` 參數要求被收合的欄位必須是 `keyword` 或 `numeric` 類型。

---

## 收合搜尋結果

若要將資料填入索引，請定義索引對應，以及一個索引為 `keyword` 的 `item` 欄位。下列範例請求說明如何定義索引對應、填入索引，然後搜尋該索引。

#### 定義索引對應

```json
PUT /bakery-items
{
  "mappings": {
    "properties": {
      "item": {
        "type": "keyword"
      },
      "category": {
        "type": "keyword"
      },
      "price": {
        "type": "float"
      },
      "baked_date": {
        "type": "date"
      }
    }
  }
}
```

#### 填入索引

```json
POST /bakery-items/_bulk
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 15, "baked_date": "2023-07-01T00:00:00Z" }
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 18, "baked_date": "2023-07-04T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 12, "baked_date": "2023-07-02T00:00:00Z" }
```

#### 搜尋索引，傳回所有結果

```json
GET /bakery-items/_search
{
  "query": {
    "match": {
      "category": "cakes"
    }
  },
  "sort": ["price"]
}
```

此查詢會傳回未收合的搜尋結果，顯示所有文件，包括「Chocolate Cake」的兩個項目。

#### 搜尋索引並收合結果

若要依 `item` 欄位將搜尋結果分組，並依 `price` 排序，您可以使用下列查詢：

**收合後的 `item` 欄位搜尋結果**

```json
GET /bakery-items/_search
{
  "query": {
    "match": {
      "category": "cakes"
    }
  },
  "collapse": {
    "field": "item"
  },
  "sort": ["price"]
}
```

**回應**

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "bakery-items",
        "_id": "mISga5EB2HLDXHkv9kAr",
        "_score": null,
        "_source": {
          "item": "Vanilla Cake",
          "category": "cakes",
          "price": 12,
          "baked_date": "2023-07-02T00:00:00Z",
          "baker": "Baker A"
        },
        "fields": {
          "item": [
            "Vanilla Cake"
          ]
        },
        "sort": [
          12
        ]
      },
      {
        "_index": "bakery-items",
        "_id": "loSga5EB2HLDXHkv9kAr",
        "_score": null,
        "_source": {
          "item": "Chocolate Cake",
          "category": "cakes",
          "price": 15,
          "baked_date": "2023-07-01T00:00:00Z",
          "baker": "Baker A"
        },
        "fields": {
          "item": [
            "Chocolate Cake"
          ]
        },
        "sort": [
          15
        ]
      }
    ]
  }
}
```

收合後的搜尋結果只會顯示一個「Chocolate Cake」項目，示範 `collapse` 參數如何減少冗餘。

`collapse` 參數只會影響最頂端的搜尋結果，不會變更任何彙總結果。回應中顯示的命中總數反映套用參數前的所有相符文件，包括重複項目。不過，回應並不會指出此操作所形成之唯一群組的確切數量。

---

## 搭配 search_after 收合

您可以使用 `search_after` 參數，為收合後的搜尋結果分頁。收合的欄位與排序欄位必須相同，且只能指定一個排序欄位。

下列範例說明如何搭配 `search_after` 使用 `collapse`：

```json
GET /bakery-items/_search
{
  "query": {
    "match": {
      "category": "cakes"
    }
  },
  "collapse": {
    "field": "item"
  },
  "sort": [
    {
      "item": "asc"
    }
  ],
  "search_after": ["Chocolate Cake"]
}
```
{% include copy-curl.html %}

## 展開收合後的結果

您可以使用 `inner_hits` 屬性展開每個收合後的最頂端命中。

下列範例請求會套用 `inner_hits`，為每種蛋糕分別擷取價格最低的項目和最新的項目：

```json
GET /bakery-items/_search
{
  "query": {
    "match": {
      "category": "cakes"
    }
  },
  "collapse": {
    "field": "item",
    "inner_hits": [
      {
        "name": "cheapest_items",
        "size": 1,
        "sort": ["price"]
      },
      {
        "name": "newest_items",
        "size": 1,
        "sort": [{ "baked_date": "desc" }]
      }
    ]
  },
  "sort": ["price"]
}

```

### 為每個收合後的命中取得多個內部命中

若要為每個收合後的結果取得多組內部命中，您可以為每個群組設定不同的準則。例如，讓我們為每個烘焙項目要求三個最新的項目：

```json
GET /bakery-items/_search
{
  "query": {
    "match": {
      "category": "cakes"
    }
  },
  "collapse": {
    "field": "item",
    "inner_hits": [
      {
        "name": "cheapest_items",
        "size": 1,
        "sort": ["price"]
      },
      {
        "name": "newest_items",
        "size": 3,
        "sort": [{ "baked_date": "desc" }]
      }
    ]
  },
  "sort": ["price"]
}
```

此查詢會搜尋 `cakes` 類別中的文件，並依 `item_name` 欄位將搜尋結果分組。針對每個 `item_name`，它會擷取三個價格最低的項目，以及三個最新的項目，並依 `baked_date` 遞減排序。

您可以為回應中每個收合後命中對應的每個內部命中請求，傳送額外的查詢來展開群組。如果群組或內部命中請求太多，這可能會大幅拖慢處理程序。您可以使用 `max_concurrent_group_searches` 請求參數，控制此階段允許的最大並行搜尋數。預設值取決於資料節點數目，以及預設搜尋執行緒集區大小。
