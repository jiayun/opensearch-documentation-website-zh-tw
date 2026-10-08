---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "簡單模式分割"
parent: Tokenizers
nav_order: 120
---

# 簡單模式分割斷詞器

`simple_pattern_split` 斷詞器使用規則運算式將文字分割成詞元。規則運算式定義了用來判斷文字分割位置的模式。文字中任何符合模式的內容都會作為分隔字元，而分隔字元之間的文字則成為詞元。當您想要定義分隔字元，並根據模式將其餘文字斷詞時，可以使用此斷詞器。

此斷詞器僅將輸入文字中符合的部分（依據規則運算式）用作分隔字元或邊界，以將文字分割成詞彙。符合的部分不會包含在產生的詞彙中。例如，如果斷詞器設定為在點字元（`.`）處分割文字，而輸入文字為 `one.two.three`，則產生的詞彙為 `one`、`two` 和 `three`。點字元本身不會包含在產生的詞彙中。

## 範例用法

下列範例請求會建立一個名為 `my_index` 的新索引，並設定一個包含 `simple_pattern_split` 斷詞器的分析器。此斷詞器設定為以連字號分割文字：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pattern_split_tokenizer": {
          "type": "simple_pattern_split",
          "pattern": "-"
        }
      },
      "analyzer": {
        "my_pattern_split_analyzer": {
          "type": "custom",
          "tokenizer": "my_pattern_split_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_pattern_split_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_pattern_split_analyzer",
  "text": "OpenSearch-2024-10-09"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "OpenSearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "word",
      "position": 0
    },
    {
      "token": "2024",
      "start_offset": 11,
      "end_offset": 15,
      "type": "word",
      "position": 1
    },
    {
      "token": "10",
      "start_offset": 16,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "09",
      "start_offset": 19,
      "end_offset": 21,
      "type": "word",
      "position": 3
    }
  ]
}
```

## 參數

`simple_pattern_split` 斷詞器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 選用 | 字串 | 用於將文字分割成詞元的模式，以 [Lucene 規則運算式](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/util/automaton/RegExp.html) 指定。預設為空字串，此時會將輸入文字作為單一詞元傳回。 