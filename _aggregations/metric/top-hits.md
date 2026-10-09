---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排名最高的命中結果"
parent: Metric aggregations
nav_order: 130
redirect_from:
  - /query-dsl/aggregations/metric/top-hits/
---

# 排名最高的命中結果彙總

`top_hits` 彙總是一種多值指標彙總，可擷取每個彙總桶 (bucket) 中分數最高的文件。請在桶彙總中使用此彙總，以傳回每個群組中具代表性或排名最高的文件。

與桶彙總（例如 [`terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)）搭配使用時，`top_hits` 彙總會依指定的屬性將結果集分組，並從每個群組中擷取分數最高或最近更新的文件。這在下列情境中很實用：

- 顯示每個產品類別中最近的一筆交易。
- 顯示每個製造商分數最高的搜尋結果。
- 從分組結果中擷取具代表性的文件，而不傳回所有相符項目。

## 參數

下表列出 `top_hits` 彙總接受的參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `from` | 整數 | 要擷取的結果相對於第一個結果的位移。預設為 `0`。 |
| `size` | 整數 | 每個桶要傳回的最相符命中項目數量上限。預設為 `3`。 |
| `sort` | 物件或陣列 | 定義最相符命中項目的排序方式。根據預設，命中項目會依主要查詢的分數排序。 |

## 支援的個別命中功能

由於 `top_hits` 彙總會傳回標準的搜尋命中項目，因此支援下列個別命中功能：

- [醒目提示]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)
- [Explain]({{site.url}}{{site.baseurl}}/api-reference/search-apis/explain/)
- [具名查詢]({{site.url}}{{site.baseurl}}/query-dsl/named-queries/)
- [來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)
- [儲存欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored-fields)
- [指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields)
- [Doc value 欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-doc-value-fields)
- [包含版本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters)
- 包含序號與主要分片任期

## 範例：依類別將結果分組

在下列範例中，會使用 `terms` 彙總依產品類別將電子商務資料集中的訂單分組，並由 `top_hits` 子彙總擷取每個類別中最近的一筆訂單。來源中只包含 `order_date`、`taxful_total_price` 和 `customer_full_name` 欄位：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category.keyword",
        "size": 3
      },
      "aggs": {
        "most_recent_sales": {
          "top_hits": {
            "sort": [
              {
                "order_date": {
                  "order": "desc"
                }
              }
            ],
            "_source": {
              "includes": ["order_date", "taxful_total_price", "customer_full_name"]
            },
            "size": 1
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    回應範例
  </summary>
  {: .text-delta}

```json
{
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "top_categories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 2346,
      "buckets": [
        {
          "key": "Men's Clothing",
          "doc_count": 2024,
          "most_recent_sales": {
            "hits": {
              "total": {
                "value": 2024,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "poN5u50BpPQaFxReh8Tz",
                  "_score": null,
                  "_source": {
                    "customer_full_name": "Youssef Jensen",
                    "order_date": "2026-05-09T23:45:36+00:00",
                    "taxful_total_price": 78.98
                  },
                  "sort": [
                    1778370336000
                  ]
                }
              ]
            }
          }
        },
        {
          "key": "Women's Clothing",
          "doc_count": 1903,
          "most_recent_sales": {
            "hits": {
              "total": {
                "value": 1903,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "6IN5u50BpPQaFxRehr5T",
                  "_score": null,
                  "_source": {
                    "customer_full_name": "Sonya Smith",
                    "order_date": "2026-05-09T23:31:12+00:00",
                    "taxful_total_price": 42.98
                  },
                  "sort": [
                    1778369472000
                  ]
                }
              ]
            }
          }
        },
        {
          "key": "Women's Shoes",
          "doc_count": 1136,
          "most_recent_sales": {
            "hits": {
              "total": {
                "value": 1136,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "3IN5u50BpPQaFxReh78O",
                  "_score": null,
                  "_source": {
                    "customer_full_name": "Brigitte Cross",
                    "order_date": "2026-05-09T23:22:34+00:00",
                    "taxful_total_price": 91.98
                  },
                  "sort": [
                    1778368954000
                  ]
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```
</details>

## 範例：欄位摺疊

欄位摺疊（又稱結果分組）會將結果集整理成邏輯群組，並傳回每個群組中排名最前的文件。群組會依其分數最高之文件的相關性排序。

您可以將 `top_hits` 彙總包在桶彙總中，以實作欄位摺疊。下列範例會在電子商務資料集中搜尋符合 `shirt` 的產品，並依 `manufacturer` 將結果分組。`max` 彙總會擷取每個製造商的最高分數，而 `terms` 彙總則使用該分數依相關性排序各個桶：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "match": {
      "products.product_name": "shirt"
    }
  },
  "aggs": {
    "top_manufacturers": {
      "terms": {
        "field": "manufacturer.keyword",
        "size": 3,
        "order": {
          "top_score": "desc"
        }
      },
      "aggs": {
        "top_hits_per_manufacturer": {
          "top_hits": {
            "_source": {
              "includes": ["products.product_name", "manufacturer"]
            },
            "size": 1
          }
        },
        "top_score": {
          "max": {
            "script": {
              "source": "_score"
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

之所以必須使用 `max`（或 `min`）彙總，是因為 `top_hits` 彙總無法直接用於 `terms` 彙總的 `order` 選項中。
{: .note}

<details markdown="block">
  <summary>
    回應範例
  </summary>
  {: .text-delta}

```json
{
  "took": 38,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1160,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "top_manufacturers": {
      "doc_count_error_upper_bound": -1,
      "sum_other_doc_count": 953,
      "buckets": [
        {
          "key": "Elitelligence",
          "doc_count": 503,
          "top_score": {
            "value": 0.9982529878616333
          },
          "top_hits_per_manufacturer": {
            "hits": {
              "total": {
                "value": 503,
                "relation": "eq"
              },
              "max_score": 0.998253,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "34N5u50BpPQaFxReicgP",
                  "_score": 0.998253,
                  "_source": {
                    "manufacturer": [
                      "Elitelligence",
                      "Low Tide Media"
                    ],
                    "products": [
                      {
                        "product_name": "Shirt - white"
                      },
                      {
                        "product_name": "Shirt - white"
                      }
                    ]
                  }
                }
              ]
            }
          }
        },
        {
          "key": "Low Tide Media",
          "doc_count": 500,
          "top_score": {
            "value": 0.9982529878616333
          },
          "top_hits_per_manufacturer": {
            "hits": {
              "total": {
                "value": 500,
                "relation": "eq"
              },
              "max_score": 0.998253,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "34N5u50BpPQaFxReicgP",
                  "_score": 0.998253,
                  "_source": {
                    "manufacturer": [
                      "Elitelligence",
                      "Low Tide Media"
                    ],
                    "products": [
                      {
                        "product_name": "Shirt - white"
                      },
                      {
                        "product_name": "Shirt - white"
                      }
                    ]
                  }
                }
              ]
            }
          }
        },
        {
          "key": "Oceanavigations",
          "doc_count": 330,
          "top_score": {
            "value": 0.9561269283294678
          },
          "top_hits_per_manufacturer": {
            "hits": {
              "total": {
                "value": 330,
                "relation": "eq"
              },
              "max_score": 0.9561269,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "VYN5u50BpPQaFxRehbyq",
                  "_score": 0.9561269,
                  "_source": {
                    "manufacturer": [
                      "Oceanavigations",
                      "Low Tide Media"
                    ],
                    "products": [
                      {
                        "product_name": "Shirt - grey"
                      },
                      {
                        "product_name": "Vibrant Patterned Shirt"
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```
</details>

## 範例：將排名最高的命中結果彙總與巢狀物件搭配使用

當 `top_hits` 彙總包在 [`nested`]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/) 或 `reverse_nested` 彙總中時，會傳回巢狀命中結果。巢狀命中結果在內部儲存為個別的 Lucene 文件，並與其父文件共用相同的文件 ID。在 `nested` 或 `reverse_nested` 彙總語境中使用時，`top_hits` 彙總可以呈現這些內部文件。

每個巢狀命中結果在回應中都包含 `_nested` 欄位，用來識別陣列欄位，以及巢狀物件在該陣列中從零起算的位移。這項資訊有助於在父文件來源中找出原始的巢狀物件。

首先，建立具有 `nested` 欄位類型的索引：

```json
PUT /top-hits-products
{
  "mappings": {
    "properties": {
      "tags": { "type": "keyword" },
      "reviews": {
        "type": "nested",
        "properties": {
          "reviewer": { "type": "keyword" },
          "comment": { "type": "text" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

新增一份包含巢狀 `reviews` 欄位的文件：

```json
PUT /top-hits-products/_doc/1?refresh=true
{
  "tags": ["laptop", "electronics"],
  "reviews": [
    {"reviewer": "tech_guru", "comment": "This laptop has outstanding battery life"},
    {"reviewer": "casual_user", "comment": "Great laptop for everyday tasks"},
    {"reviewer": "power_user", "comment": "This laptop handles heavy workloads easily"}
  ]
}
```
{% include copy-curl.html %}

下列請求會搜尋標記為 `laptop` 的產品，依評論者將巢狀評論分組，並擷取每位評論者排名最高的評論：

```json
GET /top-hits-products/_search
{
  "query": {
    "term": { "tags": "laptop" }
  },
  "aggs": {
    "by_product": {
      "nested": {
        "path": "reviews"
      },
      "aggs": {
        "by_reviewer": {
          "terms": {
            "field": "reviews.reviewer",
            "size": 1
          },
          "aggs": {
            "by_nested": {
              "top_hits": {}
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`_nested` 欄位會識別陣列欄位 (`reviews`)，以及巢狀物件在該陣列中從零起算的位置 (`offset`)：

<details markdown="block">
<summary>
    範例回應
</summary>
{: .text-delta}

```json
{
  "took": 16,
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "top-hits-products",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "tags": [
            "laptop",
            "electronics"
          ],
          "reviews": [
            {
              "reviewer": "tech_guru",
              "comment": "This laptop has outstanding battery life"
            },
            {
              "reviewer": "casual_user",
              "comment": "Great laptop for everyday tasks"
            },
            {
              "reviewer": "power_user",
              "comment": "This laptop handles heavy workloads easily"
            }
          ]
        }
      }
    ]
  },
  "aggregations": {
    "by_product": {
      "doc_count": 3,
      "by_reviewer": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 2,
        "buckets": [
          {
            "key": "casual_user",
            "doc_count": 1,
            "by_nested": {
              "hits": {
                "total": {
                  "value": 1,
                  "relation": "eq"
                },
                "max_score": 1.0,
                "hits": [
                  {
                    "_index": "top-hits-products",
                    "_id": "1",
                    "_nested": {
                      "field": "reviews",
                      "offset": 1
                    },
                    "_score": 1.0,
                    "_source": {
                      "comment": "Great laptop for everyday tasks",
                      "reviewer": "casual_user"
                    }
                  }
                ]
              }
            }
          }
        ]
      }
    }
  }
}
```
</details>

為巢狀命中結果請求 `_source` 時，只會傳回巢狀物件的來源，而不是整個父文件的來源。當 `top_hits` 位於 `nested` 或 `reverse_nested` 彙總內時，也可以透過它存取在巢狀物件層級定義的已儲存欄位。

只有巢狀命中結果包含 `_nested` 欄位。一般 (非巢狀) 命中結果不會包含此欄位。

當索引停用 `_source` 時，`_nested` 欄位也可以作為參考，用來在原始來源中找出巢狀物件。

對於包含多層巢狀物件類型的對應，`_nested` 資訊可能是階層式的。下列程式碼片段顯示一個位於 `nested_grand_child_field` 第一個位置的巢狀命中結果，而它本身又位於 `nested_child_field` 的第二個位置：

```json
"hits": [
  {
    "_index": "my-index",
    "_id": "1",
    "_score": 1,
    "_nested": {
      "field": "nested_child_field",
      "offset": 1,
      "_nested": {
        "field": "nested_grand_child_field",
        "offset": 0
      }
    },
    "_source": ...
  }
]
```

## 範例：醒目提示相符的詞彙

下列範例會在產品名稱中搜尋 `shirt`，並使用 `highlight` 在每個排名最高的命中結果中以 `<em>` 標籤包住相符的詞彙：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "match": {
      "products.product_name": "shirt"
    }
  },
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category.keyword",
        "size": 2
      },
      "aggs": {
        "top_doc": {
          "top_hits": {
            "size": 1,
            "_source": {
              "includes": ["products.product_name"]
            },
            "highlight": {
              "fields": {
                "products.product_name": {}
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
<summary>
    範例回應
</summary>
{: .text-delta}

```json
{
  "took": 17,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1160,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "top_categories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 552,
      "buckets": [
        {
          "key": "Men's Clothing",
          "doc_count": 817,
          "top_doc": {
            "hits": {
              "total": {
                "value": 817,
                "relation": "eq"
              },
              "max_score": 0.998253,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "34N5u50BpPQaFxReicgP",
                  "_score": 0.998253,
                  "_source": {
                    "products": [
                      {
                        "product_name": "Shirt - white"
                      },
                      {
                        "product_name": "Shirt - white"
                      }
                    ]
                  },
                  "highlight": {
                    "products.product_name": [
                      "<em>Shirt</em> - white",
                      "<em>Shirt</em> - white"
                    ]
                  }
                }
              ]
            }
          }
        },
        {
          "key": "Women's Clothing",
          "doc_count": 343,
          "top_doc": {
            "hits": {
              "total": {
                "value": 343,
                "relation": "eq"
              },
              "max_score": 0.91741234,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "54N5u50BpPQaFxReiccP",
                  "_score": 0.91741234,
                  "_source": {
                    "products": [
                      {
                        "product_name": "Shirt - white"
                      },
                      {
                        "product_name": "Shirt - light blue denim"
                      }
                    ]
                  },
                  "highlight": {
                    "products.product_name": [
                      "<em>Shirt</em> - white",
                      "<em>Shirt</em> - light blue denim"
                    ]
                  }
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```
</details>

## 範例：使用指令碼欄位

下列範例會擷取每個類別中價格最高的訂單，並使用 `script_fields` 定義計算 15% 的折扣：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category.keyword",
        "size": 2
      },
      "aggs": {
        "top_doc": {
          "top_hits": {
            "size": 1,
            "sort": [
              {
                "taxful_total_price": {
                  "order": "desc"
                }
              }
            ],
            "_source": {
              "includes": ["customer_full_name", "taxful_total_price"]
            },
            "script_fields": {
              "price_with_tax_discount": {
                "script": {
                  "source": "doc['taxful_total_price'].value * 0.85"
                }
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
<summary>
    範例回應
</summary>
{: .text-delta}

```json
{
  "took": 51,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "top_categories": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 3482,
      "buckets": [
        {
          "key": "Men's Clothing",
          "doc_count": 2024,
          "top_doc": {
            "hits": {
              "total": {
                "value": 2024,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "LoN5u50BpPQaFxRehr9T",
                  "_score": null,
                  "_source": {
                    "customer_full_name": "Wagdi Shaw",
                    "taxful_total_price": 2249.92
                  },
                  "fields": {
                    "price_with_tax_discount": [
                      1912.5
                    ]
                  },
                  "sort": [
                    2250.0
                  ]
                }
              ]
            }
          }
        },
        {
          "key": "Women's Clothing",
          "doc_count": 1903,
          "top_doc": {
            "hits": {
              "total": {
                "value": 1903,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "opensearch_dashboards_sample_data_ecommerce",
                  "_id": "z4N5u50BpPQaFxReicuj",
                  "_score": null,
                  "_source": {
                    "customer_full_name": "Elyssa Hart",
                    "taxful_total_price": 343.96
                  },
                  "fields": {
                    "price_with_tax_discount": [
                      292.4
                    ]
                  },
                  "sort": [
                    344.0
                  ]
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```
</details>

## 回應本文欄位

下表列出每個 `top_hits` 彙總結果中傳回的回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `hits.total.value` | 整數 | 桶 (bucket) 中符合彙總條件的文件總數。 |
| `hits.total.relation` | 字串 | 表示總數是確切值（`eq`）還是下限值（`gte`）。 |
| `hits.max_score` | 浮點數或空值 | 傳回的命中結果中最高的相關性分數。當命中結果依 `_score` 以外的欄位排序時，此值為 `null`。 |
| `hits.hits` | 陣列 | 該桶中最符合條件的文件陣列。 |
| `hits.hits._index` | 字串 | 包含該文件的索引。 |
| `hits.hits._id` | 字串 | 文件的唯一識別碼。 |
| `hits.hits._score` | 浮點數或空值 | 文件的相關性分數。當依 `_score` 以外的欄位排序時，此值為 `null`。 |
| `hits.hits._source` | 物件 | 原始文件來源。套用來源篩選時，只會傳回所請求的欄位。 |
| `hits.hits.sort` | 陣列 | 用於排序此命中結果的排序值，只有在明確指定 `sort` 時才會出現。 |
| `hits.hits._nested` | 物件 | 只有巢狀命中結果才會出現。包含 `field`（巢狀陣列欄位名稱）和 `offset`（在陣列中從零起算的位置）。 |
