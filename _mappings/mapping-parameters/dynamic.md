---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "動態"
parent: Mapping parameters
nav_order: 30
has_children: false
has_toc: false
redirect_from:
  - /field-types/mapping-parameters/dynamic/
  - /opensearch/dynamic/
  - /field-types/dynamic/
---

# 動態對應參數

`dynamic` 參數會指定新偵測到的欄位是否可以動態新增至對應。其接受下表所列的參數。

參數 | 說明
:--- | :---
`true`  | 指定新欄位可以動態新增至對應。預設值為 `true`。
`false` | 指定新欄位無法動態新增至對應。若偵測到新欄位，則不會對其編製索引或搜尋，但可從 `_source` 欄位擷取。
`false_allow_templates` | 當新欄位符合預先定義的動態範本時，將其新增至對應。不符合範本的新欄位不會編製索引或搜尋，但會存在於 `_source` 欄位中。
`strict` | 擲回例外狀況。偵測到新欄位時，編製索引作業會失敗。
`strict_allow_templates` | 若新欄位符合對應中預先定義的動態範本，則新增這些欄位。

---

## 範例：建立 `dynamic` 設為 `true` 的索引

1. 傳送下列請求，建立 `dynamic` 設為 `true` 的索引：

```json
PUT testindex1
{
  "mappings": {
    "dynamic": true
  }
}
```
{% include copy-curl.html %}

2. 傳送下列請求，將包含物件欄位 `patient`（其中有兩個字串欄位）的文件編製索引：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  } 
}
```
{% include copy-curl.html %}

3. 傳送下列請求，確認對應如預期運作：

```json
GET testindex1/_mapping
```
{% include copy-curl.html %}

物件欄位 `patient` 及兩個子欄位 `name` 和 `id` 已新增至對應，如下列回應所示：

```json
{
  "testindex1": {
    "mappings": {
      "dynamic": "true",
      "properties": {
        "patient": {
          "properties": {
            "id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
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

---

## 範例：建立 `dynamic` 設為 `false` 的索引

1. 傳送下列請求，建立具有明確對應且 `dynamic` 設為 `false` 的索引：

```json
PUT testindex1
{
  "mappings": {
    "dynamic": false,
    "properties": {
      "patient": {
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

2. 傳送下列請求，將文件編製索引。該文件包含具有兩個字串欄位的物件欄位 `patient`，以及額外的未對應欄位：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1",
  "floor": "1"
}
```
{% include copy-curl.html %}

3.  傳送下列請求，確認對應如預期運作：

```json
GET testindex1/_mapping
```
{% include copy-curl.html %}

下列回應顯示新欄位 `room` 和 `floor` 未新增至對應，對應維持不變：

```json
{
  "testindex1": {
    "mappings": {
      "dynamic": "false",
      "properties": {
        "patient": {
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
}
```

4. 傳送下列請求，從文件中取得未對應的欄位 `room` 和 `floor`：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1",
  "floor": "1"
}
```

下列請求會搜尋欄位 `room` 和 `floor`：

```json
POST testindex1/_search
{
  "query": {
    "term": {
      "room": "room1"
    }
  }
}
```

回應未傳回任何結果：

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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

---

## 範例：建立 `dynamic` 設為 `strict` 的索引

1. 傳送下列請求，建立具有明確對應且 `dynamic` 設為 `strict` 的索引：

```json
PUT testindex1
{
  "mappings": {
    "dynamic": strict,
    "properties": {
      "patient": {
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

2. 傳送下列請求，將文件編製索引。該文件包含具有兩個字串欄位的物件欄位 `patient`，以及額外的未對應欄位：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1",
  "floor": "1"
}
```
{% include copy-curl.html %}

請注意，如下列回應所示，會擲回例外狀況：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "strict_dynamic_mapping_exception",
        "reason": "mapping set to strict, dynamic introduction of [room] within [_doc] is not allowed"
      }
    ],
    "type": "strict_dynamic_mapping_exception",
    "reason": "mapping set to strict, dynamic introduction of [room] within [_doc] is not allowed"
  },
  "status": 400
}
```

---

## 範例：建立 `dynamic` 設為 `strict_allow_templates` 的索引

1. 傳送下列請求，建立具有預先定義動態範本且 `dynamic` 設為 `strict_allow_templates` 的索引：

```json
PUT testindex1
{
  "mappings": {
    "dynamic": "strict_allow_templates",
    "dynamic_templates": [
      {
        "strings": {
          "match": "room*",
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ],
    "properties": {
      "patient": {
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

2. 傳送下列請求，將文件編製索引。該文件包含具有兩個字串欄位的物件欄位 `patient`，以及符合其中一個動態範本的新欄位 `room`：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1"
}
```
{% include copy-curl.html %}

編製索引成功，因為新欄位 `room` 符合動態範本。然而，新欄位 `floor` 的編製索引失敗，因為它不符合其中一個動態範本，且未明確對應，如下列回應所示：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1",
  "floor": "1"
}
```

---

## 範例：建立 `dynamic` 設為 `false_allow_templates` 的索引

1. 傳送下列請求，建立具有預先定義動態範本且 `dynamic` 設為 `false_allow_templates` 的索引：

```json
PUT testindex1
{
  "mappings": {
    "dynamic": "false_allow_templates",
    "dynamic_templates": [
      {
        "strings": {
          "match": "room*",
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ],
    "properties": {
      "patient": {
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

2. 傳送下列請求，將文件編製索引。該文件包含具有兩個字串欄位的物件欄位 `patient`，以及符合其中一個動態範本的新欄位 `room`：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1"
}
```
{% include copy-curl.html %}

新欄位 `room` 已編製索引，因為它符合動態範本。

若您新增欄位 `floor`，即使它不符合任何對應屬性或任何動態範本，仍會編製索引。然而，不會為 `floor` 欄位建立對應。因此，諸如 `{"match": {"floor": "1"}}` 的查詢不會傳回此文件：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  },
  "room": "room1",
  "floor": "1"
}
```
{% include copy-curl.html %}
