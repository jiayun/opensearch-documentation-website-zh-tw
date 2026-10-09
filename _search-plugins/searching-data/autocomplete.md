---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動完成"
parent: Customizing search results
nav_order: 80
redirect_from:
  - /opensearch/search/autocomplete/
---

# 自動完成

自動完成會在使用者輸入時顯示建議。

例如，當使用者輸入 "pop" 時，OpenSearch 會提供 "popcorn" 或 "popsicles" 之類的建議。這些建議能預先掌握使用者的意圖，更快引導他們找到可能的搜尋詞彙。

OpenSearch 讓您設計的自動完成能隨著每次按鍵更新、提供幾個相關的建議，並容許拼字錯誤。

請使用下列其中一種方法來實作自動完成：

- [前綴比對](#prefix-matching)
- [邊緣 n-gram 比對](#edge-n-gram-matching)
- [邊輸入邊搜尋](#search-as-you-type)
- [完成建議器](#completion-suggester)

前綴比對發生在查詢時，其他三種方法則發生在索引時。所有方法都會在下列章節中說明。

## 前綴比對

前綴比對會找出與查詢字串中最後一個詞彙相符的文件。

例如，假設使用者在搜尋介面中輸入 "qui"。若要自動完成這個詞組，請使用 `match_phrase_prefix` 查詢來搜尋所有以前綴 "qui" 開頭的 `text_entry` 欄位值：

```json
GET shakespeare/_search
{
  "query": {
    "match_phrase_prefix": {
      "text_entry": {
        "query": "qui",
        "slop": 3
      }
    }
  }
}
```

若要讓字詞順序和相對位置保持彈性，請指定 `slop` 值。若要了解 `slop` 選項，請參閱 [Slop]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase#slop)。

前綴比對不需要任何特殊的對應，可直接搭配您現有的資料使用。
不過，這是相當耗費資源的操作。`a` 這樣的前綴可能會比對到數十萬個詞彙，反而對使用者沒有幫助。
若要限制前綴展開的影響，請將 `max_expansions` 設定為合理的數值：

```json
GET shakespeare/_search
{
  "query": {
    "match_phrase_prefix": {
      "text_entry": {
        "query": "qui",
        "slop": 3,
        "max_expansions": 10
      }
    }
  }
}
```

這是查詢可展開的詞彙數量上限。查詢會將搜尋詞彙「展開」為 `fuzziness` 所指定距離內的多個相符詞彙。

在查詢時實作自動完成雖然容易，但代價是效能。
若要大規模實作此功能，我們建議採用索引時的解決方案。使用索引時的解決方案，索引速度可能會變慢，但這個代價只需支付一次，而不是每次查詢都要支付。邊緣 n-gram、邊輸入邊搜尋和完成建議器方法都是索引時的解決方案。

## 邊緣 n-gram 比對

在編製索引期間，邊緣 n-gram 會將一個單字拆解成 n 個字元的序列，以支援更快速地查詢部分搜尋詞彙。

若對 "quick" 這個單字進行 n-gram 處理，結果取決於 n 的值。

n | 類型 | n-gram
:--- | :--- | :---
1 | Unigram | [ `q`, `u`, `i`, `c`, `k` ]
2 | Bigram | [ `qu`, `ui`, `ic`, `ck` ]
3 | Trigram | [ `qui`, `uic`, `ick` ]
4 | Four-gram | [ `quic`, `uick` ]
5 | Five-gram | [ `quick` ]

自動完成只需要搜尋詞組開頭的 n-gram，因此 OpenSearch 使用一種稱為*邊緣 n-gram* 的特殊 n-gram 類型。

對 "quick" 進行邊緣 n-gram 處理的結果如下：

- `q`
- `qu`
- `qui`
- `quic`
- `quick`

這與使用者輸入的順序一致。

若要將欄位設定為使用邊緣 n-gram，請建立一個帶有 `edge_ngram` 篩選器的自動完成分析器：


```json
PUT shakespeare
{
  "mappings": {
    "properties": {
      "text_entry": {
        "type": "text",
        "analyzer": "autocomplete"
      }
    }
  },
  "settings": {
    "analysis": {
      "filter": {
        "edge_ngram_filter": {
          "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "edge_ngram_filter"
          ]
        }
      }
    }
  }
}
```

此範例會建立索引，並具體化邊緣 n-gram 篩選器與分析器。

`edge_ngram_filter` 會產生最小 n-gram 長度為 1（單一字母）、最大長度為 20 的邊緣 n-gram。因此它可為最多 20 個字母的單字提供建議。

`autocomplete` 分析器會將字串斷詞成個別詞彙、將詞彙轉為小寫，然後使用 `edge_ngram_filter` 為每個詞彙產生邊緣 n-gram。

請使用 `analyze` 操作來測試此分析器：

```json
POST shakespeare/_analyze
{
  "analyzer": "autocomplete",
  "text": "quick"
}
```

它會以詞元形式傳回邊緣 n-gram：

* `q`
* `qu`
* `qui`
* `quic`
* `quick`

請在搜尋時使用 `standard` 分析器。否則，搜尋查詢會被拆解成邊緣 n-gram，您會得到所有符合 `q`、`u` 和 `i` 的結果。
這是少數幾個在索引時和查詢時使用不同分析器的情況之一：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": {
        "query": "qui",
        "analyzer": "standard"
      }
    }
  }
}
```

回應包含相符的文件：

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 533,
      "relation": "eq"
    },
    "max_score": 9.712725,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "22006",
        "_score": 9.712725,
        "_source": {
          "type": "line",
          "line_id": 22007,
          "play_name": "Antony and Cleopatra",
          "speech_number": 12,
          "line_number": "5.2.44",
          "speaker": "CLEOPATRA",
          "text_entry": "Quick, quick, good hands."
        }
      },
      {
        "_index": "shakespeare",
        "_id": "54665",
        "_score": 9.712725,
        "_source": {
          "type": "line",
          "line_id": 54666,
          "play_name": "Loves Labours Lost",
          "speech_number": 21,
          "line_number": "5.1.52",
          "speaker": "HOLOFERNES",
          "text_entry": "Quis, quis, thou consonant?"
        }
      }
      ...
    ]
  }
}
```

