---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "泰文"
parent: Tokenizers
nav_order: 140
---

# 泰文斷詞器

`thai` 斷詞器會將泰文文字斷詞。由於泰文的單字之間不以空格分隔，斷詞器必須根據語言特定的規則來識別單字邊界。

## 範例用法

下列範例請求會建立一個名為 `thai_index` 的新索引，並設定一個使用 `thai` 斷詞器的分析器：

```json
PUT /thai_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "thai_tokenizer": {
          "type": "thai"
        }
      },
      "analyzer": {
        "thai_analyzer": {
          "type": "custom",
          "tokenizer": "thai_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "thai_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器所產生的詞元：

```json
POST /thai_index/_analyze
{
  "analyzer": "thai_analyzer",
  "text": "ฉันชอบไปเที่ยวที่เชียงใหม่"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "ฉัน",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "ชอบ",
      "start_offset": 3,
      "end_offset": 6,
      "type": "word",
      "position": 1
    },
    {
      "token": "ไป",
      "start_offset": 6,
      "end_offset": 8,
      "type": "word",
      "position": 2
    },
    {
      "token": "เที่ยว",
      "start_offset": 8,
      "end_offset": 14,
      "type": "word",
      "position": 3
    },
    {
      "token": "ที่",
      "start_offset": 14,
      "end_offset": 17,
      "type": "word",
      "position": 4
    },
    {
      "token": "เชียงใหม่",
      "start_offset": 17,
      "end_offset": 26,
      "type": "word",
      "position": 5
    }
  ]
}
```
