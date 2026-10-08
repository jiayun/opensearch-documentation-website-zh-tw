---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "大寫"
parent: Token filters
nav_order: 460
---

# 大寫詞元篩選器

`uppercase` 詞元篩選器可用於在分析期間將所有詞元 (單字) 轉換為大寫。

## 範例

下列範例請求會建立名為 `uppercase_example` 的新索引，並設定含有 `uppercase` 篩選器的分析器：

```json
PUT /uppercase_example
{
  "settings": {
    "analysis": {
      "filter": {
        "uppercase_filter": {
          "type": "uppercase"
        }
      },
      "analyzer": {
        "uppercase_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "uppercase_filter"
          ]
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
GET /uppercase_example/_analyze
{
  "analyzer": "uppercase_analyzer",
  "text": "OpenSearch is powerful"
}
```
{% include copy-curl.html %}

回應中包含所產生的詞元：

```json
{
  "tokens": [
    {
      "token": "OPENSEARCH",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "IS",
      "start_offset": 11,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "POWERFUL",
      "start_offset": 14,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```
