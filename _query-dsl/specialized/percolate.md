---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Percolate
parent: Specialized queries
nav_order: 55
---

# Percolate 查詢

使用 `percolate` 查詢來尋找符合指定文件的已儲存查詢。此操作與一般搜尋相反：一般搜尋是尋找符合查詢的文件，而此操作則是尋找符合文件的所有查詢。`percolate` 查詢常用於警示、通知及反向搜尋等使用情境。

使用 `percolate` 查詢時，請考量下列重點：

- 您可以比對內嵌提供的文件，或從索引擷取現有文件進行比對。
- 文件與已儲存的查詢必須使用相同的欄位名稱與類型。
- 您可以結合反向比對、篩選與評分，以建立複雜的比對系統。
- `percolate` 查詢被視為[高成本查詢]({{site.url}}{{site.baseurl}}/query-dsl/#expensive-queries)，只有在叢集設定 `search.allow_expensive_queries` 設為 `true` (預設) 時才會執行。若此設定為 `false`，`percolate` 查詢將會被拒絕。

`percolate` 查詢在各種即時比對情境中相當實用。常見的使用情境包括：

- **電子商務通知**：使用者可以註冊對產品的關注，例如「當新的 Apple 筆記型電腦到貨時通知我」。當新的產品文件被編製索引時，系統會找出所有具有相符已儲存查詢的使用者並傳送警示。
- **職缺警示**：求職者根據偏好的職稱或地點儲存查詢，新的職缺張貼時會與這些查詢進行比對以觸發警示。
- **安全性與警示系統**：將傳入的記錄資料或事件資料與已儲存的規則或異常模式進行比對。
- **新聞篩選**：將傳入的文章與已儲存的主題設定檔進行比對，以分類或遞送相關內容。

## 反向比對的運作方式

1. 已儲存的查詢會儲存在特殊的 [`percolator` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/) 中。
2. 文件會與所有已儲存的查詢進行比對。
3. 每個相符的查詢會連同其 `_id` 一併傳回。
4. 若已啟用醒目提示，也會傳回相符的文字片段。
5. 若傳送多份文件，`_percolator_document_slot` 會顯示相符的文件。

## 範例

下列範例示範如何使用不同的方法儲存 `percolate` 查詢，並以測試文件與這些查詢進行比對。

### 建立用於儲存已儲存查詢的索引

首先，建立索引並使用 [`percolator` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/) 設定其 `mappings`，以儲存已儲存的查詢：

```json
PUT /my_percolator_index
{
  "mappings": {
    "properties": {
      "query": {
        "type": "percolator"
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

新增一個在 `title` 欄位中比對「apple」的查詢：

```json
POST /my_percolator_index/_doc/1
{
  "query": {
    "match": {
      "title": "apple"
    }
  }
}
```
{% include copy-curl.html %}

新增一個在 `title` 欄位中比對「banana」的查詢：

```json
POST /my_percolator_index/_doc/2
{
  "query": {
    "match": {
      "title": "banana"
    }
  }
}
```
{% include copy-curl.html %}

### 比對內嵌文件

以內嵌文件與已儲存的查詢進行測試：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "document": {
        "title": "Fresh Apple Harvest"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會提供已儲存的 `percolate` 查詢，該查詢會在 `title` 欄位中搜尋包含「apple」一詞的文件，並以 `_id` 識別：`1`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        }
      }
    ]
  }
}
```

### 比對多份文件

若要在同一個查詢中測試多份文件，請使用下列請求：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "documents": [
        { "title": "Banana flavoured ice-cream" },
        { "title": "Apple pie recipe" },
        { "title": "Banana bread instructions" },
        { "title": "Cherry tart" }
      ]
    }
  }
}
```
{% include copy-curl.html %}

`_percolator_document_slot` 欄位可協助您依文件在陣列中的索引位置，識別符合各個已儲存查詢的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.54726034,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.54726034,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            1
          ]
        }
      },
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.31506687,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0,
            2
          ]
        }
      }
    ]
  }
}
```

### 比對現有已編製索引的文件

您可以參照已儲存在另一個索引中的現有文件，以檢查是否有相符的 `percolate` 查詢。

為您的文件建立個別的索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

新增文件：

```json
POST /products/_doc/1
{
  "title": "Banana Smoothie Special"
}
```
{% include copy-curl.html %}

檢查已儲存的查詢是否符合已編製索引的文件：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "index": "products",
      "id": "1"
    }
  }
}
```
{% include copy-curl.html %}

使用已儲存的文件時，您必須同時提供 `index` 與 `id`。
{: .note}

對應的查詢會傳回：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        }
      }
    ]
  }
}
```

### 批次反向比對（多份文件）

您可以在同一個請求中檢查多份文件：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "documents": [
        { "title": "Apple event coming soon" },
        { "title": "Banana farms expand" },
        { "title": "Cherry season starts" }
      ]
    }
  }
}
```
{% include copy-curl.html %}

每個相符項目會在 `_percolator_document_slot` 欄位中指出相符的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.46484798,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.46484798,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            1
          ]
        }
      },
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.41211313,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        }
      }
    ]
  }
}
```

### 使用具名查詢進行多重反向比對

您可以在具名查詢中比對不同的文件：

```json
GET /my_percolator_index/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "percolate": {
            "field": "query",
            "document": {
              "title": "Apple pie recipe"
            },
            "name": "apple_doc"
          }
        },
        {
          "percolate": {
            "field": "query",
            "document": {
              "title": "Banana bread instructions"
            },
            "name": "banana_doc"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

`name` 參數會附加到 `_percolator_document_slot`，以提供相符的查詢：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot_apple_doc": [
            0
          ]
        }
      },
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot_banana_doc": [
            0
          ]
        }
      }
    ]
  }
}
```

