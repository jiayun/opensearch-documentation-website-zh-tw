---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "保加利亞語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 60
---

# 保加利亞語分析器

您可以使用下列命令，將內建的 `bulgarian` 分析器套用至文字欄位：

```json
PUT /bulgarian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "bulgarian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 與此語言分析器搭配使用：

```json
PUT index_with_stem_exclusion_bulgarian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_bulgarian_analyzer": {
          "type": "bulgarian",
          "stem_exclusion": ["авторитет", "одобрение"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 保加利亞語分析器內部結構

`bulgarian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（保加利亞語）
  - keyword
  - stemmer（保加利亞語）

## 自訂保加利亞語分析器

您可以使用下列命令建立自訂保加利亞語分析器：

```json
PUT /bulgarian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "bulgarian_stop": {
          "type": "stop",
          "stopwords": "_bulgarian_"
        },
        "bulgarian_stemmer": {
          "type": "stemmer",
          "language": "bulgarian"
        },
        "bulgarian_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "bulgarian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "bulgarian_stop",
            "bulgarian_keywords",
            "bulgarian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "bulgarian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查分析器所產生的詞元：

```json
POST /bulgarian-index/_analyze
{
  "field": "content",
  "text": "Студентите учат в българските университети. Техните номера са 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "студент","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
    {"token": "учат","start_offset": 11,"end_offset": 15,"type": "<ALPHANUM>","position": 1},
    {"token": "българск","start_offset": 18,"end_offset": 29,"type": "<ALPHANUM>","position": 3},
    {"token": "университят","start_offset": 30,"end_offset": 42,"type": "<ALPHANUM>","position": 4},
    {"token": "техн","start_offset": 44,"end_offset": 51,"type": "<ALPHANUM>","position": 5},
    {"token": "номер","start_offset": 52,"end_offset": 58,"type": "<ALPHANUM>","position": 6},
    {"token": "123456","start_offset": 62,"end_offset": 68,"type": "<NUM>","position": 8}
  ]
}
```