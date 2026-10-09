---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "片語字首比對"
parent: Full-text queries
nav_order: 30
---

# 片語字首比對查詢

使用 `match_phrase_prefix` 查詢來指定要依序比對的片語。包含您所指定片語的文件將會被傳回。片語中最後一個不完整的詞彙會被解讀為字首，因此任何包含以該片語及最後一個詞彙字首開頭之片語的文件都會被傳回。

類似於 [片語比對]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)，但會以查詢字串中的最後一個詞彙建立 [字首查詢](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PrefixQuery.html)。

如需 `match_phrase_prefix` 與 `match_bool_prefix` 查詢之間的差異，請參閱 [`match_bool_prefix` 與 `match_phrase_prefix` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/#the-match_bool_prefix-and-match_phrase_prefix-queries)。

下列範例顯示基本的 `match_phrase_prefix` 查詢：

```json
GET _search
{
  "query": {
    "match_phrase_prefix": {
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
    "match_phrase_prefix": {
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

例如，考慮一個包含下列文件的索引：

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

下列 `match_phrase_prefix` 查詢搜尋完整單字 `wind`，其後接一個以 `ri` 開頭的單字：

```json
GET testindex/_search
{
  "query": {
    "match_phrase_prefix": {
      "title": "wind ri"
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 6,
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

## 參數

此查詢接受欄位名稱（`<field>`）作為頂層參數：

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

`<field>` 接受下列參數。除 `query` 以外的所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 用於搜尋的查詢字串。必要。
`analyzer` | 字串 | 用於對查詢進行斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。
`max_expansions` | 正整數 | 查詢可擴充至的最大詞彙數。模糊查詢會「擴充至」多個在 `fuzziness` 所指定距離內的符合詞彙，然後 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`slop` | `0`（預設）或正整數 | 控制查詢中的單字可以錯序到何種程度仍被視為符合。引自 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html#getSlop--)：「查詢片語中的字詞之間允許出現的其他字詞數量。例如，交換兩個字詞的順序需要移動兩次（第一次移動會使兩個字詞重疊），因此若要允許片語重新排序，slop 至少須為 2。值為 0 時則須完全相符。」