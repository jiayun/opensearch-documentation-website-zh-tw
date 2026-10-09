---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多重比對"
parent: Full-text queries
nav_order: 50
---

# 多重比對查詢

多重比對操作的運作方式類似於 [match]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/) 操作。您可以使用 `multi_match` 查詢搜尋多個欄位。

`^` 會「提升」某些欄位的權重。提升值是乘數，會讓某個欄位的匹配比其他欄位的匹配更具份量。在以下範例中，title 欄位中對「wind」的匹配對 `_score` 的影響是 plot 欄位中匹配的四倍：

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

結果是像 *The Wind Rises* 和 *Gone with the Wind* 這類電影會接近搜尋結果頂端，而像 *Twister* 這類電影（其劇情摘要中應該有「wind」）則接近底端。

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

如果您未提供 `fields` 參數，`multi_match` 查詢會搜尋 `index.query. Default_field` 設定中指定的欄位，該設定預設為 `*`。預設行為是擷取對應中所有符合 [詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/) 資格的欄位、篩除中繼資料欄位，並結合所有擷取的欄位來建立查詢。

查詢中子句的最大數量由 `indices.query.bool.max_clause_count` 設定定義，預設值為 1,024。
{: .note}

## 多重比對查詢類型

OpenSearch 支援下列多重比對查詢類型，這些類型在內部執行查詢的方式上有所不同：

