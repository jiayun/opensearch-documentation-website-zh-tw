---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "拉脫維亞語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 230
---

# 拉脫維亞語分析器

您可以使用下列命令，將內建的 `latvian` 分析器套用至文字欄位：

```json
PUT /latvian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "latvian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_latvian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_latvian_analyzer": {
          "type": "latvian",
          "stem_exclusion": ["autoritāte", "apstiprinājums"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 拉脫維亞語分析器內部結構

`latvian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（拉脫維亞語）
  - keyword
  - stemmer（拉脫維亞語）

## 自訂拉脫維亞語分析器

您可以使用下列命令建立自訂的拉脫維亞語分析器：

```json
PUT /latvian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "latvian_stop": {
          "type": "stop",
          "stopwords": "_latvian_"
        },
        "latvian_stemmer": {
          "type": "stemmer",
          "language": "latvian"
        },
        "latvian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "latvian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "latvian_stop",
            "latvian_keywords",
            "latvian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "latvian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查分析器所產生的詞元：

```json
POST /latvian-index/_analyze
{
  "field": "content",
  "text": "Studenti mācās Latvijas universitātēs. Viņu numuri ir 123456."
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
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "māc",
      "start_offset": 9,
      "end_offset": 14,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "latvij",
      "start_offset": 15,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "universitāt",
      "start_offset": 24,
      "end_offset": 37,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "vin",
      "start_offset": 39,
      "end_offset": 43,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "numur",
      "start_offset": 44,
      "end_offset": 50,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "123456",
      "start_offset": 54,
      "end_offset": 60,
      "type": "<NUM>",
      "position": 7
    }
  ]
}
```