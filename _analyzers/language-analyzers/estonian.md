---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "愛沙尼亞文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 130
---

# 愛沙尼亞文分析器

您可以使用下列命令，將內建的 `estonian` 分析器套用至文字欄位：

```json
PUT /estonian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "estonian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_estonian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_estonian_analyzer": {
          "type": "estonian",
          "stem_exclusion": ["autoriteet", "kinnitus"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 愛沙尼亞文分析器內部結構

`estonian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（愛沙尼亞文）
  - keyword
  - stemmer（愛沙尼亞文）

## 自訂愛沙尼亞文分析器

您可以使用下列命令建立自訂的愛沙尼亞文分析器：

```json
PUT /estonian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "estonian_stop": {
          "type": "stop",
          "stopwords": "_estonian_"
        },
        "estonian_stemmer": {
          "type": "stemmer",
          "language": "estonian"
        },
        "estonian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "estonian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "estonian_stop",
            "estonian_keywords",
            "estonian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "estonian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查分析器所產生的詞元：

```json
POST /estonian-index/_analyze
{
  "field": "content",
  "text": "Õpilased õpivad Tallinnas ja Eesti ülikoolides. Nende numbrid on 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "õpilase","start_offset": 0,"end_offset": 8,"type": "<ALPHANUM>","position": 0},
    {"token": "õpi","start_offset": 9,"end_offset": 15,"type": "<ALPHANUM>","position": 1},
    {"token": "tallinna","start_offset": 16,"end_offset": 25,"type": "<ALPHANUM>","position": 2},
    {"token": "eesti","start_offset": 29,"end_offset": 34,"type": "<ALPHANUM>","position": 4},
    {"token": "ülikooli","start_offset": 35,"end_offset": 46,"type": "<ALPHANUM>","position": 5},
    {"token": "nende","start_offset": 48,"end_offset": 53,"type": "<ALPHANUM>","position": 6},
    {"token": "numbri","start_offset": 54,"end_offset": 61,"type": "<ALPHANUM>","position": 7},
    {"token": "on","start_offset": 62,"end_offset": 64,"type": "<ALPHANUM>","position": 8},
    {"token": "123456","start_offset": 65,"end_offset": 71,"type": "<NUM>","position": 9}
  ]
}
```