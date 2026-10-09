---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Multi-match 查詢"
parent: Full-text queries
nav_order: 50
---

# Multi-match 查詢

`multi_match` 查詢會同時對多個欄位執行 [`match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/) 查詢，並將各欄位的結果合併為一個分數。`type` 參數控制欄位的合併方式。

請在下列情境中使用 `multi_match` 查詢：

- 同時搜尋標題與內文欄位，且標題中的符合應佔更高比重。
- 搜尋以多種分析器編製索引的相同文字，例如詞幹化與非詞幹化的子欄位。
- 搜尋一個概念被拆分到多個欄位的結構化資料，例如名字與姓氏。
- 使用 `phrase_prefix` 或 `bool_prefix` 類型，在多個欄位間建立邊輸入邊搜尋的體驗。

使用 `^` 運算子來提高特定欄位的權重。加權值是乘數，會讓某個欄位中的符合比其他欄位中的符合更具影響力。在下列範例中，title 欄位中 "wind" 的符合對 `_score` 的影響是 plot 欄位中符合的四倍：

```json
GET _search
{
  "query": {
    "multi_match": {
      "query": "wind",
      "fields": ["title^4", "plot"]
    }
  }
}
```
{% include copy-curl.html %}

結果是像 *The Wind Rises* 和 *Gone with the Wind* 這類電影會接近搜尋結果頂端，而像 *Twister* 這類劇情簡介中可能含有 "wind" 的電影則接近底部。

您可以在欄位名稱中使用萬用字元。例如，下列查詢會搜尋 `speaker` 欄位以及所有以 `play_` 開頭的欄位，例如 `play_name` 或 `play_title`：

```json
GET _search
{
  "query": {
    "multi_match": {
      "query": "hamlet",
      "fields": ["speaker", "play_*"]
    }
  }
}
```
{% include copy-curl.html %}

如果您未提供 `fields` 參數，`multi_match` 查詢會搜尋 `index.query.default_field` 設定中指定的欄位，其預設值為 `*`。`*` 值會選取對應中所有適用於[詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/)的欄位，但排除中繼資料欄位，並且查詢會搜尋所有這些欄位。

每個欄位至少會在查詢中加入一個子句，子句總數受 `indices.query.bool.max_clause_count` 設定限制，預設值為 1,024。搜尋大量欄位，無論是明確指定或使用 `*` 這類萬用字元模式，都可能超出此限制。
{: .note}

## Multi-match 查詢類型

OpenSearch 支援下列 multi-match 查詢類型，它們在內部執行查詢的方式有所不同：

- [`best_fields`](#best-fields)（預設）：回傳符合任一欄位的文件。使用最佳符合欄位的 `_score`。
- [`most_fields`](#most-fields)：回傳符合任一欄位的文件。使用所有符合欄位分數的總和。
- [`cross_fields`](#cross-fields)：將使用相同分析器的欄位視為一個欄位，並在其中任一欄位搜尋每個詞彙。
- [`phrase`](#phrase)：在每個欄位上執行 `match_phrase` 查詢。使用最佳符合欄位的 `_score`。
- [`phrase_prefix`](#phrase-prefix)：在每個欄位上執行 `match_phrase_prefix` 查詢。使用最佳符合欄位的 `_score`。
- [`bool_prefix`](#boolean-prefix)：在每個欄位上執行 `match_bool_prefix` 查詢。使用所有符合欄位分數的總和。

`best_fields` 與 `most_fields` 類型是以欄位為中心：它們為每個欄位建立一個查詢，然後合併各欄位的分數。`cross_fields` 類型則是以詞彙為中心：它會一起在所有欄位中查詢每個查詢詞彙。並非每個參數都適用於每種類型。如需更多資訊，請參閱[各類型支援的參數](#parameter-support-by-type)。

## 最佳欄位

當查詢詞彙只有在同一個欄位中一起出現時才最具意義時，請使用 `best_fields` 類型。例如，`northern lights` 出現在單一欄位中，比 `northern` 出現在一個欄位而 `lights` 出現在另一個欄位是更強的符合。

例如，假設有一個包含下列科學文章的索引：

```json
PUT /articles/_doc/1
{
  "title": "Aurora borealis",
  "description": "Northern lights, or aurora borealis, explained"
}
```
{% include copy-curl.html %}

```json
PUT /articles/_doc/2
{
  "title": "Sun deprivation in the Northern countries",
  "description": "Using fluorescent lights for therapy"
}
```
{% include copy-curl.html %}

您可以搜尋 title 或 description 中包含 `northern lights` 的文章：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "northern lights",
      "type": "best_fields",
      "fields": [ "title", "description" ],
      "tie_breaker": 0.3
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以以下 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢執行，並為每個欄位使用一個 `match` 查詢：

```json
GET /articles/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "northern lights" }},
        { "match": { "description": "northern lights" }}
      ],
      "tie_breaker": 0.3
    }
  }
}
```

結果包含兩份文件，但文件 1 的分數較高，因為兩個字都在 `description` 欄位中：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.38367155,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.38367155,
        "_source": {
          "title": "Aurora borealis",
          "description": "Northern lights, or aurora borealis, explained"
        }
      },
      {
        "_index": "articles",
        "_id": "2",
        "_score": 0.2873873,
        "_source": {
          "title": "Sun deprivation in the Northern countries",
          "description": "Using fluorescent lights for therapy"
        }
      }
    ]
  }
}
```

