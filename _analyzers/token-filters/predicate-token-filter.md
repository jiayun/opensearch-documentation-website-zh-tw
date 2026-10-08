---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "述詞詞元篩選器"
parent: Token filters
nav_order: 340
---

# 述詞詞元篩選器

`predicate_token_filter` 會根據自訂指令碼中定義的條件，評估應保留或捨棄詞元。詞元會在分析述詞情境中進行評估。此篩選器僅支援內嵌 Painless 指令碼。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 參數

`predicate_token_filter` 有一個必要參數：`script`。此參數提供用來評估是否應保留詞元的條件。 

## 範例

下列範例請求會建立名為 `predicate_index` 的新索引，並設定使用 `predicate_token_filter` 的分析器。此篩選器指定僅輸出長度超過 7 個字元的詞元：

```json
PUT /predicate_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_predicate_filter": {
          "type": "predicate_token_filter",
          "script": {
            "source": "token.term.length() > 7"
          }
        }
      },
      "analyzer": {
        "predicate_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_predicate_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢視分析器產生的詞元：

```json
POST /predicate_index/_analyze
{
  "text": "The OpenSearch community is growing rapidly",
  "analyzer": "predicate_analyzer"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 4,
      "end_offset": 14,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "community",
      "start_offset": 15,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```
