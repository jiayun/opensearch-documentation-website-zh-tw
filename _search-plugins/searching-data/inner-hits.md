---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "擷取內部命中結果"
parent: Customizing search results
has_children: false
nav_order: 60
---

# 擷取內部命中

在 OpenSearch 中，當您使用 [巢狀物件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 或 [parent-join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 執行搜尋時，底層的命中結果（巢狀內部物件或子文件）預設會被隱藏。您可以在搜尋查詢中使用 `inner_hits` 參數來擷取內部命中。

請在下列情境中使用內部命中：

- 識別是哪些巢狀物件或子文件導致文件符合條件，例如，包含搜尋字詞的網誌文章留言，或符合查詢的支援工單更新。
- 在單一請求中同時擷取文件及其符合條件的巢狀物件或子文件，例如，產品及其符合條件的評論，或職缺及其符合條件的應徵。這可避免針對相關文件另外傳送查詢。

您也可以將 `inner_hits` 與下列功能搭配使用：

  - [突顯查詢符合項目]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)
  - [Explain]({{site.url}}{{site.baseurl}}/api-reference/explain/)

## 巢狀物件中的內部命中

巢狀物件可讓您為物件陣列編製索引，並在同一份文件中維持其關聯性。下列範例請求使用 `inner_hits` 參數來擷取基礎的內部命中。

1. 建立含有巢狀物件的索引對應：

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

3. 使用 `inner_hits` 查詢：

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

前述查詢會搜尋包含名稱 John 的巢狀使用者物件，並在回應的 `inner_hits` 區段中傳回相符的巢狀文件：

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
### 識別符合條件的巢狀物件

巢狀物件的每個 inner hit 都包含一個 `_nested` 物件，用來識別符合條件的巢狀物件。`field` 屬性包含巢狀欄位的名稱，`offset` 屬性則包含該物件在原始文件中該欄位陣列裡的位置，從 `0` 開始計算。在前述回應中，`0` 的 `offset` 表示此 inner hit 是 `user` 陣列中的第一個物件。由於 inner hits 會依分數或您指定的排序方式排序，inner hits 的順序通常與文件中物件的順序不同，因此請使用 `offset` 來識別原始物件。

預設情況下，每個 inner hit 的 `_source` 只包含符合條件的巢狀物件，而非整份來源文件。您可以使用[來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)變更傳回的欄位、為 inner hits 停用 `_source`，或在 `inner_hits` 的 `stored_fields` 中指定欄位，以傳回巢狀物件的[儲存欄位]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/)。

### 擷取巢狀內部命中而不使用來源

巢狀物件不會個別儲存：其來源是父文件來源的一部分。若要傳回巢狀內部命中的 `_source`，OpenSearch 會解析父文件的來源並擷取相符的物件。對每個內部命中都這麼做會增加搜尋時間，特別是當您為搜尋或為 `inner_hits` 增加 `size` 時。若要避免此成本，請為內部命中停用 `_source`，改為從 doc values 擷取欄位值。

下列範例使用包含巢狀 `comments` 的 `articles` 索引。建立索引並新增文件：

```json
PUT /articles
{
  "mappings": {
    "properties": {
      "comments": {
        "type": "nested",
        "properties": {
          "author": { "type": "keyword" },
          "text": { "type": "text" },
          "reactions": {
            "type": "nested",
            "properties": {
              "user": { "type": "keyword" },
              "emoji": { "type": "keyword" }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /articles/_doc/1?refresh=true
{
  "title": "Choosing a backpacking tent",
  "comments": [
    {
      "author": "ana",
      "text": "Great overview of tent weights",
      "reactions": []
    },
    {
      "author": "ben",
      "text": "Which tent survives strong wind?",
      "reactions": [
        { "user": "ana", "emoji": "thumbs_up" },
        { "user": "chen", "emoji": "heart" }
      ]
    }
  ]
}
```
{% include copy-curl.html %}

下列請求會尋找提及 `wind` 的留言，並從 doc values 只傳回每個相符留言的 `author`：

```json
GET /articles/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "comments",
      "query": {
        "match": { "comments.text": "wind" }
      },
      "inner_hits": {
        "_source": false,
        "docvalue_fields": ["comments.author"]
      }
    }
  }
}
```
{% include copy-curl.html %}

內部命中會包含 `fields` 物件，而非 `_source`：

