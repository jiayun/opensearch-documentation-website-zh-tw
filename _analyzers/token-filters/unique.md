---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Unique
parent: Token filters
nav_order: 450
---

# Unique 詞元篩選器

`unique` 詞元篩選器可確保在分析過程中只保留唯一的詞元，並移除在單一欄位或文字區塊中出現的重複詞元。

## 參數

`unique` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`only_on_same_position` | 選用 | 布林值 | 若為 `true`，此詞元篩選器會作為 `remove_duplicates` 詞元篩選器運作，且只會移除位於相同位置的詞元。預設值為 `false`。

## 範例

下列範例請求會建立名為 `unique_example` 的新索引，並設定使用 `unique` 篩選器的分析器：

```json
PUT /unique_example
{
  "settings": {
    "analysis": {
      "filter": {
        "unique_filter": {
          "type": "unique",
          "only_on_same_position": false
        }
      },
      "analyzer": {
        "unique_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "unique_filter"
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
GET /unique_example/_analyze
{
  "analyzer": "unique_analyzer",
  "text": "OpenSearch OpenSearch is powerful powerful and scalable"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 22,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "powerful",
      "start_offset": 25,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "and",
      "start_offset": 43,
      "end_offset": 46,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "scalable",
      "start_offset": 47,
      "end_offset": 55,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```
