---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "亞美尼亞語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 20
---

# 亞美尼亞語分析器

您可以使用下列命令，將內建的 `armenian` 分析器套用至文字欄位：

```json
PUT /arabic-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "armenian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_armenian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_armenian_analyzer": {
          "type": "armenian",
          "stem_exclusion": ["բարև", "խաղաղություն"] 
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 亞美尼亞語分析器內部結構

`armenian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（亞美尼亞語）
  - keyword
  - stemmer（亞美尼亞語）

## 自訂亞美尼亞語分析器

您可以使用下列命令建立自訂亞美尼亞語分析器：

```json
PUT /armenian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "armenian_stop": {
          "type": "stop",
          "stopwords": "_armenian_"
        },
        "armenian_stemmer": {
          "type": "stemmer",
          "language": "armenian"
        },
        "armenian_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "armenian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "armenian_stop",
            "armenian_keywords",
            "armenian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "armenian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器所產生的詞元：

```json
GET armenian-index/_analyze
{
  "analyzer": "stem_exclusion_armenian_analyzer",
  "text": "բարև բոլորին, մենք խաղաղություն ենք ուզում և նոր օր ենք սկսել"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "բարև","start_offset": 0,"end_offset": 4,"type": "<ALPHANUM>","position": 0},
    {"token": "բոլոր","start_offset": 5,"end_offset": 12,"type": "<ALPHANUM>","position": 1},
    {"token": "խաղաղություն","start_offset": 19,"end_offset": 31,"type": "<ALPHANUM>","position": 3},
    {"token": "ուզ","start_offset": 36,"end_offset": 42,"type": "<ALPHANUM>","position": 5},
    {"token": "նոր","start_offset": 45,"end_offset": 48,"type": "<ALPHANUM>","position": 7},
    {"token": "օր","start_offset": 49,"end_offset": 51,"type": "<ALPHANUM>","position": 8},
    {"token": "սկսել","start_offset": 56,"end_offset": 61,"type": "<ALPHANUM>","position": 10}
  ]
}
```