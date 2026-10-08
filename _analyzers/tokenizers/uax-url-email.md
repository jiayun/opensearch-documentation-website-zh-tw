---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "UAX URL 電子郵件"
parent: Tokenizers
nav_order: 150
---

# UAX URL 電子郵件斷詞器

除了處理一般文字，`uax_url_email` 斷詞器也專為處理 URL、電子郵件地址和網域名稱而設計。它以 Unicode 文字分段演算法（[UAX #29](https://www.unicode.org/reports/tr29/)）為基礎，可正確地將複雜文字切分為詞元，包括 URL 和電子郵件地址。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `uax_url_email` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "uax_url_email_tokenizer": {
          "type": "uax_url_email"
        }
      },
      "analyzer": {
        "my_uax_analyzer": {
          "type": "custom",
          "tokenizer": "uax_url_email_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_uax_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢視分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_uax_analyzer",
  "text": "Contact us at support@example.com or visit https://example.com for details."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "Contact","start_offset": 0,"end_offset": 7,"type": "<ALPHANUM>","position": 0},
    {"token": "us","start_offset": 8,"end_offset": 10,"type": "<ALPHANUM>","position": 1},
    {"token": "at","start_offset": 11,"end_offset": 13,"type": "<ALPHANUM>","position": 2},
    {"token": "support@example.com","start_offset": 14,"end_offset": 33,"type": "<EMAIL>","position": 3},
    {"token": "or","start_offset": 34,"end_offset": 36,"type": "<ALPHANUM>","position": 4},
    {"token": "visit","start_offset": 37,"end_offset": 42,"type": "<ALPHANUM>","position": 5},
    {"token": "https://example.com","start_offset": 43,"end_offset": 62,"type": "<URL>","position": 6},
    {"token": "for","start_offset": 63,"end_offset": 66,"type": "<ALPHANUM>","position": 7},
    {"token": "details","start_offset": 67,"end_offset": 74,"type": "<ALPHANUM>","position": 8}
  ]
}
```

## 參數

您可以使用下列參數設定 `uax_url_email` 斷詞器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`max_token_length` | 選用 | 整數 | 設定產生的詞元長度上限。如果超過此長度，詞元會依照 `max_token_length` 中設定的長度切分為多個詞元。預設為 `255`。

