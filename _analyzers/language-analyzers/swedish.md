---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "瑞典文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 310
---

# 瑞典文分析器

您可以使用下列命令，將內建的 `swedish` 分析器套用至文字欄位：

```json
PUT /swedish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "swedish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_swedish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_swedish_analyzer": {
          "type": "swedish",
          "stem_exclusion": ["myndighet", "godkännande"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 瑞典文分析器內部結構

`swedish` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（瑞典文）
  - keyword
  - stemmer（瑞典文）

## 自訂瑞典文分析器

您可以使用下列命令建立自訂瑞典文分析器：

```json
PUT /swedish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "swedish_stop": {
          "type": "stop",
          "stopwords": "_swedish_"
        },
        "swedish_stemmer": {
          "type": "stemmer",
          "language": "swedish"
        },
        "swedish_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "swedish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "swedish_stop",
            "swedish_keywords",
            "swedish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "swedish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /swedish-index/_analyze
{
  "field": "content",
  "text": "Studenter studerar vid svenska universitet. Deras nummer är 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "student",
      "start_offset": 0,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "studer",
      "start_offset": 10,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "svensk",
      "start_offset": 23,
      "end_offset": 30,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "universitet",
      "start_offset": 31,
      "end_offset": 42,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "numm",
      "start_offset": 50,
      "end_offset": 56,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "123456",
      "start_offset": 60,
      "end_offset": 66,
      "type": "<NUM>",
      "position": 8
    }
  ]
}
```