```json
"inner_hits": {
  "comments": {
    "hits": {
      "total": {
        "value": 1,
        "relation": "eq"
      },
      "max_score": 0.31506687,
      "hits": [
        {
          "_index": "articles",
          "_id": "1",
          "_nested": {
            "field": "comments",
            "offset": 1
          },
          "_score": 0.31506687,
          "fields": {
            "comments.author": [
              "ben"
            ]
          }
        }
      ]
    }
  }
}
```

### 多層巢狀物件的內部命中

如果巢狀物件包含其他巢狀物件，您可以在 `nested` 查詢中指定完整的點分隔路徑，以傳回任一層級的內部命中。下列請求會傳回使用者 `ana` 的回應反應，這些反應巢狀於 `comments.reactions` 中：

```json
GET /articles/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "comments.reactions",
      "query": {
        "term": { "comments.reactions.user": "ana" }
      },
      "inner_hits": {}
    }
  }
}
```
{% include copy-curl.html %}

內部命中會以完整路徑命名。每個內部命中的 `_nested` 物件會針對每個層級包含另一個 `_nested` 物件。在此回應中，該反應是第二則留言（`offset` `1`）的 `reactions` 陣列中的第一個物件（`offset` `0`）：

```json
{
  "took": 4,
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
        "_index": "articles",
        "_id": "1",
        "_score": 1,
        "inner_hits": {
          "comments.reactions": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1,
              "hits": [
                {
                  "_index": "articles",
                  "_id": "1",
                  "_nested": {
                    "field": "comments",
                    "offset": 1,
                    "_nested": {
                      "field": "reactions",
                      "offset": 0
                    }
                  },
                  "_score": 1,
                  "_source": {
                    "emoji": "thumbs_up",
                    "user": "ana"
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

## 父子物件的內部命中

父聯結 (parent-join) 關係可讓您在同一索引內建立不同類型文件之間的關係。以下範例請求使用 `inner_hits` 搭配父子物件進行搜尋。

1. 建立一個包含父聯結欄位的索引：

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

2. 為資料編製索引：

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

前述查詢會搜尋擁有符合查詢條件之子文件的父文件（在此範例中，即包含詞元 `"child"` 的文件）。它會在回應的 `inner_hits` 區段中傳回符合條件的子文件：

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

您也可以在 [`has_parent`]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-parent/) 查詢中指定 `inner_hits`。在此情況下，查詢會傳回子文件，而每個子文件的內部命中會包含其符合條件的父文件。

## 同時搭配父子聯結與巢狀物件使用內部命中

以下範例示範如何搭配 `inner_hits` 同時使用父子聯結與巢狀物件。

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

3. 使用 `inner_hits` 查詢：

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

前述查詢會搜尋具有子文件的父文件，且這些子文件包含 John 所留下的留言。指定 `inner_hits` 可確保傳回相符的子文件及其巢狀留言：

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

## Inner hits 參數

下表列出您可以在 `inner_hits` 中為巢狀物件與 parent-join 關係指定的參數。

參數 | 說明
:--- | :---
`from` | 開始傳回 inner hits 的位移。預設為 `0`。
`size` | 要傳回的 inner hits 數量上限。預設為 `3`。
`sort` | inner hits 的排序方式。預設情況下，inner hits 依相關性分數排序。
`name` | 回應中 inner hits 的自訂名稱。可用於區分單一查詢中的多個 inner hits。預設情況下，對於 `nested` 查詢，名稱為巢狀 `path`；對於 `has_child` 查詢，名稱為子關係名稱；對於 `has_parent` 查詢，名稱為父關係名稱。

Inner hits 也接受您可為搜尋請求的命中結果指定的許多選項，包括 [`highlight`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)、`explain`、[來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)、[`script_fields`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields)、[`docvalue_fields`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-doc-value-fields)、`version` 與 `seq_no_primary_term`。巢狀物件不會被指派序號，因此 OpenSearch 會拒絕 `nested` 查詢之 inner hits 中的 `seq_no_primary_term`。

### 範例：搭配巢狀物件的 inner hits 參數

1. 建立具有下列對應的索引：

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

3. 使用 `inner_hits` 查詢並提供其他參數：

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

預期結果如下：

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

### 範例：具有父子聯結關係的內部命中參數

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
## 後續步驟

- 了解如何在 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 或 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位上使用[聯結查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)。