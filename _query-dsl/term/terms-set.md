---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞項集合"
parent: Term-level queries
nav_order: 30
---

# 詞項集合查詢

使用詞項集合查詢，您可以搜尋在指定欄位中符合最少數量確切詞項的文件。`terms_set` 查詢與 `terms` 查詢類似，差別在於您可以指定要傳回文件所需符合的最少詞項數量。您可以在索引的欄位中指定此數量，或使用指令碼指定。

舉例來說，假設有一個索引包含學生姓名以及這些學生修過的課程。設定此索引的對應時，您需要提供一個 [數值]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 欄位，指定要傳回文件所需符合的最少詞項數量：

```json
PUT students
{
  "mappings": {
    "properties": {
      "name": {
        "type": "keyword"
      },
      "classes": {
        "type": "keyword"
      },
      "min_required": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將兩份對應至學生的文件編製索引：

```json
PUT students/_doc/1
{
  "name": "Mary Major",
  "classes": [ "CS101", "CS102", "MATH101" ],
  "min_required": 2
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/2
{
  "name": "John Doe",
  "classes": [ "CS101", "MATH101", "ENG101" ],
  "min_required": 2
}
```
{% include copy-curl.html %}

現在搜尋修過下列課程中至少兩門的學生：`CS101`、`CS102`、`MATH101`：

```json
GET students/_search
{
  "query": {
    "terms_set": {
      "classes": {
        "terms": [ "CS101", "CS102", "MATH101" ],
        "minimum_should_match_field": "min_required"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這兩份文件：

```json
{
  "took" : 44,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.4544616,
    "hits" : [
      {
        "_index" : "students",
        "_id" : "1",
        "_score" : 1.4544616,
        "_source" : {
          "name" : "Mary Major",
          "classes" : [
            "CS101",
            "CS102",
            "MATH101"
          ],
          "min_required" : 2
        }
      },
      {
        "_index" : "students",
        "_id" : "2",
        "_score" : 0.5013843,
        "_source" : {
          "name" : "John Doe",
          "classes" : [
            "CS101",
            "MATH101",
            "ENG101"
          ],
          "min_required" : 2
        }
      }
    ]
  }
}
```

若要使用指令碼指定文件應符合的最少詞項數量，請在 `minimum_should_match_script` 欄位中提供指令碼：

```json
GET students/_search
{
  "query": {
    "terms_set": {
      "classes": {
        "terms": [ "CS101", "CS102", "MATH101" ],
        "minimum_should_match_script": {
          "source": "Math.min(params.num_terms, doc['min_required'].value)"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

此查詢接受欄位名稱 (`<field>`) 作為最上層參數：

```json
GET _search
{
  "query": {
    "terms_set": {
      "<field>": {
        "terms": [ "term1", "term2" ],
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `terms` 之外，所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`terms` | 字串陣列 | 要在 `<field>` 中指定之欄位中搜尋的詞項陣列。只有在所需數量的詞項與文件的欄位值完全相符 (包括正確的空格與大小寫) 時，文件才會出現在結果中。
`minimum_should_match_field` | 字串 | [數值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) 欄位的名稱，該欄位指定要讓文件出現在結果中所需符合的詞項數量。您必須指定 `minimum_should_match_field` 或 `minimum_should_match_script`，但不能同時指定兩者。
`minimum_should_match_script` | 字串 | 傳回要讓文件出現在結果中所需符合之詞項數量的指令碼。您必須指定 `minimum_should_match_field` 或 `minimum_should_match_script`，但不能同時指定兩者。
`boost` | 浮點數 | 浮點值，指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設值為 1.0。
