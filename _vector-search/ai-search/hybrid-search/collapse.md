---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "摺疊混合查詢結果"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 35
---

# 摺疊混合查詢結果
**於 3.1 版引入**
{: .label .label-purple }

`collapse` 參數可讓您依欄位將結果分組，針對每個唯一欄位值僅傳回分數最高的文件。當您想避免搜尋結果重複時，這項功能相當實用。用於摺疊的欄位必須為 `keyword` 類型或數值類型。傳回的結果數量仍受查詢中的 `size` 參數限制。

`collapse` 參數可與其他混合查詢搜尋選項搭配使用，例如排序、explain 和分頁，並採用這些選項的標準語法。

在混合查詢中使用 `collapse` 時，請注意下列事項：

- `index.neural_search.hybrid_collapse_docs_per_group_per_subquery` 設定已棄用，且不會產生任何作用。如果您的索引組態中有此設定，可以放心移除。搜尋結果完全由搜尋請求中的 `size` 參數控制。
- 彙總會針對摺疊前的結果執行，而非最終輸出。
- 分頁行為會改變：由於 `collapse` 會減少結果總數，因此可能影響結果在各頁的分布。若要擷取更多結果，請考慮增加分頁深度。
- 結果可能與 [`collapse` 回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/collapse-processor/)傳回的結果不同，該處理器會在查詢執行後套用摺疊邏輯。

## 範例

下列範例示範如何收合混合查詢結果。

建立索引：

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
{% include copy-curl.html %}

將文件匯入索引：

```json
POST /bakery-items/_bulk
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 15, "baked_date": "2023-07-01T00:00:00Z" }
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 18, "baked_date": "2023-07-04T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 12, "baked_date": "2023-07-02T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 16, "baked_date": "2023-07-03T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 17, "baked_date": "2023-07-09T00:00:00Z" }
```
{% include copy-curl.html %}

建立搜尋管線。此範例使用 `min_max` 正規化技術：

```json
PUT /_search/pipeline/norm-pipeline
{
  "description": "Normalization processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

搜尋索引，並依 `item` 欄位將搜尋結果分組：

```json
GET /bakery-items/_search?search_pipeline=norm-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "item": "Chocolate Cake"
          }
        },
        {
          "bool": {
            "must": {
              "match": {
                "category": "cakes"
              }
            }
          }
        }
      ]
    }
  },
  "collapse": {
    "field": "item"
  }
}
```
{% include copy-curl.html %}

回應會傳回收合後的搜尋結果：

```json
"hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "bakery-items",
        "_id": "wBRPZZcB49c_2-1rYmO7",
        "_score": 1.0,
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
        }
      },
      {
        "_index": "bakery-items",
        "_id": "whRPZZcB49c_2-1rYmO7",
        "_score": 0.5,
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
        }
      }
    ]
  }
```

## 摺疊並排序結果

若要摺疊並排序混合查詢結果，請在查詢中提供 `collapse` 與 `sort` 參數：

```json
GET /bakery-items/_search?search_pipeline=norm-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
                "item": "Chocolate Cake"
          }
        },
        {
          "bool": {
                "must": {
                    "match": {
                        "category": "cakes"
                    }
                }
          }
        }
      ]
    }
  },
  "collapse": {
    "field": "item"
  },
  "sort": "price"
}
```
{% include copy-curl.html %}

如需在混合查詢中排序的更多資訊，請參閱 [在混合查詢中使用排序]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/sorting/)。

在回應中，文件會依最低價格排序：

```json
"hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "bakery-items",
        "_id": "whRPZZcB49c_2-1rYmO7",
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
          12.0
        ]
      },
      {
        "_index": "bakery-items",
        "_id": "wBRPZZcB49c_2-1rYmO7",
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
          15.0
        ]
      }
    ]
  }
