---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字典複合詞拆分"
parent: Token filters
nav_order: 110
---

# 字典複合詞拆分詞元篩選器

`dictionary_decompounder` 詞元篩選器會根據預先定義的字典，將複合詞拆分為其組成部分。此篩選器特別適用於德文、荷蘭文或芬蘭文等常見複合詞的語言，將複合詞拆解可以提升搜尋相關性。`dictionary_decompounder` 詞元篩選器會根據已知單字清單，判斷每個詞元（單字）是否可以拆分為較小的詞元。如果詞元可以拆分為已知單字，篩選器就會為該詞元產生子詞元。

## 參數

`dictionary_decompounder` 詞元篩選器具有下列參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`word_list` | 必要，除非已設定 `word_list_path` | 字串陣列 | 篩選器用來拆分複合詞的單字字典。
`word_list_path` | 必要，除非已設定 `word_list` | 字串 | 包含字典單字之文字檔案的檔案路徑。可接受絕對路徑，或相對於 `config` 目錄的路徑。字典檔案必須使用 UTF-8 編碼，且每個單字必須各列於單獨的一行。
`min_word_size` | 選用 | 整數 | 複合詞整體納入拆分考量的最小長度。如果複合詞短於此值，則不會被拆分。預設為 `5`。
`min_subword_size` | 選用 | 整數 | 任何子詞的最小長度。如果子詞短於此值，則不會包含在輸出中。預設為 `2`。
`max_subword_size` | 選用 | 整數 | 任何子詞的最大長度。如果子詞長於此值，則不會包含在輸出中。預設為 `15`。
`only_longest_match` | 選用 | 布林值 | 如果設定為 `true`，則只會傳回最長的相符子詞。預設為 `false`。

## 範例

下列範例請求會建立名為 `decompound_example` 的新索引，並設定使用 `dictionary_decompounder` 篩選器的分析器：

```json
PUT /decompound_example
{
  "settings": {
    "analysis": {
      "filter": {
        "my_dictionary_decompounder": {
          "type": "dictionary_decompounder",
          "word_list": ["slow", "green", "turtle"]
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "my_dictionary_decompounder"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器產生的詞元：

```json
POST /decompound_example/_analyze
{
  "analyzer": "my_analyzer",
  "text": "slowgreenturtleswim"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "slowgreenturtleswim",
      "start_offset": 0,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow",
      "start_offset": 0,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "green",
      "start_offset": 0,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "turtle",
      "start_offset": 0,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```
