---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Letter
parent: Tokenizers
nav_order: 60
---

# Letter 斷詞器

`letter` 斷詞器會在任何非字母字元處將文字拆分為單字。它適用於許多歐洲語言，但對某些不以空格分隔單字的亞洲語言則沒有效果。

## 範例用法

下列範例請求會建立一個名為 `my_index` 的新索引，並設定一個使用 `letter` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_letter_analyzer": {
          "type": "custom",
          "tokenizer": "letter"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_letter_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器所產生的詞元：

```json
POST _analyze
{
  "tokenizer": "letter",
  "text": "Cats 4EVER love chasing butterflies!"
}

```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Cats",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "EVER",
      "start_offset": 6,
      "end_offset": 10,
      "type": "word",
      "position": 1
    },
    {
      "token": "love",
      "start_offset": 11,
      "end_offset": 15,
      "type": "word",
      "position": 2
    },
    {
      "token": "chasing",
      "start_offset": 16,
      "end_offset": 23,
      "type": "word",
      "position": 3
    },
    {
      "token": "butterflies",
      "start_offset": 24,
      "end_offset": 35,
      "type": "word",
      "position": 4
    }
  ]
}
```
