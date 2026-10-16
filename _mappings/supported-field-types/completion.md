---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Completion
nav_order: 51
has_children: false
parent: Autocomplete field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/completion/
  - /opensearch/supported-field-types/completion/
  - /field-types/completion/
---

# Completion 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

Completion 欄位類型透過 completion suggester 提供自動完成功能。Completion suggester 是一種前綴建議器，因此只會比對文字的開頭。Completion suggester 會建立記憶體內資料結構，查詢速度較快，但會增加記憶體用量。使用此功能前，您需要將所有可能的完成項清單上傳至索引。

## 範例

建立包含 completion 欄位的對應：

```json
PUT chess_store
{
  "mappings": {
    "properties": {
      "suggestions": {
        "type": "completion"
      },
      "product": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 對應參數

`completion` 欄位類型支援下列對應參數。

| 參數   | 說明   |
| :--- | :--- |
| `analyzer` | 指定輸入文字在索引時使用的分析器。預設為 `simple`。請參閱[索引分析器]({{site.url}}{{site.baseurl}}/analyzers/index-analyzers/)。更多資訊請參閱[分析器]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/analyzer/)。 |
| `search_analyzer` | 定義搜尋時使用的分析器。預設為 `analyzer` 的值。請參閱[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。更多資訊請參閱[搜尋分析器]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/search-analyzer/)。 |
| `preserve_separators` | 若為 `true`（預設），會保留空格或標點符號等分隔符。若設為 `false`，則允許 `queensg` 這類查詢比對到「Queen's Gambit」這類建議。    |
| `preserve_position_increments` | 若為 `true`（預設），會保留分析後詞元的位置增量。將此設為 `false` 時，輸入 `s` 可以比對到「The Sicilian Defense」這類建議，因為它會跳過「The」這類停用詞。或者，您也可以將「Sicilian Defense」和「The Sicilian Defense」作為個別輸入編製索引，而不變更分析器。 |
| `max_input_length`             | 限制每個輸入字串的長度。預設為 `50` 個 UTF-16 字碼指標。此限制僅在索引時生效，以防止過大的輸入使底層資料結構膨脹。大多數前綴補全在此限制內都能正常運作。可動態更新。 |

### 對應範例

```json
PUT chess_store
{
  "mappings": {
    "properties": {
      "suggestions": {
        "type": "completion",
        "analyzer": "standard"
      },
      "product": {
        "type": "keyword"
      }
    }
  }
}
```

將建議編製索引至 OpenSearch：

```json
PUT chess_store/_doc/1
{
  "suggestions": {
      "input": ["Books on openings", "Books on endgames"],
      "weight" : 10
    }
}
```
{% include copy-curl.html %}

## 參數

下表列出 completion 欄位接受的參數。

參數 | 說明 
:--- | :--- 
`input` | 可能的完成項清單，以字串或字串陣列表示。不可包含 `\u0000`（空字元）、`\u001f`（資訊分隔符一）或 `\u001e`（資訊分隔符二）。必要。
`weight` | 用於為建議排序的正整數或正整數字串。選用。

多個建議可依下列方式編製索引：

```json
PUT chess_store/_doc/2
{
  "suggestions": [
    {
      "input": "Chess set",
      "weight": 20
    },
    {
      "input": "Chess pieces",
      "weight": 10
    },
    {
      "input": "Chess board",
      "weight": 5
    }
  ]
}
```
{% include copy-curl.html %}

或者，您可以使用下列簡寫標記法（請注意，此標記法無法提供 `weight` 參數）：

```json
PUT chess_store/_doc/3
{
  "suggestions" : [ "Chess clock", "Chess timer" ]
}
```
{% include copy-curl.html %}

## 查詢 completion 欄位類型

若要查詢 completion 欄位類型，請指定要搜尋的前綴，以及要在其中尋找建議的欄位名稱。

查詢索引中以「chess」一詞開頭的建議：

```json
GET chess_store/_search
{
  "suggest": {
    "product-suggestions": {
      "prefix": "chess",        
      "completion": {         
          "field": "suggestions"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含自動完成建議：

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
      "value" : 0,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "suggest" : {
    "product-suggestions" : [
      {
        "text" : "chess",
        "offset" : 0,
        "length" : 5,
        "options" : [
          {
            "text" : "Chess set",
            "_index" : "chess_store",
            "_type" : "_doc",
            "_id" : "2",
            "_score" : 20.0,
            "_source" : {
              "suggestions" : [
                {
                  "input" : "Chess set",
                  "weight" : 20
                },
                {
                  "input" : "Chess pieces",
                  "weight" : 10
                },
                {
                  "input" : "Chess board",
                  "weight" : 5
                }
              ]
            }
          },
          {
            "text" : "Chess clock",
            "_index" : "chess_store",
            "_type" : "_doc",
            "_id" : "3",
            "_score" : 1.0,
            "_source" : {
              "suggestions" : [
                "Chess clock",
                "Chess timer"
              ]
            }
          }
        ]
      }
    ]
  }
}
```

在回應中，`_score` 欄位包含索引時設定的 `weight` 參數值。`text` 欄位則填入建議的 `input` 參數。

預設情況下，回應包含整份文件，包括 `_source` 欄位，這可能影響效能。若只要傳回 `suggestions` 欄位，您可以在 `_source` 參數中指定。您也可以透過指定 `size` 參數來限制傳回的建議數量。

```json
GET chess_store/_search
{
  "_source": "suggestions", 
  "suggest": {
    "product-suggestions": {
      "prefix": "chess",        
      "completion": {         
          "field": "suggestions",
          "size" : 3
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含建議：

```json
{
  "took" : 5,
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
  },
  "suggest" : {
    "product-suggestions" : [
      {
        "text" : "chess",
        "offset" : 0,
        "length" : 5,
        "options" : [
          {
            "text" : "Chess set",
            "_index" : "chess_store",
            "_type" : "_doc",
            "_id" : "2",
            "_score" : 20.0,
            "_source" : {
              "suggestions" : [
                {
                  "input" : "Chess set",
                  "weight" : 20
                },
                {
                  "input" : "Chess pieces",
                  "weight" : 10
                },
                {
                  "input" : "Chess board",
                  "weight" : 5
                }
              ]
            }
          },
          {
            "text" : "Chess clock",
            "_index" : "chess_store",
            "_type" : "_doc",
            "_id" : "3",
            "_score" : 1.0,
            "_source" : {
              "suggestions" : [
                "Chess clock",
                "Chess timer"
              ]
            }
          }
        ]
      }
    ]
  }
}
```

若要利用來源篩選，請在 `_search` 端點上使用 suggest 功能。`_suggest` 端點不支援來源篩選。
{: .note}

## Completion 查詢參數

下表列出 completion suggester 查詢接受的參數。

參數 | 說明 
:--- | :--- 
`field` | 指定執行查詢之欄位的字串。必要。
`size` | 指定傳回建議數量上限的整數。選用。預設為 5。
`skip_duplicates` | 指定是否略過重複建議的布林值。選用。預設為 `false`。

## 模糊完成查詢

若要允許模糊比對，您可以為完成查詢指定 `fuzziness` 參數。在此情況下，即使使用者拼錯搜尋詞，完成查詢仍會傳回結果。此外，符合查詢的前置字串越長，文件的分數越高。

```json
GET chess_store/_search
{
  "suggest": {
    "product-suggestions": {
      "prefix": "chesc",        
      "completion": {         
          "field": "suggestions",
          "size" : 3,
          "fuzzy" : {
            "fuzziness" : "AUTO"
          }
      }
    }
  }
}
```
{% include copy-curl.html %}

若要使用所有預設的模糊選項，請指定 `"fuzzy": {}` 或 `"fuzzy": true`。
{: .tip}

下表列出 `fuzzy` 完成建議器查詢可接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`fuzziness` | 比對前置字串時允許的最大編輯次數，指定為 `0`、`1`、`2`、`AUTO` 或 `AUTO:<low>,<high>`。預設為 `AUTO`。如需更多資訊，請參閱 [Fuzziness]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)。
`min_length` | 整數，指定開始傳回建議時輸入必須達到的最小長度。若搜尋詞短於 `min_length`，則不會傳回任何建議。預設為 3。
`prefix_length` | 整數，指定開始傳回建議時符合的前置字串必須達到的最小長度。若 `prefix_length` 的前置字串不相符，但搜尋詞仍在 Damerau–Levenshtein 距離內，則不會傳回任何建議。預設為 1。
`transpositions` | 布林值，指定是否將換位（相鄰字元互換）計為一次編輯而非兩次。範例：建議的 `input` 參數為 `abcde`，且 `fuzziness` 為 1。若 `transpositions` 設為 `true`，`abdce` 會相符，但若 `transpositions` 設為 `false`，`abdce` 則不會相符。預設為 `true`。
`unicode_aware` | 布林值，指定在測量編輯距離、換位與長度時是否使用 Unicode 碼點。若 `unicode_aware` 設為 `true`，測量速度會較慢。預設為 `false`，在此情況下距離以位元組為單位測量。

## 正規表示式查詢

您可以使用正規表示式來定義 completion suggester 查詢的前綴。

例如，若要搜尋以「a」開頭且後面含有「d」的字串，請使用下列查詢：

```json
GET chess_store/_search
{
  "suggest": {
    "product-suggestions": {
      "regex": "a.*d",        
      "completion": {         
          "field": "suggestions"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會比對出字串 `"abcde"`：

```json
{
  "took" : 2,
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
  },
  "suggest" : {
    "product-suggestions" : [
      {
        "text" : "a.*d",
        "offset" : 0,
        "length" : 4,
        "options" : [
          {
            "text" : "abcde",
            "_index" : "chess_store",
            "_type" : "_doc",
            "_id" : "2",
            "_score" : 20.0,
            "_source" : {
              "suggestions" : [
                {
                  "input" : "abcde",
                  "weight" : 20
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```
