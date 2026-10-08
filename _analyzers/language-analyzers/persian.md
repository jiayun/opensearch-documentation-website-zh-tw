---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "波斯文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 250
---

# 波斯文分析器

您可以使用下列命令，將內建的 `persian` 分析器套用至文字欄位：

```json
PUT /persian-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "persian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_persian_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_persian_analyzer": {
          "type": "persian",
          "stem_exclusion": ["حکومت", "تأیید"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 波斯文分析器內部結構

`persian` 分析器由下列元件組成：

- 斷詞器：`standard`

- 字元篩選器：`mapping`

- 詞元篩選器：
  - lowercase
  - decimal_digit
  - normalization（阿拉伯文）
  - normalization（波斯文）
  - stop（波斯文）
  - keyword

## 自訂波斯文分析器

您可以使用下列命令建立自訂波斯文分析器：

```json
PUT /persian-index
{
  "settings": {
    "analysis": {
      "filter": {
        "persian_stop": {
          "type": "stop",
          "stopwords": "_persian_"
        },
        "persian_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "char_filter": {
        "null_width_replace_with_space": {
            "type":       "mapping",
            "mappings": [ "\\u200C=>\\u0020"] 
        }
      },
      "analyzer": {
        "persian_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": [ "null_width_replace_with_space" ],
          "filter": [
            "lowercase",
            "decimal_digit",
            "arabic_normalization",
            "persian_normalization",
            "persian_stop",
            "persian_keywords"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "persian_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查分析器產生的詞元：

```json
POST /persian-index/_analyze
{
  "field": "content",
  "text": "دانشجویان در دانشگاه‌های ایرانی تحصیل می‌کنند. شماره‌های آن‌ها ۱۲۳۴۵۶ است."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "دانشجويان","start_offset": 0,"end_offset": 9,"type": "<ALPHANUM>","position": 0},
    {"token": "دانشگاه","start_offset": 13,"end_offset": 20,"type": "<ALPHANUM>","position": 2},
    {"token": "ايراني","start_offset": 25,"end_offset": 31,"type": "<ALPHANUM>","position": 4},
    {"token": "تحصيل","start_offset": 32,"end_offset": 37,"type": "<ALPHANUM>","position": 5},
    {"token": "شماره","start_offset": 47,"end_offset": 52,"type": "<ALPHANUM>","position": 8},
    {"token": "123456","start_offset": 63,"end_offset": 69,"type": "<NUM>","position": 12}
  ]
}
```
