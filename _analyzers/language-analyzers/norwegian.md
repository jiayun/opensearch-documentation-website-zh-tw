---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "挪威語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 240
---

# 挪威語分析器

您可以使用下列命令，將內建的 `norwegian` 分析器套用至文字欄位：

```json
PUT /norwegian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "norwegian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，將 `stem_exclusion` 搭配此語言分析器使用：

```json
PUT index_with_stem_exclusion_norwegian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_norwegian_analyzer": {
          "type": "norwegian",
          "stem_exclusion": ["autoritet", "godkjenning"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 挪威語分析器內部結構

`norwegian` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop (挪威語)
  - keyword
  - stemmer (挪威語)

## 自訂挪威語分析器

您可以使用下列命令建立自訂挪威語分析器：

```json
PUT /norwegian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "norwegian_stop": {
          "type": "stop",
          "stopwords": "_norwegian_"
        },
        "norwegian_stemmer": {
          "type": "stemmer",
          "language": "norwegian"
        },
        "norwegian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "norwegian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "norwegian_stop",
            "norwegian_keywords",
            "norwegian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "norwegian_analyzer"
      }
    }
  }
}

```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /norwegian-index/_analyze
{
  "field": "content",
  "text": "Studentene studerer ved norske universiteter. Deres nummer er 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "student","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
    {"token": "studer","start_offset": 11,"end_offset": 19,"type": "<ALPHANUM>","position": 1},
    {"token": "norsk","start_offset": 24,"end_offset": 30,"type": "<ALPHANUM>","position": 3},
    {"token": "universitet","start_offset": 31,"end_offset": 44,"type": "<ALPHANUM>","position": 4},
    {"token": "numm","start_offset": 52,"end_offset": 58,"type": "<ALPHANUM>","position": 6},
    {"token": "123456","start_offset": 62,"end_offset": 68,"type": "<NUM>","position": 8}
  ]
}
```