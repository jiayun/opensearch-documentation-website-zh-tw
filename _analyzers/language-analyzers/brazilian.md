---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "巴西葡萄牙語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 50
---

# 巴西葡萄牙語分析器

您可以使用下列命令，將內建的 `brazilian` 分析器套用至文字欄位：

```json
PUT /brazilian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "brazilian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_brazilian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_brazilian_analyzer": {
          "type": "brazilian",
          "stem_exclusion": ["autoridade", "aprovação"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 巴西葡萄牙語分析器內部結構

`brazilian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - stop（巴西葡萄牙語）
  - keyword
  - stemmer（巴西葡萄牙語）

## 自訂巴西葡萄牙語分析器

您可以使用下列命令建立自訂的巴西葡萄牙語分析器：

```json
PUT /brazilian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "brazilian_stop": {
          "type": "stop",
          "stopwords": "_brazilian_"
        },
        "brazilian_stemmer": {
          "type": "stemmer",
          "language": "brazilian"
        },
        "brazilian_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "brazilian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "brazilian_stop",
            "brazilian_keywords",
            "brazilian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "brazilian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器所產生的詞元：

```json
POST /brazilian-index/_analyze
{
  "field": "content",
  "text": "Estudantes estudam em universidades brasileiras. Seus números são 123456."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "estudant","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
    {"token": "estud","start_offset": 11,"end_offset": 18,"type": "<ALPHANUM>","position": 1},
    {"token": "univers","start_offset": 22,"end_offset": 35,"type": "<ALPHANUM>","position": 3},
    {"token": "brasileir","start_offset": 36,"end_offset": 47,"type": "<ALPHANUM>","position": 4},
    {"token": "numer","start_offset": 54,"end_offset": 61,"type": "<ALPHANUM>","position": 6},
    {"token": "sao","start_offset": 62,"end_offset": 65,"type": "<ALPHANUM>","position": 7},
    {"token": "123456","start_offset": 66,"end_offset": 72,"type": "<NUM>","position": 8}
  ]
}
```