或者，您也可以直接在對應中指定 `search_analyzer`：

```json
"mappings": {
  "properties": {
    "text_entry": {
      "type": "text",
      "analyzer": "autocomplete",
      "search_analyzer": "standard"
    }
  }
}
```

## 完成建議器

完成建議器會接受一份建議清單，並將其建構成有限狀態轉換器 (FST)，這是一種本質上為圖形的最佳化資料結構。此資料結構存放在記憶體中，並針對快速的前綴查詢進行最佳化。若要進一步了解 FST，請參閱 [Wikipedia](https://en.wikipedia.org/wiki/Finite-state_transducer)。

當使用者輸入時，完成建議器會沿著相符路徑在 FST 圖形中一次移動一個字元。當使用者輸入用完後，它會檢查剩餘的結尾，以產生建議清單。

完成建議器能讓您的自動完成解決方案盡可能高效，並讓您明確控制其建議內容。

請使用名為 [`completion`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/completion/) 的專用欄位類型，它會將類似 FST 的資料結構儲存在索引中：

```json
PUT shakespeare
{
  "mappings": {
    "properties": {
      "text_entry": {
        "type": "completion"
      }
    }
  }
}
```

若要取得建議，請使用 `search` 端點搭配 `suggest` 參數：

```json
GET shakespeare/_search
{
  "suggest": {
    "autocomplete": {
      "prefix": "To be",
      "completion": {
        "field": "text_entry"
      }
    }
  }
}
```

詞組 "to be" 會與 `text_entry` 欄位的 FST 進行前綴比對：

```json
{
  "took" : 29,
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
    "autocomplete" : [
      {
        "text" : "To be",
        "offset" : 0,
        "length" : 5,
        "options" : [
          {
            "text" : "To be a comrade with the wolf and owl,--",
            "_index" : "shakespeare",
            "_id" : "50652",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 50653,
              "play_name" : "King Lear",
              "speech_number" : 68,
              "line_number" : "2.4.230",
              "speaker" : "KING LEAR",
              "text_entry" : "To be a comrade with the wolf and owl,--"
            }
          },
          {
            "text" : "To be a make-peace shall become my age:",
            "_index" : "shakespeare",
            "_id" : "78566",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 78567,
              "play_name" : "Richard II",
              "speech_number" : 20,
              "line_number" : "1.1.160",
              "speaker" : "JOHN OF GAUNT",
              "text_entry" : "To be a make-peace shall become my age:"
            }
          },
          {
            "text" : "To be a party in this injury.",
            "_index" : "shakespeare",
            "_id" : "75259",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 75260,
              "play_name" : "Othello",
              "speech_number" : 57,
              "line_number" : "5.1.93",
              "speaker" : "IAGO",
              "text_entry" : "To be a party in this injury."
            }
          },
          {
            "text" : "To be a preparation gainst the Polack;",
            "_index" : "shakespeare",
            "_id" : "33591",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 33592,
              "play_name" : "Hamlet",
              "speech_number" : 17,
              "line_number" : "2.2.67",
              "speaker" : "VOLTIMAND",
              "text_entry" : "To be a preparation gainst the Polack;"
            }
          },
          {
            "text" : "To be a public spectacle to all:",
            "_index" : "shakespeare",
            "_id" : "3709",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 3710,
              "play_name" : "Henry VI Part 1",
              "speech_number" : 6,
              "line_number" : "1.4.41",
              "speaker" : "TALBOT",
              "text_entry" : "To be a public spectacle to all:"
            }
          }
        ]
      }
    ]
  }
}
```

若要指定要傳回的建議數量，請使用 `size` 參數：

```json
GET shakespeare/_search
{
  "suggest": {
    "autocomplete": {
      "prefix": "To n",
      "completion": {
        "field": "text_entry",
        "size": 3
      }
    }
  }
}
```

最多會傳回三份文件：

```json
{
  "took" : 4109,
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
    "autocomplete" : [
      {
        "text" : "To n",
        "offset" : 0,
        "length" : 4,
        "options" : [
          {
            "text" : "To NESTOR",
            "_index" : "shakespeare",
            "_id" : "99707",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 99708,
              "play_name" : "Troilus and Cressida",
              "speech_number" : 3,
              "line_number" : "",
              "speaker" : "ULYSSES",
              "text_entry" : "To NESTOR"
            }
          },
          {
            "text" : "To name the bigger light, and how the less,",
            "_index" : "shakespeare",
            "_id" : "91884",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 91885,
              "play_name" : "The Tempest",
              "speech_number" : 91,
              "line_number" : "1.2.394",
              "speaker" : "CALIBAN",
              "text_entry" : "To name the bigger light, and how the less,"
            }
          },
          {
            "text" : "To nature none more bound; his training such,",
            "_index" : "shakespeare",
            "_id" : "40510",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 40511,
              "play_name" : "Henry VIII",
              "speech_number" : 18,
              "line_number" : "1.2.126",
              "speaker" : "KING HENRY VIII",
              "text_entry" : "To nature none more bound; his training such,"
            }
          }
        ]
      }
    ]
  }
}
```

`suggest` 參數只使用前綴比對來尋找建議。
例如，文件「To be, or not to be」不會出現在結果中。如果您想要特定文件以建議的形式傳回，可以手動新增精選建議，並新增權重來排定建議的優先順序。

將含有輸入建議的文件編製索引並指派權重：

```json
PUT shakespeare/_doc/1?refresh=true
{
  "text_entry": {
    "input": [
      "To n", "To be, or not to be: that is the question:"
    ],
    "weight": 10
  }
}
```

執行相同的搜尋：

```json
GET shakespeare/_search
{
  "suggest": {
    "autocomplete": {
      "prefix": "To n",
      "completion": {
        "field": "text_entry",
        "size": 3
      }
    }
  }
}
```

您會看到已編製索引的文件成為第一個結果：

```json
{
  "took" : 1,
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
    "autocomplete" : [
      {
        "text" : "To n",
        "offset" : 0,
        "length" : 4,
        "options" : [
          {
            "text" : "To n",
            "_index" : "shakespeare",
            "_id" : "1",
            "_score" : 10.0,
            "_source" : {
              "text_entry" : {
                "input" : [
                  "To n",
                  "To be, or not to be: that is the question:"
                ],
                "weight" : 10
              }
            }
          },
          {
            "text" : "To NESTOR",
            "_index" : "shakespeare",
            "_id" : "99707",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 99708,
              "play_name" : "Troilus and Cressida",
              "speech_number" : 3,
              "line_number" : "",
              "speaker" : "ULYSSES",
              "text_entry" : "To NESTOR"
            }
          },
          {
            "text" : "To name the bigger light, and how the less,",
            "_index" : "shakespeare",
            "_id" : "91884",
            "_score" : 1.0,
            "_source" : {
              "type" : "line",
              "line_id" : 91885,
              "play_name" : "The Tempest",
              "speech_number" : 91,
              "line_number" : "1.2.394",
              "speaker" : "CALIBAN",
              "text_entry" : "To name the bigger light, and how the less,"
            }
          }
        ]
      }
    ]
  }
}
```

您也可以在查詢中允許拼字錯誤，方法是指定 `fuzzy` 參數：

```json
GET shakespeare/_search
{
  "suggest": {
    "autocomplete": {
      "prefix": "rosenkrantz",
      "completion": {
        "field": "text_entry",
        "size": 3,
        "fuzzy" : {
            "fuzziness" : "AUTO"
        }
      }
    }
  }
}
```

結果會符合正確的拼字：

```json
{
  "took" : 1,
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
    "autocomplete" : [
      {
        "text" : "rosenkrantz",
        "offset" : 0,
        "length" : 11,
        "options" : [
          {
            "text" : "ROSENCRANTZ:",
            "_index" : "shakespeare",
            "_id" : "35196",
            "_score" : 5.0,
            "_source" : {
              "type" : "line",
              "line_id" : 35197,
              "play_name" : "Hamlet",
              "speech_number" : 2,
              "line_number" : "4.2.1",
              "speaker" : "HAMLET",
              "text_entry" : "ROSENCRANTZ:"
            }
          }
        ]
      }
    ]
  }
}
```

您可以使用規則運算式來定義完成建議器查詢的前綴：

```json
GET shakespeare/_search
{
  "suggest": {
    "autocomplete": {
      "prefix": "rosen*",
      "completion": {
        "field": "text_entry",
        "size": 3
      }
    }
  }
}
```

如需詳細資訊，請參閱 [`completion` 欄位類型文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/completion/)。

## 邊輸入邊搜尋

OpenSearch 有專用的 [`search_as_you_type`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/search-as-you-type/) 欄位類型，已針對邊輸入邊搜尋功能最佳化，並可使用前綴與中綴完成來比對詞彙。`search_as_you_type` 欄位不需要您事先設定自訂分析器，也不需要事先將建議編製索引。

首先，將欄位對應為 `search_as_you_type`：

```json
PUT shakespeare
{
  "mappings": {
    "properties": {
      "text_entry": {
        "type": "search_as_you_type"
      }
    }
  }
}
```

將文件編製索引後，OpenSearch 會自動建立並儲存其 n-gram 與邊緣 n-gram。例如，假設有字串 `that is the question`。首先，會使用標準分析器將其分割成詞彙，並將這些詞彙儲存在 `text_entry` 欄位中：

```json
[
    "that",
    "is",
    "the",
    "question"
]
```

除了儲存這些詞彙之外，此欄位的下列 2-gram 會儲存在 `text_entry._2gram` 欄位中：

```json
[
    "that is",
    "is the",
    "the question"
]
```

此欄位的下列 3-gram 會儲存在 `text_entry._3gram` 欄位中：

```json
[
    "that is the",
    "is the question"
]
```

最後，套用邊緣 n-gram 詞元篩選器之後，產生的詞彙會儲存在 `text_entry._index_prefix` 欄位中：

```json
[
    "t", 
    "th", 
    "tha", 
    "that", 
    ...
]
```

接著，您可以使用 `multi-match` 查詢的 `bool_prefix` 類型，以任何順序比對詞彙：

```json
GET shakespeare/_search
{
  "query": {
    "multi_match": {
      "query": "uncle what",
      "type": "bool_prefix",
      "fields": [
        "text_entry",
        "text_entry._2gram",
        "text_entry._3gram"
      ]
    }
  },
  "size": 3
}
```

在結果中，字詞出現順序與查詢中相同的文件會排在較前面：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4759,
      "relation" : "eq"
    },
    "max_score" : 10.437667,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "2817",
        "_score" : 10.437667,
        "_source" : {
          "type" : "line",
          "line_id" : 2818,
          "play_name" : "Henry IV",
          "speech_number" : 5,
          "line_number" : "5.2.31",
          "speaker" : "HOTSPUR",
          "text_entry" : "Uncle, what news?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "37085",
        "_score" : 9.437667,
        "_source" : {
          "type" : "line",
          "line_id" : 37086,
          "play_name" : "Henry V",
          "speech_number" : 26,
          "line_number" : "1.2.262",
          "speaker" : "KING HENRY V",
          "text_entry" : "What treasure, uncle?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "79274",
        "_score" : 9.358302,
        "_source" : {
          "type" : "line",
          "line_id" : 79275,
          "play_name" : "Richard II",
          "speech_number" : 29,
          "line_number" : "2.1.187",
          "speaker" : "KING RICHARD II",
          "text_entry" : "Why, uncle, whats the matter?"
        }
      }
    ]
  }
}
```

若要依序比對詞彙，您可以使用 `match_phrase_prefix` 查詢：

```json
GET shakespeare/_search
{
  "query": {
    "match_phrase_prefix": {
      "text_entry": "uncle wha"
    }
  },
  "size": 3
}
```

回應會包含符合前綴的文件：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 6,
      "relation" : "eq"
    },
    "max_score" : 16.37664,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "2817",
        "_score" : 16.37664,
        "_source" : {
          "type" : "line",
          "line_id" : 2818,
          "play_name" : "Henry IV",
          "speech_number" : 5,
          "line_number" : "5.2.31",
          "speaker" : "HOTSPUR",
          "text_entry" : "Uncle, what news?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "6789",
        "_score" : 16.37664,
        "_source" : {
          "type" : "line",
          "line_id" : 6790,
          "play_name" : "Henry VI Part 2",
          "speech_number" : 60,
          "line_number" : "1.3.202",
          "speaker" : "KING HENRY VI",
          "text_entry" : "Uncle, what shall we say to this in law?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "7877",
        "_score" : 16.37664,
        "_source" : {
          "type" : "line",
          "line_id" : 7878,
          "play_name" : "Henry VI Part 2",
          "speech_number" : 13,
          "line_number" : "3.2.28",
          "speaker" : "KING HENRY VI",
          "text_entry" : "Where is our uncle? whats the matter, Suffolk?"
        }
      }
    ]
  }
}
```

