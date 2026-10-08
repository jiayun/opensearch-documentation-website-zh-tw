---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Edge n-gram
parent: Token filters
nav_order: 120
---
# Edge n-gram 詞元篩選器
`edge_ngram` 詞元篩選器與 `ngram` 詞元篩選器非常相似，兩者都會將特定字串分割成不同長度的子字串。不過，`edge_ngram` 詞元篩選器只會從詞元的開頭（邊緣）產生 n-gram（子字串）。在自動完成或前綴比對等情境中，當您希望在使用者輸入時比對字詞或片語的開頭，這個篩選器特別實用。

## 參數

`edge_ngram` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min_gram` | 選用 | 整數 | 要產生的 n-gram 最小長度。預設為 `1`。
`max_gram` | 選用 | 整數 | 要產生的 n-gram 最大長度。`edge_ngram` 篩選器的預設為 `1`，自訂詞元篩選器的預設為 `2`。請避免將此參數設為過低的值。如果值設得太低，只會產生非常短的 n-gram，導致找不到搜尋詞彙。例如，如果將 `max_gram` 設為 `3`，並將「banana」這個字編製索引，產生的最長詞元會是「ban」。如果使用者搜尋「banana」，將不會傳回任何相符結果。您可以使用 `truncate` 詞元篩選器作為搜尋分析器，以降低此風險。
`preserve_original` | 選用 | 布林值 | 在輸出中包含原始詞元。預設為 `false`。

## 範例

下列範例請求會建立名為 `edge_ngram_example` 的新索引，並設定使用 `edge_ngram` 篩選器的分析器：

```json
PUT /edge_ngram_example
{
  "settings": {
    "analysis": {
      "filter": {
        "my_edge_ngram": {
          "type": "edge_ngram",
          "min_gram": 3,
          "max_gram": 4
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "my_edge_ngram"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
POST /edge_ngram_example/_analyze
{
  "analyzer": "my_analyzer",
  "text": "slow green turtle"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "slo",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "gre",
      "start_offset": 5,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "gree",
      "start_offset": 5,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "tur",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "turt",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```
