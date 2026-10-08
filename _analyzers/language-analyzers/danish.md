---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "丹麥文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 100
---

# 丹麥文分析器

您可以使用下列命令，將內建的 `danish` 分析器套用至文字欄位：

```json
PUT /danish-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "danish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 與此語言分析器搭配使用：

```json
PUT index_with_stem_exclusion_danish_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_danish_analyzer": {
          "type": "danish",
          "stem_exclusion": ["autoritet", "godkendelse"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 丹麥文分析器內部結構

`danish` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（丹麥文）
  - keyword
  - stemmer（丹麥文）

## 自訂丹麥文分析器

您可以使用下列命令建立自訂丹麥文分析器：

```json
PUT /danish-index
{
  "settings": {
    "analysis": {
      "filter": {
        "danish_stop": {
          "type": "stop",
          "stopwords": "_danish_"
        },
        "danish_stemmer": {
          "type": "stemmer",
          "language": "danish"
        },
        "danish_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "danish_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "danish_stop",
            "danish_keywords",
            "danish_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "danish_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /danish-index/_analyze
{
  "field": "content",
  "text": "Studerende studerer på de danske universiteter. Deres numre er 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "stud",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "stud",
      "start_offset": 11,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "dansk",
      "start_offset": 26,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "universitet",
      "start_offset": 33,
      "end_offset": 46,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "numr",
      "start_offset": 54,
      "end_offset": 59,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "123456",
      "start_offset": 63,
      "end_offset": 69,
      "type": "<NUM>",
      "position": 9
    }
  ]
}
```