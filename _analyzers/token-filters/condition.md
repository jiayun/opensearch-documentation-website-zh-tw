---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Condition
parent: Token filters
nav_order: 70
---

# Condition 詞元篩選器

`condition` 詞元篩選器是一種特殊類型的篩選器，可讓您根據特定條件有條件地套用其他詞元篩選器。這讓您在文字分析期間，能更精確地控制何時應套用特定詞元篩選器。
您可以設定多個篩選器，且只有在符合您定義的條件時才會套用這些篩選器。 
此詞元篩選器對於特定語言的處理及特殊字元的處理非常實用。


## 參數

若要使用 `condition` 詞元篩選器，必須設定兩個參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`filter` | 必要 | 陣列 | 指定在符合指定條件（由 `script` 參數定義）時，應對詞元套用哪些詞元篩選器。
`script` | 必要 | 物件 | 設定一個[內嵌指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/)，用於定義套用 `filter` 參數中指定的篩選器所需符合的條件（僅接受內嵌指令碼）。


## 範例

以下範例請求會建立名為 `my_conditional_index` 的新索引，並設定一個具有 `condition` 篩選器的分析器。此篩選器會對任何包含字元序列「um」的詞元套用 `lowercase` 篩選器：

```json
PUT /my_conditional_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_conditional_filter": {
          "type": "condition",
          "filter": ["lowercase"],
          "script": {
            "source": "token.getTerm().toString().contains('um')"
          }
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "my_conditional_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用以下請求來檢查使用此分析器所產生的詞元：

```json
GET /my_conditional_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "THE BLACK CAT JUMPS OVER A LAZY DOG"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "THE",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "BLACK",
      "start_offset": 4,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "CAT",
      "start_offset": 10,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "jumps",
      "start_offset": 14,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "OVER",
      "start_offset": 20,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "A",
      "start_offset": 25,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "LAZY",
      "start_offset": 27,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "DOG",
      "start_offset": 32,
      "end_offset": 35,
      "type": "<ALPHANUM>",
      "position": 7
    }
  ]
}
```