```

## 摺疊與 explain

您可以在摺疊搜尋結果時提供 `explain` 查詢參數：

```json
GET /bakery-items/_search?search_pipeline=norm-pipeline&explain=true
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
                "item": "Chocolate Cake"
          }
        },
        {
          "bool": {
                "must": {
                    "match": {
                        "category": "cakes"
                    }
                }
          }
        }
      ]
    }
  },
  "collapse": {
    "field": "item"
  }
}
```
{% include copy-curl.html %}

回應中包含每個搜尋結果評分程序的詳細資訊：

```json
"hits": {
        "total": {
            "value": 5,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_shard": "[bakery-items][0]",
                "_node": "Jlu8P9EaQCy3C1BxaFMa_g",
                "_index": "bakery-items",
                "_id": "3ZILepcBheX09_dPt8TD",
                "_score": 1.0,
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
                "_explanation": {
                    "value": 1.0,
                    "description": "combined score of:",
                    "details": [
                        {
                            "value": 1.0,
                            "description": "ConstantScore(item:Chocolate Cake)",
                            "details": []
                        },
                        {
                            "value": 1.0,
                            "description": "ConstantScore(category:cakes)",
                            "details": []
                        }
                    ]
                }
            },
            {
                "_shard": "[bakery-items][0]",
                "_node": "Jlu8P9EaQCy3C1BxaFMa_g",
                "_index": "bakery-items",
                "_id": "35ILepcBheX09_dPt8TD",
                "_score": 0.5,
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
                "_explanation": {
                    "value": 1.0,
                    "description": "combined score of:",
                    "details": [
                        {
                            "value": 0.0,
                            "description": "ConstantScore(item:Chocolate Cake) doesn't match id 2",
                            "details": []
                        },
                        {
                            "value": 1.0,
                            "description": "ConstantScore(category:cakes)",
                            "details": []
                        }
                    ]
                }
            }
        ]
    }
