---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Apostrophe
parent: Token filters
nav_order: 10
---

# Apostrophe 詞元篩選器

`apostrophe` 詞元篩選器的主要功能是移除所有格撇號及其後的所有內容。在分析大量使用撇號的語言文字時，這項功能非常實用，例如土耳其語。在土耳其語中，撇號用於分隔字根與字尾，包括所有格字尾、格標記及其他文法詞尾。


## 範例

下列範例請求會建立名為 `custom_text_index` 的新索引，其中包含在 `settings` 中設定並在 `mappings` 中使用的自訂分析器：

```json
PUT /custom_text_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "apostrophe"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "custom_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用所建立的分析器產生的詞元：

```json
POST /custom_text_index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "John's car is faster than Peter's bike"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "john",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "car",
      "start_offset": 7,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "is",
      "start_offset": 11,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "faster",
      "start_offset": 14,
      "end_offset": 20,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "than",
      "start_offset": 21,
      "end_offset": 25,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "peter",
      "start_offset": 26,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "bike",
      "start_offset": 34,
      "end_offset": 38,
      "type": "<ALPHANUM>",
      "position": 6
    }
  ]
}
```

內建的 `apostrophe` 詞元篩選器不適用於法語等在字首使用撇號的語言。例如，`"C'est l'amour de l'école"` 會產生四個詞元：「C」、「l」、「de」和「l」。
{: .note}
