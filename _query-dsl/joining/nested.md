---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巢狀"
parent: Joining queries
nav_order: 5
---

# 巢狀查詢

`nested` 查詢可作為其他查詢的包裝，用來搜尋 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 欄位。巢狀欄位物件會被視為以個別文件編製索引的方式進行搜尋。如果物件符合搜尋條件，`nested` 查詢會傳回根層級的父文件。

## 範例 

在執行 `nested` 查詢之前，您的索引必須包含 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 欄位。 

若要設定一個包含巢狀欄位的範例索引，請傳送以下請求：

```json
PUT /testindex 
{
  "mappings": {
    "properties": {
      "patient": {
        "type": "nested",
        "properties": {
          "name": {
            "type": "text"
          },
          "age": {
            "type": "integer"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將文件編製索引至範例索引中：

```json
PUT /testindex/_doc/1
{
  "patient": {
    "name": "John Doe",
    "age": 56
  }
}
```
{% include copy-curl.html %}

若要搜尋巢狀的 `patient` 欄位，請將查詢包在 `nested` 查詢中，並提供巢狀欄位的 `path`：

```json
GET /testindex/_search
{
  "query": {
    "nested": {
      "path": "patient",
      "query": {
        "match": {
          "patient.name": "John"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢會傳回符合條件的文件：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "patient": {
            "name": "John Doe",
            "age": 56
          }
        }
      }
    ]
  }
}
```

## 擷取內部命中

若要傳回符合查詢的內部命中 (inner hits)，請提供 `inner_hits` 參數：

```json
GET /testindex/_search
{
  "query": {
    "nested": {
      "path": "patient",
      "query": {
        "match": {
          "patient.name": "John"
        }
      },
      "inner_hits": {}
    }
  }
}
```
{% include copy-curl.html %}

回應會包含額外的 `inner_hits` 欄位。`_nested` 欄位可識別內部命中來源於哪個特定內部物件。它包含巢狀命中以及相對於其在 `_source` 中位置的偏移量。由於排序與評分的緣故，命中物件在 `inner_hits` 中的位置通常與其在巢狀物件中的原始位置不同。

預設情況下，`inner_hits` 內命中物件的 `_source` 會相對於 `_nested` 欄位傳回。在此範例中，`inner_hits` 內的 `_source` 包含 `name` 與 `age` 欄位，而非包含整個 `patient` 物件的頂層 `_source`：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "patient": {
            "name": "John Doe",
            "age": 56
          }
        },
        "inner_hits": {
          "patient": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 0.13076457,
              "hits": [
                {
                  "_index": "testindex",
                  "_id": "1",
                  "_nested": {
                    "field": "patient",
                    "offset": 0
                  },
                  "_score": 0.13076457,
                  "_source": {
                    "name": "John Doe",
                    "age": 56
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

您可以透過在對應中設定 `_source` 欄位來停用傳回 `_source`。如需更多資訊，請參閱[來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/)。
{: .tip}

如需有關擷取內部命中的更多資訊，請參閱[內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

## 多層巢狀查詢

您可以使用多層巢狀查詢來搜尋在其他巢狀物件內含有巢狀物件的文件。在此範例中，您將透過為階層的每一層指定一個巢狀查詢，來查詢多層巢狀欄位。

首先，建立一個具有多層巢狀欄位的索引：

```json
PUT /patients
{
  "mappings": {
    "properties": {
      "patient": {
        "type": "nested",
        "properties": {
          "name": {
            "type": "text"
          },
          "contacts": {
            "type": "nested",
            "properties": {
              "name": {
                "type": "text"
              },
              "relationship": {
                "type": "text"
              },
              "phone": {
                "type": "keyword"
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

接著，將兩份文件編製索引至範例索引中：

```json
PUT /patients/_doc/1
{
  "patient": {
    "name": "John Doe",
    "contacts": [
      {
        "name": "Jane Doe",
        "relationship": "mother",
        "phone": "5551111"
      },
      {
        "name": "Joe Doe",
        "relationship": "father",
        "phone": "5552222"
      }
    ]
  }
}
```
{% include copy-curl.html %}

```json
PUT /patients/_doc/2?refresh
{
  "patient": {
    "name": "Mary Major",
    "contacts": [
      {
        "name": "Jane Major",
        "relationship": "sister",
        "phone": "5553333"
      },
      {
        "name": "Paula Major",
        "relationship": "mother",
        "phone": "5554444"
      }
    ]
  }
}
```
{% include copy-curl.html %}

若要搜尋巢狀的 `patient` 欄位，請使用多層 `nested` 查詢。以下查詢搜尋聯絡資訊中包含名為 `Jane` 且關係為 `mother` 之聯絡人的病患：

```json
GET /patients/_search
{
  "query": {
    "nested": {
      "path": "patient",
      "query": {
        "nested": {
          "path": "patient.contacts",
          "query": {
            "bool": {
              "must": [
                { "match": { "patient.contacts.relationship": "mother" } },
                { "match": { "patient.contacts.name": "Jane" } }
              ]
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

內部 `bool` 查詢中的兩個條件必須符合同一個聯絡物件。文件 2 有一個名為 `Jane` 的聯絡人，以及另一個關係為 `mother` 的聯絡人，但它們是不同的聯絡人，因此只會傳回文件 1。如果 `contacts` 被對應為 `object` 欄位而非 `nested`，聯絡值將會被扁平化為陣列，相同的條件就會同時符合兩份文件。

查詢會傳回具有符合這些詳細資料之聯絡項目的病患：

```json
{
  "took": 9,
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
    "max_score": 0.63013375,
    "hits": [
      {
        "_index": "patients",
        "_id": "1",
        "_score": 0.63013375,
        "_source": {
          "patient": {
            "name": "John Doe",
            "contacts": [
              {
                "name": "Jane Doe",
                "relationship": "mother",
                "phone": "5551111"
              },
              {
                "name": "Joe Doe",
                "relationship": "father",
                "phone": "5552222"
              }
            ]
          }
        }
      }
    ]
  }
}
```

## 參數

下表列出 `nested` 查詢支援的所有頂層參數。

| 參數  | 必要/選用 | 說明  |
|:---|:---|:---|
| `path` | 必要 | 指定要搜尋的巢狀物件路徑。 |
| `query` | 必要 | 要在指定 `path` 內的巢狀物件上執行的查詢。如果巢狀物件符合查詢，則會傳回根父文件。您可以使用點號表示法搜尋巢狀欄位，例如 `nested_object.subfield`。支援多層巢狀並會自動偵測。因此，巢狀查詢內的內部 `nested` 查詢會自動比對正確的巢狀層級，而非根層級。 |
| `ignore_unmapped` | 選用 | 指示是否忽略未對應的 `path` 欄位，並且不傳回文件而不是擲回錯誤。當查詢多個索引，而其中某些索引可能不包含 `path` 欄位時，您可以提供此參數。預設為 `false`。 |
| `score_mode` | 選用 | 定義符合條件的內部文件分數如何影響父文件的分數。有效值為：<br> - `avg`：使用所有符合條件的內部文件的平均相關性分數。<br> - `max`：將符合條件的內部文件中最高的相關性分數指派給父文件。<br> - `min`：將符合條件的內部文件中最低的相關性分數指派給父文件。<br> - `sum`：將所有符合條件的內部文件的相關性分數加總。<br> - `none`：忽略內部文件的相關性分數，並將 `0` 的分數指派給父文件。<br> 預設為 `avg`。 |
| `inner_hits` | 選用 | 若有提供，則傳回符合查詢的底層命中。 |

## 後續步驟

- 進一步了解[擷取內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。