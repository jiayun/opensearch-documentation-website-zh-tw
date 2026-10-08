---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Fingerprint 分析器"
parent: Analyzers
nav_order: 60
---

# Fingerprint 分析器

`fingerprint` 分析器會建立文字指紋。此分析器會對從輸入產生的詞彙（詞元）進行排序與去除重複，然後使用分隔符號將它們串接起來。由於對於包含相同字詞的相似輸入，無論字詞順序為何，它都會產生相同的輸出，因此常用於資料去除重複。

`fingerprint` 分析器由下列元件組成：

- Standard 斷詞器
- Lowercase 詞元篩選器
- ASCII folding 詞元篩選器
- Stop 詞元篩選器
- Fingerprint 詞元篩選器

## 參數

`fingerprint` 分析器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`separator` | 選用 | 字串 | 指定在詞彙經過斷詞、排序與去除重複後，用來串接詞彙的字元。預設為空格（` `）。
`max_output_size` | 選用 | 整數 | 定義輸出詞元的大小上限。若串接後的指紋超過此大小，將會被截斷。預設為 `255`。
`stopwords` | 選用 | 字串或字串清單 | 自訂或預先定義的停用詞清單。預設為 `_none_`。
`stopwords_path` | 選用 | 字串 | 包含停用詞清單之檔案的路徑（絕對路徑或相對於 config 目錄的路徑）。


## 範例

使用下列命令建立名為 `my_custom_fingerprint_index` 且具有 `fingerprint` 分析器的索引：

```json
PUT /my_custom_fingerprint_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_fingerprint_analyzer": {
          "type": "fingerprint",
          "separator": "-",
          "max_output_size": 50,
          "stopwords": ["to", "the", "over", "and"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_custom_fingerprint_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器所產生的詞元：

```json
POST /my_custom_fingerprint_index/_analyze
{
  "analyzer": "my_custom_fingerprint_analyzer",
  "text": "The slow turtle swims over to the dog"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "dog-slow-swims-turtle",
      "start_offset": 0,
      "end_offset": 37,
      "type": "fingerprint",
      "position": 0
    }
  ]
}
```

## 進一步自訂

若需要進一步自訂，您可以定義包含其他 `fingerprint` 分析器元件的分析器：

```json
PUT /custom_fingerprint_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_fingerprint": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "asciifolding",
            "fingerprint"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
