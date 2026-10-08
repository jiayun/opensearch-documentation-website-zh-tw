---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Match
parent: Full-text queries
nav_order: 10
---

# Match 查詢

使用 `match` 查詢對特定文件欄位執行全文搜尋。若您對 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位執行 `match` 查詢，`match` 查詢會[分析]({{site.url}}{{site.baseurl}}/analyzers/index/)所提供的搜尋字串，並傳回符合該字串中任一詞彙的文件。若您對精確值欄位執行 `match` 查詢，則會傳回與該精確值相符的文件。搜尋精確值欄位的建議做法是使用篩選器，因為與查詢不同，篩選器會被快取。

以下範例顯示在 `title` 中搜尋單字 `wind` 的基本 `match` 查詢：

```json
GET _search
{
  "query": {
    "match": {
      "title": "wind"
    }
  }
}
```
{% include copy-curl.html %}

若要傳遞其他參數，您可以使用展開語法：

```json
GET _search
{
  "query": {
    "match": {
      "title": {
        "query": "wind",
        "analyzer": "stop"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例

在以下範例中，您將使用包含下列文件的索引：

```json
PUT testindex/_doc/1
{
  "title": "Let the wind rise"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "title": "Gone with the wind"
  
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/3
{
  "title": "Rise is gone"
}
```
{% include copy-curl.html %}

## 運算子

若對 `text` 欄位執行 `match` 查詢，文字會以 `analyzer` 參數中指定的分析器進行分析。接著，產生的詞元會使用 `operator` 參數中指定的運算子組合成布林查詢。預設運算子為 `OR`，因此查詢 `wind rise` 會轉換為 `wind OR rise`。在此範例中，此查詢會傳回文件 1--3，因為每份文件都有與查詢相符的詞彙。若要指定 `and` 運算子，請使用以下查詢：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "wind rise",
        "operator": "and"
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會建構為 `wind AND rise`，並傳回文件 1 作為相符的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 17,
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
    "max_score": 1.2667098,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 1.2667098,
        "_source": {
          "title": "Let the wind rise"
        }
      }
    ]
  }
}
```

</details>

### 最少應符合數

您可以指定 [`minimum_should_match`]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/) 參數，以控制文件必須符合的最少詞彙數量，才會在結果中傳回：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "wind rise",
        "operator": "or",
        "minimum_should_match": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

現在文件必須同時符合兩個詞彙，因此只會傳回文件 1（這等同於 `and` 運算子）：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 23,
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
    "max_score": 1.2667098,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 1.2667098,
        "_source": {
          "title": "Let the wind rise"
        }
      }
    ]
  }
}
```
</details>

## 分析器

由於在此範例中您並未明確指定分析器，因此會使用預設的 `standard` 分析器。預設分析器不會執行詞幹提取，因此若您執行查詢 `the wind rises`，將不會收到任何結果，因為詞元 `rises` 與詞元 `rise` 不相符。若要變更搜尋分析器，請在 `analyzer` 欄位中指定。例如，以下查詢使用 `english` 分析器：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "the wind rises",
        "operator": "and",
        "analyzer": "english"
      }
    }
  }
}
```
{% include copy-curl.html %}

