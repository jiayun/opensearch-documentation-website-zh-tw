---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Search as you type
nav_order: 53
has_children: false
parent: Autocomplete field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/search-as-you-type/
  - /opensearch/supported-field-types/search-as-you-type/
  - /field-types/search-as-you-type/
---

# Search-as-you-type 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

search-as-you-type 欄位類型透過前綴與中綴補全提供即時輸入搜尋功能。

## 範例

為 search-as-you-type 欄位建立對應時，會產生此欄位的 n-gram 子欄位，其中 n 的範圍為 [2, `max_shingle_size`]。此外，還會建立一個索引前綴子欄位。

建立一個包含 search-as-you-type 欄位的對應：

```json
PUT books
{
  "mappings": {
    "properties": {
      "suggestions": {
        "type": "search_as_you_type"
      }
    }
  }
}
```
{% include copy-curl.html %}

除了 `suggestions` 欄位之外，這也會建立 `suggestions._2gram`、`suggestions._3gram` 和 `suggestions._index_prefix` 欄位。

為包含 search-as-you-type 欄位的文件編製索引：

```json
PUT books/_doc/1
{
  "suggestions": "one two three four"
}
```
{% include copy-curl.html %}

若要以任意順序比對詞元，請使用 bool_prefix 或 multi-match 查詢。這些查詢會將搜尋詞元依指定順序出現的文件，排在詞元順序不符的文件之前。

```json
GET books/_search
{
  "query": {
    "multi_match": {
      "query": "tw one",
      "type": "bool_prefix",
      "fields": [
        "suggestions",
        "suggestions._2gram",
        "suggestions._3gram"
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  "took" : 13,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "suggestions" : "one two three four"
        }
      }
    ]
  }
}
```

若要依順序比對詞元，請使用 match_phrase_prefix 查詢：

```json
GET books/_search
{
  "query": {
    "match_phrase_prefix": {
      "suggestions": "two th"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  "took" : 23,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.4793051,
    "hits" : [
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.4793051,
        "_source" : {
          "suggestions" : "one two three four"
        }
      }
    ]
  }
}
```

若要精確比對最後的詞元，請使用 match_phrase 查詢：

```json
GET books/_search
{
  "query": {
    "match_phrase": {
      "suggestions": "four"
    }
  }
}
```
{% include copy-curl.html %}

回應：

```json
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.2876821,
    "hits" : [
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.2876821,
        "_source" : {
          "suggestions" : "one two three four"
        }
      }
    ]
  }
}
```

## 參數

下表列出 search-as-you-type 欄位類型接受的參數。所有參數皆為選用。

Parameter | Description 
:--- | :---
`analyzer` | 用於此欄位的分析器。預設會在編製索引時與搜尋時使用。若要在搜尋時覆寫，請設定 `search_analyzer` 參數。預設為 `standard` 分析器，該分析器使用基於文法的斷詞，並以 [Unicode Text Segmentation](https://unicode.org/reports/tr29/) 演算法為基礎。設定根欄位與子欄位。
`index` | 指定此欄位是否可搜尋的布林值。預設為 `true`。設定根欄位與子欄位。
`index_options` | 指定要在索引中儲存哪些資訊以供搜尋與突顯。有效值：`docs`（僅文件編號）、`freqs`（文件編號與詞元頻率）、`positions`（文件編號、詞元頻率與詞元位置）、`offsets`（文件編號、詞元頻率、詞元位置，以及起始與結束字元位移）。預設為 `positions`。設定根欄位與子欄位。
`max_shingle_size` | 指定 n-gram 最大長度的整數。有效值範圍為 [2, 4]。建立的 n-gram 範圍為 [2, `max_shingle_size`]。預設為 3，會建立 2-gram 與 3-gram。較大的 `max_shingle_size` 值對更具體的查詢效果較佳，但會導致索引大小增加。
`norms` | 指定計算相關性分數時是否使用欄位長度的布林值。設定根欄位與 n-gram 子欄位（預設為 `false`）。不設定前綴子欄位（在前綴子欄位中，`norms` 為 `false`）。
`search_analyzer` | 搜尋時使用的分析器。預設為 `analyzer` 參數中指定的分析器。設定根欄位與子欄位。
`search_quote_analyzer` | 搜尋時用於片語的分析器。預設為 `analyzer` 參數中指定的分析器。設定根欄位與子欄位。
`similarity` | 用於計算相關性分數的排名演算法。預設為 `BM25`。設定根欄位與子欄位。
`store` | 指定是否儲存欄位值，以及是否能從 `_source` 欄位另外擷取的布林值。預設為 `false`。僅設定根欄位。
[`term_vector`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text#term-vector-parameter) | 指定是否儲存此欄位之詞元向量的布林值。預設為 `no`。設定根欄位與 n-gram 子欄位。不設定前綴子欄位。 
