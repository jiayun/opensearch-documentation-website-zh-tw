---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Token count
nav_order: 55
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/token-count/
  - /opensearch/supported-field-types/token-count/
  - /field-types/token-count/
---

# Token count 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

Token count 欄位類型會儲存字串經分析後的詞元數量。

## 範例

建立一個包含 token count 欄位的對應：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "sentence": { 
        "type": "text",
        "fields": {
          "num_words": { 
            "type":     "token_count",
            "analyzer": "english"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將三份含有文字欄位的文件編製索引：

```json
PUT testindex/_doc/1
{ "sentence": "To be, or not to be: that is the question." }
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{ "sentence": "All the world’s a stage, and all the men and women are merely players." }
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/3
{ "sentence": "Now is the winter of our discontent." }
```
{% include copy-curl.html %}

搜尋少於 10 個詞的句子：

```json
GET testindex/_search
{
  "query": {
    "range": {
      "sentence.num_words": {
        "lt": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含一個符合的句子：

```json
{
  "took" : 8,
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
        "_index" : "testindex",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "sentence" : "Now is the winter of our discontent."
        }
      }
    ]
  }
}
```

## 參數

下表列出 token count 欄位類型接受的參數。`analyzer` 參數為必要；其餘參數皆為選用。

參數 | 說明 
:--- | :--- 
`analyzer` | 此欄位要使用的分析器。若要達到最佳效能，請指定不含詞元篩選器的分析器。必要。可動態更新。
`boost` | 指定此欄位對相關性分數權重的浮點數值。高於 1.0 的值會提高此欄位的相關性；介於 0.0 與 1.0 之間的值會降低此欄位的相關性。預設為 1.0。可動態更新。
`doc_values` | 指定是否應將此欄位儲存在磁碟上，以便用於彙總、排序或指令碼的布林值。預設為 `true`。
`enable_position_increments` | 指定是否應計算位置增量的布林值。若要避免移除停用詞，請將此欄位設為 `false`。預設為 `true`。
`index` | 指定此欄位是否應可被搜尋的布林值。預設為 `true`。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與該欄位為相同類型。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為遺失。預設為 `null`。
`store` | 指定是否應儲存欄位值，並可與 `_source` 欄位分開擷取的布林值。預設為 `false`。 
