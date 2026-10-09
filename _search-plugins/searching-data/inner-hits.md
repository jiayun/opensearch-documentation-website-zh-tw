---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "擷取內部命中結果"
parent: Customizing search results
has_children: false
nav_order: 60
---

# 擷取內部命中結果

在 OpenSearch 中，當您使用[巢狀物件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)或 [parent-join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 執行搜尋時，底層的命中結果（巢狀內部物件或子文件）預設會隱藏。您可以在搜尋查詢中使用 `inner_hits` 參數來擷取內部命中結果。

您也可以搭配下列功能使用 `inner_hits`：

  - [醒目提示查詢相符項目]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)
  - [解釋]({{site.url}}{{site.baseurl}}/api-reference/explain/)

## 巢狀物件的內部命中結果
巢狀物件可讓您為物件陣列編製索引，並在同一份文件中維持物件之間的關係。下列範例請求使用 `inner_hits` 參數來擷取底層的內部命中結果。

1. 建立包含巢狀物件的索引對應：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "user": {
            "type": "nested",
            "properties": {
              "name": { "type": "text" },
              "age": { "type": "integer" }
            }
          }
        }
      }
    }
    ```
{% include copy-curl.html %}

2. 將資料編製索引：

    ```json
    POST /my_index/_doc/1
    {
      "group": "fans",
      "user": [
        {
          "name": "John Doe",
          "age": 28
        },
        {
          "name": "Jane Smith",
          "age": 34
        }
      ]
    }
    ```
{% include copy-curl.html %}

3. 使用 `inner_hits` 進行查詢：

    ```json
    GET /my_index/_search
    {
      "query": {
        "nested": {
          "path": "user",
          "query": {
            "bool": {
              "must": [
                { "match": { "user.name": "John" } }
              ]
            }
          },
          "inner_hits": {}
        }
      }
    }
    ```
{% include copy-curl.html %}

上述查詢會搜尋包含姓名 John 的巢狀使用者物件，並在回應的 `inner_hits` 區段中傳回相符的巢狀文件：

```json
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.6931471,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 0.6931471,
        "_source" : {
          "group" : "fans",
          "user" : [
            {
              "name" : "John Doe",
              "age" : 28
            },
            {
              "name" : "Jane Smith",
              "age" : 34
            }
          ]
        },
        "inner_hits" : {
          "user" : {
            "hits" : {
              "total" : {
                "value" : 1,
                "relation" : "eq"
              },
              "max_score" : 0.6931471,
              "hits" : [
                {
                  "_index" : "my_index",
                  "_id" : "1",
                  "_nested" : {
                    "field" : "user",
                    "offset" : 0
                  },
                  "_score" : 0.6931471,
                  "_source" : {
                    "name" : "John Doe",
                    "age" : 28
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
## 父／子物件的內部命中結果
Parent-join 關係可讓您在同一個索引中，建立不同類型文件之間的關係。下列範例請求使用父／子物件，搭配 `inner_hits` 進行搜尋。

1. 建立包含 parent-join 欄位的索引：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "my_join_field": {
            "type": "join",
            "relations": {
              "parent": "child"
            }
          },
          "text": {
            "type": "text"
          }
        }
      }
    }
    ```
{% include copy-curl.html %}

2. 將資料編製索引：

    ```json
    # Index a parent document
    PUT /my_index/_doc/1
    {
      "text": "This is a parent document",
      "my_join_field": "parent"
    }
    
    # Index a child document
    PUT /my_index/_doc/2?routing=1
    {
      "text": "This is a child document",
      "my_join_field": {
        "name": "child",
        "parent": "1"
      }
    }
    ```
{% include copy-curl.html %}

3. 使用 `inner_hits` 進行搜尋：

    ```json
    GET /my_index/_search
    {
      "query": {
        "has_child": {
          "type": "child",
          "query": {
            "match": {
              "text": "child"
            }
          },
          "inner_hits": {}
        }
      }
    }
    ```
{% include copy-curl.html %}

上述查詢會搜尋具有符合查詢條件之子文件的父文件（在此範例中，子文件包含詞彙 `"child"`）。查詢會在回應的 `inner_hits` 區段中傳回相符的子文件：

```json
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "text" : "This is a parent document",
          "my_join_field" : "parent"
        },
        "inner_hits" : {
          "child" : {
            "hits" : {
              "total" : {
                "value" : 1,
                "relation" : "eq"
              },
              "max_score" : 0.6931471,
              "hits" : [
                {
                  "_index" : "my_index",
                  "_id" : "2",
                  "_score" : 0.6931471,
                  "_routing" : "1",
                  "_source" : {
                    "text" : "This is a child document",
                    "my_join_field" : {
                      "name" : "child",
                      "parent" : "1"
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

## 搭配 `inner_hits` 同時使用 parent-join 與巢狀物件

下列範例示範如何搭配 `inner_hits` 同時使用 parent-join 與巢狀物件。

1. 建立具有下列對應的索引：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "my_join_field": {
            "type": "join",
            "relations": {
              "parent": "child"
            }
          },
          "text": {
            "type": "text"
          },
          "comments": {
            "type": "nested",
            "properties": {
              "user": { "type": "text" },
              "message": { "type": "text" }
            }
          }
        }
      }
    }
    ```
{% include copy-curl.html %}

2. 將資料編製索引：

    ```json
    # Index a parent document
    PUT /my_index/_doc/1
    {
      "text": "This is a parent document",
      "my_join_field": "parent"
    }
    
    # Index a child document with nested comments
    PUT /my_index/_doc/2?routing=1
    {
      "text": "This is a child document",
      "my_join_field": {
        "name": "child",
        "parent": "1"
      },
      "comments": [
        {
          "user": "John",
          "message": "This is a comment"
        },
        {
          "user": "Jane",
          "message": "Another comment"
        }
      ]
    }
    ```
{% include copy-curl.html %}

3. 使用 `inner_hits` 進行查詢：

    ```json
    GET /my_index/_search
    {
      "query": {
        "has_child": {
          "type": "child",
          "query": {
            "nested": {
              "path": "comments",
              "query": {
                "bool": {
                  "must": [
                    { "match": { "comments.user": "John" } }
                  ]
                }
              },
              "inner_hits": {}
            }
          },
          "inner_hits": {}
        }
      }
    }
    ```
{% include copy-curl.html %}

上述查詢會搜尋具有包含 John 所發表留言之子文件的父文件。指定 `inner_hits` 可確保傳回相符的子文件及其巢狀留言：

```json
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "text" : "This is a parent document",
          "my_join_field" : "parent"
        },
        "inner_hits" : {
          "child" : {
            "hits" : {
              "total" : {
                "value" : 1,
                "relation" : "eq"
              },
              "max_score" : 0.6931471,
              "hits" : [
                {
                  "_index" : "my_index",
                  "_id" : "2",
                  "_score" : 0.6931471,
                  "_routing" : "1",
                  "_source" : {
                    "text" : "This is a child document",
                    "my_join_field" : {
                      "name" : "child",
                      "parent" : "1"
                    },
                    "comments" : [
                      {
                        "user" : "John",
                        "message" : "This is a comment"
                      },
                      {
                        "user" : "Jane",
                        "message" : "Another comment"
                      }
                    ]
                  },
                  "inner_hits" : {
                    "comments" : {
                      "hits" : {
                        "total" : {
                          "value" : 1,
                          "relation" : "eq"
                        },
                        "max_score" : 0.6931471,
                        "hits" : [
                          {
                            "_index" : "my_index",
                            "_id" : "2",
                            "_nested" : {
                              "field" : "comments",
                              "offset" : 0
                            },
                            "_score" : 0.6931471,
                            "_source" : {
                              "message" : "This is a comment",
                              "user" : "John"
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
        }
      }
    ]
  }
}
```

<!-- vale off -->
## inner_hits 參數
<!-- vale on -->
您可以在使用 `inner_hits` 進行搜尋時，傳遞下列額外參數，適用於巢狀物件與 parent-join 關聯：

* `from`：從 `inner_hits` 結果中開始擷取命中的偏移量。
* `size`：要傳回的內部命中數量上限。
* `sort`：內部命中的排序方式。
* `name`：回應中內部命中的自訂名稱。這有助於在單一查詢中區分多個內部命中。

<!-- vale off -->
### 範例：搭配巢狀物件使用 inner_hits 參數
<!-- vale on -->

1. 使用下列對應建立索引：

    ```json
    PUT /products
    {
      "mappings": {
        "properties": {
          "product_name": { "type": "text" },
          "reviews": {
            "type": "nested",
            "properties": {
              "user": { "type": "text" },
              "comment": { "type": "text" },
              "rating": { "type": "integer" }
            }
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將資料編製索引：

    ```json
    POST /products/_doc/1
    {
      "product_name": "Smartphone",
      "reviews": [
        { "user": "Alice", "comment": "Great phone", "rating": 5 },
        { "user": "Bob", "comment": "Not bad", "rating": 3 },
        { "user": "Charlie", "comment": "Excellent", "rating": 4 }
      ]
    }
    ```
    {% include copy-curl.html %}

    ```json
    POST /products/_doc/2
    {
      "product_name": "Laptop",
      "reviews": [
        { "user": "Dave", "comment": "Very good", "rating": 5 },
        { "user": "Eve", "comment": "Good value", "rating": 4 }
      ]
    }
    ```
    {% include copy-curl.html %}

3. 使用 `inner_hits` 進行查詢並提供額外參數：

    ```json
    GET /products/_search
    {
      "query": {
        "nested": {
          "path": "reviews",
          "query": {
            "match": { "reviews.comment": "Good" }
          },
          "inner_hits": {
            "from": 0,
            "size": 2,
            "sort": [
              { "reviews.rating": { "order": "desc" } }
            ],
            "name": "top_reviews"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期結果：

```json
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.83740485,
    "hits" : [
      {
        "_index" : "products",
        "_id" : "2",
        "_score" : 0.83740485,
        "_source" : {
          "product_name" : "Laptop",
          "reviews" : [
            {
              "user" : "Dave",
              "comment" : "Very good",
              "rating" : 5
            },
            {
              "user" : "Eve",
              "comment" : "Good value",
              "rating" : 4
            }
          ]
        },
        "inner_hits" : {
          "top_reviews" : {
            "hits" : {
              "total" : {
                "value" : 2,
                "relation" : "eq"
              },
              "max_score" : null,
              "hits" : [
                {
                  "_index" : "products",
                  "_id" : "2",
                  "_nested" : {
                    "field" : "reviews",
                    "offset" : 0
                  },
                  "_score" : null,
                  "_source" : {
                    "rating" : 5,
                    "comment" : "Very good",
                    "user" : "Dave"
                  },
                  "sort" : [
                    5
                  ]
                },
                {
                  "_index" : "products",
                  "_id" : "2",
                  "_nested" : {
                    "field" : "reviews",
                    "offset" : 1
                  },
                  "_score" : null,
                  "_source" : {
                    "rating" : 4,
                    "comment" : "Good value",
                    "user" : "Eve"
                  },
                  "sort" : [
                    4
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

<!-- vale off -->
### 範例：搭配 parent-join 關聯使用 inner_hits 參數
<!-- vale on -->

1. 使用下列對應建立索引：

    ```json
    PUT /company
    {
      "mappings": {
        "properties": {
          "my_join_field": {
            "type": "join",
            "relations": {
              "employee": "task"
            }
          },
          "name": { "type": "text" },
          "description": {
            "type": "text",
            "fields": {
              "keyword": { "type": "keyword" }
            }
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將資料編製索引：

    ```json
    # Index a parent document
    PUT /company/_doc/1
    {
      "name": "Alice",
      "my_join_field": "employee"
    }
    ```
    {% include copy-curl.html %}
    
    ```json
    # Index child documents
    PUT /company/_doc/2?routing=1
    {
      "description": "Complete the project",
      "my_join_field": {
        "name": "task",
        "parent": "1"
      }
    }
    ```
    {% include copy-curl.html %}
    
    ```json
    PUT /company/_doc/3?routing=1
    {
      "description": "Prepare the report",
      "my_join_field": {
        "name": "task",
        "parent": "1"
      }
    }
    ```
    {% include copy-curl.html %}

    ```json
    PUT /company/_doc/4?routing=1
    {
      "description": "Update project",
      "my_join_field": {
        "name": "task",
        "parent": "1"
      }
    }
    ```
    {% include copy-curl.html %}

3. 使用 `inner_hits` 參數進行查詢：

    ```json
    GET /company/_search
    {
      "query": {
        "has_child": {
          "type": "task",
          "query": {
            "match": { "description": "project" }
          },
          "inner_hits": {
            "from": 0,
            "size": 10,
            "sort": [
              { "description.keyword": { "order": "asc" } }
            ],
            "name": "related_tasks"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期結果：

```json
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits": [
      {
        "_index": "company",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Alice",
          "my_join_field": "employee"
        },
        "inner_hits": {
          "related_tasks": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": null,
              "hits": [
                {
                  "_index": "company",
                  "_id": "2",
                  "_score": null,
                  "_routing": "1",
                  "_source": {
                    "description": "Complete the project",
                    "my_join_field": {
                      "name": "task",
                      "parent": "1"
                    }
                  },
                  "sort": [
                    "Complete the project"
                  ]
                },
                {
                  "_index": "company",
                  "_id": "4",
                  "_score": null,
                  "_routing": "1",
                  "_source": {
                    "description": "Update project",
                    "my_join_field": {
                      "name": "task",
                      "parent": "1"
                    }
                  },
                  "sort": [
                    "Update project"
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
<!-- vale off -->
## 使用 inner_hits 的優點
<!-- vale on -->
* **詳細的查詢結果**

    您可以使用 `inner_hits` 直接從父文件的搜尋結果中，取得符合條件的巢狀或子文件的詳細資訊。這對於了解相符項目的內容與細節特別有用，且無須執行額外的查詢。
    
    範例使用情境：在部落格文章索引中，您將留言作為巢狀物件。當搜尋包含特定留言的部落格文章時，您可以取得符合搜尋條件的相關留言，以及該文章的相關資訊。

* **最佳化的效能**

    若不使用 `inner_hits`，您可能需要執行多個查詢才能取得相關文件。使用 `inner_hits` 可將這些查詢合併為單一查詢，減少與 OpenSearch 伺服器之間的來回次數，並改善整體效能。

    範例使用情境：在電子商務應用程式中，您將產品作為父文件，並將評論作為子文件。使用 `inner_hits` 的單一查詢即可取得產品及其相關評論，避免多個個別查詢。

* **簡化的查詢邏輯**

    您可以將父/子或巢狀文件邏輯合併在單一查詢中，以簡化應用程式程式碼並降低複雜度。將查詢邏輯集中於 OpenSearch 有助於確保程式碼更容易維護且更一致

    範例使用情境：在人力銀行網站中，您將職缺作為父文件，並將應徵記錄作為巢狀或子文件。您可以透過單一查詢取得職缺及其特定應徵記錄，以簡化應用程式邏輯。

* **情境相關性**

    使用 `inner_hits` 可顯示哪些巢狀或子文件確實符合查詢條件，藉此提供情境相關性。對於結果相關性取決於文件中符合查詢之特定部分的應用程式而言，這至關重要。

    範例使用情境：在客戶支援系統中，您將工單作為父文件，並將留言或更新作為巢狀或子文件。您可以判斷哪一則特定留言符合搜尋，以便更了解工單搜尋的情境。

## 後續步驟

- 了解如何在 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 或 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位上使用[聯結查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)。