---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Keyword 分析器"
parent: Analyzers
nav_order: 80
---

# Keyword 分析器

`keyword` 分析器完全不會對文字進行斷詞。它會將整個輸入視為單一詞元，而不會將其拆分為個別詞元。`keyword` 分析器通常用於包含電子郵件地址、URL 或產品 ID 的欄位，以及其他不適合進行斷詞的情況。

## 範例

使用下列命令建立名為 `my_keyword_index` 且使用 `keyword` 分析器的索引：

```json
PUT /my_keyword_index
{
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定自訂分析器

使用下列命令為索引設定與 `keyword` 分析器等效的自訂分析器：

```json
PUT /my_custom_keyword_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_keyword_analyzer": {
          "tokenizer": "keyword"
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
POST /my_custom_keyword_index/_analyze
{
  "analyzer": "my_keyword_analyzer",
  "text": "Just one token"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Just one token",
      "start_offset": 0,
      "end_offset": 14,
      "type": "word",
      "position": 0
    }
  ]
}
```