```

如需在混合查詢中使用 `explain` 的更多資訊，請參閱[混合搜尋 explain]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/explain/)。

## 收合與分頁

您可以提供 `from` 和 `size` 參數來為收合後的結果分頁。如需混合查詢中分頁的詳細資訊，請參閱[混合查詢結果分頁]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pagination/)。如需 `from` 和 `size` 的詳細資訊，請參閱[`from` 和 `size` 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。

在此範例中，請建立下列索引：

```json
PUT /bakery-items-pagination
{
    "settings": {
         "index.number_of_shards": 3
    },
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
{% include copy-curl.html %}

將下列文件匯入索引：

```json
POST /bakery-items-pagination/_bulk
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 15, "baked_date": "2023-07-01T00:00:00Z" }
{ "index": {} }
{ "item": "Chocolate Cake", "category": "cakes", "price": 18, "baked_date": "2023-07-02T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 12, "baked_date": "2023-07-02T00:00:00Z" }
{ "index": {} }
{ "item": "Vanilla Cake", "category": "cakes", "price": 11, "baked_date": "2023-07-04T00:00:00Z" }
{ "index": {} }
{ "item": "Ice Cream Cake", "category": "cakes", "price": 23, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Ice Cream Cake", "category": "cakes", "price": 22, "baked_date": "2023-07-10T00:00:00Z" }
{ "index": {} }
{ "item": "Carrot Cake", "category": "cakes", "price": 24, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Carrot Cake", "category": "cakes", "price": 26, "baked_date": "2023-07-21T00:00:00Z" }
{ "index": {} }
{ "item": "Red Velvet Cake", "category": "cakes", "price": 25, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Red Velvet Cake", "category": "cakes", "price": 29, "baked_date": "2023-07-30T00:00:00Z" }
{ "index": {} }
{ "item": "Cheesecake", "category": "cakes", "price": 27, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Cheesecake", "category": "cakes", "price": 34, "baked_date": "2023-07-21T00:00:00Z" }
{ "index": {} }
{ "item": "Coffee Cake", "category": "cakes", "price": 42, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Coffee Cake", "category": "cakes", "price": 41, "baked_date": "2023-07-05T00:00:00Z" }
{ "index": {} }
{ "item": "Cocunut Cake", "category": "cakes", "price": 23, "baked_date": "2023-07-09T00:00:00Z" }
{ "index": {} }
{ "item": "Cocunut Cake", "category": "cakes", "price": 32, "baked_date": "2023-07-12T00:00:00Z" }
```
{% include copy-curl.html %}

執行 `hybrid` 查詢，並指定 `from` 和 `size` 參數來為結果分頁。在下列範例中，查詢會要求從第六個位置開始的兩筆結果（`from: 5, size: 2`）。分頁深度設為限制每個分片最多傳回 10 份文件。擷取結果後，會套用 `collapse` 參數，依 `item` 欄位將結果分組：

```json
GET /bakery-items-pagination/_search?search_pipeline=norm-pipeline
{
  "query": {
    "hybrid": {
      "pagination_depth": 10,
      "queries": [
        {
          "match": {
                "item": "Chocolate Cake"
          }
        },
        {
          "bool": {
                "must": {
                    "match": {
                        "category": "cakes"
                    }
                }
          }
        }
      ]
    }
  },
  "from": 5,
  "size": 2,
  "collapse": {
    "field": "item"
  }
}
```
{% include copy-curl.html %}

回應包含收合結果的第六組和第七組：

```json
"hits": {
        "total": {
            "value": 16,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "bakery-items-pagination",
                "_id": "gDayepcBIkxlgFKYda0p",
                "_score": 0.5,
                "_source": {
                    "item": "Carrot Cake",
                    "category": "cakes",
                    "price": 26,
                    "baked_date": "2023-07-21T00:00:00Z"
                },
                "fields": {
                    "item": [
                        "Carrot Cake"
                    ]
                }
            },
            {
                "_index": "bakery-items-pagination",
                "_id": "aTayepcBIkxlgFKYca15",
                "_score": 0.5,
                "_source": {
                    "item": "Cheesecake",
                    "category": "cakes",
                    "price": 27,
                    "baked_date": "2023-07-09T00:00:00Z"
                },
                "fields": {
                    "item": [
                        "Cheesecake"
                    ]
                }
            }
        ]
    }
```

## 擷取摺疊混合查詢結果的內部命中
**於 3.2 版引入**
{: .label .label-purple }

您可以在 `collapse` 參數內使用 `inner_hits` 參數，從每個摺疊群組擷取額外的文件。

下列範例使用先前建立的 `bakery-items` 索引。它搜尋蛋糕商品，依 `item` 欄位摺疊（分組）結果，並傳回每個摺疊值中最便宜的兩件商品：

```json
GET /bakery-items/_search?search_pipeline=norm-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "item": "Chocolate Cake"
          }
        },
        {
          "bool": {
            "must": {
              "match": {
                "category": "cakes"
              }
            }
          }
        }
      ]
    }
  },
  "collapse": {
    "field": "item",
    "inner_hits": [
      {
        "name": "cheapest_items",
        "size": 2,
        "sort": ["price"]
      }
    ]
  }
}
```
{% include copy-curl.html %}

在回應中，主要的 `hits` 包含來自每個摺疊群組的最高分文件。`inner_hits` 則包含來自每個群組最便宜的兩件商品：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  ...
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "bakery-items",
        "_id": "bIe6e5gBAB5HT6ixTd4F",
        "_score": 1,
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
        "inner_hits": {
          "cheapest_items": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "bakery-items",
                  "_id": "bIe6e5gBAB5HT6ixTd4F",
                  "_score": null,
                  "_source": {
                    "item": "Chocolate Cake",
                    "category": "cakes",
                    "price": 15,
                    "baked_date": "2023-07-01T00:00:00Z"
                  },
                  "sort": [
                    15.0
                  ]
                },
                {
                  "_index": "bakery-items",
                  "_id": "bYe6e5gBAB5HT6ixTd4F",
                  "_score": null,
                  "_source": {
                    "item": "Chocolate Cake",
                    "category": "cakes",
                    "price": 18,
                    "baked_date": "2023-07-04T00:00:00Z"
                  },
                  "sort": [
                    18.0
                  ]
                }
              ]
            }
          }
        }
      },
      {
        "_index": "bakery-items",
        "_id": "boe6e5gBAB5HT6ixTd4F",
        "_score": 0.5,
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
        "inner_hits": {
          "cheapest_items": {
            "hits": {
              "total": {
                "value": 3,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "bakery-items",
                  "_id": "boe6e5gBAB5HT6ixTd4F",
                  "_score": null,
                  "_source": {
                    "item": "Vanilla Cake",
                    "category": "cakes",
                    "price": 12,
                    "baked_date": "2023-07-02T00:00:00Z"
                  },
                  "sort": [
                    12.0
                  ]
                },
                {
                  "_index": "bakery-items",
                  "_id": "b4e6e5gBAB5HT6ixTd4F",
                  "_score": null,
                  "_source": {
                    "item": "Vanilla Cake",
                    "category": "cakes",
                    "price": 16,
                    "baked_date": "2023-07-03T00:00:00Z"
                  },
                  "sort": [
                    16.0
                  ]
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

</details>