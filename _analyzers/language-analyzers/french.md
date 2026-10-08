---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "法文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 150
---

# 法文分析器

您可以使用下列命令，將內建的 `french` 分析器套用至文字欄位：

```json
PUT /french-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "french"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_french_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_french_analyzer": {
          "type": "french",
          "stem_exclusion": ["autorité", "acceptation"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 法文分析器內部結構

`french` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - elision（法文）
  - lowercase
  - stop（法文）
  - keyword
  - stemmer（法文）

## 自訂法文分析器

您可以使用下列命令建立自訂法文分析器：

```json
PUT /french-index
{
  "settings": {
    "analysis": {
      "filter": {
        "french_stop": {
          "type": "stop",
          "stopwords": "_french_"
        },
        "french_elision": {
          "type":         "elision",
          "articles_case": true,
          "articles": [
              "l", "m", "t", "qu", "n", "s",
              "j", "d", "c", "jusqu", "quoiqu",
              "lorsqu", "puisqu"
            ]
        },
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        },
        "french_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "french_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "french_elision",
            "lowercase",
            "french_stop",
            "french_keywords",
            "french_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "french_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /french-index/_analyze
{
  "field": "content",
  "text": "Les étudiants étudient à Paris et dans les universités françaises. Leurs numéros sont 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "etudiant","start_offset": 4,"end_offset": 13,"type": "<ALPHANUM>","position": 1},
    {"token": "etudient","start_offset": 14,"end_offset": 22,"type": "<ALPHANUM>","position": 2},
    {"token": "pari","start_offset": 25,"end_offset": 30,"type": "<ALPHANUM>","position": 4},
    {"token": "universit","start_offset": 43,"end_offset": 54,"type": "<ALPHANUM>","position": 8},
    {"token": "francais","start_offset": 55,"end_offset": 65,"type": "<ALPHANUM>","position": 9},
    {"token": "numero","start_offset": 73,"end_offset": 80,"type": "<ALPHANUM>","position": 11},
    {"token": "123456","start_offset": 86,"end_offset": 92,"type": "<NUM>","position": 13}
  ]
}
```