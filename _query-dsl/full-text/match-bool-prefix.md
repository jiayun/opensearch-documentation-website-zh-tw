---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "布林前綴比對"
parent: Full-text queries
nav_order: 40
---

# 布林前綴比對查詢

`match_bool_prefix` 查詢會分析提供的搜尋字串，並根據字串中的詞元建立[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)。它會將除了最後一個詞元以外的每個詞元都當作完整單字來比對。最後一個詞元則作為前綴使用。`match_bool_prefix` 查詢會傳回包含完整單字詞元或以該前綴開頭之詞元的文件，順序不拘。

下列範例顯示基本的 `match_bool_prefix` 查詢：

```json
GET _search
{
  "query": {
    "match_bool_prefix": {
      "title": "the wind"
    }
  }
}
```
{% include copy-curl.html %}

若要傳遞其他參數，您可以使用擴充語法：

```json
GET _search
{
  "query": {
    "match_bool_prefix": {
      "title": {
        "query": "the wind",
        "analyzer": "stop"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例

舉例來說，假設某個索引包含下列文件：

```json
PUT testindex/_doc/1
{
  "title": "The wind rises"
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

下列 `match_bool_prefix` 查詢會搜尋完整單字 `rises` 以及以 `wi` 開頭的單字，順序不拘：

```json
GET testindex/_search
{
  "query": {
    "match_bool_prefix": {
      "title": "rises wi"
    }
  }
}
```
{% include copy-curl.html %}

上述查詢等同於下列布林查詢：

```json
GET testindex/_search
{
  "query": {
    "bool" : {
      "should": [
        { "term": { "title": "rises" }},
        { "prefix": { "title": "wi"}}
      ]
    }
  }
}
```

回應會包含這兩份文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 15,
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
    "max_score": 1.73617,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 1.73617,
        "_source": {
          "title": "The wind rises"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Gone with the wind"
        }
      }
    ]
  }
}
```

</details>

## `match_bool_prefix` 與 `match_phrase_prefix` 查詢

`match_bool_prefix` 查詢會比對任何位置的詞元，而 `match_phrase_prefix` 查詢則會將詞元比對為完整詞組。為了說明差異，再次以上一節的 `match_bool_prefix` 查詢為例：

```json
GET testindex/_search
{
  "query": {
    "match_bool_prefix": {
      "title": "rises wi"
    }
  }
}
```
{% include copy-curl.html %}

`The wind rises` 與 `Gone with the wind` 都符合搜尋詞元，因此查詢會傳回這兩份文件。

現在對同一個索引執行 `match_phrase_prefix` 查詢：

```json
GET testindex/_search
{
  "query": {
    "match_phrase_prefix": {
      "title": "rises wi"
    }
  }
}
```
{% include copy-curl.html %}

回應不會傳回任何文件，因為沒有任何文件包含依指定順序排列的 `rises wi` 詞組。

## 分析器

根據預設，當您對 `text` 欄位執行查詢時，搜尋文字會使用與該欄位相關聯的索引分析器進行分析。您可以在 `analyzer` 參數中指定不同的搜尋分析器：

```json
GET testindex/_search
{
  "query": {
    "match_bool_prefix": {
      "title": {
        "query": "rise the wi",
        "analyzer": "stop"
      }
    }
  }
}
```
{% include copy-curl.html %}
 
## 參數

此查詢接受欄位名稱（`<field>`）作為最上層參數：

```json
GET _search
{
  "query": {
    "match_bool_prefix": {
      "<field>": {
        "query": "text to search for",
        ... 
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `query` 之外，所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的文字、數字、布林值或日期。必要。
`analyzer` | 字串 | 用來將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設是為 `default_field` 指定的索引時分析器。如果沒有為 `default_field` 指定分析器，則 `analyzer` 是索引的預設分析器。如需 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`fuzziness` | `AUTO`、`0` 或正整數 | 比對每個詞元（最後一個詞元除外）時允許的最大編輯次數，指定為 `0`、`1`、`2`、`AUTO` 或 `AUTO:<low>,<high>`。若未指定，詞元必須完全相符。如需詳細資訊，請參閱[模糊比對]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)。
`fuzzy_rewrite` | 字串 | 決定 OpenSearch 如何重寫查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 及 `top_terms_blended_freqs_N`。如果 `fuzziness` 參數不是 `0`，查詢預設會使用 `top_terms_blended_freqs_${max_expansions}` 的 `fuzzy_rewrite` 方法。預設為 `constant_score`。
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true`（預設）會將相鄰字元互換加入 `fuzziness` 選項的插入、刪除及取代操作。例如，如果 `fuzzy_transpositions` 為 true，`wind` 與 `wnid` 之間的距離為 1（互換「n」和「i」）；如果為 false，則距離為 2（刪除「n」、插入「n」）。如果 `fuzzy_transpositions` 為 false，則 `rewind` 和 `wnid` 與 `wind` 的距離相同（2），儘管以人為中心的觀點認為 `wnid` 是明顯的打字錯誤。預設值對大多數使用案例而言是很好的選擇。
`max_expansions` | 正整數 | 查詢可擴充至的最大詞元數。模糊查詢會「擴充至」一定數量的相符詞元，這些詞元位於 `fuzziness` 中指定的距離內。接著 OpenSearch 會嘗試比對這些詞元。預設為 `50`。
`minimum_should_match` | 正或負整數、正或負百分比、組合 | 如果查詢字串包含多個搜尋詞元，且您使用 `or` 運算子，則文件必須符合的詞元數才會被視為相符。例如，如果 `minimum_should_match` 為 2，則 `wind often rising` 不符合 `The Wind Rises.`。如果 `minimum_should_match` 為 `1`，則符合。如需詳細資訊，請參閱[最少應符合數]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`operator` | 字串 | 如果查詢字串包含多個搜尋詞元，文件必須所有詞元都符合（`and`）或只要有一個詞元符合（`or`）才被視為相符。有效值為 `or` 及 `and`。預設為 `or`。
`prefix_length` | 非負整數 | 在模糊比對中不列入考量的前置字元數。預設為 `0`。

`fuzziness`、`fuzzy_transpositions`、`fuzzy_rewrite`、`max_expansions` 及 `prefix_length` 參數可套用至為所有詞元（最後一個詞元除外）建構的詞元子查詢。它們對為最後一個詞元建構的前綴查詢沒有任何影響。
{: .note}