---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "立陶宛語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 230
---

# 立陶宛語分析器

您可以使用下列命令，將內建的 `lithuanian` 分析器套用至文字欄位：

```json
PUT /lithuanian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "lithuanian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_lithuanian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_lithuanian_analyzer": {
          "type": "lithuanian",
          "stem_exclusion": ["autoritetas", "patvirtinimas"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 立陶宛語分析器內部結構

`lithuanian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（立陶宛語）
  - keyword
  - stemmer（立陶宛語）

## 自訂立陶宛語分析器

您可以使用下列命令建立自訂立陶宛語分析器：

```json
PUT /lithuanian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "lithuanian_stop": {
          "type": "stop",
          "stopwords": "_lithuanian_"
        },
        "lithuanian_stemmer": {
          "type": "stemmer",
          "language": "lithuanian"
        },
        "lithuanian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "lithuanian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "lithuanian_stop",
            "lithuanian_keywords",
            "lithuanian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "lithuanian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /lithuanian-index/_analyze
{
  "field": "content",
  "text": "Studentai mokosi Lietuvos universitetuose. Jų numeriai yra 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "student","start_offset": 0,"end_offset": 9,"type": "<ALPHANUM>","position": 0},
    {"token": "mok","start_offset": 10,"end_offset": 16,"type": "<ALPHANUM>","position": 1},
    {"token": "lietuv","start_offset": 17,"end_offset": 25,"type": "<ALPHANUM>","position": 2},
    {"token": "universitet","start_offset": 26,"end_offset": 41,"type": "<ALPHANUM>","position": 3},
    {"token": "num","start_offset": 46,"end_offset": 54,"type": "<ALPHANUM>","position": 5},
    {"token": "123456","start_offset": 59,"end_offset": 65,"type": "<NUM>","position": 7}
  ]
}
```