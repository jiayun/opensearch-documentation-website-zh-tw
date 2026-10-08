---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "葡萄牙文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 260
---

# 葡萄牙文分析器

您可以使用下列命令，將內建的 `portuguese` 分析器套用至文字欄位：

```json
PUT /portuguese-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "portuguese"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_portuguese_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_portuguese_analyzer": {
          "type": "portuguese",
          "stem_exclusion": ["autoridade", "aprovação"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 葡萄牙文分析器內部結構

`portuguese` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（葡萄牙文）
  - keyword
  - stemmer（葡萄牙文）

## 自訂葡萄牙文分析器

您可以使用下列命令建立自訂葡萄牙文分析器：

```json
PUT /portuguese-index
{
  "settings": {
    "analysis": {
      "filter": {
        "portuguese_stop": {
          "type": "stop",
          "stopwords": "_portuguese_"
        },
        "portuguese_stemmer": {
          "type": "stemmer",
          "language": "light_portuguese"
        },
        "portuguese_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "portuguese_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "portuguese_stop",
            "portuguese_keywords",
            "portuguese_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "portuguese_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /portuguese-index/_analyze
{
  "field": "content",
  "text": "Os estudantes estudam nas universidades brasileiras. Seus números são 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "estudant",
      "start_offset": 3,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "estudam",
      "start_offset": 14,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "universidad",
      "start_offset": 26,
      "end_offset": 39,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "brasileir",
      "start_offset": 40,
      "end_offset": 51,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "numer",
      "start_offset": 58,
      "end_offset": 65,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "123456",
      "start_offset": 70,
      "end_offset": 76,
      "type": "<NUM>",
      "position": 9
    }
  ]
}
```