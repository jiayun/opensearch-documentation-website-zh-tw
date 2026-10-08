---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "空白字元"
parent: Tokenizers
nav_order: 160
---

# 空白字元斷詞器

`whitespace` 斷詞器會依空白字元（例如空格、定位字元與換行）分割文字。它將以空白字元分隔的每個單字視為一個詞元，且不執行任何額外的分析或正規化，例如轉為小寫或移除標點符號。

## 範例用法

下列範例請求會建立一個名為 `my_index` 的新索引，並設定一個使用 `whitespace` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "whitespace_tokenizer": {
          "type": "whitespace"
        }
      },
      "analyzer": {
        "my_whitespace_analyzer": {
          "type": "custom",
          "tokenizer": "whitespace_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_whitespace_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視透過該分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_whitespace_analyzer",
  "text": "OpenSearch is fast! Really fast."
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
      "token": "is",
      "start_offset": 11,
      "end_offset": 13,
      "type": "word",
      "position": 1
    },
    {
      "token": "fast!",
      "start_offset": 14,
      "end_offset": 19,
      "type": "word",
      "position": 2
    },
    {
      "token": "Really",
      "start_offset": 20,
      "end_offset": 26,
      "type": "word",
      "position": 3
    },
    {
      "token": "fast.",
      "start_offset": 27,
      "end_offset": 32,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 參數

`whitespace` 斷詞器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`max_token_length` | 選用 | 整數 | 設定所產生詞元的最大長度。若超過此長度，詞元會在 `max_token_length` 中設定的長度處被分割成多個詞元。預設為 `255`。

