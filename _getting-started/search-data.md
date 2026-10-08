---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋您的資料"
nav_order: 50
description: "了解 OpenSearch 中可用的查詢語言，並開始使用查詢字串查詢和查詢領域特定語言 (DSL) 搜尋資料。"
---

# 搜尋您的資料

OpenSearch 搜尋建立在[查詢領域特定語言 (DSL)]({{site.url}}{{site.baseurl}}/query-dsl/index/) 之上。這是 OpenSearch 的主要查詢語言，可用來建立複雜且可完全自訂的查詢。另一種選擇是[查詢字串查詢語言]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)，這是一種精簡的語言，可在搜尋請求的查詢參數中使用。本教學簡要介紹如何使用[查詢字串查詢](#query-string-queries)和 [Query DSL](#query-dsl) 進行搜尋。範例會查詢您在[將資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/) 中建立的 `students` 索引。

本教學中的搜尋會將查詢中的文字與文件中儲存的文字進行比對。OpenSearch 也支援向量搜尋，比對的是語意而非確切的字詞。如需詳細資訊，請參閱[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)。

## 擷取索引中的所有文件

若要擷取索引中的所有文件，請傳送下列請求：

```json
GET /students/_search
```
{% include copy-curl.html %}

上述請求等同於 `match_all` 查詢，會比對索引中的所有文件：

```json
GET /students/_search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回相符的文件：

```json
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      },
      {
        "_index": "students",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Jonathan Powers",
          "gpa": 3.85,
          "grad_year": 2025
        }
      },
      {
        "_index": "students",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Jane Doe",
          "gpa": 3.52,
          "grad_year": 2024
        }
      }
    ]
  }
}
```

## 回應本文欄位

上述回應包含下列欄位。

<!-- vale off -->
### took
<!-- vale on -->

`took` 欄位包含執行查詢所花費的時間，以毫秒為單位。

<!-- vale off -->
### timed_out
<!-- vale on -->

此欄位表示請求是否逾時。如果請求逾時，OpenSearch 會傳回逾時前已收集到的結果。您可以提供 `timeout` 查詢參數來設定所需的逾時值：

```json
GET /students/_search?timeout=20ms
```
{% include copy-curl.html %}

<!-- vale off -->
### _shards
<!-- vale on -->

`_shards` 物件會指出執行查詢的分片總數，以及成功或失敗的分片數。如果分片本身及其所有副本都無法使用，該分片就可能失敗。如果任何相關分片失敗，OpenSearch 會繼續在其餘分片上執行查詢。

<!-- vale off -->
### hits
<!-- vale on -->

`hits` 物件包含相符文件的總數以及文件本身（列於 `hits` 陣列中）。每份相符文件都包含 `_index` 和 `_id` 欄位，以及 `_source` 欄位，後者包含最初編製索引的完整文件。

每份文件都會在 `_score` 欄位中獲得一個相關性分數。由於您執行的是 `match_all` 搜尋，所有文件的分數都設為 `1`（它們的相關性沒有差異）。`max_score` 欄位包含所有相符文件中的最高分數。

## 查詢字串查詢

您可以將查詢字串查詢作為 `q` 查詢參數傳送。例如，下列查詢會搜尋名稱為 `john` 的學生：

```json
GET /students/_search?q=name:john
```
{% include copy-curl.html %}

OpenSearch 會傳回相符的文件：

```json
{
  "took": 18,
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
    "max_score": 0.44583148,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.44583148,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

如需查詢字串語法的詳細資訊，請參閱[查詢字串查詢語言]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。

## Query DSL

使用 Query DSL，您可以建立更複雜且自訂的查詢。

### 全文搜尋

您可以對對應為 `text` 的欄位執行全文搜尋。根據預設，文字欄位會由 `default` 分析器進行分析。分析器會將文字分割為詞彙，並將其轉換為小寫。如需 OpenSearch 分析器的詳細資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/)。

若要查看 OpenSearch 為某個欄位儲存的詞彙，請使用 Analyze API。下列請求會使用為 `name` 欄位設定的分析器來分析文字 `John Doe`：

```json
GET /students/_analyze
{
  "field": "name",
  "text": "John Doe"
}
```
{% include copy-curl.html %}

回應中的每個詞彙各對應一個詞元：

```json
{
  "tokens": [
    {
      "token": "john",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "doe",
      "start_offset": 5,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

OpenSearch 會儲存詞彙 `john` 和 `doe`，兩者皆為小寫。`match` 查詢會以相同方式分析查詢文字，因此 `John`、`john` 和 `JOHN` 都會產生詞彙 `john`，並與此文件相符。

例如，下列查詢會搜尋名稱為 `john` 的學生：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name": "john"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

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
    "max_score": 0.44583148,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.44583148,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

請注意，查詢文字是小寫，而欄位中的文字不是，但查詢仍會傳回相符的文件。

您可以重新排列搜尋字串中詞彙的順序。例如，下列查詢會搜尋 `doe john`：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name": "doe john"
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩份相符的文件：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.6594695,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.6594695,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      },
      {
        "_index": "students",
        "_id": "3",
        "_score": 0.21363801,
        "_source": {
          "name": "Jane Doe",
          "gpa": 3.52,
          "grad_year": 2024
        }
      }
    ]
  }
}
```

