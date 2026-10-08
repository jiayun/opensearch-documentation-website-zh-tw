---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Pattern 分析器"
parent: Analyzers
nav_order: 90
---

# Pattern 分析器

`pattern` 分析器可讓您定義自訂分析器，使用規則運算式 (regex) 將輸入文字分割為詞元。它也提供套用 regex 旗標、將詞元轉換為小寫，以及篩選停用詞的選項。

## 參數

`pattern` 分析器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`pattern` | 選用 | 字串 | 用於將輸入斷詞的 [Java 規則運算式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。預設為 `\W+`。
`flags` | 選用 | 字串 | 包含以管線符號分隔之 [Java regex 旗標](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#field.summary) 的字串，用於修改規則運算式的行為。
`lowercase` | 選用 | 布林值 | 是否將詞元轉換為小寫。預設為 `true`。
`stopwords` | 選用 | 字串或字串清單 | 指定預先定義停用詞清單 (例如 `_english_`) 的字串，或指定自訂停用詞清單的陣列。預設為 `_none_`。
`stopwords_path` | 選用 | 字串 | 包含停用詞清單之檔案的路徑 (絕對路徑或相對於 config 目錄的路徑)。


## 範例

使用下列命令建立名為 `my_pattern_index` 且具有 `pattern` 分析器的索引：

```json
PUT /my_pattern_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_pattern_analyzer": {
          "type": "pattern",
          "pattern": "\\W+",  
          "lowercase": true,                
          "stopwords": ["and", "is"]       
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_pattern_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器產生的詞元：

```json
POST /my_pattern_index/_analyze
{
  "analyzer": "my_pattern_analyzer",
  "text": "OpenSearch is fast and scalable"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "opensearch",
      "start_offset": 0,
      "end_offset": 10,
      "type": "word",
      "position": 0
    },
    {
      "token": "fast",
      "start_offset": 14,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "scalable",
      "start_offset": 23,
      "end_offset": 31,
      "type": "word",
      "position": 4
    }
  ]
}
```
