---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "西班牙文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 300
---

# 西班牙文分析器

您可以使用下列命令，將內建的 `spanish` 分析器套用至文字欄位：

```json
PUT /spanish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "spanish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_spanish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_spanish_analyzer": {
          "type": "spanish",
          "stem_exclusion": ["autoridad", "aprobación"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 西班牙文分析器內部結構

`spanish` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（西班牙文）
  - keyword
  - stemmer（西班牙文）

## 自訂西班牙文分析器

您可以使用下列命令建立自訂西班牙文分析器：

```json
PUT /spanish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "spanish_stop": {
          "type": "stop",
          "stopwords": "_spanish_"
        },
        "spanish_stemmer": {
          "type": "stemmer",
          "language": "light_spanish"
        },
        "spanish_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "spanish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "spanish_stop",
            "spanish_keywords",
            "spanish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "spanish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /spanish-index/_analyze
{
  "field": "content",
  "text": "Los estudiantes estudian en universidades españolas. Sus números son 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "estudiant",
      "start_offset": 4,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "estudian",
      "start_offset": 16,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "universidad",
      "start_offset": 28,
      "end_offset": 41,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "español",
      "start_offset": 42,
      "end_offset": 51,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "numer",
      "start_offset": 57,
      "end_offset": 64,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "123456",
      "start_offset": 69,
      "end_offset": 75,
      "type": "<NUM>",
      "position": 9
    }
  ]
}
```