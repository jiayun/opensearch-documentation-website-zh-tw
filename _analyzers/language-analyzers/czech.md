---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "捷克語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 90
---

# 捷克語分析器

您可以使用下列命令，將內建的 `czech` 分析器套用至文字欄位：

```json
PUT /czech-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "czech"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_czech_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_czech_analyzer": {
          "type": "czech",
          "stem_exclusion": ["autorita", "schválení"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 捷克語分析器內部結構

`czech` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（捷克語）
  - keyword
  - stemmer（捷克語）

## 自訂捷克語分析器

您可以使用下列命令建立自訂捷克語分析器：

```json
PUT /czech-index
{
  "settings": {
    "analysis": {
      "filter": {
        "czech_stop": {
          "type": "stop",
          "stopwords": "_czech_"
        },
        "czech_stemmer": {
          "type": "stemmer",
          "language": "czech"
        },
        "czech_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "czech_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "czech_stop",
            "czech_keywords",
            "czech_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "czech_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /czech-index/_analyze
{
  "field": "content",
  "text": "Studenti studují na českých univerzitách. Jejich čísla jsou 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "student",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "studuj",
      "start_offset": 9,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "česk",
      "start_offset": 20,
      "end_offset": 27,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "univerzit",
      "start_offset": 28,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "čísl",
      "start_offset": 49,
      "end_offset": 54,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "123456",
      "start_offset": 60,
      "end_offset": 66,
      "type": "<NUM>",
      "position": 8
    }
  ]
}
```