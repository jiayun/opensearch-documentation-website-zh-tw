---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Snowball
parent: Token filters
nav_order: 380
---

# Snowball 詞元篩選器

`snowball` 詞元篩選器是以 [Snowball](https://snowballstem.org/) 演算法為基礎的詞幹提取篩選器。它支援多種語言，且比 Porter 詞幹提取演算法更有效率、更準確。

## 參數

您可以使用 `language` 參數來設定 `snowball` 詞元篩選器，此參數接受下列值：

- `Arabic`
- `Armenian`
- `Basque`
- `Catalan`
- `Danish`
- `Dutch`
- `English`（預設）
- `Estonian`
- `Finnish`
- `French`
- `German`
- `German2` 
- `Hungarian`
- `Italian`
- `Irish`
- `Kp`
- `Lithuanian`
- `Lovins`
- `Norwegian`
- `Porter`
- `Portuguese`
- `Romanian`
- `Russian`
- `Spanish`
- `Swedish`
- `Turkish`

## 範例

下列範例請求會建立名為 `my-snowball-index` 的新索引，並設定一個使用 `snowball` 篩選器的分析器：

```json
PUT /my-snowball-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_snowball_filter": {
          "type": "snowball",
          "language": "English"
        }
      },
      "analyzer": {
        "my_snowball_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_snowball_filter"
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
GET /my-snowball-index/_analyze
{
  "analyzer": "my_snowball_analyzer",
  "text": "running runners"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "run",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "runner",
      "start_offset": 8,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```