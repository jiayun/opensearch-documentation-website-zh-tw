---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ASCII 摺疊"
parent: Token filters
nav_order: 20
---

# ASCII 摺疊詞元篩選器

`asciifolding` 詞元篩選器會將非 ASCII 字元轉換為最接近的 ASCII 對等字元。例如，*é* 會轉換為 *e*，*ü* 會轉換為 *u*，*ñ* 會轉換為 *n*。此過程稱為*音譯 (transliteration)*。


`asciifolding` 詞元篩選器提供多項優點：

  - **提升搜尋彈性**：使用者在輸入查詢時，經常會省略重音符號或特殊字元。`asciifolding` 詞元篩選器可確保此類查詢仍能傳回相關結果。
  - **正規化**：確保帶有重音符號的字元一律轉換為其 ASCII 對等字元，藉此將編製索引的過程標準化。
  - **國際化**：特別適用於包含多種語言和字元集的應用程式。

雖然 `asciifolding` 詞元篩選器可以簡化搜尋，但也可能導致特定資訊遺失，尤其是當資料集中帶重音符號與不帶重音符號字元之間的區別很重要時。
{: .warning}

## 參數

您可以使用 `preserve_original` 參數來設定 `asciifolding` 詞元篩選器。將此參數設為 `true` 時，詞元串流中會同時保留原始詞元及其經過 ASCII 摺疊的版本。當您希望在搜尋查詢中同時比對詞彙的原始版本（帶重音符號）與正規化版本（不帶重音符號）時，這項功能特別實用。預設值為 `false`。

## 範例

下列範例請求會建立名為 `example_index` 的新索引，並定義一個使用 `asciifolding` 篩選器且 `preserve_original` 參數設為 `true` 的分析器：

```json
PUT /example_index
{
  "settings": {
    "analysis": {
      "filter": {
        "custom_ascii_folding": {
          "type": "asciifolding",
          "preserve_original": true
        }
      },
      "analyzer": {
        "custom_ascii_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "custom_ascii_folding"
          ]
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
POST /example_index/_analyze
{
  "analyzer": "custom_ascii_analyzer",
  "text": "Résumé café naïve coördinate"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "resume",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "résumé",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "cafe",
      "start_offset": 7,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "café",
      "start_offset": 7,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "naive",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "naïve",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "coordinate",
      "start_offset": 18,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "coördinate",
      "start_offset": 18,
      "end_offset": 28,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
```