最後，若要完全比對最後一個詞彙而非以前綴比對，您可以使用 `match_phrase` 查詢：

```json
GET shakespeare/_search
{
  "query": {
    "match_phrase": {
      "text_entry": "uncle what"
    }
  },
  "size": 5
}
```

回應會包含完全相符的項目：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 14.437452,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "2817",
        "_score" : 14.437452,
        "_source" : {
          "type" : "line",
          "line_id" : 2818,
          "play_name" : "Henry IV",
          "speech_number" : 5,
          "line_number" : "5.2.31",
          "speaker" : "HOTSPUR",
          "text_entry" : "Uncle, what news?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "6789",
        "_score" : 9.461917,
        "_source" : {
          "type" : "line",
          "line_id" : 6790,
          "play_name" : "Henry VI Part 2",
          "speech_number" : 60,
          "line_number" : "1.3.202",
          "speaker" : "KING HENRY VI",
          "text_entry" : "Uncle, what shall we say to this in law?"
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "100955",
        "_score" : 8.947967,
        "_source" : {
          "type" : "line",
          "line_id" : 100956,
          "play_name" : "Troilus and Cressida",
          "speech_number" : 28,
          "line_number" : "3.2.98",
          "speaker" : "CRESSIDA",
          "text_entry" : "Well, uncle, what folly I commit, I dedicate to you."
        }
      }
    ]
  }
}
```

如果您修改前一個 `match_phrase` 查詢中的文字並省略最後一個字母，則前一個回應中的所有文件都不會被傳回：

```json
GET shakespeare/_search
{
  "query": {
    "match_phrase": {
      "text_entry": "uncle wha"
    }
  }
}
```

結果為空：

```json
{
  "took" : 1,
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

如需更多資訊，請參閱 [`search_as_you_type` 欄位類型文件]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/search-as-you-type/)。