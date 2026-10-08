---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞幹還原覆寫"
parent: Token filters
nav_order: 400
---

# 詞幹還原覆寫詞元篩選器

`stemmer_override` 詞元篩選器可讓您定義自訂的詞幹還原規則，以覆寫 Porter 或 Snowball 等預設詞幹還原器的行為。當您想對某些標準詞幹還原演算法可能無法正確處理的單字套用特定的詞幹還原行為時，這項功能就很實用。

## 參數

`stemmer_override` 詞元篩選器必須設定下列參數中的恰好一個。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`rules` | 字串 | 直接在設定中定義覆寫規則。
`rules_path` | 字串 | 指定包含自訂規則（對應）之檔案的路徑。路徑可以是絕對路徑，也可以是相對於 config 目錄的路徑。

## 範例

下列範例請求會建立名為 `my-index` 的新索引，並設定一個使用 `stemmer_override` 篩選器的分析器：

```json
PUT /my-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stemmer_override_filter": {
          "type": "stemmer_override",
          "rules": [
            "running, runner => run",
            "bought => buy",
            "best => good"
          ]
        }
      },
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_stemmer_override_filter"
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
GET /my-index/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "I am a runner and bought the best shoes"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "i",
      "start_offset": 0,
      "end_offset": 1,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "am",
      "start_offset": 2,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "a",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "run",
      "start_offset": 7,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "and",
      "start_offset": 14,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "buy",
      "start_offset": 18,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "the",
      "start_offset": 25,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "good",
      "start_offset": 29,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "shoes",
      "start_offset": 34,
      "end_offset": 39,
      "type": "<ALPHANUM>",
      "position": 8
    }
  ]
}
```