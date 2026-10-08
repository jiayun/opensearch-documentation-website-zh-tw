---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模式取代"
parent: Character filters
nav_order: 130
---

# 模式取代字元篩選器

`pattern_replace` 字元篩選器可讓您使用規則運算式定義模式，以比對並取代輸入文字中的字元。它是進行進階文字轉換的彈性工具，在處理複雜的字串模式時特別實用。

此篩選器會將模式的所有出現處取代為指定的取代字串，讓您能輕鬆對輸入文字進行替換、刪除或複雜的修改。您可以在斷詞之前使用它將輸入正規化。

## 範例

若要將電話號碼標準化，您將使用規則運算式 `[\\s()-]+`：

- `[ ]`：定義一個**字元類別**，表示它會比對括號內字元中的**任一個**。
- `\\s`：比對任何**空白**字元，例如空格、定位字元或換行字元。
- `()`：比對字面上的**括號**（`(` 或 `)`）。
- `-`：比對字面上的**連字號**（`-`）。
- `+`：指定模式應比對前述字元的**一次或多次**出現。

模式 `[\\s()-]+` 會比對由一個或多個空白字元、括號或連字號組成的任何序列，並將其從輸入文字中移除。這可確保電話號碼經過正規化，且只包含數字。

下列請求會移除空格、破折號和括號，藉此將電話號碼標準化：

```json
GET /_analyze
{
  "tokenizer": "standard",
  "char_filter": [
    {
      "type": "pattern_replace",
      "pattern": "[\\s()-]+",
      "replacement": ""
    }
  ],
  "text": "(555) 123-4567"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "5551234567",
      "start_offset": 1,
      "end_offset": 14,
      "type": "<NUM>",
      "position": 0
    }
  ]
}
```
 
## 參數

`pattern_replace` 字元篩選器必須使用下列參數進行設定。

| 參數 | 必要/選用 | 資料類型 | 說明 |
|:---|:---|
| `pattern` | 必要 | 字串 | 用於比對輸入文字部分內容的規則運算式。篩選器會識別並比對此模式以執行取代。 |
| `replacement` | 選用 | 字串 | 用來取代模式比對結果的字串。使用空字串（`""`）可移除比對到的文字。預設為空字串（`""`）。 |

## 建立自訂分析器

下列請求會建立一個索引，其中包含以 `pattern_replace` 字元篩選器設定的自訂分析器。此篩選器會移除數字中的貨幣符號和千位分隔符號（包括歐式的 `.` 和美式的 `,`）：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "standard",
          "char_filter": [
            "pattern_char_filter"
          ]
        }
      },
      "char_filter": {
        "pattern_char_filter": {
          "type": "pattern_replace",
          "pattern": "[$€,.]",
          "replacement": ""
        }
      }
    }
  }
}
```

{% include copy-curl.html %}

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "Total: $ 1,200.50 and € 1.100,75"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Total",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "120050",
      "start_offset": 9,
      "end_offset": 17,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "and",
      "start_offset": 18,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "110075",
      "start_offset": 24,
      "end_offset": 32,
      "type": "<NUM>",
      "position": 3
    }
  ]
}
```

## 使用擷取群組

您可以在 `replacement` 參數中使用擷取群組。例如，下列請求會建立一個自訂分析器，使用 `pattern_replace` 字元篩選器將電話號碼中的連字號取代為點：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "standard",
          "char_filter": [
            "pattern_char_filter"
          ]
        }
      },
      "char_filter": {
        "pattern_char_filter": {
          "type": "pattern_replace",
          "pattern": "(\\d+)-(?=\\d)",
          "replacement": "$1."
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "Call me at 555-123-4567 or 555-987-6543"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Call",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "me",
      "start_offset": 5,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "at",
      "start_offset": 8,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "555.123.4567",
      "start_offset": 11,
      "end_offset": 23,
      "type": "<NUM>",
      "position": 3
    },
    {
      "token": "or",
      "start_offset": 24,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "555.987.6543",
      "start_offset": 27,
      "end_offset": 39,
      "type": "<NUM>",
      "position": 5
    }
  ]
}
```