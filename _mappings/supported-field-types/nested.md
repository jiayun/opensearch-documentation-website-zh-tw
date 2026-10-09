---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Nested
nav_order: 42
has_children: false
parent: Object field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/nested/
  - /opensearch/supported-field-types/nested/
  - /field-types/nested/
---

# Nested 欄位類型
**於 1.0 版推出**
{: .label .label-purple }

Nested 欄位類型是一種特殊的 [object 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/object/)。

任何 object 欄位都可以接受物件陣列。陣列中的每個物件都會動態對應為 object 欄位類型，並以攤平的形式儲存。這表示陣列中的物件會被拆解成個別欄位，而所有物件中每個欄位的值會一起儲存。有時需要使用 nested 類型將巢狀物件完整保留，以便對它執行搜尋。

## 攤平形式

預設情況下，每個巢狀物件都會動態對應為 object 欄位類型。任何 object 欄位都可以接受物件陣列。

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

這些物件在儲存時會被攤平，因此其內部表示形式是每個欄位所有值的陣列：

```json
{
    "patients.name" : ["John Doe", "Mary Major"],
    "patients.age" : [56, 85],
    "patients.smoker" : [true, false]
}
```

某些查詢在這種表示形式下可以正確運作。如果您搜尋年齡大於 75 歲或吸菸的病患，文件 100 應該會符合。

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

查詢正確地傳回文件 100：

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.3616575,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "100",
        "_score" : 1.3616575,
        "_source" : {
          "patients" : [
            {
              "name" : "John Doe",
              "age" : "56",
              "smoker" : true
            },
            {
              "name" : "Mary Major",
              "age" : "85",
              "smoker" : false
            }
          ]
        }
      }
    ]
  }
}
```

或者，如果您搜尋年齡大於 75 歲且吸菸的病患，文件 100 不應該符合。

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

然而，此查詢仍然錯誤地傳回文件 100。這是因為在建立個別欄位的值陣列時，年齡與吸菸之間的關聯性遺失了。

## 將物件對應為 nested

巢狀物件會以個別文件的形式儲存，父物件會保有對其子物件的參照。若要將物件標記為 nested，請建立包含 nested 欄位類型的對應。

```json
PUT testindex1
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

接著，為包含 nested 欄位類型的文件編製索引：

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

您可以使用下列 nested 查詢來搜尋年齡大於 75 歲或吸菸的病患：

```json
GET testindex1/_search
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

查詢正確地傳回兩位病患：

```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.8465736,
    "hits" : [
      {
        "_index" : "testindex1",
        "_id" : "100",
        "_score" : 0.8465736,
        "_source" : {
          "patients" : [
            {
              "name" : "John Doe",
              "age" : 56,
              "smoker" : true
            },
            {
              "name" : "Mary Major",
              "age" : 85,
              "smoker" : false
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
GET testindex1/_search
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

如預期，前一個查詢沒有傳回任何結果：

```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 0,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
```

## 參數

下表列出 object 欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
[`dynamic`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/object#the-dynamic-parameter) | 指定是否可以動態地在物件中新增欄位。有效值為 `true`、`false`、`strict`、`strict_allow_templates` 和 `false_allow_templates`。預設值為 `true`。
`include_in_parent` | 布林值，指定是否應將子巢狀物件中的所有欄位以攤平形式一併新增至父文件。預設值為 `false`。
`include_in_root` | 布林值，指定是否應將子巢狀物件中的所有欄位以攤平形式一併新增至根文件。預設值為 `false`。
`properties` | 此物件的欄位，可以是任何支援的類型。如果 `dynamic` 設定為 `true`，則可以動態地在這個物件中新增屬性。

## 後續步驟

- 了解巢狀欄位上的 [聯結查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)。
- 了解[擷取 inner hits]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。
- 了解 [停用物件]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/disable-objects/) 對應參數。