---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "英文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 120
---

# 英文分析器

您可以使用下列命令，將內建的 `english` 分析器套用至文字欄位：

```json
PUT /english-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "english"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_english_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_english_analyzer": {
          "type": "english",
          "stem_exclusion": ["authority", "authorization"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 英文分析器內部結構

`english` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - stemmer (possessive_english)
  - lowercase
  - stop (English)
  - keyword
  - stemmer (English)

## 自訂英文分析器

您可以使用下列命令建立自訂英文分析器：

```json
PUT /english-index
{
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_keywords": {
          "type": "keyword_marker",
          "keywords": []
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english"
        }
      },
      "analyzer": {
        "english_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "english_keywords",
            "english_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "english_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢視分析器產生的詞元：

```json
POST /english-index/_analyze
{
  "field": "content",
  "text": "The students study in the USA and work at NASA. Their numbers are 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "student","start_offset": 4,"end_offset": 12,"type": "<ALPHANUM>","position": 1},
    {"token": "studi","start_offset": 13,"end_offset": 18,"type": "<ALPHANUM>","position": 2},
    {"token": "usa","start_offset": 26,"end_offset": 29,"type": "<ALPHANUM>","position": 5},
    {"token": "work","start_offset": 34,"end_offset": 38,"type": "<ALPHANUM>","position": 7},
    {"token": "nasa","start_offset": 42,"end_offset": 46,"type": "<ALPHANUM>","position": 9},
    {"token": "number","start_offset": 54,"end_offset": 61,"type": "<ALPHANUM>","position": 11},
    {"token": "123456","start_offset": 66,"end_offset": 72,"type": "<NUM>","position": 13}
  ]
}
```