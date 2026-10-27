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

`collapse` 參數會依特定欄位值將搜尋結果分組。這只會傳回各組中最頂端的文件，藉由移除重複項目來協助減少冗餘。

`collapse` 參數要求要收合的欄位必須是 `keyword` 或 `numeric` 類型、已啟用 [doc values]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)，且每份文件只包含單一值。若任何相符文件在該欄位包含多個值，OpenSearch 會拒絕收合搜尋。

您無法在 [scroll]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search) 搜尋中使用 `collapse`，也無法將其與 [`rescore`]({{site.url}}{{site.baseurl}}/query-dsl/rescore/) 一起使用。OpenSearch 會拒絕這些請求。若要分頁瀏覽收合後的結果，請使用 [`search_after`](#collapse-with-search_after)。
{: .note}

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
      "value": 3,
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
          "baked_date": "2023-07-02T00:00:00Z"
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
          "baked_date": "2023-07-01T00:00:00Z"
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

`collapse` 參數只會影響最頂端的搜尋結果，不會變更任何彙總結果。回應中顯示的命中總數反映套用參數前的所有相符文件，包括重複項目。不過，回應並不會指出此操作所形成的不重複群組的確切數量。

---

## 搭配 search_after 收合

`from` 和 `size` 參數會套用至收合後的群組，因此您可以使用這兩個參數逐頁瀏覽群組。例如，將 `from` 設為 `1`、`size` 設為 `2` 時，搜尋會略過第一個群組，並傳回第二個和第三個群組。您也可以使用 `search_after` 參數對收合後的搜尋結果進行分頁。收合欄位與排序欄位必須相同，且只能指定一個排序欄位。

以下範例說明如何搭配 `search_after` 使用 `collapse`：

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

## 展開收合結果

您可以使用 `inner_hits` 屬性展開每個收合後的最頂端命中。關於您可以在 `inner_hits` 中指定的所有選項，請參閱 [內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

下列範例請求套用 `inner_hits`，為每種蛋糕分別擷取價格最低的品項與最新的品項：

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

### 每個收合結果的多個內部命中

若要為每個收合的結果取得多組內部命中，您可以為每個群組設定不同的條件。例如，假設要為每個烘焙品項要求三個最新的項目：

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

此查詢會搜尋 `cakes` 類別中的文件，並依 `item_name` 欄位將搜尋結果分組。對於每個 `item_name`，它會擷取價格最低的三個項目以及最新的三個項目，並依 `baked_date` 遞減排序。

您可以針對回應中每個收合命中對應的每個內部命中請求，傳送額外的查詢來展開這些群組。如果群組或內部命中請求太多，這可能會大幅拖慢處理速度。您可以使用 `max_concurrent_group_searches` 請求參數來控制此階段允許的最大並行搜尋數。預設值取決於資料節點數量和預設搜尋執行緒集區大小。

### 第二層收合

您也可以在 `inner_hits` 中指定 `collapse` 物件，對每個群組的內部命中再做收合。這會傳回兩個欄位每種組合中最頂端的文件。為了示範，請在 `bakery-items` 索引中加入兩種餅乾：

```json
POST /bakery-items/_bulk?refresh=true
{ "index": {} }
{ "item": "Oatmeal Cookie", "category": "cookies", "price": 3, "baked_date": "2023-07-03T00:00:00Z" }
{ "index": {} }
{ "item": "Oatmeal Cookie", "category": "cookies", "price": 4, "baked_date": "2023-07-05T00:00:00Z" }
{ "index": {} }
{ "item": "Sugar Cookie", "category": "cookies", "price": 2, "baked_date": "2023-07-05T00:00:00Z" }
```
{% include copy-curl.html %}

下列請求會依 `category` 收合結果，並在每個類別內依 `item` 收合內部命中。因此，每個類別都會包含其中每個項目最便宜的文件：

```json
GET /bakery-items/_search
{
  "_source": ["item", "price"],
  "sort": ["price"],
  "collapse": {
    "field": "category",
    "inner_hits": {
      "name": "cheapest_per_item",
      "size": 3,
      "_source": ["item", "price"],
      "sort": ["price"],
      "collapse": {
        "field": "item"
      }
    }
  }
}
```
{% include copy-curl.html %}

在回應中，`cookies` 群組包含每種餅乾各一份文件，`cakes` 群組包含每種蛋糕各一份文件。較貴的 `Oatmeal Cookie` 與 `Chocolate Cake` 文件則被省略：

```json
{
  ...
  "hits": {
    ...
    "hits": [
      {
        ...
        "_source": {
          "item": "Sugar Cookie",
          "price": 2
        },
        "fields": {
          "category": [
            "cookies"
          ]
        },
        "inner_hits": {
          "cheapest_per_item": {
            "hits": {
              ...
              "hits": [
                {
                  ...
                  "_source": {
                    "item": "Sugar Cookie",
                    "price": 2
                  },
                  "fields": {
                    "item": [
                      "Sugar Cookie"
                    ]
                  }
                },
                {
                  ...
                  "_source": {
                    "item": "Oatmeal Cookie",
                    "price": 3
                  },
                  "fields": {
                    "item": [
                      "Oatmeal Cookie"
                    ]
                  }
                }
              ]
            }
          }
        }
      },
      {
        ...
        "_source": {
          "item": "Vanilla Cake",
          "price": 12
        },
        "fields": {
          "category": [
            "cakes"
          ]
        },
        "inner_hits": {
          "cheapest_per_item": {
            "hits": {
              ...
              "hits": [
                {
                  ...
                  "_source": {
                    "item": "Vanilla Cake",
                    "price": 12
                  },
                  "fields": {
                    "item": [
                      "Vanilla Cake"
                    ]
                  }
                },
                {
                  ...
                  "_source": {
                    "item": "Chocolate Cake",
                    "price": 15
                  },
                  "fields": {
                    "item": [
                      "Chocolate Cake"
                    ]
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

第二層的 `collapse` 物件不能包含 `inner_hits`，因此您無法在超過兩個層級上收合結果。
