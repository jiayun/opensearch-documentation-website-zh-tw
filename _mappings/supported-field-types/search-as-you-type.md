---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "輸入時搜尋"
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

參數 | 說明 
:--- | :---
`analyzer` | 此欄位要使用的分析器。預設會在編製索引時和搜尋時使用。若要在搜尋時覆寫，請設定 `search_analyzer` 參數。預設為 `standard` 分析器，此分析器使用以文法為基礎的斷詞，並以 [Unicode 文字分段](https://unicode.org/reports/tr29/)演算法為基礎。設定根欄位及子欄位。如需詳細資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/analyzer/)。
`index` | 布林值，指定欄位是否應可供搜尋。預設為 `true`。設定根欄位及子欄位。如需詳細資訊，請參閱[索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/)。
`index_options` | 指定要儲存在索引中以供搜尋及醒目提示的資訊。有效值：`docs`（僅文件編號）、`freqs`（文件編號及詞彙頻率）、`positions`（文件編號、詞彙頻率及詞彙位置）、`offsets`（文件編號、詞彙頻率、詞彙位置，以及起始與結束字元位移）。預設為 `positions`。設定根欄位及子欄位。如需詳細資訊，請參閱[索引選項]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-options/)。
`max_shingle_size` | 整數，指定 n-gram 的最大大小。有效值範圍為 [2, 4]。要建立的 n-gram 範圍為 [2, `max_shingle_size`]。預設為 3，會建立 2-gram 和 3-gram。較大的 `max_shingle_size` 值較適合較特定的查詢，但會使索引大小變大。 
`norms` | 布林值，指定在計算相關性分數時是否應使用欄位長度。設定根欄位及 n-gram 子欄位（預設為 `false`）。不會設定前綴子欄位（在前綴子欄位中，`norms` 為 `false`）。如需詳細資訊，請參閱[Norms]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/norms/)。
`search_analyzer` | 搜尋時要使用的分析器。預設為 `analyzer` 參數中指定的分析器。設定根欄位及子欄位。如需詳細資訊，請參閱[搜尋分析器]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/search-analyzer/)。
`search_quote_analyzer` | 搜尋片語時要使用的分析器。預設為 `analyzer` 參數中指定的分析器。設定根欄位及子欄位。
`similarity` | 用於計算相關性分數的排名演算法。預設為 `BM25`。設定根欄位及子欄位。如需詳細資訊，請參閱[相似度]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/similarity/)。
`store` | 布林值，指定是否應儲存欄位值，並可與 `_source` 欄位分開擷取。預設為 `false`。僅設定根欄位。如需詳細資訊，請參閱[儲存]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/)。
[`term_vector`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text#term-vector-parameter) | 布林值，指定是否應儲存此欄位的詞彙向量。預設為 `no`。設定根欄位及 n-gram 子欄位。不會設定前綴子欄位。 
