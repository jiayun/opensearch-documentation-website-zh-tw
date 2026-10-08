---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "德文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 170
---

# 德文分析器

您可以使用下列命令，將內建的 `german` 分析器套用至文字欄位：

```json
PUT /german-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "german"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_german_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_german_analyzer": {
          "type": "german",
          "stem_exclusion": ["Autorität", "Genehmigung"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 德文分析器內部結構

`german` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（德文）
  - keyword
  - normalization（德文）
  - stemmer（德文）

## 自訂德文分析器

您可以使用下列命令建立自訂德文分析器：

```json
PUT /german-index
{
  "settings": {
    "analysis": {
      "filter": {
        "german_stop": {
          "type": "stop",
          "stopwords": "_german_"
        },
        "german_stemmer": {
          "type": "stemmer",
          "language": "light_german"
        },
        "german_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "german_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "german_stop",
            "german_keywords",
            "german_normalization",
            "german_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "german_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器所產生的詞元：

```json
POST /german-index/_analyze
{
  "field": "content",
  "text": "Die Studenten studieren an den deutschen Universitäten. Ihre Nummern sind 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "student",
      "start_offset": 4,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "studi",
      "start_offset": 14,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "deutsch",
      "start_offset": 31,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "universitat",
      "start_offset": 41,
      "end_offset": 54,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "numm",
      "start_offset": 61,
      "end_offset": 68,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "123456",
      "start_offset": 74,
      "end_offset": 80,
      "type": "<NUM>",
      "position": 10
    }
  ]
}
```