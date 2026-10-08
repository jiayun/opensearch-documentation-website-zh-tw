---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Limit
parent: Token filters
nav_order: 250
---

# Limit 詞元篩選器

`limit` 詞元篩選器用於限制通過分析鏈的詞元數量。

## 參數

`limit` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`max_token_count` | 選用 | 整數 | 要產生的詞元數量上限。預設為 `1`。
`consume_all_tokens` | 選用 | 布林值 | （專家級設定）使用斷詞器產生的所有詞元，即使結果超過 `max_token_count` 也是如此。設定此參數時，輸出仍只包含 `max_token_count` 所指定數量的詞元。不過，斷詞器產生的所有詞元都會經過處理。預設為 `false`。

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `limit` 篩選器的分析器：

```json
PUT my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "three_token_limit": {
          "tokenizer": "standard",
          "filter": [ "custom_token_limit" ]
        }
      },
      "filter": {
        "custom_token_limit": {
          "type": "limit",
          "max_token_count": 3
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器產生的詞元：

```json
GET /my_index/_analyze
{
  "analyzer": "three_token_limit",
  "text": "OpenSearch is a powerful and flexible search engine."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "OpenSearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 11,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "a",
      "start_offset": 14,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```
