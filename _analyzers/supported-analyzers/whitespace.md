---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "空白字元分析器"
parent: Analyzers
nav_order: 120
---

# 空白字元分析器

`whitespace` 分析器僅根據空白字元（例如空格與定位字元）將文字拆分為詞元。它不會套用任何轉換，例如轉換為小寫或移除停用詞，因此會保留文字的原始大小寫，且標點符號會包含在詞元中。

## 範例

使用下列命令建立名為 `my_whitespace_index` 且具有 `whitespace` 分析器的索引：

```json
PUT /my_whitespace_index
{
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "whitespace"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定自訂分析器

使用下列命令為索引設定自訂分析器，該分析器等同於加上 `lowercase` 字元篩選器的 `whitespace` 分析器：

```json
PUT /my_custom_whitespace_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_whitespace_analyzer": {
          "type": "custom",
          "tokenizer": "whitespace",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_custom_whitespace_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
POST /my_custom_whitespace_index/_analyze
{
  "analyzer": "my_custom_whitespace_analyzer",
  "text": "The SLOW turtle swims away! 123"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "the","start_offset": 0,"end_offset": 3,"type": "word","position": 0},
    {"token": "slow","start_offset": 4,"end_offset": 8,"type": "word","position": 1},
    {"token": "turtle","start_offset": 9,"end_offset": 15,"type": "word","position": 2},
    {"token": "swims","start_offset": 16,"end_offset": 21,"type": "word","position": 3},
    {"token": "away!","start_offset": 22,"end_offset": 27,"type": "word","position": 4},
    {"token": "123","start_offset": 28,"end_offset": 31,"type": "word","position": 5}
  ]
}
```