這種方式可讓您為個別文件設定更多自訂的查詢邏輯。在下列範例中，第一份文件查詢 `title` 欄位，第二份文件查詢 `description` 欄位。同時也提供了 `boost` 參數：

```json
GET /my_percolator_index/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "constant_score": {
            "filter": {
              "percolate": {
                "field": "query",
                "document": {
                  "title": "Apple pie recipe"
                },
                "name": "apple_doc"
              }
            },
            "boost": 1.0
          }
        },
        {
          "constant_score": {
            "filter": {
              "percolate": {
                "field": "query",
                "document": {
                  "description": "Banana bread with honey"
                },
                "name": "banana_doc"
              }
            },
            "boost": 3.0
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}


## 批次反向比對與具名反向比對的比較

批次反向比對（使用 `documents`）與具名反向比對（使用 `bool` 搭配 `name`）都可用來比對多份文件，但兩者在結果的標記、解讀與控制方式上有所不同。它們提供的結果在功能上相似，但在結構上有重要差異，如下表所述。

| 功能                        | 批次 (`documents`)                            | 具名 (`bool` + `percolate` + `name`)            |
|-------------------------------|------------------------------------------------|--------------------------------------------------|
| 輸入格式                  | 一個 percolate 子句，文件陣列       | 多個 percolate 子句，每份文件一個     |
| 每份文件的可追蹤性     | 依槽位索引 (0, 1, ...)                      | 依名稱 (`apple_doc`, `banana_doc`)        |
| 相符槽位的回應欄位 | `_percolator_document_slot: [0]`              | `_percolator_document_slot_<name>: [0]`          |
| 突顯前置詞              | `0_title`, `1_title`                           | `apple_doc_title`, `banana_doc_title`            |
| 每份文件的自訂控制        | 不支援                                | 可自訂每個子句                     |
| 支援加權與篩選     | 否                                           | 是（每個子句）                              |
| 效能                   | 最適合大批次                      | 子句較多時稍慢              |
| 使用情境                      | 大量比對工作、大型事件串流        | 逐文件追蹤、測試、自訂控制    |


## 突顯相符項目

`percolate` 查詢處理突顯的方式與一般查詢不同：

- 在一般查詢中，文件儲存在索引中，並使用搜尋查詢來突顯相符的詞彙。
- 在 `percolate` 查詢中，角色是反過來的：使用已儲存的查詢（在 percolator 索引中）來突顯文件。

這表示在 `document` 或 `documents` 中提供的文件是突顯的目標，而 `percolate` 查詢決定要突顯的區段。

### 突顯單一文件

此範例使用 `my_percolator_index` 中先前定義的搜尋。請使用下列請求來突顯 `title` 欄位中的相符項目：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "document": {
        "title": "Apple banana smoothie"
      }
    }
  },
  "highlight": {
    "fields": {
      "title": {}
    }
  }
}
```
{% include copy-curl.html %}

相符項目會依據所符合的查詢進行突顯：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        },
        "highlight": {
          "title": [
            "<em>Apple</em> banana smoothie"
          ]
        }
      },
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.13076457,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        },
        "highlight": {
          "title": [
            "Apple <em>banana</em> smoothie"
          ]
        }
      }
    ]
  }
}
```

### 突顯多份文件

使用 `documents` 陣列比對多份文件時，每份文件都會被指派一個槽位索引。突顯鍵值接著會採用下列形式，其中 `<slot>` 是文件在 `documents` 陣列中的索引：

```json
"<slot>_<fieldname>": [ ... ]
```

請使用下列命令比對兩份文件並突顯相符內容：

```json
POST /my_percolator_index/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "documents": [
        { "title": "Apple pie recipe" },
        { "title": "Banana smoothie ideas" }
      ]
    }
  },
  "highlight": {
    "fields": {
      "title": {}
    }
  }
}
```
{% include copy-curl.html %}

回應包含以文件槽位為前置詞的突顯欄位，例如 `0_title` 和 `1_title`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.31506687,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 0.31506687,
        "_source": {
          "query": {
            "match": {
              "title": "apple"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            0
          ]
        },
        "highlight": {
          "0_title": [
            "<em>Apple</em> pie recipe"
          ]
        }
      },
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 0.31506687,
        "_source": {
          "query": {
            "match": {
              "title": "banana"
            }
          }
        },
        "fields": {
          "_percolator_document_slot": [
            1
          ]
        },
        "highlight": {
          "1_title": [
            "<em>Banana</em> smoothie ideas"
          ]
        }
      }
    ]
  }
}
```

## 參數

`percolate` 查詢支援下列參數。

| 參數 | 必要/選用 | 說明 |
|-----------|-------------------|-------------|
| `field` | 必要 | 包含已儲存 `percolate` 查詢的欄位。 |
| `document` | 選用 | 要與已儲存查詢比對的單一內嵌文件。 |
| `documents` | 選用 | 要與已儲存查詢比對的多個內嵌文件陣列。 |
| `index` | 選用 | 包含您要比對之文件的索引。 |
| `id` | 選用 | 要從索引擷取之文件的 ID。 |
| `routing` | 選用 | 擷取文件時要使用的路由值。 |
| `preference` | 選用 | 擷取文件時分片路由的偏好設定。 |
| `name` | 選用 | 指派給 `percolate` 子句的名稱。在 `bool` 查詢中使用多個 `percolate` 子句時很有幫助。 |
