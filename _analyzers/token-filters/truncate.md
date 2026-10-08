---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Truncate
parent: Token filters
nav_order: 440
---

# Truncate 詞元篩選器

`truncate` 詞元篩選器用於縮短超過指定長度的詞元。它會將詞元修剪至最大字元數，確保超過此限制的詞元會被截斷。

## 參數

`truncate` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`length` | 選用 | 整數 | 指定所產生詞元的最大長度。預設為 `10`。

## 範例

下列範例請求會建立名為 `truncate_example` 的新索引，並設定一個具有 `truncate` 篩選器的分析器：

```json
PUT /truncate_example
{
  "settings": {
    "analysis": {
      "filter": {
        "truncate_filter": {
          "type": "truncate",
          "length": 5
        }
      },
      "analyzer": {
        "truncate_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "truncate_filter"
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
GET /truncate_example/_analyze
{
  "analyzer": "truncate_analyzer",
  "text": "OpenSearch is powerful and scalable"
}

```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opens",
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
      "token": "power",
      "start_offset": 14,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "and",
      "start_offset": 23,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "scala",
      "start_offset": 27,
      "end_offset": 35,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```
