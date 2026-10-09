---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Did-you-mean
parent: Customizing search results
nav_order: 90
redirect_from:
  - /opensearch/search/did-you-mean/
---

# Did-you-mean

`Did-you-mean` 建議器會為拼錯的搜尋詞顯示建議的修正。

例如，當使用者輸入 `fliud` 時，OpenSearch 會建議類似 `fluid` 的修正搜尋詞。您可以將修正後的詞建議給使用者，甚至自動修正搜尋詞。

您可以使用下列其中一種方法來實作 `did-you-mean` 建議器：

- 使用 [詞彙建議器](#term-suggester) 為單字建議修正。
- 使用 [片語建議器](#phrase-suggester) 為片語建議修正。

## 詞彙建議器

使用詞彙建議器為單字建議修正後的拼法。
詞彙建議器使用[編輯距離](https://en.wikipedia.org/wiki/Edit_distance)來計算建議。 

編輯距離是指讓一個詞彙符合另一個詞彙所需執行的單一字元插入、刪除或取代次數。例如，要將單字「cat」改成「hats」，您需要將「c」取代為「h」並插入一個「s」，因此此例中的編輯距離為 2。

使用詞彙建議器時，您的索引不需要任何特殊的欄位對應。預設情況下，字串欄位類型會被對應為 `text`。`text` 欄位會經過分析，因此下列範例中的 `title` 會被斷詞成個別單字。為下列文件編製索引會建立一個 `books` 索引，其中 `title` 是 `text` 欄位：

```json
PUT books/_doc/1
{
  "title": "Design Patterns (Object-Oriented Software)"
}

PUT books/_doc/2
{
  "title": "Software Architecture Patterns Explained"
}
```

若要檢查字串如何被分割成詞元，您可以使用 `_analyze` 端點。若要套用與該欄位相同的分析器，您可以在 `field` 參數中指定欄位名稱：

```json
GET books/_analyze
{
  "text": "Design Patterns (Object-Oriented Software)",
  "field": "title"
}
```

預設分析器（`standard`）會在單字邊界分割字串、移除標點符號，並將詞元轉為小寫：

```json
{
  "tokens" : [
    {
      "token" : "design",
      "start_offset" : 0,
      "end_offset" : 6,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "patterns",
      "start_offset" : 7,
      "end_offset" : 15,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "object",
      "start_offset" : 17,
      "end_offset" : 23,
      "type" : "<ALPHANUM>",
      "position" : 2
    },
    {
      "token" : "oriented",
      "start_offset" : 24,
      "end_offset" : 32,
      "type" : "<ALPHANUM>",
      "position" : 3
    },
    {
      "token" : "software",
      "start_offset" : 33,
      "end_offset" : 41,
      "type" : "<ALPHANUM>",
      "position" : 4
    }
  ]
}
```

若要取得拼錯搜尋詞的建議，請使用詞彙建議器。在 `text` 欄位中指定需要建議的輸入文字，並在 `field` 欄位中指定要從中取得建議的欄位： 

```json
GET books/_search
{
  "suggest": {
    "spell-check": {
      "text": "patern",
      "term": {
        "field": "title"
      }
    }
  }
}
```

詞彙建議器會在 `options` 陣列中傳回輸入文字的修正清單：

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
    "spell-check" : [
      {
        "text" : "patern",
        "offset" : 0,
        "length" : 6,
        "options" : [
          {
            "text" : "patterns",
            "score" : 0.6666666,
            "freq" : 2
          }
        ]
      }
    ]
  }
}
```

`score` 值是根據編輯距離計算的。分數越高，建議越好。`freq` 是一個頻率，代表該詞彙出現在指定索引文件中的次數。

您可以在一個請求中包含多個建議。下列範例使用詞彙建議器進行兩個不同的建議：

```json
GET books/_search
{
  "suggest": {
    "spell-check1" : {
      "text" : "patern",
      "term" : {
        "field" : "title"
      }
    },
    "spell-check2" : {
      "text" : "desing",
      "term" : {
        "field" : "title"
      }
    }
  }
}
```

若要在多個欄位中取得相同輸入文字的建議，您可以全域定義文字以避免重複：

```json
GET books/_search
{
  "suggest": {
    "text" : "patern",
    "spell-check1" : {
      "term" : {
        "field" : "title"
      }
    },
    "spell-check2" : {
      "term" : {
        "field" : "subject"
      }
    }
  }
}
```

如果 `text` 同時指定於全域層級與個別建議層級，則建議層級的值會覆蓋全域值。

### 詞彙建議器選項

您可以為詞彙建議器指定下列選項。

選項 | 說明
:--- | :---
field | 用來取得建議的欄位。必要。可以為每個建議設定，或全域設定。
`analyzer` | 用來分析輸入文字的分析器。預設為針對 `field` 設定的分析器。
`size` | 針對輸入文字中的每個詞元要傳回的最大建議數。
`sort` | 指定回應中建議的排序方式。有效值為：<br>- `score`：先依相似度分數排序，再依文件頻率，最後依詞彙本身排序。<br>- `frequency`：先依文件頻率排序，再依相似度分數，最後依詞彙本身排序。
`suggest_mode` | 建議模式指定回應中應包含哪些詞彙的建議。有效值為：<br>- `missing`：僅為在索引指定欄位中出現次數為零的輸入詞彙傳回建議。此檢查是欄位特定的：如果詞彙出現在其他欄位但未出現在目標欄位中，仍會被視為遺漏。請注意，此模式不會考慮整個索引中的詞彙頻率---只考慮指定的欄位。 <br>- `popular`：僅在建議在文件中出現的頻率高於原始輸入文字時才傳回建議。<br> - `always`：一律為輸入文字中的每個詞彙傳回建議。<br>預設為 `missing`。
`max_edits` | 建議的最大編輯距離。有效值在 [1, 2] 範圍內。預設為 2。
`prefix_length` | 一個整數，指定開始傳回建議時相符前綴必須達到的最小長度。如果 `prefix_length` 的前綴不相符，但搜尋詞仍在編輯距離內，則不會傳回任何建議。預設為 1。較高的值可改善拼字檢查效能，因為拼錯通常不會發生在單字開頭。
`min_word_length` | 建議必須達到的最小長度，才會包含在回應中。預設為 4。
`shard_size` | 從每個分片取得的最大候選建議數。在考量所有候選建議之後，會傳回前 `shard_size` 個建議。預設等於 `size` 值。分片層級的文件頻率可能不精確，因為詞彙可能位於不同的分片中。如果 `shard_size` 大於 `size`，建議的文件頻率會更準確，但代價是效能降低。 
`max_inspections` | `shard_size` 的乘數。OpenSearch 為尋找建議所檢查的最大候選建議數計算方式為 `shard_size` 乘以 `max_inspection`。可能會提高準確性，但代價是效能降低。預設為 5。
`min_doc_freq` | 建議應出現的文件最小數量或百分比，才會被傳回。透過只傳回具有高分片層級文件頻率的建議，可能會提高準確性。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍內的浮點數。預設為 0（停用此功能）。 
`max_term_freq` | 建議應出現的文件最大數量，才會被傳回。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍內的浮點數。預設為 0.01。排除高頻詞彙可改善拼字檢查效能，因為高頻詞彙通常拼寫正確。使用分片層級的文件頻率。
`string_distance` | 用來判斷相似度的編輯距離演算法。有效值為：<br>- `internal`：預設演算法，基於 [Damerau-Levenshtein 演算法](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)，但針對比較索引中詞彙的編輯距離進行高度最佳化。<br> - `damerau_levenshtein`：基於 [Damerau-Levenshtein 演算法](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance) 的編輯距離演算法。 <br>- `levenshtein`：基於 [Levenshtein 編輯距離演算法](https://en.wikipedia.org/wiki/Levenshtein_distance) 的編輯距離演算法。<br> - `jaro_winkler`：基於 [Jaro-Winkler 演算法](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) 的編輯距離演算法。<br> - `ngram`：基於字元 n-gram 的編輯距離演算法。

## 片語建議器

若要實作 `did-you-mean`，請使用片語建議器。
片語建議器與詞彙建議器類似，差別在於它使用 n-gram 語言模型來建議整個片語，而非個別單字。

若要設定片語建議器，請建立一個名為 `trigram` 的自訂分析器，使用 `shingle` 篩選器並將詞元轉為小寫。此篩選器與 `edge_ngram` 篩選器類似，但套用於單字而非字母。接著，使用您建立的自訂分析器來設定您將從中取得建議的欄位：

```json
PUT books2
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "trigram": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "shingle"
            ]
          }
        },
        "filter": {
          "shingle": {
            "type": "shingle",
            "min_shingle_size": 2,
            "max_shingle_size": 3
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "trigram": {
            "type": "text",
            "analyzer": "trigram"
          }
        }
      }
    }
  }
}
```

將文件編製索引至新索引：

```json
PUT books2/_doc/1
{
  "title": "Design Patterns"
}

