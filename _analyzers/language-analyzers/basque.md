---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巴斯克語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 30
---

# 巴斯克語分析器

您可以使用下列命令，將內建的 `basque` 分析器套用至文字欄位：

```json
PUT /basque-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "basque"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_basque_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_basque_analyzer": {
          "type": "basque",
          "stem_exclusion": ["autoritate", "baldintza"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 巴斯克語分析器內部結構

`basque` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（巴斯克語）
  - keyword
  - stemmer（巴斯克語）

## 自訂巴斯克語分析器

您可以使用下列命令建立自訂巴斯克語分析器：

```json
PUT /basque-index
{
  "settings": {
    "analysis": {
      "filter": {
        "basque_stop": {
          "type": "stop",
          "stopwords": "_basque_"
        },
        "basque_stemmer": {
          "type": "stemmer",
          "language": "basque"
        },
        "basque_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "basque_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "basque_stop",
            "basque_keywords",
            "basque_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "basque_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /basque-index/_analyze
{
  "field": "content",
  "text": "Ikasleek euskal unibertsitateetan ikasten dute. Haien zenbakiak 123456 dira."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "ikasle","start_offset": 0,"end_offset": 8,"type": "<ALPHANUM>","position": 0},
    {"token": "euskal","start_offset": 9,"end_offset": 15,"type": "<ALPHANUM>","position": 1},
    {"token": "unibertsi","start_offset": 16,"end_offset": 33,"type": "<ALPHANUM>","position": 2},
    {"token": "ikas","start_offset": 34,"end_offset": 41,"type": "<ALPHANUM>","position": 3},
    {"token": "haien","start_offset": 48,"end_offset": 53,"type": "<ALPHANUM>","position": 5},
    {"token": "zenba","start_offset": 54,"end_offset": 63,"type": "<ALPHANUM>","position": 6},
    {"token": "123456","start_offset": 64,"end_offset": 70,"type": "<NUM>","position": 7}
  ]
}
```