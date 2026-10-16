---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "您是不是要找"
parent: Customizing search results
nav_order: 90
redirect_from:
  - /opensearch/search/did-you-mean/
---

# 您是不是要找

拼字修正建議會顯示拼錯的搜尋詞彙的修正建議。

例如，當使用者輸入 `fliud` 時，OpenSearch 會建議修正後的搜尋詞彙，例如 `fluid`。您可以將修正後的詞彙建議給使用者，甚至自動修正搜尋詞彙。

您可以使用下列其中一種建議器來實作拼字修正建議：

- 使用[詞彙建議器](#term-suggester)為單一字詞建議修正。
- 使用[片語建議器](#phrase-suggester)為片語建議修正。

## 詞彙建議器

使用詞彙建議器為個別單字建議修正後的拼寫。詞彙建議器會將輸入文字分析成詞元，並為每個詞元分別傳回建議。它只使用建議設定：同一個搜尋請求中的 `query` 不會影響建議結果。

詞彙建議器使用[_編輯距離_](https://en.wikipedia.org/wiki/Edit_distance)來計算建議。編輯距離是指讓一個詞彙與另一個詞彙相符所需的單字元插入、刪除或替換次數。例如，要將單字 "cat" 改成 "hats"，您需要將 "c" 替換為 "h" 並插入一個 "s"，因此此例中的編輯距離為 2。

使用詞彙建議器時，您的索引不需要任何特殊的欄位對應。預設情況下，字串欄位類型會對應為 `text`。`text` 欄位會被分析，因此下列範例中的 `title` 會被斷詞成個別單字。為下列文件編製索引會建立一個 `books` 索引，其中 `title` 是 `text` 欄位：

```json
PUT books/_doc/1
{
  "title": "Design Patterns (Object-Oriented Software)"
}
```
{% include copy-curl.html %}

```json
PUT books/_doc/2
{
  "title": "Software Architecture Patterns Explained"
}
```
{% include copy-curl.html %}

若要檢查字串如何被分割成詞元，您可以使用 `_analyze` 端點。若要套用與該欄位相同的分析器，您可以在 `field` 參數中指定欄位名稱：

```json
GET books/_analyze
{
  "text": "Design Patterns (Object-Oriented Software)",
  "field": "title"
}
```
{% include copy-curl.html %}

預設分析器 (`standard`) 會在單字邊界分割字串、移除標點符號，並將詞元轉為小寫：

```json
{
  "tokens": [
    {
      "token": "design",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "patterns",
      "start_offset": 7,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "object",
      "start_offset": 17,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "oriented",
      "start_offset": 24,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "software",
      "start_offset": 33,
      "end_offset": 41,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```

若要取得拼寫錯誤的搜尋詞彙的建議，請使用詞彙建議器。在 `text` 欄位中指定需要建議的輸入文字，並在 `field` 欄位中指定取得建議的來源欄位：

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
{% include copy-curl.html %}

詞彙建議器會在 `options` 陣列中傳回輸入文字的修正清單：

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
  },
  "suggest": {
    "spell-check": [
      {
        "text": "patern",
        "offset": 0,
        "length": 6,
        "options": [
          {
            "text": "patterns",
            "score": 0.6666666,
            "freq": 2
          }
        ]
      }
    ]
  }
}
```

`score` 值是根據編輯距離計算的。分數越高，建議越好。`freq` 是頻率，代表該詞彙在指定索引的文件中出現的次數。

您可以在一個請求中包含多個建議。下列範例使用詞彙建議器進行兩個不同的建議：

```json
GET books/_search
{
  "suggest": {
    "spell-check1": {
      "text": "patern",
      "term": {
        "field": "title"
      }
    },
    "spell-check2": {
      "text": "desing",
      "term": {
        "field": "title"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要對相同的輸入文字執行多個建議器，請全域定義文字以避免重複。下列範例以兩種不同的排序方式傳回 `patern` 的建議：

```json
GET books/_search
{
  "suggest": {
    "text": "patern",
    "by-score": {
      "term": {
        "field": "title",
        "sort": "score"
      }
    },
    "by-frequency": {
      "term": {
        "field": "title",
        "sort": "frequency"
      }
    }
  }
}
```
{% include copy-curl.html %}


### 詞彙建議器選項

您可以為詞彙建議器指定下列選項。

選項 | 說明
:--- | :---
`field` | 用來提供建議來源的欄位。必要。
`text` | 要為其傳回建議的輸入文字。必要。可以針對每個建議設定，或對請求中的所有建議全域設定。若兩個層級都有指定，則使用建議層級的值。
`analyzer` | 用來分析輸入文字的分析器。預設為針對 `field` 設定的分析器。
`size` | 針對輸入文字中的每個詞元要傳回的建議數量上限。
`sort` | 指定建議在回應中的排序方式。有效值為：<br>- `score`：先依相似度分數排序，再依文件頻率排序，最後依詞彙本身排序。<br>- `frequency`：先依文件頻率排序，再依相似度分數排序，最後依詞彙本身排序。
`suggest_mode` | 建議模式會指定回應中應包含哪些詞彙的建議。有效值為：<br>- `missing`：僅針對在索引指定欄位中出現次數為零的輸入詞彙傳回建議。此檢查是欄位特定的：如果某個詞彙出現在其他欄位但未出現在目標欄位中，仍視為遺漏。請注意，此模式不會考慮整個索引中的詞彙頻率——只考慮指定的欄位。 <br>- `popular`：僅當建議在文件中出現的頻率高於原始輸入文字時才傳回。<br> - `always`：一律為輸入文字中的每個詞彙傳回建議。<br>預設為 `missing`。
`max_edits` | 建議的最大編輯距離。有效值在 [1, 2] 範圍內。預設為 2。
`prefix_length` | 一個整數，指定開始傳回建議時，相符前綴必須達到的最小長度。如果 `prefix_length` 的前綴不相符，但搜尋詞彙仍在編輯距離內，則不會傳回任何建議。預設為 1。較高的值可改善拼字檢查效能，因為拼字錯誤通常不會發生在單字開頭。
`min_word_length` | 要為其傳回建議的輸入詞彙最小長度。較短的輸入詞彙不會收到建議。預設為 4。
`shard_size` | 要從每個分片取得的候選建議數量上限。所有分片中排名前 `size` 的建議會在回應中傳回。預設等於 `size` 值。分片層級的文件頻率可能不精確，因為詞彙可能位於不同的分片中。如果 `shard_size` 大於 `size`，建議的文件頻率會更準確，但代價是效能降低。 
`max_inspections` | `shard_size` 的乘數。OpenSearch 為尋找建議而檢查的候選建議數量上限，計算方式為 `shard_size` 乘以 `max_inspections`。可能以效能降低為代價來提高準確性。預設為 5。
`min_doc_freq` | 建議必須出現的最小文件數量或百分比，才會被傳回。可透過只傳回具有高分片層級文件頻率的建議來提高準確性。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍內的浮點數。預設為 0（停用此功能）。 
`max_term_freq` | 建議可出現的最大文件數量，才會被傳回。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍內的浮點數。預設為 0.01。排除高頻詞彙可改善拼字檢查效能，因為高頻詞彙通常拼字正確。使用分片層級的文件頻率。
`string_distance` | 用來判斷相似度的編輯距離演算法。有效值為：<br>- `internal`：預設演算法，以 [Damerau-Levenshtein 演算法](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)為基礎，但針對比較索引中詞彙的編輯距離進行高度最佳化。<br> - `damerau_levenshtein`：以 [Damerau-Levenshtein 演算法](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)為基礎的編輯距離演算法。 <br>- `levenshtein`：以 [Levenshtein 編輯距離演算法](https://en.wikipedia.org/wiki/Levenshtein_distance)為基礎的編輯距離演算法。<br> - `jaro_winkler`：以 [Jaro-Winkler 演算法](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)為基礎的編輯距離演算法。<br> - `ngram`：以字元 n-gram 為基礎的編輯距離演算法。

### 使用查詢參數請求詞彙建議

您也可以使用查詢參數來請求詞彙建議，取代請求本文中的 `suggest` 物件。在 `suggest_field` 中指定欄位，在 `suggest_text` 中指定輸入文字，並在 `suggest_mode` 中指定建議模式。使用這種形式時，`suggest_mode` 沒有預設值，因此您必須指定此值。如果您省略 `suggest_text`，OpenSearch 會使用 `q` 參數的值。如需完整的參數清單，請參閱 [Search API 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters)。

下列請求會從 `books` 索引的 `title` 欄位傳回拼字錯誤詞彙 `patern` 的建議：

```json
GET /books/_search?suggest_field=title&suggest_text=patern&suggest_mode=missing&size=0
```
{% include copy-curl.html %}

回應會在以欄位命名的 `suggest` 物件中包含建議：

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
  },
  "suggest": {
    "title": [
      {
        "text": "patern",
        "offset": 0,
        "length": 6,
        "options": [
          {
            "text": "patterns",
            "score": 0.6666666,
            "freq": 2
          }
        ]
      }
    ]
  }
}
```

## 片語建議器

片語建議器與詞彙建議器類似，不同之處在於它使用 n-gram 語言模型來建議完整的片語，而非個別的字詞。

若要設定片語建議器，請建立一個名為 `trigram` 的自訂分析器，該分析器使用 `shingle` 篩選器並將詞元轉換為小寫。此篩選器與 `edge_ngram` 篩選器類似，但它作用於字詞而非字母。接著，使用您建立的自訂分析器設定您要從中取得建議的欄位：

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
            "filter": ["lowercase", "shingle"]
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
{% include copy-curl.html %}

將文件編製索引至新索引：

```json
PUT books2/_doc/1
{
  "title": "Design Patterns"
}
```
{% include copy-curl.html %}

```json
PUT books2/_doc/2
{
  "title": "Software Architecture Patterns Explained"
}
```
{% include copy-curl.html %}

假設使用者搜尋了一個不正確的片語：

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
{% include copy-curl.html %}

片語建議器會傳回修正後的片語：

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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "suggest": {
    "phrase-check": [
      {
        "text": "design paterns",
        "offset": 0,
        "length": 14,
        "options": [
          {
            "text": "design patterns",
            "score": 0.31666178
          }
        ]
      }
    ]
  }
}
```

若要醒目提示建議，請為片語建議器設定 [`highlight`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/) 欄位：

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
{% include copy-curl.html %}

結果包含醒目提示的文字：

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
  },
  "suggest": {
    "phrase-check": [
      {
        "text": "design paterns",
        "offset": 0,
        "length": 14,
        "options": [
          {
            "text": "design patterns",
            "highlighted": "design <em>patterns</em>",
            "score": 0.31666178
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
`field` | 用於 n-gram 查詢的欄位。片語建議器會使用此欄位來計算建議分數。必要。
`text` | 要為其傳回建議的輸入文字。必要。可以為每個建議個別設定，或為請求中的所有建議全域設定。若兩個層級都有指定，則使用建議層級的值。
`gram_size` | 欄位中 n-gram（shingle）的大小上限 `n`。若欄位不含 n-gram（shingle），請省略此選項或將其設為 1。若欄位使用 shingle 篩選器，且未設定 `gram_size`，則 `gram_size` 會被設為 `max_shingle_size`。
`real_word_error_likelihood` | 詞彙拼錯的機率，即使該詞彙存在於字典中。預設為 0.95（字典中有 5% 的字詞是拼錯的）。
`confidence` | 信賴度是一個浮點數係數，會乘以輸入片語的分數，以計算其他建議的門檻分數。只會傳回分數高於門檻的建議。信賴度為 1.0 時，只會傳回分數高於輸入片語的建議。若 `confidence` 設為 0，則會傳回前 `size` 個候選項。預設為 1。
`max_errors` | 為了傳回建議，詞彙可出錯（拼錯）的最大數量或百分比。有效值為代表詞彙數量的整數，或代表詞彙百分比的 (0, 1) 範圍內的浮點數。預設為 0.5，表示查詢中最多一半的詞彙可被視為拼錯。將此值設得太高可能會降低效能。建議將 `max_errors` 設為較低的數字，例如 1 或 2，以減少建議呼叫相對於查詢執行所花費的時間。
`separator` | bigram 欄位中詞元的分隔符。預設為空格字元。
`size` | 為每個查詢詞元產生的候選建議數量。指定較高的值可能會傳回編輯距離較大的詞元。預設為 5。
`analyzer` | 用來分析建議文字的分析器。預設為針對 `field` 設定的分析器。
`shard_size` | 從每個分片取得的候選建議數量上限。回應中會傳回所有分片中排名前 `size` 的建議。預設為 5。
[`collate`](#collate-field) | 用於修剪索引中沒有符合文件之建議。
`collate.query` | 指定一個查詢，用來檢查建議，以修剪索引中沒有符合文件之建議。
`collate.prune` | 指定是否傳回所有建議。若 `prune` 設為 `false`，只會傳回有符合文件的建議。若 `prune` 設為 `true`，則會傳回所有建議；每個建議都會有一個額外的 `collate_match` 欄位，若該建議有符合文件則為 `true`，否則為 `false`。預設為 `false`。
`highlight` | 設定建議的醒目提示。`pre_tag` 與 `post_tag` 的值皆為必要。標籤會放置在每個被更改的詞元周圍。若連續多個詞元被更改，標籤會放置在整個群組周圍，例如 `<em>design patterns</em>`。
`highlight.pre_tag` | 醒目提示的起始標籤。
`highlight.post_tag` | 醒目提示的結束標籤。
[`smoothing`](#smoothing-models) | 平滑模型，用來平衡索引中經常出現的 shingle 與索引中不常出現的 shingle 的權重。


### Collate 欄位

若要篩除不會傳回任何結果的拼字檢查建議，您可以使用 `collate` 欄位。此欄位包含一段指令碼查詢，會針對每個傳回的建議執行。關於建構範本化查詢的資訊，請參閱[搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/)。您可以使用 `{% raw %}{{suggestion}}{% endraw %}` 變數指定目前的建議，或在 `params` 欄位中傳入您自己的範本參數（建議值會加入您指定的變數中）。

建議的 collate 查詢只會在提供該建議的來源分片上執行。此查詢為必要。

此外，如果 `prune` 參數設為 `true`，則每個建議都會新增一個 `collate_match` 欄位。如果查詢未傳回任何結果，`collate_match` 值會是 `false`。您接著可以根據 `collate_match` 欄位篩除建議。`prune` 參數的預設值為 `false`。

例如，下列查詢會設定 `collate` 欄位，以執行將 `title` 欄位與目前建議比對的 `match_phrase` 查詢：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram",
        "collate": {
          "query": {
            "source": {
              "match_phrase": {
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
{% include copy-curl.html %}

產生的建議會包含設為 `true` 的 `collate_match` 欄位，這表示 `match_phrase` 查詢會為該建議傳回相符的文件：

```json
{
  "took": 7,
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
  },
  "suggest": {
    "phrase-check": [
      {
        "text": "design paterns",
        "offset": 0,
        "length": 14,
        "options": [
          {
            "text": "design patterns",
            "score": 0.56759655,
            "collate_match": true
          }
        ]
      }
    ]
  }
}
```


### 平滑模型

在大多數使用情境中，計算建議的分數時，您不僅要考慮 shingle 的出現頻率，還要考慮 shingle 的大小。平滑模型用於計算不同大小 shingle 的分數，平衡高頻與低頻 shingle 的權重。

支援下列平滑模型。

模型 | 說明
:--- | :---
`stupid_backoff` | 當較高階 n-gram 的計數為 0 時，退回較低階的 n-gram 模型，並將較低階的 n-gram 模型乘上一個常數因子（`discount`）。這是預設的平滑模型。
`stupid_backoff.discount` | 用來乘以較低階 n-gram 模型的因子。選用。預設為 0.4。
`laplace` | 使用加法平滑，對所有計數加上常數 `alpha` 以平衡權重。
`laplace.alpha` | 加到所有計數以平衡權重的常數，通常為 1.0 或更小。選用。預設為 0.5。
`linear` | 將分數計算為 trigram、bigram 與 unigram 分數的加權平均。請在 `trigram_lambda`、`bigram_lambda` 與 `unigram_lambda` 中指定權重。權重總和必須為 1。省略的權重會設為 0。
`linear.trigram_lambda` | trigram 的權重。
`linear.bigram_lambda` | bigram 的權重。
`linear.unigram_lambda` | unigram 的權重。

預設情況下，OpenSearch 使用 Stupid Backoff 模型——這是一種簡單的演算法，從最高階的 shingle 開始，若找不到較高階的 shingle，就改用較低階的 shingle。例如，如果您將片語建議器設定為包含 3-gram、2-gram 與 1-gram，Stupid Backoff 模型會先檢查 3-gram。如果沒有 3-gram，它會檢查 2-gram，但會將分數乘以 `discount` 因子。如果沒有 2-gram，它會檢查 1-gram，並再次將分數乘以 `discount` 因子。Stupid Backoff 模型在大多數情況下運作良好。如果您需要選用 Laplace 平滑模型，請在 `smoothing` 參數中指定：

```json
GET books2/_search
{
  "suggest": {
    "phrase-check": {
      "text": "design paterns",
      "phrase": {
        "field": "title.trigram",
        "size": 1,
        "smoothing": {
          "laplace": {
            "alpha": 0.7
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 候選產生器

候選產生器會根據輸入文字中的詞彙提供可能的建議詞彙。目前有一個可用的候選產生器&mdash;`direct_generator`。直接產生器的運作方式與詞彙建議器類似：它也會針對輸入文字中的每個詞彙被呼叫。詞組建議器支援多個候選產生器，其中每個產生器都會針對輸入文字中的每個詞彙被呼叫。它也可讓您指定前置篩選器（在輸入文字詞彙進入拼字檢查階段之前對其進行分析的分析器）與後置篩選器（在產生的建議傳回之前對其進行分析的分析器）。

為詞組建議器設定直接產生器：

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
{% include copy-curl.html %}

直接產生器需要固定的前置字元：根據預設，詞彙的第一個字元必須拼寫正確，產生器才會建議更正（`prefix_length` 為 `1`）。若也要更正單字開頭的拼字錯誤，請新增第二個產生器，使用以 `reverse` 詞元篩選器編製索引的欄位。`pre_filter` 會在產生器搜尋候選詞彙之前反轉每個輸入詞彙的字元，因此產生器會從詞彙的最後一個字元開始比較。接著 `post_filter` 會還原每個候選詞彙的原始字元順序。

建立一個 `books3` 索引，其中包含供詞組建議器使用的 `title.trigram` 子欄位，以及一個以 `reverse` 分析器編製索引的 `title.reverse` 子欄位：

```json
PUT books3
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "trigram": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "shingle"]
          },
          "reverse": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "reverse"]
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
          },
          "reverse": {
            "type": "text",
            "analyzer": "reverse"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引至新索引：

```json
PUT books3/_doc/1
{
  "title": "Design Patterns"
}
```
{% include copy-curl.html %}

```json
PUT books3/_doc/2?refresh=true
{
  "title": "Software Architecture Patterns Explained"
}
```
{% include copy-curl.html %}

下列請求包含拼字錯誤的 `esign`，它缺少了第一個字母。在 `title.trigram` 上的單一產生器不會為此文字傳回任何建議。第二個產生器則透過搜尋反轉後的詞彙找到 `design`：

```json
GET books3/_search
{
  "suggest": {
    "text": "esign patterns",
    "phrase-check": {
      "phrase": {
        "field": "title.trigram",
        "size": 1,
        "direct_generator": [
          {
            "field": "title.trigram",
            "suggest_mode": "always"
          },
          {
            "field": "title.reverse",
            "suggest_mode": "always",
            "pre_filter": "reverse",
            "post_filter": "reverse"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含更正後的詞組：

```json
{
  ...
  "suggest": {
    "phrase-check": [
      {
        "text": "esign patterns",
        "offset": 0,
        "length": 14,
        "options": [
          {
            "text": "design patterns",
            "score": 0.33112788
          }
        ]
      }
    ]
  }
}
```

您可以在 `direct_generator` 物件中指定下列欄位。

欄位 | 說明
:--- | :---
`field` | 從中取得建議的欄位。必要。
`size` | 針對輸入文字中的每個詞元要傳回的建議數量上限。
`suggest_mode` | 建議模式會指定應納入各分片所產生建議的詞彙。建議模式會套用至各分片的建議，且在合併來自不同分片的建議時不會進行檢查。因此，若建議模式為 `missing`，只要該詞彙在某個分片中不存在但在另一個分片中存在，就會傳回建議。有效值為：<br>- `missing`：僅針對分片中不存在的輸入文字詞彙傳回建議。<br>- `popular`：僅在建議於文件中出現的頻率高於分片上原始輸入文字時才傳回建議。<br>- `always`：一律傳回建議。<br>預設為 `missing`。
`max_edits` | 建議的最大編輯距離。有效值介於 [1, 2] 範圍內。預設為 2。
`prefix_length` | 整數，指定必須符合的前置字元長度下限，才會開始傳回建議。若 `prefix_length` 的前置字元不符合，但搜尋詞彙仍在編輯距離內，則不會傳回任何建議。預設為 1。較高的值可提升拼字檢查效能，因為拼字錯誤通常不會發生在單字開頭。
`min_word_length` | 產生候選詞彙的輸入詞彙長度下限。預設為 4。
`max_inspections` | `shard_size` 的乘數。OpenSearch 為尋找建議而檢查的候選建議數量上限，計算方式為 `shard_size` 乘以 `max_inspections`。可能以效能降低為代價來提升準確度。預設為 5。
`min_doc_freq` | 建議必須出現的文件數量或百分比下限，才會被傳回。可能透過僅傳回具有高分片層級文件頻率的建議來提升準確度。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍浮點數。預設為 0（功能已停用）。 
`max_term_freq` | 建議必須出現的文件數量上限，才會被傳回。有效值為代表文件頻率的整數，或代表文件百分比的 [0, 1] 範圍浮點數。預設為 0.01。排除高頻詞彙可提升拼字檢查效能，因為高頻詞彙通常拼寫正確。使用分片層級文件頻率。
`pre_filter` | 在產生建議之前，套用至傳遞給產生器之每個輸入文字詞元的分析器。 
`post_filter` | 在產生的建議傳遞給詞組評分器之前，套用至每個產生建議的分析器。 

## 在回應中包含建議器類型

依預設，回應中的每項建議僅以您在請求中為建議器指定的名稱來識別。如果您的應用程式需要知道結果是由哪種類型的建議器產生，例如要選擇如何剖析結果，請在請求中加入 `typed_keys` 查詢參數。OpenSearch 接著會在每個建議名稱前加上建議器類型和 `#` 分隔符號。

下列請求會對相同的輸入文字執行詞彙建議器和片語建議器，並在回應中包含建議器類型：

```json
GET /books/_search?typed_keys=true
{
  "suggest": {
    "text": "desing paterns",
    "title-terms": {
      "term": {
        "field": "title"
      }
    },
    "title-phrase": {
      "phrase": {
        "field": "title"
      }
    }
  }
}
```
{% include copy-curl.html %}

在回應中，建議的名稱為 `term#title-terms` 和 `phrase#title-phrase`：

```json
{
  ...
  "suggest": {
    "phrase#title-phrase": [
      {
        "text": "desing paterns",
        "offset": 0,
        "length": 14,
        "options": [
          {
            "text": "desing patterns",
            "score": 0.13261011
          },
          {
            "text": "design paterns",
            "score": 0.109846905
          }
        ]
      }
    ],
    "term#title-terms": [
      {
        "text": "desing",
        "offset": 0,
        "length": 6,
        "options": [
          {
            "text": "design",
            "score": 0.8333333,
            "freq": 1
          }
        ]
      },
      {
        "text": "paterns",
        "offset": 7,
        "length": 7,
        "options": [
          {
            "text": "patterns",
            "score": 0.85714287,
            "freq": 2
          }
        ]
      }
    ]
  }
}
```

`typed_keys` 參數也會在回應中的彙總名稱前加上類型前綴。
