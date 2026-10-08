---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "路徑階層"
parent: Tokenizers
nav_order: 90
---

# 路徑階層斷詞器

`path_hierarchy` 斷詞器會將類似檔案系統的路徑（或類似的階層式結構）在每個階層層級拆分為詞元，藉此進行斷詞。當您處理階層式資料（例如檔案路徑、URL 或任何其他以分隔符號分隔的路徑）時，此斷詞器特別實用。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `path_hierarchy` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_path_tokenizer": {
          "type": "path_hierarchy"
        }
      },
      "analyzer": {
        "my_path_analyzer": {
          "type": "custom",
          "tokenizer": "my_path_tokenizer"
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
POST /my_index/_analyze
{
  "analyzer": "my_path_analyzer",
  "text": "/users/john/documents/report.txt"
}
```
{% include copy-curl.html %}

回應中包含所產生的詞元：

```json
{
  "tokens": [
    {
      "token": "/users",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0
    },
    {
      "token": "/users/john",
      "start_offset": 0,
      "end_offset": 11,
      "type": "word",
      "position": 0
    },
    {
      "token": "/users/john/documents",
      "start_offset": 0,
      "end_offset": 21,
      "type": "word",
      "position": 0
    },
    {
      "token": "/users/john/documents/report.txt",
      "start_offset": 0,
      "end_offset": 32,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 參數

`path_hierarchy` 斷詞器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`delimiter` | 選用 | 字串 | 指定用來分隔路徑元件的字元。預設為 `/`。
`replacement` | 選用 | 字串 | 設定用來取代詞元中分隔符號的字元。預設為 `/`。
`buffer_size` | 選用 | 整數 | 指定緩衝區大小。預設為 `1024`。
`reverse` | 選用 | 布林值 | 若為 `true`，則以反向順序產生詞元。預設為 `false`。
`skip` | 選用 | 整數 | 指定斷詞時要略過的初始詞元（層級）數目。預設為 `0`。

## 使用 delimiter 與 replacement 參數的範例

下列範例請求會設定自訂的 `delimiter` 與 `replacement` 參數：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_path_tokenizer": {
          "type": "path_hierarchy",
          "delimiter": "\\",
          "replacement": "\\"
        }
      },
      "analyzer": {
        "my_path_analyzer": {
          "type": "custom",
          "tokenizer": "my_path_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}


使用下列請求來檢查使用該分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_path_analyzer",
  "text": "C:\\users\\john\\documents\\report.txt"
}
```
{% include copy-curl.html %}

回應中包含所產生的詞元：

```json
{
  "tokens": [
    {
      "token": "C:",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": """C:\users""",
      "start_offset": 0,
      "end_offset": 8,
      "type": "word",
      "position": 0
    },
    {
      "token": """C:\users\john""",
      "start_offset": 0,
      "end_offset": 13,
      "type": "word",
      "position": 0
    },
    {
      "token": """C:\users\john\documents""",
      "start_offset": 0,
      "end_offset": 23,
      "type": "word",
      "position": 0
    },
    {
      "token": """C:\users\john\documents\report.txt""",
      "start_offset": 0,
      "end_offset": 34,
      "type": "word",
      "position": 0
    }
  ]
}
```