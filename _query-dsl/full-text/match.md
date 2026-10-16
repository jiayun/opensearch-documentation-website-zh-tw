---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Match
parent: Full-text queries
nav_order: 10
---

# Match 查詢

使用 `match` 查詢對特定文件欄位執行全文搜尋。如果您對 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位執行 `match` 查詢，`match` 查詢會[分析]({{site.url}}{{site.baseurl}}/analyzers/index/)所提供的搜尋字串，並傳回符合該字串任一詞彙的文件。如果您對精確值欄位執行 `match` 查詢，則會傳回符合該精確值的文件。若要搜尋精確值欄位，請在篩選條件內容中使用 [`term`]({{site.url}}{{site.baseurl}}/query-dsl/term/term/) 查詢，此方式不會計算相關性分數。如需詳細資訊，請參閱[查詢與篩選條件內容]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)。

以下範例展示在 `title` 中搜尋單字 `wind` 的基本 `match` 查詢：

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

如果對 `text` 欄位執行 `match` 查詢，文字會使用 `analyzer` 參數中指定的分析器進行分析。接著，產生的詞元會使用 `operator` 參數中指定的運算子組合成布林查詢。預設運算子為 `OR`，因此查詢 `wind rise` 會轉換為 `wind OR rise`。在此範例中，此查詢會傳回文件 1--3，因為每份文件都有符合查詢的詞彙。若要指定 `and` 運算子，請使用下列查詢：

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

此查詢會建構為 `wind AND rise`，並傳回文件 1 作為符合的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 1,
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
    "max_score": 0.41195536,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.41195536,
        "_source": {
          "title": "Let the wind rise"
        }
      }
    ]
  }
}
```

</details>

### 最低應符合數

您可以指定 [`minimum_should_match`]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/) 參數，控制文件必須符合的最低詞彙數量，才會在結果中傳回：

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

現在文件必須同時符合兩個詞彙，因此只會傳回文件 1（這相當於 `and` 運算子）：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 1,
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
    "max_score": 0.41195536,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.41195536,
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

由於此範例中您並未明確指定分析器，因此會使用預設的 `standard` 分析器。預設分析器不會執行詞幹還原，因此在使用 `and` 運算子時，查詢 `the wind rises` 不會傳回任何結果，因為詞元 `rises` 與詞元 `rise` 不相符。若要變更搜尋分析器，請在 `analyzer` 欄位中指定。例如，下列查詢使用 `english` 分析器：

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

`english` 分析器會移除停用詞 `the` 並執行詞幹還原，產生詞元 `wind` 與 `rise`。這兩個詞元都在文件 1 中，因此文件 1 會在結果中傳回：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 1,
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
    "max_score": 0.41195536,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.41195536,
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

您可以在 `zero_terms_query` 參數中指定空查詢的行為。將 `zero_terms_query` 設為 `all` 會傳回索引中的所有文件，設為 `none` 則不會傳回任何文件：

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

為了因應拼寫錯誤，請在查詢中指定 `fuzziness`。如需支援值的相關資訊，請參閱[模糊比對]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)。

在大多數情況下，將 `fuzziness` 設為 `AUTO` 值的效果最好：

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

詞元 `wnid` 會比對到 `wind`，查詢會傳回文件 1 和 2：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.15448327,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.15448327,
        "_source": {
          "title": "Let the wind rise"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.15448327,
        "_source": {
          "title": "Gone with the wind"
        }
      }
    ]
  }
}
```
</details>

### 前置字元長度

拼字錯誤很少發生在字詞的開頭。因此，您可以指定相符前置字元的最小長度，以便在結果中傳回文件。例如，您可以將前述查詢改為包含 `prefix_length`：

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

前述查詢不會傳回任何結果。如果您將 `prefix_length` 改為 1，則會傳回文件 1 和文件 2，因為詞元 `wnid` 的第一個字母並未拼錯。

### 換位

在前述範例中，字詞 `wnid` 包含一個換位（`in` 被改為 `ni`）。根據預設，模糊比對允許換位，但您可以將 `fuzzy_transpositions` 設為 `false` 來禁止換位：

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

### 模糊度與同義字

