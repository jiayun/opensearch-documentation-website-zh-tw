---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "希臘文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 180
---

# 希臘文分析器

您可以使用下列命令，將內建的 `greek` 分析器套用至文字欄位：

```json
PUT /greek-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "greek"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_greek_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_greek_analyzer": {
          "type": "greek",
          "stem_exclusion": ["αρχή", "έγκριση"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 希臘文分析器內部結構

`greek` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（希臘文）
  - keyword
  - stemmer（希臘文）

## 自訂希臘文分析器

您可以使用下列命令建立自訂希臘文分析器：

```json
PUT /greek-index
{
  "settings": {
    "analysis": {
      "filter": {
        "greek_stop": {
          "type": "stop",
          "stopwords": "_greek_"
        },
        "greek_lowercase": {
          "type": "lowercase",
          "language": "greek"
        },
        "greek_stemmer": {
          "type": "stemmer",
          "language": "greek"
        },
        "greek_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "greek_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "greek_lowercase",
            "greek_stop",
            "greek_keywords",
            "greek_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "greek_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器產生的詞元：

```json
POST /greek-index/_analyze
{
  "field": "content",
  "text": "Οι φοιτητές σπουδάζουν στα ελληνικά πανεπιστήμια. Οι αριθμοί τους είναι 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "φοιτητ",
      "start_offset": 3,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "σπουδαζ",
      "start_offset": 12,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "στα",
      "start_offset": 23,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "ελλην",
      "start_offset": 27,
      "end_offset": 35,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "πανεπιστημ",
      "start_offset": 36,
      "end_offset": 48,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "αριθμ",
      "start_offset": 53,
      "end_offset": 60,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "τ",
      "start_offset": 61,
      "end_offset": 65,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "123456",
      "start_offset": 72,
      "end_offset": 78,
      "type": "<NUM>",
      "position": 10
    }
  ]
}
```