---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "片語前綴比對"
parent: Full-text queries
nav_order: 30
---

# 片語前綴比對查詢

使用 `match_phrase_prefix` 查詢來搜尋包含指定片語詞元的文件，且詞元順序須與您指定的順序一致。片語中的最後一個詞元會解讀為前綴，因此查詢會比對任何以前面詞元開頭、並接續以最後一個詞元開頭之詞彙的片語。例如，`chocolate chip c` 會比對 `chocolate chip cookies` 和 `mint chocolate chip cake`，但不會比對 `cookies with chocolate chip`。

`match_phrase_prefix` 查詢的運作方式與[片語比對]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)查詢類似，但會針對查詢字串中的最後一個詞元建立[前綴查詢](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PrefixQuery.html)。若查詢字串只包含一個詞元，則該查詢即為該詞元的前綴查詢。

在下列情境中使用 `match_phrase_prefix` 查詢：

- 在只知道最後一個字開頭的情況下，尋找包含已知片語的文件。
- 在不變更對應的情況下，為文字欄位新增基本的隨打即搜功能。

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

例如，假設有一個索引包含下列文件：

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

下列 `match_phrase_prefix` 查詢會搜尋完整詞彙 `wind`，其後接續以 `ri` 開頭的詞彙：

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

回應包含相符的文件：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.42264006,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.42264006,
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

此查詢接受欄位名稱 (`<field>`) 作為最上層參數：

```json
GET _search
{
  "query": {
    "match_phrase_prefix": {
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
`query` | 字串 | 用於搜尋的查詢字串。OpenSearch 會將查詢字串分析為詞元，並將最後一個詞元視為前綴。必要。
`analyzer` | 字串 | 用於將查詢字串斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為 `<field>` 所對應的搜尋分析器。若未對應任何分析器，則使用索引的預設分析器。
`max_expansions` | 正整數 | 查詢字串中最後一個詞元可擴充的詞元數上限。如需詳細資訊，請參閱[使用片語前綴比對查詢進行自動完成](#using-the-match-phrase-prefix-query-for-autocomplete)。預設為 `50`。
`slop` | `0` (預設) 或正整數 | 控制查詢中的詞彙可容許錯位的程度，且仍視為相符。根據 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/PhraseQuery.html#getSlop--)：「查詢片語中詞彙之間允許出現的其他詞彙數。例如，若要調換兩個詞彙的順序需要兩次移動 (第一次移動會將兩個詞彙疊在一起)，因此若要允許片語重新排序，slop 至少須為二。值為零時要求完全相符。」例如，查詢 `wind the` 只有在 `slop` 至少為 `2` 時，才會比對標題 `Gone with the wind`。
`zero_terms_query` | 字串 | 在某些情況下，分析器會移除查詢字串中的所有詞元。例如，`stop` 分析器會移除字串 `the` 中的所有詞元。在這些情況下，`zero_terms_query` 會指定要不比對任何文件 (`none`) 或比對所有文件 (`all`)。有效值為 `none` 和 `all`。預設為 `none`。

`match_phrase_prefix` 查詢不支援 `fuzziness` 參數。 
{: .note}

## 使用片語前綴比對查詢進行自動完成

`match_phrase_prefix` 查詢不需要特殊對應，因此是為搜尋方塊新增自動完成功能的快速方法。不過，由於其擴充最後一個詞元的方式，可能會傳回不完整的結果。

對於查詢 `chocolate chip c`，OpenSearch 會建立一個片語查詢，要求 `chocolate` 後面接續 `chip`，然後將前綴 `c` 擴充為欄位詞元字典中前 `max_expansions` 個以 `c` 開頭的詞元。這些詞元是依字母順序選取，而非依相關性，因此若有許多以 `c` 開頭的詞元排序在 `cookies` 之前，則包含 `chocolate chip cookies` 的文件不會被傳回。

在隨打即搜的體驗中，這通常可以接受，因為每多輸入一個字母就會縮小前綴範圍，直到缺少的詞元出現為止。增加 `max_expansions` 會傳回更多相符項目，但會使查詢執行成本更高。

若要實現既完整又有效率的自動完成，請使用下列其中一種在編製索引時準備前綴的方法：

- [完成建議器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/#completion-suggester)，其使用 [`completion`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/completion/) 欄位類型，從記憶體內資料結構快速傳回建議。
- [`search_as_you_type`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/search-as-you-type/) 欄位類型，其會為文字欄位的 shingle 和 edge n-gram 編製索引，因此不需要在查詢時擴充前綴相符項目。

如需自動完成方法的比較，請參閱[自動完成]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)。
