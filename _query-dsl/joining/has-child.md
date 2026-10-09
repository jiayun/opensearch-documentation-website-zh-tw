---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Has child 查詢"
parent: Joining queries
nav_order: 10
---

# Has child 查詢

`has_child` 查詢會傳回子文件符合特定查詢的父文件。您可以使用 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型，在同一索引中的文件之間建立父子關係。

`has_child` 查詢因為會執行 join 操作，所以比其他查詢慢。指向不同父文件的相符子文件數量增加時，效能會下降。搜尋中的每個 `has_child` 查詢都可能對查詢效能造成顯著影響。如果您重視速度，請避免使用此查詢，或盡量限制其使用。
{: .warning}

## 範例 

在您執行 `has_child` 查詢之前，您的索引必須包含 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位，才能建立父子關係。索引對應請求使用下列格式：

```json
PUT /example_index
{
  "mappings": {
    "properties": {
      "relationship_field": {
        "type": "join",
        "relations": {
          "parent_doc": "child_doc"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，您將設定一個索引，其中包含代表產品及其品牌的文件。 

首先，建立索引並在 `brand` 與 `product` 之間建立父子關係：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "product_to_brand": { 
        "type": "join",
        "relations": {
          "brand": "product" 
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將兩個父文件 (品牌) 編製索引：

```json
PUT testindex1/_doc/1
{
  "name": "Luxury brand",
  "product_to_brand" : "brand" 
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "name": "Economy brand",
  "product_to_brand" : "brand" 
}
```
{% include copy-curl.html %}

將三個子文件 (產品) 編製索引：

```json
PUT testindex1/_doc/3?routing=1
{
  "name": "Mechanical watch",
  "sales_count": 150,
  "product_to_brand": {
    "name": "product", 
    "parent": "1" 
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/4?routing=2
{
  "name": "Electronic watch",
  "sales_count": 300,
  "product_to_brand": {
    "name": "product", 
    "parent": "2" 
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/5?routing=2
{
  "name": "Digital watch",
  "sales_count": 100,
  "product_to_brand": {
    "name": "product", 
    "parent": "2" 
  }
}
```
{% include copy-curl.html %}

若要搜尋子文件的父文件，請使用 `has_child` 查詢。下列查詢會傳回製造手錶的父文件 (品牌)：

```json
GET testindex1/_search
{
  "query" : {
    "has_child": {
      "type":"product",
      "query": {
        "match" : {
            "name": "watch"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回這兩個品牌：

```json
{
  "took": 15,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Luxury brand",
          "product_to_brand": "brand"
        }
      },
      {
        "_index": "testindex1",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Economy brand",
          "product_to_brand": "brand"
        }
      }
    ]
  }
}
```

## 擷取內部命中

若要傳回符合查詢的子文件，請提供 `inner_hits` 參數：

```json
GET testindex1/_search
{
  "query" : {
    "has_child": {
      "type":"product",
      "query": {
        "match" : {
            "name": "watch"
        }
      },
      "inner_hits": {}
    }
  }
}
```
{% include copy-curl.html %}

回應會在 `inner_hits` 欄位中包含子文件：

```json
{
  "took": 52,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Luxury brand",
          "product_to_brand": "brand"
        },
        "inner_hits": {
          "product": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 0.53899646,
              "hits": [
                {
                  "_index": "testindex1",
                  "_id": "3",
                  "_score": 0.53899646,
                  "_routing": "1",
                  "_source": {
                    "name": "Mechanical watch",
                    "sales_count": 150,
                    "product_to_brand": {
                      "name": "product",
                      "parent": "1"
                    }
                  }
                }
              ]
            }
          }
        }
      },
      {
        "_index": "testindex1",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Economy brand",
          "product_to_brand": "brand"
        },
        "inner_hits": {
          "product": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": 0.53899646,
              "hits": [
                {
                  "_index": "testindex1",
                  "_id": "4",
                  "_score": 0.53899646,
                  "_routing": "2",
                  "_source": {
                    "name": "Electronic watch",
                    "sales_count": 300,
                    "product_to_brand": {
                      "name": "product",
                      "parent": "2"
                    }
                  }
                },
                {
                  "_index": "testindex1",
                  "_id": "5",
                  "_score": 0.53899646,
                  "_routing": "2",
                  "_source": {
                    "name": "Digital watch",
                    "sales_count": 100,
                    "product_to_brand": {
                      "name": "product",
                      "parent": "2"
                    }
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

如需擷取內部命中的詳細資訊，請參閱 [內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

## 參數

下表列出 `has_child` 查詢支援的所有最上層參數。

| 參數  | 必要／選用 | 說明  |
|:---|:---|:---|
| `type` | 必要 | 指定在 `join` 欄位對應中定義的子關係名稱。 |
| `query` | 必要 | 要在子文件上執行的查詢。如果子文件符合查詢，則會傳回父文件。 |
| `ignore_unmapped` | 選用 | 指出是否忽略未對應的 `type` 欄位，並且不傳回文件，而非擲回錯誤。在查詢多個索引時，若其中部分索引可能不包含 `type` 欄位，您可以提供此參數。預設為 `false`。 |
| `max_children` | 選用 | 父文件相符子文件數目上限。若超過此上限，父文件會從搜尋結果中排除。 |
| `min_children` | 選用 | 父文件要納入結果所需的相符子文件數目下限。若未達到，父文件會遭到排除。預設為 `1`。|
| `score_mode` | 選用 | 定義相符子文件的分數如何影響父文件的分數。有效值為：<br> - `none`：忽略子文件的相關性分數，並為父文件指派 `0` 的分數。<br> - `avg`：使用所有相符子文件的平均相關性分數。<br> - `max`：將相符子文件中最高的相關性分數指派給父文件。<br> - `min`：將相符子文件中最低的相關性分數指派給父文件。<br> - `sum`：加總所有相符子文件的相關性分數。<br> 預設為 `none`。 |
| `inner_hits` | 選用 | 若提供，會傳回符合查詢的基礎命中（子文件）。 |


## 排序限制

`has_child` 查詢不支援使用標準排序選項來[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。如果您需要依子文件中的欄位來排序父文件，您可以使用 [`function_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/)，並依父文件的分數排序。 

在上述範例中，您可以依子產品的 `sales_count` 來排序父文件 (品牌)。此查詢會將分數乘以子文件的 `sales_count` 欄位，並將相符子文件中最高的相關性分數指派給父文件：

```json
GET testindex1/_search
{
  "query": {
    "has_child": {
      "type": "product",
      "query": {
        "function_score": {
          "script_score": {
            "script": "_score * doc['sales_count'].value"
          }
        }
      },
      "score_mode": "max"
    }
  }
}
```
{% include copy-curl.html %}

回應會包含依最高子文件 `sales_count` 排序的品牌：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 300,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "2",
        "_score": 300,
        "_source": {
          "name": "Economy brand",
          "product_to_brand": "brand"
        }
      },
      {
        "_index": "testindex1",
        "_id": "1",
        "_score": 150,
        "_source": {
          "name": "Luxury brand",
          "product_to_brand": "brand"
        }
      }
    ]
  }
}
```

## 後續步驟

- 進一步了解[擷取內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。