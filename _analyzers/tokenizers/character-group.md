---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字元群組"
parent: Tokenizers
nav_order: 20
has_children: false
has_toc: false
---

# 字元群組斷詞器

`char_group` 斷詞器使用特定字元作為分隔符號，將文字分割成詞元。它適用於需要簡單斷詞的情況，可作為以模式為基礎的斷詞器的較簡單替代方案，且不會增加額外的複雜性。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `char_group` 斷詞器的分析器。此斷詞器會依據空白字元、`-` 和 `:` 字元分割文字：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_char_group_tokenizer": {
          "type": "char_group",
          "tokenize_on_chars": [
            "whitespace",
            "-",
            ":"
          ]
        }
      },
      "analyzer": {
        "my_char_group_analyzer": {
          "type": "custom",
          "tokenizer": "my_char_group_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_char_group_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用此分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_char_group_analyzer",
  "text": "Fast-driving cars: they drive fast!"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Fast",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "driving",
      "start_offset": 5,
      "end_offset": 12,
      "type": "word",
      "position": 1
    },
    {
      "token": "cars",
      "start_offset": 13,
      "end_offset": 17,
      "type": "word",
      "position": 2
    },
    {
      "token": "they",
      "start_offset": 19,
      "end_offset": 23,
      "type": "word",
      "position": 3
    },
    {
      "token": "drive",
      "start_offset": 24,
      "end_offset": 29,
      "type": "word",
      "position": 4
    },
    {
      "token": "fast!",
      "start_offset": 30,
      "end_offset": 35,
      "type": "word",
      "position": 5
    }
  ]
}
```

## 參數

`char_group` 斷詞器可使用下列參數進行設定。

| **參數**        | **必要/選用** | **資料類型** | **說明** |
| :--- |  :--- |  :--- |  :--- |  
| `tokenize_on_chars`   | 必要              | 陣列         | 指定一組用來對文字進行斷詞的字元。您可以指定單一字元（例如 `-` 或 `@`），包括逸出字元（例如 `\n`），或字元類別，例如 `whitespace`、`letter`、`digit`、`punctuation` 或 `symbol`。 |
| `max_token_length`    | 選用              | 整數       | 設定所產生詞元的最大長度。若超過此長度，詞元會依 `max_token_length` 中設定的長度分割成多個詞元。預設值為 `255`。  |