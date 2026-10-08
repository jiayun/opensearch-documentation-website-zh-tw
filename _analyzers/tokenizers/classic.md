---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Classic
parent: Tokenizers
nav_order: 35

---

# Classic 斷詞器

`classic` 斷詞器會剖析文字，並套用英文文法規則將文字分割成詞元。此斷詞器包含特定邏輯，可處理下列模式：

- 首字母縮略字
- 電子郵件地址
- 網域名稱
- 特定類型的標點符號

此斷詞器最適合用於英文。對於其他語言，特別是文法結構不同的語言，可能無法產生最佳結果。
{: .note}

`classic` 斷詞器會依下列方式剖析文字：

- **標點符號**：在大多數標點符號處分割文字，並移除標點字元。後面未接空格的句點會視為詞元的一部分。
- **連字號**：在連字號處分割單字，但包含數字時除外。當詞元中包含數字時，該詞元不會被分割，而是視為產品編號處理。
- **電子郵件**：辨識電子郵件地址和主機名稱，並將其保留為單一詞元。

## 使用範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `classic` 斷詞器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_classic_analyzer": {
          "type": "custom",
          "tokenizer": "classic"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_classic_analyzer"
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
  "analyzer": "my_classic_analyzer",
  "text": "For product AB3423, visit X&Y at example.com, email info@example.com, or call the operator's phone number 1-800-555-1234. P.S. 你好."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "For",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "product",
      "start_offset": 4,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "AB3423",
      "start_offset": 12,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "visit",
      "start_offset": 20,
      "end_offset": 25,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "X&Y",
      "start_offset": 26,
      "end_offset": 29,
      "type": "<COMPANY>",
      "position": 4
    },
    {
      "token": "at",
      "start_offset": 30,
      "end_offset": 32,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "example.com",
      "start_offset": 33,
      "end_offset": 44,
      "type": "<HOST>",
      "position": 6
    },
    {
      "token": "email",
      "start_offset": 46,
      "end_offset": 51,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "info@example.com",
      "start_offset": 52,
      "end_offset": 68,
      "type": "<EMAIL>",
      "position": 8
    },
    {
      "token": "or",
      "start_offset": 70,
      "end_offset": 72,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "call",
      "start_offset": 73,
      "end_offset": 77,
      "type": "<ALPHANUM>",
      "position": 10
    },
    {
      "token": "the",
      "start_offset": 78,
      "end_offset": 81,
      "type": "<ALPHANUM>",
      "position": 11
    },
    {
      "token": "operator's",
      "start_offset": 82,
      "end_offset": 92,
      "type": "<APOSTROPHE>",
      "position": 12
    },
    {
      "token": "phone",
      "start_offset": 93,
      "end_offset": 98,
      "type": "<ALPHANUM>",
      "position": 13
    },
    {
      "token": "number",
      "start_offset": 99,
      "end_offset": 105,
      "type": "<ALPHANUM>",
      "position": 14
    },
    {
      "token": "1-800-555-1234",
      "start_offset": 106,
      "end_offset": 120,
      "type": "<NUM>",
      "position": 15
    },
    {
      "token": "P.S.",
      "start_offset": 122,
      "end_offset": 126,
      "type": "<ACRONYM>",
      "position": 16
    },
    {
      "token": "你",
      "start_offset": 127,
      "end_offset": 128,
      "type": "<CJ>",
      "position": 17
    },
    {
      "token": "好",
      "start_offset": 128,
      "end_offset": 129,
      "type": "<CJ>",
      "position": 18
    }
  ]
}
```

## 詞元類型

`classic` 斷詞器會產生下列詞元類型。

| 詞元類型    | 說明  | 
| :--- | :--- | 
| `<ALPHANUM>`  | 由字母、數字或兩者組合構成的英數字詞元。                     | 
| `<APOSTROPHE>`| 包含撇號的詞元，常用於所有格或縮寫形式（例如 `John's`）。   |
| `<ACRONYM>`   | 首字母縮略字或縮寫，通常以結尾的句點識別（例如 `P.S.` 或 `U.S.A.`）。     |
| `<COMPANY>`   | 代表公司名稱的詞元（例如 `X&Y`）。如果這些詞元未自動產生，您可能需要自訂組態或篩選器。  | 
| `<EMAIL>`     | 符合電子郵件地址的詞元，包含 `@` 符號和網域（例如 `support@widgets.co` 或 `info@example.com`）。 |
| `<HOST>`      | 符合網站或主機名稱的詞元，通常包含 `www.` 或 `.com` 之類的網域尾碼（例如 `www.example.com` 或 `example.org`）。  |
| `<NUM>`       | 僅包含數字或類似數字序列的詞元（例如 `1-800`、`12345` 或 `3.14`）。     |
| `<CJ>`        | 代表中文或日文字元的詞元。   |
| `<ACRONYM_DEP>` | 已淘汰的首字母縮略字處理方式（例如，在舊版中使用不同剖析規則的首字母縮略字）。很少使用，主要是為了與舊版斷詞器規則維持回溯相容性而存在。 | 
