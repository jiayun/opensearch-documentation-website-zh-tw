---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 數字"
parent: Token filters
nav_order: 232
---

# Kuromoji 數字詞元篩選器

`kuromoji_number` 詞元篩選器會將日文數字表示法正規化為標準阿拉伯數字。日文文字可使用漢字數字（一、二、三…）、全形數字（１、２、３…）或兩者混合來表示數字。此篩選器會將所有這類表示法轉換為對應的標準整數或小數。

此篩選器會進行如下的轉換：

- 一万二千三百四十五 轉換為 12345。
- ３，〇００ 轉換為 3000。
- 千円 轉換為 1000，單位 円 則保留為獨立的詞元。

對於包含以日文表示法書寫之價格、數量或其他數值的欄位，此篩選器適用於多面向搜尋、範圍查詢及排序。

## 安裝

`kuromoji_number` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

`kuromoji_number` 詞元篩選器沒有可設定的參數。

## 範例

下列範例會建立一個索引，其中包含使用 `kuromoji_number` 的自訂分析器：

```json
PUT /kuromoji-number-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "number_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_number"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含漢字數字表示法的文字（意思為「價格是 12,345 日圓」）測試分析器：

```json
POST /kuromoji-number-index/_analyze
{
  "analyzer": "number_analyzer",
  "text": "価格は一万二千三百四十五円です"
}
```
{% include copy-curl.html %}

回應顯示漢字數字已轉換為阿拉伯數字整數。請注意，`12345` 詞元的位移範圍為 3–12，因為來源漢字數字 `一万二千三百四十五` 的長度為 9 個字元：

```json
{
  "tokens": [
    {
      "token": "価格",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "は",
      "start_offset": 2,
      "end_offset": 3,
      "type": "word",
      "position": 1
    },
    {
      "token": "12345",
      "start_offset": 3,
      "end_offset": 12,
      "type": "word",
      "position": 2
    },
    {
      "token": "円",
      "start_offset": 12,
      "end_offset": 13,
      "type": "word",
      "position": 3
    },
    {
      "token": "です",
      "start_offset": 13,
      "end_offset": 15,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
