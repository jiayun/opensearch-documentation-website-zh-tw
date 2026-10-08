---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Shingle
parent: Token filters
nav_order: 370
---

# Shingle 詞元篩選器

`shingle` 詞元篩選器用於從輸入文字產生單字 n-gram，也就是 _shingle_。例如，對於字串 `slow green turtle`，`shingle` 篩選器會建立下列由一個和兩個單字組成的 shingle：`slow`、`slow green`、`green`、`green turtle` 和 `turtle`。

此詞元篩選器通常會與其他篩選器搭配使用，透過將片語而非個別詞元編製索引來提升搜尋準確度。如需詳細資訊，請參閱[片語建議器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/#phrase-suggester)。

## 參數

`shingle` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min_shingle_size` | 選用 | 整數 | 要串接的詞元數量下限。預設為 `2`。
`max_shingle_size` | 選用 | 整數 | 要串接的詞元數量上限。預設為 `2`。
`output_unigrams` | 選用 | 布林值 | 是否在輸出中包含 unigram（個別詞元）。預設為 `true`。
`output_unigrams_if_no_shingles` | 選用 | 布林值 | 若未產生任何 shingle，是否輸出 unigram。預設為 `false`。
`token_separator` | 選用 | 字串 |  用於將詞元串接成 shingle 的分隔符號。預設為空格（`" "`）。
`filler_token` | 選用 | 字串 | 插入空白位置或詞元之間間隙的詞元。預設為底線（`_`）。

若 `output_unigrams` 和 `output_unigrams_if_no_shingles` 都設為 `true`，則會忽略 `output_unigrams_if_no_shingles`。
{: .note}

## 範例

下列範例請求會建立名為 `my-shingle-index` 的新索引，並設定含有 `shingle` 篩選器的分析器：

```json
PUT /my-shingle-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_shingle_filter": {
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 2,
          "output_unigrams": true
        }
      },
      "analyzer": {
        "my_shingle_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_shingle_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用此分析器所產生的詞元：

```json
GET /my-shingle-index/_analyze
{
  "analyzer": "my_shingle_analyzer",
  "text": "slow green turtle"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "slow",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow green",
      "start_offset": 0,
      "end_offset": 10,
      "type": "shingle",
      "position": 0,
      "positionLength": 2
    },
    {
      "token": "green",
      "start_offset": 5,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "green turtle",
      "start_offset": 5,
      "end_offset": 17,
      "type": "shingle",
      "position": 1,
      "positionLength": 2
    },
    {
      "token": "turtle",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```