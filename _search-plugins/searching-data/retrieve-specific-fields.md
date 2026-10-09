---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
parent: Customizing search results
title: "擷取特定欄位"
nav_order: 50
---

# 擷取特定欄位

當您在 OpenSearch 中執行基本搜尋時，預設也會在回應中，於每筆命中結果的 `_source` 物件內傳回編製索引時所使用的原始 JSON 物件。這可能導致透過網路傳輸大量資料，增加延遲與成本。有數種方法可將回應限制為僅包含所需的資訊。

<!-- vale off -->
## 停用 _source
<!-- vale on -->
您可以在搜尋請求中將 `_source` 設定為 `false`，以便從回應中排除 `_source` 欄位：

```json
GET /index1/_search
{
    "_source": false,
    "query": {
        "match_all": {}
  }
}
```
{% include copy-curl.html %}

由於先前的搜尋未選取任何欄位，擷取到的命中結果只會包含每個命中的 `_index`、`_id` 與 `_score`：

```json
{
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "index1",
        "_id" : "41",
        "_score" : 1.0
      },
      {
        "_index" : "index1",
        "_id" : "51",
        "_score" : 1.0
      }
    ]
  }
}
```

您也可以在索引對應中使用下列組態來停用 `_source`：

```json
"mappings": {
  "_source": {
    "enabled": false
  }
}
```

<!-- vale off -->
如果 `_source` 在索引對應中已停用，[使用 docvalue 欄位搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-doc-value-fields)與[使用 stored 欄位搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored-fields)就會變得非常有用。
<!-- vale on -->

## 指定要擷取的欄位

您可以在 `fields` 參數中列出想要擷取的欄位。也接受萬用字元模式：

