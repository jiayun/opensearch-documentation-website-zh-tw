---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Standard
parent: Tokenizers
nav_order: 130
---

# Standard 斷詞器

`standard` 斷詞器是 OpenSearch 的預設斷詞器。它採用基於文法的方法，依據單字邊界將文字切分為詞元，可辨識字母、數字及其他字元（例如標點符號）。由於它使用 Unicode 文字分段規則（[UAX#29](https://unicode.org/reports/tr29/)）將文字切分為詞元，因此用途廣泛，適用於多種語言。

## 斷詞規則

`standard` 斷詞器遵循 [Unicode Standard Annex #29: Unicode Text Segmentation](https://unicode.org/reports/tr29/) 中定義的單字邊界規則。下表摘要說明這些規則如何套用於常見輸入。

輸入 | 規則 | 詞元
:--- | :--- | :---
`fast, and scalable.` | 空白字元與大多數標點符號（例如逗號、連字號、斜線、`+`、`#`、`%` 和 `@`）會切分文字並被移除。 | `fast`, `and`, `scalable`
`can't`, `O'Neil` | 兩個字母之間的單引號不會切分單字。 | `can't`, `O'Neil`
`end. Next` | 句號後接空格會切分文字。 | `end`, `Next`
`hello.world`, `U.S.A.` | 兩個字母之間的句號不會切分單字。結尾的句號會被移除。 | `hello.world`, `U.S.A`
`3.5`, `1,000`, `v1.2.3` | 兩個數字之間的句號或逗號不會切分數字。 | `3.5`, `1,000`, `v1.2.3`
`snake_case` | 底線不會切分單字。 | `snake_case`
`state-of-the-art` | 連字號會切分單字。 | `state`, `of`, `the`, `art`
`admin@example.com` | 電子郵件地址會在 `@` 符號處切分。 | `admin`, `example.com`
`https://opensearch.org/docs` | URL 會在冒號與斜線處切分。 | `https`, `opensearch.org`, `docs`
`東京`, `こんにちは` | 每個表意文字與平假名字元都會成為獨立的詞元。 | `東`, `京`, `こ`, `ん`, `に`, `ち`, `は`

若要將電子郵件地址與 URL 保留為單一詞元，請使用 [`uax_url_email` 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/uax-url-email/)。長度超過 `max_token_length` 的詞元會在該長度處切分。如需更多資訊，請參閱 [參數](#parameters)。

## 範例用法

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `standard` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_standard_analyzer": {
          "type": "standard"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_standard_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用該分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_standard_analyzer",
  "text": "OpenSearch is powerful, fast, and scalable."
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
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "is",
      "start_offset": 11,
      "end_offset": 13,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "powerful",
      "start_offset": 14,
      "end_offset": 22,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "fast",
      "start_offset": 24,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "and",
      "start_offset": 30,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "scalable",
      "start_offset": 34,
      "end_offset": 42,
      "type": "<ALPHANUM>",
      "position": 5
    }
  ]
}
```

## 參數

`standard` 斷詞器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`max_token_length` | 選用 | 整數 | 設定所產生詞元的最大長度。若超過此長度，詞元會在 `max_token_length` 中設定的長度處切分為多個詞元。預設值為 `255`。

