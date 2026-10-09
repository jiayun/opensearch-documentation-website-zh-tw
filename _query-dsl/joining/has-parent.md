---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Has parent 查詢"
parent: Joining queries
nav_order: 20
---

# Has parent 查詢

`has_parent` 查詢會傳回父文件符合特定查詢的子文件。您可以使用 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型，在同一個索引中的文件之間建立父子關係。

`has_parent` 查詢因為會執行聯結作業，所以比其他查詢慢。隨著符合條件的父文件數量增加，效能也會降低。搜尋中的每個 `has_parent` 查詢都可能大幅影響查詢效能。如果您優先考量速度，請避免使用此查詢，或盡可能限制其使用。
{: .warning}

## 範例 

執行 `has_parent` 查詢之前，您的索引必須包含 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位，才能建立父子關係。索引對應請求使用下列格式：

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

在此範例中，請先依照 [`has_child` 查詢範例]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-child/)中的說明，設定包含代表產品及其品牌之文件的索引。 

若要搜尋父文件的子文件，請使用 `has_parent` 查詢。下列查詢會傳回由符合查詢 `economy` 的品牌所製造的子文件（產品）：

```json
GET testindex1/_search
{
  "query" : {
    "has_parent": {
      "parent_type":"brand",
      "query": {
        "match" : {
          "name": "economy"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回該品牌製造的所有產品：

```json
{
  "took": 11,
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
        "_id": "4",
        "_score": 1,
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
        "_score": 1,
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
```

## 擷取內部命中結果

若要傳回符合查詢的父文件，請提供 `inner_hits` 參數：

```json
GET testindex1/_search
{
  "query" : {
    "has_parent": {
      "parent_type":"brand",
      "query": {
        "match" : {
          "name": "economy"
        }
      },
      "inner_hits": {}
    }
  }
}
```
{% include copy-curl.html %}

回應的 `inner_hits` 欄位中包含父文件：

```json
{
  "took": 11,
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
        "_id": "4",
        "_score": 1,
        "_routing": "2",
        "_source": {
          "name": "Electronic watch",
          "sales_count": 300,
          "product_to_brand": {
            "name": "product",
            "parent": "2"
          }
        },
        "inner_hits": {
          "brand": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.3862942,
              "hits": [
                {
                  "_index": "testindex1",
                  "_id": "2",
                  "_score": 1.3862942,
                  "_source": {
                    "name": "Economy brand",
                    "product_to_brand": "brand"
                  }
                }
              ]
            }
          }
        }
      },
      {
        "_index": "testindex1",
        "_id": "5",
        "_score": 1,
        "_routing": "2",
        "_source": {
          "name": "Digital watch",
          "sales_count": 100,
          "product_to_brand": {
            "name": "product",
            "parent": "2"
          }
        },
        "inner_hits": {
          "brand": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.3862942,
              "hits": [
                {
                  "_index": "testindex1",
                  "_id": "2",
                  "_score": 1.3862942,
                  "_source": {
                    "name": "Economy brand",
                    "product_to_brand": "brand"
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

如需擷取內部命中結果的詳細資訊，請參閱[內部命中結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

## 參數

下表列出 `has_parent` 查詢支援的所有最上層參數。

| 參數  | 必要／選用 | 說明  |
|:---|:---|:---|
| `parent_type` | 必要 | 指定 `join` 欄位對應中定義的父關係名稱。 |
| `query` | 必要 | 要對父文件執行的查詢。如果父文件符合查詢，就會傳回子文件。 |
| `ignore_unmapped` | 選用 | 指出是否忽略未對應的 `parent_type` 欄位，並且不傳回文件，而非擲回錯誤。查詢多個索引時，您可以提供此參數，因為其中某些索引可能不包含 `parent_type` 欄位。預設值為 `false`。 |
| `score` | 選用 | 指出是否將符合條件的父文件之相關性分數彙總至其子文件。如果為 `false`，則會忽略父文件的相關性分數，並為每個子文件指派等於查詢之 `boost` 的相關性分數，其預設值為 `1`。如果為 `true`，則會將符合條件的父文件之相關性分數彙總至其子文件的相關性分數。預設值為 `false`。 |
| `inner_hits` | 選用 | 若提供此參數，則會傳回符合查詢的底層命中結果（父文件）。 |


## 排序限制

`has_parent` 查詢不支援使用標準排序選項來[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。如果您需要依父文件中的欄位排序子文件，可以使用 [`function_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/)，並依子文件的分數排序。 

針對上述範例，請先新增 `customer_satisfaction` 欄位，您將依此欄位排序屬於父文件（品牌）的子文件：

```json
PUT testindex1/_doc/1
{
  "name": "Luxury watch brand",
  "product_to_brand" : "brand",
  "customer_satisfaction": 4.5
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "name": "Economy watch brand",
  "product_to_brand" : "brand",
  "customer_satisfaction": 3.9
}
```
{% include copy-curl.html %}

現在，您可以根據父品牌的 `customer_satisfaction` 欄位排序子文件（產品）。此查詢會將分數乘以父文件的 `customer_satisfaction` 欄位值：

```json
GET testindex1/_search
{
  "query": {
    "has_parent": {
      "parent_type": "brand",
      "score": true,
      "query": {
        "function_score": {
          "script_score": {
            "script": "_score * doc['customer_satisfaction'].value"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含依父文件的 `customer_satisfaction` 值由高至低排序的產品：

```json
{
  "took": 11,
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
    "max_score": 4.5,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "3",
        "_score": 4.5,
        "_routing": "1",
        "_source": {
          "name": "Mechanical watch",
          "sales_count": 150,
          "product_to_brand": {
            "name": "product",
            "parent": "1"
          }
        }
      },
      {
        "_index": "testindex1",
        "_id": "4",
        "_score": 3.9,
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
        "_score": 3.9,
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
```

## 後續步驟

- 深入瞭解[擷取內部命中結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。