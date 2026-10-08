---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Trim
parent: Token filters
nav_order: 430
---

# Trim 詞元篩選器

`trim` 詞元篩選器會移除詞元開頭和結尾的空白字元。

許多常用的斷詞器，例如 `standard`、`keyword` 和 `whitespace` 斷詞器，會在斷詞過程中自動去除開頭和結尾的空白字元。使用這些斷詞器時，不需要另外設定 `trim` 詞元篩選器。
{: .note}


## 範例

下列範例請求會建立名為 `my_pattern_trim_index` 的新索引，並設定一個使用 `trim` 篩選器和 `pattern` 斷詞器的分析器，該斷詞器不會移除開頭和結尾的空白字元：

```json
PUT /my_pattern_trim_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_trim_filter": {
          "type": "trim"
        }
      },
      "tokenizer": {
        "my_pattern_tokenizer": {
          "type": "pattern",
          "pattern": ","
        }
      },
      "analyzer": {
        "my_pattern_trim_analyzer": {
          "type": "custom",
          "tokenizer": "my_pattern_tokenizer",
          "filter": [
            "lowercase",
            "my_trim_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器所產生的詞元：

```json
GET /my_pattern_trim_index/_analyze
{
  "analyzer": "my_pattern_trim_analyzer",
  "text": " OpenSearch ,  is ,   powerful  "
}
```
{% include copy-curl.html %}

回應會包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 0,
      "end_offset": 12,
      "type": "word",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 13,
      "end_offset": 18,
      "type": "word",
      "position": 1
    },
    {
      "token": "powerful",
      "start_offset": 19,
      "end_offset": 32,
      "type": "word",
      "position": 2
    }
  ]
}
```
