---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "義大利文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 220
---

# 義大利文分析器

您可以使用下列命令，將內建的 `italian` 分析器套用至文字欄位：

```json
PUT /italian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "italian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_italian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_italian_analyzer": {
          "type": "italian",
          "stem_exclusion": ["autorità", "approvazione"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 義大利文分析器內部結構

`italian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - elision（義大利文）
  - lowercase
  - stop（義大利文）
  - keyword
  - stemmer（義大利文）

## 自訂義大利文分析器

您可以使用下列命令建立自訂義大利文分析器：

```json
PUT /italian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "italian_stop": {
          "type": "stop",
          "stopwords": "_italian_"
        },
        "italian_elision": {
          "type": "elision",
          "articles": [
                "c", "l", "all", "dall", "dell",
                "nell", "sull", "coll", "pell",
                "gl", "agl", "dagl", "degl", "negl",
                "sugl", "un", "m", "t", "s", "v", "d"
          ],
          "articles_case": true
        },
        "italian_stemmer": {
          "type": "stemmer",
          "language": "light_italian"
        },
        "italian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "italian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "italian_elision",
            "lowercase",
            "italian_stop",
            "italian_keywords",
            "italian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "italian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /italian-index/_analyze
{
  "field": "content",
  "text": "Gli studenti studiano nelle università italiane. I loro numeri sono 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "student","start_offset": 4,"end_offset": 12,"type": "<ALPHANUM>","position": 1},
    {"token": "studian","start_offset": 13,"end_offset": 21,"type": "<ALPHANUM>","position": 2},
    {"token": "universit","start_offset": 28,"end_offset": 38,"type": "<ALPHANUM>","position": 4},
    {"token": "italian","start_offset": 39,"end_offset": 47,"type": "<ALPHANUM>","position": 5},
    {"token": "numer","start_offset": 56,"end_offset": 62,"type": "<ALPHANUM>","position": 8},
    {"token": "123456","start_offset": 68,"end_offset": 74,"type": "<NUM>","position": 10}
  ]
}
```