```json
GET /index1/_search
{
    "_source": false,
    "fields": ["age", "nam*"],
    "query": {
        "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應包含 `name` 與 `age` 欄位：

```json
{
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "index1",
        "_id" : "41",
        "_score" : 1.0,
        "fields" : {
          "name" : [
            "John Doe"
          ],
          "age" : [
            30
          ]
        }
      },
      {
        "_index" : "index1",
        "_id" : "51",
        "_score" : 1.0,
        "fields" : {
          "name" : [
            "Jane Smith"
          ],
          "age" : [
            25
          ]
        }
      }
    ]
  }
}
```

### 以自訂格式擷取欄位

您也可以使用物件表示法，為所選欄位套用自訂格式。

如果您有下列文件：

```json
{
  "_index": "my_index",
  "_type": "_doc",
  "_id": "1",
  "_source": {
    "title": "Document 1",
    "date": "2023-07-04T12:34:56Z"
  }
}
```

則您可以使用 `fields` 參數與自訂格式進行查詢：

```json
GET /my_index/_search
{
  "query": {
    "match_all": {}
  },
  "fields": [
    {
      "field": "date",
      "format": "yyyy-MM-dd"
    }
  ],
  "_source": false
}
```
{% include copy-curl.html %}

此外，您可以在 `fields` 參數中使用[大多數欄位]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/#most-fields)與[欄位別名]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/alias/)，因為它會同時查詢文件的 `_source` 與索引的 `_mappings`。

## 使用 doc value 欄位搜尋

若要從索引擷取特定欄位，您也可以使用 `docvalue_fields` 參數。此參數的運作方式與 `fields` 參數略有不同。它從 doc values 而非 `_source` 欄位擷取資訊，對於未經分析的欄位（例如 keyword、date 與數值欄位）而言更有效率。Doc values 採用針對高效排序與彙總最佳化的欄式儲存格式。它以易於讀取的方式將值儲存在磁碟上。當您使用 `docvalue_fields` 時，OpenSearch 會直接從這個最佳化的儲存格式讀取值。它適合用來擷取主要用於排序、彙總以及指令碼中的欄位值。

下列範例示範如何使用 `docvalue_fields` 參數。


1. 使用下列對應建立索引：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "title": { "type": "text" },
          "author": { "type": "keyword" },
          "publication_date": { "type": "date" },
          "price": { "type": "double" }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將下列文件編製索引到新建立的索引中：

    ```json
    POST /my_index/_doc/1
    {
      "title": "OpenSearch Basics",
      "author": "John Doe",
      "publication_date": "2021-01-01",
      "price": 29.99
    }
    ```
    {% include copy-curl.html %}
    
    ```json
    POST /my_index/_doc/2
    {
      "title": "Advanced OpenSearch",
      "author": "Jane Smith",
      "publication_date": "2022-01-01",
      "price": 39.99
    }
    ```
    {% include copy-curl.html %}

3. 使用 `docvalue_fields` 僅擷取 `author` 與 `publication_date` 欄位：

    ```json
    POST /my_index/_search
    {
      "_source": false,
      "docvalue_fields": ["author", "publication_date"],
      "query": {
        "match_all": {}
      }
    }
    ```
    {% include copy-curl.html %}

回應包含 `author` 與 `publication_date` 欄位：

```json
{
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "author": ["John Doe"],
          "publication_date": ["2021-01-01T00:00:00.000Z"]
        }
      },
      {
        "_index": "my_index",
        "_id": "2",
        "_score": 1.0,
        "fields": {
          "author": ["Jane Smith"],
          "publication_date": ["2022-01-01T00:00:00.000Z"]
        }
      }
    ]
  }
}
```
<!-- vale off -->
### 使用 docvalue_fields 擷取向量欄位
<!-- vale on -->
**3.7 版新增**
{: .label .label-purple }

您可以使用 `docvalue_fields` 而非 `_source` 來擷取 `knn_vector` 欄位。這樣速度更快，因為 OpenSearch 直接從 `doc_values` 讀取向量，而不是剖析完整的 `_source` 文件。

從 `doc_values` 擷取 `knn_vector` 欄位支援所有向量資料類型（`float`、`byte` 與 `binary`）、所有壓縮層級，以及所有 k-NN 引擎（Lucene、Faiss 與 NMSLIB）。您可以在現有索引上使用它，無需重新編製索引。

如需效能調校指引，請參閱[使用 doc values 擷取向量]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-search/#retrieve-vectors-using-doc-values)。

支援下列輸出格式。

| 格式 | 說明 |
| :--- | :--- |
| `binary`（預設） | 以 Base64 編碼的小端序位元組字串傳回向量。在 JSON 傳輸時，相較於 `array` 格式可提供約 2 倍的輸送量提升，並將回應承載大小減少 30--40%。 |
| `array` | 以 JSON 數值陣列傳回向量。 |

若要使用 `docvalue_fields` 擷取向量欄位，請依照下列步驟操作：

1. 建立含有 `knn_vector` 欄位的索引：

    ```json
    PUT /my_vector_index
    {
      "settings": {
        "index.knn": true
      },
      "mappings": {
        "properties": {
          "my_vector": {
            "type": "knn_vector",
            "dimension": 4
          },
          "title": {
            "type": "text"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 編製索引一份文件：

    ```json
    POST /my_vector_index/_doc/1
    {
      "my_vector": [1.0, 2.0, 3.0, 4.0],
      "title": "Sample document"
    }
    ```
    {% include copy-curl.html %}

3. 使用 `docvalue_fields` 以預設的 `binary` 格式擷取向量：

    ```json
    POST /my_vector_index/_search
    {
      "_source": false,
      "docvalue_fields": ["my_vector"],
      "query": {
        "knn": {
          "my_vector": {
            "vector": [1.0, 2.0, 3.0, 4.0],
            "k": 5
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

    回應會以 Base64 編碼字串傳回向量：

    ```json
    {
      "hits": {
        "hits": [
          {
            "_id": "1",
            "_score": 1.0,
            "fields": {
              "my_vector": ["AACAPwAAAEAAAEBAAACAQA=="]
            }
          }
        ]
      }
    }
    ```

4. 若要以 JSON 數值陣列擷取向量，請指定 `array` 格式：

    ```json
    POST /my_vector_index/_search
    {
      "_source": false,
      "docvalue_fields": [{"field": "my_vector", "format": "array"}],
      "query": {
        "knn": {
          "my_vector": {
            "vector": [1.0, 2.0, 3.0, 4.0],
            "k": 5
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

    回應會以數值陣列傳回向量：

    ```json
    {
      "hits": {
        "hits": [
          {
            "_id": "1",
            "_score": 1.0,
            "fields": {
              "my_vector": [[1.0, 2.0, 3.0, 4.0]]
            }
          }
        ]
      }
    }
    ```

若要在使用 `doc_values` 擷取向量的同時，從 `_source` 擷取其他文件欄位，請將向量欄位從 `_source` 中排除：

```json
POST /my_vector_index/_search
{
  "_source": {
    "excludes": ["my_vector"]
  },
  "docvalue_fields": [{"field": "my_vector", "format": "array"}],
  "query": {
    "knn": {
      "my_vector": {
        "vector": [1.0, 2.0, 3.0, 4.0],
        "k": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

<!-- vale off -->
### 搭配巢狀物件使用 docvalue_fields
<!-- vale on -->

在 OpenSearch 中，如果您想擷取巢狀物件的 doc values，不能直接使用 `docvalue_fields` 參數，因為它會傳回空陣列。您應改用 `inner_hits` 參數並搭配其自身的 `docvalue_fields` 屬性，如下列範例所示。

1. 定義索引對應：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "title": { "type": "text" },
          "author": { "type": "keyword" },
          "comments": {
            "type": "nested",
            "properties": {
              "username": { "type": "keyword" },
              "content": { "type": "text" },
              "created_at": { "type": "date" }
            }
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將您的資料編製索引：

    ```json
    POST /my_index/_doc/1
    {
      "title": "OpenSearch Basics",
      "author": "John Doe",
      "comments": [
        {
          "username": "alice",
          "content": "Great article!",
          "created_at": "2023-01-01T12:00:00Z"
        },
        {
          "username": "bob",
          "content": "Very informative.",
          "created_at": "2023-01-02T12:00:00Z"
        }
      ]
    }
    ```
    {% include copy-curl.html %}

3. 使用 `inner_hits` 和 `docvalue_fields` 執行搜尋：

    ```json
    POST /my_index/_search
    {
      "query": {
        "nested": {
          "path": "comments",
          "query": {
            "match_all": {}
          },
          "inner_hits": {
            "docvalue_fields": ["username", "created_at"]
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "title": "OpenSearch Basics",
          "author": "John Doe",
          "comments": [
            {
              "username": "alice",
              "content": "Great article!",
              "created_at": "2023-01-01T12:00:00Z"
            },
            {
              "username": "bob",
              "content": "Very informative.",
              "created_at": "2023-01-02T12:00:00Z"
            }
          ]
        },
        "inner_hits": {
          "comments": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "my_index",
                  "_id": "1",
                  "_nested": {
                    "field": "comments",
                    "offset": 0
                  },
                  "docvalue_fields": {
                    "username": ["alice"],
                    "created_at": ["2023-01-01T12:00:00Z"]
                  }
                },
                {
                  "_index": "my_index",
                  "_id": "1",
                  "_nested": {
                    "field": "comments",
                    "offset": 1
                  },
                  "docvalue_fields": {
                    "username": ["bob"],
                    "created_at": ["2023-01-02T12:00:00Z"]
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

## 使用已儲存欄位搜尋

根據預設，OpenSearch 會將整份文件儲存在 `_source` 欄位中，並用它來在搜尋結果中傳回文件內容。不過，您可能也想個別儲存特定欄位，以提升擷取效率。您可以使用 `stored_fields`，將特定文件欄位與 `_source` 欄位分開個別儲存及擷取。

與 `_source` 不同，`stored_fields` 必須在您想個別儲存的欄位對應中明確定義。如果您經常只需要擷取一小部分的欄位，並想避免擷取整個 `_source` 欄位，這個做法就很實用。下列範例示範如何使用 `stored_fields` 參數。

1. 使用下列對應建立索引：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "store": true  // Store the title field separately
          },
          "author": {
            "type": "keyword",
            "store": true  // Store the author field separately
          },
          "publication_date": {
            "type": "date"
          },
          "price": {
            "type": "double"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將您的資料編製索引：

    ```json
    POST /my_index/_doc/1
    {
      "title": "OpenSearch Basics",
      "author": "John Doe",
      "publication_date": "2022-01-01",
      "price": 29.99
    }
    ```
    {% include copy-curl.html %}
    
    ```json
    POST my_index/_doc/2
    {
      "title": "Advanced OpenSearch",
      "author": "Jane Smith",
      "publication_date": "2023-01-01",
      "price": 39.99
    }
    ```
    {% include copy-curl.html %}

3. 使用 `stored_fields` 執行搜尋：

    ```json
    POST /my_index/_search
    {
      "_source": false,
      "stored_fields": ["title", "author"],
      "query": {
        "match_all": {}
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "title": ["OpenSearch Basics"],
          "author": ["John Doe"]
        }
      },
      {
        "_index": "my_index",
        "_id": "2",
        "_score": 1.0,
        "fields": {
          "title": ["Advanced OpenSearch"],
          "author": ["Jane Smith"]
        }
      }
    ]
  }
}
```

將 `stored_fields` 設為 `_none_`，即可完全停用 `stored_fields` 參數。
{: .note}
### 使用巢狀物件搜尋已儲存欄位

在 OpenSearch 中，如果您想擷取巢狀物件的 `stored_fields`，不能直接使用 `stored_fields` 參數，因為不會傳回任何資料。您應改用 `inner_hits` 參數並搭配其自身的 `stored_fields` 屬性，如下列範例所示。

1. 使用下列對應建立索引：

    ```json
    PUT /my_index
    {
      "mappings": {
        "properties": {
          "title": { "type": "text" },
          "author": { "type": "keyword" },
          "comments": {
            "type": "nested",
            "properties": {
              "username": { "type": "keyword", "store": true },
              "content": { "type": "text", "store": true },
              "created_at": { "type": "date", "store": true }
            }
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 將您的資料編製索引：

    ```json
    POST /my_index/_doc/1
    {
      "title": "OpenSearch Basics",
      "author": "John Doe",
      "comments": [
        {
          "username": "alice",
          "content": "Great article!",
          "created_at": "2023-01-01T12:00:00Z"
        },
        {
          "username": "bob",
          "content": "Very informative.",
          "created_at": "2023-01-02T12:00:00Z"
        }
      ]
    }
    ```
    {% include copy-curl.html %}

3. 使用 `inner_hits` 和 `stored_fields` 執行搜尋：

    ```json
    POST /my_index/_search
    {
      "_source": false,
      "query": {
        "nested": {
          "path": "comments",
          "query": {
            "match_all": {}
          },
          "inner_hits": {
            "stored_fields": ["comments.username", "comments.content", "comments.created_at"]
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "inner_hits": {
          "comments": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "my_index",
                  "_id": "1",
                  "_nested": {
                    "field": "comments",
                    "offset": 0
                  },
                  "fields": {
                    "comments.username": ["alice"],
                    "comments.content": ["Great article!"],
                    "comments.created_at": ["2023-01-01T12:00:00.000Z"]
                  }
                },
                {
                  "_index": "my_index",
                  "_id": "1",
                  "_nested": {
                    "field": "comments",
                    "offset": 1
                  },
                  "fields": {
                    "comments.username": ["bob"],
                    "comments.content": ["Very informative."],
                    "comments.created_at": ["2023-01-02T12:00:00.000Z"]
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

## 使用來源篩選

來源篩選是一種控制搜尋回應中包含 `_source` 欄位哪些部分的方式。在回應中只包含必要的欄位，有助於減少透過網路傳輸的資料量並提升效能。

您可以使用完整欄位名稱或簡單的萬用字元模式，在搜尋回應中包含或排除 `_source` 欄位中的特定欄位。以下範例示範如何包含特定欄位。

1. 將資料編製索引：

    ```json
    PUT /my_index/_doc/1
    {
      "title": "OpenSearch Basics",
      "author": "John Doe",
      "publication_date": "2021-01-01",
      "price": 29.99
    }
    ```
    {% include copy-curl.html %}

2. 使用來源篩選執行搜尋：

    ```json
    POST /my_index/_search
    {
      "_source": ["title", "author"],
      "query": {
        "match_all": {}
      }
    }
    ```
    {% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "title": "OpenSearch Basics",
          "author": "John Doe"
        }
      }
    ]
  }
}
```

### 使用來源篩選排除欄位

您可以選擇在搜尋請求中使用 `"excludes"` 參數來排除欄位，如下列範例所示：

```json
POST /my_index/_search
{
  "_source": {
    "excludes": ["price"]
  },
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "title": "OpenSearch Basics",
          "author": "John Doe",
          "publication_date": "2021-01-01"
        }
      }
    ]
  }
}
```

### 在同一個搜尋中包含與排除欄位

在某些情況下，可能需要同時使用 `include` 與 `exclude` 參數。當某個欄位同時符合兩個清單中的模式時，OpenSearch 會省略該欄位，因為 `excludes` 的優先順序高於 `includes`。以下範例示範如何在同一個搜尋中包含與排除欄位。

假設有一個包含下列文件的 `products` 索引：

```json
{
  "product_id": "123",
  "name": "Smartphone",
  "category": "Electronics",
  "price": 699.99,
  "description": "A powerful smartphone with a sleek design.",
  "reviews": [
    {
      "user": "john_doe",
      "rating": 5,
      "comment": "Great phone!",
      "date": "2023-01-01"
    },
    {
      "user": "jane_doe",
      "rating": 4,
      "comment": "Good value for money.",
      "date": "2023-02-15"
    }
  ],
  "supplier": {
    "name": "TechCorp",
    "contact_email": "support@techcorp.com",
    "address": {
      "street": "123 Tech St",
      "city": "Techville",
      "zipcode": "12345"
    }
  },
  "inventory": {
    "stock": 50,
    "warehouse_location": "A1"
  }
}
```

若要在這個索引上執行搜尋，並且在回應中只包含 `name`、`price`、`reviews` 和 `supplier` 欄位，同時排除 `supplier` 物件中的 `contact_email` 欄位以及 `reviews` 物件中的 `comment` 欄位，請執行下列搜尋：

```json
GET /products/_search
{
  "_source": {
    "includes": ["name", "price", "reviews.*", "supplier.*"],
    "excludes": ["reviews.comment", "supplier.contact_email"]
  },
  "query": {
    "match": {
      "category": "Electronics"
    }
  }
}
```
{% include copy-curl.html %}

以下是預期的回應：

```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "name": "Smartphone",
          "price": 699.99,
          "reviews": [
            {
              "user": "john_doe",
              "rating": 5,
              "date": "2023-01-01"
            },
            {
              "user": "jane_doe",
              "rating": 4,
              "date": "2023-02-15"
            }
          ],
          "supplier": {
            "name": "TechCorp",
            "address": {
              "street": "123 Tech St",
              "city": "Techville",
              "zipcode": "12345"
            }
          }
        }
      }
    ]
  }
}
```

### 來源篩選的限制

來源篩選會比對原始 JSON 文件中的欄位名稱，因此無法傳回 OpenSearch 在編製索引期間衍生的值。多欄位（multi-fields）、[欄位別名]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/alias/)以及由 `copy_to` 填入的欄位都不是來源的一部分，對這些欄位的請求會傳回空的 `_source` 物件。

即使請求只要求少數幾個欄位，OpenSearch 仍會載入並解析整個來源文件，因此來源篩選能減少網路傳輸量，但無法減少磁碟讀取。若要直接從索引讀取個別欄位，請使用 [`docvalue_fields`](#searching-with-doc-value-fields) 或 [`stored_fields`](#searching-with-stored-fields)。

## 使用指令碼欄位

`script_fields` 參數可讓您在搜尋結果中包含自訂欄位，其值是使用指令碼計算而得。這對於根據文件資料動態計算數值非常有用。您也可以使用類似的方式擷取 `derived fields`。如需更多資訊，請參閱[擷取欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/#retrieving-fields)。

假設您有一個產品索引，其中每個產品文件都包含 `price` 和 `discount_percentage` 欄位。您可以使用 `script_fields` 參數，在搜尋結果中包含一個顯示每項產品折扣價格的自訂欄位。以下範例示範如何使用 `script_fields` 參數：


1. 將資料編製索引：

    ```json
    PUT /products/_doc/123
    {
      "product_id": "123",
      "name": "Smartphone",
      "price": 699.99,
      "discount_percentage": 10,
      "category": "Electronics",
      "description": "A powerful smartphone with a sleek design."
    }
    ```
    {% include copy-curl.html %}

2. 使用 `script_fields` 參數，在搜尋結果中包含名為 `discounted_price` 的自訂欄位。此欄位將使用指令碼根據 `price` 和 `discount_percentage` 欄位計算而得：

    ```json
    GET /products/_search
    {
      "_source": ["product_id", "name", "price", "discount_percentage"],
      "query": {
        "match": {
          "category": "Electronics"
        }
      },
      "script_fields": {
        "discounted_price": {
          "script": {
            "lang": "painless",
            "source": "doc[\"price\"].value * (1 - doc[\"discount_percentage\"].value / 100)"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

您應該會收到下列回應：

```json
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "products",
        "_id": "123",
        "_score": 1.0,
        "_source": {
          "product_id": "123",
          "name": "Smartphone",
          "price": 699.99,
          "discount_percentage": 10
        },
        "fields": {
          "discounted_price": [629.991]
        }
      }
    ]
  }
}
```
