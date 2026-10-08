---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CJK
parent: Language analyzers
grand_parent: Analyzers
nav_order: 80
---

# CJK 分析器

內建的 `cjk` 分析器專為中文、日文和韓文 (CJK) 文字而設計。它使用二元語法 (bigram) 斷詞，將 CJK 文字拆解為相互重疊的雙字元序列，這對於不使用空格分隔單字的語言相當有效。

您可能會發現，對於 CJK 文字，ICU 分析外掛程式中的 `icu_analyzer` 效果比 `cjk` 分析器更好。請使用您的文字和查詢進行實驗。
{: .note}

您可以使用下列命令，將 `cjk` 分析器套用至文字欄位：

```json
PUT /cjk-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "cjk"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_cjk_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_cjk_analyzer": {
          "type": "cjk",
          "stem_exclusion": ["example", "words"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## CJK 分析器內部結構

`cjk` 分析器由下列元件建構而成：

- 斷詞器：`standard`

- 詞元篩選器：
  - cjk_width
  - lowercase
  - cjk_bigram
  - stop（與英文類似）

## 自訂 CJK 分析器

您可以使用下列命令建立自訂 CJK 分析器：

```json
PUT /cjk-index
{
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  [ 
            "a", "and", "are", "as", "at", "be", "but", "by", "for",
            "if", "in", "into", "is", "it", "no", "not", "of", "on",
            "or", "s", "such", "t", "that", "the", "their", "then",
            "there", "these", "they", "this", "to", "was", "will",
            "with", "www"
          ]
        }
      },
      "analyzer": {
        "cjk_custom_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "cjk_width",
            "lowercase",
            "cjk_bigram",
            "english_stop"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "cjk_custom_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
POST /cjk-index/_analyze
{
  "field": "content",
  "text": "学生们在中国、日本和韩国的大学学习。123456"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "学生","start_offset": 0,"end_offset": 2,"type": "<DOUBLE>","position": 0},
    {"token": "生们","start_offset": 1,"end_offset": 3,"type": "<DOUBLE>","position": 1},
    {"token": "们在","start_offset": 2,"end_offset": 4,"type": "<DOUBLE>","position": 2},
    {"token": "在中","start_offset": 3,"end_offset": 5,"type": "<DOUBLE>","position": 3},
    {"token": "中国","start_offset": 4,"end_offset": 6,"type": "<DOUBLE>","position": 4},
    {"token": "日本","start_offset": 7,"end_offset": 9,"type": "<DOUBLE>","position": 5},
    {"token": "本和","start_offset": 8,"end_offset": 10,"type": "<DOUBLE>","position": 6},
    {"token": "和韩","start_offset": 9,"end_offset": 11,"type": "<DOUBLE>","position": 7},
    {"token": "韩国","start_offset": 10,"end_offset": 12,"type": "<DOUBLE>","position": 8},
    {"token": "国的","start_offset": 11,"end_offset": 13,"type": "<DOUBLE>","position": 9},
    {"token": "的大","start_offset": 12,"end_offset": 14,"type": "<DOUBLE>","position": 10},
    {"token": "大学","start_offset": 13,"end_offset": 15,"type": "<DOUBLE>","position": 11},
    {"token": "学学","start_offset": 14,"end_offset": 16,"type": "<DOUBLE>","position": 12},
    {"token": "学习","start_offset": 15,"end_offset": 17,"type": "<DOUBLE>","position": 13},
    {"token": "123456","start_offset": 18,"end_offset": 24,"type": "<NUM>","position": 14}
  ]
}
```

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/) -- CJK 文字的替代方案