`english` 分析器會移除停用詞 `the` 並執行詞幹提取，產生詞元 `wind` 和 `rise`。後者與文件 1 相符，因此該文件會在結果中傳回：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 19,
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
    "max_score": 1.2667098,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 1.2667098,
        "_source": {
          "title": "Let the wind rise"
        }
      }
    ]
  }
}
```
</details>

## 空查詢

在某些情況下，分析器可能會移除查詢中的所有詞元。例如，`english` 分析器會移除停用詞，因此在查詢 `and OR or` 中，所有詞元都會被移除。若要檢查分析器的行為，您可以使用 [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/#apply-a-built-in-analyzer)：

```json
GET testindex/_analyze
{
  "analyzer" : "english",
  "text" : "and OR or"
}
```
{% include copy-curl.html %}

如預期，此查詢不會產生任何詞元：

```json
{
  "tokens": []
}
```

您可以在 `zero_terms_query` 參數中指定空查詢的行為。將 `zero_terms_query` 設定為 `all` 會傳回索引中的所有文件，設定為 `none` 則不會傳回任何文件：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "and OR or",
        "analyzer" : "english",
        "zero_terms_query": "all"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 模糊比對

為了因應拼寫錯誤，您可以為查詢指定 `fuzziness`，其值可為下列任一項：

- 一個整數，指定此編輯所允許的最大 [Damerau–Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance)。 
- `AUTO`： 
  - 0–2 個字元的字串必須完全相符。
  - 3–5 個字元的字串允許 1 次編輯。
  - 超過 5 個字元的字串允許 2 次編輯。

在大多數情況下，將 `fuzziness` 設定為 `AUTO` 值的效果最佳：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "wnid",
        "fuzziness": "AUTO"
      }
    }
  }
}
```
{% include copy-curl.html %}

詞元 `wnid` 與 `wind` 相符，且此查詢會傳回文件 1 和 2：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 31,
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
    "max_score": 0.47501624,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.47501624,
        "_source": {
          "title": "Let the wind rise"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.47501624,
        "_source": {
          "title": "Gone with the wind"
        }
      }
    ]
  }
}
```
</details>

### 前綴長度

拼字錯誤很少出現在單字的開頭。因此，您可以指定相符前綴必須達到的最小長度，文件才會在結果中傳回。例如，您可以將前述查詢變更為包含 `prefix_length`：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "wnid",
        "fuzziness": "AUTO",
        "prefix_length": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

前述查詢不會傳回任何結果。如果您將 `prefix_length` 變更為 1，則會傳回文件 1 和 2，因為詞元 `wnid` 的第一個字母沒有拼錯。

### 換位

在前述範例中，單字 `wnid` 包含一個換位（`in` 被改為 `ni`）。預設情況下，模糊比對允許換位，但您可以將 `fuzzy_transpositions` 設為 `false` 來禁止換位：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "title": {
        "query": "wnid",
        "fuzziness": "AUTO",
        "fuzzy_transpositions": false
      }
    }
  }
}
```
{% include copy-curl.html %}

現在查詢不會傳回任何結果。

## 同義詞

如果您使用 `synonym_graph` 篩選器，且 `auto_generate_synonyms_phrase_query` 設為 `true`（預設），OpenSearch 會將查詢剖析為詞彙，然後組合這些詞彙，為多詞彙同義詞產生[片語查詢](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html)。例如，如果您將 `ba,batting average` 指定為同義詞並搜尋 `ba`，OpenSearch 會搜尋 `ba OR "batting average"`。

若要以連接詞比對多詞彙同義詞，請將 `auto_generate_synonyms_phrase_query` 設為 `false`：

```json
GET /testindex/_search
{
  "query": {
    "match": {
      "text": {
        "query": "good ba",
        "auto_generate_synonyms_phrase_query": false
      }
    }
  }
}
```
{% include copy-curl.html %}

產生的查詢為 `ba OR (batting AND average)`。

## 參數

此查詢接受欄位名稱（`<field>`）作為最上層參數：

