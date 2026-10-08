---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模式取代"
parent: Token filters
nav_order: 320
---

# 模式取代詞元篩選器

`pattern_replace` 詞元篩選器可讓您使用規則運算式修改詞元。此篩選器會以指定的值取代詞元中的模式，讓您在將詞元編製索引之前，能彈性地轉換或正規化詞元。當您需要在分析期間清理文字或將文字標準化時，此篩選器特別實用。

## 參數

`pattern_replace` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 必要 | 字串 | 規則運算式模式，用於比對需要取代的文字。
`all` | 選用 | 布林值 | 是否取代所有符合模式的項目。若為 `false`，則只會取代第一個符合項目。預設為 `true`。
`replacement` | 選用 | 字串 | 用來取代符合模式之內容的字串。預設為空字串。


## 範例

下列範例請求會建立名為 `text_index` 的新索引，並設定一個使用 `pattern_replace` 篩選器的分析器，將包含數字的詞元取代為字串 `[NUM]`：

```json
PUT /text_index
{
  "settings": {
    "analysis": {
      "filter": {
        "number_replace_filter": {
          "type": "pattern_replace",
          "pattern": "\\d+",
          "replacement": "[NUM]"
        }
      },
      "analyzer": {
        "number_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "number_replace_filter"
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
POST /text_index/_analyze
{
  "text": "Visit us at 98765 Example St.",
  "analyzer": "number_analyzer"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "visit",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "us",
      "start_offset": 6,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "at",
      "start_offset": 9,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "[NUM]",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<NUM>",
      "position": 3
    },
    {
      "token": "example",
      "start_offset": 18,
      "end_offset": 25,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "st",
      "start_offset": 26,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 5
    }
  ]
}
```