PUT books2/_doc/2
{
  "title": "Software Architecture Patterns Explained"
}
```

假設使用者搜尋了錯誤的片語：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram"
      }
    }
  }
}
```

片語建議器會傳回更正後的片語：

```json
{
  "took" : 4,
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
    "phrase-check" : [
      {
        "text" : "design paterns",
        "offset" : 0,
        "length" : 14,
        "options" : [
          {
            "text" : "design patterns",
            "score" : 0.31666178
          }
        ]
      }
    ]
  }
}
```

若要醒目提示建議，請為片語建議器設定 [`highlight`]({{site.url}}{{site.baseurl}}/opensearch/search/highlight/) 欄位：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram",
        "gram_size": 3,
        "highlight": {
          "pre_tag": "<em>",
          "post_tag": "</em>"
        }
      }
    }
  }
}
```

結果會包含醒目提示的文字：

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
    "phrase-check" : [
      {
        "text" : "design paterns",
        "offset" : 0,
        "length" : 14,
        "options" : [
          {
            "text" : "design patterns",
            "highlighted" : "design <em>patterns</em>",
            "score" : 0.31666178
          }
        ]
      }
    ]
  }
}
```

### 片語建議器選項

您可以為片語建議器指定下列選項。

選項 | 說明
:--- | :---
field | 用於 n-gram 查閱的欄位。片語建議器會使用此欄位來計算建議分數。必要。
`gram_size` | 欄位中 n-gram（shingle）的最大大小 `n`。若欄位不包含 n-gram（shingle），請省略此選項或將其設為 1。若欄位使用 shingle 篩選器，且未設定 `gram_size`，則 `gram_size` 會設為 `max_shingle_size`。
`real_word_error_likelihood` | 詞彙拼錯的機率，即使該詞彙存在於字典中亦然。預設為 0.95（字典中有 5% 的詞彙拼錯）。
`confidence` | 信心水準是一個浮點因數，會乘以輸入片語的分數，以計算其他建議的閾值分數。只有分數高於閾值的建議會被傳回。信心水準為 1.0 時，只會傳回分數高於輸入片語的建議。若 `confidence` 設為 0，則會傳回前 `size` 個候選項。預設為 1。
`max_errors` | 為了傳回建議，可容許錯誤（拼錯）的詞彙數量上限或百分比。有效值為代表詞彙數量的整數，或代表詞彙百分比的 (0, 1) 範圍浮點數。預設為 0.5，允許查詢中最多一半的詞彙被視為拼錯。將此值設為高數值可能會降低效能。我們建議將 `max_errors` 設為 1 或 2 等低數值，以減少建議呼叫相對於查詢執行所花費的時間。
`separator` | bigram 欄位中詞彙的分隔符號。預設為空格字元。
`size` | 為每個查詢詞彙產生的候選建議數量。指定較高的值可能會傳回編輯距離較高的詞彙。預設為 5。
`analyzer` | 用來分析建議文字的分析器。預設為針對 `field` 設定的分析器。
`shard_size` | 從每個分片取得候選建議的數量上限。在考量所有候選建議後，會傳回前 `shard_size` 個建議。預設為 5。
[collate](#collate-field)| 用於修剪在索引中沒有相符文件的建議。
`collate.query` | 指定一個查詢，用來檢查建議，以修剪在索引中沒有相符文件的建議。
`collate.prune` | 指定是否傳回所有建議。若 `prune` 設為 `false`，則只會傳回有相符文件的建議。若 `prune` 設為 `true`，則會傳回所有建議；每個建議都會有一個額外的 `collate_match` 欄位，若該建議有相符文件則為 `true`，否則為 `false`。預設為 `false`。
`highlight` | 設定建議醒目提示。`pre_tag` 與 `post_tag` 值皆為必要。 
`highlight.pre_tag` | 醒目提示的起始標籤。 
`highlight.post_tag` | 醒目提示的結束標籤。
[smoothing](#smoothing-models) | 平滑模型，用於平衡索引中經常出現的 shingle 權重與索引中不常出現的 shingle 權重。


### Collate 欄位

若要篩除不會傳回任何結果的拼字檢查建議，您可以使用 `collate` 欄位。此欄位包含一個指令碼化查詢，會針對每個傳回的建議執行。如需建構範本化查詢的相關資訊，請參閱 [搜尋範本]({{site.url}}{{site.baseurl}}/opensearch/search-template/)。您可以使用 `{% raw %}{{suggestion}}{% endraw %}` 變數指定目前的建議，或在 `params` 欄位中傳入您自己的範本參數 (建議值會新增至您指定的變數)。

建議的 collate 查詢只會在取得該建議來源的分片上執行。此查詢為必要。  

此外，若 `prune` 參數設為 `true`，則每個建議都會新增一個 `collate_match` 欄位。若查詢未傳回任何結果，則 `collate_match` 值為 `false`。接著，您可以根據 `collate_match` 欄位篩除建議。`prune` 參數的預設值為 `false`。

例如，下列查詢會設定 `collate` 欄位，以執行將 `title` 欄位與目前建議比對的 `match_phrase` 查詢：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram",
        "collate" : {
          "query" : {
            "source": {
              "match_phrase" : {
                "title": "{{suggestion}}"
              }
            }
          },
          "prune": "true"
        }
      }
    }
  }
}
```

產生的建議會包含設為 `true` 的 `collate_match` 欄位，這表示 `match_phrase` 查詢會為該建議傳回相符的文件：

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
  },
  "suggest" : {
    "phrase-check" : [
      {
        "text" : "design paterns",
        "offset" : 0,
        "length" : 14,
        "options" : [
          {
            "text" : "design patterns",
            "score" : 0.56759655,
            "collate_match" : true
          }
        ]
      }
    ]
  }
}
```


