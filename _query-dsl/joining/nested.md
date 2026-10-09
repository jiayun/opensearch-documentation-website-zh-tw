---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巢狀"
parent: Joining queries
nav_order: 5
---

# 巢狀查詢

`nested` 查詢可包裝其他查詢，用來搜尋 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 欄位。巢狀欄位物件會以彷彿個別文件編製索引的方式進行搜尋。若某個物件符合搜尋條件，`nested` 查詢會傳回根層級的父文件。

## 範例 

在執行 `nested` 查詢之前，您的索引必須包含 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 欄位。 

若要設定包含巢狀欄位的範例索引，請傳送下列請求：

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

接著，將文件編製索引至範例索引：

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

若要搜尋巢狀 `patient` 欄位，請將您的查詢包裝在 `nested` 查詢中，並指定巢狀欄位的 `path`：

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

查詢會傳回相符的文件：

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
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.2876821,
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

若要傳回符合查詢的內部命中，請提供 `inner_hits` 參數：

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

回應包含額外的 `inner_hits` 欄位。`_nested` 欄位會識別內部命中源自哪個特定的內部物件。它包含巢狀命中，以及相對於其在 `_source` 中位置的位移。由於排序與評分，命中物件在 `inner_hits` 中的位置通常與其在巢狀物件中的原始位置不同。

根據預設，命中物件在 `inner_hits` 內的 `_source` 會相對於 `_nested` 欄位傳回。在此範例中，`inner_hits` 內的 `_source` 包含 `name` 與 `age` 欄位，而非包含整個 `patient` 物件的頂層 `_source`：

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
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.2876821,
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
              "max_score": 0.2876821,
              "hits": [
                {
                  "_index": "testindex",
                  "_id": "1",
                  "_nested": {
                    "field": "patient",
                    "offset": 0
                  },
                  "_score": 0.2876821,
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

您可以透過在對應中設定 `_source` 欄位，來停用傳回 `_source`。如需更多資訊，請參閱 [來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/)。
{: .tip}

如需擷取內部命中的更多資訊，請參閱 [內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

## 多層巢狀查詢

您可以使用多層巢狀查詢，搜尋在其他巢狀物件內含有巢狀物件的文件。在此範例中，您將為階層的每一層指定巢狀查詢，以查詢多層巢狀欄位。

首先，建立具有多層巢狀欄位的索引：

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

接著，將文件編製索引至範例索引：

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

若要搜尋巢狀 `patient` 欄位，請使用多層 `nested` 查詢。下列查詢會搜尋聯絡資訊中包含名為 `Jane`、關係為 `mother` 之人的病患：

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

查詢會傳回聯絡項目符合這些詳細資料的病患：

```json
{
  "took": 14,
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
    "max_score": 1.3862942,
    "hits": [
      {
        "_index": "patients",
        "_id": "1",
        "_score": 1.3862942,
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

下表列出 `nested` 查詢支援的所有最上層參數。

| 參數  | 必要/選用 | 說明  |
|:---|:---|:---|
| `path` | 必要 | 指定您要搜尋之巢狀物件的路徑。 |
| `query` | 必要 | 要在指定 `path` 內的巢狀物件上執行的查詢。若巢狀物件符合查詢，則會傳回根父文件。您可以使用點標記法搜尋巢狀欄位，例如 `nested_object.subfield`。支援多層巢狀，且會自動偵測。因此，另一個巢狀查詢內的內部 `nested` 查詢會自動符合正確的巢狀層級，而非根層級。 |
| `ignore_unmapped` | 選用 | 指出是否忽略未對應的 `path` 欄位並改為不傳回文件，而非擲回錯誤。當查詢多個索引時，若其中部分索引可能未包含 `path` 欄位，您可以提供此參數。預設為 `false`。 |
| `score_mode` | 選用 | 定義相符內部文件的分數如何影響父文件的分數。有效值為：<br> - `avg`：使用所有相符內部文件的平均相關性分數。<br> - `max`：將相符內部文件中最高的相關性分數指派給父文件。<br> - `min`：將相符內部文件中最低的相關性分數指派給父文件。<br> - `sum`：加總所有相符內部文件的相關性分數。<br> - `none`：忽略內部文件的相關性分數，並將分數 `0` 指派給父文件。<br> 預設為 `avg`。 |
| `inner_hits` | 選用 | 若提供，則傳回符合查詢的基礎命中。 |

## 後續步驟

- 進一步了解[擷取內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。