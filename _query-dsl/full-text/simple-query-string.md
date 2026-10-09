---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "簡易查詢字串"
parent: Full-text queries
nav_order: 70
---

# Simple query string 查詢

使用 `simple_query_string` 類型，直接在查詢字串中指定多個以正規表示式分隔的引數。Simple query string 的語法比 query string 寬鬆，因為它會捨棄字串中任何無效的部分，且不會因語法無效而回傳錯誤。

此查詢使用[簡單語法](#simple-query-string-syntax)，根據特殊運算子剖析查詢字串，並將字串拆分為詞元。剖析之後，查詢會獨立分析每個詞元，然後回傳符合的文件。

以下查詢對 `title` 欄位執行模糊搜尋：

```json
GET _search
{
  "query": {
    "simple_query_string": {
      "query": "\"rises wind the\"~4 | *ising~2",
      "fields": ["title"]
    }
  }
}
```
{% include copy-curl.html %}

## Simple query string 語法

查詢字串由 _詞元_ 和 _運算子_ 組成。詞元是單一單字（例如，在查詢 `wind rises` 中，詞元為 `wind` 和 `rises`）。如果多個詞元被引號包圍，則視為一個片語，其中的單字會依出現順序進行比對（例如 `"wind rises"`）。`+`、`|` 和 `-` 等運算子指定用來解讀查詢字串中文字的布林邏輯。

## 運算子

簡易查詢字串語法支援下列運算子。

運算子 | 說明
:--- | :---
`+` | 作為 `AND` 運算子。
`|` | 作為 `OR` 運算子。
`*` | 用於詞元結尾時，表示前綴查詢。
`"` | 將多個詞元包裝成片語（例如 `"wind rises"`）。
`(`, `)` | 為優先順序包裝子句（例如 `wind + (rises | rising)`）。
`~n` | 用於詞元之後（例如 `wnid~3`）時，設定 `fuzziness`。用於片語之後時，設定 `slop`。 
`-` | 否定該詞元。

上述所有運算子都是保留字元。若要將它們當作原始字元而非運算子使用，請以反斜線逸出其中任何字元。傳送 JSON 請求時，請使用 `\\` 來逸出保留字元（因為反斜線字元本身也是保留字元，您必須用另一個反斜線來逸出反斜線）。

## 預設運算子

預設運算子為 `OR`（除非您將 `default_operator` 設定為 `AND`）。預設運算子決定整體查詢行為。例如，考慮一個包含下列文件的索引：

```json
PUT /customers/_doc/1
{
  "first_name":"Amber",
  "last_name":"Duke",
  "address":"880 Holmes Lane"
}
```
{% include copy-curl.html %}

```json
PUT /customers/_doc/2
{
  "first_name":"Hattie",
  "last_name":"Bond",
  "address":"671 Bristol Street"
}
```
{% include copy-curl.html %}

```json
PUT /customers/_doc/3
{
  "first_name":"Nanette",
  "last_name":"Bates",
  "address":"789 Madison St"
}
```
{% include copy-curl.html %}

```json
PUT /customers/_doc/4
{
  "first_name":"Dale",
  "last_name":"Amber",
  "address":"467 Hutchinson Court"
}
```
{% include copy-curl.html %}

以下查詢嘗試尋找 address 包含 `street` 或 `st` 這些單字、且不包含 `madison` 這個單字的文件：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string": {
      "fields": [ "address" ],
      "query": "street st -madison"
    }
  }
}

```
{% include copy-curl.html %}

然而，結果不僅包含預期的文件，還包含全部四份文件：

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
      "value": 4,
      "relation": "eq"
    },
    "max_score": 2.2039728,
    "hits": [
      {
        "_index": "customers",
        "_id": "2",
        "_score": 2.2039728,
        "_source": {
          "first_name": "Hattie",
          "last_name": "Bond",
          "address": "671 Bristol Street"
        }
      },
      {
        "_index": "customers",
        "_id": "3",
        "_score": 1.2039728,
        "_source": {
          "first_name": "Nanette",
          "last_name": "Bates",
          "address": "789 Madison St"
        }
      },
      {
        "_index": "customers",
        "_id": "1",
        "_score": 1,
        "_source": {
          "first_name": "Amber",
          "last_name": "Duke",
          "address": "880 Holmes Lane"
        }
      },
      {
        "_index": "customers",
        "_id": "4",
        "_score": 1,
        "_source": {
          "first_name": "Dale",
          "last_name": "Amber",
          "address": "467 Hutchinson Court"
        }
      }
    ]
  }
}
```
</details>

