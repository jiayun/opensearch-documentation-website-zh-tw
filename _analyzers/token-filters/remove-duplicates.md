---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除重複項目"
parent: Token filters
nav_order: 350
---

# 移除重複項目詞元篩選器

`remove_duplicates` 詞元篩選器用於移除在分析期間於相同位置產生的重複詞元。

## 範例

下列範例請求會建立一個含有 `keyword_repeat` 詞元篩選器的索引。此篩選器會在與每個詞元相同的位置加入該詞元的 `keyword` 版本，接著使用 `kstem` 建立該詞元的詞幹化版本：

```json
PUT /example-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "keyword_repeat",
            "kstem"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求分析字串 `Slower turtle`：

```json
GET /example-index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "Slower turtle"
}
```
{% include copy-curl.html %}

回應中在相同位置包含兩次詞元 `turtle`：

```json
{
  "tokens": [
    {
      "token": "slower",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "turtle",
      "start_offset": 7,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "turtle",
      "start_offset": 7,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

您可以在索引設定中加入 `remove_duplicates` 詞元篩選器來移除重複的詞元：

```json
PUT /index-remove-duplicate
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "keyword_repeat",
            "kstem",
            "remove_duplicates"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
GET /index-remove-duplicate/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "Slower turtle"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "slower",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "slow",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "turtle",
      "start_offset": 7,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```