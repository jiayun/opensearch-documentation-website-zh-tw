---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "保留類型"
parent: Token filters
nav_order: 180
---

# 保留類型詞元篩選器

`keep_types` 詞元篩選器是一種用於文字分析的詞元篩選器，可控制要保留或捨棄哪些詞元類型。不同的斷詞器會產生不同的詞元類型，例如 `<HOST>`、`<NUM>` 或 `<ALPHANUM>`。

`keyword`、`simple_pattern` 和 `simple_pattern_split` 斷詞器不支援 `keep_types` 詞元篩選器，因為這些斷詞器不支援詞元類型屬性。
{: .note}

## 參數

`keep_types` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`types` | 必要 | 字串清單 | 要保留或捨棄的詞元類型清單（由 `mode` 決定）。
`mode`| 選用 | 字串 | 是否要 `include` 或 `exclude` `types` 中指定的詞元類型。預設為 `include`。
 

## 範例

下列範例請求會建立名為 `test_index` 的新索引，並設定一個含有 `keep_types` 篩選器的分析器：

```json
PUT /test_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "keep_types_filter"]
        }
      },
      "filter": {
        "keep_types_filter": {
          "type": "keep_types",
          "types": ["<ALPHANUM>"]
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
GET /test_index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "Hello 2 world! This is an example."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "hello",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "world",
      "start_offset": 8,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "this",
      "start_offset": 15,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "is",
      "start_offset": 20,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "an",
      "start_offset": 23,
      "end_offset": 25,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "example",
      "start_offset": 26,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 6
    }
  ]
}
```