模糊比對不會套用於具有同義字的查詢詞彙，也不會套用於分析器在同一位置產生多個詞元的任何其他詞彙。OpenSearch 會將這些詞元合併為同義字查詢，此查詢會混合其詞彙頻率，且不支援模糊擴充。如需範例，請參閱[同義字](#synonyms)。

## 同義字

如果欄位的搜尋分析器包含 [`synonym_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym-graph/) 詞元篩選器，則 `match` 查詢會將查詢詞彙擴充為其同義字。對於多詞彙同義字，`auto_generate_synonyms_phrase_query` 參數會決定同義字的詞彙是否必須以片語形式一起出現。

下列請求會建立 `furniture` 索引，其 `name` 欄位使用包含兩個同義字規則的搜尋分析器：`sofa, couch` 以及多詞彙同義字 `sleeper, sofa bed`：

```json
PUT furniture
{
  "settings": {
    "analysis": {
      "filter": {
        "furniture_synonyms": {
          "type": "synonym_graph",
          "synonyms": [
            "sofa, couch",
            "sleeper, sofa bed"
          ]
        }
      },
      "analyzer": {
        "synonym_search": {
          "tokenizer": "standard",
          "filter": [ "lowercase", "furniture_synonyms" ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "search_analyzer": "synonym_search"
      }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引：

```json
POST furniture/_bulk?refresh
{ "index": { "_id": "1" } }
{ "name": "Leather sofas" }
{ "index": { "_id": "2" } }
{ "name": "Velvet couch" }
{ "index": { "_id": "3" } }
{ "name": "Convertible sofa bed" }
{ "index": { "_id": "4" } }
{ "name": "Bed frame" }
{ "index": { "_id": "5" } }
{ "name": "Bed with sofa cushions" }
```
{% include copy-curl.html %}

根據預設，`auto_generate_synonyms_phrase_query` 為 `true`，因此搜尋 `sleeper` 會符合 `sleeper` 或片語 `"sofa bed"`，並且只會傳回文件 3。若要在任何位置符合多詞彙同義字的詞彙，請將 `auto_generate_synonyms_phrase_query` 設為 `false`：

```json
GET furniture/_search
{
  "query": {
    "match": {
      "name": {
        "query": "sleeper",
        "auto_generate_synonyms_phrase_query": false
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢會改寫為 `sleeper OR (sofa AND bed)`，因此會傳回文件 3 和文件 5，其中同時包含 `sofa` 和 `bed`，但並非以片語形式。若要查看 OpenSearch 如何改寫查詢，請使用 [Validate Query API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/validate/) 並搭配 `explain` 參數。對於前述查詢，其說明為 `((+name:sofa +name:bed) name:sleeper)`。

由於 `sofa` 具有同義字，因此對 `sofa` 進行模糊搜尋不會符合文件 1 中的複數形式 `sofas`，即使 `sofas` 與 `sofa` 的編輯距離為 1：

```json
GET furniture/_validate/query?explain
{
  "query": {
    "match": {
      "name": {
        "query": "sofa",
        "fuzziness": "AUTO"
      }
    }
  }
}
```
{% include copy-curl.html %}

說明中顯示 `sofa` 和 `couch` 的同義字查詢，且沒有模糊擴充：

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "valid": true,
  "explanations": [
    {
      "index": "furniture",
      "valid": true,
      "explanation": "Synonym(name:couch name:sofa)"
    }
  ]
}
```

模糊度仍會套用於查詢中的其他詞彙。例如，在查詢 `leathr sofa` 中，詞彙 `leathr` 會擴充為 `leathr~2`，而 `sofa` 只會擴充為其同義字。

## 參數

此查詢接受欄位名稱（`<field>`）作為頂層參數：

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

`<field>` 接受下列參數。除 `query` 外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的查詢字串。必要。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否為多詞同義字自動建立[片語比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。例如，若您將 `ba,batting average` 指定為同義字並搜尋 `ba`，OpenSearch 會搜尋 `ba OR "batting average"`（若此選項為 `true`）或 `ba OR (batting AND average)`（若此選項為 `false`）。預設為 `true`。
`analyzer` | 字串 | 用於將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為 `<field>` 所對應的搜尋分析器。若 `<field>` 未對應任何分析器，則使用索引的預設分析器。
`boost` | 浮點數 | 以給定的倍數提升子句的權重。適用於在複合查詢中衡量各子句的權重。[0, 1) 範圍內的值會降低相關性，大於 1 的值會提高相關性。預設為 `1`。
`enable_position_increments` | 布林值 | 當設為 `true` 時，產生的查詢會感知位置增量。當移除停用詞後在詞元之間留下不想要的「間隙」時，此設定很有用。預設為 `true`。
`fuzziness` | 字串 | 每個詞元比對時允許的最大編輯次數，可指定為 `0`、`1`、`2`、`AUTO` 或 `AUTO:<low>,<high>`。若未指定，詞元必須完全相符。如需更多資訊，請參閱[模糊比對]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)。
`fuzzy_rewrite` | 字串 | 決定 OpenSearch 如何改寫查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。若 `fuzziness` 參數不是 `0`，查詢預設使用 `top_terms_blended_freqs_${max_expansions}` 的 `fuzzy_rewrite` 方法。
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true`（預設）會在 `fuzziness` 選項的插入、刪除和取代操作中加入相鄰字元的交換。例如，若 `fuzzy_transpositions` 為 true（交換「n」和「i」），`wind` 與 `wnid` 之間的距離為 1；若為 false（刪除「n」，插入「n」），則距離為 2。若 `fuzzy_transpositions` 為 false，`rewind` 和 `wnid` 與 `wind` 的距離相同（皆為 2），儘管從以人為本的角度來看 `wnid` 顯然是拼字錯誤。預設值適合大多數使用情境。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，查詢字串 `"8.2"` 可以符合類型為 `float` 的欄位。預設為 `false`。
`max_expansions` | 正整數 | 查詢可擴展至的詞元數量上限。模糊查詢會「擴展至」`fuzziness` 所指定距離內的多個相符詞元，然後 OpenSearch 會嘗試比對這些詞元。預設為 `50`。
`minimum_should_match` | 正或負整數、正或負百分比、組合 | 若查詢字串包含多個搜尋詞彙且您使用 `or` 運算子，此參數指定文件被視為相符時必須符合的詞彙數量。例如，若 `minimum_should_match` 為 2，`wind often rising` 不符合 `The Wind Rises.`；若 `minimum_should_match` 為 `1`，則會相符。詳細資訊請參閱[最低應符合數]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`operator` | 字串 | 若查詢字串包含多個搜尋詞彙，指定文件被視為相符時是所有詞彙都需符合（`AND`），還是只需一個詞彙符合（`OR`）。有效值為：<br>- `OR`：字串 `to be` 會被解譯為 `to OR be`<br>- `AND`：字串 `to be` 會被解譯為 `to AND be`<br> 預設為 `OR`。
`prefix_length` | 非負整數 | 不納入模糊比對考量的前置字元數。預設為 `0`。
`zero_terms_query` | 字串 | 在某些情況下，分析器會移除查詢字串中的所有詞元。例如，`stop` 分析器會移除字串 `an but this` 中的所有詞元。在這些情況下，`zero_terms_query` 指定要符合零份文件（`none`）還是所有文件（`all`）。有效值為 `none` 和 `all`。預設為 `none`。
