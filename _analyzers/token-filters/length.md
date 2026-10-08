---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "長度"
parent: Token filters
nav_order: 240
---

# 長度詞元篩選器

`length` 詞元篩選器用於從詞元串流中移除不符合指定長度條件（最小值與最大值）的詞元。

## 參數

您可以使用下列參數設定 `length` 詞元篩選器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min` | 選用 | 整數 | 詞元的最小長度。預設值為 `0`。
`max` | 選用 | 整數 | 詞元的最大長度。預設值為 `Integer.MAX_VALUE`（`2147483647`）。
 

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `length` 篩選器的分析器：

```json
PUT my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "only_keep_4_to_10_characters": {
          "tokenizer": "whitespace",
          "filter": [ "length_4_to_10" ]
        }
      },
      "filter": {
        "length_4_to_10": {
          "type": "length",
          "min": 4,
          "max": 10
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
GET /my_index/_analyze
{
  "analyzer": "only_keep_4_to_10_characters",
  "text": "OpenSearch is a great tool!"
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
      "type": "word",
      "position": 0
    },
    {
      "token": "great",
      "start_offset": 16,
      "end_offset": 21,
      "type": "word",
      "position": 3
    },
    {
      "token": "tool!",
      "start_offset": 22,
      "end_offset": 27,
      "type": "word",
      "position": 4
    }
  ]
}
```
