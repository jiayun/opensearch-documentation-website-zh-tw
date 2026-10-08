---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "小寫"
parent: Tokenizers
nav_order: 70
---

# 小寫斷詞器

`lowercase` 斷詞器會在空白字元處將文字分割成詞彙，然後將所有詞彙轉換為小寫。在功能上，這與設定搭配 `lowercase` 詞元篩選器的 `letter` 斷詞器相同。不過，使用 `lowercase` 斷詞器更有效率，因為斷詞器的動作會在單一步驟中完成。

## 使用範例

下列範例請求會建立名為 `my-lowercase-index` 的新索引，並設定使用 `lowercase` 斷詞器的分析器：

```json
PUT /my-lowercase-index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_lowercase_tokenizer": {
          "type": "lowercase"
        }
      },
      "analyzer": {
        "my_lowercase_analyzer": {
          "type": "custom",
          "tokenizer": "my_lowercase_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my-lowercase-index/_analyze
{
  "analyzer": "my_lowercase_analyzer",
  "text": "This is a Test. OpenSearch 123!"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "this",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 5,
      "end_offset": 7,
      "type": "word",
      "position": 1
    },
    {
      "token": "a",
      "start_offset": 8,
      "end_offset": 9,
      "type": "word",
      "position": 2
    },
    {
      "token": "test",
      "start_offset": 10,
      "end_offset": 14,
      "type": "word",
      "position": 3
    },
    {
      "token": "opensearch",
      "start_offset": 16,
      "end_offset": 26,
      "type": "word",
      "position": 4
    }
  ]
}
```