- [`best_fields`](#best-fields)（預設）：回傳符合任一欄位的文件。使用最佳匹配欄位的 `_score`。
- [`most_fields`](#most-fields)：回傳符合任一欄位的文件。使用各匹配欄位的合併分數。
- [`cross_fields`](#cross-fields)：將所有欄位視為單一欄位。將具有相同 `analyzer` 的欄位一起處理，並匹配任一欄位中的詞。
- [`phrase`](#phrase)：在每個欄位上執行 `match_phrase` 查詢。使用最佳匹配欄位的 `_score`。
- [`phrase_prefix`](#phrase-prefix)：在每個欄位上執行 `match_phrase_prefix` 查詢。使用最佳匹配欄位的 `_score`。
- [`bool_prefix`](#boolean-prefix)：在每個欄位上執行 `match_bool_prefix` 查詢。使用各匹配欄位的合併分數。

## 最佳欄位

如果您要搜尋指定某個概念的兩個詞，您會希望這兩個詞相鄰的結果獲得較高分數。

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

上述查詢會以對每個欄位各執行一個 `match` 查詢的 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢形式執行：

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

結果包含兩份文件，但文件 1 的分數較高，因為兩個詞都出現在 `description` 欄位中：

```json
{
  "took": 30,
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
    "max_score": 0.84407747,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.84407747,
        "_source": {
          "title": "Aurora borealis",
          "description": "Northern lights, or aurora borealis, explained"
        }
      },
      {
        "_index": "articles",
        "_id": "2",
        "_score": 0.6322521,
        "_source": {
          "title": "Sun deprivation in the Northern countries",
          "description": "Using fluorescent lights for therapy"
        }
      }
    ]
  }
}
```

`best_fields` 查詢使用最佳匹配欄位的分數。如果您指定 `tie_breaker`，分數會以下列演算法計算：

取最佳匹配欄位的分數，並對所有其他匹配欄位加上（`tie_breaker` * `_score`）。

## 最多欄位

`most_fields` 查詢適用於包含相同文字但以不同方式分析的多個欄位。例如，原始欄位可能包含以 `standard` 分析器分析的文字，而另一個欄位可能包含以執行詞幹提取的 `english` 分析器分析的相同文字：

```json
PUT /articles
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

考慮在 `articles` 索引中編製索引的下列兩份文件：

```json
PUT /articles/_doc/1
{
  "title": "Buttered toasts"
}
```
{% include copy-curl.html %}

```json
PUT /articles/_doc/2
{
  "title": "Buttering a toast"
}
```
{% include copy-curl.html %}

`standard` 分析器將標題 `Buttered toast` 分析為 [`buttered`, `toasts`]，並將標題 `Buttering a toast` 分析為 [`buttering`, `a`, `toast`]。另一方面，`english` 分析器因為詞幹提取，對兩個標題都產生相同的詞元清單 [`butter`, `toast`]。

您可以使用 `most_fields` 查詢以回傳盡可能多的文件：

```json
GET /articles/_search
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

上述查詢會以下列布林查詢的形式執行：

```json
GET articles/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title": "buttered toasts" }},
        { "match": { "title.english": "buttered toasts" }}
      ]
    }
  }
}
```

為計算相關性分數，文件在所有 `match` 子句上的分數會相加，然後將結果除以 `match` 子句的數量。

納入 `title.english` 欄位可擷取符合詞幹化詞元的第二份文件：

```json
{
  "took": 9,
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
    "max_score": 1.4418206,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 1.4418206,
        "_source": {
          "title": "Buttered toasts"
        }
      },
      {
        "_index": "articles",
        "_id": "2",
        "_score": 0.09304003,
        "_source": {
          "title": "Buttering a toast"
        }
      }
    ]
  }
}
```

因為 `title` 和 `title.english` 欄位都符合第一份文件，所以它的相關性分數較高。

## 運算子與最低應符合數量

`best_fields` 與 `most_fields` 查詢會以欄位為基礎產生 match 查詢（每個欄位一個）。因此，`minimum_should_match` 與 `operator` 參數會套用至每個欄位，這通常不是您想要的行為。

例如，假設有一個 `customers` 索引包含下列文件：

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

如果您要在 `customers` 索引中搜尋 `John Doe`，您可能會建構下列查詢：

```json
GET customers/_validate/query?explain
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

此查詢中 `and` 運算子的用意是要找出同時符合 `John` 與 `Doe` 的文件。然而，此查詢不會傳回任何結果。您可以執行 Validate API 來了解查詢的執行方式：

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

從回應中可以看出，此查詢嘗試將 `John` 與 `Doe` 兩者都對應到 `first_name` 或 `last_name` 欄位：

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
      "explanation": "((+first_name:john +first_name:doe) | (+last_name:john +last_name:doe))"
    }
  ]
}
```

因為這兩個欄位都不包含這兩個詞，所以不會傳回任何結果。

跨欄位搜尋的更好替代方案是使用 [`cross_fields`](#cross-fields) 查詢。與以欄位為中心的 `best_fields` 與 `most_fields` 查詢不同，`cross_fields` 查詢是以詞為中心。

## 跨欄位

使用 `cross_fields` 查詢來跨多個欄位搜尋資料。例如，如果某個索引包含客戶資料，客戶的名字和姓氏會位於不同的欄位。然而，當您搜尋 `John Doe` 時，您會希望收到 `first_name` 欄位中有 `John` 且 `last_name` 欄位中有 `Doe` 的文件。

`most_fields` 查詢在此情況下無法運作，原因如下：

- [`operator` 與 `minimum_should_match`](#operator-and-minimum-should-match) 參數是以欄位為基礎套用，而非以詞為基礎。
- `first_name` 與 `last_name` 欄位中的詞頻可能導致非預期的結果。例如，如果某人的名字剛好是 `Doe`，則具有此名字的文件會被認為是更好的相符項目，因為這個名字不會出現在任何其他文件中。

`cross_fields` 查詢會將查詢字串分析成個別的詞，然後在任一欄位中搜尋每一個詞，就像它們是同一個欄位一樣。

以下是 `John Doe` 的 `cross_fields` 查詢：

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

回應中只包含同時具有 `John` 與 `Doe` 的那一份文件：

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
    "max_score": 0.8754687,
    "hits": [
      {
        "_index": "customers",
        "_id": "1",
        "_score": 0.8754687,
        "_source": {
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ]
  }
}
```

您可以使用 validate API 操作來深入了解上述查詢的執行方式：

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

從回應中可以看出，此查詢會在至少一個欄位中搜尋所有詞：

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

因此，混合所有欄位的詞頻可透過修正差異來解決詞頻不同的問題。

`cross_fields` 查詢通常只對 `boost` 為 1 的短字串欄位有用。在其他情況下，由於 boost、詞頻與長度正規化對分數的貢獻方式，分數無法產生有意義的詞統計混合。
{: .note}

`cross_fields` 查詢不支援 `fuzziness` 參數。
{: .note}

### 分析

`cross_fields` 查詢只有在具有相同分析器的欄位上才會以詞為中心的方式運作。具有相同分析器的欄位會群組在一起，而這些群組會以布林查詢合併。

例如，假設有一個索引，其中 `first_name` 與 `last_name` 欄位使用預設的 `standard`
 分析器進行分析，而其 `.edge` 子欄位使用 edge n-gram 分析器進行分析：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
PUT customers
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

</details>

您在 `customers` 索引中將一份文件編製索引：

```json
PUT /customers/_doc/1
{
  "first": "John",
  "last": "Doe"
}
```
{% include copy-curl.html %}

您可以使用 `cross_fields` 查詢來跨欄位搜尋 `John Doe`：

```json
GET /customers/_search
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

若要查看查詢的執行方式，您可以執行 Validate API：

```json
GET /customers/_validate/query?explain
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

回應顯示 `last_name` 與 `first_name` 欄位會群組在一起並視為單一欄位。同樣地，`last_name.edge` 與 `first_name.edge` 欄位也會群組在一起並視為單一欄位：

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
      "explanation": "(blended(terms:[last_name:john, first_name:john]) | (blended(terms:[last_name.edge:Jo, first_name.edge:Jo]) blended(terms:[last_name.edge:Joh, first_name.edge:Joh]) blended(terms:[last_name.edge:John, first_name.edge:John])))"
    }
  ]
}
```

將 `operator` 或 `minimum_should_match` 參數與上述的多個欄位群組搭配使用，可能會導致 [上一節](#operator-and-minimum-should-match) 所述的問題。若要避免此問題，您可以將上述查詢改寫為兩個以布林查詢合併的 `cross_fields` 子查詢，並將 `minimum_should_match` 套用至其中一個子查詢：

```json
GET /customers/_search
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

若要為所有欄位建立一個群組，請在查詢中指定分析器：

```json
GET customers/_search
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

對上述查詢執行 Validate API 可顯示查詢的執行方式：

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
      "explanation": "blended(terms:[last_name.edge:john, last_name:john, first_name:john, first_name.edge:john]) blended(terms:[last_name.edge:doe, last_name:doe, first_name:doe, first_name.edge:doe])"
    }
  ]
}
```

## 片語 

`phrase` 查詢的行為與 [`best_fields`](#best-fields) 查詢類似，但使用 `match_phrase` 查詢，而非 `match` 查詢。

以下是針對 [`best_fields`](#best-fields) 一節所述索引的 `phrase` 查詢範例：

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

上述查詢會以下列 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢的形式執行，每個欄位各使用一個 `match_phrase` 查詢：

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

由於 `phrase` 查詢預設只有在詞彙以相同順序出現時才會比對文字，因此結果只會傳回文件 1：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 3,
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
    "max_score": 0.84407747,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.84407747,
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

您可以使用 `slop` 參數，允許查詢片語中的字詞之間出現其他字詞。例如，以下查詢會將 `flourescent` 和 `therapy` 之間最多包含兩個字詞的文字視為相符：

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
  "took": 3,
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
    "max_score": 0.7003825,
    "hits": [
      {
        "_index": "articles",
        "_id": "2",
        "_score": 0.7003825,
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

當 `slop` 值小於 2 時，不會傳回任何文件。

`phrase` 查詢不支援 `fuzziness` 參數。
{: .note}

## 片語前綴 

`phrase_prefix` 查詢的行為與 [`phrase`](#phrase) 查詢類似，但使用 `match_phrase_prefix` 查詢，而非 `match_phrase` 查詢。

以下是針對 [`best_fields`](#best-fields) 一節所述索引的 `phrase_prefix` 查詢範例：

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

上述查詢會以下列 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢的形式執行，每個欄位各使用一個 `match_phrase_prefix` 查詢：

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

您可以使用 `slop` 參數，允許查詢片語中的字詞之間出現其他字詞。

`phrase_prefix` 查詢不支援 `fuzziness` 參數。
{: .note}

## 布林前綴 

`bool_prefix` 查詢對文件評分的方式與 [`most_fields`](#most-fields) 查詢類似，但使用 [`match_bool_prefix`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/) 查詢，而非 `match` 查詢。

以下是針對 [`best_fields`](#best-fields) 一節所述索引的 `bool_prefix` 查詢範例：

```json
GET articles/_search
{
  "query": {
    "multi_match" : {
      "query": "li northern",
      "type": "bool_prefix",
      "fields": [ "title", "description" ]
    }
  }
}
```
{% include copy-curl.html %}

上述查詢會以下列 [`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 查詢的形式執行，每個欄位各使用一個 `match_bool_prefix` 查詢：

```json
GET articles/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match_bool_prefix": { "title": "li northern" }},
        { "match_bool_prefix": { "description": "li northern" }}
      ]
    }
  }
}
```

用於建構詞彙查詢的詞彙支援 `fuzziness`、`prefix_length`、`max_expansions`、`fuzzy_rewrite` 和 `fuzzy_transpositions` 參數，但這些參數不會影響由最後一個詞彙建構的前綴查詢。
{: .note}

## 參數

此查詢接受下列參數。除了 `query` 之外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的查詢字串。必要。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否自動為多詞彙同義詞建立[片語比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。例如，若您將 `ba,batting average` 指定為同義詞並搜尋 `ba`，OpenSearch 會搜尋 `ba OR "batting average"`（若此選項為 `true`）或 `ba OR (batting AND average)`（若此選項為 `false`）。預設為 `true`。
`analyzer` | 字串 | 用於將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `default_field` 指定的索引時分析器。若未針對 `default_field` 指定分析器，則 `analyzer` 為索引的預設分析器。如需 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`boost` | 浮點數 | 依指定的乘數提高子句的權重。適合用來調整複合查詢中子句的權重。[0, 1) 範圍內的值會降低相關性，大於 1 的值則會提高相關性。預設為 `1`。
`fields` | 字串陣列 | 要搜尋的欄位清單。若您未提供 `fields` 參數，`multi_match` 查詢會搜尋 `index.query.default_field` 設定所指定的欄位，其預設為 `*`。 
`fuzziness` | 字串 | 判斷詞彙是否與某個值相符時，將一個字詞變更為另一個字詞所需的字元編輯次數（插入、刪除、替換）。例如，`wined` 與 `wind` 之間的距離為 1。有效值為非負整數或 `AUTO`。預設值 `AUTO` 會根據搜尋詞彙的長度動態選擇編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂門檻，其中 `low` 和 `high` 定義字元長度的界限。省略時，OpenSearch 使用 `AUTO:3,6` 作為預設值，並套用下列規則：<br>- 包含 0--2 個字元的詞彙：必須完全相符（0 次編輯）。<br>- 包含 3--5 個字元的詞彙：最多允許 1 次編輯。<br>- 包含 6 個以上字元的詞彙：最多允許 2 次編輯。<br>例如，`AUTO:4,7` 要求包含 0--3 個字元的詞彙完全相符，包含 4--6 個字元的詞彙最多允許 1 次編輯，包含 7 個以上字元的詞彙最多允許 2 次編輯。大多數情境建議使用 `AUTO`。`phrase`、`phrase_prefix` 和 `cross_fields` 查詢不支援此參數。
`fuzzy_rewrite` | 字串 | 決定 OpenSearch 如何改寫查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。若 `fuzziness` 參數不是 `0`，查詢預設會使用 `top_terms_blended_freqs_${max_expansions}` 作為 `fuzzy_rewrite` 方法。預設為 `constant_score`。 
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true`（預設）會在 `fuzziness` 選項的插入、刪除和替換操作之外，加入相鄰字元交換操作。例如，若 `fuzzy_transpositions` 為 true，`wind` 與 `wnid` 之間的距離為 1（交換「n」和「i」）；若為 false，距離則為 2（刪除「n」、插入「n」）。若 `fuzzy_transpositions` 為 false，`rewind` 和 `wnid` 與 `wind` 的距離相同（皆為 2），即使從人類的角度來看，`wnid` 是明顯的打字錯誤。預設值適合大多數使用案例。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，`"8.2"` 查詢字串可以與 `float` 類型的欄位相符。預設為 `false`。
`max_expansions` | 正整數 |  查詢可擴展出的詞彙數量上限。模糊查詢會「擴展為」多個相符詞彙，其距離在 `fuzziness` 指定的範圍內。接著 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`minimum_should_match` | 正整數或負整數、正百分比或負百分比、組合 | 若查詢字串包含多個搜尋詞彙，且您使用 `or` 運算子，此參數指定文件必須符合多少個詞彙，才會被視為相符。例如，若 `minimum_should_match` 為 2，`wind often rising` 不會與 `The Wind Rises.` 相符。若 `minimum_should_match` 為 `1`，則會相符。如需詳細資訊，請參閱[最低應符合數量]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`operator` | 字串 | 若查詢字串包含多個搜尋詞彙，此參數指定文件是否必須符合所有詞彙（`AND`），或只需符合一個詞彙（`OR`），才會被視為相符。有效值為：<br>- `OR`：字串 `to be` 會解讀為 `to OR be`<br>- `AND`：字串 `to be` 會解讀為 `to AND be`<br> 預設為 `OR`。
`prefix_length` | 非負整數 | 模糊比對時不納入考量的開頭字元數量。預設為 `0`。
`slop` | `0`（預設）或正整數 | 控制查詢中字詞的順序可以錯置到什麼程度，仍會被視為相符。[Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html#getSlop--) 說明：「查詢片語中的字詞之間允許出現的其他字詞數量。例如，交換兩個字詞的順序需要移動兩次（第一次移動會讓兩個字詞重疊），因此若要允許片語重新排序，slop 必須至少為 2。值為零時必須完全相符。」支援 `phrase` 和 `phrase_prefix` 查詢類型。
`tie_breaker` | 浮點數 | 介於 0 與 1.0 之間的係數，用於給予符合多個查詢子句的文件更高的權重。如需詳細資訊，請參閱 [`tie_breaker` 參數`](#the-tie_breaker-parameter)。
`type` | 字串 | 多重比對查詢類型。有效值為 `best_fields`、`most_fields`、`cross_fields`、`phrase`、`phrase_prefix`、`bool_prefix`。預設為 `best_fields`。
`zero_terms_query` | 字串 | 在某些情況下，分析器會移除查詢字串中的所有詞彙。例如，`stop` 分析器會移除字串 `an but this` 中的所有詞彙。在這些情況下，`zero_terms_query` 指定是否不與任何文件相符（`none`），或與所有文件相符（`all`）。有效值為 `none` 和 `all`。預設為 `none`。

`phrase`、`phrase_prefix` 和 `cross_fields` 查詢不支援 `fuzziness` 參數。
{: .note}

`slop` 參數僅支援 `phrase` 與 `phrase_prefix` 查詢。
{: .note}

### `tie_breaker` 參數

每個詞彙層級的混合查詢會以群組中任一欄位所傳回的最佳分數來計算文件分數。所有混合查詢的分數會相加，產生最終分數。您可以使用 `tie_breaker` 參數變更分數的計算方式。`tie_breaker` 參數接受下列值：

- 0.0（`best_fields`、`cross_fields`、`phrase` 與 `phrase_prefix` 查詢的預設值）：取群組中任一欄位所傳回的單一最佳分數。
- 1.0（`most_fields` 與 `bool_prefix` 查詢的預設值）：將群組中所有欄位的分數相加。
- (0, 1) 範圍內的浮點數值：取最佳符合欄位的單一最佳分數，並為其他所有符合的欄位加上（`tie_breaker` * `_score`）。