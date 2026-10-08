---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "愛爾蘭語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 210
---

# 愛爾蘭語分析器

您可以使用下列命令，將內建的 `irish` 分析器套用至文字欄位：

```json
PUT /irish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "irish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 與此語言分析器搭配使用：

```json
PUT index_with_stem_exclusion_irish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_irish_analyzer": {
          "type": "irish",
          "stem_exclusion": ["údarás", "faomhadh"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 愛爾蘭語分析器內部結構

`irish` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - hyphenation（愛爾蘭語）
  - elision（愛爾蘭語）
  - lowercase（愛爾蘭語）
  - stop（愛爾蘭語）
  - keyword
  - stemmer（愛爾蘭語）

## 自訂愛爾蘭語分析器

您可以使用下列命令建立自訂的愛爾蘭語分析器：

```json
PUT /irish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "irish_stop": {
          "type": "stop",
          "stopwords": "_irish_"
        },
        "irish_elision": {
          "type":       "elision",
          "articles":   [ "d", "m", "b" ],
          "articles_case": true
        },
        "irish_hyphenation": {
          "type":       "stop",
          "stopwords":  [ "h", "n", "t" ],
          "ignore_case": true
        },
        "irish_lowercase": {
          "type":       "lowercase",
          "language":   "irish"
        },
        "irish_stemmer": {
          "type": "stemmer",
          "language": "irish"
        },
        "irish_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "irish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "irish_hyphenation",
            "irish_elision",
            "irish_lowercase",
            "irish_stop",
            "irish_keywords",
            "irish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "irish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查分析器所產生的詞元：

```json
POST /irish-index/_analyze
{
  "field": "content",
  "text": "Tá mic léinn ag staidéar in ollscoileanna na hÉireann. Is iad a gcuid uimhreacha ná 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "tá","start_offset": 0,"end_offset": 2,"type": "<ALPHANUM>","position": 0},
    {"token": "mic","start_offset": 3,"end_offset": 6,"type": "<ALPHANUM>","position": 1},
    {"token": "léinn","start_offset": 7,"end_offset": 12,"type": "<ALPHANUM>","position": 2},
    {"token": "staidéar","start_offset": 16,"end_offset": 24,"type": "<ALPHANUM>","position": 4},
    {"token": "ollscoileanna","start_offset": 28,"end_offset": 41,"type": "<ALPHANUM>","position": 6},
    {"token": "héireann","start_offset": 45,"end_offset": 53,"type": "<ALPHANUM>","position": 8},
    {"token": "cuid","start_offset": 64,"end_offset": 69,"type": "<ALPHANUM>","position": 12},
    {"token": "uimhreacha","start_offset": 70,"end_offset": 80,"type": "<ALPHANUM>","position": 13},
    {"token": "123456","start_offset": 84,"end_offset": 90,"type": "<NUM>","position": 15}
  ]
}
```