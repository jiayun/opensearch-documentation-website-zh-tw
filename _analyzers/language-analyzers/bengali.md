---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "孟加拉語"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 40
---

# 孟加拉語分析器

您可以使用下列命令，將內建的 `bengali` 分析器套用至文字欄位：

```json
PUT /bengali-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "bengali"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_bengali_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_bengali_analyzer": {
          "type": "bengali",
          "stem_exclusion": ["কর্তৃপক্ষ", "অনুমোদন"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 孟加拉語分析器內部結構

`bengali` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - lowercase
  - decimal_digit
  - indic_normalization
  - normalization（孟加拉語）
  - stop（孟加拉語）
  - keyword
  - stemmer（孟加拉語）

## 自訂孟加拉語分析器

您可以使用下列命令建立自訂孟加拉語分析器：

```json
PUT /bengali-index
{
  "settings": {
    "analysis": {
      "filter": {
        "bengali_stop": {
          "type": "stop",
          "stopwords": "_bengali_"
        },
        "bengali_stemmer": {
          "type": "stemmer",
          "language": "bengali"
        },
        "bengali_keywords": {
          "type":       "keyword_marker",
          "keywords":   [] 
        }
      },
      "analyzer": {
        "bengali_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "decimal_digit",
            "bengali_keywords",
            "indic_normalization",
            "bengali_normalization",
            "bengali_stop",
            "bengali_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "bengali_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /bengali-index/_analyze
{
  "field": "content",
  "text": "ছাত্ররা বিশ্ববিদ্যালয়ে পড়াশোনা করে। তাদের নম্বরগুলি ১২৩৪৫৬।"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "ছাত্র","start_offset": 0,"end_offset": 7,"type": "<ALPHANUM>","position": 0},
    {"token": "বিসসবিদালয়","start_offset": 8,"end_offset": 23,"type": "<ALPHANUM>","position": 1},
    {"token": "পরাসোন","start_offset": 24,"end_offset": 32,"type": "<ALPHANUM>","position": 2},
    {"token": "তা","start_offset": 38,"end_offset": 43,"type": "<ALPHANUM>","position": 4},
    {"token": "নমমর","start_offset": 44,"end_offset": 53,"type": "<ALPHANUM>","position": 5},
    {"token": "123456","start_offset": 54,"end_offset": 60,"type": "<NUM>","position": 6}
  ]
}
```