因為預設運算子是 `OR`，此查詢會包含包含 `street` 或 `st` 這些單字的文件（文件 2 和 3），以及不包含 `madison` 這個單字的文件（文件 1 和 4）。

若要正確表達查詢意圖，請在 `-madison` 前面加上 `+`：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string": {
      "fields": [ "address" ],
      "query": "street st +-madison"
    }
  }
}
```
{% include copy-curl.html %}

或者，將 `AND` 指定為預設運算子，並對 `street` 和 `st` 這兩個單字使用邏輯或運算：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string": {
      "fields": [ "address" ],
      "query": "st|street -madison",
      "default_operator": "AND"
    }
  }
}
```
{% include copy-curl.html %}

上述查詢回傳文件 2：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 2.2039728,
    "hits": [
      {
        "_index": "customers",
        "_id": "2",
        "_score": 2.2039728,
        "_source": {
          "first_name": "Hattie",
          "last_name": "Bond",
          "address": "671 Bristol Street"
        }
      }
    ]
  }
}
```
</details>

## 限制運算子

若要限制簡易查詢字串剖析器支援的運算子，請在 `flags` 參數中包含您想要支援的運算子，並以 `|` 分隔。例如，以下查詢僅啟用 `OR`、`AND` 和 `FUZZY` 運算子：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string": {
      "fields": [ "address" ],
      "query": "bristol | madison +stre~2",
      "flags": "OR|AND|FUZZY"
    }
  }
}
```
{% include copy-curl.html %}

下表列出所有可用的運算子旗標。

旗標 | 說明
:--- | :--- 
`ALL`（預設） | 啟用所有運算子。 
`AND` | 啟用 `+`（`AND`）運算子。 
`ESCAPE` | 啟用 `\` 作為逸出字元。 
`FUZZY` | 在單字之後啟用 `~n` 運算子，其中 `n` 是表示比對允許編輯距離的整數。
`NEAR` | 在片語之後啟用 `~n` 運算子，其中 `n` 是比對詞元之間允許的最大位置數。等同於 `SLOP`。 
`NONE` | 停用所有運算子。 
`NOT` | 啟用 `-`（`NOT`）運算子。 
`OR` | 啟用 `|`（`OR`）運算子。 
`PHRASE` | 啟用 `"`（引號）用於片語搜尋。 
`PRECEDENCE` | 啟用 `(` 和 `)`（括號）運算子以進行運算子優先順序處理。 
`PREFIX` | 啟用 `*`（前綴）運算子。 
`SLOP` | 在片語之後啟用 `~n` 運算子，其中 `n` 是比對詞元之間允許的最大位置數。等同於 `NEAR`。 
`WHITESPACE` | 啟用空白字元作為文字分割的依據。 

## 萬用字元運算式

