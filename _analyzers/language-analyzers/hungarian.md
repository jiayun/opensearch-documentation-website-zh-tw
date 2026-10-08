---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匈牙利文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 200
---

# 匈牙利文分析器

您可以使用以下命令，將內建的 `hungarian` 分析器套用至文字欄位：

```json
PUT /hungarian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "hungarian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用以下命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_hungarian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_hungarian_analyzer": {
          "type": "hungarian",
          "stem_exclusion": ["hatalom", "jóváhagyás"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 匈牙利文分析器內部結構

`hungarian` 分析器由以下元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（匈牙利文）
  - keyword
  - stemmer（匈牙利文）

## 自訂匈牙利文分析器

您可以使用以下命令建立自訂匈牙利文分析器：

```json
PUT /hungarian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "hungarian_stop": {
          "type": "stop",
          "stopwords": "_hungarian_"
        },
        "hungarian_stemmer": {
          "type": "stemmer",
          "language": "hungarian"
        },
        "hungarian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "hungarian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "hungarian_stop",
            "hungarian_keywords",
            "hungarian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "hungarian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用以下請求檢查使用該分析器產生的詞元：

```json
POST /hungarian-index/_analyze
{
  "field": "content",
  "text": "A diákok a magyar egyetemeken tanulnak. A számaik 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "diák",
      "start_offset": 2,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "magyar",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "egyetem",
      "start_offset": 18,
      "end_offset": 29,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "tanul",
      "start_offset": 30,
      "end_offset": 38,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "szám",
      "start_offset": 42,
      "end_offset": 49,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "123456",
      "start_offset": 50,
      "end_offset": 56,
      "type": "<NUM>",
      "position": 8
    }
  ]
}
```