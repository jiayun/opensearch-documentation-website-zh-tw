---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Simple 分析器"
parent: Analyzers
nav_order: 100
---

# Simple 分析器

`simple` 分析器是一種非常基本的分析器，會在非字母字元處將文字拆分為詞彙，並將詞彙轉換為小寫。與 `standard` 分析器不同，`simple` 分析器會將字母字元以外的所有字元視為分隔符號，這表示它不會將數字、標點符號或特殊字元視為詞元的一部分。

## 範例

使用下列命令建立名為 `my_simple_index` 且使用 `simple` 分析器的索引：

```json
PUT /my_simple_index
{
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "simple"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定自訂分析器

使用下列命令為索引設定自訂分析器，該分析器等同於加入 `html_strip` 字元篩選器的 `simple` 分析器：

```json
PUT /my_custom_simple_index
{
  "settings": {
    "analysis": {
      "char_filter": {
        "html_strip": {
          "type": "html_strip"
        }
      },
      "tokenizer": {
        "my_lowercase_tokenizer": {
          "type": "lowercase"
        }
      },
      "analyzer": {
        "my_custom_simple_analyzer": {
          "type": "custom",
          "char_filter": ["html_strip"],
          "tokenizer": "my_lowercase_tokenizer",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_custom_simple_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器所產生的詞元：

```json
POST /my_custom_simple_index/_analyze
{
  "analyzer": "my_custom_simple_analyzer",
  "text": "<p>The slow turtle swims over to dogs &copy; 2024!</p>"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "the","start_offset": 3,"end_offset": 6,"type": "word","position": 0},
    {"token": "slow","start_offset": 7,"end_offset": 11,"type": "word","position": 1},
    {"token": "turtle","start_offset": 12,"end_offset": 18,"type": "word","position": 2},
    {"token": "swims","start_offset": 19,"end_offset": 24,"type": "word","position": 3},
    {"token": "over","start_offset": 25,"end_offset": 29,"type": "word","position": 4},
    {"token": "to","start_offset": 30,"end_offset": 32,"type": "word","position": 5},
    {"token": "dogs","start_offset": 33,"end_offset": 37,"type": "word","position": 6}
  ]
}
```