您可以使用 `*` 特殊字元指定萬用字元運算式，該字元會取代零個或多個字元。例如，下列查詢會搜尋所有以 `name` 結尾的欄位：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string" : {
      "query":    "Amber Bond",
      "fields": [ "*name" ] 
    }
  }
}
```
{% include copy-curl.html %}

## 提升

使用插入號 (`^`) 提升運算子，以乘數提升欄位的相關性分數。值在 [0, 1) 範圍內會降低相關性，而大於 1 的值會提高相關性。預設為 `1`。

例如，下列查詢會搜尋 `first_name` 和 `last_name` 欄位，並將 `first_name` 欄位的相符項目提升 2 倍：

```json
GET /customers/_search
{
  "query": {
    "simple_query_string" : {
      "query":    "Amber",
      "fields": [ "first_name^2", "last_name" ] 
    }
  }
}
```
{% include copy-curl.html %}

## 多重位置詞元

對於多重位置詞元，簡易查詢字串會建立 [match phrase 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。因此，如果您將 `ml, machine learning` 指定為同義字並搜尋 `ml`，OpenSearch 會搜尋 `ml OR "machine learning"`。 

或者，您可以使用 AND 運算來比對多重位置詞元。如果您將 `auto_generate_synonyms_phrase_query` 設為 `false`，OpenSearch 會搜尋 `ml OR (machine AND learning)`。 

例如，下列查詢會搜尋文字 `ml models`，並指定不要為每個同義字自動產生 match phrase 查詢：

```json
GET /testindex/_search
{
  "query": {
    "simple_query_string": {
      "fields": ["title"],
      "query": "ml models",
      "auto_generate_synonyms_phrase_query": false
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`(ml OR (machine AND learning)) models`。

## 參數

下表列出 `simple_query_string` 查詢支援的最上層參數。除了 `query` 之外，所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query`| 字串 | 可能包含 [simple query string 語法](#simple-query-string-syntax) 運算式以供搜尋的文字。必要。
`analyze_wildcard` | 布林值 | 指定 OpenSearch 是否應嘗試分析萬用字元詞彙。預設為 `false`。
`analyzer` | 字串 | 用來將查詢字串文字斷詞的分析器。預設為針對 `default_field` 指定的索引時間分析器。如果未針對 `default_field` 指定分析器，則 `analyzer` 是索引的預設分析器。如需 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否要為多重詞彙同義字自動建立 [match_phrase 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)。預設為 `true`。
`default_operator`| 字串 | 如果查詢字串包含多個搜尋詞彙，文件必須符合所有詞彙 (`AND`) 或只需符合一個詞彙 (`OR`) 才視為相符。有效值為：<br>- `OR`：字串 `to be` 會解讀為 `to OR be`<br>- `AND`：字串 `to be` 會解讀為 `to AND be`<br> 預設為 `OR`。
`fields` | 字串陣列 | 要搜尋的欄位清單 (例如 `"fields": ["title^4", "description"]`)。支援萬用字元。您可以使用插入號 (`^`) 標記法，提升特定欄位中相符項目的相關性。如果未指定，查詢會預設為 `index.query.default_field` 設定，其預設為 `["*"]` (包含所有符合詞彙查詢資格的欄位，並篩除中繼資料欄位)。您可以覆寫索引設定，或在查詢中明確設定 `default_field`。例如，若要傳回所有標題，請設定 `"default_field": "title"`。一次可搜尋的欄位數上限由 `indices.query.bool.max_clause_count` 定義，其預設為 1,024。
`flags` | 字串 | 以 `|` 分隔的[旗標](#limit-operators)字串，用於啟用 (例如 `AND|OR|NOT`)。預設為 `ALL`。
`fuzzy_max_expansions` | 正整數 | 查詢可擴充的詞彙數上限。模糊查詢會「擴充」為若干符合的詞彙，這些詞彙位於 `fuzziness` 中指定的距離內。接著 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true` (預設) 會將相鄰字元互換加入 `fuzziness` 選項的插入、刪除和取代作業。例如，如果 `fuzzy_transpositions` 為 true，則 `wind` 與 `wnid` 之間的距離為 1 (互換「n」和「i」)；如果為 false，則距離為 2 (刪除「n」、插入「n」)。如果 `fuzzy_transpositions` 為 false，則 `rewind` 和 `wnid` 與 `wind` 的距離相同 (2)，儘管以人為本的觀點認為 `wnid` 是明顯的打字錯誤。預設值對大多數使用案例而言是很好的選擇。
`fuzzy_prefix_length`| 整數 | 模糊比對時保持不變的開頭字元數。預設為 0。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，查詢字串 `"8.2"` 可能符合類型為 `float` 的欄位。預設為 `false`。
`minimum_should_match` | 正整數或負整數、正百分比或負百分比、組合 | 如果查詢字串包含多個搜尋詞彙，且您使用 `or` 運算子，則文件必須符合的詞彙數才視為相符。例如，如果 `minimum_should_match` 為 2，則 `wind often rising` 不符合 `The Wind Rises.`。如果 `minimum_should_match` 為 `1`，則會相符。如需詳細資訊，請參閱[最少應符合]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`quote_field_suffix` | 字串 | 此選項支援使用與非完全相符不同的分析方法，搜尋完全相符 (以引號括住)。例如，如果 `quote_field_suffix` 為 `.exact`，且您在 `title` 欄位中搜尋 `\"lightly\"`，OpenSearch 會在 `title.exact` 欄位中搜尋 `lightly` 這個字。第二個欄位可能使用不同的類型 (例如 `keyword` 而非 `text`) 或不同的分析器。
