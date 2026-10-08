---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "阿拉伯文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 10
---

# 阿拉伯文分析器

您可以使用下列命令，將內建的 `arabic` 分析器套用至文字欄位：

```json
PUT /arabic-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "arabic"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_arabic
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_arabic_analyzer":{
          "type":"arabic",
          "stem_exclusion":["تكنولوجيا","سلطة "]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 阿拉伯文分析器內部結構

`arabic` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - decimal_digit
  - stop（阿拉伯文）
  - normalization（阿拉伯文）
  - keyword
  - stemmer（阿拉伯文）

## 自訂阿拉伯文分析器

您可以使用下列命令建立自訂阿拉伯文分析器：

```json
PUT /arabic-index
{
  "settings": {
    "analysis": {
      "filter": {
        "arabic_stop": {
          "type": "stop",
          "stopwords": "_arabic_"
        },
        "arabic_stemmer": {
          "type": "stemmer",
          "language": "arabic"
        },
        "arabic_normalization": {
          "type": "arabic_normalization"
        },
        "decimal_digit": {
          "type": "decimal_digit"
        },
        "arabic_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "arabic_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "decimal_digit",
            "arabic_stop",
            "arabic_normalization",
            "arabic_keywords",
            "arabic_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "arabic_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /arabic-index/_analyze
{
  "field": "content",
  "text": "الطلاب يدرسون في الجامعات العربية. أرقامهم ١٢٣٤٥٦."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "طلاب",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "يدرس",
      "start_offset": 7,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "جامع",
      "start_offset": 17,
      "end_offset": 25,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "عرب",
      "start_offset": 26,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "ارقامهم",
      "start_offset": 35,
      "end_offset": 42,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "123456",
      "start_offset": 43,
      "end_offset": 49,
      "type": "<NUM>",
      "position": 6
    }
  ]
}
```