---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索拉尼語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 290
---

# 索拉尼語分析器

您可以使用下列命令，將內建的 `sorani` 分析器套用至文字欄位：

```json
PUT /sorani-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "sorani"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_sorani_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_sorani_analyzer": {
          "type": "sorani",
          "stem_exclusion": ["مؤسسه", "اجازه"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 索拉尼語分析器內部結構

`sorani` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - normalization (Sorani)
  - lowercase
  - decimal_digit
  - stop (Sorani)
  - keyword
  - stemmer (Sorani)

## 自訂索拉尼語分析器

您可以使用下列命令建立自訂索拉尼語分析器：

```json
PUT /sorani-index
{
  "settings": {
    "analysis": {
      "filter": {
        "sorani_stop": {
          "type": "stop",
          "stopwords": "_sorani_"
        },
        "sorani_stemmer": {
          "type": "stemmer",
          "language": "sorani"
        },
        "sorani_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "sorani_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "sorani_normalization",
            "lowercase",
            "decimal_digit",
            "sorani_stop",
            "sorani_keywords",
            "sorani_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "sorani_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /sorani-index/_analyze
{
  "field": "content",
  "text": "خوێندنی فەرمی لە هەولێرەوە. ژمارەکان ١٢٣٤٥٦."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "خوێندن",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "فەرم",
      "start_offset": 8,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "هەولێر",
      "start_offset": 17,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "ژمار",
      "start_offset": 28,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "123456",
      "start_offset": 37,
      "end_offset": 43,
      "type": "<NUM>",
      "position": 5
    }
  ]
}
```