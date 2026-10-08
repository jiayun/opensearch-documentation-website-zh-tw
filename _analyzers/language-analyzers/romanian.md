---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "羅馬尼亞文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 270
---

# 羅馬尼亞文分析器

您可以使用下列命令，將內建的 `romanian` 分析器套用至文字欄位：

```json
PUT /romanian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "romanian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_romanian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_romanian_analyzer": {
          "type": "romanian",
          "stem_exclusion": ["autoritate", "aprobat"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 羅馬尼亞文分析器內部結構

`romanian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（羅馬尼亞文）
  - keyword
  - stemmer（羅馬尼亞文）

## 自訂羅馬尼亞文分析器

您可以使用下列命令建立自訂羅馬尼亞文分析器：

```json
PUT /romanian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "romanian_stop": {
          "type": "stop",
          "stopwords": "_romanian_"
        },
        "romanian_stemmer": {
          "type": "stemmer",
          "language": "romanian"
        },
        "romanian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "romanian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "romanian_stop",
            "romanian_keywords",
            "romanian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "romanian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器產生的詞元：

```json
POST /romanian-index/_analyze
{
  "field": "content",
  "text": "Studenții învață la universitățile din România. Numerele lor sunt 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "studenț",
      "start_offset": 0,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "învaț",
      "start_offset": 10,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "universităț",
      "start_offset": 20,
      "end_offset": 34,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "român",
      "start_offset": 39,
      "end_offset": 46,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "numer",
      "start_offset": 48,
      "end_offset": 56,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "123456",
      "start_offset": 66,
      "end_offset": 72,
      "type": "<NUM>",
      "position": 9
    }
  ]
}
```