---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Stop 分析器"
parent: Analyzers
nav_order: 110
---

# Stop 分析器

`stop` 分析器會移除預先定義的停用詞清單。此分析器由 `lowercase` 斷詞器和 `stop` 詞元篩選器組成。

## 參數

您可以使用下列參數設定 `stop` 分析器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`stopwords` | 選用 | 字串或字串清單 | 指定預先定義之停用詞清單的字串 (例如 `_english_`)，或指定自訂停用詞清單的陣列。預設為 `_english_`。
`stopwords_path` | 選用 | 字串 | 包含停用詞清單之檔案的路徑 (絕對路徑或相對於 config 目錄的路徑)。

## 範例

使用下列命令建立名為 `my_stop_index` 且使用 `stop` 分析器的索引：

```json
PUT /my_stop_index
{
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "stop"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定自訂分析器

使用下列命令為索引設定與 `stop` 分析器等效的自訂分析器：

```json
PUT /my_custom_stop_analyzer_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_stop_analyzer": {
          "tokenizer": "lowercase",
          "filter": [
            "stop"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_field": {
        "type": "text",
        "analyzer": "my_custom_stop_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用該分析器所產生的詞元：

```json
POST /my_custom_stop_analyzer_index/_analyze
{
  "analyzer": "my_custom_stop_analyzer",
  "text": "The large turtle is green and brown"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "large",
      "start_offset": 4,
      "end_offset": 9,
      "type": "word",
      "position": 1
    },
    {
      "token": "turtle",
      "start_offset": 10,
      "end_offset": 16,
      "type": "word",
      "position": 2
    },
    {
      "token": "green",
      "start_offset": 20,
      "end_offset": 25,
      "type": "word",
      "position": 4
    },
    {
      "token": "brown",
      "start_offset": 30,
      "end_offset": 35,
      "type": "word",
      "position": 6
    }
  ]
}
```

# 指定停用詞

下列範例請求會指定自訂停用詞清單：

```json
PUT /my_new_custom_stop_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_stop_analyzer": {
          "type": "stop",                     
          "stopwords": ["is", "and", "was"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "my_custom_stop_analyzer" 
      }
    }
  }
}
```
{% include copy-curl.html %}

下列範例請求會指定包含停用詞之檔案的路徑：

```json
PUT /my_new_custom_stop_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_stop_analyzer": {
          "type": "stop",                     
          "stopwords_path": "stopwords.txt"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "my_custom_stop_analyzer" 
      }
    }
  }
}
```
{% include copy-curl.html %}

在此範例中，檔案位於 config 目錄中。您也可以指定檔案的完整路徑。