match 查詢類型預設使用 `OR` 作為運算子，因此此查詢在功能上等同於 `doe OR john`。`John Doe` 和 `Jane Doe` 都比對到字詞 `doe`，但 `John Doe` 的分數較高，因為它也比對到 `john`。如需 OpenSearch 如何計算這些分數的說明，請參閱[相關性]({{site.url}}{{site.baseurl}}/getting-started/intro/#relevance)。

### 要求每個詞彙都必須相符

若只要傳回包含所有查詢詞彙的文件，請將 `operator` 設為 `and`：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name": {
        "query": "doe john",
        "operator": "and"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應只包含 `John Doe`，也就是同時包含這兩個詞彙的唯一一份文件：

```json
{
  "took": 0,
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
    "max_score": 0.6594695,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.6594695,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

### 比對片語

`match` 查詢會忽略詞彙的順序。若要求詞彙必須相鄰且依照指定的順序出現，請使用 `match_phrase` 查詢：

```json
GET /students/_search
{
  "query": {
    "match_phrase": {
      "name": "john doe"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

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
    "max_score": 0.6594694,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.6594694,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

使用相同的查詢搜尋 `doe john` 不會傳回任何結果，因為這些詞彙在欄位中是以相反的順序出現。

如需詳細資訊，請參閱[比對片語查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。

### 比對拼錯的字詞

到目前為止的查詢，都要求查詢詞彙與儲存的詞彙完全相符。即使索引中包含 `john`，搜尋 `jhon` 仍不會傳回任何結果：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name": "jhon"
    }
  }
}
```
{% include copy-curl.html %}

若要比對拼法相近的詞彙，請將 `fuzziness` 設為 OpenSearch 在尋找相符項目時，可對查詢詞彙進行的單一字元變更次數。一次變更是指插入、刪除、替換一個字元，或對調兩個相鄰的字元。這個數字稱為「_編輯距離_」。將 `jhon` 變成 `john` 需要對調 `h` 與 `o`，因此編輯距離為 `1` 就已足夠：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name": {
        "query": "jhon",
        "fuzziness": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件。由於 OpenSearch 會對模糊比對結果降低評分，因此其分數會低於完全符合 `john` 時的分數：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.3343736,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 0.3343736,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

將 `fuzziness` 設為 `AUTO`，可讓 OpenSearch 根據查詢詞彙的長度選擇編輯距離，以避免比對到不相關的短字詞。如需詳細資訊，請參閱[模糊度]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/#fuzziness)。

### 關鍵字搜尋

由於[匯入資料]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)中的大量請求讓 OpenSearch 自行推斷欄位類型，因此 `name` 欄位包含一個由 OpenSearch 自動新增的 `name.keyword` 子欄位。請試著以類似前一個請求的方式搜尋 `name.keyword` 欄位：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name.keyword": "john"
    }
  }
}
```
{% include copy-curl.html %}

此請求不會傳回任何結果，因為 `keyword` 欄位必須完全相符。

現在請搜尋確切的文字 `John Doe`：

```json
GET /students/_search
{
  "query": {
    "match": {
      "name.keyword": "John Doe"
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回相符的文件：

```json
{
  "took": 0,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

### 篩選條件

使用布林值查詢時，您可以針對具有確切值的欄位，在查詢中加入篩選子句。

詞彙篩選條件會比對特定詞彙。例如，下列布林值查詢會搜尋畢業年份為 2022 年的學生：

```json
GET /students/_search
{
  "query": { 
    "bool": { 
      "filter": [ 
        { "term":  { "grad_year": 2022 }}
      ]
    }
  }
}
```
{% include copy-curl.html %}

使用範圍篩選條件，您可以指定值的範圍。例如，下列布林值查詢會搜尋 GPA 大於 3.6 的學生：

```json
GET /students/_search
{
  "query": { 
    "bool": { 
      "filter": [ 
        { "range": { "gpa": { "gt": 3.6 }}}
      ]
    }
  }
}
```
{% include copy-curl.html %}

如需篩選條件的詳細資訊，請參閱[查詢與篩選內容]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)。

### 複合查詢

複合查詢可讓您結合多個查詢或篩選子句。布林值查詢就是複合查詢的一個範例。

例如，若要搜尋名稱符合 `doe` 的學生，並依畢業年份和 GPA 進行篩選，請使用下列請求：

```json
GET /students/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "name": "doe"
          }
        },
        { "range": { "gpa": { "gte": 3.6, "lte": 3.9 } } },
        { "term":  { "grad_year": 2022 }}
      ]
    }
  }
}
```
{% include copy-curl.html %}

如需布林值查詢及其他複合查詢的詳細資訊，請參閱[複合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/index/)。

## 其他查詢語言

除了 Query DSL 和查詢字串查詢之外，OpenSearch 還支援下列查詢語言：

- [SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql/index/)：一種傳統的查詢語言，可銜接傳統關聯式資料庫概念與 OpenSearch 以文件為導向的資料儲存空間所具備的彈性。
- [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/)：OpenSearch 中用於可觀測性的主要語言。PPL 使用管道語法，將多個命令串連成一個查詢。
- [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/dql/)：一種以文字為基礎的查詢語言，用於在 OpenSearch Dashboards 中篩選資料。

## 搜尋方法

除了本教學所述的傳統全文搜尋之外，OpenSearch 還支援多種由機器學習 (ML) 驅動的搜尋方法，包括向量搜尋，以及由 AI 驅動的搜尋，例如語意搜尋、多模態搜尋、稀疏搜尋、混合搜尋和對話式搜尋。如需 OpenSearch 支援的所有搜尋方法的相關資訊，請參閱[搜尋]({{site.url}}{{site.baseurl}}/search-plugins/)。

## 延伸閱讀

- 如需可用查詢類型的相關資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/index/)。
- 如需可用搜尋方法的相關資訊，請參閱[搜尋]({{site.url}}{{site.baseurl}}/search-plugins/)。
- 如需向量搜尋的相關資訊，請參閱[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)。

## 後續步驟

- 若要載入較大的範例資料集並加以摘要，請參閱[分析您的資料]({{site.url}}{{site.baseurl}}/getting-started/analyze-data/)。
