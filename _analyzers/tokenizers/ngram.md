---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: N-gram
parent: Tokenizers
nav_order: 80
---

# N-gram 斷詞器

`ngram` 斷詞器會將文字分割成指定長度的重疊 n-gram（字元序列）。當您想要執行部分字詞比對或自動完成搜尋功能時，此斷詞器特別有用，因為它會產生原始輸入文字的子字串（字元 n-gram）。

## 使用範例

下列範例請求會建立一個名為 `my_index` 的新索引，並設定一個帶有 `ngram` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 3,
          "max_gram": 4,
          "token_chars": ["letter", "digit"]
        }
      },
      "analyzer": {
        "my_ngram_analyzer": {
          "type": "custom",
          "tokenizer": "my_ngram_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_ngram_analyzer",
  "text": "OpenSearch"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "Sea","start_offset": 0,"end_offset": 3,"type": "word","position": 0},
    {"token": "Sear","start_offset": 0,"end_offset": 4,"type": "word","position": 1},
    {"token": "ear","start_offset": 1,"end_offset": 4,"type": "word","position": 2},
    {"token": "earc","start_offset": 1,"end_offset": 5,"type": "word","position": 3},
    {"token": "arc","start_offset": 2,"end_offset": 5,"type": "word","position": 4},
    {"token": "arch","start_offset": 2,"end_offset": 6,"type": "word","position": 5},
    {"token": "rch","start_offset": 3,"end_offset": 6,"type": "word","position": 6}
  ]
}
```

## 參數

`ngram` 斷詞器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`min_gram` | 選用 | 整數 | n-gram 的最小長度。預設為 `1`。
`max_gram` | 選用 | 整數 | n-gram 的最大長度。預設為 `2`。
`token_chars` | 選用 | 字串陣列 | 要包含在斷詞中的字元類別。有效值為：<br>- `letter`<br>- `digit`<br>- `whitespace`<br>- `punctuation`<br>- `symbol`<br>- `custom`（您還必須指定 `custom_token_chars` 參數）<br>預設為空陣列（`[]`），會保留所有字元。
`custom_token_chars` | 選用 | 字串 | 要包含在詞元中的自訂字元。

### `min_gram` 與 `max_gram` 之間的最大差異

`min_gram` 與 `max_gram` 之間的最大差異是使用索引層級的 `index.max_ngram_diff` 設定來設定，預設為 `1`。

下列範例請求會建立一個具有自訂 `index.max_ngram_diff` 設定的索引：

```json
PUT /my-index
{
  "settings": {
    "index.max_ngram_diff": 2, 
    "analysis": {
      "tokenizer": {
        "my_ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 3,
          "max_gram": 5,
          "token_chars": ["letter", "digit"]
        }
      },
      "analyzer": {
        "my_ngram_analyzer": {
          "type": "custom",
          "tokenizer": "my_ngram_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
