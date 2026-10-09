---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞組比對"
parent: Full-text queries
nav_order: 20
---

# 詞組比對查詢

使用 `match_phrase` 查詢來比對包含指定順序之確切詞組的文件。您可以提供 `slop` 參數，讓詞組比對更有彈性。

`match_phrase` 查詢會建立一個[詞組查詢](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html)，用來比對一連串的詞元。

下列範例顯示基本的 `match_phrase` 查詢：

```json
GET _search
{
  "query": {
    "match_phrase": {
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
    "match_phrase": {
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

舉例來說，假設某個索引含有下列文件：

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

下列 `match_phrase` 查詢會搜尋詞組 `wind rises`，其中 `wind` 這個字後面接著 `rises` 這個字：

```json
GET testindex/_search
{
  "query": {
    "match_phrase": {
      "title": "wind rises"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}


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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.92980814,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.92980814,
        "_source": {
          "title": "The wind rises"
        }
      }
    ]
  }
}
```
</details>

## 分析器

根據預設，當您對 `text` 欄位執行查詢時，搜尋文字會使用與該欄位相關聯的索引分析器進行分析。您可以在 `analyzer` 參數中指定不同的搜尋分析器。例如，下列查詢使用 `english` 分析器：

```json
GET testindex/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "the winds",
        "analyzer": "english"
      }
    }
  }
}
```
{% include copy-curl.html %}

`english` 分析器會移除停用詞 `the` 並執行詞幹擷取，產生詞元 `wind`。兩份文件都符合這個詞元，並會出現在結果中：

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
    "max_score": 0.19363807,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.19363807,
        "_source": {
          "title": "The wind rises"
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.17225474,
        "_source": {
          "title": "Gone with the wind"
        }
      }
    ]
  }
}
```
</details>

## Slop

如果您提供 `slop` 參數，查詢會容忍搜尋詞彙重新排序。Slop 會指定查詢詞組中允許的單字之間可插入多少個其他單字。例如，在下列查詢中，搜尋文字與文件文字相比經過重新排序：

```json
GET _search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "wind rises the",
        "slop": 3
      }
    }
  }
}
```

查詢仍會傳回相符的文件：

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
    "max_score": 0.44026947,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.44026947,
        "_source": {
          "title": "The wind rises"
        }
      }
    ]
  }
}
```
</details>

## 空查詢

如需可能出現空查詢的相關資訊，請參閱對應的 [match 查詢小節]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/#empty-query)。

## 參數

此查詢接受欄位名稱 (`<field>`) 作為最上層參數：

```json
GET _search
{
  "query": {
    "match_phrase": {
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
`query` | 字串 | 要用於搜尋的查詢字串。必要。
`analyzer` | 字串 | 用來將查詢字串文字斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設是為 `default_field` 指定的索引時間分析器。如果沒有為 `default_field` 指定分析器，則 `analyzer` 是索引的預設分析器。如需 `index.query.default_field` 的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`slop` | `0` (預設) 或正整數 | 控制查詢中的單字可以錯序到什麼程度仍被視為相符。根據 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html#getSlop--)：「查詢詞組中允許的單字之間可插入多少個其他單字。例如，要交換兩個單字的順序需要移動兩次 (第一次移動會將兩個單字放在彼此上方)，因此若要允許詞組重新排序，slop 至少必須為二。值為零則要求完全相符。」
`zero_terms_query` | 字串 | 在某些情況下，分析器會從查詢字串中移除所有詞彙。例如，`stop` 分析器會從字串 `an but this` 中移除所有詞彙。在這些情況下，`zero_terms_query` 會指定要比對沒有文件 (`none`) 還是所有文件 (`all`)。有效值為 `none` 和 `all`。預設為 `none`。