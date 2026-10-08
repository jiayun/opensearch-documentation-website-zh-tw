---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Porter 詞幹"
parent: Token filters
nav_order: 340
---

# Porter 詞幹詞元篩選器

`porter_stem` 詞元篩選器會將單字還原為其基本（或稱 _詞幹_）形式，並移除單字的常見字尾，有助於依據字根比對相似的單字。例如，單字 `running` 會被詞幹化為 `run`。此詞元篩選器主要用於英文，並依據 [Porter 詞幹提取演算法](https://snowballstem.org/algorithms/porter/stemmer.html) 提供詞幹提取功能。


## 範例

下列範例請求會建立名為 `my_stem_index` 的新索引，並設定一個含有 `porter_stem` 篩選器的分析器：

```json
PUT /my_stem_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_porter_stem": {
          "type": "porter_stem"
        }
      },
      "analyzer": {
        "porter_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_porter_stem"
          ]
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
POST /my_stem_index/_analyze
{
  "text": "running runners ran",
  "analyzer": "porter_analyzer"
}
```
{% include copy-curl.html %}

回應中包含所產生的詞元：

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
    },
    {
      "token": "ran",
      "start_offset": 16,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```
