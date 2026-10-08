---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ICU 轉換"
parent: Token filters
nav_order: 175
---

# ICU 轉換詞元篩選器

`icu_transform` 詞元篩選器會對詞元套用 ICU 文字轉換，以執行音譯、大小寫對應、正規化及雙向文字處理等操作。此篩選器使用 [ICU Transform](https://unicode-org.github.io/icu/userguide/transforms/general/) 框架所定義的轉換規則。

常見使用案例包括：
- **音譯**：將文字從一種文字系統轉換為另一種文字系統（例如從西里爾字母轉換為拉丁字母）
- **文字系統轉換**：在不同書寫系統之間進行轉換
- **移除重音符號**：將基本字元與變音符號分離
- **自訂轉換**：套用使用者定義的轉換規則

## 安裝

`icu_transform` 詞元篩選器需要 `analysis-icu` 外掛程式。如需安裝說明，請參閱 [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)。

## 參數

下表列出 `icu_transform` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`id` | 字串 | 指定要套用哪一種轉換的 ICU 轉換 ID。可以是單一轉換 ID，也可以是以分號分隔多個轉換的複合 ID。預設為 `Null`（不進行轉換）。
`dir` | 字串 | 轉換的文字方向。有效值為 `forward`（預設，由左至右）和 `reverse`（由右至左）。預設為 `forward`。

## 轉換 ID

您可以使用標準 ICU 轉換 ID 來指定轉換。常見的轉換包括：

- `Any-Latin`：將任何文字系統的文字音譯為拉丁字元
- `Latin-Cyrillic`：將拉丁文字轉換為西里爾字母
- `NFD; [:Nonspacing Mark:] Remove; NFC`：分解字元、移除變音符號，然後重新組合
- `Lower`：將文字轉換為小寫
- `Upper`：將文字轉換為大寫
- `Hiragana-Katakana`：將平假名轉換為片假名

您可以使用分號分隔多個轉換，將它們串接在一起。

## 範例：音譯為拉丁字母

下列範例示範將多種文字系統音譯為拉丁字元：

```json
PUT /icu-transform-latin
{
  "settings": {
    "analysis": {
      "filter": {
        "latin_transform": {
          "type": "icu_transform",
          "id": "Any-Latin"
        }
      },
      "analyzer": {
        "latin_analyzer": {
          "tokenizer": "keyword",
          "filter": ["latin_transform"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用不同文字系統的文字測試分析器：

```json
POST /icu-transform-latin/_analyze
{
  "analyzer": "latin_analyzer",
  "text": "Москва"
}
```
{% include copy-curl.html %}

西里爾文字會被音譯為拉丁字母：

```json
{
  "tokens": [
    {
      "token": "Moskva",
      "start_offset": 0,
      "end_offset": 6,
      "type": "word",
      "position": 0
    }
  ]
}
```

使用日文文字進行測試：

```json
POST /icu-transform-latin/_analyze
{
  "analyzer": "latin_analyzer",
  "text": "東京"
}
```
{% include copy-curl.html %}

日文字元會被音譯：

```json
{
  "tokens": [
    {
      "token": "dōng jīng",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 範例：移除重音符號

下列範例會移除文字中的變音符號：

```json
PUT /icu-transform-no-accents
{
  "settings": {
    "analysis": {
      "filter": {
        "remove_accents": {
          "type": "icu_transform",
          "id": "NFD; [:Nonspacing Mark:] Remove; NFC"
        }
      },
      "analyzer": {
        "accent_removal_analyzer": {
          "tokenizer": "keyword",
          "filter": ["remove_accents"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

測試分析器：

```json
POST /icu-transform-no-accents/_analyze
{
  "analyzer": "accent_removal_analyzer",
  "text": "Ênrique Iglesias"
}
```
{% include copy-curl.html %}

重音符號已被移除：

```json
{
  "tokens": [
    {
      "token": "Enrique Iglesias",
      "start_offset": 0,
      "end_offset": 16,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 範例：文字系統之間的轉換

下列範例會將拉丁文字轉換為西里爾字母：

```json
PUT /icu-transform-cyrillic
{
  "settings": {
    "analysis": {
      "filter": {
        "to_cyrillic": {
          "type": "icu_transform",
          "id": "Latin-Cyrillic"
        }
      },
      "analyzer": {
        "cyrillic_analyzer": {
          "tokenizer": "keyword",
          "filter": ["to_cyrillic"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用拉丁文字進行測試：

```json
POST /icu-transform-cyrillic/_analyze
{
  "analyzer": "cyrillic_analyzer",
  "text": "Sankt Peterburg"
}
```
{% include copy-curl.html %}

文字會被轉換為西里爾字母：

```json
{
  "tokens": [
    {
      "token": "Санкт Петербург",
      "start_offset": 0,
      "end_offset": 15,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 複合轉換

您可以使用分號分隔轉換 ID，將多個轉換串接在一起。這些轉換會依由左至右的順序套用。

例如，複合 ID `"Any-Latin; NFD; [:Nonspacing Mark:] Remove; NFC"` 會執行下列步驟：
1. 音譯為拉丁字母
2. 套用標準分解 (NFD)
3. 移除非間距標記（重音符號）
4. 套用標準組合 (NFC)

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [ICU 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/icu-tokenizer/)
- [ICU 摺疊詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-folding/)
