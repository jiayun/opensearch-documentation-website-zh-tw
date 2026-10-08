---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "芬蘭文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 140
---

# 芬蘭文分析器

您可以使用下列命令，將內建的 `finnish` 分析器套用至文字欄位：

```json
PUT /finnish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "finnish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_finnish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_finnish_analyzer": {
          "type": "finnish",
          "stem_exclusion": ["valta", "hyväksyntä"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 芬蘭文分析器內部結構

`finnish` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（芬蘭文）
  - keyword
  - stemmer（芬蘭文）

## 自訂芬蘭文分析器

您可以使用下列命令建立自訂芬蘭文分析器：

```json
PUT /finnish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "finnish_stop": {
          "type": "stop",
          "stopwords": "_finnish_"
        },
        "finnish_stemmer": {
          "type": "stemmer",
          "language": "finnish"
        },
        "finnish_keywords": {
          "type": "keyword_marker",
          "keywords": ["Helsinki", "Suomi"]
        }
      },
      "analyzer": {
        "finnish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "finnish_stop",
            "finnish_keywords",
            "finnish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "finnish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器所產生的詞元：

```json
POST /finnish-index/_analyze
{
  "field": "content",
  "text": "Opiskelijat opiskelevat Helsingissä ja Suomen yliopistoissa. Heidän numeronsa ovat 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "opiskelij","start_offset": 0,"end_offset": 11,"type": "<ALPHANUM>","position": 0},
    {"token": "opiskelev","start_offset": 12,"end_offset": 23,"type": "<ALPHANUM>","position": 1},
    {"token": "helsing","start_offset": 24,"end_offset": 35,"type": "<ALPHANUM>","position": 2},
    {"token": "suome","start_offset": 39,"end_offset": 45,"type": "<ALPHANUM>","position": 4},
    {"token": "yliopisto","start_offset": 46,"end_offset": 59,"type": "<ALPHANUM>","position": 5},
    {"token": "numero","start_offset": 68,"end_offset": 77,"type": "<ALPHANUM>","position": 7},
    {"token": "123456","start_offset": 83,"end_offset": 89,"type": "<NUM>","position": 9}
  ]
}
```