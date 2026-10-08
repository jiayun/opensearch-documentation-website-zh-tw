---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關鍵字重複"
parent: Token filters
nav_order: 210
---

# 關鍵字重複詞元篩選器

`keyword_repeat` 詞元篩選器會將詞元的關鍵字版本輸出至詞元串流中。當您希望在進一步的詞元轉換（例如詞幹提取或同義詞擴充）之後，同時保留原始詞元及其修改後的版本時，通常會使用此篩選器。重複的詞元可讓未經變更的原始詞元版本，與修改後的版本一同保留在最終分析結果中。

`keyword_repeat` 詞元篩選器應放置在詞幹提取篩選器之前。詞幹提取並不會套用至每個詞元，因此在詞幹提取之後，同一位置可能會出現重複的詞元。若要移除重複的詞元，請在詞幹提取器之後使用 `remove_duplicates` 詞元篩選器。
{: .note} 


## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定含有 `keyword_repeat` 篩選器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_kstem": {
          "type": "kstem"
        },
        "my_lowercase": {
          "type": "lowercase"
        }
      },
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "my_lowercase",
            "keyword_repeat",
            "my_kstem"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "Stopped quickly"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "stopped",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "stop",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "quickly",
      "start_offset": 8,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "quick",
      "start_offset": 8,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

您可以在 `_analyze` 查詢中加入下列參數，以進一步檢查 `keyword_repeat` 詞元篩選器的影響：

```json
POST /my_index/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "Stopped quickly",
  "explain": true,
  "attributes": "keyword"
}
```
{% include copy-curl.html %}

回應中包含詳細資訊，例如斷詞、篩選，以及特定詞元篩選器的套用情形：

```json
{
  "detail": {
    "custom_analyzer": true,
    "charfilters": [],
    "tokenizer": {
      "name": "standard",
      "tokens": [
        {"token": "OpenSearch","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
        {"token": "helped","start_offset": 11,"end_offset": 17,"type": "<ALPHANUM>","position": 1},
        {"token": "many","start_offset": 18,"end_offset": 22,"type": "<ALPHANUM>","position": 2},
        {"token": "employers","start_offset": 23,"end_offset": 32,"type": "<ALPHANUM>","position": 3}
      ]
    },
    "tokenfilters": [
      {
        "name": "lowercase",
        "tokens": [
          {"token": "opensearch","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0},
          {"token": "helped","start_offset": 11,"end_offset": 17,"type": "<ALPHANUM>","position": 1},
          {"token": "many","start_offset": 18,"end_offset": 22,"type": "<ALPHANUM>","position": 2},
          {"token": "employers","start_offset": 23,"end_offset": 32,"type": "<ALPHANUM>","position": 3}
        ]
      },
      {
        "name": "keyword_marker_filter",
        "tokens": [
          {"token": "opensearch","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0,"keyword": true},
          {"token": "helped","start_offset": 11,"end_offset": 17,"type": "<ALPHANUM>","position": 1,"keyword": false},
          {"token": "many","start_offset": 18,"end_offset": 22,"type": "<ALPHANUM>","position": 2,"keyword": false},
          {"token": "employers","start_offset": 23,"end_offset": 32,"type": "<ALPHANUM>","position": 3,"keyword": false}
        ]
      },
      {
        "name": "kstem_filter",
        "tokens": [
          {"token": "opensearch","start_offset": 0,"end_offset": 10,"type": "<ALPHANUM>","position": 0,"keyword": true},
          {"token": "help","start_offset": 11,"end_offset": 17,"type": "<ALPHANUM>","position": 1,"keyword": false},
          {"token": "many","start_offset": 18,"end_offset": 22,"type": "<ALPHANUM>","position": 2,"keyword": false},
          {"token": "employer","start_offset": 23,"end_offset": 32,"type": "<ALPHANUM>","position": 3,"keyword": false}
        ]
      }
    ]
  }
}
```