`best_fields` 查詢使用最佳符合欄位的分數。如果您指定 `tie_breaker`，分數會以下列演算法計算：

取最佳符合欄位的分數，並為所有其他符合欄位加上 (`tie_breaker` * `_score`)。

## 最多欄位

`most_fields` 查詢適用於多個包含相同文字但以不同方式分析的欄位。例如，原始欄位可能包含以 `standard` 分析器分析的文字，而另一個欄位可能包含以 `english` 分析器（會執行詞幹化）分析的相同文字。詞幹化欄位會符合最多文件，而非詞幹化欄位則會將最接近的符合移到結果頂端。

下列請求會建立一個 `recipes` 索引，其中 `title` 欄位有一個 `english` 子欄位：

```json
PUT /recipes
{
  "mappings": {
    "properties": {
      "title": { 
        "type": "text",
        "fields": {
          "english": { 
            "type": "text",
            "analyzer": "english"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

考量在 `recipes` 索引中編製索引的下列兩份文件：

```json
PUT /recipes/_doc/1
{
  "title": "Buttered toasts"
}
```
{% include copy-curl.html %}

```json
PUT /recipes/_doc/2
{
  "title": "Buttering a toast"
}
```
{% include copy-curl.html %}

`standard` 分析器將標題 `Buttered toasts` 分析為 [`buttered`, `toasts`]，將標題 `Buttering a toast` 分析為 [`buttering`, `a`, `toast`]。另一方面，`english` 分析器對兩個標題都產生相同的詞元清單 [`butter`, `toast`]，因為它會執行詞幹化並移除停用詞 `a`。

下列 `most_fields` 查詢會同時搜尋 `title` 欄位及其 `english` 子欄位：

```json
GET /recipes/_search
{
  "query": {
    "multi_match": {
      "query": "buttered toast",
      "fields": [ 
        "title",
        "title.english"
      ],
      "type": "most_fields" 
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以下列布林查詢執行：

```json
GET recipes/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title": "buttered toast" }},
        { "match": { "title.english": "buttered toast" }}
      ]
    }
  }
}
```

為計算相關性分數，OpenSearch 會將所有符合該文件的 `match` 子句的分數加總。

兩份文件對 `title.english` 欄位的符合程度相同，因為它們的詞幹化詞元完全一致。在 `title` 欄位中，文件 1 符合詞彙 `buttered`，文件 2 符合詞彙 `toast`。每個詞彙只出現在一個文件中，但文件 1 的 `title` 欄位包含較少的詞元，因此其符合分數較高。若沒有 `title.english` 欄位，使用不同字詞形式的文件，例如 `buttering`，將只會在剩餘的詞彙上符合：

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
    "max_score": 0.508889,
    "hits": [
      {
        "_index": "recipes",
        "_id": "1",
        "_score": 0.508889,
        "_source": {
          "title": "Buttered toasts"
        }
      },
      {
        "_index": "recipes",
        "_id": "2",
        "_score": 0.4569852,
        "_source": {
          "title": "Buttering a toast"
        }
      }
    ]
  }
}
```

文件 1 在 `title` 欄位的分數為 `0.34314215`，在 `title.english` 欄位的分數為 `0.16574687`，其最終分數為兩者之和 `0.508889`。

## 運算子與最少應符合數

`best_fields` 和 `most_fields` 查詢會以欄位為單位產生 match 查詢（每個欄位一個）。因此，`minimum_should_match` 和 `operator` 參數會套用至每個欄位，而這通常不是您想要的行為。

例如，假設有一個 `customers` 索引，其中包含下列文件：

```json
PUT customers/_doc/1 
{
  "first_name": "John",
  "last_name": "Doe"
}
```
{% include copy-curl.html %}

```json
PUT customers/_doc/2 
{
  "first_name": "Jane",
  "last_name": "Doe"
}
```
{% include copy-curl.html %}

若您要在 `customers` 索引中搜尋 `John Doe`，可能會建構下列查詢：

```json
GET customers/_search
{
  "query": {
    "multi_match" : {
      "query": "John Doe",
      "type": "best_fields",
      "fields": [ "first_name", "last_name" ],
      "operator": "and" 
    }
  }
}
```
{% include copy-curl.html %}

此查詢中 `and` 運算子的用意是尋找同時符合 `John` 和 `Doe` 的文件。然而，此查詢不會傳回任何結果。您可以執行 [Validate Query API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/validate/) 來了解查詢的執行方式：

```json
GET customers/_validate/query?explain
{
  "query": {
    "multi_match" : {
      "query":      "John Doe",
      "type":       "best_fields",
      "fields":     [ "first_name", "last_name" ],
      "operator":   "and" 
    }
  }
}
```
{% include copy-curl.html %}

從回應中可以看到，此查詢嘗試將 `John` 和 `Doe` 兩者都與 `first_name` 或 `last_name` 欄位比對：

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
      "index": "customers",
      "valid": true,
      "explanation": "((+last_name:john +last_name:doe) | (+first_name:john +first_name:doe))"
    }
  ]
}
```

由於沒有任何欄位同時包含這兩個字，因此不會傳回任何結果。

跨欄位搜尋的更佳替代方案是使用 [`cross_fields`](#cross-fields) 查詢。與以欄位為中心的 `best_fields` 和 `most_fields` 查詢不同，`cross_fields` 查詢是以詞彙為中心。

## 跨欄位

使用 `cross_fields` 查詢可跨多個欄位搜尋資料。例如，若索引包含客戶資料，客戶的名字和姓氏會位於不同欄位中。然而，當您搜尋 `John Doe` 時，您會希望收到 `John` 位於 `first_name` 欄位且 `Doe` 位於 `last_name` 欄位的文件。

`most_fields` 查詢在此情況下無法運作，原因如下：

- [`operator` 和 `minimum_should_match`](#operator-and-minimum-should-match) 參數是以欄位為單位套用，而非以詞彙為單位套用。
- `first_name` 和 `last_name` 欄位中的詞頻可能導致非預期的結果。例如，若某人的名字剛好是 `Doe`，具有此名字的文件會被視為更佳的符合項目，因為此名字不會出現在任何其他文件中。

避免這兩個問題的一種方法，是在編製索引時使用 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 對應參數，將 `first_name` 和 `last_name` 的值複製到單一 `full_name` 欄位中，然後搜尋該欄位。`cross_fields` 查詢則在查詢時解決相同的問題，而不需要變更對應。

`cross_fields` 查詢會將查詢字串分析為個別詞彙，然後在任一欄位中搜尋每個詞彙，就如同這些欄位是同一個欄位一樣。

以下是針對 `John Doe` 的 `cross_fields` 查詢：

```json
GET /customers/_search
{
  "query": {
    "multi_match" : {
      "query": "John Doe",
      "type": "cross_fields",
      "fields": [ "first_name", "last_name" ],
      "operator": "and"
    }
  }
}
```
{% include copy-curl.html %}

回應包含唯一同時存在 `John` 和 `Doe` 的文件：

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
    "max_score": 0.3979403,
    "hits": [
      {
        "_index": "customers",
        "_id": "1",
        "_score": 0.3979403,
        "_source": {
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ]
  }
}
```

使用 Validate Query API 查看前述查詢的執行方式：

```json
GET /customers/_validate/query?explain
{
  "query": {
    "multi_match" : {
      "query": "John Doe",
      "type": "cross_fields",
      "fields": [ "first_name", "last_name" ],
      "operator": "and"
    }
  }
}
```
{% include copy-curl.html %}

從回應中可以看到，每個詞彙都必須至少存在於其中一個欄位中：

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
      "index": "customers",
      "valid": true,
      "explanation": "+blended(terms:[last_name:john, first_name:john]) +blended(terms:[last_name:doe, first_name:doe])"
    }
  ]
}
```

每個 `blended` 子句都會將其所有欄位視為同一個欄位來為詞彙評分。為此，OpenSearch 會調整詞彙在每個欄位中的文件頻率。詞彙最常出現的欄位會保留其文件頻率，其他每個欄位則會收到該頻率加一。例如，若 `doe` 出現在 3 份文件的 `last_name` 欄位中，以及 1 份文件的 `first_name` 欄位中，則 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/explain/) 會回報 `last_name:doe` 的文件頻率為 3，`first_name:doe` 的文件頻率為 4。因此，`doe` 在 `first_name` 欄位中的罕見出現不再勝過在 `last_name` 欄位中的常見出現，而在 `last_name`（最有可能包含 `doe` 的欄位）中的符合項目分數會稍高一些。

`cross_fields` 查詢通常只適用於 `boost` 為 1 的短字串欄位。在其他情況下，由於加權 (boost)、詞頻和長度正規化對分數的影響方式，分數無法產生有意義的詞彙統計資料混合結果。
{: .note}

`cross_fields` 查詢不支援 `fuzziness` 參數。如需詳細資訊，請參閱[各類型的參數支援](#parameter-support-by-type)。
{: .note}

### 分析

`cross_fields` 查詢只會在使用相同搜尋分析器的欄位之間混合詞彙，因為只有這些欄位會從查詢字串產生相同的詞彙。OpenSearch 會依分析器將欄位分組，為每個群組建立一組 `blended` 子句，然後在 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢中合併這些群組。分數最高的群組決定分數，而 `tie_breaker` 參數控制其他群組的貢獻程度。

例如，下列請求會建立 `customer_names` 索引，其中 `first_name` 和 `last_name` 欄位使用預設的 `standard` 分析器，而其 `edge` 子欄位則使用 edge n-gram 分析器：

```json
PUT customer_names
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "my_tokenizer"
        }
      },
      "tokenizer": {
        "my_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "first_name": { 
        "type": "text",
        "fields": {
          "edge": { 
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      },
      "last_name": { 
        "type": "text",
        "fields": {
          "edge": { 
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將一份文件編製索引至 `customer_names` 索引：

```json
PUT /customer_names/_doc/1
{
  "first_name": "John",
  "last_name": "Doe"
}
```
{% include copy-curl.html %}

下列 `cross_fields` 查詢會在全部四個欄位中搜尋 `John`：

```json
GET /customer_names/_search
{
  "query": {
    "multi_match" : {
      "query": "John",
      "type": "cross_fields",
      "fields": [
        "first_name", "first_name.edge",
        "last_name",  "last_name.edge"
      ]
    }
  }
}
```
{% include copy-curl.html %}

若要查看查詢的執行方式，請執行 Validate Query API：

```json
GET /customer_names/_validate/query?explain
{
  "query": {
    "multi_match" : {
      "query": "John",
      "type": "cross_fields",
      "fields": [
        "first_name", "first_name.edge",
        "last_name",  "last_name.edge"
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應顯示以 `|`（`dis_max`）運算子分隔的兩個群組。`last_name` 和 `first_name` 欄位組成一個群組，`last_name.edge` 和 `first_name.edge` 欄位組成另一個群組。在第二個群組中，edge n-gram 分析器會將 `John` 分割為詞彙 `Jo`、`Joh` 和 `John`。由於自訂分析器沒有 `lowercase` 篩選器，這些詞彙會保留原本的大小寫：

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
      "index": "customer_names",
      "valid": true,
      "explanation": "(blended(terms:[last_name:john, first_name:john]) | (blended(terms:[last_name.edge:Jo, first_name.edge:Jo]) blended(terms:[last_name.edge:Joh, first_name.edge:Joh]) blended(terms:[last_name.edge:John, first_name.edge:John])))"
    }
  ]
}
```

#### 使用運算子和最少應符合數結合欄位群組

`operator` 和 `minimum_should_match` 參數會分別套用至每個欄位群組。當群組產生的詞彙數量不同時，可能導致 [`operator` 和 `minimum_should_match`](#operator-and-minimum-should-match) 中所述的問題。例如，使用 `"operator": "and"` 時，查詢 `John Doe` 會要求 `edge` 群組符合 `John Doe` 的每個 n-gram，包括索引中從未出現的 `John D` 和 `John Do`。此時，文件只能透過 `standard` 群組符合查詢。

若要獨立控制每個群組，請將查詢改寫為兩個 `cross_fields` 子查詢，並在 `bool` 查詢中結合這些子查詢，且僅將 `minimum_should_match` 套用至其中一個子查詢：

```json
GET /customer_names/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "multi_match": {
            "query": "John Doe",
            "type": "cross_fields",
            "fields": [
              "first_name",
              "last_name"
            ],
            "minimum_should_match": "1"
          }
        },
        {
          "multi_match": {
            "query": "John Doe",
            "type": "cross_fields",
            "fields": [
              "first_name.edge",
              "last_name.edge"
            ]
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

#### 強制將所有欄位放入同一群組

若要將所有欄位放入同一群組，請在查詢中指定 `analyzer`。OpenSearch 接著會使用該分析器分析查詢字串一次，並在每個欄位中搜尋產生的詞彙：

```json
GET customer_names/_search
{
  "query": {
   "multi_match" : {
      "query": "John Doe",
      "type": "cross_fields",
      "analyzer": "standard", 
      "fields": [ "first_name", "last_name", "*.edge" ]
    }
  }
}
```
{% include copy-curl.html %}

對上述查詢執行 Validate Query API，會顯示每個詞彙都有一個 `blended` 子句，涵蓋全部四個欄位：

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
      "index": "customer_names",
      "valid": true,
      "explanation": "blended(terms:[last_name.edge:john, last_name:john, first_name:john, first_name.edge:john]) blended(terms:[last_name.edge:doe, last_name:doe, first_name:doe, first_name.edge:doe])"
    }
  ]
}
```

當您覆寫分析器時，查詢詞彙便不再符合子欄位編製索引的方式。在此範例中，`standard` 分析器會針對查詢 `Jo` 產生小寫詞彙 `jo`，但 `edge` 子欄位僅包含 `Jo`。因此，使用 `"analyzer": "standard"` 搜尋 `Jo` 不會傳回任何文件，而不使用 `analyzer` 參數執行相同搜尋時，則會透過 `edge` 子欄位符合文件 1。只有當所有分組欄位都能符合分析器產生的詞彙時，才應覆寫分析器。
{: .important}

## 片語 

`phrase` 查詢的行為與 [`best_fields`](#best-fields) 查詢類似，但使用 `match_phrase` 查詢來取代 `match` 查詢。

以下是針對 [`best_fields`](#best-fields) 一節中所述索引的 `phrase` 查詢範例：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "northern lights",
      "type": "phrase",
      "fields": [ "title", "description" ]
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以以下 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢的形式執行，每個欄位各有一個 `match_phrase` 查詢：

```json
GET articles/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match_phrase": { "title": "northern lights" }},
        { "match_phrase": { "description": "northern lights" }}
      ]
    }
  }
}
```

依預設，`phrase` 查詢只會在詞彙以相同順序相鄰出現時符合。文件 2 包含這兩個詞彙，但未構成片語，因此結果只會傳回文件 1：

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
    "max_score": 0.38367155,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.38367155,
        "_source": {
          "title": "Aurora borealis",
          "description": "Northern lights, or aurora borealis, explained"
        }
      }
    ]
  }
}
```
</details>

