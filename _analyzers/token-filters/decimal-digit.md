---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "十進位數字"
parent: Token filters
nav_order: 80
---

# 十進位數字詞元篩選器

`decimal_digit` 詞元篩選器用於將各種文字系統中的十進位數字字元 (0--9) 正規化為對應的 ASCII 字元。若您希望在文字分析中統一處理所有數字，而不論其以何種文字系統書寫，此篩選器便十分實用。


## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `decimal_digit` 篩選器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_decimal_digit_filter": {
          "type": "decimal_digit"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["my_decimal_digit_filter"]
        }
      }
    }
  }
}

```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器所產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "123 ١٢٣ १२३"
}
```
{% include copy-curl.html %}

`text` 細分說明：

 - 「123」(ASCII 數字)
 - 「١٢٣」(阿拉伯-印度數字)
 - 「१२३」(天城文數字)

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "123",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<NUM>",
      "position": 0
    },
    {
      "token": "123",
      "start_offset": 4,
      "end_offset": 7,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "123",
      "start_offset": 8,
      "end_offset": 11,
      "type": "<NUM>",
      "position": 2
    }
  ]
}
```
