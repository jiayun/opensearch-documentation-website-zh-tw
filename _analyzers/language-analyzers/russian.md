---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "俄文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 280
---

# 俄文分析器

您可以使用下列命令，將內建的 `russian` 分析器套用至文字欄位：

```json
PUT /russian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "russian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_russian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_russian_analyzer": {
          "type": "russian",
          "stem_exclusion": ["авторитет", "одобрение"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 俄文分析器內部結構

`russian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（俄文）
  - keyword
  - stemmer（俄文）

## 自訂俄文分析器

您可以使用下列命令建立自訂俄文分析器：

```json
PUT /russian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "russian_stop": {
          "type": "stop",
          "stopwords": "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        },
        "russian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "russian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "russian_stop",
            "russian_keywords",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "russian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /russian-index/_analyze
{
  "field": "content",
  "text": "Студенты учатся в университетах России. Их номера 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "студент",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "учат",
      "start_offset": 9,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "университет",
      "start_offset": 18,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "росс",
      "start_offset": 32,
      "end_offset": 38,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "номер",
      "start_offset": 43,
      "end_offset": 49,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "123456",
      "start_offset": 50,
      "end_offset": 56,
      "type": "<NUM>",
      "position": 7
    }
  ]
}
```