```json
GET _search
{
  "query": {
    "match": {
      "<field>": {
        "query": "text to search for",
        ... 
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `query` 之外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的查詢字串。必要。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否為多詞彙同義詞自動建立[比對片語查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。例如，如果您將 `ba,batting average` 指定為同義詞並搜尋 `ba`，OpenSearch 會搜尋 `ba OR "batting average"`（若此選項為 `true`）或 `ba OR (batting AND average)`（若此選項為 `false`）。預設為 `true`。
`analyzer` | 字串 | 用於將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `default_field` 指定的索引時間分析器。如果未針對 `default_field` 指定分析器，則 `analyzer` 為該索引的預設分析器。如需有關 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`boost` | 浮點數 | 依指定的倍數提升子句權重。適用於在複合查詢中為子句加權。介於 [0, 1) 範圍內的值會降低相關性，大於 1 的值會提高相關性。預設為 `1`。
`enable_position_increments` | 布林值 | 為 `true` 時，產生的查詢會考量位置增量。當移除停用詞在詞彙之間留下不必要的「間隙」時，此設定很有用。預設為 `true`。
`fuzziness` | 字串 | 在判斷詞彙是否與某個值相符時，將一個單字變更為另一個單字所需的字元編輯次數（插入、刪除、替換或換位）。例如，`wined` 與 `wind` 之間的距離為 1。有效值為非負整數或 `AUTO`。預設值 `AUTO` 會根據搜尋詞彙的長度動態選取編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂閾值，其中 `low` 與 `high` 定義字元長度的邊界。若省略，OpenSearch 會使用 `AUTO:3,6` 作為預設值，並套用下列規則：<br>- 包含 0--2 個字元的詞彙：需要完全相符（0 次編輯）。<br>- 包含 3--5 個字元的詞彙：最多允許 1 次編輯。<br>- 包含 6 個以上字元的詞彙：最多允許 2 次編輯。<br>例如，`AUTO:4,7` 對包含 0--3 個字元的詞彙要求完全相符，對包含 4--6 個字元的詞彙最多允許 1 次編輯，對包含 7 個以上字元的詞彙最多允許 2 次編輯。在大多數情境下，建議使用 `AUTO`。
`fuzzy_rewrite` | 字串 | 決定 OpenSearch 如何重寫查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。如果 `fuzziness` 參數不是 `0`，查詢預設會使用 `top_terms_blended_freqs_${max_expansions}` 的 `fuzzy_rewrite` 方法。預設為 `constant_score`。 
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true`（預設）會在 `fuzziness` 選項的插入、刪除和替換操作之外，加入相鄰字元互換。例如，若 `fuzzy_transpositions` 為 true（互換「n」和「i」），`wind` 與 `wnid` 之間的距離為 1；若為 false（刪除「n」、插入「n」），則距離為 2。如果 `fuzzy_transpositions` 為 false，則 `rewind` 和 `wnid` 與 `wind` 的距離相同（2），儘管從人類的角度來看，`wnid` 顯然是打字錯誤。預設值適合大多數使用案例。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，查詢字串 `"8.2"` 可以比對類型為 `float` 的欄位。預設為 `false`。
`max_expansions` | 正整數 |  查詢可擴展的最大詞彙數量。模糊查詢會「擴展到」`fuzziness` 所指定距離內的多個相符詞彙，然後 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`minimum_should_match` | 正或負整數、正或負百分比、組合 | 如果查詢字串包含多個搜尋詞彙且您使用 `or` 運算子，此參數為文件被視為相符所需相符的詞彙數量。例如，如果 `minimum_should_match` 為 2，`wind often rising` 不會與 `The Wind Rises.` 相符。如果 `minimum_should_match` 為 `1`，則會相符。如需詳細資訊，請參閱[最少應相符數]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`operator` | 字串 | 如果查詢字串包含多個搜尋詞彙，此參數決定文件被視為相符時，需要所有詞彙都相符（`AND`）或只需一個詞彙相符（`OR`）。有效值為：<br>- `OR`：字串 `to be` 會被解讀為 `to OR be`<br>- `AND`：字串 `to be` 會被解讀為 `to AND be`<br> 預設為 `OR`。
`prefix_length` | 非負整數 | 在模糊度中不予考量的開頭字元數。預設為 `0`。
`zero_terms_query` | 字串 | 在某些情況下，分析器會移除查詢字串中的所有詞彙。例如，`stop` 分析器會移除字串 `an but this` 中的所有詞彙。在這些情況下，`zero_terms_query` 指定不比對任何文件（`none`）或比對所有文件（`all`）。有效值為 `none` 和 `all`。預設為 `none`。