使用 `slop` 參數可允許查詢片語中的字詞之間出現其他字詞。例如，以下查詢會將 `fluorescent` 和 `therapy` 之間最多包含兩個字詞的文字視為符合：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "fluorescent therapy",
      "type": "phrase",
      "fields": [ "title", "description" ],
      "slop": 2
    }
  }
}
```
{% include copy-curl.html %}

回應包含文件 2：

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
    "max_score": 0.31835568,
    "hits": [
      {
        "_index": "articles",
        "_id": "2",
        "_score": 0.31835568,
        "_source": {
          "title": "Sun deprivation in the Northern countries",
          "description": "Using fluorescent lights for therapy"
        }
      }
    ]
  }
}
```
</details>

當 `slop` 的值小於 2 時，不會傳回任何文件。

`phrase` 查詢不支援 `fuzziness` 參數。如需詳細資訊，請參閱[各類型的參數支援](#parameter-support-by-type)。
{: .note}

## 片語前綴 

`phrase_prefix` 查詢的行為與 [`phrase`](#phrase) 查詢類似，但使用 `match_phrase_prefix` 查詢來取代 `match_phrase` 查詢。

以下是針對 [`best_fields`](#best-fields) 一節中所述索引的 `phrase_prefix` 查詢範例：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "northern light",
      "type": "phrase_prefix",
      "fields": [ "title", "description" ]
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以以下 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢的形式執行，每個欄位各有一個 `match_phrase_prefix` 查詢：

```json
GET articles/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match_phrase_prefix": { "title": "northern light" }},
        { "match_phrase_prefix": { "description": "northern light" }}
      ]
    }
  }
}
```

`phrase_prefix` 類型接受 `slop` 參數，其運作方式與 `phrase` 類型相同。它也接受 `max_expansions` 參數，用來限制查詢中最後一個詞彙可擴展成的詞彙數量。預設值為 `50`。

`phrase_prefix` 查詢不支援 `fuzziness` 參數。如需詳細資訊，請參閱[各類型的參數支援](#parameter-support-by-type)。
{: .note}

## 布林前綴

`bool_prefix` 查詢為文件評分的方式與 [`most_fields`](#most-fields) 查詢類似，但使用 [`match_bool_prefix`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/) 查詢，而非 `match` 查詢。`match_bool_prefix` 查詢會精確比對除了最後一個詞彙以外的每個詞彙，並將最後一個詞彙視為前綴，這使其適用於隨打即搜的體驗。

以下是針對 [`best_fields`](#best-fields) 一節所述索引的範例 `bool_prefix` 查詢：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "northern li",
      "type": "bool_prefix",
      "fields": [ "title", "description" ]
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以針對每個欄位的 `match_bool_prefix` 查詢，執行為下列布林查詢。所有相符子句的分數會相加：

```json
GET articles/_search
{
  "query": {
    "bool": {
      "should": [
        { "match_bool_prefix": { "title": "northern li" }},
        { "match_bool_prefix": { "description": "northern li" }}
      ]
    }
  }
}
```

兩份文件都會被傳回。文件 1 在 `description` 欄位中符合 `northern` 與前綴 `li` (`lights`)。文件 2 在 `title` 欄位中符合 `northern`，並在 `description` 欄位中符合前綴 `li`：

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
    "max_score": 1.3037697,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 1.3037697,
        "_source": {
          "title": "Aurora borealis",
          "description": "Northern lights, or aurora borealis, explained"
        }
      },
      {
        "_index": "articles",
        "_id": "2",
        "_score": 1.261565,
        "_source": {
          "title": "Sun deprivation in the Northern countries",
          "description": "Using fluorescent lights for therapy"
        }
      }
    ]
  }
}
```
</details>

用於建構 term 查詢的詞彙支援 `fuzziness`、`prefix_length`、`max_expansions`、`fuzzy_rewrite` 及 `fuzzy_transpositions` 參數，但這些參數不會影響由最後一個詞彙所建構的前綴查詢。`bool_prefix` 查詢不支援 `slop` 參數。
{: .note}

## 參數

此查詢接受下列參數。除了 `query` 以外的所有參數都是選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的查詢字串。必要。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否要為多詞元同義詞自動建立 [match phrase 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。例如，若您將 `ba,batting average` 指定為同義詞並搜尋 `ba`，OpenSearch 會搜尋 `ba OR "batting average"` (若此選項為 `true`) 或 `ba OR (batting AND average)` (若此選項為 `false`)。預設為 `true`。
`analyzer` | 字串 | 用於將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `default_field` 所指定的索引時分析器。若未為 `default_field` 指定分析器，則 `analyzer` 是索引的預設分析器。如需 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`boost` | 浮點數 | 以指定的乘數提升子句。適用於在複合查詢中加權子句。位於 [0, 1) 範圍內的值會降低相關性，大於 1 的值則會提高相關性。預設為 `1`。
`fields` | 字串陣列 | 要搜尋的欄位清單。若您未提供 `fields` 參數，`multi_match` 查詢會搜尋 `index.query.default_field` 設定中指定的欄位，該設定預設為 `*`。
`fuzziness` | 字串 | 在判斷某個詞元是否符合某個值時，將一個字變更為另一個字所需的字元編輯次數 (插入、刪除、取代)。例如，`wined` 與 `wind` 之間的距離為 1。有效值為非負整數或 `AUTO`。預設值 `AUTO` 會根據搜尋詞元的長度動態選取編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂閾值，其中 `low` 與 `high` 定義字元長度界線。省略時，OpenSearch 會使用 `AUTO:3,6` 作為預設值，套用下列規則：<br>- 包含 0--2 個字元的詞元：需要完全相符 (0 次編輯)。<br>- 包含 3--5 個字元的詞元：最多允許 1 次編輯。<br>- 包含 6 個以上字元的詞元：最多允許 2 次編輯。<br>例如，`AUTO:4,7` 要求包含 0--3 個字元的詞元完全相符，包含 4--6 個字元的詞元最多允許 1 次編輯，包含 7 個以上字元的詞元最多允許 2 次編輯。大多數情境建議使用 `AUTO`。`phrase`、`phrase_prefix` 及 `cross_fields` 查詢不支援。
`fuzzy_rewrite` | 字串 | 決定 OpenSearch 如何重寫查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 及 `top_terms_blended_freqs_N`。若 `fuzziness` 參數不是 `0`，查詢預設會使用 `top_terms_blended_freqs_${max_expansions}` 的 `fuzzy_rewrite` 方法。預設為 `constant_score`。
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true` (預設) 會將相鄰字元的交換加入 `fuzziness` 選項的插入、刪除及取代操作。例如，若 `fuzzy_transpositions` 為 true，`wind` 與 `wnid` 之間的距離為 1 (交換 "n" 與 "i")；若為 false，則距離為 2 (刪除 "n"、插入 "n")。若 `fuzzy_transpositions` 為 false，則 `rewind` 與 `wnid` 與 `wind` 的距離相同 (2)，儘管以更貼近人類的觀點來看，`wnid` 是明顯的打字錯誤。預設值對大多數使用情境而言是很好的選擇。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，查詢字串 `"8.2"` 可能符合類型為 `float` 的欄位。預設為 `false`。
`max_expansions` | 正整數 | 查詢可擴展的詞元數上限。模糊查詢會「擴展為」若干符合 `fuzziness` 中所指定距離的相符詞元。接著 OpenSearch 會嘗試比對這些詞元。預設為 `50`。
`minimum_should_match` | 正整數或負整數、正百分比或負百分比，或其組合 | 若查詢字串包含多個搜尋詞元，且您使用 `or` 運算子，則文件必須符合的詞元數才會被視為相符。例如，若 `minimum_should_match` 為 2，則 `wind often rising` 不符合 `The Wind Rises.`；若 `minimum_should_match` 為 `1`，則符合。如需詳細資訊，請參閱[最少應符合數]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`operator` | 字串 | 若查詢字串包含多個搜尋詞元，文件必須所有詞元都符合 (`AND`) 或只需一個詞元符合 (`OR`) 才會被視為相符。有效值為：<br>- `OR`：字串 `to be` 會解讀為 `to OR be`<br>- `AND`：字串 `to be` 會解讀為 `to AND be`<br> 預設為 `OR`。
`prefix_length` | 非負整數 | 模糊比對時不列入考量的前置字元數。預設為 `0`。
`slop` | `0` (預設) 或正整數 | 控制查詢中的詞元可以錯排到什麼程度仍被視為相符。根據 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html#getSlop--)：「查詢片語中詞元之間允許的其他詞元數。例如，要交換兩個詞元的順序需要兩次移動 (第一次移動會將詞元疊在一起)，因此若要允許片語重新排序，slop 必須至少為二。值為零則需要完全相符。」支援 `phrase` 與 `phrase_prefix` 查詢類型。
`tie_breaker` | 浮點數 | 介於 0 與 1.0 之間的係數，用於讓符合多個查詢子句的文件獲得更高權重。如需詳細資訊，請參閱[`tie_breaker` 參數](#the-tie_breaker-parameter)。
`type` | 字串 | 多重比對查詢類型。有效值為 `best_fields`、`most_fields`、`cross_fields`、`phrase`、`phrase_prefix`、`bool_prefix`。預設為 `best_fields`。
`zero_terms_query` | 字串 | 在某些情況下，分析器會移除查詢字串中的所有詞元。例如，`stop` 分析器會從字串 `an but this` 中移除所有詞元。在這些情況下，`zero_terms_query` 會指定要比對沒有文件 (`none`) 或所有文件 (`all`)。有效值為 `none` 與 `all`。預設為 `none`。

### 各類型支援的參數

並非每個參數都適用於每種查詢類型。OpenSearch 會以 `400` 錯誤拒絕下列組合。

參數 | 查詢類型 | 錯誤
:--- | :--- | :---
`fuzziness` | `cross_fields`, `phrase`, `phrase_prefix` | `Fuzziness not allowed for type [<type>]`
`slop` | `bool_prefix` | `[slop] not allowed for type [bool_prefix]`

查詢類型未使用的其他參數會被忽略，不會產生錯誤。例如，`slop` 參數對 `best_fields` 或 `most_fields` 查詢沒有作用。下表列出每種查詢類型除了 `query`、`fields`、`type`、`analyzer`、`boost`、`lenient` 和 `zero_terms_query`（這些適用於所有類型）之外，還有作用的參數。

查詢類型 | 額外支援的參數
:--- | :---
`best_fields` | `auto_generate_synonyms_phrase_query`, `fuzziness`, `fuzzy_rewrite`, `fuzzy_transpositions`, `max_expansions`, `minimum_should_match`, `operator`, `prefix_length`, `tie_breaker`
`most_fields` | `auto_generate_synonyms_phrase_query`, `fuzziness`, `fuzzy_rewrite`, `fuzzy_transpositions`, `max_expansions`, `minimum_should_match`, `operator`, `prefix_length`, `tie_breaker`
`cross_fields` | `auto_generate_synonyms_phrase_query`, `minimum_should_match`, `operator`, `tie_breaker`
`phrase` | `slop`, `tie_breaker`
`phrase_prefix` | `max_expansions`, `slop`, `tie_breaker`
`bool_prefix` | `auto_generate_synonyms_phrase_query`, `fuzziness`, `fuzzy_rewrite`, `fuzzy_transpositions`, `max_expansions`, `minimum_should_match`, `operator`, `prefix_length`, `tie_breaker`

對於 `bool_prefix` 類型，模糊參數會套用至除了最後一個詞元以外的每個詞元，最後一個詞元一律以字首比對。

### tie_breaker 參數

`tie_breaker` 參數決定符合的欄位分數如何合併。對於 `cross_fields` 類型，它也決定每個 `blended` 子句內欄位的分數以及欄位群組的分數如何合併。`tie_breaker` 參數接受下列值：

- 0.0（`best_fields`、`cross_fields`、`phrase` 和 `phrase_prefix` 查詢的預設值）：採用群組中任一欄位傳回的最佳單一分數。
- 1.0（`most_fields` 和 `bool_prefix` 查詢的預設值）：將群組中所有欄位的分數相加。
- (0, 1) 範圍內的浮點數值：採用最佳符合欄位的最佳單一分數，並為所有其他符合的欄位加上 (`tie_breaker` * `_score`)。