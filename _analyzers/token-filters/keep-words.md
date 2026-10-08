---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "保留字詞"
parent: Token filters
nav_order: 190
---

# 保留字詞詞元篩選器

`keep_words` 詞元篩選器的用途是在分析過程中僅保留特定字詞。如果您有大量文字，但只關注其中的特定關鍵字或術語，此篩選器就很實用。

## 參數

您可以使用下列參數設定 `keep_words` 詞元篩選器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`keep_words` |  未設定 `keep_words_path` 時為必要 | 字串清單 | 要保留的字詞清單。
`keep_words_path` | 未設定 `keep_words` 時為必要 | 字串 | 包含要保留之字詞清單的檔案路徑。
`keep_words_case` | 選用 | 布林值 | 是否在比較時將所有字詞轉換為小寫。預設為 `false`。
 

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `keep_words` 篩選器的分析器：

```json
PUT my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_keep_word": {
          "tokenizer": "standard",
          "filter": [ "keep_words_filter" ]
        }
      },
      "filter": {
        "keep_words_filter": {
          "type": "keep",
          "keep_words": ["example", "world", "opensearch"],
          "keep_words_case": true
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器所產生的詞元：

```json
GET /my_index/_analyze
{
  "analyzer": "custom_keep_word",
  "text": "Hello, world! This is an OpenSearch example."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "world",
      "start_offset": 7,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "OpenSearch",
      "start_offset": 25,
      "end_offset": 35,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "example",
      "start_offset": 36,
      "end_offset": 43,
      "type": "<ALPHANUM>",
      "position": 6
    }
  ]
}
```
