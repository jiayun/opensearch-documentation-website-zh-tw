---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CJK 寬度"
parent: Token filters
nav_order: 40
---

# CJK 寬度詞元篩選器

`cjk_width` 詞元篩選器會正規化中文、日文和韓文 (CJK) 詞元，將全形 ASCII 字元轉換為對應的標準 (半形) ASCII 字元，並將半形片假名字元轉換為對應的全形字元。

### 轉換全形 ASCII 字元

在 CJK 文字中，ASCII 字元 (例如字母和數字) 可能以全形形式出現，佔用兩個半形字元的空間。全形 ASCII 字元通常用於東亞排版，以便與 CJK 字元的寬度對齊。然而，為了編製索引和搜尋，這些全形字元需要正規化為對應的標準 (半形) ASCII 字元。

下列範例說明 ASCII 字元正規化：

```
        Full-Width:              ＡＢＣＤＥ １２３４５
        Normalized (half-width): ABCDE 12345
```

### 轉換半形片假名字元

`cjk_width` 詞元篩選器會將半形片假名字元轉換為對應的全形字元，也就是日文文字中使用的標準形式。如下列範例所示，此正規化對於文字處理和搜尋的一致性非常重要：


```
        Half-Width katakana:               ｶﾀｶﾅ
        Normalized (full-width) katakana:  カタカナ
```

## 範例

下列範例請求會建立名為 `cjk_width_example_index` 的新索引，並定義一個使用 `cjk_width` 篩選器的分析器：

```json
PUT /cjk_width_example_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "cjk_width_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["cjk_width"]
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
POST /cjk_width_example_index/_analyze
{
  "analyzer": "cjk_width_analyzer",
  "text": "Ｔｏｋｙｏ 2024 ｶﾀｶﾅ"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Tokyo",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "2024",
      "start_offset": 6,
      "end_offset": 10,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "カタカナ",
      "start_offset": 11,
      "end_offset": 15,
      "type": "<KATAKANA>",
      "position": 2
    }
  ]
}
```
