---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "正規化"
parent: Token filters
nav_order: 300
---

# 正規化詞元篩選器

`normalization` 詞元篩選器的用途是調整並簡化文字，以減少變化形式，特別是特殊字元的變化形式。它主要用於將特定語言中的字元標準化，藉此處理書寫上的變化形式。

可用的 `normalization` 詞元篩選器如下：

- [arabic_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/ar/ArabicNormalizationFilter.html)
- [german_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/de/GermanNormalizationFilter.html)
- [hindi_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/hi/HindiNormalizationFilter.html)
- [indic_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/in/IndicNormalizationFilter.html)
- [sorani_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/ckb/SoraniNormalizationFilter.html)
- [persian_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/fa/PersianNormalizationFilter.html)
- [scandinavian_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/miscellaneous/ScandinavianNormalizationFilter.html)
- [scandinavian_folding](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/miscellaneous/ScandinavianFoldingFilter.html)
- [serbian_normalization](https://lucene.apache.org/core/{{site.lucene_version}}/analysis/common/org/apache/lucene/analysis/sr/SerbianNormalizationFilter.html)


## 範例

下列範例請求會建立名為 `german_normalizer_example` 的新索引，並設定含有 `german_normalization` 篩選器的分析器：

```json
PUT /german_normalizer_example
{
  "settings": {
    "analysis": {
      "filter": {
        "german_normalizer": {
          "type": "german_normalization"
        }
      },
      "analyzer": {
        "german_normalizer_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "lowercase", 
            "german_normalizer"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器所產生的詞元：

```json
POST /german_normalizer_example/_analyze
{
  "text": "Straße München",
  "analyzer": "german_normalizer_analyzer"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "strasse",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "munchen",
      "start_offset": 7,
      "end_offset": 14,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```
