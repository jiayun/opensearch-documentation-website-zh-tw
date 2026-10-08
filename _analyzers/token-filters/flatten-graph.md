---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "扁平化圖形"
parent: Token filters
nav_order: 150
---

# 扁平化圖形詞元篩選器

`flatten_graph` 詞元篩選器用於處理在圖形結構中，多個詞元產生於同一位置時所形成的複雜詞元關係。部分詞元篩選器（例如 `synonym_graph` 和 `word_delimiter_graph`）會產生多位置詞元，也就是彼此重疊或跨越多個位置的詞元。這些詞元圖形對搜尋查詢很有用，但在編製索引時並不直接支援。`flatten_graph` 詞元篩選器會將多位置詞元解析為線性的詞元序列。將圖形扁平化可確保與編製索引程序相容。

詞元圖形扁平化是一個有損的程序。請盡可能避免使用 `flatten_graph` 篩選器。請改為僅在搜尋分析器中套用圖形詞元篩選器，如此便不需要使用 `flatten_graph` 篩選器。
{: .important}

## 範例

下列範例請求會建立名為 `test_index` 的新索引，並設定一個使用 `flatten_graph` 篩選器的分析器：

```json
PUT /test_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_index_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "my_custom_filter",
            "flatten_graph"
          ]
        }
      },
      "filter": {
        "my_custom_filter": {
          "type": "word_delimiter_graph",
          "catenate_all": true
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
POST /test_index/_analyze
{
  "analyzer": "my_index_analyzer",
  "text": "OpenSearch helped many employers"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "OpenSearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 0,
      "positionLength": 2
    },
    {
      "token": "Open",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "Search",
      "start_offset": 4,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "helped",
      "start_offset": 11,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "many",
      "start_offset": 18,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "employers",
      "start_offset": 23,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```
