---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "簡單模式"
parent: Tokenizers
nav_order: 110
---

# 簡單模式斷詞器

`simple_pattern` 斷詞器會根據規則運算式找出文字中相符的序列，並將這些序列做為詞元。它會擷取符合規則運算式的詞彙。當您想直接將特定模式擷取為詞彙時，請使用此斷詞器。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `simple_pattern` 斷詞器的分析器。此斷詞器會從文字中擷取數字詞彙：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pattern_tokenizer": {
          "type": "simple_pattern",
          "pattern": "\\d+"
        }
      },
      "analyzer": {
        "my_pattern_analyzer": {
          "type": "custom",
          "tokenizer": "my_pattern_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_pattern_analyzer",
  "text": "OpenSearch-2024-10-09"
}
```
{% include copy-curl.html %}

回應中包含所產生的詞元：

```json
{
  "tokens": [
    {
      "token": "2024",
      "start_offset": 11,
      "end_offset": 15,
      "type": "word",
      "position": 0
    },
    {
      "token": "10",
      "start_offset": 16,
      "end_offset": 18,
      "type": "word",
      "position": 1
    },
    {
      "token": "09",
      "start_offset": 19,
      "end_offset": 21,
      "type": "word",
      "position": 2
    }
  ]
}
```

## 參數

`simple_pattern` 斷詞器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 選用 | 字串 | 用於將文字分割成詞元的模式，以 [Lucene 規則運算式](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/util/automaton/RegExp.html) 指定。預設為空字串，會將輸入文字以單一詞元回傳。 

