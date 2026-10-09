---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立自訂分析器"
nav_order: 40
parent: Analyzers
---

# 建立自訂分析器

若要建立自訂分析器，請指定下列元件的組合：

- 字元篩選器（零個或多個）

- 斷詞器（一個）

- 詞元篩選器（零個或多個）

## 組態

下列參數可用來設定自訂分析器。

| 參數                | 必要／選用 | 說明  |
|:--- | :--- | :--- |
| `type`                   | 選用          | 分析器類型。預設為 `custom`。您也可以使用此參數指定預先建置的分析器。              |
| `tokenizer`              | 必要          | 要包含在分析器中的斷詞器。 |
| `char_filter`            | 選用          | 要包含在分析器中的字元篩選器清單。 |
| `filter`                 | 選用          | 要包含在分析器中的詞元篩選器清單。 |
| `position_increment_gap` | 選用          | 將具有多個值的文字欄位編製索引時，在各值之間套用的額外間距。如需詳細資訊，請參閱[位置增量間隔](#position-increment-gap)。預設為 `100`。 |

## 範例

下列範例示範各種自訂分析器組態。

### 使用字元篩選器移除 HTML 的自訂分析器

下列範例分析器會在斷詞前移除文字中的 HTML 標籤：

```json
PUT simple_html_strip_analyzer_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "html_strip_analyzer": {
          "type": "custom",
          "char_filter": ["html_strip"],
          "tokenizer": "whitespace",
          "filter": ["lowercase"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查此分析器產生的詞元：

```json
GET simple_html_strip_analyzer_index/_analyze
{
  "analyzer": "html_strip_analyzer",
  "text": "<p>OpenSearch is <strong>awesome</strong>!</p>"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 3,
      "end_offset": 13,
      "type": "word",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 14,
      "end_offset": 16,
      "type": "word",
      "position": 1
    },
    {
      "token": "awesome!",
      "start_offset": 25,
      "end_offset": 42,
      "type": "word",
      "position": 2
    }
  ]
}
```

### 使用對應字元篩選器替換同義詞的自訂分析器

下列範例分析器會在套用同義詞篩選器之前，替換特定字元和模式：

```json
PUT mapping_analyzer_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "synonym_mapping_analyzer": {
          "type": "custom",
          "char_filter": ["underscore_to_space"],
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "synonym_filter"]
        }
      },
      "char_filter": {
        "underscore_to_space": {
          "type": "mapping",
          "mappings": ["_ => ' '"]
        }
      },
      "filter": {
        "synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "quick, fast, speedy",
            "big, large, huge"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查此分析器產生的詞元：

```json
GET mapping_analyzer_index/_analyze
{
  "analyzer": "synonym_mapping_analyzer",
  "text": "The slow_green_turtle is very large"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "slow","start_offset": 4,"end_offset": 8,"type": "<ALPHANUM>","position": 1},
    {"token": "green","start_offset": 9,"end_offset": 14,"type": "<ALPHANUM>","position": 2},
    {"token": "turtle","start_offset": 15,"end_offset": 21,"type": "<ALPHANUM>","position": 3},
    {"token": "very","start_offset": 25,"end_offset": 29,"type": "<ALPHANUM>","position": 5},
    {"token": "large","start_offset": 30,"end_offset": 35,"type": "<ALPHANUM>","position": 6},
    {"token": "big","start_offset": 30,"end_offset": 35,"type": "SYNONYM","position": 6},
    {"token": "huge","start_offset": 30,"end_offset": 35,"type": "SYNONYM","position": 6}
  ]
}
```

### 使用自訂模式字元篩選器將號碼正規化的自訂分析器

下列範例分析器會移除連字號和空格，將電話號碼正規化，並對正規化後的文字套用 edge n-grams，以支援部分比對：

```json
PUT advanced_pattern_replace_analyzer_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "phone_number_analyzer": {
          "type": "custom",
          "char_filter": ["phone_normalization"],
          "tokenizer": "standard",
          "filter": ["lowercase", "edge_ngram"]
        }
      },
      "char_filter": {
        "phone_normalization": {
          "type": "pattern_replace",
          "pattern": "[-\\s]",
          "replacement": ""
        }
      },
      "filter": {
        "edge_ngram": {
          "type": "edge_ngram",
          "min_gram": 3,
          "max_gram": 10
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查此分析器產生的詞元：

```json
GET advanced_pattern_replace_analyzer_index/_analyze
{
  "analyzer": "phone_number_analyzer",
  "text": "123-456 7890"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "123","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "1234","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "12345","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "123456","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "1234567","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "12345678","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "123456789","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0},
    {"token": "1234567890","start_offset": 0,"end_offset": 12,"type": "<NUM>","position": 0}
  ]
}
```

## 處理正規表示式模式中的特殊字元

在分析器中使用自訂正規表示式模式時，請確保正確處理特殊字元或非英文字元。依預設，Java 的正規表示式只會將 `[A-Za-z0-9_]` 視為單字字元（`\w`）。這可能導致使用 `\w` 或 `\b` 時出現非預期的行為，這兩者會比對單字字元與非單字字元之間的邊界。  

例如，下列分析器嘗試使用模式 `(\b\p{L}+\b)`，比對任何語言中由單字邊界包圍的一個或多個字母字元（`\p{L}`）：  

```json
PUT /buggy_custom_analyzer
{
  "settings": {
    "analysis": {
      "filter": {
        "capture_words": {
          "type": "pattern_capture",
          "patterns": [
            "(\\b\\p{L}+\\b)"
          ]
        }
      },
      "analyzer": {
        "filter_only_analyzer": {
          "type": "custom",
          "tokenizer": "keyword",
          "filter": [
            "capture_words"
          ]
        }
      }
    }
  }
}
```  

然而，此分析器會錯誤地將 `él-empezó-a-reír` 斷詞為 `l`、`empez`、`a` 和 `reír`，因為 `\b` 無法比對帶有重音符號的字元與字串開頭或結尾之間的邊界。   

若要正確處理特殊字元，請將 Unicode 大小寫旗標 `(?U)` 加入您的模式：  

```json
PUT /fixed_custom_analyzer
{
  "settings": {
    "analysis": {
      "filter": {
        "capture_words": {
          "type": "pattern_capture",
          "patterns": [
            "(?U)(\\b\\p{L}+\\b)"
          ]
        }
      },
      "analyzer": {
        "filter_only_analyzer": {
          "type": "custom",
          "tokenizer": "keyword",
          "filter": [
            "capture_words"
          ]
        }
      }
    }
  }
}
```  
{% include copy-curl.html %}

## 位置增量間隔

`position_increment_gap` 參數會在將陣列等多值欄位編製索引時，設定詞彙之間的位置間隔。此間隔可確保片語查詢不會比對不同值中的詞彙，除非明確允許。例如，預設間隔 100 表示不同陣列項目中的詞彙相距 100 個位置，可避免片語搜尋中出現非預期的比對。您可以調整此值，或將其設為 `0`，以允許片語跨越陣列中的不同值。

下列範例使用 `match_phrase` 查詢示範 `position_increment_gap` 的效果。

1. 在 `test-index` 中將文件編製索引：

     ```json
     PUT test-index/_doc/1
     {
       "names": [ "Slow green", "turtle swims"]
     }
     ```
     {% include copy-curl.html %}

1. 使用 `match_phrase` 查詢來查詢文件：

    ```json
    GET test-index/_search
    {
      "query": {
        "match_phrase": {
          "names": {
            "query": "green turtle" 
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}
    
    回應未傳回任何命中結果，因為詞彙 `green` 和 `turtle` 之間的距離為 `100`（預設的 `position_increment_gap`）。

1. 現在使用 `match_phrase` 查詢來查詢文件，並將 `slop` 參數設為大於 `position_increment_gap` 的值：

    ```json
    GET test-index/_search
    {
      "query": {
        "match_phrase": {
          "names": {
            "query": "green turtle",
            "slop": 101
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

    回應包含符合的文件：

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
          "value": 1,
          "relation": "eq"
        },
        "max_score": 0.010358453,
        "hits": [
          {
            "_index": "test-index",
            "_id": "1",
            "_score": 0.010358453,
            "_source": {
              "names": [
                "Slow green",
                "turtle swims"
              ]
            }
          }
        ]
      }
    }
    ```
