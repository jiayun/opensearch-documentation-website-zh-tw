---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Percolate
parent: Specialized queries
nav_order: 55
---

# Percolate 查詢

使用 `percolate` 查詢來找出符合指定文件的已儲存查詢。此操作與一般搜尋相反：不是找出符合查詢的文件，而是找出符合文件的查詢。`percolate` 查詢常用於警示、通知與反向搜尋等使用情境。

使用 `percolate` 查詢時，請考量以下重點：

- 您可以對內嵌提供的文件執行 percolate，或從索引擷取現有文件。
- 文件與已儲存的查詢必須使用相同的欄位名稱與類型。
- 您可以將 percolation 與篩選及評分結合，以建立複雜的比對系統。
- `percolate` 查詢被視為[昂貴的查詢]({{site.url}}{{site.baseurl}}/query-dsl/#expensive-queries)，只有在叢集設定 `search.allow_expensive_queries` 設為 `true`（預設）時才會執行。如果此設定為 `false`，OpenSearch 會拒絕 `percolate` 查詢。

`percolate` 查詢在各種即時比對情境中都很有用。常見的使用案例包括：

- 使用者登記對產品的興趣，例如「新款 Apple 筆記型電腦有貨時通知我」。當新的產品文件被編製索引時，系統會找出所有擁有相符已儲存查詢的使用者，並傳送通知給他們。
- 求職者依偏好的職稱或地點儲存查詢，新的職缺公告會與這些查詢比對以觸發警示。
- 傳入的記錄檔或事件資料會與已儲存的安全性規則或異常模式進行 percolate 比對。
- 傳入的新聞文章會與已儲存的主題設定檔比對，以進行分類或傳送給感興趣的讀者。

已儲存的查詢儲存在 [`percolator` 欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/)中。當您執行 `percolate` 查詢時，OpenSearch 會將文件與已儲存的查詢比對，並傳回每個相符的查詢，以其 `_id` 識別。如果您啟用高亮顯示，回應也會包含文件中相符的文字。如果您對多份文件執行 percolate，`_percolator_document_slot` 欄位會識別每個查詢所比對到的文件。

## 範例

下列範例示範如何使用不同方法儲存查詢，並對它們測試文件。

### 建立用於儲存已儲存查詢的索引

首先，建立一個索引，並在其 `mappings` 中設定 [`percolator` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/)以儲存已儲存的查詢：

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

索引還必須對應已儲存查詢所搜尋的每個欄位---在此範例中為 `title`。OpenSearch 使用這些對應來剖析每個已儲存的查詢與被 percolate 的文件。如果某個欄位沒有對應，儲存搜尋該欄位的查詢時會失敗，並出現 `No field mapping can be found for the field with name [title]` 錯誤。

在 `title` 欄位中新增一個比對 "apple" 的查詢：

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

在 `title` 欄位中新增一個比對 "banana" 的查詢：

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

### 對內嵌文件執行 percolate

使用已儲存的查詢測試內嵌文件：

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

回應會提供搜尋 `title` 欄位中包含 "apple" 一詞之文件的已儲存查詢，以 `_id` 識別：`1`：

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

### 在篩選情境中執行 percolate

預設情況下，OpenSearch 會為每個相符的查詢計算相關性分數。已儲存查詢是否相符通常可以僅從其擷取的詞元來判斷，但評分需要對每個候選查詢與文件進行完整評估。如果您不需要分數，可以將 `percolate` 查詢包在 `constant_score` 查詢中，或包在 `bool` 查詢的 `filter` 子句中：

```json
POST /my_percolator_index/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "percolate": {
          "field": "query",
          "document": {
            "title": "Fresh Apple Harvest"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

相同的查詢會相符，但每個命中都會得到常數分數 `1.0`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 1.0,
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

查詢快取永遠不會儲存 `percolate` 查詢或任何包含此類查詢的複合查詢，因為這些查詢會使用大量記憶體。
{: .note}

### 對多份文件執行 percolate

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

`_percolator_document_slot` 欄位會依文件在 `documents` 陣列中的位置（從 `0` 開始）識別已儲存查詢所比對到的每份文件：

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

### 對現有已編製索引的文件執行 percolate

您可以參照已儲存在另一個索引中的現有文件，以檢查是否有相符的已儲存查詢。

為您的文件建立一個獨立的索引：

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

新增一份文件：

```json
POST /products/_doc/1
{
  "title": "Banana Smoothie Special"
}
```
{% include copy-curl.html %}

檢查已儲存的查詢是否與已編製索引的文件相符：

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

使用已儲存的文件時，您必須同時提供 `index` 和 `id`。
{: .note}

系統會傳回對應的查詢：

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

若要確保您對預期版本的文件執行 percolate，請指定 `version` 參數。例如，若只想在文件仍為版本 `1` 時才執行 percolate，請在 `percolate` 查詢中加入 `"version": 1`。如果文件在此之後已更新，請求會失敗，並傳回 `version_conflict_engine_exception` 和 `409` 狀態碼。

### 在個別子句中對多份文件執行 percolate

若要對多份文件執行 percolate，並為每份文件使用個別的 `percolate` 子句，請將這些子句組合在 `bool` 查詢中，並為每個子句指定 `name`：

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

OpenSearch 會將每個子句的 `name` 附加到 `_percolator_document_slot` 欄位，因此欄位名稱會顯示每個已儲存查詢相符的是哪個子句，也就是哪份文件：

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

如果您在多個 `percolate` 子句中省略 `name`，OpenSearch 會改為將 `field` 值附加到 slot 欄位名稱。在此範例中，兩個子句都會在同一個 `_percolator_document_slot_query` 欄位中回報相符結果，因此您無法分辨每個查詢相符的是哪份文件。

由於每份文件都有自己的子句，您也可以為文件指定不同的權重。在下列範例中，每個 `percolate` 子句都包裝在一個指定不同 `boost` 的 `constant_score` 查詢中，因此第二份文件的相符結果分數較高：

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
                  "title": "Banana bread with honey"
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

與第二份文件相符的查詢會獲得較高的分數：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 3.0,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "2",
        "_score": 3.0,
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
      },
      {
        "_index": "my_percolator_index",
        "_id": "1",
        "_score": 1.0,
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
      }
    ]
  }
}
```


## 批次 percolate 與個別子句的比較

批次 percolate（使用 `documents`）與個別子句（使用 `bool`，並為每份文件使用具名的 `percolate` 子句）都能對多份文件執行 percolate，並傳回相同的相符結果。下表比較這兩種方式如何建構請求、識別相符的文件，以及支援個別文件的評分。

| 功能                        | 批次（`documents`）                            | 個別子句（`bool` + `percolate` + `name`） |
|-------------------------------|------------------------------------------------|--------------------------------------------------|
| 輸入格式                  | 一個包含文件陣列的 `percolate` 子句 | 每份文件一個 `percolate` 子句     |
| 文件識別       | 依據在 `documents` 陣列中的位置（`0`、`1`、...） | 依據子句名稱（`apple_doc`、`banana_doc`） |
| 相符 slot 的回應欄位 | `_percolator_document_slot: [0]`              | `_percolator_document_slot_<name>: [0]`          |
| 醒目提示前置詞              | `0_title`、`1_title`                           | `apple_doc_title`、`banana_doc_title`            |
| 加權（boost）                        | 整個子句使用一個 boost，套用至所有文件 | 每份文件的子句各有獨立的 boost |
| 查詢剖析                 | 每個已儲存查詢只剖析一次，並一次比對所有文件 | 每個子句分別比對其對應的文件 |
| 使用情境                      | 大量比對作業、大型事件串流        | 個別文件追蹤、測試、個別文件加權 |


## 突顯相符項目

`percolate` 回應中的突顯會標示您提交文件中的詞彙。每個命中的突顯會顯示其已儲存查詢所比對到的詞彙，因此比對同一份文件的兩個已儲存查詢可以突顯文件的不同部分。

### 突顯單一文件

此範例使用 `my_percolator_index` 中的已儲存查詢。請使用下列請求來突顯 `title` 欄位中的相符項目：

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

每個命中都會突顯其已儲存查詢所比對到的詞彙：

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

使用 `documents` 陣列對多份文件進行 percolate 時，突顯鍵會採用下列形式，其中 `<slot>` 是文件在 `documents` 陣列中的位置，從 `0` 開始：

```json
"<slot>_<fieldname>": [ ... ]
```

請使用下列命令對兩份文件進行 percolate 並突顯：

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

回應包含以文件插槽為前綴的突顯欄位，例如 `0_title` 和 `1_title`：

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

## 效能考量

當您為已儲存查詢編製索引時，OpenSearch 會擷取查詢的詞彙，並將它們與查詢一併編製索引。在搜尋時，OpenSearch 會將被 percolate 的文件放入暫時的記憶體內索引，並使用擷取的詞彙來選取候選查詢。接著只會對文件執行這些候選查詢，因此大多數已儲存查詢永遠不會被評估。

某些查詢類型無法擷取詞彙，例如 `wildcard` 和 `geo_shape` 查詢。對於 `bool` 查詢，如果不支援的查詢是唯一的 `must` 或 `filter` 子句，或者它是沒有 `must` 或 `filter` 子句的查詢中其中一個 `should` 子句，擷取就會失敗。如果另一個必要子句（例如 `must` 或 `filter` 中的 `match` 查詢）具有可擷取的詞彙，OpenSearch 會改用那些詞彙來選取候選查詢。無法擷取詞彙的已儲存查詢會對每份被 percolate 的文件進行評估，隨著這類查詢數量增加，percolation 速度會變慢。這些查詢仍然會正確比對。

若要找出無法擷取詞彙的已儲存查詢，請搜尋 `percolator` 欄位中 `extraction_result` 子欄位裡的 `failed` 值。下列範例先新增一個 `wildcard` 查詢，然後搜尋詞彙擷取失敗的查詢：

```json
POST /my_percolator_index/_doc/3?refresh=true
{
  "query": {
    "wildcard": {
      "title": "cher*"
    }
  }
}
```
{% include copy-curl.html %}

```json
GET /my_percolator_index/_search
{
  "query": {
    "term": {
      "query.extraction_result": "failed"
    }
  }
}
```
{% include copy-curl.html %}

回應包含 `wildcard` 查詢：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_percolator_index",
        "_id": "3",
        "_score": 1.0,
        "_source": {
          "query": {
            "wildcard": {
              "title": "cher*"
            }
          }
        }
      }
    ]
  }
}
```

請將已儲存查詢與被 percolate 的文件儲存在不同的索引中，如前面的範例所示。分開的索引具有下列優點：

- 每個索引中的文件共用相同的欄位，因此 OpenSearch 能以更精簡的方式儲存它們。
- 您可以獨立於文件索引來設定已儲存查詢索引的設定，例如主要分片的數量。這很重要，因為 percolation 效能的擴展方式與一般搜尋效能不同。

## 參數

`percolate` 查詢支援下列參數。請以內嵌方式（使用 `document` 或 `documents`）或以參照方式（使用 `index` 和 `id`）提供要 percolate 的文件。

| 參數 | 必要/選用 | 說明 |
|-----------|-------------------|-------------|
| `field` | 必要 | 包含已儲存查詢的 `percolator` 欄位。 |
| `document` | 選用 | 要與已儲存查詢比對的單一內嵌文件。 |
| `documents` | 選用 | 要與已儲存查詢比對的內嵌文件陣列。 |
| `index` | 選用 | 包含要 percolate 之已儲存文件的索引。若指定 `id` 則為必要。 |
| `id` | 選用 | 要 percolate 之已儲存文件的 ID。若指定 `index` 則為必要。 |
| `routing` | 選用 | 擷取已儲存文件時要使用的路由值。 |
| `preference` | 選用 | 擷取已儲存文件時要使用的分片偏好。 |
| `version` | 選用 | 已儲存文件的預期版本。如果文件目前的版本不同，請求會失敗並出現版本衝突錯誤。 |
| `name` | 選用 | `percolate` 子句的名稱。OpenSearch 會將該名稱附加到回應中的 `_percolator_document_slot` 欄位。當搜尋包含多個 `percolate` 子句時，請使用 `name` 來區分相符項目。 |
