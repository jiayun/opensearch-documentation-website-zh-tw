---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Shingle
parent: Token filters
nav_order: 370
---

# Shingle 詞元篩選器

`shingle` 詞元篩選器用於從輸入文字產生字詞 n-gram，即 _shingle_。例如，對於字串 `slow green turtle`，`shingle` 篩選器會建立下列一詞與兩詞的 shingle：`slow`、`slow green`、`green`、`green turtle` 和 `turtle`。

此詞元篩選器常與其他篩選器搭配使用，透過將片語（而非個別詞元）編製索引來提升搜尋準確度。如需更多資訊，請參閱 [Phrase suggester]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/#phrase-suggester)。

若要加速 [`match_phrase`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/) 等片語查詢，請在 `text` 欄位上設定 [`index_phrases`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-phrases/) 對應參數。OpenSearch 接著會在獨立的子欄位中為兩詞 shingle 編製索引，並使用它們執行片語查詢，因此您不需要包含 `shingle` 篩選器的自訂分析器。
{: .tip}

## 參數

`shingle` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min_shingle_size` | 選用 | 整數 | 要串接的詞元數量下限。預設為 `2`。
`max_shingle_size` | 選用 | 整數 | 要串接的詞元數量上限。`max_shingle_size` 與 `min_shingle_size` 的差值，若 `output_unigrams` 為 `true` 時再加 1，不得超過 [`index.max_shingle_diff`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings) 索引設定（預設為 `3`）。因此在預設設定下，`max_shingle_size` 最多只能比 `min_shingle_size` 多 2。預設為 `2`。
`output_unigrams` | 選用 | 布林值 | 是否將單一詞元（個別詞元）納入輸出。預設為 `true`。
`output_unigrams_if_no_shingles` | 選用 | 布林值 | 若未產生任何 shingle，是否輸出單一詞元。預設為 `false`。
`token_separator` | 選用 | 字串 | 用於將詞元串接成 shingle 的分隔符號。預設為空格（`" "`）。
`filler_token` | 選用 | 字串 | 插入空白位置或詞元間隙的詞元。當先前的篩選器（例如 [`stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stop/)）移除某個詞元時，就會產生間隙。填充詞元只會出現在 shingle 內，絕不會以個別詞元的形式輸出。例如，若 `on` 是停用詞，且 `filler_token` 為 `+`，則文字 `tent on sale` 會產生詞元 `tent`、`tent +`、`+ sale` 和 `sale`。預設為底線（`_`）。

若 `output_unigrams` 與 `output_unigrams_if_no_shingles` 都設為 `true`，則會忽略 `output_unigrams_if_no_shingles`。
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