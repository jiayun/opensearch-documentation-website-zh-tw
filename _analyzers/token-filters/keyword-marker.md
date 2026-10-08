---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Keyword marker
parent: Token filters
nav_order: 200
---

# Keyword marker 詞元篩選器

`keyword_marker` 詞元篩選器用於防止特定詞元被詞幹分析器或其他篩選器修改。`keyword_marker` 詞元篩選器會將指定的詞元標記為 `keywords`，藉此避免任何詞幹提取或其他處理，確保特定字詞維持原始形式。

## 參數

`keyword_marker` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`ignore_case` | 選用 | 布林值 | 比對關鍵字時是否忽略字母大小寫。預設為 `false`。
`keywords` | 若未設定 `keywords_path` 或 `keywords_pattern`，則為必要 | 字串清單 | 要標記為關鍵字的詞元清單。
`keywords_path` | 若未設定 `keywords` 或 `keywords_pattern`，則為必要 | 字串 | 關鍵字清單的路徑（相對於 `config` 目錄的路徑或絕對路徑）。
`keywords_pattern` | 若未設定 `keywords` 或 `keywords_path`，則為必要 | 字串 | 用於比對要標記為關鍵字之詞元的[規則運算式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。
 

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `keyword_marker` 篩選器的分析器。此篩選器會將字詞 `example` 標記為關鍵字：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "keyword_marker_filter", "stemmer"]
        }
      },
      "filter": {
        "keyword_marker_filter": {
          "type": "keyword_marker",
          "keywords": ["example"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器所產生的詞元：

```json
GET /my_index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "Favorite example"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元。請注意，字詞 `favorite` 經過了詞幹提取，但字詞 `example` 因為已被標記為關鍵字，所以未經詞幹提取：

```json
{
  "tokens": [
    {
      "token": "favorit",
      "start_offset": 0,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "example",
      "start_offset": 9,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

您可以在 `_analyze` 查詢中加入下列參數，進一步檢查 `keyword_marker` 詞元篩選器的影響：

```json
GET /my_index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "This is an OpenSearch example demonstrating keyword marker.",
  "explain": true,
  "attributes": "keyword"
}
```
{% include copy-curl.html %}

這會在回應中產生額外的詳細資訊，類似如下：

```json
{
    "name": "porter_stem",
    "tokens": [
      ...
      {
        "token": "example",
        "start_offset": 22,
        "end_offset": 29,
        "type": "<ALPHANUM>",
        "position": 4,
        "keyword": true
      },
      {
        "token": "demonstr",
        "start_offset": 30,
        "end_offset": 43,
        "type": "<ALPHANUM>",
        "position": 5,
        "keyword": false
      },
      ...
    ]
}
```
