---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "印地語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 190
---

# 印地語分析器

您可以使用下列命令，將內建的 `hindi` 分析器套用至文字欄位：

```json
PUT /hindi-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "hindi"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，在此語言分析器中使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_hindi_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_hindi_analyzer": {
          "type": "hindi",
          "stem_exclusion": ["अधिकार", "अनुमोदन"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 印地語分析器內部結構

`hindi` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - decimal_digit
  - keyword
  - normalization (indic)
  - normalization（印地語）
  - stop（印地語）
  - stemmer（印地語）

## 自訂印地語分析器

您可以使用下列命令建立自訂印地語分析器：

```json
PUT /hindi-index
{
  "settings": {
    "analysis": {
      "filter": {
        "hindi_stop": {
          "type": "stop",
          "stopwords": "_hindi_"
        },
        "hindi_stemmer": {
          "type": "stemmer",
          "language": "hindi"
        },
        "hindi_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "hindi_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "decimal_digit",
            "hindi_keywords",
            "indic_normalization",
            "hindi_normalization",
            "hindi_stop",
            "hindi_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "hindi_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求，檢查使用此分析器產生的詞元：

```json
POST /hindi-index/_analyze
{
  "field": "content",
  "text": "छात्र भारतीय विश्वविद्यालयों में पढ़ते हैं। उनके नंबर १२३४५६ हैं।"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "छातर",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "भारतिय",
      "start_offset": 6,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "विशवविदयालय",
      "start_offset": 13,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "पढ",
      "start_offset": 33,
      "end_offset": 38,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "नंबर",
      "start_offset": 49,
      "end_offset": 53,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "123456",
      "start_offset": 54,
      "end_offset": 60,
      "type": "<NUM>",
      "position": 8
    }
  ]
}
```