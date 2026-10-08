---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "荷蘭文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 110
---

# 荷蘭文分析器

您可以使用下列命令，將內建的 `dutch` 分析器套用至文字欄位：

```json
PUT /dutch-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "dutch"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_dutch_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_dutch_analyzer": {
          "type": "dutch",
          "stem_exclusion": ["autoriteit", "goedkeuring"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 荷蘭文分析器內部結構

`dutch` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（荷蘭文）
  - keyword
  - stemmer_override
  - stemmer（荷蘭文）

## 自訂荷蘭文分析器

您可以使用下列命令建立自訂荷蘭文分析器：

```json
PUT /dutch-index
{
  "settings": {
    "analysis": {
      "filter": {
        "dutch_stop": {
          "type": "stop",
          "stopwords": "_dutch_"
        },
        "dutch_stemmer": {
          "type": "stemmer",
          "language": "dutch"
        },
        "dutch_keywords": {
          "type": "keyword_marker",
          "keywords": []
        },
        "dutch_override": {
          "type": "stemmer_override",
          "rules": [
            "fiets=>fiets",
            "bromfiets=>bromfiets",
            "ei=>eier",
            "kind=>kinder"
          ]
        }
      },
      "analyzer": {
        "dutch_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "dutch_stop",
            "dutch_keywords",
            "dutch_override",
            "dutch_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "dutch_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /dutch-index/_analyze
{
  "field": "content",
  "text": "De studenten studeren in Nederland en bezoeken Amsterdam. Hun nummers zijn 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "student","start_offset": 3,"end_offset": 12,"type": "<ALPHANUM>","position": 1},
    {"token": "studer","start_offset": 13,"end_offset": 21,"type": "<ALPHANUM>","position": 2},
    {"token": "nederland","start_offset": 25,"end_offset": 34,"type": "<ALPHANUM>","position": 4},
    {"token": "bezoek","start_offset": 38,"end_offset": 46,"type": "<ALPHANUM>","position": 6},
    {"token": "amsterdam","start_offset": 47,"end_offset": 56,"type": "<ALPHANUM>","position": 7},
    {"token": "nummer","start_offset": 62,"end_offset": 69,"type": "<ALPHANUM>","position": 9},
    {"token": "123456","start_offset": 75,"end_offset": 81,"type": "<NUM>","position": 11}
  ]
}
```