### 平滑模型

在大多數使用案例中，計算建議的分數時，您不僅需要考量 shingle 的頻率，也需要考量 shingle 的大小。平滑模型用於計算不同大小的 shingle 的分數，以平衡高頻與低頻 shingle 的權重。

支援下列平滑模型。

模型 | 說明
:--- | :---
`stupid_backoff` | 如果高階 n-gram 的計數為 0，則退回使用較低階的 n-gram 模型，並將較低階的 n-gram 模型乘以常數因子（`discount`）。這是預設的平滑模型。
`stupid.backoff.discount` | 用於乘上較低階 n-gram 模型的因子。選用。預設為 0.4。
`laplace` | 使用加法平滑，將常數 `alpha` 加到所有計數上，以平衡權重。
`laplace.alpha` | 加到所有計數上以平衡權重的常數，通常為 1.0 或更小。選用。預設為 0.5。

依預設，OpenSearch 使用 Stupid Backoff 模型&mdash;這是一種簡單的演算法，從最高階的 shingle 開始，如果找不到高階 shingle，就採用較低階的 shingle。例如，如果您將片語建議器設定為具有 3-gram、2-gram 和 1-gram，Stupid Backoff 模型會先檢查 3-gram。如果沒有 3-gram，則會檢查 2-gram，但會將分數乘以 `discount` 因子。如果沒有 2-gram，則會檢查 1-gram，但會再次將分數乘以 `discount` 因子。Stupid Backoff 模型在大多數情況下都能有效運作。如果您需要選擇 Laplace 平滑模型，請在 `smoothing` 參數中指定：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram",
        "size" : 1,
        "smoothing" : {
          "laplace" : {
            "alpha" : 0.7
          }
        }
      }
    }
  }
}
```

### 候選產生器

候選產生器會根據輸入文字中的詞彙，提供可能的建議詞彙。目前有一個可用的候選產生器&mdash;`direct_generator`。直接產生器的運作方式與詞彙建議器類似：也會針對輸入文字中的每個詞彙呼叫。片語建議器支援多個候選產生器，每個產生器都會針對輸入文字中的每個詞彙呼叫。它也讓您指定前置篩選器（在輸入文字的詞彙進入拼字檢查階段之前，對其進行分析的分析器）與後置篩選器（在產生的建議傳回之前，對其進行分析的分析器）。

為片語建議器設定直接產生器：

```json
GET books2/_search
{
  "suggest": {
    "text": "design paterns",
    "phrase-check": {
      "phrase": {
        "field": "title.trigram",
        "size": 1,
        "direct_generator": [
          {
            "field": "title.trigram",
            "suggest_mode": "always",
            "min_word_length": 3
          }
        ]
      }
    }
  }
}
```

您可以指定下列直接產生器選項。

選項 | 說明
:--- | :---
field | 提供建議來源的欄位。必要。可針對每個建議設定，或全域設定。
`size` | 針對輸入文字中的每個詞元傳回的建議數量上限。
`suggest_mode` | 建議模式指定應納入各分片所產生建議的詞彙。建議模式會套用至每個分片的建議，而在合併來自不同分片的建議時，不會進行檢查。因此，如果建議模式為 `missing`，當詞彙在某個分片中不存在，但在另一個分片中存在時，仍會傳回建議。有效值為：<br>- `missing`：僅針對分片中不存在的輸入文字詞彙傳回建議。<br>- `popular`：僅在建議詞彙於分片文件中的出現頻率高於原始輸入文字詞彙時，傳回建議。<br>- `always`：一律傳回建議。<br>預設為 `missing`。
`max_edits` | 建議的編輯距離上限。有效值的範圍為 [1, 2]。預設為 2。
`prefix_length` | 指定開始傳回建議所需的相符前綴長度下限的整數。如果 `prefix_length` 的前綴不相符，即使搜尋詞彙仍在編輯距離範圍內，也不會傳回建議。預設為 1。較高的值可提升拼字檢查效能，因為拼字錯誤通常不會出現在單字的開頭。
`min_word_length` | 建議必須達到才能納入的長度下限。預設為 4。
`max_inspections` | `shard_size` 的乘數因子。OpenSearch 為尋找建議而檢查的候選建議數量上限，計算方式為 `shard_size` 乘以 `max_inspection`。可能提高準確度，但會降低效能。預設為 5。
`min_doc_freq` | 建議必須出現於多少文件或多少百分比的文件中，才會傳回的下限。透過僅傳回分片層級文件頻率較高的建議，可能提高準確度。有效值為代表文件頻率的整數，或範圍為 [0, 1]、代表文件百分比的浮點數。預設為 0（功能停用）。 
`max_term_freq` | 建議可出現於多少文件中，仍會傳回的數量上限。有效值為代表文件頻率的整數，或範圍為 [0, 1]、代表文件百分比的浮點數。預設為 0.01。排除高頻詞彙可提升拼字檢查效能，因為高頻詞彙通常拼字正確。使用分片層級的文件頻率。
`pre_filter` | 在產生建議之前，套用至傳入產生器的每個輸入文字詞元的分析器。 
`post_filter` | 在每個產生的建議傳入片語評分器之前，套用至該建議的分析器。 
