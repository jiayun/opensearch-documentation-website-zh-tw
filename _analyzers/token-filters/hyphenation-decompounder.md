---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Hyphenation decompounder
parent: Token filters
nav_order: 170
---

# Hyphenation decompounder 詞元篩選器

`hyphenation_decompounder` 詞元篩選器用於將複合字拆解為其組成部分。此篩選器特別適用於德文、荷蘭文和瑞典文等常見複合字的語言。此篩選器使用斷字模式（通常定義於 .xml 檔案中）來找出複合字中可拆分為各個組成部分的可能位置，接著將這些組成部分與提供的字典進行比對。若相符，這些組成部分即視為有效的詞元。如需有關斷字模式檔案的詳細資訊，請參閱 [Apache Formatting Objects Processor (FOP) XML 斷字模式](https://offo.sourceforge.net/#FOP+XML+Hyphenation+Patterns)。

## 參數

`hyphenation_decompounder` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`hyphenation_patterns_path` | 必要 | 字串 | 斷字模式檔案的路徑（相對於 `config` 目錄的相對路徑或絕對路徑），此檔案包含特定語言的拆字規則。此檔案通常為 XML 格式。範例檔案可從 [OFFO SourceForge 專案](https://sourceforge.net/projects/offo/)下載。
`word_list` | 若未設定 `word_list_path` 則為必要 | 字串陣列 | 用於驗證斷字模式所產生之組成部分的字詞清單。
`word_list_path` | 若未設定 `word_list` 則為必要 | 字串 | 子字清單的路徑（相對於 `config` 目錄的相對路徑或絕對路徑）。
`max_subword_size` | 選用 | 整數 | 子字的最大長度。若產生的子字超過此長度，則不會加入產生的詞元中。預設為 `15`。
`min_subword_size` | 選用 | 整數 | 子字的最小長度。若產生的子字短於指定長度，則不會加入產生的詞元中。預設為 `2`。
`min_word_size` | 選用 | 整數 | 字詞的最小字元長度。短於此長度的字詞詞元不會被拆解為子字。預設為 `5`。
`only_longest_match` | 選用 | 布林值 | 產生的詞元中僅包含最長的子字。預設為 `false`。

## 範例

下列範例請求會建立名為 `test_index` 的新索引，並設定具有 `hyphenation_decompounder` 篩選器的分析器：

```json
PUT /test_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_hyphenation_decompounder": {
          "type": "hyphenation_decompounder",
          "hyphenation_patterns_path": "analysis/hyphenation_patterns.xml",
          "word_list": ["notebook", "note", "book"],
          "min_subword_size": 3,
          "min_word_size": 5,
          "only_longest_match": false
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_hyphenation_decompounder"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST /test_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "notebook"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "notebook",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "note",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "book",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```
