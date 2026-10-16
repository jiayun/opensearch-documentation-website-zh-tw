---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巢狀"
nav_order: 42
has_children: false
parent: Object field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/nested/
  - /opensearch/supported-field-types/nested/
  - /field-types/nested/
---

# 巢狀欄位類型
**於 1.0 版推出**
{: .label .label-purple }

巢狀欄位類型是一種特殊的[物件欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/object/)。

任何物件欄位都可以接受物件陣列。陣列中的每個物件都會動態對應為物件欄位類型，並以扁平化的形式儲存。這表示陣列中的物件會被拆解為個別欄位，且所有物件中同一欄位的值會儲存在一起。有時必須使用巢狀類型將巢狀物件作為一個整體保留，以便您對其執行搜尋。

當文件包含物件陣列，且您的查詢必須比對同一物件內的條件時，請使用巢狀類型，例如尋找年齡超過 75 歲且吸菸的病患。巢狀物件的編製索引與查詢成本比一般物件更高，因此請僅在需要這種獨立性時使用。若要儲存鍵因文件而異的鍵值組，請考慮使用 [`flat_object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/) 欄位類型，它會將整個物件對應為單一欄位。

## 攤平形式

為包含病人物件陣列的文件編製索引：

```json
PUT testindex1/_doc/100
{ 
  "patients": [ 
    {"name" : "John Doe", "age" : 56, "smoker" : true},
    {"name" : "Mary Major", "age" : 85, "smoker" : false}
  ] 
}
```
{% include copy-curl.html %}

這些物件在儲存時會被攤平，因此其內部表示法中，每個欄位都有一個包含所有值的陣列：

```json
{
    "patients.name" : ["John Doe", "Mary Major"],
    "patients.age" : [56, 85],
    "patients.smoker" : [true, false]
}
```

某些查詢在這種表示法下可以正確運作。如果您搜尋年齡大於 75 歲 OR 有吸菸的病人，文件 100 會符合。

```json
GET testindex1/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "patients.smoker": true
          }
        },
        {
          "range": {
            "patients.age": {
              "gte": 75
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

此查詢會正確傳回文件 100：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.1643897,
    "hits": [
      {
        "_index": "testindex1",
        "_id": "100",
        "_score": 1.1643897,
        "_source": {
          "patients": [
            {
              "name": "John Doe",
              "age": 56,
              "smoker": true
            },
            {
              "name": "Mary Major",
              "age": 85,
              "smoker": false
            }
          ]
        }
      }
    ]
  }
}
```

反之，如果您搜尋年齡大於 75 歲 AND 有吸菸的病人，文件 100 應該不符合。

```json
GET testindex1/_search 
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "patients.smoker": true
          }
        },
        {
          "range": {
            "patients.age": {
              "gte": 75
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

然而，此查詢仍然會錯誤地傳回文件 100。這是因為在為個別欄位建立值陣列時，年齡與吸菸之間的關聯性已經遺失。

## 將物件對應為巢狀類型

巢狀物件會儲存為個別文件，而父物件會保留其子物件的參照。若要將物件標記為巢狀類型，請建立一個包含巢狀欄位類型對應的索引：

```json
PUT testindex2
{
  "mappings" : {
    "properties": {
      "patients": { 
        "type" : "nested"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將含有巢狀欄位類型的文件編製索引：

```json
PUT testindex2/_doc/100
{ 
  "patients": [ 
    {"name" : "John Doe", "age" : 56, "smoker" : true},
    {"name" : "Mary Major", "age" : 85, "smoker" : false}
  ] 
}
```
{% include copy-curl.html %}

您可以使用下列 nested 查詢來搜尋年齡大於 75 歲或吸菸的病患：

```json
GET testindex2/_search
{
  "query": {
    "nested": {
      "path": "patients",
      "query": {
        "bool": {
          "should": [
            {
              "term": {
                "patients.smoker": true
              }
            },
            {
              "range": {
                "patients.age": {
                  "gte": 75
                }
              }
            }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

由於至少有一位病患符合條件，此查詢會正確傳回文件 100：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.6575334,
    "hits": [
      {
        "_index": "testindex2",
        "_id": "100",
        "_score": 0.6575334,
        "_source": {
          "patients": [
            {
              "name": "John Doe",
              "age": 56,
              "smoker": true
            },
            {
              "name": "Mary Major",
              "age": 85,
              "smoker": false
            }
          ]
        }
      }
    ]
  }
}
```

您可以使用下列 nested 查詢來搜尋年齡大於 75 歲且吸菸的病患：

```json
GET testindex2/_search
{
  "query": {
    "nested": {
      "path": "patients",
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "patients.smoker": true
              }
            },
            {
              "range": {
                "patients.age": {
                  "gte": 75
                }
              }
            }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如預期般，先前的查詢不會傳回任何結果：

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

## 擷取相符的巢狀物件

巢狀查詢會傳回整個父文件。若要查看哪些巢狀物件相符，請在查詢中新增 `inner_hits`。下列請求會搜尋名為 Mary 且年齡超過 75 歲的病患，並醒目顯示相符的姓名：

```json
GET testindex2/_search
{
  "_source": false,
  "query": {
    "nested": {
      "path": "patients",
      "query": {
        "bool": {
          "must": [
            { "match": { "patients.name": "mary" } },
            { "range": { "patients.age": { "gte": 75 } } }
          ]
        }
      },
      "inner_hits": {
        "highlight": {
          "fields": {
            "patients.name": {}
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中的 `inner_hits` 物件只包含相符的病患。`_nested.offset` 值是該病患在 `patients` 陣列中的位置：

```json
{
  "took": 22,
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
    "max_score": 1.3150668,
    "hits": [
      {
        "_index": "testindex2",
        "_id": "100",
        "_score": 1.3150668,
        "inner_hits": {
          "patients": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.3150668,
              "hits": [
                {
                  "_index": "testindex2",
                  "_id": "100",
                  "_nested": {
                    "field": "patients",
                    "offset": 1
                  },
                  "_score": 1.3150668,
                  "_source": {
                    "smoker": false,
                    "name": "Mary Major",
                    "age": 85
                  },
                  "highlight": {
                    "patients.name": [
                      "<em>Mary</em> Major"
                    ]
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

如需更多資訊，請參閱 [Inner hits]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。

## 使用巢狀物件

由於每個巢狀物件都會以個別的隱藏文件儲存，對上層文件的一般查詢不會比對到巢狀物件中的欄位。在前述範例中，對 `patients.smoker` 執行未以 `nested` 查詢包裝的 `term` 查詢不會傳回任何結果。請使用下列功能來處理巢狀物件：

- [`nested` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/nested/)：搜尋巢狀物件
- [`nested`]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/) 與 [`reverse_nested`]({{site.url}}{{site.baseurl}}/aggregations/bucket/reverse-nested/) 彙總：對巢狀欄位進行彙總並返回上層文件
- [巢狀排序]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/#sorting-nested-objects)：依巢狀物件中的值排序上層文件
- [內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)：傳回符合條件的巢狀物件

擷取欄位值時也適用同樣的分離原則。在最上層的 `docvalue_fields` 或 `stored_fields` 參數中請求巢狀欄位不會傳回任何值。若要擷取這些欄位，請在 `inner_hits` 中請求。

若也要在上層文件中為巢狀欄位編製索引，請將 `include_in_parent` 或 `include_in_root` 設定為 `true`。如此一來，一般查詢即可比對這些欄位，但上層文件會以扁平化形式儲存這些值，因此這些查詢無法判斷哪些值屬於同一個物件。

巢狀欄位可以包含其他巢狀欄位。只有當巢狀欄位超過一層深度時，這兩個參數才會有所不同。例如，若 `patients` 是包含巢狀 `visits` 欄位的巢狀欄位，在 `visits` 上設定 `include_in_parent` 會將 visit 欄位加入每個 `patients` 物件，因此對 `patients` 執行 `nested` 查詢即可比對到這些欄位。在 `visits` 上設定 `include_in_root` 則會將 visit 欄位加入最上層文件，因此一般查詢即可比對到這些欄位。

## 巢狀欄位的限制

OpenSearch 會將每個巢狀物件除了父文件之外，另外編製索引為獨立的 Lucene 文件。在前述範例中，文件 100 會儲存為三份 Lucene 文件：一份為父文件，另外各一份給每位病患。`GET _cat/indices` 傳回的 `docs.count` 值會包含這些隱藏文件，而 Count API 只會計算父文件。

為避免過度使用資源，OpenSearch 提供下列限制：

- `index.mapping.nested_fields.limit`：索引對應中相異 `nested` 欄位的數量上限。預設為 `50`。
- `index.mapping.nested_objects.limit`：單一文件中巢狀物件的總數上限，會跨所有 `nested` 欄位計算。預設為 `10000`。

如需更多資訊，請參閱[對應爆炸]({{site.url}}{{site.baseurl}}/mappings/mapping-explosion/#mapping-limit-settings)。

## 參數

下表列出 nested 欄位類型接受的參數。所有參數皆為選用。

參數 | 描述 
:--- | :--- 
[`dynamic`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/object#the-dynamic-parameter) | 指定是否可以動態新增欄位至物件。有效值為 `true`、`false`、`strict`、`strict_allow_templates` 和 `false_allow_templates`。預設為 `true`。
`include_in_parent` | 布林值，指定是否將子巢狀物件中的所有欄位以攤平形式一併新增至父文件。預設為 `false`。
`include_in_root` | 布林值，指定是否將子巢狀物件中的所有欄位以攤平形式一併新增至根文件。預設為 `false`。
`properties` | 此物件的欄位，可以是任何支援的類型。若 `dynamic` 設定為 `true`，即可動態新增屬性至此物件。如需更多資訊，請參閱 [Properties]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/properties/)。

## 後續步驟

- 了解巢狀欄位上的 [聯結查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)。
- 了解[擷取 inner hits]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。
- 了解 [停用物件]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/disable-objects/) 對應參數。