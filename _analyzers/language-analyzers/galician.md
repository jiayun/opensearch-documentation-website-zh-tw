---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "加利西亞語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 160
---

# 加利西亞語分析器

您可以使用下列命令，將內建的 `galician` 分析器套用至文字欄位：

```json
PUT /galician-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "galician"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 與此語言分析器搭配使用：

```json
PUT index_with_stem_exclusion_galician_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_galician_analyzer": {
          "type": "galician",
          "stem_exclusion": ["autoridade", "aceptación"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 加利西亞語分析器內部結構

`galician` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（加利西亞語）
  - keyword
  - stemmer（加利西亞語）

## 自訂加利西亞語分析器

您可以使用下列命令建立自訂加利西亞語分析器：

```json
PUT /galician-index
{
  "settings": {
    "analysis": {
      "filter": {
        "galician_stop": {
          "type": "stop",
          "stopwords": "_galician_"
        },
        "galician_stemmer": {
          "type": "stemmer",
          "language": "galician"
        },
        "galician_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "galician_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "galician_stop",
            "galician_keywords",
            "galician_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "galician_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器產生的詞元：

```json
POST /galician-index/_analyze
{
  "field": "content",
  "text": "Os estudantes estudan en Santiago e nas universidades galegas. Os seus números son 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "estud","start_offset": 3,"end_offset": 13,"type": "<ALPHANUM>","position": 1},
    {"token": "estud","start_offset": 14,"end_offset": 21,"type": "<ALPHANUM>","position": 2},
    {"token": "santiag","start_offset": 25,"end_offset": 33,"type": "<ALPHANUM>","position": 4},
    {"token": "univers","start_offset": 40,"end_offset": 53,"type": "<ALPHANUM>","position": 7},
    {"token": "galeg","start_offset": 54,"end_offset": 61,"type": "<ALPHANUM>","position": 8},
    {"token": "numer","start_offset": 71,"end_offset": 78,"type": "<ALPHANUM>","position": 11},
    {"token": "son","start_offset": 79,"end_offset": 82,"type": "<ALPHANUM>","position": 12},
    {"token": "123456","start_offset": 83,"end_offset": 89,"type": "<NUM>","position": 13}
  ]
}
```