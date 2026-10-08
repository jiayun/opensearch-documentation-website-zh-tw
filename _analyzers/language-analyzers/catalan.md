---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "加泰隆尼亞語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 70
---

# 加泰隆尼亞語分析器

您可以使用下列命令，將內建的 `catalan` 分析器套用至文字欄位：

```json
PUT /catalan-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "catalan"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_catalan_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_catalan_analyzer": {
          "type": "catalan",
          "stem_exclusion": ["autoritat", "aprovació"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 加泰隆尼亞語分析器內部結構

`catalan` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - elision（加泰隆尼亞語）
  - lowercase
  - stop（加泰隆尼亞語）
  - keyword
  - stemmer（加泰隆尼亞語）

## 自訂加泰隆尼亞語分析器

您可以使用下列命令建立自訂的加泰隆尼亞語分析器：

```json
PUT /catalan-index
{
  "settings": {
    "analysis": {
      "filter": {
        "catalan_stop": {
          "type": "stop",
          "stopwords": "_catalan_"
        },
        "catalan_elision": {
          "type":       "elision",
          "articles":   [ "d", "l", "m", "n", "s", "t"],
          "articles_case": true
        },
        "catalan_stemmer": {
          "type": "stemmer",
          "language": "catalan"
        },
        "catalan_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "catalan_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "catalan_elision",
            "lowercase",
            "catalan_stop",
            "catalan_keywords",
            "catalan_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "catalan_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /catalan-index/_analyze
{
  "field": "content",
  "text": "Els estudiants estudien a les universitats catalanes. Els seus números són 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "estud","start_offset": 4,"end_offset": 14,"type": "<ALPHANUM>","position": 1},
    {"token": "estud","start_offset": 15,"end_offset": 23,"type": "<ALPHANUM>","position": 2},
    {"token": "univer","start_offset": 30,"end_offset": 42,"type": "<ALPHANUM>","position": 5},
    {"token": "catalan","start_offset": 43,"end_offset": 52,"type": "<ALPHANUM>","position": 6},
    {"token": "numer","start_offset": 63,"end_offset": 70,"type": "<ALPHANUM>","position": 9},
    {"token": "123456","start_offset": 75,"end_offset": 81,"type": "<NUM>","position": 11}
  ]
}
```