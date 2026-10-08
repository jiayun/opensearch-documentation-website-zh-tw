---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "印尼文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 210
---

# 印尼文分析器

您可以使用下列命令，將內建的 `indonesian` 分析器套用至文字欄位：

```json
PUT /indonesian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "indonesian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_indonesian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_indonesian_analyzer": {
          "type": "indonesian",
          "stem_exclusion": ["otoritas", "persetujuan"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 印尼文分析器內部結構

`indonesian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（印尼文）
  - keyword
  - stemmer（印尼文）

## 自訂印尼文分析器

您可以使用下列命令建立自訂印尼文分析器：

```json
PUT /indonesian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "indonesian_stop": {
          "type": "stop",
          "stopwords": "_indonesian_"
        },
        "indonesian_stemmer": {
          "type": "stemmer",
          "language": "indonesian"
        },
        "indonesian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "indonesian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "indonesian_stop",
            "indonesian_keywords",
            "indonesian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "indonesian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求，檢查使用此分析器所產生的詞元：

```json
POST /indonesian-index/_analyze
{
  "field": "content",
  "text": "Mahasiswa belajar di universitas Indonesia. Nomor mereka adalah 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "mahasiswa",
      "start_offset": 0,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ajar",
      "start_offset": 10,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "universitas",
      "start_offset": 21,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "indonesia",
      "start_offset": 33,
      "end_offset": 42,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "nomor",
      "start_offset": 44,
      "end_offset": 49,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "123456",
      "start_offset": 64,
      "end_offset": 70,
      "type": "<NUM>",
      "position": 8
    }
  ]
}
```