---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "土耳其語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 330
---

# 土耳其語分析器

您可以使用下列命令，將內建的 `turkish` 分析器套用至文字欄位：

```json
PUT /turkish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "turkish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_turkish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_turkish_analyzer": {
          "type": "turkish",
          "stem_exclusion": ["otorite", "onay"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 土耳其語分析器內部結構

`turkish` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - apostrophe
  - lowercase（土耳其語）
  - stop（土耳其語）
  - keyword
  - stemmer（土耳其語）

## 自訂土耳其語分析器

您可以使用下列命令建立自訂土耳其語分析器：

```json
PUT /turkish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "turkish_stop": {
          "type": "stop",
          "stopwords": "_turkish_"
        },
        "turkish_stemmer": {
          "type": "stemmer",
          "language": "turkish"
        },
        "turkish_lowercase": {
          "type":       "lowercase",
          "language":   "turkish"
        },
        "turkish_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "turkish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "apostrophe",
            "turkish_lowercase",
            "turkish_stop",
            "turkish_keywords",
            "turkish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "turkish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /turkish-index/_analyze
{
  "field": "content",
  "text": "Öğrenciler Türk üniversitelerinde öğrenim görüyor. Numara 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "öğrenci","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
    {"token": "türk","start_offset": 11,"end_offset": 15,"type": "<ALPHANUM>","position": 1},
    {"token": "üniversite","start_offset": 16,"end_offset": 33,"type": "<ALPHANUM>","position": 2},
    {"token": "öğre","start_offset": 34,"end_offset": 41,"type": "<ALPHANUM>","position": 3},
    {"token": "görüyor","start_offset": 42,"end_offset": 49,"type": "<ALPHANUM>","position": 4},
    {"token": "numar","start_offset": 51,"end_offset": 57,"type": "<ALPHANUM>","position": 5},
    {"token": "123456","start_offset": 58,"end_offset": 64,"type": "<NUM>","position": 6}
  ]
}
```