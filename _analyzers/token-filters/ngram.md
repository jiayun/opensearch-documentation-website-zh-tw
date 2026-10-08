---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: N-gram
parent: Token filters
nav_order: 290
---

# N-gram 詞元篩選器

`ngram` 詞元篩選器是一項強大的工具，可將文字拆解為較小的組成單位，稱為 _n-gram_，藉此提升部分比對與模糊搜尋的能力。其運作方式是將詞元分割為指定長度的較短子字串。這類篩選器常用於搜尋應用程式中，以支援自動完成、部分比對及容錯拼字搜尋。如需更多資訊，請參閱[自動完成功能]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)與[您是不是要找]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/)。

## 參數

`ngram` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min_gram` | 選用 | 整數 | n-gram 的最小長度。預設為 `1`。
`max_gram` | 選用 | 整數 | n-gram 的最大長度。預設為 `2`。
`preserve_original` | 選用 | 布林值 | 是否將原始詞元保留為輸出之一。預設為 `false`。

## 範例

下列範例請求會建立名為 `ngram_example_index` 的新索引，並設定具有 `ngram` 篩選器的分析器：

```json
PUT /ngram_example_index
{
  "settings": {
    "analysis": {
      "filter": {
        "ngram_filter": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      },
      "analyzer": {
        "ngram_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "ngram_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器所產生的詞元：

```json
POST /ngram_example_index/_analyze
{
  "analyzer": "ngram_analyzer",
  "text": "Search"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "se",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "sea",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ea",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ear",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ar",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "arc",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "rc",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "rch",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "ch",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```
