---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分隔詞頻"
parent: Token filters
nav_order: 100
---

# 分隔詞頻詞元篩選器

`delimited_term_freq` 詞元篩選器會根據提供的分隔符號，將詞元串流分隔為詞元及其對應的詞頻。詞元由分隔符號之前的所有字元組成，而詞頻則是分隔符號之後的整數。例如，若分隔符號為 `|`，則對於字串 `foo|5`，`foo` 是詞元，`5` 是其詞頻。若沒有分隔符號，詞元篩選器不會修改詞頻。

您可以使用預先設定的 `delimited_term_freq` 詞元篩選器，或建立自訂的詞元篩選器。

## 預先設定的 `delimited_term_freq` 詞元篩選器

預先設定的 `delimited_term_freq` 詞元篩選器使用 `|` 預設分隔符號。若要使用預先設定的詞元篩選器分析文字，請將下列請求傳送至 `_analyze` 端點：

```json
POST /_analyze
{
  "text": "foo|100",
  "tokenizer": "keyword",
  "filter": ["delimited_term_freq"],
  "attributes": ["termFrequency"],
  "explain": true
}
```
{% include copy-curl.html %}

`attributes` 陣列指定您要篩選 `explain` 參數的輸出，僅傳回 `termFrequency`。回應同時包含原始詞元，以及詞元篩選器剖析後包含詞頻的輸出：

```json
{
  "detail": {
    "custom_analyzer": true,
    "charfilters": [],
    "tokenizer": {
      "name": "keyword",
      "tokens": [
        {
          "token": "foo|100",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0,
          "termFrequency": 1
        }
      ]
    },
    "tokenfilters": [
      {
        "name": "delimited_term_freq",
        "tokens": [
          {
            "token": "foo",
            "start_offset": 0,
            "end_offset": 7,
            "type": "word",
            "position": 0,
            "termFrequency": 100
          }
        ]
      }
    ]
  }
}
```

## 自訂 `delimited_term_freq` 詞元篩選器

若要設定自訂的 `delimited_term_freq` 詞元篩選器，請先在對應請求中指定分隔符號，本範例中為 `^`：

```json
PUT /testindex
{
  "settings": {
    "analysis": {
      "filter": {
        "my_delimited_term_freq": {
          "type": "delimited_term_freq",
          "delimiter": "^"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

接著使用您建立的自訂詞元篩選器分析文字：

```json
POST /testindex/_analyze
{
  "text": "foo^3",
  "tokenizer": "keyword",
  "filter": ["my_delimited_term_freq"],
  "attributes": ["termFrequency"],
  "explain": true
}
```
{% include copy-curl.html %}

回應同時包含原始詞元，以及剖析後包含詞頻的版本：

```json
{
  "detail": {
    "custom_analyzer": true,
    "charfilters": [],
    "tokenizer": {
      "name": "keyword",
      "tokens": [
        {
          "token": "foo|100",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0,
          "termFrequency": 1
        }
      ]
    },
    "tokenfilters": [
      {
        "name": "delimited_term_freq",
        "tokens": [
          {
            "token": "foo",
            "start_offset": 0,
            "end_offset": 7,
            "type": "word",
            "position": 0,
            "termFrequency": 100
          }
        ]
      }
    ]
  }
}
```

## 將 `delimited_token_filter` 與指令碼搭配使用

您可以撰寫 Painless 指令碼，為結果中的文件計算自訂分數。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

首先，建立索引並提供下列對應與設定：

```json
PUT /test
{
  "settings": {
    "number_of_shards": 1,
    "analysis": {
      "tokenizer": {
        "keyword_tokenizer": {
          "type": "keyword"
        }
      },
      "filter": {
        "my_delimited_term_freq": {
          "type": "delimited_term_freq",
          "delimiter": "^"
        }
      },
      "analyzer": {
        "custom_delimited_analyzer": {
          "tokenizer": "keyword_tokenizer",
          "filter": ["my_delimited_term_freq"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "f1": {
        "type": "keyword"
      },
      "f2": {
        "type": "text",
        "analyzer": "custom_delimited_analyzer",
        "index_options": "freqs"
      }
    }
  }
}
```
{% include copy-curl.html %}

`test` 索引使用 keyword 斷詞器、分隔詞頻詞元篩選器（其分隔符號為 `^`），以及包含 keyword 斷詞器與分隔詞頻詞元篩選器的自訂分析器。對應指定欄位 `f1` 為 keyword 欄位，欄位 `f2` 為 text 欄位。欄位 `f2` 使用設定中定義的自訂分析器進行文字分析。此外，指定 `index_options` 會通知 OpenSearch 將詞頻加入反向索引。您將使用詞頻為含有重複詞彙的文件提供較高的分數。

接著，使用大量上傳將兩份文件編製索引：

```json
POST /_bulk?refresh=true
{"index": {"_index": "test", "_id": "doc1"}}
{"f1": "v0|100", "f2": "v1^30"}
{"index": {"_index": "test", "_id": "doc2"}}
{"f2": "v2|100"}
```
{% include copy-curl.html %}

下列查詢會搜尋索引中的所有文件，並以欄位 `f2` 中詞彙 `v1` 的詞頻作為文件分數：

```json
GET /test/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": "termFreq(params.field, params.term)",
          "params": {
            "field": "f2",
            "term": "v1"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

在回應中，文件 1 的分數為 30，因為欄位 `f2` 中詞彙 `v1` 的詞頻為 30。文件 2 的分數為 0，因為詞彙 `v1` 未出現在 `f2` 中：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 30,
    "hits": [
      {
        "_index": "test",
        "_id": "doc1",
        "_score": 30,
        "_source": {
          "f1": "v0|100",
          "f2": "v1^30"
        }
      },
      {
        "_index": "test",
        "_id": "doc2",
        "_score": 0,
        "_source": {
          "f2": "v2|100"
        }
      }
    ]
  }
}
```

## 參數

下表列出 `delimited_term_freq` 支援的所有參數。

參數 | 必要/選用 | 說明
:--- | :--- | :---
`delimiter` | 選用 | 用於將詞元與詞頻分隔的分隔符號。必須是單一非 null 字元。預設為 `|`。