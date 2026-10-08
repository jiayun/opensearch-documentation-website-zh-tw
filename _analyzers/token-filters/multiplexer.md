---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Multiplexer
parent: Token filters
nav_order: 280
---

# Multiplexer 詞元篩選器

`multiplexer` 詞元篩選器可讓您套用不同的篩選器，為同一個詞元建立多個版本。當您想以多種方式分析同一個詞元時，這項功能非常實用。例如，您可能想使用不同的詞幹提取、同義詞或 n-gram 篩選器來分析某個詞元，並一併使用所有產生的詞元。此詞元篩選器的運作方式是複製詞元串流，並對每個副本套用不同的篩選器。

`multiplexer` 詞元篩選器會從詞元串流中移除重複的詞元。
{: .important}

`multiplexer` 詞元篩選器不支援多字詞的 `synonym` 或 `synonym_graph` 詞元篩選器，也不支援 `shingle` 詞元篩選器，因為這些篩選器不僅需要分析目前的詞元，還需要分析後續的詞元，才能判斷如何正確轉換輸入。
{: .important}

## 參數

`multiplexer` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`filters` | 選用 | 字串清單 | 以逗號分隔的詞元篩選器清單，會套用至詞元串流的每個副本。預設為空清單。
`preserve_original` | 選用 | 布林值 | 是否將原始詞元保留為輸出之一。預設為 `true`。

## 範例

下列範例請求會建立名為 `multiplexer_index` 的新索引，並設定一個使用 `multiplexer` 篩選器的分析器：

```json
PUT /multiplexer_index
{
  "settings": {
    "analysis": {
      "filter": {
        "english_stemmer": {
          "type": "stemmer",
          "name": "english"
        },
        "synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "quick,fast"
          ]
        },
        "multiplexer_filter": {
          "type": "multiplexer",
          "filters": ["english_stemmer", "synonym_filter"],
          "preserve_original": true
        }
      },
      "analyzer": {
        "multiplexer_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "multiplexer_filter"
          ]
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
POST /multiplexer_index/_analyze
{
  "analyzer": "multiplexer_analyzer",
  "text": "The slow turtle hides from the quick dog"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow",
      "start_offset": 4,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "turtle",
      "start_offset": 9,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "turtl",
      "start_offset": 9,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "hides",
      "start_offset": 16,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "hide",
      "start_offset": 16,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "from",
      "start_offset": 22,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "the",
      "start_offset": 27,
      "end_offset": 30,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "quick",
      "start_offset": 31,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "fast",
      "start_offset": 31,
      "end_offset": 36,
      "type": "SYNONYM",
      "position": 6
    },
    {
      "token": "dog",
      "start_offset": 37,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 7
    }
  ]
}
```
